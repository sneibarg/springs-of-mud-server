from __future__ import annotations
from api.ItemApi import ItemApi

from item.ItemFactory import ItemFactory

import inspect
import random
from dataclasses import replace

from typing import Any

from injector import inject

from api.InterpApi import InterpApi
from api.GameApi import GameApi
from item.EffectHandler import EffectHandler
from item.Item import Item
from item.ItemOwnership import ItemOwnership
from util.DisplayUtil import DisplayUtil
from util.GenericUtil import GenericUtil
from util.FightUtil import FightUtil
from item.Effect import Effect
from util.EffectUtil import EffectUtil
from util.ElementalExposure import ElementalExposure
from api.CharacterApi import CharacterApi
from util.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory
from skill.SpellContext import SpellContext
from skill.SpellSpeech import SpellSpeech
from skill.Ability import Ability
from skill.AbilityResolver import AbilityResolver


class _SafeFormatTokens(dict):
    def __missing__(self, key):
        return ""


class SpellApi:

    @inject
    def __init__(self, effect_handler: EffectHandler, interp_api: InterpApi,
                 elemental_exposure: ElementalExposure = None):
        self.__name__ = "SpellApi"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.effect_handler = effect_handler
        self.interp_api = interp_api
        self.elemental_exposure = elemental_exposure

    @staticmethod
    def casting_proficiency(actor, spell) -> int:
        if CharacterApi.is_npc(actor):
            rating = 40 + 2 * int(actor.level)
        elif int(actor.level) < FightUtil.level_for_class(spell, actor):
            rating = 0
        else:
            rating = actor.learned_entry_level(actor.get_learned(spell.name, collection_name="spells"))
        status = actor.status_flags
        if status.pulse_daze > 0:
            rating //= 2
        if not CharacterApi.is_npc(actor) and status.drunk > 10:
            rating = 9 * rating // 10
        return max(0, min(100, rating))

    def cast(self, ctx: SpellContext, mana_cost: int) -> bool:
        """Resolve an approved normal cast attempt; item/NPC script execution stays separate."""
        self.queue_cast_announcement(ctx)
        ctx.actor.status_flags.pulse_wait = max(ctx.actor.status_flags.pulse_wait, int(ctx.spell.beats))
        if random.randint(1, 100) > self.casting_proficiency(ctx.actor, ctx.spell):
            ctx.queue_payload(self.interp_api.render_message_key(ctx.command_context, "skill_failure"))
            Ability.check_improve(ctx.actor, ctx.spell.id, False, 1)
            ctx.actor.mana -= mana_cost // 2
            return False
        ctx.actor.mana -= mana_cost
        if ctx.cast_level is None:
            full_level = CharacterApi.is_npc(ctx.actor) or ctx.actor.character_class.mana_gain
            ctx.cast_level = int(ctx.actor.level) if full_level else 3 * int(ctx.actor.level) // 4
        self.execute_lambdas(ctx)
        Ability.check_improve(ctx.actor, ctx.spell.id, True, 1)
        return True

    def execute_lambdas(self, ctx: SpellContext, steps: list[str] | None = None) -> bool:
        lambdas = list(getattr(ctx.spell, "lambdas", []) or []) if steps is None else list(steps)
        if not lambdas:
            return self.default_spell(ctx) if steps is None else bool(ctx.performed)

        for lambda_str in lambdas:
            try:
                func = eval(lambda_str)
                if not callable(func):
                    continue
                result = func(ctx)
                if inspect.isawaitable(result):
                    raise TypeError(f"Async spell lambdas are not supported: {lambda_str}")
            except Exception as exc:
                self.logger.error(
                    f"Spell lambda failed for {getattr(ctx.spell, 'name', '')}: {lambda_str} | {exc}",
                    exc_info=True,
                )
                return ctx.fail("Your spell fizzles and dies.\r\n")
            if ctx.done:
                break
        return bool(ctx.performed)

    def default_spell(self, ctx: SpellContext):
        if ctx.target is not None:
            return self.apply_affect_data(ctx)
        return ctx.mark_performed()

    def queue_cast_announcement(self, ctx: SpellContext):
        spell_label = str(getattr(ctx.spell, "name", "spell") or "spell")
        if spell_label.strip().lower() == "ventriloquate":
            return False
        victim = ctx.victim
        actor_name = DisplayUtil.entity_name(ctx.actor, is_npc=CharacterApi.is_npc)
        self.send(ctx, to_char=f"You cast {spell_label}" + (f" on {DisplayUtil.entity_name(victim, is_npc=CharacterApi.is_npc)}" if victim is not None and victim is not ctx.actor else "") + ".\r\n")

        visible_spell = SpellSpeech.utterance(spell_label, actor_name, translated=False)
        obscure_spell = SpellSpeech.utterance(spell_label, actor_name, translated=True)

        if victim is not None and victim is not ctx.actor and not CharacterApi.is_npc(victim):
            self.send(
                ctx,
                to_victim=visible_spell if self._same_class(ctx.actor, victim) else obscure_spell,
                victim=victim,
            )

        same_class_targets: list[Any] = []
        other_targets: list[Any] = []
        exclude_ids = {str(getattr(ctx.actor, "id", "") or "")}
        if victim is not None:
            exclude_ids.add(str(getattr(victim, "id", "") or ""))
        for player in self._room_players(ctx.room, exclude_ids=exclude_ids):
            if self._same_class(ctx.actor, player):
                same_class_targets.append(player)
            else:
                other_targets.append(player)

        if same_class_targets:
            ctx.queue_payload({"to_room": visible_spell, "targets": same_class_targets})
        if other_targets:
            ctx.queue_payload({"to_room": obscure_spell, "targets": other_targets})
        return True

    def check_offensive_cast(self, ctx: SpellContext):
        target_type = str(getattr(ctx.spell, "target", "") or "").upper()
        if target_type not in ("CHAR_OFFENSIVE", "OBJ_CHAR_OFF") or CharacterApi.is_npc(ctx.actor):
            return
        victim = ctx.victim
        if victim is not None and victim is not ctx.actor:
            notice = self._fight_handler(ctx).check_killer(ctx.actor, victim)
            if notice:
                ctx.queue_payload(notice)

    def start_offensive_combat(self, ctx: SpellContext):
        """Let a still-present, idle offensive target retaliate after a cast attempt."""
        victim = ctx.victim
        target_type = str(getattr(ctx.spell, "target", "") or "").upper()
        if (victim is None or victim is ctx.actor or target_type not in ("CHAR_OFFENSIVE", "OBJ_CHAR_OFF")
                or getattr(victim, "master", None) is ctx.actor or getattr(victim, "fighting", None) is not None):
            return
        room = ctx.room
        if room is None or (getattr(ctx.actor, "room_id", "") and str(ctx.actor.room_id) != str(room.id)):
            room = self._find_room_for_entity(ctx.actor)
        if room is None or not any(entity is victim for entity in self._room_entities(room)):
            return
        fight = self._fight_handler(ctx)
        notice = fight.check_killer(victim, ctx.actor)
        result = fight.multi_hit(victim, ctx.actor, dt="TYPE_UNDEFINED")
        attack = fight.build_round_payload(victim, ctx.actor, room, result)
        ctx.queue_payload({"actor": victim, "payloads": [*([notice] if notice else []), attack]})

    def send(self, ctx: SpellContext, to_char: str = "", to_room: str = "",to_victim: str = "", victim: Any = None,
             include_actor_in_room: bool = False, include_victim_in_room: bool = False, prepend: bool = False) -> bool:
        target = ctx.resolve(victim) if victim is not None else ctx.victim
        payload: dict[str, Any] = {}
        if to_char and ctx.is_player_source:
            payload["to_char"] = to_char
        if to_victim and target is not None and not CharacterApi.is_npc(target):
            payload["victim"] = target
            payload["to_victim"] = to_victim
        if to_room:
            exclude = set()
            if not include_actor_in_room:
                exclude.add(str(getattr(ctx.actor, "id", "") or ""))
            if target is not None and not include_victim_in_room:
                exclude.add(str(getattr(target, "id", "") or ""))
            targets = self._room_players(ctx.room, exclude_ids=exclude)
            if targets:
                payload["to_room"] = to_room
                payload["targets"] = targets
        if payload:
            if prepend:
                ctx.payloads.insert(0, payload)
            else:
                ctx.queue_payload(payload)
        return True

    def stop_if_affected(self, ctx: SpellContext, effect_name: str, message: str = "", target_message: str = "", target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.target
        if victim is None or not self._effect_active(victim, effect_name):
            return False
        message_ref = target_message if victim is not ctx.actor and target_message else message
        if message_ref:
            ctx.fail(self._render_spell_to_char(ctx, message_ref))
        else:
            ctx.stop()
        return True

    def _render_spell_to_char(self, ctx: SpellContext, message_ref: str) -> str:
        text = str(message_ref or "")
        tokens = ctx.payload_tokens() if callable(getattr(ctx, "payload_tokens", None)) else {}
        message_key = next(iter(GenericUtil.camel_to_snake_case({text: ""}).keys()), text)
        rendered = self.interp_api.render_message_key(ctx, message_key, channel="to_char", **tokens)
        if isinstance(rendered, dict) and rendered.get("to_char"):
            return str(rendered["to_char"])
        spell = getattr(ctx, "spell", None)
        if spell is not None and callable(getattr(spell, "message", None)):
            direct = spell.message("to_char", message_key, **tokens)
            if direct:
                return direct
        try:
            return text.format_map(_SafeFormatTokens(tokens))
        except (KeyError, ValueError):
            return text

    def saves_spell(self, ctx: SpellContext, dam_type: str = "DAM_OTHER", level_adjust: int = 0,
                    target: Any = None) -> bool:
        """Resolve a typed save with the same immunity rules as combat damage."""
        victim = ctx.resolve(target) if target is not None else ctx.victim
        return victim is not None and EffectUtil.saves_spell(
            ctx.level + int(level_adjust), victim, dam_type,
            immunity=self._fight_handler(ctx)._check_immunity,
        )

    def stop_if_saved(self, ctx: SpellContext, level_adjust: int = 0, target: Any = None, message: str = "",
                      dam_type: str = "DAM_OTHER"):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None or not self.saves_spell(ctx, dam_type, level_adjust, target=victim):
            return False
        if message:
            ctx.fail(message)
        else:
            ctx.stop()
        return True

    def apply_affect_data(self, ctx: SpellContext, target: Any = None, *, join: bool = False,
                         modifier_expr: str | None = None, duration_expr: str | None = None):
        victim = ctx.resolve(target) if target is not None else ctx.target
        if victim is None:
            return False
        options = {}
        if getattr(ctx, "cast_level", None) is not None:
            options["caster_level"] = ctx.level
        if join:
            options["join"] = True
        spell = ctx.spell
        if modifier_expr is not None or duration_expr is not None:
            effects = []
            for template in spell.affect_data:
                effect = self.effect_handler.effect_from_spell_affect(spell, template, ctx.level)
                if modifier_expr is not None:
                    effect.modifier = self.eval_int(ctx, modifier_expr, victim=victim)
                if duration_expr is not None:
                    effect.duration = self.eval_int(ctx, duration_expr, victim=victim)
                effects.append(effect)
            spell = replace(spell, affect_data=effects)
        self.effect_handler.apply_spell_effects(ctx.actor, victim, spell, **options)
        self._queue_apply_affect_messages(ctx, victim)
        return ctx.mark_performed()

    def _queue_apply_affect_messages(self, ctx: SpellContext, victim: Any) -> None:
        payload = self.interp_api.evaluate_guards_only(ctx, getattr(ctx.spell, "name", "spell"))
        if not isinstance(payload, dict):
            return

        routed = {
            key: value
            for key, value in payload.items()
            if key not in {"blocked", "blocked_key"}
        }

        if victim is ctx.actor and routed.get("to_victim"):
            routed["to_char"] = routed.pop("to_victim")
        elif routed.get("to_victim"):
            routed["victim"] = victim

        if routed.get("to_room"):
            exclude = {str(getattr(ctx.actor, "id", "") or "")}
            if not ctx.is_object_target():
                exclude.add(str(getattr(victim, "id", "") or ""))
            targets = self._room_players(ctx.room, exclude_ids=exclude)
            if targets:
                routed["targets"] = targets
            else:
                routed.pop("to_room", None)

        ctx.queue_payload(routed)

    def remove_effects(self, ctx: SpellContext, *effect_names: str, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        for effect_name in effect_names:
            normalized = str(effect_name or "").strip().lower()
            handler_id = normalized if normalized.startswith(("spell.", "skill.")) else FightUtil.spell_handler_name(normalized.replace("_", " "))
            self.effect_handler.affect_strip(victim, handler_id)
            self.effect_handler.affect_strip(victim, normalized)
        return ctx.mark_performed()

    def dispel_effects(self, ctx: SpellContext, *effect_names: str, target: Any = None,
                       notify: bool = True, level_adjust: int = 0):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        removed_effects = []
        for effect_name in effect_names:
            removed_effects.extend(self.effect_handler.dispel_effects(ctx.level + level_adjust, victim, str(effect_name or "").strip().lower()))
        if removed_effects:
            if notify:
                self._queue_removed_effect_messages(ctx, victim, removed_effects)
            ctx.mark_performed()
        return bool(removed_effects)

    def dispel_sequence(self, ctx: SpellContext, entries: list[dict], level_adjust: int = 0):
        """Attempt content-defined effects and raw-flag fallbacks in order."""
        removed = False
        for entry in entries:
            if entry.get("flag"):
                success = self.dispel_flag(ctx, entry["flag"], entry["effect"], level_adjust=level_adjust)
            else:
                success = self.dispel_effects(ctx, entry["effect"], level_adjust=level_adjust)
            if success:
                removed = True
                if entry.get("message"):
                    self.send_message(ctx, entry["message"], include_actor_in_room=True)
        return removed

    def dispel_flag(self, ctx: SpellContext, flag: str, effect: str, level_adjust: int = 0):
        # ROM rolls for a raw bit before checking whether its spell record survived.
        if (not self.is_affected(ctx, flag)
                or EffectUtil.saves_dispel(ctx.level + level_adjust, int(ctx.victim.level), -1)
                or self.is_affected(ctx, effect)):
            return False
        return self.clear_affected_flags(ctx, flag)

    def clear_affected_flags(self, ctx: SpellContext, *flags: str, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        bits = GameApi.get_enum("affectedBy")
        raw = GameApi.flags_to_int(victim.status_flags.affected_by)
        for flag in flags:
            raw = GameApi.unset_bit(raw, int(getattr(bits, flag)))
        victim.status_flags.assign_bitfield("affected_by", raw)
        return ctx.mark_performed()

    def _queue_removed_effect_messages(self, ctx: SpellContext, victim: Any, effects: list[Effect]) -> None:
        seen = set()
        for effect in effects:
            effect_type = str(getattr(effect, "type", "")).strip().lower()
            if effect_type in seen:
                continue
            seen.add(effect_type)
            ability = self._ability_for_effect(ctx, getattr(effect, "type", ""))
            if ability is None:
                continue
            text = DisplayUtil.display_effect_message(self._ability_message(ability, "to_char", "msg_off", ctx, victim))
            if not text:
                continue
            if not text.endswith(("\r\n", "\n\r", "\n")):
                text = f"{text}\r\n"
            if victim is ctx.actor:
                ctx.queue_payload({"to_char": text})
            else:
                ctx.queue_payload({"victim": victim, "to_victim": text})

    def _ability_for_effect(self, ctx: SpellContext, effect_type: Any):
        registry = getattr(getattr(ctx, "handler", None), "spell_registry", None)
        return AbilityResolver(spell_registry=registry).effect_owner(effect_type, spell_only=True)

    def _ability_message(self, ability: Any, channel: str, key: str, ctx: SpellContext, target: Any) -> str:
        tokens = ctx.payload_tokens() if callable(getattr(ctx, "payload_tokens", None)) else {}
        target_name = DisplayUtil.entity_name(target, is_npc=CharacterApi.is_npc)
        tokens.update(
            {
                "victim": target_name,
                "target": target_name,
                "t": target_name,
                "n": target_name,
                "item": Item.short(target) if hasattr(target, "item_type") else tokens.get("item", ""),
                "actor_his": getattr(getattr(ctx, "actor", None), "his_her", lambda: "its")(),
                "victim_his": getattr(target, "his_her", lambda: "its")(),
                "victim_him": getattr(target, "him_her", lambda: "it")(),
            }
        )
        if callable(getattr(ability, "message", None)):
            return str(ability.message(channel, key, **tokens) or "")
        return ""

    def damage_expr(
        self,
        ctx: SpellContext,
        expression: str,
        dam_type: str = "DAM_NONE",
        save_half: bool = True,
        save_level_adjust: int = 0,
        target: Any = None,
        dt: str = "",
        object_effect: str = "",
        on_failed_save=None,
        post_save_expression: str = "",
        save_divisor: int = 2,
    ):
        if object_effect not in ("", "acid"):
            raise ValueError(f"Unsupported object effect: {object_effect}")
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        damage = self.eval_int(ctx, expression, victim=victim)
        saved = save_half and self.saves_spell(ctx, dam_type, save_level_adjust, target=victim)
        if object_effect == "acid":
            self.acid_effect(ctx, ctx.level // 2 if saved else ctx.level,
                             damage // 4 if saved else damage, target=victim)
        if saved:
            damage = GenericUtil.trunc_div(damage, int(save_divisor))
        elif on_failed_save is not None:
            on_failed_save(ctx)
        if post_save_expression:
            damage = self.eval_int(ctx, post_save_expression, damage=damage, saved=saved, victim=victim)
        payload = self._fight_handler(ctx).damage(
            ctx.actor,
            victim,
            damage,
            dt=dt or getattr(ctx.spell, "noun_damage", "") or getattr(ctx.spell, "name", "spell"),
            dam_type=dam_type,
        )
        self._queue_damage_payload(ctx, payload, victim)
        return ctx.mark_performed()

    def damage_table(self, ctx: SpellContext, dam_type: str, on_failed_save=None):
        """Roll uniform table damage using a bounded level for saves and follow-ups."""
        table = ctx.spell.tables.get("damage", [])
        if not table:
            raise ValueError("Table damage requires a nonempty tables.damage.")
        level = max(0, min(ctx.level, len(table) - 1))
        scoped = replace(ctx, cast_level=level, aliases=dict(ctx.aliases))
        result = self.damage_expr(
            scoped, f"number_range({int(table[level]) // 2}, {int(table[level]) * 2})",
            dam_type, on_failed_save=on_failed_save,
        )
        if scoped.performed:
            ctx.mark_performed()
        return result

    def invoke_spell(self, ctx: SpellContext, name: str, level: int):
        """Execute another spell's content without a new cast attempt or announcement."""
        spell = self._ability_for_effect(ctx, name)
        if spell is None:
            raise ValueError(f"Unknown spell: {name}")
        child = replace(ctx, spell=spell, cast_level=int(level), aliases={},
                        done=False, performed=False, failed=False)
        result = self.execute_lambdas(child)
        if child.performed:
            ctx.mark_performed()
        return result

    def alignment(self, ctx: SpellContext, target: Any = None) -> int:
        return self._alignment(ctx.resolve(target) if target is not None else ctx.victim)

    def is_npc(self, ctx: SpellContext, target: Any = None) -> bool:
        return CharacterApi.is_npc(ctx.resolve(target) if target is not None else ctx.actor)

    def is_immortal(self, ctx: SpellContext, target: Any = None) -> bool:
        return CharacterApi.is_immortal(ctx.resolve(target) if target is not None else ctx.actor)

    def room_combat_stats(self, ctx: SpellContext, player_divisor: int = 1) -> dict[str, int]:
        """Summarize fighting positions without conflating them with opponent pointers."""
        if player_divisor <= 0:
            raise ValueError("Combat level weighting requires a positive player divisor.")
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        position = CharacterApi.pos_value("POS_FIGHTING")
        fighters = [entity for entity in self._room_entities(room)
                    if CharacterApi.position_value(entity) == position]
        levels = [int(entity.level) for entity in fighters]
        return {"count": len(fighters), "highest": max([0, *levels]),
                "total": sum(int(entity.level) if CharacterApi.is_npc(entity)
                             else GenericUtil.trunc_div(int(entity.level), player_divisor)
                             for entity in fighters)}

    def roll_range(self, ctx: SpellContext, low: int, high: int) -> int:
        return self._range_roll(int(low), int(high))

    def stop_fighting(self, ctx: SpellContext, target: Any = None, both: bool = False):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if (getattr(victim, "fighting", None) is not None
                or CharacterApi.position_value(victim) == CharacterApi.pos_value("POS_FIGHTING")):
            self._fight_handler(ctx).stop_fighting(victim, both=both)
            return ctx.mark_performed()
        return False

    def alignment_group(self, ctx: SpellContext, target: Any = None) -> int:
        value = self.alignment(ctx, target)
        return 1 if value >= 350 else -1 if value <= -350 else 0

    def is_affected(self, ctx: SpellContext, name: str, target: Any = None) -> bool:
        return self._effect_active(ctx.resolve(target) if target is not None else ctx.victim, name)

    def is_safe_spell(self, ctx: SpellContext, target: Any = None, area: bool = True) -> bool:
        victim = ctx.resolve(target) if target is not None else ctx.victim
        return self._fight_handler(ctx).is_safe_spell(ctx.actor, victim, area=area)

    def is_safe(self, ctx: SpellContext, target: Any = None) -> bool:
        return self._fight_handler(ctx).is_safe(ctx.actor, ctx.resolve(target) if target is not None else ctx.victim)

    def character_flag(self, ctx: SpellContext, field: str, flag: str, target: Any = None) -> bool:
        enums = {"act": "actBits", "off": "offenseTypes", "imm": "mobImmunity"}
        victim = ctx.resolve(target) if target is not None else ctx.victim
        enum = GameApi.get_enum(enums[field])
        bit = getattr(enum, flag).value
        return GameApi.is_set(GameApi.flags_to_int(getattr(victim.status_flags, field, 0)), bit)

    def invisibility_level(self, ctx: SpellContext, target: Any = None) -> int:
        victim = ctx.resolve(target) if target is not None else ctx.victim
        return int(getattr(getattr(victim, "status_flags", None), "invis_level", 0))

    def room_has_flag(self, ctx: SpellContext, flag: str) -> bool:
        return self._room_flag(self._find_room_for_entity(ctx.victim) or ctx.room, flag)

    def same_group(self, ctx: SpellContext, target: Any = None) -> bool:
        return CharacterApi.is_same_group(ctx.actor, ctx.resolve(target) if target is not None else ctx.victim)

    def item_kind(self, ctx: SpellContext) -> str:
        raw = str(getattr(ctx.obj, "item_type", "")).lower()
        return GameApi.item_table_map().get(raw, {}).get("type", raw).lower().removeprefix("item_")

    def item_has_flag(self, ctx: SpellContext, flag: str, weapon: bool = False, target: Any = None) -> bool:
        enum = GameApi.get_enum("weaponType" if weapon else "itemFlags")
        item = ctx.resolve(target) if target is not None else ctx.obj
        value = getattr(item, "value4" if weapon else "extra_flags", 0)
        return GameApi.is_set(GameApi.flags_to_int(value), getattr(enum, flag).value)

    def object_value_expr(self, ctx: SpellContext, index: int, expression: str):
        if ctx.obj is None or int(index) not in range(5):
            raise ValueError("Object value index must be between zero and four.")
        setattr(ctx.obj, f"value{int(index)}", str(self.eval_int(ctx, expression)))
        return ctx.mark_performed()

    def roll_different(self, ctx: SpellContext, low: int, high: int, current: int) -> int:
        if high < low or (high == low and low == current):
            raise ValueError("The random range must contain an alternative value.")
        result = self._range_roll(low, high)
        while result == current:
            result = self._range_roll(low, high)
        return result

    def counter_effect(self, ctx: SpellContext, flag: str, effect: str,
                       success_key: str, failure_key: str):
        """Try an opposed effect, then finish without applying the new effect."""
        if not self.is_affected(ctx, flag):
            return False
        removed = self.dispel_effects(ctx, effect)
        self.send_message(ctx, success_key if removed else failure_key, include_actor_in_room=True)
        ctx.stop()
        return bool(removed)

    def counter_item_flag(self, ctx: SpellContext, flag: str, effect: str,
                          success_key: str, failure_key: str):
        if not self.item_has_flag(ctx, flag):
            return False
        item = ctx.obj
        matching = [entry for entry in getattr(item, "effects", [])
                    if str(entry.type).lower() == effect.lower()]
        level = matching[0].level if matching else item.level
        if EffectUtil.saves_dispel(ctx.level, int(level), 0):
            self.send_message(ctx, failure_key)
        else:
            if matching:
                self.effect_handler.remove_effect(item, matching[0])
            bit = getattr(GameApi.get_enum("itemFlags"), flag).value
            flags = GameApi.flags_to_int(item.extra_flags)
            item.extra_flags = GameApi.flags_to_letters(GameApi.unset_bit(flags, bit))
            self.send_message(ctx, success_key, include_actor_in_room=True)
            ctx.mark_performed()
        ctx.stop()
        return bool(ctx.performed)

    def follow(self, ctx: SpellContext, master: Any = None, grouped: bool = False):
        """Detach an old following relationship, then establish the requested one."""
        follower = ctx.victim
        master = ctx.resolve(master) if master is not None else ctx.actor
        previous = getattr(follower, "master", None)

        def notify(key, recipient, leader):
            tokens = {**ctx.payload_tokens(), "follower": DisplayUtil.entity_name(follower, is_npc=CharacterApi.is_npc),
                      "master": DisplayUtil.entity_name(leader, is_npc=CharacterApi.is_npc)}
            self.send(ctx, victim=recipient,
                      to_victim=ctx.spell.message("to_victim", key, **tokens))

        if previous is not None:
            if self.is_affected(ctx, "AFF_CHARM"):
                self.clear_affected_flags(ctx, "AFF_CHARM")
                self.remove_effects(ctx, "spell.charm_person")
            if ctx.room is not None and CharacterApi.can_see(previous, follower, ctx.room):
                notify("follow_stop_master", previous, previous)
                notify("follow_stop", follower, previous)
            if getattr(previous, "pet", None) is follower:
                previous.pet = None
            follower.master = follower.leader = None
        follower.master = master
        follower.leader = master if grouped else None
        if CharacterApi.can_see(master, follower, ctx.room):
            notify("follow_start_master", master, master)
        notify("follow_start", follower, master)
        return ctx.mark_performed()

    def has_position(self, ctx: SpellContext, name: str, target: Any = None) -> bool:
        victim = ctx.resolve(target) if target is not None else ctx.victim
        position = getattr(victim, "position", None)
        if position is None:
            return False
        positions = GameApi.get_enum("positions")
        return CharacterApi.position_value(victim) == int(getattr(positions, name))

    def for_each_room(self, ctx: SpellContext, operation, predicate=None, safe: bool = False,
                      stop_on_block: bool = False):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        for victim in self._room_entities(room):
            scoped = replace(ctx, target=victim, aliases=dict(ctx.aliases, target=victim, victim=victim),
                             done=False, performed=False)
            if predicate is not None and not predicate(scoped):
                continue
            if safe and self._fight_handler(ctx).is_safe_spell(ctx.actor, victim, area=True):
                continue
            operation(scoped)
            if scoped.performed:
                ctx.mark_performed()
            if stop_on_block and scoped.done:
                ctx.finish()
                break
        return bool(ctx.performed)

    def is_outside(self, ctx: SpellContext) -> bool:
        return not self._room_flag(ctx.room, "ROOM_INDOORS")

    def is_raining(self, ctx: SpellContext) -> bool:
        weather = getattr(ctx.handler, "weather_handler", None)
        sky = getattr(getattr(weather, "weather_info", None), "sky", None)
        return sky is not None and int(sky) >= int(GameApi.get_enum("timeAndWeather").SKY_RAINING)

    def area_message(self, ctx: SpellContext, key: str, outdoors: bool = False, awake: bool = False):
        registry = self._room_registry(ctx)
        if registry is None or ctx.room is None:
            return False
        area_id = getattr(ctx.room, "area_id", None)
        for room in registry.all_rooms():
            if room is ctx.room or area_id is None or getattr(room, "area_id", None) != area_id:
                continue
            if outdoors and self._room_flag(room, "ROOM_INDOORS"):
                continue
            for victim in self._room_entities(room):
                if awake and not CharacterApi.is_awake(victim):
                    continue
                scoped = replace(ctx, room=room, target=victim, aliases={})
                self.send_message(scoped, key)
        return True

    def breath_damage(self, ctx: SpellContext, minimum_hp: int, lower_divisor: int,
                      upper_divisor: int, dice_sides: int, upper_limit: int | None = None):
        hp = max(minimum_hp, int(ctx.actor.hit))
        low = hp // lower_divisor + 1
        high = hp // upper_divisor if upper_limit is None else upper_limit
        # ROM number_range returns the lower bound when the interval is reversed.
        hp_damage = self._range_roll(low, high)
        dice_damage = self.eval_int(ctx, f"dice(level, {dice_sides})")
        return max(hp_damage + dice_damage // 10, dice_damage + hp_damage // 10)

    @staticmethod
    def _range_roll(low: int, high: int) -> int:
        return low if high <= low else random.randint(low, high)

    def current_stat(self, ctx: SpellContext, name: str, target: Any = None) -> int:
        victim = ctx.resolve(target) if target is not None else ctx.victim
        return CharacterApi.current_stat(victim, name)

    def heat_equipment(self, ctx: SpellContext):
        """Heat carried equipment; content owns damage ratios and outcome messages."""
        from game.Equipped import Equipped

        victim = ctx.victim
        if victim is None:
            return False
        rules = ctx.spell.rules
        flags = GameApi.get_enum("itemFlags")
        weapon_flags = GameApi.get_enum("weaponType")
        immunity = GameApi.get_enum("mobImmunity")
        room = self._find_room_for_entity(victim) or ctx.room
        damage = 0
        acted = False

        def has_flag(item, name):
            return GameApi.is_set(GameApi.flags_to_int(item.extra_flags), getattr(flags, name).value)

        def notify(key, item):
            tokens = {**ctx.payload_tokens(), "victim": DisplayUtil.entity_name(victim, is_npc=CharacterApi.is_npc), "item": Item.short(item)}
            self.send(ctx, victim=victim, include_actor_in_room=True,
                      to_victim=ctx.spell.message("to_victim", key, **tokens),
                      to_room=ctx.spell.message("to_room", key, **tokens))

        if (not self.saves_spell(ctx, "DAM_FIRE", level_adjust=2)
                and not GameApi.is_set(GameApi.flags_to_int(victim.status_flags.imm), immunity.IMM_FIRE.value)):
            for item in list(victim.owned_items()):
                if self._range_roll(1, 2 * ctx.level) <= int(item.level):
                    continue
                if (self.saves_spell(ctx, "DAM_FIRE") or has_flag(item, "ITEM_NONMETAL")
                        or has_flag(item, "ITEM_BURN_PROOF")):
                    continue
                raw_type = str(item.item_type).lower()
                kind = GameApi.item_table_map().get(raw_type, {}).get("type", raw_type).lower().removeprefix("item_")
                if kind not in rules:
                    continue
                rule = rules[kind]
                slot = victim.equipped_slot_of(item)
                worn = slot is not None
                if (worn and rule.get("skip_flaming") and GameApi.is_set(
                        GameApi.flags_to_int(item.value4), weapon_flags.WEAPON_FLAMING.value)):
                    continue
                can_drop = not has_flag(item, "ITEM_NODROP") or (
                    not CharacterApi.is_npc(victim) and CharacterApi.is_immortal(victim))
                dropped = can_drop
                if worn and dropped and rule.get("weight_check"):
                    dropped = int(item.weight) // 10 < self._range_roll(1, 2 * self.current_stat(ctx, "dexterity"))
                if worn and dropped:
                    result = Equipped.remove_item(victim, slot, item, flags, effect_handler=self.effect_handler)
                    dropped = not bool(result.blocked_key)
                    notify("removed" if dropped else "no_remove", item)
                outcome = ("worn_" if worn else "carried_") + ("drop" if dropped else "stuck")
                outcome_rule = rule[outcome]
                notify(outcome_rule["message"], item)
                if "constant" in outcome_rule:
                    damage += int(outcome_rule["constant"])
                else:
                    damage += self._range_roll(1, int(item.level)) // int(outcome_rule["divisor"])
                if dropped:
                    victim.remove_item(item)
                    room.add_item_to_room(item)
                acted = True
        if not acted:
            self.send_message(ctx, "no_effect")
            return False
        return self.damage_expr(ctx, str(damage), "DAM_FIRE", save_half=False,
            post_save_expression="trunc_div(2 * damage, 3) if ctx.saves_spell('DAM_FIRE') else damage")

    def chain_damage(self, ctx: SpellContext, expression: str, dam_type: str,
                     level_step: int = 4, save_divisor: int = 3,
                     first_message: str = "", arc_message: str = "",
                     rebound_message: str = "", fizzle_message: str = ""):
        """Repeat room sweeps, avoiding consecutive hits and rebounding when stranded."""
        if level_step <= 0:
            raise ValueError("Chain damage requires a positive level step.")
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None or ctx.victim is None:
            return False
        level = ctx.level
        last = ctx.victim
        actor_was_present = any(entity is ctx.actor for entity in self._room_entities(room))

        def strike(victim, message):
            scoped = replace(ctx, target=victim, cast_level=level, aliases={})
            if message:
                self.send_message(scoped, message, include_actor_in_room=message != first_message)
            self.damage_expr(scoped, expression, dam_type, save_divisor=save_divisor)
            ctx.mark_performed()

        strike(last, first_message)
        level -= level_step
        while level > 0:
            room = self._find_room_for_entity(ctx.actor) or room
            if actor_was_present and not any(entity is ctx.actor for entity in self._room_entities(room)):
                break
            found = False
            for victim in self._room_entities(room):
                # A preceding hit may have extracted another entry from this sweep.
                if not any(entity is victim for entity in self._room_entities(room)):
                    continue
                if self._fight_handler(ctx).is_safe_spell(ctx.actor, victim, area=True) or victim is last:
                    continue
                found = True
                last = victim
                strike(victim, arc_message)
                level -= level_step
            if not found:
                if last is ctx.actor:
                    if fizzle_message:
                        self.send_message(ctx, fizzle_message, target=ctx.actor)
                    break
                last = ctx.actor
                strike(last, rebound_message)
                level -= level_step
        return bool(ctx.performed)

    def send_message(self, ctx: SpellContext, key: str, target: Any = None, **routing):
        """Render a content-owned message through the usual spell payload channels."""
        key = next(iter(GenericUtil.camel_to_snake_case({key: ""})), key)
        victim = ctx.resolve(target) if target is not None else ctx.victim
        return self.send(ctx, victim=victim, **{
            channel: self._ability_message(ctx.spell, channel, key, ctx, victim)
            for channel in ("to_char", "to_victim", "to_room")
        }, **routing)

    def stop_when(self, ctx: SpellContext, condition: bool, message_key: str = "", **routing):
        if not condition:
            return False
        if message_key:
            self.send_message(ctx, message_key, **routing)
        return ctx.stop()

    def resource_expr(self, ctx: SpellContext, resource: str, expression: str, target: Any = None):
        """Set a character resource from content, or apply an experience gain/loss."""
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        if resource not in {"hit", "mana", "movement", "alignment", "experience"}:
            raise ValueError(f"Unsupported character resource: {resource}")
        if resource == "experience":
            from player.CharacterAdvancement import CharacterAdvancement
            CharacterAdvancement.gain_experience(victim, self.eval_int(ctx, expression, victim=victim))
        else:
            owner = victim
            field = resource
            if resource == "alignment":
                owner = getattr(victim, "character_attributes", None) or victim
            elif resource == "movement" and not hasattr(victim, "movement"):
                field = "move"
            current = GenericUtil.to_int(getattr(owner, field, 0), 0)
            value = self.eval_int(ctx, expression, victim=victim, current=current)
            setattr(owner, field, value)
        return ctx.mark_performed()

    def acid_effect(self, ctx: SpellContext, level: int, damage: int, target: Any = None):
        from game.RandomNumberGenerator import RandomNumberGenerator
        from util.AcidExposure import AcidExposure

        entity = ctx.resolve(target) if target is not None else ctx.target
        if entity is None:
            return False
        if hasattr(entity, "owned_items"):
            room = self._find_room_for_entity(entity) or ctx.room
        elif hasattr(entity, "contents"):
            room = entity
        else:
            raise ValueError("Acid exposure requires a character or room target.")
        exposure = AcidExposure(self.effect_handler, GameApi.get_enum("itemFlags"),
                                GameApi.get_enum("applyTypes"), GameApi.item_table_map(),
                                RandomNumberGenerator())

        def notify(key, item):
            text = ctx.spell.message("to_room", key, item=Item.short(item))
            if text:
                # ROM TO_ALL: every player in the object's room, including caster
                # and carrier, receives the destruction/etching notice.
                def render(observer):
                    rendered = ctx.spell.message("to_room", key, **DisplayUtil.visible_tokens({"item": item}, observer, room))
                    return rendered.rstrip("\r\n") + "\r\n"
                ctx.queue_payload({"to_room": DisplayUtil.room_text(text.rstrip("\r\n") + "\r\n", render, room),
                                   "targets": self._room_players(room, exclude_ids=set())})

        if hasattr(entity, "owned_items"):
            exposure.character(entity, level, damage, room, notify)
        else:
            exposure.room(entity, level, damage, notify)
        return True

    def elemental_effect(self, ctx: SpellContext, kind: str, level: int, damage: int, target: Any = None):
        entity = ctx.resolve(target) if target is not None else ctx.target
        if entity is None:
            return False
        fight = self._fight_handler(ctx)
        room = (self._find_room_for_entity(entity) or ctx.room) if hasattr(entity, "owned_items") else entity
        exposure = getattr(self, "elemental_exposure", None) or fight.weapon_hit_handler
        result = exposure.expose(kind, ctx.actor, entity, level, damage, room,
                                                 fight._check_immunity, payload=ctx.spell.payload)
        if hasattr(entity, "owned_items"):
            self._queue_damage_payload(ctx, result, entity)
        elif result.get("to_room"):
            ctx.queue_payload({"to_room": result["to_room"], "targets": self._room_players(room)})
        return True

    def elemental_breath(self, ctx: SpellContext, expression: str, kind: str, area: bool = False):
        """Apply breath exposure before HP damage, with ROM collateral scaling."""
        damage_types = {"flaming": "DAM_FIRE", "frost": "DAM_COLD", "shocking": "DAM_LIGHTNING"}
        if kind not in damage_types or (area and kind == "shocking"):
            raise ValueError(f"Unsupported breath exposure: {kind}, area={area}")
        primary = ctx.victim
        if primary is None:
            return False
        room = self._find_room_for_entity(primary) or ctx.room
        if room is None:
            return False
        fight = self._fight_handler(ctx)
        damage_type = damage_types[kind]
        base_damage = self.eval_int(ctx, expression, victim=primary)
        if area:
            self.elemental_effect(ctx, kind, ctx.level, base_damage // 2, target=room)
        victims = self._room_entities(room) if area else [primary]
        for victim in victims:
            if area:
                if victim is ctx.actor or fight.is_safe_spell(ctx.actor, victim, area=True):
                    continue
                if (CharacterApi.is_npc(ctx.actor) and CharacterApi.is_npc(victim)
                        and (getattr(ctx.actor, "fighting", None) is not victim
                             or getattr(victim, "fighting", None) is not ctx.actor)):
                    continue
            collateral = area and victim is not primary
            saved = EffectUtil.saves_spell(ctx.level - (2 if collateral else 0), victim, damage_type,
                                          immunity=fight._check_immunity)
            if collateral:
                effect_level = ctx.level // 4 if saved else ctx.level // 2
                effect_damage = base_damage // 8 if saved else base_damage // 4
                damage = base_damage // 4 if saved else base_damage // 2
            else:
                effect_level = ctx.level // 2 if saved else ctx.level
                effect_damage = base_damage // 4 if saved else base_damage
                damage = base_damage // 2 if saved else base_damage
            self.elemental_effect(ctx, kind, effect_level, effect_damage, target=victim)
            result = fight.damage(ctx.actor, victim, damage, dam_type=damage_type,
                                  dt=getattr(ctx.spell, "noun_damage", "") or getattr(ctx.spell, "name", "spell"))
            self._queue_damage_payload(ctx, result, victim)
        return ctx.mark_performed()

    def poison_effect(self, ctx: SpellContext, level: int, damage: int, target: Any = None):
        from game.RandomNumberGenerator import RandomNumberGenerator
        from util.PoisonExposure import PoisonExposure

        entity = ctx.resolve(target) if target is not None else ctx.target
        if entity is None:
            return False
        exposure = PoisonExposure(self.effect_handler, GameApi.get_enum("itemFlags"),
                                  GameApi.item_table_map(), RandomNumberGenerator())

        def notify(victim):
            room = self._find_room_for_entity(victim) or ctx.room
            text = self._ability_message(ctx.spell, "to_room", "poisoned", ctx, victim)
            def render(observer):
                return ctx.spell.message("to_room", "poisoned", **DisplayUtil.visible_tokens({"victim": victim}, observer, room))
            self.send(ctx,
                      to_victim=self._ability_message(ctx.spell, "to_victim", "poisoned", ctx, victim),
                      to_room=DisplayUtil.room_text(text, render, room),
                      victim=victim, include_actor_in_room=True)

        if hasattr(entity, "owned_items"):
            saves = lambda level, victim, kind: EffectUtil.saves_spell(
                level, victim, kind, immunity=self._fight_handler(ctx)._check_immunity)
            exposure.character(entity, level, damage, saves, notify)
        elif hasattr(entity, "contents"):
            exposure.room(entity, level, damage)
        else:
            raise ValueError("Poison exposure requires a character or room target.")
        return True

    def damage_room_expr(self, ctx: SpellContext, expression: str, dam_type: str = "DAM_NONE", save_half: bool = True,
                         effect: str = "", target_filter=None):
        if effect not in ("", "poison"):
            raise ValueError(f"Unsupported room effect: {effect}")
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        acted = False
        if effect == "poison":
            # Gas exposes floor objects before character safety checks and rolls
            # one base damage amount for the entire cloud, as in ROM.
            base_damage = self.eval_int(ctx, expression)
            self.poison_effect(ctx, ctx.level, base_damage, target=room)
            acted = True
        for victim in self._room_entities(room):
            if victim is ctx.actor or self._fight_handler(ctx).is_safe_spell(ctx.actor, victim, area=True):
                continue
            if target_filter is not None and not target_filter(victim):
                continue
            damage = base_damage if effect == "poison" else self.eval_int(ctx, expression, victim=victim)
            if effect == "poison":
                saved = save_half and EffectUtil.saves_spell(ctx.level, victim, dam_type,
                                                           immunity=self._fight_handler(ctx)._check_immunity)
                self.poison_effect(ctx, ctx.level // 2 if saved else ctx.level,
                                   damage // 4 if saved else damage, target=victim)
            else:
                saved = save_half and self.saves_spell(ctx, dam_type, target=victim)
            if saved:
                damage //= 2
            payload = self._fight_handler(ctx).damage(
                ctx.actor,
                victim,
                damage,
                dt=getattr(ctx.spell, "noun_damage", "") or getattr(ctx.spell, "name", "spell"),
                dam_type=dam_type,
            )
            self._queue_damage_payload(ctx, payload, victim)
            acted = True
        if acted:
            ctx.mark_performed()
        return acted

    def heal_expr(self, ctx: SpellContext, expression: str, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        amount = max(0, self.eval_int(ctx, expression, victim=victim))
        current = GenericUtil.to_int(getattr(victim, "hit", 0), 0)
        maximum = GenericUtil.to_int(getattr(victim, "max_hit", current), current)
        victim.hit = min(maximum, current + amount)
        self._fight_handler(ctx).update_pos(victim)
        return ctx.mark_performed()

    def restore_move_expr(self, ctx: SpellContext, expression: str, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        amount = max(0, self.eval_int(ctx, expression, victim=victim))
        current = GenericUtil.to_int(getattr(victim, "movement", getattr(victim, "move", 0)), 0)
        maximum = GenericUtil.to_int(getattr(victim, "max_movement", getattr(victim, "max_move", current)), current)
        updated = min(maximum, current + amount)
        if hasattr(victim, "movement"):
            victim.movement = updated
        if hasattr(victim, "move"):
            victim.move = updated
        return ctx.mark_performed()

    def create_object(self, ctx: SpellContext, vnum: str, destination: str = "room"):
        registry = getattr(getattr(ctx.handler, "registry_service", None), "item_registry", None)
        if registry is None:
            return False
        prototype = registry.get_or_none(vnum=str(vnum))
        if prototype is None:
            return False
        item = ItemFactory.create(prototype)
        if destination == "inventory":
            from game.Equipped import Equipped
            Equipped.add_to_inventory(ctx.actor, item)
        elif ctx.room is not None:
            ctx.room.add_item_to_room(item)
        ctx.set_alias("created_item", item)
        return ctx.mark_performed()

    def find_world_target(self, ctx: SpellContext):
        return ctx.set_target(self._find_world_character(ctx, ctx.target_name))

    def item_worn(self, ctx: SpellContext, target: Any = None) -> bool:
        item = ctx.resolve(target) if target is not None else ctx.obj
        return (int(getattr(item, 'wear_loc', -1)) != -1
                or any(value is item for value in getattr(getattr(ctx.actor, 'equipped', None), '__dict__', {}).values()))

    def set_item_flag(self, ctx: SpellContext, flag: str, target: Any = None):
        item = ctx.resolve(target) if target is not None else ctx.obj
        raw = GameApi.flags_to_int(item.extra_flags)
        item.extra_flags = GameApi.flags_to_letters(GameApi.set_bit(raw, int(getattr(GameApi.get_enum('itemFlags'), flag))))
        return ctx.mark_performed()

    def configure_object(self, ctx: SpellContext, expressions: dict, target: Any = 'created_item'):
        item = ctx.resolve(target)
        allowed = {'timer', 'level', 'cost', 'weight', *(f'value{i}' for i in range(5))}
        for field, expression in expressions.items():
            if field not in allowed:
                raise ValueError(f'Unsupported numeric object field: {field}')
            value = self.eval_int(ctx, expression, obj=item)
            setattr(item, field, str(value) if field.startswith('value') else value)
        return ctx.mark_performed()

    def find_carried_object(self, ctx: SpellContext):
        from util.LookupUtil import LookupUtil
        return ctx.set_target(LookupUtil.inventory(ctx.actor, ctx.target_name,
            visible=lambda item: ItemApi.can_see_object(ctx.room, ctx.actor, item)))

    def equipped_item(self, ctx: SpellContext, slot: str):
        return getattr(getattr(ctx.actor, 'equipped', None), slot, None)

    def equip_created(self, ctx: SpellContext, slot: str):
        from game.Equipped import Equipped
        old = self.equipped_item(ctx, slot)
        if old is not None:
            self.effect_handler.remove_item_effects(ctx.actor, old)
            Equipped.unequip_item(ctx.actor, slot)
            self.send(ctx, to_char=ctx.spell.message('to_char', 'removed', item=Item.short(old)))
        item = ctx.get_alias('created_item')
        Equipped.equip_item(ctx.actor, item, slot)
        self.effect_handler.apply_item_effects(ctx.actor, item)
        self.send(ctx, to_char=ctx.spell.message('to_char', 'equipped', item=Item.short(item)),
                  to_room=ctx.spell.message('to_room', 'equipped', actor=DisplayUtil.entity_name(ctx.actor, is_npc=CharacterApi.is_npc), item=Item.short(item)),
                  include_victim_in_room=True)
        return ctx.mark_performed()

    def fill_liquid(self, ctx: SpellContext, liquid: str, amount_expr: str):
        item = ctx.obj
        amount = min(self.eval_int(ctx, amount_expr), int(item.value0) - int(item.value1))
        if amount <= 0:
            return False
        item.value1, item.value2 = str(int(item.value1) + amount), liquid
        definition = GameApi.liquids_map().get(liquid, {})
        item.liquid_color = definition.get('color')
        item.liquid_affect_data = list(definition.get('affect', []))
        if liquid.lower() not in item.name.lower().split():
            item.name += ' ' + liquid
        return ctx.mark_performed()

    def movement_full(self, ctx: SpellContext) -> bool:
        victim = ctx.victim
        return int(getattr(victim, 'movement', getattr(victim, 'move', 0))) == int(
            getattr(victim, 'max_movement', getattr(victim, 'max_move', 0)))

    def world_object_locations(self, ctx: SpellContext):
        yield from ItemOwnership(self.effect_handler, self._room_registry(ctx)).walk_world_items()

    def extract_object(self, ctx: SpellContext, target: Any = None):
        item = ctx.resolve(target) if target is not None else ctx.obj
        registry = self._room_registry(ctx)
        ownership = ItemOwnership(self.effect_handler, registry)
        location = ownership.find_location(item, None if registry is not None else [ctx.room])
        if location is not None:
            ownership.detach(item, location)
            return ctx.mark_performed()
        if item in self._owned_items(ctx.actor):
            ownership.detach_carried(ctx.actor, item)
            return ctx.mark_performed()
        return False

    def enchant_item(self, ctx: SpellContext, rules: dict):
        self.object_affects(ctx, ctx.obj)
        result = self.effect_handler.enchant_object(ctx.obj, ctx.spell.handler_id, ctx.level, rules,
            self.eval_int(ctx, rules['level_reduction']), self.eval_int(ctx, rules['exceptional_boundary']),
            self.game_parameter(ctx, 'LEVEL_HERO') - 1, self.roll_range(ctx, 1, 100))
        self.send_message(ctx, result)
        if result == 'destroyed':
            return self.extract_object(ctx)
        return ctx.mark_performed() if result != 'failed' else False

    def object_affects(self, ctx: SpellContext, item):
        if not getattr(item, 'enchanted', False) and not getattr(item, 'effects', None) and getattr(item, 'affect_data', []):
            item.effects = []
            ItemFactory.update_affect_data(item)
        return self.effect_handler.ensure_effects(item)

    def describe_object(self, ctx: SpellContext, rules: dict):
        item = ctx.obj
        lines = []
        def emit(key, **tokens):
            lines.append(ctx.spell.message('to_char', key, **tokens))
        def labels(enum_name, raw):
            enum = GameApi.get_enum(enum_name)
            numeric = EffectUtil.enum_value(enum, raw, None)
            if numeric is None:
                numeric = GameApi.flags_to_int(raw)
            return ' '.join(name.split('_', 1)[-1].lower().replace('_', ' ') for name, bit in enum.__members__.items()
                            if int(bit) and numeric & int(bit)) or 'none'
        values = [getattr(item, f'value{i}', '0') for i in range(5)]
        kind = self.item_kind(ctx)
        emit('summary', name=item.name, kind=kind, flags=labels('itemFlags', item.extra_flags),
             weight=GenericUtil.trunc_div(int(item.weight), 10), cost=item.cost, level=item.level)
        def spell_name(reference):
            name = self.reference_name(ctx, reference, rules['spell_indices'])
            return " '" + name + "'" if name else ''
        if kind in ('scroll', 'potion', 'pill'):
            emit('spells', level=values[0], spells=''.join(spell_name(value) for value in values[1:]))
        elif kind in ('wand', 'staff'):
            emit('charges', charges=values[2], level=values[0], spell=spell_name(values[3]))
        elif kind == 'drink_con':
            liquid = str(values[2]).strip("'\"")
            if liquid == '0': liquid = 'water'
            emit('liquid', liquid=liquid, color=GameApi.liquids_map().get(liquid, {}).get('color')
                 or getattr(item, 'liquid_color', None) or 'unknown')
        elif kind == 'container':
            emit('container', capacity=values[0], maximum=values[3], flags=labels('containerState', values[1]))
            if int(values[4]) != 100:
                emit('multiplier', multiplier=values[4])
        elif kind == 'weapon':
            classes = GameApi.get_enum('weaponClass')
            numeric = EffectUtil.enum_value(classes, values[0], None)
            class_names = {name.removeprefix('WEAPON_').lower() for name in classes.__members__}
            named = str(values[0]).lower().removeprefix('weapon_')
            weapon = next((name.removeprefix('WEAPON_').lower() for name, value in classes.__members__.items()
                           if int(value) == numeric), named if named in class_names else 'unknown')
            emit('weapon', weapon=rules.get('weapon_names', {}).get(weapon, weapon))
            low, high = int(values[1]), int(values[2])
            if getattr(item, 'new_format', True):
                emit('dice', count=low, sides=high, average=GenericUtil.trunc_div((1 + high) * low, 2))
            else:
                emit('range', low=low, high=high, average=GenericUtil.trunc_div(low + high, 2))
            if GameApi.flags_to_int(values[4]):
                emit('weapon_flags', flags=labels('weaponType', values[4]))
        elif kind == 'armor':
            emit('armor', pierce=values[0], bash=values[1], slash=values[2], magic=values[3])
        apply_types = GameApi.get_enum('applyTypes')
        where_types = GameApi.get_enum('whereAffect')
        for effect in self.object_affects(ctx, item):
            location = EffectUtil.enum_value(apply_types, effect.location, 0)
            if location == int(apply_types.APPLY_NONE) or int(effect.modifier) == 0:
                continue
            name = next((name for name, value in apply_types.__members__.items() if int(value) == location), 'unknown')
            name = rules.get('apply_names', {}).get(name, name.removeprefix('APPLY_').lower().replace('_', ' '))
            prototype = not item.enchanted and GenericUtil.to_int(effect.type, 0) < 0
            duration = int(effect.duration)
            emit('affect_timed' if not prototype and duration >= 0 else 'affect',
                 location=name, modifier=effect.modifier, duration=duration)
            where = EffectUtil.enum_value(where_types, effect.where, -1)
            entry = next((entry for name, entry in rules['affect_flags'].items()
                          if where == EffectUtil.enum_value(where_types, name, -2)), None)
            if entry is not None and EffectUtil.enum_value(GameApi.get_enum(entry['enum']), effect.bitvector, 0):
                emit(entry['message'], flags=labels(entry['enum'], effect.bitvector))
            elif entry is None and str(effect.bitvector or '0') != '0':
                emit('unknown', where=effect.where, bit=effect.bitvector)
        self.send(ctx, to_char=''.join(lines))
        return ctx.mark_performed()

    def reference_name(self, ctx: SpellContext, reference: Any, indices: dict | None = None) -> str:
        if isinstance(reference, dict):
            reference = reference.get('name', reference.get('handlerId', ''))
        reference = getattr(reference, 'name', reference)
        value = str(reference if reference is not None else '').strip()
        number = GenericUtil.to_int(value, None)
        if number is not None:
            return next((name for name, index in (indices or {}).items() if index == number), '')
        ability = self._ability_for_effect(ctx, value)
        return str(getattr(ability, 'name', value))

    def reference_index(self, ctx: SpellContext, reference: Any, indices: dict) -> int:
        number = GenericUtil.to_int(reference, None) if isinstance(reference, (str, int)) else None
        if number is not None:
            return number
        name = self.reference_name(ctx, reference)
        if name not in indices:
            raise ValueError(f'No configured ordinal for spell reference: {name}')
        return indices[name]

    def recharge_item(self, ctx: SpellContext, rules: dict):
        item = ctx.obj
        ordinal = self.reference_index(ctx, item.value3, rules['spell_indices'])
        if ordinal >= self.eval_int(ctx, rules['skill_limit']):
            self.send_message(ctx, 'tooAdvanced')
            return False
        if int(item.value1) == 0:
            self.send_message(ctx, 'used')
            return False
        maximum, current = int(item.value1), int(item.value2)
        chance = self.eval_int(ctx, rules['chance'], ordinal=ordinal, maximum=maximum, current=current)
        percent = self.roll_range(ctx, 1, 100)
        if percent < GenericUtil.trunc_div(chance, 2):
            self.send_message(ctx, 'recharged')
            item.value2, item.value1 = str(max(maximum, current)), '0'
        elif percent <= chance:
            # This checkout sends the partial-success notice twice to the caster.
            self.send_message(ctx, 'partial')
            self.send_message(ctx, 'partial')
            chargeback = max(1, GenericUtil.trunc_div((maximum - current) * percent, 100)) if maximum > current else 0
            item.value2, item.value1 = str(current + chargeback), '0'
        elif percent <= min(95, GenericUtil.trunc_div(3 * chance, 2)):
            self.send_message(ctx, 'unchanged')
            if maximum > 1:
                item.value1 = str(maximum - 1)
        else:
            self.send_message(ctx, 'destroyed')
            return self.extract_object(ctx)
        return ctx.mark_performed()

    def locate_objects(self, ctx: SpellContext, rules: dict):
        from util.LookupUtil import LookupUtil
        found = 0
        limit = self.eval_int(ctx, rules['limit'])
        for item, root, location in self.world_object_locations(ctx):
            room = location['room']
            if (not ItemApi.can_see_object(ctx.room, ctx.actor, item)
                    or not LookupUtil.matches(ctx.target_name, item.name)
                    or GameApi.is_set(GameApi.flags_to_int(item.extra_flags), int(GameApi.get_enum('itemFlags').ITEM_NOLOCATE))):
                continue
            if self.roll_range(ctx, 1, 100) > self.eval_int(ctx, rules['chance']) or ctx.actor.level < item.level:
                continue
            owner = None if location['kind'] == 'room' else location['parent']
            tokens = {'owner': '', 'room': '', 'vnum': ''}
            if owner is not None and CharacterApi.can_see(ctx.actor, owner, ctx.room):
                key, tokens['owner'] = 'carried', DisplayUtil.entity_name(owner, is_npc=CharacterApi.is_npc)
            elif owner is not None:
                key = 'somewhere'
            else:
                key = 'roomImmortal' if self.is_immortal(ctx) else 'room'
                tokens.update(room=room.name, vnum=room.vnum)
            normalized = next(iter(GenericUtil.camel_to_snake_case({key: ''})))
            self.send(ctx, to_char=ctx.spell.message('to_char', normalized, **tokens))
            found += 1
            if found >= limit:
                break
        if not found:
            self.send_message(ctx, 'absent')
        return ctx.mark_performed()

    def change_weather(self, ctx: SpellContext, expression: str):
        weather = getattr(ctx.handler, 'weather_handler', None)
        if weather is None:
            return False
        weather.weather_info.change += self.eval_int(ctx, expression)
        return ctx.mark_performed()

    def throw_voice(self, ctx: SpellContext):
        from util.InterpUtil import InterpUtil
        speaker, text = InterpUtil.one_argument(ctx.target_name)
        for listener in self._room_entities(ctx.room):
            if speaker in str(listener.name).lower().split() or not CharacterApi.is_awake(listener):
                continue
            saved = self.saves_spell(ctx, 'DAM_OTHER', target=listener)
            message = ctx.spell.message('to_victim', 'saved' if saved else 'spoken', speaker=speaker, speech=text)
            if not saved and message:
                message = message[0].upper() + message[1:]
            self.send(ctx, victim=listener, to_victim=message)
        return ctx.mark_performed()

    def room_of(self, ctx: SpellContext, target: Any = None):
        entity = ctx.resolve(target) if target is not None else ctx.victim
        registry = self._room_registry(ctx)
        room_id = getattr(entity, "room_id", "")
        if registry is not None and room_id:
            return registry.get_or_none(id=room_id)
        return self._find_room_for_entity(entity)

    def get_room(self, ctx: SpellContext, vnum: str):
        registry = self._room_registry(ctx)
        return registry.get_or_none(vnum=str(vnum)) if registry is not None else None

    def room_flag(self, ctx: SpellContext, flag: str, room: Any = None) -> bool:
        room = ctx.resolve(room) if room is not None else self.room_of(ctx)
        return room is not None and self._room_flag(room, flag)

    def can_view_room(self, ctx: SpellContext, room: Any, target: Any = None) -> bool:
        viewer = ctx.resolve(target) if target is not None else ctx.actor
        return CharacterApi.can_see_room(viewer, ctx.resolve(room))

    def game_parameter(self, ctx: SpellContext, name: str) -> int:
        return int(getattr(GameApi.get_enum("gameParameters"), name))

    def player_flag(self, ctx: SpellContext, flag: str, target: Any = None) -> bool:
        victim = ctx.resolve(target) if target is not None else ctx.victim
        bit = int(getattr(GameApi.get_enum("playerActBits"), flag))
        return GameApi.is_set(GameApi.flags_to_int(victim.status_flags.act), bit)

    def clan_mismatch(self, ctx: SpellContext, target: Any = None) -> bool:
        victim = ctx.resolve(target) if target is not None else ctx.victim
        return CharacterApi.is_clan(victim) and str(victim.guild).strip().lower() != str(
            getattr(ctx.actor, "guild", "") or "").strip().lower()

    def is_shopkeeper(self, ctx: SpellContext, target: Any = None) -> bool:
        victim = ctx.resolve(target) if target is not None else ctx.victim
        registry = getattr(getattr(ctx.handler, "registry_service", None), "shop_registry", None)
        return CharacterApi.is_npc(victim) and registry is not None and registry.find_by_keeper_vnum(
            getattr(victim, "vnum", "")) is not None

    def held_item_kind(self, ctx: SpellContext, kind: str) -> bool:
        item = getattr(getattr(ctx.actor, "equipped", None), "held", None)
        return item is not None and str(item.item_type).lower().removeprefix("item_") == kind.lower()

    def consume_held_item(self, ctx: SpellContext, kind: str, message_key: str):
        if not self.held_item_kind(ctx, kind):
            return False
        from game.Equipped import Equipped
        item = ctx.actor.equipped.held
        message_key = next(iter(GenericUtil.camel_to_snake_case({message_key: ""})))
        self.send(ctx, to_char=ctx.spell.message("to_char", message_key, item=Item.short(item)))
        self.effect_handler.remove_item_effects(ctx.actor, item)
        Equipped.unequip_item(ctx.actor, "held")
        Equipped.remove_from_inventory(ctx.actor, item)
        return ctx.mark_performed()

    def pet_in_room(self, ctx: SpellContext):
        pet = getattr(ctx.actor, "pet", None)
        current = self.room_of(ctx, ctx.actor)
        return pet if pet is not None and current is not None and self.room_of(ctx, pet) is current else None

    def random_room(self, ctx: SpellContext, target: Any = None):
        """Choose uniformly among the rooms accepted by ROM's random-room helper."""
        victim = ctx.resolve(target) if target is not None else ctx.victim
        registry = self._room_registry(ctx)
        if registry is None:
            return None
        flags = GameApi.get_enum("roomFlags")
        rooms = [room for room in registry.all_rooms() if room is not None
                 and CharacterApi.can_see_room(victim, room) and not room.is_private(flags)
                 and not any(self._room_flag(room, flag) for flag in
                             ("ROOM_PRIVATE", "ROOM_SOLITARY", "ROOM_SAFE"))
                 and (CharacterApi.is_npc(victim) or self.character_flag(ctx, "act", "ACT_AGGRESSIVE", target=victim)
                      or not self._room_flag(room, "ROOM_LAW"))]
        return random.choice(rooms) if rooms else None

    def move_to(self, ctx: SpellContext, room: Any, target: Any = None, departure_key: str = "",
                arrival_key: str = "", notice_key: str = "", notice_before: bool = False):
        """Relocate one character with content-owned notices and an automatic room view."""
        victim = ctx.resolve(target) if target is not None else ctx.victim
        room = ctx.resolve(room)
        current = self.room_of(ctx, victim)
        if current is None or room is None:
            return False
        exclude = {str(victim.id)}
        if departure_key:
            self._queue_room_text(ctx, current, self._ability_message(ctx.spell, "to_room", departure_key, ctx, victim), exclude)
        if notice_key and notice_before:
            self.send_message(ctx, notice_key, target=victim)
        if CharacterApi.is_npc(victim):
            current.remove_mobile_from_room(victim)
            room.add_mobile_to_room(victim)
        else:
            current.remove_player_from_room(victim)
            room.add_player_to_room(victim)
        victim.room_id, victim.area_id = room.id, room.area_id
        if arrival_key:
            self._queue_room_text(ctx, room, self._ability_message(ctx.spell, "to_room", arrival_key, ctx, victim), exclude)
        if notice_key and not notice_before:
            self.send_message(ctx, notice_key, target=victim)
        if not CharacterApi.is_npc(victim):
            ctx.queue_payload({"view_character": victim, "to_room_obj": room})
        return ctx.mark_performed()

    def create_portals(self, ctx: SpellContext, vnum: str, timer_expr: str, two_way: bool = False):
        destination = self.room_of(ctx)
        registry = getattr(getattr(ctx.handler, "registry_service", None), "item_registry", None)
        prototype = registry.get_or_none(vnum=str(vnum)) if registry is not None else None
        if prototype is None or destination is None or ctx.room is None:
            return False
        routes = [(ctx.room, destination)]
        if two_way and destination is not ctx.room:
            routes.append((destination, ctx.room))
        for index, (origin, endpoint) in enumerate(routes):
            portal = ItemFactory.create(prototype)
            portal.timer = self.eval_int(ctx, timer_expr)
            portal.value3 = str(endpoint.vnum)
            origin.add_item_to_room(portal)
            tokens = {**ctx.payload_tokens(), "item": Item.short(portal)}
            key = "created" if index == 0 else "created_remote"
            room_text = ctx.spell.message("to_room", key, **tokens)
            self._queue_room_text(ctx, origin, room_text, {str(ctx.actor.id)} if index == 0 else set())
            if index == 0:
                self.send(ctx, to_char=ctx.spell.message("to_char", key, **tokens))
        return ctx.mark_performed()

    def scan(self, ctx: SpellContext, rules: dict):
        """Scan local exits; intentionally follows this checkout's scan.c, including closed exits."""
        arguments = str(ctx.target_name or "").lower().split()
        word = arguments[0] if arguments else ""
        directions = rules["directions"]
        direction = next((i for i, name in enumerate(directions) if word in (name, name[0])), None) if word else None
        if word and direction is None:
            return self.send_message(ctx, "invalid")
        room = ctx.room
        registry = self._room_registry(ctx)
        if room is None or registry is None:
            return False
        def report(scan_room, depth, door):
            for entity in self._room_entities(scan_room):
                if entity is ctx.actor or not CharacterApi.can_see(ctx.actor, entity, ctx.room):
                    continue
                distance = rules["distances"][depth].format(direction=directions[door] if door is not None else "")
                self.send(ctx, to_char=ctx.spell.message("to_char", "seen", victim=DisplayUtil.entity_name(entity, is_npc=CharacterApi.is_npc), distance=distance))
        def adjacent(origin, door):
            exit_obj = origin.get_exit(door)
            if exit_obj is None:
                return None
            return (registry.get_or_none(id=exit_obj.to_room_id) if exit_obj.to_room_id
                    else registry.get_or_none(vnum=str(exit_obj.to_room_vnum)))
        if not word:
            self.send_message(ctx, "around", include_victim_in_room=True)
            report(room, 0, None)
            for door in range(len(directions)):
                neighbor = adjacent(room, door)
                if neighbor is not None:
                    report(neighbor, 1, door)
        else:
            tokens = {**ctx.payload_tokens(), "direction": directions[direction]}
            self.send(ctx, to_char=ctx.spell.message("to_char", "peer", **tokens),
                      to_room=ctx.spell.message("to_room", "peer", **tokens), include_victim_in_room=True)
            for depth in range(1, len(rules["distances"])):
                neighbor = adjacent(room, direction)
                if neighbor is not None:
                    room = neighbor
                    report(room, depth, direction)
        return ctx.mark_performed()

    def uncurse_item(self, ctx: SpellContext):
        return self._remove_curse_item(ctx, ctx.obj) if ctx.obj is not None else False

    def uncurse_owned_items(self, ctx: SpellContext, target: Any = None,
                           limit: int = 1, level_adjust: int = 0):
        """Try carried items in order, stopping after the requested number of successes."""
        victim = ctx.resolve(target) if target is not None else ctx.victim
        successes = 0
        for item in self._owned_items(victim):
            if successes >= limit:
                break
            if self._remove_curse_item(ctx, item, owner=victim, quiet=True, level_adjust=level_adjust):
                tokens = {**ctx.payload_tokens(), "victim": DisplayUtil.entity_name(victim, is_npc=CharacterApi.is_npc), "item": Item.short(item)}
                self.send(ctx, victim=victim, include_actor_in_room=True,
                          to_victim=ctx.spell.message("to_victim", "item_cured", **tokens),
                          to_room=ctx.spell.message("to_room", "item_cured", **tokens))
                successes += 1
                ctx.mark_performed()
        return bool(successes)

    def sleep(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        if self.apply_affect_data(ctx, join=True):
            if CharacterApi.is_awake(victim):
                self.send_message(ctx, "apply", include_actor_in_room=True)
                CharacterApi.set_position(victim, "POS_SLEEPING")
            return True
        return False

    def eval_int(self, ctx: SpellContext, expression: str, **extras) -> int:
        locals_dict = {
            "ctx": ctx,
            "actor": ctx.actor,
            "spell": ctx.spell,
            "room": ctx.room,
            "target": ctx.target,
            "victim": ctx.victim,
            "obj": ctx.obj,
            "level": ctx.level,
            "dice": lambda n, s: sum(random.randint(1, max(1, GenericUtil.to_int(s, 1))) for _ in range(max(0, GenericUtil.to_int(n, 0)))),
            "number_range": lambda low, high: random.randint(GenericUtil.to_int(low, 0), GenericUtil.to_int(high, GenericUtil.to_int(low, 0))),
            "number_fuzzy": lambda value: EffectUtil.number_fuzzy(value),
            "UMAX": lambda a, b: max(GenericUtil.to_int(a, 0), GenericUtil.to_int(b, 0)),
            "UMIN": lambda a, b: min(GenericUtil.to_int(a, 0), GenericUtil.to_int(b, 0)),
            "abs": abs,
            "max": max,
            "min": min,
            "int": int,
            "trunc_div": GenericUtil.trunc_div,
        }
        locals_dict.update(extras)
        return int(eval(str(expression), {"__builtins__": {}}, locals_dict))

    def _effect_active(self, target, effect_name: str) -> bool:
        name = str(effect_name or "").strip()
        if not name:
            return False
        normalized = name.lower()
        if any(str(getattr(effect, "type", "")).strip().lower() == normalized for effect in getattr(target, "effects", []) or []):
            return True
        if name.upper().startswith("AFF_"):
            return CharacterApi.is_affected_by_name(target, CharacterApi.get_enum("affectedBy"), name.upper())
        return False

    def _queue_damage_payload(self, ctx: SpellContext, payload: dict, victim):
        if not payload:
            return
        for notice in payload.get("pre_damage_payloads", []):
            ctx.queue_payload(notice)
        self.send(
            ctx,
            to_char=payload.get("to_char", "") or "",
            to_room=payload.get("to_room", "") or "",
            to_victim=payload.get("to_victim", "") or "",
            victim=victim,
        )
        notice = {key: payload[key] for key in
                  ("to_wiznet", "wiznet_actor", "wiznet_flag", "global_message", "global_targets") if key in payload}
        if notice:
            ctx.queue_payload(notice)

        for reward in payload.get("reward_payloads", []):
            ctx.queue_payload(reward)
        for action in payload.get("post_damage_actions", []):
            ctx.queue_payload(action)

    def _find_room_for_entity(self, entity):
        registry = self._room_registry(entity)
        if registry is None or not getattr(entity, "room_id", ""):
            return None
        return registry.get_or_none(id=getattr(entity, "room_id", ""))

    def _find_world_character(self, ctx: SpellContext, name: str):
        wanted = str(name or "").strip()
        registry = self._room_registry(ctx)
        if not wanted or registry is None:
            return None
        for room in registry.all_rooms():
            target = PlayerUtil.get_target(ctx.actor, wanted, room, self._room_helper(ctx))
            if target is not None:
                return target
        return None

    @staticmethod
    def _alignment(entity) -> int:
        from game.AnimateEntity import AnimateEntity
        return AnimateEntity.get_alignment(entity)

    @staticmethod
    def _room_players(room, exclude_ids: set[str] | None = None) -> list[Any]:
        if room is None:
            return []
        exclude = {str(value) for value in (exclude_ids or set())}
        return [player for player in getattr(room, "characters", {}).values() if str(getattr(player, "id", "")) not in exclude]

    @staticmethod
    def _room_entities(room) -> list[Any]:
        if room is None:
            return []
        return list(getattr(room, "characters", {}).values()) + list(getattr(room, "mobiles", {}).values())

    def _room_flag(self, room, flag_name: str) -> bool:
        flags = CharacterApi.get_enum("roomFlags")
        bit = CharacterApi.enum_bit(flags, flag_name)
        return bit > 0 and CharacterApi.is_set(GenericUtil.to_int(getattr(room, "room_flags", 0), 0), bit)

    def _queue_room_text(self, ctx: SpellContext, room, text: str, exclude_ids: set[str] | None = None):
        if room is None or not text:
            return False
        targets = self._room_players(room, exclude_ids=exclude_ids)
        if not targets:
            return False
        ctx.queue_payload({"to_room": text, "targets": targets})
        return True

    @staticmethod
    def _same_side(actor, entity) -> bool:
        return CharacterApi.is_npc(actor) == CharacterApi.is_npc(entity)

    @staticmethod
    def _same_class(actor, entity) -> bool:
        if actor is None or entity is None or CharacterApi.is_npc(entity):
            return False
        actor_class = str(getattr(getattr(actor, "character_class", None), "name", "") or "").strip().lower()
        entity_class = str(getattr(getattr(entity, "character_class", None), "name", "") or "").strip().lower()
        return bool(actor_class) and actor_class == entity_class

    @staticmethod
    def _room_combatants(room) -> list[Any]:
        fighting_pos = CharacterApi.pos_value("POS_FIGHTING")
        fighters = []
        for entity in SpellApi._room_entities(room):
            position = GenericUtil.to_int(getattr(entity, "position", getattr(getattr(entity, "character_attributes", None), "position", 0)), 0)
            if getattr(entity, "fighting", None) is not None or position == fighting_pos:
                fighters.append(entity)
        return fighters

    @staticmethod
    def _owned_items(owner) -> list[Any]:
        if callable(getattr(owner, "owned_items", None)):
            return list(owner.owned_items())
        items = list(getattr(owner, "loot", []) or [])
        equipped = getattr(owner, "equipped", None)
        if equipped is not None:
            for item in getattr(equipped, "__dict__", {}).values():
                if item is not None and item not in items:
                    items.append(item)
        return items

    def _remove_curse_item(self, ctx: SpellContext, item, owner: Any = None, quiet: bool = False,
                           level_adjust: int = 2) -> bool:
        item_flags = CharacterApi.get_enum("itemFlags")
        nodrop = item_flags.ITEM_NODROP
        noremove = item_flags.ITEM_NOREMOVE
        nouncurse = item_flags.ITEM_NOUNCURSE
        raw_flags = GameApi.flags_to_int(getattr(item, "extra_flags", 0))
        cursed = GameApi.is_set(raw_flags, nodrop.value) or GameApi.is_set(raw_flags, noremove.value)
        if not cursed:
            if quiet:
                return False
            return ctx.fail(f"There doesn't seem to be a curse on {Item.short(item)}.\r\n")
        if GameApi.is_set(raw_flags, nouncurse.value):
            if quiet:
                return False
            return ctx.fail(f"The curse on {Item.short(item)} is beyond your power.\r\n")
        if EffectUtil.saves_dispel(ctx.level + level_adjust, GenericUtil.to_int(getattr(item, "level", 0), 0), 0):
            if quiet:
                return False
            return ctx.fail(f"The curse on {Item.short(item)} is beyond your power.\r\n")
        raw_flags = GameApi.unset_bit(raw_flags, nodrop.value)
        raw_flags = GameApi.unset_bit(raw_flags, noremove.value)
        item.extra_flags = GameApi.flags_to_letters(raw_flags)
        if quiet:
            return True
        if owner is not None and owner is not ctx.actor:
            self.send(ctx, to_victim=f"Your {Item.short(item)} glows blue.\r\n", victim=owner)
            self.send(ctx, to_room=f"{DisplayUtil.entity_name(owner, is_npc=CharacterApi.is_npc)}'s {Item.short(item)} glows blue.\r\n", victim=owner)
        else:
            self.send(ctx, to_char=f"{Item.short(item)} glows blue.\r\n")
            self.send(ctx, to_room=f"{Item.short(item)} glows blue.\r\n")
        return ctx.mark_performed()

    @staticmethod
    def _mob_has_act(entity, flag_name: str) -> bool:
        if entity is None or not CharacterApi.is_npc(entity):
            return False
        act_bits = CharacterApi.get_enum("actBits")
        bit = CharacterApi.enum_bit(act_bits, flag_name)
        if bit <= 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(entity, "status_flags", None), "act", 0), 0)
        return CharacterApi.is_set(flags, bit)

    @staticmethod
    def _mob_has_imm(entity, flag_name: str) -> bool:
        if entity is None or not CharacterApi.is_npc(entity):
            return False
        flag_letters = CharacterApi.get_enum("flagLetters")
        if flag_name not in flag_letters.__members__:
            return False
        flags = GenericUtil.to_int(getattr(getattr(entity, "status_flags", None), "imm", 0), 0)
        return CharacterApi.is_set(flags, flag_letters[flag_name].value)

    @staticmethod
    def _player_has_act(entity, flag_name: str) -> bool:
        if entity is None or CharacterApi.is_npc(entity):
            return False
        act_bits = CharacterApi.get_enum("playerActBits")
        if flag_name not in act_bits.__members__:
            return False
        flags = GenericUtil.to_int(CharacterApi.convert_flags(getattr(getattr(entity, "status_flags", None), "act", "") or "0"), 0)
        return CharacterApi.is_set(flags, act_bits[flag_name].value)

    @staticmethod
    def _room_helper(ctx_or_entity):
        handler = getattr(ctx_or_entity, "handler", None)
        return getattr(handler, "room_helper", None) if handler is not None else None

    @staticmethod
    def _fight_handler(ctx_or_entity):
        handler = getattr(ctx_or_entity, "handler", None)
        if handler is None:
            return None
        return (
            getattr(handler, "fight_commands", None)
            or getattr(handler, "fight_handler", None)
            or handler
        )

    @staticmethod
    def _room_registry(ctx_or_entity):
        handler = getattr(ctx_or_entity, "handler", None)
        if handler is not None and getattr(handler, "room_registry", None) is not None:
            return handler.room_registry
        if handler is not None and getattr(getattr(handler, "registry_service", None), "room_registry", None) is not None:
            return handler.registry_service.room_registry
        return getattr(ctx_or_entity, "room_registry", None)

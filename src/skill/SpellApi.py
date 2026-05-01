from __future__ import annotations

import inspect
import random

from typing import Any

from game.GameMacros import GameMacros
from util.GenericUtil import GenericUtil
from util.FightUtil import FightUtil
from util.ObjectUtil import ObjectUtils
from object.Effect import Effect
from util.EffectUtil import EffectUtil
from util.ItemUtil import ItemUtil
from player.CharacterMacros import CharacterMacros
from util.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory
from skill.SpellContext import SpellContext
from skill.SpellSpeech import SpellSpeech


class SpellApi:
    DISPEL_EFFECTS = (
        "spell.armor",
        "spell.bless",
        "spell.blindness",
        "spell.calm",
        "spell.change_sex",
        "spell.charm_person",
        "spell.curse",
        "spell.detect_evil",
        "spell.detect_good",
        "spell.detect_hidden",
        "spell.detect_invis",
        "spell.detect_magic",
        "spell.faerie_fire",
        "spell.fly",
        "spell.frenzy",
        "spell.giant_strength",
        "spell.haste",
        "spell.infravision",
        "spell.invis",
        "spell.mass_invis",
        "spell.pass_door",
        "spell.plague",
        "spell.poison",
        "spell.protection_evil",
        "spell.protection_good",
        "spell.sanctuary",
        "spell.shield",
        "spell.sleep",
        "spell.slow",
        "spell.stone_skin",
        "spell.weaken",
    )

    def __init__(self):
        self.__name__ = "SpellApi"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def execute_lambdas(self, ctx: SpellContext) -> bool:
        lambdas = list(getattr(ctx.spell, "lambdas", []) or [])
        if not lambdas:
            return self.default_spell(ctx)

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
        actor_name = self._entity_name(ctx.actor)
        self.send(ctx, to_char=f"You cast {spell_label}" + (f" on {self._entity_name(victim)}" if victim is not None and victim is not ctx.actor else "") + ".\r\n", prepend=True)

        visible_spell = SpellSpeech.utterance(spell_label, actor_name, translated=False)
        obscure_spell = SpellSpeech.utterance(spell_label, actor_name, translated=True)

        if victim is not None and victim is not ctx.actor and not CharacterMacros.is_npc(victim):
            self.send(
                ctx,
                to_victim=visible_spell if self._same_class(ctx.actor, victim) else obscure_spell,
                victim=victim,
                prepend=True,
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
            ctx.payloads.insert(0, {"to_room": visible_spell, "targets": same_class_targets})
        if other_targets:
            ctx.payloads.insert(0, {"to_room": obscure_spell, "targets": other_targets})
        return True

    def start_offensive_combat(self, ctx: SpellContext):
        victim = ctx.victim
        target_type = str(getattr(ctx.spell, "target", "") or "").upper()
        if victim is None or victim is ctx.actor or target_type not in ("CHAR_OFFENSIVE", "OBJ_CHAR_OFF"):
            return
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return
        if getattr(ctx.actor, "fighting", None) is None:
            self._fight_handler(ctx).set_fighting(ctx.actor, victim, room.id)
        if getattr(victim, "fighting", None) is None:
            self._fight_handler(ctx).set_fighting(victim, ctx.actor, room.id)

    def send(self, ctx: SpellContext, to_char: str = "", to_room: str = "",to_victim: str = "", victim: Any = None,
             include_actor_in_room: bool = False, include_victim_in_room: bool = False, prepend: bool = False) -> bool:
        target = ctx.resolve(victim) if victim is not None else ctx.victim
        payload: dict[str, Any] = {}
        if to_char and ctx.is_player_source:
            payload["to_char"] = str(to_char)
        if to_victim and target is not None and not CharacterMacros.is_npc(target):
            payload["victim"] = target
            payload["to_victim"] = str(to_victim)
        if to_room:
            exclude = set()
            if not include_actor_in_room:
                exclude.add(str(getattr(ctx.actor, "id", "") or ""))
            if target is not None and not include_victim_in_room:
                exclude.add(str(getattr(target, "id", "") or ""))
            targets = self._room_players(ctx.room, exclude_ids=exclude)
            if targets:
                payload["to_room"] = str(to_room)
                payload["targets"] = targets
        if payload:
            if prepend:
                ctx.payloads.insert(0, payload)
            else:
                ctx.queue_payload(payload)
        return True

    def stop_if_affected(self, ctx: SpellContext, effect_name: str, message: str = "", target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.target
        if victim is None or not self._effect_active(victim, effect_name):
            return False
        if message:
            ctx.fail(message)
        else:
            ctx.stop()
        return True

    def stop_if_saved(self, ctx: SpellContext, level_adjust: int = 0, target: Any = None, message: str = ""):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None or not EffectUtil.saves_spell(ctx.level + int(level_adjust), victim, 0):
            return False
        if message:
            ctx.fail(message)
        else:
            ctx.stop()
        return True

    def apply_affect_data(self, ctx: SpellContext, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.target
        if victim is None:
            return False
        EffectUtil.apply_spell_effects(ctx.actor, victim, ctx.spell)
        return ctx.mark_performed()

    def remove_effects(self, ctx: SpellContext, *effect_names: str, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        for effect_name in effect_names:
            normalized = str(effect_name or "").strip().lower()
            handler_id = normalized if normalized.startswith("spell.") else FightUtil.spell_handler_name(normalized.replace("_", " "))
            EffectUtil.affect_strip(victim, handler_id)
            EffectUtil.affect_strip(victim, normalized)
        return ctx.mark_performed()

    def dispel_effects(self, ctx: SpellContext, *effect_names: str, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        removed = False
        for effect_name in effect_names:
            removed = EffectUtil.check_dispel(ctx.level, victim, str(effect_name or "").strip().lower()) or removed
        if removed:
            ctx.mark_performed()
        return removed

    def damage_expr(
        self,
        ctx: SpellContext,
        expression: str,
        dam_type: str = "DAM_NONE",
        save_half: bool = True,
        save_level_adjust: int = 0,
        target: Any = None,
        dt: str = "",
    ):
        victim = ctx.resolve(target) if target is not None else ctx.victim
        if victim is None:
            return False
        damage = self.eval_int(ctx, expression, victim=victim)
        if save_half and EffectUtil.saves_spell(ctx.level + int(save_level_adjust), victim, 0):
            damage //= 2
        payload = self._fight_handler(ctx).damage(
            ctx.actor,
            victim,
            damage,
            dt=dt or getattr(ctx.spell, "noun_damage", "") or getattr(ctx.spell, "name", "spell"),
            dam_type=dam_type,
        )
        self._queue_damage_payload(ctx, payload, victim)
        return ctx.mark_performed()

    def damage_room_expr(self, ctx: SpellContext, expression: str, dam_type: str = "DAM_NONE", save_half: bool = True):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        acted = False
        for victim in self._room_entities(room):
            if victim is ctx.actor or self._fight_handler(ctx).is_safe_spell(ctx.actor, victim, area=True):
                continue
            damage = self.eval_int(ctx, expression, victim=victim)
            if save_half and EffectUtil.saves_spell(ctx.level, victim, 0):
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
        item = ItemUtil.create_object(prototype)
        if destination == "inventory" and hasattr(ctx.actor, "loot"):
            ObjectUtils.add_to_inventory(ctx.actor, item)
        elif ctx.room is not None:
            ctx.room.add_item_to_room(item)
        ctx.set_alias("created_item", item)
        return ctx.mark_performed()

    def create_water(self, ctx: SpellContext):
        obj = ctx.obj
        if obj is None:
            return ctx.fail("What should the spell be cast upon?\r\n")
        item_type = str(getattr(obj, "item_type", "") or "").upper()
        if "DRINK" not in item_type and "FOUNTAIN" not in item_type:
            return ctx.fail("It is unable to hold water.\r\n")
        total = GenericUtil.to_int(getattr(obj, "value0", 0), 0)
        current = GenericUtil.to_int(getattr(obj, "value1", 0), 0)
        obj.value1 = str(min(total or max(1, ctx.level * 2), current + max(1, ctx.level * 2)))
        obj.value2 = "0"
        return ctx.mark_performed()

    def detect_poison(self, ctx: SpellContext):
        obj = ctx.obj
        if obj is None:
            return ctx.fail("What should the spell be cast upon?\r\n")
        item_type = str(getattr(obj, "item_type", "") or "").upper()
        poisoned = "FOOD" in item_type or "DRINK" in item_type or "FOUNTAIN" in item_type
        poisoned = poisoned and GenericUtil.to_int(getattr(obj, "value3", 0), 0) != 0
        return self.send(ctx, to_char="You smell poisonous fumes.\r\n" if poisoned else "It looks delicious.\r\n") and ctx.mark_performed()

    def identify(self, ctx: SpellContext):
        target = ctx.target
        if target is None:
            return ctx.fail("You failed to identify anything.\r\n")
        if ctx.obj is not None:
            text = (
                f"Object '{getattr(target, 'short_description', getattr(target, 'name', 'item'))}'.\r\n"
                f"Item type: {getattr(target, 'item_type', 'unknown')}.\r\n"
                f"Level {getattr(target, 'level', 0)}, weight {getattr(target, 'weight', 0)}, value {getattr(target, 'cost', 0)}.\r\n"
            )
        else:
            text = f"{self._entity_name(target)} is level {getattr(target, 'level', 0)} with alignment {self._alignment(target)}.\r\n"
        return self.send(ctx, to_char=text) and ctx.mark_performed()

    def locate_object(self, ctx: SpellContext):
        registry = self._room_registry(ctx)
        wanted = str(ctx.target_name or "").strip().lower()
        if registry is None or not wanted:
            return ctx.fail("Locate what?\r\n")
        lines = []
        limit = max(2, ctx.level // 2)
        for room in registry.all_rooms():
            for obj in getattr(room, "contents", {}).values():
                if wanted in str(getattr(obj, "name", "") or "").lower():
                    lines.append(f"{getattr(obj, 'short_description', getattr(obj, 'name', 'item'))} is in {getattr(room, 'name', 'somewhere')}.\r\n")
                    if len(lines) >= limit:
                        return self.send(ctx, to_char="".join(lines)) and ctx.mark_performed()
        return self.send(ctx, to_char="".join(lines) if lines else "Nothing like that is in heaven or earth.\r\n") and ctx.mark_performed()

    def teleport_target(self, ctx: SpellContext, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.victim or ctx.actor
        current = self._find_room_for_entity(victim)
        room = self._find_random_room(ctx)
        if victim is None or room is None or current is None or self._room_flag(current, "ROOM_NO_RECALL"):
            return ctx.fail("You failed.\r\n")
        if victim is not ctx.actor:
            if self._mob_has_imm(victim, "IMM_SUMMON") or getattr(victim, "fighting", None) is not None:
                return ctx.fail("You failed.\r\n")
            if EffectUtil.saves_spell(ctx.level - 5, victim, 0):
                return ctx.fail("You failed.\r\n")
        return self._move_character(
            ctx,
            victim,
            room,
            notify_victim=victim is not ctx.actor,
            line="You have been teleported!\r\n",
            from_room_line=f"{self._entity_name(victim)} vanishes!\r\n",
            to_room_line=f"{self._entity_name(victim)} slowly fades into existence.\r\n",
        )

    def summon_target(self, ctx: SpellContext):
        victim = self._find_world_character(ctx, ctx.target_name)
        current = self._find_room_for_entity(victim)
        if victim is None or victim is ctx.actor or ctx.room is None or current is None:
            return ctx.fail("You failed.\r\n")
        if (
            self._room_flag(ctx.room, "ROOM_SAFE")
            or self._room_flag(current, "ROOM_SAFE")
            or self._room_flag(current, "ROOM_PRIVATE")
            or self._room_flag(current, "ROOM_SOLITARY")
            or self._room_flag(current, "ROOM_NO_RECALL")
            or getattr(victim, "fighting", None) is not None
            or self._mob_has_act(victim, "ACT_AGGRESSIVE")
            or self._mob_has_imm(victim, "IMM_SUMMON")
            or self._player_has_act(victim, "PLR_NOSUMMON")
            or (CharacterMacros.is_npc(victim) and EffectUtil.saves_spell(ctx.level, victim, 0))
        ):
            return ctx.fail("You failed.\r\n")
        return self._move_character(
            ctx,
            victim,
            ctx.room,
            notify_victim=True,
            line=f"{self._entity_name(ctx.actor)} has summoned you!\r\n",
            from_room_line=f"{self._entity_name(victim)} disappears suddenly.\r\n",
            to_room_line=f"{self._entity_name(victim)} arrives suddenly.\r\n",
        )

    def word_of_recall(self, ctx: SpellContext, target: Any = None):
        victim = ctx.resolve(target) if target is not None else ctx.victim or ctx.actor
        current = self._find_room_for_entity(victim)
        room_registry = self._room_registry(ctx)
        temple = room_registry.get_or_none(vnum="3001") if room_registry is not None else None
        if victim is None or CharacterMacros.is_npc(victim) or temple is None or current is None:
            return ctx.fail("You are completely lost.\r\n")
        if current.id == temple.id:
            return False
        if self._room_flag(current, "ROOM_NO_RECALL") or self._effect_active(victim, "spell.curse") or self._effect_active(victim, "AFF_CURSE"):
            return ctx.fail("Spell failed.\r\n")
        if getattr(victim, "fighting", None) is not None:
            self._fight_handler(ctx).stop_fighting(victim, both=True)
        if hasattr(victim, "move"):
            victim.move = max(0, GenericUtil.to_int(getattr(victim, "move", 0), 0) // 2)
        if hasattr(victim, "movement"):
            victim.movement = max(0, GenericUtil.to_int(getattr(victim, "movement", 0), 0) // 2)
        return self._move_character(
            ctx,
            victim,
            temple,
            from_room_line=f"{self._entity_name(victim)} disappears.\r\n",
            to_room_line=f"{self._entity_name(victim)} appears in the room.\r\n",
        )

    def gate(self, ctx: SpellContext):
        victim = self._find_world_character(ctx, ctx.target_name)
        room = self._find_room_for_entity(victim)
        if (
            victim is None
            or victim is ctx.actor
            or room is None
            or ctx.room is None
            or self._room_flag(room, "ROOM_SAFE")
            or self._room_flag(room, "ROOM_PRIVATE")
            or self._room_flag(room, "ROOM_SOLITARY")
            or self._room_flag(room, "ROOM_NO_RECALL")
            or self._room_flag(ctx.room, "ROOM_NO_RECALL")
            or GenericUtil.to_int(getattr(victim, "level", 0), 0) >= ctx.level + 3
            or self._mob_has_imm(victim, "IMM_SUMMON")
            or (CharacterMacros.is_npc(victim) and EffectUtil.saves_spell(ctx.level, victim, 0))
        ):
            return ctx.fail("You failed.\r\n")
        return self._move_character(
            ctx,
            ctx.actor,
            room,
            notify_victim=True,
            line="You step through a gate and vanish.\r\n",
            from_room_line=f"{self._entity_name(ctx.actor)} steps through a gate and vanishes.\r\n",
            to_room_line=f"{self._entity_name(ctx.actor)} has arrived through a gate.\r\n",
        )

    def portal(self, ctx: SpellContext):
        return self._spawn_portal(ctx, two_way=False)

    def nexus(self, ctx: SpellContext):
        return self._spawn_portal(ctx, two_way=True)

    def farsight(self, ctx: SpellContext):
        target = self._find_world_character(ctx, ctx.target_name)
        room = self._find_room_for_entity(target)
        if room is None:
            return ctx.fail("You can't see that far.\r\n")
        return self.send(ctx, to_char=f"You gaze toward {self._entity_name(target)} in {getattr(room, 'name', 'somewhere')}.\r\n") and ctx.mark_performed()

    def control_weather(self, ctx: SpellContext):
        weather = getattr(ctx.handler, "weather_handler", None)
        if weather is None or getattr(weather, "weather_info", None) is None:
            return False
        direction = -1 if str(ctx.target_name or "").strip().lower() in ("better", "clear", "sunny") else 1
        weather.weather_info.change += 5 * direction
        weather.weather_info.mmhg += 10 * direction
        return ctx.mark_performed()

    def know_alignment(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return ctx.fail("Know the alignment of whom?\r\n")
        alignment = self._alignment(victim)
        if alignment > 350:
            text = f"{self._entity_name(victim)} has an aura of pure goodness.\r\n"
        elif alignment > 100:
            text = f"{self._entity_name(victim)} is of good alignment.\r\n"
        elif alignment < -350:
            text = f"{self._entity_name(victim)} radiates pure evil.\r\n"
        elif alignment < -100:
            text = f"{self._entity_name(victim)} is of evil alignment.\r\n"
        else:
            text = f"{self._entity_name(victim)} seems neutral.\r\n"
        return self.send(ctx, to_char=text) and ctx.mark_performed()

    def recharge(self, ctx: SpellContext):
        obj = ctx.obj
        if obj is None:
            return ctx.fail("What should the spell be cast upon?\r\n")
        item_type = str(getattr(obj, "item_type", "") or "").upper()
        if "WAND" not in item_type and "STAFF" not in item_type:
            return ctx.fail("That item does not hold magical charges.\r\n")
        max_charges = GenericUtil.to_int(getattr(obj, "value1", 0), 0)
        current = GenericUtil.to_int(getattr(obj, "value2", 0), 0)
        obj.value2 = str(min(max_charges, current + max(1, ctx.level // 8)))
        return ctx.mark_performed()

    def ray_of_truth(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        alignment = self._alignment(victim)
        if alignment < -350:
            return self.send(ctx, to_char=f"{self._entity_name(victim)} is unaffected by your ray of truth.\r\n") and ctx.mark_performed()
        damage = max(1, ctx.level * 10 - alignment // 10)
        return self.damage_expr(ctx, str(damage), "DAM_HOLY", save_half=False, dt="ray of truth")

    def enchant_weapon(self, ctx: SpellContext):
        return self._enchant_item(ctx, weapon=True)

    def enchant_armor(self, ctx: SpellContext):
        return self._enchant_item(ctx, weapon=False)

    def mass_invis(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        affected = False
        for entity in self._room_entities(room):
            if getattr(entity, "fighting", None) is not None or not self._same_side(ctx.actor, entity) or self._effect_active(entity, "AFF_INVISIBLE") or self._effect_active(entity, "spell.invis"):
                continue
            EffectUtil.apply_spell_effects(ctx.actor, entity, ctx.spell)
            affected = True
        return ctx.mark_performed() if affected else False

    def mass_healing(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        affected = False
        for entity in self._room_entities(room):
            if not self._same_side(ctx.actor, entity):
                continue
            self.heal_expr(ctx, "100", target=entity)
            self.restore_move_expr(ctx, "level", target=entity)
            affected = True
        return ctx.mark_performed() if affected else False

    def calm(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        fighters = self._room_combatants(room)
        if not fighters:
            return False
        for entity in fighters:
            if (CharacterMacros.is_npc(entity) and (self._mob_has_imm(entity, "IMM_MAGIC") or self._mob_has_act(entity, "ACT_UNDEAD"))) or self._effect_active(entity, "AFF_CALM") or self._effect_active(entity, "AFF_BERSERK") or self._effect_active(entity, "spell.frenzy"):
                return False

        count = len(fighters)
        high_level = max(GenericUtil.to_int(getattr(entity, "level", 0), 0) for entity in fighters)
        mlevel = 0
        for entity in fighters:
            entity_level = GenericUtil.to_int(getattr(entity, "level", 0), 0)
            mlevel += entity_level if CharacterMacros.is_npc(entity) else entity_level // 2
        chance = max(0, 4 * ctx.level - high_level + 2 * count)
        if random.randint(0, chance) < mlevel:
            return False

        for entity in fighters:
            self.send(ctx, to_victim="A wave of calm passes over you.\r\n", victim=entity)
            if getattr(entity, "fighting", None) is not None:
                self._fight_handler(ctx).stop_fighting(entity, both=False)
            EffectUtil.apply_spell_effects(ctx.actor, entity, ctx.spell)
        return ctx.mark_performed()

    def chain_lightning(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None or ctx.victim is None:
            return ctx.fail("Cast the spell on whom?\r\n")
        damage = max(1, ctx.level * 4)
        victims = [ctx.victim] + [entity for entity in self._room_entities(room) if entity not in (ctx.actor, ctx.victim)]
        for victim in victims:
            payload = self._fight_handler(ctx).damage(ctx.actor, victim, damage, dt=getattr(ctx.spell, "noun_damage", "lightning"), dam_type="DAM_LIGHTNING")
            self._queue_damage_payload(ctx, payload, victim)
            damage = max(1, damage // 2)
        return ctx.mark_performed()

    def holy_word(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        actor_alignment = self._alignment(ctx.actor)
        if room is None or abs(actor_alignment) < 350:
            return ctx.fail("You utter a word of no power.\r\n")
        for victim in self._room_entities(room):
            if victim is ctx.actor:
                self.heal_expr(ctx, "100", target=victim)
                continue
            target_alignment = self._alignment(victim)
            if actor_alignment > 0 and target_alignment < 0:
                if self._fight_handler(ctx).is_safe_spell(ctx.actor, victim, area=True):
                    continue
                self.damage_expr(ctx, "dice(level, 4) + 50", "DAM_HOLY", save_half=False, target=victim, dt="divine wrath")
            elif actor_alignment < 0 and target_alignment > 0:
                if self._fight_handler(ctx).is_safe_spell(ctx.actor, victim, area=True):
                    continue
                self.damage_expr(ctx, "dice(level, 4) + 50", "DAM_NEGATIVE", save_half=False, target=victim, dt="divine wrath")
            else:
                self.heal_expr(ctx, "50", target=victim)
        return ctx.mark_performed()

    def heat_metal(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        extra = 0
        equipped = getattr(victim, "equipped", None)
        for item in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
            material = str(getattr(item, "material", "") or "").lower()
            if item is not None and material in ("iron", "steel", "silver", "metal"):
                extra += max(1, ctx.level // 6)
        return self.damage_expr(ctx, f"dice(level, 2) + {extra}", "DAM_FIRE", target=victim, dt="heat metal")

    def energy_drain(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        if EffectUtil.saves_spell(ctx.level, victim, 0):
            return self.damage_expr(ctx, "1", "DAM_NEGATIVE", save_half=False, target=victim, dt="energy drain")
        victim.level = max(1, GenericUtil.to_int(getattr(victim, "level", 1), 1) - 1)
        victim.hit = max(1, GenericUtil.to_int(getattr(victim, "hit", 1), 1) - ctx.level)
        if hasattr(victim, "mana"):
            victim.mana = max(0, GenericUtil.to_int(getattr(victim, "mana", 0), 0) - ctx.level)
        ctx.actor.hit = min(
            GenericUtil.to_int(getattr(ctx.actor, "max_hit", getattr(ctx.actor, "hit", 0)), 0),
            GenericUtil.to_int(getattr(ctx.actor, "hit", 0), 0) + ctx.level,
        )
        return self.damage_expr(ctx, "level", "DAM_NEGATIVE", save_half=False, target=victim, dt="energy drain")

    def change_sex(self, ctx: SpellContext):
        victim = ctx.victim or ctx.actor
        current = GenericUtil.to_int(getattr(victim, "sex", 0), 0)
        options = [0, 1, 2]
        if current in options:
            options.remove(current)
        victim.sex = str(random.choice(options or [current]))
        return ctx.mark_performed()

    def faerie_fog(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        for victim in self._room_entities(room):
            if victim is ctx.actor:
                continue
            EffectUtil.affect_strip(victim, "spell.invis")
            EffectUtil.affect_strip(victim, "AFF_HIDE")
            EffectUtil.apply_spell_effects(ctx.actor, victim, ctx.spell)
        return ctx.mark_performed()

    def dispel_magic(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        removed = False
        for effect_name in self.DISPEL_EFFECTS:
            removed = EffectUtil.check_dispel(ctx.level, victim, effect_name) or removed
        if not removed:
            self.send(ctx, to_char="Spell failed.\r\n")
        return ctx.mark_performed() if removed else False

    def cancellation(self, ctx: SpellContext):
        return self.dispel_magic(ctx)

    def remove_curse(self, ctx: SpellContext):
        if ctx.obj is not None:
            return self._remove_curse_item(ctx, ctx.obj)
        victim = ctx.victim or ctx.actor
        if victim is None:
            return False
        removed = self.dispel_effects(ctx, "spell.curse", target=victim)
        for item in self._owned_items(victim):
            removed = self._remove_curse_item(ctx, item, owner=victim, quiet=True) or removed
        if removed:
            if victim is not ctx.actor:
                self.send(ctx, to_victim="You feel better.\r\n", victim=victim)
                self.send(ctx, to_room=f"{self._entity_name(victim)} looks more relaxed.\r\n", victim=victim, include_victim_in_room=True)
            return ctx.mark_performed()
        return False

    def poison(self, ctx: SpellContext):
        if ctx.obj is not None:
            return self.apply_affect_data(ctx)
        victim = ctx.victim
        if victim is None or self.stop_if_saved(ctx):
            return False
        effect = Effect(
            where="TO_AFFECTS",
            type=getattr(ctx.spell, "handler_id", getattr(ctx.spell, "name", "spell")),
            level=ctx.level,
            duration=max(1, ctx.level // 2),
            location="APPLY_STR",
            modifier=-2,
            bitvector="AFF_POISON",
            apply_to="char",
        )
        EffectUtil.affect_join(victim, effect)
        return ctx.mark_performed()

    def charm_person(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        if victim is ctx.actor:
            return ctx.fail("You like yourself even better!\r\n")
        if self.stop_if_saved(ctx):
            return False
        return self.apply_affect_data(ctx)

    def sleep(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None or self.stop_if_affected(ctx, "AFF_SLEEP") or self.stop_if_saved(ctx, level_adjust=-4):
            return False
        if self.apply_affect_data(ctx):
            if hasattr(victim, "position"):
                victim.position = CharacterMacros.pos_value("POS_SLEEPING")
            elif hasattr(getattr(victim, "character_attributes", None), "position"):
                victim.character_attributes.position = CharacterMacros.pos_value("POS_SLEEPING")
            return True
        return False

    def slow(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        if self.stop_if_affected(ctx, "spell.slow") or self.stop_if_affected(ctx, "AFF_SLOW"):
            return False
        if self._effect_active(victim, "AFF_HASTE"):
            self.dispel_effects(ctx, "spell.haste")
            return ctx.mark_performed()
        if self.stop_if_saved(ctx):
            self.send(ctx, to_victim="You feel momentarily lethargic.\r\n", victim=victim)
            return False
        return self.apply_affect_data(ctx)

    def chill_touch(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        if self.damage_expr(ctx, "dice(level, 5)", "DAM_COLD"):
            if not EffectUtil.saves_spell(ctx.level, victim, 0):
                effect = Effect(
                    where="TO_AFFECTS",
                    type=getattr(ctx.spell, "handler_id", getattr(ctx.spell, "name", "spell")),
                    level=ctx.level,
                    duration=6,
                    location="APPLY_STR",
                    modifier=-1,
                    bitvector="0",
                    apply_to="char",
                )
                EffectUtil.affect_join(victim, effect)
            return True
        return False

    def call_lightning(self, ctx: SpellContext):
        weather = getattr(ctx.handler, "weather_handler", None)
        if weather is None or getattr(weather, "weather_info", None) is None:
            return ctx.fail("You failed.\r\n")
        return self.damage_room_expr(ctx, "dice(level, 4) + level // 2", "DAM_LIGHTNING")

    def harm(self, ctx: SpellContext):
        victim = ctx.victim
        if victim is None:
            return False
        damage = max(0, GenericUtil.to_int(getattr(victim, "hit", 0), 0) - random.randint(1, 4))
        return self.damage_expr(ctx, str(damage), "DAM_HARM", dt="harm spell")

    def ventriloquate(self, ctx: SpellContext):
        text = str(ctx.target_name or "").strip()
        if not text:
            return ctx.fail("What voice do you wish to throw?\r\n")
        parts = text.split(" ", 1)
        speaker = parts[0]
        message = parts[1].strip() if len(parts) > 1 else ""
        if not message:
            return ctx.fail("What voice do you wish to throw?\r\n")
        return self.send(ctx, to_room=f"{speaker} says '{message}'.\r\n", include_victim_in_room=True) and ctx.mark_performed()

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
            "number_fuzzy": lambda value: max(1, GenericUtil.to_int(value, 0) + random.randint(-1, 1)),
            "UMAX": lambda a, b: max(GenericUtil.to_int(a, 0), GenericUtil.to_int(b, 0)),
            "UMIN": lambda a, b: min(GenericUtil.to_int(a, 0), GenericUtil.to_int(b, 0)),
            "abs": abs,
            "max": max,
            "min": min,
            "int": int,
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
            return EffectUtil.is_affected(target, name.upper())
        return False

    def _queue_damage_payload(self, ctx: SpellContext, payload: dict, victim):
        if not payload:
            return
        self.send(
            ctx,
            to_char=str(payload.get("to_char", "") or ""),
            to_room=str(payload.get("to_room", "") or ""),
            to_victim=str(payload.get("to_victim", "") or ""),
            victim=victim,
        )

    def _find_room_for_entity(self, entity):
        registry = self._room_registry(entity)
        if registry is None or not getattr(entity, "room_id", ""):
            return None
        return registry.get_or_none(id=getattr(entity, "room_id", ""))

    def _find_random_room(self, ctx: SpellContext):
        registry = self._room_registry(ctx)
        if registry is None:
            return None
        rooms = [room for room in registry.all_rooms() if room is not None and not self._room_flag(room, "ROOM_NO_RECALL")]
        return random.choice(rooms) if rooms else None

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

    def _move_character(
        self,
        ctx: SpellContext,
        victim,
        room,
        notify_victim: bool = False,
        line: str = "",
        from_room_line: str = "",
        to_room_line: str = "",
    ):
        current = self._find_room_for_entity(victim)
        if current is None or room is None or str(getattr(current, "id", "")) == str(getattr(room, "id", "")):
            return False
        exclude_ids = {str(getattr(victim, "id", "") or "")}
        if from_room_line:
            self._queue_room_text(ctx, current, from_room_line, exclude_ids=exclude_ids)
        if CharacterMacros.is_npc(victim):
            current.mobiles.pop(str(getattr(victim, "id", "")), None)
            room.add_mobile_to_room(victim)
        else:
            current.characters.pop(str(getattr(victim, "id", "")), None)
            room.add_player_to_room(victim)
        victim.room_id = room.id
        victim.area_id = getattr(room, "area_id", getattr(victim, "area_id", ""))
        if notify_victim and line:
            self.send(ctx, to_victim=line, victim=victim)
        if to_room_line:
            self._queue_room_text(ctx, room, to_room_line, exclude_ids=exclude_ids)
        if not CharacterMacros.is_npc(victim):
            payload = {"view_character": victim, "to_room_obj": room}
            if victim is ctx.actor:
                payload["aggressive_rounds"] = self._fight_handler(ctx).aggressive_entry_rounds(victim, room)
            ctx.queue_payload(payload)
        return ctx.mark_performed()

    def _spawn_portal(self, ctx: SpellContext, two_way: bool):
        victim = self._find_world_character(ctx, ctx.target_name)
        destination = self._find_room_for_entity(victim)
        if victim is None or destination is None or ctx.room is None or not self.create_object(ctx, "25"):
            return ctx.fail("You failed.\r\n")
        portal = ctx.get_alias("created_item")
        portal.timer = max(2, 1 + ctx.level // 10)
        portal.value3 = str(getattr(destination, "vnum", getattr(destination, "id", "")))
        if two_way and destination is not ctx.room:
            registry = getattr(getattr(ctx.handler, "registry_service", None), "item_registry", None)
            prototype = registry.get_or_none(vnum="25") if registry is not None else None
            if prototype is not None:
                second = ItemUtil.create_object(prototype)
                second.timer = portal.timer
                second.value3 = str(getattr(ctx.room, "vnum", ctx.room.id))
                destination.add_item_to_room(second)
        return True

    def _enchant_item(self, ctx: SpellContext, weapon: bool):
        obj = ctx.obj
        if obj is None:
            return ctx.fail("What should the spell be cast upon?\r\n")
        item_type = str(getattr(obj, "item_type", "") or "").upper()
        if weapon and "WEAPON" not in item_type:
            return ctx.fail("That item is not a weapon.\r\n")
        if not weapon and "ARMOR" not in item_type:
            return ctx.fail("That item is not armor.\r\n")
        effect = Effect(
            where="TO_OBJECT",
            type=getattr(ctx.spell, "handler_id", getattr(ctx.spell, "name", "spell")),
            level=ctx.level,
            duration=-1,
            location="APPLY_HITROLL" if weapon else "APPLY_AC",
            modifier=max(1, ctx.level // 10) if weapon else -max(1, ctx.level // 8),
            bitvector="0",
            apply_to="object",
        )
        EffectUtil.affect_to_obj(obj, effect)
        if weapon:
            EffectUtil.affect_to_obj(
                obj,
                Effect(
                    where="TO_OBJECT",
                    type=getattr(ctx.spell, "handler_id", getattr(ctx.spell, "name", "spell")),
                    level=ctx.level,
                    duration=-1,
                    location="APPLY_DAMROLL",
                    modifier=max(1, ctx.level // 12),
                    bitvector="0",
                    apply_to="object",
                ),
            )
        obj.level = max(GenericUtil.to_int(getattr(obj, "level", 0), 0), ctx.level)
        obj.enchanted = True
        return ctx.mark_performed()

    @staticmethod
    def _entity_name(entity) -> str:
        if entity is None:
            return "someone"
        if CharacterMacros.is_npc(entity):
            return str(getattr(entity, "short_description", "") or getattr(entity, "name", "someone"))
        return str(getattr(entity, "name", "someone"))

    @staticmethod
    def _alignment(entity) -> int:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            return GenericUtil.to_int(getattr(attrs, "alignment", 0), 0)
        perm = getattr(entity, "perm_stat", None)
        if perm is not None:
            return GenericUtil.to_int(getattr(perm, "alignment", 0), 0)
        return GenericUtil.to_int(getattr(entity, "alignment", 0), 0)

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
        flags = CharacterMacros.get_enum("roomFlags")
        bit = CharacterMacros.enum_bit(flags, flag_name)
        return bit > 0 and CharacterMacros.is_set(GenericUtil.to_int(getattr(room, "room_flags", 0), 0), bit)

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
        return CharacterMacros.is_npc(actor) == CharacterMacros.is_npc(entity)

    @staticmethod
    def _same_class(actor, entity) -> bool:
        if actor is None or entity is None or CharacterMacros.is_npc(entity):
            return False
        actor_class = str(getattr(getattr(actor, "character_class", None), "name", "") or "").strip().lower()
        entity_class = str(getattr(getattr(entity, "character_class", None), "name", "") or "").strip().lower()
        return bool(actor_class) and actor_class == entity_class

    @staticmethod
    def _room_combatants(room) -> list[Any]:
        fighting_pos = CharacterMacros.pos_value("POS_FIGHTING")
        fighters = []
        for entity in SpellApi._room_entities(room):
            position = GenericUtil.to_int(getattr(entity, "position", getattr(getattr(entity, "character_attributes", None), "position", 0)), 0)
            if getattr(entity, "fighting", None) is not None or position == fighting_pos:
                fighters.append(entity)
        return fighters

    @staticmethod
    def _owned_items(owner) -> list[Any]:
        items = list(getattr(owner, "loot", []) or [])
        equipped = getattr(owner, "equipped", None)
        if equipped is not None:
            for item in getattr(equipped, "__dict__", {}).values():
                if item is not None and item not in items:
                    items.append(item)
        return items

    def _remove_curse_item(self, ctx: SpellContext, item, owner: Any = None, quiet: bool = False) -> bool:
        item_flags = CharacterMacros.get_enum("itemFlags")
        nodrop = getattr(item_flags, "ITEM_NODROP", None)
        noremove = getattr(item_flags, "ITEM_NOREMOVE", None)
        nouncurse = getattr(item_flags, "ITEM_NOUNCURSE", None)
        raw_flags = GameMacros.flags_to_int(getattr(item, "extra_flags", 0))
        cursed = (nodrop is not None and GameMacros.is_set(raw_flags, nodrop.value)) or (noremove is not None and GameMacros.is_set(raw_flags, noremove.value))
        if not cursed:
            if quiet:
                return False
            return ctx.fail(f"There doesn't seem to be a curse on {ObjectUtils.short(item)}.\r\n")
        if nouncurse is not None and GameMacros.is_set(raw_flags, nouncurse.value):
            if quiet:
                return False
            return ctx.fail(f"The curse on {ObjectUtils.short(item)} is beyond your power.\r\n")
        if EffectUtil.saves_dispel(ctx.level + 2, GenericUtil.to_int(getattr(item, "level", 0), 0), 0):
            if quiet:
                return False
            return ctx.fail(f"The curse on {ObjectUtils.short(item)} is beyond your power.\r\n")
        if nodrop is not None:
            raw_flags = GameMacros.unset_bit(raw_flags, nodrop.value)
        if noremove is not None:
            raw_flags = GameMacros.unset_bit(raw_flags, noremove.value)
        item.extra_flags = GameMacros.flags_to_letters(raw_flags)
        if quiet:
            return True
        if owner is not None and owner is not ctx.actor:
            self.send(ctx, to_victim=f"Your {ObjectUtils.short(item)} glows blue.\r\n", victim=owner)
            self.send(ctx, to_room=f"{self._entity_name(owner)}'s {ObjectUtils.short(item)} glows blue.\r\n", victim=owner)
        else:
            self.send(ctx, to_char=f"{ObjectUtils.short(item)} glows blue.\r\n")
            self.send(ctx, to_room=f"{ObjectUtils.short(item)} glows blue.\r\n")
        return ctx.mark_performed()

    @staticmethod
    def _mob_has_act(entity, flag_name: str) -> bool:
        if entity is None or not CharacterMacros.is_npc(entity):
            return False
        act_bits = CharacterMacros.get_enum("actBits")
        bit = CharacterMacros.enum_bit(act_bits, flag_name)
        if bit <= 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(entity, "status_flags", None), "act", 0), 0)
        return CharacterMacros.is_set(flags, bit)

    @staticmethod
    def _mob_has_imm(entity, flag_name: str) -> bool:
        if entity is None or not CharacterMacros.is_npc(entity):
            return False
        flag_letters = CharacterMacros.get_enum("flagLetters")
        if not hasattr(flag_letters, flag_name):
            return False
        flags = GenericUtil.to_int(getattr(getattr(entity, "status_flags", None), "imm", 0), 0)
        return CharacterMacros.is_set(flags, getattr(flag_letters, flag_name).value)

    @staticmethod
    def _player_has_act(entity, flag_name: str) -> bool:
        if entity is None or CharacterMacros.is_npc(entity):
            return False
        act_bits = CharacterMacros.get_enum("playerActBits")
        if not hasattr(act_bits, flag_name):
            return False
        flags = GenericUtil.to_int(CharacterMacros.convert_flags(getattr(getattr(entity, "status_flags", None), "act", "") or "0"), 0)
        return CharacterMacros.is_set(flags, getattr(act_bits, flag_name).value)

    @staticmethod
    def _room_helper(ctx_or_entity):
        handler = getattr(ctx_or_entity, "handler", None)
        return getattr(handler, "room_helper", None) if handler is not None else None

    @staticmethod
    def _fight_handler(ctx_or_entity):
        handler = getattr(ctx_or_entity, "handler", None)
        return getattr(handler, "fight_handler", None) if handler is not None else None

    @staticmethod
    def _room_registry(ctx_or_entity):
        handler = getattr(ctx_or_entity, "handler", None)
        if handler is not None and getattr(handler, "room_registry", None) is not None:
            return handler.room_registry
        if handler is not None and getattr(getattr(handler, "registry_service", None), "room_registry", None) is not None:
            return handler.registry_service.room_registry
        return getattr(ctx_or_entity, "room_registry", None)

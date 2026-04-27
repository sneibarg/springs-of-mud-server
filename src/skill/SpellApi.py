from __future__ import annotations

import inspect
import random

from typing import Any, Iterable

from game.GenericUtil import GenericUtil
from interp.commands.FightUtil import FightUtil
from interp.commands.ObjectUtils import ObjectUtils
from object.Effect import Effect
from object.EffectUtil import EffectUtil
from object.ItemUtil import ItemUtil
from player.CharacterMacros import CharacterMacros
from player.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory
from skill.SpellContext import SpellContext


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
                self.logger.error(f"Spell lambda failed for {getattr(ctx.spell, 'name', '')}: {lambda_str} | {exc}", exc_info=True)
                return ctx.fail("Your spell fizzles and dies.\r\n")
            if ctx.done:
                break
        return bool(ctx.performed)

    def default_spell(self, ctx: SpellContext):
        if ctx.target is not None:
            EffectUtil.apply_spell_effects(ctx.actor, ctx.target, ctx.spell)
        return ctx.mark_performed()

    @staticmethod
    def merge_player_payloads(ctx: SpellContext) -> dict:
        payload = {"to_char": "", "to_room": "", "targets": [], "victim": None, "to_victim": ""}
        seen_targets = set()
        for entry in ctx.payloads:
            payload["to_char"] += str(entry.get("to_char", "") or "")
            payload["to_room"] += str(entry.get("to_room", "") or "")
            for target in entry.get("targets", []) or []:
                target_id = str(getattr(target, "id", "") or "")
                if target_id and target_id not in seen_targets:
                    seen_targets.add(target_id)
                    payload["targets"].append(target)
            if payload["victim"] is None and entry.get("victim") is not None and entry.get("to_victim"):
                payload["victim"] = entry["victim"]
                payload["to_victim"] = str(entry.get("to_victim", "") or "")
        return payload

    def queue_cast_announcement(self, ctx: SpellContext):
        spell_label = str(getattr(ctx.spell, "name", "spell") or "spell")
        actor_name = self._entity_name(ctx.actor)
        room_targets = self._room_players(ctx.room, exclude_ids={str(getattr(ctx.actor, "id", ""))})
        victim = ctx.target if self._is_character(ctx.target) else None

        payload = {
            "to_char": f"You cast {spell_label}" + (f" on {self._entity_name(victim)}" if victim is not None and victim is not ctx.actor else "") + ".\r\n",
            "to_room": f"{actor_name} casts {spell_label}" + (f" on {self._entity_name(victim)}" if victim is not None and victim is not ctx.actor else "") + ".\r\n",
            "targets": room_targets,
        }
        if victim is not None and victim is not ctx.actor and not CharacterMacros.is_npc(victim):
            payload["victim"] = victim
            payload["to_victim"] = f"{actor_name} casts {spell_label} on you.\r\n"
        ctx.payloads.insert(0, payload)

    def start_offensive_combat(self, ctx: SpellContext):
        target_type = str(getattr(ctx.spell, "target", "") or "").upper()
        victim = ctx.target if self._is_character(ctx.target) else None
        if victim is None:
            return
        if target_type not in ("CHAR_OFFENSIVE", "OBJ_CHAR_OFF"):
            return
        if victim is ctx.actor:
            return
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return
        if getattr(ctx.actor, "fighting", None) is None:
            self._fight_handler(ctx).set_fighting(ctx.actor, victim, room.id)
        if getattr(victim, "fighting", None) is None:
            self._fight_handler(ctx).set_fighting(victim, ctx.actor, room.id)

    def effect_to_char(self, ctx: SpellContext, text: str):
        if text and ctx.source == "player" and not CharacterMacros.is_npc(ctx.actor):
            ctx.queue_payload({"to_char": str(text)})
        return True

    def effect_to_victim(self, ctx: SpellContext, text: str, victim=None):
        target = victim or (ctx.target if self._is_character(ctx.target) else None)
        if text and target is not None and not CharacterMacros.is_npc(target):
            ctx.queue_payload({"victim": target, "to_victim": str(text)})
        return True

    def effect_to_room(self, ctx: SpellContext, text: str, victim=None):
        target = victim or (ctx.target if self._is_character(ctx.target) else None)
        exclude = {str(getattr(ctx.actor, "id", "") or "")}
        if target is not None:
            exclude.add(str(getattr(target, "id", "") or ""))
        targets = self._room_players(ctx.room, exclude_ids=exclude)
        if text and targets:
            ctx.queue_payload({"to_room": str(text), "targets": targets})
        return True

    def apply_affect_data(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None:
            return False
        EffectUtil.apply_spell_effects(ctx.actor, victim, ctx.spell)
        return ctx.mark_performed()

    def remove_effects(self, ctx: SpellContext, *effect_names: str, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None:
            return False
        for effect_name in effect_names:
            handler_id = FightUtil.spell_handler_name(effect_name.replace("spell.", "").replace("_", " ").replace(".", " "))
            EffectUtil.affect_strip(victim, handler_id)
            EffectUtil.affect_strip(victim, effect_name)
        return ctx.mark_performed()

    def dispel_effects(self, ctx: SpellContext, *effect_names: str, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None:
            return False
        removed = False
        for effect_name in effect_names:
            removed = EffectUtil.check_dispel(ctx.level, victim, effect_name) or removed
        if removed:
            ctx.mark_performed()
        return removed

    def damage_expr(self, ctx: SpellContext, expression: str, dam_type: str = "DAM_NONE", save_half: bool = True, save_level_adjust: int = 0, target: Any = None, dt: str = ""):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        damage = self.eval_int(ctx, expression, victim=victim)
        if save_half and EffectUtil.saves_spell(ctx.level + int(save_level_adjust), victim, 0):
            damage //= 2
        payload = self._fight_handler(ctx).damage(ctx.actor, victim, damage, dt=dt or getattr(ctx.spell, "noun_damage", "") or getattr(ctx.spell, "name", "spell"), dam_type=dam_type)
        self._queue_damage_payload(ctx, payload, victim)
        return ctx.mark_performed()

    def damage_fixed(self, ctx: SpellContext, amount: int, dam_type: str = "DAM_NONE", save_half: bool = True, target: Any = None, dt: str = ""):
        return self.damage_expr(ctx, str(int(amount)), dam_type=dam_type, save_half=save_half, target=target, dt=dt)

    def damage_room_expr(self, ctx: SpellContext, expression: str, dam_type: str = "DAM_NONE", save_half: bool = True, skip_actor: bool = True):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        acted = False
        for victim in self._room_entities(room):
            if skip_actor and victim is ctx.actor:
                continue
            if self._fight_handler(ctx).is_safe_spell(ctx.actor, victim, area=True):
                continue
            damage = self.eval_int(ctx, expression, victim=victim)
            if save_half and EffectUtil.saves_spell(ctx.level, victim, 0):
                damage //= 2
            payload = self._fight_handler(ctx).damage(ctx.actor, victim, damage, dt=getattr(ctx.spell, "noun_damage", "") or getattr(ctx.spell, "name", "spell"), dam_type=dam_type)
            self._queue_damage_payload(ctx, payload, victim)
            acted = True
        if acted:
            ctx.mark_performed()
        return acted

    def heal_expr(self, ctx: SpellContext, expression: str, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        amount = max(0, self.eval_int(ctx, expression, victim=victim))
        field = "hit" if hasattr(victim, "hit") else "hp"
        current = GenericUtil.to_int(getattr(victim, field, 0), 0)
        maximum = GenericUtil.to_int(getattr(victim, "max_hit", current), current)
        setattr(victim, field, min(maximum, current + amount))
        ctx.mark_performed()
        return True

    def restore_move_expr(self, ctx: SpellContext, expression: str, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        amount = max(0, self.eval_int(ctx, expression, victim=victim))
        current = GenericUtil.to_int(getattr(victim, "movement", getattr(victim, "move", 0)), 0)
        maximum = GenericUtil.to_int(getattr(victim, "max_movement", getattr(victim, "max_move", current)), current)
        updated = min(maximum, current + amount)
        if hasattr(victim, "movement"):
            victim.movement = updated
        if hasattr(victim, "move"):
            victim.move = updated
        ctx.mark_performed()
        return True

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
        obj = ctx.target if self._is_object(ctx.target) else None
        if obj is None:
            return ctx.fail("What should the spell be cast upon?\r\n")
        item_type = str(getattr(obj, "item_type", "") or "").upper()
        if "DRINK" not in item_type and "FOUNTAIN" not in item_type:
            return ctx.fail("It is unable to hold water.\r\n")
        total = GenericUtil.to_int(getattr(obj, "value0", 0), 0)
        current = GenericUtil.to_int(getattr(obj, "value1", 0), 0)
        amount = max(1, ctx.level * 2)
        obj.value1 = str(min(total or amount, current + amount))
        obj.value2 = "0"
        return ctx.mark_performed()

    def detect_poison(self, ctx: SpellContext):
        obj = ctx.target if self._is_object(ctx.target) else None
        if obj is None:
            return ctx.fail("What should the spell be cast upon?\r\n")
        poisoned = False
        if "FOOD" in str(getattr(obj, "item_type", "") or "").upper():
            poisoned = GenericUtil.to_int(getattr(obj, "value3", 0), 0) != 0
        elif "DRINK" in str(getattr(obj, "item_type", "") or "").upper() or "FOUNTAIN" in str(getattr(obj, "item_type", "") or "").upper():
            poisoned = GenericUtil.to_int(getattr(obj, "value3", 0), 0) != 0
        message = "You smell poisonous fumes.\r\n" if poisoned else "It looks delicious.\r\n"
        ctx.queue_payload({"to_char": message})
        return ctx.mark_performed()

    def identify(self, ctx: SpellContext):
        target = ctx.target
        if target is None:
            return ctx.fail("You failed to identify anything.\r\n")
        if self._is_object(target):
            text = [
                f"Object '{getattr(target, 'short_description', getattr(target, 'name', 'item'))}'.\r\n",
                f"Item type: {getattr(target, 'item_type', 'unknown')}.\r\n",
                f"Level {getattr(target, 'level', 0)}, weight {getattr(target, 'weight', 0)}, value {getattr(target, 'cost', 0)}.\r\n",
            ]
            ctx.queue_payload({"to_char": "".join(text)})
        else:
            alignment = self._alignment(target)
            ctx.queue_payload({"to_char": f"{self._entity_name(target)} is level {getattr(target, 'level', 0)} with alignment {alignment}.\r\n"})
        return ctx.mark_performed()

    def locate_object(self, ctx: SpellContext):
        registry = getattr(ctx.handler, "room_registry", None) or getattr(getattr(ctx.handler, "registry_service", None), "room_registry", None)
        if registry is None:
            return False
        wanted = str(ctx.target_name or "").strip().lower()
        if not wanted:
            return ctx.fail("Locate what?\r\n")
        lines = []
        found = 0
        for room in registry.all_rooms():
            for obj in getattr(room, "contents", {}).values():
                name = str(getattr(obj, "name", "") or "").lower()
                if wanted in name:
                    lines.append(f"{getattr(obj, 'short_description', obj.name)} is in {getattr(room, 'name', 'somewhere')}.\r\n")
                    found += 1
                    if found >= max(2, ctx.level // 2):
                        break
            if found >= max(2, ctx.level // 2):
                break
        ctx.queue_payload({"to_char": "".join(lines) if lines else "Nothing like that is in heaven or earth.\r\n"})
        return ctx.mark_performed()

    def teleport_target(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        room = self._find_random_room(ctx, victim)
        if room is None:
            return ctx.fail("You failed.\r\n")
        return self._move_character(ctx, victim, room, notify_victim=victim is not ctx.actor, line="You have been teleported!\r\n")

    def summon_target(self, ctx: SpellContext):
        victim = self._find_world_character(ctx, ctx.target_name)
        if victim is None or victim is ctx.actor:
            return ctx.fail("You failed.\r\n")
        if ctx.room is None:
            return ctx.fail("You failed.\r\n")
        return self._move_character(ctx, victim, ctx.room, notify_victim=True, line=f"{self._entity_name(ctx.actor)} has summoned you!\r\n")

    def word_of_recall(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or CharacterMacros.is_npc(victim):
            return False
        room_registry = getattr(ctx.handler, "room_registry", None) or getattr(getattr(ctx.handler, "registry_service", None), "room_registry", None)
        temple = room_registry.get_or_none(vnum="3001") if room_registry is not None else None
        if temple is None:
            return ctx.fail("You are completely lost.\r\n")
        if getattr(victim, "fighting", None) is not None:
            self._fight_handler(ctx).stop_fighting(victim, both=True)
        victim.move = max(0, GenericUtil.to_int(getattr(victim, "move", getattr(victim, "movement", 0)), 0) // 2)
        if hasattr(victim, "movement"):
            victim.movement = max(0, GenericUtil.to_int(getattr(victim, "movement", 0), 0) // 2)
        return self._move_character(ctx, victim, temple)

    def gate(self, ctx: SpellContext):
        victim = self._find_world_character(ctx, ctx.target_name)
        if victim is None or victim is ctx.actor or getattr(victim, "room_id", "") == getattr(ctx.actor, "room_id", ""):
            return ctx.fail("You failed.\r\n")
        room = self._find_room_for_entity(victim)
        if room is None:
            return ctx.fail("You failed.\r\n")
        return self._move_character(ctx, ctx.actor, room)

    def portal(self, ctx: SpellContext):
        return self._spawn_portal(ctx, two_way=False)

    def nexus(self, ctx: SpellContext):
        return self._spawn_portal(ctx, two_way=True)

    def farsight(self, ctx: SpellContext):
        target = self._find_world_character(ctx, ctx.target_name)
        room = self._find_room_for_entity(target) if target is not None else None
        if room is None:
            return ctx.fail("You can't see that far.\r\n")
        ctx.queue_payload({"to_char": f"You gaze toward {self._entity_name(target)} in {getattr(room, 'name', 'somewhere')}.\r\n"})
        return ctx.mark_performed()

    def control_weather(self, ctx: SpellContext):
        weather = getattr(ctx.handler, "weather_handler", None)
        if weather is None or getattr(weather, "weather_info", None) is None:
            return False
        direction = -1 if str(ctx.target_name or "").strip().lower() in ("better", "clear", "sunny") else 1
        weather.weather_info.change += 5 * direction
        weather.weather_info.mmhg += 10 * direction
        return ctx.mark_performed()

    def know_alignment(self, ctx: SpellContext):
        victim = ctx.target if self._is_character(ctx.target) else None
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
        ctx.queue_payload({"to_char": text})
        return ctx.mark_performed()

    def recharge(self, ctx: SpellContext):
        obj = ctx.target if self._is_object(ctx.target) else None
        if obj is None:
            return ctx.fail("What should the spell be cast upon?\r\n")
        item_type = str(getattr(obj, "item_type", "") or "").upper()
        if "WAND" not in item_type and "STAFF" not in item_type:
            return ctx.fail("That item does not hold magical charges.\r\n")
        max_charges = GenericUtil.to_int(getattr(obj, "value1", 0), 0)
        current = GenericUtil.to_int(getattr(obj, "value2", 0), 0)
        restored = max(1, ctx.level // 8)
        obj.value2 = str(min(max_charges, current + restored))
        return ctx.mark_performed()

    def enchant_weapon(self, ctx: SpellContext):
        return self._enchant_item(ctx, weapon=True)

    def enchant_armor(self, ctx: SpellContext):
        return self._enchant_item(ctx, weapon=False)

    def fireproof(self, ctx: SpellContext):
        return self.apply_affect_data(ctx)

    def mass_invis(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        for entity in self._room_entities(room):
            if getattr(entity, "fighting", None) is not None:
                continue
            EffectUtil.apply_spell_effects(ctx.actor, entity, ctx.spell)
        return ctx.mark_performed()

    def mass_healing(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        for entity in self._room_entities(room):
            if not self._is_character(entity):
                continue
            self.heal_expr(ctx, "100 + dice(3, 8)", target=entity)
            self.remove_effects(ctx, "spell.blindness", "spell.poison", "spell.plague", target=entity)
        return ctx.mark_performed()

    def calm(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        for entity in self._room_entities(room):
            if getattr(entity, "fighting", None) is not None:
                self._fight_handler(ctx).stop_fighting(entity, both=False)
            EffectUtil.apply_spell_effects(ctx.actor, entity, ctx.spell)
        return ctx.mark_performed()

    def chain_lightning(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        first = ctx.target if self._is_character(ctx.target) else None
        if room is None or first is None:
            return ctx.fail("Cast the spell on whom?\r\n")
        damage = max(1, ctx.level * 4)
        victims = [first] + [entity for entity in self._room_entities(room) if entity not in (ctx.actor, first)]
        for victim in victims:
            payload = self._fight_handler(ctx).damage(ctx.actor, victim, damage, dt=getattr(ctx.spell, "noun_damage", "lightning"), dam_type="DAM_LIGHTNING")
            self._queue_damage_payload(ctx, payload, victim)
            damage = max(1, damage // 2)
        return ctx.mark_performed()

    def holy_word(self, ctx: SpellContext):
        room = ctx.room or self._find_room_for_entity(ctx.actor)
        if room is None:
            return False
        actor_alignment = self._alignment(ctx.actor)
        if abs(actor_alignment) < 350:
            return ctx.fail("You utter a word of no power.\r\n")
        for victim in self._room_entities(room):
            if victim is ctx.actor:
                self.heal_expr(ctx, "100", target=victim)
                continue
            target_alignment = self._alignment(victim)
            if actor_alignment > 0 and target_alignment < 0:
                self.damage_expr(ctx, "dice(level, 4) + 50", "DAM_HOLY", target=victim, dt="divine wrath")
                self.spell_blindness(ctx, target=victim)
                self.spell_curse(ctx, target=victim)
            elif actor_alignment > 0:
                self.heal_expr(ctx, "50", target=victim)
            elif actor_alignment < 0 and target_alignment > 0:
                self.damage_expr(ctx, "dice(level, 4) + 50", "DAM_NEGATIVE", target=victim, dt="divine wrath")
                self.spell_blindness(ctx, target=victim)
                self.spell_curse(ctx, target=victim)
            elif actor_alignment < 0:
                self.heal_expr(ctx, "50", target=victim)
        return ctx.mark_performed()

    def heat_metal(self, ctx: SpellContext):
        victim = ctx.target if self._is_character(ctx.target) else None
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
        victim = ctx.target if self._is_character(ctx.target) else None
        if victim is None:
            return False
        if EffectUtil.saves_spell(ctx.level, victim, 0):
            return self.damage_expr(ctx, "1", "DAM_NEGATIVE", save_half=False, target=victim, dt="energy drain")
        victim.level = max(1, GenericUtil.to_int(getattr(victim, "level", 1), 1) - 1)
        victim.hit = max(1, GenericUtil.to_int(getattr(victim, "hit", 1), 1) - ctx.level)
        if hasattr(victim, "mana"):
            victim.mana = max(0, GenericUtil.to_int(getattr(victim, "mana", 0), 0) - ctx.level)
        ctx.actor.hit = min(GenericUtil.to_int(getattr(ctx.actor, "max_hit", getattr(ctx.actor, "hit", 0)), 0), GenericUtil.to_int(getattr(ctx.actor, "hit", 0), 0) + ctx.level)
        return self.damage_expr(ctx, "ctx.level", "DAM_NEGATIVE", save_half=False, target=victim, dt="energy drain")

    def ray_of_truth(self, ctx: SpellContext):
        victim = ctx.target if self._is_character(ctx.target) else None
        if victim is None:
            return False
        alignment = self._alignment(victim)
        if alignment < -350:
            ctx.queue_payload({"to_char": f"{self._entity_name(victim)} is unaffected by your ray of truth.\r\n"})
            return ctx.mark_performed()
        damage = max(1, ctx.level * 10 - alignment // 10)
        return self.damage_fixed(ctx, damage, "DAM_HOLY", save_half=False, target=victim, dt="ray of truth")

    def change_sex(self, ctx: SpellContext):
        victim = ctx.target if self._is_character(ctx.target) else None
        if victim is None:
            return False
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
        affected = CharacterMacros.get_enum("affectedBy")
        invis = CharacterMacros.enum_bit(affected, "AFF_INVISIBLE")
        hide = CharacterMacros.enum_bit(affected, "AFF_HIDE")
        for victim in self._room_entities(room):
            if victim is ctx.actor:
                continue
            raw = GenericUtil.to_int(CharacterMacros.convert_flags(getattr(getattr(victim, "character_flags", None), "affected_by", "") or ""), 0) if hasattr(victim, "character_flags") else GenericUtil.to_int(getattr(getattr(victim, "mobile_flags", None), "affected_by", 0), 0)
            if invis and CharacterMacros.is_set(raw, invis):
                EffectUtil.affect_strip(victim, "spell.invis")
            if hide and CharacterMacros.is_set(raw, hide):
                EffectUtil.affect_strip(victim, "AFF_HIDE")
            EffectUtil.apply_spell_effects(ctx.actor, victim, ctx.spell)
        return ctx.mark_performed()

    def dispel_magic(self, ctx: SpellContext):
        victim = ctx.target if self._is_character(ctx.target) else None
        if victim is None:
            return False
        removed = False
        for effect_name in self.DISPEL_EFFECTS:
            removed = EffectUtil.check_dispel(ctx.level, victim, effect_name) or removed
        if not removed:
            ctx.queue_payload({"to_char": "Spell failed.\r\n"})
        return ctx.mark_performed() if removed else False

    def cancellation(self, ctx: SpellContext):
        return self.dispel_magic(ctx)

    def remove_curse(self, ctx: SpellContext):
        target = ctx.target
        if self._is_object(target):
            flags = str(getattr(target, "extra_flags", "") or "")
            target.extra_flags = flags
            return ctx.mark_performed()
        return self.dispel_effects(ctx, "spell.curse", target=target)

    def curse(self, ctx: SpellContext, target: Any = None):
        return self.spell_curse(ctx, target=target)

    def bless(self, ctx: SpellContext, target: Any = None):
        return self.spell_bless(ctx, target=target)

    def blindness(self, ctx: SpellContext, target: Any = None):
        return self.spell_blindness(ctx, target=target)

    def poison(self, ctx: SpellContext, target: Any = None):
        return self.spell_poison(ctx, target=target)

    def sleep(self, ctx: SpellContext, target: Any = None):
        return self.spell_sleep(ctx, target=target)

    def weaken(self, ctx: SpellContext, target: Any = None):
        return self.spell_weaken(ctx, target=target)

    def slow(self, ctx: SpellContext, target: Any = None):
        return self.spell_slow(ctx, target=target)

    def charm_person(self, ctx: SpellContext, target: Any = None):
        return self.spell_charm_person(ctx, target=target)

    def cure_blindness(self, ctx: SpellContext):
        return self.remove_effects(ctx, "spell.blindness")

    def cure_poison(self, ctx: SpellContext):
        return self.remove_effects(ctx, "spell.poison")

    def cure_disease(self, ctx: SpellContext):
        return self.remove_effects(ctx, "spell.plague")

    def spell_armor(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.armor", "You are already armored.\r\n")

    def spell_bless(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if self._is_object(victim):
            return self.apply_affect_data(ctx, target=victim)
        return self._apply_named_affect_spell(ctx, "spell.bless", "You are already blessed.\r\n", target=victim)

    def spell_blindness(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        if CharacterMacros.is_affected_by_name(victim, CharacterMacros.get_enum("affectedBy"), "AFF_BLIND"):
            return False
        if EffectUtil.saves_spell(ctx.level, victim, 0):
            return False
        return self.apply_affect_data(ctx, target=victim)

    def spell_charm_person(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        if victim is ctx.actor:
            return ctx.fail("You like yourself even better!\r\n")
        if EffectUtil.saves_spell(ctx.level, victim, 0):
            return False
        return self.apply_affect_data(ctx, target=victim)

    def spell_sleep(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        if CharacterMacros.is_affected_by_name(victim, CharacterMacros.get_enum("affectedBy"), "AFF_SLEEP"):
            return False
        if EffectUtil.saves_spell(max(1, ctx.level - 4), victim, 0):
            return False
        if self.apply_affect_data(ctx, target=victim):
            if hasattr(victim, "position"):
                victim.position = CharacterMacros.pos_value("POS_SLEEPING")
            elif hasattr(getattr(victim, "character_attributes", None), "position"):
                victim.character_attributes.position = CharacterMacros.pos_value("POS_SLEEPING")
            return True
        return False

    def spell_poison(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if self._is_object(victim):
            return self.apply_affect_data(ctx, target=victim)
        if victim is None or not self._is_character(victim):
            return False
        if EffectUtil.saves_spell(ctx.level, victim, 0):
            return False
        effect = Effect(where="TO_AFFECTS", type=getattr(ctx.spell, "handler_id", getattr(ctx.spell, "name", "spell")), level=ctx.level, duration=max(1, ctx.level // 2), location="APPLY_STR", modifier=-2, bitvector="AFF_POISON", apply_to="char")
        EffectUtil.affect_join(victim, effect)
        return ctx.mark_performed()

    def spell_weaken(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        if EffectUtil.saves_spell(ctx.level, victim, 0):
            return False
        return self.apply_affect_data(ctx, target=victim)

    def spell_slow(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None or not self._is_character(victim):
            return False
        if CharacterMacros.is_affected_by_name(victim, CharacterMacros.get_enum("affectedBy"), "AFF_HASTE"):
            self.dispel_effects(ctx, "spell.haste", target=victim)
            return ctx.mark_performed()
        if EffectUtil.saves_spell(ctx.level, victim, 0):
            return False
        return self.apply_affect_data(ctx, target=victim)

    def spell_curse(self, ctx: SpellContext, target: Any = None):
        victim = target if target is not None else ctx.target
        if self._is_object(victim):
            return self.apply_affect_data(ctx, target=victim)
        return self.apply_affect_data(ctx, target=victim)

    def spell_acid_blast(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 12)", "DAM_ACID")

    def spell_burning_hands(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 7)", "DAM_FIRE")

    def spell_call_lightning(self, ctx: SpellContext):
        weather = getattr(ctx.handler, "weather_handler", None)
        if weather is None or getattr(weather, "weather_info", None) is None:
            return ctx.fail("You failed.\r\n")
        return self.damage_room_expr(ctx, "dice(level, 4) + level // 2", "DAM_LIGHTNING")

    def spell_calm(self, ctx: SpellContext):
        return self.calm(ctx)

    def spell_cancellation(self, ctx: SpellContext):
        return self.cancellation(ctx)

    def spell_cause_light(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(1, 8) + level // 3", "DAM_HARM")

    def spell_cause_serious(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(2, 8) + level // 2", "DAM_HARM")

    def spell_cause_critical(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(3, 8) + level - 6", "DAM_HARM")

    def spell_chain_lightning(self, ctx: SpellContext):
        return self.chain_lightning(ctx)

    def spell_change_sex(self, ctx: SpellContext):
        return self.change_sex(ctx)

    def spell_chill_touch(self, ctx: SpellContext):
        if self.damage_expr(ctx, "dice(level, 5)", "DAM_COLD"):
            victim = ctx.target
            if victim is not None and not EffectUtil.saves_spell(ctx.level, victim, 0):
                effect = Effect(where="TO_AFFECTS", type=getattr(ctx.spell, "handler_id", ctx.spell.name), level=ctx.level, duration=6, location="APPLY_STR", modifier=-1, bitvector="0", apply_to="char")
                EffectUtil.affect_join(victim, effect)
            return True
        return False

    def spell_colour_spray(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 6)", "DAM_LIGHT")

    def spell_continual_light(self, ctx: SpellContext):
        return self.create_object(ctx, "21")

    def spell_control_weather(self, ctx: SpellContext):
        return self.control_weather(ctx)

    def spell_create_food(self, ctx: SpellContext):
        return self.create_object(ctx, "20")

    def spell_create_rose(self, ctx: SpellContext):
        return self.create_object(ctx, "1001")

    def spell_create_spring(self, ctx: SpellContext):
        return self.create_object(ctx, "22")

    def spell_create_water(self, ctx: SpellContext):
        return self.create_water(ctx)

    def spell_cure_blindness(self, ctx: SpellContext):
        return self.cure_blindness(ctx)

    def spell_cure_critical(self, ctx: SpellContext):
        return self.heal_expr(ctx, "dice(3, 8) + level - 6")

    def spell_cure_disease(self, ctx: SpellContext):
        return self.cure_disease(ctx)

    def spell_cure_light(self, ctx: SpellContext):
        return self.heal_expr(ctx, "dice(1, 8) + level // 3")

    def spell_cure_poison(self, ctx: SpellContext):
        return self.cure_poison(ctx)

    def spell_cure_serious(self, ctx: SpellContext):
        return self.heal_expr(ctx, "dice(2, 8) + level // 2")

    def spell_demonfire(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 4) + 20", "DAM_NEGATIVE")

    def spell_detect_evil(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.detect_evil", "You can already sense evil.\r\n")

    def spell_detect_good(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.detect_good", "You can already sense good.\r\n")

    def spell_detect_hidden(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.detect_hidden", "You can already see hidden things.\r\n")

    def spell_detect_invis(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.detect_invis", "You can already see invisible things.\r\n")

    def spell_detect_magic(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.detect_magic", "You can already sense magic.\r\n")

    def spell_detect_poison(self, ctx: SpellContext):
        return self.detect_poison(ctx)

    def spell_dispel_evil(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 4)", "DAM_HOLY")

    def spell_dispel_good(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 4)", "DAM_NEGATIVE")

    def spell_dispel_magic(self, ctx: SpellContext):
        return self.dispel_magic(ctx)

    def spell_earthquake(self, ctx: SpellContext):
        return self.damage_room_expr(ctx, "level + dice(2, 8)", "DAM_BASH")

    def spell_enchant_armor(self, ctx: SpellContext):
        return self.enchant_armor(ctx)

    def spell_enchant_weapon(self, ctx: SpellContext):
        return self.enchant_weapon(ctx)

    def spell_energy_drain(self, ctx: SpellContext):
        return self.energy_drain(ctx)

    def spell_faerie_fire(self, ctx: SpellContext):
        return self.apply_affect_data(ctx)

    def spell_faerie_fog(self, ctx: SpellContext):
        return self.faerie_fog(ctx)

    def spell_farsight(self, ctx: SpellContext):
        return self.farsight(ctx)

    def spell_fireball(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 10)", "DAM_FIRE")

    def spell_fireproof(self, ctx: SpellContext):
        return self.fireproof(ctx)

    def spell_flamestrike(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(6, 8) + level", "DAM_FIRE")

    def spell_floating_disc(self, ctx: SpellContext):
        return self.create_object(ctx, "23")

    def spell_fly(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.fly", "You are already airborne.\r\n")

    def spell_frenzy(self, ctx: SpellContext):
        return self.apply_affect_data(ctx)

    def spell_frost_breath(self, ctx: SpellContext):
        return self.damage_room_expr(ctx, "dice(level, 16)", "DAM_COLD")

    def spell_gas_breath(self, ctx: SpellContext):
        return self.damage_room_expr(ctx, "dice(level, 12)", "DAM_POISON")

    def spell_gate(self, ctx: SpellContext):
        return self.gate(ctx)

    def spell_general_purpose(self, ctx: SpellContext):
        return self.damage_expr(ctx, "number_range(25, 100)", "DAM_PIERCE")

    def spell_giant_strength(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.giant_strength", "You are already as strong as a giant.\r\n")

    def spell_harm(self, ctx: SpellContext):
        victim = ctx.target
        if victim is None:
            return False
        damage = max(0, GenericUtil.to_int(getattr(victim, "hit", 0), 0) - random.randint(1, 4))
        return self.damage_fixed(ctx, damage, "DAM_HARM", save_half=True, dt="harm spell")

    def spell_haste(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.haste", "You can't move any faster!\r\n")

    def spell_heal(self, ctx: SpellContext):
        return self.heal_expr(ctx, "100")

    def spell_heat_metal(self, ctx: SpellContext):
        return self.heat_metal(ctx)

    def spell_high_explosive(self, ctx: SpellContext):
        return self.damage_expr(ctx, "number_range(30, 120)", "DAM_PIERCE")

    def spell_holy_word(self, ctx: SpellContext):
        return self.holy_word(ctx)

    def spell_identify(self, ctx: SpellContext):
        return self.identify(ctx)

    def spell_infravision(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.infravision", "You can already see in the dark.\r\n")

    def spell_invis(self, ctx: SpellContext):
        return self.apply_affect_data(ctx)

    def spell_know_alignment(self, ctx: SpellContext):
        return self.know_alignment(ctx)

    def spell_lightning_bolt(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 7)", "DAM_LIGHTNING")

    def spell_lightning_breath(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 20)", "DAM_LIGHTNING")

    def spell_locate_object(self, ctx: SpellContext):
        return self.locate_object(ctx)

    def spell_magic_missile(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 4)", "DAM_ENERGY")

    def spell_mass_healing(self, ctx: SpellContext):
        return self.mass_healing(ctx)

    def spell_mass_invis(self, ctx: SpellContext):
        return self.mass_invis(ctx)

    def spell_nexus(self, ctx: SpellContext):
        return self.nexus(ctx)

    def spell_pass_door(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.pass_door", "You are already out of phase.\r\n")

    def spell_plague(self, ctx: SpellContext):
        return self.apply_affect_data(ctx)

    def spell_portal(self, ctx: SpellContext):
        return self.portal(ctx)

    def spell_protection_evil(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.protection_evil", "You are already protected from evil.\r\n")

    def spell_protection_good(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.protection_good", "You are already protected from good.\r\n")

    def spell_ray_of_truth(self, ctx: SpellContext):
        return self.ray_of_truth(ctx)

    def spell_recharge(self, ctx: SpellContext):
        return self.recharge(ctx)

    def spell_refresh(self, ctx: SpellContext):
        return self.restore_move_expr(ctx, "level")

    def spell_remove_curse(self, ctx: SpellContext):
        return self.remove_curse(ctx)

    def spell_sanctuary(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.sanctuary", "You are already in sanctuary.\r\n")

    def spell_shield(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.shield", "You are already shielded from harm.\r\n")

    def spell_shocking_grasp(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 5)", "DAM_LIGHTNING")

    def spell_slow(self, ctx: SpellContext):
        return self.slow(ctx)

    def spell_stone_skin(self, ctx: SpellContext):
        return self._apply_named_affect_spell(ctx, "spell.stone_skin", "Your skin is already as hard as a rock.\r\n")

    def spell_summon(self, ctx: SpellContext):
        return self.summon_target(ctx)

    def spell_teleport(self, ctx: SpellContext):
        return self.teleport_target(ctx)

    def spell_ventriloquate(self, ctx: SpellContext):
        speaker = (ctx.target_name or "Someone").split(" ", 1)[0]
        message = ctx.target_name[len(speaker):].strip() if ctx.target_name else ""
        if not message:
            return ctx.fail("What voice do you wish to throw?\r\n")
        room_targets = self._room_players(ctx.room, exclude_ids={str(getattr(ctx.actor, "id", ""))})
        if room_targets:
            ctx.queue_payload({"to_room": f"{speaker} says '{message}'.\r\n", "targets": room_targets})
        return ctx.mark_performed()

    def spell_weaken(self, ctx: SpellContext):
        return self.weaken(ctx)

    def spell_word_of_recall(self, ctx: SpellContext):
        return self.word_of_recall(ctx)

    def spell_acid_breath(self, ctx: SpellContext):
        return self.damage_expr(ctx, "dice(level, 16)", "DAM_ACID")

    def spell_fire_breath(self, ctx: SpellContext):
        return self.damage_room_expr(ctx, "dice(level, 20)", "DAM_FIRE")

    def _apply_named_affect_spell(self, ctx: SpellContext, effect_name: str, already_message: str = "", target: Any = None):
        victim = target if target is not None else ctx.target
        if victim is None:
            return False
        if not self._is_object(victim) and any(str(getattr(effect, "type", "")).strip().lower() == effect_name for effect in getattr(victim, "effects", []) or []):
            return ctx.fail(already_message) if already_message else False
        return self.apply_affect_data(ctx, target=victim)

    def _queue_damage_payload(self, ctx: SpellContext, payload: dict, victim):
        if not payload:
            return
        queued = {
            "to_char": str(payload.get("to_char", "") or ""),
            "to_room": str(payload.get("to_room", "") or ""),
            "targets": self._room_players(ctx.room, exclude_ids={str(getattr(ctx.actor, "id", "")), str(getattr(victim, "id", ""))}),
        }
        if victim is not None and not CharacterMacros.is_npc(victim):
            queued["victim"] = victim
            queued["to_victim"] = str(payload.get("to_victim", "") or "")
        ctx.queue_payload(queued)

    def _find_room_for_entity(self, entity):
        return self._room_registry(entity).get_or_none(id=getattr(entity, "room_id", "")) if getattr(entity, "room_id", "") else None

    def _find_random_room(self, ctx: SpellContext, victim):
        rooms = [room for room in self._room_registry(ctx).all_rooms() if room is not None and not self._room_flag(room, "ROOM_NO_RECALL")]
        return random.choice(rooms) if rooms else None

    def _find_world_character(self, ctx: SpellContext, name: str):
        wanted = str(name or "").strip()
        if not wanted:
            return None
        for room in self._room_registry(ctx).all_rooms():
            target = PlayerUtil.get_target(ctx.actor, wanted, room, self._room_helper(ctx))
            if target is not None:
                return target
        return None

    def _move_character(self, ctx: SpellContext, victim, room, notify_victim: bool = False, line: str = ""):
        current = self._find_room_for_entity(victim)
        if current is None or room is None:
            return False
        if CharacterMacros.is_npc(victim):
            current.mobiles.pop(str(getattr(victim, "id", "")), None)
            room.add_mobile_to_room(victim)
        else:
            current.characters.pop(str(getattr(victim, "id", "")), None)
            room.add_player_to_room(victim)
        victim.room_id = room.id
        victim.area_id = getattr(room, "area_id", getattr(victim, "area_id", ""))
        if notify_victim and line and not CharacterMacros.is_npc(victim):
            ctx.queue_payload({"victim": victim, "to_victim": line})
        return ctx.mark_performed()

    def _spawn_portal(self, ctx: SpellContext, two_way: bool):
        victim = self._find_world_character(ctx, ctx.target_name)
        if victim is None:
            return ctx.fail("You failed.\r\n")
        destination = self._find_room_for_entity(victim)
        if destination is None or ctx.room is None:
            return ctx.fail("You failed.\r\n")
        if not self.create_object(ctx, "25"):
            return ctx.fail("You failed.\r\n")
        portal = ctx.get_alias("created_item")
        portal.timer = max(2, 1 + ctx.level // 10)
        portal.value3 = str(getattr(destination, "vnum", getattr(destination, "id", "")))
        if two_way and destination is not ctx.room:
            second = ItemUtil.create_object(getattr(getattr(ctx.handler, "registry_service", None), "item_registry", None).get_or_none(vnum="25"))
            second.timer = portal.timer
            second.value3 = str(getattr(ctx.room, "vnum", ctx.room.id))
            destination.add_item_to_room(second)
        return True

    def _enchant_item(self, ctx: SpellContext, weapon: bool):
        obj = ctx.target if self._is_object(ctx.target) else None
        if obj is None:
            return ctx.fail("What should the spell be cast upon?\r\n")
        item_type = str(getattr(obj, "item_type", "") or "").upper()
        if weapon and "WEAPON" not in item_type:
            return ctx.fail("That item is not a weapon.\r\n")
        if not weapon and "ARMOR" not in item_type:
            return ctx.fail("That item is not armor.\r\n")
        if weapon:
            hitroll = Effect(where="TO_OBJECT", type=getattr(ctx.spell, "handler_id", ctx.spell.name), level=ctx.level, duration=-1, location="APPLY_HITROLL", modifier=max(1, ctx.level // 10), bitvector="0", apply_to="object")
            damroll = Effect(where="TO_OBJECT", type=getattr(ctx.spell, "handler_id", ctx.spell.name), level=ctx.level, duration=-1, location="APPLY_DAMROLL", modifier=max(1, ctx.level // 12), bitvector="0", apply_to="object")
            EffectUtil.affect_to_obj(obj, hitroll)
            EffectUtil.affect_to_obj(obj, damroll)
        else:
            armor = Effect(where="TO_OBJECT", type=getattr(ctx.spell, "handler_id", ctx.spell.name), level=ctx.level, duration=-1, location="APPLY_AC", modifier=-max(1, ctx.level // 8), bitvector="0", apply_to="object")
            EffectUtil.affect_to_obj(obj, armor)
        obj.level = max(GenericUtil.to_int(getattr(obj, "level", 0), 0), ctx.level)
        obj.enchanted = True
        return ctx.mark_performed()

    def eval_int(self, ctx: SpellContext, expression: str, **extras) -> int:
        locals_dict = {
            "ctx": ctx,
            "actor": ctx.actor,
            "spell": ctx.spell,
            "room": ctx.room,
            "target": ctx.target,
            "victim": ctx.target if self._is_character(ctx.target) else None,
            "obj": ctx.target if self._is_object(ctx.target) else None,
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

    def _is_character(self, value: Any) -> bool:
        return value is not None and not self._is_object(value)

    @staticmethod
    def _is_object(value: Any) -> bool:
        return value is not None and hasattr(value, "item_type")

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
        entities = []
        entities.extend(list(getattr(room, "characters", {}).values()))
        entities.extend(list(getattr(room, "mobiles", {}).values()))
        return entities

    def _room_flag(self, room, flag_name: str) -> bool:
        flags = CharacterMacros.get_enum("roomFlags")
        bit = CharacterMacros.enum_bit(flags, flag_name)
        if bit <= 0:
            return False
        return CharacterMacros.is_set(GenericUtil.to_int(getattr(room, "room_flags", 0), 0), bit)

    @staticmethod
    def _room_helper(ctx):
        return getattr(ctx.handler, "room_helper", None)

    @staticmethod
    def _fight_handler(ctx):
        return getattr(ctx.handler, "fight_handler", None)

    @staticmethod
    def _room_registry(ctx_or_entity):
        handler = getattr(ctx_or_entity, "handler", None)
        if handler is not None and getattr(handler, "room_registry", None) is not None:
            return handler.room_registry
        if handler is not None and getattr(getattr(handler, "registry_service", None), "room_registry", None) is not None:
            return handler.registry_service.room_registry
        return getattr(ctx_or_entity, "room_registry")

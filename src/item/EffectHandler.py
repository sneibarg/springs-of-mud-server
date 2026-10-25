from __future__ import annotations

import random

from contextlib import nullcontext
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from injector import inject

from api.GameApi import GameApi
from game.EnumProvider import EnumProvider
from item.Effect import Effect
from server.LoggerFactory import LoggerFactory
from util.EffectUtil import EffectUtil
from util.GenericUtil import GenericUtil


@dataclass
class EffectTickResult:
    expired_effects: list[Effect]


class EffectHandler:
    @inject
    def __init__(self, enum_provider: EnumProvider):
        self.__name__ = "EffectHandler"
        self.logger = LoggerFactory.get_logger(__name__)
        self.where_enum = enum_provider.get("whereAffect")
        self.apply_types = enum_provider.get("applyTypes")
        self.affected_by = enum_provider.get("affectedBy")
        self.item_flags = enum_provider.get("itemFlags")
        self.weapon_type = enum_provider.get("weaponType")

    @staticmethod
    def _lock_for(entity):
        lock = getattr(entity, "lock", None)
        return lock if lock is not None else nullcontext()

    @staticmethod
    def _get_affected_raw(entity) -> int:
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is None:
            return 0
        return GenericUtil.to_int(getattr(status_flags, "affected_by", 0), 0)

    @staticmethod
    def _set_affected_raw(entity, value: int) -> None:
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is None:
            return
        status_flags.assign_bitfield("affected_by", GenericUtil.to_int(value, 0))

    @staticmethod
    def _apply_stat_modifier(entity, location: int, modifier: int, apply_types) -> None:
        if modifier == 0:
            return

        def location_name(*candidates):
            for candidate in candidates:
                if apply_types is not None and candidate in apply_types.__members__:
                    return int(apply_types[candidate].value)
            return None

        attrs = getattr(entity, "character_attributes", None)
        if attrs is None:
            return

        if location == location_name("APPLY_STR"):
            attrs.strength = GenericUtil.to_int(getattr(attrs, "strength", 0), 0) + modifier
        elif location == location_name("APPLY_DEX"):
            attrs.dexterity = GenericUtil.to_int(getattr(attrs, "dexterity", 0), 0) + modifier
        elif location == location_name("APPLY_INT"):
            attrs.intelligence = GenericUtil.to_int(getattr(attrs, "intelligence", 0), 0) + modifier
        elif location == location_name("APPLY_WIS"):
            attrs.wisdom = GenericUtil.to_int(getattr(attrs, "wisdom", 0), 0) + modifier
        elif location == location_name("APPLY_CON"):
            attrs.constitution = GenericUtil.to_int(getattr(attrs, "constitution", 0), 0) + modifier
        elif location == location_name("APPLY_SEX"):
            if hasattr(entity, "sex"):
                entity.sex = str(GenericUtil.to_int(getattr(entity, "sex", 0), 0) + modifier)
        elif location in (location_name("APPLY_HITROLL"), location_name("APPLY_HIT_ROLL")):
            if hasattr(entity, "hit_roll"):
                entity.hit_roll = GenericUtil.to_int(getattr(entity, "hit_roll", 0), 0) + modifier
            elif hasattr(entity, "hitroll"):
                entity.hitroll = GenericUtil.to_int(getattr(entity, "hitroll", 0), 0) + modifier
        elif location in (location_name("APPLY_DAMROLL"), location_name("APPLY_DAM_ROLL")):
            if hasattr(entity, "dam_roll"):
                entity.dam_roll = GenericUtil.to_int(getattr(entity, "dam_roll", 0), 0) + modifier
            elif hasattr(entity, "damroll"):
                entity.damroll = GenericUtil.to_int(getattr(entity, "damroll", 0), 0) + modifier
        elif location == location_name("APPLY_AC"):
            from game.ArmorValues import ArmorValues
            armor = getattr(entity, "armor_class", None)
            if armor is not None:
                ArmorValues.adjust_all(armor, modifier)
        elif location in (location_name("APPLY_SAVING_SPELL"), location_name("APPLY_SAVES")):
            if hasattr(entity, "saving_throw"):
                entity.saving_throw = GenericUtil.to_int(getattr(entity, "saving_throw", 0), 0) + modifier

    def as_effect(self, affect_like, source: str = "") -> Effect:
        if isinstance(affect_like, Effect):
            effect = deepcopy(affect_like)
            if source:
                effect.source = source
            return effect
        if isinstance(affect_like, (dict, str)):
            effect = Effect.from_json(affect_like)
            if source:
                effect.source = source
            return effect
        return Effect(
            where=getattr(affect_like, "where", 0),
            type=getattr(affect_like, "type", ""),
            level=GenericUtil.to_int(getattr(affect_like, "level", 0), 0),
            duration=GenericUtil.to_int(getattr(affect_like, "duration", 0), 0),
            location=getattr(affect_like, "location", 0),
            modifier=GenericUtil.to_int(getattr(affect_like, "modifier", 0), 0),
            bitvector=getattr(affect_like, "bitvector", 0),
            apply_to=str(getattr(affect_like, "apply_to", "") or ""),
            source=source,
        )

    def ensure_effects(self, entity) -> list[Effect]:
        effects = getattr(entity, "effects", None)
        if effects is None:
            effects = []
            setattr(entity, "effects", effects)
            return effects
        for index, effect in enumerate(list(effects)):
            if isinstance(effect, Effect):
                continue
            effects[index] = self.as_effect(effect)
        return effects

    def affect_modify(self, entity, effect: Effect, add: bool) -> None:
        where = EffectUtil.enum_value(self.where_enum, getattr(effect, "where", None), EffectUtil.enum_value(self.where_enum, "TO_AFFECTS", 0))
        location = EffectUtil.enum_value(self.apply_types, getattr(effect, "location", None), 0)
        modifier = GenericUtil.to_int(getattr(effect, "modifier", 0), 0)
        if not add:
            modifier = -modifier

        raw_bit = getattr(effect, "bitvector", 0)
        if where == EffectUtil.enum_value(self.where_enum, "TO_AFFECTS", -1):
            bit = EffectUtil.enum_value(self.affected_by, raw_bit, 0)
            if bit != 0:
                raw = self._get_affected_raw(entity)
                raw = GameApi.set_bit(raw, bit) if add else GameApi.unset_bit(raw, bit)
                self._set_affected_raw(entity, raw)
        elif where == EffectUtil.enum_value(self.where_enum, "TO_OBJECT", -1):
            bit = EffectUtil.enum_value(self.item_flags, raw_bit, 0)
            if bit != 0 and hasattr(entity, "extra_flags"):
                flags = GameApi.convert_flags(getattr(entity, "extra_flags", "") or "")
                flags = GameApi.set_bit(flags, bit) if add else GameApi.unset_bit(flags, bit)
                entity.extra_flags = GameApi.flags_to_letters(flags)
        elif where == EffectUtil.enum_value(self.where_enum, "TO_WEAPON", -1):
            bit = EffectUtil.enum_value(self.weapon_type, raw_bit, 0)
            if bit != 0 and hasattr(entity, "value4"):
                value = GenericUtil.to_int(getattr(entity, "value4", 0), 0)
                value = GameApi.set_bit(value, bit) if add else GameApi.unset_bit(value, bit)
                entity.value4 = str(value)

        self._apply_stat_modifier(entity, location, modifier, self.apply_types)

    def affect_find(self, effects: list[Effect], effect_type) -> Effect | None:
        wanted = str(effect_type).strip().lower()
        for effect in effects or []:
            if str(getattr(effect, "type", "")).strip().lower() == wanted:
                return effect
        return None

    def affect_check(self, entity, where, vector) -> None:
        where_value = EffectUtil.enum_value(self.where_enum, where, -1)
        if where_value != EffectUtil.enum_value(self.where_enum, "TO_AFFECTS", -1):
            return
        bit = EffectUtil.enum_value(self.affected_by, vector, 0)
        if bit == 0:
            return
        for effect in self.ensure_effects(entity):
            if (EffectUtil.enum_value(self.where_enum, effect.where, -1) == where_value
                    and EffectUtil.enum_value(self.affected_by, effect.bitvector, 0) == bit):
                self._set_affected_raw(entity, GameApi.set_bit(self._get_affected_raw(entity), bit))
                return

    def apply_effect(self, entity: Any, effect: Effect):
        new_effect = self.as_effect(effect)
        with self._lock_for(entity):
            self.ensure_effects(entity).append(new_effect)
            self.affect_modify(entity, new_effect, True)
        self._refresh_item_wearer(entity)
        return new_effect

    def remove_effect(self, entity: Any, effect: Effect) -> bool:
        with self._lock_for(entity):
            effects = self.ensure_effects(entity)
            if effect not in effects:
                return False
            where = getattr(effect, "where", 0)
            vector = getattr(effect, "bitvector", 0)
            self.affect_modify(entity, effect, False)
            effects.remove(effect)
            if not hasattr(entity, "item_type"):
                self.affect_check(entity, where, vector)
        self._refresh_item_wearer(entity)
        return True

    def affect_to_char(self, character, effect: Effect):
        return self.apply_effect(character, effect)

    def affect_to_obj(self, obj, effect: Effect):
        return self.apply_effect(obj, effect)

    def affect_remove(self, character, effect: Effect) -> bool:
        return self.remove_effect(character, effect)

    def affect_remove_obj(self, obj, effect: Effect) -> bool:
        return self.remove_effect(obj, effect)

    def affect_strip(self, entity, effect_type) -> None:
        want = str(effect_type).strip().lower()
        for effect in list(self.ensure_effects(entity)):
            if str(getattr(effect, "type", "")).strip().lower() == want:
                self.remove_effect(entity, effect)

    def affect_join(self, entity, effect: Effect):
        new_effect = self.as_effect(effect)
        for old in list(self.ensure_effects(entity)):
            if str(getattr(old, "type", "")).strip().lower() != str(getattr(new_effect, "type", "")).strip().lower():
                continue
            new_effect.level = (GenericUtil.to_int(new_effect.level, 0) + GenericUtil.to_int(old.level, 0)) // 2
            new_effect.duration = GenericUtil.to_int(new_effect.duration, 0) + GenericUtil.to_int(old.duration, 0)
            new_effect.modifier = GenericUtil.to_int(new_effect.modifier, 0) + GenericUtil.to_int(old.modifier, 0)
            self.remove_effect(entity, old)
            break
        return self.apply_effect(entity, new_effect)

    def effect_from_spell_affect(self, spell, affect_like, caster_level: int, source: str = "") -> Effect:
        effect = self.as_effect(affect_like, source=source)
        raw_type = str(getattr(effect, "type", "") or "").strip().lower()
        if raw_type in ("sn", "skill", "spell"):
            effect.type = str(getattr(spell, "handler_id", "") or getattr(spell, "name", ""))
        effect.level = EffectUtil._eval_expr(getattr(effect, "level", 0), caster_level, int(caster_level))
        effect.duration = EffectUtil._eval_expr(getattr(effect, "duration", 0), caster_level, 0)
        effect.modifier = EffectUtil._eval_expr(getattr(effect, "modifier", 0), caster_level, 0)
        return effect

    def apply_spell_effects(self, caster, victim, spell, *, caster_level: int | None = None,
                            join: bool = False) -> None:
        """Add target-compatible effects; join character effects only when requested."""
        affects = list(getattr(spell, "affect_data", []) or getattr(spell, "affects", []) or [])
        if not affects or victim is None:
            return
        source = f"spell:{getattr(spell, 'handler_id', getattr(spell, 'name', ''))}"
        if caster_level is None:
            caster_level = GenericUtil.to_int(getattr(caster, "level", 0), 0)
        for affect_like in affects:
            effect = self.effect_from_spell_affect(spell, affect_like, caster_level, source=source)
            apply_to = str(getattr(effect, "apply_to", "") or "").strip().lower()
            where = EffectUtil.enum_value(self.where_enum, effect.where, -1)
            wants_object = apply_to in ("item", "object") or where in (
                EffectUtil.enum_value(self.where_enum, "TO_OBJECT", -2),
                EffectUtil.enum_value(self.where_enum, "TO_WEAPON", -2),
            )
            if wants_object and hasattr(victim, "item_type"):
                self.affect_to_obj(victim, effect)
            elif not wants_object and not hasattr(victim, "item_type"):
                if join:
                    self.affect_join(victim, effect)
                else:
                    self.affect_to_char(victim, effect)

    def apply_item_effects(self, character, item) -> None:
        item._effect_wearer = character
        effects = list(getattr(item, "effects", []) or [])
        if not effects:
            return
        source = f"item:{getattr(item, 'id', '')}:{id(item)}"
        for affect_like in effects:
            effect = self.as_effect(affect_like, source=source)
            self.affect_to_char(character, effect)

    def remove_item_effects(self, character, item) -> None:
        source = f"item:{getattr(item, 'id', '')}:{id(item)}"
        for effect in list(self.ensure_effects(character)):
            if getattr(effect, "source", "") == source:
                self.remove_effect(character, effect)
        if getattr(item, "_effect_wearer", None) is character:
            item._effect_wearer = None

    def _refresh_item_wearer(self, item) -> None:
        """Keep worn-item stat contributions in sync with live object affects."""
        wearer = getattr(item, "_effect_wearer", None)
        if wearer is None:
            return
        self.remove_item_effects(wearer, item)
        self.apply_item_effects(wearer, item)

    def dispel_effects(self, dis_level: int, victim, effect_type) -> list[Effect]:
        want = str(effect_type).strip().lower()
        matching = [effect for effect in self.ensure_effects(victim)
                    if str(getattr(effect, "type", "")).strip().lower() == want]
        for effect in matching:
            if not EffectUtil.saves_dispel(
                dis_level,
                GenericUtil.to_int(getattr(effect, "level", 0), 0),
                GenericUtil.to_int(getattr(effect, "duration", 0), 0),
            ):
                for removed in matching:
                    self.remove_effect(victim, removed)
                return matching
            else:
                effect.level = GenericUtil.to_int(getattr(effect, "level", 0), 0) - 1
        return []

    def check_dispel(self, dis_level: int, victim, effect_type) -> bool:
        return bool(self.dispel_effects(dis_level, victim, effect_type))

    def enchant_object(self, item, spell_type: str, level: int, rules: dict,
                       level_reduction: int, exceptional_boundary: int, level_cap: int, roll: int) -> str:
        """Resolve a configured risky enchantment over the instance's canonical affects."""
        effects = self.ensure_effects(item)
        locations = {EffectUtil.enum_value(self.apply_types, name, -1): coefficient
                     for name, coefficient in rules['locations'].items()}
        fail = int(rules['base_fail'])
        for effect in effects:
            location = EffectUtil.enum_value(self.apply_types, effect.location, -1)
            fail += (locations[location] * int(effect.modifier) ** 2 if location in locations
                     else int(rules['other_penalty']))
        raw_flags = GameApi.flags_to_int(item.extra_flags)
        for flag, adjustment in rules['flag_adjustments'].items():
            if GameApi.is_set(raw_flags, int(getattr(self.item_flags, flag))):
                fail += adjustment
        fail = max(rules['min_fail'], min(rules['max_fail'], fail - level_reduction))
        if roll < fail // rules['destroy_divisor']:
            return 'destroyed'
        if roll < fail // rules['disenchant_divisor']:
            item.enchanted = True
            effects.clear()
            item.extra_flags = GameApi.flags_to_letters(0)
            return 'disenchanted'
        if roll <= fail:
            return 'failed'
        if not item.enchanted:
            for effect in effects:
                if GenericUtil.to_int(effect.type, 0) < 0:
                    effect.type = 0
        item.enchanted = True
        exceptional = roll > exceptional_boundary
        added = rules['exceptional_added'] if exceptional else rules['added']
        raw_flags = GameApi.set_bit(raw_flags, int(self.item_flags.ITEM_MAGIC))
        if exceptional:
            raw_flags = GameApi.set_bit(raw_flags, int(self.item_flags.ITEM_GLOW))
        if item.level < level_cap:
            item.level = min(level_cap, item.level + 1)
        for name in rules['locations']:
            location = EffectUtil.enum_value(self.apply_types, name, -1)
            matching = [effect for effect in effects
                        if EffectUtil.enum_value(self.apply_types, effect.location, -1) == location]
            if matching:
                for effect in matching:
                    effect.type = spell_type
                    effect.modifier = int(effect.modifier) + added
                    effect.level = max(int(effect.level), level)
                    if rules.get('hum_above') is not None and effect.modifier > rules['hum_above']:
                        raw_flags = GameApi.set_bit(raw_flags, int(self.item_flags.ITEM_HUM))
            else:
                effects.insert(0, Effect(valid=True, where='TO_OBJECT', type=spell_type, level=level,
                    duration=-1, location=name, modifier=added, bitvector=0, apply_to='object'))
        item.extra_flags = GameApi.flags_to_letters(raw_flags)
        return 'exceptional' if exceptional else 'success'

    def tick_effects(self, entity) -> EffectTickResult:
        expired_effects: list[Effect] = []
        effects = list(self.ensure_effects(entity))
        for idx, effect in enumerate(effects):
            duration = GenericUtil.to_int(getattr(effect, "duration", 0), 0)
            if duration > 0:
                effect.duration = duration - 1
                level = GenericUtil.to_int(getattr(effect, "level", 0), 0)
                if level > 0 and random.randint(0, 4) == 0:
                    effect.level = level - 1
                continue
            if duration < 0:
                continue

            next_effect = effects[idx + 1] if idx + 1 < len(effects) else None
            suppress_msg = (
                next_effect is not None
                and str(getattr(next_effect, "type", "")).strip().lower() == str(getattr(effect, "type", "")).strip().lower()
                and GenericUtil.to_int(getattr(next_effect, "duration", 0), 0) <= 0
            )
            if not suppress_msg:
                expired_effects.append(effect)
            self.remove_effect(entity, effect)
        return EffectTickResult(expired_effects=expired_effects)

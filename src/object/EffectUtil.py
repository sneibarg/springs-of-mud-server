from __future__ import annotations

from copy import deepcopy

from game.GameMacros import GameMacros
from game.GenericUtil import GenericUtil
from object.Effect import Effect


class _EffectStatics:
    @staticmethod
    def get_affected_raw(entity) -> int:
        if hasattr(entity, "character_flags") and getattr(entity, "character_flags", None) is not None:
            return GameMacros.convert_flags(getattr(entity.character_flags, "affected_by", "") or "")
        if hasattr(entity, "mobile_flags") and getattr(entity, "mobile_flags", None) is not None:
            return GenericUtil.to_int(getattr(entity.mobile_flags, "affected_by", 0), 0)
        return 0

    @staticmethod
    def set_affected_raw(entity, value: int):
        if hasattr(entity, "character_flags") and getattr(entity, "character_flags", None) is not None:
            entity.character_flags.affected_by = GenericUtil.flags_to_letters(value)
            return
        if hasattr(entity, "mobile_flags") and getattr(entity, "mobile_flags", None) is not None:
            entity.mobile_flags.affected_by = int(value)

    @staticmethod
    def apply_stat_modifier(entity, location: int, modifier: int, apply_types):
        if modifier == 0:
            return

        def location_name(*candidates):
            for candidate in candidates:
                if apply_types is not None and hasattr(apply_types, candidate):
                    return int(getattr(apply_types, candidate).value)
            return None

        attrs = getattr(entity, "character_attributes", None) or getattr(entity, "perm_stat", None)
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
            armor = getattr(entity, "armor_class", None)
            if armor is not None:
                for field in ("piercing", "bashing", "slashing", "magic", "pierce", "bash", "slash", "exotic"):
                    if hasattr(armor, field):
                        setattr(armor, field, GenericUtil.to_int(getattr(armor, field, 0), 0) + modifier)
        elif location in (location_name("APPLY_SAVING_SPELL"), location_name("APPLY_SAVES")):
            if hasattr(entity, "saving_throw"):
                entity.saving_throw = GenericUtil.to_int(getattr(entity, "saving_throw", 0), 0) + modifier


class EffectUtil:
    @staticmethod
    def ensure_effects(entity) -> list[Effect]:
        effects = getattr(entity, "effects", None)
        if effects is None:
            effects = []
            setattr(entity, "effects", effects)
        return effects

    @staticmethod
    def as_effect(affect_like, source: str = "") -> Effect:
        if isinstance(affect_like, Effect):
            effect = deepcopy(affect_like)
            if source:
                effect.source = source
            return effect
        effect = Effect(
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
        return effect

    @staticmethod
    def enum_value(enum_type, raw_value, default: int = 0) -> int:
        if raw_value is None:
            return default
        int_value = GenericUtil.to_int(raw_value, None)
        if int_value is not None:
            return int_value
        key = str(raw_value).strip().upper()
        if enum_type is not None and hasattr(enum_type, key):
            return int(getattr(enum_type, key).value)
        return default

    @staticmethod
    def affect_modify(entity, effect: Effect, add: bool, enums: dict):
        where_enum = enums.get("whereAffect")
        apply_types = enums.get("applyTypes")
        affected_by = enums.get("affectedBy")
        item_flags = enums.get("itemFlags")
        weapon_type = enums.get("weaponType")

        where = EffectUtil.enum_value(where_enum, effect.where, EffectUtil.enum_value(where_enum, "TO_AFFECTS", 0))
        location = EffectUtil.enum_value(apply_types, effect.location, 0)
        modifier = GenericUtil.to_int(effect.modifier, 0)
        if not add:
            modifier = -modifier

        raw_bit = effect.bitvector
        if where == EffectUtil.enum_value(where_enum, "TO_AFFECTS", -1):
            bit = EffectUtil.enum_value(affected_by, raw_bit, 0)
            if bit != 0:
                raw = _EffectStatics.get_affected_raw(entity)
                raw = GameMacros.set_bit(raw, bit) if add else GameMacros.unset_bit(raw, bit)
                _EffectStatics.set_affected_raw(entity, raw)
        elif where == EffectUtil.enum_value(where_enum, "TO_OBJECT", -1):
            bit = EffectUtil.enum_value(item_flags, raw_bit, 0)
            if bit != 0 and hasattr(entity, "extra_flags"):
                flags = GameMacros.convert_flags(getattr(entity, "extra_flags", "") or "")
                flags = GameMacros.set_bit(flags, bit) if add else GameMacros.unset_bit(flags, bit)
                entity.extra_flags = GenericUtil.flags_to_letters(flags)
        elif where == EffectUtil.enum_value(where_enum, "TO_WEAPON", -1):
            bit = EffectUtil.enum_value(weapon_type, raw_bit, 0)
            if bit != 0 and hasattr(entity, "value4"):
                value = GenericUtil.to_int(getattr(entity, "value4", 0), 0)
                value = GameMacros.set_bit(value, bit) if add else GameMacros.unset_bit(value, bit)
                entity.value4 = str(value)

        _EffectStatics.apply_stat_modifier(entity, location, modifier, apply_types)

    @staticmethod
    def affect_find(effects: list[Effect], effect_type) -> Effect | None:
        want = str(effect_type).strip().lower()
        for effect in effects or []:
            if str(getattr(effect, "type", "")).strip().lower() == want:
                return effect
        return None

    @staticmethod
    def affect_to_char(character, effect: Effect, enums: dict):
        new_effect = EffectUtil.as_effect(effect)
        EffectUtil.ensure_effects(character).append(new_effect)
        EffectUtil.affect_modify(character, new_effect, True, enums)

    @staticmethod
    def affect_to_obj(obj, effect: Effect, enums: dict):
        new_effect = EffectUtil.as_effect(effect)
        EffectUtil.ensure_effects(obj).append(new_effect)
        EffectUtil.affect_modify(obj, new_effect, True, enums)

    @staticmethod
    def affect_check(character, where, vector, enums: dict):
        if GenericUtil.to_int(vector, 0) == 0:
            return
        where_enum = enums.get("whereAffect")
        where_value = EffectUtil.enum_value(where_enum, where, -1)
        for effect in EffectUtil.ensure_effects(character):
            if EffectUtil.enum_value(where_enum, effect.where, -1) == where_value and str(effect.bitvector) == str(vector):
                EffectUtil.affect_modify(character, effect, True, enums)
                return

    @staticmethod
    def affect_remove(character, effect: Effect, enums: dict):
        effects = EffectUtil.ensure_effects(character)
        if effect not in effects:
            return
        where = effect.where
        vector = effect.bitvector
        EffectUtil.affect_modify(character, effect, False, enums)
        effects.remove(effect)
        EffectUtil.affect_check(character, where, vector, enums)

    @staticmethod
    def affect_remove_obj(obj, effect: Effect, enums: dict):
        effects = EffectUtil.ensure_effects(obj)
        if effect not in effects:
            return
        EffectUtil.affect_modify(obj, effect, False, enums)
        effects.remove(effect)

    @staticmethod
    def affect_strip(character, effect_type, enums: dict):
        effects = list(EffectUtil.ensure_effects(character))
        want = str(effect_type).strip().lower()
        for effect in effects:
            if str(getattr(effect, "type", "")).strip().lower() == want:
                EffectUtil.affect_remove(character, effect, enums)

    @staticmethod
    def is_affected(character, effect_type) -> bool:
        want = str(effect_type).strip().lower()
        for effect in EffectUtil.ensure_effects(character):
            if str(getattr(effect, "type", "")).strip().lower() == want:
                return True
        return False

    @staticmethod
    def affect_join(character, effect: Effect, enums: dict):
        new_effect = EffectUtil.as_effect(effect)
        effects = EffectUtil.ensure_effects(character)
        for old in list(effects):
            if str(getattr(old, "type", "")).strip().lower() == str(getattr(new_effect, "type", "")).strip().lower():
                new_effect.level = (GenericUtil.to_int(new_effect.level, 0) + GenericUtil.to_int(old.level, 0)) // 2
                new_effect.duration = GenericUtil.to_int(new_effect.duration, 0) + GenericUtil.to_int(old.duration, 0)
                new_effect.modifier = GenericUtil.to_int(new_effect.modifier, 0) + GenericUtil.to_int(old.modifier, 0)
                EffectUtil.affect_remove(character, old, enums)
                break
        EffectUtil.affect_to_char(character, new_effect, enums)

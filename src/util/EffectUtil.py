from __future__ import annotations

import ast
import random

from copy import deepcopy

from game.GameMacros import GameMacros
from util.GenericUtil import GenericUtil
from object.Effect import Effect
from player.CharacterMacros import CharacterMacros


class _EffectStatics:
    @staticmethod
    def get_affected_raw(entity) -> int:
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is not None:
            return GenericUtil.to_int(getattr(status_flags, "affected_by", 0), 0)
        return 0

    @staticmethod
    def set_affected_raw(entity, value: int):
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is not None:
            status_flags.assign_bitfield("affected_by", GenericUtil.to_int(value, 0))

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


class _SafeNumericExpression:
    BIN_OPS = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.FloorDiv: lambda a, b: a // b,
        ast.Mod: lambda a, b: a % b,
    }
    UNARY_OPS = {
        ast.UAdd: lambda value: +value,
        ast.USub: lambda value: -value,
        ast.Not: lambda value: not value,
    }
    COMPARE_OPS = {
        ast.Eq: lambda a, b: a == b,
        ast.NotEq: lambda a, b: a != b,
        ast.Lt: lambda a, b: a < b,
        ast.LtE: lambda a, b: a <= b,
        ast.Gt: lambda a, b: a > b,
        ast.GtE: lambda a, b: a >= b,
    }
    BOOL_OPS = {
        ast.And: all,
        ast.Or: any,
    }

    @classmethod
    def evaluate(cls, expression: str, env: dict):
        tree = ast.parse(str(expression), mode="eval")
        return cls._eval_node(tree.body, env)

    @classmethod
    def _eval_node(cls, node, env: dict):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float, bool)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value!r}")

        if isinstance(node, ast.Name):
            if node.id not in env:
                raise ValueError(f"Unknown name: {node.id}")
            return env[node.id]

        if isinstance(node, ast.BinOp):
            operator = cls.BIN_OPS.get(type(node.op))
            if operator is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return operator(cls._eval_node(node.left, env), cls._eval_node(node.right, env))

        if isinstance(node, ast.UnaryOp):
            operator = cls.UNARY_OPS.get(type(node.op))
            if operator is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return operator(cls._eval_node(node.operand, env))

        if isinstance(node, ast.BoolOp):
            operator = cls.BOOL_OPS.get(type(node.op))
            if operator is None:
                raise ValueError(f"Unsupported boolean operator: {type(node.op).__name__}")
            return operator(bool(cls._eval_node(value, env)) for value in node.values)

        if isinstance(node, ast.Compare):
            left = cls._eval_node(node.left, env)
            for operator_node, comparator_node in zip(node.ops, node.comparators):
                operator = cls.COMPARE_OPS.get(type(operator_node))
                if operator is None:
                    raise ValueError(f"Unsupported comparison operator: {type(operator_node).__name__}")
                right = cls._eval_node(comparator_node, env)
                if not operator(left, right):
                    return False
                left = right
            return True

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only direct function calls are allowed.")
            func = env.get(node.func.id)
            if not callable(func):
                raise ValueError(f"Unsupported function: {node.func.id}")
            if node.keywords:
                raise ValueError("Keyword arguments are not allowed.")
            args = [cls._eval_node(arg, env) for arg in node.args]
            return func(*args)

        raise ValueError(f"Unsupported expression node: {type(node).__name__}")


class EffectUtil:
    @staticmethod
    def _expr_env(level: int, target=None, caster=None) -> dict:
        def dice(number, size):
            count = max(0, GenericUtil.to_int(number, 0))
            sides = max(1, GenericUtil.to_int(size, 1))
            return sum(random.randint(1, sides) for _ in range(count))

        def number_range(low, high):
            lo = GenericUtil.to_int(low, 0)
            hi = GenericUtil.to_int(high, lo)
            if hi < lo:
                lo, hi = hi, lo
            return random.randint(lo, hi)

        def number_fuzzy(value):
            base = GenericUtil.to_int(value, 0)
            return max(1, base + random.randint(-1, 1))

        return {
            "level": GenericUtil.to_int(level, 0),
            "victim": target,
            "target": target,
            "caster": caster,
            "actor": caster,
            "dice": dice,
            "number_range": number_range,
            "number_fuzzy": number_fuzzy,
            "UMAX": lambda a, b: max(GenericUtil.to_int(a, 0), GenericUtil.to_int(b, 0)),
            "UMIN": lambda a, b: min(GenericUtil.to_int(a, 0), GenericUtil.to_int(b, 0)),
            "abs": abs,
            "max": max,
            "min": min,
            "int": int,
        }

    @staticmethod
    def _eval_expr(value, level: int, default: int = 0, target=None, caster=None) -> int:
        return EffectUtil.safe_eval_int(
            value,
            default=default,
            level=level,
            target=target,
            victim=target,
            caster=caster,
            actor=caster,
        )

    @staticmethod
    def safe_eval_int(value, default: int = 0, **env) -> int:
        if value is None:
            return default
        converted = GenericUtil.to_int(value, None)
        if converted is not None:
            return converted
        expr = str(value or "").strip()
        if not expr:
            return default
        try:
            return int(_SafeNumericExpression.evaluate(expr, env={**EffectUtil._expr_env(GenericUtil.to_int(env.get("level", 0), 0), target=env.get("target"), caster=env.get("caster")), **env}))
        except Exception:
            return default

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
    def affect_modify(entity, effect: Effect, add: bool):
        where_enum = CharacterMacros.get_enum("whereAffect")
        apply_types = CharacterMacros.get_enum("applyTypes")
        affected_by = CharacterMacros.get_enum("affectedBy")
        item_flags = CharacterMacros.get_enum("itemFlags")
        weapon_type = CharacterMacros.get_enum("weaponType")

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
                entity.extra_flags = GameMacros.flags_to_letters(flags)
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
    def affect_to_char(character, effect: Effect):
        new_effect = EffectUtil.as_effect(effect)
        if hasattr(character, "apply_effect"):
            character.apply_effect(new_effect)
            return
        EffectUtil.ensure_effects(character).append(new_effect)
        EffectUtil.affect_modify(character, new_effect, True)

    @staticmethod
    def affect_to_obj(obj, effect: Effect):
        new_effect = EffectUtil.as_effect(effect)
        if hasattr(obj, "apply_effect"):
            obj.apply_effect(new_effect)
            return
        EffectUtil.ensure_effects(obj).append(new_effect)
        EffectUtil.affect_modify(obj, new_effect, True)

    @staticmethod
    def affect_check(character, where, vector):
        if GenericUtil.to_int(vector, 0) == 0:
            return
        where_enum = CharacterMacros.get_enum("whereAffect")
        where_value = EffectUtil.enum_value(where_enum, where, -1)
        for effect in EffectUtil.ensure_effects(character):
            if EffectUtil.enum_value(where_enum, effect.where, -1) == where_value and str(effect.bitvector) == str(vector):
                EffectUtil.affect_modify(character, effect, True)
                return

    @staticmethod
    def affect_remove(character, effect: Effect):
        if hasattr(character, "remove_effect"):
            character.remove_effect(effect)
            return
        effects = EffectUtil.ensure_effects(character)
        if effect not in effects:
            return
        where = effect.where
        vector = effect.bitvector
        EffectUtil.affect_modify(character, effect, False)
        effects.remove(effect)
        EffectUtil.affect_check(character, where, vector)

    @staticmethod
    def affect_remove_obj(obj, effect: Effect):
        if hasattr(obj, "remove_effect"):
            obj.remove_effect(effect)
            return
        effects = EffectUtil.ensure_effects(obj)
        if effect not in effects:
            return
        EffectUtil.affect_modify(obj, effect, False)
        effects.remove(effect)

    @staticmethod
    def affect_strip(character, effect_type):
        effects = list(EffectUtil.ensure_effects(character))
        want = str(effect_type).strip().lower()
        for effect in effects:
            if str(getattr(effect, "type", "")).strip().lower() == want:
                EffectUtil.affect_remove(character, effect)

    @staticmethod
    def affect_join(character, effect: Effect):
        if hasattr(character, "join_effect"):
            character.join_effect(effect)
            return
        new_effect = EffectUtil.as_effect(effect)
        effects = EffectUtil.ensure_effects(character)
        for old in list(effects):
            if str(getattr(old, "type", "")).strip().lower() == str(getattr(new_effect, "type", "")).strip().lower():
                new_effect.level = (GenericUtil.to_int(new_effect.level, 0) + GenericUtil.to_int(old.level, 0)) // 2
                new_effect.duration = GenericUtil.to_int(new_effect.duration, 0) + GenericUtil.to_int(old.duration, 0)
                new_effect.modifier = GenericUtil.to_int(new_effect.modifier, 0) + GenericUtil.to_int(old.modifier, 0)
                EffectUtil.affect_remove(character, old)
                break
        EffectUtil.affect_to_char(character, new_effect)

    @staticmethod
    def effect_from_spell_affect(spell, affect_like, caster_level: int, source: str = "") -> Effect:
        effect = EffectUtil.as_effect(affect_like, source=source)
        raw_type = str(getattr(effect, "type", "") or "").strip().lower()
        if raw_type in ("sn", "skill", "spell"):
            effect.type = str(getattr(spell, "handler_id", "") or getattr(spell, "name", ""))
        effect.level = EffectUtil._eval_expr(getattr(effect, "level", 0), caster_level, int(caster_level))
        effect.duration = EffectUtil._eval_expr(getattr(effect, "duration", 0), caster_level, 0)
        effect.modifier = EffectUtil._eval_expr(getattr(effect, "modifier", 0), caster_level, 0)
        return effect

    @staticmethod
    def apply_spell_effects(caster, victim, spell):
        affects = list(getattr(spell, "affect_data", []) or getattr(spell, "affects", []) or [])
        if not affects or victim is None:
            return
        source = f"spell:{getattr(spell, 'handler_id', getattr(spell, 'name', ''))}"
        caster_level = GenericUtil.to_int(getattr(caster, "level", 0), 0)
        for affect_like in affects:
            effect = EffectUtil.effect_from_spell_affect(spell, affect_like, caster_level, source=source)
            apply_to = str(getattr(effect, "apply_to", "") or "").strip().lower()
            where = str(getattr(effect, "where", "") or "").strip().upper()
            wants_object = apply_to == "object" or where in ("TO_OBJECT", "TO_WEAPON")
            if wants_object and hasattr(victim, "item_type"):
                EffectUtil.affect_to_obj(victim, effect)
            elif not hasattr(victim, "item_type"):
                EffectUtil.affect_join(victim, effect)

    @staticmethod
    def apply_item_effects(character, item):
        effects = list(getattr(item, "effects", []) or [])
        if not effects:
            return
        source = f"item:{getattr(item, 'id', '')}:{id(item)}"
        for affect_like in effects:
            effect = EffectUtil.as_effect(affect_like, source=source)
            EffectUtil.affect_to_char(character, effect)

    @staticmethod
    def remove_item_effects(character, item):
        source = f"item:{getattr(item, 'id', '')}:{id(item)}"
        for effect in list(EffectUtil.ensure_effects(character)):
            if getattr(effect, "source", "") == source:
                EffectUtil.affect_remove(character, effect)

    @staticmethod
    def is_affected(character, effect_type) -> bool:
        affected_by = CharacterMacros.get_enum("affectedBy")
        if CharacterMacros.is_affected(character, effect_type):
            return True
        if hasattr(affected_by, str(effect_type)):
            bit = getattr(affected_by, str(effect_type)).value
            return CharacterMacros.is_affected(character, bit)
        return False

    @staticmethod
    def saves_dispel(dis_level: int, spell_level: int, duration: int) -> bool:
        save = 50 + (GenericUtil.to_int(spell_level, 0) - GenericUtil.to_int(dis_level, 0)) * 5
        if GenericUtil.to_int(duration, 0) == -1:
            save += 5
        save = max(5, min(95, save))
        return random.randint(1, 100) < save

    @staticmethod
    def check_dispel(dis_level: int, victim, effect_type) -> bool:
        removed = False
        for effect in list(EffectUtil.ensure_effects(victim)):
            if str(getattr(effect, "type", "")).strip().lower() != str(effect_type).strip().lower():
                continue
            if not EffectUtil.saves_dispel(dis_level, GenericUtil.to_int(getattr(effect, "level", 0), 0), GenericUtil.to_int(getattr(effect, "duration", 0), 0)):
                EffectUtil.affect_remove(victim, effect)
                removed = True
            else:
                effect.level = max(0, GenericUtil.to_int(getattr(effect, "level", 0), 0) - 1)
        return removed

    @staticmethod
    def saves_spell(level: int, victim, _dam_type: int = 0) -> bool:
        victim_level = GenericUtil.to_int(getattr(victim, "level", 0), 0)
        saving_throw = GenericUtil.to_int(getattr(victim, "saving_throw", 0), 0)
        save = 50 + (victim_level - GenericUtil.to_int(level, 0)) * 5 - saving_throw * 2
        if CharacterMacros.is_affected_by_name(victim, CharacterMacros.get_enum("affectedBy"),"AFF_BERSERK"):
            save += victim_level // 2
        save = max(5, min(95, save))
        return random.randint(1, 100) < save

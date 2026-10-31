from __future__ import annotations

import ast
import random

from api.CharacterApi import CharacterApi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player.Character import Character
from util.GenericUtil import GenericUtil


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
    """Shared effect calculations, expression evaluation, and affect presentation."""

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

        return {
            "level": GenericUtil.to_int(level, 0),
            "victim": target,
            "target": target,
            "caster": caster,
            "actor": caster,
            "dice": dice,
            "number_range": number_range,
            "number_fuzzy": EffectUtil.number_fuzzy,
            "UMAX": lambda a, b: max(GenericUtil.to_int(a, 0), GenericUtil.to_int(b, 0)),
            "UMIN": lambda a, b: min(GenericUtil.to_int(a, 0), GenericUtil.to_int(b, 0)),
            "abs": abs,
            "max": max,
            "min": min,
            "int": int,
        }

    @staticmethod
    def number_fuzzy(value) -> int:
        from game.RandomNumberGenerator import RandomNumberGenerator

        return RandomNumberGenerator().number_fuzzy(GenericUtil.to_int(value, 0))

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
            base_env = EffectUtil._expr_env(
                GenericUtil.to_int(env.get("level", 0), 0),
                target=env.get("target"),
                caster=env.get("caster"),
            )
            return int(_SafeNumericExpression.evaluate(expr, env={**base_env, **env}))
        except Exception:
            return default

    @staticmethod
    def enum_value(enum_type, raw_value, default: int = 0) -> int:
        if raw_value is None:
            return default
        int_value = GenericUtil.to_int(raw_value, None)
        if int_value is not None:
            return int_value
        key = str(raw_value).strip().upper()
        if enum_type is not None and key in enum_type.__members__:
            return int(enum_type[key].value)
        return default

    @staticmethod
    def saves_dispel(dis_level: int, spell_level: int, duration: int) -> bool:
        save = 50 + (GenericUtil.to_int(spell_level, 0) - GenericUtil.to_int(dis_level, 0)) * 5
        if GenericUtil.to_int(duration, 0) == -1:
            save += 25  # ROM adds five spell levels before multiplying by five.
        save = max(5, min(95, save))
        return random.randint(1, 100) < save

    @staticmethod
    def saves_spell(level: int, victim, _dam_type: int | str = 0, *, immunity=None,
                    berserk: bool | None = None, roll=None) -> bool:
        victim_level = GenericUtil.to_int(getattr(victim, "level", 0), 0)
        saving_throw = GenericUtil.to_int(getattr(victim, "saving_throw", 0), 0)
        save = 50 + (victim_level - GenericUtil.to_int(level, 0)) * 5 - saving_throw * 2
        if berserk is None:
            berserk = CharacterApi.is_affected_by_name(victim, CharacterApi.get_enum("affectedBy"), "AFF_BERSERK")
        if berserk:
            save += victim_level // 2
        if immunity is not None:
            status = immunity(victim, _dam_type)
            if status == "IS_IMMUNE":
                return True
            if status == "IS_RESISTANT":
                save += 2
            elif status == "IS_VULNERABLE":
                save -= 2
        if not CharacterApi.is_npc(victim) and getattr(getattr(victim, "character_class", None), "mana_gain", False):
            save = int(9 * save / 10)
        save = max(5, min(95, save))
        return (roll() if roll is not None else random.randint(1, 100)) < save

    @staticmethod
    def format_affects(character: Character) -> str:
        AffectedBits = CharacterApi.get_enum("affectedBy")
        ApplyTypes = CharacterApi.get_enum("applyTypes")
        raw = GenericUtil.to_int(getattr(character.status_flags, "affected_by", 0), 0)
        show_details = GenericUtil.to_int(getattr(character, "level", 0), 0) >= 20
        lines = []
        seen_bits = set()
        listed_names = set()
        last_effect_type = None

        for effect in list(getattr(character, "effects", []) or []):
            effect_type = str(getattr(effect, "type", "") or "").strip()
            if not effect_type or effect_type.lstrip("-").isdigit():
                continue
            pretty = effect_type.removeprefix("spell.").removeprefix("skill.").replace("_", " ").lower()
            listed_names.add(pretty)
            bit = EffectUtil.enum_value(AffectedBits, getattr(effect, "bitvector", 0), 0)
            if bit != 0:
                seen_bits.add(bit)

            same_as_last = effect_type.lower() == last_effect_type
            if same_as_last and not show_details:
                continue

            prefix = " " * 22 if same_as_last else f"Spell: {pretty:<15}"
            if show_details:
                location = EffectUtil._affect_location_name(getattr(effect, "location", 0), ApplyTypes)
                modifier = GenericUtil.to_int(getattr(effect, "modifier", 0), 0)
                duration = GenericUtil.to_int(getattr(effect, "duration", 0), 0)
                duration_text = "permanently" if duration == -1 else f"for {duration} hours"
                lines.append(f"{prefix}: modifies {location} by {modifier} {duration_text}\r\n")
            else:
                lines.append(f"Spell: {pretty}\r\n")
            last_effect_type = effect_type.lower()

        for name, member in AffectedBits.__members__.items():
            if not CharacterApi.is_set(raw, member.value) or int(member.value) in seen_bits:
                continue
            pretty = name.replace("AFF_", "").replace("_", " ").lower()
            if pretty in listed_names:
                continue
            lines.append(f"Spell: {pretty}\r\n")

        if not lines:
            return "You are not affected by any spells.\r\n"
        return "You are affected by the following spells:\r\n" + "".join(lines)

    @staticmethod
    def _affect_location_name(location, apply_types) -> str:
        rom_names = {
            "APPLY_NONE": "none",
            "APPLY_STR": "strength",
            "APPLY_DEX": "dexterity",
            "APPLY_INT": "intelligence",
            "APPLY_WIS": "wisdom",
            "APPLY_CON": "constitution",
            "APPLY_SEX": "sex",
            "APPLY_CLASS": "class",
            "APPLY_LEVEL": "level",
            "APPLY_AGE": "age",
            "APPLY_MANA": "mana",
            "APPLY_HIT": "hp",
            "APPLY_MOVE": "moves",
            "APPLY_GOLD": "gold",
            "APPLY_EXP": "experience",
            "APPLY_AC": "armor class",
            "APPLY_HITROLL": "hit roll",
            "APPLY_DAMROLL": "damage roll",
            "APPLY_SAVES": "saves",
            "APPLY_SAVING_ROD": "save vs rod",
            "APPLY_SAVING_PETRI": "save vs petrification",
            "APPLY_SAVING_BREATH": "save vs breath",
            "APPLY_SAVING_SPELL": "save vs spell",
            "APPLY_SPELL_AFFECT": "none",
        }

        key = str(location or "").strip().upper()
        if key in rom_names:
            return rom_names[key]

        value = GenericUtil.to_int(location, None)
        if value is not None:
            for name in rom_names:
                if apply_types is not None and name in apply_types.__members__ and int(apply_types[name].value) == value:
                    return rom_names[name]

        return "(unknown)"

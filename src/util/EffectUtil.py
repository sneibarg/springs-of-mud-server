from __future__ import annotations

import ast
import random

from api.CharacterApi import CharacterApi
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
    _handler = None

    @classmethod
    def configure(cls, effect_handler) -> None:
        cls._handler = effect_handler

    @classmethod
    def handler(cls):
        if cls._handler is None:
            raise RuntimeError("EffectUtil has not been configured with an EffectHandler.")
        return cls._handler

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
    def remove_item_effects(character, item):
        return EffectUtil.handler().remove_item_effects(character, item)

    @staticmethod
    def is_affected(character, effect_type) -> bool:
        affected_by = CharacterApi.get_enum("affectedBy")
        if CharacterApi.is_affected(character, effect_type):
            return True
        if hasattr(affected_by, str(effect_type)):
            bit = getattr(affected_by, str(effect_type)).value
            return CharacterApi.is_affected(character, bit)
        return False

    @staticmethod
    def saves_dispel(dis_level: int, spell_level: int, duration: int) -> bool:
        save = 50 + (GenericUtil.to_int(spell_level, 0) - GenericUtil.to_int(dis_level, 0)) * 5
        if GenericUtil.to_int(duration, 0) == -1:
            save += 5
        save = max(5, min(95, save))
        return random.randint(1, 100) < save

    @staticmethod
    def saves_spell(level: int, victim, _dam_type: int = 0) -> bool:
        victim_level = GenericUtil.to_int(getattr(victim, "level", 0), 0)
        saving_throw = GenericUtil.to_int(getattr(victim, "saving_throw", 0), 0)
        save = 50 + (victim_level - GenericUtil.to_int(level, 0)) * 5 - saving_throw * 2
        if CharacterApi.is_affected_by_name(victim, CharacterApi.get_enum("affectedBy"), "AFF_BERSERK"):
            save += victim_level // 2
        save = max(5, min(95, save))
        return random.randint(1, 100) < save

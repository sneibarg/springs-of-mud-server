import random
import re
import time

from enum import IntEnum
from typing import Dict, Any, Iterable

from server.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_logger("GenericUtil")


class GenericUtil:
    pass

    @staticmethod
    def convert_numeric_to_string(value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, str):
            if value.lstrip('-').isdigit():
                return value
        return str(value) if value else '0'

    @staticmethod
    def to_int(value, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def to_float(value, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def letters_to_flags(value: str) -> int:
        total = 0
        for c in str(value or "").upper():
            if "A" <= c <= "Z":
                total |= (1 << (ord(c) - ord("A")))
        return total

    @staticmethod
    def flags_to_letters(value: int) -> str:
        if GenericUtil.to_int(value, 0) <= 0:
            return ""
        out = []
        raw = GenericUtil.to_int(value, 0)
        for bit in range(26):
            if raw & (1 << bit):
                out.append(chr(ord("A") + bit))
        return "".join(out)

    @staticmethod
    def flags_to_int(raw) -> int:
        value = GenericUtil.to_int(raw, None)
        if value is not None:
            return value
        return GenericUtil.letters_to_flags(str(raw or "0"))

    @staticmethod
    def camel_to_snake_case(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        if dictionary is None:
            return {}

        def camel_case_to_snake_case(string: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        snake_case_dict = {}
        try:
            snake_case_dict = {camel_case_to_snake_case(key): value for key, value in dictionary.items()}
        except AttributeError:
            logger.error(f"Error converting dictionary to snake case: {dictionary}")
        return snake_case_dict

    @staticmethod
    def build_int_enum(enum_name: str, enum_fields: dict[str, int] | list[str] | tuple[str, ...] | None) -> type[IntEnum]:
        if isinstance(enum_fields, dict):
            items: Iterable[tuple[str, int]] = (
                (str(member_name), int(member_value))
                for member_name, member_value in enum_fields.items()
            )
        elif isinstance(enum_fields, (list, tuple)):
            items = (
                (str(member_name), index)
                for index, member_name in enumerate(enum_fields)
            )
        else:
            raise TypeError(
                f"enum_fields for '{enum_name}' must be dict/list/tuple, got {type(enum_fields).__name__}"
            )

        members = {}
        for member_name, member_value in items:
            normalized_name = member_name.strip().upper()
            if not normalized_name:
                raise ValueError(f"Enum '{enum_name}' contains an empty member name")
            members[normalized_name] = member_value

        return IntEnum(enum_name, members)

    @staticmethod
    def generate_mongo_id() -> str:
        timestamp = int(time.time()).to_bytes(4, 'big')
        machine_id = random.getrandbits(24).to_bytes(3, 'big')
        process_id = random.getrandbits(16).to_bytes(2, 'big')
        counter = random.getrandbits(24).to_bytes(3, 'big')
        return (timestamp + machine_id + process_id + counter).hex()

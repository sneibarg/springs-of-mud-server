import re

from enum import IntEnum
from typing import Dict, Any, Iterable


class ServerUtil:
    pass

    @staticmethod
    def camel_to_snake_case(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        if dictionary is None:
            return {}

        def camel_case_to_snake_case(string: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        snake_case_dict = {}
        for key, value in dictionary.items():
            snake_case_dict[camel_case_to_snake_case(key)] = value
        return snake_case_dict

    @staticmethod
    def build_int_enum(enum_name: str, enum_fields: dict[str, int] | list[str] | tuple[str, ...]) -> type[IntEnum]:
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

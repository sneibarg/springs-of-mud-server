import re
from enum import StrEnum

from typing import Dict, Any


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
    def build_enum_lookup(enum_source: dict) -> dict[str, dict[str, int]]:
        """
        Build normalized lookup tables for all enums.

        Supports both:
          list enums  -> ["dead","mortal","standing"]
          dict enums  -> {"standing":8,"sleeping":4}
        """
        lookup = {}
        for enum_name, values in enum_source.items():
            if isinstance(values, dict):
                lookup[enum_name] = {str(k).lower(): int(v) for k, v in values.items()}
            else:
                lookup[enum_name] = {
                    str(v).lower(): i for i, v in enumerate(values)
                }

        return lookup

    @staticmethod
    def build_enum(field_prefix: str, enum_name: str, enum_fields: list[str]) -> type[StrEnum]:
        """
        Create enum:
            ITEM_LIGHT = "light"
            ITEM_SCROLL = "scroll"
            ...
        """
        members = {f"{field_prefix}_{name}": name.lower() for name in enum_fields}
        return StrEnum(enum_name, members)

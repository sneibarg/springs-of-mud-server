from __future__ import annotations

from enum import IntEnum
from typing import Type, TypeVar

T = TypeVar("T", bound=IntEnum)


class EnumProvider:
    def __init__(self, enums: dict[str, Type[IntEnum]]):
        self._enums: dict[str, Type[IntEnum]] = dict(enums)

    def get(self, name: str, default: Type[T] | None = None) -> Type[IntEnum] | Type[T]:
        try:
            return self._enums[name]
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"No enum registered with name '{name}'") from None

    def get_member(self, enum_name: str, member_name: str) -> IntEnum:
        enum_cls = self.get(enum_name)
        try:
            return enum_cls[member_name]
        except KeyError:
            raise KeyError(f"Enum '{enum_name}' has no member '{member_name}'") from None

    def get_value(self, enum_name: str, member_name: str) -> int:
        return self.get_member(enum_name, member_name).value

    def contains(self, enum_name: str) -> bool:
        return enum_name in self._enums

    def all_names(self) -> list[str]:
        return list(self._enums.keys())

    def __getitem__(self, name: str) -> Type[IntEnum]:
        return self.get(name)

    def __getattr__(self, enum_name: str) -> Type[IntEnum]:
        if enum_name in self._enums:
            return self._enums[enum_name]
        raise AttributeError(f"No enum named '{enum_name}'")
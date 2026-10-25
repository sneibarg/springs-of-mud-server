from __future__ import annotations

from dataclasses import dataclass
from game.ArmorValues import ArmorValues
from typing import Any


@dataclass
class ArmorClass(ArmorValues):
    piercing: int
    bashing: int
    slashing: int
    magic: int

    @classmethod
    def from_json(cls, data) -> ArmorClass:
        return cls(**data)

    def get_ac(self, char: Any, ac: int) -> int:
        from combat.ArmorDefense import legacy_armor_class
        return legacy_armor_class(self, char, ac)

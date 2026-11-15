from __future__ import annotations

from dataclasses import dataclass
from game.ArmorValues import ArmorValues


@dataclass
class ArmorClass(ArmorValues):
    piercing: int
    bashing: int
    slashing: int
    magic: int

    @classmethod
    def from_json(cls, data) -> ArmorClass:
        return cls(**data)

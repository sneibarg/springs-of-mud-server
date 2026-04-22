import ast
import json

from dataclasses import dataclass
from typing import Mapping


@dataclass
class PCArmorClass:
    piercing: int
    bashing: int
    slashing: int
    magic: int

    @classmethod
    def from_json(cls, data) -> PCArmorClass:
        return cls(**data)

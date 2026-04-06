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
    def from_json(cls, data):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            try:
                data = ast.literal_eval(data)
            except (SyntaxError, ValueError):
                data = json.loads(data.replace("'", '"'))

        if not isinstance(data, Mapping):
            raise TypeError(f"CharacterClass.from_json expected mapping or JSON string, got {type(data).__name__}")
        return cls(**data)

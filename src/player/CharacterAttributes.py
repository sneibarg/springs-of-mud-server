import json
import ast

from typing import Mapping
from dataclasses import dataclass


@dataclass
class CharacterAttributes:
    strength: int
    intelligence: int
    wisdom: int
    dexterity: int
    constitution: int
    alignment: int
    max_weight: int
    max_items: int
    position: int
    wimpy: int
    trains: int
    practices: int

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

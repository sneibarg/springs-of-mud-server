import ast
import json

from dataclasses import dataclass
from collections.abc import Mapping


@dataclass
class CharacterClass:
    name: str
    attr_prime: int
    weapon: int
    guild: int
    skill_adept: int
    thac0_00: int
    thac0_32: int
    hp_min: int
    hp_max: int
    mana_gain: bool
    base_group: str
    default_group: str

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

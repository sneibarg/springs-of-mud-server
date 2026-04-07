import json

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
    def from_json(cls, data) -> CharacterAttributes:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise TypeError(f"CharacterClass.from_json expected mapping or JSON string, got {type(data).__name__}")
        return cls(**data)

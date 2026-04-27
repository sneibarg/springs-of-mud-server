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
    points: int
    experience: int
    accumulated_experience: int
    experience_per_level: int

    @classmethod
    def from_json(cls, data) -> CharacterAttributes:
        from game.GenericUtil import GenericUtil
        return cls(**GenericUtil.camel_to_snake_case(data))

    @classmethod
    def default(cls) -> CharacterAttributes:
        return cls(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

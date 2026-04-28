from dataclasses import dataclass


@dataclass
class CharacterClass:
    name: str
    attr_prime: int
    weapon: int
    guild: int
    skill_adept: int
    thac000: int
    thac032: int
    hp_min: int
    hp_max: int
    mana_gain: bool
    base_group: str
    default_group: str

    @classmethod
    def from_json(cls, data):
        from util.GenericUtil import GenericUtil
        return cls(**GenericUtil.camel_to_snake_case(data))

from dataclasses import dataclass


@dataclass
class ArmorClass:
    piercing: int
    bashing: int
    slashing: int
    magic: int

    @classmethod
    def from_json(cls, data) -> ArmorClass:
        return cls(**data)

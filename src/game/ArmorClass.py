from dataclasses import dataclass


@dataclass
class ArmorClass:
    pierce: int
    slash: int
    bash: int
    exotic: int

    @classmethod
    def from_json(cls, data) -> ArmorClass:
        return cls(**data)

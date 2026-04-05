import json

from dataclasses import dataclass


@dataclass
class ArmorClass:
    pierce: int
    slash: int
    bash: int
    exotic: int

    @classmethod
    def from_json(cls, data) -> ArmorClass:
        try:
            data = json.loads(data.replace("'", '"'))
        except json.JSONDecodeError:
            print(f"ERROR: data={data}")
        return cls(**data)

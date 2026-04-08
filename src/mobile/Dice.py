import json
from dataclasses import dataclass


@dataclass
class Dice:
    number: int
    type: int
    bonus: int

    @staticmethod
    def _parse_dice(value: str):
        try:
            if value is None:
                value = str({"number": 0, "type": 0, "bonus": 0})
            dice = json.loads(value.replace("'", '"'))
            return dice
        except json.JSONDecodeError:
            return {"number": 0, "type": 0, "bonus": 0}

    @classmethod
    def from_json(cls, value: str):
        return cls(**Dice._parse_dice(value))

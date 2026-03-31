from dataclasses import dataclass


@dataclass
class Dice:
    number: int
    type: int
    bonus: int

    @staticmethod
    def _parse_dice(value: str):
        text = str(value).strip().lower()
        if "d" in text:
            left, right = text.split("d", 1)
            if "+" in right:
                die_type, bonus = right.split("+", 1)
            else:
                die_type, bonus = right, "0"
            return {"number": int(left or 0), "type": int(die_type or 0), "bonus": int(bonus or 0)}
        return {"number": 0, "type": 0, "bonus": 0}

    @classmethod
    def get_dice(cls, value: str):
        if value is None:
            value = str({"number": 0, "type": 0, "bonus": 0})
        return cls(**Dice._parse_dice(value))

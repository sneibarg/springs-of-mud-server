from dataclasses import dataclass
from typing import Any


@dataclass
class ArmorClass:
    piercing: int
    bashing: int
    slashing: int
    magic: int

    @classmethod
    def from_json(cls, data) -> ArmorClass:
        return cls(**data)

    def get_ac(self, char: Any, ac: int) -> int:
        from api.CharacterApi import CharacterApi
        key = ac
        if isinstance(ac, int):
            if ac == 0:
                key = "pierce"
            elif ac == 1:
                key = "bash"
            elif ac == 2:
                key = "slash"
            elif ac == 3:
                key = "exotic"
            else:
                key = "pierce"

        if isinstance(key, str):
            normalized_key = key.lower()
            if normalized_key in ("pierce", "piercing"):
                base = getattr(self, "piercing", getattr(self, "pierce", 0))
            elif normalized_key == "bash":
                base = getattr(self, "bashing", getattr(self, "bash", 0))
            elif normalized_key == "slash":
                base = getattr(self, "slashing", getattr(self, "slash", 0))
            else:
                base = getattr(self, "magic", getattr(self, "exotic", 0))
        else:
            base = 0

        dex_value = 0
        if hasattr(char, "character_attributes"):
            dex_value = getattr(char.character_attributes, "dexterity", 0)
        dex_defensive = CharacterApi.get_attribute_bonus("dexterity", str(dex_value)).get("defensive", 0)
        return int(base) + int(dex_defensive)

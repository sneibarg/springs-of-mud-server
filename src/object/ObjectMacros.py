from enum import IntEnum
from typing import Dict, List

from game import GameData
from object import Item


class ObjectMacros:
    def __init__(self, game_data: GameData):
        self.game_data = game_data

    def can_wear(self, obj: Item, part: int) -> bool:
        pass

    def is_obj_stat(self, obj: Item, stat: int) -> bool:
        pass

    def is_weapon_stat(self, obj: Item, stat: int) -> bool:
        pass

    def weight_multiplier(self, obj: Item) -> int:
        pass

    def decode_form_and_parts(self, race_name: str, BodyForm: type[IntEnum], BodyParts: type[IntEnum]) -> Dict[str, List[str]]:
        race = self.game_data.races.get(race_name)
        if not race:
            return {"form": [], "parts": []}

        form_value: int = race.get("form", 0)
        parts_value: int = race.get("parts", 0)

        decoded_form = [member.name for member in BodyForm if form_value & member.value]
        decoded_parts = [member.name for member in BodyParts if parts_value & member.value]

        return {
            "form": decoded_form,
            "parts": decoded_parts
        }

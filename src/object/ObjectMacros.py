from enum import IntEnum
from typing import Dict, List
from game.GameMacros import GameMacros
from object import Item


class ObjectMacros(GameMacros):
    def __init__(self, races: dict, item_table: dict, ItemTypes: type[IntEnum]):
        self.races = races
        self.item_table = item_table
        self.ItemTypes = ItemTypes

    def can_wear(self, obj: Item, part: int) -> bool:
        return self.is_set(int(obj.wear_flags), part)

    def is_obj_stat(self, obj: Item, stat: int) -> bool:
        return self.is_set(int(obj.extra_flags), stat)

    def is_weapon_stat(self, obj: Item, stat: int) -> bool:
        return self.is_set(int(obj.value4), stat)

    def weight_multiplier(self, obj: Item) -> int:
        return int(obj.value3) if self.item_table[obj.item_type] == self.ItemTypes.ITEM_CONTAINER.name else 100

    def decode_form_and_parts(self, race_name: str, BodyForm: type[IntEnum], BodyParts: type[IntEnum]) -> Dict[str, List[str]]:
        race = self.races.get(race_name)
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

from enum import IntEnum
from typing import Dict, List
from object import Item


class ObjectMacros:
    def __init__(self, races: dict, item_table: dict, ItemTypes: type[IntEnum]):
        self.races = races
        self.item_table = item_table
        self.ItemTypes = ItemTypes

    @staticmethod
    def is_set(flag: int, bit) -> bool:
        if hasattr(bit, "value"):
            return (flag & bit.value) != 0
        return (flag & bit) != 0

    def can_wear(self, obj: Item, part: int) -> bool:
        return self.is_set(int(obj.wear_flags), part)

    def is_obj_stat(self, obj: Item, stat: int) -> bool:
        return self.is_set(int(obj.extra_flags), stat)

    def is_weapon_stat(self, obj: Item, stat: int) -> bool:
        return self.is_set(int(obj.value4), stat)

    def weight_multiplier(self, obj: Item) -> int:
        return obj.value3 if self.item_table[obj.item_type] == self.ItemTypes.ITEM_CONTAINER.name else 100

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

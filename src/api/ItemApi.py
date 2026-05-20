from enum import IntEnum
from typing import Any, Dict, List

from api.GameApi import GameApi
from item.Item import Item
from player.Character import Character
from util.GenericUtil import GenericUtil


class ItemApi(GameApi):
    @classmethod
    def race_data(cls, race_name: str) -> dict:
        return cls._races_map().get(race_name, {})

    @classmethod
    def is_container_closed(cls, item) -> bool:
        try:
            flags = int(item.value1)
            container_state = cls.get_enum("containerState")
            if not hasattr(container_state, "CONT_CLOSED"):
                return False
            return cls.is_set(flags, container_state.CONT_CLOSED.value)
        except (TypeError, ValueError):
            return False

    @classmethod
    def can_wear(cls, obj: Item, part: int) -> bool:
        return cls.is_set(int(obj.wear_flags), part)

    @classmethod
    def is_obj_stat(cls, obj: Item, stat: int) -> bool:
        return cls.is_set(int(obj.extra_flags), stat)

    @classmethod
    def is_weapon_stat(cls, obj: Item, stat: int) -> bool:
        return cls.is_set(int(obj.value4), stat)

    @classmethod
    def weight_multiplier(cls, obj: Item) -> int:
        item_types = cls.get_enum("itemTypes")
        item_table = cls._item_table_map()
        return int(obj.value3) if item_table[obj.item_type] == item_types.ITEM_CONTAINER.name else 100

    @classmethod
    def decode_form_and_parts(cls, race_name: str, BodyForm: type[IntEnum], BodyParts: type[IntEnum]) -> Dict[str, List[str]]:
        race = cls._races_map().get(race_name)
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

    @classmethod
    def item_takeable(cls, obj: Any, wear_flags_enum) -> bool:
        take_bit = cls.enum_bit(wear_flags_enum, "ITEM_TAKE")
        if take_bit == 0:
            return False
        wear_flags = GameApi.flags_to_int(getattr(obj, "wear_flags", 0))
        return (wear_flags & take_bit) != 0

    @staticmethod
    def find_comparable_equipped_item(character: Character, source_item):
        src_type = str(getattr(source_item, "item_type", "") or "").strip().lower()
        equipped = getattr(character, "equipped", None)
        for slot_item in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
            if slot_item is None or slot_item == source_item:
                continue
            item_type = str(getattr(slot_item, "item_type", "") or "").strip().lower()
            if item_type == src_type:
                return slot_item
        return None

    @staticmethod
    def compare_value(item) -> int | None:
        item_type = str(getattr(item, "item_type", "") or "").strip().lower()
        if "weapon" in item_type:
            dam_min = GenericUtil.to_int(getattr(item, "value1", 0), 0)
            dam_max = GenericUtil.to_int(getattr(item, "value2", 0), 0)
            return (dam_min + dam_max) // 2
        if "armor" in item_type:
            return GenericUtil.to_int(getattr(item, "value0", 0), 0)
        return None

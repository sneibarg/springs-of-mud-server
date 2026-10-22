from enum import IntEnum
from typing import Any, Dict, List

from api.GameApi import GameApi
from item.Item import Item
from player.Character import Character
from util.GenericUtil import GenericUtil


class ItemApi(GameApi):
    @classmethod
    def race_data(cls, race_name: str) -> dict:
        return cls.races_map().get(race_name, {})

    @classmethod
    def lazy_load(cls) -> None:
        cls.load_enums(
            TimeAndWeather="timeAndWeather",
            GameParameters="gameParameters",
            AffectedBits="affectedBy",
            positions="positions",
            RoomFlags="roomFlags",
            CommFlags="commFlags",
            PlayerActBits="playerActBits",
            OffenseTypes="offenseTypes",
            SectorTypes="sectorTypes",
            ItemFlags="itemFlags",
        )

    @classmethod
    def is_no_sac(cls, item: Item) -> bool:
        wear_flags = cls.get_enum("wearFlags")
        no_sac = cls.enum_bit(wear_flags, "ITEM_NO_SAC")
        return not cls.item_takeable(item, wear_flags) or cls.is_set(
            cls.flags_to_int(item.wear_flags), no_sac
        )

    @classmethod
    def can_loot(cls, character, item, owners) -> bool:
        """Apply ROM ownership rules against entities currently in the world."""
        from api.CharacterApi import CharacterApi

        if CharacterApi.is_immortal(character):
            return True
        owner_name = str(getattr(item, "owner", "") or "").casefold()
        if not owner_name:
            return True
        owner = next((entity for entity in owners
                      if str(getattr(entity, "name", "") or "").casefold() == owner_name), None)
        if owner is None:
            return True
        if str(getattr(character, "name", "") or "").casefold() == owner_name:
            return True
        can_loot = cls.enum_bit(cls.get_enum("playerActBits"), "PLR_CANLOOT")
        if not CharacterApi.is_npc(owner) and cls.is_set(
            getattr(getattr(owner, "status_flags", None), "act", 0), can_loot
        ):
            return True
        return CharacterApi.is_same_group(character, owner)

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
        extra_flags = GameApi.flags_to_int(obj.extra_flags)
        return cls.is_set(extra_flags, stat)

    @classmethod
    def has_item_flag(cls, obj: Item, item_flags_enum, *flag_names: str) -> bool:
        bit = cls.enum_bit(item_flags_enum, *flag_names)
        if bit == 0:
            return False
        return cls.is_obj_stat(obj, bit)

    @classmethod
    def is_weapon_stat(cls, obj: Item, stat: int) -> bool:
        return cls.is_set(int(obj.value4), stat)

    @staticmethod
    def carried_count(character) -> int:
        return sum(Item.object_number(item) for item in character.owned_items())

    @staticmethod
    def carried_weight(character, *, include_coins=True) -> int:
        weight = sum(Item.object_weight(item) for item in character.owned_items())
        if include_coins:
            weight += GenericUtil.to_int(getattr(character, "silver", 0), 0) // 10
            weight += GenericUtil.to_int(getattr(character, "gold", 0), 0) * 2 // 5
        return weight

    @classmethod
    def weight_multiplier(cls, obj: Item) -> int:
        return Item.weight_multiplier(obj)

    @classmethod
    def decode_form_and_parts(cls, race_name: str, BodyForm: type[IntEnum], BodyParts: type[IntEnum]) -> Dict[str, List[str]]:
        race = cls.races_map().get(race_name)
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
            return True
        wear_flags = GameApi.flags_to_int(obj.wear_flags)
        return (wear_flags & take_bit) != 0

    @staticmethod
    def find_comparable_equipped_item(character: Character, source_item):
        src_type = str(source_item.item_type or "").strip().lower()
        equipped = character.equipped
        for slot_item in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
            if slot_item is None or slot_item == source_item:
                continue
            item_type = str(slot_item.item_type or "").strip().lower()
            if item_type == src_type:
                return slot_item
        return None

    @staticmethod
    def compare_value(item) -> int | None:
        item_type = str(item.item_type or "").strip().lower()
        if "weapon" in item_type:
            dam_min = GenericUtil.to_int(item.value1, 0)
            dam_max = GenericUtil.to_int(item.value2, 0)
            return (dam_min + dam_max) // 2
        if "armor" in item_type:
            return GenericUtil.to_int(item.value0, 0)
        return None

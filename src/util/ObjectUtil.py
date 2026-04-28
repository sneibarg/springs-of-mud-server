from __future__ import annotations

from game.Equipped import Equipped, WEAR_LOC_TO_EQUIPPED_SLOT
from game.GameMacros import GameMacros
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil


class ObjectUtils:
    EQUIPPED_SLOT_TO_WEAR_LOC = {slot: wear_loc for wear_loc, slot in WEAR_LOC_TO_EQUIPPED_SLOT.items()}
    WEAR_SLOT_ORDER = {
        "ITEM_WEAR_FINGER": ("finger1", "finger2"),
        "ITEM_WEAR_NECK": ("neck1", "neck2"),
        "ITEM_WEAR_BODY": ("torso",),
        "ITEM_WEAR_HEAD": ("head",),
        "ITEM_WEAR_LEGS": ("legs",),
        "ITEM_WEAR_FEET": ("feet",),
        "ITEM_WEAR_HANDS": ("hands",),
        "ITEM_WEAR_ARMS": ("arms",),
        "ITEM_WEAR_SHIELD": ("shield",),
        "ITEM_WEAR_ABOUT": ("body",),
        "ITEM_WEAR_WAIST": ("waist",),
        "ITEM_WEAR_WRIST": ("wrist1", "wrist2"),
        "ITEM_WIELD": ("wielded",),
        "ITEM_HOLD": ("held",),
        "ITEM_WEAR_FLOAT": ("floating_nearby",),
    }

    @staticmethod
    def parse_raw_arguments(raw_result, parameters) -> tuple[str, str]:
        text = (raw_result if isinstance(raw_result, str) else "").strip()
        if not text:
            text = " ".join(parameters or []).strip()
        a1, rest = InterpUtil.one_argument(text)
        a2, rest2 = InterpUtil.one_argument(rest)
        if a2 in ("from", "in", "on"):
            a2, rest2 = InterpUtil.one_argument(rest2)
        return a1, f"{a2} {rest2}".strip()

    @staticmethod
    def has_flag(raw_flags, bit_value: int) -> bool:
        return (GameMacros.flags_to_int(raw_flags) & int(bit_value)) != 0

    @staticmethod
    def ensure_equipped(character):
        if getattr(character, "equipped", None) is None:
            character.equipped = Equipped()
        return character.equipped

    @staticmethod
    def find_inventory_item(character, wanted: str):
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for item in list(getattr(character, "loot", []) or []):
            name = (getattr(item, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return item
        return None

    @staticmethod
    def find_room_item(room, wanted: str):
        if room is None:
            return None
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for item in room.contents.values():
            name = (getattr(item, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return item
        return None

    @staticmethod
    def find_character_in_room(room, actor, wanted: str):
        if room is None:
            return None
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for ch in room.characters.values():
            if ch.id == actor.id:
                continue
            name = (getattr(ch, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return ch
        return None

    @staticmethod
    def find_container(character, room, wanted: str):
        return ObjectUtils.find_inventory_item(character, wanted) or ObjectUtils.find_room_item(room, wanted)

    @staticmethod
    def remove_from_inventory(character, item):
        loot = getattr(character, "loot", None)
        if loot is None:
            return
        try:
            loot.remove(item)
        except ValueError:
            pass

    @staticmethod
    def add_to_inventory(character, item):
        if getattr(character, "loot", None) is None:
            character.loot = []
        if item not in character.loot:
            character.loot.append(item)

    @staticmethod
    def equipped_slot_of(character, item):
        equipped = getattr(character, "equipped", None)
        if equipped is None:
            return None
        for slot, equipped_item in equipped.__dict__.items():
            if equipped_item is item:
                return slot
        return None

    @staticmethod
    def equip_item(character, item, slot_name: str):
        equipped = ObjectUtils.ensure_equipped(character)
        ObjectUtils.remove_from_inventory(character, item)
        setattr(equipped, slot_name, item)
        setattr(item, "wear_location", slot_name)
        setattr(item, "wear_loc", ObjectUtils.EQUIPPED_SLOT_TO_WEAR_LOC.get(slot_name, -1))
        return slot_name

    @staticmethod
    def unequip_item(character, slot_name: str):
        equipped = getattr(character, "equipped", None)
        if equipped is None or not hasattr(equipped, slot_name):
            return None
        item = getattr(equipped, slot_name)
        setattr(equipped, slot_name, None)
        if item is not None:
            setattr(item, "wear_location", "")
            setattr(item, "wear_loc", -1)
            ObjectUtils.add_to_inventory(character, item)
        return item

    @staticmethod
    def find_wear_slot(character, item, wear_flags_enum, forced: str = ""):
        equipped = ObjectUtils.ensure_equipped(character)
        if forced:
            slot = forced.strip().lower()
            return slot if hasattr(equipped, slot) and getattr(equipped, slot) is None else None

        flags = GameMacros.flags_to_int(getattr(item, "wear_flags", 0))
        for flag_name, slots in ObjectUtils.WEAR_SLOT_ORDER.items():
            if wear_flags_enum is None or not hasattr(wear_flags_enum, flag_name):
                continue
            bit = getattr(wear_flags_enum, flag_name).value
            if (flags & bit) == 0:
                continue
            for slot in slots:
                if getattr(equipped, slot) is None:
                    return slot
        return None

    @staticmethod
    def item_takeable(item, wear_flags_enum) -> bool:
        if wear_flags_enum is None or not hasattr(wear_flags_enum, "ITEM_TAKE"):
            return True
        return ObjectUtils.has_flag(getattr(item, "wear_flags", 0), wear_flags_enum.ITEM_TAKE.value)

    @staticmethod
    def is_nodrop(item, item_flags_enum) -> bool:
        if item_flags_enum is None or not hasattr(item_flags_enum, "ITEM_NODROP"):
            return False
        return ObjectUtils.has_flag(getattr(item, "extra_flags", 0), item_flags_enum.ITEM_NODROP.value)

    @staticmethod
    def is_nosac(item, item_flags_enum) -> bool:
        if item_flags_enum is None or not hasattr(item_flags_enum, "ITEM_NO_SAC"):
            return False
        return ObjectUtils.has_flag(getattr(item, "extra_flags", 0), item_flags_enum.ITEM_NO_SAC.value)

    @staticmethod
    def item_type_name(item) -> str:
        return str(getattr(item, "item_type", "") or "").strip().upper()

    @staticmethod
    def is_pc_corpse(item) -> bool:
        return ObjectUtils.item_type_name(item) == "ITEM_CORPSE_PC"

    @staticmethod
    def is_npc_corpse(item) -> bool:
        return ObjectUtils.item_type_name(item) == "ITEM_CORPSE_NPC"

    @staticmethod
    def is_corpse(item) -> bool:
        item_type = ObjectUtils.item_type_name(item)
        return item_type in {"ITEM_CORPSE_NPC", "ITEM_CORPSE_PC"}

    @staticmethod
    def sacrifice_silver_value(item) -> int:
        silver = max(1, GenericUtil.to_int(getattr(item, "level", 1), 0) * 3)
        if not ObjectUtils.is_corpse(item):
            silver = min(silver, max(0, GenericUtil.to_int(getattr(item, "cost", 0), 0)))
        return silver

    @staticmethod
    def sacrifice_reward_message(silver: int) -> str:
        if GenericUtil.to_int(silver, 0) == 1:
            return "Mota gives you one silver coin for your sacrifice.\r\n"
        return f"Mota gives you {GenericUtil.to_int(silver, 0)} silver coins for your sacrifice.\r\n"

    @staticmethod
    def is_container(item) -> bool:
        item_type = (getattr(item, "item_type", "") or "").upper()
        return "ITEM_CONTAINER" in item_type or "CONTAINER" in item_type

    @staticmethod
    def short(item) -> str:
        return getattr(item, "short_description", None) or getattr(item, "name", "it")

    @staticmethod
    def add_to_contains(container, obj):
        if getattr(container, "contains", None) is None:
            container.contains = []
        container.contains.append(obj)

    @staticmethod
    def remove_from_contains(container, obj):
        try:
            container.contains.remove(obj)
        except Exception:
            pass

    @staticmethod
    def find_in_contains(container, wanted: str):
        q = (wanted or "").strip().lower()
        for obj in list(getattr(container, "contains", []) or []):
            name = (getattr(obj, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return obj
        return None

    @staticmethod
    def first_fountain(room):
        if room is None:
            return None
        for item in room.contents.values():
            if "FOUNTAIN" in ((getattr(item, "item_type", "") or "").upper()):
                return item
        return None

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from item.Item import Item

WEAR_LOC_TO_EQUIPPED_SLOT = {
    0: "light",
    1: "finger1",
    2: "finger2",
    3: "neck1",
    4: "neck2",
    5: "torso",
    6: "head",
    7: "legs",
    8: "feet",
    9: "hands",
    10: "arms",
    11: "shield",
    12: "body",
    13: "waist",
    14: "wrist1",
    15: "wrist2",
    16: "wielded",
    17: "held",
    18: "floating_nearby",
}
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


@dataclass
class Equipped:
    light: Optional[Item] = None
    finger1: Optional[Item] = None
    finger2: Optional[Item] = None
    neck1: Optional[Item] = None
    neck2: Optional[Item] = None
    torso: Optional[Item] = None
    head: Optional[Item] = None
    legs: Optional[Item] = None
    feet: Optional[Item] = None
    hands: Optional[Item] = None
    arms: Optional[Item] = None
    shield: Optional[Item] = None
    body: Optional[Item] = None
    waist: Optional[Item] = None
    wrist1: Optional[Item] = None
    wrist2: Optional[Item] = None
    wielded: Optional[Item] = None
    held: Optional[Item] = None
    floating_nearby: Optional[Item] = None

    def format_equipped(self) -> str:
        return "\n".join(f"{slot}: {item.name}" for slot, item in self.__dict__.items() if item)

    def slot_of(self, item) -> Optional[str]:
        for slot, equipped_item in self.__dict__.items():
            if equipped_item is item:
                return slot
        return None

    @staticmethod
    def ensure_on(character):
        if getattr(character, "equipped", None) is None:
            character.equipped = Equipped()
        return character.equipped

    @staticmethod
    def add_to_inventory(character, item) -> None:
        if hasattr(character, "add_item"):
            character.add_item(item)
            return
        if getattr(character, "loot", None) is None:
            character.loot = []
        if item not in character.loot:
            character.loot.append(item)

    @staticmethod
    def remove_from_inventory(character, item) -> None:
        if hasattr(character, "remove_item"):
            character.remove_item(item)
            return
        loot = getattr(character, "loot", None)
        if loot is None:
            return
        try:
            loot.remove(item)
        except ValueError:
            pass

    @classmethod
    def equip_item(cls, character, item, slot_name: str):
        equipped = cls.ensure_on(character)
        cls.remove_from_inventory(character, item)
        setattr(equipped, slot_name, item)
        setattr(item, "wear_location", slot_name)
        setattr(item, "wear_loc", EQUIPPED_SLOT_TO_WEAR_LOC.get(slot_name, -1))
        return slot_name

    @classmethod
    def unequip_item(cls, character, slot_name: str):
        equipped = getattr(character, "equipped", None)
        if equipped is None or not hasattr(equipped, slot_name):
            return None
        item = getattr(equipped, slot_name)
        setattr(equipped, slot_name, None)
        if item is not None:
            setattr(item, "wear_location", "")
            setattr(item, "wear_loc", -1)
            cls.add_to_inventory(character, item)
        return item

    @staticmethod
    def is_light_item(item) -> bool:
        return str(getattr(item, "item_type", "") or "").strip().lower() == "light"

    def is_shield_equipped(self) -> bool:
        return self.shield is None

    @classmethod
    def wear_slot_groups_for_item(cls, item, wear_flags_enum, *, preferred_slot: str = "", forced_slot: str = "") -> list[tuple[str, ...]]:
        from item.ItemMacros import ItemMacros

        groups: list[tuple[str, ...]] = []
        requested = (forced_slot or preferred_slot or "").strip().lower()

        if cls.is_light_item(item):
            groups.append(("light",))

        flags = ItemMacros.flags_to_int(getattr(item, "wear_flags", 0))
        for flag_name, slots in WEAR_SLOT_ORDER.items():
            if wear_flags_enum is None or not hasattr(wear_flags_enum, flag_name):
                continue
            if (flags & getattr(wear_flags_enum, flag_name).value) == 0:
                continue
            groups.append(tuple(slots))

        if not requested:
            return groups

        if requested in ("hold", "held") and cls.is_light_item(item):
            requested = "light"
        return [slots for slots in groups if requested in slots]

    def resolve_wear_slot(self, character, slots: tuple[str, ...], replace: bool, *,
                          can_remove_item: Callable[[object], bool],
                          remove_item: Callable[[object, str, object], None]) -> tuple[str | None, dict]:
        for slot in slots:
            if getattr(self, slot, None) is None:
                return slot, {}

        combined_payload = {"to_char": "", "to_room": ""}
        if not replace:
            return None, combined_payload

        for slot in slots:
            removed, payload = self.remove_equipped_item(character, slot, replace=replace, can_remove_item=can_remove_item, remove_item=remove_item)
            combined_payload["to_char"] += payload.get("to_char", "")
            combined_payload["to_room"] += payload.get("to_room", "")
            if removed:
                return slot, combined_payload

        return None, combined_payload

    def remove_equipped_item(self, character, slot: str, *, replace: bool,
                             can_remove_item: Callable[[object], bool],
                             remove_item: Callable[[object, str, object], None]) -> tuple[bool, dict]:
        if not hasattr(self, slot):
            return True, {"to_char": "", "to_room": ""}

        item = getattr(self, slot)
        if item is None:
            return True, {"to_char": "", "to_room": ""}
        if not replace:
            return False, {"to_char": "", "to_room": ""}
        if not can_remove_item(item):
            return False, {"to_char": f"You can't remove {self.short(item)}.\r\n", "to_room": ""}

        remove_item(character, slot, item)
        return True, {
            "to_char": f"You stop using {self.short(item)}.\r\n",
            "to_room": f"{character.name} stops using {self.short(item)}.\r\n",
        }

    @staticmethod
    def build_wear_payload(character, room, to_char: str, to_room: str = "") -> dict:
        payload = {"to_char": to_char}
        if room is not None and to_room:
            payload["to_room"] = to_room
            payload["targets"] = room.player_targets(character)
        return payload

    @classmethod
    def slot_wear_payload(cls, character, room, item, slot: str) -> dict:
        short = cls.short(item)
        templates = {
            "light": (f"You light {short} and hold it.\r\n", f"{character.name} lights {short} and holds it.\r\n"),
            "finger1": (f"You wear {short} on your left finger.\r\n", f"{character.name} wears {short} on their left finger.\r\n"),
            "finger2": (f"You wear {short} on your right finger.\r\n", f"{character.name} wears {short} on their right finger.\r\n"),
            "neck1": (f"You wear {short} around your neck.\r\n", f"{character.name} wears {short} around their neck.\r\n"),
            "neck2": (f"You wear {short} around your neck.\r\n", f"{character.name} wears {short} around their neck.\r\n"),
            "torso": (f"You wear {short} on your torso.\r\n", f"{character.name} wears {short} on their torso.\r\n"),
            "head": (f"You wear {short} on your head.\r\n", f"{character.name} wears {short} on their head.\r\n"),
            "legs": (f"You wear {short} on your legs.\r\n", f"{character.name} wears {short} on their legs.\r\n"),
            "feet": (f"You wear {short} on your feet.\r\n", f"{character.name} wears {short} on their feet.\r\n"),
            "hands": (f"You wear {short} on your hands.\r\n", f"{character.name} wears {short} on their hands.\r\n"),
            "arms": (f"You wear {short} on your arms.\r\n", f"{character.name} wears {short} on their arms.\r\n"),
            "body": (f"You wear {short} about your torso.\r\n", f"{character.name} wears {short} about their torso.\r\n"),
            "waist": (f"You wear {short} about your waist.\r\n", f"{character.name} wears {short} about their waist.\r\n"),
            "wrist1": (f"You wear {short} around your left wrist.\r\n", f"{character.name} wears {short} around their left wrist.\r\n"),
            "wrist2": (f"You wear {short} around your right wrist.\r\n", f"{character.name} wears {short} around their right wrist.\r\n"),
            "shield": (f"You wear {short} as a shield.\r\n", f"{character.name} wears {short} as a shield.\r\n"),
            "wielded": (f"You wield {short}.\r\n", f"{character.name} wields {short}.\r\n"),
            "held": (f"You hold {short} in your hand.\r\n", f"{character.name} holds {short} in their hand.\r\n"),
            "floating_nearby": (f"You release {short} and it floats next to you.\r\n", f"{character.name} releases {short} and it floats next to them.\r\n"),
        }
        to_char, to_room = templates.get(slot, (f"You wear {short}.\r\n", f"{character.name} wears {short}.\r\n"))
        return cls.build_wear_payload(character, room, to_char, to_room)

    @staticmethod
    def short(item) -> str:
        return getattr(item, "short_description", None) or getattr(item, "name", "it")

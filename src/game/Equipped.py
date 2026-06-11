from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional
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
class WearResult:
    blocked_key: str = ""
    blocked_tokens: dict = field(default_factory=dict)
    shared_messages: list[tuple[str, dict]] = field(default_factory=list)
    char_messages: list[tuple[str, dict]] = field(default_factory=list)


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
        if character.equipped is None:
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
        return str(item.item_type or "").strip().lower() == "light"

    def is_shield_equipped(self) -> bool:
        return self.shield is None

    @classmethod
    def wear_slot_groups_for_item(cls, item, wear_flags_enum, *, preferred_slot: str = "", forced_slot: str = "") -> list[tuple[str, ...]]:
        from api.ItemApi import ItemApi

        groups: list[tuple[str, ...]] = []
        requested = (forced_slot or preferred_slot or "").strip().lower()

        if cls.is_light_item(item):
            groups.append(("light",))

        flags = ItemApi.flags_to_int(item.wear_flags)
        for flag_name, slots in WEAR_SLOT_ORDER.items():
            if wear_flags_enum is None or flag_name not in wear_flags_enum.__members__:
                continue
            if (flags & wear_flags_enum[flag_name].value) == 0:
                continue
            groups.append(tuple(slots))

        if not requested:
            return groups

        if requested in ("hold", "held") and cls.is_light_item(item):
            requested = "light"
        return [slots for slots in groups if requested in slots]

    @classmethod
    def wear_item(cls, character, item, wear_flags_enum, item_flags, *, replace: bool,
                  preferred_slot: str = "", forced_slot: str = "", effect_handler=None) -> WearResult:
        result = WearResult()
        item_short = Item.short(item)
        item_level = int(item.level or 0)
        if int(character.level or 0) < item_level:
            result.blocked_key = "insufficientLevel"
            result.blocked_tokens = {"d": item_level, "t": item_short}
            return result

        slot_groups = cls.wear_slot_groups_for_item(item, wear_flags_enum, preferred_slot=preferred_slot, forced_slot=forced_slot)
        if not slot_groups:
            result.blocked_key = "invalidTargetThere" if forced_slot else "invalidTarget"
            return result

        equipped = cls.ensure_on(character)
        selected_slot, removal = equipped.resolve_wear_slot(
            character,
            slot_groups[0],
            replace,
            can_remove_item=lambda worn_item: cls._can_remove_item(worn_item, item_flags),
            remove_item=lambda owner, slot_name, worn_item: cls._remove_item(owner, slot_name, worn_item, effect_handler=effect_handler),
        )
        if removal.get("blocked_key"):
            result.blocked_key = str(removal.get("blocked_key", "") or "")
            result.blocked_tokens = dict(removal.get("tokens", {}) or {})
            return result
        if removal.get("key"):
            result.shared_messages.append((removal["key"], dict(removal.get("tokens", {}) or {})))
        if selected_slot is None:
            return result

        if selected_slot == "shield":
            weapon = character.equipped.wielded
            if weapon is not None and int(character.size_value()) < int(character.large_size_value()) and bool(weapon.is_two_handed_weapon()):
                result.blocked_key = "weaponTwoHanded"
                return result

        if selected_slot == "wielded":
            if bool(item.weapon_too_heavy(character)):
                result.blocked_key = "tooHeavy"
                return result

            shield = character.equipped.shield
            if shield is not None and int(character.size_value()) < int(character.large_size_value()) and bool(item.is_two_handed_weapon()):
                result.blocked_key = "wearingShield"
                return result

        character.equip_item(item, selected_slot)
        if effect_handler is not None:
            effect_handler.apply_item_effects(character, item)
        result.shared_messages.append(cls.slot_message(selected_slot, item_short))
        skill_key = item.weapon_skill_feedback_key(character)
        if selected_slot == "wielded" and skill_key:
            result.char_messages.append((skill_key, {"t": item_short}))
        return result

    @classmethod
    def wear_all(cls, character, wear_flags_enum, item_flags, *, effect_handler=None) -> WearResult:
        result = WearResult()
        for item in list(character.loot or []):
            item_result = cls.wear_item(character, item, wear_flags_enum, item_flags, replace=False, effect_handler=effect_handler)
            result.shared_messages.extend(item_result.shared_messages)
            result.char_messages.extend(item_result.char_messages)
        return result

    def resolve_wear_slot(self, character, slots: tuple[str, ...], replace: bool, *,
                          can_remove_item: Callable[[object], bool],
                          remove_item: Callable[[object, str, object], None]) -> tuple[str | None, dict]:
        for slot in slots:
            if getattr(self, slot, None) is None:
                return slot, {}

        combined_payload: dict = {}
        if not replace:
            return None, combined_payload

        for slot in slots:
            removed, payload = self.remove_equipped_item(character, slot, replace=replace, can_remove_item=can_remove_item, remove_item=remove_item)
            if removed:
                return slot, payload
            if payload:
                return None, payload

        return None, combined_payload

    def find_remove_target(self, query: str) -> tuple[str, object | None]:
        wanted = str(query or "").strip().lower()
        if not wanted:
            return "", None
        if hasattr(self, wanted):
            return wanted, getattr(self, wanted)

        for slot, item in self.__dict__.items():
            if item is None:
                continue
            name = str(item.name or "").strip().lower()
            if name == wanted or name.startswith(wanted):
                return slot, item
        return "", None

    def remove_equipped_item(self, character, slot: str, *, replace: bool,
                             can_remove_item: Callable[[object], bool],
                             remove_item: Callable[[object, str, object], None]) -> tuple[bool, dict]:
        if not hasattr(self, slot):
            return True, {}

        item = getattr(self, slot)
        if item is None:
            return True, {}
        if not replace:
            return False, {}
        if not can_remove_item(item):
            return False, {"blocked_key": "noRemove", "tokens": {"t": Item.short(item)}}

        remove_item(character, slot, item)
        return True, {"key": "removed", "tokens": {"t": Item.short(item)}}

    @classmethod
    def remove_item(cls, character, slot: str, item, item_flags, *, effect_handler=None) -> WearResult:
        result = WearResult()
        if item is None:
            return result
        if not cls._can_remove_item(item, item_flags):
            result.blocked_key = "noRemove"
            result.blocked_tokens = {"t": Item.short(item)}
            return result

        cls._remove_item(character, slot, item, effect_handler=effect_handler)
        result.shared_messages.append(("removed", {"t": Item.short(item)}))
        return result

    @staticmethod
    def build_wear_payload(character, room, to_char: str, to_room: str = "") -> dict:
        payload = {"to_char": to_char}
        if room is not None and to_room:
            payload["to_room"] = to_room
            payload["targets"] = room.player_targets(character)
        return payload

    @classmethod
    def slot_wear_payload(cls, character, room, item, slot: str) -> dict:
        short = Item.short(item)
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
    def slot_message(slot: str, item_short: str) -> tuple[str, dict]:
        templates = {
            "light": ("light", {"t": item_short}),
            "finger1": ("finger", {"t": item_short, "s": "left"}),
            "finger2": ("finger", {"t": item_short, "s": "right"}),
            "neck1": ("neck", {"t": item_short}),
            "neck2": ("neck", {"t": item_short}),
            "torso": ("torso", {"t": item_short}),
            "head": ("head", {"t": item_short}),
            "legs": ("legs", {"t": item_short}),
            "feet": ("feet", {"t": item_short}),
            "hands": ("hands", {"t": item_short}),
            "arms": ("arms", {"t": item_short}),
            "body": ("aboutTorso", {"t": item_short}),
            "waist": ("aboutWaist", {"t": item_short}),
            "wrist1": ("wrist", {"t": item_short, "s": "left"}),
            "wrist2": ("wrist", {"t": item_short, "s": "right"}),
            "shield": ("shield", {"t": item_short}),
            "wielded": ("wield", {"t": item_short}),
            "held": ("hold", {"t": item_short}),
            "floating_nearby": ("float", {"t": item_short}),
        }
        return templates.get(slot, ("invalidTarget", {}))

    @staticmethod
    def _can_remove_item(item, item_flags) -> bool:
        return bool(item.can_remove(item_flags))

    @staticmethod
    def _remove_item(character, slot: str, item, *, effect_handler=None) -> None:
        if effect_handler is not None:
            effect_handler.remove_item_effects(character, item)
        character.unequip_item(slot)


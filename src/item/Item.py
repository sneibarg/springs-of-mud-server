from __future__ import annotations

import json
import threading

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

from api.GameApi import GameApi
from item.ExtraDescriptionData import ExtraDescriptionData
from item.Effect import Effect
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil

if TYPE_CHECKING:
    from area.Room import Room
    from player.Character import Character


@dataclass
class FillResult:
    blocked_key: str = ""
    liquid_name: str = ""


@dataclass
class PourResult:
    blocked_key: str = ""
    liquid_name: str = ""
    amount: int = 0


@dataclass
class Item:
    id: str
    area_id: str
    vnum: str
    name: str
    short_description: str
    long_description: str
    material: str
    item_type: str
    extra_flags: str
    wear_flags: str
    value0: str
    value1: str
    value2: str
    value3: str
    value4: str
    condition: str
    level: int
    weight: int
    cost: int
    affect_data: list
    contains: list
    count: int = 0
    room_data: dict[str, Room] = field(default_factory=dict)
    enchanted: Optional[bool] = False
    timer: Optional[int] = None
    damage_type: Optional[str] = None
    weapon_type: Optional[str] = None
    liquid_color: Optional[str] = None
    liquid_affect_data: Optional[list] = None
    effects: Optional[List[Effect]] = None
    extra_description: Optional[ExtraDescriptionData] = None

    def __post_init__(self):
        self.__name__ = "Item"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.lock = threading.RLock()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.id == other.id
        return False

    def contents(self) -> str:
        text = ""
        if len(self.contains) > 0:
            for item in self.contains:
                text = text + "\t" + item.name + "\r\n"
        return text

    def short(self) -> str:
        return self.short_description or self.name or "it"

    def add_contained_item(self, item) -> None:
        with self.lock:
            if self.contains is None:
                self.contains = []
            self.contains.append(item)

    def remove_contained_item(self, item) -> bool:
        with self.lock:
            contents = self.contains or []
            try:
                contents.remove(item)
                return True
            except ValueError:
                return False

    def find_contained_item(self, wanted: str):
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for obj in list(self.contains or []):
            name = (obj.name or "").lower()
            if name == q or name.startswith(q):
                return obj
        return None

    def add_item_to_room(self, room: Room):
        with self.lock:
            if room.id not in self.room_data:
                self.room_data[room.id] = room

    def remove_item_from_room(self, room: Room):
        with self.lock:
            if room.id in self.room_data:
                del self.room_data[room.id]

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from util.GenericUtil import GenericUtil
        data = GenericUtil.camel_to_snake_case(data)
        data['contains'] = []
        data['effects'] = [
            effect if isinstance(effect, Effect) else Effect.from_json(effect)
            for effect in list(data.get('effects', []) or [])
        ]
        extra_descr = data.pop('extra_descr', None)
        item = cls(**data)
        if extra_descr is not None:
            item.extra_descr = extra_descr
        cls.update_extra_description(item)
        return item

    @staticmethod
    def update_extra_description(item):
        extra_descr = list(getattr(item, "extra_descr", []) or [])
        if len(extra_descr) >= 2:
            keyword = str(extra_descr[0] or "").strip()
            description = str(extra_descr[1] or "")
            item.extra_description = ExtraDescriptionData(valid=True, keyword=keyword, description=description) if (keyword or description) else None
            return item.extra_description

        extra_description = getattr(item, "extra_description", None)
        if extra_description:
            try:
                item.extra_description = ExtraDescriptionData.from_json(extra_description)
            except (TypeError, ValueError):
                item.extra_description = None
            return item.extra_description

        item.extra_description = None
        return None

    @staticmethod
    def is_drink_container(item) -> bool:
        item_type = str(item.item_type or "").strip().lower()
        return ("drink" in item_type) or ("fountain" in item_type)

    @staticmethod
    def is_fountain(item) -> bool:
        item_type = str(item.item_type or "").strip().lower()
        return "fountain" in item_type

    def is_edible(self) -> bool:
        item_type = str(self.item_type or "").strip().lower()
        return ("food" in item_type) or ("pill" in item_type)

    @staticmethod
    def _item_type(item) -> str:
        return str(item.item_type or "").strip().lower()

    @classmethod
    def item_type_name(cls, item) -> str:
        return cls._item_type(item).upper()

    @classmethod
    def is_container_like(cls, item) -> bool:
        item_type = cls._item_type(item)
        return ("container" in item_type) or ("corpse" in item_type)

    @classmethod
    def is_container(cls, item) -> bool:
        return "container" in cls._item_type(item)

    @classmethod
    def is_pc_corpse(cls, item) -> bool:
        return cls.item_type_name(item) == "ITEM_CORPSE_PC"

    @classmethod
    def is_npc_corpse(cls, item) -> bool:
        return cls.item_type_name(item) == "ITEM_CORPSE_NPC"

    @classmethod
    def is_corpse(cls, item) -> bool:
        return cls.item_type_name(item) in {"NPC_CORPSE", "CORPSE_PC"}

    @classmethod
    def is_potion(cls, item) -> bool:
        return "potion" in cls._item_type(item)

    @classmethod
    def is_scroll(cls, item) -> bool:
        return "scroll" in cls._item_type(item)

    @classmethod
    def is_staff(cls, item) -> bool:
        return "staff" in cls._item_type(item)

    @classmethod
    def is_wand(cls, item) -> bool:
        return "wand" in cls._item_type(item)

    @staticmethod
    def spell_level(item) -> int:
        return GenericUtil.to_int(item.value0, 0)

    @staticmethod
    def spell_refs(item, *slots: int) -> list:
        refs = []
        for slot in slots:
            value = getattr(item, f"value{int(slot)}", "")
            if str(value or "").strip():
                refs.append(value)
        return refs

    @staticmethod
    def charges(item) -> int:
        return GenericUtil.to_int(item.value2, 0)

    @staticmethod
    def spend_charge(item) -> int:
        remaining = Item.charges(item) - 1
        item.value2 = str(remaining)
        return remaining

    @classmethod
    def inspect_pour(cls, source, destination=None, *, pour_out: bool = False) -> PourResult:
        result = PourResult()
        if source is None:
            result.blocked_key = "targetMissing"
            return result
        if cls.is_fountain(source) or not cls.is_drink_container(source):
            result.blocked_key = "notContainer"
            return result

        source_amount = GenericUtil.to_int(source.value1, 0)
        source_liquid = str(source.value2 or "")
        result.liquid_name = source_liquid

        if pour_out:
            if source_amount <= 0:
                result.blocked_key = "emptyTarget"
                return result
            result.amount = source_amount
            return result

        if destination is None:
            result.blocked_key = "pourTargetMissing"
            return result
        if cls.is_fountain(destination) or not cls.is_drink_container(destination):
            result.blocked_key = "targetContainerInvalid"
            return result
        if destination is source:
            result.blocked_key = "targetSelf"
            return result

        dest_amount = GenericUtil.to_int(destination.value1, 0)
        dest_capacity = GenericUtil.to_int(destination.value0, 0)
        dest_liquid = str(destination.value2 or "")
        if dest_amount > 0 and dest_liquid != source_liquid:
            result.blocked_key = "invalidLiquid"
            return result
        if source_amount <= 0:
            result.blocked_key = "missingLiquid"
            return result
        if dest_capacity > 0 and dest_amount >= dest_capacity:
            result.blocked_key = "filled"
            return result

        result.amount = min(source_amount, max(0, dest_capacity - dest_amount))
        return result

    @classmethod
    def pour(cls, source, destination=None, *, pour_out: bool = False) -> PourResult:
        result = cls.inspect_pour(source, destination, pour_out=pour_out)
        if result.blocked_key:
            return result

        if pour_out:
            source.value1 = "0"
            source.value3 = "0"
            return result

        dest_amount = GenericUtil.to_int(destination.value1, 0)
        source_amount = GenericUtil.to_int(source.value1, 0)
        destination.value1 = str(dest_amount + result.amount)
        source.value1 = str(source_amount - result.amount)
        destination.value2 = result.liquid_name
        return result

    @staticmethod
    def first_fountain(room):
        if room is None:
            return None
        for item in room.contents.values():
            if Item.is_fountain(item):
                return item
        return None

    @classmethod
    def inspect_fill(cls, destination, source) -> FillResult:
        result = FillResult()
        if source is None:
            result.blocked_key = "sourceMissing"
            return result
        if cls.is_fountain(destination) or not cls.is_drink_container(destination) or not cls.is_drink_container(source):
            result.blocked_key = "notContainer"
            return result

        dest_capacity = GenericUtil.to_int(destination.value0, 0)
        dest_amount = GenericUtil.to_int(destination.value1, 0)
        if dest_capacity > 0 and dest_amount >= dest_capacity:
            result.blocked_key = "containerFull"
            return result

        source_liquid = str(source.value2 or "")
        dest_liquid = str(destination.value2 or "")
        if dest_amount > 0 and source_liquid and dest_liquid != source_liquid:
            result.blocked_key = "differentLiquid"
            return result

        if not cls.is_fountain(source):
            source_amount = GenericUtil.to_int(source.value1, 0)
            if source_amount <= 0:
                result.blocked_key = "sourceEmpty"
                return result

        result.liquid_name = source_liquid
        return result

    @classmethod
    def fill_from_source(cls, destination, source) -> FillResult:
        result = cls.inspect_fill(destination, source)
        if result.blocked_key:
            return result

        destination_capacity = GenericUtil.to_int(destination.value0, 0)
        source_amount = GenericUtil.to_int(source.value1, 0)
        if result.liquid_name:
            destination.value2 = result.liquid_name
        destination.value1 = str(destination_capacity if destination_capacity > 0 else source_amount)
        return result

    def weapon_too_heavy(self, character: Character) -> bool:
        from api.CharacterApi import CharacterApi
        if CharacterApi.is_npc(character):
            return False
        strength = max(0, GenericUtil.to_int(character.character_attributes.strength, 0))
        try:
            strength_bonus = CharacterApi.get_attribute_bonus("strength", str(character.level))
        except RuntimeError:
            strength_bonus = {}
        wield_limit = GenericUtil.to_int(strength_bonus.get(str(strength), {}).get("wield", 0), 0) * 10
        return 0 < wield_limit < GenericUtil.to_int(self.weight, 0)

    def is_two_handed_weapon(self) -> bool:
        from api.CharacterApi import CharacterApi
        try:
            weapon_flags = CharacterApi.get_enum("weaponType")
        except RuntimeError:
            return False
        if not hasattr(weapon_flags, "WEAPON_TWO_HANDS"):
            return False
        return GameApi.is_set(self.value4, weapon_flags.WEAPON_TWO_HANDS.value)

    def can_remove(self, item_flags) -> bool:
        from api.CharacterApi import CharacterApi
        no_remove_bit = CharacterApi.enum_bit(item_flags, "ITEM_NOREMOVE")
        if no_remove_bit == 0:
            return True
        return not GameApi.is_set(self.extra_flags, no_remove_bit)

    def weapon_skill_feedback_key(self, character: Character) -> str:
        from api.CharacterApi import CharacterApi
        if CharacterApi.is_npc(character):
            return ""

        try:
            weapon_class = CharacterApi.get_enum("weaponClass")
        except RuntimeError:
            weapon_class = None
        if weapon_class is None:
            return ""

        skill_map = {
            getattr(weapon_class, "WEAPON_SWORD", None): "sword",
            getattr(weapon_class, "WEAPON_DAGGER", None): "dagger",
            getattr(weapon_class, "WEAPON_SPEAR", None): "spear",
            getattr(weapon_class, "WEAPON_MACE", None): "mace",
            getattr(weapon_class, "WEAPON_AXE", None): "axe",
            getattr(weapon_class, "WEAPON_FLAIL", None): "flail",
            getattr(weapon_class, "WEAPON_WHIP", None): "whip",
            getattr(weapon_class, "WEAPON_POLEARM", None): "polearm",
        }
        class_value = GenericUtil.to_int(self.value0, 0)
        skill_name = ""
        for enum_member, name in skill_map.items():
            if enum_member is not None and class_value == int(enum_member.value):
                skill_name = name
                break
        if not skill_name:
            return ""

        skill = 0
        for entry in list(character.skills or []):
            if isinstance(entry, dict):
                entry_name = str(entry.get("name", "")).strip().lower()
                entry_level = entry.get("level", 0)
            else:
                entry_name = str(entry.name).strip().lower()
                entry_level = entry.level
            if entry_name == skill_name:
                skill = max(0, min(100, GenericUtil.to_int(entry_level, 0)))
                break

        if skill >= 100:
            return "skill100"
        if skill > 85:
            return "skill85"
        if skill > 70:
            return "skill70"
        if skill > 50:
            return "skill50"
        if skill > 25:
            return "skill25"
        if skill > 1:
            return "skill1"
        return "skill0"

from __future__ import annotations

import threading

from dataclasses import dataclass, field
from typing import Any, Optional, TYPE_CHECKING

from game.Equipped import Equipped
from player.CharacterAttributes import CharacterAttributes
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil

if TYPE_CHECKING:
    from item.Item import Item


@dataclass
class AnimateEntity:
    id: str
    area_id: str
    room_id: str
    name: str
    sex: str
    level: int
    gold: int
    silver: int
    fighting: Optional[Any] = field(default=None, kw_only=True)
    master: Optional[Any] = field(default=None, kw_only=True)
    leader: Optional[Any] = field(default=None, kw_only=True)
    equipped: Optional[Equipped] = field(default=None, kw_only=True)
    inventory: list[Any] = field(default_factory=list, kw_only=True)
    effects: list[Any] = field(default_factory=list, kw_only=True)
    status_flags: Optional[Any] = field(default=None, kw_only=True)
    character_attributes: Optional[CharacterAttributes] = field(default=None, kw_only=True)
    armor_class: Optional[Any] = field(default=None, kw_only=True)
    lock: threading.RLock = field(default_factory=threading.RLock, kw_only=True)

    def __post_init__(self):
        logger_name = self.__dict__["__name__"] if "__name__" in self.__dict__ else self.__class__.__name__
        self.logger = LoggerFactory.get_logger(logger_name)
        if self.lock is None:
            self.lock = threading.RLock()

    def get_alignment(self) -> int:
        return GenericUtil.to_int(self.character_attributes.alignment, 0)

    def set_alignment(self, value: int) -> None:
        attrs = self.character_attributes
        if attrs is not None:
            attrs.alignment = int(value)
            return
        setattr(self, "alignment", int(value))

    def _item_collection_name(self) -> str:
        loot = getattr(self, "loot", None)
        if loot is not None:
            return "loot"
        return "inventory"

    def _item_collection(self) -> list[Any]:
        collection_name = self._item_collection_name()
        collection = getattr(self, collection_name, None)
        if collection is None:
            collection = []
            setattr(self, collection_name, collection)
        return collection

    def add_item(self, item: Any) -> None:
        with self.lock:
            collection = self._item_collection()
            if item not in collection:
                collection.append(item)

    def remove_item(self, item: Any) -> bool:
        with self.lock:
            inv = self._item_collection()
            try:
                inv.remove(item)
                return True
            except ValueError:
                return False

    def find_inventory_item(self, wanted: str) -> Optional[Item]:
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for item in list(self._item_collection()):
            name = (item.name or "").lower()
            if name == q or name.startswith(q):
                return item
        return None

    def ensure_equipped(self):
        return Equipped.ensure_on(self)

    def equipped_slot_of(self, item: Item) -> Optional[str]:
        equipped = self.equipped
        if equipped is None:
            return None
        return equipped.slot_of(item)

    def equip_item(self, item: Item, slot_name: str):
        return Equipped.equip_item(self, item, slot_name)

    def unequip_item(self, slot_name: str):
        return Equipped.unequip_item(self, slot_name)

    def owned_items(self) -> list:
        seen = set()
        items = []
        for item in list(getattr(self, "loot", []) or []):
            item_id = id(item)
            if item is not None and item_id not in seen:
                items.append(item)
                seen.add(item_id)
        equipped = getattr(self, "equipped", None)
        for item in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
            item_id = id(item)
            if item is not None and item_id not in seen:
                items.append(item)
                seen.add(item_id)
        return items

    def find_owned_item(self, wanted: str):
        key = (wanted or "").strip().lower()
        if not key:
            return None
        for item in self.owned_items():
            name = (item.name or "").lower()
            if name == key or name.startswith(key):
                return item
        return None

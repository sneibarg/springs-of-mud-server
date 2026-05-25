from __future__ import annotations

import threading

from dataclasses import dataclass, field
from typing import Any, Optional, TYPE_CHECKING

from game.Equipped import Equipped
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
    leader: Optional[Any] = field(default=None, kw_only=True)
    equipped: Optional[Equipped] = field(default=None, kw_only=True)
    inventory: list[Any] = field(default_factory=list, kw_only=True)
    effects: list[Any] = field(default_factory=list, kw_only=True)
    status_flags: Optional[Any] = field(default=None, kw_only=True)
    character_attributes: Optional[Any] = field(default=None, kw_only=True)
    armor_class: Optional[Any] = field(default=None, kw_only=True)
    lock: threading.RLock = field(default_factory=threading.RLock, kw_only=True)

    def __post_init__(self):
        self.logger = LoggerFactory.get_logger(getattr(self, "__name__", self.__class__.__name__))
        if self.lock is None:
            self.lock = threading.RLock()

    def get_alignment(self) -> int:
        attrs = getattr(self, "character_attributes", None)
        if attrs is not None:
            return GenericUtil.to_int(getattr(attrs, "alignment", 0), 0)
        return GenericUtil.to_int(getattr(self, "alignment", 0), 0)

    def set_alignment(self, value: int) -> None:
        attrs = getattr(self, "character_attributes", None)
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
            name = (getattr(item, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return item
        return None

    def ensure_equipped(self):
        return Equipped.ensure_on(self)

    def equipped_slot_of(self, item: Item) -> Optional[str]:
        equipped = getattr(self, "equipped", None)
        if equipped is None:
            return None
        return equipped.slot_of(item)

    def equip_item(self, item: Item, slot_name: str):
        return Equipped.equip_item(self, item, slot_name)

    def unequip_item(self, slot_name: str):
        return Equipped.unequip_item(self, slot_name)

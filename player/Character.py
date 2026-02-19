import threading
from asyncio import StreamWriter, StreamReader
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from injector import Injector
from object.Item import Item
from server.LoggerFactory import LoggerFactory


@dataclass
class Character:
    id: str
    account_id: str
    title: str
    description: str
    cloaked: bool
    guild: str
    race: str
    name: str
    area_id: str
    room_id: str
    character_class: str
    guild: str
    role: str
    sex: str
    cloaked: bool
    level: int
    health: int
    mana: int
    movement: int
    experience: int
    accumulated_experience: int
    trains: int
    practices: int
    gold: int
    silver: int
    wimpy: int
    position: int
    max_weight: int
    max_items: int
    reputation: int
    piercing: int
    bashing: int
    slashing: int
    magic: int
    injector: Injector
    inventory: List[str]
    loot: Dict[str, object] = field(default_factory=dict)
    # statuses: List[str] = field(default_factory=list)
    # skills: List[str] = field(default_factory=list)
    # cmd: Optional[str] = None
    writer: Optional[StreamWriter] = None
    reader: Optional[StreamReader] = None
    lock: threading.Lock = field(default_factory=threading.Lock)

    def __post_init__(self):
        self.logger = LoggerFactory.get_logger(__name__)
        self.load_inventory()

    def load_inventory(self):
        with self.lock:
            self.logger.info("Loading inventory...")
            for item in self.inventory:
                lootable = Item.from_json(item)
                self.loot[lootable.id] = lootable
            self.logger.info("Inventory loaded.")

    def get_items(self):
        return self.loot.values()

    def get_fuzzy_item(self, fuzzy_item, usage):
        fuzzy_item = fuzzy_item.strip().replace("\r\n", "")
        self.logger.debug("get_fuzzy_item: fuzzy_item=" + str(fuzzy_item))
        for item_id in self.loot:
            lootable = self.loot[item_id]
            if not isinstance(lootable, Item):
                self.logger.debug("get_fuzzy_item: lootable=" + str(lootable))
                continue
            if lootable.name.startswith(fuzzy_item) or fuzzy_item == lootable.name:
                return lootable
        usage(self)

    @classmethod
    def from_json(cls, data):
        return cls(**data)


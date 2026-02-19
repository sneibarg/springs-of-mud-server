import threading
from asyncio import StreamWriter, StreamReader
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from uuid import uuid1
from injector import Injector
from object.Item import Item
from server import LoggerFactory
from utilities.mobile_util import move_mobile
from utilities.player_util import print_room


@dataclass
class RomMobile:
    area_id: str
    vnum: str
    name: str
    short_description: str
    long_description: str
    description: str
    act_flags: str
    affect_flags: str
    alignment: str
    race: str
    sex: str
    start_pos: str
    default_pos: str
    id: str
    level: int
    inventory: List[str]
    injector: Optional[Injector] = None
    writer: Optional[StreamWriter] = None
    reader: Optional[StreamReader] = None
    loot: Optional[Dict[str, Item]] = None
    lock: threading.Lock = field(default_factory=threading.Lock)

    def __init__(self):
        self.role = None
        self.room_id = None

    def __post_init__(self):
        self.instance_id = uuid1()
        if self.lock is None:
            self.lock = threading.Lock()
        self.__name__ = "Mobile-" + str(self.instance_id)
        self.logger = LoggerFactory.get_logger(self.__name__)
        if self.loot is None:
            self.loot = self.load_inventory()
        self.logger.info("Instantiated " + self.__name__)

    @classmethod
    def from_json(cls, data):
        data.setdefault('injector', None)
        data.setdefault('writer', None)
        data.setdefault('reader', None)
        data.setdefault('loot', None)
        data.setdefault('lock', None)
        return cls(**data)

    def load_inventory(self) -> Dict[str, Item]:
        with self.lock:
            loot = {}
            for item in self.get_items():
                loot[item.name] = item
        return loot

    def get_fuzzy_item(self, fuzzy_item, usage):
        fuzzy_item = fuzzy_item.strip().replace("\r\n", "")
        self.logger.debug("get_fuzzy_item: fuzzy_item=" + str(fuzzy_item))
        for lootable in self.loot:
            if not isinstance(self.loot[lootable], Item):
                self.logger.debug("get_fuzzy_item: lootable=" + str(lootable))
                continue
            if lootable.startswith(fuzzy_item) or fuzzy_item == lootable:
                return self.loot[lootable]
        usage(self)

    def get_items(self):
        from object import ItemService
        if self.injector is None:
            self.logger.error("Injector is not initialized.")
            return []
        object_service = self.injector.get(ItemService)
        items = [Item.from_json(object_service.get_item_by_id(item_id)) for item_id in self.inventory]
        self.logger.debug("get_items: " + str(items))
        return items

    def move_mobile(self, area_service, direction):
        result = move_mobile(area_service, self, direction)
        self.logger.info("move_mobile: " + str(result))
        if result is not None:
            self.room_id = result.id
            print_room(area_service, self.writer, self)

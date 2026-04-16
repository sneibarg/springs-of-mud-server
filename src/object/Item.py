import json
import threading

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

from object.ExtraDescriptionData import ExtraDescriptionData
from object.AffectData import AffectData
from server.LoggerFactory import LoggerFactory

if TYPE_CHECKING:
    from area.Room import Room


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
    extra_descr: list
    contains: list
    count: int = 0
    room_data: dict[str, Room] = field(default_factory=dict)
    enchanted: Optional[bool] = False
    timer: Optional[int] = None
    damage_type: Optional[str] = None
    weapon_type: Optional[str] = None
    liquid_color: Optional[str] = None
    liquid_affect_data: Optional[list] = None
    effects: Optional[List[AffectData]] = None
    extra_description: Optional[ExtraDescriptionData] = None

    def __post_init__(self):
        self.__name__ = "Item"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.lock = threading.Lock()

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

    def add_item_to_room(self, room: Room):
        with self.lock:
            if self.room_data[room.id] is None:
                self.room_data[room.id] = room

    def remove_item_from_room(self, room: Room):
        with self.lock:
            if room.id in self.room_data:
                del self.room_data[room.id]

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from game.GenericUtil import GenericUtil
        data = GenericUtil.camel_to_snake_case(data)
        data['contains'] = []
        return cls(**data)




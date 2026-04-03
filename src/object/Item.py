import json

from dataclasses import dataclass
from typing import Optional, List
from object.ExtraDescriptionData import ExtraDescriptionData
from object.AffectData import AffectData
from server.LoggerFactory import LoggerFactory


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
    weight: str
    condition: str
    level: int
    weight: int
    cost: int
    affect_data: list
    extra_descr: list
    enchanted: Optional[bool] = False
    timer: Optional[int] = None
    damage_type: Optional[str] = None
    weapon_type: Optional[str] = None
    liquid_color: Optional[str] = None
    liquid_affect_data: Optional[list] = None
    effects: Optional[List[AffectData]] = None
    extra_description: Optional[ExtraDescriptionData] = None
    room_index_data: Optional[dict] = None

    def __post_init__(self):
        self.__name__ = "Item"
        self.logger = LoggerFactory.get_logger(self.__name__)

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)




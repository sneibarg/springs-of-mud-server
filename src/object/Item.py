import json

from dataclasses import dataclass
from typing import Optional
from server.ServerUtil import ServerUtil
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
    damage_type: Optional[str] = None
    weapon_type: Optional[str] = None
    liquid_affect_data: Optional[list] = None

    def __post_init__(self):
        self.__name__ = "Item"
        self.logger = LoggerFactory.get_logger(self.__name__)

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)

    def get_name(self):
        return self.name

    def print_name(self, writer):
        msg = "\t" + self.name + "\r\n"
        writer.write(msg.encode('utf-8'))

    def print_description(self, writer):
        if writer is None:
            self.logger.debug("print_description: writer="+str(writer)+", item_id="+str(id))
            return
        msg = "\r\n\n" + self.long_description + "\r\n\n"
        writer.write(msg.encode('utf-8'))


from dataclasses import dataclass
from typing import Tuple
from area import Room
from area.Reset import Reset
from area.Shop import Shop
from area.Special import Special
from object.Item import Item
from mobile.Mobile import Mobile
from server.LoggerFactory import LoggerFactory


@dataclass
class Area:
    author: str
    name: str
    id: str
    description: str = ""
    reset_msg: str = ""
    vnum: str = ""
    security: str = "0"
    min_vnum: str = "0"
    max_vnum: str = "0"
    age: int = 15
    number_of_players: int = 0
    suggested_level_range: str = None
    vnum_range: Tuple[int, int] | Tuple[int, ...] = None
    area_flags: list = None
    rooms: list[Room] = None
    mobiles: list[Mobile] = None
    objects: list[Item] = None
    shops: list[Shop] = None
    resets: list[Reset] = None
    specials: list[Special] = None
    empty: bool = False

    def __post_init__(self):
        self.__name__ = f"Area.{self.name}"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.vnum_range = self.parse_vnum_range(self.suggested_level_range)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Area):
            return self.id == other.id
        return False

    def parse_vnum_range(self, vnum_range: str) -> tuple[int, int] | tuple[int, ...]:
        if vnum_range is None or vnum_range == "None" or not vnum_range.strip():
            return 0, 0
        parts = vnum_range.split()
        if len(parts) != 2:
            self.logger.warning(f"Invalid vnum range format: '{vnum_range}'")
            return 0, 0
        return tuple(int(x.strip()) for x in parts)

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        if data['suggested_level_range'] == "All":
            data['suggested_level_range'] = "1 50"
        data['suggested_level_range'] = data['suggested_level_range'].replace("-", " ")
        if 'area_id' in data:
            data['id'] = data.pop('area_id')
        return cls(**data)

from dataclasses import dataclass
from typing import Tuple, Optional

from area import Reset
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
    age: int = 0
    number_of_players: int = 0
    suggested_level_range: Tuple[int, int] = None
    vnum_range: Tuple[int, int] = None
    area_flags: list = None
    rooms: list = None
    mobiles: list = None
    objects: list = None
    shops: list = None
    resets: list = None
    specials: list = None
    reset_first: Optional[Reset] = None
    reset_last: Optional[Reset] = None

    def __post_init__(self):
        self.__name__ = f"Area.{self.name}"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Area):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        if 'area_id' in data:
            data['id'] = data.pop('area_id')
        return cls(**data)

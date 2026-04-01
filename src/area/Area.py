from dataclasses import dataclass
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
    last_reset: int = 0
    suggested_level_range: tuple = None
    area_flags: list = None
    rooms: list = None
    mobiles: list = None
    objects: list = None
    shops: list = None
    resets: list = None
    specials: list = None

    def __post_init__(self):
        self.__name__ = "Area"
        self.logger = LoggerFactory.get_logger(self.__name__)

    @classmethod
    def from_json(cls, data):
        if 'area_id' in data:
            data['id'] = data.pop('area_id')
        return cls(**data)

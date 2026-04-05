from dataclasses import dataclass
from server.LoggerFactory import LoggerFactory


@dataclass
class Special:
    id: str
    area_id: str
    mob_vnum: str
    special_function: str
    comment: str

    def __post_init__(self):
        self.__name__ = "Special"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Special):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)

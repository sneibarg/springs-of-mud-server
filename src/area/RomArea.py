from dataclasses import dataclass


@dataclass
class RomArea:
    author: str
    name: str
    id: str
    suggested_level_range: tuple
    rooms: list
    mobiles: list
    objects: list
    shops: list
    resets: list
    specials: list

    def __post_init__(self):
        self.__name__ = "RomArea"
        from server import LoggerFactory
        self.logger = LoggerFactory.get_logger(self.__name__)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

from dataclasses import dataclass
from server.LoggerFactory import LoggerFactory


@dataclass
class Reset:
    id: str
    area_id: str
    command: str
    arg1: str
    arg2: str
    arg3: str
    arg4: str
    comment: str

    def __post_init__(self):
        self.__name__ = "Reset"
        self.logger = LoggerFactory.get_logger(self.__name__)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

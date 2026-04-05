from dataclasses import dataclass
from enum import IntEnum
from server.LoggerFactory import LoggerFactory


class ShopEnum(IntEnum):
    MAX_TRADE = 5


@dataclass
class Shop:
    id: str
    area_id: str
    comment: str
    keeper: int
    buy_type0: int
    buy_type1: int
    buy_type2: int
    buy_type3: int
    buy_type4: int
    profit_buy: int
    profit_sell: int
    open_hour: int
    close_hour: int

    def __post_init__(self):
        self.__name__ = "Shop"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Shop):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)

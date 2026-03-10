from dataclasses import dataclass


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
    buy_type5: int
    profit_buy: int
    profit_sell: int
    open_hour: int
    close_hour: int

    def __init__(self):
        pass

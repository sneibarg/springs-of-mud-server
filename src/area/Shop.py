from dataclasses import dataclass
from enum import IntEnum
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil


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

    @property
    def buy_types(self) -> tuple[int, ...]:
        return (
            GenericUtil.to_int(self.buy_type0, 0),
            GenericUtil.to_int(self.buy_type1, 0),
            GenericUtil.to_int(self.buy_type2, 0),
            GenericUtil.to_int(self.buy_type3, 0),
            GenericUtil.to_int(self.buy_type4, 0),
        )

    def matches_keeper_vnum(self, keeper_vnum: str | int) -> bool:
        return str(GenericUtil.to_int(self.keeper, 0)) == str(GenericUtil.to_int(keeper_vnum, -1))

    def is_open_at(self, hour: int) -> bool:
        current_hour = GenericUtil.to_int(hour, -1)
        if current_hour < 0:
            return True
        return GenericUtil.to_int(self.open_hour, 0) <= current_hour <= GenericUtil.to_int(self.close_hour, 23)

    def buys_item(self, item, item_types) -> bool:
        if item is None or item_types is None:
            return False
        item_type_name = str(getattr(item, "item_type", "") or "").strip().upper()
        if not item_type_name or not hasattr(item_types, item_type_name):
            return False
        item_type_value = int(getattr(item_types, item_type_name).value)
        return item_type_value in self.buy_types

    def buy_price(self, item) -> int:
        if item is None:
            return 0
        base_cost = GenericUtil.to_int(getattr(item, "cost", 0), 0)
        price = base_cost * GenericUtil.to_int(self.profit_buy, 0) // 100
        return self._charge_adjusted_price(item, price)

    def sell_price(self, item, keeper_inventory: list, item_types, item_flags) -> int:
        if item is None or not self.buys_item(item, item_types):
            return 0

        price = GenericUtil.to_int(getattr(item, "cost", 0), 0) * GenericUtil.to_int(self.profit_sell, 0) // 100
        sell_extract_bit = 0
        inventory_bit = 0
        if item_flags is not None:
            if hasattr(item_flags, "ITEM_SELL_EXTRACT"):
                sell_extract_bit = int(getattr(item_flags, "ITEM_SELL_EXTRACT").value)
            if hasattr(item_flags, "ITEM_INVENTORY"):
                inventory_bit = int(getattr(item_flags, "ITEM_INVENTORY").value)

        item_extra_flags = GenericUtil.to_int(getattr(item, "extra_flags", 0), 0)
        if sell_extract_bit == 0 or (item_extra_flags & sell_extract_bit) == 0:
            for stocked in list(keeper_inventory or []):
                if not self._same_stock_item(item, stocked):
                    continue
                stocked_flags = GenericUtil.to_int(getattr(stocked, "extra_flags", 0), 0)
                if inventory_bit and (stocked_flags & inventory_bit) != 0:
                    price //= 2
                else:
                    price = price * 3 // 4

        return self._charge_adjusted_price(item, price)

    @staticmethod
    def _same_stock_item(left, right) -> bool:
        return (
            left is not None
            and right is not None
            and str(getattr(left, "vnum", "") or "") == str(getattr(right, "vnum", "") or "")
            and str(getattr(left, "short_description", "") or "") == str(getattr(right, "short_description", "") or "")
        )

    @staticmethod
    def _charge_adjusted_price(item, base_price: int) -> int:
        price = max(0, GenericUtil.to_int(base_price, 0))
        item_type_name = str(getattr(item, "item_type", "") or "").strip().upper()
        if item_type_name not in {"ITEM_STAFF", "ITEM_WAND"}:
            return price

        max_charges = GenericUtil.to_int(getattr(item, "value1", 0), 0)
        current_charges = GenericUtil.to_int(getattr(item, "value2", 0), 0)
        if max_charges <= 0:
            return price // 4
        return price * current_charges // max_charges

    @classmethod
    def from_json(cls, data):
        from util.GenericUtil import GenericUtil
        data = GenericUtil.camel_to_snake_case(data)
        return cls(**data)

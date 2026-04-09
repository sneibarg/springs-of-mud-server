from registries import Registry
from area.Shop import Shop
from server.LoggerFactory import LoggerFactory


class ShopRegistry(Registry[Shop]):
    lookup_attrs = ('id',)

    def __init__(self):
        super().__init__()

        self.__name__ = "ShopRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_shops(self) -> set[Shop]:
        return self._items

    def all_shops_by_area_id(self, area_id: str) -> list[Shop]:
        return [shop for shop in self._items if shop.area_id == area_id]

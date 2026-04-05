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

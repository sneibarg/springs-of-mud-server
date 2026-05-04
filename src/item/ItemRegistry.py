from registries import Registry
from item.Item import Item
from server.LoggerFactory import LoggerFactory


class ItemRegistry(Registry[Item]):
    lookup_attrs = ('id', 'vnum')

    def __init__(self):
        super().__init__()

        self.__name__ = "ItemRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_items(self) -> set[Item]:
        return self._items

    def all_items_by_area_id(self, area_id: str) -> list[Item]:
        return [item for item in self._items if item.area_id == area_id]


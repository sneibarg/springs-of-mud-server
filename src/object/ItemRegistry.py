from registries import Registry
from object.Item import Item
from server.LoggerFactory import LoggerFactory


class ItemRegistry(Registry[Item]):
    lookup_attrs = ('id', 'vnum')

    def __init__(self):
        super().__init__()

        self.__name__ = "ItemRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_items(self) -> list[Item]:
        return list(self.registry.values())


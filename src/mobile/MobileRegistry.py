from mobile.Mobile import Mobile
from registries import Registry
from server.LoggerFactory import LoggerFactory


class MobileRegistry(Registry[Mobile]):
    lookup_attrs = ('id', 'vnum')

    def __init__(self):
        super().__init__()

        self.__name__ = "MobileRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_mobiles(self) -> set[Mobile]:
        return self._items

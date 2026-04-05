from registries import Registry
from area.Special import Special
from server.LoggerFactory import LoggerFactory


class SpecialRegistry(Registry[Special]):
    lookup_attrs = ('id',)

    def __init__(self):
        super().__init__()

        self.__name__ = "SpecialRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_specials(self) -> set[Special]:
        return self._items
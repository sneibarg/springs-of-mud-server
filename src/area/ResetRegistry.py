from registries import Registry
from area.Reset import Reset
from server.LoggerFactory import LoggerFactory


class ResetRegistry(Registry[Reset]):
    lookup_attrs = ('id',)

    def __init__(self):
        super().__init__()

        self.__name__ = "ResetRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_resets(self) -> set[Reset]:
        return self._items
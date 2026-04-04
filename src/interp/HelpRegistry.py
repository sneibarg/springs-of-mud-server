from registries import Registry
from interp.HelpEntry import HelpEntry
from server.LoggerFactory import LoggerFactory


class HelpRegistry(Registry[HelpEntry]):
    lookup_attrs = ('id', 'keyword')

    def __init__(self):
        super().__init__()

        self.__name__ = "HelpRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_helps(self) -> set[HelpEntry]:
        return self._items

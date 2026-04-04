from registries import Registry
from interp.Command import Command
from server.LoggerFactory import LoggerFactory


class InterpRegistry(Registry[Command]):
    lookup_attrs = ('name', 'id')

    def __init__(self):
        super().__init__()

        self.__name__ = "InterpRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_commands(self) -> set[Command]:
        return self._items

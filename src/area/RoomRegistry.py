from registries import Registry
from area.Room import Room
from server.LoggerFactory import LoggerFactory


class RoomRegistry(Registry[Room]):
    lookup_attrs = ('id', 'vnum')

    def __init__(self):
        super().__init__()

        self.__name__ = "RoomRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_rooms(self) -> set[Room]:
        return self._items

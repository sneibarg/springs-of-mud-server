from registries import Registry
from skill.GroupType import GroupType
from server.LoggerFactory import LoggerFactory


class GroupRegistry(Registry[GroupType]):
    lookup_attrs = ('name', )

    def __init__(self):
        super().__init__()
        self.__name__ = "GroupRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_groups(self) -> set[GroupType]:
        return self._items

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

    def all_specials_by_area_id(self, area_id: str) -> list[Special]:
        return [special for special in self._items if special.area_id == area_id]

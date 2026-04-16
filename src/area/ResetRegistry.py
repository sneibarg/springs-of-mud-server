from registries import Registry
from area.Reset import Reset
from server.LoggerFactory import LoggerFactory


class ResetRegistry(Registry[Reset]):
    lookup_attrs = ('id',)

    def __init__(self):
        super().__init__()

        self.__name__ = "ResetRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self._ordered_resets: list[Reset] = []

    def all_resets(self) -> set[Reset]:
        return self._items

    def register(self, item: Reset):
        super().register(item)
        self._ordered_resets.append(item)
        return item

    def reset(self):
        super().reset()
        self._ordered_resets = []

    def all_resets_by_area_id(self, area_id: str) -> list[Reset]:
        return [reset for reset in self._ordered_resets if reset.area_id == area_id]

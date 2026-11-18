from registries import Registry
from area.Area import Area
from server.LoggerFactory import LoggerFactory


class AreaRegistry(Registry[Area]):
    lookup_attrs = ('id', 'name', 'vnum')

    def __init__(self):
        super().__init__()

        self.__name__ = "AreaRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_areas(self) -> set[Area]:
        return self._items

    def areas_in_load_order(self) -> list[Area]:
        """Read registration order from the ID index, including after a reload."""
        with self._lock:
            return list(self._registry['id'].values())




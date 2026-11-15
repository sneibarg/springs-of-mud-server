from registries import Registry
from area.Special import Special
from server.LoggerFactory import LoggerFactory


class SpecialRegistry(Registry[Special]):
    lookup_attrs = ('id',)

    def __init__(self):
        super().__init__()

        self.__name__ = "SpecialRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self._indexed_items = None
        self._by_name: dict[str, Special] = {}

    def on_item_registered(self, item: Special) -> None:
        self._indexed_items = None

    def on_item_unregistered(self, item: Special) -> None:
        self._indexed_items = None

    def by_name(self, name: str) -> Special | None:
        """Resolve a named delegate from the current set of definitions."""
        self.populate()
        with self._lock:
            if self._indexed_items is not self._items:
                named = {}
                for special in sorted(self._items, key=lambda entry: (
                        not entry.special_function, bool(entry.mob_vnum), entry.id)):
                    name_key = str(special.name or "").strip().lower()
                    if name_key:
                        named.setdefault(name_key, special)
                self._by_name = named
                self._indexed_items = self._items
            return self._by_name.get(str(name or "").strip().lower())

    def all_specials(self) -> set[Special]:
        return self._items

    def all_specials_by_area_id(self, area_id: str) -> list[Special]:
        return [special for special in self._items if special.area_id == area_id]

    def for_mobile(self, area_id: str, vnum: str) -> Special | None:
        return next((special for special in self._items
                     if special.area_id == str(area_id) and special.mob_vnum == str(vnum)), None)

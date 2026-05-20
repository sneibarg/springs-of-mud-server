from registries import Registry
from server.LoggerFactory import LoggerFactory
from skill.Spell import Spell


class SpellRegistry(Registry[Spell]):
    lookup_attrs = ('name', 'id')

    def __init__(self):
        super().__init__()

        self.__name__ = "SpellRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_spells(self) -> set[Spell]:
        return self._items

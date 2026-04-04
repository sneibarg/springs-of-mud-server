from registries import Registry
from player.Player import Player
from server.LoggerFactory import LoggerFactory


class PlayerRegistry(Registry[Player]):
    lookup_attrs = ('id', )

    def __init__(self):
        super().__init__()

        self.__name__ = "PlayerRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_players(self) -> set[Player]:
        return self._items

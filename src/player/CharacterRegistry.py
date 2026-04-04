from registries import Registry
from player.Character import Character
from server.LoggerFactory import LoggerFactory


class CharacterRegistry(Registry[Character]):
    lookup_attrs = ('id', )

    def __init__(self):
        super().__init__()

        self.__name__ = "CharacterRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.playing = {}

    def set_playing(self, character: Character):
        self.playing[character.id] = character

    def remove_playing(self, character: Character):
        del self.playing[character.id]

    def all_characters(self) -> set[Character]:
        return self._items

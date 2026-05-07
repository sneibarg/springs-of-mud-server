from __future__ import annotations

from typing import TYPE_CHECKING

from registries import Registry
from server.LoggerFactory import LoggerFactory

if TYPE_CHECKING:
    from player.Character import Character


class CharacterRegistry(Registry):
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

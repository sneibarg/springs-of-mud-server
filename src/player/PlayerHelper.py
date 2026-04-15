from injector import inject

from area import Room
from area.RoomHelper import RoomHelper
from area.RoomRegistry import RoomRegistry
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory


class PlayerHelper:
    @inject
    def __init__(self, character_macros: CharacterMacros, room_registry: RoomRegistry, room_helper: RoomHelper):
        self.__name__ = "PlayerHelper"
        self.character_macros = character_macros
        self.room_registry = room_registry
        self.room_helper = room_helper
        self.logger = LoggerFactory.get_logger(__name__)

    def get_players_in_room(self, character: Character) -> str:
        text = ""
        room = self.room_registry.get(id=character.room_id)
        for char_in_room in self.players_in_room(character, room):
            if char_in_room.cloaked:
                continue
            name = char_in_room.name
            text = text + f"{name} {char_in_room.title} is here.\r\n"
        return text

    def players_in_room(self, character: Character, room: Room):
        loiterers = []
        if room is None:
            return loiterers
        for char in room.characters.values():
            if char.id == character.id:
                continue
            if self.character_macros.can_see(character, char, self.room_helper):
                loiterers.append(char)
        return loiterers

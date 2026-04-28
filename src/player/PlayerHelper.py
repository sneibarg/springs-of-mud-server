from injector import inject

from area import Room
from area.RoomHelper import RoomHelper
from area.RoomRegistry import RoomRegistry
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from util.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory


class PlayerHelper:
    @inject
    def __init__(self, room_registry: RoomRegistry, room_helper: RoomHelper):
        self.__name__ = "PlayerHelper"
        self.room_registry = room_registry
        self.room_helper = room_helper
        self.logger = LoggerFactory.get_logger(__name__)

    def get_players_in_room(self, character: Character) -> str:
        text = ""
        room = self.room_registry.get(id=character.room_id)
        for char_in_room in self.players_in_room(character, room):
            if char_in_room.cloaked:
                continue
            text += PlayerUtil.format_visible_character_line(character, char_in_room)
        return text

    def players_in_room(self, character: Character, room: Room):
        loiterers = []
        if room is None:
            return loiterers
        for char in room.characters.values():
            if char.id == character.id:
                continue
            if CharacterMacros.can_see(character, char, self.room_helper):
                loiterers.append(char)
        return loiterers

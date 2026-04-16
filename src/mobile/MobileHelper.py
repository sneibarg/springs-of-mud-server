from typing import List
from injector import inject

from area.Room import Room
from area.RoomHelper import RoomHelper
from area.RoomRegistry import RoomRegistry
from mobile.Mobile import Mobile
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory


class MobileHelper:
    @inject
    def __init__(self, character_macros: CharacterMacros, room_registry: RoomRegistry, room_helper: RoomHelper):
        self.__name__ = "MobileHelper"
        self.character_macros = character_macros
        self.room_registry = room_registry
        self.room_helper = room_helper
        self.logger = LoggerFactory.get_logger(__name__)

    def get_mobiles_in_room(self, character: Character) -> str:
        text = ""
        room = self.room_registry.get(id=character.room_id)
        for char_in_room in self.mobiles_in_room(character, room):
            name = (char_in_room.long_description or "").strip()
            if name:
                text += name + "\r\n"
            else:
                text += f"{char_in_room.short_description or char_in_room.name} is here.\r\n"
        return text

    def mobiles_in_room(self, character: Character, room: Room) -> List[Mobile]:
        loiterers = []
        if room is None:
            return loiterers
        for mobile in room.mobiles.values():
            if self.character_macros.can_see(character, mobile, self.room_helper):
                loiterers.append(mobile)
        return loiterers

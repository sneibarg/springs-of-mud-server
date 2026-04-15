from area import Room
from area.RoomHelper import RoomHelper
from interp.InterpUtil import InterpUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from server.session.SessionHandler import SessionHandler
from typing import List


class PlayerUtil:
    pass

    @staticmethod
    def visible(character: Character, session_handler: SessionHandler) -> List[Character]:
        visible = []
        for session in session_handler.get_playing_sessions():
            char: Character = session.character
            if char.id == character.id:
                continue
            if char.cloaked and character.role == "player":
                continue
            visible.append(char)
        return visible

    @staticmethod
    def is_target_playing(target: str, session_handler: SessionHandler) -> bool:
        for session in session_handler.get_playing_sessions():
            char: Character = session.character
            if char.name == target:
                return True
        return False

    @staticmethod
    def get_target(character: Character, victim: str, room: Room, character_macros: CharacterMacros, room_helper: RoomHelper):
        if room is None:
            return None

        target = PlayerUtil._get_character_target(character, victim, room, character_macros, room_helper)
        if target is None:
            target = PlayerUtil._get_mobile_target(character, victim, room, character_macros, room_helper)

        return target

    @staticmethod
    def _get_character_target(character: Character, victim: str, room: Room, character_macros: CharacterMacros, room_helper: RoomHelper):
        for char in room.characters.values():
            if not character_macros.can_see(character, char, room_helper) or victim != char.name:
                continue

            if char.room_id is room.id:
                char_name = (char.name or "").lower()
                if char_name == victim or char_name.startswith(victim):
                    return char
        return None

    @staticmethod
    def _get_mobile_target(character, victim: str, room: Room, character_macros: CharacterMacros, room_helper: RoomHelper):
        mob = InterpUtil.find_nth_by_keyword(room.mobiles, victim)  # support for 1.mob_name; 2.mob_name, etc
        if mob is not None and character_macros.can_see(character, mob, room_helper):
            return mob
        else:
            return None

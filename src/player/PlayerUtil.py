from player.Character import Character
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

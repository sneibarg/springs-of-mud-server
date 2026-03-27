from typing import Any
from area import Room
from game import GameData
from player import Character
from registry import RegistryService
from server.LoggerFactory import LoggerFactory


class CharacterMacros:
    def __init__(self, game_data: GameData, registry_service: RegistryService):
        self.__name__ = "CharacterMacros"
        self.game_data = game_data
        self.registry_service = registry_service
        self.logger = LoggerFactory.get_logger(__name__)

    def is_npc(self, char: Any) -> bool:
        pass

    def is_immortal(self, char: Any) -> bool:
        pass

    def is_hero(self, char: Any) -> bool:
        pass

    def is_trusted(self, char: Any) -> bool :
        pass

    def is_affected(self, char: Any) -> bool:
        pass

    def get_age(self, char: Character) -> int:
        pass

    def is_good(self, char: Any) -> bool:
        pass

    def is_evil(self, char: Any) -> bool:
        pass

    def is_neutral(self, char: Any) -> bool:
        pass

    def get_ac(self, char: Any, ac: int) -> int:
        pass

    def get_hitroll(self, char: Any) -> int:
        pass

    def get_damroll(self, char: Any) -> int:
        pass

    def is_outside(self, char: Any) -> bool:
        room: Room = self.registry_service.room_registry[char.room_id]
        self.logger.debug(f"is_outside: {room.room_flags}={self.game_data.flags['room']['INDOORS']}")
        return (room.room_flags & self.game_data.flags['room']["INDOORS"]) == 0

    def wait_state(self, char: Character, npulse: int) -> int:
        pass

    def daze_state(self, char: Character, npulse: int) -> int:
        pass

    def act(self, act_format: str, char: Any, arg1: str, arg2: str, act_type: int):
        pass

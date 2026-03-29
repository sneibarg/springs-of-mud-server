from datetime import datetime
from typing import Any
from injector import inject
from area import Room
from game import GameData
from mobile.Mobile import Mobile
from player import Character
from player.CharacterConstants import CharacterConstants
from registry import RegistryService
from server.LoggerFactory import LoggerFactory


class CharacterMacros:
    @inject
    def __init__(self, game_data: GameData, registry_service: RegistryService, character_constants: CharacterConstants):
        self.__name__ = "CharacterMacros"
        self.game_data = game_data
        self.registry_service = registry_service
        self.character_constants = character_constants
        self.attribute_bonuses = self.game_data.attribute_bonuses
        self.logger = LoggerFactory.get_logger(__name__)

    def is_npc(self, char: Any) -> bool:
        pass

    def is_immortal(self, char: Character) -> bool:
        pass

    def is_hero(self, char: Character) -> bool:
        pass

    def is_trusted(self, char: Character) -> bool :
        pass

    def is_affected(self, char: Character | Mobile) -> bool:
        pass

    @staticmethod
    def get_age(char: Character) -> int:
        return int(17 + (char.played + datetime.now().timestamp() - char.logon) / 72000)

    @staticmethod
    def is_good(char: Character | Mobile) -> bool:
        return char.alignment >= 350

    @staticmethod
    def is_evil(char: Character | Mobile) -> bool:
        return char.alignment <= -350

    @staticmethod
    def is_neutral(char: Character | Mobile) -> bool:
        return not CharacterMacros.is_good(char) and not CharacterMacros.is_evil(char)

    # requires normalization
    def get_ac(self, char: Character | Mobile, ac: int) -> int:
        pass

    # requires normalization
    def get_hitroll(self, char: Character | Mobile) -> int:
        return self.character_constants.get_attribute_bonus(attr_name="strength", attr_level=str(char.level)).get('tohit')

    # requires normalization
    def get_damroll(self, char: Character | Mobile) -> int:
        return self.character_constants.get_attribute_bonus(attr_name="strength", attr_level=str(char.level)).get('todam')

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

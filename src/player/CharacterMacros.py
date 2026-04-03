from datetime import datetime
from typing import Any
from area import Room
from game.GameMacros import GameMacros
from mobile.Mobile import Mobile
from player.Character import Character
from player.CharacterConstants import CharacterConstants
from server.LoggerFactory import LoggerFactory
from game.RegistryService import RegistryService


class CharacterMacros(GameMacros):
    def __init__(self, registry_service: RegistryService,
                 room_flags: dict,
                 attribute_bonuses: dict,
                 character_constants: CharacterConstants):
        self.__name__ = "CharacterMacros"
        self.registry_service = registry_service
        self.room_flags = room_flags
        self.character_constants = character_constants
        self.attribute_bonuses = attribute_bonuses
        self.logger = LoggerFactory.get_logger(__name__)

    def _get_trust(self, char: Character) -> int:
        if char.trust > 0:
            return char.trust
        if self.is_npc(char) and char.level >= self.character_constants.immortal_levels.get("LEVEL_HERO"):
            return self.character_constants.immortal_levels.get("LEVEL_HERO") - 1;
        else:
            return char.level

    def get_attribute_bonus(self, attr_name: str, attr_level: str):
        return self.attribute_bonuses.get(attr_name).get(attr_level)

    def is_immortal_sufficient(self, level: int, immortal_name: str) -> bool:
        return level >= self.character_constants.immortal_levels.get(immortal_name)

    def is_npc(self, char: Any) -> bool:
        return self.is_set(char.act, self.character_constants.act_bits.ACT_IS_NPC)

    def is_immortal(self, char: Character) -> bool:
        return self._get_trust(char) >= self.character_constants.immortal_levels.get("LEVEL_IMMORTAL")

    def is_hero(self, char: Character) -> bool:
        return self._get_trust(char) >= self.character_constants.immortal_levels.get("LEVEL_HERO")

    def is_trusted(self, char: Character) -> bool:
        return self._get_trust(char) >= char.level

    def is_affected(self, char: Character | Mobile, effect) -> bool:
        from server.ServerUtil import ServerUtil
        return self.is_set(ServerUtil.convert_flags(char.affected_by), effect)

    def is_awake(self, char: Any) -> bool:
        return char.position > self.character_constants.positions.POS_SLEEPING.name

    @staticmethod
    def get_age(char: Character) -> int:
        return int(17 + (char.played + datetime.now().timestamp() - char.logon) / 72000)

    @staticmethod
    def is_good(char: Character | Mobile) -> bool:
        return char.alignment >= 350

    @staticmethod
    def is_evil(char: Character | Mobile) -> bool:
        return char.alignment <= -350

    def is_neutral(self, char: Character | Mobile) -> bool:
        return not self.is_good(char) and not self.is_evil(char)

    # requires normalization
    def get_ac(self, char: Character | Mobile, ac: int) -> int:
        pass

    # requires normalization
    def get_hitroll(self, char: Character | Mobile) -> int:
        return self.get_attribute_bonus(attr_name="strength", attr_level=str(char.level)).get('tohit')

    # requires normalization
    def get_damroll(self, char: Character | Mobile) -> int:
        return self.get_attribute_bonus(attr_name="strength", attr_level=str(char.level)).get('todam')

    def is_outside(self, char: Any) -> bool:
        room: Room = self.registry_service.room_registry[char.room_id]
        self.logger.debug(f"is_outside: {room.room_flags}={self.room_flags['room']['INDOORS']}")
        return (room.room_flags & self.room_flags['room']["INDOORS"]) == 0

    @staticmethod
    def get_carry_weight(char: Any) -> int:
        return int(char.max_weight + ((char.silver / 10) + (char.gold * 2 / 5)))

    @staticmethod
    def wait_state(char: Character, npulse: int) -> int:
        return max(char.pulse_wait, npulse)

    @staticmethod
    def daze_state(char: Character, npulse: int) -> int:
        return max(char.pulse_daze, npulse)

    def act(self, act_format: str, char: Any, arg1: str, arg2: str, act_type: int):
        pass

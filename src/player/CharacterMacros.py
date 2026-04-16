from datetime import datetime
from enum import IntEnum
from typing import Any, TYPE_CHECKING

from area.Room import Room
from game.GameMacros import GameMacros
from game.RandomNumberGenerator import RandomNumberGenerator
from mobile.Mobile import Mobile
from player.Character import Character
from server.LoggerFactory import LoggerFactory


if TYPE_CHECKING:
    from area.RoomHelper import RoomHelper

rng = RandomNumberGenerator()


class CharacterMacros(GameMacros):
    def __init__(self,
                 registry_service,
                 character_constants,
                 enums: dict[str, IntEnum],
                 attribute_bonuses: dict[str, dict[str, dict[str, int]]]):
        self.__name__ = "CharacterMacros"
        self.registry_service = registry_service
        self.enums = enums
        self.character_constants = character_constants
        self.weather_handler = None
        self.RoomFlagsEnum = self.enums.get("roomFlags")
        self.PlayerActBits = self.enums.get("playerActBits")
        self.AffectedBits = self.enums.get('affectedBy')
        self.TimeAndWeatherEnum = enums.get('timeAndWeather')
        self.PositionsEnum = enums.get('positions')
        self.GameParametersEnum = enums.get('gameParameters')
        self.attribute_bonuses = attribute_bonuses
        self.logger = LoggerFactory.get_logger(__name__)

    def lazy_load(self, weather_handler):
        self.weather_handler = weather_handler

    def get_trust(self, char: Any) -> int:
        if type(char) is Character and char.trust > 0:
            return char.trust
        if self.is_npc(char) and char.level >= self.character_constants.immortal_levels.get("LEVEL_HERO"):
            return self.character_constants.immortal_levels.get("LEVEL_HERO") - 1
        else:
            return char.level

    def get_attribute_bonus(self, attr_name: str, attr_level: str):
        return self.attribute_bonuses.get(attr_name).get(attr_level)

    def is_immortal_sufficient(self, level: int, immortal_name: str) -> bool:
        return level >= self.character_constants.immortal_levels.get(immortal_name)

    # let's deprecate ACT_IS_NPC
    @staticmethod
    def is_npc(char: Any) -> bool:
        return True if type(char) is Mobile else False

    def is_immortal(self, char: Character) -> bool:
        return self.get_trust(char) >= self.GameParametersEnum.LEVEL_IMMORTAL.value

    def is_hero(self, char: Character) -> bool:
        return self.get_trust(char) >= self.GameParametersEnum.LEVEL_HERO.value

    def is_trusted(self, char: Character) -> bool:
        return self.get_trust(char) >= char.level

    def is_affected(self, char: Any, effect) -> bool:
        if type(char) is Character:
            return self.is_set(self.convert_flags(char.character_flags.affected_by), effect)
        else:
            return self.is_set(self.convert_flags(char.mobile_flags.affected_by), effect)

    def is_blind(self, character: Any) -> bool:
        return self.is_set(int(self.convert_flags(character.character_flags.act)), self.AffectedBits.AFF_BLIND.value)

    def is_awake(self, char: Any) -> bool:
        return char.character_attributes.position > self.character_constants.positions.POS_SLEEPING.value

    @staticmethod
    def get_age(char: Character) -> int:
        return int(17 + (char.played + datetime.now().timestamp() - char.logon) / 72000)

    @staticmethod
    def is_good(char: Any) -> bool:
        if type(char) is Character:
            return char.character_attributes.alignment >= 350
        else:
            return char.perm_stat.alignment >= 350

    @staticmethod
    def is_evil(char: Any) -> bool:
        if type(char) is Character:
            return char.character_attributes.alignment <= -350
        else:
            return char.perm_stat.alignment <= -350

    def is_neutral(self, char: Any) -> bool:
        return not self.is_good(char) and not self.is_evil(char)

    # requires normalization
    def get_ac(self, char: Any, ac: int) -> int:
        pass

    # requires normalization
    def get_hitroll(self, char: Any) -> int:
        return self.get_attribute_bonus(attr_name="strength", attr_level=str(char.level)).get('tohit')

    # requires normalization
    def get_damroll(self, char: Any) -> int:
        return self.get_attribute_bonus(attr_name="strength", attr_level=str(char.level)).get('todam')

    def is_outside(self, char: Any) -> bool:
        room: Room = self.registry_service.room_registry.get(id=char.room_id)
        self.logger.debug(f"is_outside: {room.room_flags}={self.RoomFlagsEnum.ROOM_INDOORS}")
        return (room.room_flags & self.RoomFlagsEnum.ROOM_INDOORS) == 0

    @staticmethod
    def get_carry_weight(char: Any) -> int:
        return int(char.character_attributes.max_weight + ((char.silver / 10) + (char.gold * 2 / 5)))

    @staticmethod
    def wait_state(char: Character, npulse: int) -> int:
        return max(char.temporal_mechanics.pulse_wait, npulse)

    @staticmethod
    def daze_state(char: Character, npulse: int) -> int:
        return max(char.temporal_mechanics.pulse_daze, npulse)

    def act(self, act_format: str, char: Any, arg1: str, arg2: str, act_type: int):
        pass

    def has_holy_light(self, character) -> bool:
        return self.is_set(int(self.convert_flags(character.character_flags.act)), self.PlayerActBits.PLR_HOLYLIGHT.value)

    def can_see(self, character: Any, victim: Any, room_helper: RoomHelper) -> bool:
        if character == victim:
            return True

        if self.get_trust(character) < victim.invis_level:
            return False

        if self.get_trust(character) < victim.incog_level and character.room_id != victim.room_id:
            return False

        if ((not self.is_npc(character) and self.has_holy_light(character))
                or (self.is_npc(character) and self.is_immortal(character))):
            return True

        if self.is_affected(character, self.AffectedBits.AFF_BLIND.value):
            return False

        if room_helper.is_room_dark(character.room_id) and not self.is_affected(character, self.AffectedBits.AFF_INFRARED.value):
            return False

        if self.is_affected(victim, self.AffectedBits.AFF_INVISIBLE.value) and not self.is_affected(character, self.AffectedBits.AFF_DETECT_INVIS.value):
            return False

        # to-do: implement sneak chance
        #     int chance;
        #     chance = get_skill(victim, gsn_sneak);
        #     chance += get_curr_stat(victim, STAT_DEX) * 3 / 2;
        #     chance -= get_curr_stat(ch, STAT_INT) * 2;
        #     chance -= ch->level - victim->level * 3 / 2;
        if self.is_affected(victim, self.AffectedBits.AFF_SNEAK.value) \
                and not self.is_affected(character, self.AffectedBits.AFF_DETECT_HIDDEN.value)\
                and victim.fighting is None:
            pass

        if self.weather_handler.weather_info.sunlight == self.TimeAndWeatherEnum.SUN_SET.value\
                or self.weather_handler.weather_info.sunlight == self.TimeAndWeatherEnum.SUN_DARK.value:
            return True
        chance = 0
        if rng.number_percent() < chance:
            return False
        return True

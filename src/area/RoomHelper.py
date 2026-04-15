from injector import inject
from area.RoomRegistry import RoomRegistry
from game.RandomNumberGenerator import RandomNumberGenerator
from game.WeatherHandler import WeatherHandler
from player.Character import Character
from area.Room import Room
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from server.messaging.MessageBus import MessageBus
from server.protocol.Message import Message

rng = RandomNumberGenerator()


class RoomHelper:
    @inject
    def __init__(self, message_bus: MessageBus, character_macros: CharacterMacros, room_registry: RoomRegistry):
        self.__name__ = "RoomHelper"
        self.message_bus = message_bus
        self.character_macros = character_macros
        self.room_registry = room_registry
        self.PlayerActBits = character_macros.enums.get('playerActBits')
        self.AffectedBits = character_macros.enums.get('affectedBy')
        self.RoomFlags = character_macros.enums.get('roomFlags')
        self.SectorTypes = character_macros.enums.get('sectorTypes')
        self.TimeAndWeatherEnum = character_macros.enums.get('timeAndWeather')
        self.logger = LoggerFactory.get_logger(__name__)
        self.weather_handler: WeatherHandler = None

    def set_weather_service(self, weather_handler):
        self.weather_handler = weather_handler

    def can_see(self, character: Character, victim: Character) -> bool:
        if character == victim:
            return True

        if self.character_macros.get_trust(character) < victim.invis_level:
            return False

        if self.character_macros.get_trust(character) < victim.incog_level and character.room_id != victim.room_id:
            return False

        if (not self.character_macros.is_npc(character) and self.character_macros.is_set(int(character.character_flags.act), self.PlayerActBits.PLR_HOLYLIGHT.value))\
                or (self.character_macros.is_npc(character) and self.character_macros.is_immortal(character)):
            return True

        if self.character_macros.is_affected(character, self.AffectedBits.AFF_BLIND.value):
            return False

        if self.is_room_dark(character.room_id) and not self.character_macros.is_affected(character, self.AffectedBits.AFF_INFRARED.value):
            return False

        if self.character_macros.is_affected(victim, self.AffectedBits.AFF_INVISIBLE.value) and not self.character_macros.is_affected(character, self.AffectedBits.AFF_DETECT_INVIS.value):
            return False

        # to-do: implement sneak chance
        #     int chance;
        #     chance = get_skill(victim, gsn_sneak);
        #     chance += get_curr_stat(victim, STAT_DEX) * 3 / 2;
        #     chance -= get_curr_stat(ch, STAT_INT) * 2;
        #     chance -= ch->level - victim->level * 3 / 2;
        if self.character_macros.is_affected(victim, self.AffectedBits.AFF_SNEAK.value) \
                and not self.character_macros.is_affected(character, self.AffectedBits.AFF_DETECT_HIDDEN.value)\
                and victim.fighting is None:
            pass

        if self.weather_handler.weather_info.sunlight == self.TimeAndWeatherEnum.SUN_SET.value\
                or self.weather_handler.weather_info.sunlight == self.TimeAndWeatherEnum.SUN_DARK.value:
            return True
        chance = 0
        if rng.number_percent() < chance:
            return False
        return True

    def check_blind(self, character: Character) -> bool:
        if not self.character_macros.is_npc(character) and self.character_macros.is_set(int(character.character_flags.act), self.PlayerActBits.PLR_HOLYLIGHT.value):
            return True
        if self.character_macros.is_affected(character, self.AffectedBits.AFF_BLIND.value):
            self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You can't see a thing!\n\r"))
            return False
        return True

    def is_room_dark(self, room_id: str) -> bool:
        room = self.room_registry.get_or_none(id=room_id)
        if room is None:
            return True

        if room.light > 0:
            return False

        if self.character_macros.is_set(room.room_flags, self.RoomFlags.ROOM_DARK.value):
            return True

        if room.sector_type == self.SectorTypes.SECT_INSIDE.value or room.sector_type == self.SectorTypes.SECT_CITY.value:
            return False

        return False

    def get_in_room(self, character: Character, session_handler):
        loiterers = []
        for session in session_handler.get_playing_sessions():
            char: Character = session.character
            if char.id == character.id:
                continue
            if char.room_id == character.room_id and self.can_see(character, char):
                loiterers.append(char.id)
        return loiterers

    def get_room(self, room_id) -> Room | None:
        if room_id is None:
            self.logger.debug("get_room: room_id is None")
            return None
        if room_id not in self.room_registry.all_rooms():
            self.logger.debug("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.room_registry.get(id=room_id)

    def format_room_description(self, room_name: str, description: str) -> Message:
        return self.message_bus.text_to_message(f"[{room_name}]\r\n{description}\r\n")

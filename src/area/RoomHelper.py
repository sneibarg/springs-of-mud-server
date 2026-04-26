from typing import Any

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
    def __init__(self, message_bus: MessageBus, room_registry: RoomRegistry):
        self.__name__ = "RoomHelper"
        self.message_bus = message_bus
        self.room_registry = room_registry
        self.PlayerActBits = None
        self.AffectedBits = None
        self.RoomFlags = None
        self.SectorTypes = None
        self.TimeAndWeatherEnum = None
        self.logger = LoggerFactory.get_logger(__name__)
        self.weather_handler: WeatherHandler = None

    def lazy_load(self, weather_handler):
        self.weather_handler = weather_handler
        self.PlayerActBits = CharacterMacros.get_enum('playerActBits')
        self.AffectedBits = CharacterMacros.get_enum('affectedBy')
        self.RoomFlags = CharacterMacros.get_enum('roomFlags')
        self.SectorTypes = CharacterMacros.get_enum('sectorTypes')
        self.TimeAndWeatherEnum = CharacterMacros.get_enum('timeAndWeather')

    @staticmethod
    def check_blind(character: Character) -> bool:
        if not CharacterMacros.is_npc(character) and CharacterMacros.has_holy_light(character):
            return True
        if CharacterMacros.is_blind(character):
            return False
        return True

    def is_room_dark(self, room_id: str) -> bool:
        room = self.room_registry.get_or_none(id=room_id)
        if room is None:
            return True

        if room.light > 0:
            return False

        if CharacterMacros.is_set(room.room_flags, self.RoomFlags.ROOM_DARK.value):
            return True

        if room.sector_type == self.SectorTypes.SECT_INSIDE.value or room.sector_type == self.SectorTypes.SECT_CITY.value:
            return False

        return False

    def get_room(self, room_id) -> Room | None:
        if room_id is None:
            self.logger.debug("get_room: room_id is None")
            return None
        if room_id not in self.room_registry.all_rooms():
            self.logger.debug("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.room_registry.get(id=room_id)

    def format_room_description(self, room_name: str, description: str) -> Message:
        body = str(description or "").strip()
        return self.message_bus.text_to_message(f"{room_name}\r\n{body}")

    @staticmethod
    def can_see_room_vnum(char: Any) -> bool:
        if CharacterMacros.is_immortal(char) and (CharacterMacros.is_npc(char) or CharacterMacros.has_holy_light(char)):
            return True
        return False

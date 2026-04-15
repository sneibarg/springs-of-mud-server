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

    def check_blind(self, character: Character) -> bool:
        if not self.character_macros.is_npc(character) and self.character_macros.has_holy_light(character):
            return True
        if self.character_macros.is_blind(character):
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

    def can_see_room_vnum(self, char: Any) -> bool:
        if self.character_macros.is_immortal(char) and (self.character_macros.is_npc(char) or self.character_macros.has_holy_light(char)):
            return True
        return False

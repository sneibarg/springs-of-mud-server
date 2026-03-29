from dataclasses import dataclass
from injector import inject

from game.GameData import GameData
from player.CharacterMacros import CharacterMacros
from registry.RegistryService import RegistryService
from numbers.RandomNumberGenerator import RandomNumberGenerator
from server.LoggerFactory import LoggerFactory
from server.messaging.MessageBus import MessageBus
from server.protocol.Message import Message, MessageType

rng = RandomNumberGenerator()


@dataclass(slots=True)
class WeatherInfo:
    mmhg: int
    change: int
    sky: int
    sunlight: int


@dataclass(slots=True)
class TimeInfo:
    hour: int
    day: int
    month: int
    year: int


class WeatherService:
    @inject
    def __init__(self, message_bus: MessageBus, registry_service: RegistryService, game_data: GameData, character_macros: CharacterMacros):
        self.__name__ = "WeatherService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.character_macros = character_macros
        self.game_data = game_data
        self.time_and_weather_enum = self._load_enums()
        self.weather_info = WeatherInfo(mmhg=1000, change=0, sky=self.time_and_weather_enum.SKY_CLOUDLESS, sunlight=self.time_and_weather_enum.SUN_LIGHT)
        self.time_info = TimeInfo(hour=0, day=1, month=1, year=1)
        self.pulse_count = 0
        self.pulse_tick = self.game_data.constants.pulses.get('tick', 60 * game_data.constants.pulses.get('perSecond', 4))
        self.logger.info(f"WeatherService initialized. Pulse tick: {self.pulse_tick}")

    def _load_enums(self):
        from server.ServerUtil import ServerUtil
        return ServerUtil.build_int_enum('time_and_weather', self.game_data.enums.get('timeAndWeather'))

    # every 60 seconds is one game hour.
    async def update(self):
        """Update weather and time."""
        self.pulse_count += 1
        self.logger.debug(f"WeatherService pulse count: {self.pulse_count}")
        if self.pulse_count >= self.pulse_tick:
            self.pulse_count = 0
            self.logger.info("TimeInfo: " + str(self.time_info) + " WeatherInfo: " + str(self.weather_info))
            await self.time_update()
            await self.sky_update()

    async def time_update(self):
        time_msg = self._time_change()
        if time_msg:
            self.logger.info(f"Time update: {time_msg}")
            message = Message(type=MessageType.GAME, data={'text': time_msg})
            await self.message_bus.broadcast(message, self._indoors())

    async def sky_update(self):
        self._update_barometric_pressure()

        sky_msg = self._sky_change()
        if sky_msg:
            self.logger.info(f"Sky update: {sky_msg}")
            message = Message(type=MessageType.GAME, data={'text': sky_msg})
            await self.message_bus.broadcast(message, self._indoors())

    def _indoors(self) -> list:
        indoors = []
        for character in self.registry_service.character_registry.values():
            if not self._is_player_outdoors(character.id):
                indoors.append(character.id)
        return indoors

    def _is_player_outdoors(self, character_id: str) -> bool:
        character = self.registry_service.character_registry.get(character_id)
        self.logger.debug(f"Checking if player {character_id} is outdoors: {character}")
        if character:
            return self.character_macros.is_outside(char=character)
        return False

    def _time_change(self):
        time_message: str = ""
        self.time_info.hour += 1
        if self.time_info.hour == 5:
            self.weather_info.sunlight = self.time_and_weather_enum.SUN_LIGHT
            time_message = "The day has begun\n\r"
        elif self.time_info.hour == 6:
            self.weather_info.sunlight = self.time_and_weather_enum.SUN_RISE
            time_message = "The sun rises in the east.\n\r"
        elif self.time_info.hour == 19:
            self.weather_info.sunlight = self.time_and_weather_enum.SUN_SET
            time_message = "The sun slowly disappears in the west.\n\r"
        elif self.time_info.hour == 20:
            self.weather_info.sunlight = self.time_and_weather_enum.SUN_DARK
            time_message = "The night has begun\n\r"
        elif self.time_info.hour == 24:
            self.time_info.day += 1
            self.time_info.hour = 0

        if self.time_info.day >= 35:
            self.time_info.day = 0
            self.time_info.month += 1

        if self.time_info.month >= 17:
            self.time_info.month = 0
            self.time_info.year += 1

        return time_message

    def _update_barometric_pressure(self):
        if 9 <= self.time_info.month <= 16:
            diff = -2 if self.weather_info.mmhg > 985 else 2
        else:
            diff = -2 if self.weather_info.mmhg > 1015 else 2

        self.weather_info.change += diff * rng.dice(1, 4) + rng.dice(2, 6) - rng.dice(2, 6)
        self.weather_info.change = max(self.weather_info.change, -12)
        self.weather_info.change = min(self.weather_info.change, 12)

        self.weather_info.mmhg += self.weather_info.change
        self.weather_info.mmhg = max(self.weather_info.mmhg, 960)
        self.weather_info.mmhg = min(self.weather_info.mmhg, 1040)

    def _sky_change(self) -> str:
        def chance():
            return rng.number_bits(2) == 0

        sky_update: str = ""
        if self.weather_info.sky == self.time_and_weather_enum.SKY_CLOUDLESS:
            if self.weather_info.mmhg < 990 or (self.weather_info.mmhg < 1010 and chance()):
                sky_update += "The sky is getting cloudy.\n\r"
                self.weather_info.sky = self.time_and_weather_enum.SKY_CLOUDY
        elif self.weather_info.sky == self.time_and_weather_enum.SKY_CLOUDY:
            if self.weather_info.mmhg < 970 or (self.weather_info.mmhg < 990 and chance()):
                sky_update += "It starts to rain.\n\r"
                self.weather_info.sky = self.time_and_weather_enum.SKY_RAINING
            elif self.weather_info.sky > 1030 and chance():
                sky_update += "The clouds disappear.\n\r"
                self.weather_info.sky = self.time_and_weather_enum.SKY_CLOUDLESS
        elif self.weather_info.sky == self.time_and_weather_enum.SKY_RAINING:
            if self.weather_info.sky < 970 and chance():
                sky_update += "Lightning flashes in the sky.\n\r"
                self.weather_info.sky = self.time_and_weather_enum.SKY_LIGHTNING
            elif self.weather_info.sky > 1030 or (self.weather_info.mmhg > 1010 and chance()):
                sky_update += "The rain stopped.\n\r"
                self.weather_info.sky = self.time_and_weather_enum.SKY_CLOUDY
        elif self.weather_info.sky == self.time_and_weather_enum.SKY_LIGHTNING:
            if self.weather_info.mmhg > 1010 or (self.weather_info.mmhg > 990 and chance()):
                sky_update += "The lightning has stopped.\n\r"
                self.weather_info.sky = self.time_and_weather_enum.SKY_RAINING
        else:
            sky_update = f"Weather_update: bad sky {self.weather_info.sky}."
            self.weather_info.sky = self.time_and_weather_enum.SKY_CLOUDLESS
        return sky_update

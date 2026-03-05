from dataclasses import dataclass
from injector import inject

from area import RoomService
from player import PlayerService
from numbers import RandomNumberGenerator
from server.messaging import MessageBus
from server.protocol import Message, MessageType

rng = RandomNumberGenerator()

SUN_DARK: int = 0
SUN_RISE: int = 1
SUN_LIGHT: int = 2
SUN_SET: int = 3

SKY_CLOUDLESS: int = 0
SKY_CLOUDY: int = 1
SKY_RAINING: int = 2
SKY_LIGHTNING: int = 3


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
    def __init__(self, message_bus: MessageBus, player_service: PlayerService, room_service: RoomService):
        self.message_bus = message_bus
        self.player_service = player_service
        self.room_service = room_service
        self.weather_info = WeatherInfo(mmhg=1000, change=0, sky=SKY_CLOUDLESS, sunlight=SUN_LIGHT)
        self.time_info = TimeInfo(hour=0, day=1, month=1, year=1)

    async def time_update(self):
        """Send time updates to all outdoor players."""
        time_msg = self._time_change()
        if time_msg:
            message = Message(type=MessageType.SYSTEM, data={'text': time_msg})
            await self.message_bus.send_to_outdoor_players(message, self._is_player_outdoors)

    async def sky_update(self):
        """Send weather updates to all outdoor players"""
        sky_msg = self._sky_change()
        if sky_msg:
            message = Message(type=MessageType.SYSTEM, data={'text': sky_msg})
            await self.message_bus.send_to_outdoor_players(message, self._is_player_outdoors)

    def _is_player_outdoors(self, player_id: str) -> bool:
        """Check if a player is currently outdoors."""
        character = self.player_service.character_registry.get(player_id)
        if character:
            room = self.room_service.get_room(character.room_id)
            return self.room_service.is_outside(room)
        return False

    def _time_change(self):
        time_message: str = ""
        self.time_info.hour += 1
        if self.time_info.hour == 5:
            self.weather_info.sunlight = SUN_LIGHT
            time_message = "The day has begun\n\r"
        elif self.time_info.hour == 6:
            self.weather_info.sunlight = SUN_RISE
            time_message = "The sun rises in the east.\n\r"
        elif self.time_info.hour == 19:
            self.weather_info.sunlight = SUN_SET
            time_message = "The sun slowly disappears in the west.\n\r"
        elif self.time_info.hour == 20:
            self.weather_info.sunlight = SUN_DARK
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

    def _weather_change(self) -> str:
        weather_update: str = ""
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

        return weather_update

    def _sky_change(self) -> str:
        def chance():
            return rng.number_bits(2) == 0

        sky_update: str = ""
        if self.weather_info.sky == SKY_CLOUDLESS:
            if self.weather_info.mmhg < 990 or (self.weather_info.mmhg < 1010 and chance()):
                sky_update += "The sky is getting cloudy.\n\r"
                self.weather_info.sky = SKY_CLOUDY
        elif self.weather_info.sky == SKY_CLOUDY:
            if self.weather_info.mmhg < 970 or (self.weather_info.mmhg < 990 and chance()):
                sky_update += "It starts to rain.\n\r"
                self.weather_info.sky = SKY_RAINING
            elif self.weather_info.sky > 1030 and chance():
                sky_update += "The clouds disappear.\n\r"
                self.weather_info.sky = SKY_CLOUDLESS
        elif self.weather_info.sky == SKY_RAINING:
            if self.weather_info.sky < 970 and chance():
                sky_update += "Lightning flashes in the sky.\n\r"
                self.weather_info.sky = SKY_LIGHTNING
            elif self.weather_info.sky > 1030 or (self.weather_info.mmhg > 1010 and chance()):
                sky_update += "The rain stopped.\n\r"
                self.weather_info.sky = SKY_CLOUDY
        elif self.weather_info.sky == SKY_LIGHTNING:
            if self.weather_info.mmhg > 1010 or (self.weather_info.mmhg > 990 and chance()):
                sky_update += "The lightning has stopped.\n\r"
                self.weather_info.sky = SKY_RAINING
        else:
            sky_update = f"Weather_update: bad sky {self.weather_info.sky}."
            self.weather_info.sky = SKY_CLOUDLESS
        return sky_update

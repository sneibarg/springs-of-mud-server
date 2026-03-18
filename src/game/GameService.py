import requests

from typing import TYPE_CHECKING
from injector import inject

from game import GameData
from mobile import MobileService
from server.LoggerFactory import LoggerFactory
from server.ServerUtil import ServerUtil
from server.TimeVal import gettimeofday, TimeVal, stall_until_last_time
from server.ServiceConfig import ServiceConfig

if TYPE_CHECKING:
    from update.WeatherService import WeatherService


class GameService:
    @inject
    def __init__(self, config: ServiceConfig):
        self.__name__ = "GameService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.weather_service = None
        self.mobile_service = None
        self.game_data_endpoint = config.game_data_endpoint
        self.game_data = self._load_game_data()
        self.enums = dict()
        self._load_enums()
        self.last_time: TimeVal = gettimeofday()

    def set_weather_service(self, weather_service: WeatherService):
        self.weather_service = weather_service

    def start_mobile_service(self, mobile_service: MobileService):
        self.mobile_service = mobile_service
        self.mobile_service.start()

    async def start(self):
        await self.game_loop()

    async def game_loop(self):
        while True:
            await self._game_loop_iteration()

    async def _game_loop_iteration(self):
        self.last_time = gettimeofday()
        current_time = self.last_time.tv_sec
        self.logger.debug(f"Current time: {current_time}; Pulses per second: {self.game_data.constants.pulses['perSecond']}")
        await self.weather_service.update()
        stall_until_last_time(self.last_time, self.game_data.constants.pulses['perSecond'])

    def _load_game_data(self):
        try:
            url = self.game_data_endpoint
            response = requests.get(url).json()[0]
            return GameData.from_json(response)
        except Exception as e:
            self.logger.error(f"Failed to load game data: {e}")
            raise RuntimeError(f"Failed to load game data: {e}")

    def _load_enums(self):
        for enum_name in self.game_data.enums:
            member_list = self.game_data.enums[enum_name]
            if enum_name == "positions":
                self.enums[enum_name] = ServerUtil.build_string_enum("POS", enum_name, member_list)
            elif enum_name == "itemType":
                self.enums[enum_name] = ServerUtil.build_string_enum("ITEM", enum_name, member_list)
            elif enum_name == "acType":
                self.enums[enum_name] = ServerUtil.build_string_enum("AC", enum_name, member_list)
            elif enum_name == "weaponClass":
                self.enums[enum_name] = ServerUtil.build_string_enum("WEAPON", enum_name, member_list)
            elif enum_name == "condition":
                self.enums[enum_name] = ServerUtil.build_string_enum("COND", enum_name, member_list)
            elif enum_name == "wearSlot":
                self.enums[enum_name] = ServerUtil.build_string_enum("WEAR", enum_name, member_list)
            elif enum_name == "damageType":
                self.enums[enum_name] = ServerUtil.build_string_enum("DAM", enum_name, member_list)
            elif enum_name == "applyType":
                self.enums[enum_name] = ServerUtil.build_string_enum("APPLY", enum_name, member_list)
            elif enum_name == "target":
                self.enums[enum_name] = ServerUtil.build_string_enum("TAR", enum_name, member_list)
            elif enum_name == "sector":
                self.enums[enum_name] = ServerUtil.build_string_enum("SECT", enum_name, member_list)
            elif enum_name == "size":
                self.enums[enum_name] = ServerUtil.build_string_enum("SIZE", enum_name, member_list)
            elif enum_name == "direction":
                self.enums[enum_name] = ServerUtil.build_string_enum("DIR", enum_name, member_list)
            elif enum_name == "sex":
                self.enums[enum_name] = ServerUtil.build_string_enum("SEX", enum_name, member_list)

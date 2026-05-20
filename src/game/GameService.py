import requests

from api.GameApi import GameApi
from injector import inject
from game.GameData import GameData
from server.LoggerFactory import LoggerFactory
from server.TimeVal import gettimeofday, TimeVal, stall_until_last_time
from server.ServiceConfig import ServiceConfig


class GameService:
    @inject
    def __init__(self, config: ServiceConfig):
        self.__name__ = "GameService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.game_data_endpoint = config.game_data_endpoint
        self.update_handler = None
        self.game_data = self._fetch_game_data()
        self.enums = dict()
        self._load_enums()
        self.last_time: TimeVal = gettimeofday()

    def set_update_handler(self, update_handler):
        self.update_handler = update_handler

    async def start(self):
        await self._game_loop()

    async def _game_loop(self):
        while True:
            await self._game_loop_iteration()

    async def _game_loop_iteration(self):
        self.last_time = gettimeofday()
        current_time = self.last_time.tv_sec
        self.logger.debug(f"Current time: {current_time}; Pulses per second: {self.enums['gameParameters']['PULSE_PER_SECOND']}")
        await self.update_handler.handle_updates()
        stall_until_last_time(self.last_time, self.enums['gameParameters']['PULSE_PER_SECOND'])

    def _fetch_game_data(self):
        try:
            url = self.game_data_endpoint
            response = requests.get(url).json()[0]
            return GameData.from_json(response)
        except Exception as e:
            self.logger.error(f"Failed to load game data: {e}")
            raise RuntimeError(f"Failed to load game data: {e}")

    def _load_enums(self):
        from util.GenericUtil import GenericUtil
        for enum_name in self.game_data.enums:
            member_map = self.game_data.enums.get(enum_name)
            self.enums[enum_name] = GenericUtil.build_int_enum(enum_name, member_map)

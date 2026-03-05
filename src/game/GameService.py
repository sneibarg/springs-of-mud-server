import requests
from injector import inject

from area import RomRoom
from game import GameData
from server.LoggerFactory import LoggerFactory
from server.TimeVal import gettimeofday, TimeVal, stall_until_last_time
from server.ServiceConfig import ServiceConfig


class GameService:
    @inject
    def __init__(self, config: ServiceConfig):
        self.__name__ = "GameService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.game_data_endpoint = config.game_data_endpoint
        self.game_data = self._load_game_data()
        self.last_time: TimeVal = gettimeofday()

    async def start(self):
        await self.game_loop()

    async def game_loop(self):
        while True:
            await self._game_loop_iteration()

    async def _game_loop_iteration(self):
        self.last_time = gettimeofday()
        current_time = self.last_time.tv_sec
        self.logger.debug(f"Current time: {current_time}; Pulses per second: {self.game_data.constants.pulses['perSecond']}")
        stall_until_last_time(self.last_time, self.game_data.constants.pulses['perSecond'])

    def _load_game_data(self):
        try:
            url = self.game_data_endpoint
            response = requests.get(url).json()[0]
            return GameData.from_json(response)
        except Exception as e:
            self.logger.error(f"Failed to load game data: {e}")
            raise RuntimeError(f"Failed to load game data: {e}")

import asyncio
import requests

from mobile import RomMobile


class MobileService:
    def __init__(self, injector, config):
        self.__name__ = "MobileService"
        from server import LoggerFactory
        self.logger = LoggerFactory.get_logger(self.__name__)
        from registry import RegistryService
        self.registry = injector.get(RegistryService)
        self.config = config['endpoints']
        from area.AreaService import AreaService
        self.area_service = injector.get(AreaService)
        from event import EventHandler
        self.event_handler = injector.get(EventHandler)
        self.task = None
        self.stop_flag = False
        self.all_mobiles = {}
        self.get_mobiles()
        self.logger.info("Initialized MobileService instance with a total of "+str(len(self.all_mobiles))+" mobiles in memory.")

    async def start(self):
        initial_spawn = False
        while not self.stop_flag:
            if not initial_spawn:
                for room_id in self.area_service.rooms:
                    room = self.area_service.rooms[room_id]

    def return_mobile_by_id(self, mobile_id):
        return self.all_mobiles[mobile_id]

    def get_mobiles(self):
        try:
            for mobile in requests.get(self.config['mobiles_endpoint']).json():
                self.all_mobiles[mobile['id']] = mobile
        except Exception as e:
            self.logger.error("Failed to get items: "+str(e))
        return None

    def start_task(self):
        self.task = asyncio.create_task(self.start())


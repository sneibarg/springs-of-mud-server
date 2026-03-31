import requests
from injector import inject

from area.Area import Area
from registry.RegistryService import RegistryService
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class AreaService:
    @inject
    def __init__(self, config: ServiceConfig, registry: RegistryService):
        self.__name__ = "AreaService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry = registry
        self.areas_endpoint = config.areas_endpoint
        self.load_areas()
        self.logger.info(f"Initialized AreaService instance with {str(len(self.registry.area_registry))} areas and {str(len(self.registry.room_registry))} rooms in memory.")

    def load_areas(self):
        from server.ServerUtil import ServerUtil
        response = requests.get(self.areas_endpoint).json()
        for area_json in response:
            area = Area.from_json(ServerUtil.camel_to_snake_case(area_json))
            self.logger.debug("Registering area: "+str(area))
            self.registry.register_area(area)

    def load_area(self, area_id):
        from server.ServerUtil import ServerUtil
        url = self.areas_endpoint + "/" + area_id
        area_json = requests.get(url).json()
        self.registry.register_area(Area.from_json(ServerUtil.camel_to_snake_case(area_json)))

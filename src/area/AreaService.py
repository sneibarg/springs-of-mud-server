import requests

from injector import inject
from area.Special import Special
from area.Shop import Shop
from area.Reset import Reset
from area.Area import Area
from registry.AreaRegistry import AreaRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class AreaService:
    @inject
    def __init__(self, config: ServiceConfig, area_registry: AreaRegistry):
        self.__name__ = "AreaService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.area_registry = area_registry
        self.areas_endpoint = config.areas_endpoint
        self.resets_endpoint = config.resets_endpoint
        self.shops_endpoint = config.shops_endpoint
        self.specials_endpoint = config.specials_endpoint
        self.load_areas()
        self.logger.info(f"Initialized AreaService instance with {str(len(self.area_registry.registry))} areas in memory.")

    def load_specials(self):
        response = requests.get(self.specials_endpoint).json()
        for special_json in response:
            special = Special.from_json(special_json)
            self.area_registry.register_special(special)

    def load_shops(self):
        response = requests.get(self.shops_endpoint).json()
        for shop_json in response:
            shop = Shop.from_json(shop_json)
            self.area_registry.register_shop(shop)

    def load_resets(self):
        response = requests.get(self.resets_endpoint).json()
        for reset_json in response:
            reset = Reset.from_json(reset_json)
            self.area_registry.register_reset(reset)

    def load_areas(self):
        from server.ServerUtil import ServerUtil
        response = requests.get(self.areas_endpoint).json()
        for area_json in response:
            area = Area.from_json(ServerUtil.camel_to_snake_case(area_json))
            self.area_registry.register_area(area)

    def load_area(self, area_id):
        from server.ServerUtil import ServerUtil
        url = self.areas_endpoint + "/" + area_id
        area_json = requests.get(url).json()
        self.area_registry.register_area(Area.from_json(ServerUtil.camel_to_snake_case(area_json)))

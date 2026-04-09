import requests

from typing import Optional
from injector import inject
from area.Area import Area
from game.RegistryService import RegistryService
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class AreaService:
    @inject
    def __init__(self, config: ServiceConfig, registry_service: RegistryService):
        self.__name__ = "AreaService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.area_registry = self.registry_service.area_registry
        self.reset_registry = self.registry_service.reset_registry
        self.shop_registry = self.registry_service.shop_registry
        self.special_registry = self.registry_service.special_registry
        self.mobile_registry = self.registry_service.mobile_registry
        self.item_registry = self.registry_service.item_registry
        self.areas_endpoint = config.areas_endpoint
        self.load_areas()
        self.logger.info(f"Initialized AreaService instance with {len(self.area_registry.all_areas())} areas in memory.")

    def reload_areas(self):
        self.logger.info("Reloading all areas...")
        self.area_registry.reset()
        self.load_areas()
        self.logger.info("Areas reload completed.")

    def load_areas(self):
        self._fetch_and_register(self.areas_endpoint, "all areas")

    def load_area(self, area_name: str):
        url = f"{self.areas_endpoint}/name/{area_name}"
        return self._fetch_and_register(url, f"area '{area_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Area]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                for area_data in data:
                    area = Area.from_json(area_data)
                    self._lazy_load(area)
                    self.area_registry.register(area)
                return None
            else:
                area = Area.from_json(data)
                self.area_registry.register(area)
                self._lazy_load(area)
                self.logger.info(f"Loaded {description}.")
                return area

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None

    def _lazy_load(self, area: Area):
        area.resets = self.reset_registry.all_resets_by_area_id(area.id)
        area.shops = self.shop_registry.all_shops_by_area_id(area.id)
        area.specials = self.special_registry.all_specials_by_area_id(area.id)
        area.items = self.item_registry.all_items_by_area_id(area.id)
        area.mobiles = self.mobile_registry.all_mobiles_by_area_id(area.id)

import requests

from typing import Optional
from injector import inject
from area.Area import Area
from area.SpecialRegistry import SpecialRegistry
from area.AreaRegistry import AreaRegistry
from area.ResetRegistry import ResetRegistry
from area.ShopRegistry import ShopRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class AreaService:
    @inject
    def __init__(self, config: ServiceConfig,
                 area_registry: AreaRegistry,
                 reset_registry: ResetRegistry,
                 shop_registry: ShopRegistry,
                 special_registry: SpecialRegistry):
        self.__name__ = "AreaService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.area_registry = area_registry
        self.reset_registry = reset_registry
        self.shop_registry = shop_registry
        self.special_registry = special_registry
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
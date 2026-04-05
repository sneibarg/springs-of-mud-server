import requests

from typing import Optional
from injector import inject
from area.Shop import Shop
from area.ShopRegistry import ShopRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class ShopService:
    @inject
    def __init__(self, config: ServiceConfig, shop_registry: ShopRegistry):
        self.__name__ = "ShopService"
        self.logger = LoggerFactory.get_logger(__name__)
        self.shops_endpoint = config.shops_endpoint
        self.shop_registry = shop_registry
        self.load_shops()

    def reload_shops(self):
        self.logger.info("Reloading shops...")
        self.shop_registry.reset()
        self.load_shops()
        self.logger.info("Shops reload completed.")

    def load_shops(self):
        self._fetch_and_register(self.shops_endpoint, "shops")
        self.logger.info(f"Loaded {len(self.shop_registry.all_shops())} shops.")

    def load_shop(self, shop_name: str):
        url = f"{self.shops_endpoint}/name/{shop_name}"
        return self._fetch_and_register(url, f"shop '{shop_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Shop]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                for shop_data in data:
                    shop = Shop.from_json(shop_data)
                    self.shop_registry.register(shop)
                return None
            else:
                shop = Shop.from_json(data)
                self.shop_registry.register(shop)
                self.logger.info(f"Loaded {description}.")
                return shop

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None
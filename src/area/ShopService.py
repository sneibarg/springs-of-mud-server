from injector import inject
from area.Shop import Shop
from area.ShopRegistry import ShopRegistry
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class ShopService(FetchAndRegisterMixin):
    log_fetch_list_count = False

    @inject
    def __init__(self, config: ServiceConfig, shop_registry: ShopRegistry):
        self.__name__ = "ShopService"
        self.logger = LoggerFactory.get_logger(self.__name__)
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

    def _build_fetch_item(self, shop_data) -> Shop:
        return Shop.from_json(shop_data)

    def _register_fetch_item(self, shop: Shop) -> None:
        self.shop_registry.register(shop)

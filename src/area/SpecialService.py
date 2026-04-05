import requests

from typing import Optional
from injector import inject
from area.Special import Special
from area.SpecialRegistry import SpecialRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class SpecialService:
    @inject
    def __init__(self, config: ServiceConfig, special_registry: SpecialRegistry):
        self.__name__ = "SpecialService"
        self.logger = LoggerFactory.get_logger(__name__)
        self.specials_endpoint = config.specials_endpoint
        self.special_registry = special_registry
        self.load_specials()

    def reload_specials(self):
        self.logger.info("Reloading specials...")
        self.special_registry.reset()
        self.load_specials()
        self.logger.info("Specials reload completed.")

    def load_specials(self):
        self._fetch_and_register(self.specials_endpoint, "specials")
        self.logger.info(f"Loaded {len(self.special_registry.all_specials())} specials.")

    def load_shop(self, special_name: str):
        url = f"{self.specials_endpoint}/name/{special_name}"
        return self._fetch_and_register(url, f"shop '{special_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Special]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                for special_data in data:
                    special = Special.from_json(special_data)
                    self.special_registry.register(special)
                return None
            else:
                special = Special.from_json(data)
                self.special_registry.register(special)
                self.logger.info(f"Loaded {description}.")
                return special

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None
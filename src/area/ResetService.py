import requests

from typing import Optional
from injector import inject
from area.Reset import Reset
from area.ResetRegistry import ResetRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class ResetService:
    @inject
    def __init__(self, config: ServiceConfig, reset_registry: ResetRegistry):
        self.__name__ = "ResetService"
        self.logger = LoggerFactory.get_logger(__name__)
        self.resets_endpoint = config.resets_endpoint
        self.reset_registry = reset_registry
        self.load_resets()

    def reload_resets(self):
        self.logger.info("Reloading resets...")
        self.reset_registry.reset()
        self.load_resets()
        self.logger.info("Resets reload completed.")

    def load_resets(self):
        self._fetch_and_register(self.resets_endpoint, "resets")
        self.logger.info(f"Loaded {len(self.reset_registry.all_resets())} resets.")

    def load_shop(self, reset_name: str):
        url = f"{self.resets_endpoint}/name/{reset_name}"
        return self._fetch_and_register(url, f"shop '{reset_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Reset]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                for reset_data in data:
                    reset = Reset.from_json(reset_data)
                    self.reset_registry.register(reset)
                return None
            else:
                reset = Reset.from_json(data)
                self.reset_registry.register(reset)
                self.logger.info(f"Loaded {description}.")
                return reset

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None
import requests

from injector import inject
from typing import Optional
from interp.HelpRegistry import HelpRegistry
from interp.HelpEntry import HelpEntry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class HelpService:
    @inject
    def __init__(self, config: ServiceConfig, help_registry: HelpRegistry):
        self.__name__ = "HelpService"
        self.helps_endpoint = config.helps_endpoint
        self.help_registry = help_registry
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.load_helps()

    def reload_helps(self):
        self.logger.info("Reloading all helps...")
        self.help_registry.reset()
        self.load_helps()
        self.logger.info("Helps reload completed.")

    def load_helps(self):
        self._fetch_and_register(self.helps_endpoint, "helps")

    def _fetch_and_register(self, url: str, description: str) -> Optional[HelpEntry]:
        from .InterpUtil import InterpUtil
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            normalized_data = InterpUtil.normalize_help_entries(data, "summary")
            if isinstance(data, list):
                count = 0
                for help_data in data:
                    help_entry = HelpEntry.from_json(help_data)
                    self.help_registry.register(help_entry)
                    count += 1
                self.logger.info(f"Loaded {count} {description}.")
                return None
            else:
                help_entry = HelpEntry.from_json(data)
                self.help_registry.register(help_entry)
                self.logger.info(f"Loaded {description}.")
                return help_entry

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None

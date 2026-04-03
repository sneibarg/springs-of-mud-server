import requests

from typing import Optional
from injector import inject
from interp.Social import Social
from server.LoggerFactory import LoggerFactory
from interp.SocialRegistry import SocialRegistry
from server.ServiceConfig import ServiceConfig


class SocialService:
    @inject
    def __init__(self, config: ServiceConfig, social_registry: SocialRegistry):
        self.__name__ = "SocialService"
        self.logger = LoggerFactory.get_logger(__name__)
        self.socials_endpoint = config.socials_endpoint
        self.social_registry = social_registry
        self.load_socials()

    def reload_socials(self) -> None:
        self.logger.info("Reloading all socials...")
        self.social_registry.reset()
        self.load_socials()
        self.logger.info("Socials reload completed.")

    def load_socials(self):
        self._fetch_and_register(self.socials_endpoint, "all socials")

    def load_social(self, social_name: str):
        url = f"{self.socials_endpoint}/name/{social_name}"
        return self._fetch_and_register(url, f"social '{social_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Social]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                count = 0
                for social_data in data:
                    social = Social.from_json(social_data)
                    self.social_registry.register(social)
                    count += 1
                self.logger.info(f"Loaded {count} {description}.")
                return None
            else:
                social = Social.from_json(data)
                self.social_registry.register(social)
                self.logger.info(f"Loaded {description}.")
                return social

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None

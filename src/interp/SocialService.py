from injector import inject
from interp.Social import Social
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from interp.SocialRegistry import SocialRegistry
from server.ServiceConfig import ServiceConfig


class SocialService(FetchAndRegisterMixin):
    @inject
    def __init__(self, config: ServiceConfig, social_registry: SocialRegistry):
        self.__name__ = "SocialService"
        self.logger = LoggerFactory.get_logger(self.__name__)
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

    def _build_fetch_item(self, social_data) -> Social:
        return Social.from_json(social_data)

    def _register_fetch_item(self, social: Social) -> None:
        self.social_registry.register(social)

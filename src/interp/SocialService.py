import requests

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
        self.logger.info(f"Initialized SocialService instance with a total of {len(self.social_registry.registry)} socials.")

    def load_socials(self):
        social_list = requests.get(self.socials_endpoint).json()
        for social_data in social_list:
            social = Social.from_json(social_data)
            self.social_registry.register_social(social)

    def load_social(self, social_name: str):
        social_data = requests.get(self.socials_endpoint + "/name/" + social_name).json()
        social = Social.from_json(social_data)
        self.social_registry.register_social(social)

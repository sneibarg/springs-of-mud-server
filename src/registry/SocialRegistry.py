import threading

from typing import Optional
from injector import inject
from command.Social import Social
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus


class SocialRegistry:
    @inject
    def __init__(self, message_bus: MessageBus):
        self.__name__ = "SocialRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry = {}
        self.message_bus = message_bus
        self.lock = threading.Lock()

    def get_social_by_id(self, social_id: int) -> Optional[Social]:
        try:
            return self.registry[social_id]
        except KeyError:
            self.logger.error(f"Social with ID {social_id} not found")
            return None

    def get_social_by_name(self, social_name: str) -> Optional[Social]:
        social_name = social_name.strip().lower()
        try:
            for social in self.registry.values():
                if social.name.lower() == social_name:
                    return social
        except Exception as e:
            self.logger.error(f"Error retrieving social by name: {e}")
            return None

    def register_social(self, social: Social):
        with self.lock:
            self.registry[social.id] = social

    def unregister_social(self, social_id: str):
        with self.lock:
            if social_id in self.registry:
                del self.registry[social_id]
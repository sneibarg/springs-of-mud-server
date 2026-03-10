from injector import inject
from server.LoggerFactory import LoggerFactory


class EventHandler:
    @inject
    def __init__(self):
        self.__name__ = "EventHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.command_list = list()
        self.character_registry = dict()
        self.mobile_registry = dict()
        self.combat_events = dict()
        self.logger.info("Initialized EventHandler instance.")

    def register_character(self, character):
        self.logger.info("Registering character "+character.name)
        self.character_registry[character.name] = character

    def unregister_character(self, character):
        self.logger.info("Unregistering character "+character)
        del self.character_registry[character]

    def register_mobile(self, mobile):
        self.logger.debug("Registering mobile "+mobile.id)
        self.mobile_registry[mobile.id] = mobile

    def unregister_mobile(self, mobile):
        self.logger.debug("Unregistering mobile "+mobile.id)
        del self.mobile_registry[mobile.id]

from injector import inject

from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from server.LoggerFactory import LoggerFactory


class EffectHandler:
    @inject
    def __init__(self, registry_service: RegistryService, enum_provider: EnumProvider):
        self.__name__ = "EffectHandler"
        self.logger = LoggerFactory.get_logger(__name__)
        self.registry_service = registry_service
        self.enum_provider = enum_provider

    

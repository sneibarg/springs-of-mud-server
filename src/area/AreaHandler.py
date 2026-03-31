from injector import inject
from registry import RegistryService
from server.messaging import MessageBus


class AreaHandler:
    @inject
    def __init__(self, message_bus: MessageBus, registry_service: RegistryService):
        self.__name__ = "AreaHandler"
        self.message_bus = message_bus
        self.registry_service = registry_service

    def passes_update_check(self, area_id, last_reset):
        return self.registry_service.area_registry[area_id].last_reset != last_reset

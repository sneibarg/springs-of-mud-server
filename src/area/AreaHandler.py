from injector import inject

from area.AreaRegistry import AreaRegistry
from server.messaging import MessageBus


class AreaHandler:
    @inject
    def __init__(self, message_bus: MessageBus, area_registry: AreaRegistry):
        self.__name__ = "AreaHandler"
        self.message_bus = message_bus
        self.area_registry = area_registry

    def passes_update_check(self, area_id, last_reset):
        if area_id not in self.area_registry.registry:
            return False
        return self.area_registry.get_area_by_id(area_id).last_reset != last_reset

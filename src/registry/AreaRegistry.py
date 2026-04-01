import threading

from typing import Optional
from area.Area import Area


class AreaRegistry:
    def __init__(self):
        self.registry = {}
        self.lock = threading.Lock()

    def get_area_by_name(self, area_name: str) -> Optional[Area]:
        for area in self.registry.values():
            if area.name == area_name:
                return area
        return None

    def get_area_by_id(self, area_id) -> Optional[Area]:
        try:
            return self.registry[area_id]
        except KeyError:
            return None

    def unregister_area(self, area: Area):
        with self.lock:
            del self.registry[area.id]

    def register_area(self, area: Area):
        with self.lock:
            self.registry[area.id] = area

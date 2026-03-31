import threading

from area.Area import Area


class AreaRegistry:
    def __init__(self):
        self.registry = dict()
        self.lock = threading.Lock()

    def get_area_by_name(self, area_name: str) -> Area | None:
        for area in self.registry.values():
            if area.name == area_name:
                return area
        return None

    def get_area_by_id(self, area_id) -> Area | None:
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

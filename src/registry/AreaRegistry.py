import threading

from typing import Optional
from area.Reset import Reset
from area.Area import Area
from area.Shop import Shop
from area.Special import Special


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

    def get_reset_by_area_id(self, area_id: str) -> Optional[Reset]:
        for reset in self.registry.values():
            if reset.area_id == area_id:
                return reset
        return None

    def unregister_area(self, area: Area):
        with self.lock:
            del self.registry[area.id]

    def register_area(self, area: Area):
        with self.lock:
            self.registry[area.id] = area

    def register_reset(self, reset: Reset):
        with self.lock:
            self.registry[reset.id] = reset

    def unregister_reset(self, reset_id: str):
        with self.lock:
            del self.registry[reset_id]

    def register_shop(self, shop: Shop):
        with self.lock:
            self.registry[shop.id] = shop

    def unregister_shop(self, shop_id: str):
        with self.lock:
            del self.registry[shop_id]

    def register_special(self, special: Special):
        with self.lock:
            self.registry[special.id] = special

    def unregister_special(self, special_id: str):
        with self.lock:
            del self.registry[special_id]
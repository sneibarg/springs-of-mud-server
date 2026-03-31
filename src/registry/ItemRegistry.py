import threading
from typing import Optional

from object.Item import Item


class ItemRegistry:
    def __init__(self):
        self.registry = {}
        self.lock = threading.Lock()

    def get_item_by_id(self, item_id) -> Optional[Item]:
        try:
            return self.registry[item_id]
        except KeyError:
            return None

    def get_item_by_name(self, item_name: str) -> Optional[Item]:
        for item in self.registry:
            if item.name == item_name:
                return item
        return None

    def register_item(self, item: Item):
        with self.lock:
            self.registry[item.id] = item

    def unregister_item(self, item: Item):
        with self.lock:
            del self.registry[item.id]


import threading

from object.Item import Item


class ItemRegistry:
    def __init__(self):
        self.registry = {}
        self.lock = threading.Lock()

    def get_item_by_id(self, item_id) -> Item | None:
        try:
            return self.registry[item_id]
        except KeyError:
            return None

    def get_item_by_name(self, item_name: str) -> Item | None:
        for item in self.registry:
            if item.name == item_name:
                return item
        return None
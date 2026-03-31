import threading

from mobile.Mobile import Mobile


class MobileRegistry:
    def __init__(self):
        self.registry = {}
        self.lock = threading.Lock()

    def get_mobile_by_id(self, mobile_id) -> Mobile | None:
        try:
            return self.registry[mobile_id]
        except KeyError:
            return None

    def get_mobile_by_name(self, mobile_name) -> Mobile | None:
        for mobile in self.registry.values():
            if mobile_name == mobile.name:
                return mobile
        return None

    def unregister_mobile(self, mobile: Mobile):
        with self.lock:
            del self.registry[mobile.id]

    def register_mobile(self, mobile):
        with self.lock:
            self.registry[mobile.id] = mobile

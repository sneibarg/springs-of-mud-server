import threading


class RegistryService:
    def __init__(self):
        self.area_registry = {}
        self.room_registry = {}
        self.character_registry = {}
        self.mobile_registry = {}
        self.lock = threading.Lock()

    def unregister_room(self, room):
        with self.lock:
            del self.room_registry[room.id]

    def register_room(self, room):
        with self.lock:
            self.room_registry[room.id] = room

    def unregister_area(self, area):
        with self.lock:
            del self.area_registry[area.id]

    def register_area(self, area):
        with self.lock:
            self.area_registry[area.id] = area

    def get_area_from_registry(self, area_id):
        return self.area_registry[area_id]

    def unregister_mobile(self, mobile):
        with self.lock:
            del self.area_registry[mobile.id]

    def register_mobile(self, mobile):
        with self.lock:
            self.mobile_registry[mobile.id] = mobile

    def get_mobile_from_registry(self, mobile_id):
        return self.mobile_registry[mobile_id]

    def unregister_character(self, character):
        with self.lock:
            del self.character_registry[character.id]

    def register_character(self, character):
        with self.lock:
            self.character_registry[character.id] = character

    def get_character_from_registry(self, character_id):
        return self.character_registry[character_id]

import threading


class RegistryService:
    def __init__(self):
        self.player_list = {}
        self.character_list = {}
        self.area_registry = {}
        self.room_registry = {}
        self.character_registry = {}
        self.mobile_registry = {}
        self.lock = threading.Lock()

    def get_player_characters(self, player_id):
        return self.player_list[player_id]['playerCharacterList']

    def get_player_by_name(self, name):
        for player in self.player_list.values():
            if player.name == name:
                return player
        return None

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
            del self.mobile_registry[mobile.id]

    def register_mobile(self, mobile):
        with self.lock:
            self.mobile_registry[mobile.id] = mobile

    def get_mobile_from_registry(self, mobile_id):
        return self.mobile_registry[mobile_id]

    def unregister_character(self, character_id):
        with self.lock:
            del self.character_registry[character_id]

    def register_character(self, character, player_id):
        with self.lock:
            self.character_registry[character.id] = dict()
            self.character_registry[character.id]["current_character"] = character
            self.character_registry[character.id]["player_id"] = dict()
            self.character_registry[character.id]["player_id"] = player_id

    def get_character_from_registry(self, character_id):
        return self.character_registry[character_id]

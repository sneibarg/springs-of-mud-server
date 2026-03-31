import threading

from player.Character import Character


class CharacterRegistry:
    def __init__(self):
        self.registry = {}
        self.lock = threading.Lock()

    def get_character_by_id(self, character_id) -> Character | None:
        if "current_character" not in self.registry[character_id]:
            return None
        try:
            return self.registry[character_id]["current_character"]
        except KeyError:
            return None

    def get_character_by_name(self, character_name) -> Character | None:
        for character in self.registry.values():
            if "current_character" in character and character["current_character"].name == character_name:
                return character["current_character"]
        return None

    def unregister_character(self, character: Character):
        with self.lock:
            if "current_character" in self.registry[character.id]:
                del self.registry[character.id]["current_character"]

    def register_character(self, player_id, character):
        with self.lock:
            self.registry[character.id] = dict()
            self.registry[character.id]["current_character"] = character
            self.registry[character.id]["player_id"] = dict()
            self.registry[character.id]["player_id"] = player_id

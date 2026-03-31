import threading

from typing import List
from player.Player import Player


class PlayerRegistry:
    def __init__(self):
        self.registry = {}
        self.lock = threading.Lock()

    def get_player_characters(self, player_id) -> List[str] | None:
        try:
            return self.registry[player_id].player_character_list
        except KeyError:
            return None

    def get_player_by_id(self, player_id) -> Player | None:
        try:
            return self.registry[player_id]
        except KeyError:
            return None

    def get_player_by_name(self, player_name: str) -> Player | None:
        try:
            return self.registry[player_name]
        except KeyError:
            return None

    def register_player(self, player: Player):
        with self.lock:
            self.registry[player.id] = player

    def unregister_player(self, player_id: str):
        with self.lock:
            if player_id in self.registry:
                del self.registry[player_id]

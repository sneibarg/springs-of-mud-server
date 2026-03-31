import threading

from typing import Optional
from area.Room import Room


class RoomRegistry:
    def __init__(self):
        self.registry = {}
        self.lock = threading.Lock()

    def get_room_by_id(self, room_id) -> Optional[Room]:
        try:
            return self.registry[room_id]
        except KeyError:
            return None

    def get_room_by_name(self, room_name) -> Optional[Room]:
        for room in self.registry.values():
            if room.name == room_name:
                return room
        return None

    def unregister_room(self, room: Room):
        with self.lock:
            del self.registry[room.id]

    def register_room(self, room: Room):
        with self.lock:
            self.registry[room.id] = room

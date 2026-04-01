import threading

from typing import Optional


class CommandRegistry:
    def __init__(self):
        self.registry = {}
        self.lock = threading.Lock()

    def get_command_by_id(self, command_id) -> Optional[dict]:
        try:
            return self.registry[command_id]
        except KeyError:
            return None

    def get_command_by_name(self, command_name) -> Optional[dict]:
        for command in self.registry.values():
            if command['name'] == command_name:
                return command
        return None

    def register_command(self, command: dict):
        with self.lock:
            self.registry[command['id']] = command

    def unregister_command(self, command_id: str):
        with self.lock:
            del self.registry[command_id]

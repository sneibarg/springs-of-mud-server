import threading

from typing import Optional


class InterpRegistry:
    def __init__(self):
        self.registry = {}
        self.help_registry = {}
        self.lock = threading.Lock()

    def get_help_by_keyword(self, keyword: str) -> Optional[dict]:
        keyword_lower = keyword.lower()
        for help_data in self.help_registry.values():
            if keyword_lower in help_data['keyword'].lower().split():
                return help_data
        return None

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

    def register_help(self, help_data: dict):
        with self.lock:
            self.help_registry[help_data['keyword'].lower()] = help_data

    def unregister_help(self, keyword: str):
        with self.lock:
            del self.help_registry[keyword]

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from game.HandlerService import HandlerService
from player.Player import Player
from area.Room import Room
from server.connection import TelnetConnection


@dataclass
class Context:
    """Shared context passed through the lambda pipeline."""
    player: Player
    character: Any
    connection: TelnetConnection = None
    handler_service: HandlerService = None
    parameters: Any = None
    room: Optional[Room] = None
    result: Any = None
    data: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get_handler(self, key: str):
        if self.handler_service:
            return self.handler_service.get_handler(key)
        return None

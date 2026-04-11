from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from player.Player import Player
from area.Room import Room


@dataclass
class Context:
    """Shared context passed through the lambda pipeline."""
    player: Player
    character: Any
    parameters: Any = None
    injector: Any = None
    room: Optional[Room] = None
    result: Any = None
    data: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value

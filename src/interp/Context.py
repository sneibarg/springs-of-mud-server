from typing import TYPE_CHECKING
from dataclasses import dataclass
from typing import Any, Optional, List
from player.Player import Player
from area.Room import Room

if TYPE_CHECKING:
    from game.HandlerService import HandlerService


@dataclass
class Context:
    """Shared context passed through the lambda pipeline."""
    player: Player
    character: Any
    handler_service: HandlerService = None
    parameters: List[str] = None
    result: Any = None
    done: bool = False
    next_index: int = 0
    count: Optional[int] = 0  # used for counting items; result of number_argument
    room: Optional[Room] = None

    def mobile_handler(self):
        if self.handler_service:
            return self.handler_service.get_handler("mh")
        return None

    def room_handler(self):
        if self.handler_service:
            return self.handler_service.get_handler("rh")
        return None

    def item_handler(self):
        if self.handler_service:
            return self.handler_service.get_handler("ih")
        return None

    def player_handler(self):
        if self.handler_service:
            return self.handler_service.get_handler("ph")
        return None

    def social_handler(self):
        if self.handler_service:
            return self.handler_service.get_handler("sh")
        return None

    def jump_to(self, index: int):
        self.next_index = index

    def finish(self):
        self.done = True

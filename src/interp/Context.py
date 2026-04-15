from typing import TYPE_CHECKING
from dataclasses import dataclass
from typing import Any, Optional, List
from player.Player import Player


if TYPE_CHECKING:
    from game.HandlerService import HandlerService
    from area.Room import Room
    from server.connection.TelnetConnection import TelnetConnection


@dataclass
class Context:
    """Shared context passed through the lambda pipeline."""
    player: Player
    character: Any
    handler_service: HandlerService = None
    conn: TelnetConnection = None
    parameters: List[str] = None
    result: Any = None
    done: bool = False
    number: int = 1
    next_index: Optional[int] = None
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

    def look_register_match(self) -> bool:
        self.count += 1
        return self.count == self.number

    async def disconnect(self):
        await self.conn.close()

    @staticmethod
    def look_keyword_matches(token: str, keyword: str) -> bool:
        t = (token or "").strip().lower()
        k = (keyword or "").strip().lower()
        if not t or not k:
            return False
        words = [w for w in k.split() if w]
        return any(w == t or w.startswith(t) for w in words)


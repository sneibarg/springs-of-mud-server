from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from typing import Any, Optional, List


if TYPE_CHECKING:
    from game.HandlerService import HandlerService
    from game.RegistryService import RegistryService
    from area.Room import Room
    from server.connection.TelnetConnection import TelnetConnection
    from interp.Command import Command


@dataclass
class Context:
    """Shared context passed through the lambda pipeline."""
    character: Any
    registry_service: RegistryService = field(kw_only=True)
    command: Command = None
    handler_service: HandlerService = None
    conn: TelnetConnection = None
    parameters: List[str] = None
    result: Any = None
    done: bool = False
    number: int = 1
    next_index: Optional[int] = None
    count: Optional[int] = 0  # used for counting items; result of number_argument
    room: Optional[Room] = None
    raw_command: str | None = None

    @classmethod
    def from_subject(cls, subject):
        """Unwrap a view's context, or return an already unwrapped context."""
        return getattr(subject, "context", subject)

    @classmethod
    def for_character(cls, character) -> dict[str, Any]:
        """Return a character's mutable state, initializing its dictionary if needed."""
        current = getattr(character, "context", None)
        if not isinstance(current, dict):
            current = {}
            setattr(character, "context", current)
        return current

    def __post_init__(self):
        if self.registry_service is None:
            raise TypeError("Context requires a registry service")

    @property
    def argument(self) -> str:
        if isinstance(self.result, str):
            return self.result.strip()
        if self.parameters:
            return " ".join(self.parameters).strip()
        return ""

    @property
    def current_fighting(self):
        return self.character.fighting

    @property
    def position(self) -> int:
        from api.CharacterApi import CharacterApi
        return CharacterApi.position_value(self.character)

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

    def wiz_handler(self):
        if self.handler_service:
            return self.handler_service.get_handler("wh")
        return None

    def register_match(self) -> bool:
        """Count a candidate and report whether it is the requested ordinal."""
        self.count += 1
        return self.count == self.number

    def jump_to(self, index: int):
        self.next_index = index

    def finish(self):
        self.done = True

    async def disconnect(self):
        await self.conn.close()

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from player.Character import Character


class SessionStatus(Enum):
    CONNECTED = auto()
    AUTHENTICATING = auto()
    PLAYING = auto()
    IDLING = auto()
    DISCONNECTING = auto()
    DISCONNECTED = auto()


@dataclass
class SessionState:
    session_id: str
    status: SessionStatus = SessionStatus.CONNECTED
    player_id: Optional[str] = None
    account_name: Optional[str] = None
    character: Optional[Character] = None
    ansi_enabled: bool = False
    connected_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    auth_attempts: int = 0
    metadata: dict = field(default_factory=dict)

    def update_activity(self) -> None:
        self.last_activity = datetime.now()

    def is_authenticated(self) -> bool:
        return self.player_id is not None

    def is_playing(self) -> bool:
        return self.status == SessionStatus.PLAYING

    def is_idle(self) -> bool:
        return self.status == SessionStatus.IDLING

    def can_authenticate(self) -> bool:
        return self.auth_attempts < 3 and self.status in (SessionStatus.CONNECTED, SessionStatus.AUTHENTICATING)

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


class SessionPhase(Enum):
    CONNECTED = auto()
    AUTHENTICATING = auto()
    PLAYING = auto()
    DISCONNECTING = auto()
    DISCONNECTED = auto()


@dataclass
class SessionState:
    session_id: str
    phase: SessionPhase = SessionPhase.CONNECTED
    player_id: Optional[str] = None
    character_id: Optional[str] = None
    account_name: Optional[str] = None
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
        return self.phase == SessionPhase.PLAYING

    def can_authenticate(self) -> bool:
        return self.auth_attempts < 3 and self.phase in (SessionPhase.CONNECTED, SessionPhase.AUTHENTICATING)

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


class SessionPhase(Enum):
    """Phases of a player session"""
    CONNECTED = auto()
    AUTHENTICATING = auto()
    SELECTING_CHARACTER = auto()
    PLAYING = auto()
    DISCONNECTING = auto()
    DISCONNECTED = auto()


@dataclass
class SessionState:
    """
    Tracks the state of a player session.
    Decouples session lifecycle from Player object.
    """
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
        """Update last activity timestamp"""
        self.last_activity = datetime.now()

    def is_authenticated(self) -> bool:
        """Check if session is authenticated"""
        return self.player_id is not None

    def is_playing(self) -> bool:
        """Check if session is in playing phase"""
        return self.phase == SessionPhase.PLAYING

    def can_authenticate(self) -> bool:
        """Check if session can attempt authentication"""
        return self.auth_attempts < 3 and self.phase in (SessionPhase.CONNECTED, SessionPhase.AUTHENTICATING)

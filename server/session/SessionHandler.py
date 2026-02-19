from typing import Dict, Optional
from .SessionState import SessionState, SessionPhase
from server.protocol import Message


class SessionHandler:
    """
    Manages session states for all connected clients.
    Works alongside ConnectionManager to track session lifecycle.
    """

    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def create_session(self, session_id: str) -> SessionState:
        """Create a new session"""
        session = SessionState(session_id=session_id)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SessionState]:
        """Get session by ID"""
        return self._sessions.get(session_id)

    def get_session_by_player(self, player_id: str) -> Optional[SessionState]:
        """Get session by player ID"""
        for session in self._sessions.values():
            if session.player_id == player_id:
                return session
        return None

    def remove_session(self, session_id: str) -> None:
        """Remove a session"""
        if session_id in self._sessions:
            session = self._sessions[session_id]
            session.phase = SessionPhase.DISCONNECTED
            del self._sessions[session_id]

    def get_active_sessions(self) -> list[SessionState]:
        """Get all active sessions"""
        return [s for s in self._sessions.values() if s.phase != SessionPhase.DISCONNECTED]

    def get_playing_sessions(self) -> list[SessionState]:
        """Get all sessions in playing phase"""
        return [s for s in self._sessions.values() if s.is_playing()]

    def session_count(self) -> int:
        """Get count of active sessions"""
        return len(self._sessions)

    def update_session_activity(self, session_id: str) -> None:
        """Update last activity timestamp for session"""
        session = self.get_session(session_id)
        if session:
            session.update_activity()

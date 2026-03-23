from typing import Dict, Optional
from server.session.SessionState import SessionState, SessionStatus


class SessionHandler:
    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def create_session(self, session_id: str) -> SessionState:
        session = SessionState(session_id=session_id)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SessionState]:
        return self._sessions.get(session_id)

    def get_session_by_player(self, player_id: str) -> Optional[SessionState]:
        for session in self._sessions.values():
            if session.player_id == player_id:
                return session
        return None

    def remove_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            session = self._sessions[session_id]
            session.status = SessionStatus.DISCONNECTED
            del self._sessions[session_id]

    def get_active_sessions(self) -> list[SessionState]:
        return [s for s in self._sessions.values() if s.status != SessionStatus.DISCONNECTED]

    def get_playing_sessions(self) -> list[SessionState]:
        return [s for s in self._sessions.values() if s.is_playing()]

    def session_count(self) -> int:
        return len(self._sessions)

    def update_session_activity(self, session_id: str) -> None:
        session = self.get_session(session_id)
        if session:
            session.update_activity()

from datetime import datetime
from typing import Dict, Optional
from server.session.SessionState import SessionState, SessionStatus


class SessionHandler:
    def __init__(self, max_idle_time: int = 30):
        self.__name__ = "SessionHandler"
        self._sessions: Dict[str, SessionState] = {}
        self.max_idle_time = max_idle_time

    def create_session(self, session_id: str) -> SessionState:
        session = SessionState(session_id=session_id)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SessionState]:
        return self._sessions.get(session_id)

    def get_session_by_player(self, player_id: str) -> Optional[SessionState] :
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
        return [s for s in self._sessions.values() if s.is_playing() or s.is_idle()]

    def session_count(self) -> int:
        return len(self._sessions)

    def update_session_activity(self, session_id: str) -> None:
        session = self.get_session(session_id)
        if session:
            session.update_activity()

    def is_session_idle(self, session: SessionState) -> bool:
        idle_time = int(datetime.now().timestamp()) - int(session.last_activity.timestamp())
        return idle_time < (self.max_idle_time * 1000)

    def get_idle_timeout(self, session) -> int:
        return int(session.last_activity.timestamp()) + self.max_idle_time

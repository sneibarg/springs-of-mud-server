from typing import Dict, Optional, List

from server.connection.TelnetConnection import TelnetConnection
from server.connection.Connection import Connection


class ConnectionManager:
    def __init__(self):
        self._connections: Dict[str, TelnetConnection] = {}
        self._character_sessions: Dict[str, str] = {}  # character_id -> session_id

    def add_connection(self, connection: TelnetConnection) -> None:
        self._connections[connection.session_id] = connection

    def remove_connection(self, session_id: str) -> None:
        if session_id in self._connections:
            del self._connections[session_id]

        character_id = self._get_character_id_by_session(session_id)
        if character_id:
            del self._character_sessions[character_id]

    def get_connection(self, session_id: str) -> Optional[TelnetConnection]:
        return self._connections.get(session_id)

    def get_connection_by_character(self, character_id: str) -> Optional[TelnetConnection]:
        session_id = self._character_sessions.get(character_id)
        if session_id:
            return self._connections.get(session_id)
        return None

    def bind_character(self, character_id: str, session_id: str) -> None:
        self._character_sessions[character_id] = session_id

    def unbind_character(self, character_id: str) -> None:
        if character_id in self._character_sessions:
            del self._character_sessions[character_id]

    def get_all_sessions(self) -> List[str]:
        return list(self._connections.keys())

    def get_all_connections(self) -> List[Connection]:
        return list(self._connections.values())

    def _get_character_id_by_session(self, session_id: str) -> Optional[str]:
        for character_id, sid in self._character_sessions.items():
            if sid == session_id:
                return character_id
        return None

    async def close_all(self) -> None:
        for connection in list(self._connections.values()):
            try:
                await connection.close()
            except Exception:
                pass
        self._connections.clear()
        self._character_sessions.clear()

    def connection_count(self) -> int:
        return len(self._connections)

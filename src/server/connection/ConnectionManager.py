from typing import Dict, Optional, List
from server.connection.Connection import Connection
from server.protocol import Message


class ConnectionManager:
    def __init__(self):
        self._connections: Dict[str, Connection] = {}
        self._player_sessions: Dict[str, str] = {}  # player_id -> session_id

    def add_connection(self, connection: Connection) -> None:
        self._connections[connection.session_id] = connection

    def remove_connection(self, session_id: str) -> None:
        if session_id in self._connections:
            del self._connections[session_id]

        player_id = self._get_player_id_by_session(session_id)
        if player_id:
            del self._player_sessions[player_id]

    def get_connection(self, session_id: str) -> Optional[Connection]:
        return self._connections.get(session_id)

    def get_connection_by_player(self, player_id: str) -> Optional[Connection]:
        session_id = self._player_sessions.get(player_id)
        if session_id:
            return self._connections.get(session_id)
        return None

    def bind_player(self, player_id: str, session_id: str) -> None:
        self._player_sessions[player_id] = session_id

    def unbind_player(self, player_id: str) -> None:
        if player_id in self._player_sessions:
            del self._player_sessions[player_id]

    def get_all_sessions(self) -> List[str]:
        return list(self._connections.keys())

    def get_all_connections(self) -> List[Connection]:
        return list(self._connections.values())

    def _get_player_id_by_session(self, session_id: str) -> Optional[str]:
        for player_id, sid in self._player_sessions.items():
            if sid == session_id:
                return player_id
        return None

    async def close_all(self) -> None:
        for connection in list(self._connections.values()):
            try:
                await connection.close()
            except Exception:
                pass
        self._connections.clear()
        self._player_sessions.clear()

    def connection_count(self) -> int:
        return len(self._connections)

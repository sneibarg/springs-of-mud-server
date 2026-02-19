from typing import Dict, Optional, List
from .Connection import Connection
from server.protocol import Message


class ConnectionManager:
    """
    Manages all active connections.
    Provides lookup by session_id and broadcast capabilities.
    """

    def __init__(self):
        self._connections: Dict[str, Connection] = {}
        self._player_sessions: Dict[str, str] = {}  # player_id -> session_id

    def add_connection(self, connection: Connection) -> None:
        """Add a new connection"""
        self._connections[connection.session_id] = connection

    def remove_connection(self, session_id: str) -> None:
        """Remove a connection"""
        if session_id in self._connections:
            del self._connections[session_id]

        # Also remove from player sessions
        player_id = self._get_player_id_by_session(session_id)
        if player_id:
            del self._player_sessions[player_id]

    def get_connection(self, session_id: str) -> Optional[Connection]:
        """Get connection by session ID"""
        return self._connections.get(session_id)

    def get_connection_by_player(self, player_id: str) -> Optional[Connection]:
        """Get connection by player ID"""
        session_id = self._player_sessions.get(player_id)
        if session_id:
            return self._connections.get(session_id)
        return None

    def bind_player(self, player_id: str, session_id: str) -> None:
        """Associate a player with a session"""
        self._player_sessions[player_id] = session_id

    def unbind_player(self, player_id: str) -> None:
        """Remove player-session association"""
        if player_id in self._player_sessions:
            del self._player_sessions[player_id]

    def get_all_sessions(self) -> List[str]:
        """Get all active session IDs"""
        return list(self._connections.keys())

    def get_all_connections(self) -> List[Connection]:
        """Get all active connections"""
        return list(self._connections.values())

    def _get_player_id_by_session(self, session_id: str) -> Optional[str]:
        """Internal helper to find player ID by session"""
        for player_id, sid in self._player_sessions.items():
            if sid == session_id:
                return player_id
        return None

    async def broadcast(self, message: Message, exclude_sessions: Optional[List[str]] = None) -> None:
        """Broadcast a message to all connections"""
        exclude = exclude_sessions or []
        for session_id, connection in self._connections.items():
            if session_id not in exclude and not connection.is_closed():
                try:
                    await connection.send_message(message)
                except Exception:
                    pass  # Connection failed, will be cleaned up later

    async def close_all(self) -> None:
        """Close all connections"""
        for connection in list(self._connections.values()):
            try:
                await connection.close()
            except Exception:
                pass
        self._connections.clear()
        self._player_sessions.clear()

    def connection_count(self) -> int:
        """Get count of active connections"""
        return len(self._connections)

from typing import List, Optional
from server.protocol import Message, MessageType
from server.connection import ConnectionManager


class MessageBus:
    """
    Central message routing system.
    Handles sending messages to players, rooms, areas, and broadcasts.
    """

    def __init__(self, connection_manager: ConnectionManager, session_handler):
        self.connection_manager = connection_manager
        self.session_handler = session_handler

    async def send_to_player(self, player_id: str, message: Message) -> bool:
        """
        Send a message to a specific player.
        Returns True if sent successfully.
        """
        connection = self.connection_manager.get_connection_by_player(player_id)
        if connection and not connection.is_closed():
            try:
                await connection.send_message(message)
                return True
            except Exception:
                return False
        return False

    async def send_to_session(self, session_id: str, message: Message) -> bool:
        """
        Send a message to a specific session.
        Returns True if sent successfully.
        """
        connection = self.connection_manager.get_connection(session_id)
        if connection and not connection.is_closed():
            try:
                await connection.send_message(message)
                return True
            except Exception:
                return False
        return False

    async def send_to_room(self, room_id: str, message: Message, exclude_player_ids: Optional[List[str]] = None) -> int:
        """
        Send a message to all players in a room.
        Returns count of players who received the message.
        """
        exclude = exclude_player_ids or []
        count = 0
        sessions = self.session_handler.get_playing_sessions()

        for session in sessions:
            if session.player_id in exclude:
                continue

            if await self.send_to_player(session.player_id, message):
                count += 1

        return count

    async def send_to_area(self, area_id: str, message: Message) -> int:
        """
        Send a message to all players in an area.
        Returns count of players who received the message.
        """
        count = 0
        sessions = self.session_handler.get_playing_sessions()

        for session in sessions:
            if await self.send_to_player(session.player_id, message):
                count += 1

        return count

    async def broadcast(self, message: Message, exclude_player_ids: Optional[List[str]] = None) -> int:
        """
        Broadcast a message to all connected players.
        Returns count of players who received the message.
        """
        exclude = exclude_player_ids or []
        count = 0

        sessions = self.session_handler.get_active_sessions()

        for session in sessions:
            if session.player_id and session.player_id not in exclude:
                if await self.send_to_player(session.player_id, message):
                    count += 1

        return count

    async def send_prompt(self, player_id: str, health: int, mana: int, movement: int) -> bool:
        """Send a game prompt to a player"""
        from server.connection import TelnetConnection
        connection = self.connection_manager.get_connection_by_player(player_id)

        if connection and isinstance(connection, TelnetConnection):
            try:
                await connection.send_prompt(health, mana, movement)
                return True
            except Exception:
                return False
        return False

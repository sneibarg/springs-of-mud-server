from typing import List, Optional, Callable
from injector import inject
from server.LoggerFactory import LoggerFactory
from server.connection import ConnectionManager, TelnetConnection
from server.protocol import Message
from server.session import SessionHandler


class MessageBus:
    """
    Central message routing system.
    Handles sending messages to players, rooms, areas, and broadcasts.
    """

    @inject
    def __init__(self, connection_manager: ConnectionManager, session_handler: SessionHandler):
        self.__name__ = "MessageBus"
        self.logger = LoggerFactory.get_logger(self.__name__)
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
                self.logger.debug(f"Successfully sent message to player {player_id}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to send message to player {player_id}: {e}", exc_info=True)
                return False
        else:
            self.logger.warning(f"No active connection found for player {player_id}")
        return False

    async def send_to_room(self, room_id: str, message: Message, exclude_player_ids: Optional[List[str]] = None) -> int:
        """
        Send a message to all players in a room.
        NOTE: Consider using RoomService.send_to_room() for game logic.
        This method provides basic room broadcasting functionality.
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
        connection = self.connection_manager.get_connection_by_player(player_id)
        if connection and isinstance(connection, TelnetConnection):
            try:
                await connection.send_prompt(health, mana, movement)
                return True
            except Exception:
                return False
        return False

    async def send_to_outdoor_players(self, message: Message, is_outdoor_check: Callable[[str], bool]) -> int:
        """
        Send a message to all players who are currently outdoors.

        Args:
            message: The message to send
            is_outdoor_check: Function that takes a player_id and returns True if they are outdoors

        Returns:
            Count of players who received the message
        """
        count = 0
        sessions = self.session_handler.get_playing_sessions()
        for session in sessions:
            self.logger.debug(f"Checking player {session.character_id} for outdoor status")
            if session.player_id and is_outdoor_check(session.character_id):
                self.logger.debug(f"Sending message to player {session.player_id} (character {session.character_id}): {message}")
                if await self.send_to_player(session.player_id, message):
                    count += 1

        return count

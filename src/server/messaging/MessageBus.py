from typing import List, Optional
from injector import inject

from area.Area import Area
from area.Room import Room
from player.Character import Character
from server.LoggerFactory import LoggerFactory
from server.connection.ConnectionManager import ConnectionManager
from server.connection.TelnetConnection import TelnetConnection
from server.protocol.Message import Message, MessageType
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus


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

    @staticmethod
    def text_to_message(text: str) -> Message:
        return Message(MessageType.GAME, data={"text": text})

    async def send_to_character(self, player_id: str, message: Message) -> bool:
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
        exclude = exclude_player_ids or []
        count = 0
        sessions = self.session_handler.get_playing_sessions()

        for session in sessions:
            if session.player_id in exclude:
                continue

            if session.character.room_id == room_id:
                await self.send_to_character(session.player_id, message)
                count += 1

        return count

    async def send_to_area(self, area_id: str, message: Message) -> int:
        count = 0
        sessions = self.session_handler.get_playing_sessions()

        for session in sessions:
            if session.character.area_id == area_id:
                await self.send_to_character(session.player_id, message)
                count += 1

        return count

    async def send_prompt(self, player_id: str, character: Character, area: Area, room: Room) -> bool:
        connection = self.connection_manager.get_connection_by_player(player_id)
        if connection and isinstance(connection, TelnetConnection):
            try:
                await connection.send_message(character.prompt_format.render_prompt(SessionStatus.PLAYING, character, room, area))
                return True
            except Exception as e:
                self.logger.error(f"Failed to send prompt to player {player_id}: {e}", exc_info=True)
                return False
        return False

    async def broadcast(self, message: Message, exclude_player_ids: Optional[List[str]] = None) -> int:
        exclude = exclude_player_ids or []
        count = 0
        sessions = self.session_handler.get_active_sessions()
        for session in sessions:
            if session.player_id and session.player_id not in exclude:
                if await self.send_to_character(session.player_id, message):
                    count += 1

        return count

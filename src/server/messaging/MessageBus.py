from typing import List, Optional
from injector import inject

from area.Area import Area
from area.Room import Room
from util.GenericUtil import GenericUtil
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
    Handles sending messages to characters, rooms, areas, and broadcasts.
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

    async def send_to_character(self, character_id: str, message: Message) -> bool:
        connection = self.connection_manager.get_connection_by_character(character_id)
        if connection and not connection.is_closed():
            try:
                session = self.session_handler.get_session_by_character(character_id)
                if (session is not None and message.type == MessageType.GAME
                        and isinstance(message.data, dict) and not session.metadata.get("paging_active", False)):
                    text = str(message.data.get("text", "") or "")
                    scroll_lines = 0
                    if session.character is not None:
                        scroll_lines = GenericUtil.to_int(
                            (session.character.context or {}).get("scroll_lines", 0), 0
                        )

                    if text and scroll_lines > 0:
                        pages = self._split_into_pages(text, scroll_lines)
                        if len(pages) > 1:
                            session.metadata["paging_active"] = True
                            session.metadata["paging_queue"] = pages[1:]
                            message = self.text_to_message(pages[0] + "\r\n[Hit Enter to continue]\r\n")

                await connection.send_message(message)
                self._record_message_spacing(session, message)
                self.logger.debug(f"Successfully sent message to character {character_id}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to send message to character {character_id}: {e}", exc_info=True)
                return False
        else:
            self.logger.warning(f"No active connection found for character {character_id}")
        return False

    async def send_to_room(self, message: Message, in_room: List[Character]) -> None:
        for character in in_room:
            await self.send_to_character(character.id, message)

    async def send_to_area(self, area_id: str, message: Message) -> int:
        count = 0
        sessions = self.session_handler.get_playing_sessions()

        for session in sessions:
            if session.character.area_id == area_id:
                await self.send_to_character(session.character.id, message)
                count += 1

        return count

    async def send_prompt(self, character: Character, area: Area, room: Room) -> bool:
        session = self.session_handler.get_session_by_character(character.id)
        if session and session.metadata.get("paging_active", False):
            return True

        comm_raw = GenericUtil.to_int(getattr(getattr(character, "status_flags", None), "comm", 0), 0)
        if comm_raw > 0 and (comm_raw & 8192) == 0:  # COMM_PROMPT
            return True

        connection = self.connection_manager.get_connection_by_character(character.id)
        if connection and isinstance(connection, TelnetConnection):
            try:
                message = character.prompt_format.render_prompt(SessionStatus.PLAYING, character, room, area)
                if isinstance(message.data, dict):
                    text = str(message.data.get("text", "") or "")
                    message.data["text"] = "\r\n" + text.lstrip("\r\n")
                await connection.send_message(message)
                self._record_message_spacing(session, message)
                return True
            except Exception as e:
                self.logger.error(f"Failed to send prompt to character {character.id}: {e}", exc_info=True)
                return False
        return False

    async def broadcast(self, message: Message, exclude_character_ids: Optional[List[str]] = None) -> int:
        exclude = exclude_character_ids or []
        count = 0
        sessions = self.session_handler.get_active_sessions()
        for session in sessions:
            if session.character and session.character.id not in exclude:
                if await self.send_to_character(session.character.id, message):
                    count += 1

        return count

    @staticmethod
    def _split_into_pages(text: str, max_lines: int) -> list[str]:
        if max_lines <= 0:
            return [text]
        lines = text.splitlines(keepends=True)
        if not lines:
            return [text]
        return ["".join(lines[i:i + max_lines]) for i in range(0, len(lines), max_lines)]

    @staticmethod
    def _record_message_spacing(session, message: Message) -> None:
        if session is None:
            return
        session.metadata["last_trailing_breaks"] = MessageBus._message_trailing_breaks(message)

    @staticmethod
    def _last_trailing_breaks(session) -> int:
        if session is None:
            return 0
        return GenericUtil.to_int(session.metadata.get("last_trailing_breaks", 0), 0)

    @staticmethod
    def _message_trailing_breaks(message: Message) -> int:
        text = ""
        if isinstance(getattr(message, "data", None), dict):
            text = str(message.data.get("text", "") or "")
        if not text.endswith("\r\n"):
            text += "\r\n"

        count = 0
        idx = len(text)
        while idx > 0:
            if text[max(0, idx - 2):idx] == "\r\n":
                count += 1
                idx -= 2
                continue
            if text[idx - 1] in ("\r", "\n"):
                count += 1
                idx -= 1
                continue
            break
        return count

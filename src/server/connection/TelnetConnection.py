from typing import Optional
from asyncio import StreamReader, StreamWriter
from server.connection.Connection import Connection
from server.protocol.Message import Message, MessageType
from server.protocol.TelnetProtocol import TelnetProtocol
from server.LoggerFactory import LoggerFactory


class TelnetConnection(Connection):
    def __init__(self, reader: StreamReader, writer: StreamWriter, ansi_enabled: bool = False):
        super().__init__(reader, writer)
        self.logger = LoggerFactory.get_logger(__name__)
        self.protocol = TelnetProtocol(ansi_enabled=ansi_enabled)
        self.ansi_enabled = ansi_enabled

    async def send_message(self, message: Message) -> None:
        if self.is_closed():
            return

        try:
            data = self.protocol.encode_message(message)
            self.writer.write(data)
            await self.writer.drain()
        except Exception as e:
            self._closed = True
            self.logger.error(f"Error sending message: {e}")
            raise

    async def receive_message(self) -> Optional[Message]:
        if self.is_closed():
            return None

        try:
            if self.reader.at_eof():
                self._closed = True
                return None

            data = await self.reader.readline()
            if not data:
                self._closed = True
                return None

            message = self.protocol.decode_input(data)
            message.session_id = self.session_id
            return message
        except Exception as e:
            self._closed = True
            self.logger.error(f"Error reading message: {e}")
            return None

    async def close(self) -> None:
        if self._closed:
            return

        self._closed = True
        try:
            if not self.writer.is_closing():
                self.writer.close()
                await self.writer.wait_closed()
        except Exception as e:
            self.logger.error(f"Error closing connection: {e}")

    def set_ansi_enabled(self, enabled: bool) -> None:
        self.ansi_enabled = enabled
        self.protocol.ansi_enabled = enabled

    async def send_text(self, text: str, message_type: MessageType = MessageType.GAME) -> None:
        message = Message(type=message_type, data={'text': text})
        await self.send_message(message)

from typing import Optional
from asyncio import StreamReader, StreamWriter
from .Connection import Connection
from server.protocol import Message, MessageType, TelnetProtocol


class TelnetConnection(Connection):
    """
    Telnet-specific connection implementation.
    Handles telnet protocol negotiation and text-based communication.
    """

    def __init__(self, reader: StreamReader, writer: StreamWriter, ansi_enabled: bool = False):
        super().__init__(reader, writer)
        self.protocol = TelnetProtocol(ansi_enabled=ansi_enabled)
        self.ansi_enabled = ansi_enabled

    async def send_message(self, message: Message) -> None:
        """Send a message to the telnet client"""
        if self.is_closed():
            return

        try:
            data = self.protocol.encode_message(message)
            self.writer.write(data)
            await self.writer.drain()
        except Exception as e:
            # Connection error - mark as closed
            self._closed = True
            raise

    async def receive_message(self) -> Optional[Message]:
        """Receive a message from the telnet client"""
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
            # Connection error
            self._closed = True
            return None

    async def close(self) -> None:
        """Close the telnet connection"""
        if self._closed:
            return

        self._closed = True
        try:
            if not self.writer.is_closing():
                self.writer.close()
                await self.writer.wait_closed()
        except Exception:
            pass

    def set_ansi_enabled(self, enabled: bool) -> None:
        """Enable or disable ANSI color support"""
        self.ansi_enabled = enabled
        self.protocol.ansi_enabled = enabled

    async def send_prompt(self, health: int, mana: int, movement: int) -> None:
        """Send a game prompt"""
        prompt = self.protocol.create_prompt(health, mana, movement)
        await self.send_message(prompt)

    async def send_text(self, text: str, message_type: MessageType = MessageType.SYSTEM) -> None:
        """Convenience method to send plain text"""
        message = Message(type=message_type, data={'text': text})
        await self.send_message(message)

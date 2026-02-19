from abc import ABC, abstractmethod
from typing import Optional
from asyncio import StreamReader, StreamWriter
from server.protocol import Message
import uuid


class Connection(ABC):
    """
    Abstract base class for client connections.
    Decouples Player/Character from transport layer.
    """

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.session_id = str(uuid.uuid4())
        self.reader = reader
        self.writer = writer
        self._closed = False

    @abstractmethod
    async def send_message(self, message: Message) -> None:
        """Send a message to the client"""
        pass

    @abstractmethod
    async def receive_message(self) -> Optional[Message]:
        """Receive a message from the client"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the connection"""
        pass

    def is_closed(self) -> bool:
        """Check if connection is closed"""
        return self._closed or self.writer.is_closing()

    def get_peer_info(self) -> tuple:
        """Get client address information"""
        try:
            return self.writer.get_extra_info('peername')
        except Exception:
            return ('unknown', 0)

import asyncio
import threading
from abc import ABC, abstractmethod
from typing import Optional
from asyncio import StreamReader, StreamWriter
from server.protocol.Message import Message

import uuid


class Connection(ABC):
    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.session_id = str(uuid.uuid4())
        self.reader = reader
        self.writer = writer
        self._closed = False
        self.owner_thread_id = threading.get_ident()
        try:
            self.owner_loop = asyncio.get_running_loop()
        except RuntimeError:
            self.owner_loop = None

    @abstractmethod
    async def send_message(self, message: Message) -> None:
        pass

    @abstractmethod
    async def receive_message(self) -> Optional[Message]:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    def is_closed(self) -> bool:
        return self._closed or self.writer.is_closing()

    def get_peer_info(self) -> tuple:
        try:
            return self.writer.get_extra_info('peername')
        except Exception:
            return ('unknown', 0)

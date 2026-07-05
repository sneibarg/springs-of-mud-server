import asyncio
import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from server.connection.ConnectionManager import ConnectionManager
from server.messaging.MessageBus import MessageBus
from server.protocol.Message import Message
from server.protocol.MessageTypes import MessageType
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus


class TestMessageBusBroadcast(unittest.TestCase):
    def setUp(self):
        self.connection_manager = ConnectionManager()
        self.session_handler = SessionHandler()
        self.message_bus = MessageBus(self.connection_manager, self.session_handler)

    def test_broadcast_only_targets_playing_sessions(self):
        async def run_test():
            connected = self.session_handler.create_session("connected-session")
            connected.character = SimpleNamespace(id="connected-character", area_id="area-1", context={})
            connected.status = SessionStatus.CONNECTED

            playing = self.session_handler.create_session("playing-session")
            playing.character = SimpleNamespace(id="playing-character", area_id="area-1", context={})
            playing.status = SessionStatus.PLAYING

            connection = AsyncMock()
            connection.session_id = "playing-session"
            connection.is_closed = Mock(return_value=False)
            self.connection_manager.add_connection(connection)
            self.connection_manager.bind_character("playing-character", "playing-session")

            message = Message(type=MessageType.GAME, data={"text": "The sky is getting cloudy.\n\r"})

            count = await self.message_bus.broadcast(message)

            self.assertEqual(count, 1)
            connection.send_message.assert_awaited_once_with(message)

        asyncio.run(run_test())

    def test_send_to_character_mirrors_snoop_output_with_target_prompt(self):
        async def run_test():
            target = self.session_handler.create_session("target-session")
            target.character = SimpleNamespace(id="target-character", name="Target", area_id="area-1", context={})
            target.status = SessionStatus.PLAYING
            target.metadata["snoop_by_session_id"] = "snooper-session"

            snooper = self.session_handler.create_session("snooper-session")
            snooper.character = SimpleNamespace(id="snooper-character", name="Snooper", area_id="area-1", context={})
            snooper.status = SessionStatus.PLAYING

            target_connection = AsyncMock()
            target_connection.session_id = "target-session"
            target_connection.is_closed = Mock(return_value=False)
            self.connection_manager.add_connection(target_connection)
            self.connection_manager.bind_character("target-character", "target-session")

            snooper_connection = AsyncMock()
            snooper_connection.session_id = "snooper-session"
            snooper_connection.is_closed = Mock(return_value=False)
            self.connection_manager.add_connection(snooper_connection)

            message = Message(type=MessageType.GAME, data={"text": "Hello.\r\n"})

            self.assertTrue(await self.message_bus.send_to_character("target-character", message))

            target_connection.send_message.assert_awaited_once_with(message)
            snoop_message = snooper_connection.send_message.await_args.args[0]
            self.assertEqual(MessageType.GAME, snoop_message.type)
            self.assertEqual("Target> Hello.\r\n", snoop_message.data["text"])

        asyncio.run(run_test())

    def test_mirror_snoop_input_uses_percent_prompt(self):
        async def run_test():
            target = self.session_handler.create_session("target-session")
            target.character = SimpleNamespace(id="target-character", name="Target", area_id="area-1", context={})
            target.status = SessionStatus.PLAYING
            target.metadata["snoop_by_session_id"] = "snooper-session"

            snooper = self.session_handler.create_session("snooper-session")
            snooper.character = SimpleNamespace(id="snooper-character", name="Snooper", area_id="area-1", context={})
            snooper.status = SessionStatus.PLAYING

            snooper_connection = AsyncMock()
            snooper_connection.session_id = "snooper-session"
            snooper_connection.is_closed = Mock(return_value=False)
            self.connection_manager.add_connection(snooper_connection)

            await self.message_bus.mirror_snoop_input(target, "look")

            snoop_message = snooper_connection.send_message.await_args.args[0]
            self.assertEqual(MessageType.GAME, snoop_message.type)
            self.assertEqual("% look\r\n", snoop_message.data["text"])

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()

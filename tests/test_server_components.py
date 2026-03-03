import unittest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import asyncio
from server.connection.Connection import Connection
from server.connection.TelnetConnection import TelnetConnection
from server.connection.ConnectionManager import ConnectionManager
from server.messaging.MessageBus import MessageBus
from server.messaging.MessageFormatter import MessageFormatter
from server.protocol.Message import Message
from server.protocol.MessageTypes import MessageType
from server.session.SessionState import SessionState
from server.session.SessionState import SessionPhase
from server.session.SessionHandler import SessionHandler


class TestConnection(unittest.TestCase):
    """Test Connection abstract base class"""

    def test_connection_initialization(self):
        """Test Connection initialization"""
        mock_reader = Mock()
        mock_writer = Mock()

        class TestConnection(Connection):
            async def send_message(self, message):
                pass

            async def receive_message(self):
                pass

            async def close(self):
                pass

        conn = TestConnection(mock_reader, mock_writer)
        self.assertIsNotNone(conn.session_id)
        self.assertEqual(conn.reader, mock_reader)
        self.assertEqual(conn.writer, mock_writer)
        self.assertFalse(conn._closed)

    def test_is_closed(self):
        """Test is_closed method"""

        class TestConnection(Connection):
            async def send_message(self, message):
                pass

            async def receive_message(self):
                pass

            async def close(self):
                pass

        mock_writer = Mock()
        mock_writer.is_closing.return_value = False
        conn = TestConnection(Mock(), mock_writer)

        self.assertFalse(conn.is_closed())

        conn._closed = True
        self.assertTrue(conn.is_closed())

    def test_get_peer_info(self):
        """Test getting peer info"""

        class TestConnection(Connection):
            async def send_message(self, message):
                pass

            async def receive_message(self):
                pass

            async def close(self):
                pass

        mock_writer = Mock()
        mock_writer.get_extra_info.return_value = ('127.0.0.1', 12345)

        conn = TestConnection(Mock(), mock_writer)
        peer_info = conn.get_peer_info()

        self.assertEqual(peer_info, ('127.0.0.1', 12345))

    def test_get_peer_info_error(self):
        """Test getting peer info handles errors"""

        class TestConnection(Connection):
            async def send_message(self, message):
                pass

            async def receive_message(self):
                pass

            async def close(self):
                pass

        mock_writer = Mock()
        mock_writer.get_extra_info.side_effect = Exception('Error')

        conn = TestConnection(Mock(), mock_writer)
        peer_info = conn.get_peer_info()

        self.assertEqual(peer_info, ('unknown', 0))


class TestTelnetConnection(unittest.TestCase):
    """Test TelnetConnection"""

    def setUp(self):
        self.mock_reader = AsyncMock()
        # at_eof() is a synchronous method, not async
        self.mock_reader.at_eof = Mock(return_value=False)
        self.mock_writer = MagicMock()
        # write is synchronous, drain is async
        self.mock_writer.write = Mock()
        self.mock_writer.drain = AsyncMock()
        self.mock_writer.is_closing.return_value = False
        self.connection = TelnetConnection(self.mock_reader, self.mock_writer)

    def test_initialization(self):
        """Test TelnetConnection initialization"""
        self.assertIsNotNone(self.connection.protocol)
        self.assertFalse(self.connection.ansi_enabled)

    def test_initialization_with_ansi(self):
        """Test TelnetConnection initialization with ANSI enabled"""
        conn = TelnetConnection(self.mock_reader, self.mock_writer, ansi_enabled=True)
        self.assertTrue(conn.ansi_enabled)

    def test_set_ansi_enabled(self):
        """Test setting ANSI enabled"""
        self.connection.set_ansi_enabled(True)
        self.assertTrue(self.connection.ansi_enabled)
        self.assertTrue(self.connection.protocol.ansi_enabled)

    async def test_send_message(self):
        """Test sending message"""
        message = Message(type=MessageType.SYSTEM, data={'text': 'test'})

        await self.connection.send_message(message)
        self.mock_writer.write.assert_called_once()
        self.mock_writer.drain.assert_called_once()

    async def test_send_message_when_closed(self):
        """Test sending message when connection is closed"""
        self.connection._closed = True
        message = Message(type=MessageType.SYSTEM, data={'text': 'test'})

        await self.connection.send_message(message)
        self.mock_writer.write.assert_not_called()

    async def test_receive_message_at_eof(self):
        """Test receiving message at EOF"""
        self.mock_reader.at_eof.return_value = True

        message = await self.connection.receive_message()
        self.assertIsNone(message)
        self.assertTrue(self.connection._closed)

    async def test_close(self):
        """Test closing connection"""
        self.mock_writer.wait_closed = AsyncMock()
        await self.connection.close()
        self.assertTrue(self.connection._closed)
        self.mock_writer.close.assert_called_once()

    async def test_receive_message(self):
        """Test receiving message"""
        self.mock_reader.readline.return_value = b'test message\r\n'

        message = await self.connection.receive_message()
        self.assertIsNotNone(message)
        self.assertEqual(message.session_id, self.connection.session_id)

    def test_run_async_tests(self):
        """Run all async tests"""
        asyncio.run(self.test_send_message())
        self.setUp()
        asyncio.run(self.test_send_message_when_closed())
        self.setUp()
        asyncio.run(self.test_receive_message())
        self.setUp()
        asyncio.run(self.test_receive_message_at_eof())
        self.setUp()
        asyncio.run(self.test_close())


class TestConnectionManager(unittest.TestCase):
    """Test ConnectionManager"""

    def setUp(self):
        self.manager = ConnectionManager()

    def test_initialization(self):
        """Test ConnectionManager initialization"""
        self.assertEqual(len(self.manager._connections), 0)
        self.assertEqual(len(self.manager._player_sessions), 0)

    def test_add_connection(self):
        """Test adding connection"""
        mock_connection = Mock()
        mock_connection.session_id = 'session_001'

        self.manager.add_connection(mock_connection)
        self.assertIn('session_001', self.manager._connections)

    def test_get_connection(self):
        """Test getting connection by session ID"""
        mock_connection = Mock()
        mock_connection.session_id = 'session_001'

        self.manager.add_connection(mock_connection)
        result = self.manager.get_connection('session_001')

        self.assertEqual(result, mock_connection)

    def test_get_connection_not_found(self):
        """Test getting nonexistent connection"""
        result = self.manager.get_connection('nonexistent')
        self.assertIsNone(result)

    def test_remove_connection(self):
        """Test removing connection"""
        mock_connection = Mock()
        mock_connection.session_id = 'session_001'

        self.manager.add_connection(mock_connection)
        self.assertIn('session_001', self.manager._connections)

        self.manager.remove_connection('session_001')
        self.assertNotIn('session_001', self.manager._connections)

    def test_bind_player(self):
        """Test binding player to connection"""
        mock_connection = Mock()
        mock_connection.session_id = 'session_001'

        self.manager.add_connection(mock_connection)
        self.manager.bind_player('player_001', 'session_001')

        self.assertIn('player_001', self.manager._player_sessions)
        self.assertEqual(self.manager._player_sessions['player_001'], 'session_001')

    def test_get_connection_by_player(self):
        """Test getting connection by player ID"""
        mock_connection = Mock()
        mock_connection.session_id = 'session_001'

        self.manager.add_connection(mock_connection)
        self.manager.bind_player('player_001', 'session_001')

        result = self.manager.get_connection_by_player('player_001')
        self.assertEqual(result, mock_connection)

    def test_unbind_player(self):
        """Test unbinding player"""
        mock_connection = Mock()
        mock_connection.session_id = 'session_001'

        self.manager.add_connection(mock_connection)
        self.manager.bind_player('player_001', 'session_001')

        self.manager.unbind_player('player_001')
        self.assertNotIn('player_001', self.manager._player_sessions)

    def test_get_all_connections(self):
        """Test getting all connections"""
        conn1 = Mock()
        conn1.session_id = 'session_001'
        conn2 = Mock()
        conn2.session_id = 'session_002'

        self.manager.add_connection(conn1)
        self.manager.add_connection(conn2)

        all_conns = self.manager.get_all_connections()
        self.assertEqual(len(all_conns), 2)


class TestMessageBus(unittest.TestCase):
    """Test MessageBus"""

    def setUp(self):
        self.connection_manager = ConnectionManager()
        self.session_handler = SessionHandler()
        self.message_bus = MessageBus(self.connection_manager, self.session_handler)

    async def test_send_to_player_success(self):
        """Test sending message to player successfully"""
        mock_connection = AsyncMock()
        mock_connection.is_closed = Mock(return_value=False)
        mock_connection.session_id = 'session_001'
        mock_connection.send_message = AsyncMock()

        self.connection_manager.add_connection(mock_connection)
        self.connection_manager.bind_player('player_001', 'session_001')

        message = Message(type=MessageType.SYSTEM, data={'text': 'test'})
        result = await self.message_bus.send_to_player('player_001', message)

        self.assertTrue(result)
        mock_connection.send_message.assert_called_once_with(message)

    async def test_send_to_player_not_found(self):
        """Test sending message to nonexistent player"""
        message = Message(type=MessageType.SYSTEM, data={'text': 'test'})
        result = await self.message_bus.send_to_player('nonexistent', message)

        self.assertFalse(result)

    async def test_send_to_session_success(self):
        """Test sending message to session"""
        mock_connection = AsyncMock()
        mock_connection.is_closed = Mock(return_value=False)
        mock_connection.session_id = 'session_001'

        self.connection_manager.add_connection(mock_connection)

        message = Message(type=MessageType.SYSTEM, data={'text': 'test'})
        result = await self.message_bus.send_to_session('session_001', message)

        self.assertTrue(result)

    async def test_broadcast(self):
        """Test broadcasting message"""
        # Create sessions
        session1 = self.session_handler.create_session('session_001')
        session1.player_id = 'player_001'
        session1.phase = SessionPhase.PLAYING

        session2 = self.session_handler.create_session('session_002')
        session2.player_id = 'player_002'
        session2.phase = SessionPhase.PLAYING

        # Create connections
        conn1 = AsyncMock()
        conn1.is_closed = Mock(return_value=False)
        conn1.session_id = 'session_001'

        conn2 = AsyncMock()
        conn2.is_closed = Mock(return_value=False)
        conn2.session_id = 'session_002'

        self.connection_manager.add_connection(conn1)
        self.connection_manager.bind_player('player_001', 'session_001')

        self.connection_manager.add_connection(conn2)
        self.connection_manager.bind_player('player_002', 'session_002')

        message = Message(type=MessageType.SYSTEM, data={'text': 'broadcast'})
        count = await self.message_bus.broadcast(message)

        self.assertEqual(count, 2)

    def test_run_async_tests(self):
        """Run all async tests"""
        asyncio.run(self.test_send_to_player_success())
        self.setUp()  # Reset state
        asyncio.run(self.test_send_to_player_not_found())
        self.setUp()  # Reset state
        asyncio.run(self.test_send_to_session_success())
        self.setUp()  # Reset state
        asyncio.run(self.test_broadcast())


class TestSessionState(unittest.TestCase):
    """Test SessionState"""

    def test_initialization(self):
        """Test SessionState initialization"""
        session = SessionState(session_id='session_001')
        self.assertEqual(session.session_id, 'session_001')
        self.assertEqual(session.phase, SessionPhase.CONNECTED)
        self.assertIsNone(session.player_id)
        self.assertIsNone(session.character_id)
        self.assertEqual(session.auth_attempts, 0)

    def test_can_authenticate(self):
        """Test can_authenticate method"""
        session = SessionState(session_id='session_001')
        self.assertTrue(session.can_authenticate())

        session.auth_attempts = 3
        self.assertFalse(session.can_authenticate())

    def test_is_playing(self):
        """Test is_playing method"""
        session = SessionState(session_id='session_001')
        self.assertFalse(session.is_playing())

        session.phase = SessionPhase.PLAYING
        self.assertTrue(session.is_playing())

    def test_update_activity(self):
        """Test update_activity method"""
        session = SessionState(session_id='session_001')
        old_activity = session.last_activity

        import time
        time.sleep(0.01)
        session.update_activity()

        self.assertGreater(session.last_activity, old_activity)


class TestSessionHandler(unittest.TestCase):
    """Test SessionHandler"""

    def setUp(self):
        self.handler = SessionHandler()

    def test_create_session(self):
        """Test creating session"""
        session = self.handler.create_session('session_001')
        self.assertEqual(session.session_id, 'session_001')
        self.assertIn('session_001', self.handler._sessions)

    def test_get_session(self):
        """Test getting session"""
        session = self.handler.create_session('session_001')
        result = self.handler.get_session('session_001')
        self.assertEqual(result, session)

    def test_get_session_not_found(self):
        """Test getting nonexistent session"""
        result = self.handler.get_session('nonexistent')
        self.assertIsNone(result)

    def test_remove_session(self):
        """Test removing session"""
        self.handler.create_session('session_001')
        self.assertIn('session_001', self.handler._sessions)

        self.handler.remove_session('session_001')
        self.assertNotIn('session_001', self.handler._sessions)

    def test_get_active_sessions(self):
        """Test getting active sessions"""
        session1 = self.handler.create_session('session_001')
        session2 = self.handler.create_session('session_002')

        active = self.handler.get_active_sessions()
        self.assertEqual(len(active), 2)

    def test_get_playing_sessions(self):
        """Test getting playing sessions"""
        session1 = self.handler.create_session('session_001')
        session1.phase = SessionPhase.PLAYING

        session2 = self.handler.create_session('session_002')
        session2.phase = SessionPhase.CONNECTED

        playing = self.handler.get_playing_sessions()
        self.assertEqual(len(playing), 1)
        self.assertEqual(playing[0].session_id, 'session_001')


class TestMessageFormatter(unittest.TestCase):
    """Test MessageFormatter"""

    @unittest.skip("format_room_description moved to RoomService")
    def test_format_room_description(self):
        """Test formatting room description"""
        # Moved to RoomService in area package
        pass

    def test_format_error(self):
        """Test formatting error message"""
        message = MessageFormatter.format_error('Error occurred')
        self.assertEqual(message.type, MessageType.ERROR)
        self.assertEqual(message.data['text'], 'ERROR: Error occurred\r\n')

    @unittest.skip("There is no MessageFormatter.format_info")
    def test_format_info(self):
        """Test formatting info message"""
        message = MessageFormatter.format_info('Info message')
        self.assertEqual(message.type, MessageType.INFO)
        self.assertEqual(message.data['text'], 'Info message')


if __name__ == '__main__':
    unittest.main()

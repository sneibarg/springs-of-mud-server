import unittest
from unittest.mock import Mock, AsyncMock, patch, MagicMock, call, ANY
import asyncio

from player import PlayerService
from server.MudServer import MudServer


class TestMudServer(unittest.TestCase):
    """Test MudServer"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_config = {
            'mudserver': {
                'host': 'localhost',
                'port': 4000,
                'modulith_host': 'localhost',
                'modulith_port': 9080,
                'api_version': '/api/v1',
                'services': {
                    'endpoints': {
                        'commands_endpoint': '/commands',
                        'players_endpoint': '/players',
                        'characters_endpoint': '/characters',
                        'areas_endpoint': '/areas',
                        'rooms_endpoint': '/rooms',
                        'items_endpoint': '/items',
                        'mobiles_endpoint': '/mobiles',
                        'game_data_endpoint': '/game'
                    }
                },
                'playerone': {
                    'accountId': 'test_account_123'
                }
            }
        }
        self.mock_logger_factory = Mock()
        self.mock_logger = Mock()
        self.mock_logger_factory.get_logger.return_value = self.mock_logger

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    def test_initialization(self, mock_injector_class, mock_util, mock_registry, mock_cmd_handler,
                            mock_cmd_service, mock_mobile_service, mock_item_service,
                            mock_area_service, mock_room_service, mock_player_service_class,
                            mock_connection_handler_class, mock_game_service_class):
        """Test MudServer initialization"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: Mock(),
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            self.assertEqual(server.host, 'localhost')
            self.assertEqual(server.port, 4000)
            self.assertIsNotNone(server.injector)
            self.assertIsNotNone(server.connection_handler)
            self.assertIsNotNone(server.player_service)

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    def test_configure_player_data(self, mock_injector_class, mock_util, mock_registry,
                                   mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                   mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                   mock_connection_handler_class, mock_game_service_class):
        """Test _configure_player_data method"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = ['account1', 'account2']
        mock_player_service.get_characters.return_value = ['char1', 'char2']
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: Mock(),
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            self.assertEqual(server.account_list, ['account1', 'account2'])
            self.assertEqual(server.character_list, ['char1', 'char2'])

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    def test_load_player_one(self, mock_injector_class, mock_util, mock_registry, mock_cmd_handler,
                             mock_cmd_service, mock_mobile_service, mock_item_service,
                             mock_area_service, mock_room_service, mock_player_service_class,
                             mock_connection_handler_class, mock_game_service_class):
        """Test _load_player_one method"""
        expected_account = {'id': 'test_account_123', 'name': 'TestPlayer'}
        mock_util.camel_to_snake_case.return_value = expected_account

        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = expected_account

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: Mock(),
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        mock_player_instance = Mock()

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = mock_player_instance

            server = MudServer(self.mock_config, self.mock_logger_factory)

            self.assertEqual(server.player_one, mock_player_instance)
            mock_player_service.get_account_by_id.assert_called_once_with('test_account_123')
            mock_player.from_json.assert_called_once_with(expected_account)

    @patch('server.MudServer.threading.Thread')
    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    @patch('asyncio.start_server')
    async def test_start(self, mock_start_server, mock_injector_class, mock_util, mock_registry,
                         mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                         mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                         mock_connection_handler_class, mock_game_service_class, mock_thread_class):
        """Test start method"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_game_service = Mock()
        mock_game_service.start = AsyncMock()

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: Mock(),
            mock_game_service_class: mock_game_service
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        mock_thread = Mock()
        mock_thread_class.return_value = mock_thread

        mock_server = AsyncMock()
        mock_server.serve_forever = AsyncMock()
        mock_start_server.return_value = mock_server

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            # Run start in background and cancel after verification
            task = asyncio.create_task(server.start())
            await asyncio.sleep(0.01)  # Let it start
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

            # Verify thread was created and started
            mock_thread_class.assert_called_once_with(
                target=server._run_game_loop, daemon=True, name="GameLoop"
            )
            mock_thread.start.assert_called_once()

            mock_start_server.assert_called_once_with(
                server.handle_client, 'localhost', 4000
            )
            self.mock_logger.info.assert_called()

    @patch('server.MudServer.asyncio.new_event_loop')
    @patch('server.MudServer.asyncio.set_event_loop')
    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    def test_run_game_loop(self, mock_injector_class, mock_util, mock_registry,
                           mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                           mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                           mock_connection_handler_class, mock_game_service_class,
                           mock_set_event_loop, mock_new_event_loop):
        """Test _run_game_loop method"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_game_service = Mock()
        mock_game_service.start = AsyncMock()

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: Mock(),
            mock_game_service_class: mock_game_service
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        mock_loop = Mock()
        mock_loop.run_until_complete = Mock()
        mock_loop.close = Mock()
        mock_new_event_loop.return_value = mock_loop

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            # Run the game loop
            server._run_game_loop()

            # Verify event loop was created and set
            mock_new_event_loop.assert_called_once()
            mock_set_event_loop.assert_called_once_with(mock_loop)

            # Verify game service start was called
            mock_loop.run_until_complete.assert_called_once_with(ANY)

            # Verify loop was closed
            mock_loop.close.assert_called_once()

    @patch('server.MudServer.asyncio.new_event_loop')
    @patch('server.MudServer.asyncio.set_event_loop')
    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    def test_run_game_loop_error_handling(self, mock_injector_class, mock_util, mock_registry,
                                          mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                          mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                          mock_connection_handler_class, mock_game_service_class,
                                          mock_set_event_loop, mock_new_event_loop):
        """Test _run_game_loop error handling"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_game_service = Mock()
        mock_game_service.start = AsyncMock()

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: Mock(),
            mock_game_service_class: mock_game_service
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        mock_loop = Mock()
        mock_loop.run_until_complete = Mock(side_effect=Exception("Test error"))
        mock_loop.close = Mock()
        mock_new_event_loop.return_value = mock_loop

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            # Run the game loop with error
            server._run_game_loop()

            # Verify error was logged
            self.mock_logger.error.assert_called()

            # Verify loop was still closed even after error
            mock_loop.close.assert_called_once()

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    async def test_handle_client_success(self, mock_injector_class, mock_util, mock_registry,
                                         mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                         mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                         mock_connection_handler_class, mock_game_service_class):
        """Test handle_client with successful connection"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_connection_handler = Mock()
        mock_connection_handler.handle_new_connection = AsyncMock()

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: mock_connection_handler,
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            mock_reader = AsyncMock()
            mock_writer = MagicMock()
            mock_writer.close = Mock()
            mock_writer.wait_closed = AsyncMock()

            await server.handle_client(mock_reader, mock_writer)

            mock_connection_handler.handle_new_connection.assert_called_once_with(
                mock_reader, mock_writer
            )

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    async def test_handle_client_cancelled_error(self, mock_injector_class, mock_util, mock_registry,
                                                 mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                                 mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                                 mock_connection_handler_class, mock_game_service_class):
        """Test handle_client with CancelledError"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_connection_handler = Mock()
        mock_connection_handler.handle_new_connection = AsyncMock(
            side_effect=asyncio.CancelledError()
        )

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: mock_connection_handler,
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            mock_reader = AsyncMock()
            mock_writer = MagicMock()
            mock_writer.close = Mock()
            mock_writer.wait_closed = AsyncMock()

            with self.assertRaises(asyncio.CancelledError):
                await server.handle_client(mock_reader, mock_writer)

            self.mock_logger.info.assert_called_with("Client connection cancelled")

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    async def test_handle_client_connection_reset(self, mock_injector_class, mock_util, mock_registry,
                                                  mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                                  mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                                  mock_connection_handler_class, mock_game_service_class):
        """Test handle_client with ConnectionResetError"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_connection_handler = Mock()
        mock_connection_handler.handle_new_connection = AsyncMock(
            side_effect=ConnectionResetError("Connection reset by peer")
        )

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: mock_connection_handler,
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            mock_reader = AsyncMock()
            mock_writer = MagicMock()
            mock_writer.close = Mock()
            mock_writer.wait_closed = AsyncMock()

            await server.handle_client(mock_reader, mock_writer)

            self.mock_logger.warning.assert_called()
            mock_writer.close.assert_called_once()
            mock_writer.wait_closed.assert_called_once()

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    async def test_handle_client_broken_pipe(self, mock_injector_class, mock_util, mock_registry,
                                             mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                             mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                             mock_connection_handler_class, mock_game_service_class):
        """Test handle_client with BrokenPipeError"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_connection_handler = Mock()
        mock_connection_handler.handle_new_connection = AsyncMock(
            side_effect=BrokenPipeError("Broken pipe")
        )

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: mock_connection_handler,
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            mock_reader = AsyncMock()
            mock_writer = MagicMock()
            mock_writer.close = Mock()
            mock_writer.wait_closed = AsyncMock()

            await server.handle_client(mock_reader, mock_writer)

            self.mock_logger.warning.assert_called()
            mock_writer.close.assert_called_once()

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    async def test_handle_client_os_error(self, mock_injector_class, mock_util, mock_registry,
                                          mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                          mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                          mock_connection_handler_class, mock_game_service_class):
        """Test handle_client with OSError"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_connection_handler = Mock()
        mock_connection_handler.handle_new_connection = AsyncMock(
            side_effect=OSError("Network error")
        )

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: mock_connection_handler,
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            mock_reader = AsyncMock()
            mock_writer = MagicMock()
            mock_writer.close = Mock()
            mock_writer.wait_closed = AsyncMock()

            await server.handle_client(mock_reader, mock_writer)

            self.mock_logger.error.assert_called()
            mock_writer.close.assert_called_once()

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    async def test_handle_client_unexpected_error(self, mock_injector_class, mock_util, mock_registry,
                                                  mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                                  mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                                  mock_connection_handler_class, mock_game_service_class):
        """Test handle_client with unexpected exception"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_connection_handler = Mock()
        mock_connection_handler.handle_new_connection = AsyncMock(
            side_effect=ValueError("Unexpected error")
        )

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: mock_connection_handler,
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            mock_reader = AsyncMock()
            mock_writer = MagicMock()
            mock_writer.close = Mock()
            mock_writer.wait_closed = AsyncMock()

            await server.handle_client(mock_reader, mock_writer)

            # Check that error was logged with "Unexpected error"
            error_calls = [call for call in self.mock_logger.error.call_args_list
                           if 'Unexpected error handling client' in str(call)]
            self.assertTrue(len(error_calls) > 0)
            mock_writer.close.assert_called_once()

    @patch('server.MudServer.GameService')
    @patch('server.MudServer.ConnectionHandler')
    @patch('server.MudServer.PlayerService')
    @patch('server.MudServer.RoomService')
    @patch('server.MudServer.AreaService')
    @patch('server.MudServer.ItemService')
    @patch('server.MudServer.MobileService')
    @patch('server.MudServer.CommandService')
    @patch('server.MudServer.CommandHandler')
    @patch('server.MudServer.RegistryService')
    @patch('server.MudServer.ServerUtil')
    @patch('server.MudServer.Injector')
    async def test_handle_client_close_error(self, mock_injector_class, mock_util, mock_registry,
                                             mock_cmd_handler, mock_cmd_service, mock_mobile_service,
                                             mock_item_service, mock_area_service, mock_room_service, mock_player_service_class,
                                             mock_connection_handler_class, mock_game_service_class):
        """Test handle_client when closing writer fails"""
        mock_util.camel_to_snake_case.return_value = {'id': 'test'}
        mock_player_service = Mock()
        mock_player_service.get_accounts.return_value = []
        mock_player_service.get_characters.return_value = []
        mock_player_service.get_account_by_id.return_value = {'id': 'test'}

        mock_connection_handler = Mock()
        mock_connection_handler.handle_new_connection = AsyncMock()

        mock_injector = Mock()
        mock_injector.binder.bind = Mock()
        mock_injector.get.side_effect = lambda cls: {
            mock_player_service_class: mock_player_service,
            mock_connection_handler_class: mock_connection_handler,
            mock_game_service_class: Mock()
        }.get(cls, Mock())
        mock_injector_class.return_value = mock_injector

        with patch('server.MudServer.Player') as mock_player:
            mock_player.from_json.return_value = Mock()

            server = MudServer(self.mock_config, self.mock_logger_factory)

            mock_reader = AsyncMock()
            mock_writer = MagicMock()
            mock_writer.close = Mock(side_effect=Exception("Close failed"))
            mock_writer.wait_closed = AsyncMock()

            await server.handle_client(mock_reader, mock_writer)

            self.mock_logger.debug.assert_called()

    def test_run_async_tests(self):
        """Run all async tests"""
        asyncio.run(self.test_start())
        self.setUp()
        asyncio.run(self.test_handle_client_success())
        self.setUp()
        asyncio.run(self.test_handle_client_cancelled_error())
        self.setUp()
        asyncio.run(self.test_handle_client_connection_reset())
        self.setUp()
        asyncio.run(self.test_handle_client_broken_pipe())
        self.setUp()
        asyncio.run(self.test_handle_client_os_error())
        self.setUp()
        asyncio.run(self.test_handle_client_unexpected_error())
        self.setUp()
        asyncio.run(self.test_handle_client_close_error())


if __name__ == '__main__':
    unittest.main()

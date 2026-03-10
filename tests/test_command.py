import unittest
from unittest.mock import Mock, MagicMock, patch
from command.CommandHandler import CommandHandler
from command.CommandService import (
    CommandService, get_class_obj, parse_args, get_args,
    handle_lambdas, lambda_mappings
)
from player.Player import Player
from player.Character import Character


class TestCommandHandler(unittest.TestCase):
    """Test CommandHandler"""

    def setUp(self):
        from command.CommandService import CommandService
        self.mock_command_service = Mock(spec=CommandService)
        self.mock_command_service.command_list = {
            'look': {
                'name': 'look',
                'shortcuts': 'l',
                'usage': None,
                'lambda': []
            },
            'say': {
                'name': 'say',
                'shortcuts': 's',
                'usage': 'lambda p: p.to_player("Say what?")',
                'lambda': []
            }
        }
        self.handler = CommandHandler(self.mock_command_service)

    def test_initialization(self):
        """Test CommandHandler initialization"""
        self.assertIsNotNone(self.handler.logger)
        self.assertIsNotNone(self.handler.command_list)

    def test_extract_parameters_full_command(self):
        """Test extracting parameters from full command"""
        cmd, params = self.handler.extract_parameters('look north')
        self.assertEqual(cmd['name'], 'look')
        self.assertEqual(params, 'north')

    def test_extract_parameters_shortcut(self):
        """Test extracting parameters from shortcut"""
        cmd, params = self.handler.extract_parameters('l')
        self.assertEqual(cmd['name'], 'look')
        self.assertEqual(params, '')

    def test_extract_parameters_with_multiple_params(self):
        """Test extracting multiple parameters"""
        cmd, params = self.handler.extract_parameters('say hello world')
        self.assertEqual(cmd['name'], 'say')
        self.assertEqual(params, 'hello world')

    def test_extract_parameters_invalid_command(self):
        """Test extracting parameters from invalid command"""
        cmd, params = self.handler.extract_parameters('invalid')
        self.assertIsNone(cmd)
        self.assertIsNone(params)

    def test_handle_command_with_usage(self):
        """Test handling command with usage function"""
        mock_player = Mock()
        mock_player.writer.return_value = Mock()

        self.handler.handle_command(mock_player, 'say')
        mock_player.set_usage.assert_called()

    def test_handle_command_invalid(self):
        """Test handling invalid command"""
        mock_player = Mock()
        mock_writer = Mock()
        mock_player.writer.return_value = mock_writer

        self.handler.handle_command(mock_player, 'invalidcmd')
        mock_writer.write.assert_called_with(b'Huh?\r\n')


class TestCommandService(unittest.TestCase):
    """Test CommandService"""

    def setUp(self):
        from server.ServiceConfig import ServiceConfig
        self.mock_injector = Mock()
        self.commands_endpoint = 'http://test.com/api/commands'
        self.mock_service_config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint=self.commands_endpoint,
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles"
        )

    @patch('command.CommandService.requests.get')
    def test_initialization_success(self, mock_get):
        """Test successful initialization"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'name': 'look', 'shortcuts': ['l'], 'lambda': []},
            {'name': 'say', 'shortcuts': ['s'], 'lambda': []}
        ]
        mock_get.return_value = mock_response

        service = CommandService(self.mock_service_config, self.mock_injector)
        self.assertEqual(len(service.command_list), 2)
        self.assertIn('look', service.command_list)
        self.assertIn('say', service.command_list)

    @patch('command.CommandService.requests.get')
    def test_initialization_failure(self, mock_get):
        """Test initialization failure"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            CommandService(self.mock_injector, self.commands_endpoint)

    @patch('command.CommandService.requests.get')
    def test_get_command_by_name(self, mock_get):
        """Test getting single command"""
        # First call for initialization
        init_response = Mock()
        init_response.status_code = 200
        init_response.json.return_value = []

        # Second call for fetching specific command
        fetch_response = Mock()
        fetch_response.status_code = 200
        fetch_response.json.return_value = {
            'id': 'cmd_001',
            'name': 'look'
        }

        mock_get.side_effect = [init_response, fetch_response]
        service = CommandService(self.mock_service_config, self.mock_injector)

        result = service.get_command_by_name('look')
        self.assertEqual(result['name'], 'look')

    @patch('command.CommandService.requests.get')
    def test_get_message(self, mock_get):
        """Test getting command message"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'name': 'look', 'message': 'You look around.', 'shortcuts': [], 'lambda': []}
        ]
        mock_get.return_value = mock_response

        service = CommandService(self.mock_service_config, self.mock_injector)
        message = service.get_message('look')
        self.assertEqual(message, 'You look around.')

    @patch('command.CommandService.requests.get')
    def test_call_lambda_with_null_json(self, mock_get):
        """Test call_lambda with nonexistent command sends Huh? message"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        service = CommandService(self.mock_service_config, self.mock_injector)
        mock_player = Mock()
        mock_writer = Mock()
        mock_player.writer.return_value = mock_writer

        service.call_lambda(mock_player, 'nonexistent', {}, '')
        mock_writer.write.assert_called_with(b"Huh?\r\n")


class TestCommandUtilityFunctions(unittest.TestCase):
    """Test command utility functions"""

    def test_get_class_obj_player(self):
        """Test getting Player class object"""
        result = get_class_obj('Player')
        self.assertEqual(result, Player)

    def test_get_class_obj_character(self):
        """Test getting Character class object"""
        result = get_class_obj('Character')
        self.assertEqual(result, Character)

    def test_get_class_obj_lambda(self):
        """Test getting lambda returns None"""
        result = get_class_obj('lambda')
        self.assertIsNone(result)

    def test_get_class_obj_rom_room(self):
        """Test getting Room returns string"""
        result = get_class_obj('Room')
        self.assertEqual(result, 'Room')

    def test_get_class_obj_str(self):
        """Test getting str class"""
        result = get_class_obj('str')
        self.assertEqual(result, str)

    def test_parse_args_single(self):
        """Test parsing single argument"""
        result = parse_args('lambda p: p.do_something()')
        self.assertEqual(result[0], 'p')

    def test_parse_args_multiple(self):
        """Test parsing multiple arguments"""
        result = parse_args('lambda p, c, msg: p.say(msg)')
        self.assertEqual(result, ['p', 'c', 'msg'])

    def test_get_args_with_player(self):
        """Test getting args with player"""
        mock_player = Mock(spec=Player)
        mock_injector = Mock()
        mock_registry = Mock()
        mock_injector.get.return_value = mock_registry

        args = get_args('lambda p: p.do_something()', mock_player, mock_injector, '')
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0], mock_player)

    def test_get_args_with_character(self):
        """Test getting args with character"""
        mock_character = Mock(spec=Character)
        mock_player = Mock(spec=Player)
        mock_player.current_character = mock_character
        mock_injector = Mock()
        mock_registry = Mock()
        mock_injector.get.return_value = mock_registry

        args = get_args('lambda c: c.do_something()', mock_player, mock_injector, '')
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0], mock_character)

    def test_get_args_with_message(self):
        """Test getting args with message string"""
        mock_player = Mock(spec=Player)
        mock_injector = Mock()
        mock_registry = Mock()
        mock_injector.get.return_value = mock_registry

        args = get_args('lambda msg: print(msg)', mock_player, mock_injector, 'test message')
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0], 'test message')

    def test_get_args_with_invalid_message_type(self):
        """Test getting args with non-string message"""
        mock_player = Mock(spec=Player)
        mock_injector = Mock()
        mock_registry = Mock()
        mock_injector.get.return_value = mock_registry

        with self.assertRaises(ValueError):
            get_args('lambda msg: print(msg)', mock_player, mock_injector, 123)

    def test_get_args_with_callable_message(self):
        """Test getting args with callable message raises error"""
        mock_player = Mock(spec=Player)
        mock_injector = Mock()
        mock_registry = Mock()
        mock_injector.get.return_value = mock_registry

        with self.assertRaises(ValueError):
            get_args('lambda msg: print(msg)', mock_player, mock_injector, lambda: 'test')

    def test_get_args_with_invalid_argument(self):
        """Test getting args with invalid argument name"""
        mock_player = Mock(spec=Player)
        mock_injector = Mock()
        mock_registry = Mock()
        mock_injector.get.return_value = mock_registry

        with self.assertRaises(ValueError):
            get_args('lambda x: x.do_something()', mock_player, mock_injector, '')

    @patch('command.CommandService.requests.get')
    def test_handle_lambdas_success(self, mock_get):
        """Test handling lambdas successfully"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        from server.ServiceConfig import ServiceConfig
        mock_config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint='http://test.com/api/commands',
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles"
        )
        command_service = CommandService(mock_config, Mock())

        mock_player = Mock(spec=Player)
        mock_writer = Mock()
        mock_player.writer.return_value = mock_writer

        command = {
            'name': 'test',
            'lambda': ['lambda p: p.writer().write(b"test")']
        }

        # Should execute without error
        handle_lambdas(command_service, mock_player, command, '')

    @patch('command.CommandService.requests.get')
    def test_handle_lambdas_with_none(self, mock_get):
        """Test handling lambdas with None value"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        from server.ServiceConfig import ServiceConfig
        mock_config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint='http://test.com/api/commands',
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles"
        )
        command_service = CommandService(mock_config, Mock())

        command = {
            'name': 'test',
            'lambda': [None]
        }

        with self.assertRaises(ValueError):
            handle_lambdas(command_service, Mock(), command, '')

    @patch('command.CommandService.requests.get')
    def test_handle_lambdas_with_non_string(self, mock_get):
        """Test handling lambdas with non-string value"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        from server.ServiceConfig import ServiceConfig
        mock_config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint='http://test.com/api/commands',
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles"
        )
        command_service = CommandService(mock_config, Mock())

        command = {
            'name': 'test',
            'lambda': [123]
        }

        with self.assertRaises(TypeError):
            handle_lambdas(command_service, Mock(), command, '')


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import Mock, patch
import threading
from player.Player import Player
from player.Character import Character
from object.Item import Item


class TestPlayer(unittest.TestCase):
    """Test Player class"""

    def setUp(self):
        self.player_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'account_name': 'johndoe',
            'email_address': 'john@example.com',
            'password': 'password123',
            'player_character_list': ['char_001', 'char_002'],
            'id': 'player_001'
        }

    def test_from_json(self):
        """Test creating Player from JSON"""
        player = Player.from_json(self.player_data)
        self.assertEqual(player.id, 'player_001')
        self.assertEqual(player.account_name, 'johndoe')
        self.assertEqual(player.first_name, 'John')
        self.assertEqual(player.last_name, 'Doe')

    def test_post_init_creates_lock(self):
        """Test __post_init__ creates thread lock"""
        player = Player.from_json(self.player_data)
        self.assertIsNotNone(player.lock)
        self.assertIsInstance(player.lock, threading.Lock)

    def test_post_init_creates_logger(self):
        """Test __post_init__ creates logger"""
        player = Player.from_json(self.player_data)
        self.assertIsNotNone(player.logger)

    def test_player_defaults(self):
        """Test Player default values"""
        player = Player.from_json(self.player_data)
        self.assertIsNone(player.current_character)
        self.assertIsNone(player.connection)
        self.assertIsNone(player.session_id)
        self.assertFalse(player.ansi_enabled)
        self.assertIsNone(player.usage)

    def test_reader(self):
        """Test reader method"""
        player = Player.from_json(self.player_data)
        mock_reader = Mock()
        mock_writer = Mock()
        player.connection = (mock_reader, mock_writer)

        self.assertEqual(player.reader(), mock_reader)

    def test_writer(self):
        """Test writer method"""
        player = Player.from_json(self.player_data)
        mock_reader = Mock()
        mock_writer = Mock()
        player.connection = (mock_reader, mock_writer)

        self.assertEqual(player.writer(), mock_writer)

    def test_print_visible(self):
        """Test printing visible characters"""
        player = Player.from_json(self.player_data)
        mock_writer = Mock()
        player.connection = (Mock(), mock_writer)

        # Create current character
        current_char = Mock()
        current_char.level = 10
        current_char.race = 'Human'
        current_char.character_class = 'Warrior'
        current_char.name = 'TestChar'
        current_char.title = 'the Brave'
        player.current_character = current_char

        # Create visible characters
        visible_char = Mock()
        visible_char.level = 5
        visible_char.race = 'Elf'
        visible_char.character_class = 'Mage'
        visible_char.name = 'OtherChar'
        visible_char.title = 'the Wise'

        player.print_visible([visible_char])

        # Verify writer was called
        self.assertGreaterEqual(mock_writer.write.call_count, 2)

    def test_to_player(self):
        """Test sending message to player"""
        player = Player.from_json(self.player_data)
        mock_writer = Mock()
        player.connection = (Mock(), mock_writer)

        player.to_player('Hello World')

        mock_writer.write.assert_called_once()
        call_args = mock_writer.write.call_args[0][0]
        self.assertIn(b'Hello World', call_args)

    def test_to_room(self):
        """Test sending message to room"""
        player = Player.from_json(self.player_data)
        mock_player_service = Mock()

        player.to_room(mock_player_service, 'test message', '%p says %m')

        mock_player_service.to_room.assert_called_once_with(
            player, 'test message', '%p says %m'
        )

    def test_player_character_list(self):
        """Test player character list"""
        player = Player.from_json(self.player_data)
        self.assertEqual(len(player.player_character_list), 2)
        self.assertIn('char_001', player.player_character_list)
        self.assertIn('char_002', player.player_character_list)

    def test_lock_is_thread_safe(self):
        """Test lock can be acquired and released"""
        player = Player.from_json(self.player_data)
        self.assertTrue(player.lock.acquire(blocking=False))
        player.lock.release()


class TestCharacter(unittest.TestCase):
    """Test Character class"""

    def setUp(self):
        self.character_data = {
            'id': 'char_001',
            'account_id': 'account_001',
            'title': 'the Brave',
            'description': 'A brave warrior',
            'cloaked': False,
            'guild': 'Warriors',
            'race': 'Human',
            'name': 'TestChar',
            'area_id': 'area_001',
            'room_id': 'room_001',
            'character_class': 'Warrior',
            'role': 'player',
            'sex': 'male',
            'level': 10,
            'health': 100,
            'mana': 50,
            'movement': 100,
            'experience': 1000,
            'accumulated_experience': 1000,
            'trains': 5,
            'practices': 10,
            'gold': 100,
            'silver': 50,
            'wimpy': 10,
            'position': 1,
            'max_weight': 100,
            'max_items': 50,
            'reputation': 0,
            'piercing': 10,
            'bashing': 10,
            'slashing': 10,
            'magic': 5,
            'injector': Mock(),
            'inventory': []
        }

    def test_from_json(self):
        """Test creating Character from JSON"""
        character = Character.from_json(self.character_data)
        self.assertEqual(character.id, 'char_001')
        self.assertEqual(character.name, 'TestChar')
        self.assertEqual(character.level, 10)

    def test_character_attributes(self):
        """Test character attributes are set correctly"""
        character = Character.from_json(self.character_data)
        self.assertEqual(character.race, 'Human')
        self.assertEqual(character.character_class, 'Warrior')
        self.assertEqual(character.health, 100)
        self.assertEqual(character.mana, 50)
        self.assertEqual(character.movement, 100)
        self.assertEqual(character.gold, 100)
        self.assertEqual(character.silver, 50)

    def test_post_init_creates_logger(self):
        """Test __post_init__ creates logger"""
        character = Character.from_json(self.character_data)
        self.assertIsNotNone(character.logger)

    def test_post_init_loads_inventory(self):
        """Test __post_init__ loads inventory"""
        character = Character.from_json(self.character_data)
        self.assertIsNotNone(character.loot)
        self.assertIsInstance(character.loot, dict)

    def test_load_inventory_empty(self):
        """Test loading empty inventory"""
        character = Character.from_json(self.character_data)
        self.assertEqual(len(character.loot), 0)

    def test_load_inventory_with_items(self):
        """Test loading inventory with items"""
        item_data = {
            'id': 'item_001',
            'area_id': 'area_001',
            'vnum': '100',
            'description': 'A sword',
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'item_type': 'weapon',
            'weight': '5',
            'extra_flags': '',
            'wear_flags': '',
            'value': '100',
            'level': '5',
            'affect_data': [],
            'extra_descr': []
        }

        char_data = self.character_data.copy()
        char_data['inventory'] = [item_data]

        character = Character.from_json(char_data)
        self.assertEqual(len(character.loot), 1)
        self.assertIn('item_001', character.loot)

    def test_get_items(self):
        """Test getting items from inventory"""
        item_data = {
            'id': 'item_001',
            'area_id': 'area_001',
            'vnum': '100',
            'description': 'A sword',
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'item_type': 'weapon',
            'weight': '5',
            'extra_flags': '',
            'wear_flags': '',
            'value': '100',
            'level': '5',
            'affect_data': [],
            'extra_descr': []
        }

        char_data = self.character_data.copy()
        char_data['inventory'] = [item_data]

        character = Character.from_json(char_data)
        items = character.get_items()
        self.assertEqual(len(list(items)), 1)

    def test_get_fuzzy_item_exact_match(self):
        """Test getting item with exact name match"""
        item_data = {
            'id': 'item_001',
            'area_id': 'area_001',
            'vnum': '100',
            'description': 'A sword',
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'item_type': 'weapon',
            'weight': '5',
            'extra_flags': '',
            'wear_flags': '',
            'value': '100',
            'level': '5',
            'affect_data': [],
            'extra_descr': []
        }

        char_data = self.character_data.copy()
        char_data['inventory'] = [item_data]
        character = Character.from_json(char_data)

        mock_usage = Mock()
        result = character.get_fuzzy_item('sword', mock_usage)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'sword')
        mock_usage.assert_not_called()

    def test_get_fuzzy_item_partial_match(self):
        """Test getting item with partial name match"""
        item_data = {
            'id': 'item_001',
            'area_id': 'area_001',
            'vnum': '100',
            'description': 'A sword',
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'item_type': 'weapon',
            'weight': '5',
            'extra_flags': '',
            'wear_flags': '',
            'value': '100',
            'level': '5',
            'affect_data': [],
            'extra_descr': []
        }

        char_data = self.character_data.copy()
        char_data['inventory'] = [item_data]
        character = Character.from_json(char_data)

        mock_usage = Mock()
        result = character.get_fuzzy_item('sw', mock_usage)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'sword')

    def test_get_fuzzy_item_no_match(self):
        """Test getting item with no match calls usage"""
        character = Character.from_json(self.character_data)

        mock_usage = Mock()
        result = character.get_fuzzy_item('nonexistent', mock_usage)

        self.assertIsNone(result)
        mock_usage.assert_called_once_with(character)

    def test_get_fuzzy_item_strips_whitespace(self):
        """Test get_fuzzy_item strips whitespace"""
        item_data = {
            'id': 'item_001',
            'area_id': 'area_001',
            'vnum': '100',
            'description': 'A sword',
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'item_type': 'weapon',
            'weight': '5',
            'extra_flags': '',
            'wear_flags': '',
            'value': '100',
            'level': '5',
            'affect_data': [],
            'extra_descr': []
        }

        char_data = self.character_data.copy()
        char_data['inventory'] = [item_data]
        character = Character.from_json(char_data)

        mock_usage = Mock()
        result = character.get_fuzzy_item('  sword\r\n', mock_usage)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'sword')

    def test_combat_stats(self):
        """Test combat-related stats"""
        character = Character.from_json(self.character_data)
        self.assertEqual(character.piercing, 10)
        self.assertEqual(character.bashing, 10)
        self.assertEqual(character.slashing, 10)
        self.assertEqual(character.magic, 5)

    def test_lock_is_thread_safe(self):
        """Test lock can be acquired and released"""
        character = Character.from_json(self.character_data)
        self.assertTrue(character.lock.acquire(blocking=False))
        character.lock.release()


class TestPlayerService(unittest.TestCase):
    """Test PlayerService"""

    def setUp(self):
        self.mock_injector = Mock()
        self.mock_event_handler = Mock()
        self.mock_event_handler.character_registry = {}
        self.mock_injector.get.return_value = self.mock_event_handler

        self.player_config = {
            'endpoints': {
                'players_endpoint': 'http://test.com/api/players',
                'account_endpoint': 'http://test.com/api/account'
            }
        }
        self.character_config = {
            'endpoints': {
                'characters_endpoint': 'http://test.com/api/characters',
                'character_endpoint': 'http://test.com/api/character'
            }
        }

    @patch('player.PlayerService.requests.get')
    def test_initialization(self, mock_get):
        """Test PlayerService initialization"""
        from player.PlayerService import PlayerService

        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        service = PlayerService(
            self.mock_injector,
            self.player_config,
            self.character_config
        )

        self.assertIsNotNone(service.logger)
        self.assertIsNotNone(service.player_list)
        self.assertIsNotNone(service.character_list)

    @patch('player.PlayerService.requests.get')
    def test_get_connected_players(self, mock_get):
        """Test getting connected players"""
        from player.PlayerService import PlayerService

        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        service = PlayerService(
            self.mock_injector,
            self.player_config,
            self.character_config
        )

        result = service.get_connected_players()
        self.assertEqual(result, {})

    @patch('player.PlayerService.requests.get')
    def test_get_account_by_id(self, mock_get):
        """Test getting account by ID"""
        from player.PlayerService import PlayerService

        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        service = PlayerService(
            self.mock_injector,
            self.player_config,
            self.character_config
        )

        mock_get.return_value.json.return_value = {
            'id': 'account_001',
            'accountName': 'testuser'
        }

        result = service.get_account_by_id('account_001')
        self.assertEqual(result['id'], 'account_001')

    @patch('player.PlayerService.requests.post')
    @patch('player.PlayerService.requests.get')
    def test_create_account(self, mock_get, mock_post):
        """Test creating account"""
        from player.PlayerService import PlayerService

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.mock_injector,
            self.player_config,
            self.character_config
        )

        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'new_account_id'}
        mock_post.return_value = mock_response

        result = service.create_account('newuser', 'password')
        self.assertEqual(result, 'new_account_id')


if __name__ == '__main__':
    unittest.main()

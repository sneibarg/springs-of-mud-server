import unittest
from unittest.mock import Mock, patch
import threading
from player import Player, PlayerService
from player.Character import Character
from player.CharacterClass import CharacterClass
from registry import RegistryService
from server.ServiceConfig import ServiceConfig


class TestPlayer(unittest.TestCase):
    """Test Player class"""

    def setUp(self):
        self.service_config: ServiceConfig = Mock()
        self.registry_service: RegistryService = Mock()
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
        self.character_class = str({
            "name": "Mage",
            "attr_prime": 0,
            "weapon": 0,
            "guild": 0,
            "skill_adept": 0,
            "thac0_00": 0,
            "thac0_32": 0,
            "hp_min": 0,
            "hp_max": 0,
            "mana_gain": True,
            "base_group": "mage basics",
            "default_group": "mage basics"
        })
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
            'character_class': self.character_class,
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
            'piercing': 10,
            'bashing': 10,
            'slashing': 10,
            'magic': 5,
            'alignment': 900,
            'pulse_wait': 0,
            'pulse_daze': 0,
            'trust': 0,
            'played': 0,
            'logon': 0,
            'act': "",
            'comm': "",
            'attributes': [],
            'affected_by': [],
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
        # self.assertEqual(character.character_class, 'Warrior')
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
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'material': 'steel',
            'item_type': 'weapon',
            'extra_flags': '',
            'wear_flags': '',
            'value0': '100',
            'value1': '0',
            'value2': '0',
            'value3': '0',
            'value4': '0',
            'weight': 5,
            'condition': '100',
            'level': 5,
            'cost': 100,
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
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'material': 'steel',
            'item_type': 'weapon',
            'extra_flags': '',
            'wear_flags': '',
            'value0': '100',
            'value1': '0',
            'value2': '0',
            'value3': '0',
            'value4': '0',
            'weight': 5,
            'condition': '100',
            'level': 5,
            'cost': 100,
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
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'item_type': 'weapon',
            'material': 'steel',
            'weight': '5',
            'extra_flags': '',
            'wear_flags': '',
            'value0': '100',
            'value1': '0',
            'value2': '0',
            'value3': '0',
            'value4': '0',
            'level': '5',
            'cost': '100',
            'condition': '100',
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
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'material': 'steel',
            'item_type': 'weapon',
            'extra_flags': '',
            'wear_flags': '',
            'value0': '100',
            'value1': '0',
            'value2': '0',
            'value3': '0',
            'value4': '0',
            'weight': 5,
            'condition': '100',
            'level': 5,
            'cost': 100,
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
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A sword',
            'material': 'steel',
            'item_type': 'weapon',
            'extra_flags': '',
            'wear_flags': '',
            'value0': '100',
            'value1': '0',
            'value2': '0',
            'value3': '0',
            'value4': '0',
            'weight': 5,
            'condition': '100',
            'level': 5,
            'cost': 100,
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
        from server.ServiceConfig import ServiceConfig
        from registry import RegistryService

        self.registry_service = RegistryService()
        self.players_endpoint = 'http://test.com/api/players'
        self.characters_endpoint = 'http://test.com/api/characters'
        self.service_config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint="http://test/commands",
            players_endpoint=self.players_endpoint,
            characters_endpoint=self.characters_endpoint,
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles"
        )

    @patch('player.PlayerService.requests.get')
    def test_initialization(self, mock_get):
        """Test PlayerService initialization"""

        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        service = PlayerService(
            self.service_config,
            self.registry_service
        )

        self.assertIsNotNone(service.logger)
        self.assertIsNotNone(service.player_list)
        self.assertIsNotNone(service.character_list)

    @unittest.skip("Method get_connected_players no longer exists in PlayerService")
    @patch('player.PlayerService.requests.get')
    def test_get_connected_players(self, mock_get):
        """Test getting connected players"""

        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        service = PlayerService(
            self.service_config,
            self.registry_service
        )

        result = service.get_connected_players()
        self.assertEqual(result, {})

    @patch('player.PlayerService.requests.get')
    def test_get_account_by_id(self, mock_get):
        """Test getting account by ID"""

        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        service = PlayerService(
            self.service_config,
            self.registry_service
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

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'new_account_id'}
        mock_post.return_value = mock_response

        result = service.create_account('newuser', 'password')
        self.assertEqual(result, 'new_account_id')

    @patch('player.PlayerService.requests.get')
    def test_get_in_room(self, mock_get):
        """Test getting characters in the same room"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        # Setup character registry
        char1 = Mock()
        char1.name = 'char1'
        char1.get_room_id.return_value = 'room_001'

        char2 = Mock()
        char2.name = 'char2'
        char2.get_room_id.return_value = 'room_001'

        char3 = Mock()
        char3.name = 'char3'
        char3.get_room_id.return_value = 'room_002'

        service.registry_service.character_registry = {
            'char1': char1,
            'char2': char2,
            'char3': char3
        }

        result = service.get_in_room(char1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'char2')

    @patch('player.PlayerService.requests.get')
    def test_to_room_with_pattern(self, mock_get):
        """Test sending message to room with pattern"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        character = Mock()
        character.name = 'TestChar'
        character.cloaked = False
        character.get_name.return_value = 'TestChar'
        character.get_room_id.return_value = 'room_001'

        other = Mock()
        other.name = 'OtherChar'
        other.get_name.return_value = 'OtherChar'
        other.get_room_id.return_value = 'room_001'
        mock_writer = Mock()
        other.get_writer.return_value = mock_writer

        service.registry_service.character_registry = {
            'TestChar': character,
            'OtherChar': other
        }

        service.to_room(character, 'hello', '%p says %m')
        mock_writer.write.assert_called_once()
        call_args = mock_writer.write.call_args[0][0]
        self.assertIn(b'TestChar says hello', call_args)

    @patch('player.PlayerService.requests.get')
    def test_to_room_cloaked(self, mock_get):
        """Test sending message to room while cloaked"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        character = Mock()
        character.name = 'TestChar'
        character.cloaked = True
        character.get_name.return_value = 'TestChar'
        character.get_room_id.return_value = 'room_001'

        other = Mock()
        other.name = 'OtherChar'
        other.get_name.return_value = 'OtherChar'
        other.get_room_id.return_value = 'room_001'
        mock_writer = Mock()
        other.get_writer.return_value = mock_writer

        service.registry_service.character_registry = {
            'TestChar': character,
            'OtherChar': other
        }

        service.to_room(character, 'hello', '%p says %m')
        mock_writer.write.assert_called_once()
        call_args = mock_writer.write.call_args[0][0]
        self.assertIn(b'Someone says hello', call_args)

    @patch('player.PlayerService.requests.get')
    def test_to_room_no_pattern(self, mock_get):
        """Test sending message to room without pattern"""
        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        character = Mock()
        character.name = 'TestChar'
        character.get_name.return_value = 'TestChar'
        character.get_room_id.return_value = 'room_001'

        other = Mock()
        other.name = 'OtherChar'
        other.get_name.return_value = 'OtherChar'
        other.get_room_id.return_value = 'room_001'
        mock_writer = Mock()
        other.get_writer.return_value = mock_writer

        service.registry_service.character_registry = {
            'TestChar': character,
            'OtherChar': other
        }

        service.to_room(character, 'hello world', None)
        mock_writer.write.assert_called_once()
        call_args = mock_writer.write.call_args[0][0]
        self.assertEqual(call_args, b'hello world\r\n')

    @unittest.skip("Method get_connected_player no longer exists in PlayerService")
    @patch('player.PlayerService.requests.get')
    def test_get_connected_player(self, mock_get):
        """Test getting a specific connected player"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        mock_char = Mock()
        service.registry_service.character_registry = {'TestChar': mock_char}

        result = service.get_connected_player('TestChar')
        self.assertEqual(result, mock_char)

    @patch('player.PlayerService.requests.get')
    def test_get_account_by_name(self, mock_get):
        """Test getting account by name"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        mock_get.return_value.json.return_value = {
            'id': 'account_001',
            'accountName': 'testuser'
        }

        result = service.get_account_by_name('testuser')
        self.assertEqual(result['accountName'], 'testuser')
        mock_get.assert_called_with('http://test.com/api/players/name/testuser')

    @patch('player.PlayerService.requests.get')
    def test_get_player_characters(self, mock_get):
        """Test getting player characters by account ID"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        mock_get.return_value.json.return_value = [
            {'id': 'char_001', 'name': 'Character1'},
            {'id': 'char_002', 'name': 'Character2'}
        ]

        result = service.get_player_characters('account_001')
        self.assertEqual(len(result), 2)
        mock_get.assert_called_with('http://test.com/api/characters/account/account_001')

    @patch('player.PlayerService.requests.get')
    def test_get_character(self, mock_get):
        """Test getting a specific character"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        mock_get.return_value.json.return_value = {
            'id': 'char_001',
            'name': 'TestChar'
        }

        result = service.get_character('char_001')
        self.assertEqual(result['id'], 'char_001')
        mock_get.assert_called_with(
            'http://test.com/api/characters',
            params={'characterId': 'char_001'}
        )

    @patch('player.PlayerService.requests.post')
    @patch('player.PlayerService.requests.get')
    def test_create_character_with_sheet(self, mock_get, mock_post):
        """Test creating character with sheet"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        sheet = '{"name": "TestChar", "class": "Warrior"}'
        mock_post.return_value.status_code = 201  # Add this line
        mock_post.return_value.json.return_value = {'id': 'char_001'}

        result = service.create_character(sheet)
        self.assertEqual(result['id'], 'char_001')
        mock_post.assert_called_with(
            'http://test.com/api/characters',
            json=sheet
        )

    @patch('player.PlayerService.requests.post')
    @patch('player.PlayerService.requests.get')
    def test_create_character_with_name_and_account(self, mock_get, mock_post):
        """Test creating character with name and account ID"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'char_001'}
        mock_post.return_value = mock_response

        sheet = '{"characterName": "TestChar", "accountId": "account_001"}'
        result = service.create_character(sheet)
        self.assertEqual(result, {'id': 'char_001'})
        mock_post.assert_called_with(
            'http://test.com/api/characters',
            json='{"characterName": "TestChar", "accountId": "account_001"}'
        )

    @patch('player.PlayerService.requests.post')
    @patch('player.PlayerService.requests.get')
    def test_create_character_error(self, mock_get, mock_post):
        """Test creating character with error response"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Bad request'
        mock_post.return_value = mock_response

        sheet = '{"account_id": "account_001", "character_name": "TestChar"}'
        with self.assertRaises(Exception) as context:
            service.create_character(sheet)
        self.assertIn('Error creating character', str(context.exception))

    @patch('player.PlayerService.requests.delete')
    @patch('player.PlayerService.requests.get')
    def test_delete_character(self, mock_get, mock_delete):
        """Test deleting a character"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        mock_delete.return_value.json.return_value = {'success': True}

        result = service.delete_character('char_001')
        self.assertEqual(result['success'], True)
        mock_delete.assert_called_with(
            'http://test.com/api/characters',
            json={'characterId': 'char_001'}
        )

    @patch('player.PlayerService.requests.get')
    def test_visible_player_role(self, mock_get):
        """Test visible method filters cloaked characters for players"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        # Setup player
        player = Mock()
        current_char = Mock()
        current_char.name = 'Player1'
        current_char.role = 'player'
        player.current_character = current_char

        # Setup other characters
        visible_char = Mock()
        visible_char.name = 'VisibleChar'
        visible_char.cloaked = False

        cloaked_char = Mock()
        cloaked_char.name = 'CloakedChar'
        cloaked_char.cloaked = True

        service.registry_service.character_registry = {
            'Player1': current_char,
            'VisibleChar': visible_char,
            'CloakedChar': cloaked_char
        }

        result = service.visible(player)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'VisibleChar')

    @patch('player.PlayerService.requests.get')
    def test_visible_admin_role(self, mock_get):
        """Test visible method shows all characters to admins"""

        mock_get.return_value.json.return_value = []
        service = PlayerService(
            self.service_config,
            self.registry_service,
        )

        # Setup admin player
        player = Mock()
        current_char = Mock()
        current_char.name = 'Admin1'
        current_char.role = 'admin'

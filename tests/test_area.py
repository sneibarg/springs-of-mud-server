import unittest

from unittest.mock import Mock, MagicMock, patch
from area.RomArea import RomArea
from area.RomRoom import RomRoom
from area.AreaService import AreaService
from registry.RegistryService import RegistryService


class TestRomArea(unittest.TestCase):
    """Test RomArea dataclass"""

    def setUp(self):
        self.area_data = {
            'id': 'area_001',
            'name': 'Test Area',
            'vnum': '1000',
            'description': 'A test area',
            'author': 'TestBuilder',
            'area_flags': 'none',
            'reset_msg': 'The area shimmers.',
            'security': '9',
            'min_vnum': '1000',
            'max_vnum': '1099'
        }

    def test_from_json(self):
        """Test creating RomArea from JSON"""
        area = RomArea.from_json(self.area_data)
        self.assertEqual(area.id, 'area_001')
        self.assertEqual(area.name, 'Test Area')
        self.assertEqual(area.vnum, '1000')

    def test_area_attributes(self):
        """Test all area attributes are set correctly"""
        area = RomArea.from_json(self.area_data)
        self.assertEqual(area.description, 'A test area')
        self.assertEqual(area.min_vnum, '1000')
        self.assertEqual(area.max_vnum, '1099')


class TestRomRoom(unittest.TestCase):
    """Test RomRoom dataclass"""

    def setUp(self):
        self.room_data = {
            'id': 'room_001',
            'area_id': 'area_001',
            'vnum': '1001',
            'name': 'Test Room',
            'description': 'A test room',
            'room_flags': 'none',
            'sector_type': 'inside',
            'exit_north': 'room_002',
            'exit_south': None,
            'exit_east': None,
            'exit_west': None,
            'exit_up': None,
            'exit_down': None,
            'pvp': False,
            'spawn': False,
            'spawn_timer': None,
            'spawn_time': None,
            'tele_delay': None,
            'extra_description': '',
            'mobiles': []
        }

    def test_from_json(self):
        """Test creating RomRoom from JSON"""
        room = RomRoom.from_json(self.room_data)
        self.assertEqual(room.id, 'room_001')
        self.assertEqual(room.name, 'Test Room')
        self.assertEqual(room.vnum, '1001')

    def test_room_directions(self):
        """Test room directional exits"""
        room = RomRoom.from_json(self.room_data)
        self.assertEqual(room.exit_north, 'room_002')
        self.assertIsNone(room.exit_east)
        self.assertIsNone(room.exit_west)

    @unittest.skip('Refactored out; likely to be removed.')
    @patch('area.RomRoom.StreamWriter')
    def test_print_description(self, mock_writer):
        """Test printing room description"""
        room = RomRoom.from_json(self.room_data)
        writer = Mock()
        room.print_description(writer, room)
        writer.write.assert_called()


class TestAreaService(unittest.TestCase):
    """Test AreaService"""

    def setUp(self):
        from server.ServiceConfig import ServiceConfig
        self.mock_registry = RegistryService()
        self.areas_endpoint = 'http://test.com/api/areas'
        self.rooms_endpoint = 'http://test.com/api/rooms'
        self.mock_service_config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint="http://test/commands",
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint=self.rooms_endpoint,
            areas_endpoint=self.areas_endpoint,
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles"
        )

    @patch('area.AreaService.requests.get')
    def test_load_areas(self, mock_get):
        """Test loading areas from API"""
        def mock_get_side_effect(url):
            mock_response = Mock()
            if 'areas' in url:
                mock_response.json.return_value = [{
                    'id': 'area_001',
                    'name': 'Test Area',
                    'author': 'TestBuilder',
                    'areaFlags': None,
                    'vnum': '1000',
                    'description': 'Test',
                    'suggestedLevelRange': (1, 50),
                    'resetMsg': 'Reset',
                    'security': '9',
                    'minVnum': '1000',
                    'maxVnum': '1099',
                    'rooms': [],
                    'mobiles': [],
                    'objects': [],
                    'shops': [],
                    'resets': [],
                    'specials': []
                }]
            else:  # rooms endpoint
                mock_response.json.return_value = []
            return mock_response

        mock_get.side_effect = mock_get_side_effect

        service = AreaService(self.mock_service_config, self.mock_registry)
        self.assertEqual(len(service.registry.area_registry), 1)

    @patch('area.AreaService.requests.get')
    def test_load_rooms(self, mock_get):
        """Test loading rooms from API"""
        def mock_get_side_effect(url):
            mock_response = Mock()
            if 'areas' in url:
                mock_response.json.return_value = []
            else:  # rooms endpoint
                mock_response.json.return_value = [{
                    'id': 'room_001',
                    'areaId': 'area_001',
                    'vnum': '1001',
                    'name': 'Test Room',
                    'description': 'Test',
                    'roomFlags': 'none',
                    'sectorType': 'inside',
                    'exit_north': None,
                    'exit_south': None,
                    'exit_east': None,
                    'exit_west': None,
                    'exit_up': None,
                    'exit_down': None,
                    'pvp': False,
                    'spawn': False,
                    'spawn_timer': None,
                    'spawn_time': None,
                    'tele_delay': None,
                    'extra_description': '',
                }]
            return mock_response

        mock_get.side_effect = mock_get_side_effect

        service = AreaService(self.mock_service_config, self.mock_registry)
        self.assertEqual(len(service.registry.room_registry), 1)

    @patch('area.AreaService.requests.get')
    def test_load_area_by_id(self, mock_get):
        """Test loading single area by ID"""
        # Initial empty load
        def mock_get_initial(url):
            mock_response = Mock()
            mock_response.json.return_value = []
            return mock_response

        mock_get.side_effect = mock_get_initial
        service = AreaService(self.mock_service_config, self.mock_registry)

        # Load specific area
        def mock_get_specific(url):
            mock_response = Mock()
            if 'area_002' in url:
                mock_response.json.return_value = {
                    'id': 'area_002',
                    'name': 'New Area',
                    'author': 'TestBuilder',
                    'suggested_level_range': (1, 50),
                    'vnum': '2000',
                    'description': 'New',
                    'areaFlags': 'none',
                    'resetMsg': 'Reset',
                    'security': '9',
                    'minVnum': '2000',
                    'maxVnum': '2099',
                    'rooms': [],
                    'mobiles': [],
                    'objects': [],
                    'shops': [],
                    'resets': [],
                    'specials': []
                }
            return mock_response

        mock_get.side_effect = mock_get_specific
        service.load_area('area_002')
        self.assertIn('area_002', service.registry.area_registry)

    @patch('area.AreaService.requests.get')
    def test_move_mobile_valid_direction(self, mock_get):
        """Test moving mobile in valid direction"""
        # Setup rooms
        def mock_get_side_effect(url):
            mock_response = Mock()
            mock_response.json.return_value = []
            return mock_response

        mock_get.side_effect = mock_get_side_effect
        service = AreaService(self.mock_service_config, self.mock_registry)

        # Create test rooms
        room1 = RomRoom.from_json({
            'id': 'room_001',
            'area_id': 'area_001',
            'vnum': '1001',
            'name': 'Room 1',
            'description': 'First room',
            'room_flags': 'none',
            'sector_type': 'inside',
            'exit_north': 'room_002',
            'exit_south': None,
            'exit_east': None,
            'exit_west': None,
            'exit_up': None,
            'exit_down': None,
            'pvp': False,
            'spawn': False,
            'spawn_timer': None,
            'spawn_time': None,
            'tele_delay': None,
            'extra_description': '',
            'mobiles': []
        })

        room2 = RomRoom.from_json({
            'id': 'room_002',
            'area_id': 'area_001',
            'vnum': '1002',
            'name': 'Room 2',
            'description': 'Second room',
            'room_flags': 'none',
            'sector_type': 'inside',
            'exit_north': None,
            'exit_south': None,
            'exit_east': 'room_001',
            'exit_west': None,
            'exit_up': None,
            'exit_down': None,
            'pvp': False,
            'spawn': False,
            'spawn_timer': None,
            'spawn_time': None,
            'tele_delay': None,
            'extra_description': '',
            'mobiles': []
        })

        service.registry.register_room(room1)
        service.registry.register_room(room2)

        # Create mock character
        character = Mock()
        character.room_id = 'room_001'
        character.writer = Mock()

        # Move north
        service.move_mobile(character, 'exit_north')
        self.assertEqual(character.room_id, 'room_002')

    @patch('area.AreaService.requests.get')
    def test_move_mobile_invalid_direction(self, mock_get):
        """Test moving mobile in invalid direction"""
        def mock_get_side_effect(url):
            mock_response = Mock()
            mock_response.json.return_value = []
            return mock_response

        mock_get.side_effect = mock_get_side_effect
        service = AreaService(self.mock_service_config, self.mock_registry)

        room = RomRoom.from_json({
            'id': 'room_001',
            'area_id': 'area_001',
            'vnum': '1001',
            'name': 'Room 1',
            'description': 'First room',
            'room_flags': 'none',
            'sector_type': 'inside',
            'exit_north': None,
            'exit_south': None,
            'exit_east': None,
            'exit_west': None,
            'exit_up': None,
            'exit_down': None,
            'pvp': False,
            'spawn': False,
            'spawn_timer': None,
            'spawn_time': None,
            'tele_delay': None,
            'extra_description': '',
            'mobiles': []
        })

        service.registry.register_room(room)

        character = Mock()
        character.room_id = 'room_001'
        character.writer = Mock()

        # Try to move in direction with no exit
        service.move_mobile(character, 'exit_north')
        character.writer.write.assert_called_with(b"You can't go that direction!\r\n")
        self.assertEqual(character.room_id, 'room_001')


if __name__ == '__main__':
    unittest.main()

import unittest

from unittest.mock import Mock, patch
from area.AreaRegistry import AreaRegistry
from area.Area import Area
from area.AreaService import AreaService
from area.Room import Room


class TestArea(unittest.TestCase):
    """Test Area dataclass"""

    def setUp(self):
        self.exit_data = {
            'north': 'room_001',
            'south': None,
            'east': None,
            'west': None,
            'up': None,
            'down': None
        }
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
        area = Area.from_json(self.area_data)
        self.assertEqual(area.id, 'area_001')
        self.assertEqual(area.name, 'Test Area')
        self.assertEqual(area.vnum, '1000')

    def test_area_attributes(self):
        """Test all area attributes are set correctly"""
        area = Area.from_json(self.area_data)
        self.assertEqual(area.description, 'A test area')
        self.assertEqual(area.min_vnum, '1000')
        self.assertEqual(area.max_vnum, '1099')


class TestRoom(unittest.TestCase):
    """Test Room dataclass"""

    def setUp(self):
        self.exit_data = {
            'north': 'room_001',
            'south': None,
            'east': None,
            'west': None,
            'up': None,
            'down': None
        }
        self.room_data = {
            'id': 'room_001',
            'area_id': 'area_001',
            'vnum': '1001',
            'name': 'Test Room',
            'description': 'A test room',
            'room_flags': 'none',
            'sector_type': 'inside',
            'exits': self.exit_data,
            'pvp': False,
            'spawn': False,
            'spawn_timer': None,
            'spawn_time': None,
            'tele_delay': None,
            'extra_description': '',
            'mobiles': []
        }

    def test_from_json(self):
        """Test creating Room from JSON"""
        room = Room.from_json(self.room_data)
        self.assertEqual(room.id, 'room_001')
        self.assertEqual(room.name, 'Test Room')
        self.assertEqual(room.vnum, '1001')


class TestAreaService(unittest.TestCase):
    """Test AreaService"""

    def setUp(self):
        from server.ServiceConfig import ServiceConfig
        self.mock_area_registry = AreaRegistry()
        self.areas_endpoint = 'http://test.com/api/areas'
        self.mock_service_config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint="http://test/commands",
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
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

        service = AreaService(self.mock_service_config, self.mock_area_registry)
        self.assertEqual(len(service.area_registry), 1)

    @patch('area.AreaService.requests.get')
    def test_load_rooms(self, mock_get):
        """Test loading rooms from API"""
        def mock_get_side_effect(url):
            mock_response = Mock()
            exit_data = self.exit_data
            exit_data['north'] = 'room_002'
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
                    'exits': exit_data,
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
        self.assertEqual(len(service.registry_service.room_registry), 1)

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
        self.assertIn('area_002', service.registry_service.area_registry)


if __name__ == '__main__':
    unittest.main()

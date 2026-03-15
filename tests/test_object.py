import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, patch
import json

from game import GameData, Version, Constants, Integrity, BuildInfo
from object.Item import Item
from object.ItemService import ItemService


def create_mock_game_data() -> GameData:
    """Create a mock GameData object for testing"""
    return GameData(
        id="test-game",
        kind="mud",
        status="active",
        version=Version(
            family="test",
            lineage=["v1"],
            semver="1.0.0",
            created_at=datetime.now(timezone.utc),
            notes="Test version",
        ),
        constants=Constants(
            max={"players": 100, "level": 50},
            pulses={"perSecond": 4},
        ),
        enums={"directions": ["north", "south", "east", "west"]},
        flags={"room": {"DARK": 1, "NO_MOB": 2}},
        well_known_vnums={"temple": {"room": 3001}},
        integrity=Integrity(
            content_hash="abc123",
            build=BuildInfo(source="test", tool_version="1.0.0", extra={}),
        ),
    )

class TestItem(unittest.TestCase):
    """Test Item class"""

    def setUp(self):
        self.game_data = create_mock_game_data()
        self.item_data = {
            'id': 'item_001',
            'area_id': 'area_001',
            'vnum': '100',
            'name': 'sword',
            'short_description': 'a sword',
            'long_description': 'A beautifully crafted sword lies here.',
            'material': 'steel',
            'item_type': 'weapon',
            'extra_flags': 'magic',
            'wear_flags': 'wield',
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

    def test_from_json(self):
        """Test creating Item from JSON string"""
        json_str = json.dumps(self.item_data)
        item = Item.from_json(json_str)
        self.assertEqual(item.id, 'item_001')
        self.assertEqual(item.name, 'sword')
        self.assertEqual(item.item_type, 'weapon')

    def test_from_json_with_camel_case(self):
        """Test from_json converts camelCase to snake_case"""
        camel_case_data = {
            'id': 'item_001',
            'areaId': 'area_001',
            'vnum': '100',
            'name': 'sword',
            'shortDescription': 'a sword',
            'longDescription': 'A sword lies here',
            'material': 'steel',
            'itemType': 'weapon',
            'extraFlags': 'magic',
            'wearFlags': 'wield',
            'value0': '100',
            'value1': '0',
            'value2': '0',
            'value3': '0',
            'value4': '0',
            'weight': 5,
            'condition': '100',
            'level': 5,
            'cost': 100,
            'affectData': [],
            'extraDescr': []
        }
        json_str = json.dumps(camel_case_data)
        item = Item.from_json(json_str)
        self.assertEqual(item.area_id, 'area_001')
        self.assertEqual(item.short_description, 'a sword')
        self.assertEqual(item.long_description, 'A sword lies here')

    def test_get_name(self):
        """Test getting item name"""
        json_str = json.dumps(self.item_data)
        item = Item.from_json(json_str)
        self.assertEqual(item.get_name(), 'sword')

    def test_print_name(self):
        """Test printing item name"""
        json_str = json.dumps(self.item_data)
        item = Item.from_json(json_str)

        mock_writer = Mock()
        item.print_name(mock_writer)

        mock_writer.write.assert_called_once()
        call_args = mock_writer.write.call_args[0][0]
        self.assertIn(b'sword', call_args)

    def test_print_description(self):
        """Test printing item description"""
        json_str = json.dumps(self.item_data)
        item = Item.from_json(json_str)

        mock_writer = Mock()
        item.print_description(mock_writer)

        mock_writer.write.assert_called_once()
        call_args = mock_writer.write.call_args[0][0]
        self.assertIn(b'A beautifully crafted sword lies here.', call_args)

    def test_print_description_with_none_writer(self):
        """Test print_description with None writer doesn't crash"""
        json_str = json.dumps(self.item_data)
        item = Item.from_json(json_str)

        # Should not raise an error
        item.print_description(None)

    def test_item_attributes(self):
        """Test all item attributes are set correctly"""
        json_str = json.dumps(self.item_data)
        item = Item.from_json(json_str)

        self.assertEqual(item.id, 'item_001')
        self.assertEqual(item.area_id, 'area_001')
        self.assertEqual(item.vnum, '100')
        self.assertEqual(item.material, 'steel')
        self.assertEqual(item.weight, 5)
        self.assertEqual(item.extra_flags, 'magic')
        self.assertEqual(item.wear_flags, 'wield')
        self.assertEqual(item.value0, '100')
        self.assertEqual(item.level, 5)
        self.assertEqual(item.cost, 100)
        self.assertEqual(item.condition, '100')
        self.assertEqual(item.affect_data, [])
        self.assertEqual(item.extra_descr, [])

    def test_post_init_creates_logger(self):
        """Test __post_init__ creates logger"""
        json_str = json.dumps(self.item_data)
        item = Item.from_json(json_str)
        self.assertIsNotNone(item.logger)
        self.assertEqual(item.__name__, 'Item')


class TestItemService(unittest.TestCase):
    """Test ItemService"""

    def setUp(self):
        from server.ServiceConfig import ServiceConfig
        self.game_data = create_mock_game_data()
        self.items_endpoint = 'http://test.com/api/items'
        self.mock_service_config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint="http://test/commands",
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint=self.items_endpoint,
            mobiles_endpoint="http://test/mobiles"
        )

    @patch('object.ItemService.requests.get')
    def test_initialization(self, mock_get):
        """Test ItemService initialization"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 'item_001', 'name': 'sword'},
            {'id': 'item_002', 'name': 'shield'}
        ]
        mock_get.return_value = mock_response

        service = ItemService(self.mock_service_config, self.game_data)

        self.assertEqual(service.total_items, 2)
        self.assertEqual(len(service.all_items), 2)
        self.assertIn('item_001', service.all_items)
        self.assertIn('item_002', service.all_items)

    @patch('object.ItemService.requests.get')
    def test_initialization_empty(self, mock_get):
        """Test ItemService initialization with empty items"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        service = ItemService(self.mock_service_config, self.game_data)

        self.assertEqual(service.total_items, 0)
        self.assertEqual(len(service.all_items), 0)

    @patch('object.ItemService.requests.get')
    def test_initialization_failure(self, mock_get):
        """Test ItemService handles initialization failure gracefully"""
        mock_get.side_effect = Exception('API Error')

        service = ItemService(self.mock_service_config, self.game_data)

        # Should still initialize but with 0 items
        self.assertEqual(service.total_items, 0)
        self.assertEqual(len(service.all_items), 0)

    @patch('object.ItemService.requests.get')
    def test_return_item_by_id(self, mock_get):
        """Test returning item by ID from cache"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 'item_001', 'name': 'sword'},
        ]
        mock_get.return_value = mock_response

        service = ItemService(self.mock_service_config, self.game_data)
        item = service.return_item_by_id('item_001')

        self.assertEqual(item['id'], 'item_001')
        self.assertEqual(item['name'], 'sword')

    @patch('object.ItemService.requests.get')
    def test_return_item_by_id_not_found(self, mock_get):
        """Test returning item by ID when not in cache"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        service = ItemService(self.mock_service_config, self.game_data)

        with self.assertRaises(KeyError):
            service.return_item_by_id('nonexistent')

    @patch('object.ItemService.requests.get')
    def test_get_item_by_id_success(self, mock_get):
        """Test getting item by ID from API"""
        # Initial load
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        service = ItemService(self.mock_service_config, self.game_data)

        # Get specific item
        mock_get.return_value.json.return_value = {
            'id': 'item_001',
            'name': 'sword'
        }

        result = service.get_item_by_id('item_001')
        self.assertEqual(result['id'], 'item_001')
        self.assertEqual(result['name'], 'sword')

    @patch('object.ItemService.requests.get')
    def test_get_item_by_id_failure(self, mock_get):
        """Test getting item by ID handles failure"""
        # Initial load
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        service = ItemService(self.mock_service_config, self.game_data)

        # Fail on specific item
        mock_get.side_effect = Exception('API Error')

        result = service.get_item_by_id('item_001')
        self.assertIsNone(result)

    @patch('object.ItemService.requests.get')
    def test_load_items_counts_correctly(self, mock_get):
        """Test load_items counts items correctly"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 'item_001', 'name': 'sword'},
            {'id': 'item_002', 'name': 'shield'},
            {'id': 'item_003', 'name': 'potion'}
        ]
        mock_get.return_value = mock_response

        service = ItemService(self.mock_service_config, self.game_data)

        self.assertEqual(service.total_items, 3)
        self.assertEqual(len(service.all_items), 3)

    @patch('object.ItemService.requests.get')
    def test_load_items_stores_by_id(self, mock_get):
        """Test load_items stores items by ID"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 'item_001', 'name': 'sword', 'value': '100'},
            {'id': 'item_002', 'name': 'shield', 'value': '50'}
        ]
        mock_get.return_value = mock_response

        service = ItemService(self.mock_service_config, self.game_data)

        self.assertEqual(service.all_items['item_001']['name'], 'sword')
        self.assertEqual(service.all_items['item_001']['value'], '100')
        self.assertEqual(service.all_items['item_002']['name'], 'shield')
        self.assertEqual(service.all_items['item_002']['value'], '50')


if __name__ == '__main__':
    unittest.main()

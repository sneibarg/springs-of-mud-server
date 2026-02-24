import unittest
from unittest.mock import Mock, MagicMock, patch
import threading
from mobile import RomMobile
from object.Item import Item


class TestRomMobile(unittest.TestCase):
    """Test RomMobile class"""

    def setUp(self):
        self.mobile_data = {
            'area_id': 'area_001',
            'vnum': '1001',
            'name': 'goblin',
            'short_description': 'a goblin',
            'long_description': 'A small goblin stands here.',
            'description': 'This is a nasty looking goblin.',
            'act_flags': 'sentinel',
            'affect_flags': 'detect_invis',
            'alignment': '-500',
            'race': 'goblin',
            'sex': 'male',
            'start_pos': 'standing',
            'default_pos': 'standing',
            'id': 'mob_001',
            'level': 5,
            'inventory': []
        }

    def test_from_json(self):
        """Test creating RomMobile from JSON"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertEqual(mobile.id, 'mob_001')
        self.assertEqual(mobile.name, 'goblin')
        self.assertEqual(mobile.level, 5)
        self.assertEqual(mobile.race, 'goblin')

    def test_from_json_with_defaults(self):
        """Test creating RomMobile from JSON sets defaults"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertIsNone(mobile.injector)
        self.assertIsNone(mobile.writer)
        self.assertIsNone(mobile.reader)

    def test_post_init_creates_instance_id(self):
        """Test __post_init__ creates instance_id"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertIsNotNone(mobile.instance_id)

    def test_post_init_creates_lock(self):
        """Test __post_init__ creates thread lock"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertIsNotNone(mobile.lock)
        self.assertIsInstance(mobile.lock, threading.Lock)

    def test_post_init_creates_logger(self):
        """Test __post_init__ creates logger"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertIsNotNone(mobile.logger)
        self.assertTrue(mobile.__name__.startswith('Mobile-'))

    def test_load_inventory_empty(self):
        """Test loading empty inventory"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertEqual(len(mobile.loot), 0)

    @patch('mobile.RomMobile.RomMobile.get_items')
    def test_load_inventory_with_items(self, mock_get_items):
        """Test loading inventory with items"""
        mock_item = Mock(spec=Item)
        mock_item.name = 'sword'
        mock_get_items.return_value = [mock_item]

        mobile = RomMobile.from_json(self.mobile_data)
        self.assertIn('sword', mobile.loot)
        self.assertEqual(mobile.loot['sword'], mock_item)

    def test_get_items_without_injector(self):
        """Test get_items without injector returns empty list"""
        mobile = RomMobile.from_json(self.mobile_data)
        mobile.injector = None
        items = mobile.get_items()
        self.assertEqual(items, [])

    def test_get_items_with_injector(self):
        """Test get_items with injector"""
        mobile_data = self.mobile_data.copy()
        mobile_data['inventory'] = ['item_001', 'item_002']

        mobile = RomMobile.from_json(mobile_data)
        mock_injector = Mock()
        mock_item_service = Mock()

        mock_item1 = {
            'id': 'item_001',
            'name': 'sword',
            'area_id': 'area_001',
            'vnum': '100',
            'description': 'A sword',
            'short_description': 'a sword',
            'long_description': 'A sharp sword',
            'item_type': 'weapon',
            'weight': '5',
            'extra_flags': '',
            'wear_flags': '',
            'value': '100',
            'level': '5',
            'affect_data': [],
            'extra_descr': []
        }

        mock_item_service.get_item_by_id.return_value = str(mock_item1).replace("'", '"')
        mock_injector.get.return_value = mock_item_service
        mobile.injector = mock_injector

        with patch('object.Item.Item.from_json') as mock_from_json:
            mock_item_obj = Mock(spec=Item)
            mock_from_json.return_value = mock_item_obj
            items = mobile.get_items()
            self.assertEqual(len(items), 2)

    def test_get_fuzzy_item_exact_match(self):
        """Test getting item with exact name match"""
        mobile = RomMobile.from_json(self.mobile_data)

        mock_item = Mock(spec=Item)
        mock_item.name = 'sword'
        mobile.loot['sword'] = mock_item

        mock_usage = Mock()
        result = mobile.get_fuzzy_item('sword', mock_usage)

        self.assertEqual(result, mock_item)
        mock_usage.assert_not_called()

    def test_get_fuzzy_item_partial_match(self):
        """Test getting item with partial name match"""
        mobile = RomMobile.from_json(self.mobile_data)

        mock_item = Mock(spec=Item)
        mock_item.name = 'sword'
        mobile.loot['sword'] = mock_item

        mock_usage = Mock()
        result = mobile.get_fuzzy_item('sw', mock_usage)

        self.assertEqual(result, mock_item)
        mock_usage.assert_not_called()

    def test_get_fuzzy_item_no_match(self):
        """Test getting item with no match calls usage"""
        mobile = RomMobile.from_json(self.mobile_data)

        mock_item = Mock(spec=Item)
        mock_item.name = 'sword'
        mobile.loot['sword'] = mock_item

        mock_usage = Mock()
        result = mobile.get_fuzzy_item('axe', mock_usage)

        self.assertIsNone(result)
        mock_usage.assert_called_once_with(mobile)

    def test_get_fuzzy_item_strips_whitespace(self):
        """Test getting item strips whitespace and carriage returns"""
        mobile = RomMobile.from_json(self.mobile_data)

        mock_item = Mock(spec=Item)
        mock_item.name = 'sword'
        mobile.loot['sword'] = mock_item

        mock_usage = Mock()
        result = mobile.get_fuzzy_item('  sword\r\n', mock_usage)

        self.assertEqual(result, mock_item)

    def test_get_fuzzy_item_skips_non_items(self):
        """Test get_fuzzy_item skips non-Item objects in loot"""
        mobile = RomMobile.from_json(self.mobile_data)

        # Add non-Item object
        mobile.loot['not_an_item'] = 'invalid'

        # Add valid item
        mock_item = Mock(spec=Item)
        mock_item.name = 'sword'
        mobile.loot['sword'] = mock_item

        mock_usage = Mock()
        result = mobile.get_fuzzy_item('sword', mock_usage)

        self.assertEqual(result, mock_item)

    def test_mobile_attributes(self):
        """Test all mobile attributes are set correctly"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertEqual(mobile.area_id, 'area_001')
        self.assertEqual(mobile.vnum, '1001')
        self.assertEqual(mobile.short_description, 'a goblin')
        self.assertEqual(mobile.long_description, 'A small goblin stands here.')
        self.assertEqual(mobile.act_flags, 'sentinel')
        self.assertEqual(mobile.affect_flags, 'detect_invis')
        self.assertEqual(mobile.alignment, '-500')
        self.assertEqual(mobile.sex, 'male')
        self.assertEqual(mobile.start_pos, 'standing')
        self.assertEqual(mobile.default_pos, 'standing')

    def test_multiple_mobiles_have_unique_instance_ids(self):
        """Test that multiple mobiles have unique instance IDs"""
        mobile1 = RomMobile.from_json(self.mobile_data)
        mobile2 = RomMobile.from_json(self.mobile_data)

        self.assertNotEqual(mobile1.instance_id, mobile2.instance_id)

    def test_loot_dict_is_initialized(self):
        """Test loot dict is properly initialized"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertIsNotNone(mobile.loot)
        self.assertIsInstance(mobile.loot, dict)

    def test_lock_is_thread_safe(self):
        """Test lock can be acquired and released"""
        mobile = RomMobile.from_json(self.mobile_data)
        self.assertTrue(mobile.lock.acquire(blocking=False))
        mobile.lock.release()


if __name__ == '__main__':
    unittest.main()

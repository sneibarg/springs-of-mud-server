import unittest
from unittest.mock import Mock, patch
import threading
import json
import os
import copy
from mobile import Mobile, MobileService


class TestMobile(unittest.TestCase):
    """Test Mobile class"""

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
            'group': '',
            'dam_type': 'blunt',
            'off_flags': 'aggressive',
            'imm_flags': 'fire',
            'res_flags': 'cold',
            'vuln_flags': '',
            'form': '',
            'parts': '',
            'size': '',
            'material': '',
            'flags': '',
            'hit_roll': 0,
            'hit_dice_number': 0,
            'hit_dice_type': 0,
            'hit_dice_bonus': 0,
            'mana_dice_number': 0,
            'mana_dice_type': 0,
            'mana_dice_bonus': 0,
            'damage_dice_number': 0,
            'damage_dice_type': 0,
            'damage_dice_bonus': 0,
            'ac_pierce': 0,
            'ac_bash': 0,
            'ac_slash': 0,
            'ac_exotic': 0,
            'gold': 0,
        }

    def test_from_json(self):
        """Test creating Mobile from JSON"""
        mobile = Mobile.from_json(self.mobile_data)
        self.assertEqual(mobile.id, 'mob_001')
        self.assertEqual(mobile.name, 'goblin')
        self.assertEqual(mobile.level, 5)
        self.assertEqual(mobile.race, 'goblin')
        self.assertEqual(mobile.group, '')
        self.assertEqual(mobile.dam_type, 'blunt')
        self.assertEqual(mobile.off_flags, 'aggressive')
        self.assertEqual(mobile.imm_flags, 'fire')
        self.assertEqual(mobile.res_flags, 'cold')
        self.assertEqual(mobile.vuln_flags, '')
        self.assertEqual(mobile.form, '')
        self.assertEqual(mobile.parts, '')

    def test_post_init_creates_instance_id(self):
        """Test __post_init__ creates instance_id"""
        mobile = Mobile.from_json(self.mobile_data)
        self.assertIsNotNone(mobile.instance_id)

    def test_post_init_creates_lock(self):
        """Test __post_init__ creates thread lock"""
        mobile = Mobile.from_json(self.mobile_data)
        self.assertIsNotNone(mobile.lock)
        self.assertIsInstance(mobile.lock, threading.Lock)

    def test_post_init_creates_logger(self):
        """Test __post_init__ creates logger"""
        mobile = Mobile.from_json(self.mobile_data)
        self.assertIsNotNone(mobile.logger)
        self.assertTrue(mobile.__name__.startswith('Mobile-'))

    def test_mobile_attributes(self):
        """Test all mobile attributes are set correctly"""
        mobile = Mobile.from_json(self.mobile_data)
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
        mobile1 = Mobile.from_json(self.mobile_data)
        mobile2 = Mobile.from_json(self.mobile_data)

        self.assertNotEqual(mobile1.instance_id, mobile2.instance_id)

    def test_lock_is_thread_safe(self):
        """Test lock can be acquired and released"""
        mobile = Mobile.from_json(self.mobile_data)
        self.assertTrue(mobile.lock.acquire(blocking=False))
        mobile.lock.release()


class TestMobileService(unittest.TestCase):
    """Test MobileService class"""

    def setUp(self):
        """Set up test fixtures"""
        from server.ServiceConfig import ServiceConfig
        from game import GameData
        from registry import RegistryService
        from area import AreaService
        from event import EventHandler

        self.mock_config = Mock(spec=ServiceConfig)
        self.mock_config.mobiles_endpoint = 'http://test/mobiles'

        self.mock_game_data = Mock(spec=GameData)
        self.mock_game_data.enums = {
            'position': {'standing': 8, 'sleeping': 4, 'sitting': 6},
            'sex': {'male': 1, 'female': 2, 'neutral': 0},
            'size': {'tiny': 0, 'small': 1, 'medium': 2, 'large': 3, 'huge': 4}
        }

        self.mock_registry = Mock(spec=RegistryService)
        self.mock_area_service = Mock(spec=AreaService)
        self.mock_event_handler = Mock(spec=EventHandler)

        # Load real mobile data
        json_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'collections', 'SOMDB.Mobiles.json')
        with open(json_path, 'r') as f:
            self.mobile_json_data = json.load(f)

    def _get_default_race(self):
        """Helper to get default race data"""
        return {
            'id': 'goblin',
            'name': 'Goblin',
            'act': 0,
            'aff': 0,
            'off': 0,
            'imm': 0,
            'res': 0,
            'vuln': 0,
            'form': 0,
            'parts': 0
        }

    def _get_mobile_from_json(self, vnum):
        """Helper to get a mobile from the loaded JSON by vnum - returns deep copy"""
        for mobile in self.mobile_json_data:
            if str(mobile.get('vnum')) == str(vnum):
                return copy.deepcopy(mobile)
        return None

    def _get_mobile_id(self, mobile_data):
        """Helper to get the mobile ID as it will be resolved by MobileService"""
        return str(mobile_data.get('id') or mobile_data.get('_id') or mobile_data.get('vnum') or '').strip()

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_basic(self, mock_get):
        """Test loading mobiles from REST endpoint"""
        # Use first mobile from JSON file (vnum 1000 - fairy dragon)
        test_mobile = self._get_mobile_from_json('1000')
        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        # Setup game_data mocks
        self.mock_game_data.flag_value.return_value = 1  # ACT_IS_NPC flag
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()

        self.assertEqual(len(result), 1)
        # Get the mobile ID as MobileService will resolve it
        mobile_id = self._get_mobile_id(test_mobile)
        self.assertIn(mobile_id, result)
        self.assertIsInstance(result[mobile_id], Mobile)
        self.assertEqual(result[mobile_id].name, 'oldstyle fairy dragon')
        self.assertEqual(result[mobile_id].level, 5)

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_duplicate_rejection(self, mock_get):
        """Test that duplicate mobile IDs raise an error"""
        test_mobile = self._get_mobile_from_json('1000')
        # Create duplicate by copying
        duplicate_mobile = test_mobile.copy()

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile, duplicate_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        with self.assertRaises(ValueError) as context:
            MobileService(
                self.mock_config,
                self.mock_game_data,
                self.mock_registry,
                self.mock_area_service,
                self.mock_event_handler
            ).start()

        self.assertIn('duplicated', str(context.exception))

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_capitalization(self, mock_get):
        """Test that long_description and description are capitalized"""
        test_mobile = self._get_mobile_from_json('1000')
        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()
        mobile_id = self._get_mobile_id(test_mobile)
        mobile = result[mobile_id]

        # Verify capitalization
        self.assertTrue(mobile.long_description[0].isupper())
        self.assertTrue(mobile.description[0].isupper())

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_race_flag_merge(self, mock_get):
        """Test that race flags are merged with mobile flags"""
        test_mobile = self._get_mobile_from_json('1000')
        # Override flags for testing
        test_mobile['actFlags'] = 2
        test_mobile['affectFlags'] = 4
        test_mobile['offFlags'] = 8

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1  # ACT_IS_NPC
        self.mock_game_data.get_race.return_value = {
            'id': 'goblin',
            'act': 16,
            'aff': 32,
            'off': 64,
            'imm': 128,
            'res': 256,
            'vuln': 512,
            'form': 1024,
            'parts': 2048
        }

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()
        mobile_id = self._get_mobile_id(test_mobile)
        mobile = result[mobile_id]

        # act_flags = 2 (mobile) | 1 (NPC) | 16 (race) = 19
        self.assertEqual(mobile.act_flags, '19')
        # affect_flags = 4 (mobile) | 32 (race) = 36
        self.assertEqual(mobile.affect_flags, '36')
        # off_flags = 8 (mobile) | 64 (race) = 72
        self.assertEqual(mobile.off_flags, '72')

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_flag_removes(self, mock_get):
        """Test that flag_removes are applied correctly"""
        test_mobile = self._get_mobile_from_json('1000')
        # Override for testing
        test_mobile['actFlags'] = 31  # Binary: 11111
        test_mobile['flagRemoves'] = [
            {'domain': 'act', 'vector': 8}  # Remove bit 8
        ]

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = {'id': 'goblin', 'act': 0}

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()
        mobile_id = self._get_mobile_id(test_mobile)
        mobile = result[mobile_id]

        # act_flags = (31 | 1) & ~8 = 31 & ~8 = 23
        self.assertEqual(mobile.act_flags, '23')

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_position_normalization(self, mock_get):
        """Test position normalization"""
        test_mobile = self._get_mobile_from_json('1000')
        test_mobile['startPos'] = 'sleeping'
        test_mobile['defaultPos'] = 'standing'

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()
        mobile_id = self._get_mobile_id(test_mobile)
        mobile = result[mobile_id]

        self.assertEqual(mobile.start_pos, '4')  # SLEEPING
        self.assertEqual(mobile.default_pos, '8')  # STANDING

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_kill_table(self, mock_get):
        """Test kill_table is populated correctly"""
        # Use three real mobiles from the JSON with specific levels
        mob1 = self._get_mobile_from_json('1000').copy()
        mob2 = self._get_mobile_from_json('1001').copy()

        # Modify IDs and levels for testing
        mob1['level'] = 5
        mob2['level'] = 5
        mob2['_id'] = {'$oid': 'unique_id_002'}

        mock_response = Mock()
        mock_response.json.return_value = [mob1, mob2]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        service.load_mobiles()

        self.assertEqual(service.kill_table[5], 2)  # Two level 5 mobs

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_parse_dice_string(self, mock_get):
        """Test parsing dice notation strings"""
        test_mobile = self._get_mobile_from_json('1000')
        # Override with string dice notation
        test_mobile['hit'] = '3d8+12'
        test_mobile['mana'] = '2d6+5'
        test_mobile['damage'] = '1d4+2'

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()
        mobile_id = self._get_mobile_id(test_mobile)
        mobile = result[mobile_id]

        # Check individual dice fields
        self.assertEqual(mobile.hit_dice_number, 3)
        self.assertEqual(mobile.hit_dice_type, 8)
        self.assertEqual(mobile.hit_dice_bonus, 12)
        self.assertEqual(mobile.mana_dice_number, 2)
        self.assertEqual(mobile.mana_dice_type, 6)
        self.assertEqual(mobile.mana_dice_bonus, 5)
        self.assertEqual(mobile.damage_dice_number, 1)
        self.assertEqual(mobile.damage_dice_type, 4)
        self.assertEqual(mobile.damage_dice_bonus, 2)

        # Check backwards compatibility fields
        self.assertEqual(mobile.hit, {'number': 3, 'type': 8, 'bonus': 12})
        self.assertEqual(mobile.mana, {'number': 2, 'type': 6, 'bonus': 5})
        self.assertEqual(mobile.damage, {'number': 1, 'type': 4, 'bonus': 2})

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_parse_dice_dict(self, mock_get):
        """Test parsing dice notation as dict"""
        test_mobile = self._get_mobile_from_json('1000')
        # Override with dict dice notation
        test_mobile['hit'] = {'number': 3, 'type': 8, 'bonus': 12}

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()
        mobile_id = self._get_mobile_id(test_mobile)
        mobile = result[mobile_id]

        # Check individual dice fields
        self.assertEqual(mobile.hit_dice_number, 3)
        self.assertEqual(mobile.hit_dice_type, 8)
        self.assertEqual(mobile.hit_dice_bonus, 12)
        # Check backwards compatibility field
        self.assertEqual(mobile.hit, {'number': 3, 'type': 8, 'bonus': 12})

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_parse_ac(self, mock_get):
        """Test parsing AC values"""
        test_mobile = self._get_mobile_from_json('1000')
        # Override with dict AC notation
        test_mobile['ac'] = {
            'pierce': 10,
            'bash': 20,
            'slash': 15,
            'exotic': 25
        }

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()
        mobile_id = self._get_mobile_id(test_mobile)
        mobile = result[mobile_id]

        # Check individual AC fields
        self.assertEqual(mobile.ac_pierce, 10)
        self.assertEqual(mobile.ac_bash, 20)
        self.assertEqual(mobile.ac_slash, 15)
        self.assertEqual(mobile.ac_exotic, 25)
        # Check backwards compatibility field
        self.assertEqual(mobile.ac, {'pierce': 10, 'bash': 20, 'slash': 15, 'exotic': 25})

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_missing_id(self, mock_get):
        """Test that mobiles without ID are skipped"""
        test_mobile1 = self._get_mobile_from_json('1000').copy()
        test_mobile2 = self._get_mobile_from_json('1001').copy()

        # Remove ID from first mobile
        del test_mobile1['_id']
        del test_mobile1['vnum']

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile1, test_mobile2]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_race.return_value = self._get_default_race()
        self.mock_game_data.get_attack.return_value = None

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()

        self.assertEqual(len(result), 1)
        mobile_id2 = self._get_mobile_id(test_mobile2)
        self.assertIn(mobile_id2, result)

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_race_name_resolution(self, mock_get):
        """Test race name resolution from player name"""
        test_mobile = self._get_mobile_from_json('1000').copy()
        # Override to test race inference
        test_mobile['name'] = 'orc warrior'
        del test_mobile['race']

        mock_response = Mock()
        mock_response.json.return_value = [test_mobile]
        mock_get.return_value = mock_response

        self.mock_game_data.flag_value.return_value = 1
        self.mock_game_data.get_attack.return_value = None

        # Mock get_race to return None for first call (no explicit race),
        # then return orc data when called with 'orc'
        def get_race_side_effect(race_name):
            if race_name == 'orc':
                return {'id': 'orc', 'name': 'Orc', 'act': 0, 'aff': 0, 'off': 0, 'imm': 0, 'res': 0, 'vuln': 0, 'form': 0, 'parts': 0}
            return None

        self.mock_game_data.get_race.side_effect = get_race_side_effect

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()
        mobile_id = self._get_mobile_id(test_mobile)
        mobile = result[mobile_id]

        self.assertEqual(mobile.race, 'orc')

    @patch('mobile.MobileService.requests.get')
    def test_load_mobiles_api_failure(self, mock_get):
        """Test handling of API failure"""
        mock_get.side_effect = Exception('Network error')

        service = MobileService(
            self.mock_config,
            self.mock_game_data,
            self.mock_registry,
            self.mock_area_service,
            self.mock_event_handler
        )

        result = service.load_mobiles()

        self.assertEqual(result, {})
        self.assertEqual(service.all_mobiles, {})
        self.assertEqual(service.kill_table, {})


if __name__ == '__main__':
    unittest.main()

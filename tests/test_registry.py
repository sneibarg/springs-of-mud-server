import unittest
from unittest.mock import Mock
import threading
from registry.RegistryService import RegistryService


class TestRegistryService(unittest.TestCase):
    """Test RegistryService"""

    def setUp(self):
        self.registry = RegistryService()

    def test_initialization(self):
        """Test RegistryService initialization"""
        self.assertIsNotNone(self.registry.area_registry)
        self.assertIsNotNone(self.registry.room_registry)
        self.assertIsNotNone(self.registry.character_registry)
        self.assertIsNotNone(self.registry.mobile_registry)
        self.assertIsNotNone(self.registry.lock)
        self.assertIsInstance(self.registry.lock, threading.Lock)

    def test_registries_start_empty(self):
        """Test all registries start empty"""
        self.assertEqual(len(self.registry.area_registry), 0)
        self.assertEqual(len(self.registry.room_registry), 0)
        self.assertEqual(len(self.registry.character_registry), 0)
        self.assertEqual(len(self.registry.mobile_registry), 0)

    def test_register_area(self):
        """Test registering an area"""
        mock_area = Mock()
        mock_area.id = 'area_001'

        self.registry.register_area(mock_area)
        self.assertIn('area_001', self.registry.area_registry)
        self.assertEqual(self.registry.area_registry['area_001'], mock_area)

    def test_register_multiple_areas(self):
        """Test registering multiple areas"""
        area1 = Mock()
        area1.id = 'area_001'
        area2 = Mock()
        area2.id = 'area_002'

        self.registry.register_area(area1)
        self.registry.register_area(area2)

        self.assertEqual(len(self.registry.area_registry), 2)
        self.assertIn('area_001', self.registry.area_registry)
        self.assertIn('area_002', self.registry.area_registry)

    def test_unregister_area(self):
        """Test unregistering an area"""
        mock_area = Mock()
        mock_area.id = 'area_001'

        self.registry.register_area(mock_area)
        self.assertIn('area_001', self.registry.area_registry)

        self.registry.unregister_area(mock_area)
        self.assertNotIn('area_001', self.registry.area_registry)

    def test_get_area_from_registry(self):
        """Test getting area from registry"""
        mock_area = Mock()
        mock_area.id = 'area_001'
        mock_area.name = 'Test Area'

        self.registry.register_area(mock_area)
        result = self.registry.get_area_from_registry('area_001')

        self.assertEqual(result, mock_area)
        self.assertEqual(result.name, 'Test Area')

    def test_register_room(self):
        """Test registering a room"""
        mock_room = Mock()
        mock_room.id = 'room_001'

        self.registry.register_room(mock_room)
        self.assertIn('room_001', self.registry.room_registry)
        self.assertEqual(self.registry.room_registry['room_001'], mock_room)

    def test_register_multiple_rooms(self):
        """Test registering multiple rooms"""
        room1 = Mock()
        room1.id = 'room_001'
        room2 = Mock()
        room2.id = 'room_002'

        self.registry.register_room(room1)
        self.registry.register_room(room2)

        self.assertEqual(len(self.registry.room_registry), 2)
        self.assertIn('room_001', self.registry.room_registry)
        self.assertIn('room_002', self.registry.room_registry)

    def test_unregister_room(self):
        """Test unregistering a room"""
        mock_room = Mock()
        mock_room.id = 'room_001'

        self.registry.register_room(mock_room)
        self.assertIn('room_001', self.registry.room_registry)

        self.registry.unregister_room(mock_room)
        self.assertNotIn('room_001', self.registry.room_registry)

    def test_register_character(self):
        """Test registering a character"""
        mock_character = Mock()
        mock_character.id = 'char_001'

        self.registry.register_character(mock_character)
        self.assertIn('char_001', self.registry.character_registry)
        self.assertEqual(self.registry.character_registry['char_001']["current_character"], mock_character)

    def test_register_multiple_characters(self):
        """Test registering multiple characters"""
        char1 = Mock()
        char1.id = 'char_001'
        char2 = Mock()
        char2.id = 'char_002'

        self.registry.register_character(char1)
        self.registry.register_character(char2)

        self.assertEqual(len(self.registry.character_registry), 2)
        self.assertIn('char_001', self.registry.character_registry)
        self.assertIn('char_002', self.registry.character_registry)

    def test_unregister_character(self):
        """Test unregistering a character"""
        mock_character = Mock()
        mock_character.id = 'char_001'

        self.registry.register_character(mock_character)
        self.assertIn('char_001', self.registry.character_registry)

        self.registry.unregister_character(mock_character)
        self.assertNotIn('char_001', self.registry.character_registry)

    def test_get_character_from_registry(self):
        """Test getting character from registry"""
        mock_character = Mock()
        mock_character.id = 'char_001'
        mock_character.name = 'TestChar'

        self.registry.register_character(mock_character)
        result = self.registry.get_character_from_registry('char_001')

        self.assertEqual(result, mock_character)
        self.assertEqual(result.name, 'TestChar')

    def test_register_mobile(self):
        """Test registering a mobile"""
        mock_mobile = Mock()
        mock_mobile.id = 'mob_001'

        self.registry.register_mobile(mock_mobile)
        self.assertIn('mob_001', self.registry.mobile_registry)
        self.assertEqual(self.registry.mobile_registry['mob_001'], mock_mobile)

    def test_register_multiple_mobiles(self):
        """Test registering multiple mobiles"""
        mob1 = Mock()
        mob1.id = 'mob_001'
        mob2 = Mock()
        mob2.id = 'mob_002'

        self.registry.register_mobile(mob1)
        self.registry.register_mobile(mob2)

        self.assertEqual(len(self.registry.mobile_registry), 2)
        self.assertIn('mob_001', self.registry.mobile_registry)
        self.assertIn('mob_002', self.registry.mobile_registry)

    def test_unregister_mobile(self):
        """Test unregistering a mobile"""
        mock_mobile = Mock()
        mock_mobile.id = 'mob_001'

        self.registry.register_mobile(mock_mobile)
        self.assertIn('mob_001', self.registry.mobile_registry)

        self.registry.unregister_mobile(mock_mobile)
        self.assertNotIn('mob_001', self.registry.mobile_registry)

    def test_get_mobile_from_registry(self):
        """Test getting mobile from registry"""
        mock_mobile = Mock()
        mock_mobile.id = 'mob_001'
        mock_mobile.name = 'Goblin'

        self.registry.register_mobile(mock_mobile)
        result = self.registry.get_mobile_from_registry('mob_001')

        self.assertEqual(result, mock_mobile)
        self.assertEqual(result.name, 'Goblin')

    def test_register_same_id_overwrites(self):
        """Test registering same ID overwrites previous entry"""
        area1 = Mock()
        area1.id = 'area_001'
        area1.name = 'First Area'

        area2 = Mock()
        area2.id = 'area_001'
        area2.name = 'Second Area'

        self.registry.register_area(area1)
        self.registry.register_area(area2)

        self.assertEqual(len(self.registry.area_registry), 1)
        self.assertEqual(self.registry.area_registry['area_001'].name, 'Second Area')

    def test_unregister_nonexistent_raises_keyerror(self):
        """Test unregistering nonexistent entry raises KeyError"""
        mock_area = Mock()
        mock_area.id = 'nonexistent'

        with self.assertRaises(KeyError):
            self.registry.unregister_area(mock_area)

    def test_get_nonexistent_raises_keyerror(self):
        """Test getting nonexistent entry raises KeyError"""
        with self.assertRaises(KeyError):
            self.registry.get_area_from_registry('nonexistent')

    def test_thread_safety_area(self):
        """Test thread-safe area operations"""
        mock_area = Mock()
        mock_area.id = 'area_001'

        # Should be able to acquire lock
        self.assertTrue(self.registry.lock.acquire(blocking=False))
        self.registry.lock.release()

        # Operations should work
        self.registry.register_area(mock_area)
        self.assertIn('area_001', self.registry.area_registry)

    def test_thread_safety_room(self):
        """Test thread-safe room operations"""
        mock_room = Mock()
        mock_room.id = 'room_001'

        self.registry.register_room(mock_room)
        self.assertIn('room_001', self.registry.room_registry)

    def test_thread_safety_character(self):
        """Test thread-safe character operations"""
        mock_character = Mock()
        mock_character.id = 'char_001'

        self.registry.register_character(mock_character)
        self.assertIn('char_001', self.registry.character_registry)

    def test_thread_safety_mobile(self):
        """Test thread-safe mobile operations"""
        mock_mobile = Mock()
        mock_mobile.id = 'mob_001'

        self.registry.register_mobile(mock_mobile)
        self.assertIn('mob_001', self.registry.mobile_registry)

    def test_all_registries_independent(self):
        """Test all registries are independent"""
        area = Mock()
        area.id = 'id_001'
        room = Mock()
        room.id = 'id_002'
        character = Mock()
        character.id = 'id_003'
        mobile = Mock()
        mobile.id = 'id_004'

        self.registry.register_area(area)
        self.registry.register_room(room)
        self.registry.register_character(character)
        self.registry.register_mobile(mobile)

        self.assertEqual(len(self.registry.area_registry), 1)
        self.assertEqual(len(self.registry.room_registry), 1)
        self.assertEqual(len(self.registry.character_registry), 1)
        self.assertEqual(len(self.registry.mobile_registry), 1)


if __name__ == '__main__':
    unittest.main()

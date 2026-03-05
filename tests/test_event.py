import unittest
from unittest.mock import Mock
from event import EventHandler


class TestEventHandler(unittest.TestCase):
    """Test EventHandler"""

    def setUp(self):
        self.event_handler = EventHandler()

    def test_initialization(self):
        """Test EventHandler initialization"""
        self.assertIsNotNone(self.event_handler.logger)
        self.assertIsInstance(self.event_handler.command_list, list)
        self.assertIsInstance(self.event_handler.character_registry, dict)
        self.assertIsInstance(self.event_handler.mobile_registry, dict)
        self.assertIsInstance(self.event_handler.character_events, dict)
        self.assertIsInstance(self.event_handler.mobile_events, dict)

    def test_register_character(self):
        """Test registering a character"""
        mock_character = Mock()
        mock_character.name = 'TestChar'

        self.event_handler.register_character(mock_character)
        self.assertIn('TestChar', self.event_handler.character_registry)
        self.assertEqual(self.event_handler.character_registry['TestChar'], mock_character)

    def test_register_multiple_characters(self):
        """Test registering multiple characters"""
        char1 = Mock()
        char1.name = 'Char1'
        char2 = Mock()
        char2.name = 'Char2'

        self.event_handler.register_character(char1)
        self.event_handler.register_character(char2)

        self.assertEqual(len(self.event_handler.character_registry), 2)
        self.assertIn('Char1', self.event_handler.character_registry)
        self.assertIn('Char2', self.event_handler.character_registry)

    def test_register_same_character_twice(self):
        """Test registering same character twice (should overwrite)"""
        mock_char1 = Mock()
        mock_char1.name = 'TestChar'

        mock_char2 = Mock()
        mock_char2.name = 'TestChar'

        self.event_handler.register_character(mock_char1)
        self.event_handler.register_character(mock_char2)

        self.assertEqual(len(self.event_handler.character_registry), 1)
        self.assertEqual(self.event_handler.character_registry['TestChar'], mock_char2)

    def test_unregister_character(self):
        """Test unregistering a character"""
        mock_character = Mock()
        mock_character.name = 'TestChar'

        self.event_handler.register_character(mock_character)
        self.assertIn('TestChar', self.event_handler.character_registry)

        self.event_handler.unregister_character('TestChar')
        self.assertNotIn('TestChar', self.event_handler.character_registry)

    def test_register_mobile(self):
        """Test registering a mobile"""
        mock_mobile = Mock()
        mock_mobile.name = 'Goblin'
        mock_mobile.id = 'mob_001'

        self.event_handler.register_mobile(mock_mobile)
        self.assertIn('mob_001', self.event_handler.mobile_registry)
        self.assertEqual(self.event_handler.mobile_registry['mob_001'], mock_mobile)

    def test_register_multiple_mobiles(self):
        """Test registering multiple mobiles"""
        mob1 = Mock()
        mob1.name = 'Goblin'
        mob1.id = 'mob_001'

        mob2 = Mock()
        mob2.name = 'Orc'
        mob2.id = 'mob_002'

        self.event_handler.register_mobile(mob1)
        self.event_handler.register_mobile(mob2)

        self.assertEqual(len(self.event_handler.mobile_registry), 2)
        self.assertIn('mob_001', self.event_handler.mobile_registry)
        self.assertIn('mob_002', self.event_handler.mobile_registry)

    def test_register_same_mobile_twice(self):
        """Test registering same mobile twice (should overwrite)"""
        mob1 = Mock()
        mob1.name = 'Goblin'
        mob1.id = 'mob_001'

        mob2 = Mock()
        mob2.name = 'Goblin'
        mob2.id = 'mob_001'

        self.event_handler.register_mobile(mob1)
        self.event_handler.register_mobile(mob2)

        self.assertEqual(len(self.event_handler.mobile_registry), 1)
        self.assertEqual(self.event_handler.mobile_registry['mob_001'], mob2)

    def test_unregister_mobile(self):
        """Test unregistering a mobile"""
        mock_mobile = Mock()
        mock_mobile.name = 'Goblin'
        mock_mobile.id = 'mob_001'

        self.event_handler.register_mobile(mock_mobile)
        self.assertIn('mob_001', self.event_handler.mobile_registry)

        self.event_handler.unregister_mobile(mock_mobile)
        self.assertNotIn('mob_001', self.event_handler.mobile_registry)

    def test_character_events_dict(self):
        """Test character_events dictionary is accessible"""
        self.assertIsInstance(self.event_handler.character_events, dict)
        self.assertEqual(len(self.event_handler.character_events), 0)

    def test_mobile_events_dict(self):
        """Test mobile_events dictionary is accessible"""
        self.assertIsInstance(self.event_handler.mobile_events, dict)
        self.assertEqual(len(self.event_handler.mobile_events), 0)

    def test_command_list_initialized(self):
        """Test command_list is initialized as empty list"""
        self.assertIsInstance(self.event_handler.command_list, list)
        self.assertEqual(len(self.event_handler.command_list), 0)


if __name__ == '__main__':
    unittest.main()

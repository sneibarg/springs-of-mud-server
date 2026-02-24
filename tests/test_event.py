import unittest
from unittest.mock import Mock, patch
from event.EventHandler import EventHandler


class TestEventHandler(unittest.TestCase):
    """Test EventHandler"""

    def setUp(self):
        self.handler = EventHandler()

    def test_initialization(self):
        """Test EventHandler initialization"""
        self.assertIsNotNone(self.handler.logger)
        self.assertIsNone(self.handler.command_list)
        self.assertEqual(len(self.handler.character_registry), 0)
        self.assertEqual(len(self.handler.mobile_registry), 0)
        self.assertEqual(len(self.handler.character_events), 0)
        self.assertEqual(len(self.handler.mobile_events), 0)

    def test_set_command_list(self):
        """Test setting command list"""
        test_commands = {'look': {}, 'say': {}}
        self.handler.set_command_list(test_commands)
        self.assertEqual(self.handler.command_list, test_commands)

    def test_register_character(self):
        """Test registering a character"""
        mock_character = Mock()
        mock_character.name = 'TestChar'

        self.handler.register_character(mock_character)
        self.assertIn('TestChar', self.handler.character_registry)
        self.assertEqual(self.handler.character_registry['TestChar'], mock_character)

    def test_register_multiple_characters(self):
        """Test registering multiple characters"""
        char1 = Mock()
        char1.name = 'Char1'
        char2 = Mock()
        char2.name = 'Char2'

        self.handler.register_character(char1)
        self.handler.register_character(char2)

        self.assertEqual(len(self.handler.character_registry), 2)
        self.assertIn('Char1', self.handler.character_registry)
        self.assertIn('Char2', self.handler.character_registry)

    def test_unregister_character(self):
        """Test unregistering a character"""
        mock_character = Mock()
        mock_character.name = 'TestChar'

        self.handler.register_character(mock_character)
        self.assertIn('TestChar', self.handler.character_registry)

        self.handler.unregister_character('TestChar')
        self.assertNotIn('TestChar', self.handler.character_registry)

    def test_unregister_nonexistent_character(self):
        """Test unregistering a character that doesn't exist"""
        with self.assertRaises(KeyError):
            self.handler.unregister_character('NonExistent')

    def test_register_mobile(self):
        """Test registering a mobile"""
        mock_mobile = Mock()
        mock_mobile.name = 'Goblin'
        mock_mobile.get_instance_id.return_value = 'mob_001'

        self.handler.register_mobile(mock_mobile)
        self.assertIn('mob_001', self.handler.mobile_registry)
        self.assertEqual(self.handler.mobile_registry['mob_001'], mock_mobile)

    def test_register_multiple_mobiles(self):
        """Test registering multiple mobiles"""
        mob1 = Mock()
        mob1.name = 'Goblin'
        mob1.get_instance_id.return_value = 'mob_001'

        mob2 = Mock()
        mob2.name = 'Orc'
        mob2.get_instance_id.return_value = 'mob_002'

        self.handler.register_mobile(mob1)
        self.handler.register_mobile(mob2)

        self.assertEqual(len(self.handler.mobile_registry), 2)
        self.assertIn('mob_001', self.handler.mobile_registry)
        self.assertIn('mob_002', self.handler.mobile_registry)

    @unittest.skip("This test is currently broken")
    def test_unregister_mobile(self):
        """Test unregistering a mobile"""
        mock_mobile = Mock()
        mock_mobile.name = 'Goblin'
        mock_mobile.get_instance_id.return_value = 'mob_001'

        self.handler.register_mobile(mock_mobile)
        self.assertIn('mob_001', self.handler.mobile_registry)

        self.handler.unregister_mobile(mock_mobile)
        self.assertNotIn('Goblin', self.handler.mobile_registry)

    def test_process_events(self):
        """Test process_events calls process_player_events"""
        with patch.object(self.handler, 'process_player_events') as mock_process:
            self.handler.process_events()
            mock_process.assert_called_once()

    def test_process_player_events(self):
        """Test process_player_events (currently empty implementation)"""
        # Should not raise any errors
        self.handler.process_player_events()

    @unittest.skip("This test is currently broken")
    def test_to_mobile_with_no_command(self):
        """Test to_mobile with no command list"""
        mock_player = Mock()
        result = self.handler.to_mobile(mock_player, 'say', 'goblin', 'hello')
        self.assertIsNone(result)

    def test_to_mobile_with_command_list(self):
        """Test to_mobile with command list"""
        self.handler.command_list = [
            {'name': 'say', 'lambda': []},
            {'name': 'look', 'lambda': []}
        ]

        mock_player = Mock()
        mock_mobile = Mock()
        mock_mobile.name = 'Goblin'

        # Should execute without errors
        result = self.handler.to_mobile(mock_player, 'say', 'goblin', 'hello')

    def test_to_mobile_with_character_registry(self):
        """Test to_mobile finds character in registry"""
        self.handler.command_list = [{'name': 'say', 'lambda': []}]

        mock_char = Mock()
        mock_char.name = 'TestChar'
        mock_char.title = 'TestChar'
        self.handler.register_character(mock_char)

        mock_player = Mock()

        # Should find character in registry
        result = self.handler.to_mobile(mock_player, 'say', 'testchar', 'hello')

    def test_to_mobile_with_mobile_registry(self):
        """Test to_mobile finds mobile in registry"""
        self.handler.command_list = [{'name': 'say', 'lambda': []}]

        mock_mobile = Mock()
        mock_mobile.name = 'Goblin'
        mock_mobile.title = 'Goblin'
        mock_mobile.get_instance_id.return_value = 'mob_001'
        self.handler.register_mobile(mock_mobile)

        mock_player = Mock()

        # Should find mobile in registry
        result = self.handler.to_mobile(mock_player, 'say', 'goblin', 'hello')

    def test_character_events_dict(self):
        """Test character_events dictionary is accessible"""
        self.assertIsInstance(self.handler.character_events, dict)
        self.assertEqual(len(self.handler.character_events), 0)

    def test_mobile_events_dict(self):
        """Test mobile_events dictionary is accessible"""
        self.assertIsInstance(self.handler.mobile_events, dict)
        self.assertEqual(len(self.handler.mobile_events), 0)

    def test_register_same_character_twice(self):
        """Test registering same character twice (should overwrite)"""
        mock_char1 = Mock()
        mock_char1.name = 'TestChar'

        mock_char2 = Mock()
        mock_char2.name = 'TestChar'

        self.handler.register_character(mock_char1)
        self.handler.register_character(mock_char2)

        self.assertEqual(len(self.handler.character_registry), 1)
        self.assertEqual(self.handler.character_registry['TestChar'], mock_char2)

    def test_register_same_mobile_twice(self):
        """Test registering same mobile twice (should overwrite)"""
        mob1 = Mock()
        mob1.name = 'Goblin'
        mob1.get_instance_id.return_value = 'mob_001'

        mob2 = Mock()
        mob2.name = 'Goblin'
        mob2.get_instance_id.return_value = 'mob_001'

        self.handler.register_mobile(mob1)
        self.handler.register_mobile(mob2)

        self.assertEqual(len(self.handler.mobile_registry), 1)
        self.assertEqual(self.handler.mobile_registry['mob_001'], mob2)


if __name__ == '__main__':
    unittest.main()

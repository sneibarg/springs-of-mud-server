"""
Unit tests for session management (SessionState, SessionHandler).
"""
import unittest
from datetime import datetime, timedelta
from server.session import SessionState, SessionPhase, SessionHandler


class TestSessionState(unittest.TestCase):
    """Test suite for SessionState class"""

    def test_session_state_creation(self):
        """Test basic session state creation"""
        session = SessionState(session_id='test-123')

        self.assertEqual(session.session_id, 'test-123')
        self.assertEqual(session.phase, SessionPhase.CONNECTED)
        self.assertIsNone(session.player_id)
        self.assertIsNone(session.character_id)
        self.assertFalse(session.ansi_enabled)
        self.assertEqual(session.auth_attempts, 0)
        self.assertIsInstance(session.connected_at, datetime)
        self.assertIsInstance(session.last_activity, datetime)

    def test_session_state_with_values(self):
        """Test session state with initial values"""
        session = SessionState(
            session_id='test-456',
            phase=SessionPhase.PLAYING,
            player_id='player-789',
            character_id='char-101',
            ansi_enabled=True
        )

        self.assertEqual(session.phase, SessionPhase.PLAYING)
        self.assertEqual(session.player_id, 'player-789')
        self.assertEqual(session.character_id, 'char-101')
        self.assertTrue(session.ansi_enabled)

    def test_update_activity(self):
        """Test updating last activity timestamp"""
        session = SessionState(session_id='test-123')
        original_time = session.last_activity

        # Wait a tiny bit
        import time
        time.sleep(0.01)

        session.update_activity()

        self.assertGreater(session.last_activity, original_time)

    def test_is_authenticated(self):
        """Test is_authenticated method"""
        session = SessionState(session_id='test-123')
        self.assertFalse(session.is_authenticated())

        session.player_id = 'player-456'
        self.assertTrue(session.is_authenticated())

    def test_is_playing(self):
        """Test is_playing method"""
        session = SessionState(session_id='test-123')
        self.assertFalse(session.is_playing())

        session.phase = SessionPhase.PLAYING
        self.assertTrue(session.is_playing())

        session.phase = SessionPhase.AUTHENTICATING
        self.assertFalse(session.is_playing())

    def test_can_authenticate_new_session(self):
        """Test can_authenticate for new session"""
        session = SessionState(session_id='test-123')
        self.assertTrue(session.can_authenticate())

    def test_can_authenticate_with_attempts(self):
        """Test can_authenticate with failed attempts"""
        session = SessionState(session_id='test-123')

        session.auth_attempts = 1
        self.assertTrue(session.can_authenticate())

        session.auth_attempts = 2
        self.assertTrue(session.can_authenticate())

        session.auth_attempts = 3
        self.assertFalse(session.can_authenticate())

    def test_can_authenticate_wrong_phase(self):
        """Test can_authenticate in wrong phase"""
        session = SessionState(session_id='test-123')

        # Should work in CONNECTED phase
        session.phase = SessionPhase.CONNECTED
        self.assertTrue(session.can_authenticate())

        # Should work in AUTHENTICATING phase
        session.phase = SessionPhase.AUTHENTICATING
        self.assertTrue(session.can_authenticate())

        # Should not work in PLAYING phase
        session.phase = SessionPhase.PLAYING
        self.assertFalse(session.can_authenticate())

    def test_metadata(self):
        """Test metadata dictionary"""
        session = SessionState(session_id='test-123')

        session.metadata['custom_key'] = 'custom_value'
        session.metadata['count'] = 42

        self.assertEqual(session.metadata['custom_key'], 'custom_value')
        self.assertEqual(session.metadata['count'], 42)


class TestSessionPhase(unittest.TestCase):
    """Test suite for SessionPhase enum"""

    def test_session_phases_exist(self):
        """Test that expected session phases exist"""
        expected_phases = [
            'CONNECTED', 'AUTHENTICATING', 'PLAYING', 'DISCONNECTING', 'DISCONNECTED'
        ]

        for phase_name in expected_phases:
            self.assertTrue(
                hasattr(SessionPhase, phase_name),
                f"SessionPhase.{phase_name} should exist"
            )

    def test_session_phase_values_unique(self):
        """Test that all session phase values are unique"""
        values = [sp.value for sp in SessionPhase]
        self.assertEqual(len(values), len(set(values)))


class TestSessionHandler(unittest.TestCase):
    """Test suite for SessionHandler class"""

    def setUp(self):
        """Set up test fixtures"""
        self.handler = SessionHandler()

    def test_create_session(self):
        """Test creating a new session"""
        session = self.handler.create_session('session-123')

        self.assertEqual(session.session_id, 'session-123')
        self.assertEqual(session.phase, SessionPhase.CONNECTED)

    def test_get_session(self):
        """Test retrieving a session"""
        self.handler.create_session('session-123')

        session = self.handler.get_session('session-123')

        self.assertIsNotNone(session)
        self.assertEqual(session.session_id, 'session-123')

    def test_get_nonexistent_session(self):
        """Test retrieving a session that doesn't exist"""
        session = self.handler.get_session('nonexistent')

        self.assertIsNone(session)

    def test_get_session_by_player(self):
        """Test retrieving session by player ID"""
        session = self.handler.create_session('session-123')
        session.player_id = 'player-456'

        retrieved = self.handler.get_session_by_player('player-456')

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.session_id, 'session-123')
        self.assertEqual(retrieved.player_id, 'player-456')

    def test_get_session_by_nonexistent_player(self):
        """Test retrieving session for nonexistent player"""
        retrieved = self.handler.get_session_by_player('nonexistent')

        self.assertIsNone(retrieved)

    def test_remove_session(self):
        """Test removing a session"""
        self.handler.create_session('session-123')
        self.assertIsNotNone(self.handler.get_session('session-123'))

        self.handler.remove_session('session-123')

        self.assertIsNone(self.handler.get_session('session-123'))

    def test_remove_session_sets_disconnected(self):
        """Test that removing session sets phase to DISCONNECTED"""
        session = self.handler.create_session('session-123')
        session.phase = SessionPhase.PLAYING

        self.handler.remove_session('session-123')

        self.assertEqual(session.phase, SessionPhase.DISCONNECTED)

    def test_get_active_sessions(self):
        """Test getting all active sessions"""
        session1 = self.handler.create_session('session-1')
        session2 = self.handler.create_session('session-2')
        session3 = self.handler.create_session('session-3')

        # Disconnect one
        session3.phase = SessionPhase.DISCONNECTED

        active = self.handler.get_active_sessions()

        self.assertEqual(len(active), 2)
        self.assertIn(session1, active)
        self.assertIn(session2, active)
        self.assertNotIn(session3, active)

    def test_get_playing_sessions(self):
        """Test getting all playing sessions"""
        session1 = self.handler.create_session('session-1')
        session2 = self.handler.create_session('session-2')
        session3 = self.handler.create_session('session-3')

        session1.phase = SessionPhase.PLAYING
        session2.phase = SessionPhase.AUTHENTICATING
        session3.phase = SessionPhase.PLAYING

        playing = self.handler.get_playing_sessions()

        self.assertEqual(len(playing), 2)
        self.assertIn(session1, playing)
        self.assertNotIn(session2, playing)
        self.assertIn(session3, playing)

    def test_session_count(self):
        """Test session count"""
        self.assertEqual(self.handler.session_count(), 0)

        self.handler.create_session('session-1')
        self.assertEqual(self.handler.session_count(), 1)

        self.handler.create_session('session-2')
        self.handler.create_session('session-3')
        self.assertEqual(self.handler.session_count(), 3)

        self.handler.remove_session('session-2')
        self.assertEqual(self.handler.session_count(), 2)

    def test_update_session_activity(self):
        """Test updating session activity timestamp"""
        session = self.handler.create_session('session-123')
        original_time = session.last_activity

        import time
        time.sleep(0.01)

        self.handler.update_session_activity('session-123')

        self.assertGreater(session.last_activity, original_time)

    def test_update_nonexistent_session_activity(self):
        """Test updating activity for nonexistent session (should not crash)"""
        # Should handle gracefully
        self.handler.update_session_activity('nonexistent')

    def test_multiple_players(self):
        """Test handling multiple players"""
        session1 = self.handler.create_session('session-1')
        session1.player_id = 'player-A'
        session1.phase = SessionPhase.PLAYING

        session2 = self.handler.create_session('session-2')
        session2.player_id = 'player-B'
        session2.phase = SessionPhase.PLAYING

        # Both should be in playing sessions
        playing = self.handler.get_playing_sessions()
        self.assertEqual(len(playing), 2)

        # Should be able to find by player ID
        found1 = self.handler.get_session_by_player('player-A')
        found2 = self.handler.get_session_by_player('player-B')

        self.assertEqual(found1.session_id, 'session-1')
        self.assertEqual(found2.session_id, 'session-2')


if __name__ == '__main__':
    unittest.main()

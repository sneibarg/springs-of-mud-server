import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests.test_update_handler_active_players import Character, build_character_data
from server.handlers.ConnectionHandler import ConnectionHandler
from server.connection.ConnectionManager import ConnectionManager
from server.connection.TelnetConnection import TelnetConnection
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus
from server.protocol.Message import Message, MessageType
from game.EntityUpdateHandler import EntityUpdateHandler
from server.session.AuthenticationService import AuthenticationService


class ReconnectTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.character = Character.from_json(build_character_data())
        self.viewer = Character.from_json(build_character_data('viewer'))
        self.room = SimpleNamespace(characters={self.character.id: self.character, 'viewer': self.viewer},
                                    players_in_room=lambda: [self.character, self.viewer], mobiles={})
        self.account = SimpleNamespace(banned=False, current_characters=[self.character], first_name='Test', last_name='Account')
        self.playing = {self.character.id: self.character}
        self.registries = SimpleNamespace(
            room_registry=SimpleNamespace(all_rooms=lambda: [self.room], get_or_none=lambda **kw: self.room),
            area_registry=SimpleNamespace(get_or_none=lambda **kw: object()),
            player_registry=SimpleNamespace(get_or_none=lambda **kw: self.account, get=lambda **kw: self.account),
            character_registry=SimpleNamespace(set_playing=lambda ch: self.playing.update({ch.id: ch}),
                                               remove_playing=lambda ch: self.playing.pop(ch.id, None)))
        self.manager = ConnectionManager()
        self.sessions = SessionHandler()
        self.bus = Mock(send_to_character=AsyncMock(), send_prompt=AsyncMock(), text_to_message=lambda text: text)
        self.wiz = Mock(wiznet_targets=Mock(return_value=[]))
        self.handler = ConnectionHandler(self.manager, self.sessions, self.bus, self.registries,
                                         Mock(), Mock(), Mock(), Mock(), self.wiz)
        self.patches = [patch('server.handlers.ConnectionHandler.GameApi.check_ban', return_value=False),
                        patch('server.handlers.ConnectionHandler.CharacterApi.get_enum', return_value=SimpleNamespace(POS_RESTING=SimpleNamespace(value=5))),
                        patch('server.handlers.ConnectionHandler.CharacterApi.position_value', return_value=8),
                        patch('server.handlers.ConnectionHandler.CharacterApi.can_see', return_value=True)]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def connection(self, sid, attached=False, answers=()):
        connection = Mock(session_id=sid, is_closed=Mock(return_value=False), send_text=AsyncMock(),
                          receive_message=AsyncMock(side_effect=list(answers)), get_peer_info=Mock(return_value=('local', 1)))
        async def close():
            connection.is_closed.return_value = True
        connection.close = AsyncMock(side_effect=close)
        session = self.sessions.create_session(sid)
        session.player_id = 'acct_001'
        self.manager.add_connection(connection)
        if attached:
            session.character = self.character
            session.status = SessionStatus.PLAYING
            self.manager.bind_character(self.character.id, sid)
        return connection, session

    async def test_link_loss_keeps_live_character_and_announces_rom_message(self):
        _, session = self.connection('old', True)
        self.character.hit = 7
        await self.handler._cleanup_session(session)
        self.assertIs(self.room.characters[self.character.id], self.character)
        self.assertIs(self.playing[self.character.id], self.character)
        self.assertEqual(self.character.hit, 7)
        self.assertIsNone(self.manager.get_connection_by_character(self.character.id))
        self.assertEqual(self.account.current_characters, [])
        self.bus.send_to_character.assert_awaited_once_with('viewer', 'Tester has lost his link.\r\n')

    async def test_link_loss_and_reconnect_preserve_area_occupancy(self):
        from area.Area import Area
        from area.Room import Room

        area = Area(author='ROM', name='Test', id=self.character.area_id, empty=True)
        self.room = Room(id=self.character.room_id, area_id=area.id)
        self.room.bind_area(area)
        self.room.add_player_to_room(self.character)
        _, old_session = self.connection('old', True)
        area.age = 9
        await self.handler._cleanup_session(old_session)
        self.assertEqual((area.number_of_players, area.empty, area.age), (1, False, 9))
        connection, session = self.connection('new')
        await self.handler._attach_character(self.character, session, connection)
        self.assertEqual((area.number_of_players, area.empty, area.age), (1, False, 9))
        self.room.remove_player_from_room(self.character)
        await self.handler._cleanup_session(session)
        self.assertEqual(area.number_of_players, 0)

    async def test_reconnect_uses_live_character_and_rom_messages(self):
        connection, session = self.connection('new')
        stale = Character.from_json(build_character_data())
        self.character.hit = 7
        _, actual = await self.handler._attach_character(stale, session, connection)
        self.assertIs(actual, self.character)
        self.assertEqual(actual.hit, 7)
        self.assertTrue(session.metadata['entered_world'])
        self.assertIs(self.manager.get_connection_by_character(actual.id), connection)
        self.assertEqual([call.args for call in self.bus.send_to_character.await_args_list], [
            (actual.id, 'Reconnecting. Type replay to see missed tells.\r\n'),
            ('viewer', 'Tester has reconnected.\r\n')])

    async def test_takeover_confirms_and_late_cleanup_cannot_unbind_new_session(self):
        old, old_session = self.connection('old', True)
        new, new_session = self.connection('new', answers=[Message(MessageType.GAME, {'text': 'maybe'}), Message(MessageType.GAME, {'text': 'Y'})])
        await self.handler._attach_character(self.character, new_session, new)
        old.close.assert_awaited_once()
        self.assertEqual([c.args[0] for c in new.send_text.await_args_list], [
            'That character is already playing.\r\n', 'Do you wish to connect anyway (Y/N)?', 'Please type Y or N? '])
        await self.handler._cleanup_session(old_session)
        self.manager.unbind_character(self.character.id, session_id='old')
        self.assertIs(self.manager.get_connection_by_character(self.character.id), new)
        self.assertEqual(self.account.current_characters, [self.character])
        self.assertEqual([c.args[1] for c in self.bus.send_to_character.await_args_list], [
            'Tester has lost his link.\r\n', 'Reconnecting. Type replay to see missed tells.\r\n', 'Tester has reconnected.\r\n'])

    async def test_declining_takeover_preserves_old_connection(self):
        old, old_session = self.connection('old', True)
        new, new_session = self.connection('new', answers=[Message(MessageType.GAME, {'text': 'N'})])
        self.assertIsNone(await self.handler._attach_character(self.character, new_session, new))
        await self.handler._cleanup_session(new_session)
        self.assertIs(self.manager.get_connection_by_character(self.character.id), old)
        self.assertTrue(old_session.is_playing())
        old.close.assert_not_awaited()
        self.bus.send_to_character.assert_not_awaited()

    async def test_quit_removal_does_not_announce_link_loss(self):
        _, session = self.connection('old', True)
        self.room.characters.pop(self.character.id)
        await self.handler._cleanup_session(session)
        self.assertNotIn(self.character.id, self.playing)
        self.bus.send_to_character.assert_not_awaited()

    async def test_full_reconnect_skips_room_entry_and_aggression(self):
        connection, session = self.connection('new')
        self.handler._receive_initial_message = AsyncMock(return_value=(True, 'acct_001', self.character))
        self.handler._game_loop = AsyncMock()
        with patch('server.handlers.ConnectionHandler.TelnetConnection', return_value=connection), \
                patch.object(self.sessions, 'create_session', return_value=session), \
                patch.object(self.handler, '_peer_denied', return_value=False):
            await self.handler.handle_new_connection(Mock(), Mock())
        self.handler.room_handler.print_room.assert_not_called()
        self.handler.fight_handler.aggressive_entry_rounds.assert_not_called()
        self.handler._game_loop.assert_awaited_once()
        self.assertIs(self.room.characters[self.character.id], self.character)

    async def test_banned_account_cannot_replace_live_connection(self):
        old, _ = self.connection('old', True)
        new, session = self.connection('new')
        self.account.banned = True
        self.assertIsNone(await self.handler._attach_character(self.character, session, new))
        self.assertIs(self.manager.get_connection_by_character(self.character.id), old)
        old.close.assert_not_awaited()

    async def test_snoop_disconnect_notification_and_cleanup(self):
        _, session = self.connection('old', True)
        snooper, _ = self.connection('snooper')
        _, victim = self.connection('victim')
        session.metadata['snoop_by_session_id'] = 'snooper'
        victim.metadata['snoop_by_session_id'] = 'old'
        await self.handler._cleanup_session(session)
        snooper.send_text.assert_awaited_once_with('Your victim has left the game.\r\n')
        self.assertNotIn('snoop_by_session_id', victim.metadata)

    async def test_authentication_uses_live_character_only_for_authorized_account(self):
        service = AuthenticationService(Mock(), SimpleNamespace(playing=self.playing, get=Mock()))
        self.assertIs(service._get_character_by_id(self.character.id, [self.character.id]), self.character)
        self.assertIsNone(service._get_character_by_id(self.character.id, ['another-character']))
        service.character_registry.get.assert_not_called()

    async def test_wiznet_link_messages(self):
        self.wiz.wiznet_targets.return_value = [SimpleNamespace(id='immortal')]
        self.wiz.decorate_wiznet_text.side_effect = lambda recipient, text: text
        await self.handler._announce_link(self.character, 'lost')
        await self.handler._announce_link(self.character, 'reconnect')
        messages = [call.args for call in self.bus.send_to_character.await_args_list if call.args[0] == 'immortal']
        self.assertEqual(messages, [('immortal', 'Net death has claimed Tester.\r\n'),
                                    ('immortal', 'Tester groks the fullness of his link.\r\n')])
        self.wiz.wiznet_targets.assert_called_with(self.character, flag_name='WIZ_LINKS')

    async def test_hidden_character_and_sleeping_observers(self):
        with patch('server.handlers.ConnectionHandler.CharacterApi.can_see', return_value=False):
            await self.handler._announce_link(self.character, 'lost')
        self.bus.send_to_character.assert_awaited_once_with('viewer', 'Someone has lost his link.\r\n')
        self.bus.send_to_character.reset_mock()
        with patch('server.handlers.ConnectionHandler.CharacterApi.position_value', return_value=4):
            await self.handler._announce_link(self.character, 'lost')
        self.bus.send_to_character.assert_not_awaited()

    async def test_linkdead_characters_keep_ticking_without_double_ticks(self):
        handler = EntityUpdateHandler.__new__(EntityUpdateHandler)
        handler.room_registry = self.registries.room_registry
        handler.tick = AsyncMock()
        await handler.update([self.viewer])
        self.assertEqual([c.args[0].id for c in handler.tick.await_args_list], ['viewer', self.character.id])

    async def test_eof_marked_connection_still_closes_writer(self):
        connection = TelnetConnection.__new__(TelnetConnection)
        connection._closed = True
        connection.owner_loop = None
        connection.writer = Mock(is_closing=Mock(return_value=False), wait_closed=AsyncMock())
        await connection.close()
        connection.writer.close.assert_called_once()
        connection.writer.wait_closed.assert_awaited_once()


if __name__ == '__main__':
    unittest.main()

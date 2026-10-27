import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_review_application_fixes import RuntimeFixture
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from game.GameData import GameData
from game.GameService import GameService
from game.SiteBans import SiteBans
from interp.CommandAccess import CommandAccess
from interp.commands.Wiz import Wiz
from player.CharacterRegistry import CharacterRegistry
from server.handlers.ConnectionHandler import ConnectionHandler
from server.connection.ConnectionManager import ConnectionManager
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus


class SiteBanPolicyTests(unittest.TestCase):
    def test_exact_prefix_suffix_and_substring_are_case_insensitive_and_type_specific(self):
        for pattern, host, other in [('EXAMPLE.COM', 'example.com', 'notexample.com'),
                                     ('*.example.com', 'a.example.com', 'example.com.bad'),
                                     ('192.0.2.*', '192.0.2.17', '1192.0.2.17'),
                                     ('*example*', 'a.example.com', 'other.com')]:
            with self.subTest(pattern=pattern):
                policy = SiteBans()
                self.assertEqual('default', policy.ban_site(pattern, 'p', 59, True)[0])
                self.assertTrue(policy.check_ban(host.upper(), 'permit'))
                self.assertFalse(policy.check_ban(other, 'permit'))
                self.assertFalse(policy.check_ban(host, 'all'))

    def test_temporary_rules_do_not_survive_roundtrip_and_last_permanent_removal_persists(self):
        policy = SiteBans()
        policy.ban_site('temp', '', 58)
        policy.ban_site('*permanent*', 'n', 59, True)
        restored = SiteBans()
        restored.load_bans(policy.save_bans())
        self.assertFalse(restored.check_ban('temp'))
        self.assertTrue(restored.check_ban('permanent.example', 'newbies'))
        self.assertEqual('removed', restored.allow('permanent', 59))
        self.assertEqual([], restored.save_bans())

    def test_trust_protects_replacement_and_removal(self):
        policy = SiteBans()
        policy.ban_site('*example', 'all', 60, True)
        self.assertEqual('insufficient_level', policy.ban_site('example*', 'permit', 59)[0])
        self.assertEqual('insufficient_level', policy.allow('example', 59))
        self.assertEqual('default', policy.ban_site('example*', 'permit', 60)[0])
        self.assertEqual(1, len(policy.entries))
        self.assertEqual('removed', policy.allow('EXAMPLE', 60))

    def test_invalid_patterns_and_types_leave_state_unchanged(self):
        policy = SiteBans()
        for pattern in ('*', '**', 'foo*bar', ''):
            self.assertEqual('no_argument', policy.ban_site(pattern, 'all', 60)[0])
        self.assertEqual('invalid_option', policy.ban_site('host', 'everything', 60)[0])
        self.assertEqual([], policy.entries)
        self.assertEqual('no_such_ban', policy.allow('host', 60))

    def test_load_is_atomic_on_invalid_record(self):
        policy = SiteBans()
        policy.ban_site('old', 'all', 60)
        with self.assertRaises(ValueError):
            policy.load_bans([dict(name='new', level=60), dict(name='', level=60)])
        self.assertTrue(policy.check_ban('old'))


class SiteBanRuntimeTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.actor.level, self.actor.trust, self.actor.role = 60, 60, 'immortal'
        self.wiz = Wiz.__new__(Wiz)
        self.wiz.interp_api = self.api
        self.wiz.game_service = NS(queue_save_bans=Mock())
        self.account = NS(banned=False, current_characters=[], first_name='Test', last_name='Account')
        self.handler = ConnectionHandler.__new__(ConnectionHandler)
        self.handler.logger = Mock()
        self.handler.registry_service = NS(player_registry=NS(get_or_none=lambda **kwargs: self.account,
                                                             get=lambda **kwargs: self.account),
                                           character_registry=CharacterRegistry(), room_registry=self.rooms)
        self.handler.session_handler = SessionHandler()

    def run_command(self, name, text):
        context = self.context(name, text)
        self.assertIsNone(CommandAccess.check(self.actor, context.command))
        return self.wiz.execute(self.actor, context)

    def test_commands_use_site_first_syntax_and_persist_without_account_ban(self):
        result = self.run_command('ban', '192.0.2.* permit')
        self.assertEqual('default', result['message_key'])
        self.assertFalse(self.account.banned)
        self.assertTrue(GameApi.check_ban('192.0.2.7', 'permit'))
        self.assertFalse(GameApi.site_bans().entries[0].permanent)
        self.run_command('permban', '*.example.com newbies')
        self.assertTrue(GameApi.site_bans().entries[0].permanent)
        listing = self.run_command('ban', '')['to_char']
        self.assertIn('*.example.com', listing)
        self.assertIn('newbies', listing)
        self.assertIn('perm', listing)
        self.assertIn('temp', listing)
        self.assertEqual('removed', self.run_command('allow', '.example.com')['message_key'])
        self.assertEqual(3, self.wiz.game_service.queue_save_bans.call_count)

    def test_immortal_command_levels_and_lower_setter_trust(self):
        self.actor.level, self.actor.trust, self.actor.role = 10, 0, 'player'
        for name in ('ban', 'allow', 'permban'):
            self.assertIsNotNone(CommandAccess.check(self.actor, self.command(name)))
        self.actor.level, self.actor.trust, self.actor.role = 58, 58, 'immortal'
        self.assertIsNone(CommandAccess.check(self.actor, self.command('ban')))
        self.assertIsNotNone(CommandAccess.check(self.actor, self.command('permban')))
        GameApi.site_bans().ban_site('host', 'all', 60, True)
        result = self.run_command('allow', 'host')
        self.assertEqual('insufficient_level', result['message_key'])
        self.wiz.game_service.queue_save_bans.assert_not_called()

    def test_legacy_deny_list_is_enforced_and_can_be_allowed(self):
        GameApi.add_denied_site('192.0.2.*')
        self.assertTrue(ConnectionHandler._peer_denied(('192.0.2.7', 123)))
        self.run_command('allow', '192.0.2.*')
        self.assertFalse(GameApi.check_ban('192.0.2.7'))

    async def test_permit_admission_rejects_once_then_allows_flagged_character(self):
        GameApi.site_bans().ban_site('192.0.2.*', 'permit', 60)
        session = self.handler.session_handler.create_session('blocked')
        session.player_id = 'account'
        connection = NS(send_text=AsyncMock(), close=AsyncMock(), get_peer_info=lambda: ('192.0.2.7', 1))
        self.assertIsNone(await self.handler._nanny(self.actor, session, connection))
        self.assertIsNone(await self.handler._nanny(self.actor, session, connection))
        connection.send_text.assert_awaited_once()
        connection.close.assert_awaited_once()
        self.assertEqual(SessionStatus.DISCONNECTING, session.status)
        self.assertIsNone(session.character)
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_PERMIT)
        session = self.handler.session_handler.create_session('allowed')
        session.player_id = 'account'
        self.assertIs(self.account, await self.handler._nanny(self.actor, session, connection))
        self.assertTrue(session.is_playing())

    def test_all_ban_overrides_permit_newbies_does_not_deny_existing_characters(self):
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_PERMIT)
        GameApi.site_bans().ban_site('192.0.2.*', 'all', 60)
        self.assertIn('site has been banned', self.handler._login_error(self.actor, self.account, ('192.0.2.1', 1)))
        GameApi.site_bans().ban_site('192.0.2.*', 'newbies', 60)
        self.assertEqual('', self.handler._login_error(self.actor, self.account, ('192.0.2.1', 1)))
        self.account.banned = True
        self.assertIn('banned from the server', self.handler._login_error(self.actor, self.account))
        self.account.banned = False
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_DENY)
        self.assertIn('denied access', self.handler._login_error(self.actor, self.account))

    def test_game_data_loading_and_prepared_save_snapshot(self):
        record = dict(self.game_document, bans=[dict(name='host', level=60, type='permit', prefix=True)])
        game = GameService.__new__(GameService)
        game.game_data = GameData.from_json(record)
        self.assertTrue(game.game_data.site_bans.check_ban('myhost', 'permit'))
        with patch('game.GameService.submit') as submit:
            game.queue_save_bans()
        payload = submit.call_args.args[2]
        game.game_data.site_bans.allow('host', 60)
        self.assertEqual('host', payload['bans'][0]['name'])
        self.assertEqual([], game.game_data.site_bans.save_bans())

    async def test_all_site_rejected_before_welcome_or_authentication(self):
        GameApi.site_bans().ban_site('192.0.2.*', 'all', 60)
        connection = NS(session_id='blocked-peer', get_peer_info=lambda: ('192.0.2.7', 1),
                        close=AsyncMock(), send_text=AsyncMock())
        self.handler.connection_manager = ConnectionManager()
        self.handler._send_welcome = AsyncMock()
        self.handler._receive_initial_message = AsyncMock()
        with patch('server.handlers.ConnectionHandler.TelnetConnection', return_value=connection):
            await self.handler.handle_new_connection(None, None)
        self.handler._send_welcome.assert_not_awaited()
        self.handler._receive_initial_message.assert_not_awaited()
        connection.send_text.assert_awaited_once()
        self.assertEqual([], list(self.handler.session_handler.get_active_sessions()))

    async def test_permit_rejection_precedes_existing_connection_takeover(self):
        GameApi.site_bans().ban_site('192.0.2.*', 'permit', 60)
        session = self.handler.session_handler.create_session('takeover')
        session.player_id = 'account'
        connection = NS(send_text=AsyncMock(), close=AsyncMock(), get_peer_info=lambda: ('192.0.2.7', 1))
        self.handler._existing_connection = Mock()
        self.assertIsNone(await self.handler._attach_character(self.actor, session, connection))
        self.handler._existing_connection.assert_not_called()
        self.assertIs(self.actor, self.room.characters[self.actor.id])

    async def test_domain_resolution_is_async_and_ip_policy_is_still_checked(self):
        GameApi.site_bans().ban_site('*.example.com', 'permit', 60)
        with patch('server.handlers.ConnectionHandler.socket.gethostbyaddr', return_value=('peer.example.com', [], [])) as lookup:
            host = await self.handler._resolve_peer_host(('192.0.2.7', 1))
        lookup.assert_called_once_with('192.0.2.7')
        self.assertEqual('peer.example.com', host)
        self.assertIn('banned', self.handler._login_error(self.actor, self.account, ('192.0.2.7', 1), host))
        with patch('server.handlers.ConnectionHandler.socket.gethostbyaddr', side_effect=OSError):
            self.assertEqual('192.0.2.7', await self.handler._resolve_peer_host(('192.0.2.7', 1)))
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_PERMIT)
        GameApi.site_bans().ban_site('192.0.2.*', 'all', 60)
        self.assertIn('banned', self.handler._login_error(self.actor, self.account, ('192.0.2.7', 1), host))

    def test_failed_persistence_reports_failure_and_keeps_in_memory_rules(self):
        import requests
        GameApi.site_bans().ban_site('host', 'all', 60, True)
        game = GameService.__new__(GameService)
        game.game_data = GameApi._game_data
        game.game_data_endpoint = 'http://content.invalid/game'
        game.logger = Mock()
        with patch('game.GameService.requests.patch', side_effect=requests.Timeout):
            self.assertFalse(game._persist_deny_list('game', {'bans': game.game_data.site_bans.save_bans()}))
        self.assertTrue(GameApi.check_ban('host'))
        game.logger.error.assert_called_once()

    def test_older_account_ban_payload_cannot_emit_victim_or_wiznet_messages(self):
        GameApi.site_bans().ban_site('host', 'all', 60, True)
        context = self.context('ban', '')
        context.command.payload.to_char.pop('list_header')
        context.command.payload.to_char.pop('list_row')
        context.command.guards = [dict(predicate="lambda v: True", message_key='target_missing')]
        result = self.wiz.do_ban(self.actor, context)
        self.assertIn('Banned sites', result['to_char'])
        self.assertIn('host', result['to_char'])
        context = self.context('ban', 'host')
        context.command.payload.to_char.pop('insufficient_level')
        self.actor.trust = 58
        result = self.wiz.do_ban(self.actor, context)
        self.assertEqual('to_char', result['channel'])
        self.assertEqual('That ban was set by a higher power.', result['fallback'])
        self.assertNotIn('disconnect_character', result)

    def test_durable_snapshot_http_contract(self):
        GameApi.site_bans().ban_site('host', 'all', 60, True)
        GameApi.site_bans().ban_site('temporary', 'permit', 60)
        game = GameService.__new__(GameService)
        game.game_data = GameApi._game_data
        game.game_data_endpoint = 'http://content.invalid/game'
        game.logger = Mock()
        with patch('game.GameService.submit') as submit:
            game.queue_save_bans()
        operation, identifier, payload = submit.call_args.args
        with patch('game.GameService.requests.patch', return_value=Mock()) as request:
            self.assertTrue(operation(identifier, payload))
        self.assertEqual(['host'], [entry['name'] for entry in payload['bans']])
        request.assert_called_once_with(f'{game.game_data_endpoint}/{identifier}', json=payload, timeout=10)


if __name__ == '__main__':
    unittest.main()

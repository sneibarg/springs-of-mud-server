import asyncio
import json
import threading
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

import requests

from tests.test_update_handler_active_players import Character, build_character_data
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from api.InterpApi import InterpApi
from area.Room import Room
from area.RoomService import RoomService
from devtools.collection_query import load_collections
from game.AnimateEntity import RegenerationContext
from game.EnumProvider import EnumProvider
from game.GameData import GameData
from interp.Command import Command
from interp.CommandAccess import CommandAccess
from interp.CommandExecutor import CommandExecutor
from interp.Context import Context
from interp.InterpHandler import InterpHandler
from interp.commands.Communications import Communications
from interp.commands.Info import Info
from mobile.Mobile import Mobile
from notes.InGameNote import InGameNote
from notes.NoteHandler import NoteHandler
from player.CharacterRegistry import CharacterRegistry
from player.CharacterService import CharacterService
from player.PlayerHandler import PlayerHandler
from server.connection.ConnectionManager import ConnectionManager
from server.handlers.ConnectionHandler import ConnectionHandler
from server.session.SessionHandler import SessionHandler
from server.session.AuthenticationService import AuthenticationService
from server.session.SessionState import SessionStatus
from util.GenericUtil import GenericUtil


ROOT = Path(__file__).resolve().parents[1]


class RuntimeFixture:
    @classmethod
    def setUpClass(cls):
        collections = load_collections(ROOT / 'resources/collections', ['commands', 'gamedata'])
        cls.documents = {doc['name']: doc for doc in collections['commands'].documents}
        cls.game_document = collections['gamedata'].documents[0]

    def setUp(self):
        GameApi.reset_for_tests()
        self.addCleanup(GameApi.reset_for_tests)
        data = GameData.from_json(deepcopy(self.game_document))
        self.enums = EnumProvider({name: GenericUtil.build_int_enum(name, values)
                                  for name, values in data.enums.items()})
        GameApi.configure(data, self.enums)
        CharacterApi.lazy_load(None, NS())
        self.actor = self.character('actor')
        self.room = Room(id=self.actor.room_id, area_id=self.actor.area_id)
        self.room.add_player_to_room(self.actor)
        self.rooms = NS(all_rooms=lambda: [self.room], get_or_none=lambda **kw: self.room)
        self.api = InterpApi()

    def character(self, name):
        document = build_character_data(name)
        document['name'] = name
        return Character.from_json(document)

    def command(self, name):
        data = deepcopy(self.documents[name])
        for key, value in [('shortcuts', ''), ('usage', ''), ('function', [])]:
            data.setdefault(key, value)
        return Command.from_json(data)

    def context(self, name, text=''):
        return Context(character=self.actor, command=self.command(name), room=self.room,
                       result=text, parameters=[], conn=NS(close=AsyncMock(), is_closed=lambda: False))


class QuitPersistenceTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.registry = CharacterRegistry()
        self.registry.register(self.actor)
        self.registry.set_playing(self.actor)
        self.service = CharacterService.__new__(CharacterService)
        self.service.logger = Mock()
        self.service.characters_endpoint = 'http://content.invalid/characters'
        self.service.character_registry = self.registry
        info = Info.__new__(Info)
        info.interp_api = self.api
        self.handler = PlayerHandler.__new__(PlayerHandler)
        self.handler.info_commands = info
        self.handler.interp_api = self.api
        self.handler.character_service = self.service
        self.handler.character_registry = self.registry
        self.handler.room_registry = self.rooms
        self.sessions = SessionHandler()
        self.session = self.sessions.create_session('quit-session')
        self.session.character, self.session.status = self.actor, SessionStatus.PLAYING
        self.handler.message_bus = Mock(text_to_message=lambda text: text,
                                        send_to_character=AsyncMock(), session_handler=self.sessions)

    async def test_quit_persists_final_currency_and_notes_before_disconnect(self):
        self.actor.gold = 314
        self.actor.mark_note_read(0, 123)
        context = self.context('quit')
        snapshots = []

        def persist(_url, *, json, timeout):
            snapshots.append(deepcopy(json))
            self.assertNotIn(self.actor.id, self.room.characters)
            self.assertFalse(self.sessions.get_playing_sessions())
            return Mock()

        with patch('player.CharacterService.requests.put', side_effect=persist):
            await self.handler.do_quit(self.actor, context)
        restored = Character.from_json(json.loads(json.dumps(snapshots[0])))
        self.assertEqual(314, restored.gold)
        self.assertEqual(123, restored.note_read_stamp(0))
        self.assertNotIn(self.actor.id, self.room.characters)
        self.assertNotIn(self.actor.id, self.registry.playing)
        context.conn.close.assert_awaited_once()

    async def test_failed_final_save_keeps_character_playing_and_renders_content_message(self):
        context = self.context('quit')
        with patch('player.CharacterService.requests.put', side_effect=requests.Timeout):
            await self.handler.do_quit(self.actor, context)
        self.assertIs(self.room.characters[self.actor.id], self.actor)
        self.assertIs(self.registry.playing[self.actor.id], self.actor)
        self.assertTrue(self.session.is_playing())
        self.assertNotIn('quitting', self.session.metadata)
        context.conn.close.assert_not_awaited()
        expected = context.command.render_message('to_char', 'unsaved') + '\r\n'
        self.handler.message_bus.send_to_character.assert_awaited_once_with(self.actor.id, expected)

    async def test_blocked_quit_never_submits_a_save(self):
        self.actor.character_attributes.position = self.enums.get('positions').POS_FIGHTING.value
        with patch.object(self.service, 'queue_save_character') as save:
            await self.handler.do_quit(self.actor, self.context('quit'))
        save.assert_not_called()
        self.assertIn(self.actor.id, self.room.characters)

    async def test_slow_save_yields_while_character_is_excluded_from_world_updates(self):
        entered, release = threading.Event(), threading.Event()
        context = self.context('quit')

        def persist(*args, **kwargs):
            entered.set()
            if not release.wait(2):
                raise requests.Timeout('test release timed out')
            return Mock()

        with patch('player.CharacterService.requests.put', side_effect=persist):
            task = asyncio.create_task(self.handler.do_quit(self.actor, context))
            try:
                self.assertTrue(await asyncio.to_thread(entered.wait, 1))
                self.assertFalse(task.done())
                self.assertNotIn(self.actor.id, self.room.characters)
                self.assertNotIn(self.actor.id, self.registry.playing)
                self.assertFalse(self.sessions.get_playing_sessions())
                self.assertTrue(self.session.metadata['quitting'])
            finally:
                release.set()
            await asyncio.wait_for(task, 2)
        context.conn.close.assert_awaited_once()
        self.assertNotIn(self.actor.id, self.registry.playing)
        self.assertNotIn('quitting', self.session.metadata)

    async def test_cancelling_quit_keeps_world_ownership_and_does_not_cancel_save(self):
        entered, release, completed = threading.Event(), threading.Event(), threading.Event()
        context = self.context('quit')

        def persist(*args, **kwargs):
            entered.set()
            if not release.wait(2):
                raise requests.Timeout('test release timed out')
            completed.set()
            return Mock()

        with patch('player.CharacterService.requests.put', side_effect=persist):
            task = asyncio.create_task(self.handler.do_quit(self.actor, context))
            try:
                self.assertTrue(await asyncio.to_thread(entered.wait, 1))
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task
                self.assertIn(self.actor.id, self.room.characters)
                self.assertTrue(self.session.is_playing())
                self.assertNotIn('quitting', self.session.metadata)
                context.conn.close.assert_not_awaited()
            finally:
                release.set()
                self.assertTrue(await asyncio.to_thread(completed.wait, 1))

    async def test_closed_connection_does_not_emit_farewells_after_successful_save(self):
        context = self.context('quit')

        async def save(_character):
            context.conn.is_closed = lambda: True
            return True

        self.service.save_character_async = save
        await self.handler.do_quit(self.actor, context)
        self.assertNotIn(self.actor.id, self.room.characters)
        self.assertNotIn(self.actor.id, self.registry.playing)
        self.handler.message_bus.send_to_character.assert_not_awaited()

    async def test_quit_uses_current_room_even_with_a_stale_command_context(self):
        destination = Room(id='destination', area_id=self.room.area_id)
        context = self.context('quit')

        self.room.remove_player_from_room(self.actor)
        self.actor.room_id = destination.id
        destination.add_player_to_room(self.actor)
        self.service.save_character_async = AsyncMock(return_value=True)
        self.handler.room_registry = NS(get_or_none=lambda **kw: destination)
        await self.handler.do_quit(self.actor, context)
        self.assertFalse(destination.characters)
        context.conn.close.assert_awaited_once()


class DeniedCharacterTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.account = NS(banned=False, current_characters=[], first_name='Test', last_name='Account')
        self.registry = CharacterRegistry()
        self.manager, self.sessions = ConnectionManager(), SessionHandler()
        registries = NS(room_registry=self.rooms, character_registry=self.registry,
                        player_registry=NS(get_or_none=lambda **kw: self.account, get=lambda **kw: self.account),
                        area_registry=NS(get_or_none=lambda **kw: None))
        bus = Mock(send_to_character=AsyncMock(), send_prompt=AsyncMock(), text_to_message=lambda text: text)
        self.handler = ConnectionHandler(self.manager, self.sessions, bus, registries,
                                         Mock(), Mock(), Mock(), Mock(), Mock())

    def connection(self, sid):
        connection = Mock(session_id=sid, is_closed=Mock(return_value=False),
                          send_text=AsyncMock(), close=AsyncMock())
        session = self.sessions.create_session(sid)
        session.player_id = self.actor.account_id
        self.manager.add_connection(connection)
        return connection, session

    async def test_denial_survives_save_load_and_rejects_offline_admission(self):
        self.room.remove_player_from_room(self.actor)
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_DENY)
        restored = Character.from_json(json.loads(json.dumps(CharacterService._serialize_character(self.actor))))
        connection, session = self.connection('new')
        self.assertIsNone(await self.handler._attach_character(restored, session, connection))
        self.assertIsNone(session.character)
        self.assertNotEqual(SessionStatus.PLAYING, session.status)
        self.assertFalse(self.registry.playing)
        self.assertFalse(self.account.current_characters)
        self.assertIsNone(self.manager.get_connection_by_character(restored.id))
        connection.close.assert_awaited_once()

    async def test_denial_logs_the_rejection_reason_without_authentication_payload(self):
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_DENY)
        self.handler.logger = Mock()
        connection, session = self.connection('rejected')
        await self.handler._attach_character(self.actor, session, connection)
        self.handler.logger.warning.assert_called_once_with(
            'Login rejected for character %s on session %s: %s',
            self.actor.name, session.session_id, 'You are denied access to this character.')

    async def test_rejection_is_terminal_and_printed_once_even_if_admission_is_reentered(self):
        deny = self.enums.get('playerActBits').PLR_DENY
        self.actor.status_flags.set_flag('act', deny)
        connection, session = self.connection('rejected')

        async def send(*args):
            # Simulate another admission path running while transport yields.
            self.actor.status_flags.unset_flag('act', deny)
            self.assertIsNone(await self.handler._nanny(self.actor, session, connection))

        connection.send_text.side_effect = send
        self.assertIsNone(await self.handler._attach_character(self.actor, session, connection))
        self.assertIsNone(await self.handler._attach_character(self.actor, session, connection))
        connection.send_text.assert_awaited_once()
        connection.close.assert_awaited_once()
        self.assertEqual(SessionStatus.DISCONNECTING, session.status)
        self.assertIsNone(session.character)
        self.assertFalse(self.registry.playing)

    async def test_denied_telnet_login_prints_once_closes_and_never_enters_game_loop(self):
        self.room.remove_player_from_room(self.actor)
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_DENY)
        self.registry.register(self.actor)
        self.account.account_name = 'review-account'
        self.account.player_character_list = [self.actor.id]
        self.handler.auth_service = AuthenticationService(
            self.handler.registry_service.player_registry, self.registry)
        self.handler._peer_denied = Mock(return_value=False)
        self.handler._game_loop = AsyncMock()
        reader = Mock(at_eof=Mock(return_value=False), readline=AsyncMock(return_value=(
            'logon ' + json.dumps({'accountId': self.actor.account_id, 'characterId': self.actor.id}) + '\r\n'
        ).encode()))
        writer = Mock(is_closing=Mock(return_value=False), drain=AsyncMock(), wait_closed=AsyncMock(),
                      get_extra_info=Mock(return_value=('local', 1234)))
        writer.close.side_effect = lambda: setattr(writer.is_closing, 'return_value', True)
        await self.handler.handle_new_connection(reader, writer)
        wire = b''.join(call.args[0] for call in writer.write.call_args_list)
        self.assertEqual(1, wire.count(b'You are denied access to this character.'))
        self.handler._game_loop.assert_not_awaited()
        self.handler.room_handler.print_room.assert_not_called()
        self.assertFalse(self.room.characters)
        self.assertFalse(self.registry.playing)
        self.assertFalse(self.account.current_characters)
        self.assertEqual(0, self.sessions.session_count())
        self.assertIsNone(self.manager.get_connection_by_character(self.actor.id))
        writer.close.assert_called_once()
        reader.readline.assert_awaited_once()

    async def test_shipped_janky_snapshot_has_no_denial_bit(self):
        collection = load_collections(ROOT / 'resources/collections', ['characters'])['characters']
        document = next(row for row in collection.documents if row.get('name') == 'Janky')
        self.assertFalse(int(document['statusFlags']['act']) & int(self.enums.get('playerActBits').PLR_DENY))

    async def test_live_denial_overrides_stale_character_and_preserves_existing_binding(self):
        stale = self.character('actor')
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_DENY)
        old, old_session = self.connection('old')
        old_session.character, old_session.status = self.actor, SessionStatus.PLAYING
        self.manager.bind_character(self.actor.id, 'old')
        new, session = self.connection('new')
        self.assertIsNone(await self.handler._attach_character(stale, session, new))
        self.assertIs(old, self.manager.get_connection_by_character(self.actor.id))
        old.close.assert_not_awaited()

    async def test_denial_added_during_takeover_prompt_is_rechecked(self):
        old, old_session = self.connection('old')
        old_session.character, old_session.status = self.actor, SessionStatus.PLAYING
        self.manager.bind_character(self.actor.id, 'old')
        new, session = self.connection('new')

        async def confirm(_connection):
            self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_DENY)
            return True

        self.handler._confirm_replacement = confirm
        self.assertIsNone(await self.handler._attach_character(self.actor, session, new))
        self.assertIs(old, self.manager.get_connection_by_character(self.actor.id))
        old.close.assert_not_awaited()

    async def test_denial_does_not_ban_allowed_sibling_character(self):
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_DENY)
        sibling = self.character('sibling')
        connection, session = self.connection('sibling-session')
        result = await self.handler._attach_character(sibling, session, connection)
        self.assertIs(result[1], sibling)
        self.assertTrue(session.is_playing())
        self.assertFalse(self.account.banned)

    async def test_reconnect_cannot_reattach_character_while_final_quit_save_is_pending(self):
        self.room.remove_player_from_room(self.actor)
        old, old_session = self.connection('old')
        old_session.character, old_session.status = self.actor, SessionStatus.DISCONNECTING
        old_session.metadata['quitting'] = True
        self.manager.bind_character(self.actor.id, 'old')
        new, session = self.connection('new')
        self.assertIsNone(await self.handler._attach_character(self.actor, session, new))
        self.assertIs(old, self.manager.get_connection_by_character(self.actor.id))
        self.assertIsNone(session.character)
        old.close.assert_not_awaited()


class FrozenInputTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_FREEZE)
        self.executors = NS(do_communications_command=AsyncMock())
        self.social = Mock(handle_social=AsyncMock())
        self.services = NS(get_handler=lambda name: {'ph': self.executors, 'sh': self.social}.get(name))
        self.say = self.command('say')
        self.commands = NS(get_or_none=lambda **kw: self.say if kw.get('name') == 'say' else None,
                           all_commands=lambda: [self.say])
        self.bus = Mock(send_to_character=AsyncMock(), text_to_message=lambda text: text,
                        connection_manager=NS(get_connection_by_character=lambda key: None))
        self.interp = InterpHandler.__new__(InterpHandler)
        for key, value in dict(registry_service=NS(interp_registry=self.commands), interp_registry=self.commands,
                               social_registry=NS(get_or_none=lambda **kw: object()), social_handler=self.social,
                               message_bus=self.bus, handler_service=self.services, room_registry=self.rooms,
                               connection_manager=self.bus.connection_manager, logger=Mock()).items():
            setattr(self.interp, key, value)
        self.nested = PlayerHandler.__new__(PlayerHandler)
        self.nested.interp_registry = self.commands
        self.nested.social_registry = self.interp.social_registry
        self.nested.room_registry = self.rooms
        self.nested.message_bus = self.bus

    async def test_frozen_normal_alias_and_social_input_are_blocked(self):
        self.actor.aliases = {'chat': 'say hello'}
        for text in ['say hello', 'chat', 'smile']:
            await self.interp.handle_command(NS(usage='player'), self.actor, text)
        self.executors.do_communications_command.assert_not_awaited()
        self.social.handle_social.assert_not_awaited()
        self.assertEqual(3, self.bus.send_to_character.await_count)

    async def test_nested_commands_and_socials_cannot_bypass_freeze(self):
        context = Context(character=self.actor, handler_service=self.services)
        for text in ['say hello', 'smile']:
            await self.nested._interpret_nested_command(self.actor, context, text)
        # Direct executor calls must enforce the same restriction.
        context.command = self.say
        await CommandExecutor.execute(self.say, context, authorization=CommandAccess.check, message_bus=self.bus)
        self.executors.do_communications_command.assert_not_awaited()
        self.social.handle_social.assert_not_awaited()

    async def test_thaw_restores_input_and_command_can_override_denial_text(self):
        self.say.payload.to_char['command_frozen'] = 'Content-owned frozen message.'
        self.assertEqual('Content-owned frozen message.\r\n', CommandAccess.check(self.actor, self.say).render(self.say))
        self.actor.status_flags.unset_flag('act', self.enums.get('playerActBits').PLR_FREEZE)
        await self.interp.handle_command(NS(usage='player'), self.actor, 'say hello')
        self.executors.do_communications_command.assert_awaited_once()

    async def test_controlled_body_uses_frozen_principal_but_npc_act_bits_are_not_player_flags(self):
        body = Mobile.__new__(Mobile)
        body.level, body.name, body.id = 1, 'body', 'body'
        body.context = {'controller_original': self.actor}
        body.character_attributes = NS(position=self.enums.get('positions').POS_STANDING.value)
        body.status_flags = self.actor.status_flags
        self.assertEqual('command_frozen', CommandAccess.check(body, self.say).message_key)
        body.context.clear()
        self.assertIsNone(CommandAccess.check_actor(body))


class GroupTellTests(RuntimeFixture, unittest.TestCase):
    def test_authored_group_tell_routes_local_and_remote_members_without_bystanders_or_npcs(self):
        bystander, local, remote = [self.character(name) for name in ['bystander', 'local', 'remote']]
        local.leader = remote.leader = self.actor
        other_room = Room(id='remote-room', characters={remote.id: remote})
        for character in [bystander, local]:
            self.room.add_player_to_room(character)
        npc = Mobile.__new__(Mobile)
        npc.id, npc.leader = 'pet', self.actor
        self.room.mobiles[npc.id] = npc
        registry = NS(all_rooms=lambda: [self.room, other_room])
        player_handler = NS(room_registry=registry)
        communications = Communications.__new__(Communications)
        from api.CommunicationsApi import CommunicationsApi
        communications.communications_api = CommunicationsApi
        communications.interp_api = self.api
        context = self.context('gtell', 'secret')
        context.handler_service = NS(get_handler=lambda key: player_handler)
        payload = communications.do_gtell(context)
        self.assertEqual({local.id, remote.id}, {member.id for member in payload['targets']})
        self.assertIn('secret', payload['to_char'])
        self.assertIn('secret', payload['to_room'])

    def test_empty_group_tell_preserves_authored_guard(self):
        communications = Communications.__new__(Communications)
        communications.interp_api = self.api
        payload = communications.do_gtell(self.context('gtell'))
        self.assertTrue(payload['blocked'])
        self.assertNotIn('targets', payload)


class NoteCursorAndRoomTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    async def test_read_and_catchup_survive_save_load_separately_for_each_note_type(self):
        notes = {kind: [InGameNote(id=str(kind), type=kind, to_list='all', date_stamp=100 + kind)]
                 for kind in range(5)}
        service = NS(get_notes_by_type=lambda kind: notes[kind])
        handler = NoteHandler(None, service, None, self.api)
        names = ['note', 'idea', 'penalty', 'news', 'changes']
        for kind, name in enumerate(names):
            await handler.execute(self.actor, self.context(name, 'read 1' if kind % 2 else 'catchup'))
        self.actor.context = {'runtime_only': object()}
        payload = CharacterService._serialize_character(self.actor)
        self.assertNotIn('context', payload)
        restored = Character.from_json(json.loads(json.dumps(payload)))
        self.assertEqual({str(kind): 100 + kind for kind in range(5)}, restored.note_read_stamps)
        for name in names:
            context = self.context(name)
            result = await handler.execute(restored, context)
            self.assertIn('no unread', result['to_char'])

    async def test_legacy_null_and_default_note_cursors_are_independent_and_monotonic(self):
        data = build_character_data()
        for value in ['missing', None, {}]:
            with self.subTest(value=value):
                if value != 'missing':
                    data['noteReadStamps'] = value
                first, second = Character.from_json(data), Character.from_json(data)
                first.mark_note_read(0, 20)
                first.mark_note_read(0, 10)
                self.assertEqual(20, first.note_read_stamp(0))
                self.assertEqual(0, second.note_read_stamp(0))

    async def test_room_service_preserves_regeneration_rates_including_zero(self):
        service = RoomService.__new__(RoomService)
        service.logger = Mock()
        for rates in [{}, {'healRate': 250, 'manaRate': 175}, {'healRate': 0, 'manaRate': 0}]:
            with self.subTest(rates=rates):
                room = service._build_fetch_item(dict(id='r', **rates))
                self.assertEqual(rates.get('healRate', 100), room.heal_rate)
                self.assertEqual(rates.get('manaRate', 100), room.mana_rate)
                self.actor.hit = self.actor.mana = self.actor.movement = 0
                self.actor.max_hit = self.actor.max_mana = self.actor.max_movement = 1000
                context = RegenerationContext(self.enums.get('positions'), self.enums.get('affectedBy'),
                                              Mock(number_percent=Mock(return_value=100)))
                base = Room()
                hit, mana = self.actor.hit_gain(base, context), self.actor.mana_gain(base, context)
                self.actor.regenerate(room, context)
                self.assertEqual(hit * room.heal_rate // 100, self.actor.hit)
                self.assertEqual(mana * room.mana_rate // 100, self.actor.mana)


if __name__ == '__main__':
    unittest.main()

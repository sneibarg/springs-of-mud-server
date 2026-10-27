import asyncio
from concurrent.futures import Future
from types import SimpleNamespace as NS
import unittest
from unittest.mock import AsyncMock, Mock

from tests import test_review_application_fixes as fixtures
from api.CharacterApi import CharacterApi
from interp.commands.Wiz import Wiz
from mobile.Mobile import Mobile
from player.CharacterRegistry import CharacterRegistry
from player.PlayerHandler import PlayerHandler
from server.RuntimeControl import RuntimeControl
from server.handlers.ConnectionHandler import ConnectionHandler
from server.session.SessionHandler import SessionHandler
from util.EntityExtractor import EntityExtractor


def resolved(value):
    future = Future()
    future.set_result(value)
    return future


class PunishmentGuardsTests(fixtures.RuntimeFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.actor.level = self.actor.trust = 60
        CharacterApi.set_act_flags(self.actor, self.enums.get('playerActBits').PLR_HOLYLIGHT)
        self.victim = self.character('victim')
        self.victim.room_id = self.room.id
        self.room.add_player_to_room(self.victim)
        self.registry = CharacterRegistry()
        for value in (self.actor, self.victim):
            self.registry.register(value)
        self.wiz = Wiz.__new__(Wiz)
        self.wiz.character_registry = self.registry
        self.wiz.room_registry = self.rooms
        self.wiz.interp_api = self.api
        self.wiz.CommFlagsEnum = self.enums.get('commFlags')
        self.wiz.PlayerActBitsEnum = self.enums.get('playerActBits')
        self.wiz.character_service = NS(queue_save_character=Mock())

    def execute(self, name, text):
        context = self.context(name, text)
        ph = NS(character_registry=self.registry, room_registry=self.rooms)
        context.handler_service = NS(get_handler=lambda key: ph)
        return self.wiz.execute(self.actor, context)

    def test_missing_arguments_and_targets_are_denied_without_mutation(self):
        for name in ('freeze', 'nochannels', 'noemote', 'noshout', 'notell'):
            old = (self.victim.status_flags.act, self.victim.status_flags.comm)
            for argument, text in (('', 'whom'), ('absent', "aren't here")):
                with self.subTest(command=name, argument=argument):
                    result = self.execute(name, argument)
                    self.assertIn(text, result['to_char'].lower())
                    self.assertEqual(old, (self.victim.status_flags.act, self.victim.status_flags.comm))

    def test_equal_and_higher_trust_are_protected_for_every_punishment(self):
        for trust in (59, 60):
            self.actor.trust = 59
            self.victim.trust = trust
            for name in ('freeze', 'nochannels', 'noemote', 'noshout', 'notell'):
                self.assertIn('failed', self.execute(name, 'victim')['to_char'].lower())
        self.wiz.character_service.queue_save_character.assert_not_called()

    def test_freeze_and_unfreeze_save_and_emit_victim_payload(self):
        bit = self.wiz.PlayerActBitsEnum.PLR_FREEZE
        for enabled in (True, False):
            result = self.execute('freeze', 'victim')
            self.assertEqual(CharacterApi.is_set(self.victim.status_flags.act, bit), enabled)
            self.assertIs(result['victim'], self.victim)
            self.assertEqual(result['message_key'], 'set' if enabled else 'removed')
        self.assertEqual(self.wiz.character_service.queue_save_character.call_count, 2)

    def test_npc_exclusions_and_valid_communication_toggles(self):
        mobile = mobile_entity('npc', self.victim.status_flags)
        mobile.room_id = self.room.id
        self.room.add_mobile_to_room(mobile)
        self.registry.register(mobile)
        for name in ('freeze', 'noshout'):
            self.assertIn('npc', self.execute(name, 'npc')['to_char'].lower())
        for name in ('nochannels', 'noemote', 'noshout', 'notell'):
            self.assertEqual(self.execute(name, 'victim')['message_key'], 'set')
            self.assertEqual(self.execute(name, 'victim')['message_key'], 'removed')


def mobile_entity(name, status):
    from copy import deepcopy
    return Mobile(id=name, area_id='area', room_id='room', name=name, sex='1', level=1,
                  gold=0, silver=0, vnum='1', short_description=name, long_description=name,
                  description=name, race='human', flags='', alignment='0', group='',
                  dam_type='punch', size='medium', material='flesh', hit_roll=0, status_flags=deepcopy(status))


class WizlockTests(fixtures.RuntimeFixture, unittest.TestCase):
    def test_login_checks_lock_and_shutdown_but_allow_immortals(self):
        handler = ConnectionHandler.__new__(ConnectionHandler)
        handler.runtime_control = None
        handler.wiz_handler = NS(wizlocked=True)
        handler.registry_service = NS(room_registry=self.rooms)
        self.room.remove_player_from_room(self.actor)
        account = NS(banned=False)
        self.assertIn('wizlocked', handler._login_error(self.actor, account))
        self.room.add_player_to_room(self.actor)
        self.assertEqual('', handler._login_error(self.actor, account))
        self.room.remove_player_from_room(self.actor)
        self.actor.level = self.actor.trust = 60
        self.assertEqual('', handler._login_error(self.actor, account))
        handler.runtime_control = NS(shutting_down=True)
        self.assertIn('shutting down', handler._login_error(self.actor, account))


class ExtractionTests(fixtures.RuntimeFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.registry = CharacterRegistry()
        self.registry.register(self.actor)
        self.registry.set_playing(self.actor)
        self.mobile = mobile_entity('body', self.actor.status_flags)
        self.mobile.room_id = self.room.id
        self.room.add_mobile_to_room(self.mobile)
        self.registry.register(self.mobile)
        self.registries = NS(character_registry=self.registry, room_registry=self.rooms)
        def stop(value, both):
            opponent = value.fighting
            value.fighting = None
            if both and opponent is not None:
                opponent.fighting = None
        self.fight = NS(stop_fighting=Mock(side_effect=stop), effect_handler=Mock())
        self.wiz = NS(current_session=lambda value: None, return_character=Mock())
        self.extractor = EntityExtractor(self.registries, self.fight, self.wiz)

    def test_npc_extraction_stops_combat_and_cleans_followers_pets_and_replies(self):
        self.actor.fighting = self.mobile
        self.mobile.fighting = self.actor
        follower = self.character('follower')
        follower.master = follower.leader = self.mobile
        follower.context = {'reply_to': self.mobile.id}
        self.registry.register(follower)
        self.actor.pet = self.mobile
        self.extractor.extract(self.mobile)
        self.assertIsNone(self.actor.fighting)
        self.assertIsNone(follower.master)
        self.assertIsNone(follower.leader)
        self.assertIsNone(self.actor.pet)
        self.assertNotIn('reply_to', follower.context)
        self.assertNotIn(self.mobile.id, self.room.mobiles)
        self.assertIsNone(self.registry.get_or_none(id=self.mobile.id))

    def test_extraction_returns_switched_controller(self):
        session = NS(character=self.mobile, metadata={'switched_original': self.actor})
        self.wiz.current_session = lambda value: session if value is self.mobile else None
        self.extractor.extract(self.mobile)
        self.wiz.return_character.assert_called_once_with(self.mobile)

    def test_purged_inventory_is_detached_and_room_purge_honors_nopurge(self):
        item = NS(id='sword')
        self.mobile.inventory = [item]
        protected = mobile_entity('protected', self.actor.status_flags)
        protected.room_id = self.room.id
        bit = self.enums.get('actBits').ACT_NOPURGE
        CharacterApi.set_act_flags(protected, bit)
        self.room.add_mobile_to_room(protected)
        self.registry.register(protected)
        wiz = Wiz.__new__(Wiz)
        wiz.room_registry = self.rooms
        wiz.entity_extractor = self.extractor
        wiz.ActBitsEnum = self.enums.get('actBits')
        wiz.ItemFlagsEnum = self.enums.get('itemExtraFlags') if self.enums.contains('itemExtraFlags') else self.enums.get('itemFlags')
        wiz.do_purge(self.actor, self.context('purge'))
        self.assertEqual(self.mobile.inventory, [])
        self.assertNotIn(self.mobile.id, self.room.mobiles)
        self.assertIn(protected.id, self.room.mobiles)
        self.assertIn(self.actor.id, self.room.characters)

    def test_player_retirement_preserves_offline_cache_and_room_hint(self):
        self.actor.pet = self.mobile
        room_id = self.actor.room_id
        self.extractor.extract(self.actor)
        self.assertTrue(self.actor.world_retired)
        self.assertNotIn(self.actor.id, self.room.characters)
        self.assertNotIn(self.actor.id, self.registry.playing)
        self.assertIs(self.registry.get_or_none(id=self.actor.id), self.actor)
        self.assertEqual(self.actor.room_id, room_id)
        self.assertNotIn(self.mobile.id, self.room.mobiles)


class SavedShutdownTests(fixtures.RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.sessions = SessionHandler()
        session = self.sessions.create_session('player')
        session.character = self.actor
        self.events = []
        async def pause():
            self.events.append('pause')
        self.game = NS(pause_updates=AsyncMock(side_effect=pause), resume_updates=Mock(), stop=Mock())
        self.saves = NS(queue_save_character=Mock(side_effect=lambda value: self.save(value)))
        self.manager = NS(close_all=AsyncMock())
        self.control = RuntimeControl(self.game, self.saves, self.sessions, self.manager)
        self.listener = NS(close=Mock(), wait_closed=AsyncMock())
        self.control.bind_listener(self.listener)

    def save(self, value):
        self.events.append('save:' + value.id)
        return resolved(True)

    async def test_save_originals_before_announcement_listener_and_connection_close(self):
        body = mobile_entity('body', self.actor.status_flags)
        session = self.sessions.get_session('player')
        session.character = body
        session.metadata['switched_original'] = self.actor
        duplicate = self.sessions.create_session('duplicate')
        duplicate.character = self.actor
        self.listener.close.side_effect = lambda: self.events.append('listener')
        async def broadcast():
            self.events.append('announce')
        async def close_all():
            self.events.append('clients')
        self.manager.close_all.side_effect = close_all
        self.assertTrue(await self.control.shutdown('reboot', broadcast))
        self.assertEqual(self.events, ['pause', 'save:' + self.actor.id, 'announce', 'listener', 'clients'])
        self.saves.queue_save_character.assert_called_once_with(self.actor)
        self.game.stop.assert_called_once()
        self.assertTrue(self.control._stopped.is_set())
        self.assertEqual(self.control.shutdown_kind, 'reboot')

    async def test_save_failure_rolls_back_without_disconnecting_or_announcing(self):
        self.saves.queue_save_character.return_value = resolved(False)
        self.saves.queue_save_character.side_effect = None
        broadcast = AsyncMock()
        self.assertFalse(await self.control.shutdown('shutdown', broadcast))
        self.assertFalse(self.control.shutting_down)
        self.game.resume_updates.assert_called_once()
        self.game.stop.assert_not_called()
        self.listener.close.assert_not_called()
        self.manager.close_all.assert_not_awaited()
        broadcast.assert_not_awaited()
        self.assertNotIn('shutdown_pending', self.sessions.get_session('player').metadata)

    async def test_in_flight_save_blocks_shutdown_completion(self):
        future = Future()
        self.saves.queue_save_character.side_effect = lambda value: future
        task = asyncio.create_task(self.control.shutdown('shutdown'))
        await asyncio.sleep(0)
        self.assertTrue(self.sessions.get_session('player').metadata['shutdown_pending'])
        self.listener.close.assert_not_called()
        future.set_result(True)
        self.assertTrue(await task)

    async def test_shutdown_waits_for_other_commands_before_snapshotting(self):
        session = self.sessions.get_session('player')
        session.metadata['command_task'] = object()
        session.metadata['command_idle'] = asyncio.Event()
        task = asyncio.create_task(self.control.shutdown('shutdown'))
        await asyncio.sleep(0)
        self.saves.queue_save_character.assert_not_called()
        session.metadata['command_idle'].set()
        self.assertTrue(await task)

    async def test_shutdown_cancellation_resumes_admission_and_world_updates(self):
        self.saves.queue_save_character.side_effect = lambda value: Future()
        task = asyncio.create_task(self.control.shutdown('shutdown'))
        await asyncio.sleep(0)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertFalse(self.control.shutting_down)
        self.game.resume_updates.assert_called_once()
        self.assertNotIn('shutdown_pending', self.sessions.get_session('player').metadata)

    async def test_teardown_error_does_not_resume_a_closed_server(self):
        self.control.logger = Mock()
        self.listener.wait_closed.side_effect = OSError('listener failed')
        self.assertTrue(await self.control.shutdown('shutdown'))
        self.assertTrue(self.control.shutting_down)
        self.assertTrue(self.control._stopped.is_set())
        self.game.stop.assert_called_once()
        self.manager.close_all.assert_awaited_once()
        self.game.resume_updates.assert_not_called()

    async def test_player_command_delegates_announcement_to_saved_shutdown(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        payload = {'shutdown_kind': 'reboot'}
        handler.wiz_commands = NS(execute=lambda actor, ctx: payload)
        handler.runtime_control = self.control
        handler._handle_standard_command_payload = AsyncMock()
        await handler.do_wiz_command(self.actor, self.context('reboot'))
        handler._handle_standard_command_payload.assert_awaited_once_with(self.actor, unittest.mock.ANY, payload)
        self.assertEqual(self.control.shutdown_kind, 'reboot')


class PurgePersistenceTests(fixtures.RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    async def test_player_save_failure_leaves_target_in_world(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.wiz_handler = NS(current_session=lambda value: NS(session_id='victim', metadata={}))
        connection = NS(close=AsyncMock())
        handler.message_bus = NS(connection_manager=NS(get_connection=lambda sid: connection))
        handler.character_service = NS(save_character_async=AsyncMock(return_value=False))
        handler.interp_api = self.api
        handler._handle_standard_command_payload = AsyncMock()
        extractor = Mock()
        handler.wiz_commands = NS(entity_extractor=extractor)
        handler.room_registry = self.rooms
        self.actor.level = 10
        await handler._handle_purge_payload(self.actor, self.context('purge', 'actor'), {'purge_character': self.actor})
        self.assertFalse(self.actor.world_retired)
        self.assertIn(self.actor.id, self.room.characters)
        extractor.extract.assert_not_called()
        connection.close.assert_not_awaited()

    async def test_player_is_saved_before_extraction_and_disconnection(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        events = []
        session = NS(session_id='victim', metadata={})
        handler.wiz_handler = NS(current_session=lambda value: session)
        async def close(): events.append('close')
        handler.message_bus = NS(connection_manager=NS(get_connection=lambda sid: NS(close=close)))
        async def save(value):
            self.assertIn(value.id, self.room.characters)
            self.assertTrue(session.metadata['quitting'])
            events.append('save')
            return True
        handler.character_service = NS(save_character_async=save)
        handler._handle_standard_command_payload = AsyncMock()
        handler.wiz_commands = NS(entity_extractor=NS(extract=lambda value: events.append('extract')))
        self.actor.level = 10
        await handler._handle_purge_payload(self.actor, self.context('purge', 'actor'), {'purge_character': self.actor})
        self.assertEqual(events, ['save', 'extract', 'close'])
        self.assertNotIn('quitting', session.metadata)

    async def test_cancelled_save_releases_retirement_and_session_gate(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        session = NS(session_id='victim', metadata={})
        handler.wiz_handler = NS(current_session=lambda value: session)
        handler.message_bus = NS(connection_manager=NS(get_connection=lambda sid: NS(close=AsyncMock())))
        started = asyncio.Event()
        async def save(value):
            started.set()
            await asyncio.Event().wait()
        handler.character_service = NS(save_character_async=save)
        self.actor.level = 10
        task = asyncio.create_task(handler._handle_purge_payload(self.actor, self.context('purge'), {'purge_character': self.actor}))
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertFalse(self.actor.world_retired)
        self.assertNotIn('quitting', session.metadata)

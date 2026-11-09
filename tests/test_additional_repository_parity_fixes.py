"""End-to-end regressions for the second October 31 ROM24 review."""
from copy import deepcopy
import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests import test_repository_parity_remediation as remediation
from tests.test_review_application_fixes import ROOT
from tests.test_movement_rules_parity import item
from api.SpellApi import SpellApi
from combat.CombatHandler import FightHandler
from devtools.collection_query import load_collections
from interp.commands.Info import Info
from player.Character import Character
from player.CharacterService import CharacterService
from server.handlers.ConnectionHandler import ConnectionHandler
from server.session.SessionState import SessionState
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus
from server.connection.ConnectionManager import ConnectionManager
from skill.Spell import Spell
from skill.SpellContext import SpellContext
from util.ElementalExposure import ElementalExposure
from util.DisplayUtil import RecipientText
from util.EntityExtractor import EntityExtractor


class AdditionalParityTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        remediation.PublicInputTests.setUpClass()

    def setUp(self):
        self.holder = remediation.PublicInputTests()
        self.holder.setUp()
        self.addCleanup(self.holder.doCleanups)
        self.f = self.holder.fixture

    async def command(self, text):
        f = self.f
        for connection in f.connections.values():
            connection.send_message.reset_mock()
        await f.interpreter.handle_command(f.actor, text)
        return {person.name: f.messages(person) for person in (f.actor, f.bob, f.cara)}

    async def test_punctuation_matches_full_command_delivery(self):
        for shortcut, name in ((',', 'emote'), (';', 'gtell'), ('.', 'gossip')):
            with self.subTest(shortcut=shortcut):
                expected = await self.command(name + ' hello   world')
                self.assertEqual(expected, await self.command(shortcut + 'hello   world'))

    async def test_dot_respects_gossip_flags_and_does_not_toggle_grats(self):
        f = self.f
        flags = f.enums.get('commFlags')
        f.bob.status_flags.set_flag('comm', flags.COMM_NOGOSSIP)
        f.cara.status_flags.set_flag('comm', flags.COMM_NOGRATS)
        f.actor.status_flags.set_flag('comm', flags.COMM_NOGRATS | flags.COMM_NOGOSSIP)
        messages = await self.command('.hello')
        self.assertEqual([], messages['Bob'])
        self.assertEqual(["Alice gossips 'hello'\r\n"], messages['Cara'])
        self.assertFalse(f.actor.status_flags.comm & flags.COMM_NOGOSSIP)
        self.assertTrue(f.actor.status_flags.comm & flags.COMM_NOGRATS)
        for disabled in (True, False):
            await self.command('.')
            self.assertEqual(disabled, bool(f.actor.status_flags.comm & flags.COMM_NOGOSSIP))
            self.assertTrue(f.actor.status_flags.comm & flags.COMM_NOGRATS)

    async def test_semicolon_requires_a_body_and_honors_notell(self):
        for name in (';', 'gtell'):
            with self.subTest(command=name):
                messages = await self.command(name)
                self.assertEqual(['Tell your group what?\r\n'], messages['Alice'])
                self.assertFalse(messages['Bob'])
                self.f.actor.status_flags.set_flag('comm', self.f.enums.get('commFlags').COMM_NOTELL)
                messages = await self.command(name + ' private')
                self.assertEqual(["Your message didn't get through!\r\n"], messages['Alice'])
                self.assertFalse(messages['Bob'])
                self.f.actor.status_flags.unset_flag('comm', self.f.enums.get('commFlags').COMM_NOTELL)

    async def test_comma_uses_emote_restriction(self):
        f = self.f
        f.actor.status_flags.set_flag('comm', f.enums.get('commFlags').COMM_NOEMOTE)
        messages = await self.command(',waves')
        self.assertEqual(["You can't show your emotions.\r\n"], messages['Alice'])
        self.assertFalse(messages['Bob'])

    async def test_pose_uses_authored_variants_with_per_observer_visibility(self):
        f = self.f
        f.flag(f.actor, 'AFF_INVISIBLE')
        f.flag(f.cara, 'AFF_DETECT_INVIS')
        for key in ('pose_heroic', 'pose_cautious', 'pose_happy', 'pose_yawn', 'pose_ponder'):
            with self.subTest(key=key), patch('interp.commands.Communications.random.choice', return_value=key):
                messages = await self.command('pose')
                self.assertTrue(messages['Alice'][0].startswith('You '))
                self.assertTrue(messages['Bob'][0].startswith('Someone '))
                self.assertTrue(messages['Cara'][0].startswith('Alice '))
        f.bob.set_position(int(f.enums.get('positions').POS_SLEEPING))
        self.assertFalse((await self.command('pose'))['Bob'])

    def test_npcs_do_not_pose(self):
        f = self.f
        self.assertEqual({}, f.commands.execute(f.ctx('pose', character=f.npc())))

    async def test_teleport_snapshots_visibility_in_both_rooms_and_delivers_variants(self):
        f = self.f
        f.flag(f.actor, 'AFF_INVISIBLE')
        f.flag(f.cara, 'AFF_DETECT_INVIS')
        document = next(doc for doc in load_collections(ROOT / 'resources/collections', ['spells'])['spells'].documents
                        if doc['name'] == 'teleport')
        spell = Spell.from_json(deepcopy(document))
        api = SpellApi(f.effects, f.api)
        f.room.remove_player_from_room(f.cara)
        f.destination.add_player_to_room(f.cara)
        f.cara.room_id, f.cara.area_id = f.destination.id, f.destination.area_id
        ctx = SpellContext(f.actor, spell, NS(spell_api=api, registry_service=f.registries), f.room, target=f.actor)
        with patch.object(api, 'random_room', return_value=f.destination):
            self.assertTrue(api.execute_lambdas(ctx))
        notices = [p for p in ctx.payloads if p.get('to_room')]
        self.assertEqual(2, len(notices))
        # Visibility is captured before later mutations or asynchronous delivery.
        f.flag(f.bob, 'AFF_DETECT_INVIS')
        f.flag(f.cara, 'AFF_DETECT_INVIS', False)
        for payload in notices:
            await f.bus.send_to_room(f.bus.text_to_message(payload['to_room']), payload['targets'])
        self.assertEqual(['Someone vanishes!\r\n'], f.messages(f.bob))
        self.assertEqual(['Alice slowly fades into existence.\r\n'], f.messages(f.cara))
        self.assertEqual([], f.messages(f.actor))

    async def test_combat_merge_and_round_delivery_keep_hidden_weapon_generic(self):
        f = self.f
        weapon = item('blade', itemType='weapon', shortDescription='an invisible blade',
                      extraFlags=int(f.enums.get('itemFlags').ITEM_INVIS))
        rule = f.game_document['combat']['weaponHitEffects']['flaming']
        notice = ElementalExposure._messages(rule, 'hit', f.actor, f.bob, weapon, f.room)
        merged = FightHandler._merge_attack_payloads({'to_room': 'Base hit.\r\n'}, notice)
        merged = FightHandler._merge_attack_payloads(merged, notice)
        combat = FightHandler.__new__(FightHandler)
        payload = combat.build_round_payload(f.actor, f.bob, f.room, merged)
        self.assertIsInstance(payload['to_room'], RecipientText)
        with patch.object(f.commands, 'execute', return_value=payload):
            await f.execute('gossip', 'ignored')
        self.assertEqual(['Base hit.\r\n' + 'Bob is burned by something.\r\n' * 2], f.messages(f.cara))

    def test_condition_append_preserves_recipient_text(self):
        text = RecipientText('base', {'viewer': 'hidden'}, 'unknown')
        with patch('combat.CombatHandler.InfoUtil.target_condition_line', return_value='Condition.'):
            result = FightHandler._append_condition_line(text, self.f.actor)
        self.assertEqual('hidden\r\nCondition.\r\n', result.for_recipient('viewer'))
        self.assertEqual('unknown\r\nCondition.\r\n', result.for_recipient('new'))

    def login_handler(self):
        account = NS(first_name='Test', last_name='Player', current_characters=[], ansi_enabled=False)
        handler = ConnectionHandler.__new__(ConnectionHandler)
        handler.registry_service = NS(player_registry=NS(get_or_none=lambda **kw: account, get=lambda **kw: account),
                                      character_registry=NS(set_playing=Mock()))
        handler._login_error = Mock(return_value='')
        handler.logger = Mock()
        return handler

    async def test_fresh_login_resets_stale_clock_and_reconnect_does_not_reset_it(self):
        f = self.f
        f.actor.status_flags.played, f.actor.status_flags.logon = 3600, 900
        handler = self.login_handler()
        for now in (10000, 10100):
            with patch('player.Character.datetime') as clock:
                clock.now.return_value.timestamp.return_value = now
                await handler._nanny(f.actor, SessionState(str(now), player_id='account'), NS(get_peer_info=lambda: None))
        self.assertEqual((3600, 10000), (f.actor.status_flags.played, f.actor.status_flags.logon))
        self.assertEqual((3700, 10100), f.actor.playtime_snapshot(10100))
        with patch('interp.commands.Info.datetime') as clock:
            clock.now.return_value.timestamp.return_value = 10100
            self.assertIn('(1 hours)', Info.do_score(Info.__new__(Info), f.actor, f.ctx('score')))
        victim = f.npc()
        victim.status_flags.set_flag('act', f.enums.get('actBits').ACT_NOALIGN)
        f.actor.current_time = 10100
        with patch('combat.CombatHandler.random.randint', side_effect=lambda low, high: low):
            self.assertEqual(9, FightHandler.xp_compute(FightHandler.__new__(FightHandler), f.actor, victim, f.actor.level))

    async def test_link_loss_and_actual_reattachment_preserve_live_playtime(self):
        f = self.f
        manager, sessions = ConnectionManager(), SessionHandler()
        account = NS(first_name='Test', last_name='Player', banned=False, current_characters=[f.actor])
        registries = NS(room_registry=f.rooms, area_registry=NS(get_or_none=lambda **kw: NS()),
                        player_registry=NS(get_or_none=lambda **kw: account, get=lambda **kw: account),
                        character_registry=NS(set_playing=Mock(), remove_playing=Mock()))
        bus = NS(send_to_character=AsyncMock(), send_prompt=AsyncMock(), text_to_message=lambda text: text)
        handler = ConnectionHandler(manager, sessions, bus, registries, Mock(), Mock(), Mock(), Mock(),
                                    NS(wiznet_targets=lambda *args, **kwargs: [], wizlocked=False, newlocked=False))
        def connection(sid):
            conn = NS(session_id=sid, is_closed=lambda: False, send_text=AsyncMock(),
                      get_peer_info=lambda: ('local', 1), close=AsyncMock())
            manager.add_connection(conn)
            session = sessions.create_session(sid)
            session.player_id = 'account'
            return conn, session
        f.actor.status_flags.played = 0
        f.actor.start_playtime(1000)
        _, old = connection('old')
        old.character, old.status = f.actor, SessionStatus.PLAYING
        manager.bind_character(f.actor.id, 'old')
        await handler._cleanup_session(old)
        self.assertTrue(f.actor._playtime_active)
        conn, session = connection('new')
        with patch('player.Character.datetime') as clock:
            clock.now.return_value.timestamp.return_value = 1200
            self.assertIsNotNone(await handler._attach_character(f.actor, session, conn))
        self.assertEqual((200, 1200), f.actor.playtime_snapshot(1200))
        self.assertEqual(1000, f.actor.status_flags.logon)

    def test_world_extraction_stops_player_clock(self):
        f = self.f
        f.actor.status_flags.played = 0
        f.actor.start_playtime(1000)
        f.registries.character_registry = NS(all_characters=lambda: [f.actor], remove_playing=Mock())
        extractor = EntityExtractor(f.registries, NS(stop_fighting=Mock()), NS(current_session=lambda actor: None))
        with patch('player.Character.datetime') as clock:
            clock.now.return_value.timestamp.return_value = 1100
            extractor.extract(f.actor)
        self.assertEqual((100, 0), f.actor.playtime_snapshot(99999))
        self.assertFalse(f.actor._playtime_active)

    def test_autosaves_accumulate_only_in_snapshots_and_restart_excludes_offline_time(self):
        actor = self.f.actor
        actor.status_flags.played = 3600
        actor.start_playtime(10000)
        for now, total in ((10100, 3700), (10200, 3800)):
            with patch('player.Character.datetime') as clock:
                clock.now.return_value.timestamp.return_value = now
                snapshot = CharacterService._serialize_character(actor)
            self.assertEqual((total, now), (snapshot['statusFlags']['played'], snapshot['statusFlags']['logon']))
            self.assertEqual((3600, 10000), (actor.status_flags.played, actor.status_flags.logon))
        restored = Character.from_json(snapshot)
        restored.start_playtime(99999)
        self.assertEqual((3800, 99999), restored.playtime_snapshot(99999))
        actor.stop_playtime(10250)
        actor.start_playtime(55555)
        self.assertEqual((3850, 55555), actor.playtime_snapshot(55555))

    def test_zero_logon_records_start_accumulating_at_world_entry(self):
        actor = self.f.actor
        actor.status_flags.played = actor.status_flags.logon = 0
        actor.start_playtime(1000)
        self.assertEqual((3600, 4600), actor.playtime_snapshot(4600))
        actor.stop_playtime(4600)
        actor.stop_playtime(99999)
        self.assertEqual((3600, 0), actor.playtime_snapshot(99999))

    async def test_successful_quit_stops_playtime_and_failed_quit_keeps_it_active(self):
        f = self.f
        player = f.interpreter.handler_service.get_handler('ph')
        player.info_commands = NS(do_quit=lambda ctx: {'to_char': 'Bye', 'to_room': 'Left'})
        player.character_registry = NS(remove_playing=Mock(), set_playing=Mock(), all_characters=lambda: [])
        registries = NS(room_registry=f.rooms, character_registry=player.character_registry)
        player.entity_extractor = EntityExtractor(registries, Mock(), NS(current_session=lambda entity: None))
        player.interp_api = f.api
        player.character_service = NS(save_character_async=AsyncMock(return_value=False))
        for saved in (False, True):
            with self.subTest(saved=saved):
                f.actor.start_playtime(1000)
                player.character_service.save_character_async.return_value = saved
                context = f.ctx('quit')
                context.disconnect = AsyncMock()
                with patch('player.Character.datetime') as clock:
                    clock.now.return_value.timestamp.return_value = 1100
                    await player._quit(f.actor, context)
                self.assertEqual(not saved, f.actor._playtime_active)


if __name__ == '__main__':
    unittest.main()

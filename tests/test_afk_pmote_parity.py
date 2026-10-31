"""AFK state transitions and ROM pmote recipient rendering through real payload delivery."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock

from tests.test_movement_rules_parity import MovementFixture
from api.CommunicationsApi import CommunicationsApi
from interp.commands.Communications import Communications
from player.PlayerHandler import PlayerHandler
from server.messaging.MessageBus import MessageBus


class AfkPmoteTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.commands = Communications(self.registries, NS(), NS(), self.enums, self.api)
        self.actor.name = 'Alice'
        self.bob = self.follower('Bob')
        self.cara = self.follower('Cara')

    def test_afk_repeatedly_toggles_only_its_own_flag_and_uses_authored_messages(self):
        quiet = self.enums.get('commFlags').COMM_QUIET
        afk = self.enums.get('commFlags').COMM_AFK
        self.actor.status_flags.set_flag('comm', quiet)
        for enabled in (True, False, True, False):
            payload = self.commands.execute(self.ctx('afk'))
            self.assertEqual(enabled, bool(self.actor.status_flags.comm & afk))
            self.assertTrue(self.actor.status_flags.comm & quiet)
            self.assertEqual(self.command('afk').render_message('to_char', 'enable' if enabled else 'disable') + '\r\n', payload['to_char'])

    def test_afk_retains_tell_buffer_for_replay(self):
        self.addCleanup(CommunicationsApi._tell_buffer.clear)
        self.commands.execute(self.ctx('afk'))
        CommunicationsApi.append_tell_buffer(self.actor, self.bob, 'hello')
        self.commands.execute(self.ctx('afk'))
        self.assertTrue(CommunicationsApi.has_buffered_tells(self.actor))
        payload = self.commands.execute(self.ctx('replay'))
        self.assertIn("Bob tells you 'hello'", payload['to_char'])
        self.assertFalse(CommunicationsApi.has_buffered_tells(self.actor))

    def test_pmote_names_possessives_repeated_and_case_sensitive_mentions(self):
        for text, expected in [("waves at Bob.", 'waves at you.'),
                               ("takes Bob's hand.", 'takes your hand.'),
                               ('greets Bob and Bob.', 'greets you and you.'),
                               ('greets bob.', 'greets bob.'), ('waves.', 'waves.')]:
            with self.subTest(text=text):
                payload = self.commands.execute(self.ctx('pmote', text))
                self.assertEqual('Alice ' + expected + '\r\n', payload['to_room'].for_recipient(self.bob.id))
                self.assertEqual('Alice ' + text + '\r\n', payload['to_room'].for_recipient(self.cara.id))
                self.assertEqual('Alice ' + text + '\r\n', payload['to_char'])

    def test_pmote_respects_visibility_resting_threshold_and_guards(self):
        self.flag(self.actor, 'AFF_INVISIBLE')
        self.flag(self.cara, 'AFF_DETECT_INVIS')
        payload = self.commands.execute(self.ctx('pmote', 'waves at Bob.'))
        self.assertEqual('Someone waves at you.\r\n', payload['to_room'].for_recipient(self.bob.id))
        self.assertEqual('Alice waves at Bob.\r\n', payload['to_room'].for_recipient(self.cara.id))
        self.bob.set_position(int(self.enums.get('positions').POS_SLEEPING))
        self.assertNotIn(self.bob, self.commands.execute(self.ctx('pmote', 'waves'))['targets'])
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOEMOTE)
        self.assertTrue(self.commands.execute(self.ctx('pmote', 'waves'))['blocked'])
        self.actor.status_flags.unset_flag('comm', self.enums.get('commFlags').COMM_NOEMOTE)
        self.assertTrue(self.commands.execute(self.ctx('pmote'))['blocked'])

    def test_pmote_connected_mobile_is_a_recipient(self):
        npc = self.npc()
        npc.name = 'Guard'
        npc.context = {'controller_original': self.cara}
        self.room.add_mobile_to_room(npc)
        payload = self.commands.execute(self.ctx('pmote', 'waves at Guard.'))
        self.assertIn(npc, payload['targets'])
        self.assertEqual('Alice waves at you.\r\n', payload['to_room'].for_recipient(npc.id))
        payload = self.commands.execute(self.ctx('pmote', 'waves.', character=npc))
        self.assertNotIn(npc, payload['targets'])

    async def test_real_message_bus_delivers_distinct_observer_text_once(self):
        connections = {entity.id: NS(is_closed=lambda: False, send_message=AsyncMock())
                       for entity in (self.actor, self.bob, self.cara)}
        manager = NS(get_connection_by_character=connections.get)
        sessions = NS(get_session_by_character=lambda identifier: None)
        bus = MessageBus(manager, sessions)
        emitter = PlayerHandler.__new__(PlayerHandler)
        emitter.message_bus = bus
        emitter._send_prompt = AsyncMock()
        context = self.ctx('pmote', "takes Bob's hand.")
        payload = self.commands.execute(context)
        await emitter._emit_standard_payload(self.actor, payload, context=context)
        for entity, expected in ((self.actor, "Alice takes Bob's hand.\r\n"),
                                 (self.bob, 'Alice takes your hand.\r\n'),
                                 (self.cara, "Alice takes Bob's hand.\r\n")):
            connections[entity.id].send_message.assert_awaited_once()
            self.assertEqual(expected, connections[entity.id].send_message.call_args.args[0].data['text'])


if __name__ == '__main__':
    unittest.main()

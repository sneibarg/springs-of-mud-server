"""Local speech uses ROM's listener visibility and resting-position minimum."""
import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock

from tests.test_movement_rules_parity import MovementFixture
from interp.commands.Communications import Communications
from interp.commands.Info import Info
from player.PlayerHandler import PlayerHandler
from server.messaging.MessageBus import MessageBus


class LocalSpeechTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.actor.name = 'Alice'
        self.bob, self.cara = self.follower('Bob'), self.follower('Cara')
        self.commands = Communications(self.registries, NS(), NS(), self.enums, self.api)
        self.info = Info.__new__(Info)
        self.info.room_registry = self.rooms

    def speech(self, name, text='hello', actor=None):
        actor = actor or self.actor
        if name == 'report':
            payload = self.info.do_report(actor)
            payload['targets'] = payload['people']
            return payload
        return self.commands.execute(self.ctx(name, text, character=actor))

    def test_unseen_speaker_is_anonymous_only_to_listeners_without_detection(self):
        self.flag(self.actor, 'AFF_INVISIBLE')
        self.flag(self.cara, 'AFF_DETECT_INVIS')
        for name in ('say', 'emote', 'report'):
            with self.subTest(command=name):
                payload = self.speech(name)
                self.assertTrue(payload['to_room'].for_recipient(self.bob.id).startswith('Someone '))
                self.assertTrue(payload['to_room'].for_recipient(self.cara.id).startswith('Alice '))
                self.assertTrue(payload['to_room'].for_recipient('missing').startswith('Someone '))

    def test_position_boundary_includes_resting_and_excludes_sleeping_and_stunned(self):
        positions = self.enums.get('positions')
        for position, eligible in (('POS_STUNNED', False), ('POS_SLEEPING', False),
                                   ('POS_RESTING', True), ('POS_SITTING', True), ('POS_STANDING', True)):
            self.bob.set_position(int(getattr(positions, position)))
            for name in ('say', 'emote', 'report'):
                with self.subTest(command=name, position=position):
                    targets = self.speech(name)['targets']
                    self.assertEqual(eligible, self.bob in targets)
                    self.assertNotIn(self.actor, targets)

    def test_only_controlled_mobile_listeners_are_included(self):
        mobile = self.npc()
        self.room.add_mobile_to_room(mobile)
        for name in ('say', 'emote', 'report'):
            self.assertNotIn(mobile, self.speech(name)['targets'])
        mobile.context = {'controller_original': self.cara}
        for name in ('say', 'emote', 'report'):
            self.assertIn(mobile, self.speech(name)['targets'])
        mobile.set_position(int(self.enums.get('positions').POS_SLEEPING))
        self.assertNotIn(mobile, self.speech('say')['targets'])

    def test_npc_speaker_uses_short_description_for_visible_listeners(self):
        mobile = self.npc()
        mobile.name, mobile.short_description = 'guard sentinel', 'a sentinel'
        mobile.hit, mobile.max_hit, mobile.mana, mobile.max_mana = 25, 30, 15, 20
        self.room.add_mobile_to_room(mobile)
        for name in ('say', 'emote', 'report'):
            text = self.speech(name, actor=mobile)['to_room'].for_recipient(self.bob.id)
            self.assertTrue(text.startswith('A sentinel '))
            self.assertNotIn('guard sentinel', text)

    def test_authored_payload_and_body_names_are_preserved(self):
        self.flag(self.actor, 'AFF_INVISIBLE')
        context = self.ctx('say', 'Alice')
        context.command = deepcopy(context.command)
        context.command.payload.to_room['default'] = '%c whispers: %s'
        payload = self.commands.execute(context)
        self.assertEqual('Someone whispers: Alice\r\n', payload['to_room'].for_recipient(self.bob.id))
        self.assertEqual("You say 'Alice'\r\n", payload['to_char'])

    def test_empty_arguments_and_noemote_guards_still_block(self):
        for name in ('say', 'emote'):
            self.assertTrue(self.speech(name, '')['blocked'])
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOEMOTE)
        self.assertTrue(self.speech('emote')['blocked'])

    async def test_real_message_bus_delivers_each_variant_once_and_skips_sleepers(self):
        sleeper = self.follower('Sleeper')
        sleeper.set_position(int(self.enums.get('positions').POS_SLEEPING))
        self.flag(self.actor, 'AFF_INVISIBLE')
        self.flag(self.cara, 'AFF_DETECT_INVIS')
        connections = {entity.id: NS(is_closed=lambda: False, send_message=AsyncMock())
                       for entity in (self.actor, self.bob, self.cara, sleeper)}
        emitter = PlayerHandler.__new__(PlayerHandler)
        emitter.message_bus = MessageBus(NS(get_connection_by_character=connections.get),
                                        NS(get_session_by_character=lambda identifier: None))
        emitter._send_prompt = AsyncMock()
        emitter.info_commands = self.info
        for name in ('say', 'emote', 'report'):
            for connection in connections.values():
                connection.send_message.reset_mock()
            context = self.ctx(name, 'hello')
            if name == 'report':
                await emitter.do_report(self.actor, context)
            else:
                await emitter._emit_standard_payload(self.actor, self.commands.execute(context), context=context)
            for entity in (self.actor, self.bob, self.cara):
                connections[entity.id].send_message.assert_awaited_once()
            self.assertTrue(connections[self.bob.id].send_message.call_args.args[0].data['text'].startswith('Someone '))
            self.assertTrue(connections[self.cara.id].send_message.call_args.args[0].data['text'].startswith('Alice '))
            connections[sleeper.id].send_message.assert_not_awaited()


if __name__ == '__main__':
    unittest.main()

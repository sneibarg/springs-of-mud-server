"""Complete message bodies through interpreter execution and actual bus delivery."""
import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, patch

from tests.test_movement_rules_parity import MovementFixture
from interp.InterpHandler import InterpHandler
from interp.commands.Communications import Communications
from player.PlayerHandler import PlayerHandler
from server.messaging.MessageBus import MessageBus


class SpeechTextTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    CHANNELS = {'gossip': 'COMM_NOGOSSIP', 'auction': 'COMM_NOAUCTION',
                'music': 'COMM_NOMUSIC', 'question': 'COMM_NOQUESTION',
                'quote': 'COMM_NOQUOTE', 'grats': 'COMM_NOGRATS'}

    def setUp(self):
        super().setUp()
        self.actor.name = 'Alice'
        self.bob, self.cara = self.follower('Bob'), self.follower('Cara')
        self.bob.leader = self.actor
        people = (self.actor, self.bob, self.cara)
        self.connections = {c.id: NS(is_closed=lambda: False, send_message=AsyncMock()) for c in people}
        sessions = NS(get_playing_sessions=lambda: [NS(character=c) for c in people],
                      get_session_by_character=lambda identifier: None)
        manager = NS(get_connection_by_character=self.connections.get)
        self.bus = MessageBus(manager, sessions)
        self.commands = Communications(self.registries, sessions, NS(), self.enums, self.api)
        registry = NS(get_or_none=lambda **kw: next((c for c in people if c.id == kw['id']), None))
        self.commands.character_registry = registry
        player = PlayerHandler.__new__(PlayerHandler)
        player.communications_commands = self.commands
        player.character_registry, player.room_registry = registry, self.rooms
        player.message_bus, player._send_prompt = self.bus, AsyncMock()
        self.interpreter = InterpHandler.__new__(InterpHandler)
        self.interpreter.handler_service = NS(get_handler=lambda key: player)
        self.interpreter.connection_manager, self.interpreter.room_registry = manager, self.rooms
        self.interpreter.message_bus = self.bus

    async def execute(self, name, text='', command=None):
        for connection in self.connections.values():
            connection.send_message.reset_mock()
        await self.interpreter._handle_lambdas(self.actor, command or self.command(name), text,
                                                raw_command=f'{name} {text}'.rstrip())

    def messages(self, character):
        return [call.args[0].data['text'] for call in self.connections[character.id].send_message.call_args_list]

    async def test_full_body_reaches_sender_and_recipient_on_every_affected_command(self):
        names = ('say', 'shout', 'yell', 'gtell', *self.CHANNELS)
        for name in names:
            for body in ('hello brave world', 'hello', "it's a fine day!", "'hello brave' world", 'hello   brave world'):
                with self.subTest(command=name, body=body):
                    await self.execute(name, body)
                    for character in (self.actor, self.bob):
                        messages = self.messages(character)
                        self.assertTrue(messages)
                        self.assertTrue(all(body in message for message in messages), messages)
                    self.assertEqual(1, len(self.messages(self.bob)))

    async def test_targeted_tell_and_reply_keep_target_separate_from_full_body(self):
        self.actor.context = {'reply_to': self.bob.id}
        for name, argument in (('tell', 'Bob hello brave world'), ('reply', 'hello brave world')):
            with self.subTest(command=name):
                await self.execute(name, argument)
                self.assertEqual(["You tell Bob 'hello brave world'\r\n"], self.messages(self.actor))
                self.assertEqual(["Alice tells you 'hello brave world'\r\n"], self.messages(self.bob))

    async def test_authored_body_tokens_all_receive_complete_untargeted_text(self):
        command = deepcopy(self.command('gossip'))
        command.payload.to_char['default'] = '%s | %t | %e'
        command.payload.to_world['default'] = '%c: %t | %s | %e'
        await self.execute('gossip', 'hello brave world', command)
        expected = 'hello brave world | hello brave world | hello brave world\r\n'
        self.assertEqual([expected], self.messages(self.actor))
        self.assertEqual(['Alice: ' + expected], self.messages(self.bob))

    async def test_channel_toggles_and_sending_auto_enable_remain_intact(self):
        for name, flag in self.CHANNELS.items():
            bit = getattr(self.enums.get('commFlags'), flag)
            self.actor.status_flags.unset_flag('comm', bit)
            await self.execute(name)
            self.assertTrue(self.actor.status_flags.comm & int(bit))
            self.assertFalse(self.messages(self.bob))
            await self.execute(name)
            self.assertFalse(self.actor.status_flags.comm & int(bit))
            self.actor.status_flags.set_flag('comm', bit)
            await self.execute(name, 'hello brave world')
            self.assertFalse(self.actor.status_flags.comm & int(bit))
            self.assertIn('hello brave world', self.messages(self.bob)[0])

    async def test_channel_filters_and_sender_guards_remain_intact(self):
        for name, flag in self.CHANNELS.items():
            bit = getattr(self.enums.get('commFlags'), flag)
            self.bob.status_flags.set_flag('comm', bit)
            await self.execute(name, 'hello brave world')
            self.assertFalse(self.messages(self.bob))
            self.assertIn('hello brave world', self.messages(self.cara)[0])
            self.bob.status_flags.unset_flag('comm', bit)
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOCHANNELS)
        await self.execute('gossip', 'hello brave world')
        self.assertFalse(self.messages(self.bob))
        self.assertTrue(self.messages(self.actor))

    async def test_local_visibility_and_sleep_filters_preserve_the_full_body(self):
        self.flag(self.actor, 'AFF_INVISIBLE')
        self.flag(self.cara, 'AFF_DETECT_INVIS')
        self.cara.set_position(int(self.enums.get('positions').POS_SLEEPING))
        await self.execute('say', 'Alice is here')
        self.assertEqual(["Someone says 'Alice is here'\r\n"], self.messages(self.bob))
        self.assertFalse(self.messages(self.cara))
        self.cara.set_position(int(self.enums.get('positions').POS_RESTING))
        await self.execute('say', 'Alice is here')
        self.assertEqual(["Alice says 'Alice is here'\r\n"], self.messages(self.cara))

    async def test_parameters_fallback_preserves_full_message(self):
        for name in ('say', 'shout', 'yell', 'gtell', *self.CHANNELS):
            with self.subTest(command=name):
                context = self.ctx(name)
                context.result, context.parameters = None, ['hello', 'brave', 'world']
                payload = self.commands.execute(context)
                self.assertIn('hello brave world', payload['to_char'])
                room_text = payload.get('to_room') or payload.get('to_area') or payload.get('global_message')
                self.assertIn('hello brave world', str(room_text))

    async def test_public_channels_and_yell_deliver_once_per_listener(self):
        for name in ('yell', *self.CHANNELS):
            with self.subTest(command=name):
                await self.execute(name, 'hello brave world')
                for character in (self.actor, self.bob, self.cara):
                    self.assertEqual(1, len(self.messages(character)))

    async def test_clan_broadcast_delivers_once_only_to_matching_clan(self):
        self.actor.guild = self.bob.guild = 'rom'
        self.cara.guild = 'other'
        await self.execute('clan', 'hello brave world')
        self.assertEqual(["You clan 'hello brave world'\r\n"], self.messages(self.actor))
        self.assertEqual(["Alice clans 'hello brave world'\r\n"], self.messages(self.bob))
        self.assertFalse(self.messages(self.cara))

    async def test_payload_dispatch_preserves_single_delivery_and_exclusions(self):
        cases = [
            ({'global_message': 'targeted', 'global_targets': [self.bob]}, (0, 1, 0)),
            ({'global_message': 'targeted-id', 'global_targets': [self.bob.id]}, (0, 1, 0)),
            ({'global_message': 'empty', 'global_targets': []}, (0, 0, 0)),
            ({'broadcast_message': 'broadcast', 'exclude_character_ids': [self.actor.id]}, (0, 1, 1)),
            ({'to_world': 'world'}, (0, 1, 1)),
            ({'to_area': 'area'}, (1, 1, 1)),
        ]
        for payload, counts in cases:
            with self.subTest(payload=payload):
                with patch.object(self.commands, 'execute', return_value=payload):
                    await self.execute('gossip', 'hello')
                self.assertEqual(counts, tuple(len(self.messages(c)) for c in (self.actor, self.bob, self.cara)))

    async def test_nested_payload_broadcasts_are_dispatched_once(self):
        payload = {'payloads': [
            {'global_message': 'first', 'global_targets': [self.bob]},
            {'broadcast_message': 'second', 'exclude_character_ids': [self.actor.id]},
        ]}
        with patch.object(self.commands, 'execute', return_value=payload):
            await self.execute('gossip', 'hello')
        self.assertEqual(['first', 'second'], self.messages(self.bob))
        self.assertEqual(['second'], self.messages(self.cara))
        self.assertFalse(self.messages(self.actor))

    async def test_yell_and_shout_respect_listener_optouts_and_exclude_sender(self):
        flags = self.enums.get('commFlags')
        for name in ('yell', 'shout'):
            for flag in ('COMM_QUIET', 'COMM_SHOUTSOFF'):
                with self.subTest(command=name, flag=flag):
                    self.bob.status_flags.assign_bitfield('comm', int(getattr(flags, flag)))
                    await self.execute(name, 'hello brave world')
                    expected = 1 if name == 'yell' and flag == 'COMM_SHOUTSOFF' else 0
                    self.assertEqual(expected, len(self.messages(self.bob)))
                    self.assertEqual(1, len(self.messages(self.cara)))
                    self.assertEqual([f"You {name} 'hello brave world'\r\n"], self.messages(self.actor))

    async def test_yell_and_shout_require_resting_or_higher_listeners(self):
        for name in ('yell', 'shout'):
            for position, eligible in (('POS_SLEEPING', False), ('POS_STUNNED', False),
                                       ('POS_RESTING', True), ('POS_STANDING', True)):
                with self.subTest(command=name, position=position):
                    self.bob.set_position(int(getattr(self.enums.get('positions'), position)))
                    await self.execute(name, 'hello brave world')
                    self.assertEqual(int(eligible), len(self.messages(self.bob)))
                    self.assertEqual(1, len(self.messages(self.actor)))

    async def test_yell_and_shout_render_invisible_speaker_per_listener(self):
        self.flag(self.actor, 'AFF_INVISIBLE')
        self.flag(self.cara, 'AFF_DETECT_INVIS')
        for name in ('yell', 'shout'):
            await self.execute(name, 'Alice is here')
            self.assertEqual([f"Someone {name}s 'Alice is here'\r\n"], self.messages(self.bob))
            self.assertEqual([f"Alice {name}s 'Alice is here'\r\n"], self.messages(self.cara))

    async def test_remote_listener_visibility_uses_listeners_room(self):
        self.destination.area_id = self.room.area_id
        self.room.remove_player_from_room(self.bob)
        self.destination.add_player_to_room(self.bob)
        self.bob.room_id = self.destination.id
        dark = int(self.enums.get('roomFlags').ROOM_DARK)
        self.destination.room_flags = dark
        for name in ('yell', 'shout'):
            await self.execute(name, 'hello brave world')
            self.assertTrue(self.messages(self.bob)[0].startswith('Someone '))
            self.assertTrue(self.messages(self.cara)[0].startswith('Alice '))
        self.destination.room_flags = 0
        self.room.room_flags = dark
        for name in ('yell', 'shout'):
            await self.execute(name, 'hello brave world')
            self.assertTrue(self.messages(self.bob)[0].startswith('Alice '))

    async def test_yell_and_shout_keep_the_authored_area_scope(self):
        self.room.remove_player_from_room(self.bob)
        self.temple.add_player_to_room(self.bob)
        self.bob.room_id, self.bob.area_id = self.temple.id, self.temple.area_id
        for name in ('yell', 'shout'):
            await self.execute(name, 'hello brave world')
            self.assertFalse(self.messages(self.bob))
            self.assertEqual(1, len(self.messages(self.cara)))

    async def test_yell_and_shout_keep_authored_text_with_filtered_delivery(self):
        for name, channel in (('yell', 'to_room'), ('shout', 'to_area')):
            command = deepcopy(self.command(name))
            getattr(command.payload, channel)['default'] = '%c calls: %s'
            await self.execute(name, 'hello brave world', command)
            self.assertEqual(['Alice calls: hello brave world\r\n'], self.messages(self.bob))
            self.assertEqual(1, len(self.messages(self.actor)))


if __name__ == '__main__':
    unittest.main()

"""ROM tell/reply pointers, AFK deferral and replay through authored payloads."""
import asyncio
import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock

from tests.test_movement_rules_parity import MovementFixture
from api.CommunicationsApi import CommunicationsApi
from interp.commands.Communications import Communications
from player.PlayerHandler import PlayerHandler
from server.messaging.MessageBus import MessageBus


class TellDeliveryTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        CommunicationsApi._tell_buffer.clear()
        self.addCleanup(CommunicationsApi._tell_buffer.clear)
        self.actor.name = 'Alice'
        self.bob, self.cara = self.follower('Bob'), self.follower('Cara')
        people = (self.actor, self.bob, self.cara)
        self.sessions = [NS(character=c) for c in people]
        sessions = NS(get_playing_sessions=lambda: self.sessions)
        self.commands = Communications(self.registries, sessions, NS(), self.enums, self.api)
        self.commands.character_registry = NS(get_or_none=lambda **kw: next(
            (c for c in people if c.id == kw['id']), None))

    def run_command(self, name, text='', actor=None):
        return self.commands.execute(self.ctx(name, text, character=actor))

    def afk(self, actor):
        actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_AFK)

    def test_outgoing_tell_preserves_sender_reply_and_updates_recipient(self):
        self.actor.context = {'reply_to': self.cara.id}
        result = self.run_command('tell', 'Bob hello')
        self.assertEqual(self.cara.id, self.actor.context['reply_to'])
        self.assertEqual(self.actor.id, self.bob.context['reply_to'])
        self.assertEqual("Alice tells you 'hello'\r\n", result['to_victim'])
        reply = self.run_command('reply', 'answer')
        self.assertIs(self.cara, reply['victim'])
        self.assertEqual(self.cara.id, self.actor.context['reply_to'])

    def test_outgoing_tell_without_incoming_reply_leaves_sender_unset(self):
        self.run_command('tell', 'Bob hello')
        self.assertFalse((self.actor.context or {}).get('reply_to'))

    def test_live_tells_and_replies_do_not_populate_replay(self):
        self.run_command('tell', 'Bob hello')
        self.run_command('reply', 'answer', self.bob)
        for actor in (self.actor, self.bob):
            self.assertFalse(CommunicationsApi.has_buffered_tells(actor))
            self.assertIn('no tells to replay', self.run_command('replay', actor=actor)['to_char'])

    def test_afk_tell_and_reply_preserve_both_pointers_and_only_acknowledge(self):
        self.afk(self.bob)
        self.bob.context = {'reply_to': self.cara.id}
        for name, argument, old_reply in (('tell', 'Bob hello', self.cara.id),
                                          ('reply', 'hello', self.bob.id)):
            with self.subTest(command=name):
                self.actor.context = {'reply_to': old_reply}
                result = self.run_command(name, argument)
                self.assertNotIn('to_victim', result)
                self.assertNotIn("You tell", result['to_char'])
                self.assertIn('AFK', result['to_char'])
                self.assertEqual(old_reply, self.actor.context['reply_to'])
                self.assertEqual(self.cara.id, self.bob.context['reply_to'])

    def test_replay_formats_deferred_tells_once_in_order_then_clears(self):
        self.afk(self.bob)
        self.run_command('tell', "Bob it's hello")
        self.run_command('tell', 'Bob second', self.cara)
        self.run_command('afk', actor=self.bob)
        result = self.run_command('replay', actor=self.bob)
        self.assertEqual("Alice tells you 'it's hello'\r\nCara tells you 'second'\r\n", result['to_char'])
        self.assertFalse(CommunicationsApi.has_buffered_tells(self.bob))

    def test_replay_preserves_authored_recipient_text(self):
        self.afk(self.bob)
        context = self.ctx('tell', 'Bob hello')
        context.command = deepcopy(context.command)
        context.command.payload.to_victim['default'] = '[private] %s'
        self.commands.execute(context)
        self.assertEqual('[private] hello\r\n', self.run_command('replay', actor=self.bob)['to_char'])

    def test_blocked_tell_does_not_buffer_or_change_pointers(self):
        self.afk(self.bob)
        self.actor.context = {'reply_to': self.cara.id}
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOTELL)
        self.run_command('tell', 'Bob hello')
        self.assertFalse(CommunicationsApi.has_buffered_tells(self.bob))
        self.assertEqual(self.cara.id, self.actor.context['reply_to'])
        self.assertFalse((self.bob.context or {}).get('reply_to'))

    def test_mortal_cannot_reach_sleeping_recipient_even_when_afk(self):
        self.bob.set_position(int(self.enums.get('positions').POS_SLEEPING))
        self.afk(self.bob)
        self.actor.context = {'reply_to': self.bob.id}
        for name, text in (('tell', 'Bob hello'), ('reply', 'hello')):
            with self.subTest(command=name):
                payload = self.run_command(name, text)
                self.assertIn("Bob can't hear you", payload.get('to_char', ''))
                self.assertNotIn('to_victim', payload)
                self.assertFalse(CommunicationsApi.has_buffered_tells(self.bob))
                self.assertFalse((self.bob.context or {}).get('reply_to'))

    def test_sleeping_recipient_immortal_threshold_differs_for_tell_and_reply(self):
        self.bob.set_position(int(self.enums.get('positions').POS_SLEEPING))
        self.actor.context = {'reply_to': self.bob.id}
        immortal = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        for level, command, text, allowed in ((immortal, 'tell', 'Bob hello', False),
                                               (immortal, 'reply', 'hello', True),
                                               (immortal + 1, 'tell', 'Bob hello', True)):
            with self.subTest(level=level, command=command):
                self.actor.level = level
                payload = self.run_command(command, text)
                self.assertEqual(allowed, bool(payload.get('to_victim')))

    def test_recipient_notell_only_restricts_outgoing_messages(self):
        self.bob.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOTELL)
        self.actor.context = {'reply_to': self.bob.id}
        for name, text in (('tell', 'Bob hello'), ('reply', 'hello')):
            self.assertIn('to_victim', self.run_command(name, text))

    def test_quiet_and_deaf_recipient_immortal_exceptions(self):
        immortal = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        for flag in ('COMM_QUIET', 'COMM_DEAF'):
            for name, text in (('tell', 'Bob hello'), ('reply', 'hello')):
                for sender_immortal, recipient_immortal in ((False, False), (True, False), (False, True)):
                    with self.subTest(flag=flag, command=name, sender=sender_immortal, target=recipient_immortal):
                        self.actor.level = immortal if sender_immortal else 20
                        self.bob.level = immortal if recipient_immortal else 20
                        self.actor.context = {'reply_to': self.bob.id}
                        self.bob.status_flags.assign_bitfield('comm', int(getattr(self.enums.get('commFlags'), flag)))
                        payload = self.run_command(name, text)
                        allowed = sender_immortal or (name == 'reply' and recipient_immortal)
                        self.assertEqual(allowed, bool(payload.get('to_victim')))

    def test_sender_outgoing_restrictions_still_apply(self):
        self.actor.context = {'reply_to': self.bob.id}
        for flag in ('COMM_NOTELL', 'COMM_QUIET'):
            self.actor.status_flags.assign_bitfield('comm', int(getattr(self.enums.get('commFlags'), flag)))
            for name, text in (('tell', 'Bob hello'), ('reply', 'hello')):
                self.assertNotIn('to_victim', self.run_command(name, text))

    def test_linkdead_tell_and_reply_buffer_before_recipient_state_checks(self):
        self.sessions = [session for session in self.sessions if session.character is not self.bob]
        self.actor.context = {'reply_to': self.bob.id}
        self.bob.context = {'reply_to': self.cara.id}
        self.bob.set_position(int(self.enums.get('positions').POS_SLEEPING))
        self.bob.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_QUIET)
        self.afk(self.bob)
        for name, text in (('tell', 'Bob hello'), ('reply', 'answer')):
            with self.subTest(command=name):
                result = self.run_command(name, text)
                self.assertIn('Bob seems to have misplaced', result.get('to_char', ''))
                self.assertNotIn('to_victim', result)
                self.assertEqual(self.cara.id, self.bob.context['reply_to'])
                self.assertEqual(self.bob.id, self.actor.context['reply_to'])
        self.sessions.append(NS(character=self.bob))
        self.bob.set_position(int(self.enums.get('positions').POS_STANDING))
        replay = self.run_command('replay', actor=self.bob)
        self.assertEqual("Alice tells you 'hello'\r\nAlice tells you 'answer'\r\n", replay['to_char'])
        self.assertFalse(CommunicationsApi.has_buffered_tells(self.bob))

    def test_registry_only_offline_players_are_not_tell_or_reply_targets(self):
        self.sessions = [session for session in self.sessions if session.character is not self.bob]
        self.room.remove_player_from_room(self.bob)
        self.actor.context = {'reply_to': self.bob.id}
        for name, text in (('tell', 'Bob hello'), ('reply', 'answer')):
            self.assertIn("They aren't here", self.run_command(name, text)['to_char'])
        self.assertFalse(CommunicationsApi.has_buffered_tells(self.bob))

    def test_linkdead_lookup_rejects_retired_or_invisible_players(self):
        self.sessions = [session for session in self.sessions if session.character is not self.bob]
        self.flag(self.bob, 'AFF_INVISIBLE')
        self.assertIn("They aren't here", self.run_command('tell', 'Bob hello')['to_char'])
        self.flag(self.bob, 'AFF_INVISIBLE', False)
        self.bob.world_retired = True
        self.actor.context = {'reply_to': self.bob.id}
        for name, text in (('tell', 'Bob hello'), ('reply', 'answer')):
            self.assertIn("They aren't here", self.run_command(name, text)['to_char'])

    def test_sender_notell_still_blocks_disconnected_delivery(self):
        self.sessions = [session for session in self.sessions if session.character is not self.bob]
        self.actor.context = {'reply_to': self.bob.id}
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOTELL)
        for name, text in (('tell', 'Bob hello'), ('reply', 'answer')):
            self.assertNotIn('to_victim', self.run_command(name, text))
        self.assertFalse(CommunicationsApi.has_buffered_tells(self.bob))

    def test_afk_recipient_receives_nothing_live_through_message_bus(self):
        self.afk(self.bob)
        connections = {c.id: NS(send_message=AsyncMock(), is_closed=lambda: False)
                       for c in (self.actor, self.bob)}
        bus = MessageBus(NS(get_connection_by_character=connections.get),
                         NS(get_session_by_character=lambda identifier: None))
        emitter = PlayerHandler.__new__(PlayerHandler)
        emitter.message_bus, emitter._send_prompt = bus, AsyncMock()
        context = self.ctx('tell', 'Bob hello')
        asyncio.run(emitter._emit_standard_payload(self.actor, self.commands.execute(context), context=context))
        connections[self.bob.id].send_message.assert_not_awaited()
        connections[self.actor.id].send_message.assert_awaited_once()
        self.assertIn('AFK', connections[self.actor.id].send_message.call_args.args[0].data['text'])


if __name__ == '__main__':
    unittest.main()

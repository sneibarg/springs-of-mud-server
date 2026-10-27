from types import SimpleNamespace as NS
import unittest
from unittest.mock import AsyncMock, Mock

from tests import test_wiz_recovery_parity as recovery

methods = recovery.methods


class TestImmortalMovementParity(unittest.TestCase):
    def setUp(self):
        fixture = recovery.TestImmortalRecovery()
        fixture.setUp()
        self.__dict__.update(fixture.__dict__)
        self.api.can_see = lambda actor, victim, room: victim.name != 'hidden'
        self.api.get_trust = lambda actor: getattr(actor, 'trust', 60)
        self.actor.trust = 60
        self.util.split_argument = lambda text: tuple((text.split(maxsplit=1) + [''])[:2])
        self.util.name_matches = lambda query, candidate: bool(query) and query.lower() in candidate.lower().split()
        self.old = self.room
        self.old.id = 'room'
        self.old.area_id = 'area'
        self.old.player_targets = lambda actor: []
        self.destination = NS(id='destination', area_id='area', characters={}, mobiles={}, player_targets=lambda actor: [])
        self.rooms = {'room': self.old, 'destination': self.destination}
        self.wiz.room_registry = NS(get_or_none=lambda **kw: self.rooms.get(kw.get('id')))
        self.util.room_of_entity = lambda registry, victim: self.rooms.get(victim.room_id)
        self.moves = []
        def move(registry, victim, room):
            old = self.rooms.get(victim.room_id)
            self.assertIsNone(victim.fighting)
            self.moves.append(victim.id)
            victim.room_id = room.id
            return old
        self.util.move_entity = move
        self.area = NS(find_location=lambda name, *args, **kwargs: self.rooms.get(name))
        self.proto = NS(level=5, new_format=True, short_description='a sword')
        self.created = []
        def create(proto):
            obj = NS(**vars(proto))
            self.created.append(obj)
            return obj
        self.wiz.item_registry = NS(get_or_none=lambda **kw: self.proto)
        self.wiz.WearFlagsEnum = None
        self.actor.add_item = Mock()
        scope = {'WizApi': self.WizApi, 'WizUtil': self.util, 'CharacterApi': self.api,
                 'InterpApi': self.interp, 'AreaApi': self.area,
                 'GenericUtil': NS(to_int=lambda value, default: int(value)),
                 'ItemFactory': NS(create=create), 'ItemApi': NS(item_takeable=lambda *args: True)}
        Wiz = methods('src/interp/commands/Wiz.py', 'Wiz',
                      {'do_goto', 'do_violate', 'do_transfer', '_transfer_target', 'do_load',
                       '_poof_text', '_visible_room_targets'}, scope)
        self.wiz.__class__ = Wiz
        self.wiz._command_text = lambda *args, **kwargs: ''
        self.wiz.wiz_handler.room_is_private_for_actor = lambda *args: False

    def context(self, argument, command='transfer'):
        return NS(character=self.actor, room=self.old, result=None, parameters=argument,
                  command=NS(name=command), finish=Mock())

    def test_teleports_end_both_sides_before_moving(self):
        for command in ('goto', 'violate', 'transfer'):
            with self.subTest(command=command):
                self.actor.room_id = 'room'
                self.target.room_id = 'room'
                self.actor.fighting = self.target
                self.target.fighting = self.actor
                argument = 'target destination' if command == 'transfer' else 'destination'
                getattr(self.wiz, 'do_' + command)(self.actor, self.context(argument, command))
                self.assertIsNone(self.actor.fighting)
                self.assertIsNone(self.target.fighting)
                moved = self.target if command == 'transfer' else self.actor
                self.assertEqual(moved.room_id, 'destination')

    def test_rejected_teleport_preserves_combat(self):
        self.actor.fighting = self.target
        self.wiz.interp_api.evaluate_guards_only = lambda *args: {'blocked': True}
        self.wiz.do_goto(self.actor, self.context('destination', 'goto'))
        self.assertIs(self.actor.fighting, self.target)
        self.assertEqual(self.moves, [])

    def test_transfer_all_filters_sessions_and_preserves_message_recipients(self):
        hidden = recovery.TestImmortalRecovery.entity('hidden')
        limbo = recovery.TestImmortalRecovery.entity('limbo'); limbo.room_id = ''
        self.wiz.wiz_handler.session_handler.get_playing_sessions = lambda: [
            NS(character=v) for v in (self.actor, self.target, hidden, limbo, None)]
        payloads = self.wiz.do_transfer(self.actor, self.context('all destination'))['payloads']
        self.assertEqual(self.moves, ['target'])
        self.assertEqual(len(payloads), 1)
        self.assertIs(payloads[0]['actor'], self.actor)
        self.assertIs(payloads[0]['victim'], self.target)
        self.assertIs(payloads[0]['view_character'], self.target)

    def test_transfer_all_defaults_to_actor_room(self):
        self.target.room_id = 'destination'
        self.wiz.do_transfer(self.actor, self.context('all'))
        self.assertEqual(self.target.room_id, 'room')

    def test_transfer_payload_sends_ack_to_actor_and_room_view_to_victim(self):
        Handler = methods('src/player/PlayerHandler.py', 'PlayerHandler',
                          {'_emit_standard_payload'},
                          {'CharacterApi': self.api, 'Ability': NS(take_improve_messages=lambda v: '')})
        handler = Handler()
        handler._resolve_standard_payload = lambda actor, payload, context: dict(payload)
        handler._show_room_to_character = AsyncMock()
        handler._send_prompt = AsyncMock()
        handler.message_bus = NS(send_to_character=AsyncMock(), text_to_message=lambda text: text)
        context = self.context('target destination')
        payload = self.wiz.do_transfer(self.actor, context)
        # AsyncMock awaits complete immediately; no socket-backed event loop is needed.
        coroutine = handler._emit_standard_payload(self.target, payload, context)
        with self.assertRaises(StopIteration):
            coroutine.send(None)
        messages = handler.message_bus.send_to_character.await_args_list
        self.assertEqual(messages[0].args, ('admin', 'Ok.\r\n'))
        self.assertEqual(messages[1].args, ('target', 'admin has transferred you.\r\n'))
        handler._show_room_to_character.assert_awaited_once_with(self.target, self.destination, context)

    def test_transfer_all_with_no_eligible_sessions_is_empty(self):
        self.wiz.wiz_handler.session_handler.get_playing_sessions = lambda: [NS(character=self.actor)]
        self.assertEqual(self.wiz.do_transfer(self.actor, self.context('all')), {'payloads': []})

    def test_private_destination_denial_does_not_end_combat(self):
        self.target.fighting = self.actor
        self.wiz.wiz_handler.room_is_private_for_actor = lambda *args: True
        self.wiz.do_transfer(self.actor, self.context('target destination'))
        self.assertIs(self.target.fighting, self.actor)
        self.assertEqual(self.moves, [])

    def test_loaded_object_levels_follow_format(self):
        for new_format in (True, False):
            for level in ('', ' 0', ' 12'):
                with self.subTest(new_format=new_format, level=level):
                    self.proto.new_format = new_format
                    self.wiz.do_load(self.actor, self.context('obj 100' + level, 'load'))
                    expected = 5 if new_format else int(level or '60')
                    self.assertEqual(self.created[-1].level, expected)
                    self.assertEqual(self.proto.level, 5)

    def test_object_level_validation_applies_to_both_formats(self):
        for new_format in (True, False):
            self.proto.new_format = new_format
            result = self.wiz.do_load(self.actor, self.context('obj 100 61', 'load'))
            self.assertEqual(result['message_key'], 'invalid_object_level')
        self.assertEqual(self.created, [])

    def test_goto_private_occupancy_and_owner_exemptions(self):
        self.api.get_enum = lambda name: NS(MAX_LEVEL=NS(value=60))
        Handler = methods('src/game/WizHandler.py', 'WizHandler', {'room_is_private_for_actor'},
                          {'CharacterApi': self.api, 'WizUtil': self.util})
        handler = Handler()
        self.destination.owner = ''
        self.destination.is_private = lambda flags: True
        for trust, count, owner, expected in (
                (59, 1, '', True), (60, 1, '', False),
                (60, 2, '', True), (60, 3, 'admin', False)):
            with self.subTest(trust=trust, count=count, owner=owner):
                self.actor.trust = trust
                self.destination.characters = {str(i): object() for i in range(count - 1)}
                self.destination.mobiles = {'npc': object()}
                self.destination.owner = owner
                self.assertEqual(handler.room_is_private_for_actor(
                    self.actor, self.destination, deny_occupied=True), expected)
        self.destination.owner = ''
        self.assertFalse(handler.room_is_private_for_actor(self.actor, self.destination))
        self.destination.is_private = lambda flags: False
        self.assertFalse(handler.room_is_private_for_actor(self.actor, self.destination, deny_occupied=True))

    def test_goto_guard_requests_occupancy_check(self):
        handler = NS(room_is_private_for_actor=Mock(return_value=True))
        Api = methods('src/api/WizApi.py', 'WizApi', {'goto_private'}, {})
        Api.location = lambda view: self.destination
        # The extracted static method resolves its original class by name.
        view = NS(context=NS(character=self.actor, wiz_handler=lambda: handler))
        self.assertTrue(Api.goto_private(view))
        handler.room_is_private_for_actor.assert_called_once_with(
            self.actor, self.destination, deny_occupied=True)


import importlib.util
import sys
import unittest
from dataclasses import dataclass, field
from enum import Enum
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests import test_weapon_hit_effects as weapons
from tests.test_spell_affect_payload_messages import _load_spell_api


DisplayUtil = weapons.WeaponHitHandler._messages.__globals__['DisplayUtil']


class TestElementalVisibility(unittest.TestCase):
    def setUp(self):
        self.seer = SimpleNamespace(id='seer', name='Seer', is_npc=False, sees=True)
        self.blind = SimpleNamespace(id='blind', name='Blind', is_npc=False, sees=False)
        self.victim = SimpleNamespace(id='victim', name='Invisible target', is_npc=False, sees=True)
        self.item = SimpleNamespace(item_type='scroll', short_description='an invisible scroll')
        self.room = SimpleNamespace(characters={'seer': self.seer, 'blind': self.blind})
        self.character_visibility = Mock(side_effect=lambda observer, entity, room: observer.sees)
        self.object_visibility = Mock(side_effect=lambda observer, room, item: observer.sees)
        dependencies = patch.dict(sys.modules, {
            'api.CharacterApi': SimpleNamespace(CharacterApi=SimpleNamespace(
                can_see=self.character_visibility, is_npc=lambda e: e.is_npc)),
            'util.LookupUtil': SimpleNamespace(LookupUtil=SimpleNamespace(object_visible=self.object_visibility)),
        })
        dependencies.start()
        self.addCleanup(dependencies.stop)

    def notice(self):
        rule = {'payload': {channel: {'secondary': '{victim} loses {weapon}.'}
                            for channel in ('toChar', 'toVictim', 'toRoom')}}
        return weapons.WeaponHitHandler._messages(rule, 'secondary', self.seer, self.victim, self.item, self.room)

    def test_individual_character_and_object_substitutions(self):
        messages = self.notice()
        self.assertEqual('Invisible target loses an invisible scroll.\r\n', messages['to_char'])
        self.assertEqual('someone loses something.\r\n', messages['to_room'].for_recipient('blind'))
        self.assertEqual('Invisible target loses an invisible scroll.\r\n', messages['to_room'].for_recipient('seer'))
        self.character_visibility.assert_any_call(self.blind, self.victim, self.room)
        self.object_visibility.assert_any_call(self.blind, self.room, self.item)

    def test_visibility_is_captured_before_objects_or_observers_change(self):
        text = self.notice()['to_room']
        self.seer.sees = False
        self.blind.sees = True
        self.item.short_description = 'changed item'
        self.assertIn('invisible scroll', text.for_recipient('seer'))
        self.assertNotIn('invisible', text.for_recipient('blind'))
        self.assertEqual('someone loses something.\r\n', text.for_recipient('late-arrival'))

    def test_direct_recipient_is_also_rendered_against_visibility(self):
        self.seer.sees = False
        messages = self.notice()
        self.assertEqual('someone loses something.\r\n', messages['to_char'])
        self.assertEqual('Invisible target loses an invisible scroll.\r\n', messages['to_victim'])

    def test_concatenation_preserves_each_recipient_and_plain_damage_text(self):
        first = self.notice()['to_room']
        second = self.notice()['to_room']
        result = weapons.WeaponHitHandler._merge({'to_room': 'Hit.\r\n' + first}, {'to_room': second})['to_room']
        self.assertEqual('Hit.\r\n' + 'someone loses something.\r\n' * 2, result.for_recipient('blind'))
        self.assertEqual('Hit.\r\n' + 'Invisible target loses an invisible scroll.\r\n' * 2,
                         result.for_recipient('seer'))

    def test_spell_queue_keeps_recipient_variants(self):
        Api = _load_spell_api()
        api = Api(Mock(), Mock())
        ctx = SimpleNamespace(actor=SimpleNamespace(id='caster'), victim=None, is_player_source=False,
                              room=self.room, queue_payload=Mock())
        api._queue_damage_payload(ctx, {'to_room': self.notice()['to_room']}, None)
        queued = ctx.queue_payload.call_args.args[0]['to_room']
        self.assertEqual('someone loses something.\r\n', queued.for_recipient('blind'))

    def test_acid_notices_use_per_observer_object_descriptions(self):
        from tests import test_acid_exposure as acid
        fixture = acid.TestAcidExposure()
        fixture.setUp()
        armor = fixture.item('armor')
        armor.short_description = 'hidden armor'
        fixture.victim.inventory = [armor]
        fixture.room.characters = self.room.characters
        Api = _load_spell_api()
        api = Api(fixture.effects, Mock())
        api._find_room_for_entity = Mock(return_value=fixture.room)
        ctx = SimpleNamespace(target=fixture.victim, room=fixture.room, queue_payload=Mock(),
                              spell=SimpleNamespace(message=lambda channel, key, item: item + ' is etched.'))
        game_api = SimpleNamespace(get_enum=acid.ENUMS.get, item_table_map=lambda: acid.DATA['itemTable'])
        with patch.dict(Api.acid_effect.__globals__, GameApi=game_api, DisplayUtil=DisplayUtil), patch.dict(sys.modules, {
                'util.AcidExposure': acid.MODULES['util.AcidExposure'],
                'game.RandomNumberGenerator': SimpleNamespace(RandomNumberGenerator=lambda: fixture.rng)}):
            api.acid_effect(ctx, 80, 200)
        text = ctx.queue_payload.call_args.args[0]['to_room']
        self.assertEqual('something is etched.\r\n', text.for_recipient('blind'))
        self.assertEqual('hidden armor is etched.\r\n', text.for_recipient('seer'))

    def test_poison_room_notice_uses_per_observer_character_names(self):
        from tests import test_poison_exposure as poison
        self.victim.owned_items = lambda: []
        Api = _load_spell_api()
        api = Api(Mock(), Mock())
        api._find_room_for_entity = Mock(return_value=self.room)
        api._fight_handler = Mock(return_value=Mock())
        api.send = Mock()
        spell = SimpleNamespace(message=lambda channel, key, **tokens:
                                tokens.get('victim', '') + ' looks very ill.' if channel == 'to_room' else 'You feel ill.')
        ctx = SimpleNamespace(target=self.victim, room=self.room, spell=spell)
        game_api = SimpleNamespace(get_enum=poison.fixtures.ENUMS.get,
                                   item_table_map=lambda: poison.fixtures.DATA['itemTable'])
        with patch.dict(Api.poison_effect.__globals__, GameApi=game_api, DisplayUtil=DisplayUtil), patch.dict(sys.modules, {
                'util.PoisonExposure': poison.MODULE,
                'game.RandomNumberGenerator': SimpleNamespace(RandomNumberGenerator=Mock)}), patch.object(
                    Api.poison_effect.__globals__['EffectUtil'], 'saves_spell', return_value=False, create=True):
            api.poison_effect(ctx, 80, 200)
        text = api.send.call_args.kwargs['to_room']
        self.assertEqual('someone looks very ill.', text.for_recipient('blind'))
        self.assertEqual('Invisible target looks very ill.', text.for_recipient('seer'))


class MessageType(Enum):
    GAME = 1


@dataclass
class Message:
    type: object
    data: dict
    metadata: dict = field(default_factory=dict)


def load_bus():
    replacements = {
        'injector': SimpleNamespace(inject=lambda cls: cls),
        'area.Area': SimpleNamespace(Area=object), 'area.Room': SimpleNamespace(Room=object),
        'player.Character': SimpleNamespace(Character=object),
        'util.GenericUtil': SimpleNamespace(GenericUtil=SimpleNamespace(to_int=lambda value, default: int(value))),
        'server.LoggerFactory': SimpleNamespace(LoggerFactory=SimpleNamespace(get_logger=lambda *a: Mock())),
        'server.connection.ConnectionManager': SimpleNamespace(ConnectionManager=object),
        'server.connection.TelnetConnection': SimpleNamespace(TelnetConnection=object),
        'server.protocol.Message': SimpleNamespace(Message=Message, MessageType=MessageType),
        'server.session.SessionHandler': SimpleNamespace(SessionHandler=object),
        'server.session.SessionState': SimpleNamespace(SessionStatus=object),
    }
    with patch.dict(sys.modules, replacements):
        spec = importlib.util.spec_from_file_location('_visibility_bus', weapons.ROOT / 'src/server/messaging/MessageBus.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.MessageBus


class TestRecipientDelivery(unittest.TestCase):
    def test_room_delivery_resolves_before_paging_and_snooping_without_mutating_shared_message(self):
        Bus = load_bus()
        connection = SimpleNamespace(is_closed=lambda: False, send_message=AsyncMock())
        bus = Bus(SimpleNamespace(get_connection_by_character=lambda _: connection), SimpleNamespace(
            get_session_by_character=lambda _: SimpleNamespace(metadata={}, character=SimpleNamespace(context={'scroll_lines': 2}))))
        bus._split_into_pages = Mock(side_effect=lambda text, _: [text])
        bus._record_message_spacing = Mock()
        bus._mirror_snoop_output = AsyncMock()
        text = DisplayUtil.room_text('original', lambda observer: 'visible' if observer else 'anonymous',
                                     SimpleNamespace(characters={'seer': SimpleNamespace(id='seer')}))
        message = Message(MessageType.GAME, {'text': text}, metadata={'marker': True})
        async def run():
            await bus.send_to_room(message, [SimpleNamespace(id='seer'), SimpleNamespace(id='blind')])
        # All IO is mocked and completes immediately; avoid opening the Windows
        # event loop's socket pair in restricted test environments.
        with self.assertRaises(StopIteration):
            run().send(None)
        sent = [call.args[0] for call in connection.send_message.await_args_list]
        self.assertEqual(['visible', 'anonymous'], [msg.data['text'] for msg in sent])
        self.assertTrue(all(msg.metadata == {'marker': True} for msg in sent))
        self.assertEqual(['visible', 'anonymous'], [call.args[0] for call in bus._split_into_pages.call_args_list])
        self.assertEqual(['visible', 'anonymous'], [call.args[1].data['text'] for call in bus._mirror_snoop_output.await_args_list])
        self.assertIs(text, message.data['text'])


if __name__ == '__main__':
    unittest.main()

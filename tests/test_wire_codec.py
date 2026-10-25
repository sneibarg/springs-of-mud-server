import json
import unittest
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import ClassVar

from tests.test_update_handler_active_players import Character, build_character_data
from item.Effect import AffectWhere, Effect
from player.CharacterService import CharacterService
from player.Player import Player
from player.PlayerService import PlayerService
from server.WireCodec import serialize_wire_value


class Color(Enum):
    RED = 'red'


class Number(IntEnum):
    ONE = 1


@dataclass
class Record:
    field_name: str
    user_values: dict = field(default_factory=dict)
    class_setting: ClassVar[str] = 'not an instance field'


class WireCodecTests(unittest.TestCase):
    def test_nested_schema_fields_convert_but_mapping_keys_never_collide(self):
        source = Record('schema', {'go_home': Record('nested'), 'goHome': 'distinct',
                                   'two__words': {'Another_Key': 'unchanged'}})
        expected = {'fieldName': 'schema', 'userValues': {
            'go_home': {'fieldName': 'nested', 'userValues': {}}, 'goHome': 'distinct',
            'two__words': {'Another_Key': 'unchanged'}}}
        self.assertEqual(expected, json.loads(json.dumps(serialize_wire_value(source))))
        self.assertIsInstance(source.user_values['go_home'], Record)

    def test_enums_sequences_nulls_and_primitives_are_json_values(self):
        result = serialize_wire_value([None, True, 2, 3.5, Color.RED, Number.ONE, (Color.RED,), {Number.ONE}])
        self.assertEqual([None, True, 2, 3.5, 'red', 1, ['red'], [1]], json.loads(json.dumps(result)))
        self.assertIs(type(result[5]), int)

    def test_recursive_exclusions_belong_to_each_service(self):
        @dataclass
        class RuntimeRecord:
            persisted_field: str = 'value'
            room_data: object = 'rooms'
            connection: object = 'socket'
            current_characters: object = 'characters'
            lock: object = 'lock'
            logger: object = 'logger'
        value = {'nested': [RuntimeRecord()]}
        character = serialize_wire_value(value, excluded_fields=CharacterService._WIRE_EXCLUDED_FIELDS)['nested'][0]
        account = serialize_wire_value(value, excluded_fields=PlayerService._WIRE_EXCLUDED_FIELDS)['nested'][0]
        self.assertNotIn('roomData', character)
        self.assertEqual('socket', character['connection'])
        self.assertEqual({'persistedField': 'value', 'roomData': 'rooms'}, account)
        self.assertIn('room_data', RuntimeRecord.__dataclass_fields__)

    def test_exclusions_do_not_remove_user_dictionary_keys(self):
        data = {'room_data': {'lock': 'user value'}}
        self.assertEqual(data, serialize_wire_value(data, excluded_fields=frozenset({'room_data', 'lock'})))

    def test_results_are_independent_of_mutable_inputs(self):
        source = Record('name', {'a_key': [1]})
        encoded = serialize_wire_value(source)
        source.user_values['a_key'].append(2)
        self.assertEqual([1], encoded['userValues']['a_key'])

    def test_character_round_trip_preserves_nested_effects_aliases_and_prompt_schema(self):
        actor = Character.from_json(build_character_data())
        actor.aliases = {'go_home': 'recall', 'gohome': 'north'}
        actor.effects = [Effect(where=AffectWhere.TO_AFFECTS, apply_to='strength', duration=2)]
        actor.prompt_format.alignment = True
        actor.prompt_format.max_mana = True
        actor.context = {'runtime_only': object()}
        payload = CharacterService._serialize_character(actor)
        self.assertEqual(0, payload['effects'][0]['where'])
        self.assertEqual('strength', payload['effects'][0]['applyTo'])
        self.assertTrue(payload['promptFormat']['max_mana'])
        self.assertNotIn('maxMana', payload['promptFormat'])
        self.assertNotIn('context', payload)
        self.assertNotIn('lock', payload)
        restored = Character.from_json(json.loads(json.dumps(payload)))
        self.assertEqual(actor.aliases, restored.aliases)
        self.assertTrue(restored.prompt_format.alignment)
        self.assertEqual(payload, CharacterService._serialize_character(restored))

    def test_account_round_trip_keeps_explicit_schema_and_omits_runtime_state(self):
        account = Player.from_json(dict(id='account', banned=False, firstName='First', lastName='Last',
                                       accountName='test', emailAddress='example.invalid', password='hash',
                                       playerCharacterList=['character'], ansiEnabled=True, usage='player'))
        account.connection = (object(),)
        account.current_characters = [object()]
        account.session_id = 'runtime-session'
        payload = PlayerService._serialize_player(account)
        self.assertEqual({'id', 'banned', 'firstName', 'lastName', 'accountName', 'emailAddress',
                          'password', 'playerCharacterList', 'ansiEnabled', 'usage'}, set(payload))
        restored = Player.from_json(json.loads(json.dumps(payload)))
        self.assertEqual(payload, PlayerService._serialize_player(restored))


if __name__ == '__main__':
    unittest.main()

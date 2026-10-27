"""Isolate command methods from bootstrap dependencies; exercise ROM state transitions."""
import ast
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]


def methods(path, class_name, names, scope):
    tree = ast.parse((ROOT / path).read_text(encoding='utf-8'))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name)
    cls.body = [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in names]
    cls.decorator_list = []
    exec(compile(ast.fix_missing_locations(ast.Module(body=[cls], type_ignores=[])), path, 'exec'), scope)
    return scope[class_name]


class TestImmortalRecovery(unittest.TestCase):
    def setUp(self):
        self.api = NS(is_npc=lambda v: v.npc, get_trust=lambda v: 60,
                      enum_bit=lambda *a: 1, unset_act_flags=lambda v, bit: setattr(v, 'aggressive', False))
        scope = {'CharacterApi': self.api, 'GenericUtil': NS(to_int=lambda v, d: int(v)),
                 'FightUtil': NS(entity_position_value=lambda v: v.character_attributes.position)}
        Fight = methods('src/combat/CombatHandler.py', 'FightHandler',
                        {'update_pos', '_set_position', '_set_default_combat_position', 'stop_fighting'}, scope)
        self.fight = Fight()
        self.fight.PositionsEnum = NS(**{name: NS(value=i) for i, name in enumerate(
            ['POS_DEAD', 'POS_MORTAL', 'POS_INCAP', 'POS_STUNNED', 'POS_SLEEPING', 'POS_RESTING', 'POS_STANDING'])})
        self.fight.combat_registry = NS(get_by_combatant=lambda _: [])
        self.fight.effect_handler = NS(affect_strip=self.strip)
        self.WizApi = methods('src/api/WizApi.py', 'WizApi', {'restore_character'}, {})
        self.util = NS(argument_text=lambda result, params: params,
                       room_of_entity=lambda registry, v: self.room if v.room_id else None,
                       find_world_entity=lambda *a, **kw: self.target, display_name=lambda v: v.name)
        self.interp = NS(command_payload=lambda key, **kwargs: dict(message_key=key, **kwargs))
        Wiz = methods('src/interp/commands/Wiz.py', 'Wiz',
                      {'do_restore', 'do_peace', '_actor_target_tokens'},
                      {'WizApi': self.WizApi, 'WizUtil': self.util, 'CharacterApi': self.api, 'InterpApi': self.interp})
        self.wiz = Wiz()
        self.actor = self.entity('admin')
        self.target = self.entity('target')
        self.room = NS(characters={'a': self.actor, 't': self.target}, mobiles={}, vnum=1)
        self.wiz.room_registry = NS(get_or_none=lambda **kw: self.room)
        self.wiz.character_registry = None
        self.wiz.interp_api = NS(evaluate_guards_only=lambda *a: None)
        self.wiz.fight_handler = self.fight
        self.wiz.ActBitsEnum = None
        self.wiz.GameParameters = NS(MAX_LEVEL=NS(value=60))
        self.wiz.wiz_handler = NS(session_handler=NS(get_playing_sessions=lambda: [NS(character=v) for v in [self.actor, self.target]]))

    @staticmethod
    def entity(name, npc=False, position=6, hit=10):
        return NS(id=name, name=name, npc=npc, character_attributes=NS(position=position),
                  hit=hit, mana=1, movement=1, max_hit=100, max_mana=80, max_movement=60,
                  effects=[], fighting=None, room_id='room', default_pos=5, aggressive=True)

    @staticmethod
    def strip(victim, name):
        victim.effects[:] = [e for e in victim.effects if e != name]

    def context(self, argument):
        return NS(character=self.actor, room=self.room, result=None, parameters=argument,
                  command=NS(name='restore'), finish=Mock())

    def test_restore_strips_only_rom_ailments_and_recovers_position(self):
        for position in (0, 1, 2, 3, 4, 5):
            with self.subTest(position=position):
                v = self.entity('patient', position=position, hit=-8)
                v.effects = [prefix + name for prefix in ('', 'spell.') for name in
                             ('plague', 'poison', 'blindness', 'sleep', 'curse')] + ['spell.armor']
                self.WizApi.restore_character(v, self.fight)
                self.assertEqual(v.effects, ['spell.armor'])
                self.assertEqual((v.hit, v.mana, v.movement), (100, 80, 60))
                self.assertEqual(v.character_attributes.position, 6 if position <= 3 else position)

    def test_every_restore_mode_recovers_target(self):
        for argument in ('room', 'all', 'target'):
            with self.subTest(argument=argument):
                self.target.effects = ['spell.poison']
                self.target.hit = -8
                self.target.character_attributes.position = 2
                self.wiz.do_restore(self.actor, self.context(argument))
                self.assertEqual(self.target.effects, [])
                self.assertEqual(self.target.character_attributes.position, 6)

    def test_bulk_restore_notifies_each_recipient_before_acknowledgment(self):
        for argument in ('', 'room', 'all'):
            payloads = self.wiz.do_restore(self.actor, self.context(argument))['payloads']
            messages = [p for p in payloads if p.get('channel') == 'to_victim']
            self.assertEqual([p['victim'].id for p in messages], ['admin', 'target'])
            self.assertTrue(all(p['message_key'] == 'default' for p in messages))
            self.assertEqual(payloads[len(messages)]['message_key'], 'active_players' if argument == 'all' else 'room')

    def test_global_restore_skips_npc_and_roomless_notification(self):
        self.target.room_id = ''
        npc = self.entity('mobile', npc=True)
        self.wiz.wiz_handler.session_handler.get_playing_sessions = lambda: [NS(character=v) for v in [self.target, npc]]
        payloads = self.wiz.do_restore(self.actor, self.context('all'))['payloads']
        self.assertEqual(len(payloads), 1)
        self.assertEqual(self.target.hit, 100)
        self.assertEqual(npc.hit, 10)

    def test_peace_preserves_bystanders_and_recovers_combatants(self):
        sleeper = self.entity('sleeper', position=4)
        wounded = self.entity('wounded', position=1, hit=-8)
        mobile = self.entity('mobile', npc=True)
        self.target.hit = -8
        self.target.fighting = mobile
        mobile.fighting = self.target
        self.room.characters.update(s=sleeper, w=wounded)
        self.room.mobiles['m'] = mobile
        self.wiz.do_peace(self.actor, self.context(''))
        self.assertEqual(sleeper.character_attributes.position, 4)
        self.assertEqual(wounded.character_attributes.position, 1)
        self.assertEqual(self.target.character_attributes.position, 1)
        self.assertEqual(mobile.character_attributes.position, 5)
        self.assertIsNone(self.target.fighting)
        self.assertIsNone(mobile.fighting)
        self.assertFalse(mobile.aggressive)

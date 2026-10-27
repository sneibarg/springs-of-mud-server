import json
from copy import deepcopy
from enum import IntEnum
from types import SimpleNamespace as NS
import unittest

from tests import test_wiz_recovery_parity as recovery

methods = recovery.methods
ROOT = recovery.ROOT


class Parameters(IntEnum):
    MAX_LEVEL = 60
    LEVEL_HERO = 51
    GOD = 56
    IMMORTAL = 55
    DEMI = 54
    ANGEL = 53
    AVATAR = 52


class TestForceParity(unittest.TestCase):
    def setUp(self):
        self.actor = NS(name='admin', trust=58, level=58, npc=False)
        self.mortal = NS(name='mortal', trust=10, level=10, npc=False)
        self.hero = NS(name='hero', trust=51, level=51, npc=False)
        self.peer = NS(name='peer', trust=58, level=58, npc=False)
        self.npc = NS(name='npc', trust=1, level=1, npc=True)
        self.entities = [self.actor, self.mortal, self.hero, self.peer, self.npc]
        self.registry = NS(all_characters=lambda: self.entities)
        api = NS(get_enum=lambda name: Parameters, get_trust=lambda v: v.trust, is_npc=lambda v: v.npc)
        util = NS(split_argument=lambda s: tuple((s.split(maxsplit=1) + [''])[:2]),
                  live_world_entities=lambda rooms: self.entities,
                  find_world_entity=lambda registry, rooms, name, **kw: next((v for v in self.entities if v.name == name), None),
                  room_of_entity=lambda *args: None)
        interp = NS(argument_text=lambda v: v.context.parameters,
                    one_argument=util.split_argument)
        self.Api = methods('src/api/WizApi.py', 'WizApi',
                           {name for name in ('force_parts', 'force_missing_argument', 'force_delete', 'force_target',
                            'force_target_missing', 'force_target_self', 'force_private', 'force_target_higher_level',
                            'force_insufficient_level', 'force_targets')},
                           {'WizUtil': util, 'InterpUtil': interp, 'CharacterApi': api})
        self.Api.character_registry = lambda view: self.registry
        self.Api.room_registry = lambda view: None
        command = next(v for v in json.loads((ROOT / 'resources/collections/SOMDB.Commands.json').read_text()) if v['name'] == 'force')
        self.guards = command['guards']
        self.command = NS(name='force')
        def guards(context, name):
            view = NS(context=context)
            for guard in self.guards:
                if eval(guard['predicate'], {'WizApi': self.Api})(view):
                    return {'message_key': guard['messageKey']}
            return None
        Wiz = methods('src/interp/commands/Wiz.py', 'Wiz', {'do_force'},
                      {'WizApi': self.Api, 'InterpApi': NS(command_payload=lambda key: dict(message_key=key))})
        self.wiz = Wiz()
        self.wiz.interp_api = NS(evaluate_guards_only=guards, build_interp_view=lambda ctx: NS(context=ctx))

    def execute(self, text):
        return self.wiz.do_force(self.actor, NS(character=self.actor, parameters=text, command=self.command, finish=lambda: None))

    def test_player_and_all_threshold(self):
        for trust in (53, 56, 57):
            for selector in ('all', 'mortal'):
                with self.subTest(trust=trust, selector=selector):
                    self.actor.trust = trust
                    result = self.execute(selector + ' smile')
                    if trust < 57:
                        self.assertEqual(result['message_key'], 'insufficientLevel')
                    else:
                        self.assertIn('forced_commands', result)

    def test_lower_trust_can_still_force_individual_npc(self):
        self.actor.trust = 53
        self.assertIs(self.execute('npc smile')['forced_commands'][0]['victim'], self.npc)

    def test_all_excludes_npcs_and_equal_or_higher_trust(self):
        victims = [entry['victim'].name for entry in self.execute('all smile')['forced_commands']]
        self.assertEqual(victims, ['mortal', 'hero'])

    def test_group_threshold_and_hero_boundary(self):
        for selector, expected in (('players', ['mortal']), ('gods', ['hero'])):
            self.actor.trust = 57
            self.assertEqual(self.execute(selector + ' smile')['message_key'], 'insufficientLevel')
            self.actor.trust = 58
            victims = [entry['victim'].name for entry in self.execute(selector + ' smile')['forced_commands']]
            self.assertEqual(victims, expected)

    def test_empty_group_and_delete_guard(self):
        self.entities = [self.actor, self.npc]
        self.assertEqual(self.execute('players smile')['forced_commands'], [])
        self.assertEqual(self.execute('gods delete')['message_key'], 'delete')

    def test_single_target_guard_order_is_preserved(self):
        self.actor.trust = 53
        self.assertEqual(self.execute('admin smile')['message_key'], 'targetSelf')
        self.assertEqual(self.execute('peer smile')['message_key'], 'targetHigherLevel')
        self.assertEqual(self.execute('missing smile')['message_key'], 'targetMissing')


class TestCloneContentsParity(unittest.TestCase):
    def setUp(self):
        self.Factory = methods('src/item/ItemFactory.py', 'ItemFactory', {'copy_instance'}, {'deepcopy': deepcopy})
        self.Factory.create = lambda obj: NS(**vars(obj))
        api = NS(get_enum=lambda name: Parameters, get_trust=lambda actor: actor.trust)
        self.Util = methods('src/util/WizUtil.py', 'WizUtil', {'can_clone_object', 'can_clone_mobile'},
                            {'CharacterApi': api, 'GenericUtil': NS(to_int=lambda value, default: int(value))})
        self.actor = NS(name='admin', trust=55)
        self.allowed = self.item('allowed', 20, 1000)
        self.forbidden = self.item('forbidden', 21, 1001)
        self.inner = self.item('inner', 1, 1, [self.allowed, self.forbidden])
        self.denied_container = self.item('denied-container', 30, 5000, [self.allowed])
        self.outer = self.item('outer', 1, 1, [self.inner, self.denied_container])

    @staticmethod
    def item(name, level, cost, contents=None):
        return NS(id=name, name=name, short_description=name, level=level, cost=cost, contains=contents or [], extra_descr=[], effects=[])

    def test_nested_contents_and_denied_subtrees_are_filtered(self):
        clone = self.Factory.copy_instance(self.outer, item_filter=lambda item: self.Util.can_clone_object(self.actor, item))
        self.assertEqual([item.name for item in clone.contains], ['inner'])
        self.assertEqual([item.name for item in clone.contains[0].contains], ['allowed'])
        self.assertEqual(len(self.outer.contains), 2)
        self.assertIsNot(clone.contains[0].contains[0], self.allowed)

    def test_unrestricted_callers_keep_full_contents(self):
        clone = self.Factory.copy_instance(self.outer)
        self.assertEqual(len(clone.contains), 2)
        self.assertEqual(len(clone.contains[0].contains), 2)

    def test_high_trust_can_clone_all_contents(self):
        self.actor.trust = 56
        clone = self.Factory.copy_instance(self.outer, item_filter=lambda item: self.Util.can_clone_object(self.actor, item))
        self.assertEqual(len(clone.contains), 2)
        self.assertEqual(len(clone.contains[0].contains), 2)

    def test_mobile_inventory_equipment_and_nested_contents(self):
        MobileFactory = methods('src/mobile/MobileFactory.py', 'MobileFactory', {'copy_instance'},
                                {'ItemFactory': self.Factory, 'WEAR_LOC_TO_EQUIPPED_SLOT': {},
                                 'GenericUtil': NS(to_int=lambda value, default: int(value)),
                                 'StatusFlags': NS(from_template=lambda flags: flags)})
        mob = NS(**{name: '' for name in ('short_description', 'long_description', 'description', 'name', 'race',
                 'flags', 'group', 'dam_type', 'sex', 'size', 'material', 'hit_roll', 'gold', 'silver', 'start_pos', 'default_pos')})
        mob.level = 1; mob.status_flags = None; mob.get_alignment = lambda: 0
        mob.owned_items = lambda: [self.inner, self.allowed, self.forbidden]
        mob.equipped_slot_of = lambda item: 'head' if item is self.allowed else None
        carried, equipped = [], {}
        MobileFactory.create = lambda *args: NS(set_alignment=lambda value: None, add_item=carried.append,
                                                equip_item=lambda item, slot: equipped.update({slot: item}))
        MobileFactory.copy_instance(mob, None, item_filter=lambda item: self.Util.can_clone_object(self.actor, item))
        self.assertEqual([item.name for item in carried], ['inner'])
        self.assertEqual([item.name for item in carried[0].contains], ['allowed'])
        self.assertEqual(equipped['head'].name, 'allowed')

    def test_clone_command_supplies_filter(self):
        scope = {'WizUtil': self.Util, 'ItemFactory': self.Factory,
                 'CharacterApi': NS(is_npc=lambda obj: False, get_trust=lambda actor: actor.trust),
                 'InterpApi': NS(command_payload=lambda key, **kw: dict(message_key=key, **kw))}
        Wiz = methods('src/interp/commands/Wiz.py', 'Wiz', {'do_clone'}, scope)
        self.Util.argument_text = lambda result, params: params
        self.Util.split_argument = lambda text: tuple(text.split(maxsplit=1))
        room_items = {}
        self.Util.name_matches = lambda *a: True
        room = NS(contents={}, find_room_item=lambda name: self.outer, player_targets=lambda actor: [])
        self.actor.room_id = 'room'; self.actor.find_inventory_item = lambda name: None
        self.actor.add_item = lambda obj: room_items.update(clone=obj)
        wiz = Wiz(); wiz.room_registry = NS(get_or_none=lambda **kw: room)
        wiz.interp_api = NS(evaluate_guards_only=lambda *a: None)
        context = NS(command=NS(name='clone'), result=None, parameters='obj outer', finish=lambda: None)
        wiz.do_clone(self.actor, context)
        self.assertEqual([obj.name for obj in room_items['clone'].contains], ['inner'])

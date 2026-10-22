import importlib.util
import json
import sys
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'resources/collections/SOMDB.GameData.json').read_text())[0]
ENUMS = {name: IntEnum(name, DATA['enums'][name])
         for name in ('itemFlags', 'applyTypes', 'whereAffect', 'affectedBy', 'weaponType')}


class GameApi:
    flags_to_int = staticmethod(lambda value: int(value or 0))
    is_set = staticmethod(lambda flags, bit: bool(flags & bit))
    set_bit = staticmethod(lambda flags, bit: flags | bit)
    unset_bit = staticmethod(lambda flags, bit: flags & ~bit)


def enum_value(enums, value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return int(enums[value]) if value in enums.__members__ else default


def load_runtime():
    replacements = {
        'injector': SimpleNamespace(inject=lambda cls: cls),
        'api.GameApi': SimpleNamespace(GameApi=GameApi),
        'game.EnumProvider': SimpleNamespace(EnumProvider=object),
        'server.LoggerFactory': SimpleNamespace(LoggerFactory=SimpleNamespace(get_logger=lambda *_: Mock())),
        'util.EffectUtil': SimpleNamespace(EffectUtil=SimpleNamespace(enum_value=enum_value)),
    }
    with patch.dict(sys.modules, replacements):
        loaded = {}
        for name, path in [('util.GenericUtil', 'util/GenericUtil.py'),
                           ('item.Effect', 'item/Effect.py'),
                           ('item.EffectHandler', 'item/EffectHandler.py'),
                           ('util.AcidExposure', 'util/AcidExposure.py')]:
            spec = importlib.util.spec_from_file_location(name, ROOT / 'src' / path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            loaded[name] = module
        return loaded


# Restore module state so unrelated tests can use their own runtime fixtures.
with patch.dict(sys.modules):
    MODULES = load_runtime()
Effect = MODULES['item.Effect'].Effect
EffectHandler = MODULES['item.EffectHandler'].EffectHandler
AcidExposure = MODULES['util.AcidExposure'].AcidExposure


class TestAcidExposure(unittest.TestCase):
    def setUp(self):
        self.effects = EffectHandler(SimpleNamespace(get=ENUMS.get))
        self.rng = Mock(number_range=Mock(return_value=1), number_percent=Mock(return_value=1))
        self.exposure = AcidExposure(self.effects, ENUMS['itemFlags'], ENUMS['applyTypes'],
                                     DATA['itemTable'], self.rng)
        self.room = SimpleNamespace(contents={})
        self.room.add_item_to_room = lambda obj: self.room.contents.update({obj.id: obj})
        self.room.remove_item_from_room = lambda obj: self.room.contents.pop(obj.id, None)
        self.victim = SimpleNamespace(inventory=[], equipped=SimpleNamespace(), effects=[],
                                      character_attributes=SimpleNamespace(),
                                      armor_class=SimpleNamespace(piercing=0, bashing=0, slashing=0, magic=0))
        self.victim.owned_items = lambda: list(self.victim.inventory) + [v for v in vars(self.victim.equipped).values() if v]
        self.victim.equipped_slot_of = lambda obj: next((k for k, v in vars(self.victim.equipped).items() if v is obj), None)
        self.victim.remove_item = lambda obj: self.victim.inventory.remove(obj) if obj in self.victim.inventory else None
        def unequip(slot):
            self.victim.inventory.append(getattr(self.victim.equipped, slot))
            setattr(self.victim.equipped, slot, None)
        self.victim.unequip_item = unequip
        self.notify = Mock()

    @staticmethod
    def item(kind, **changes):
        return SimpleNamespace(**dict(dict(id=kind, item_type=kind, level=0, extra_flags=0,
                                          effects=[], contains=[], enchanted=False), **changes))

    def expose(self, obj, level=80, damage=200):
        self.victim.inventory = [obj]
        self.exposure.character(self.victim, level, damage, self.room, self.notify)

    def test_armor_etches_existing_numeric_affect_without_mutating_shared_record(self):
        original = Effect(type='spell.enchant_armor', level=100, duration=-1,
                          where='TO_OBJECT', location=str(int(ENUMS['applyTypes'].APPLY_AC)), modifier='-3')
        armor = self.item('armor', effects=[original])
        self.expose(armor)
        effect = armor.effects[0]
        self.assertEqual((-1, 100, -1, -2), (effect.type, effect.level, effect.duration, effect.modifier))
        self.assertEqual('-3', original.modifier)
        self.assertTrue(armor.enchanted)
        self.assertIn(armor, self.victim.inventory)
        self.expose(armor, level=120)
        self.assertEqual((120, -1), (armor.effects[0].level, armor.effects[0].modifier))

    def test_worn_armor_penalty_survives_remove_and_reapply(self):
        armor = self.item('armor')
        self.victim.equipped.torso = armor
        self.exposure.character(self.victim, 80, 200, self.room, self.notify)
        self.assertEqual([1] * 4, list(vars(self.victim.armor_class).values()))
        self.assertEqual(1, len(armor.effects))
        self.assertEqual((-1, -1, 1), (armor.effects[0].type, armor.effects[0].duration, armor.effects[0].modifier))
        self.effects.remove_item_effects(self.victim, armor)
        self.assertEqual([0] * 4, list(vars(self.victim.armor_class).values()))
        self.effects.apply_item_effects(self.victim, armor)
        self.assertEqual([1] * 4, list(vars(self.victim.armor_class).values()))

    def test_supported_types_destroy_and_other_types_survive(self):
        for kind in ('container', 'pc_corpse', 'npc_corpse', 'clothing', 'staff', 'wand', 'scroll'):
            with self.subTest(kind=kind):
                obj = self.item(kind)
                self.expose(obj)
                self.assertEqual([], self.victim.inventory)
        for kind in ('weapon', 'potion', 'jewelry', 'food'):
            obj = self.item(kind)
            self.expose(obj)
            self.assertEqual([obj], self.victim.inventory)

    def test_protections_and_bypass_prevent_changes(self):
        for flag, gate in (('ITEM_BURN_PROOF', 1), ('ITEM_NOPURGE', 1), (None, 0)):
            obj = self.item('scroll', extra_flags=int(ENUMS['itemFlags'][flag]) if flag else 0)
            self.rng.number_range.return_value = gate
            self.expose(obj)
            self.assertEqual([obj], self.victim.inventory)
        self.notify.assert_not_called()

    def test_chance_softcaps_bless_level_type_bonus_and_inclusive_endpoint(self):
        # 400/4 + 800/10 = 180 -> 102 -> 76; bless -5; level -20; scroll +10 = 61.
        for roll, destroyed in ((61, True), (62, False)):
            obj = self.item('scroll', level=10, extra_flags=int(ENUMS['itemFlags'].ITEM_BLESS))
            self.rng.number_percent.return_value = roll
            self.expose(obj, 400, 800)
            self.assertEqual(destroyed, not self.victim.inventory)

    def test_destroyed_container_spills_children_and_halves_exposure(self):
        # Parent chance 32; child at (40,100) has 20+10 scroll bonus = 30.
        child = self.item('scroll')
        bag = self.item('container', contains=[child])
        self.rng.number_percent.side_effect = [32, 31]
        self.expose(bag)
        self.assertEqual([], bag.contains)
        self.assertEqual([], self.victim.inventory)
        self.assertIs(child, self.room.contents['scroll'])
        self.assertEqual(['acid_container'], [call.args[0] for call in self.notify.call_args_list])

    def test_focus_penalty_and_chance_bounds(self):
        for kind, level, damage, roll, destroyed in (
                ('staff', 80, 200, 22, True), ('wand', 80, 200, 23, False),
                ('clothing', 0, 0, 5, True), ('clothing', 0, 0, 6, False),
                ('scroll', 4000, 4000, 95, True), ('scroll', 4000, 4000, 96, False)):
            with self.subTest(kind=kind, roll=roll):
                obj = self.item(kind)
                self.rng.number_percent.return_value = roll
                self.expose(obj, level, damage)
                self.assertEqual(destroyed, not self.victim.inventory)

    def test_worn_existing_armor_affect_accumulates_exactly_one_penalty_per_hit(self):
        armor = self.item('armor', effects=[Effect(where='TO_OBJECT', location='APPLY_AC', modifier=-3)])
        self.victim.equipped.torso = armor
        self.effects.apply_item_effects(self.victim, armor)
        for expected in (-2, -1):
            self.exposure.character(self.victim, 80, 200, self.room, self.notify)
            self.assertEqual([expected] * 4, list(vars(self.victim.armor_class).values()))
            self.assertEqual(expected, armor.effects[0].modifier)
        self.effects.remove_item_effects(self.victim, armor)
        self.assertEqual([0] * 4, list(vars(self.victim.armor_class).values()))

    def test_destroyed_equipment_removes_modifiers(self):
        staff = self.item('staff', effects=[Effect(where='TO_OBJECT', location='APPLY_AC', modifier=-2)])
        self.victim.equipped.held = staff
        self.effects.apply_item_effects(self.victim, staff)
        self.exposure.character(self.victim, 80, 200, self.room, self.notify)
        self.assertIsNone(self.victim.equipped.held)
        self.assertEqual([], self.victim.inventory)
        self.assertEqual([0] * 4, list(vars(self.victim.armor_class).values()))

    def test_room_items_and_recursive_destruction(self):
        child = self.item('scroll')
        bag = self.item('container', contains=[child])
        self.room.add_item_to_room(bag)
        self.exposure.room(self.room, 80, 200, self.notify)
        self.assertEqual({}, self.room.contents)
        self.assertEqual(['acid_container', 'acid_scroll'], [c.args[0] for c in self.notify.call_args_list])

    def test_no_room_discards_contents_without_recursing_exposure(self):
        nested = self.item('container', contains=[self.item('armor')])
        bag = self.item('container', contains=[nested])
        self.victim.inventory = [bag]
        self.exposure.character(self.victim, 80, 200, None, self.notify)
        self.assertEqual([], self.victim.inventory)
        self.assertEqual([], nested.contains)
        self.assertEqual(1, self.rng.number_percent.call_count)


class TestAcidSpellIntegration(unittest.TestCase):
    def test_actual_spell_payload_reaches_caster_carrier_and_bystanders(self):
        from tests.test_spell_affect_payload_messages import _load_spell_api, Spell
        fixture = TestAcidExposure()
        fixture.setUp()
        armor = fixture.item('armor')
        armor.short_description = 'a steel breastplate'
        fixture.victim.inventory = [armor]
        players = [SimpleNamespace(id=str(i)) for i in range(3)]
        fixture.room.characters = {player.id: player for player in players}
        document = next(doc for doc in json.loads((ROOT / 'resources/collections/SOMDB.Spells.json').read_text())
                        if doc['handlerId'] == 'spell.acid_breath')
        Api = _load_spell_api()
        api = Api(fixture.effects, Mock())
        api._find_room_for_entity = Mock(return_value=fixture.room)
        ctx = SimpleNamespace(target=fixture.victim, room=fixture.room,
                              spell=Spell.from_json({**document, 'levelByClass': {}, 'ratingByClass': {}}),
                              queue_payload=Mock())
        game_api = SimpleNamespace(get_enum=ENUMS.get, item_table_map=lambda: DATA['itemTable'])
        with patch.dict(Api.acid_effect.__globals__, GameApi=game_api), patch.dict(sys.modules, {
                'util.AcidExposure': MODULES['util.AcidExposure'],
                'game.RandomNumberGenerator': SimpleNamespace(RandomNumberGenerator=lambda: fixture.rng)}):
            self.assertTrue(api.acid_effect(ctx, 80, 200))
        self.assertEqual(1, armor.effects[0].modifier)
        ctx.queue_payload.assert_called_once_with({
            'to_room': 'a steel breastplate is pitted and etched.\r\n', 'targets': players})

    def test_collection_lambda_scales_exposure_before_damage_for_both_save_outcomes(self):
        from tests.test_spell_affect_payload_messages import _load_spell_api
        Api = _load_spell_api()
        api = Api(Mock(), Mock())
        spell = next(doc for doc in json.loads((ROOT / 'resources/collections/SOMDB.Spells.json').read_text())
                     if doc['handlerId'] == 'spell.acid_breath')
        ctx = SimpleNamespace(level=80, victim=object(), spell=SimpleNamespace(noun_damage=spell['nounDamage']),
                              actor=object(), mark_performed=Mock(return_value=True))
        ctx.damage_expr = lambda *args, **kwargs: api.damage_expr(ctx, *args, **kwargs)
        api.eval_int = Mock(return_value=200)
        api._queue_damage_payload = Mock()
        for saved, expected in ((False, (80, 200, 200)), (True, (40, 50, 100))):
            with self.subTest(saved=saved):
                events = []
                api.acid_effect = Mock(side_effect=lambda *a, **kw: events.append(('exposure', a[1], a[2])))
                fight = Mock()
                fight.damage.side_effect = lambda *a, **kw: events.append(('damage', a[2])) or {}
                api._fight_handler = Mock(return_value=fight)
                effect_util = Api.damage_expr.__globals__['EffectUtil']
                with patch.object(effect_util, 'saves_spell', return_value=saved, create=True):
                    self.assertTrue(eval(spell['lambdas'][0])(ctx))
                self.assertEqual([('exposure', expected[0], expected[1]), ('damage', expected[2])], events)
        self.assertEqual('{item} is pitted and etched.', spell['payload']['toRoom']['acidArmor'])


if __name__ == '__main__':
    unittest.main()

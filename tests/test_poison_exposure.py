import importlib.util
import json
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_acid_exposure as fixtures


with patch.dict(sys.modules, {'api.GameApi': SimpleNamespace(GameApi=fixtures.GameApi),
                              'item.Effect': fixtures.MODULES['item.Effect']}):
    spec = importlib.util.spec_from_file_location('_poison_exposure_test', fixtures.ROOT / 'src/util/PoisonExposure.py')
    MODULE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(MODULE)
PoisonExposure = MODULE.PoisonExposure


class TestPoisonExposure(unittest.TestCase):
    def setUp(self):
        self.effects = fixtures.EffectHandler(SimpleNamespace(get=fixtures.ENUMS.get))
        self.rng = Mock(number_range=Mock(return_value=1), number_percent=Mock(return_value=1))
        self.exposure = PoisonExposure(self.effects, fixtures.ENUMS['itemFlags'], fixtures.DATA['itemTable'], self.rng)

    @staticmethod
    def item(kind='food', **values):
        return SimpleNamespace(**dict(dict(item_type=kind, extra_flags=0, level=0, value0='10',
                                          value1='5', value3='0', contains=[]), **values))

    def test_protections_bypass_and_nopurge_exception(self):
        for flag, gate, poisoned in (('ITEM_BURN_PROOF', 1, False), ('ITEM_BLESS', 1, False),
                                     ('ITEM_NOPURGE', 1, True), (None, 0, False)):
            with self.subTest(flag=flag, gate=gate):
                item = self.item(extra_flags=int(fixtures.ENUMS['itemFlags'][flag]) if flag else 0)
                self.rng.number_range.return_value = gate
                self.exposure.object(item, 80, 200)
                self.assertEqual('1' if poisoned else '0', item.value3)

    def test_drink_capacity_equality_guard_including_empty_container(self):
        for capacity, amount, poisoned in ((10, 10, False), (10, 0, True), (10, 5, True), (0, 0, False)):
            item = self.item('drink', value0=str(capacity), value1=str(amount))
            self.exposure.object(item, 80, 200)
            self.assertEqual('1' if poisoned else '0', item.value3)

    def test_only_food_and_drink_are_contaminated_and_contents_are_not_traversed(self):
        for kind in ('food', 'drink', 'ITEM_DRINK_CON', 'fountain', 'weapon', 'potion', 'container'):
            child = self.item()
            item = self.item(kind, contains=[child])
            self.exposure.object(item, 80, 200)
            self.assertEqual('1' if kind in ('food', 'drink', 'ITEM_DRINK_CON') else '0', item.value3)
            self.assertEqual('0', child.value3)

    def test_softcaps_item_level_clamps_and_inclusive_endpoint(self):
        # 100 + 80 -> 102 -> 76, then level-10 penalty -> 56.
        for level, damage, item_level, roll, poisoned in (
                (400, 800, 10, 56, True), (400, 800, 10, 57, False),
                (0, 0, 50, 5, True), (0, 0, 50, 6, False),
                (4000, 4000, 0, 95, True), (4000, 4000, 0, 96, False)):
            item = self.item(level=item_level)
            self.rng.number_percent.return_value = roll
            self.exposure.object(item, level, damage)
            self.assertEqual('1' if poisoned else '0', item.value3)

    def test_character_save_does_not_protect_inventory_and_failed_saves_join(self):
        item = self.item()
        victim = SimpleNamespace(effects=[], character_attributes=SimpleNamespace(strength=15),
                                 status_flags=Mock(affected_by=0), owned_items=lambda: [item])
        saves = Mock(return_value=True)
        notify = Mock()
        self.exposure.character(victim, 80, 200, saves, notify)
        saves.assert_called_once_with(30, victim, 'DAM_POISON')
        self.assertEqual('1', item.value3)
        self.assertEqual([], victim.effects)
        notify.assert_not_called()
        saves.return_value = False
        self.exposure.character(victim, 80, 200, saves, notify)
        self.exposure.character(victim, 40, 50, saves, notify)
        effect, = victim.effects
        self.assertEqual(('spell.poison', 60, 60, -2, 'AFF_POISON'),
                         (effect.type, effect.level, effect.duration, effect.modifier, effect.bitvector))
        self.assertEqual(13, victim.character_attributes.strength)
        self.assertEqual(2, notify.call_count)

    def test_room_exposure_checks_floor_items(self):
        food = self.item()
        room = SimpleNamespace(contents={'food': food})
        self.exposure.room(room, 80, 200)
        self.assertEqual('1', food.value3)
        self.assertIs(food, room.contents['food'])


class TestGasBreathIntegration(unittest.TestCase):
    def test_floor_exposure_still_runs_when_every_character_is_safe(self):
        from tests.test_spell_affect_payload_messages import _load_spell_api
        Api = _load_spell_api()
        api = Api(Mock(), Mock())
        actor, safe, room = object(), object(), object()
        ctx = SimpleNamespace(actor=actor, room=room, level=80, mark_performed=Mock(return_value=True))
        api._room_entities = Mock(return_value=[actor, safe])
        fight = Mock()
        fight.is_safe_spell.return_value = True
        api._fight_handler = Mock(return_value=fight)
        api.eval_int = Mock(return_value=200)
        api.poison_effect = Mock()
        self.assertTrue(api.damage_room_expr(ctx, 'dice(level, 12)', 'DAM_POISON', effect='poison'))
        api.poison_effect.assert_called_once_with(ctx, 80, 200, target=room)
        ctx.mark_performed.assert_called_once()
        fight.damage.assert_not_called()

    def test_collection_lambda_room_first_then_scaled_character_effects_before_damage(self):
        from tests.test_spell_affect_payload_messages import _load_spell_api
        Api = _load_spell_api()
        api = Api(Mock(), Mock())
        doc = next(doc for doc in json.loads((fixtures.ROOT / 'resources/collections/SOMDB.Spells.json').read_text())
                   if doc['handlerId'] == 'spell.gas_breath')
        victim1, victim2, safe = object(), object(), object()
        ctx = SimpleNamespace(level=80, room=object(), actor=object(), spell=SimpleNamespace(noun_damage='gas'),
                              mark_performed=Mock(return_value=True))
        ctx.damage_room_expr = lambda *a, **kw: api.damage_room_expr(ctx, *a, **kw)
        api._room_entities = Mock(return_value=[ctx.actor, victim1, safe, victim2])
        api.eval_int = Mock(return_value=200)
        events = []
        api.poison_effect = Mock(side_effect=lambda ctx, level, dam, target: events.append(('exposure', target, level, dam)))
        fight = Mock()
        fight.is_safe_spell.side_effect = lambda actor, victim, area: victim is safe
        fight.damage.side_effect = lambda actor, victim, dam, **kw: events.append(('damage', victim, dam)) or {}
        api._fight_handler = Mock(return_value=fight)
        api._queue_damage_payload = Mock()
        with patch.object(Api.damage_room_expr.__globals__['EffectUtil'], 'saves_spell',
                          side_effect=[True, False], create=True):
            self.assertTrue(eval(doc['lambdas'][0])(ctx))
        self.assertEqual([('exposure', ctx.room, 80, 200), ('exposure', victim1, 40, 50),
                          ('damage', victim1, 100), ('exposure', victim2, 80, 200), ('damage', victim2, 200)], events)
        api.eval_int.assert_called_once()

    def test_poison_effect_renders_collection_messages_for_victim_and_room(self):
        from tests.test_spell_affect_payload_messages import _load_spell_api, Spell
        fixture = TestPoisonExposure()
        fixture.setUp()
        Api = _load_spell_api()
        api = Api(fixture.effects, Mock())
        victim = SimpleNamespace(name='target', effects=[], character_attributes=SimpleNamespace(strength=15),
                                 status_flags=Mock(affected_by=0), owned_items=lambda: [])
        document = next(doc for doc in json.loads((fixtures.ROOT / 'resources/collections/SOMDB.Spells.json').read_text())
                        if doc['handlerId'] == 'spell.gas_breath')
        ctx = SimpleNamespace(target=victim, spell=Spell.from_json({**document, 'levelByClass': {}, 'ratingByClass': {}}))
        ctx.room = None
        api._find_room_for_entity = Mock(return_value=None)
        api.send = Mock()
        api._fight_handler = Mock(return_value=Mock())
        with patch.dict(Api.poison_effect.__globals__, GameApi=SimpleNamespace(
                get_enum=fixtures.ENUMS.get, item_table_map=lambda: fixtures.DATA['itemTable'])), patch.dict(sys.modules, {
                    'util.PoisonExposure': MODULE,
                    'game.RandomNumberGenerator': SimpleNamespace(RandomNumberGenerator=lambda: fixture.rng)}), patch.object(
                        Api.poison_effect.__globals__['EffectUtil'], 'saves_spell', return_value=False, create=True) as saves:
            self.assertTrue(api.poison_effect(ctx, 40, 50))
            self.assertEqual((12, victim, 'DAM_POISON'), saves.call_args.args)
        self.assertEqual('spell.poison', victim.effects[0].type)
        self.assertEqual('You feel poison coursing through your veins.\r\n', api.send.call_args.kwargs['to_victim'])
        self.assertEqual('target looks very ill.\r\n', api.send.call_args.kwargs['to_room'])
        self.assertTrue(api.send.call_args.kwargs['include_actor_in_room'])

    def test_typed_saves_include_immunity_resistance_mana_and_strict_endpoint(self):
        from tests.test_effect_util_affects import _load_effect_util
        Util = _load_effect_util()
        victim = SimpleNamespace(level=10, saving_throw=0, character_class=SimpleNamespace(mana_gain=False))
        char_api = SimpleNamespace(is_affected_by_name=lambda *a: False, get_enum=lambda *a: None, is_npc=lambda v: False)
        immunity = Mock()
        with patch.dict(Util.saves_spell.__globals__, CharacterApi=char_api):
            for status, mana, roll, expected in (('IS_NORMAL', False, 50, False), ('IS_NORMAL', False, 49, True),
                    ('IS_RESISTANT', False, 51, True), ('IS_VULNERABLE', False, 48, False),
                    ('IS_NORMAL', True, 45, False), ('IS_NORMAL', True, 44, True)):
                immunity.return_value = status
                victim.character_class.mana_gain = mana
                with patch('random.randint', return_value=roll):
                    self.assertEqual(expected, Util.saves_spell(10, victim, 'DAM_POISON', immunity=immunity))
            immunity.return_value = 'IS_IMMUNE'
            with patch('random.randint') as roll:
                self.assertTrue(Util.saves_spell(100, victim, 'DAM_POISON', immunity=immunity))
                roll.assert_not_called()


if __name__ == '__main__':
    unittest.main()

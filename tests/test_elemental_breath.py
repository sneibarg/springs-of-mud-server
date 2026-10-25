import json
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_weapon_hit_effects as weapons
from tests.test_spell_affect_payload_messages import _load_spell_api


DOCUMENTS = {doc['name']: doc for doc in json.loads(
    (weapons.ROOT / 'resources/collections/SOMDB.Spells.json').read_text())}


class TestElementalBreath(unittest.TestCase):
    def setUp(self):
        self.Api = _load_spell_api()
        self.api = self.Api(Mock(), Mock())
        self.primary = SimpleNamespace(is_npc=False)
        self.other = SimpleNamespace(is_npc=False)
        self.actor = SimpleNamespace(is_npc=False)
        self.room = object()
        self.ctx = SimpleNamespace(victim=self.primary, actor=self.actor, room=self.room, level=80,
                                   spell=SimpleNamespace(noun_damage='breath'), mark_performed=Mock(return_value=True))
        self.api._find_room_for_entity = Mock(return_value=self.room)
        self.api._room_entities = Mock(return_value=[self.actor, self.primary, self.other])
        self.api.eval_int = Mock(return_value=200)
        self.api._queue_damage_payload = Mock()
        self.fight = Mock()
        self.fight.is_safe_spell.return_value = False
        self.fight.damage.return_value = {}
        self.api._fight_handler = Mock(return_value=self.fight)

    def test_fire_and_frost_collection_lambdas_scale_primary_and_collateral(self):
        for name, kind in [('fire breath', 'flaming'), ('frost breath', 'frost')]:
            for saved in (False, True):
                with self.subTest(name=name, saved=saved):
                    events = []
                    self.api.elemental_effect = Mock(side_effect=lambda ctx, kind, level, dam, target:
                                                     events.append(('effect', target, level, dam)))
                    self.fight.damage.side_effect = lambda actor, victim, dam, **kw: events.append(('damage', victim, dam)) or {}
                    self.ctx.elemental_breath = lambda *a, **kw: self.api.elemental_breath(self.ctx, *a, **kw)
                    with patch.object(self.Api.elemental_breath.__globals__['EffectUtil'], 'saves_spell',
                                      return_value=saved, create=True) as saves:
                        self.assertTrue(eval(DOCUMENTS[name]['lambdas'][0])(self.ctx))
                    expected = [('effect', self.room, 80, 100),
                                ('effect', self.primary, 40 if saved else 80, 50 if saved else 200),
                                ('damage', self.primary, 100 if saved else 200),
                                ('effect', self.other, 20 if saved else 40, 25 if saved else 50),
                                ('damage', self.other, 50 if saved else 100)]
                    self.assertEqual(expected, events)
                    self.assertEqual([80, 78], [call.args[0] for call in saves.call_args_list])
                    self.assertEqual(2, saves.call_count)

    def test_lightning_only_exposes_primary_before_damage(self):
        for saved in (False, True):
            events = []
            self.api.elemental_effect = Mock(side_effect=lambda ctx, kind, level, dam, target:
                                             events.append(('effect', target, level, dam)))
            self.fight.damage.side_effect = lambda actor, victim, dam, **kw: events.append(('damage', victim, dam)) or {}
            self.ctx.elemental_breath = lambda *a, **kw: self.api.elemental_breath(self.ctx, *a, **kw)
            with patch.object(self.Api.elemental_breath.__globals__['EffectUtil'], 'saves_spell',
                              return_value=saved, create=True):
                self.assertTrue(eval(DOCUMENTS['lightning breath']['lambdas'][0])(self.ctx))
            self.assertEqual([('effect', self.primary, 40 if saved else 80, 50 if saved else 200),
                              ('damage', self.primary, 100 if saved else 200)], events)
        self.api._room_entities.assert_not_called()

    def test_floor_exposure_precedes_safety_and_runs_when_all_characters_are_safe(self):
        events = []
        self.api.elemental_effect = Mock(side_effect=lambda *a, **kw: events.append('floor'))
        self.fight.is_safe_spell.side_effect = lambda *a, **kw: events.append('safe') or True
        self.assertTrue(self.api.elemental_breath(self.ctx, '200', 'flaming', area=True))
        self.assertEqual(['floor', 'safe', 'safe'], events)
        self.fight.damage.assert_not_called()
        self.api.eval_int.assert_called_once()

    def test_area_breath_preserves_rom_mutual_combat_requirement_for_npcs(self):
        self.actor.is_npc = self.primary.is_npc = self.other.is_npc = True
        self.actor.fighting = self.primary
        self.primary.fighting = self.actor
        self.other.fighting = None
        self.api.elemental_effect = Mock()
        with patch.object(self.Api.elemental_breath.__globals__['EffectUtil'], 'saves_spell',
                          return_value=False, create=True):
            self.api.elemental_breath(self.ctx, '200', 'frost', area=True)
        self.assertEqual(1, self.fight.damage.call_count)
        self.assertIs(self.primary, self.fight.damage.call_args.args[1])

    def test_missing_primary_does_not_roll_damage_or_expose_room(self):
        self.ctx.victim = None
        self.api.elemental_effect = Mock()
        self.assertFalse(self.api.elemental_breath(self.ctx, '200', 'flaming', area=True))
        self.api.eval_int.assert_not_called()
        self.api.elemental_effect.assert_not_called()


class TestSharedElementalExposure(unittest.TestCase):
    def setUp(self):
        weapons.TestWeaponHitEffects.setUpClass()
        self.fixture = weapons.TestWeaponHitEffects()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.handler = self.fixture.handler
        self.handler.elemental_exposure._saves = Mock(return_value=False)
        self.handler.rng.number_percent.return_value = 1

    def expose(self, name, kind, target=None, level=80, damage=200):
        f = self.fixture
        return self.handler.expose(kind, f.attacker, target or f.victim, level, damage, f.room,
                                   f.immunity, payload=DOCUMENTS[name]['payload'])

    def test_fire_blindness_and_frost_chill_use_shared_weapon_implementation(self):
        f = self.fixture
        for name, kind, effect_type, duration, condition in (
                ('fire breath', 'flaming', 'spell.fire_breath', 8, 'thirst'),
                ('frost breath', 'frost', 'spell.chill_touch', 6, 'hunger')):
            result = self.expose(name, kind)
            method = f.effects.affect_to_char if kind == 'flaming' else f.effects.affect_join
            effect = method.call_args.args[1]
            self.assertEqual((effect_type, 80, duration), (effect.type, effect.level, effect.duration))
            f.victim.gain_condition.assert_called_with(condition, 10)
            self.assertTrue(result['to_victim'])
            self.handler.elemental_exposure._saves.assert_called_with(30, f.victim, self.handler.rules[kind]['damageType'], f.immunity)

    def test_existing_blindness_skips_secondary_save_but_still_exposes_gear(self):
        f = self.fixture
        f.victim.status_flags.affected_by = int(f.enums['affectedBy'].AFF_BLIND)
        item = f._item('scroll', 'scroll')
        f.victim.inventory = [item]
        result = self.expose('fire breath', 'flaming')
        self.handler.elemental_exposure._saves.assert_not_called()
        f.effects.affect_to_char.assert_not_called()
        self.assertEqual([], f.victim.inventory)
        self.assertIn('scroll crackles', result['to_victim'])

    def test_saved_character_still_exposes_gear(self):
        f = self.fixture
        self.handler.elemental_exposure._saves.return_value = True
        f.victim.inventory = [f._item('potion', 'potion')]
        self.expose('frost breath', 'frost')
        self.assertEqual([], f.victim.inventory)
        f.effects.affect_join.assert_not_called()

    def test_lightning_daze_preserves_longer_duration_and_destroys_equipment(self):
        f = self.fixture
        for existing, expected in ((0, 30), (50, 50)):
            f.victim.status_flags.pulse_daze = existing
            f.victim.inventory = [f._item('wand', 'wand')]
            result = self.expose('lightning breath', 'shocking')
            self.assertEqual(expected, f.victim.status_flags.pulse_daze)
            self.assertEqual([], f.victim.inventory)
            self.assertIn('muscles stop responding', result['to_victim'])

    def test_floor_fire_spills_contents_and_frost_shatters_potions(self):
        f = self.fixture
        child = f._item('scroll', 'scroll')
        bag = f._item('bag', 'container')
        bag.contains = [child]
        room = SimpleNamespace(contents={'bag': bag}, add_item_to_room=Mock(), remove_item_from_room=Mock())
        result = self.expose('fire breath', 'flaming', target=room)
        room.add_item_to_room.assert_called_once_with(child)
        self.assertEqual(2, room.remove_item_from_room.call_count)
        self.assertIn('scroll crackles', result['to_room'])
        potion = f._item('potion', 'potion')
        room.contents = {'potion': potion}
        result = self.expose('frost breath', 'frost', target=room)
        self.assertIn('potion freezes', result['to_room'])

    def test_spell_payload_overrides_weapon_messages(self):
        f = self.fixture
        result = self.handler.expose('shocking', f.attacker, f.victim, 80, 200, f.room, f.immunity,
                                     payload={'toVictim': {'secondary': 'Custom spell notice'}})
        self.assertEqual('Custom spell notice\r\n', result['to_victim'])

    def test_spell_adapter_routes_floor_notices_to_all_room_players(self):
        Api = _load_spell_api()
        api = Api(Mock(), Mock())
        players = [SimpleNamespace(id='caster'), SimpleNamespace(id='victim')]
        room = SimpleNamespace(contents={}, characters={'caster': players[0], 'victim': players[1]})
        fight = Mock(weapon_hit_handler=self.handler)
        api._fight_handler = Mock(return_value=fight)
        api._find_room_for_entity = Mock(return_value=room)
        ctx = SimpleNamespace(actor=self.fixture.attacker, room=room, target=room, queue_payload=Mock(),
                              spell=SimpleNamespace(payload=DOCUMENTS['frost breath']['payload']))
        room.contents['potion'] = self.fixture._item('potion', 'potion')
        room.remove_item_from_room = Mock()
        api.elemental_effect(ctx, 'frost', 80, 200)
        self.assertEqual(players, ctx.queue_payload.call_args.args[0]['targets'])
        self.assertIn('potion freezes', ctx.queue_payload.call_args.args[0]['to_room'])


if __name__ == '__main__':
    unittest.main()

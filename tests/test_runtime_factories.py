import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_mobile_armor_isolation as mobile_fixtures
from tests import test_item_persistence as item_fixtures
from game.Equipped import Equipped
from item.Effect import Effect
from item.ExtraDescriptionData import ExtraDescriptionData
from item.Item import Item
from item.ItemFactory import ItemFactory
from item.ItemService import ItemService
from mobile.MobileFactory import MobileFactory
from mobile.MobileService import MobileService


class RuntimeFactoryTests(unittest.TestCase):
    def test_item_service_uses_factory_with_both_ability_registries(self):
        service = ItemService.__new__(ItemService)
        service.game_data = SimpleNamespace(liquids={'water': {}})
        service.spell_registry, service.skill_registry = Mock(), Mock()
        document = {'id': 'prototype'}
        with patch.object(ItemFactory, 'from_data', return_value=self.item('prototype')) as build:
            result = service._build_fetch_item(document)
        build.assert_called_once_with(document, service.game_data.liquids,
                                      (service.spell_registry, service.skill_registry))
        self.assertEqual('prototype', result.id)

    def test_mobile_service_binds_special_after_factory_construction(self):
        service = MobileService.__new__(MobileService)
        service.game_data = SimpleNamespace(races={'human': {}})
        special = SimpleNamespace(name='guard', special_function=['lambda ctx: ctx.finish()'])
        service.special_registry = SimpleNamespace(for_mobile=Mock(return_value=special))
        prototype = SimpleNamespace(id='prototype', area_id='area', vnum='100')
        document = {'id': 'prototype'}
        with patch.object(MobileFactory, 'from_data', return_value=prototype) as build:
            result = service._build_fetch_item(document)
        build.assert_called_once_with(document, service.game_data.races)
        service.special_registry.for_mobile.assert_called_once_with('area', '100')
        self.assertEqual('guard', result.special_name)
        self.assertEqual(special.special_function, result.special_function)
        self.assertIsNot(special.special_function, result.special_function)

    def test_mobile_service_data_preserves_identity_and_normalizes_fields(self):
        document = {
            'id': 'prototype', 'areaId': 'area', 'vnum': '100',
            'name': 'guard', 'race': 'human', 'level': '10', 'gold': 50,
            'startPos': 8, 'defaultPos': 8, 'sex': '1', 'size': 'medium',
            'statusFlags': {'act': '1'},
            'hitDice': '{"number": 2, "type": 6, "bonus": 5}',
            'manaDice': '{"number": 1, "type": 6, "bonus": 0}',
            'damageDice': '{"number": 1, "type": 4, "bonus": 0}',
            'armorClass': '{"pierce": 70, "slash": 60, "bash": 50, "exotic": 40}',
        }
        mobile = MobileFactory.from_data(document, {'human': {'id': 'human'}})
        self.assertEqual('prototype', mobile.id)
        self.assertEqual('area', mobile.area_id)
        self.assertEqual(10, mobile.level)
        self.assertEqual(50, mobile.gold)
        self.assertEqual(2, mobile.hit_dice.number)
        self.assertEqual(70, mobile.armor_class.pierce)
        self.assertEqual(1, mobile.status_flags.act)
        self.assertIsNone(mobile.character_attributes)
        self.assertNotIn('area_id', document)

    def item(self, identifier):
        return Item.from_json(item_fixtures.TestItemPersistence._document(identifier))

    def test_spawn_does_not_copy_room_ownership_or_contents(self):
        source = self.item('bag')
        source.contains = [self.item('gem')]
        # A live room contains locks and may refer back to the source item.
        source.room_data = {'room': source}
        source.extra_description = ExtraDescriptionData(True, 'bag', 'A stitched bag.')
        source.effects = [Effect(type='spell.bless', modifier=2)]
        spawned = ItemFactory.create(source)
        self.assertNotEqual(source.id, spawned.id)
        self.assertEqual({}, spawned.room_data)
        self.assertEqual([], spawned.contains)
        self.assertEqual('A stitched bag.', spawned.extra_description.description)
        spawned.effects[0].modifier = 99
        self.assertEqual(2, source.effects[0].modifier)
        self.assertEqual(1, len(source.contains))

    def test_copy_preserves_current_values_and_independent_nested_state(self):
        source = self.item('bag')
        source.enchanted = True
        source.extra_description = ExtraDescriptionData(True, 'bag', 'A stitched bag.')
        source.contains = [self.item('gem')]
        source.contains[0].effects = [Effect(modifier=3)]
        copied = ItemFactory.copy_instance(source)
        self.assertTrue(copied.enchanted)
        self.assertEqual('A stitched bag.', copied.extra_description.description)
        self.assertIsNot(source.extra_description, copied.extra_description)
        self.assertNotEqual(source.contains[0].id, copied.contains[0].id)
        copied.contains[0].effects[0].modifier = 99
        self.assertEqual(3, source.contains[0].effects[0].modifier)

    def test_mobile_copy_handles_equipped_only_and_unworn_items_once(self):
        fixture = mobile_fixtures.MobileArmorIsolationTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        source = MobileFactory.create(fixture.prototype, fixture.enums)
        worn, carried = self.item('sword'), self.item('bag')
        carried.contains = [self.item('gem')]
        source.equipped = Equipped(wielded=worn)
        # Also tolerate reset-loaded equipment present in both ownership views.
        source.inventory = [carried, worn]
        copied = MobileFactory.copy_instance(source, fixture.enums)
        self.assertEqual(2, len(copied.owned_items()))
        self.assertEqual('sword', copied.equipped.wielded.name)
        self.assertEqual(['bag'], [item.name for item in copied.inventory])
        self.assertIsNot(worn, copied.equipped.wielded)
        copied.inventory[0].contains.clear()
        self.assertEqual(1, len(carried.contains))

    def test_factories_reject_missing_prototypes(self):
        with self.assertRaises(ValueError):
            ItemFactory.create(None)
        with self.assertRaises(ValueError):
            MobileFactory.create(None, None)


if __name__ == '__main__':
    unittest.main()

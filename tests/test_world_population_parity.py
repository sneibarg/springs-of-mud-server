import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_shared_gameplay_parity import SharedFixture
from area.AreaHandler import AreaHandler
from area.Room import Room
from mobile.MobileFactory import MobileFactory
from mobile.Dice import Dice
from mobile.ArmorClass import ArmorClass


class WorldPopulationParityTests(SharedFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.other = Room(id='other', area_id='another-area')
        self.handler = AreaHandler.__new__(AreaHandler)
        self.handler.room_registry = NS(get=lambda **kw: self.room,
                                        all_rooms=lambda: [self.room, self.other])
        self.handler.enum_provider = self.enums
        self.handler._mark_pet_shop_stock_mob = Mock()
        self.handler._register_live_character = Mock()
        self.prototype = self.npc()
        self.handler.mobile_registry = NS(get=lambda **kw: self.prototype)
        self.reset = NS(arg1=self.prototype.vnum, arg2=1, arg3=self.room.id, arg4=1)

    def test_global_cap_includes_mobile_that_wandered_to_other_area(self):
        self.other.add_mobile_to_room(self.npc())
        with patch('area.AreaHandler.MobileFactory.create') as create:
            self.assertEqual((False, None), self.handler._do_mob_reset(True, self.reset))
            create.assert_not_called()

    def test_room_cap_is_independent_of_global_cap(self):
        self.reset.arg2 = 5
        self.room.add_mobile_to_room(self.npc())
        with patch('area.AreaHandler.MobileFactory.create') as create:
            self.assertEqual((False, None), self.handler._do_mob_reset(True, self.reset))
            create.assert_not_called()

    def test_mobile_spawns_below_both_caps(self):
        self.reset.arg2 = 2
        self.other.add_mobile_to_room(self.npc())
        spawned = self.npc()
        with patch('area.AreaHandler.MobileFactory.create', return_value=spawned):
            self.assertEqual((True, spawned), self.handler._do_mob_reset(True, self.reset))
        self.assertIs(self.room.mobiles[spawned.id], spawned)
        self.handler._register_live_character.assert_called_once_with(spawned)

    def object_reset(self, vnum):
        return self.handler._do_object_reset(NS(arg1=vnum, arg3=self.room.id), NS(number_of_players=0))

    def test_distinct_floor_resets_coexist_duplicates_are_suppressed_and_cost_is_zero(self):
        template = NS(cost=125)
        self.handler.item_registry = NS(get=lambda **kw: template)
        self.room.add_item_to_room(NS(id='unrelated', vnum='99'))
        def spawn(prototype):
            return NS(id=str(len(self.room.contents)), vnum=self.vnum, cost=prototype.cost)
        with patch('area.AreaHandler.ItemFactory.create', side_effect=spawn) as create:
            for self.vnum in ('10', '20'):
                self.assertTrue(self.object_reset(self.vnum))
                self.assertFalse(self.object_reset(self.vnum))
            self.assertEqual(create.call_count, 2)
        self.assertEqual(template.cost, 125)
        self.assertEqual([obj.cost for obj in self.room.contents.values() if obj.vnum != '99'], [0, 0])

    def test_nested_matching_item_does_not_suppress_floor_reset(self):
        self.room.add_item_to_room(NS(id='container', vnum='99', contains=[NS(vnum='10')]))
        self.handler.item_registry = NS(get=lambda **kw: NS(cost=100))
        with patch('area.AreaHandler.ItemFactory.create', return_value=NS(id='floor', vnum='10', cost=100)):
            self.assertTrue(self.object_reset('10'))

    def test_innate_effects_have_identity_permanent_duration_and_reversible_modifiers(self):
        for level, bonus in ((17, 1), (18, 2), (24, 2), (25, 3), (31, 3), (32, 4)):
            with self.subTest(level=level):
                mob = self.npc()
                mob.level = level
                original_dex = mob.character_attributes.dexterity
                original_save = mob.saving_throw
                for flag in ('AFF_SANCTUARY', 'AFF_HASTE', 'AFF_PROTECT_EVIL', 'AFF_PROTECT_GOOD'):
                    self.flag(mob, flag)
                MobileFactory._apply_affected_by(mob, self.enums)
                self.assertEqual(mob.character_attributes.dexterity, original_dex + bonus)
                self.assertEqual(mob.saving_throw, original_save - 2)
                self.assertEqual({effect.type for effect in mob.effects},
                                 {'spell.sanctuary', 'spell.haste', 'spell.protection_evil', 'spell.protection_good'})
                for effect in list(mob.effects):
                    self.assertEqual((effect.level, effect.duration), (level, -1))
                    self.effects.affect_strip(mob, effect.type)
                self.assertEqual(mob.effects, [])
                self.assertEqual(mob.character_attributes.dexterity, original_dex)
                self.assertEqual(mob.saving_throw, original_save)
                for flag in ('AFF_SANCTUARY', 'AFF_HASTE', 'AFF_PROTECT_EVIL', 'AFF_PROTECT_GOOD'):
                    self.assertFalse(mob.status_flags.affected_by & self.enums.get('affectedBy')[flag].value)

    def test_spawn_effects_are_independent_of_prototype_and_siblings(self):
        prototype = self.prototype
        prototype.hit_dice = Dice(1, 6, 0)
        prototype.mana_dice = Dice(1, 6, 0)
        prototype.damage_dice = Dice(1, 6, 0)
        prototype.armor_class = ArmorClass(0, 0, 0, 0)
        self.flag(prototype, 'AFF_HASTE')
        first = MobileFactory.create(prototype, self.enums)
        second = MobileFactory.create(prototype, self.enums)
        self.assertEqual(prototype.effects, [])
        self.assertEqual(len(first.effects), 1)
        self.assertEqual(len(second.effects), 1)
        self.assertIsNot(first.effects[0], second.effects[0])
        self.effects.affect_strip(first, 'spell.haste')
        self.assertEqual(len(second.effects), 1)
        clone = MobileFactory.copy_instance(second, self.enums)
        self.assertEqual(clone.character_attributes.dexterity, second.character_attributes.dexterity)
        self.assertEqual(len(clone.effects), 1)
        self.assertIsNot(clone.effects[0], second.effects[0])


if __name__ == '__main__':
    unittest.main()


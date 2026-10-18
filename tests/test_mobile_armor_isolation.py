import unittest
from dataclasses import asdict
from unittest.mock import Mock, patch

from tests.test_update_handler_active_players import Character  # Initialize isolated package imports.
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from mobile.Mobile import Mobile
from util.MobileUtil import MobileUtil


class MobileArmorIsolationTests(unittest.TestCase):
    def setUp(self):
        self.prototype = Mobile.from_json(dict(
            id='prototype', area_id='area', room_id='', name='guard', sex='male',
            level=10, gold=0, silver=0, vnum='100', short_description='a guard',
            long_description='A guard is here.', description='A guard.', race='human',
            flags='', alignment='0', group='', dam_type='slash', size='medium', material='flesh',
            hit_roll=3, hit_dice=Dice(2, 6, 5), mana_dice=Dice(1, 6, 0), damage_dice=Dice(1, 4, 0),
            armor_class=ArmorClass(pierce=70, slash=60, bash=50, exotic=40)))
        self.enums = Mock()
        for name in ('_apply_mob_stat_bonuses', '_apply_affected_by'):
            patcher = patch.object(MobileUtil, name)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_spawn_copies_all_four_values_and_isolates_siblings_and_future_spawns(self):
        expected = asdict(self.prototype.armor_class)
        first = MobileUtil.create_mobile(self.prototype, self.enums)
        second = MobileUtil.create_mobile(self.prototype, self.enums)
        self.assertEqual(asdict(first.armor_class), expected)
        self.assertIsNot(first.armor_class, self.prototype.armor_class)
        self.assertIsNot(first.armor_class, second.armor_class)
        for field in expected:
            setattr(first.armor_class, field, -100)
        self.assertEqual(asdict(second.armor_class), expected)
        self.assertEqual(asdict(self.prototype.armor_class), expected)
        later = MobileUtil.create_mobile(self.prototype, self.enums)
        self.assertEqual(asdict(later.armor_class), expected)

    def test_clone_copies_current_armor_without_sharing_parent_state(self):
        parent = MobileUtil.create_mobile(self.prototype, self.enums)
        parent.armor_class.pierce = -20
        clone = MobileUtil.clone_mobile_instance(parent, self.enums)
        self.assertEqual(asdict(clone.armor_class), asdict(parent.armor_class))
        self.assertIsNot(clone.armor_class, parent.armor_class)
        clone.armor_class.pierce = -50
        parent.armor_class.slash = -30
        self.assertEqual(parent.armor_class.pierce, -20)
        self.assertEqual(clone.armor_class.slash, 60)
        self.assertEqual(self.prototype.armor_class.pierce, 70)

    def test_missing_armor_remains_optional(self):
        self.prototype.armor_class = None
        mobile = MobileUtil.create_mobile(self.prototype, self.enums)
        self.assertIsNone(mobile.armor_class)


if __name__ == '__main__':
    unittest.main()

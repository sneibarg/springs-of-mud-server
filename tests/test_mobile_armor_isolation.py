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

    def test_real_mobile_status_timers_recover_and_clamp(self):
        from combat.CombatHandler import FightHandler
        from game.StatusFlags import StatusFlags
        self.prototype.status_flags = StatusFlags.from_json({})
        mobile = MobileUtil.create_mobile(self.prototype, self.enums)
        mobile.status_flags.pulse_wait = 25
        mobile.status_flags.pulse_daze = 13
        for expected in ((13, 1), (1, 0), (0, 0), (0, 0)):
            FightHandler._decrement_combat_timers(mobile)
            self.assertEqual(expected, (mobile.status_flags.pulse_wait, mobile.status_flags.pulse_daze))
        self.assertFalse(hasattr(mobile, 'pulse_wait'))

    def test_spawn_and_clone_preserve_authored_and_current_alignment(self):
        from api.CharacterApi import CharacterApi
        from api.SpellApi import SpellApi
        for alignment in (900, -900, 0, 349, -349, 350, -350):
            with self.subTest(alignment=alignment):
                self.prototype.alignment = str(alignment)
                mobile = MobileUtil.create_mobile(self.prototype, self.enums)
                self.assertEqual(str(alignment), mobile.alignment)
                self.assertEqual(alignment, mobile.get_alignment())
                self.assertEqual(alignment, mobile.character_attributes.alignment)
                self.assertEqual(alignment >= 350, CharacterApi.is_good(mobile))
                self.assertEqual(alignment <= -350, CharacterApi.is_evil(mobile))
                self.assertEqual(-350 < alignment < 350, CharacterApi.is_neutral(mobile))
                self.assertEqual(alignment, SpellApi._alignment(mobile))
                mobile.set_alignment(-alignment)
                clone = MobileUtil.clone_mobile_instance(mobile, self.enums)
                self.assertEqual(-alignment, clone.get_alignment())
                self.assertEqual(-alignment, SpellApi._alignment(clone))
                clone.set_alignment(123)
                self.assertEqual(-alignment, mobile.get_alignment())
                self.assertEqual(alignment, self.prototype.get_alignment())
                self.assertIsInstance(self.prototype.alignment, str)

    def test_missing_armor_remains_optional(self):
        self.prototype.armor_class = None
        mobile = MobileUtil.create_mobile(self.prototype, self.enums)
        self.assertIsNone(mobile.armor_class)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import Mock

from tests.test_movement_rules_parity import MovementFixture
from combat.CombatHandler import FightHandler
from mobile.MobileFactory import MobileFactory


class AccuracyMobileClassTests(MovementFixture, unittest.TestCase):
    def test_backstab_accuracy_bonus_matches_c_at_proficiency_boundaries(self):
        handler = FightHandler.__new__(FightHandler)
        handler._current_hitroll = Mock(return_value=0)
        for proficiency, reduction in ((0, 1000), (1, 990), (50, 500), (99, 10), (100, 0)):
            handler._skill_percent = Mock(return_value=proficiency)
            normal = handler._thac0(self.actor, 'TYPE_HIT', 100)
            for attack in ('backstab', 'gsn_backstab'):
                with self.subTest(proficiency=proficiency, attack=attack):
                    self.assertEqual(normal - reduction, handler._thac0(self.actor, attack, 100))

    def test_all_mobile_class_flag_combinations_accumulate_stat_bonuses(self):
        bits = self.enums.get('actBits')
        # STR, INT, WIS, DEX, CON deltas from db.c's independent branches.
        modifiers = (
            (bits.ACT_WARRIOR, (3, -1, 0, 0, 2)),
            (bits.ACT_THIEF, (0, 1, -1, 3, 0)),
            (bits.ACT_CLERIC, (1, 0, 3, -1, 0)),
            (bits.ACT_MAGE, (-1, 3, 0, 1, 0)),
        )
        for mask in range(16):
            with self.subTest(mask=mask):
                mob = self.npc()
                mob.level = 10
                mob.size = 'medium'
                mob.status_flags.set_flag('off', 0)
                selected = [entry for index, entry in enumerate(modifiers) if mask & (1 << index)]
                mob.status_flags.set_flag('act', sum(int(flag) for flag, _ in selected))
                MobileFactory._apply_mob_stat_bonuses(mob, self.enums)
                actual = tuple(getattr(mob.character_attributes, name) for name in
                               ('strength', 'intelligence', 'wisdom', 'dexterity', 'constitution'))
                expected = tuple(13 + sum(delta[index] for _, delta in selected) for index in range(5))
                self.assertEqual(expected, actual)

    def test_mobile_thac0_keeps_first_matching_class_priority(self):
        handler = FightHandler.__new__(FightHandler)
        handler.ActBits = self.enums.get('actBits')
        handler._current_hitroll = Mock(return_value=0)
        mob = self.npc()
        mob.level = 32
        bits = handler.ActBits
        mob.status_flags.set_flag('act', bits.ACT_WARRIOR)
        warrior = handler._thac0(mob, 'TYPE_HIT', 100)
        mob.status_flags.set_flag('act', int(bits.ACT_WARRIOR) | int(bits.ACT_CLERIC) | int(bits.ACT_MAGE))
        self.assertEqual(warrior, handler._thac0(mob, 'TYPE_HIT', 100))


if __name__ == '__main__':
    unittest.main()

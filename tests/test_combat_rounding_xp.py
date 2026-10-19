import sys
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_combat_handler_aggression as fixtures

Runtime = sys.modules[fixtures.FightHandler.__module__]


class TestCombatRoundingXp(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.actor, self.victim, self.handler = self.fixtures._killer_pair()

    def test_integer_division_truncates_signed_values_without_float_loss(self):
        for numerator, denominator, expected in ((-1, 5, 0), (-11, 10, -1), (11, -10, -1),
                                                  (-11, -10, 1), (11, 10, 1), (10**30 + 1, 3, 10**30 // 3)):
            self.assertEqual(expected, Runtime.GenericUtil.trunc_div(numerator, denominator))
        with self.assertRaises(ZeroDivisionError):
            Runtime.GenericUtil.trunc_div(1, 0)

    def test_interpolation_and_negative_thac0_compression(self):
        self.assertEqual(20, Runtime.FightUtil.interpolate(1, 20, -4))
        self.actor.level = 40
        self.actor.character_class = SimpleNamespace(thac000=20, thac032=-10)
        self.handler._current_hitroll = Mock(return_value=0)
        # interpolate = -17, then -8, then -6 (each division toward zero).
        self.assertEqual(-6, self.handler._thac0(self.actor, "TYPE_HIT", 100))
        self.actor.level = 0
        self.handler._current_hitroll.return_value = -3
        self.assertEqual(23, self.handler._thac0(self.actor, "TYPE_HIT", 110))
        self.assertEqual(23, self.handler._thac0(self.actor, "TYPE_HIT", 60))

    def test_negative_armor_conversion_and_compression_change_borderline_hit(self):
        self.victim.armor_class = SimpleNamespace(slashing=-161)
        self.victim.character_attributes.dexterity = 10
        with patch.object(Runtime.CharacterApi, "get_attribute_bonus", return_value={"defensive": 0}, create=True):
            self.assertEqual(-16, self.handler._victim_ac_for_damage_type(self.victim, "DAM_SLASH"))
        room = self.fixtures._safety_room(self.actor, self.victim)
        room.id = "room-1"
        self.handler.room_registry.get = Mock(return_value=room)
        self.handler._thac0 = Mock(return_value=0)
        self.handler._victim_ac_for_damage_type = Mock(return_value=-16)
        self.handler._to_hit_roll = Mock(return_value=15)
        self.handler._attack_damage = Mock(return_value=7)
        self.handler.damage = Mock(return_value={})
        with patch.object(Runtime.CharacterApi, "can_see", return_value=True):
            self.handler.one_hit(self.actor, self.victim)
        self.assertEqual(7, self.handler.damage.call_args.args[2])

    def xp_setup(self, level=20, alignment=0):
        self.actor.level = self.victim.level = level
        self.actor.character_attributes.alignment = alignment
        self.actor.get_alignment = lambda: self.actor.character_attributes.alignment
        self.actor.set_alignment = lambda value: setattr(self.actor.character_attributes, "alignment", value)
        self.victim.get_alignment = lambda: alignment
        self.actor.current_time = 10000
        self.actor.status_flags.played = self.actor.status_flags.logon = 0

    def test_negative_alignment_uses_two_separate_truncating_divisions(self):
        self.xp_setup(level=10, alignment=-101)
        with patch.object(Runtime.random, "randint", side_effect=lambda low, high: low):
            self.handler.xp_compute(self.actor, self.victim, 30)
        self.assertEqual(-96, self.actor.get_alignment())

    def test_xp_quarter_hour_boundary_and_time_cap(self):
        for elapsed, expected_bounds in ((53999, (4, 7)), (54000, (7, 12)),
                                          (72000, (9, 16)), (9999999, (30, 51))):
            with self.subTest(elapsed=elapsed):
                self.xp_setup()
                self.actor.status_flags.played = elapsed
                with patch.object(Runtime.random, "randint", side_effect=lambda low, high: low) as roll:
                    self.handler.xp_compute(self.actor, self.victim, 20)
                roll.assert_called_once_with(*expected_bounds)

    def test_xp_combines_saved_time_and_current_session_from_status_flags(self):
        self.xp_setup()
        self.actor.status_flags.played = 50000
        self.actor.status_flags.logon = 6000
        self.actor.played = 9999999  # status_flags is authoritative.
        with patch.object(Runtime.random, "randint", side_effect=lambda low, high: low) as roll:
            self.handler.xp_compute(self.actor, self.victim, 20)
        roll.assert_called_once_with(7, 12)

    def test_zero_or_missing_timing_still_applies_low_level_curve(self):
        for level, bounds in ((1, (71, 118)), (10, (12, 21)), (20, (4, 7))):
            for missing in (False, True):
                with self.subTest(level=level, missing=missing):
                    self.xp_setup(level=level)
                    if missing:
                        del self.actor.status_flags.played
                        del self.actor.status_flags.logon
                    with patch.object(Runtime.random, "randint", side_effect=lambda low, high: low) as roll:
                        self.handler.xp_compute(self.actor, self.victim, level)
                    roll.assert_called_once_with(*bounds)


if __name__ == "__main__":
    unittest.main()

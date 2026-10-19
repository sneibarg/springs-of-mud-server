import sys
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_combat_handler_aggression as fixtures

Runtime = sys.modules[fixtures.FightHandler.__module__]


class TestCombatDamageBonuses(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.attacker, self.victim, self.handler = self.fixtures._killer_pair()

    def test_unarmed_npc_dice_and_fallback_continue_through_position_and_damroll(self):
        for dice in (None, SimpleNamespace(number=2, type=6, bonus=0)):
            for awake, position, expected in ((True, 8, 13), (True, 6, 18), (False, 6, 23)):
                with self.subTest(dice=dice, awake=awake, position=position):
                    npc = self.fixtures._mob("attacker")
                    npc.damage_dice = dice
                    self.victim.character_attributes.position = position
                    self.handler.rng.dice = Mock(return_value=10)
                    self.handler.rng.number_range = Mock(return_value=10)
                    self.handler._current_damroll = Mock(return_value=5)
                    with patch.object(Runtime.CharacterApi, "is_awake", return_value=awake):
                        self.assertEqual(expected, self.handler._attack_damage(npc, self.victim, skill=60))

    def test_damroll_proficiency_cap_negative_truncation_and_minimum(self):
        weapon = SimpleNamespace(value1=1, value2=10, value4=0)
        self.handler.rng.dice = Mock(return_value=10)
        self.handler._skill_percent = Mock(return_value=0)
        for skill, damroll, expected in ((60, 10, 12), (120, 10, 22), (60, -3, 5), (60, -100, 1)):
            with self.subTest(skill=skill, damroll=damroll):
                self.handler._current_damroll = Mock(return_value=damroll)
                with patch.object(Runtime.GameApi, "is_set", return_value=False, create=True):
                    self.assertEqual(expected, self.handler._attack_damage(self.attacker, weapon=weapon, skill=skill))

    def test_player_skill_penalties_order_and_drunk_boundary(self):
        for daze, drunk, expected in ((0, 10, 99), (1, 10, 66), (0, 11, 89), (1, 11, 59)):
            with self.subTest(daze=daze, drunk=drunk):
                self.attacker.status_flags.pulse_daze = daze
                self.attacker.status_flags.drunk = drunk
                with patch.object(Runtime.Character, "get_learned", return_value=99), \
                        patch.object(Runtime.Character, "learned_entry_level", side_effect=lambda value: value):
                    self.assertEqual(expected, self.handler._skill_percent(self.attacker, "second attack"))
                    self.assertEqual(expected, self.handler._defense_skill_percent(self.attacker, "parry"))

    def test_npc_skill_penalties_precede_cap_and_ignore_drunk(self):
        npc = self.fixtures._mob("attacker")
        npc.level = 50
        npc.status_flags.pulse_daze = 1
        npc.status_flags.drunk = 100
        self.handler.ActBits = SimpleNamespace(ACT_WARRIOR=SimpleNamespace(name="ACT_WARRIOR"),
                                               ACT_THIEF=SimpleNamespace(name="ACT_THIEF"))
        self.handler._mob_has_act = Mock(return_value=True)
        self.handler._mob_has_off = Mock(return_value=True)
        self.handler.OffenseTypes = SimpleNamespace(OFF_PARRY=SimpleNamespace(name="OFF_PARRY"),
                                                   OFF_DODGE=SimpleNamespace(name="OFF_DODGE"))
        self.assertEqual(100, self.handler._skill_percent(npc, "second attack"))
        self.assertEqual(100, self.handler._skill_percent(npc, "third attack"))
        self.assertEqual(66, self.handler._defense_skill_percent(npc, "parry"))
        self.assertEqual(66, self.handler._defense_skill_percent(npc, "dodge"))
        self.assertEqual(73, self.handler._defense_skill_percent(npc, "shield block"))
        self.assertEqual(0, self.handler._skill_percent(npc, "enhanced damage"))

    def test_weapon_proficiency_retains_separate_unpenalized_lookup(self):
        self.attacker.status_flags.pulse_daze = 1
        self.attacker.status_flags.drunk = 20
        self.handler._weapon_skill_name = Mock(return_value="sword")
        with patch.object(Runtime.Character, "get_learned", return_value=99), \
                patch.object(Runtime.Character, "learned_entry_level", side_effect=lambda value: value):
            self.assertEqual(59, self.handler._skill_percent(self.attacker, "sword"))
            self.assertEqual(119, self.handler._weapon_skill_total(self.attacker, object()))


if __name__ == "__main__":
    unittest.main()

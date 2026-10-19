import sys
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_combat_handler_aggression as fixtures

Runtime = sys.modules[fixtures.FightHandler.__module__]


class TestCombatDefenses(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.attacker, self.victim, self.handler = self.fixtures._killer_pair()
        self.attacker.level = self.victim.level = 30
        self.victim.equipped = SimpleNamespace(wielded=object())
        self.room = object()
        self.handler._find_room_for_entity = Mock(return_value=self.room)
        self.handler._defense_skill_percent = Mock(return_value=100)

    def test_defense_probability_has_strict_endpoint_and_no_dexterity_bonus(self):
        for defense in (self.handler.check_parry, self.handler.check_dodge):
            for dex in (1, 100):
                self.victim.character_attributes.dexterity = dex
                for roll, expected in ((49, True), (50, False)):
                    with self.subTest(defense=defense.__name__, dex=dex, roll=roll), \
                            patch.object(Runtime.CharacterApi, "can_see", return_value=True), \
                            patch.object(Runtime.random, "randint", return_value=roll):
                        self.assertEqual(expected, defense(self.attacker, self.victim))

    def test_visibility_direction_and_level_bonus_after_halving(self):
        self.victim.level += 7
        for defense, observer, target in ((self.handler.check_parry, self.attacker, self.victim),
                                          (self.handler.check_dodge, self.victim, self.attacker)):
            for roll, expected in ((31, True), (32, False)):
                with self.subTest(defense=defense.__name__, roll=roll), \
                        patch.object(Runtime.CharacterApi, "can_see", return_value=False) as sight, \
                        patch.object(Runtime.random, "randint", return_value=roll):
                    self.assertEqual(expected, defense(self.attacker, self.victim))
                    sight.assert_called_once_with(observer, target, self.room)

    def test_unarmed_players_cannot_parry_but_npcs_have_quarter_skill(self):
        self.victim.equipped = None
        with patch.object(Runtime.random, "randint") as rng:
            self.assertFalse(self.handler.check_parry(self.attacker, self.victim))
            rng.assert_not_called()
        npc = self.fixtures._mob("defender")
        npc.level = self.attacker.level
        for roll, expected in ((24, True), (25, False)):
            with patch.object(Runtime.CharacterApi, "can_see", return_value=True), \
                    patch.object(Runtime.random, "randint", return_value=roll):
                self.assertEqual(expected, self.handler.check_parry(self.attacker, npc))

    def test_integer_halving_and_uncapped_level_adjustment(self):
        for skill, difference, visible, roll, expected in (
                (99, 0, False, 23, True), (99, 0, False, 24, False),
                (100, 51, True, 100, True), (100, -50, True, 1, False)):
            with self.subTest(skill=skill, difference=difference, roll=roll):
                self.handler._defense_skill_percent.return_value = skill
                self.victim.level = self.attacker.level + difference
                with patch.object(Runtime.CharacterApi, "can_see", return_value=visible), \
                        patch.object(Runtime.random, "randint", return_value=roll):
                    self.assertEqual(expected, self.handler.check_dodge(self.attacker, self.victim))

    def test_asleep_defender_does_not_roll_and_zero_skill_still_gets_level_bonus(self):
        with patch.object(Runtime.CharacterApi, "is_awake", return_value=False), \
                patch.object(Runtime.random, "randint") as rng:
            self.assertFalse(self.handler.check_parry(self.attacker, self.victim))
            self.assertFalse(self.handler.check_dodge(self.attacker, self.victim))
            rng.assert_not_called()
        self.handler._defense_skill_percent.return_value = 0
        self.victim.level += 5
        with patch.object(Runtime.CharacterApi, "can_see", return_value=True), \
                patch.object(Runtime.random, "randint", return_value=4):
            self.assertTrue(self.handler.check_dodge(self.attacker, self.victim))

    def test_backstab_bypasses_all_defenses_but_ordinary_hit_is_parried(self):
        for dt in ("backstab", "gsn_backstab", "TYPE_HIT"):
            with self.subTest(dt=dt):
                attacker, victim, handler = self.fixtures._killer_pair()
                room = self.fixtures._safety_room(attacker, victim)
                room.id = "room-1"
                handler.room_registry.get = Mock(return_value=room)
                handler.is_safe = Mock(return_value=(False, ""))
                handler.check_killer = Mock(return_value={})
                handler._check_immunity = Mock(return_value="IS_NORMAL")
                handler.dam_message = Mock(return_value={"to_char": "hit", "to_victim": "hit", "to_room": "hit"})
                handler._thac0 = Mock(return_value=0)
                handler._victim_ac_for_damage_type = Mock(return_value=0)
                handler._to_hit_roll = Mock(return_value=19)
                handler._attack_damage = Mock(return_value=10)
                handler.AffectBits = SimpleNamespace(AFF_SANCTUARY=4, AFF_PROTECT_EVIL=8, AFF_PROTECT_GOOD=16)
                handler.check_parry = Mock(return_value=True)
                handler.check_dodge = Mock(return_value=True)
                handler.check_shield_block = Mock(return_value=True)
                attacker.fighting, victim.fighting = victim, attacker
                victim.hit, victim.status_flags.drunk = 100, 0
                with patch.object(Runtime.CharacterApi, "is_affected", return_value=False):
                    handler.one_hit(attacker, victim, dt=dt)
                self.assertEqual(100 if dt == "TYPE_HIT" else 90, victim.hit)
                self.assertEqual(dt == "TYPE_HIT", handler.check_parry.called)
                handler.check_dodge.assert_not_called()
                handler.check_shield_block.assert_not_called()


if __name__ == "__main__":
    unittest.main()

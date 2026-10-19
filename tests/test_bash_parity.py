import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests.test_combat_survival import Components

Module = Components["interp.commands.Fight"]


class TestBashParity(unittest.TestCase):
    def setUp(self):
        self.commands = Module.Fight.__new__(Module.Fight)
        self.actor = self.entity()
        self.victim = self.entity()
        self.skill = SimpleNamespace(name="bash", beats=13)
        self.room = SimpleNamespace(contents={}, characters={})
        self.context = SimpleNamespace(finish=Mock())
        self.commands.game_parameters = SimpleNamespace(PULSE_VIOLENCE=SimpleNamespace(value=10))
        self.commands.AffectBits = object()
        self.commands.skill_registry = SimpleNamespace(get=Mock(return_value=SimpleNamespace(name="dodge")))
        self.commands.skill_api = SimpleNamespace(get_rating=Mock(side_effect=lambda actor, skill: 80 if skill.name == "bash" else 0))
        self.commands.fight_api = SimpleNamespace(build_fight_view=Mock(return_value=SimpleNamespace(
            skill=self.skill, room=self.room, victim=self.victim)), evaluate_guards_only_view=Mock(return_value=None))
        self.commands.fight_handler = SimpleNamespace(_mob_has_off=Mock(return_value=False),
            damage=Mock(return_value={}), build_round_payload=Mock(return_value={"to_char": "round"}))
        for name, options in (("is_npc", {"side_effect": lambda entity: entity.is_npc}),
                              ("is_awake", {"return_value": True}),
                              ("get_attribute_bonus", {"return_value": {"defensive": 0}}),
                              ("is_affected_by_name", {"return_value": False}),
                              ("set_position", {"side_effect": lambda entity, name: setattr(entity.character_attributes, "position", name)})):
            patcher = patch.object(Module.CharacterApi, name, create=True, **options)
            patcher.start()
            self.addCleanup(patcher.stop)

    @staticmethod
    def entity():
        return SimpleNamespace(is_npc=False, level=20, size=2, carry_weight=lambda: 0,
            armor_class=SimpleNamespace(bashing=0), status_flags=SimpleNamespace(pulse_wait=0, pulse_daze=0),
            character_attributes=SimpleNamespace(strength=18, dexterity=15, position="POS_FIGHTING"))

    def test_formula_weight_size_armor_and_level(self):
        self.actor.carry_weight = lambda: 750
        self.victim.carry_weight = lambda: 400
        self.actor.size, self.victim.size = 4, 2
        self.actor.level = 23
        self.victim.armor_class.bashing = -49
        # 80 + 3 - 2 + 20 + 18 - 20 - (-1) + 3 = 103.
        self.assertEqual(103, self.commands._bash_chance(self.actor, self.victim, self.skill))
        self.actor.size = 1
        self.assertEqual(68, self.commands._bash_chance(self.actor, self.victim, self.skill))

    def test_speed_flags_and_haste_do_not_stack_and_slow_has_no_direct_term(self):
        self.commands.fight_handler._mob_has_off.return_value = True
        with patch.object(Module.CharacterApi, "is_affected_by_name", return_value=True):
            self.assertEqual(58, self.commands._bash_chance(self.actor, self.victim, self.skill))

    def test_player_dodge_correction_is_uncapped_and_not_applied_to_npcs(self):
        self.commands.skill_api.get_rating.side_effect = lambda actor, skill: 80 if skill.name == "bash" else 90
        self.assertEqual(42, self.commands._bash_chance(self.actor, self.victim, self.skill))
        self.victim.is_npc = True
        self.assertEqual(78, self.commands._bash_chance(self.actor, self.victim, self.skill))

    def test_success_damage_range_daze_wait_and_hidden_normal_damage(self):
        self.commands._check_improve = Mock()
        with patch.object(Module.random, "randint", side_effect=[77, 9]) as roll:
            payload = self.commands.do_bash(self.actor, self.context)
        self.assertEqual([(1, 100), (2, 9)], [c.args for c in roll.call_args_list])
        self.assertEqual(30, self.victim.status_flags.pulse_daze)
        self.assertEqual(13, self.actor.status_flags.pulse_wait)
        self.assertEqual("POS_RESTING", self.victim.character_attributes.position)
        self.commands.fight_handler.damage.assert_called_once_with(self.actor, self.victim, 9,
            dt="bash", dam_type="DAM_BASH", show=False)
        self.commands._check_improve.assert_called_once_with(self.actor, self.skill, True, 1)
        self.assertEqual("success", payload["payloads"][0]["message_key"])

    def test_failure_at_exact_chance_rests_attacker_and_uses_one_and_half_beats(self):
        self.commands._check_improve = Mock()
        with patch.object(Module.random, "randint", return_value=78):
            payload = self.commands.do_bash(self.actor, self.context)
        self.assertEqual("POS_RESTING", self.actor.character_attributes.position)
        self.assertEqual(19, self.actor.status_flags.pulse_wait)
        self.commands.fight_handler.damage.assert_called_once_with(self.actor, self.victim, 0,
            dt="bash", dam_type="DAM_BASH", show=False)
        self.commands._check_improve.assert_called_once_with(self.actor, self.skill, False, 1)
        keys = [p.get("message_key") for p in payload["payloads"][1:]]
        self.assertEqual(["fallFlatFace", "fallsFlatFace", "evadeSBashCausing"], keys)
        documents = json.loads((Path(__file__).resolve().parents[1] / "resources/collections/SOMDB.Commands.json").read_text())
        command = next(d for d in documents if d["name"] == "bash")
        for channel, key in zip(("toChar", "toRoom", "toVictim"), keys):
            self.assertTrue(command["payload"][channel][key])

    def test_guard_failure_has_no_wait_roll_or_damage(self):
        self.commands.fight_api.evaluate_guards_only_view.return_value = {"blocked": True}
        with patch.object(Module.random, "randint") as roll:
            self.assertEqual({"blocked": True}, self.commands.do_bash(self.actor, self.context))
            roll.assert_not_called()
        self.commands.fight_handler.damage.assert_not_called()
        self.assertEqual(0, self.actor.status_flags.pulse_wait)


if __name__ == "__main__":
    unittest.main()

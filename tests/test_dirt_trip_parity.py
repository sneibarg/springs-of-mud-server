import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_bash_parity as bash

Module = bash.Module


class TestDirtTripParity(unittest.TestCase):
    def setUp(self):
        fixture = bash.TestBashParity()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.commands, self.actor, self.victim = fixture.commands, fixture.actor, fixture.victim
        self.room, self.context, self.skill = fixture.room, fixture.context, fixture.skill
        self.commands._check_improve = Mock()
        self.commands.skill_api.get_rating.return_value = 80
        self.commands.skill_api.get_rating.side_effect = None
        self.commands._dirt_terrain_adjustment = Mock(return_value=0)
        self.commands.fight_api.build_fight_view.return_value.extra = {}

    def test_dirt_and_trip_dexterity_size_and_speed_formulas(self):
        self.actor.character_attributes.dexterity = 17
        self.victim.character_attributes.dexterity = 15
        self.actor.level = 22
        self.assertEqual(71, self.commands._dexterity_attack_chance(self.actor, self.victim, self.skill, dirt=True))
        self.assertEqual(79, self.commands._dexterity_attack_chance(self.actor, self.victim, self.skill, dirt=False))
        self.actor.size = 1
        self.assertEqual(69, self.commands._dexterity_attack_chance(self.actor, self.victim, self.skill, dirt=False))
        self.actor.size = 4
        self.assertEqual(79, self.commands._dexterity_attack_chance(self.actor, self.victim, self.skill, dirt=False))
        self.commands.fight_handler._mob_has_off.return_value = True
        with patch.object(Module.CharacterApi, "is_affected_by_name", return_value=True):
            self.assertEqual(56, self.commands._dexterity_attack_chance(self.actor, self.victim, self.skill, dirt=True))
            self.assertEqual(69, self.commands._dexterity_attack_chance(self.actor, self.victim, self.skill, dirt=False))

    def test_dirt_adjusts_multiples_of_five_before_terrain_and_uses_strict_roll(self):
        self.commands._dexterity_attack_chance = Mock(return_value=60)
        self.commands._dirt_terrain_adjustment.return_value = -20
        with patch.object(Module.random, "randint", return_value=41):
            self.commands.do_dirt(self.actor, self.context)
        self.commands.fight_handler.damage.assert_called_once_with(self.actor, self.victim, 0,
            dt="dirt", dam_type="DAM_NONE", show=True)
        self.assertEqual(13, self.actor.status_flags.pulse_wait)

    def test_dirt_final_zero_chance_rejects_without_wait_or_damage(self):
        self.commands._dexterity_attack_chance = Mock(return_value=19)
        self.commands._dirt_terrain_adjustment.return_value = -19
        with patch.object(Module.random, "randint") as roll:
            result = self.commands.do_dirt(self.actor, self.context)
            roll.assert_not_called()
        self.assertEqual("noTerrain", result["message_key"])
        self.commands.fight_handler.damage.assert_not_called()
        self.assertEqual(0, self.actor.status_flags.pulse_wait)

    def test_dirt_damage_precedes_effect_even_on_lethal_result(self):
        for killed in (False, True):
            with self.subTest(killed=killed):
                order = []
                self.commands.fight_handler.damage.side_effect = lambda *args, **kw: order.append("damage") or {"killed": killed}
                self.commands.effect_handler = SimpleNamespace(affect_to_char=Mock(side_effect=lambda *args: order.append("effect")))
                self.commands._check_improve.side_effect = lambda *args: order.append("improve")
                with patch.object(Module, "Effect", side_effect=lambda **kw: SimpleNamespace(**kw)), \
                        patch.object(Module.random, "randint", side_effect=[1, 4]):
                    result = self.commands.do_dirt(self.actor, self.context)
                self.assertEqual(["damage", "improve", "effect"], order)
                self.commands.fight_handler.damage.assert_called_with(self.actor, self.victim, 4,
                    dt="dirt", dam_type="DAM_NONE", show=False)
                effect = self.commands.effect_handler.affect_to_char.call_args.args[1]
                self.assertEqual(("skill.dirt", 0, -4, "AFF_BLIND"),
                                 (effect.type, effect.duration, effect.modifier, effect.bitvector))
                payloads = result["payloads"]
                self.assertEqual("kicksDirtEyes", payloads[2]["message_key"])
                self.assertEqual({"to_char": "round"}, payloads[3])
                self.assertEqual("blinded", payloads[4]["message_key"])

    def test_trip_success_damage_type_range_and_loaded_daze(self):
        self.victim.size = 0
        with patch.object(Module.random, "randint", side_effect=[1, 2]) as roll:
            self.commands.do_trip(self.actor, self.context)
        self.assertEqual((2, 2), roll.call_args.args)
        self.assertEqual(20, self.victim.status_flags.pulse_daze)
        self.assertEqual(13, self.actor.status_flags.pulse_wait)
        self.commands.fight_handler.damage.assert_called_once_with(self.actor, self.victim, 2,
            dt="trip", dam_type="DAM_BASH", show=True)

    def test_trip_failed_roll_uses_two_thirds_beats_without_resting_target(self):
        self.commands._dexterity_attack_chance = Mock(return_value=50)
        with patch.object(Module.random, "randint", return_value=50):
            self.commands.do_trip(self.actor, self.context)
        self.assertEqual(8, self.actor.status_flags.pulse_wait)
        self.assertEqual("POS_FIGHTING", self.victim.character_attributes.position)
        self.commands.fight_handler.damage.assert_called_once_with(self.actor, self.victim, 0,
            dt="trip", dam_type="DAM_BASH", show=True)

    def test_dirt_payload_separates_post_damage_blindness_message(self):
        documents = json.loads((Path(__file__).resolve().parents[1] / "resources/collections/SOMDB.Commands.json").read_text())
        command = next(d for d in documents if d["name"] == "dirt")
        self.assertEqual("You can't see a thing!", command["payload"]["toVictim"]["blinded"])
        self.assertIn("kicks dirt", command["payload"]["toVictim"]["kicksDirtEyes"])


if __name__ == "__main__":
    unittest.main()

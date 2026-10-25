import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock

from tests.test_update_handler_active_players import Character, build_character_data
from api.CharacterApi import CharacterApi
from skill.Ability import Ability
from skill.LearningService import LearningService


class TestLearningParity(unittest.TestCase):
    def learning_case(self, learned=75, collection="skills", rating=2, required=1):
        character = Character.from_json(build_character_data())
        character.level = 20
        character.character_class.skill_adept = 75
        character.skills, character.spells = [], []
        if learned is not None:
            setattr(character, collection, [{"name": "sword", "level": learned}])
        class_name = character.character_class.name.lower()
        definition = Ability(
            id="sword", name="sword", kind="skill", handler_id="", target="",
            min_position="", noun_damage="", slot=0, min_mana=0, beats=0,
            rating_by_class={class_name: rating}, level_by_class={class_name: required},
        )
        resolver = NS(by_id=lambda _: (definition, collection))
        rules = NS(is_npc=lambda _: False, skill_value_for_class=CharacterApi.skill_value_for_class,
                   get_attribute_bonus=Mock(return_value={"learn": 18}))
        percent, random, advance = Mock(), Mock(), Mock()
        percent.number_percent.return_value = 1
        random.randint.side_effect = lambda low, high: 3 if high == 3 else 1
        learning = LearningService(resolver, rules, percent, random, advance, Mock())
        return character, learning, percent, random, advance

    def test_improvement_can_pass_practice_adept_and_caps_at_100(self):
        for collection in ("skills", "spells"):
            for success in (True, False):
                for learned in (75, 90, 99):
                    with self.subTest(collection=collection, success=success, learned=learned):
                        ch, learning, percent, random, advance = self.learning_case(learned, collection)
                        learning.check_improve(ch, "sword", success)
                        self.assertEqual(min(100, learned + (1 if success else 3)),
                                         ch.get_learned("sword", collection_name=collection)["level"])
                        advance.assert_called_once_with(ch, 4)
                        self.assertIn("sword", ch.take_improve_messages())
                        self.assertEqual(75, learning.practice_adept(ch))

    def test_success_probability_uses_100_instead_of_practice_adept(self):
        ch, learning, percent, _, _ = self.learning_case(75)
        percent.number_percent.return_value = 20  # Below 100-75, above the old minimum of 5.
        learning.check_improve(ch, "sword", True)
        self.assertEqual(76, ch.get_learned("sword")["level"])

    def test_ineligible_abilities_skip_random_messages_and_experience(self):
        for collection in ("skills", "spells"):
            for success in (True, False):
                for options in ({"required": 21}, {"rating": 0}, {"learned": 0},
                                {"learned": None}, {"learned": 100}):
                    with self.subTest(collection=collection, success=success, options=options):
                        ch, learning, percent, random, advance = self.learning_case(collection=collection, **options)
                        before = [dict(entry) for entry in getattr(ch, collection)]
                        learning.check_improve(ch, "sword", success)
                        self.assertEqual(before, getattr(ch, collection))
                        percent.number_percent.assert_not_called()
                        random.randint.assert_not_called()
                        learning.rules.get_attribute_bonus.assert_not_called()
                        advance.assert_not_called()
                        self.assertEqual("", ch.take_improve_messages())

    def test_required_level_is_inclusive(self):
        ch, learning, _, _, advance = self.learning_case(required=20)
        learning.check_improve(ch, "sword", True)
        self.assertEqual(76, ch.get_learned("sword")["level"])
        advance.assert_called_once_with(ch, 4)


if __name__ == "__main__":
    unittest.main()

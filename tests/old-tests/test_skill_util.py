import unittest

from types import SimpleNamespace
from unittest.mock import Mock, patch

from player.CharacterClass import CharacterClass
from util.SkillUtil import SkillUtil


class TestSkillUtil(unittest.TestCase):
    def _character_class(self, name: str, skill_adept: int = 75) -> CharacterClass:
        return CharacterClass(
            name=name,
            attr_prime=0,
            weapon=0,
            guild=0,
            skill_adept=skill_adept,
            thac000=0,
            thac032=0,
            hp_min=0,
            hp_max=0,
            mana_gain=False,
            base_group="",
            default_group="",
        )

    def test_check_improve_updates_skill_entry(self):
        character = SimpleNamespace(
            level=20,
            character_class=self._character_class("warrior", skill_adept=75),
            character_attributes=SimpleNamespace(intelligence=18),
            skills=[{"name": "sword", "level": 40}],
            spells=[],
        )
        ability = SimpleNamespace(
            name="sword",
            level_by_class={"warrior": 1},
            rating_by_class={"warrior": 2},
        )
        registry = SimpleNamespace(
            skill_registry=SimpleNamespace(get_or_none=Mock(return_value=ability)),
            spell_registry=SimpleNamespace(get_or_none=Mock(return_value=None)),
        )

        with patch("util.SkillUtil.CharacterMacros.is_npc", return_value=False), \
                patch("util.SkillUtil.CharacterMacros.get_registry", return_value=registry), \
                patch("util.SkillUtil.CharacterMacros.get_attribute_bonus", return_value={"learn": 18}), \
                patch("util.SkillUtil.random.randint", side_effect=[1, 1]), \
                patch("util.SkillUtil.CharacterAdvancement.gain_experience") as gain_experience:
            SkillUtil.check_improve(character, "skill-id", True)

        self.assertEqual(41, character.skills[0]["level"])
        gain_experience.assert_called_once_with(character, 4)

    def test_check_improve_uses_spell_registry_and_caps_at_adept(self):
        character = SimpleNamespace(
            level=30,
            character_class=self._character_class("mage", skill_adept=52),
            character_attributes=SimpleNamespace(intelligence=20),
            skills=[],
            spells=[{"name": "magic missile", "level": 51}],
        )
        spell = SimpleNamespace(
            name="magic missile",
            level_by_class={"mage": 1},
            rating_by_class={"mage": 4},
        )
        registry = SimpleNamespace(
            skill_registry=SimpleNamespace(get_or_none=Mock(return_value=None)),
            spell_registry=SimpleNamespace(get_or_none=Mock(return_value=spell)),
        )

        with patch("util.SkillUtil.CharacterMacros.is_npc", return_value=False), \
                patch("util.SkillUtil.CharacterMacros.get_registry", return_value=registry), \
                patch("util.SkillUtil.CharacterMacros.get_attribute_bonus", return_value={"learn": 20}), \
                patch("util.SkillUtil.random.randint", side_effect=[1, 1, 3]), \
                patch("util.SkillUtil.CharacterAdvancement.gain_experience") as gain_experience:
            SkillUtil.check_improve(character, "spell-id", False)

        self.assertEqual(52, character.spells[0]["level"])
        gain_experience.assert_called_once_with(character, 8)


if __name__ == "__main__":
    unittest.main()

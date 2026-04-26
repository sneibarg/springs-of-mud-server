import unittest
from types import SimpleNamespace

from player.CharacterMacros import CharacterMacros


class TestCharacterMacrosTrain(unittest.TestCase):
    def tearDown(self):
        CharacterMacros.reset_for_tests()

    def test_get_max_train_uses_configured_pc_races(self):
        CharacterMacros.configure(
            registry_provider=lambda: None,
            enums_provider=lambda: {},
            attribute_bonuses_provider=lambda: {},
            pc_races_provider=lambda: {
                "human": {"max_stats": [18, 18, 18, 18, 18]},
                "elf": {"max_stats": [16, 20, 18, 21, 15]},
            },
        )
        character = SimpleNamespace(race="human")

        self.assertEqual(18, CharacterMacros.get_max_train(character, 0, 17))
        self.assertEqual(18, CharacterMacros.get_max_train(character, 4, 13))

    def test_get_max_train_falls_back_when_race_missing(self):
        CharacterMacros.configure(
            registry_provider=lambda: None,
            enums_provider=lambda: {},
            attribute_bonuses_provider=lambda: {},
            pc_races_provider=lambda: {"human": {"max_stats": [18, 18, 18, 18, 18]}},
        )
        character = SimpleNamespace(race="unknown")

        self.assertEqual(14, CharacterMacros.get_max_train(character, 0, 14))

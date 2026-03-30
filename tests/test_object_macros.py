import unittest

from enum import IntEnum
from unittest.mock import MagicMock
from game.GameData import GameData
from object.Item import Item
from object.ObjectMacros import ObjectMacros


class TestBodyForm(IntEnum):
    FORM_EDIBLE = 1
    FORM_POISON = 2
    FORM_MAGICAL = 4
    FORM_INSTANT_DECAY = 8
    FORM_OTHER = 16
    FORM_ANIMAL = 64
    FORM_SENTIENT = 128
    FORM_UNDEAD = 256
    FORM_CONSTRUCT = 512
    FORM_MIST = 1024
    FORM_INTANGIBLE = 2048
    FORM_BIPED = 4096
    FORM_CENTAUR = 8192
    FORM_INSECT = 16384
    FORM_SPIDER = 32768
    FORM_CRUSTACEAN = 65536
    FORM_WORM = 131072
    FORM_BLOB = 262144
    FORM_MAMMAL = 2097152
    FORM_BIRD = 4194304
    FORM_REPTILE = 8388608
    FORM_SNAKE = 16777216
    FORM_DRAGON = 33554432
    FORM_AMPHIBIAN = 67108864
    FORM_FISH = 134217728
    FORM_COLD_BLOOD = 268435456


class TestBodyParts(IntEnum):
    PART_HEAD = 1
    PART_ARMS = 2
    PART_LEGS = 4
    PART_HEART = 8
    PART_BRAINS = 16
    PART_GUTS = 32
    PART_HANDS = 64
    PART_FEET = 128
    PART_FINGERS = 256
    PART_EAR = 512
    PART_EYE = 1024
    PART_LONG_TONGUE = 2048
    PART_EYESTALKS = 4096
    PART_TENTACLES = 8192
    PART_FINS = 16384
    PART_WINGS = 32768
    PART_TAIL = 65536
    PART_CLAWS = 1048576
    PART_FANGS = 2097152
    PART_HORNS = 4194304
    PART_SCALES = 8388608
    PART_TUSKS = 16777216


class TestObjectMacros(unittest.TestCase):

    def setUp(self):
        self.mock_game_data = MagicMock(spec=GameData)
        self.mock_game_data.races = {
            "human": {
                "form": 2101377,  # A|H|M|V → EDIBLE + SENTIENT + BIPED + MAMMAL
                "parts": 2047  # All basic humanoid parts
            },
            "dragon": {
                "form": 33554561,  # EDIBLE + SENTIENT + DRAGON
                "parts": 11634685
            },
            "bat": {
                "form": 2097217,
                "parts": 34493
            },
            "empty_race": {},
        }

        self.macros = ObjectMacros(self.mock_game_data)

    def test_decode_form_and_parts_human(self):
        result = self.macros.decode_form_and_parts("human", TestBodyForm, TestBodyParts)

        expected_form = {"FORM_EDIBLE", "FORM_SENTIENT", "FORM_BIPED", "FORM_MAMMAL"}
        self.assertEqual(set(result["form"]), expected_form)
        self.assertGreater(len(result["parts"]), 8)

    def test_decode_form_and_parts_dragon(self):
        result = self.macros.decode_form_and_parts("dragon", TestBodyForm, TestBodyParts)

        expected_form = {"FORM_EDIBLE", "FORM_SENTIENT", "FORM_DRAGON"}
        self.assertEqual(set(result["form"]), expected_form)

        dragon_parts = set(result["parts"])
        self.assertIn("PART_WINGS", dragon_parts)
        self.assertIn("PART_TAIL", dragon_parts)
        self.assertIn("PART_SCALES", dragon_parts)

    def test_decode_form_and_parts_nonexistent_race(self):
        result = self.macros.decode_form_and_parts("nonexistent_race", TestBodyForm, TestBodyParts)
        self.assertEqual(result["form"], [])
        self.assertEqual(result["parts"], [])

    def test_decode_form_and_parts_empty_race(self):
        result = self.macros.decode_form_and_parts("empty_race", TestBodyForm, TestBodyParts)
        self.assertEqual(result["form"], [])
        self.assertEqual(result["parts"], [])

    def test_decode_form_and_parts_zero_values(self):
        self.mock_game_data.races["zero"] = {"form": 0, "parts": 0}
        result = self.macros.decode_form_and_parts("zero", TestBodyForm, TestBodyParts)
        self.assertEqual(result["form"], [])
        self.assertEqual(result["parts"], [])

    def test_can_wear_returns_false_by_default(self):
        obj = MagicMock(spec=Item)
        result = self.macros.can_wear(obj, 1)
        self.assertIsNone(result)

    def test_is_obj_stat_returns_false_by_default(self):
        obj = MagicMock(spec=Item)
        result = self.macros.is_obj_stat(obj, 1)
        self.assertIsNone(result)

    def test_is_weapon_stat_returns_false_by_default(self):
        obj = MagicMock(spec=Item)
        result = self.macros.is_weapon_stat(obj, 1)
        self.assertIsNone(result)

    def test_weight_multiplier_returns_none_by_default(self):
        obj = MagicMock(spec=Item)
        result = self.macros.weight_multiplier(obj)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

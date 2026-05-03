import unittest

from enum import IntEnum
from unittest.mock import MagicMock
from game.GameData import GameData
from object.Item import Item
from object.ObjectMacros import ObjectMacros


class TestItemTypes(IntEnum):
    ITEM_LIGHT = 1
    ITEM_SCROLL = 2
    ITEM_WAND = 3
    ITEM_STAFF = 4
    ITEM_WEAPON = 5
    ITEM_TREASURE = 8
    ITEM_ARMOR = 9
    ITEM_POTION = 10
    ITEM_CLOTHING = 11
    ITEM_FURNITURE = 12
    ITEM_TRASH = 13
    ITEM_CONTAINER = 15
    ITEM_DRINK_CON = 17
    ITEM_KEY = 18
    ITEM_FOOD = 19
    ITEM_MONEY = 20
    ITEM_BOAT = 22
    ITEM_CORPSE_NPC = 23
    ITEM_CORPSE_PC = 24
    ITEM_FOUNTAIN = 25
    ITEM_PILL = 26
    ITEM_PROTECT = 27
    ITEM_MAP = 28
    ITEM_PORTAL = 29
    ITEM_WARP_STONE = 30
    ITEM_ROOM_KEY = 31
    ITEM_GEM = 32
    ITEM_JEWELRY = 33
    ITEM_JUKEBOX = 3


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
        self.mock_item_table = MagicMock(spec=dict)
        self.mock_item_types = TestItemTypes
        self.races = {
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

        self.macros = ObjectMacros(self.races, self.mock_item_table, self.mock_item_types)

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
        self.races["zero"] = {"form": 0, "parts": 0}
        result = self.macros.decode_form_and_parts("zero", TestBodyForm, TestBodyParts)
        self.assertEqual(result["form"], [])
        self.assertEqual(result["parts"], [])

    def test_can_wear_returns_false_by_default(self):
        obj = MagicMock(spec=Item)
        obj.wear_flags = "0"
        result = self.macros.can_wear(obj, 1)
        self.assertFalse(result)

    def test_is_obj_stat_returns_false_by_default(self):
        obj = MagicMock(spec=Item)
        obj.extra_flags = "0"
        result = self.macros.is_obj_stat(obj, 1)
        self.assertFalse(result)

    def test_is_weapon_stat_returns_false_by_default(self):
        obj = MagicMock(spec=Item)
        obj.value4 = "0"
        result = self.macros.is_weapon_stat(obj, 1)
        self.assertFalse(result)

    def test_weight_multiplier_returns_none_by_default(self):
        obj = MagicMock(spec=Item)
        obj.item_type = "weapon"
        obj.value3 = "100"
        result = self.macros.weight_multiplier(obj)
        self.assertEqual(result, 100)

    def test_can_wear_emerald_sword_take(self):
        obj = Item(
            id="test_id",
            area_id="test_area",
            vnum="2222",
            name="sword emerald",
            short_description="an emerald sword",
            long_description="An emerald long sword is leaning against the wall.",
            material="oldstyle",
            item_type="weapon",
            extra_flags="0",
            wear_flags="8193",  # AN = (1<<0) | (1<<13) = 1 | 8192 = 8193
            value0="sword",
            value1="4",
            value2="6",
            value3="slash",
            value4="8",  # D = 1<<3 = 8
            weight="240",
            condition="100",
            level=28,
            cost=2300,
            affect_data=[],
            extra_descr=[]
        )

        result = self.macros.can_wear(obj, 1)
        self.assertTrue(result, "Emerald sword should have ITEM_TAKE flag")

    def test_can_wear_emerald_sword_wield(self):
        obj = Item(
            id="test_id",
            area_id="test_area",
            vnum="2222",
            name="sword emerald",
            short_description="an emerald sword",
            long_description="An emerald long sword is leaning against the wall.",
            material="oldstyle",
            item_type="weapon",
            extra_flags="0",
            wear_flags="8193",  # AN = 1 | 8192
            value0="sword",
            value1="4",
            value2="6",
            value3="slash",
            value4="8",  # D = 8
            weight="240",
            condition="100",
            level=28,
            cost=2300,
            affect_data=[],
            extra_descr=[]
        )

        result = self.macros.can_wear(obj, 8192)
        self.assertTrue(result, "Emerald sword should have ITEM_WIELD flag")

    def test_can_wear_emerald_sword_no_finger(self):
        obj = Item(
            id="test_id",
            area_id="test_area",
            vnum="2222",
            name="sword emerald",
            short_description="an emerald sword",
            long_description="An emerald long sword is leaning against the wall.",
            material="oldstyle",
            item_type="weapon",
            extra_flags="0",
            wear_flags="8193",  # AN = 1 | 8192 (only TAKE and WIELD)
            value0="sword",
            value1="4",
            value2="6",
            value3="slash",
            value4="8",
            weight="240",
            condition="100",
            level=28,
            cost=2300,
            affect_data=[],
            extra_descr=[]
        )

        result = self.macros.can_wear(obj, 2)
        self.assertFalse(result, "Emerald sword should NOT have ITEM_WEAR_FINGER flag")

    def test_is_obj_stat_emerald_sword_no_flags(self):
        obj = Item(
            id="test_id",
            area_id="test_area",
            vnum="2222",
            name="sword emerald",
            short_description="an emerald sword",
            long_description="An emerald long sword is leaning against the wall.",
            material="oldstyle",
            item_type="weapon",
            extra_flags="0",  # No extra flags
            wear_flags="8193",
            value0="sword",
            value1="4",
            value2="6",
            value3="slash",
            value4="8",
            weight="240",
            condition="100",
            level=28,
            cost=2300,
            affect_data=[],
            extra_descr=[]
        )

        self.assertFalse(self.macros.is_obj_stat(obj, 1), "Emerald sword should not glow")
        self.assertFalse(self.macros.is_obj_stat(obj, 2), "Emerald sword should not hum")
        self.assertFalse(self.macros.is_obj_stat(obj, 8), "Emerald sword should not be magical")

    def test_is_weapon_stat_emerald_sword_sharp(self):
        obj = Item(
            id="test_id",
            area_id="test_area",
            vnum="2222",
            name="sword emerald",
            short_description="an emerald sword",
            long_description="An emerald long sword is leaning against the wall.",
            material="oldstyle",
            item_type="weapon",
            extra_flags="0",
            wear_flags="8193",
            value0="sword",
            value1="4",
            value2="6",
            value3="slash",
            value4="8",  # D = 1<<3 = 8 = WEAPON_SHARP
            weight="240",
            condition="100",
            level=28,
            cost=2300,
            affect_data=[],
            extra_descr=[]
        )

        result = self.macros.is_weapon_stat(obj, 8)
        self.assertTrue(result, "Emerald sword should have WEAPON_SHARP flag")

    def test_is_weapon_stat_emerald_sword_no_vorpal(self):
        obj = Item(
            id="test_id",
            area_id="test_area",
            vnum="2222",
            name="sword emerald",
            short_description="an emerald sword",
            long_description="An emerald long sword is leaning against the wall.",
            material="oldstyle",
            item_type="weapon",
            extra_flags="0",
            wear_flags="8193",
            value0="sword",
            value1="4",
            value2="6",
            value3="slash",
            value4="8",  # Only SHARP (D=8), not VORPAL (E=16)
            weight="240",
            condition="100",
            level=28,
            cost=2300,
            affect_data=[],
            extra_descr=[]
        )

        result = self.macros.is_weapon_stat(obj, 16)
        self.assertFalse(result, "Emerald sword should NOT have WEAPON_VORPAL flag")

    def test_is_weapon_stat_multiple_flags(self):
        obj = Item(
            id="test_id",
            area_id="test_area",
            vnum="9999",
            name="flaming sharp sword",
            short_description="a flaming sharp sword",
            long_description="A sword both flaming and sharp.",
            material="steel",
            item_type="weapon",
            extra_flags="0",
            wear_flags="8193",
            value0="sword",
            value1="5",
            value2="8",
            value3="slash",
            value4="9",  # AD = (1<<0) | (1<<3) = 1 | 8 = 9
            weight="300",
            condition="100",
            level=30,
            cost=5000,
            affect_data=[],
            extra_descr=[]
        )

        self.assertTrue(self.macros.is_weapon_stat(obj, 1), "Should have WEAPON_FLAMING")
        self.assertTrue(self.macros.is_weapon_stat(obj, 8), "Should have WEAPON_SHARP")
        self.assertFalse(self.macros.is_weapon_stat(obj, 2), "Should NOT have WEAPON_FROST")


if __name__ == "__main__":
    unittest.main(verbosity=2)

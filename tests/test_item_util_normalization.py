import builtins
import json
import os
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def _stub_package(name: str):
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [str(Path(__file__).resolve().parents[1] / "src" / name)]
    sys.modules[name] = module
    return module


for package_name in ("api", "game", "item", "mobile", "player", "server", "util"):
    _stub_package(package_name)

mobile_module = types.ModuleType("mobile.Mobile")
mobile_module.Mobile = type("Mobile", (), {})
sys.modules["mobile.Mobile"] = mobile_module

character_module = types.ModuleType("player.Character")
character_module.Character = type("Character", (), {})
sys.modules["player.Character"] = character_module

item_registry_module = types.ModuleType("item.ItemRegistry")
item_registry_module.ItemRegistry = type("ItemRegistry", (), {})
sys.modules["item.ItemRegistry"] = item_registry_module

interp_util_module = types.ModuleType("util.InterpUtil")
interp_util_module.InterpUtil = SimpleNamespace(one_argument=lambda text: (text.strip(), ""))
sys.modules["util.InterpUtil"] = interp_util_module
builtins.Room = type("Room", (), {})

from api.ItemApi import ItemApi
from game.GameData import GameData
from util.ItemUtil import ItemUtil


class TestItemUtilNormalization(unittest.TestCase):
    @staticmethod
    def _load_game_data():
        repo_root = Path(__file__).resolve().parents[1]
        game_data_path = repo_root / "resources" / "collections" / "SOMDB.GameData.json"
        with game_data_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, list):
            for entry in payload:
                if isinstance(entry, dict) and "enums" in entry:
                    return GameData.from_json(entry)
            raise AssertionError("Game data payload did not contain an enums document.")
        return GameData.from_json(payload)

    def setUp(self):
        ItemApi.reset_for_tests()
        ItemApi.configure(self._load_game_data())
        self.liquids = {"water": {"affect": [0, 1, 10, 0, 16], "color": "clear"}}

    def tearDown(self):
        ItemApi.reset_for_tests()

    def test_fountain_preserves_liquid_name_and_metadata(self):
        item_data = {
            "id": "item-1",
            "areaId": "area-1",
            "vnum": "3135",
            "name": "fountain water",
            "shortDescription": "a fountain",
            "longDescription": "A small white fountain gushes forth here.",
            "material": "",
            "itemType": "fountain",
            "extraFlags": "0",
            "wearFlags": "0",
            "value0": "0",
            "value1": "0",
            "value2": "water",
            "value3": "0",
            "value4": "0",
            "level": 0,
            "weight": 0,
            "cost": 0,
            "condition": "G",
            "affectData": [],
            "extraDescr": [],
        }

        item = ItemUtil.normalize_item_data(item_data, self.liquids, SimpleNamespace())

        self.assertEqual("water", item.value2)
        self.assertEqual([0, 1, 10, 0, 16], item.liquid_affect_data)
        self.assertEqual("clear", item.liquid_color)

    def test_drink_container_preserves_liquid_name_and_metadata(self):
        item_data = {
            "id": "item-2",
            "areaId": "area-1",
            "vnum": "3000",
            "name": "waterskin",
            "shortDescription": "a leather waterskin",
            "longDescription": "A leather waterskin lies here.",
            "material": "leather",
            "itemType": "drink",
            "extraFlags": "0",
            "wearFlags": "A",
            "value0": "10",
            "value1": "10",
            "value2": "water",
            "value3": "0",
            "value4": "0",
            "level": 0,
            "weight": 1,
            "cost": 5,
            "condition": "G",
            "affectData": [],
            "extraDescr": [],
        }

        item = ItemUtil.normalize_item_data(item_data, self.liquids, SimpleNamespace())

        self.assertEqual("water", item.value2)
        self.assertEqual([0, 1, 10, 0, 16], item.liquid_affect_data)
        self.assertEqual("clear", item.liquid_color)


if __name__ == "__main__":
    unittest.main()

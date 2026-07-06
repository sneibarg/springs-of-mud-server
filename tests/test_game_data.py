import json
import os
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def _stub_package(name: str):
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [str(Path(__file__).resolve().parents[1] / "src" / name)]
    sys.modules[name] = module
    return module


for package_name in ("api", "game", "server", "util"):
    _stub_package(package_name)

logger_factory_module = types.ModuleType("server.LoggerFactory")
logger_factory_module.LoggerFactory = type(
    "LoggerFactory",
    (),
    {"get_logger": staticmethod(lambda *_args, **_kwargs: None)},
)
sys.modules["server.LoggerFactory"] = logger_factory_module

from api.GameApi import GameApi
from game.GameData import GameData


class TestGameData(unittest.TestCase):
    @staticmethod
    def _minimal_doc(**overrides):
        doc = {
            "_id": "test-game-data",
            "kind": "ruleset",
            "status": "active",
            "version": {
                "family": "rom24",
                "lineage": ["rom24"],
                "semver": "1.0.0",
                "createdAt": "2026-02-02T00:00:00Z",
            },
            "enums": {},
        }
        doc.update(overrides)
        return doc

    @staticmethod
    def _load_collection_doc():
        repo_root = Path(__file__).resolve().parents[1]
        game_data_path = repo_root / "resources" / "collections" / "SOMDB.GameData.json"
        with game_data_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload[0] if isinstance(payload, list) else payload

    def tearDown(self):
        GameApi.reset_for_tests()

    def test_from_json_treats_null_weapons_as_empty_table(self):
        game_data = GameData.from_json(self._minimal_doc(weapons=None))

        self.assertEqual({}, game_data.weapons)

    def test_collection_includes_rom_weapon_selection_table(self):
        game_data = GameData.from_json(self._load_collection_doc())

        self.assertEqual(
            ["sword", "mace", "dagger", "axe", "staff", "flail", "whip", "polearm"],
            list(game_data.weapons),
        )
        self.assertEqual(
            {
                "name": "staff",
                "vnum": "OBJ_VNUM_SCHOOL_STAFF",
                "type": "WEAPON_SPEAR",
                "gsn": "gsn_spear",
                "skill": "spear",
            },
            game_data.weapons["staff"],
        )

    def test_game_api_exposes_weapon_table(self):
        weapons = {
            "sword": {
                "name": "sword",
                "vnum": "OBJ_VNUM_SCHOOL_SWORD",
                "type": "WEAPON_SWORD",
                "gsn": "gsn_sword",
                "skill": "sword",
            }
        }
        game_data = GameData.from_json(self._minimal_doc(weapons=weapons))

        GameApi.configure(game_data)

        self.assertEqual(weapons, GameApi.weapons_map())

    def test_game_api_tracks_denied_sites_with_rom_wildcards(self):
        game_data = GameData.from_json(self._minimal_doc(denyList=[]))
        GameApi.configure(game_data)

        self.assertTrue(GameApi.add_denied_site("192.0.2.*"))
        self.assertFalse(GameApi.add_denied_site("192.0.2.*"))
        self.assertTrue(GameApi.has_denied_site("192.0.2.*"))
        self.assertTrue(GameApi.is_site_denied("192.0.2.10"))
        self.assertFalse(GameApi.has_denied_site("192.0.2.10"))
        self.assertFalse(GameApi.remove_denied_site("192.0.2.10"))
        self.assertTrue(GameApi.remove_denied_site("192.0.2.*"))
        self.assertEqual([], GameApi.deny_list())


if __name__ == "__main__":
    unittest.main()

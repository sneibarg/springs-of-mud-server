import json
import unittest
from pathlib import Path

from game.GameData import GameData
from object.BodyForm import BodyForm
from object.BodyParts import BodyParts


class TestBodyEnums(unittest.TestCase):
    @staticmethod
    def _game_data_doc() -> dict:
        repo_root = Path(__file__).resolve().parents[1]
        game_data_path = repo_root / "resources" / "collections" / "SOMDB.GameData.json"
        with game_data_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, list):
            for entry in payload:
                if isinstance(entry, dict) and "enums" in entry:
                    return entry
            return {}
        return payload

    def tearDown(self):
        BodyForm.reset_for_tests()
        BodyParts.reset_for_tests()

    def test_body_form_matches_game_data(self):
        game_data = GameData.from_json(self._game_data_doc())
        BodyForm.reset_for_tests()
        BodyForm.configure(game_data)

        game_data_body_form = game_data.enums.get("bodyForm", {})
        class_body_form = {name: int(member.value) for name, member in BodyForm.members().items()}
        self.assertEqual(game_data_body_form, class_body_form)

    def test_body_parts_matches_game_data(self):
        game_data = GameData.from_json(self._game_data_doc())
        BodyParts.reset_for_tests()
        BodyParts.configure(game_data)

        game_data_body_parts = game_data.enums.get("bodyParts", {})
        class_body_parts = {name: int(member.value) for name, member in BodyParts.members().items()}
        self.assertEqual(game_data_body_parts, class_body_parts)

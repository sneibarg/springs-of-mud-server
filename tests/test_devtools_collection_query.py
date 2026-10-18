import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from devtools import collection_query


class TestCollectionQuery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.collections_dir = Path(self.tmp.name)
        self._write(
            "SOMDB.Skills.json",
            [
                {
                    "_id": {"$oid": "skill-1"},
                    "name": "axe",
                    "kind": "skill",
                    "handlerId": "skill.none",
                    "target": "IGNORE",
                    "levelByClass": {"mage": 1, "warrior": 1},
                    "payload": {"toChar": {"msgOff": "!Axe!"}},
                },
                {
                    "_id": {"$oid": "skill-2"},
                    "name": "bash",
                    "kind": "skill",
                    "handlerId": "skill.bash",
                    "target": "CHARACTER_DEFENSIVE",
                    "levelByClass": {"mage": 99, "warrior": 6},
                },
            ],
        )
        self._write(
            "SOMDB.Items.json",
            [
                {
                    "_id": {"$oid": "item-1"},
                    "vnum": "6600",
                    "name": "axe toy",
                    "itemType": "weapon",
                    "level": 0,
                }
            ],
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name, payload):
        path = self.collections_dir / name
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle)

    def _run(self, *argv):
        output = StringIO()
        args = ["--collections-dir", str(self.collections_dir), *argv]
        with redirect_stdout(output):
            status = collection_query.main(args)
        self.assertEqual(0, status)
        return output.getvalue()

    def test_list_shows_collection_counts(self):
        output = self._run("list")

        self.assertIn("skills", output)
        self.assertIn("items", output)
        self.assertIn("2", output)

    def test_get_returns_concise_default_fields(self):
        output = self._run("get", "skills", "axe")

        self.assertIn("name", output)
        self.assertIn("handlerId", output)
        self.assertIn("skill.none", output)
        self.assertNotIn("levelByClass", output)

    def test_find_can_limit_search_and_print_fields(self):
        output = self._run(
            "find",
            "axe",
            "items",
            "--search-field",
            "name",
            "--field",
            "vnum",
            "--field",
            "name",
        )

        self.assertIn("6600", output)
        self.assertIn("axe toy", output)
        self.assertNotIn("handlerId", output)

    def test_values_support_nested_paths(self):
        output = self._run("values", "skills", "levelByClass.warrior")

        self.assertIn("1", output)
        self.assertIn("6", output)

    def test_path_prints_nested_scalar(self):
        output = self._run("path", "skills", "axe", "payload.toChar.msgOff")

        self.assertEqual("!Axe!", output.strip())


if __name__ == "__main__":
    unittest.main()

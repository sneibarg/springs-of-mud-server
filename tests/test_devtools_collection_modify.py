import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from devtools import collection_modify


class TestCollectionModify(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.collections_dir = Path(self.tmp.name)
        self.path = self.collections_dir / "SOMDB.Skills.json"
        self.documents = [
            {
                "_id": {"$oid": "skill-1"},
                "name": "axe",
                "kind": "skill",
                "handlerId": "skill.none",
                "target": "IGNORE",
                "slot": 0,
                "levelByClass": {"mage": 1, "cleric": 1, "thief": 1, "warrior": 1},
                "payload": {"toChar": {"msgObj": "", "msgOff": "!Axe!"}},
            },
            {
                "_id": {"$oid": "skill-2"},
                "name": "bash",
                "kind": "skill",
                "handlerId": "skill.bash",
                "target": "CHARACTER_DEFENSIVE",
                "slot": 0,
                "levelByClass": {"mage": 99, "cleric": 99, "thief": 8, "warrior": 6},
                "payload": {"toChar": {"msgObj": "", "msgOff": "!Bash!"}},
            },
        ]
        self._write(self.documents)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, payload):
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def _read(self):
        with self.path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _run(self, *argv):
        output = StringIO()
        args = ["--collections-dir", str(self.collections_dir), *argv]
        with redirect_stdout(output):
            status = collection_modify.main(args)
        self.assertEqual(0, status)
        return output.getvalue()

    def test_set_is_dry_run_by_default(self):
        output = self._run("set", "skills", "axe", "target", "CHAR_OFFENSIVE")

        self.assertIn("Dry run only", output)
        self.assertEqual("IGNORE", self._read()[0]["target"])

    def test_set_write_rewrites_existing_field(self):
        self._run("set", "skills", "axe", "target", "CHAR_OFFENSIVE", "--write")

        self.assertEqual("CHAR_OFFENSIVE", self._read()[0]["target"])

    def test_set_validates_existing_type_convention(self):
        with self.assertRaises(SystemExit):
            self._run("set", "skills", "axe", "slot", "not-an-int", "--write")

        self.assertEqual(0, self._read()[0]["slot"])

    def test_set_missing_key_requires_explicit_add_section(self):
        with self.assertRaises(SystemExit):
            self._run("set", "skills", "axe", "payload.toChar.success", "Done.", "--write")

        self.assertNotIn("success", self._read()[0]["payload"]["toChar"])

    def test_set_can_create_key_with_add_section_when_sibling_type_matches(self):
        self._run("set", "skills", "axe", "payload.toChar.success", "Done.", "--add-section", "--write")

        self.assertEqual("Done.", self._read()[0]["payload"]["toChar"]["success"])

    def test_add_section_requires_explicit_command(self):
        self._run("add-section", "skills", "axe", "payload.toRoom", "--write")

        self.assertEqual({}, self._read()[0]["payload"]["toRoom"])

    def test_rename_section_requires_explicit_command(self):
        self._run("rename-section", "skills", "axe", "payload", "toChar", "toRoom", "--write")

        payload = self._read()[0]["payload"]
        self.assertNotIn("toChar", payload)
        self.assertEqual({"msgObj": "", "msgOff": "!Axe!"}, payload["toRoom"])


if __name__ == "__main__":
    unittest.main()

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

    def test_add_document_dry_run_shows_document_without_writing(self):
        before = self.path.read_bytes()
        output = self._run("add-document", "skills", "--value", '{"id":"new", "name":"kick"}')
        self.assertIn('"name": "kick"', output)
        self.assertIn("Dry run only", output)
        self.assertEqual(before, self.path.read_bytes())

    def test_add_document_from_file_preserves_existing_documents(self):
        document = {"_id": {"$oid": "skill-3"}, "name": "axe", "payload": {"toChar": {"success": "Café"}}}
        source = self.collections_dir / "new-document.json"
        source.write_text(json.dumps(document), encoding="utf-8-sig")
        self._run("add-document", "skills", "--value-file", str(source), "--write")
        self.assertEqual([*self.documents, document], self._read())

    def test_add_document_rejects_duplicates_and_invalid_values_without_writing(self):
        for value in [[], {}, "text", {"name": "kick"}, {"id": True},
                      {"_id": {"$oid": "skill-1"}}, {"id": "new", "_id": {"$oid": "skill-2"}}]:
            with self.subTest(value=value):
                before = self.path.read_bytes()
                with self.assertRaises(SystemExit):
                    self._run("add-document", "skills", "--value", json.dumps(value), "--write")
                self.assertEqual(before, self.path.read_bytes())

    def test_add_document_custom_identifier(self):
        self._run("add-document", "skills", "--value", '{"name":"kick"}', "--lookup-field", "name", "--write")
        with self.assertRaises(SystemExit):
            self._run("add-document", "skills", "--value", '{"name":"kick"}', "--lookup-field", "name", "--write")
        self.assertEqual(3, len(self._read()))

    def test_add_document_to_empty_collection(self):
        self._write([])
        self._run("add-document", "skills", "--value", '{"vnum":0}', "--write")
        self.assertEqual([{"vnum": 0}], self._read())

    def test_add_document_rejects_malformed_json_and_missing_file(self):
        for source in [("--value", "{"), ("--value-file", str(self.collections_dir / "missing.json"))]:
            with self.subTest(source=source), self.assertRaises(SystemExit):
                self._run("add-document", "skills", *source, "--write")
        self.assertEqual(self.documents, self._read())

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

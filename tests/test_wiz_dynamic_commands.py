import json
import os
import unittest


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COMMANDS_PATH = os.path.join(ROOT, "resources", "collections", "SOMDB.Commands.json")


class TestWizDynamicCommandMetadata(unittest.TestCase):
    def test_migrated_wiz_commands_have_guards(self):
        expected = {
            "at",
            "clone",
            "freeze",
            "goto",
            "incognito",
            "invis",
            "log",
            "nochannels",
            "noemote",
            "noshout",
            "notell",
            "poofin",
            "poofout",
            "prefix",
            "restore",
            "return",
            "set",
            "smote",
            "snoop",
            "switch",
        }
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        for name in expected:
            self.assertTrue(commands[name].get("guards"), name)

    def test_set_command_metadata_has_payloads_for_subcommands(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        payload = commands["set"]["payload"]["toChar"]
        expected_keys = {
            "syntax",
            "skillSyntax",
            "mobileSyntax",
            "objectSyntax",
            "roomSyntax",
            "targetMissing",
            "unknownSkill",
            "valueMustBeNumeric",
            "noSuchObject",
            "noSuchLocation",
            "privateRoom",
        }
        self.assertTrue(expected_keys.issubset(payload.keys()))

    def test_at_command_metadata_uses_destination_guards(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        guards = commands["at"]["guards"]
        predicates = [entry.get("predicate", "") for entry in guards]
        self.assertIn("lambda v: WizApi.at_missing_argument(v)", predicates)
        self.assertIn("lambda v: WizApi.at_location(v) is None", predicates)
        self.assertIn("lambda v: WizApi.at_private(v)", predicates)


if __name__ == "__main__":
    unittest.main()

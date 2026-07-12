import json
import os
import unittest


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COMMANDS_PATH = os.path.join(ROOT, "resources", "collections", "SOMDB.Commands.json")


class TestWizDynamicCommandMetadata(unittest.TestCase):
    def test_migrated_wiz_commands_have_guards(self):
        expected = {
            "advance",
            "allow",
            "at",
            "ban",
            "clone",
            "deny",
            "flag",
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

    def test_switch_metadata_uses_rom_order_low_code_guards(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        guards = commands["switch"]["guards"]
        predicates = [entry.get("predicate", "") for entry in guards]
        message_keys = [entry.get("messageKey", "") for entry in guards]
        self.assertEqual(
            [
                "lambda v: not InterpUtil.argument_text(v)",
                "lambda v: WizApi.switch_without_session(v)",
                "lambda v: WizApi.switched(v)",
                "lambda v: WizApi.switch_target(v) is None",
                "lambda v: WizApi.switch_self(v)",
                "lambda v: WizApi.switch_non_mobile(v)",
                "lambda v: WizApi.switch_private(v)",
                "lambda v: WizApi.switch_in_use(v)",
            ],
            predicates,
        )
        self.assertEqual("", message_keys[1])
        self.assertEqual("default", message_keys[4])

    def test_advance_metadata_uses_low_code_guards(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        guards = commands["advance"]["guards"]
        self.assertEqual(
            [
                "lambda v: WizApi.advance_syntax_invalid(v)",
                "lambda v: WizApi.advance_target_missing(v)",
                "lambda v: WizApi.advance_target_is_npc(v)",
                "lambda v: WizApi.advance_level_invalid(v)",
                "lambda v: WizApi.advance_trust_limited(v)",
            ],
            [entry.get("predicate", "") for entry in guards],
        )
        self.assertEqual("lambda v: WizApi.max_level_token(v)", guards[3].get("tokenFactory", ""))

    def test_flag_metadata_uses_low_code_guards(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        guards = commands["flag"]["guards"]
        self.assertEqual(
            [
                "lambda v: WizApi.flag_kind_missing(v)",
                "lambda v: WizApi.flag_target_arg_missing(v)",
                "lambda v: WizApi.flag_field_missing(v)",
                "lambda v: WizApi.flag_changes_missing(v)",
                "lambda v: WizApi.flag_kind_invalid(v)",
                "lambda v: WizApi.flag_target_missing(v)",
                "lambda v: WizApi.flag_act_is_pc(v)",
                "lambda v: WizApi.flag_plr_is_npc(v)",
                "lambda v: WizApi.flag_form_pc(v)",
                "lambda v: WizApi.flag_parts_pc(v)",
                "lambda v: WizApi.flag_comm_npc(v)",
                "lambda v: WizApi.flag_field_invalid(v)",
                "lambda v: WizApi.flag_unknown_name(v)",
            ],
            [entry.get("predicate", "") for entry in guards],
        )

    def test_allow_deny_ban_metadata_uses_low_code_guards(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        self.assertEqual(
            [
                "lambda v: not InterpUtil.argument_text(v)",
                "lambda v: WizApi.allow_site_missing(v)",
            ],
            [entry.get("predicate", "") for entry in commands["allow"]["guards"]],
        )
        self.assertEqual(
            [
                "lambda v: not InterpUtil.argument_text(v)",
                "lambda v: WizApi.deny_target_missing(v)",
                "lambda v: WizApi.deny_target_is_npc(v)",
                "lambda v: WizApi.deny_target_trust_failed(v)",
            ],
            [entry.get("predicate", "") for entry in commands["deny"]["guards"]],
        )
        self.assertEqual(
            [
                "lambda v: not InterpUtil.argument_text(v)",
                "lambda v: WizApi.ban_target_missing(v)",
                "lambda v: WizApi.ban_target_is_npc(v)",
                "lambda v: WizApi.ban_target_trust_failed(v)",
                "lambda v: WizApi.ban_target_account_missing(v)",
            ],
            [entry.get("predicate", "") for entry in commands["ban"]["guards"]],
        )

    def test_follow_metadata_uses_rom_order_low_code_guards(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        guards = commands["follow"]["guards"]
        self.assertEqual(
            [
                "lambda v: not InterpUtil.argument_text(v)",
                "lambda v: CommunicationsApi.follow_target(v) is None",
                "lambda v: CommunicationsApi.follow_charmed_with_master(v)",
                "lambda v: CommunicationsApi.follow_self_without_master(v)",
                "lambda v: CommunicationsApi.follow_target_blocks_followers(v)",
            ],
            [entry.get("predicate", "") for entry in guards],
        )
        self.assertEqual("lambda v: CommunicationsApi.follow_target_tokens(v)", guards[2].get("tokenFactory", ""))
        self.assertEqual("lambda v: CommunicationsApi.follow_target_tokens(v)", guards[4].get("tokenFactory", ""))

    def test_order_group_split_metadata_uses_rom_order_low_code_guards(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}

        self.assertEqual(
            [
                "lambda v: CommunicationsApi.order_delete(v)",
                "lambda v: CommunicationsApi.order_missing_argument(v)",
                "lambda v: CommunicationsApi.order_actor_charmed(v)",
                "lambda v: CommunicationsApi.order_target_missing(v)",
                "lambda v: CommunicationsApi.order_target_self(v)",
                "lambda v: CommunicationsApi.order_target_not_submissive(v)",
            ],
            [entry.get("predicate", "") for entry in commands["order"]["guards"]],
        )
        self.assertEqual(
            [
                "lambda v: CommunicationsApi.group_target_missing(v)",
                "lambda v: CommunicationsApi.group_actor_follows_another(v)",
                "lambda v: CommunicationsApi.group_target_not_follower(v)",
                "lambda v: CommunicationsApi.group_target_charmed(v)",
                "lambda v: CommunicationsApi.group_actor_charmed(v)",
            ],
            [entry.get("predicate", "") for entry in commands["group"]["guards"]],
        )
        self.assertEqual(
            [
                "lambda v: CommunicationsApi.split_missing_amount(v)",
                "lambda v: CommunicationsApi.split_negative(v)",
                "lambda v: CommunicationsApi.split_zero(v)",
                "lambda v: CommunicationsApi.split_insufficient_funds(v)",
                "lambda v: CommunicationsApi.split_too_few_members(v)",
                "lambda v: CommunicationsApi.split_share_zero(v)",
            ],
            [entry.get("predicate", "") for entry in commands["split"]["guards"]],
        )


if __name__ == "__main__":
    unittest.main()

import unittest
from enum import IntEnum
from types import SimpleNamespace

from player.CharacterMacros import CharacterMacros
from util.CommunicationsUtil import CommunicationsUtil


class _PlayerActBits(IntEnum):
    PLR_AUTOEXIT = 1 << 0
    PLR_AUTOASSIST = 1 << 1


class _CommFlags(IntEnum):
    COMM_BRIEF = 1 << 2


class _AffectedBy(IntEnum):
    AFF_HIDE = 1 << 2


class TestCharacterMacrosTrain(unittest.TestCase):
    def tearDown(self):
        CharacterMacros.reset_for_tests()

    def _configure_with_flag_enums(self):
        CharacterMacros.configure(
            registry_provider=lambda: None,
            enums_provider=lambda: {
                "playerActBits": _PlayerActBits,
                "commFlags": _CommFlags,
                "affectedBy": _AffectedBy,
            },
            attribute_bonuses_provider=lambda: {},
            pc_races_provider=lambda: {},
        )

    def test_get_max_train_uses_configured_pc_races(self):
        CharacterMacros.configure(
            registry_provider=lambda: None,
            enums_provider=lambda: {},
            attribute_bonuses_provider=lambda: {},
            pc_races_provider=lambda: {
                "human": {"max_stats": [18, 18, 18, 18, 18]},
                "elf": {"max_stats": [16, 20, 18, 21, 15]},
            },
        )
        character = SimpleNamespace(race="human")

        self.assertEqual(18, CharacterMacros.get_max_train(character, 0, 17))
        self.assertEqual(18, CharacterMacros.get_max_train(character, 4, 13))

    def test_get_max_train_prefers_character_race_object(self):
        CharacterMacros.configure(
            registry_provider=lambda: None,
            enums_provider=lambda: {},
            attribute_bonuses_provider=lambda: {},
            pc_races_provider=lambda: {"human": {"max_stats": [18, 18, 18, 18, 18]}},
        )
        character = SimpleNamespace(
            race="human",
            character_race=SimpleNamespace(
                max_strength=20,
                max_intelligence=16,
                max_wisdom=19,
                max_dexterity=14,
                max_constitution=21,
            ),
        )

        self.assertEqual(20, CharacterMacros.get_max_train(character, 0, 17))
        self.assertEqual(21, CharacterMacros.get_max_train(character, 4, 13))

    def test_get_max_train_falls_back_when_race_missing(self):
        CharacterMacros.configure(
            registry_provider=lambda: None,
            enums_provider=lambda: {},
            attribute_bonuses_provider=lambda: {},
            pc_races_provider=lambda: {"human": {"max_stats": [18, 18, 18, 18, 18]}},
        )
        character = SimpleNamespace(race="unknown")

        self.assertEqual(14, CharacterMacros.get_max_train(character, 0, 14))

    def test_toggle_player_act_keeps_status_flag_integer(self):
        self._configure_with_flag_enums()
        character = SimpleNamespace(status_flags=SimpleNamespace(act=0), role="player")

        result = CharacterMacros.toggle_player_act(character, "PLR_AUTOEXIT", "off", "on")

        self.assertEqual("on", result)
        self.assertEqual(_PlayerActBits.PLR_AUTOEXIT.value, character.status_flags.act)
        self.assertIsInstance(character.status_flags.act, int)

    def test_set_act_flags_sets_bit_without_replacing_existing_bits(self):
        self._configure_with_flag_enums()
        character = SimpleNamespace(
            status_flags=SimpleNamespace(act=_PlayerActBits.PLR_AUTOEXIT.value),
            role="player",
        )

        CharacterMacros.set_act_flags(character, _PlayerActBits.PLR_AUTOASSIST.value)

        self.assertEqual(
            _PlayerActBits.PLR_AUTOEXIT.value | _PlayerActBits.PLR_AUTOASSIST.value,
            character.status_flags.act,
        )

    def test_toggle_comm_keeps_status_flag_integer(self):
        self._configure_with_flag_enums()
        character = SimpleNamespace(status_flags=SimpleNamespace(comm=0))

        result = CharacterMacros.toggle_comm(character, "COMM_BRIEF", "off", "on")

        self.assertEqual("on", result)
        self.assertEqual(_CommFlags.COMM_BRIEF.value, character.status_flags.comm)
        self.assertIsInstance(character.status_flags.comm, int)

    def test_set_comm_flags_sets_bit_without_replacing_existing_bits(self):
        self._configure_with_flag_enums()
        character = SimpleNamespace(status_flags=SimpleNamespace(comm=1))

        CharacterMacros.set_comm_flags(character, _CommFlags.COMM_BRIEF.value)

        self.assertEqual(1 | _CommFlags.COMM_BRIEF.value, character.status_flags.comm)

    def test_set_affected_by_name_keeps_status_flag_integer(self):
        self._configure_with_flag_enums()
        character = SimpleNamespace(status_flags=SimpleNamespace(affected_by=0))

        CharacterMacros.set_affected_by_name(character, _AffectedBy, "AFF_HIDE", True)

        self.assertEqual(_AffectedBy.AFF_HIDE.value, character.status_flags.affected_by)
        self.assertIsInstance(character.status_flags.affected_by, int)

    def test_communications_util_sets_comm_flag_as_integer(self):
        character = SimpleNamespace(status_flags=SimpleNamespace(comm=0))

        CommunicationsUtil.set_comm(character, _CommFlags, "COMM_BRIEF", True)

        self.assertEqual(_CommFlags.COMM_BRIEF.value, character.status_flags.comm)
        self.assertIsInstance(character.status_flags.comm, int)

    def test_player_auto_assist_checks_player_act_bits(self):
        self._configure_with_flag_enums()
        character = SimpleNamespace(
            status_flags=SimpleNamespace(act=_PlayerActBits.PLR_AUTOASSIST.value),
            role="player",
        )

        self.assertTrue(CharacterMacros.player_auto_assist(character))

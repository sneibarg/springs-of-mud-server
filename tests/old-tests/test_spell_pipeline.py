import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from interp.commands.Fight import Fight
from skill.Spell import Spell
from skill.SpellSpeech import SpellSpeech


class TestSpellPipeline(unittest.TestCase):
    def test_spell_from_json_extracts_oid_and_lambdas(self):
        spell = Spell.from_json(
            {
                "_id": {"$oid": "abc123"},
                "name": "unit spell",
                "kind": "spell",
                "handlerId": "spell.unit_spell",
                "target": "IGNORE",
                "minPosition": "STANDING",
                "slot": 1,
                "minMana": 5,
                "beats": 12,
                "nounDamage": "",
                "msgOff": "",
                "msgObj": "",
                "levelByClass": {},
                "ratingByClass": {},
                "functionName": "unit_spell",
                "lambdas": ["lambda ctx: ctx.mark_performed()"],
                "affectData": [],
            }
        )

        self.assertEqual("abc123", spell.id)
        self.assertEqual(["lambda ctx: ctx.mark_performed()"], spell.lambdas)

    def test_do_cast_executes_spell_lambdas_and_deducts_mana(self):
        registry_service = Mock()
        registry_service.room_registry = Mock()
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()

        spell = SimpleNamespace(
            name="unit spell",
            kind="spell",
            handler_id="spell.unit_spell",
            target="IGNORE",
            min_position="STANDING",
            slot=1,
            min_mana=5,
            beats=12,
            noun_damage="",
            msg_off="",
            msg_obj="",
            level_by_class={},
            rating_by_class={},
            function_name="unit_spell",
            lambdas=["lambda ctx: ctx.mark_performed()"],
            affect_data=[],
        )
        registry_service.spell_registry.all_spells.return_value = [spell]

        character = SimpleNamespace(
            id="char1",
            name="Tester",
            room_id="room1",
            mana=12,
            fighting=None,
            level=10,
            character_class=SimpleNamespace(name="mage"),
        )
        same_class = SimpleNamespace(id="char2", name="MagePeer", character_class=SimpleNamespace(name="mage"))
        other_class = SimpleNamespace(id="char3", name="ClericPeer", character_class=SimpleNamespace(name="cleric"))
        room = SimpleNamespace(id="room1", characters={"char1": character, "char2": same_class, "char3": other_class}, mobiles={}, contents={})
        registry_service.room_registry.get_or_none.return_value = room

        commands = Fight(
            registry_service=registry_service,
            room_helper=Mock(),
            fight_handler=Mock(),
        )
        context = SimpleNamespace(result="'unit spell'", parameters=[], finish=Mock())

        with patch("interp.commands.Fight.CharacterApi.is_npc", return_value=False), \
             patch("skill.SpellApi.CharacterApi.is_npc", return_value=False):
            payload = commands.do_cast(character, context)

        self.assertEqual(7, character.mana)
        payloads = payload["payloads"]
        self.assertEqual("You cast unit spell.\r\n", next(entry["to_char"] for entry in payloads if entry.get("to_char")))
        room_payloads = [entry for entry in payloads if entry.get("to_room")]
        visible_payload = next(entry for entry in room_payloads if entry["targets"] == [same_class])
        obscure_payload = next(entry for entry in room_payloads if entry["targets"] == [other_class])
        self.assertEqual("Tester utters the words, 'unit spell'.\r\n", visible_payload["to_room"])
        self.assertEqual("Tester utters the words, 'jiuh gszrr'.\r\n", obscure_payload["to_room"])
        context.finish.assert_called_once()

    def test_spell_speech_translates_rom_syllables(self):
        self.assertEqual("jiuh gszrr", SpellSpeech.translate_spell_name("unit spell"))
        self.assertEqual("oculocandushi a qruh", SpellSpeech.translate_spell_name("detect a trap"))

    def test_spell_collection_entries_define_lambdas(self):
        spells = json.loads(Path("resources/collections/SOMDB.Spells.json").read_text())
        self.assertTrue(spells)
        self.assertTrue(all(isinstance(spell.get("lambdas"), list) and spell["lambdas"] for spell in spells))

    def test_spell_collection_uses_composable_api_calls(self):
        spells = json.loads(Path("resources/collections/SOMDB.Spells.json").read_text())
        lambdas = [entry for spell in spells for entry in spell.get("lambdas", [])]
        self.assertTrue(all("ctx.spell_" not in entry for entry in lambdas))
        self.assertTrue(any("ctx.apply_affect_data(" in entry for entry in lambdas))

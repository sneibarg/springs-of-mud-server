import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from api.InterpApi import InterpApi
from api.SpellApi import SpellApi
from area.Room import Room
from devtools.collection_query import load_collections
from game.EnumProvider import EnumProvider
from game.GameData import GameData
from interp.Command import Command
from interp.Context import Context
from interp.commands.Fight import Fight
from item.EffectHandler import EffectHandler
from player.Character import Character
from skill.Ability import Ability
from skill.Spell import Spell
from skill.SpellRegistry import SpellRegistry
from util.FightUtil import FightUtil
from util.GenericUtil import GenericUtil


class TestCastLearnedContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collections = load_collections(
            ROOT / "resources" / "collections", ["characters", "commands", "spells", "gamedata"])

    def setUp(self):
        GameApi.reset_for_tests()
        self.addCleanup(GameApi.reset_for_tests)
        game_data = GameData.from_json(self.collections["gamedata"].documents[0])
        enums = EnumProvider({name: GenericUtil.build_int_enum(name, members)
                              for name, members in game_data.enums.items()})
        GameApi.configure(game_data, enums)
        CharacterApi.load_enums(**CharacterApi.ACTOR_ENUM_ALIASES)

        document = deepcopy(next(doc for doc in self.collections["characters"].documents
                                 if doc["name"] == "Fizban"))
        document["id"] = document.pop("_id")["$oid"]
        document.pop("_class", None)
        document.setdefault("description", "")
        document.update(level=20, mana=100, inventory=[], equipped={}, effects=[],
                        skills=[{"name": "armor", "level": 100}],
                        spells=[{"name": "armor", "level": 75}])
        self.character = Character.from_json(document)
        self.character.status_flags.pulse_daze = 0
        self.character.status_flags.drunk = 0
        self.character.character_attributes.position = CharacterApi.pos_value("POS_STANDING")

        spell_document = deepcopy(next(doc for doc in self.collections["spells"].documents
                                       if doc["name"] == "armor"))
        # Supply the class metadata required by the runtime ability contract.
        spell_document.update(levelByClass={"mage": 10}, ratingByClass={"mage": 1})
        self.spell = Spell.from_json(spell_document)
        registry = SpellRegistry()
        registry.register(self.spell)

        command_document = deepcopy(next(doc for doc in self.collections["commands"].documents
                                         if doc["name"] == "cast"))
        command_document.update(function=[], usage="")
        command = Command.from_json(command_document)
        room = Room(id=self.character.room_id, area_id=self.character.area_id)
        room.add_player_to_room(self.character)
        self.context = Context(character=self.character, command=command, room=room,
                               parameters=[], result="armor")
        interp_api = InterpApi()
        self.spell_api = SpellApi(EffectHandler(enums), interp_api)
        self.commands = Fight.__new__(Fight)
        self.commands.spell_registry = registry
        self.commands.interp_api = interp_api
        self.commands.spell_api = self.spell_api

    def test_learned_spell_resolves_guards_casts_and_applies_its_content(self):
        self.assertIs(self.spell, FightUtil.find_spell(self.commands.spell_registry, "arm", self.character))
        self.assertEqual(75, self.spell_api.casting_proficiency(self.character, self.spell))
        initial_armor = self.character.armor_class.piercing
        cost = FightUtil.cast_mana_cost(self.character, self.spell)
        with patch("api.SpellApi.random.randint", return_value=1), \
                patch.object(Ability, "check_improve") as improve:
            payload = self.commands.do_cast(self.character, self.context)

        self.assertTrue(self.context.done)
        self.assertEqual(100 - cost, self.character.mana)
        self.assertEqual(self.spell.beats, self.character.status_flags.pulse_wait)
        self.assertEqual(initial_armor - 20, self.character.armor_class.piercing)
        self.assertTrue(any(effect.type == "spell.armor" for effect in self.character.effects))
        text = "".join(entry.get("to_char", "") for entry in payload["payloads"])
        self.assertIn("You cast armor", text)
        self.assertIn("You feel someone protecting you.", text)
        improve.assert_called_once_with(self.character, self.spell.id, True, 1)

    def test_same_named_skill_does_not_satisfy_the_spell_guard(self):
        self.character.spells.clear()
        self.assertEqual(0, self.spell_api.casting_proficiency(self.character, self.spell))
        with patch.object(self.spell_api, "cast") as cast:
            payload = self.commands.do_cast(self.character, self.context)
        self.assertTrue(payload["blocked"])
        self.assertEqual("spell_not_learned", payload["blocked_key"])
        self.assertIn("don't know any spells", payload["to_char"])
        cast.assert_not_called()
        self.assertEqual(100, self.character.mana)
        self.assertEqual([], self.character.effects)

    def test_below_class_level_is_rejected_before_casting(self):
        self.character.level = 9
        self.assertEqual(0, self.spell_api.casting_proficiency(self.character, self.spell))
        with patch.object(self.spell_api, "cast") as cast:
            payload = self.commands.do_cast(self.character, self.context)
        self.assertEqual("spell_not_learned", payload["blocked_key"])
        cast.assert_not_called()

    def test_real_learned_entry_preserves_daze_and_drunk_penalties(self):
        self.character.set_learned("armor", 99, collection_name="spells")
        self.character.status_flags.pulse_daze = 1
        self.character.status_flags.drunk = 11
        self.assertEqual(44, self.spell_api.casting_proficiency(self.character, self.spell))


if __name__ == "__main__":
    unittest.main()

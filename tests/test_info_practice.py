import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from interp.commands.InfoCommands import InfoCommands


class TestInfoPractice(unittest.TestCase):
    def setUp(self):
        registry_service = Mock()
        registry_service.interp_registry = Mock()
        registry_service.room_registry = Mock()
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        registry_service.skill_registry.all_skills.return_value = []
        registry_service.spell_registry.all_spells.return_value = []

        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry
        self.commands = InfoCommands(
            registry_service=registry_service,
            command_helper=Mock(),
            room_helper=Mock(),
            player_helper=Mock(),
            session_handler=Mock(),
            weather_handler=Mock(),
        )

    def test_do_practice_lists_known_skills(self):
        self.skill_registry.all_skills.return_value = [
            SimpleNamespace(name="dagger", level_by_class={"thief": 1}, rating_by_class={"thief": 4}),
            SimpleNamespace(name="backstab", level_by_class={"thief": 1}, rating_by_class={"thief": 4}),
        ]
        self.spell_registry.all_spells.return_value = [
            SimpleNamespace(name="magic missile", level_by_class={"thief": 99}, rating_by_class={"thief": 0}),
        ]
        character = SimpleNamespace(
            skills=[
                {"name": "dagger", "level": 25},
                {"name": "backstab", "level": 1},
            ],
            spells=[
                {"name": "magic missile", "level": 33},
            ],
            level=10,
            character_class=SimpleNamespace(name="thief", skill_adept=75),
            character_attributes=SimpleNamespace(practices=3),
        )
        context = SimpleNamespace(result="", parameters=[], finish=Mock())

        with patch("interp.commands.InfoCommands.CharacterMacros.is_npc", return_value=False):
            text = self.commands.do_practice(character, context)

        self.assertIn("dagger", text)
        self.assertIn("backstab", text)
        self.assertNotIn("magic missile", text)
        self.assertIn("You have 3 practice sessions left.", text)

    def test_do_practice_practices_skill(self):
        self.skill_registry.all_skills.return_value = [
            SimpleNamespace(name="dagger", level_by_class={"thief": 1}, rating_by_class={"thief": 4}),
        ]
        attributes = SimpleNamespace(practices=2, intelligence=18)
        character = SimpleNamespace(
            id="char1",
            name="Tester",
            room_id="room1",
            level=10,
            skills=[{"name": "dagger", "level": 10}],
            spells=[],
            character_attributes=attributes,
            character_class=SimpleNamespace(name="thief", skill_adept=75),
        )
        trainer = SimpleNamespace(mobile_flags=SimpleNamespace(act=4), special_name="")
        room = SimpleNamespace(id="room1", mobiles={"mob1": trainer})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="dagger", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_PRACTICE=SimpleNamespace(value=4))

        with patch("interp.commands.InfoCommands.CharacterMacros.is_npc", return_value=False), \
             patch("interp.commands.InfoCommands.CharacterMacros.is_awake", return_value=True), \
             patch("interp.commands.InfoCommands.CharacterMacros.get_enum", return_value=act_bits), \
             patch("interp.commands.InfoCommands.CharacterMacros.is_set", side_effect=lambda flags, bit: (flags & bit) != 0), \
             patch("interp.commands.InfoCommands.CharacterMacros.get_attribute_bonus", return_value={"learn": 40}), \
            patch("interp.commands.InfoCommands.CharacterMacros.room_targets", return_value=[]):
            payload = self.commands.do_practice(character, context)

        self.assertEqual(1, attributes.practices)
        self.assertEqual(20, character.skills[0]["level"])
        self.assertEqual("You practice dagger.\r\n", payload["to_char"])

    def test_do_practice_rejects_unknown_skill(self):
        attributes = SimpleNamespace(practices=2, intelligence=18)
        character = SimpleNamespace(
            room_id="room1",
            level=10,
            skills=[{"name": "dagger", "level": 10}],
            spells=[],
            character_attributes=attributes,
            character_class=SimpleNamespace(name="thief", skill_adept=75),
        )
        trainer = SimpleNamespace(mobile_flags=SimpleNamespace(act=4), special_name="")
        room = SimpleNamespace(id="room1", mobiles={"mob1": trainer})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="bash", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_PRACTICE=SimpleNamespace(value=4))

        with patch("interp.commands.InfoCommands.CharacterMacros.is_npc", return_value=False), \
             patch("interp.commands.InfoCommands.CharacterMacros.is_awake", return_value=True), \
             patch("interp.commands.InfoCommands.CharacterMacros.get_enum", return_value=act_bits), \
             patch("interp.commands.InfoCommands.CharacterMacros.is_set", side_effect=lambda flags, bit: (flags & bit) != 0):
            text = self.commands.do_practice(character, context)

        self.assertEqual("You can't practice that.\r\n", text)

    def test_do_practice_accepts_textual_practice_trainer(self):
        self.skill_registry.all_skills.return_value = [
            SimpleNamespace(name="sword", level_by_class={"warrior": 1}, rating_by_class={"warrior": 2}),
        ]
        attributes = SimpleNamespace(practices=2, intelligence=18)
        character = SimpleNamespace(
            id="char1",
            name="Tester",
            room_id="room1",
            level=10,
            skills=[{"name": "sword", "level": 10}],
            spells=[],
            character_attributes=attributes,
            character_class=SimpleNamespace(name="warrior", skill_adept=75),
        )
        trainer = SimpleNamespace(
            mobile_flags=SimpleNamespace(act=0),
            special_name="",
            long_description="The priest of Circe is ready to help you practice.",
        )
        room = SimpleNamespace(id="room1", mobiles={"mob1": trainer})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="sword", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_PRACTICE=SimpleNamespace(value=4))

        with patch("interp.commands.InfoCommands.CharacterMacros.is_npc", return_value=False), \
             patch("interp.commands.InfoCommands.CharacterMacros.is_awake", return_value=True), \
             patch("interp.commands.InfoCommands.CharacterMacros.get_enum", return_value=act_bits), \
             patch("interp.commands.InfoCommands.CharacterMacros.is_set", side_effect=lambda flags, bit: (flags & bit) != 0), \
             patch("interp.commands.InfoCommands.CharacterMacros.get_attribute_bonus", return_value={"learn": 40}), \
             patch("interp.commands.InfoCommands.CharacterMacros.room_targets", return_value=[]):
            payload = self.commands.do_practice(character, context)

        self.assertEqual("You practice sword.\r\n", payload["to_char"])

    def test_do_practice_hides_skill_until_required_level(self):
        self.skill_registry.all_skills.return_value = [
            SimpleNamespace(name="second attack", level_by_class={"thief": 12}, rating_by_class={"thief": 5}),
            SimpleNamespace(name="sword", level_by_class={"thief": 1}, rating_by_class={"thief": 3}),
        ]
        character = SimpleNamespace(
            skills=[
                {"name": "second attack", "level": 1},
                {"name": "sword", "level": 10},
            ],
            spells=[],
            level=1,
            character_class=SimpleNamespace(name="thief", skill_adept=75),
            character_attributes=SimpleNamespace(practices=3),
        )
        context = SimpleNamespace(result="", parameters=[], finish=Mock())

        with patch("interp.commands.InfoCommands.CharacterMacros.is_npc", return_value=False):
            text = self.commands.do_practice(character, context)

        self.assertIn("sword", text)
        self.assertNotIn("second attack", text)

    def test_do_practice_rejects_skill_below_required_level(self):
        self.skill_registry.all_skills.return_value = [
            SimpleNamespace(name="second attack", level_by_class={"thief": 12}, rating_by_class={"thief": 5}),
        ]
        attributes = SimpleNamespace(practices=2, intelligence=18)
        character = SimpleNamespace(
            room_id="room1",
            level=1,
            skills=[{"name": "second attack", "level": 1}],
            spells=[],
            character_attributes=attributes,
            character_class=SimpleNamespace(name="thief", skill_adept=75),
        )
        trainer = SimpleNamespace(mobile_flags=SimpleNamespace(act=4), special_name="")
        room = SimpleNamespace(id="room1", mobiles={"mob1": trainer})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="second attack", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_PRACTICE=SimpleNamespace(value=4))

        with patch("interp.commands.InfoCommands.CharacterMacros.is_npc", return_value=False), \
             patch("interp.commands.InfoCommands.CharacterMacros.is_awake", return_value=True), \
             patch("interp.commands.InfoCommands.CharacterMacros.get_enum", return_value=act_bits), \
             patch("interp.commands.InfoCommands.CharacterMacros.is_set", side_effect=lambda flags, bit: (flags & bit) != 0):
            text = self.commands.do_practice(character, context)

        self.assertEqual("You can't practice that.\r\n", text)

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from interp.commands.Movement import Movement


class TestMovementTrain(unittest.TestCase):
    def setUp(self):
        registry_service = Mock()
        registry_service.room_registry = Mock()

        self.room_registry = registry_service.room_registry
        self.commands = Movement(
            registry_service=registry_service,
            player_helper=Mock(),
            game_data=SimpleNamespace(
                pc_races={
                    "human": {"max_stats": [18, 18, 18, 18, 18]},
                    "elf": {"max_stats": [16, 20, 18, 21, 15]},
                }
            ),
        )

    def test_do_train_lists_options_without_argument(self):
        character = SimpleNamespace(
            race="human",
            room_id="room1",
            sex="male",
            character_attributes=SimpleNamespace(
                strength=17,
                intelligence=18,
                wisdom=16,
                dexterity=18,
                constitution=18,
                trains=3,
            ),
        )
        trainer = SimpleNamespace(
            mobile_flags=SimpleNamespace(act=0),
            special_name="",
            long_description="A sailor stands here, waiting to train you.",
            description="",
        )
        room = SimpleNamespace(id="room1", mobiles={"mob1": trainer})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_TRAIN=SimpleNamespace(value=8))

        with patch("interp.commands.Movement.CharacterApi.is_npc", return_value=False), \
             patch("interp.commands.Movement.CharacterApi.get_enum", return_value=act_bits), \
             patch("interp.commands.Movement.CharacterApi.is_set", side_effect=lambda flags, bit: (flags & bit) != 0):
            text = self.commands.do_train(character, context)

        self.assertIn("You have 3 training sessions.", text)
        self.assertIn("You can train: str wis hp mana.", text)

    def test_do_train_accepts_textual_trainer_and_trains_stat(self):
        attributes = SimpleNamespace(
            strength=17,
            intelligence=13,
            wisdom=13,
            dexterity=13,
            constitution=13,
            trains=2,
        )
        character = SimpleNamespace(
            id="char1",
            name="Tester",
            race="human",
            room_id="room1",
            sex="male",
            character_attributes=attributes,
        )
        trainer = SimpleNamespace(
            mobile_flags=SimpleNamespace(act=0),
            special_name="",
            long_description="Your guildmaster stands here.",
            description="A smaller man dressed in nothing but a tunic stands here waiting to train you.",
        )
        room = SimpleNamespace(id="room1", mobiles={"mob1": trainer}, characters={})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="str", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_TRAIN=SimpleNamespace(value=8))

        with patch("interp.commands.Movement.CharacterApi.is_npc", return_value=False), \
             patch("interp.commands.Movement.CharacterApi.get_enum", return_value=act_bits), \
             patch("interp.commands.Movement.CharacterApi.is_set", side_effect=lambda flags, bit: (flags & bit) != 0), \
             patch("interp.commands.Movement.CharacterApi.room_targets", return_value=[]):
            payload = self.commands.do_train(character, context)

        self.assertEqual(18, attributes.strength)
        self.assertEqual(1, attributes.trains)
        self.assertEqual("Your strength increases!\r\n", payload["to_char"])

    def test_do_train_accepts_mud_school_trainer_text(self):
        attributes = SimpleNamespace(
            strength=17,
            intelligence=13,
            wisdom=13,
            dexterity=13,
            constitution=13,
            trains=2,
        )
        character = SimpleNamespace(
            id="char1",
            name="Tester",
            race="human",
            room_id="room1",
            sex="male",
            character_attributes=attributes,
        )
        trainer = SimpleNamespace(
            mobile_flags=SimpleNamespace(act=0),
            special_name="",
            long_description="An adept of Furey is here, training young students.",
            description="He is big and bad.  Don't mess with him.",
        )
        room = SimpleNamespace(id="room1", mobiles={"mob1": trainer}, characters={})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="str", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_TRAIN=SimpleNamespace(value=8))

        with patch("interp.commands.Movement.CharacterApi.is_npc", return_value=False), \
             patch("interp.commands.Movement.CharacterApi.get_enum", return_value=act_bits), \
             patch("interp.commands.Movement.CharacterApi.is_set", side_effect=lambda flags, bit: (flags & bit) != 0), \
             patch("interp.commands.Movement.CharacterApi.room_targets", return_value=[]):
            payload = self.commands.do_train(character, context)

        self.assertEqual(18, attributes.strength)
        self.assertEqual(1, attributes.trains)
        self.assertEqual("Your strength increases!\r\n", payload["to_char"])

    def test_do_train_trains_hp(self):
        attributes = SimpleNamespace(
            strength=13,
            intelligence=13,
            wisdom=13,
            dexterity=13,
            constitution=13,
            trains=1,
        )
        character = SimpleNamespace(
            id="char1",
            name="Tester",
            race="human",
            room_id="room1",
            sex="male",
            hit=40,
            max_hit=40,
            mana=20,
            max_mana=20,
            character_attributes=attributes,
        )
        trainer = SimpleNamespace(
            mobile_flags=SimpleNamespace(act=8),
            special_name="",
            long_description="",
            description="",
        )
        room = SimpleNamespace(id="room1", mobiles={"mob1": trainer}, characters={})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="hp", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_TRAIN=SimpleNamespace(value=8))

        with patch("interp.commands.Movement.CharacterApi.is_npc", return_value=False), \
             patch("interp.commands.Movement.CharacterApi.get_enum", return_value=act_bits), \
             patch("interp.commands.Movement.CharacterApi.is_set", side_effect=lambda flags, bit: (flags & bit) != 0), \
             patch("interp.commands.Movement.CharacterApi.room_targets", return_value=[]):
            payload = self.commands.do_train(character, context)

        self.assertEqual(0, attributes.trains)
        self.assertEqual(50, character.hit)
        self.assertEqual(50, character.max_hit)
        self.assertEqual("Your durability increases!\r\n", payload["to_char"])

    def test_do_train_rejects_missing_trainer(self):
        character = SimpleNamespace(
            race="human",
            room_id="room1",
            character_attributes=SimpleNamespace(
                strength=13,
                intelligence=13,
                wisdom=13,
                dexterity=13,
                constitution=13,
                trains=2,
            ),
        )
        room = SimpleNamespace(id="room1", mobiles={})
        self.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="str", parameters=[], finish=Mock())
        act_bits = SimpleNamespace(ACT_TRAIN=SimpleNamespace(value=8))

        with patch("interp.commands.Movement.CharacterApi.is_npc", return_value=False), \
             patch("interp.commands.Movement.CharacterApi.get_enum", return_value=act_bits):
            text = self.commands.do_train(character, context)

        self.assertEqual("You can't do that here.\r\n", text)

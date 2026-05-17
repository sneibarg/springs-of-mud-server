import unittest
from enum import IntEnum
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from game.UpdateHandler import UpdateHandler
from interp.commands.Communications import Communications
from player.Character import Character
from player.CharacterRegistry import CharacterRegistry
from player.CharacterService import CharacterService
from server.ServiceConfig import ServiceConfig


def build_character_data(character_id: str = "char_001") -> dict:
    return {
        "id": character_id,
        "accountId": "acct_001",
        "title": "the Tester",
        "description": "A test character.",
        "cloaked": False,
        "guild": "",
        "characterRace": {
            "whoName": "Human",
            "points": 0,
            "classMult": 100,
            "skills": [""],
            "strength": 13,
            "maxStrength": 18,
            "intelligence": 13,
            "maxIntelligence": 18,
            "wisdom": 13,
            "maxWisdom": 18,
            "dexterity": 13,
            "maxDexterity": 18,
            "constitution": 13,
            "maxConstitution": 18,
            "size": "SIZE_MEDIUM",
        },
        "name": "Tester",
        "areaId": "area_001",
        "roomId": "room_001",
        "role": "player",
        "sex": "male",
        "level": 5,
        "hit": 25,
        "maxHit": 30,
        "mana": 15,
        "maxMana": 20,
        "movement": 18,
        "maxMovement": 20,
        "gold": 10,
        "silver": 5,
        "trust": 0,
        "inventory": [],
        "effects": [],
        "skills": [],
        "spells": [],
        "characterFlags": {
            "act": "",
            "comm": "",
            "affectedBy": "",
        },
        "characterAttributes": {
            "strength": 13,
            "intelligence": 12,
            "wisdom": 11,
            "dexterity": 10,
            "constitution": 9,
            "alignment": 0,
            "maxWeight": 100,
            "maxItems": 10,
            "position": 8,
            "wimpy": 0,
            "trains": 0,
            "practices": 0,
            "points": 0,
            "experience": 100,
            "accumulatedExperience": 100,
            "experiencePerLevel": 1000,
        },
        "temporalMechanics": {
            "played": 0,
            "logon": 0,
            "pulseWait": 0,
            "pulseDaze": 0,
        },
        "armorClass": {
            "piercing": 100,
            "bashing": 100,
            "slashing": 100,
            "magic": 100,
        },
        "characterClass": {
            "name": "Mage",
            "attrPrime": 0,
            "weapon": 0,
            "guild": 0,
            "skillAdept": 75,
            "thac000": 20,
            "thac032": -4,
            "hpMin": 8,
            "hpMax": 12,
            "manaGain": True,
            "baseGroup": "mage basics",
            "defaultGroup": "mage default",
        },
        "promptFormat": {
            "hp": True,
            "max_hp": True,
            "mana": True,
            "max_mana": False,
            "movement": True,
            "max_movement": False,
            "xp": False,
            "max_xp": False,
            "gold": False,
            "silver": False,
            "alignment": False,
            "room_name": False,
            "exits": False,
            "room_vnum": False,
            "area_name": False,
            "carriage_return": False,
        },
        "equipped": {},
    }


class TestCharacterSave(unittest.TestCase):
    def test_character_from_json_reads_character_race_map(self):
        character = Character.from_json(build_character_data("char_001"))

        self.assertEqual("Human", character.race)
        self.assertEqual("Human", character.character_race.who_name)
        self.assertEqual(18, character.character_race.max_strength)
        self.assertEqual(100, character.character_race.class_mult)

    def test_character_from_json_translates_rom_style_character_race(self):
        payload = build_character_data("char_001")
        payload["characterRace"] = {
            "whoName": "Human",
            "points": 0,
            "classMult": [100, 100, 100, 100],
            "skills": [""],
            "stats": [13, 13, 13, 13, 13],
            "maxStats": [18, 18, 18, 18, 18],
            "size": "SIZE_MEDIUM",
        }

        character = Character.from_json(payload)

        self.assertEqual(100, character.character_race.class_mult)
        self.assertEqual(13, character.character_race.strength)
        self.assertEqual(18, character.character_race.max_constitution)

    @patch("player.CharacterService.requests.put")
    @patch("player.CharacterService.requests.get")
    def test_character_service_save_character_puts_payload_with_id(self, mock_get, mock_put):
        mock_get.return_value.json.return_value = []
        mock_get.return_value.raise_for_status.return_value = None
        mock_put.return_value.raise_for_status.return_value = None
        mock_put.return_value.json.return_value = build_character_data("char_001")

        config = ServiceConfig(
            game_data_endpoint="http://test/game",
            commands_endpoint="http://test/commands",
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles",
            skills_endpoint="http://test/skills",
            spells_endpoint="http://test/spells",
            shops_endpoint="http://test/shops",
            specials_endpoint="http://test/specials",
            socials_endpoint="http://test/socials",
            helps_endpoint="http://test/helps",
            resets_endpoint="http://test/resets",
            notes_endpoint="http://test/notes",
        )
        service = CharacterService(config, CharacterRegistry())
        character = Character.from_json(build_character_data("char_001"))

        saved = service.save_character(character)

        self.assertTrue(saved)
        payload = mock_put.call_args.kwargs["json"]
        self.assertEqual("char_001", payload["id"])
        self.assertEqual("acct_001", payload["accountId"])
        self.assertEqual("Human", payload["characterRace"]["whoName"])
        self.assertEqual(100, payload["characterRace"]["classMult"])
        self.assertEqual(18, payload["characterRace"]["maxStrength"])
        self.assertEqual(True, payload["promptFormat"]["hp"])
        self.assertEqual(True, payload["promptFormat"]["max_hp"])

    def test_do_save_uses_character_service(self):
        registry_service = Mock()
        registry_service.character_registry = Mock()
        registry_service.room_registry = Mock()
        session_handler = Mock()
        character_service = Mock()
        character_service.save_character.return_value = True
        command = Communications(registry_service, session_handler, character_service)

        context = Mock()
        payload = command.do_save(Mock(spec=Character), context)

        context.finish.assert_called_once()
        character_service.save_character.assert_called_once()
        self.assertEqual({"to_char": "Saving. Remember that ROM has automatic saving now.\r\n", "blocked": False}, payload)


class TestUpdateAutosave(unittest.IsolatedAsyncioTestCase):
    async def test_char_update_autosaves_only_due_bucket(self):
        class Positions(IntEnum):
            POS_STUNNED = 4

        registry_service = Mock()
        registry_service.character_registry.all_characters.return_value = []
        registry_service.room_registry.all_rooms.return_value = []
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        registry_service.combat_registry = Mock()

        due_character = Character.from_json(build_character_data("a"))
        later_character = Character.from_json(build_character_data("b"))

        session_handler = Mock()
        session_handler.get_playing_sessions.return_value = [
            SimpleNamespace(character=due_character),
            SimpleNamespace(character=later_character),
        ]

        handler = UpdateHandler(
            player_helper=Mock(),
            weather_handler=Mock(),
            area_handler=Mock(),
            mobile_handler=Mock(),
            fight_handler=Mock(),
            message_bus=Mock(),
            registry_service=registry_service,
            character_service=Mock(),
            session_handler=session_handler,
        )
        handler.PositionsEnum = Positions
        handler.save_number = 6

        with patch("game.UpdateHandler.asyncio.to_thread", new=AsyncMock(side_effect=lambda fn, *args: fn(*args))):
            await handler.char_update()

        handler.character_service.save_character.assert_called_once_with(due_character)

    async def test_char_update_applies_rom_condition_tick_and_messages(self):
        class Positions(IntEnum):
            POS_STUNNED = 4

        registry_service = Mock()
        character = Character.from_json(build_character_data("char_001"))
        character.status_flags.drunk = 1
        character.status_flags.thirst = 1
        character.status_flags.hunger = 1
        registry_service.character_registry.all_characters.return_value = [character]
        registry_service.room_registry.all_rooms.return_value = []
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        registry_service.combat_registry = Mock()

        message_bus = Mock()
        message_bus.text_to_message.side_effect = lambda text: text
        message_bus.send_to_character = AsyncMock()
        session_handler = Mock()
        session_handler.get_playing_sessions.return_value = []

        handler = UpdateHandler(
            player_helper=Mock(),
            weather_handler=Mock(),
            area_handler=Mock(),
            mobile_handler=Mock(),
            fight_handler=Mock(),
            message_bus=message_bus,
            registry_service=registry_service,
            character_service=Mock(),
            session_handler=session_handler,
        )
        handler.PositionsEnum = Positions

        with patch("game.UpdateHandler.CharacterApi.is_immortal", return_value=False):
            await handler.char_update()

        self.assertEqual(0, character.status_flags.drunk)
        self.assertEqual(0, character.status_flags.thirst)
        self.assertEqual(0, character.status_flags.hunger)
        self.assertEqual(
            [
                ("char_001", "You are sober.\r\n"),
                ("char_001", "You are thirsty.\r\n"),
                ("char_001", "You are hungry.\r\n"),
            ],
            [call.args for call in message_bus.send_to_character.await_args_list],
        )

    async def test_char_update_uses_faster_hunger_tick_for_large_races(self):
        class Positions(IntEnum):
            POS_STUNNED = 4
            POS_STANDING = 8

        registry_service = Mock()
        character = Character.from_json(build_character_data("large_char"))
        character.character_race.size = "SIZE_LARGE"
        character.status_flags.hunger = 2
        registry_service.character_registry.all_characters.return_value = [character]
        registry_service.room_registry.all_rooms.return_value = []
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        registry_service.combat_registry = Mock()

        message_bus = Mock()
        message_bus.text_to_message.side_effect = lambda text: text
        message_bus.send_to_character = AsyncMock()
        session_handler = Mock()
        session_handler.get_playing_sessions.return_value = []

        handler = UpdateHandler(
            player_helper=Mock(),
            weather_handler=Mock(),
            area_handler=Mock(),
            mobile_handler=Mock(),
            fight_handler=Mock(),
            message_bus=message_bus,
            registry_service=registry_service,
            character_service=Mock(),
            session_handler=session_handler,
        )
        handler.PositionsEnum = Positions

        with patch("game.UpdateHandler.CharacterApi.is_immortal", return_value=False):
            await handler.char_update()

        self.assertEqual(0, character.status_flags.hunger)
        message_bus.send_to_character.assert_awaited_once_with("large_char", "You are hungry.\r\n")

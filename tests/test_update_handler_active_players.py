import asyncio
import os
import sys
import unittest
from enum import IntEnum
from types import ModuleType
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, SRC_PATH)


def _stub_package(package_name: str) -> None:
    if package_name in sys.modules:
        return
    package = ModuleType(package_name)
    package.__path__ = [os.path.join(SRC_PATH, package_name)]
    sys.modules[package_name] = package


for package_name in ["area", "fight", "game", "interp", "item", "mobile", "player", "server", "skill", "util"]:
    _stub_package(package_name)

from game.UpdateHandler import UpdateHandler
from player.Character import Character


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


class Positions(IntEnum):
    POS_STUNNED = 4


class TestUpdateHandlerActivePlayers(unittest.TestCase):
    def _handler(self, playing_characters):
        registry_service = Mock()
        registry_service.character_registry.all_characters.return_value = []
        registry_service.room_registry.all_rooms.return_value = []
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        registry_service.combat_registry = Mock()

        message_bus = Mock()
        message_bus.text_to_message.side_effect = lambda text: text
        message_bus.send_to_character = AsyncMock()

        session_handler = Mock()
        session_handler.get_playing_sessions.return_value = [
            SimpleNamespace(character=character) for character in playing_characters
        ]

        handler = UpdateHandler(
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
        return handler, registry_service, message_bus

    def test_char_update_does_not_tick_offline_registry_characters(self):
        async def run_test():
            offline = Character.from_json(build_character_data("offline_char"))
            offline.status_flags.thirst = 1
            offline.status_flags.hunger = 1

            handler, registry_service, message_bus = self._handler([])
            registry_service.character_registry.all_characters.return_value = [offline]

            with patch("game.UpdateHandler.CharacterMacros.is_immortal", return_value=False):
                await handler.char_update()

            self.assertEqual(1, offline.status_flags.thirst)
            self.assertEqual(1, offline.status_flags.hunger)
            message_bus.send_to_character.assert_not_awaited()

        asyncio.run(run_test())

    def test_char_update_ticks_active_session_characters(self):
        async def run_test():
            active = Character.from_json(build_character_data("active_char"))
            active.status_flags.thirst = 1
            active.status_flags.hunger = 1

            handler, _, message_bus = self._handler([active])

            with patch("game.UpdateHandler.CharacterMacros.is_immortal", return_value=False):
                await handler.char_update()

            self.assertEqual(0, active.status_flags.thirst)
            self.assertEqual(0, active.status_flags.hunger)
            self.assertEqual(
                [
                    ("active_char", "You are thirsty.\r\n"),
                    ("active_char", "You are hungry.\r\n"),
                ],
                [call.args for call in message_bus.send_to_character.await_args_list],
            )

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()

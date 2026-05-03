import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"

for package_name in ("area", "fight", "game", "interp", "mobile", "object", "player", "util"):
    if package_name not in sys.modules:
        package = types.ModuleType(package_name)
        package.__path__ = [str(SRC_ROOT / package_name)]
        sys.modules[package_name] = package

if "registries" not in sys.modules:
    registries = types.ModuleType("registries")

    class Registry:
        def __class_getitem__(cls, _item):
            return cls

    registries.Registry = Registry
    sys.modules["registries"] = registries

if "injector" not in sys.modules:
    injector = types.ModuleType("injector")

    def inject(target):
        return target

    injector.inject = inject
    sys.modules["injector"] = injector

if "server" not in sys.modules:
    server = types.ModuleType("server")
    server.__path__ = [str(SRC_ROOT / "server")]
    sys.modules["server"] = server

if "server.protocol" not in sys.modules:
    protocol = types.ModuleType("server.protocol")
    protocol.__path__ = []
    sys.modules["server.protocol"] = protocol

if "server.protocol.Message" not in sys.modules:
    message_mod = types.ModuleType("server.protocol.Message")

    class MessageType:
        GAME = "GAME"

    class Message:
        def __init__(self, type=None, data=None):
            self.type = type
            self.data = data or {}

    message_mod.Message = Message
    message_mod.MessageType = MessageType
    sys.modules["server.protocol.Message"] = message_mod

if "server.LoggerFactory" not in sys.modules:
    logger_factory = types.ModuleType("server.LoggerFactory")

    class _Logger:
        def info(self, *_args, **_kwargs):
            return None

        def debug(self, *_args, **_kwargs):
            return None

        def warning(self, *_args, **_kwargs):
            return None

        def error(self, *_args, **_kwargs):
            return None

    class LoggerFactory:
        @staticmethod
        def get_logger(_name):
            return _Logger()

    logger_factory.LoggerFactory = LoggerFactory
    sys.modules["server.LoggerFactory"] = logger_factory

from game.Equipped import Equipped
from interp.commands.ObjectCommands import ObjectCommands


class WearFlags:
    ITEM_WEAR_BODY = SimpleNamespace(value=1 << 0)


class TestObjectCommandsEquipment(unittest.TestCase):
    def _build_commands(self, room):
        room_registry = Mock()
        room_registry.get_or_none.return_value = room
        player_helper = Mock()
        player_helper.players_in_room.return_value = []
        commands = ObjectCommands(
            registry_service=SimpleNamespace(room_registry=room_registry),
            player_helper=player_helper,
        )
        commands.wear_flags = WearFlags
        commands.item_flags = SimpleNamespace()
        return commands

    @staticmethod
    def _build_character(item):
        character = SimpleNamespace(
            id="char1",
            name="Tester",
            level=1,
            room_id="room1",
            loot=[item],
            equipped=Equipped(),
        )
        character.ensure_equipped = lambda: character.equipped
        character.equip_item = lambda equipped_item, slot: Equipped.equip_item(character, equipped_item, slot)
        character.unequip_item = lambda slot: Equipped.unequip_item(character, slot)
        return character

    def test_wearing_armor_does_not_trigger_wield_weight_message(self):
        room = SimpleNamespace(player_targets=lambda _character: [])
        item = SimpleNamespace(
            id="vest1",
            name="vest",
            short_description="a vest",
            level=1,
            wear_flags=WearFlags.ITEM_WEAR_BODY.value,
            weight=999,
            weapon_too_heavy=lambda _character: False,
            is_two_handed_weapon=lambda: False,
        )
        character = self._build_character(item)

        with patch("interp.commands.ObjectCommands.EffectUtil.apply_item_effects"):
            payload = self._build_commands(room)._wear_item(character, item, room, replace=True)

        self.assertEqual("You wear a vest on your torso.\r\n", payload["to_char"])
        self.assertIs(character.equipped.torso, item)
        self.assertNotIn("too heavy for you to wield", payload["to_char"].lower())

    def test_remove_armor_by_name_stops_using_item(self):
        room = SimpleNamespace(player_targets=lambda _character: [])
        item = SimpleNamespace(
            id="vest1",
            name="vest",
            short_description="a vest",
            level=1,
            wear_flags=WearFlags.ITEM_WEAR_BODY.value,
            weight=1,
            weapon_too_heavy=lambda _character: False,
            is_two_handed_weapon=lambda: False,
        )
        character = self._build_character(item)
        commands = self._build_commands(room)
        context = SimpleNamespace(result="vest", parameters=[], finish=Mock())

        with patch("interp.commands.ObjectCommands.EffectUtil.apply_item_effects"), \
             patch("interp.commands.ObjectCommands.EffectUtil.remove_item_effects"):
            commands._wear_item(character, item, room, replace=True)
            payload = commands.do_remove(character, context)

        self.assertEqual("You stop using a vest.\r\n", payload["to_char"])
        self.assertIsNone(character.equipped.torso)
        self.assertIn(item, character.loot)

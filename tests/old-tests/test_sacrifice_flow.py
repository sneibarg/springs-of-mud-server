import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"

for package_name in ("area", "fight", "game", "interp", "mobile", "item", "player", "util"):
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
    server.__path__ = []
    sys.modules["server"] = server

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

if "server.messaging" not in sys.modules:
    messaging = types.ModuleType("server.messaging")
    messaging.__path__ = []
    sys.modules["server.messaging"] = messaging

if "server.messaging.MessageBus" not in sys.modules:
    message_bus = types.ModuleType("server.messaging.MessageBus")

    class MessageBus:
        pass

    message_bus.MessageBus = MessageBus
    sys.modules["server.messaging.MessageBus"] = message_bus

from fight.FightHandler import FightHandler
from interp.commands.ObjectCommands import ObjectCommands


class TestRoom:
    def __init__(self, room_id="room1"):
        self.id = room_id
        self.contents = {}
        self.characters = {}
        self.mobiles = {}

    def add_item_to_room(self, item):
        self.contents[item.id] = item

    def remove_item_from_room(self, item):
        self.contents.pop(item.id, None)


class TestSacrificeFlow(unittest.TestCase):
    @staticmethod
    def _wear_flags():
        return SimpleNamespace(ITEM_TAKE=SimpleNamespace(value=1))

    @staticmethod
    def _item_flags():
        return SimpleNamespace(ITEM_NO_SAC=SimpleNamespace(value=1 << 15))

    def _build_object_commands(self, room):
        room_registry = Mock()
        room_registry.get_or_none.return_value = room
        player_helper = Mock()
        player_helper.players_in_room.return_value = []
        commands = ObjectCommands(
            registry_service=SimpleNamespace(room_registry=room_registry),
            player_helper=player_helper,
        )
        commands.wear_flags = self._wear_flags()
        commands.item_flags = self._item_flags()
        return commands

    def _build_fight_handler(self):
        return FightHandler(
            message_bus=Mock(),
            combat_registry=Mock(),
            area_registry=Mock(),
            room_registry=Mock(),
            room_helper=Mock(),
            item_registry=Mock(),
            mobile_registry=Mock(),
        )

    def test_manual_sacrifice_uses_room_corpse_rules_and_scaled_reward(self):
        room = TestRoom("room1")
        corpse = SimpleNamespace(
            id="corpse1",
            name="corpse monster",
            short_description="the corpse of the monster",
            item_type="ITEM_CORPSE_NPC",
            contains=[],
            wear_flags=1,
            extra_flags=0,
            level=5,
            cost=0,
        )
        room.add_item_to_room(corpse)
        character = SimpleNamespace(name="Tester", room_id="room1", silver=0)
        context = SimpleNamespace(result="corpse", parameters=[], finish=Mock())

        payload = self._build_object_commands(room).do_sacrifice(character, context)

        self.assertEqual(15, character.silver)
        self.assertNotIn("corpse1", room.contents)
        self.assertEqual("Mota gives you 15 silver coins for your sacrifice.\r\n", payload["to_char"])
        self.assertIn("Tester sacrifices the corpse of the monster to Mota.\r\n", payload["to_room"])

    def test_manual_sacrifice_rejects_nonempty_player_corpse(self):
        room = TestRoom("room1")
        corpse = SimpleNamespace(
            id="corpse1",
            name="corpse tester",
            short_description="the corpse of Tester",
            item_type="ITEM_CORPSE_PC",
            contains=[SimpleNamespace(id="coin1")],
            wear_flags=1,
            extra_flags=0,
            level=10,
            cost=0,
        )
        room.add_item_to_room(corpse)
        character = SimpleNamespace(name="Tester", room_id="room1", silver=0)
        context = SimpleNamespace(result="corpse", parameters=[], finish=Mock())

        payload = self._build_object_commands(room).do_sacrifice(character, context)

        self.assertEqual("Mota wouldn't like that.\r\n", payload["to_char"])
        self.assertIn("corpse1", room.contents)
        self.assertEqual(0, character.silver)

    def test_autoloot_then_autosac_loots_takeable_items_and_uses_corpse_value(self):
        handler = self._build_fight_handler()
        room = TestRoom("room1")
        attacker = SimpleNamespace(id="char1", name="Tester", silver=0, loot=[])
        victim = SimpleNamespace(id="mob1", name="monster", short_description="the monster")
        room.characters = {"char1": attacker}
        room.mobiles = {"mob1": victim}

        loot = SimpleNamespace(id="loot1", name="dagger", short_description="a dagger", wear_flags=1)
        corpse = SimpleNamespace(
            id="corpse1",
            name="corpse monster",
            short_description="the corpse of the monster",
            item_type="ITEM_CORPSE_NPC",
            contains=[loot],
            wear_flags=1,
            extra_flags=0,
            level=5,
            cost=0,
        )
        room.add_item_to_room(corpse)

        def enum_lookup(name):
            if name == "wearFlags":
                return self._wear_flags()
            if name == "itemFlags":
                return self._item_flags()
            return SimpleNamespace()

        with patch("fight.FightHandler.CharacterMacros.is_npc", side_effect=lambda entity: entity is victim), \
             patch.object(handler, "_player_act_enabled", side_effect=lambda _character, flag: flag in {"PLR_AUTOLOOT", "PLR_AUTOSAC"}), \
             patch("fight.FightHandler.CharacterMacros.get_enum", side_effect=enum_lookup):
            payload = handler.build_round_payload(
                attacker,
                victim,
                room,
                {"to_char": "You hit the monster.\r\n", "to_room": "", "killed": True, "xp_gain": 0},
            )

        self.assertIn(loot, attacker.loot)
        self.assertNotIn("corpse1", room.contents)
        self.assertEqual(15, attacker.silver)
        self.assertIn("Mota gives you 15 silver coins for your sacrifice.\r\n", payload["to_char"])
        self.assertIn("Tester sacrifices the corpse of the monster to Mota.\r\n", payload["to_room"])

    def test_autosac_leaves_corpse_when_autoloot_cannot_empty_it(self):
        handler = self._build_fight_handler()
        room = TestRoom("room1")
        attacker = SimpleNamespace(id="char1", name="Tester", silver=0, loot=[])
        victim = SimpleNamespace(id="mob1", name="monster", short_description="the monster")
        room.characters = {"char1": attacker}
        room.mobiles = {"mob1": victim}

        stuck_loot = SimpleNamespace(id="loot1", name="altar", short_description="an altar", wear_flags=0)
        corpse = SimpleNamespace(
            id="corpse1",
            name="corpse monster",
            short_description="the corpse of the monster",
            item_type="ITEM_CORPSE_NPC",
            contains=[stuck_loot],
            wear_flags=1,
            extra_flags=0,
            level=5,
            cost=0,
        )
        room.add_item_to_room(corpse)

        def enum_lookup(name):
            if name == "wearFlags":
                return self._wear_flags()
            if name == "itemFlags":
                return self._item_flags()
            return SimpleNamespace()

        with patch("fight.FightHandler.CharacterMacros.is_npc", side_effect=lambda entity: entity is victim), \
             patch.object(handler, "_player_act_enabled", side_effect=lambda _character, flag: flag in {"PLR_AUTOLOOT", "PLR_AUTOSAC"}), \
             patch("fight.FightHandler.CharacterMacros.get_enum", side_effect=enum_lookup):
            payload = handler.build_round_payload(
                attacker,
                victim,
                room,
                {"to_char": "You hit the monster.\r\n", "to_room": "", "killed": True, "xp_gain": 0},
            )

        self.assertEqual([], attacker.loot)
        self.assertIn("corpse1", room.contents)
        self.assertEqual([stuck_loot], corpse.contains)
        self.assertEqual(0, attacker.silver)
        self.assertNotIn("Mota gives you", payload["to_char"])

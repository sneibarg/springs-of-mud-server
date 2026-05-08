import sys
import types
import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _stub_package(name: str):
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [str(SRC / name)]
    sys.modules[name] = module
    return module


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def _load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, SRC / relative_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class _Logger:
    def info(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None

    def warn(self, *_args, **_kwargs):
        return None


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


class _CharacterMacros:
    @staticmethod
    def get_enum(_name):
        return SimpleNamespace(
            POS_DEAD=SimpleNamespace(value=0),
            POS_MORTAL=SimpleNamespace(value=1),
            POS_INCAP=SimpleNamespace(value=2),
            POS_STUNNED=SimpleNamespace(value=3),
            POS_STANDING=SimpleNamespace(value=8),
        )

    @classmethod
    def pos_value(cls, name: str) -> int:
        positions = cls.get_enum("positions")
        return int(getattr(positions, name).value) if hasattr(positions, name) else -1

    @staticmethod
    def position_value(character) -> int:
        attrs = getattr(character, "character_attributes", None)
        if attrs is not None and getattr(attrs, "position", None) is not None:
            return int(attrs.position)
        return int(getattr(character, "position", 8))


def _noop(*_args, **_kwargs):
    return None


_stub_module("injector", inject=lambda target: target)
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_stub_module("util.InfoUtil", InfoUtil=SimpleNamespace(target_condition_line=_noop))
_stub_module("util.InterpUtil", InterpUtil=SimpleNamespace())
_stub_module("util.ItemUtil", ItemUtil=SimpleNamespace())
_stub_module("util.PlayerUtil", PlayerUtil=SimpleNamespace(visible=lambda *_args, **_kwargs: []))
_stub_module("util.SkillUtil", SkillUtil=SimpleNamespace())
_stub_package("game")
_load_module("game.GamePayload", "game/GamePayload.py")
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("game.WeatherHandler", WeatherHandler=object)
_stub_package("area")
_stub_module("area.RoomRegistry", RoomRegistry=object)
_stub_package("player")
_stub_module("player.Character", Character=object)
_stub_module("player.CharacterMacros", CharacterMacros=_CharacterMacros)
_stub_package("server.session")
_stub_module("server.session.SessionHandler", SessionHandler=object)
_stub_package("interp")
_load_module("interp.HelpEntry", "interp/HelpEntry.py")
_stub_module("interp.Context", Context=object)
Command = _load_module("interp.Command", "interp/Command.py").Command
_load_module("interp.InterpView", "interp/InterpView.py")
_load_module("interp.InterpCheck", "interp/InterpCheck.py")
_load_module("interp.InterpActionDefinition", "interp/InterpActionDefinition.py")
_load_module("interp.InterpPlan", "interp/InterpPlan.py")
_load_module("interp.InterpApi", "interp/InterpApi.py")
InfoCommands = _load_module("interp.commands.Info", "interp/commands/Info.py").InfoCommands


class TestQuitCommandChecks(unittest.TestCase):
    def _build_commands(self):
        room_registry = Mock()
        room_registry.get_or_none.return_value = SimpleNamespace()
        registry_service = SimpleNamespace(
            interp_registry=Mock(),
            room_registry=room_registry,
            skill_registry=Mock(),
            spell_registry=Mock(),
        )
        return InfoCommands(registry_service, Mock(), Mock())

    @staticmethod
    def _quit_command():
        return Command.from_json(
            {
                "_id": {"$oid": "cmd-quit"},
                "name": "quit",
                "shortcuts": "qui",
                "role": "player",
                "lambdas": ["lambda ctx: ctx.player_handler().do_quit(ctx.character, ctx)"],
                "enabled": True,
                "position": "POS_DEAD",
                "level": 0,
                "log": "LOG_NORMAL",
                "pipeline": False,
                "maxArguments": 0,
                "checks": [
                    {
                        "predicate": "lambda v: v.context.current_fighting is not None",
                        "messageKey": "fighting",
                    },
                    {
                        "predicate": "lambda v: v.context.position < CharacterMacros.pos_value('POS_STUNNED')",
                        "messageKey": "stunned",
                    },
                ],
                "payload": {
                    "toChar": {
                        "fighting": "No way! You are fighting.",
                        "stunned": "You're not DEAD yet.",
                        "default": "Alas, all good things must come to an end.",
                    },
                    "toRoom": {
                        "default": "%c has left the game.",
                    },
                    "toVictim": {},
                },
                "function": [],
                "usage": "",
            }
        )

    def test_quit_blocks_while_fighting(self):
        commands = self._build_commands()
        fighting = object()
        character = SimpleNamespace(name="Tester", room_id="room-1", fighting=fighting, position=8)
        context = SimpleNamespace(command=self._quit_command(), room=SimpleNamespace(), finish=Mock(), character=character, current_fighting=fighting, position=8)

        payload = commands.do_quit(context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("No way! You are fighting.\r\n", payload["to_char"])
        context.finish.assert_called_once()

    def test_quit_uses_default_payload_when_allowed(self):
        commands = self._build_commands()
        character = SimpleNamespace(name="Tester", room_id="room-1", fighting=None, position=8)
        context = SimpleNamespace(command=self._quit_command(), room=SimpleNamespace(), finish=Mock(), character=character, current_fighting=None, position=8)

        payload = commands.do_quit(context)

        self.assertFalse(payload["blocked"])
        self.assertEqual("Alas, all good things must come to an end.\r\n", payload["to_char"])
        self.assertEqual("Tester has left the game.\r\n", payload["to_room"])
        context.finish.assert_called_once()


if __name__ == "__main__":
    unittest.main()

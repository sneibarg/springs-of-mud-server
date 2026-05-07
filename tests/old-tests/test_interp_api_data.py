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
        return int(getattr(character, "position", 8))


_stub_module("injector", inject=lambda target: target)
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_stub_package("game")
_load_module("game.GamePayload", "game/GamePayload.py")
_stub_package("area")
_stub_module("area.RoomRegistry", RoomRegistry=object)
_stub_package("player")
_stub_module("player.CharacterMacros", CharacterMacros=_CharacterMacros)
_stub_package("interp")
_load_module("interp.HelpEntry", "interp/HelpEntry.py")
_stub_module("interp.Context", Context=object)
_load_module("interp.Command", "interp/Command.py")
_load_module("interp.InterpView", "interp/InterpView.py")
_load_module("interp.InterpCheck", "interp/InterpCheck.py")
_load_module("interp.InterpActionDefinition", "interp/InterpActionDefinition.py")
_load_module("interp.InterpPlan", "interp/InterpPlan.py")

Command = sys.modules["interp.Command"].Command
InterpApi = _load_module("interp.InterpApi", "interp/InterpApi.py").InterpApi


class TestInterpApiData(unittest.TestCase):
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
                    }
                ],
                "payload": {
                    "toChar": {
                        "fighting": "No way! You are fighting.",
                        "default": "Alas, all good things must come to an end.",
                    },
                    "toRoom": {
                        "default": "%c has left the game.",
                    },
                },
                "function": [],
                "usage": "",
            }
        )

    def test_quit_check_stops_with_payload_message(self):
        api = InterpApi()
        fighting = object()
        character = SimpleNamespace(name="Tester", room_id="room-1", fighting=fighting, position=8)
        context = SimpleNamespace(
            command=self._quit_command(),
            room=SimpleNamespace(),
            result="",
            parameters=[],
            finish=Mock(),
            character=character,
            current_fighting=fighting,
            position=8,
        )

        payload = api.run_action(context, "quit")

        self.assertTrue(payload["blocked"])
        self.assertEqual("No way! You are fighting.\r\n", payload["to_char"])
        context.finish.assert_called_once()

    def test_quit_executor_renders_default_messages(self):
        character = SimpleNamespace(name="Tester", room_id="room-1", fighting=None, position=8)
        api = InterpApi()
        context = SimpleNamespace(
            command=self._quit_command(),
            room=SimpleNamespace(),
            result="",
            parameters=[],
            finish=Mock(),
            character=character,
            current_fighting=None,
            position=8,
        )

        payload = api.run_action(context, "quit")

        self.assertFalse(payload["blocked"])
        self.assertEqual("Alas, all good things must come to an end.\r\n", payload["to_char"])
        self.assertEqual("Tester has left the game.\r\n", payload["to_room"])
        context.finish.assert_called_once()


if __name__ == "__main__":
    unittest.main()

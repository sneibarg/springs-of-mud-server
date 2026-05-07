import unittest
import sys
import types
import importlib.util
from pathlib import Path

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


_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_stub_package("game")
_load_module("game.GamePayload", "game/GamePayload.py")
_stub_package("interp")
_load_module("interp.HelpEntry", "interp/HelpEntry.py")

GamePayload = sys.modules["game.GamePayload"].GamePayload
Command = _load_module("interp.Command", "interp/Command.py").Command


class TestCommandData(unittest.TestCase):
    def test_command_from_json_normalizes_payload_and_checks(self):
        command = Command.from_json(
            {
                "_id": {"$oid": "cmd-1"},
                "name": "practice",
                "shortcuts": "pr",
                "role": "player",
                "position": "POS_SLEEPING",
                "enabled": True,
                "lambdas": ["lambda ctx: ctx.player_handler().do_practice(ctx.character, ctx)"],
                "function": [],
                "usage": "",
                "level": 0,
                "maxArguments": 0,
                "payload": {"toChar": {"noPractice": "You have no practice sessions left."}},
                "checks": [
                    {
                        "predicate": "lambda v: not v.argument",
                        "messageKey": "noPractice",
                        "tokenFactory": "lambda v: {'count': 0}",
                    }
                ],
            }
        )

        self.assertIsInstance(command.payload, GamePayload)
        self.assertEqual("You have no practice sessions left.", command.payload.to_char["no_practice"])
        self.assertEqual("no_practice", command.checks[0]["message_key"])
        self.assertEqual("lambda v: {'count': 0}", command.checks[0]["token_factory"])


if __name__ == "__main__":
    unittest.main()

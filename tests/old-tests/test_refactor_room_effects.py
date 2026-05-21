import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"

for package_name in ("area", "game", "interp", "item", "player"):
    if package_name not in sys.modules:
        package = types.ModuleType(package_name)
        package.__path__ = [str(SRC_ROOT / package_name)]
        sys.modules[package_name] = package

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

from area.Room import Room
from item.Effect import Effect
from util.EffectUtil import EffectUtil


class TestRefactorRoomEffects(unittest.TestCase):
    def test_room_owns_exit_and_door_lookup(self):
        north_exit = SimpleNamespace(direction=0, to_room_id="room-2", keyword="oak door")
        east_exit = SimpleNamespace(direction=1, to_room_id="room-3", keyword="gate")
        room = Room(id="room-1", exits=[north_exit, east_exit])

        self.assertIs(north_exit, room.get_exit(0))
        self.assertEqual("room-2", room.destination_id_for_direction("north"))
        self.assertEqual(0, room.find_door("north"))
        self.assertEqual(0, room.find_door("oak"))
        self.assertEqual(-1, room.find_door("south"))

    def test_effect_eval_supports_numeric_expressions_and_rejects_code_execution(self):
        self.assertEqual(2, EffectUtil._eval_expr("1 + (level >= 18) + (level >= 25)", level=20))
        self.assertEqual(2, EffectUtil._eval_expr("level / 8", level=20))
        self.assertEqual(7, EffectUtil._eval_expr("__import__('os').system('echo hacked')", level=20, default=7))

if __name__ == "__main__":
    unittest.main()

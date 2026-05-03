import unittest
import sys
import types

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

from game.StatusFlags import StatusFlags


class TestStatusFlagsDeserialization(unittest.TestCase):
    def test_from_json_ignores_internal_and_unknown_fields(self):
        flags = StatusFlags.from_json({
            "act": 5,
            "_bitfield_write_enabled": True,
            "_initialized": True,
            "nonexistent_field": 99,
        })

        self.assertEqual(5, flags.act)
        self.assertFalse(getattr(flags, "_bitfield_write_enabled"))
        self.assertTrue(getattr(flags, "_initialized"))

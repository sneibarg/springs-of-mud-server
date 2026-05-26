import importlib.util
import os
import sys
import types
import unittest
from unittest.mock import patch

server_package = types.ModuleType("server")
logger_factory_module = types.ModuleType("server.LoggerFactory")


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return None


logger_factory_module.LoggerFactory = _LoggerFactory
sys.modules["server"] = server_package
sys.modules["server.LoggerFactory"] = logger_factory_module

MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "game", "RandomNumberGenerator.py")
SPEC = importlib.util.spec_from_file_location("test_random_number_generator_module", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
RandomNumberGenerator = MODULE.RandomNumberGenerator


class TestRandomNumberGenerator(unittest.TestCase):
    @patch.object(RandomNumberGenerator, "number_mm", return_value=0b101101)
    def test_number_bits_masks_number_mm(self, mock_number_mm):
        self.assertEqual(0b101, RandomNumberGenerator.number_bits(3))
        mock_number_mm.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

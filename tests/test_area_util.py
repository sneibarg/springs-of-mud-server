import os
import sys
import types
import unittest
from types import SimpleNamespace


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

api_pkg = types.ModuleType("api")
api_pkg.__path__ = [os.path.join(SRC, "api")]
sys.modules.setdefault("api", api_pkg)
sys.modules.setdefault("api.CharacterApi", types.ModuleType("api.CharacterApi"))
sys.modules["api.CharacterApi"].CharacterApi = SimpleNamespace()

from util.AreaUtil import AreaUtil


class TestAreaUtilDoorResets(unittest.TestCase):
    def test_door_reset_locks_closed_exit_without_isdoor_bit(self):
        exit_flags = SimpleNamespace(
            EX_ISDOOR=SimpleNamespace(value=1),
            EX_CLOSED=SimpleNamespace(value=2),
            EX_LOCKED=SimpleNamespace(value=4),
        )
        exit_obj = SimpleNamespace(exit_flags=2)

        AreaUtil.apply_door_reset(exit_obj, 2, exit_flags)

        self.assertEqual(6, exit_obj.exit_flags)


if __name__ == "__main__":
    unittest.main()

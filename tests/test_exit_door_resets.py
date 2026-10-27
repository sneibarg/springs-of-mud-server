import unittest
from types import SimpleNamespace

from tests import test_runtime_factories as runtime
from area.Exit import Exit


class TestExitDoorResets(unittest.TestCase):
    def test_door_reset_locks_closed_exit_without_isdoor_bit(self):
        flags = SimpleNamespace(EX_ISDOOR=SimpleNamespace(value=1),
                                EX_CLOSED=SimpleNamespace(value=2),
                                EX_LOCKED=SimpleNamespace(value=4))
        exit_obj = Exit(0, '', '', 2, 0, 0, '', '')
        exit_obj.apply_door_reset(2, flags)
        self.assertEqual(6, exit_obj.exit_flags)


if __name__ == '__main__':
    unittest.main()

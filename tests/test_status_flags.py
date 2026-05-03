import unittest

from game.StatusFlags import BitField, StatusFlags


class TestStatusFlags(unittest.TestCase):
    def test_bitfield_members_are_coerced_on_init(self):
        flags = StatusFlags(
            act=1,
            comm=2,
            affected_by=4,
            off=8,
            imm=16,
            res=32,
            vuln=64,
            form=128,
            parts=256,
            invis_level=0,
            incog_level=0,
            played=0,
            logon=0,
            pulse_wait=0,
            pulse_daze=0,
        )

        self.assertIsInstance(flags.act, BitField)
        self.assertIsInstance(flags.parts, BitField)

    def test_assign_bitfield_coerces_plain_integer(self):
        flags = StatusFlags.default()

        flags.assign_bitfield("act", 3)

        self.assertEqual(3, flags.act)
        self.assertIsInstance(flags.act, BitField)

    def test_set_and_unset_flag_preserve_bitfield_type(self):
        flags = StatusFlags.default()

        flags.set_flag("comm", 2)
        flags.set_flag("comm", 4)
        flags.unset_flag("comm", 2)

        self.assertEqual(4, flags.comm)
        self.assertIsInstance(flags.comm, BitField)

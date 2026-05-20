import unittest

from game.StatusFlags import BitField, StatusFlags


class TestStatusFlags(unittest.TestCase):
    def test_bitfield_members_are_stored_as_plain_integers(self):
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
            hunger=48,
            thirst=48,
            drunk=0,
            invis_level=0,
            incog_level=0,
            played=0,
            logon=0,
            pulse_wait=0,
            pulse_daze=0,
        )

        self.assertEqual(1, flags.act)
        self.assertEqual(256, flags.parts)
        self.assertIsInstance(flags.act, int)
        self.assertIsInstance(flags.parts, int)

    def test_assign_bitfield_keeps_plain_integer_storage(self):
        flags = StatusFlags.default()

        flags.assign_bitfield("act", 3)

        self.assertEqual(3, flags.act)
        self.assertIsInstance(flags.act, int)

    def test_set_and_unset_flag_preserve_plain_integer_storage(self):
        flags = StatusFlags.default()

        flags.set_flag("comm", 2)
        flags.set_flag("comm", 4)
        flags.unset_flag("comm", 2)

        self.assertEqual(4, flags.comm)
        self.assertIsInstance(flags.comm, int)

    def test_default_initializes_condition_fields(self):
        flags = StatusFlags.default()

        self.assertEqual(48, flags.hunger)
        self.assertEqual(48, flags.thirst)
        self.assertEqual(0, flags.drunk)

    def test_bitfield_members_reject_direct_assignment_after_init(self):
        flags = StatusFlags.default()

        with self.assertRaises(AttributeError):
            flags.act = 7

    def test_bitfield_utility_methods_operate_on_integers(self):
        self.assertEqual(5, BitField.set_bit(1, 4))
        self.assertEqual(1, BitField.unset_bit(5, 4))

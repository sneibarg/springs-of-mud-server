"""Donation pit trust gates and temporary versus original object timers."""
import sys
import unittest
from unittest.mock import patch
from tests import test_object_bulk_put_parity as bulk

h = bulk.h


class TestObjectDonationPitParity(unittest.TestCase):
    def setUp(self):
        self.base = bulk.TestObjectBulkPutParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.commands, self.room, self.actor = self.base.commands, self.base.room, self.base.actor
        self.pit = self.base.bag
        self.pit.vnum = str(self.base.enums["wellKnownObjectVnums"].OBJ_VNUM_PIT.value)
        self.pit.wear_flags = "0"
        self.had_timer = self.base.enums["itemFlags"].ITEM_HAD_TIMER.value
        self.magic = self.base.enums["itemFlags"].ITEM_MAGIC.value
        self.base.base.swap(sys.modules[h.Object.__module__].CharacterApi, "get_trust", create=True,
                            side_effect=lambda actor: getattr(actor, "trust", 0) or actor.level)
        self.roll = self.base.base.swap(bulk.container_tests.consumption.RNG, "number_range", return_value=143)
        self.actor.level = 10

    def item(self, **kw):
        return self.base.item("gem", vnum=99000, level=10, **kw)

    def put(self, item):
        self.actor.loot.append(item)
        return self.base.put("gem bag")

    def get(self, item, command="get"):
        context = self.base.fixture._build_context("gem bag", self.room, self.actor, command)
        return self.commands.do_get(self.actor, context)

    def test_single_put_assigns_temporary_timer_and_pickup_removes_it(self):
        item = self.item(timer=0, extra_flags=str(self.magic))
        self.put(item)
        self.assertEqual(143, item.timer)
        self.assertEqual(self.magic, int(item.extra_flags))
        self.roll.assert_called_once_with(100, 200)
        item.timer = 105  # countdown while it remains donated
        payload = self.get(item)
        self.assertEqual(0, item.timer)
        self.assertEqual(self.magic, int(item.extra_flags))
        self.assertIn(item, self.actor.loot)
        self.assertEqual([], self.pit.contains)
        self.assertIn("You get gem from bag", payload["to_char"])

    def test_original_timer_retains_remaining_time_and_clears_marker(self):
        item = self.item(timer=17, extra_flags=str(self.magic))
        self.put(item)
        self.assertEqual(17, item.timer)
        self.assertEqual(self.magic | self.had_timer, int(item.extra_flags))
        self.roll.assert_not_called()
        item.timer = 11
        self.get(item, "take")
        self.assertEqual(11, item.timer)
        self.assertEqual(self.magic, int(item.extra_flags))

    def test_trust_gate_preserves_object_and_timer_for_get_and_take(self):
        item = self.item(timer=17, extra_flags=str(self.had_timer | self.magic))
        self.pit.contains.append(item)
        self.actor.level = 9
        for command in ("get", "take"):
            payload = self.get(item, command)
            self.assertEqual("You are not powerful enough to use it.\r\n", payload["to_char"])
            self.assertEqual([item], self.pit.contains)
            self.assertEqual([], self.actor.loot)
            self.assertEqual((17, self.had_timer | self.magic), (item.timer, int(item.extra_flags)))
            self.assertNotIn("to_room", payload)
        self.actor.trust = 10
        self.get(item)
        self.assertIn(item, self.actor.loot)

    def test_portable_pit_still_checks_trust_but_preserves_timer(self):
        self.pit.wear_flags = "1"
        item = self.item(timer=17)
        self.put(item)
        self.roll.assert_not_called()
        self.assertFalse(int(item.extra_flags) & self.had_timer)
        self.actor.level = 9
        self.assertIn("not powerful", self.get(item)["to_char"])
        self.actor.level = 10
        self.get(item)
        self.assertEqual(17, item.timer)

    def test_normal_container_does_not_change_timer_but_pickup_clears_marker(self):
        self.pit.vnum = "99999"
        item = self.item(timer=17, extra_flags=str(self.magic | self.had_timer))
        self.put(item)
        self.actor.level = 1
        self.get(item)
        self.assertEqual((17, self.magic), (item.timer, int(item.extra_flags)))
        self.assertIn(item, self.actor.loot)
        self.roll.assert_not_called()

    def test_failed_put_does_not_assign_timer_or_marker(self):
        item = self.item(timer=0, weight=1000)
        self.put(item)
        self.assertIn(item, self.actor.loot)
        self.assertEqual(0, item.timer)
        self.roll.assert_not_called()

    def test_capacity_denial_precedes_pit_level_and_timer_changes(self):
        item = self.item(item_type="weapon", timer=17, extra_flags=str(self.had_timer))
        self.pit.contains.append(item)
        self.actor.level = 1
        self.actor.max_items = lambda: 1
        self.actor.carry_count = lambda: 1
        payload = self.get(item)
        self.assertIn("can't carry that many", payload["to_char"])
        self.assertEqual((17, self.had_timer), (item.timer, int(item.extra_flags)))
        self.assertEqual([item], self.pit.contains)

    def test_bulk_put_does_not_apply_single_put_timer_rule(self):
        item = self.item(timer=0, wear_flags="1")
        self.actor.loot.append(item)
        self.base.put("all bag")
        self.assertIn(item, self.pit.contains)
        self.assertEqual(0, item.timer)
        self.roll.assert_not_called()

    def test_bulk_get_immortal_still_respects_trust_for_each_item(self):
        low = self.item(timer=143)
        high = self.base.item("relic", vnum=99001, level=11, timer=17, extra_flags=str(self.had_timer))
        self.pit.contains.extend([low, high])
        self.actor.is_immortal = True
        payload = self.commands.do_get(self.actor, self.base.fixture._build_context("all bag", self.room, self.actor))
        self.assertIn(low, self.actor.loot)
        self.assertEqual(0, low.timer)
        self.assertEqual([high], self.pit.contains)
        self.assertEqual((17, self.had_timer), (high.timer, int(high.extra_flags)))
        self.assertIn("not powerful", payload["to_char"])


if __name__ == "__main__":
    unittest.main()

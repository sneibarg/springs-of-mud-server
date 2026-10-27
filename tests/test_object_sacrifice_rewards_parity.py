"""ROM24 sacrifice reward floor, cost cap, corpse aliases, and autosplit."""
import unittest
from tests import test_object_currency_parity as currency

RealItemApi = currency.RealItemApi
h = currency.h


class TestSacrificeRewardsParity(unittest.TestCase):
    def setUp(self):
        self.base = currency.TestObjectCurrencyParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands

    def item(self, **kwargs):
        return self.base.base.item("offering", **kwargs)

    def sacrifice(self, item):
        self.room.contents[item.id] = item
        return self.commands.do_sacrifice(self.actor, self.base.context("sacrifice", "offering"))

    def test_noncorpse_rewards_are_capped_by_cost_without_post_cap_floor(self):
        for level, cost, expected in [(10, 0, 0), (10, 1, 1), (10, 2, 2), (10, 100, 30),
                                      (0, 100, 1), (0, 0, 0), (1, 100, 3)]:
            with self.subTest(level=level, cost=cost):
                self.assertEqual(expected, RealItemApi.sacrifice_silver_value(self.item(level=level, cost=cost)))

    def test_all_supported_corpse_aliases_are_exempt_from_cost_cap(self):
        for kind in ("pc_corpse", "corpse_pc", "ITEM_CORPSE_PC", "npc_corpse", "corpse_npc", "ITEM_CORPSE_NPC"):
            with self.subTest(kind=kind):
                item = self.item(item_type=kind, level=10, cost=0)
                self.assertTrue(h.Item.is_corpse(item))
                self.assertEqual(30, RealItemApi.sacrifice_silver_value(item))
                item.level = 0
                self.assertEqual(1, RealItemApi.sacrifice_silver_value(item))

    def test_string_level_is_multiplied_numerically(self):
        self.assertEqual(6, RealItemApi.sacrifice_silver_value(self.item(level="2", cost="100")))

    def test_zero_and_one_silver_rewards_render_messages_without_autosplit(self):
        ally = self.base.member()
        for cost, text in [(0, "Mota gives you 0 silver coins"), (1, "Mota gives you one silver coin")]:
            with self.subTest(cost=cost):
                before = self.actor.silver
                item = self.item(level=10, cost=cost)
                payload = self.sacrifice(item)
                self.assertEqual(before + cost, self.actor.silver)
                self.assertEqual(0, ally.silver)
                self.assertNotIn("payloads", payload)
                self.assertIn(text, payload["to_char"])
                self.assertNotIn(item.id, self.room.contents)

    def test_two_silver_reward_autosplits_at_the_existing_threshold(self):
        ally = self.base.member()
        before = self.actor.silver
        payload = self.sacrifice(self.item(level=10, cost=2))
        self.assertEqual(before + 1, self.actor.silver)
        self.assertEqual(1, ally.silver)
        self.assertIn("2 silver coins", payload["payloads"][0]["to_char"])

    def test_empty_pc_and_npc_corpses_receive_uncapped_rewards(self):
        for kind in ("pc_corpse", "corpse_npc"):
            with self.subTest(kind=kind):
                before = self.actor.silver
                self.sacrifice(self.item(item_type=kind, level=10, cost=0, contains=[]))
                self.assertEqual(before + 30, self.actor.silver)


if __name__ == "__main__":
    unittest.main()

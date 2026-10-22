"""ROM24 transaction haggle rolls, rounding, caps, guards, and learning."""
import sys
import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch
from tests import test_object_container_shop_spell_parity as fixtures

h = fixtures.h
ObjectModule = sys.modules[h.Object.__module__]


class TestObjectHaggleParity(unittest.TestCase):
    def setUp(self):
        self.base = fixtures.TestObjectContainerShopSpellParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.shop = self.base.fixture._build_shop()
        self.shop.buy_type0 = self.base.enums["itemTypes"].ITEM_WEAPON.value
        self.shop.buy_type1 = self.base.enums["itemTypes"].ITEM_TRASH.value
        self.keeper = NS(id="keeper", vnum="100", inventory=[], short_description="the shopkeeper", gold=100, silver=0)
        self.room.mobiles = {self.keeper.id: self.keeper}
        self.commands._find_keeper = Mock(return_value=(self.keeper, self.shop, ""))
        self.actor.level = 20
        self.actor.gold, self.actor.silver = 100, 0
        self.actor.skill_level = lambda name: 80
        self.actor.character_class = NS(name="thief")
        self.skill = NS(id="haggle-id", level_by_class={"thief": 1})
        self.commands.skill_registry = NS(get_or_none=lambda **kw: self.skill if kw.get("name") == "haggle" else None)
        self.roll = self.base.swap(fixtures.consumption.RNG, "number_percent", return_value=50)
        self.improve = self.base.swap(ObjectModule.Ability, "check_improve")

    def item(self, name="sword", **kw):
        kw.setdefault("item_type", "weapon")
        kw.setdefault("cost", 101)
        kw.setdefault("timer", 0)
        return self.base.item(name, **kw)

    def command(self, name, raw):
        context = self.base.fixture._build_context(raw, self.room, self.actor, name)
        payload = getattr(self.commands, "do_" + name)(self.actor, context)
        self.assertTrue(context.done)
        return payload, context

    def wealth(self, actor):
        return actor.gold * 100 + actor.silver

    def test_single_buy_uses_base_cost_rounding_and_updates_item_and_balances(self):
        item = self.item()
        self.keeper.inventory = [item]
        before = self.wealth(self.keeper)
        payload, ctx = self.command("buy", "sword")
        self.assertEqual((96, 96), (ctx.buy_cost, ctx.buy_total_cost))  # 121 - (101/2)*50/100
        self.assertEqual(9904, self.wealth(self.actor))
        self.assertEqual(before + 96, self.wealth(self.keeper))
        self.assertEqual(96, item.cost)
        self.assertIn(item, self.actor.loot)
        self.assertEqual("You haggle with the shopkeeper.\r\nYou buy sword for 96 silver.\r\n", payload["to_char"])
        self.assertEqual("Tester buys sword.\r\n", payload["to_room"])
        self.roll.assert_called_once_with()
        self.improve.assert_called_once_with(self.actor, "haggle-id", True, 4)

    def test_quantity_buy_rolls_once_and_multiplies_discounted_unit_price(self):
        first, second = self.item(), self.item()
        first.id, second.id = "first", "second"
        self.keeper.inventory = [first, second]
        payload, ctx = self.command("buy", "2*sword")
        self.assertEqual(192, ctx.buy_total_cost)
        self.assertEqual(9808, self.wealth(self.actor))
        self.assertEqual([first, second], self.actor.loot)
        self.assertEqual((96, 96), (first.cost, second.cost))
        self.assertIn("[2] for 192 silver", payload["to_char"])
        self.roll.assert_called_once_with()
        self.improve.assert_called_once()

    def test_roll_equal_to_skill_fails_without_learning(self):
        self.actor.skill_level = lambda name: 50
        self.keeper.inventory = [self.item()]
        payload, ctx = self.command("buy", "sword")
        self.assertEqual(121, ctx.buy_cost)
        self.assertNotIn("haggle", payload["to_char"])
        self.improve.assert_not_called()

    def test_sell_extract_consumes_roll_without_discount_or_learning(self):
        self.keeper.inventory = [self.item(extra_flags=str(self.base.enums["itemFlags"].ITEM_SELL_EXTRACT.value))]
        payload, ctx = self.command("buy", "sword")
        self.assertEqual(121, ctx.buy_cost)
        self.assertNotIn("haggle", payload["to_char"])
        self.roll.assert_called_once_with()
        self.improve.assert_not_called()

    def test_base_affordability_denial_happens_before_purchase_roll(self):
        item = self.item()
        self.keeper.inventory = [item]
        self.actor.gold, self.actor.silver = 1, 0  # can afford 96, cannot afford base 121
        payload, ctx = self.command("buy", "sword")
        self.assertTrue(payload["blocked"])
        self.assertEqual([item], self.keeper.inventory)
        self.assertEqual(100, self.wealth(self.actor))
        self.roll.assert_not_called()
        self.improve.assert_not_called()

    def test_capacity_denial_does_not_roll(self):
        item = self.item(weight=1000)
        self.keeper.inventory = [item]
        self.actor.character_attributes.max_weight = 10
        payload, ctx = self.command("buy", "sword")
        self.assertTrue(payload["blocked"])
        self.roll.assert_not_called()

    def pet_shop(self):
        proto = NS(level=3, short_description="a puppy")
        self.base.swap(h.Shop, "is_pet_shop", return_value=True)
        self.base.swap(h.Shop, "pet_stock_room", return_value=NS())
        self.base.swap(h.Shop, "find_pet", return_value=proto)
        def purchase(actor, room, prototype, name, cost, *flags):
            h.Shop._deduct_money(actor, cost)
            actor.pet = NS(short_description="a puppy", name=name)
            return actor.pet
        return self.base.swap(h.Shop, "complete_pet_purchase", side_effect=purchase)

    def test_pet_discount_uses_pet_price_and_collection_message(self):
        purchase = self.pet_shop()
        payload, ctx = self.command("buy", "puppy Fido")
        self.assertEqual(68, ctx.buy_cost)  # 90 - 45*50/100
        self.assertEqual(9932, self.wealth(self.actor))
        self.assertEqual("Fido", self.actor.pet.name)
        self.assertEqual(68, purchase.call_args.args[4])
        self.assertEqual("You haggle the price down to 68 coins.\r\nEnjoy your pet.\r\n", payload["to_char"])
        self.improve.assert_called_once_with(self.actor, "haggle-id", True, 4)

    def test_pet_base_affordability_and_level_guards_precede_roll(self):
        purchase = self.pet_shop()
        self.actor.gold, self.actor.silver = 0, 80
        payload, ctx = self.command("buy", "puppy")
        self.assertTrue(payload["blocked"])
        self.actor.gold = 100
        self.actor.level = 2
        payload, ctx = self.command("buy", "puppy")
        self.assertTrue(payload["blocked"])
        purchase.assert_not_called()
        self.roll.assert_not_called()

    def test_sale_increases_price_and_orders_room_then_haggle_and_receipt(self):
        item = self.item()
        self.actor.loot.append(item)
        before = self.wealth(self.keeper)
        payload, ctx = self.command("sell", "sword")
        self.assertEqual((75, 0, 75), (ctx.sell_cost, ctx.sell_gold, ctx.sell_silver))
        self.assertEqual(10075, self.wealth(self.actor))
        self.assertEqual(before - 75, self.wealth(self.keeper))
        self.assertIn(item, self.keeper.inventory)
        self.assertNotIn(item, self.actor.loot)
        self.assertEqual("Tester sells sword.\r\n", payload["payloads"][0]["to_room"])
        self.assertEqual("You haggle with the shopkeeper.\r\nYou sell sword for 75 silver and 0 gold pieces.\r\n", payload["payloads"][1]["to_char"])
        self.improve.assert_called_once_with(self.actor, "haggle-id", True, 4)

    def test_sale_price_is_capped_by_keeper_wealth(self):
        self.actor.loot.append(self.item())
        self.keeper.gold, self.keeper.silver = 0, 60
        payload, ctx = self.command("sell", "sword")
        self.assertEqual(60, ctx.sell_cost)
        self.assertEqual(0, self.wealth(self.keeper))
        self.assertEqual(10060, self.wealth(self.actor))

    def test_sale_price_is_capped_at_95_percent_of_buy_quote(self):
        self.actor.loot.append(self.item())
        self.shop.profit_buy, self.shop.profit_sell = 60, 50
        payload, ctx = self.command("sell", "sword")
        self.assertEqual(57, ctx.sell_cost)  # min(75, 95*60/100)
        self.assertEqual(10057, self.wealth(self.actor))

    def test_keeper_base_affordability_denial_precedes_sale_roll(self):
        item = self.item()
        self.actor.loot.append(item)
        self.keeper.gold, self.keeper.silver = 0, 49
        payload, ctx = self.command("sell", "sword")
        self.assertTrue(payload["blocked"])
        self.assertIn(item, self.actor.loot)
        self.roll.assert_not_called()
        self.improve.assert_not_called()

    def test_failed_and_sell_extract_sales_do_not_learn_or_adjust(self):
        for extract in (False, True):
            with self.subTest(extract=extract):
                item = self.item(extra_flags=str(self.base.enums["itemFlags"].ITEM_SELL_EXTRACT.value if extract else 0))
                self.actor.loot.clear()
                self.actor.loot.append(item)
                self.keeper.inventory = []
                self.actor.skill_level = lambda name: 0 if not extract else 100
                self.roll.reset_mock()
                payload, ctx = self.command("sell", "sword")
                self.assertEqual(50, ctx.sell_cost)
                self.assertNotIn("haggle", payload["to_char"])
                self.roll.assert_called_once_with()
                self.improve.assert_not_called()
                if extract:
                    self.assertNotIn(item, self.keeper.inventory)

    def test_value_never_haggles_or_learns(self):
        item = self.item()
        self.actor.loot.append(item)
        payload, ctx = self.command("value", "sword")
        self.assertIn("50 silver", payload["to_char"])
        self.assertIn(item, self.actor.loot)
        self.roll.assert_not_called()
        self.improve.assert_not_called()

    def test_haggle_skill_applies_class_level_daze_drunk_and_npc_rules(self):
        self.actor.level = 0
        self.assertEqual(0, self.commands._haggle_skill_percent(self.actor))
        self.actor.level = 20
        self.actor.skill_level = lambda name: 79
        self.actor.status_flags.pulse_daze = 1
        self.actor.status_flags.drunk = 11
        self.assertEqual(46, self.commands._haggle_skill_percent(self.actor))  # 79*2/3=52, *9/10=46
        self.actor.is_npc = True
        self.assertEqual(0, self.commands._haggle_skill_percent(self.actor))


if __name__ == "__main__":
    unittest.main()

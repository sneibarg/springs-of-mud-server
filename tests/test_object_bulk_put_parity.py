"""ROM24 bulk put selection, limits, silent skips, and transfer messages."""
import sys
import unittest
from unittest.mock import patch

from tests import test_object_container_shop_spell_parity as container_tests
from tests.test_object_loot_and_sacrifice_parity import RealItemApi

h = container_tests.h


class TestObjectBulkPutParity(unittest.TestCase):
    def setUp(self):
        self.base = container_tests.TestObjectContainerShopSpellParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.commands, self.room = self.base.commands, self.base.room
        self.enums, self.fixture = self.base.enums, self.base.fixture
        self.commands.container_state = self.enums["containerState"]
        self.base.swap(RealItemApi, "get_enum", side_effect=self.enums.__getitem__)
        self.commands.well_known_object_vnums = self.enums["wellKnownObjectVnums"]
        for module in (sys.modules[h.Object.__module__], sys.modules[h.InterpApi.__module__]):
            self.base.swap(module, "ItemApi", new=RealItemApi)
        self.visibility = self.base.swap(RealItemApi, "can_see_object",
                                         side_effect=lambda room, actor, item: not getattr(item, "hidden", False))
        self.actor = self.fixture._build_character()
        self.bag = self.base.bag()
        self.room.contents = {self.bag.id: self.bag}

    def item(self, name="gem", **kwargs):
        return self.base.item(name, **kwargs)

    def put(self, raw="all bag"):
        context = self.fixture._build_context(raw, self.room, self.actor, "put")
        payload = self.commands.do_put(self.actor, context)
        self.assertTrue(context.done)
        return payload

    def test_put_all_moves_each_eligible_item_in_inventory_order(self):
        first, second = self.item("ruby"), self.item("coin")
        self.actor.loot.extend([first, second])
        payload = self.put("all in bag")
        self.assertEqual([first, second], self.bag.contains)
        self.assertEqual([], self.actor.loot)
        self.assertEqual(["You put ruby in bag.\r\n", "You put coin in bag.\r\n"],
                         [entry["to_char"] for entry in payload["payloads"]])
        self.assertEqual(["Tester puts ruby in bag.\r\n", "Tester puts coin in bag.\r\n"],
                         [entry["to_room"] for entry in payload["payloads"]])
        for entry in payload["payloads"]:
            self.assertEqual([self.base.base.witness], entry["targets"])

    def test_all_name_matches_keyword_prefixes_and_quoted_multiple_words(self):
        red = self.item("gem ruby red")
        blue = self.item("gem sapphire blue")
        sword = self.item("sword steel")
        self.actor.loot.extend([red, blue, sword])
        self.put("'all.re ru' bag")
        self.assertEqual([red], self.bag.contains)
        self.assertEqual([blue, sword], self.actor.loot)
        self.put("ALL.SAP bag")
        self.assertEqual([red, blue], self.bag.contains)

    def test_bulk_silently_skips_invisible_worn_cursed_magic_and_destination_items(self):
        hidden = self.item("hidden")
        hidden.hidden = True
        worn = self.item("worn")
        metadata_worn = self.item("metadata")
        metadata_worn.wear_loc = 4
        cursed = self.item("cursed", extra_flags=str(self.enums["itemFlags"].ITEM_NODROP.value))
        magic = self.item("magic", item_type="container", value4="50")
        gem = self.item()
        self.actor.loot.extend([hidden, worn, metadata_worn, cursed, magic, self.bag, gem])
        self.actor.equip_item(worn, "head")
        payload = self.put()
        self.assertEqual([gem], self.bag.contains)
        self.assertEqual([hidden, metadata_worn, cursed, magic, self.bag], self.actor.loot)
        self.assertIs(worn, self.actor.equipped.head)
        self.assertEqual(1, len(payload["payloads"]))
        self.visibility.assert_any_call(self.room, self.actor, hidden)

    def test_oversized_items_do_not_stop_later_fitting_items_and_capacity_is_rechecked(self):
        self.bag.value0, self.bag.value3 = "1", "10"  # shell weighs two; eight free
        huge, first, excess, small = (self.item("huge", weight=100), self.item("first", weight=6),
                                      self.item("excess", weight=3), self.item("small", weight=2))
        self.actor.loot.extend([huge, first, excess, small])
        payload = self.put()
        self.assertEqual([first, small], self.bag.contains)
        self.assertEqual([huge, excess], self.actor.loot)
        self.assertEqual(2, len(payload["payloads"]))

    def test_bulk_individual_limit_is_strict_but_single_put_allows_equality(self):
        self.bag.value3 = "1"
        exact = self.item("exact", weight=10)
        smaller = self.item("smaller", weight=9)
        self.actor.loot.extend([exact, smaller])
        self.put()
        self.assertEqual([smaller], self.bag.contains)
        self.assertEqual([exact], self.actor.loot)
        self.put("exact bag")
        self.assertEqual([smaller, exact], self.bag.contains)

    def test_bulk_uses_recursive_weight_and_unscaled_destination_capacity(self):
        self.bag.value0, self.bag.value3, self.bag.value4 = "1", "10", "1"
        self.bag.contains.append(self.item("old", weight=3))
        filled = self.item("filled", item_type="container", weight=1, value4="100",
                           contains=[self.item("heavy", weight=5)])
        self.actor.loot.append(filled)
        self.assertEqual({"payloads": []}, self.put())
        self.assertEqual([filled], self.actor.loot)

    def test_silent_skips_do_not_depend_on_error_message_text(self):
        oversized = self.item(weight=1000)
        self.actor.loot.append(oversized)
        context = self.fixture._build_context("all bag", self.room, self.actor, "put")
        context.command.payload = h.GamePayload()
        self.assertEqual({"payloads": []}, self.commands.do_put(self.actor, context))
        self.assertEqual([oversized], self.actor.loot)
        self.assertEqual([], self.bag.contains)

    def test_no_matches_empty_selector_and_full_container_are_silent(self):
        gem = self.item()
        self.actor.loot.append(gem)
        for raw in ("all.absent bag", "all. bag"):
            self.assertEqual({"payloads": []}, self.put(raw))
        self.bag.value0 = "0"
        self.assertEqual({"payloads": []}, self.put())
        self.assertEqual([gem], self.actor.loot)
        self.actor.loot.clear()
        self.assertEqual({"payloads": []}, self.put())

    def test_invalid_destination_closed_container_and_missing_arguments_still_block(self):
        gem = self.item()
        self.actor.loot.append(gem)
        for raw, message in (("all", "Put what in what?"), ("all absent", "I see no absent here."),
                              ("all all", "You can't do that."), ("all all.bag", "You can't do that.")):
            with self.subTest(raw=raw):
                self.assertEqual(message + "\r\n", self.put(raw)["to_char"])
        self.bag.value1 = str(self.enums["containerState"].CONT_CLOSED.value)
        self.assertEqual("The bag is closed.\r\n", self.put()["to_char"])
        self.bag.value1, self.bag.item_type = "0", "drink"
        self.assertEqual("That's not a container.\r\n", self.put()["to_char"])
        self.assertEqual([gem], self.actor.loot)

    def test_surface_flag_controls_bulk_and_single_put_messages(self):
        gem = self.item()
        self.actor.loot.append(gem)
        self.bag.value1 = str(self.enums["containerState"].CONT_PUT_ON.value)
        payload = self.put("all in bag")
        self.assertEqual("You put gem on bag.\r\n", payload["payloads"][0]["to_char"])
        self.assertEqual("Tester puts gem on bag.\r\n", payload["payloads"][0]["to_room"])
        coin = self.item("coin")
        self.actor.loot.append(coin)
        self.bag.value1 = "0"
        self.assertEqual("You put coin in bag.\r\n", self.put("coin on bag")["to_char"])

    def test_immortal_can_bulk_put_nodrop_but_mortal_cannot(self):
        gem = self.item(extra_flags=str(self.enums["itemFlags"].ITEM_NODROP.value))
        self.actor.loot.append(gem)
        self.assertEqual({"payloads": []}, self.put())
        self.actor.is_immortal = True
        self.put()
        self.assertEqual([gem], self.bag.contains)

    def test_bulk_pit_timer_uses_reference_item_takeability_predicate(self):
        self.bag.vnum = str(self.enums["wellKnownObjectVnums"].OBJ_VNUM_PIT.value)
        self.bag.wear_flags = "0"
        plain = self.item("plain", wear_flags="0", timer=0)
        timed = self.item("timed", wear_flags="0", timer=7)
        takeable = self.item("takeable", wear_flags="1", timer=0)
        self.actor.loot.extend([plain, timed, takeable])
        with patch.object(container_tests.consumption.RNG, "number_range", return_value=137) as roll:
            self.put()
        roll.assert_called_once_with(100, 200)
        self.assertEqual((137, 7, 0), (plain.timer, timed.timer, takeable.timer))
        had_timer = self.enums["itemFlags"].ITEM_HAD_TIMER.value
        self.assertTrue(int(timed.extra_flags) & had_timer)
        self.assertFalse(int(plain.extra_flags) & had_timer)
        self.assertEqual([plain, timed, takeable], self.bag.contains)


if __name__ == "__main__":
    unittest.main()

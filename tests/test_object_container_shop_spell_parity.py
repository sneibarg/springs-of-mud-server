"""ROM act_obj put capacity, loaded shop types, and obj_cast_spell targeting."""
import json
import sys
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests import test_object_consumption_parity as consumption

h = consumption.h
RealItemApi = h._load_module("container_parity_item_api", "api/ItemApi.py").ItemApi
GameApi = sys.modules[h.Item.__module__].GameApi
ROOT = Path(__file__).resolve().parents[1]


class TestObjectContainerShopSpellParity(unittest.TestCase):
    def setUp(self):
        self.base = consumption.TestObjectConsumptionParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.fixture = self.base.fixture
        data = json.loads((ROOT / "resources/collections/SOMDB.GameData.json").read_text(encoding="utf-8"))[0]
        self.enums = {name: IntEnum(name, values) for name, values in data["enums"].items()}
        self.item_table = data["itemTable"]
        self.swap(GameApi, "item_table_map", return_value=self.item_table)
        self.swap(RealItemApi, "get_enum", side_effect=self.enums.__getitem__)
        for module in (sys.modules[h.Object.__module__], sys.modules[h.InterpApi.__module__]):
            self.swap(module, "ItemApi", new=RealItemApi)
        self.commands.item_types = self.enums["itemTypes"]
        self.commands.item_flags = self.enums["itemFlags"]
        self.commands.wear_flags = self.enums["wearFlags"]
        self.commands.fight_handler = NS(is_safe=Mock(return_value=(False, "")),
                                         is_safe_spell=Mock(return_value=False))

    def swap(self, target, name, **kwargs):
        swap = patch.object(target, name, **kwargs)
        result = swap.start()
        self.addCleanup(swap.stop)
        return result

    @staticmethod
    def item(name="gem", **kwargs):
        kwargs.setdefault("item_type", "gem")
        return consumption.TestObjectConsumptionParity.item(name, **kwargs)

    def put(self, obj, container):
        self.actor = self.fixture._build_character(obj, container)
        self.room.contents = {}
        context = self.fixture._build_context(obj.name + " " + container.name, self.room, self.actor, "put")
        payload = self.commands.do_put(self.actor, context)
        self.assertTrue(context.done)
        return payload

    def bag(self, **kwargs):
        values = dict(item_type="container", weight=2, value0="10", value3="5", value4="100")
        values.update(kwargs)
        return self.item("bag", **values)

    def assert_put_blocked(self, obj, bag, message):
        original = list(bag.contains)
        payload = self.put(obj, bag)
        self.assertEqual(message + "\r\n", payload["to_char"])
        self.assertIn(obj, self.actor.loot)
        self.assertEqual(original, bag.contains)
        self.assertNotIn("to_room", payload)

    def test_put_capacity_includes_container_shell_and_existing_contents(self):
        bag = self.bag(value0="1", value3="2", contains=[self.item("old", weight=3)])
        obj = self.item(weight=6)
        self.assert_put_blocked(obj, bag, "It won't fit.")
        obj.weight = 5
        self.put(obj, bag)
        self.assertIn(obj, bag.contains)  # exact total limit of ten is allowed
        self.assertNotIn(obj, self.actor.loot)

    def test_put_individual_limit_allows_exact_boundary_but_not_one_more(self):
        bag = self.bag(value3="1")
        obj = self.item(weight=11)
        self.assert_put_blocked(obj, bag, "It won't fit.")
        obj.weight = 10
        self.put(obj, bag)
        self.assertIn(obj, bag.contains)

    def test_recursive_weights_and_destination_multiplier_match_rom(self):
        child = self.item("inner", item_type="container", weight=2, value4="50",
                          contains=[self.item("rock", weight=7)])
        outer = self.item("outer", item_type="container", weight=1, value4="100", contains=[child])
        self.assertEqual(5, h.Item.object_weight(child))  # 2 + trunc(7 * .5)
        self.assertEqual(6, h.Item.object_weight(outer))
        bag = self.bag(value0="1", value3="10", value4="1", contains=[self.item("old", weight=3)])
        self.assertEqual(5, h.Item.true_weight(bag))  # destination multiplier does not discount capacity
        self.assert_put_blocked(outer, bag, "It won't fit.")

    def test_put_rejects_weight_reducing_and_increasing_containers_using_value4(self):
        for multiplier in (0, 50, 150):
            with self.subTest(multiplier=multiplier):
                obj = self.item("nested", item_type="container", weight=1, value3="100", value4=str(multiplier))
                self.assert_put_blocked(obj, self.bag(), "You have a feeling that would be a bad idea.")
                self.assertEqual(multiplier, RealItemApi.weight_multiplier(obj))
        obj = self.item("nested", item_type="container", weight=1, value3="1", value4="100")
        bag = self.bag()
        self.put(obj, bag)
        self.assertIn(obj, bag.contains)

    def test_closed_and_noncontainer_guards_preserve_inventory(self):
        self.assert_put_blocked(self.item(), self.bag(value1=str(self.enums["containerState"].CONT_CLOSED.value)),
                                "The bag is closed.")
        self.assert_put_blocked(self.item(), self.bag(item_type="drink"), "That's not a container.")

    def test_nodrop_precedes_weight_checks_and_immortal_can_put_nodrop(self):
        obj = self.item(extra_flags=str(self.enums["itemFlags"].ITEM_NODROP.value), weight=1000)
        self.assert_put_blocked(obj, self.bag(), "You can't let go of it.")
        obj.weight = 1
        bag = self.bag()
        self.actor = self.fixture._build_character(obj, bag, is_immortal=True)
        context = self.fixture._build_context("gem bag", self.room, self.actor, "put")
        self.commands.do_put(self.actor, context)
        self.assertIn(obj, bag.contains)

    def test_all_designer_item_aliases_resolve_through_gamedata(self):
        shop = self.fixture._build_shop()
        for alias, definition in self.item_table.items():
            with self.subTest(alias=alias):
                item = self.item(item_type=alias)
                shop.buy_type0 = self.enums["itemTypes"][definition["type"]].value
                self.assertTrue(shop.buys_item(item, self.enums["itemTypes"]))
                self.assertEqual(alias, item.item_type)
                item.item_type = definition["type"]
                self.assertTrue(shop.buys_item(item, self.enums["itemTypes"]))
        self.assertFalse(shop.buys_item(self.item(item_type="unknown"), self.enums["itemTypes"]))

    def test_sale_and_value_for_loaded_weapon_and_trash_extraction(self):
        shop = self.fixture._build_shop(profit_sell=50)
        keeper = NS(inventory=[], gold=10, silver=0, short_description="keeper")
        for kind in ("weapon", "trash"):
            with self.subTest(kind=kind):
                keeper.inventory.clear()
                item = self.item(item_type=kind, cost=100)
                shop.buy_type0 = self.enums["itemTypes"]["ITEM_" + kind.upper()].value
                self.actor = self.fixture._build_character(item)
                self.assertEqual(50, shop.quote_value(item, keeper, self.enums["itemTypes"], self.commands.item_flags).cost)
                shop.complete_sale(self.actor, keeper, item, 50, self.commands.item_flags)
                self.assertNotIn(item, self.actor.loot)
                self.assertEqual(50, self.actor.gold * 100 + self.actor.silver)
                self.assertEqual(kind != "trash", item in keeper.inventory)

    def test_wand_staff_charge_adjustment_applies_to_buy_sell_and_value(self):
        shop = self.fixture._build_shop(profit_buy=120, profit_sell=50)
        keeper = NS(inventory=[], short_description="keeper")
        for kind in ("wand", "staff", "ITEM_WAND", "ITEM_STAFF"):
            with self.subTest(kind=kind):
                item = self.item(item_type=kind, cost=100, value1="4", value2="1")
                shop.buy_type0 = self.enums["itemTypes"][h.Item.enum_type_name(item)].value
                self.assertEqual(30, shop.buy_price(item))
                self.assertEqual(12, shop.sell_price(item, [], self.enums["itemTypes"], self.commands.item_flags))
                self.assertEqual(12, shop.quote_value(item, keeper, self.enums["itemTypes"], self.commands.item_flags).cost)
                item.value1 = "0"
                self.assertEqual(30, shop.buy_price(item))
                item.value1, item.value2 = "4", "0"
                self.assertEqual(0, shop.buy_price(item))

    def cast(self, category, target=None, command="recite"):
        spell = self.base.spell("test")
        spell.target = category
        self.commands.cast_observations.clear()
        self.commands.spell_api.start_offensive_combat = Mock()
        context = self.fixture._build_context("", self.room, self.actor, command)
        result = self.commands._cast_item_spell(self.actor, self.room, self.item(value0="17"), spell,
                                               target=target, target_name="unused", command_context=context)
        return result

    def test_item_spell_target_category_matrix(self):
        obj = self.item()
        victim = self.fixture._build_character(name="Victim")
        for category, selected, expected in (
            ("IGNORE", victim, None), ("CHAR_DEFENSIVE", obj, self.actor),
            ("CHAR_SELF", obj, self.actor), ("CHAR_SELF", victim, victim),
            ("OBJ_INV", obj, obj), ("CHAR_OFFENSIVE", victim, victim),
            ("OBJ_CHAR_OFF", obj, obj), ("OBJ_CHAR_OFF", victim, victim),
            ("OBJ_CHAR_DEF", obj, obj), ("OBJ_CHAR_DEF", None, self.actor),
        ):
            with self.subTest(category=category):
                self.cast(category, selected)
                self.assertIs(expected, self.commands.cast_observations[0][2])
                self.assertEqual(17, self.commands.cast_observations[0][1])

    def test_offensive_fallback_uses_fighting_target_and_missing_targets_do_not_cast(self):
        victim = self.fixture._build_character(name="Victim")
        self.actor.fighting = victim
        for kind, target in (("CHAR_OFFENSIVE", self.item()), ("OBJ_CHAR_OFF", None)):
            self.cast(kind, target)
            self.assertIs(victim, self.commands.cast_observations[0][2])
        self.actor.fighting = None
        for category, selected in (("CHAR_OFFENSIVE", None), ("OBJ_CHAR_OFF", None), ("OBJ_INV", victim)):
            with self.subTest(category=category):
                result = self.cast(category, selected)
                self.assertEqual([], self.commands.cast_observations)
                self.assertEqual("You can't do that.\r\n", result[0]["to_char"])
                self.commands.spell_api.start_offensive_combat.assert_not_called()

    def test_safety_checked_before_non_damage_spell_effects(self):
        victim = self.fixture._build_character(name="Victim")
        for category in ("CHAR_OFFENSIVE", "OBJ_CHAR_OFF"):
            with self.subTest(category=category):
                self.commands.fight_handler.is_safe.return_value = (True, "Protected.\r\n")
                self.commands.fight_handler.is_safe_spell.return_value = True
                result = self.cast(category, victim)
                self.assertEqual([], self.commands.cast_observations)
                self.commands.spell_api.start_offensive_combat.assert_not_called()
                self.assertTrue(result[0]["to_char"].endswith("Something isn't right...\r\n"))
        self.commands.fight_handler.is_safe.assert_called_with(self.actor, victim, room=self.room)
        self.commands.fight_handler.is_safe_spell.assert_called_with(self.actor, victim, area=False)

    def test_self_offense_and_object_targets_bypass_character_safety(self):
        for category, target in (("CHAR_OFFENSIVE", self.actor), ("OBJ_CHAR_OFF", self.actor),
                                 ("OBJ_CHAR_OFF", self.item())):
            self.cast(category, target)
            self.assertEqual(1, len(self.commands.cast_observations))
        self.commands.fight_handler.is_safe.assert_not_called()
        self.commands.fight_handler.is_safe_spell.assert_not_called()

    def test_denied_scroll_spell_still_consumes_scroll_and_continues_later_slots(self):
        victim = self.fixture._build_character(name="Victim")
        self.room.characters[victim.id] = victim
        blocked = self.base.spell("bad")
        blocked.target = "CHAR_OFFENSIVE"
        heal = self.base.spell("heal")
        self.commands.spell_registry = NS(all_spells=lambda: [blocked, heal])
        self.commands.fight_handler.is_safe.return_value = (True, "Protected.\r\n")
        scroll = self.item("scroll", item_type="scroll", value0="17", value1="bad", value2="heal", value3="")
        self.actor.loot.append(scroll)
        context = self.fixture._build_context("scroll Victim", self.room, self.actor, "recite")
        with patch.object(self.commands, "_item_skill_check", return_value=True):
            result = self.commands.do_recite(self.actor, context)
        self.assertNotIn(scroll, self.actor.loot)
        self.assertEqual(["heal"], [entry[0] for entry in self.commands.cast_observations])
        self.assertIn("Something isn't right...", result["payloads"][1]["to_char"])

    def test_denied_wand_and_staff_spells_still_spend_charge_and_wait(self):
        victim = self.fixture._build_character(name="Victim", is_npc=True)
        self.room.mobiles[victim.id] = victim
        spell = self.base.spell("bad")
        spell.target = "CHAR_OFFENSIVE"
        self.commands.spell_registry = NS(all_spells=lambda: [spell])
        self.commands.fight_handler.is_safe.return_value = (True, "Protected.\r\n")
        for command, kind, argument in (("zap", "wand", "Victim"), ("brandish", "staff", "")):
            with self.subTest(command=command):
                item = self.item(kind, item_type=kind, value0="17", value2="2", value3=spell)
                self.actor.loot.append(item)
                self.actor.equip_item(item, "held")
                context = self.fixture._build_context(argument, self.room, self.actor, command)
                with patch.object(self.commands, "_item_skill_check", return_value=True):
                    result = getattr(self.commands, "do_" + command)(self.actor, context)
                self.assertEqual("1", item.value2)
                self.assertEqual(24, self.actor.wait)
                self.assertEqual([], self.commands.cast_observations)
                self.assertTrue(any("Something isn't right..." in p.get("to_char", "") for p in result["payloads"]))
                self.actor.unequip_item("held")

    def test_unknown_spell_target_does_not_execute(self):
        self.assertEqual([], self.cast("UNSUPPORTED", self.actor))
        self.assertEqual([], self.commands.cast_observations)


if __name__ == "__main__":
    unittest.main()

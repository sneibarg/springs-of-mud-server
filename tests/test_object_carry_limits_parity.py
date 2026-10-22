"""Recursive object counts, carried weights, and command-specific carry limits."""
import sys
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
from tests import test_object_container_shop_spell_parity as fixtures

h = fixtures.h
ItemApi = fixtures.RealItemApi
stubs = {name: NS(**{attr: object}) for name, attr in (
    ("player.CharacterAttributes", "CharacterAttributes"), ("player.ArmorClass", "ArmorClass"),
    ("player.CharacterClass", "CharacterClass"), ("player.CharacterFlags", "CharacterFlags"),
    ("player.CharacterRace", "CharacterRace"), ("interp.PromptFormat", "PromptFormat"),
    ("game.StatusFlags", "StatusFlags"))}
with patch.dict(sys.modules, stubs):
    Entity = h._load_module("carry_entity", "game/AnimateEntity.py").AnimateEntity
    with patch.dict(sys.modules, {"game.AnimateEntity": NS(AnimateEntity=Entity)}):
        Character = h._load_module("carry_character", "player/Character.py").Character


class TestObjectCarryLimitsParity(unittest.TestCase):
    def setUp(self):
        self.base = fixtures.TestObjectContainerShopSpellParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.actor.gold = self.actor.silver = 0
        self.wire(self.actor)

    def wire(self, actor):
        actor.carry_count = lambda: ItemApi.carried_count(actor)
        actor.carry_weight = lambda: ItemApi.carried_weight(actor)
        actor.max_items = lambda: actor.character_attributes.max_items
        actor.max_weight = lambda: actor.character_attributes.max_weight
        actor.character_attributes.max_items = 10
        actor.character_attributes.max_weight = 100

    def item(self, name="sword", **kw):
        kw.setdefault("item_type", "weapon")
        return self.base.item(name, **kw)

    def bag(self, **kw):
        return self.base.bag(**kw)

    def get(self, item, container=None):
        context = self.base.fixture._build_context("sword", self.room, self.actor)
        if container is None:
            self.room.contents[item.id] = item
        else:
            container.contains.append(item)
        return self.commands._get_one(self.actor, self.room, context, item, container)

    def test_recursive_count_exempts_only_four_shell_types(self):
        for kind in ("container", "money", "gem", "jewelry"):
            obj = self.item(item_type=kind, contains=[self.item("one"), self.item("two")])
            self.assertEqual(2, h.Item.object_number(obj), kind)
        corpse = self.item(item_type="corpse_npc", contains=[self.item()])
        self.assertEqual(2, h.Item.object_number(corpse))

    def test_nested_weight_multiplies_and_truncates_each_child_separately(self):
        inner = self.bag(weight=2, value4="50", contains=[self.item("one", weight=3), self.item("two", weight=3)])
        outer = self.bag(weight=1, value4="25", contains=[inner])
        self.assertEqual(4, h.Item.object_weight(inner))
        self.assertEqual(2, h.Item.object_weight(outer))
        self.assertEqual(5, h.Item.true_weight(outer))
        corpse = self.item(item_type="corpse_npc", weight=2, value4="1", contains=[self.item(weight=8)])
        self.assertEqual(10, h.Item.object_weight(corpse))

    def test_real_character_counts_equipment_once_and_rounds_denominations_separately(self):
        actor = Character.__new__(Character)
        sword = self.item(weight=3)
        bag = self.bag(weight=2, value4="50", contains=[self.item("dagger", weight=5)])
        actor.loot = [bag, sword]
        actor.equipped = h.Equipped()
        actor.equipped.head = sword  # tolerate duplicate inventory/equipment identity
        actor.silver, actor.gold = 9, 2
        with patch.dict(sys.modules, {"api.ItemApi": NS(ItemApi=ItemApi)}):
            self.assertEqual(2, actor.carry_count())
            self.assertEqual(7, actor.carry_weight())  # 9/10 and 4/5 each truncate to zero
            actor.silver, actor.gold = 10, 3
            self.assertEqual(9, actor.carry_weight())
        actor.loot.remove(sword)
        self.assertEqual(2, ItemApi.carried_count(actor))
        self.assertEqual(7, ItemApi.carried_weight(actor, include_coins=False))

    def test_pickup_counts_contents_and_preserves_on_overflow(self):
        bag = self.bag(contains=[self.item("one"), self.item("two")])
        self.actor.character_attributes.max_items = 1
        self.assertIn("can't carry that many", self.get(bag)["to_char"])
        self.assertIn(bag.id, self.room.contents)
        self.actor.character_attributes.max_items = 2
        self.assertIn("You get", self.get(bag)["to_char"])
        self.assertIn(bag, self.actor.loot)

    def test_gem_and_empty_container_can_be_picked_up_at_item_limit(self):
        self.actor.character_attributes.max_items = 1
        self.actor.loot.append(self.item("old"))
        for obj in (self.item("ruby", item_type="gem"), self.bag()):
            self.get(obj)
            self.assertIn(obj, self.actor.loot)
        self.assertEqual(1, self.actor.carry_count())

    def test_pickup_uses_weighted_contents_with_exact_boundary(self):
        bag = self.bag(weight=2, value4="50", contains=[self.item(weight=18)])
        self.actor.character_attributes.max_weight = 10
        self.assertIn("can't carry that much", self.get(bag)["to_char"])
        self.actor.character_attributes.max_weight = 11
        self.get(bag)
        self.assertIn(bag, self.actor.loot)

    def test_direct_carried_container_skips_weight_check_but_still_checks_count(self):
        bag = self.bag(weight=2, value4="1")
        self.actor.loot.append(bag)
        self.actor.character_attributes.max_weight = 2
        obj = self.item(weight=100)
        self.get(obj, bag)
        self.assertIn(obj, self.actor.loot)
        self.assertEqual([], bag.contains)
        self.actor.character_attributes.max_items = 1
        second = self.item("second")
        self.assertIn("can't carry that many", self.get(second, bag)["to_char"])
        self.assertIn(second, bag.contains)

    def test_room_and_nested_carried_containers_do_not_get_weight_exemption(self):
        for nested in (False, True):
            with self.subTest(nested=nested):
                self.actor.loot = []
                bag = self.bag()
                if nested:
                    self.actor.loot.append(self.bag(contains=[bag]))
                self.actor.character_attributes.max_weight = 5
                obj = self.item(weight=20)
                self.assertIn("can't carry that much", self.get(obj, bag)["to_char"])
                self.assertIn(obj, bag.contains)

    def test_buy_collection_guards_use_recursive_quantity_and_exclude_coins(self):
        item = self.bag(weight=2, contains=[self.item(weight=3), self.item("dagger", weight=3)])
        self.actor.gold = 1000
        context = self.base.fixture._build_context("2 bag", self.room, self.actor, "buy")
        context.buy_is_pet_shop = False
        context.buy_quantity, context.buy_item = 2, item
        view = self.commands.interp_api.build_interp_view(context)
        env = {"ItemApi": ItemApi, "Item": h.Item}
        count_guard, weight_guard = context.command.guards[-2:]
        count = eval(count_guard["predicate"], env)
        weight = eval(weight_guard["predicate"], env)
        self.actor.character_attributes.max_items = 3
        self.assertTrue(count(view))
        self.actor.character_attributes.max_items = 4
        self.assertFalse(count(view))
        self.actor.character_attributes.max_weight = 15
        self.assertTrue(weight(view))
        self.actor.character_attributes.max_weight = 16
        self.assertFalse(weight(view))

    def test_give_capacity_uses_recipient_recursive_load_and_incoming_contents(self):
        victim = self.base.fixture._build_character()
        victim.id, victim.name = "victim", "Victim"
        victim.gold = victim.silver = 0
        self.wire(victim)
        self.room.characters[victim.id] = victim
        bag = self.bag(weight=2, contains=[self.item(weight=8), self.item("dagger", weight=8)])
        self.actor.loot.append(bag)
        context = self.base.fixture._build_context("bag Victim", self.room, self.actor, "give")
        victim.character_attributes.max_items = 1
        self.commands._prepare_give_context(self.actor, context)
        self.assertTrue(context.give_target_hands_full)
        victim.character_attributes.max_items = 2
        victim.character_attributes.max_weight = 17
        self.commands._prepare_give_context(self.actor, context)
        self.assertFalse(context.give_target_hands_full)
        self.assertTrue(context.give_target_encumbered)
        victim.character_attributes.max_weight = 18
        self.commands._prepare_give_context(self.actor, context)
        self.assertFalse(context.give_target_encumbered)

    def test_steal_checks_recursive_incoming_count_and_weight(self):
        victim = self.base.fixture._build_character()
        victim.id, victim.name = "victim", "Victim"
        bag = self.bag(weight=2, contains=[self.item(weight=8), self.item("dagger", weight=8)])
        victim.loot.append(bag)
        self.room.characters[victim.id] = victim
        self.actor.character_attributes.max_items = 1
        context = self.base.fixture._build_context("bag Victim", self.room, self.actor, "steal")
        self.commands._prepare_steal_context(self.actor, context)
        self.commands._prepare_steal_item_context(self.actor, context)
        self.assertTrue(context.steal_inventory_full)
        self.actor.character_attributes.max_items = 2
        self.actor.character_attributes.max_weight = 17
        self.commands._prepare_steal_context(self.actor, context)
        self.commands._prepare_steal_item_context(self.actor, context)
        self.assertFalse(context.steal_inventory_full)
        self.assertTrue(context.steal_encumbered)
        self.actor.character_attributes.max_weight = 18
        self.actor.gold = 1000  # ROM theft checks item load without carried coins
        self.commands._prepare_steal_context(self.actor, context)
        self.commands._prepare_steal_item_context(self.actor, context)
        self.assertFalse(context.steal_encumbered)
        self.assertEqual([bag], victim.loot)

    def test_money_pickup_at_item_limit_credits_balances(self):
        self.actor.loot.append(self.item("old"))
        self.actor.character_attributes.max_items = 1
        money = self.item("coins", item_type="money", weight=0, value0="5", value1="2")
        self.get(money)
        self.assertEqual((5, 2), (self.actor.silver, self.actor.gold))
        self.assertNotIn(money.id, self.room.contents)
        self.assertEqual(1, self.actor.carry_count())

    def test_bulk_pickup_rechecks_recursive_load_after_each_transfer(self):
        first = self.bag(contains=[self.item("one"), self.item("two")])
        second = self.item("last")
        self.room.contents = {first.id: first, second.id: second}
        self.actor.character_attributes.max_items = 2
        context = self.base.fixture._build_context("all", self.room, self.actor)
        payload = self.commands.do_get(self.actor, context)
        self.assertIn(first, self.actor.loot)
        self.assertNotIn(second, self.actor.loot)
        self.assertIn(second.id, self.room.contents)
        self.assertIn("can't carry that many", payload["to_char"])


if __name__ == "__main__":
    unittest.main()

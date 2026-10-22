"""ROM24 currency drop merging and pickup/sacrifice autosplit regressions."""
import sys
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
from tests import test_object_container_shop_spell_parity as fixtures
from tests.test_object_loot_and_sacrifice_parity import RealItemUtil

h = fixtures.h
ObjectModule = sys.modules[h.Object.__module__]
CommunicationsApi = ObjectModule.CommunicationsApi


class TestObjectCurrencyParity(unittest.TestCase):
    def setUp(self):
        self.base = fixtures.TestObjectContainerShopSpellParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.commands, self.room, self.actor = self.base.commands, self.base.room, self.base.actor
        self.fixture = self.base.fixture
        self.enums = self.base.enums
        self.commands.PlayerActBits = self.enums["playerActBits"]
        self.commands.well_known_object_vnums = self.enums["wellKnownObjectVnums"]
        self.room.characters = {self.actor.id: self.actor}
        self.actor.gold, self.actor.silver = 20, 100
        self.actor.status_flags.act = self.enums["playerActBits"].PLR_AUTOSPLIT.value
        for module in (ObjectModule, sys.modules[h.InterpApi.__module__]):
            self.base.swap(module, "ItemUtil", new=RealItemUtil)
        self.base.swap(ObjectModule.CharacterApi, "is_same_group", create=True,
                       side_effect=lambda a, b: getattr(a, "leader", None) is getattr(b, "leader", None))
        self.base.swap(CommunicationsApi, "is_charmed", side_effect=lambda ch: getattr(ch, "charmed", False))
        self.base.swap(RealItemUtil, "can_see_object", return_value=True)
        self.prototypes = {}
        for name, silver, gold, text in [
            ("SILVER_ONE", 1, 0, "a silver coin"), ("GOLD_ONE", 0, 1, "a gold coin"),
            ("SILVER_SOME", 0, 0, "%d silver coins"), ("GOLD_SOME", 0, 0, "%d gold coins"),
            ("COINS", 0, 0, "%d silver and %d gold coins")]:
            vnum = getattr(self.commands.well_known_object_vnums, "OBJ_VNUM_" + name).value
            self.prototypes[vnum] = self.base.item(name, vnum=vnum, item_type="money",
                value0=str(silver), value1=str(gold), short_description=text)
        self.commands.item_registry = NS(get=lambda **kw: self.prototypes[kw["vnum"]])

    def context(self, name, raw):
        return self.fixture._build_context(raw, self.room, self.actor, name)

    def drop(self, raw):
        return self.commands.do_drop(self.actor, self.context("drop", raw))

    def member(self, name="ally", **kwargs):
        ch = self.fixture._build_character()
        ch.id, ch.name, ch.silver, ch.gold = name, name, 0, 0
        ch.__dict__.update(kwargs)
        self.room.characters[name] = ch
        return ch

    def money(self, silver, gold=0):
        return RealItemUtil.create_money(gold, silver, self.commands.item_registry,
                                         self.commands.well_known_object_vnums)

    def pickup(self, silver, gold=0, container=None):
        money = self.money(silver, gold)
        if container is None:
            self.room.contents[money.id] = money
        else:
            container.contains.append(money)
        return self.commands._get_one(self.actor, self.room, self.context("get", "coins"), money, container)

    def test_currency_aliases_deduct_silver_only_and_render_collection_messages(self):
        for alias in ("silver", "coin", "coins", "SILVER"):
            with self.subTest(alias=alias):
                self.room.contents = {}
                self.actor.silver = 100
                payload = self.drop("10 " + alias)
                self.assertEqual((90, 20), (self.actor.silver, self.actor.gold))
                pile = next(iter(self.room.contents.values()))
                self.assertEqual((10, 0), (int(pile.value0), int(pile.value1)))
                self.assertEqual("OK.\r\n", payload["to_char"])
                self.assertEqual("Tester drops some coins.\r\n", payload["to_room"])

    def test_gold_drop_and_single_coin_prototypes(self):
        self.drop("1 gold")
        pile = next(iter(self.room.contents.values()))
        self.assertEqual(self.commands.well_known_object_vnums.OBJ_VNUM_GOLD_ONE.value, int(pile.vnum))
        self.assertEqual(19, self.actor.gold)
        self.room.contents = {}
        self.drop("1 silver")
        pile = next(iter(self.room.contents.values()))
        self.assertEqual(self.commands.well_known_object_vnums.OBJ_VNUM_SILVER_ONE.value, int(pile.vnum))

    def test_invalid_and_insufficient_requests_leave_balances_and_room_unchanged(self):
        for raw, message in [("0 silver", "Sorry"), ("-2 gold", "Sorry"), ("10 gems", "Sorry"),
                             ("10", "Sorry"), ("101 coins", "You don't have that much silver"),
                             ("21 gold", "You don't have that much gold")]:
            with self.subTest(raw=raw):
                self.assertTrue(self.drop(raw)["to_char"].startswith(message))
                self.assertEqual((100, 20), (self.actor.silver, self.actor.gold))
                self.assertEqual({}, self.room.contents)

    def test_merges_all_standard_piles_by_vnum_and_preserves_other_objects(self):
        piles = [self.money(1), self.money(0, 1), self.money(12), self.money(0, 3), self.money(7, 2)]
        piles[0].value0 = "999"  # the one-coin prototype still contributes exactly one
        piles[1].value1 = "999"
        for pile in piles:
            pile.hidden = True
            self.room.contents[pile.id] = pile
        odd = self.base.item("odd", item_type="money", vnum=999999, value0="90")
        bag = self.base.bag(vnum=999998, contains=[self.money(30)])
        self.room.contents.update({odd.id: odd, bag.id: bag})
        self.drop("5 silver")
        self.assertEqual(3, len(self.room.contents))
        pile = next(obj for obj in self.room.contents.values() if obj not in (odd, bag))
        self.assertEqual((25, 6), (int(pile.value0), int(pile.value1)))
        self.assertEqual(30, int(bag.contains[0].value0))

    def test_missing_money_prototype_does_not_destroy_existing_money(self):
        old = self.money(2)
        self.room.contents[old.id] = old
        self.prototypes.clear()
        with self.assertRaises(KeyError):
            self.drop("10 silver")
        self.assertEqual(100, self.actor.silver)
        self.assertIs(old, self.room.contents[old.id])

    def test_pickup_splits_only_new_money_and_keeps_remainders(self):
        ally = self.member()
        payload = self.pickup(9, 5)
        self.assertEqual((105, 23), (self.actor.silver, self.actor.gold))
        self.assertEqual((4, 2), (ally.silver, ally.gold))
        self.assertEqual({}, self.room.contents)
        self.assertEqual([], self.actor.loot)
        split = payload["payloads"][1]["payloads"][0]
        self.assertEqual(ally.id, split["target_messages"][0]["id"])
        self.assertIn("Your share is 5 silver", split["to_char"])
        self.assertIn("4 silver and 2 gold", split["target_messages"][0]["text"])

    def test_pickup_excludes_charmed_and_ungrouped_but_includes_mobile_members(self):
        charmed = self.member("charmed", charmed=True)
        outsider = self.member("outsider", leader=object())
        mob = self.member("mob")
        self.room.mobiles = {mob.id: self.room.characters.pop(mob.id)}
        self.pickup(8)
        self.assertEqual((104, 4, 0, 0), (self.actor.silver, mob.silver, charmed.silver, outsider.silver))

    def test_pickup_with_only_charmed_member_does_not_invoke_split(self):
        self.member(charmed=True)
        self.assertNotIn("payloads", self.pickup(8))
        self.assertEqual(108, self.actor.silver)

    def test_disabled_autosplit_single_silver_and_too_small_share(self):
        ally = self.member()
        self.assertNotIn("payloads", self.pickup(1))
        payload = self.pickup(0, 1)
        self.assertIn("cheapskate", payload["payloads"][1]["payloads"][0]["to_char"])
        self.assertEqual((101, 21, 0), (self.actor.silver, self.actor.gold, ally.gold))
        self.actor.status_flags.act = 0
        self.assertNotIn("payloads", self.pickup(8))
        self.assertEqual(109, self.actor.silver)

    def test_container_pickup_and_bulk_pickup_preserve_split_payloads(self):
        ally = self.member()
        bag = self.base.bag()
        self.pickup(6, container=bag)
        self.assertEqual([], bag.contains)
        piles = [self.money(4), self.money(8)]
        self.room.contents = {p.id: p for p in piles}
        payload = self.commands._get_many(self.actor, self.room, self.context("get", "all"), piles)
        self.assertEqual(2, len(payload["payloads"]))
        self.assertTrue(all("payloads" in entry for entry in payload["payloads"]))
        self.assertEqual((109, 9), (self.actor.silver, ally.silver))

    def test_automatic_split_needs_no_command_or_player_handler_in_parent_context(self):
        ally = self.member()
        self.actor.silver += 8
        context = NS(character=self.actor, room=self.room)
        payload = self.commands._autosplit(self.actor, self.room, context, 8)
        self.assertEqual((104, 4), (self.actor.silver, ally.silver))
        self.assertIsNone(payload["context"].handler_service)
        self.assertEqual("split", payload["context"].command.name)

    def test_sacrifice_splits_reward_before_room_notice(self):
        ally = self.member()
        item = self.base.item("idol", level=9, cost=100)
        self.room.contents[item.id] = item
        reward = RealItemUtil.sacrifice_silver_value(item)
        payload = self.commands.do_sacrifice(self.actor, self.context("sacrifice", "idol"))
        self.assertEqual(100 + reward // 2 + reward % 2, self.actor.silver)
        self.assertEqual(reward // 2, ally.silver)
        self.assertIn("to_char", payload["payloads"][0])
        self.assertIn("to_room", payload["payloads"][2])
        self.assertEqual({}, self.room.contents)

    def test_sacrifice_counts_charmed_members_then_split_excludes_them(self):
        ally = self.member(charmed=True)
        item = self.base.item("idol", level=9, cost=100)
        self.room.contents[item.id] = item
        payload = self.commands.do_sacrifice(self.actor, self.context("sacrifice", "idol"))
        self.assertEqual("Just keep it all.\r\n", payload["payloads"][1]["payloads"][0]["to_char"])
        self.assertEqual(0, ally.silver)


if __name__ == "__main__":
    unittest.main()

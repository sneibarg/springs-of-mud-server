import importlib.util
import sys
import unittest
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_combat_handler_aggression as fixtures


ROOT = Path(__file__).resolve().parents[1]
Runtime = sys.modules[fixtures.FightHandler.__module__]


def _item_class():
    spec = importlib.util.spec_from_file_location("_corpse_currency_item", ROOT / "src/item/Item.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.Item


Item = _item_class()


class TestCorpseCurrency(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.room = SimpleNamespace(add_item_to_room=Mock())
        self.handler = self.fixtures._handler(self.room)
        self.handler.item_registry = SimpleNamespace(get=Mock(return_value=object()))
        self.handler.WellKnownObjectVnums = SimpleNamespace(
            OBJ_VNUM_CORPSE_PC=SimpleNamespace(value=11), OBJ_VNUM_CORPSE_NPC=SimpleNamespace(value=10))
        self.handler.PlayerActBits = SimpleNamespace(PLR_CANLOOT=8)
        self.money_factory = Mock(side_effect=lambda gold, silver, *_args: SimpleNamespace(gold=gold, silver=silver))
        self.object_factory = Mock(side_effect=lambda _prototype: Item.from_json(self._document()))
        patcher = patch.object(Runtime, "ItemUtil", SimpleNamespace(create_money=self.money_factory,
                                                                   create_object=self.object_factory))
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch.object(Runtime.CharacterApi, "unset_act_flags", create=True,
                               side_effect=lambda entity, bit: setattr(entity.status_flags, "act", entity.status_flags.act & ~int(bit)))
        self.unset_flags = patcher.start()
        self.addCleanup(patcher.stop)

    @staticmethod
    def _document():
        return {
            "id": "corpse", "areaId": "area", "vnum": "11", "name": "corpse",
            "shortDescription": "the corpse of %s", "longDescription": "The corpse of %s is lying here.",
            "material": "flesh", "itemType": "pc_corpse", "extraFlags": "0", "wearFlags": "1",
            "value0": "0", "value1": "0", "value2": "0", "value3": "0", "value4": "0",
            "condition": "G", "level": 0, "weight": 1, "cost": 100, "affectData": [], "contains": [],
            "owner": "prototype owner",
        }

    def _victim(self, guild, gold, silver, *, npc=False):
        victim = self.fixtures._mob("victim") if npc else self.fixtures._player("victim")
        victim.name, victim.guild = "Victim", guild
        victim.gold, victim.silver = gold, silver
        victim.status_flags.act = 8 | 128
        victim.owned_items = lambda: []
        return victim

    def _corpse(self, victim):
        self.handler.make_corpse(victim, self.room)
        return self.room.add_item_to_room.call_args.args[0]

    def test_nonclan_players_keep_all_money_and_own_the_corpse(self):
        for guild in ("", "none", "clanless"):
            with self.subTest(guild=guild):
                victim = self._victim(guild, 101, 103)
                corpse = self._corpse(victim)
                self.assertEqual((101, 103), (victim.gold, victim.silver))
                self.assertEqual("Victim", corpse.owner)
                self.assertEqual([], corpse.contains)
                self.assertEqual(128, victim.status_flags.act)
                self.assertEqual("the corpse of Victim", corpse.short_description)
                self.assertEqual(0, corpse.cost)
                self.assertEqual(victim.level, corpse.level)
                self.assertTrue(25 <= corpse.timer <= 40)
        self.money_factory.assert_not_called()
        self.handler.item_registry.get.assert_called_with(vnum="11")

    def test_clan_players_deposit_integer_halves_and_retain_odd_remainders(self):
        for guild in ("rom", "loner", "independent"):
            for gold, silver in ((100, 100), (101, 103), (1, 2), (2, 1), (0, 7), (7, 0)):
                with self.subTest(guild=guild, gold=gold, silver=silver):
                    victim = self._victim(guild, gold, silver)
                    self.money_factory.reset_mock()
                    corpse = self._corpse(victim)
                    money = corpse.contains[0]
                    self.assertEqual((gold // 2, silver // 2), (money.gold, money.silver))
                    self.assertEqual((gold - gold // 2, silver - silver // 2), (victim.gold, victim.silver))
                    self.assertEqual((gold, silver), (money.gold + victim.gold, money.silver + victim.silver))
                    self.assertIs(type(victim.gold), int)
                    self.assertIs(type(victim.silver), int)
                    self.assertIsNone(corpse.owner)
                    self.assertEqual(128, victim.status_flags.act)
                    self.money_factory.assert_called_once_with(gold // 2, silver // 2,
                                                               self.handler.item_registry, self.handler.WellKnownObjectVnums)

    def test_small_clan_balances_do_not_create_zero_value_money(self):
        for gold, silver in ((0, 0), (1, 0), (0, 1), (1, 1)):
            with self.subTest(gold=gold, silver=silver):
                victim = self._victim("rom", gold, silver)
                corpse = self._corpse(victim)
                self.assertEqual((gold, silver), (victim.gold, victim.silver))
                self.assertEqual([], corpse.contains)
                self.assertIsNone(corpse.owner)
        self.money_factory.assert_not_called()

    def test_npc_currency_gate_timers_and_flags_keep_rom_behavior(self):
        for gold, silver in ((5, 7), (1, 0), (0, 7), (0, 0)):
            with self.subTest(gold=gold, silver=silver):
                victim = self._victim("", gold, silver, npc=True)
                self.money_factory.reset_mock()
                corpse = self._corpse(victim)
                self.assertIsNone(corpse.owner)
                self.assertTrue(3 <= corpse.timer <= 6)
                self.assertEqual(136, victim.status_flags.act)
                if gold:
                    self.assertEqual((gold, silver), (corpse.contains[0].gold, corpse.contains[0].silver))
                    self.assertEqual((0, 0), (victim.gold, victim.silver))
                else:
                    self.assertEqual([], corpse.contains)
                    self.assertEqual((gold, silver), (victim.gold, victim.silver))
                    self.money_factory.assert_not_called()
        self.unset_flags.assert_not_called()
        self.handler.item_registry.get.assert_called_with(vnum="10")

    def test_owner_is_optional_and_survives_nested_item_round_trip(self):
        document = self._document()
        document.pop("owner")
        self.assertIsNone(Item.from_json(document).owner)
        document["owner"] = "Victim"
        owned = Item.from_json(document)
        container = Item.from_json(self._document())
        container.contains = [owned]
        restored = Item.from_json(asdict(container))
        self.assertEqual("Victim", restored.contains[0].owner)
        self.assertEqual("prototype owner", restored.owner)


if __name__ == "__main__":
    unittest.main()

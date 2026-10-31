"""OUTFIT instance values using bundled prototypes and actual equipment/shop rules."""
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace as NS

from tests.test_movement_rules_parity import MovementFixture
from area.Shop import Shop
from devtools.collection_query import load_collections
from item.ItemFactory import ItemFactory
from interp.commands.Object import Object


class OutfitValueTests(MovementFixture, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        data = load_collections(Path(__file__).resolve().parents[1] / 'resources/collections', ['items'])
        cls.item_documents = [d for d in data['items'].documents
                         if str(d['vnum']) in ('3701', '3702', '3703', '3704', '3706', '3716')]

    def setUp(self):
        super().setUp()
        self.actor.level = 1
        self.prototypes = {}
        for document in self.item_documents:
            data = deepcopy(document)
            data['id'] = data.pop('_id')['$oid']
            data.pop('_class', None)
            self.prototypes[str(data['vnum'])] = ItemFactory.from_data(data, {}, self.skill_registry)
        self.commands = Object.__new__(Object)
        self.commands.item_registry = NS(get_or_none=lambda **kw: self.prototypes.get(str(kw['vnum'])))
        self.commands.well_known_object_vnums = self.enums.get('wellKnownObjectVnums')
        self.commands.wear_flags = self.enums.get('wearFlags')
        self.commands.item_flags = self.enums.get('itemFlags')
        self.commands.effect_handler, self.commands.interp_api = self.effects, self.api

    def outfit(self):
        context = self.ctx('outfit')
        self.commands.do_outfit(self.actor, context)
        self.assertTrue(context.done)
        return {str(item.vnum): item for item in self.actor.owned_items() if str(item.vnum) in self.prototypes}

    def test_free_grants_are_valueless_but_prototypes_and_weapon_keep_cost(self):
        original = {vnum: item.cost for vnum, item in self.prototypes.items()}
        issued = self.outfit()
        for vnum in ('3716', '3703', '3704'):
            self.assertEqual(0, issued[vnum].cost)
        weapon_vnum = self.commands._outfit_weapon_vnum(self.actor)
        self.assertEqual(original[weapon_vnum], issued[weapon_vnum].cost)
        self.assertEqual(original, {vnum: item.cost for vnum, item in self.prototypes.items()})

    def test_repeated_outfit_does_not_change_already_owned_gear(self):
        issued = self.outfit()
        issued['3703'].cost = 999
        again = self.outfit()
        self.assertEqual({key: id(value) for key, value in issued.items()},
                         {key: id(value) for key, value in again.items()})
        self.assertEqual(999, again['3703'].cost)

    def test_free_vest_has_no_merchant_value_while_prototype_has_value(self):
        types, flags = self.enums.get('itemTypes'), self.enums.get('itemFlags')
        shop = Shop(id='shop', area_id='area', comment='', keeper=1,
                    buy_type0=int(types.ITEM_ARMOR), buy_type1=0, buy_type2=0, buy_type3=0, buy_type4=0,
                    profit_buy=100, profit_sell=50, open_hour=0, close_hour=23)
        issued = self.outfit()
        self.assertEqual(0, shop.sell_price(issued['3703'], [], types, flags))
        self.assertGreater(shop.sell_price(self.prototypes['3703'], [], types, flags), 0)


if __name__ == '__main__':
    unittest.main()

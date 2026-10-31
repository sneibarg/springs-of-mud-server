import unittest

from tests.test_movement_rules_parity import MovementFixture, item
from api.ItemApi import ItemApi
from interp.commands.Info import Info


class CompareParityTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.info = Info.__new__(Info)
        self.info.room_registry = self.rooms
        self.info.interp_api = self.api

    def compare(self, text):
        return self.info.do_compare(self.actor, self.ctx('compare', text))

    def carried(self, name, **values):
        obj = item(name, **values)
        self.actor.loot.append(obj)
        return obj

    def test_new_and_old_weapon_values_and_mixed_format_ranking(self):
        alpha = self.carried('alpha', itemType='weapon', value1='2', value2='6')
        beta = self.carried('beta', itemType='weapon', value1='1', value2='9')
        self.assertEqual(14, ItemApi.compare_value(alpha))
        self.assertEqual(10, ItemApi.compare_value(beta))
        self.assertIn('better than', self.compare('alpha beta'))
        alpha.new_format = False
        self.assertEqual(8, ItemApi.compare_value(alpha))
        self.assertIn('worse than', self.compare('alpha beta'))
        beta.new_format = False
        self.assertEqual(10, ItemApi.compare_value(beta))

    def test_armor_sums_three_physical_values_and_ignores_exotic(self):
        alpha = self.carried('alpha', itemType='armor', value0='1', value1='10', value2='10', value3='0')
        self.carried('beta', itemType='armor', value0='5', value1='1', value2='1', value3='999')
        self.assertEqual(21, ItemApi.compare_value(alpha))
        self.assertIn('better than', self.compare('alpha beta'))

    def test_no_rounding_tie_for_low_damage_weapons(self):
        self.carried('alpha', itemType='weapon', value1='1', value2='2')
        self.carried('beta', itemType='weapon', value1='1', value2='3')
        self.assertIn('worse than', self.compare('alpha beta'))

    def test_implicit_equipment_requires_visibility_and_shared_wear_location(self):
        flags = self.enums.get('wearFlags')
        source = self.carried('ring', itemType='armor', wearFlags=int(flags.ITEM_TAKE | flags.ITEM_WEAR_FINGER))
        vest = item('vest', itemType='armor', wearFlags=int(flags.ITEM_TAKE | flags.ITEM_WEAR_BODY))
        self.actor.equip_item(vest, 'torso')
        self.assertIn("aren't wearing anything comparable", self.compare('ring'))
        worn = item('band', itemType='armor', wearFlags=int(flags.ITEM_TAKE | flags.ITEM_WEAR_FINGER),
                    extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))
        self.actor.equip_item(worn, 'finger1')
        self.assertIn("aren't wearing anything comparable", self.compare('ring'))
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        self.assertIs(worn, ItemApi.find_comparable_equipped_item(self.actor, source, room=self.room))
        self.assertIn('band', self.compare('ring'))

    def test_named_operands_are_visible_unworn_inventory(self):
        source = self.carried('alpha', itemType='armor')
        worn = item('beta', itemType='armor')
        self.actor.equip_item(worn, 'torso')
        self.assertIn('do not have', self.compare('alpha beta'))
        self.assertIn('do not have', self.compare('beta alpha'))
        source.extra_flags = int(self.enums.get('itemFlags').ITEM_INVIS)
        self.assertIn('do not have', self.compare('alpha'))

    def test_numbered_inventory_lookup_and_equality(self):
        self.carried('sword first', itemType='weapon', value1='1', value2='1')
        self.carried('sword second', itemType='weapon', value1='2', value2='6')
        self.carried('axe', itemType='weapon', value1='2', value2='6')
        self.assertIn('about the same', self.compare('2.sword axe'))

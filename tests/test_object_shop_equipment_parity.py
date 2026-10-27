"""ROM24 shop object visibility, paired-slot fallback, and wield capacity."""
import sys
import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock
from tests import test_object_haggle_parity as haggle
from tests.test_object_loot_and_sacrifice_parity import RealItemApi

h = haggle.h
ObjectModule = sys.modules[h.Object.__module__]


class TestShopEquipmentParity(unittest.TestCase):
    def setUp(self):
        self.base = haggle.TestObjectHaggleParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.keeper, self.shop = self.base.keeper, self.base.shop
        self.swap = self.base.base.swap
        self.enums = self.base.base.enums
        self.swap(RealItemApi, "get_enum", side_effect=self.enums.__getitem__)
        for module in (ObjectModule, sys.modules[h.InterpApi.__module__]):
            self.swap(module, "ItemApi", new=RealItemApi)
        self.keeper.is_npc = True
        self.keeper.status_flags = NS(act=0, affected_by=0)
        self.actor.status_flags.affected_by = 0
        self.room.is_room_dark = lambda: False
        self.swap(ObjectModule.CharacterApi, "get_enum", side_effect=self.enums.__getitem__)
        self.swap(ObjectModule.CharacterApi, "is_affected", create=True,
                  side_effect=lambda ch, bit: bool(ch.status_flags.affected_by & bit))
        self.actor.character_attributes.strength = 10
        self.bonus = self.swap(ObjectModule.CharacterApi, "get_attribute_bonus", create=True,
                               side_effect=lambda attr, value: {"wield": int(value)})
        self.commands.container_state = self.enums["containerState"]
        self.commands.effect_handler = NS(remove_item_effects=Mock(), apply_item_effects=Mock())

    def item(self, name="sword", **kw):
        return self.base.item(name, **kw)

    def command(self, name, raw):
        return self.base.command(name, raw)[0]

    def test_sell_and_value_reject_equipped_items_without_removal_or_roll(self):
        item = self.item(extra_flags=str(self.enums["itemFlags"].ITEM_NOREMOVE.value))
        self.actor.loot.append(item)
        self.actor.equip_item(item, "wielded")
        for command in ("sell", "value"):
            payload = self.command(command, "sword")
            self.assertEqual("You don't have that item.\r\n", payload["to_char"])
            self.assertIs(item, self.actor.equipped.wielded)
        self.commands.effect_handler.remove_item_effects.assert_not_called()
        self.base.roll.assert_not_called()

    def test_inventory_wear_metadata_is_also_excluded(self):
        item = self.item()
        item.wear_loc = 16
        self.actor.loot.append(item)
        for command in ("sell", "value"):
            self.assertEqual("target_missing", self.command(command, "sword")["blocked_key"])
        self.assertIn(item, self.actor.loot)

    def test_keeper_must_see_normalized_invisible_item(self):
        self.actor.status_flags.affected_by = self.enums["affectedBy"].AFF_DETECT_INVIS.value
        for flag in (str(self.enums["itemFlags"].ITEM_INVIS.value), "F"):
            item = self.item(extra_flags=flag)
            self.actor.loot.append(item)
            for command in ("sell", "value"):
                payload = self.command(command, "sword")
                self.assertEqual("keeper_cannot_see_item", payload["blocked_key"])
                self.assertEqual("the shopkeeper doesn't see what you are offering.\r\n", payload["to_char"])
                self.assertIn(item, self.actor.loot)
            self.actor.loot.remove(item)
        self.base.roll.assert_not_called()
        self.base.improve.assert_not_called()

    def test_actor_must_see_item_before_keeper_check(self):
        item = self.item(extra_flags=str(self.enums["itemFlags"].ITEM_INVIS.value))
        self.actor.loot.append(item)
        self.keeper.status_flags.affected_by = self.enums["affectedBy"].AFF_DETECT_INVIS.value
        for command in ("sell", "value"):
            self.assertEqual("target_missing", self.command(command, "sword")["blocked_key"])

    def test_visibility_and_curse_guard_order_differs_between_sell_and_value(self):
        item = self.item(extra_flags=str(self.enums["itemFlags"].ITEM_INVIS.value | self.enums["itemFlags"].ITEM_NODROP.value))
        self.actor.loot.append(item)
        self.actor.status_flags.affected_by = self.enums["affectedBy"].AFF_DETECT_INVIS.value
        self.assertEqual("can_t_let_go", self.command("sell", "sword")["blocked_key"])
        self.assertEqual("keeper_cannot_see_item", self.command("value", "sword")["blocked_key"])

    def test_visible_unworn_item_can_be_quoted_and_sold(self):
        item = self.item(extra_flags=str(self.enums["itemFlags"].ITEM_INVIS.value))
        self.actor.loot.append(item)
        for ch in (self.actor, self.keeper):
            ch.status_flags.affected_by = self.enums["affectedBy"].AFF_DETECT_INVIS.value
        self.assertIn("50 silver", self.command("value", "sword")["to_char"])
        self.command("sell", "sword")
        self.assertNotIn(item, self.actor.loot)
        self.assertIn(item, self.keeper.inventory)

    def test_shop_lookup_skips_hidden_matches_and_supports_numbered_keywords(self):
        hidden = self.item("steel sword", extra_flags=str(self.enums["itemFlags"].ITEM_INVIS.value))
        first = self.item("iron sword")
        second = self.item("bronze sword")
        self.actor.loot.extend([hidden, first, second])
        ctx = self.base.base.fixture._build_context("2.swo", self.room, self.actor, "value")
        self.commands._prepare_value_context(self.actor, ctx)
        self.assertIs(second, ctx.value_item)

    def pair(self, slots, flag, cursed_first=True, cursed_second=False):
        first = self.item("first", item_type="armor", wear_flags=str(flag),
                          extra_flags=str(self.enums["itemFlags"].ITEM_NOREMOVE.value if cursed_first else 0))
        second = self.item("second", item_type="armor", wear_flags=str(flag),
                           extra_flags=str(self.enums["itemFlags"].ITEM_NOREMOVE.value if cursed_second else 0))
        new = self.item("new", item_type="armor", wear_flags=str(flag))
        self.actor.loot.extend([first, second, new])
        self.actor.equip_item(first, slots[0])
        self.actor.equip_item(second, slots[1])
        return first, second, new

    def test_all_paired_slots_fall_back_after_cursed_first_slot_and_preserve_messages(self):
        for slots, name in [(('finger1','finger2'),'ITEM_WEAR_FINGER'), (('neck1','neck2'),'ITEM_WEAR_NECK'), (('wrist1','wrist2'),'ITEM_WEAR_WRIST')]:
            with self.subTest(slots=slots):
                first, second, new = self.pair(slots, self.enums["wearFlags"][name].value)
                payload = self.command("wear", "new")
                self.assertIs(first, getattr(self.actor.equipped, slots[0]))
                self.assertIs(new, getattr(self.actor.equipped, slots[1]))
                self.assertIn(second, self.actor.loot)
                self.assertNotIn("blocked_key", payload)
                text = payload["to_char"]
                self.assertLess(text.index("first"), text.index("second"))
                self.assertLess(text.index("second"), text.index("new"))
                self.commands.effect_handler.remove_item_effects.assert_called_with(self.actor, second)
                self.commands.effect_handler.apply_item_effects.assert_called_with(self.actor, new)
                self.actor.loot.remove(second)

    def test_both_cursed_slots_report_both_failures_and_preserve_equipment(self):
        first, second, new = self.pair(('finger1','finger2'), self.enums["wearFlags"].ITEM_WEAR_FINGER.value, cursed_second=True)
        payload = self.command("wear", "new")
        self.assertEqual("noRemove", payload["blocked_key"])
        self.assertIn("first", payload["to_char"])
        self.assertIn("second", payload["to_char"])
        self.assertLess(payload["to_char"].index("first"), payload["to_char"].index("second"))
        self.assertIs(first, self.actor.equipped.finger1)
        self.assertIs(second, self.actor.equipped.finger2)
        self.assertIn(new, self.actor.loot)
        self.commands.effect_handler.remove_item_effects.assert_not_called()

    def test_wear_all_does_not_replace_and_empty_pair_slot_needs_no_removal(self):
        first, second, new = self.pair(('finger1','finger2'), self.enums["wearFlags"].ITEM_WEAR_FINGER.value)
        self.command("wear", "all")
        self.assertIn(new, self.actor.loot)
        self.assertIs(second, self.actor.equipped.finger2)
        self.actor.unequip_item("finger2")
        self.command("wear", "new")
        self.assertIs(new, self.actor.equipped.finger2)
        self.commands.effect_handler.remove_item_effects.assert_not_called()

    def test_wield_uses_strength_row_recursive_weight_and_exact_boundary(self):
        item = self.item(weight=99, contains=[self.item("child", weight=2)])
        self.assertTrue(item.weapon_too_heavy(self.actor))
        self.bonus.assert_called_with("strength", "10")
        item.weight = 98
        self.assertFalse(item.weapon_too_heavy(self.actor))
        self.actor.character_attributes.strength = 11
        item.weight = 108
        self.assertFalse(item.weapon_too_heavy(self.actor))
        item.weight = 109
        self.assertTrue(item.weapon_too_heavy(self.actor))
        self.bonus.assert_called_with("strength", "11")

    def test_wield_clamps_strength_and_keeps_npc_exemption(self):
        item = self.item(weight=31)
        self.actor.character_attributes.strength = -5
        self.assertTrue(item.weapon_too_heavy(self.actor))
        self.bonus.assert_called_with("strength", "3")
        self.actor.character_attributes.strength = 100
        item.weight = 250
        self.assertFalse(item.weapon_too_heavy(self.actor))
        self.bonus.assert_called_with("strength", "25")
        self.actor.is_npc = True
        item.weight = 10000
        self.assertFalse(item.weapon_too_heavy(self.actor))

    def test_zero_wield_allowance_rejects_positive_weight(self):
        self.bonus.side_effect = None
        self.bonus.return_value = {"wield": 0}
        self.assertTrue(self.item(weight=1).weapon_too_heavy(self.actor))

    def test_visibility_preserves_blind_potion_light_and_death_flag_ordering(self):
        blind = self.enums["affectedBy"].AFF_BLIND.value
        self.actor.status_flags.affected_by = blind
        self.assertTrue(RealItemApi.can_see_object(self.room, self.actor, self.item(item_type="potion")))
        self.assertFalse(RealItemApi.can_see_object(self.room, self.actor, self.item(item_type="light", value2="1")))
        self.actor.status_flags.affected_by = 0
        light = self.item(item_type="light", value2="1", extra_flags=str(self.enums["itemFlags"].ITEM_INVIS.value))
        self.assertTrue(RealItemApi.can_see_object(self.room, self.actor, light))
        light.extra_flags = str(self.enums["itemFlags"].ITEM_VIS_DEATH.value)
        self.assertFalse(RealItemApi.can_see_object(self.room, self.actor, light))

    def test_wield_checks_strength_after_previous_weapon_effects_are_removed(self):
        flag = self.enums["wearFlags"].ITEM_WIELD.value
        old = self.item("old", wear_flags=str(flag))
        new = self.item("new", wear_flags=str(flag), weight=101)
        self.actor.loot.extend([old, new])
        self.actor.equip_item(old, "wielded")
        self.actor.character_attributes.strength = 20
        self.commands.effect_handler.remove_item_effects.side_effect = lambda actor, item: setattr(actor.character_attributes, "strength", 10)
        payload = self.command("wield", "new")
        self.assertEqual("tooHeavy", payload["blocked_key"])
        self.assertIsNone(self.actor.equipped.wielded)
        self.assertIn(old, self.actor.loot)
        self.assertIn(new, self.actor.loot)
        self.commands.effect_handler.apply_item_effects.assert_not_called()


if __name__ == "__main__":
    unittest.main()

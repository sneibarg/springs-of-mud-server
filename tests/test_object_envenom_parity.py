"""Normalized weapon damage eligibility and ROM24 envenom training/lifetime."""
import sys
import unittest
from types import SimpleNamespace as NS
from tests import test_object_container_shop_spell_parity as fixtures
from tests.test_object_loot_and_sacrifice_parity import RealItemUtil

h = fixtures.h
ObjectModule = sys.modules[h.Object.__module__]


class TestObjectEnvenomParity(unittest.TestCase):
    def setUp(self):
        self.base = fixtures.TestObjectContainerShopSpellParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.enums = self.base.enums
        self.commands.weapon_type = self.enums["weaponType"]
        self.actor.level = 10
        self.actor.skill_level = lambda name: 80
        self.actor.status_flags.pulse_wait = 0
        self.skill = NS(id="envenom-id", beats=24)
        self.commands.skill_registry = NS(get_or_none=lambda **kw: self.skill if kw.get("name") == "envenom" else None)
        self.roll = self.base.swap(ObjectModule.random, "randint", return_value=1)
        self.improve = self.base.swap(ObjectModule.Ability, "check_improve")
        self.base.swap(ObjectModule.CharacterApi, "get_enum", side_effect=self.enums.__getitem__)
        effects = self.base.base.effects
        effects.where_enum = self.enums["whereAffect"]
        effects.weapon_type = self.enums["weaponType"]
        self.commands.effect_handler = effects

    def weapon(self, attack="pierce", **kwargs):
        # Exercise the actual normalization step that turns attack names into damage categories.
        data = {"value3": attack}
        RealItemUtil.attack_type(self.enums["damageTypes"], data)
        values = dict(item_type="weapon", value3=attack, damage_type=data["damage_type"], value4="0")
        values.update(kwargs)
        return self.base.item("weapon", **values)

    def envenom(self, item):
        if item not in self.actor.loot:
            self.actor.loot.append(item)
        ctx = self.base.fixture._build_context(item.name, self.room, self.actor, "envenom")
        result = self.commands.do_envenom(self.actor, ctx)
        self.assertTrue(ctx.done)
        return result

    def test_normalized_bash_attacks_are_rejected_without_wait_roll_or_learning(self):
        for attack in ("pound", "crush", "blast", "peckb", "thwack"):
            with self.subTest(attack=attack):
                item = self.weapon(attack)
                self.assertEqual(self.enums["damageTypes"].DAM_BASH.value, item.damage_type)
                result = self.envenom(item)
                self.assertEqual("You can only envenom edged weapons.\r\n", result["to_char"])
                self.assertEqual("0", item.value4)
                self.assertFalse(item.effects)
                self.assertEqual(0, self.actor.status_flags.pulse_wait)
                self.actor.loot.remove(item)
        self.roll.assert_not_called()
        self.improve.assert_not_called()

    def test_normalized_non_bash_categories_are_allowed_including_elemental_attacks(self):
        for attack in ("slash", "pierce", "flame", "chill", "shock", "divine"):
            with self.subTest(attack=attack):
                item = self.weapon(attack)
                result = self.envenom(item)
                self.assertIn("You coat", result["to_char"])
                self.assertTrue(int(item.value4) & self.enums["weaponType"].WEAPON_POISON.value)
                self.assertEqual(1, len(item.effects))
                self.actor.loot.remove(item)

    def test_numeric_string_and_enum_damage_categories_reject_bash(self):
        for value in (self.enums["damageTypes"].DAM_BASH, str(self.enums["damageTypes"].DAM_BASH.value)):
            self.assertFalse(self.commands._is_edged_weapon(self.weapon(damage_type=value)))
        for value in (self.enums["damageTypes"].DAM_PIERCE, str(self.enums["damageTypes"].DAM_PIERCE.value)):
            self.assertTrue(self.commands._is_edged_weapon(self.weapon(damage_type=value)))

    def test_negative_attack_index_is_rejected_independently_of_damage_category(self):
        item = self.weapon(value3="-1")
        self.assertIn("only envenom edged", self.envenom(item)["to_char"])
        self.roll.assert_not_called()
        self.improve.assert_not_called()

    def test_text_damage_fallback_rejects_bash_and_accepts_pierce(self):
        for name in ("bash", "DAM_BASH", "pound", "blast"):
            self.assertFalse(self.commands._is_edged_weapon(self.weapon(damage_type=name)))
        self.assertTrue(self.commands._is_edged_weapon(self.weapon(damage_type="pierce")))

    def test_weapon_poison_can_have_zero_duration_and_uses_training_multiplier_three(self):
        item = self.weapon()
        self.actor.level = 1
        self.envenom(item)
        effect = item.effects[0]
        self.assertEqual((0, 0), (effect.level, effect.duration))
        self.assertEqual(24, self.actor.status_flags.pulse_wait)
        self.improve.assert_called_once_with(self.actor, "envenom-id", True, 3)
        tick = self.commands.effect_handler.tick_effects(item)
        self.assertEqual([effect], tick.expired_effects)
        self.assertEqual([], item.effects)
        self.assertFalse(int(item.value4) & self.enums["weaponType"].WEAPON_POISON.value)

    def test_weapon_duration_keeps_integer_operation_order(self):
        self.actor.level = 11
        self.roll.return_value = 60
        item = self.weapon()
        self.envenom(item)
        self.assertEqual((6, 3), (item.effects[0].level, item.effects[0].duration))
        self.roll.assert_called_once_with(1, 100)

    def test_failed_weapon_attempt_uses_multiplier_three_and_no_effect(self):
        self.roll.return_value = 80  # strict below-skill threshold
        item = self.weapon()
        self.assertIn("fail to envenom", self.envenom(item)["to_char"])
        self.assertFalse(item.effects)
        self.assertEqual("0", item.value4)
        self.assertEqual(24, self.actor.status_flags.pulse_wait)
        self.improve.assert_called_once_with(self.actor, "envenom-id", False, 3)

    def test_food_and_drink_success_uses_multiplier_four(self):
        for kind in ("food", "drink"):
            with self.subTest(kind=kind):
                self.improve.reset_mock()
                item = self.base.item(kind, item_type=kind, value3="0")
                self.envenom(item)
                self.assertEqual("1", item.value3)
                self.improve.assert_called_once_with(self.actor, "envenom-id", True, 4)

    def test_failed_food_uses_multiplier_four_but_already_poisoned_food_never_learns(self):
        self.roll.return_value = 80
        item = self.base.item("food", item_type="food", value3="0")
        self.assertIn("fail to poison", self.envenom(item)["to_char"])
        self.improve.assert_called_once_with(self.actor, "envenom-id", False, 4)
        self.improve.reset_mock()
        item.value3 = "1"
        self.envenom(item)
        self.roll.return_value = 1
        self.envenom(item)
        self.improve.assert_not_called()
        self.assertEqual("1", item.value3)

    def test_enchanted_guard_precedes_bash_and_already_poisoned_checks(self):
        item = self.weapon("pound", value4=str(self.enums["weaponType"].WEAPON_POISON.value),
                           extra_flags=str(self.enums["itemFlags"].ITEM_BLESS.value))
        self.assertIn("can't seem to envenom", self.envenom(item)["to_char"])
        self.roll.assert_not_called()
        self.improve.assert_not_called()


if __name__ == "__main__":
    unittest.main()

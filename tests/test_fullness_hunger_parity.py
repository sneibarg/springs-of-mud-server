"""Independent ROM24 fullness/hunger consumption, decay, immunity, and persistence."""
import json
import sys
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
from tests import test_object_container_shop_spell_parity as fixtures
from tests.test_object_carry_limits_parity import Character

h = fixtures.h
StatusFlags = h._load_module("fullness_status_flags", "game/StatusFlags.py").StatusFlags
stubs = {name: NS(**{attr: object}) for name, attr in (
    ("player.CharacterRegistry", "CharacterRegistry"), ("server.FetchAndRegisterMixin", "FetchAndRegisterMixin"),
    ("server.ServiceConfig", "ServiceConfig"))}
stubs["requests"] = NS()
with patch.dict(sys.modules, stubs):
    CharacterService = h._load_module("fullness_character_service", "player/CharacterService.py").CharacterService
stubs = {name: NS(**{attr: object}) for name, attr in (
    ("api.WizApi", "WizApi"), ("game.WizHandler", "WizHandler"),
    ("player.CharacterAdvancement", "CharacterAdvancement"), ("util.AreaUtil", "AreaUtil"),
    ("util.WizUtil", "WizUtil"))}
with patch.dict(sys.modules, stubs):
    WizModule = h._load_module("fullness_wiz_set", "api/WizSetApi.py")


class TestFullnessHungerParity(unittest.TestCase):
    def setUp(self):
        self.base = fixtures.TestObjectContainerShopSpellParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.actor.status_flags = StatusFlags.default()
        self.actor.status_flags.hunger = self.actor.status_flags.fullness = 0
        self.actor.status_flags.thirst = 0
        self.actor.gain_condition = lambda name, amount: Character.gain_condition(self.actor, name, amount)
        self.actor.is_large_race = lambda: False

    def eat(self, *, full=2, hunger=3):
        item = self.base.item("food", item_type="food", value0=str(full), value1=str(hunger), value3="0")
        self.actor.loot.append(item)
        context = self.base.fixture._build_context("food", self.room, self.actor, "eat")
        return self.commands.do_eat(self.actor, context), item

    def drink(self, affect=None):
        item = self.base.item("bottle", item_type="drink", value0="10", value1="10", value2="water", value3="0",
                              liquid_affect_data=affect or [0, 2, 10, 3, 4])
        self.actor.loot.append(item)
        context = self.base.fixture._build_context("bottle", self.room, self.actor, "drink")
        return self.commands.do_drink(self.actor, context), item

    def test_food_increases_fullness_and_hunger_independently(self):
        payload, item = self.eat()
        self.assertEqual((2, 3), (self.actor.status_flags.fullness, self.actor.status_flags.hunger))
        self.assertIn("no longer hungry", payload["to_char"])
        self.assertNotIn(item, self.actor.loot)

    def test_drink_maps_all_four_liquid_condition_columns_separately(self):
        self.drink()
        self.assertEqual((0, 2, 4, 6), (self.actor.status_flags.drunk, self.actor.status_flags.fullness,
                                      self.actor.status_flags.thirst, self.actor.status_flags.hunger))

    def test_negative_liquid_gains_truncate_toward_zero_like_c(self):
        flags = self.actor.status_flags
        flags.drunk = flags.fullness = flags.thirst = flags.hunger = 10
        self.drink([-1, -1, -1, -1, 1])
        self.assertEqual((10, 10, 10, 10), (flags.drunk, flags.fullness, flags.thirst, flags.hunger))

    def test_food_limit_uses_fullness_not_hunger_and_has_strict_boundary(self):
        self.actor.status_flags.fullness, self.actor.status_flags.hunger = 41, 0
        payload, item = self.eat()
        self.assertIn("too full", payload["to_char"])
        self.assertIn(item, self.actor.loot)
        self.actor.loot.remove(item)
        self.actor.status_flags.fullness, self.actor.status_flags.hunger = 40, 48
        payload, item = self.eat()
        self.assertNotIn(item, self.actor.loot)
        self.assertEqual((42, 48), (self.actor.status_flags.fullness, self.actor.status_flags.hunger))
        self.assertIn("You are full", payload["to_char"])

    def test_drink_limit_uses_fullness_not_hunger_and_has_strict_boundary(self):
        self.actor.status_flags.fullness, self.actor.status_flags.hunger = 46, 0
        payload, item = self.drink()
        self.assertIn("too full", payload["to_char"])
        self.assertEqual("10", item.value1)
        self.actor.loot.remove(item)
        self.actor.status_flags.fullness, self.actor.status_flags.hunger = 45, 48
        payload, item = self.drink()
        self.assertEqual("6", item.value1)
        self.assertEqual((47, 48), (self.actor.status_flags.fullness, self.actor.status_flags.hunger))
        self.assertIn("You are full", payload["to_char"])

    def test_no_longer_hungry_message_takes_precedence_over_full(self):
        self.actor.status_flags.fullness = 40
        payload, item = self.eat()
        self.assertIn("no longer hungry", payload["to_char"])
        self.assertNotIn("You are full", payload["to_char"])

    def test_zero_fullness_gain_does_not_emit_hunger_warning(self):
        payload, item = self.eat(full=0, hunger=0)
        self.assertNotIn("hungry", payload["to_char"])
        self.assertEqual((0, 0), (self.actor.status_flags.fullness, self.actor.status_flags.hunger))

    def test_condition_ticks_decay_fullness_twice_as_fast_and_only_hunger_warns(self):
        flags = self.actor.status_flags
        flags.fullness, flags.hunger, flags.thirst, flags.drunk = 2, 1, 2, 1
        messages = Character.tick_conditions(self.actor)
        self.assertEqual((0, 0, 1, 0), (flags.fullness, flags.hunger, flags.thirst, flags.drunk))
        self.assertEqual(["You are sober.\r\n", "You are hungry.\r\n"], messages)
        self.actor.is_large_race = lambda: True
        flags.fullness, flags.hunger = 8, 5
        Character.tick_conditions(self.actor)
        self.assertEqual((4, 3), (flags.fullness, flags.hunger))

    def test_disabled_conditions_stay_independent_and_upper_bound_is_48(self):
        flags = self.actor.status_flags
        flags.fullness, flags.hunger = -1, 47
        self.eat(full=100, hunger=100)
        self.assertEqual((-1, 48), (flags.fullness, flags.hunger))
        flags.fullness, flags.hunger = 47, -1
        self.eat(full=100, hunger=100)  # fullness guard rejects before gains
        self.actor.gain_condition("fullness", 100)
        self.actor.gain_condition("hunger", 100)
        self.assertEqual((48, -1), (flags.fullness, flags.hunger))

    def test_npc_and_immortal_conditions_do_not_gain_or_decay(self):
        for field in ("is_npc", "is_immortal"):
            with self.subTest(field=field):
                setattr(self.actor, field, True)
                self.actor.gain_condition("fullness", 10)
                self.actor.gain_condition("hunger", 10)
                self.eat()
                self.drink()
                self.assertEqual([], Character.tick_conditions(self.actor))
                self.assertEqual((0, 0), (self.actor.status_flags.fullness, self.actor.status_flags.hunger))
                setattr(self.actor, field, False)

    def test_default_legacy_load_and_template_have_rom_fullness_default(self):
        self.assertEqual((48, 48), (StatusFlags.default().fullness, StatusFlags.default().hunger))
        legacy = StatusFlags.from_json({"hunger": 7, "thirst": 9})
        self.assertEqual((48, 7), (legacy.fullness, legacy.hunger))
        legacy.fullness = 2
        template = StatusFlags.from_template(legacy)
        self.assertEqual((48, 48), (template.fullness, template.hunger))

    def test_saved_fullness_and_hunger_round_trip_independently(self):
        flags = self.actor.status_flags
        flags.fullness, flags.hunger = 8, -1
        payload = CharacterService._serialize_value(flags)
        self.assertEqual((8, -1), (payload["fullness"], payload["hunger"]))
        restored = StatusFlags.from_json(json.loads(json.dumps(payload)))
        self.assertEqual((8, -1), (restored.fullness, restored.hunger))

    def test_hunger_not_fullness_controls_starvation_regeneration_penalty(self):
        entity = Character.__new__(Character)
        entity.is_npc = False
        entity.level, entity.hit, entity.max_hit = 10, 0, 100
        entity.character_attributes = NS(constitution=20, position=self.base.enums["positions"].POS_SLEEPING.value)
        entity.character_class = NS(hp_max=10)
        entity.status_flags = StatusFlags.default()
        entity._skill_percent = lambda name: 0
        positions = self.base.enums["positions"]
        context = NS(positions=positions, affected_bits=self.base.enums["affectedBy"],
                     rng=NS(number_percent=lambda: 100), position=lambda key: positions[key].value)
        room = NS(heal_rate=100)
        entity.status_flags.fullness, entity.status_flags.hunger = 0, 48
        baseline = entity.hit_gain(room, context)
        entity.status_flags.fullness = 48
        self.assertEqual(baseline, entity.hit_gain(room, context))
        entity.status_flags.hunger = 0
        self.assertEqual(baseline // 2, entity.hit_gain(room, context))

    def test_administrator_full_setting_changes_fullness_only(self):
        api = WizModule.WizSetApi.__new__(WizModule.WizSetApi)
        api.character_registry = api.room_registry = NS()
        self.base.swap(WizModule, "WizUtil", new=NS(find_world_entity=lambda *args: self.actor))
        context = self.base.fixture._build_context("", self.room, self.actor)
        api._set_mobile(context, "Tester full 12")
        self.assertEqual((12, 0), (self.actor.status_flags.fullness, self.actor.status_flags.hunger))
        api._set_mobile(context, "Tester hunger 7")
        self.assertEqual((12, 7), (self.actor.status_flags.fullness, self.actor.status_flags.hunger))


if __name__ == "__main__":
    unittest.main()

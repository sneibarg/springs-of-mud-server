"""Pill casting and ingested poison, derived from ROM24 act_obj.c."""
import sys
import unittest
from enum import IntEnum
from types import SimpleNamespace as NS
from unittest.mock import patch

from tests import test_object_get_dynamic_commands as h


EffectUtil = h._load_module("consumption_effect_util", "util/EffectUtil.py").EffectUtil
with patch.dict(sys.modules, {"util.EffectUtil": NS(EffectUtil=EffectUtil)}):
    EffectHandler = h._load_module("consumption_effect_handler", "item/EffectHandler.py").EffectHandler
    SpellApi = h._load_module("consumption_spell_api", "api/SpellApi.py").SpellApi
RNG = h._load_module("consumption_rng", "game/RandomNumberGenerator.py").RandomNumberGenerator


class Where(IntEnum):
    TO_AFFECTS = 0
    TO_OBJECT = 1
    TO_WEAPON = 5


class Apply(IntEnum):
    APPLY_NONE = 0


class Affected(IntEnum):
    AFF_POISON = 4096


class TestObjectConsumptionParity(unittest.TestCase):
    def setUp(self):
        self.fixture = h.TestObjectGetDynamicCommands()
        self.actor = self.fixture._build_character()
        self.actor.effects = []
        self.actor.status_flags.hunger = 0
        self.actor.status_flags.fullness = 0
        self.actor.status_flags.thirst = 0
        self.actor.status_flags.drunk = 0
        self.actor.status_flags.affected_by = 0
        self.actor.status_flags.assign_bitfield = lambda name, value: setattr(self.actor.status_flags, name, value)
        self.room = h._Room(id="room-1", contents={}, characters={})
        self.witness = NS(id="witness")
        self.room.characters[self.witness.id] = self.witness
        self.commands = self.fixture._commands(self.room)
        enums = {"whereAffect": Where, "applyTypes": Apply, "affectedBy": Affected,
                 "itemFlags": IntEnum("ItemFlags", {}), "weaponType": IntEnum("WeaponType", {})}
        self.effects = EffectHandler(NS(get=enums.__getitem__))
        self.commands.effect_handler = self.effects
        self.commands.spell_api = SpellApi(self.effects, self.commands.interp_api)
        self.commands.cast_observations = []
        swap = patch.object(sys.modules[h.Object.__module__], "RandomNumberGenerator", RNG)
        swap.start()
        self.addCleanup(swap.stop)
        swap = patch.object(RNG, "number_bits", return_value=1)
        swap.start()
        self.addCleanup(swap.stop)

    @staticmethod
    def item(name="food", **kwargs):
        values = dict(id=name, area_id="area", vnum="1", name=name,
                      short_description=name, long_description="", material="food",
                      item_type="food", extra_flags="0", wear_flags="1", value0="5",
                      value1="0", value2="", value3="0", value4="", condition="100",
                      level=1, weight=1, cost=1, affect_data=[], contains=[])
        values.update(kwargs)
        return h.Item(**values)

    def eat(self, item):
        self.actor.loot.append(item)
        context = self.fixture._build_context(item.name, self.room, self.actor, "eat")
        result = self.commands.do_eat(self.actor, context)
        self.assertTrue(context.done)
        return result

    def drink(self, item, raw=None):
        self.room.contents[item.id] = item
        context = self.fixture._build_context(item.name if raw is None else raw, self.room, self.actor, "drink")
        return self.commands.do_drink(self.actor, context)

    def spell(self, name):
        return NS(name=name, handler_id="spell." + name, target="CHAR_DEFENSIVE", lambdas=[
            "lambda ctx: ctx.handler.cast_observations.append((ctx.spell.name, ctx.level, ctx.target, len(ctx.actor.loot)))",
            "lambda ctx: ctx.send(to_char=ctx.spell.name + ' effect.\\r\\n')",
            "lambda ctx: ctx.mark_performed()",
        ])

    def register_spells(self, *spells):
        self.commands.spell_registry = NS(all_spells=lambda: spells)

    def assert_poison(self, level, duration):
        self.assertEqual(1, len(self.actor.effects))
        effect = self.actor.effects[0]
        self.assertEqual(("spell.poison", level, duration, "APPLY_NONE", 0, "AFF_POISON"),
                         (effect.type, effect.level, effect.duration, effect.location, effect.modifier, effect.bitvector))
        self.assertEqual(Affected.AFF_POISON, self.actor.status_flags.affected_by)

    def test_pill_casts_three_slots_on_eater_at_item_spell_level_before_removal(self):
        spells = [self.spell(name) for name in ("first", "second", "third", "fourth")]
        self.register_spells(*spells)
        pill = self.item("pill", item_type="pill", level=99, value0="17",
                         value1="first", value2=spells[1], value3="third", value4="fourth")
        payload = self.eat(pill)
        self.assertEqual([(name, 17, self.actor, 1) for name in ("first", "second", "third")],
                         self.commands.cast_observations)
        self.assertEqual("You eat pill.\r\n", payload["payloads"][0]["to_char"])
        self.assertEqual(["first effect.\r\n", "second effect.\r\n", "third effect.\r\n"],
                         [p["to_char"] for p in payload["payloads"][1:]])
        self.assertEqual([], self.actor.loot)
        self.assertEqual([], self.actor.effects)  # value3 is a spell, not a poison marker
        self.assertEqual(0, self.actor.status_flags.hunger)
        self.assertEqual(0, self.actor.status_flags.pulse_wait)

    def test_pill_empty_invalid_and_failing_slots_do_not_skip_later_spells(self):
        broken = self.spell("broken")
        broken.lambdas = ["lambda ctx: ctx.fail('No effect.\\r\\n')"]
        self.register_spells(broken, self.spell("third"))
        payload = self.eat(self.item("pill", item_type="ITEM_PILL", value1="broken", value2="-1", value3="third"))
        self.assertEqual(["third"], [entry[0] for entry in self.commands.cast_observations])
        self.assertEqual(["No effect.\r\n", "third effect.\r\n"],
                         [p["to_char"] for p in payload["payloads"][1:]])
        self.assertEqual([], self.actor.loot)
        self.actor.status_flags.hunger = 0
        self.commands.cast_observations.clear()
        result = self.eat(self.item("empty", item_type="pill", value1="", value2=0, value3=""))
        self.assertEqual(1, len(result["payloads"]))
        self.assertEqual([], self.commands.cast_observations)

    def test_pill_affect_data_uses_spell_level_instead_of_eater_level(self):
        spell = NS(name="armor", handler_id="spell.armor", target="CHAR_DEFENSIVE",
                   lambdas=["lambda ctx: ctx.apply_affect_data()"], guards=[], payload=h.GamePayload(),
                   affect_data=[dict(type="sn", where="TO_AFFECTS", level="level", duration="level + 1",
                                     location="APPLY_NONE", modifier=0, bitvector=0, apply_to="char")])
        self.register_spells(spell)
        self.actor.level = 50
        self.eat(self.item("pill", item_type="pill", value0="7", value1="armor"))
        self.assertEqual(1, len(self.actor.effects))
        effect = self.actor.effects[0]
        self.assertEqual(("spell.armor", 7, 8), (effect.type, effect.level, effect.duration))

    def test_food_poison_formula_messages_and_extraction(self):
        food = self.item(value0="5", value3="1")
        payload = self.eat(food)
        self.assert_poison(5, 10)
        self.assertTrue(payload["to_char"].endswith("You choke and gag.\r\n"))
        self.assertEqual("Tester eats food.\r\nTester chokes and gags.\r\n", payload["to_room"])
        self.assertEqual([self.witness], payload["targets"])
        self.assertNotIn(food, self.actor.loot)

    def test_food_poison_also_affects_npcs_and_immortals(self):
        for npc, immortal in ((True, False), (False, True)):
            with self.subTest(npc=npc, immortal=immortal):
                self.actor.effects.clear()
                self.actor.status_flags.affected_by = 0
                self.actor.is_npc, self.actor.is_immortal = npc, immortal
                self.eat(self.item(value0="3", value3="-1"))
                self.assert_poison(3, 6)

    def test_short_drink_uses_actual_serving_and_depletes_after_poison(self):
        bottle = self.item("bottle", item_type="drink", value0="20", value1="2", value2="water",
                           value3="1", liquid_affect_data=[0, 0, 0, 0, 5])
        observed_volume = []
        join = self.effects.affect_join
        def record_join(entity, effect):
            observed_volume.append(bottle.value1)
            return join(entity, effect)
        with patch.object(self.effects, "affect_join", side_effect=record_join):
            payload = self.drink(bottle)
        self.assert_poison(2, 6)
        self.assertEqual(["2"], observed_volume)
        self.assertEqual("0", bottle.value1)
        self.assertEqual("You drink water from bottle.\r\nYou choke and gag.\r\n", payload["to_char"])
        self.assertEqual("Tester drinks water from bottle.\r\nTester chokes and gags.\r\n", payload["to_room"])
        self.assertEqual([self.witness], payload["targets"])
        self.assertIn(bottle.id, self.room.contents)

    def test_fountain_poison_uses_triple_serving_including_default_drink(self):
        fountain = self.item("fountain", item_type="fountain", value0="0", value1="0", value2="water",
                             value3="1", liquid_affect_data=[0, 0, 0, 0, 5])
        self.drink(fountain, raw="")
        self.assert_poison(15, 45)
        self.assertEqual("0", fountain.value1)

    def test_poison_drink_also_affects_npcs_and_immortals(self):
        for npc, immortal in ((True, False), (False, True)):
            with self.subTest(npc=npc, immortal=immortal):
                self.actor.effects.clear()
                self.actor.status_flags.affected_by = 0
                self.actor.is_npc, self.actor.is_immortal = npc, immortal
                bottle = self.item("bottle", item_type="drink", value0="10", value1="10", value2="water",
                                   value3="1", liquid_affect_data=[0, 0, 0, 0, 4])
                self.drink(bottle)
                self.assert_poison(4, 12)

    def test_consumed_poison_joins_existing_effect_instead_of_duplicating(self):
        from item.Effect import Effect
        self.effects.affect_join(self.actor, Effect(type="spell.poison", where="TO_AFFECTS", level=9,
                                                  duration=4, bitvector="AFF_POISON", location="APPLY_NONE"))
        self.eat(self.item(value0="5", value3="1"))
        self.assert_poison(7, 14)

    def test_fuzzy_level_matches_rom_four_way_roll_and_minimum(self):
        for roll, expected in ((0, 4), (1, 5), (2, 5), (3, 6)):
            with self.subTest(roll=roll):
                self.actor.effects.clear()
                self.actor.status_flags.hunger = 0
                with patch.object(RNG, "number_bits", return_value=roll):
                    self.eat(self.item(value0="5", value3="1"))
                self.assert_poison(expected, 10)
        self.actor.effects.clear()
        self.actor.status_flags.hunger = 0
        with patch.object(RNG, "number_bits", return_value=0):
            self.eat(self.item(value0="0", value3="1"))
        self.assert_poison(1, 0)

    def test_clean_food_and_drink_apply_no_poison(self):
        self.eat(self.item())
        bottle = self.item("bottle", item_type="drink", value0="10", value1="10", value2="water",
                           liquid_affect_data=[0, 0, 0, 0, 4])
        payload = self.drink(bottle)
        self.assertEqual([], self.actor.effects)
        self.assertNotIn("gag", payload["to_char"])
        self.assertEqual("6", bottle.value1)

    def test_guard_rejections_preserve_items_and_apply_no_effects(self):
        self.register_spells(self.spell("first"))
        for kind in ("food", "pill"):
            with self.subTest(kind=kind):
                self.actor.status_flags.fullness = 48
                food = self.item(kind, item_type=kind, value1="first" if kind == "pill" else "0", value3="1")
                payload = self.eat(food)
                self.assertIn("too full", payload["to_char"])
                self.assertIn(food, self.actor.loot)
        for volume, drunk, fullness in (("0", 0, 0), ("10", 11, 0), ("10", 0, 48)):
            with self.subTest(volume=volume, drunk=drunk, fullness=fullness):
                self.actor.status_flags.drunk, self.actor.status_flags.fullness = drunk, fullness
                bottle = self.item("bottle", item_type="drink", value0="10", value1=volume,
                                   value2="water", value3="1", liquid_affect_data=[0, 0, 0, 0, 4])
                self.drink(bottle)
                self.assertEqual(volume, bottle.value1)
        self.assertEqual([], self.actor.effects)
        self.assertEqual([], self.commands.cast_observations)


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
import sys
import types
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class CharacterApi:
    is_npc = staticmethod(lambda entity: entity.is_npc)
    enum_bit = staticmethod(lambda enums, name: int(getattr(enums, name, 0)))
    can_see = staticmethod(lambda observer, entity, room: True)


def _load_runtime():
    # Load production models/renderer and the new engine primitive in isolation.
    replacements = {
        "injector": SimpleNamespace(inject=lambda target: target),
        "api.CharacterApi": SimpleNamespace(CharacterApi=CharacterApi),
        "api.GameApi": SimpleNamespace(GameApi=SimpleNamespace(
            flags_to_int=lambda value: int(value or 0), is_set=lambda flags, bit: bool(flags & bit))),
        "game.EnumProvider": SimpleNamespace(EnumProvider=object),
        "item.EffectHandler": SimpleNamespace(EffectHandler=object),
        "server.LoggerFactory": SimpleNamespace(LoggerFactory=SimpleNamespace(get_logger=lambda *_args: Mock())),
    }
    with patch.dict(sys.modules, replacements):
        modules = {}
        for name, path in (
            ("util.GenericUtil", "util/GenericUtil.py"),
            ("util.DisplayUtil", "util/DisplayUtil.py"),
            ("game.GameData", "game/GameData.py"),
            ("game.GamePayload", "game/GamePayload.py"),
            ("game.RandomNumberGenerator", "game/RandomNumberGenerator.py"),
            ("item.Effect", "item/Effect.py"),
            ("combat.WeaponHitHandler", "combat/WeaponHitHandler.py"),
        ):
            spec = importlib.util.spec_from_file_location(name, SRC / path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            modules[name] = module
    return modules["combat.WeaponHitHandler"].WeaponHitHandler, modules["game.GameData"].GameData


WeaponHitHandler, GameData = _load_runtime()


class TestWeaponHitEffects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = GameData.from_json(json.loads((ROOT / "resources/collections/SOMDB.GameData.json").read_text())[0])

    def setUp(self):
        visibility = patch.dict(sys.modules, {
            "api.CharacterApi": SimpleNamespace(CharacterApi=CharacterApi),
            "util.LookupUtil": SimpleNamespace(LookupUtil=SimpleNamespace(object_visible=lambda *args: True)),
        })
        visibility.start()
        self.addCleanup(visibility.stop)
        self.enums = {name: IntEnum(name, self.data.enums[name])
                      for name in ("weaponType", "itemFlags", "affectedBy", "gameParameters")}
        self.effects = Mock()
        self.effects.ensure_effects.side_effect = lambda entity: entity.effects
        self.handler = WeaponHitHandler(self.effects, SimpleNamespace(get=self.enums.get), self.data)
        self.handler.rng = Mock(number_range=Mock(side_effect=lambda low, high: high),
                                number_percent=Mock(return_value=100))
        self.attacker = self._entity("attacker")
        self.victim = self._entity("victim")
        self.attacker.fighting = self.victim
        self.weapon = self._item("blade", "weapon")
        self.weapon.level = 24
        self.room = SimpleNamespace(add_item_to_room=Mock(), remove_item_from_room=Mock())
        self.damage = Mock(return_value={"killed": False, "xp_gain": 0})
        self.immunity = Mock(return_value="IS_NORMAL")

    @staticmethod
    def _entity(name):
        entity = SimpleNamespace(name=name, level=10, hit=100, is_npc=False, fighting=None,
                                 status_flags=SimpleNamespace(affected_by=0, pulse_daze=0), effects=[],
                                 saving_throw=0, equipped=SimpleNamespace(), inventory=[], alignment=0)
        entity.get_alignment = lambda: entity.alignment
        entity.set_alignment = lambda value: setattr(entity, "alignment", value)
        entity.owned_items = lambda: list(entity.inventory) + [x for x in vars(entity.equipped).values() if x]
        entity.gain_condition = Mock(return_value="")
        entity.remove_item = lambda item: entity.inventory.remove(item) if item in entity.inventory else None
        entity.unequip_item = lambda slot: setattr(entity.equipped, slot, None)
        return entity

    @staticmethod
    def _item(name, item_type):
        return SimpleNamespace(name=name, short_description=name, item_type=item_type,
                               level=0, value4=0, extra_flags=0, effects=[], contains=[])

    def _flags(self, *names):
        self.weapon.value4 = sum(int(self.enums["weaponType"]["WEAPON_" + name.upper()]) for name in names)

    def _apply(self):
        return self.handler.apply(self.attacker, self.victim, self.weapon, damage=self.damage,
                                  immunity=self.immunity, room=self.room)

    def test_poison_uses_coating_level_and_depletes_even_when_saved(self):
        for saved in (False, True):
            with self.subTest(saved=saved):
                self._flags("poison")
                coating = SimpleNamespace(type="spell.poison", level=2, duration=1)
                self.weapon.effects = [coating]
                self.handler.elemental_exposure._saves = Mock(return_value=saved)
                self.effects.affect_join.reset_mock()
                result = self._apply()
                self.handler.elemental_exposure._saves.assert_called_once_with(1, self.victim, "DAM_POISON", self.immunity)
                self.assertEqual((0, 0), (coating.level, coating.duration))
                self.assertIn("has worn off", result["to_char"])
                self.assertIn(coating, self.weapon.effects)  # removal belongs to effect ticking
                if saved:
                    self.effects.affect_join.assert_not_called()
                    self.assertEqual("", result["to_victim"])
                else:
                    affect = self.effects.affect_join.call_args.args[1]
                    self.assertEqual((1, 1, -1, "AFF_POISON"),
                                     (affect.level, affect.duration, affect.modifier, affect.bitvector))
                    self.assertIn("veins", result["to_victim"])
                self.damage.assert_not_called()

    def test_innate_poison_uses_weapon_level_without_temporary_coating(self):
        self._flags("poison")
        self.handler.elemental_exposure._saves = Mock(return_value=False)
        self._apply()
        affect = self.effects.affect_join.call_args.args[1]
        self.assertEqual((18, 12, "spell.poison"), (affect.level, affect.duration, affect.type))
        self.assertEqual([], self.weapon.effects)

    def test_vampiric_heals_roll_without_hp_cap_even_if_damage_is_immune(self):
        self._flags("vampiric")
        self.attacker.alignment = -1000
        self.damage.return_value = {"damage_applied": 0}
        result = self._apply()
        self.damage.assert_called_once_with(self.attacker, self.victim, 5, dt="0", dam_type="DAM_NEGATIVE", show=False)
        self.assertEqual(102, self.attacker.hit)
        self.assertEqual(-1000, self.attacker.alignment)
        self.assertIn("draws life", result["to_room"])

    def test_proc_order_and_roll_bounds_match_rom(self):
        self._flags("poison", "vampiric", "flaming", "frost", "shocking")
        self.handler.elemental_exposure._saves = Mock(return_value=True)
        self._apply()
        self.assertEqual(["DAM_NEGATIVE", "DAM_FIRE", "DAM_COLD", "DAM_LIGHTNING"],
                         [call.kwargs["dam_type"] for call in self.damage.call_args_list])
        self.assertEqual([(1, 5), (1, 7), (1, 6), (1, 6)],
                         [call.args for call in self.handler.rng.number_range.call_args_list])

    def test_secondary_kill_stops_remaining_procs_and_retains_reward_metadata(self):
        self._flags("vampiric", "flaming", "frost", "shocking")
        def kill(*_args, **_kwargs):
            self.attacker.fighting = None
            return {"killed": True, "xp_gain": 40, "level_up_messages": "level gained"}
        self.damage.side_effect = kill
        result = self._apply()
        self.assertEqual(1, self.damage.call_count)
        self.assertEqual(40, result["xp_gain"])
        self.assertEqual("level gained", result["level_up_messages"])
        self.assertTrue(result["killed"])
        self.assertEqual(102, self.attacker.hit)

    def test_no_flags_or_ended_fight_causes_no_rolls(self):
        self._apply()
        self._flags("poison", "vampiric")
        self.attacker.fighting = None
        self._apply()
        self.damage.assert_not_called()
        self.handler.rng.number_range.assert_not_called()
        self.handler.rng.number_percent.assert_not_called()

    def test_elemental_character_side_effects_have_rom_levels_and_timing(self):
        for kind, effect_type, duration in (("flaming", "spell.fire_breath", 1), ("frost", "spell.chill_touch", 6)):
            with self.subTest(kind=kind):
                self._flags(kind)
                self.effects.reset_mock()
                self.effects.ensure_effects.side_effect = lambda entity: entity.effects
                self.handler.elemental_exposure._saves = Mock(return_value=False)
                self._apply()
                method = self.effects.affect_to_char if kind == "flaming" else self.effects.affect_join
                effect = method.call_args.args[1]
                self.assertEqual((effect_type, 12, duration), (effect.type, effect.level, effect.duration))
                self.handler.elemental_exposure._saves.assert_called_with(3, self.victim, self.data.weapon_hit_effects[kind]["damageType"], self.immunity)
        self._flags("shocking")
        self.victim.status_flags.pulse_daze = 20
        result = self._apply()
        self.assertEqual(20, self.victim.status_flags.pulse_daze)
        self.assertIn("muscles stop responding", result["to_victim"])

    def test_existing_blindness_avoids_fire_save_and_effect(self):
        self._flags("flaming")
        self.victim.status_flags.affected_by = int(self.enums["affectedBy"].AFF_BLIND)
        self.handler.elemental_exposure._saves = Mock(return_value=False)
        self._apply()
        self.handler.elemental_exposure._saves.assert_not_called()
        self.effects.affect_to_char.assert_not_called()

    def test_elemental_conditions_follow_positive_rom_adjustment(self):
        self.weapon.level = 200
        self.handler.elemental_exposure._saves = Mock(return_value=True)
        for kind, condition, amount in (("flaming", "thirst", 2), ("frost", "hunger", 1)):
            with self.subTest(kind=kind):
                self._flags(kind)
                self.victim.gain_condition.reset_mock()
                self._apply()
                self.victim.gain_condition.assert_called_once_with(condition, amount)
        self.victim.level = int(self.enums["gameParameters"].LEVEL_IMMORTAL)
        self.victim.gain_condition.reset_mock()
        self._apply()
        self.victim.gain_condition.assert_not_called()

    def test_object_chance_uses_softcaps_bless_item_level_and_inclusive_endpoint(self):
        potion = self._item("potion", "potion")
        potion.extra_flags = int(self.enums["itemFlags"].ITEM_BLESS)
        potion.level = 10
        # 120/4 + 400/10 = 70 -> 47; bless -5; item level -20; potion +25 = 47.
        for roll, destroyed in ((47, True), (48, False)):
            with self.subTest(roll=roll):
                self.victim.inventory = [potion]
                self.handler.rng.number_percent.return_value = roll
                self.handler.elemental_exposure._object_effect("frost", self.data.weapon_hit_effects["frost"],
                                            self.attacker, self.victim, potion, 120, 400, self.room,
                                            carrier=self.victim)
                self.assertEqual(not destroyed, potion in self.victim.inventory)

    def test_saving_throw_immunity_resistance_mana_and_strict_endpoint(self):
        for status, mana, roll, saved in (("IS_NORMAL", False, 50, False), ("IS_NORMAL", False, 49, True),
                                          ("IS_RESISTANT", False, 51, True), ("IS_VULNERABLE", False, 48, False),
                                          ("IS_NORMAL", True, 45, False), ("IS_NORMAL", True, 44, True)):
            with self.subTest(status=status, mana=mana, roll=roll):
                self.immunity.return_value = status
                self.victim.character_class = SimpleNamespace(mana_gain=mana)
                self.handler.rng.number_percent.return_value = roll
                self.assertEqual(saved, self.handler.elemental_exposure._saves(10, self.victim, "DAM_FIRE", self.immunity))
        self.immunity.return_value = "IS_IMMUNE"
        self.handler.rng.number_percent.reset_mock()
        self.assertTrue(self.handler.elemental_exposure._saves(100, self.victim, "DAM_FIRE", self.immunity))
        self.handler.rng.number_percent.assert_not_called()

    def test_fire_container_spills_then_damages_contents_and_removes_equipped_effects(self):
        self._flags("flaming")
        self.handler.elemental_exposure._saves = Mock(return_value=True)
        self.handler.rng.number_percent.return_value = 1
        bag = self._item("bag", "container")
        scroll = self._item("scroll", "scroll")
        bag.contains = [scroll]
        self.victim.equipped.held = bag
        result = self._apply()
        self.assertIsNone(self.victim.equipped.held)
        self.effects.remove_item_effects.assert_called_once_with(self.victim, bag)
        self.room.add_item_to_room.assert_called_once_with(scroll)
        self.room.remove_item_from_room.assert_called_once_with(scroll)
        self.assertEqual([], bag.contains)
        self.assertIn("bag ignites", result["to_victim"])
        self.assertIn("scroll crackles", result["to_room"])

    def test_cold_and_shock_destroy_only_eligible_item_types(self):
        for kind, types in (("frost", ("potion", "drink")), ("shocking", ("wand", "staff", "jewelry"))):
            with self.subTest(kind=kind):
                self._flags(kind)
                self.handler.elemental_exposure._saves = Mock(return_value=True)
                self.handler.rng.number_percent.return_value = 1
                self.victim.inventory = [self._item(name, name) for name in (*types, "weapon")]
                self._apply()
                self.assertEqual(["weapon"], [item.item_type for item in self.victim.inventory])

    def test_object_immunities_and_random_gate_prevent_destruction(self):
        for flag, gate in (("ITEM_BURN_PROOF", 4), ("ITEM_NOPURGE", 4), (None, 0)):
            with self.subTest(flag=flag, gate=gate):
                self._flags("frost")
                self.handler.elemental_exposure._saves = Mock(return_value=True)
                self.handler.rng.number_percent.return_value = 1
                self.handler.rng.number_range.side_effect = lambda low, high: gate if (low, high) == (0, 4) else high
                potion = self._item("potion", "potion")
                potion.extra_flags = int(self.enums["itemFlags"][flag]) if flag else 0
                self.victim.inventory = [potion]
                self._apply()
                self.assertEqual([potion], self.victim.inventory)


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
from tests import test_combat_handler_aggression as fixtures
from tests.test_combat_survival import Components

ROOT = Path(__file__).resolve().parents[1]
Runtime = sys.modules[fixtures.FightHandler.__module__]


def load_classes():
    stubs = {name: SimpleNamespace(**{attr: object}) for name, attr in (
        ("area.Shop", "Shop"), ("game.WeatherHandler", "WeatherHandler"), ("item.Effect", "Effect"),
        ("item.EffectHandler", "EffectHandler"), ("util.EnumUtil", "EnumUtil"),
        ("api.InterpApi", "InterpApi"), ("api.SpellApi", "SpellApi"),
        ("skill.SpellContext", "SpellContext"), ("util.PlayerUtil", "PlayerUtil"))}
    stubs["interp.Context"] = Components["interp.Context"]
    stubs["combat.CombatHandler"] = SimpleNamespace(FightHandler=Runtime.FightHandler)
    stubs["game.GameData"] = SimpleNamespace(GameData=object)
    stubs["player.CharacterAdvancement"] = SimpleNamespace(CharacterAdvancement=SimpleNamespace(gain_experience=Mock()))
    classes = []
    with patch.dict(sys.modules, stubs):
        for name, file, cls in (("interp.commands.Object", "interp/commands/Object.py", "Object"),
                                 ("_combat_death_rules", "combat/CombatDeathHandler.py", "CombatDeathHandler")):
            spec = importlib.util.spec_from_file_location(name, ROOT / "src" / file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            classes.append((getattr(module, cls), module))
    return classes


(Object, ObjectModule), (DeathHandler, DeathModule) = load_classes()


class TestCombatDeathRules(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.actor, self.victim, self.combat = self.fixtures._killer_pair()
        self.victim.name = "Victim"
        self.room = SimpleNamespace(name="Arena", vnum="100", player_targets=lambda actor: [self.actor] if actor is self.victim else [self.victim],
                                    exits=[], add_item_to_room=Mock())
        self.config = json.loads((ROOT / "resources/collections/SOMDB.GameData.json").read_text())[0]["combat"]["death"]
        self.registry = SimpleNamespace(interp_registry=SimpleNamespace(get_or_none=Mock(return_value=SimpleNamespace(name="get"))),
                                        room_registry=SimpleNamespace(get_or_none=Mock(return_value=None)))
        self.objects = Object.__new__(Object)
        self.death = DeathHandler(SimpleNamespace(death_rules=self.config), self.registry, self.objects)

    def test_inventory_extraction_rot_and_visibility_flags(self):
        item = SimpleNamespace(extra_flags=7, contains=[SimpleNamespace(contains=[])], timer=0)
        flags = {"ITEM_ROT_DEATH": 1, "ITEM_VIS_DEATH": 2, "ITEM_INVENTORY": 4}
        with patch.object(DeathModule.ItemApi, "has_item_flag", side_effect=lambda obj, enum, name: bool(obj.extra_flags & flags[name]), create=True), \
                patch.object(DeathModule.CharacterApi, "enum_bit", side_effect=lambda enum, name: flags[name]), \
                patch.object(DeathModule.CharacterApi, "unset_bit", side_effect=lambda value, bit: value & ~bit, create=True), \
                patch.object(DeathModule.random, "randint", return_value=7):
            keep, notices = self.death.item_transfer(item, False, self.victim, self.room, object())
        self.assertFalse(keep)
        self.assertEqual((4, 7, []), (item.extra_flags, item.timer, item.contains))

    def test_floating_rot_spills_contents_without_destroying_them(self):
        child = SimpleNamespace(contains=[object()])
        item = SimpleNamespace(name="orb", short_description="an orb", extra_flags=1, contains=[child])
        with patch.object(DeathModule.ItemApi, "has_item_flag", side_effect=lambda obj, enum, name: name == "ITEM_ROT_DEATH", create=True), \
                patch.object(DeathModule.CharacterApi, "enum_bit", return_value=0), \
                patch.object(DeathModule.CharacterApi, "unset_bit", side_effect=lambda value, bit: value & ~bit, create=True):
            keep, notices = self.death.item_transfer(item, True, self.victim, self.room, object())
        self.assertFalse(keep)
        self.room.add_item_to_room.assert_called_once_with(child)
        self.assertEqual(1, len(child.contains))
        self.assertIn("scattering", notices[0]["to_room"])

    def test_total_xp_penalty_and_cross_clan_flag_precedence(self):
        self.victim.character_attributes.experience = 301
        self.victim.character_attributes.experience_per_level = 1000
        self.victim.character_attributes.accumulated_experience = 5301
        self.victim.status_flags.act = 3
        self.actor.guild, self.victim.guild = "one", "two"
        with patch.object(DeathModule.CharacterAdvancement, "gain_experience") as gain:
            notice = self.death.penalty(self.actor, self.victim, self.room)
        gain.assert_called_once_with(self.victim, -150)
        self.assertEqual("WIZ_DEATHS", notice["wiznet_flag"])
        with patch.object(DeathModule.CharacterApi, "enum_bit", side_effect=lambda flags, name: 1 if name == "PLR_KILLER" else 2), \
                patch.object(DeathModule.CharacterApi, "unset_act_flags", side_effect=lambda entity, bit: setattr(entity.status_flags, "act", entity.status_flags.act & ~bit), create=True):
            self.death.cleanup_flags(self.actor, self.victim, object())
            self.assertEqual(2, self.victim.status_flags.act)
            self.death.cleanup_flags(self.actor, self.victim, object())
            self.assertEqual(0, self.victim.status_flags.act)

    def test_wounds_death_and_adjacent_cry_recipients(self):
        self.victim.max_hit, self.victim.hit = 100, 20
        warnings = self.death.wounds(self.actor, self.victim, self.room, 26, "")
        self.assertEqual(2, len(warnings))
        notices = self.death.wounds(self.actor, self.victim, self.room, 1, "POS_DEAD")
        self.assertIn("KILLED", notices[1]["to_victim"])
        adjacent = SimpleNamespace(player_targets=lambda actor: ["witness"])
        self.registry.room_registry.get_or_none.return_value = adjacent
        self.room.exits = [SimpleNamespace(to_room_id="next")]
        cries = self.death.cry(self.victim, self.room, 0, 0, SimpleNamespace())
        self.assertIn("DEAD", cries[0]["to_room"])
        self.assertEqual(["witness"], cries[1]["targets"])
        self.assertIn("someone's", cries[1]["to_room"])

    def test_real_pickup_money_conversion_and_capacity_rejection(self):
        money = SimpleNamespace(item_type="money", value0="7", value1="3")
        container = SimpleNamespace(remove_contained_item=Mock(), short_description="a corpse")
        self.actor.silver, self.actor.gold = 1, 2
        self.actor.add_item = Mock()
        self.objects._get_item_error = Mock(return_value="")
        self.objects._render_command_message = Mock(return_value="pickup")
        with patch.object(ObjectModule, "Item", SimpleNamespace(short=lambda obj: "coins" if obj is money else "corpse")):
            result = self.objects._get_one(self.actor, self.room, SimpleNamespace(), money, container)
        self.assertEqual((8, 5), (self.actor.silver, self.actor.gold))
        self.actor.add_item.assert_not_called()
        container.remove_contained_item.assert_called_once_with(money)
        self.objects._get_item_error.return_value = "too heavy"
        self.assertEqual({"to_char": "too heavy"}, self.objects._get_one(self.actor, self.room, object(), money, container))

    def test_autogold_only_money_and_autosac_preserves_failed_autoloot(self):
        money, sword = SimpleNamespace(item_type="money"), SimpleNamespace(item_type="weapon")
        corpse = SimpleNamespace(item_type="corpse_npc", contains=[money, sword])
        combat = SimpleNamespace(_find_latest_corpse=Mock(return_value=corpse),
            _player_act_enabled=lambda actor, name: name in ("PLR_AUTOGOLD", "PLR_AUTOSAC"),
            _autosacrifice_corpse=Mock(return_value={"to_char": "sac"}))
        self.objects._get_one = Mock(return_value={"to_char": "coins"})
        with patch.object(DeathModule.ItemUtil, "can_see_object", return_value=True, create=True):
            self.death.auto_loot(combat, self.actor, self.victim, self.room, set())
            self.objects._get_one.assert_called_once()
            self.assertIs(money, self.objects._get_one.call_args.args[3])
            combat._player_act_enabled = lambda actor, name: name in ("PLR_AUTOLOOT", "PLR_AUTOSAC")
            combat._autosacrifice_corpse.reset_mock()
            self.death.auto_loot(combat, self.actor, self.victim, self.room, set())
            combat._autosacrifice_corpse.assert_not_called()
        corpse.item_type = "corpse_pc"
        self.assertEqual([], self.death.auto_loot(combat, self.actor, self.victim, self.room, set()))

    def test_damage_death_orders_wounds_rewards_cry_and_autoloot_once(self):
        victim = self.fixtures._mob("mob")
        victim.name, victim.max_hit, victim.hit = "Victim", 20, 1
        room = self.fixtures._safety_room(self.actor, victim)
        room.id, room.vnum, room.name, room.contents = "room-1", "100", "Arena", {}
        room.player_targets = lambda actor: [self.actor]
        combat = self.fixtures._damage_handler(room)
        combat._find_room_for_entity = Mock(return_value=room)
        combat.death_handler = self.death
        combat.is_safe = Mock(return_value=(False, ""))
        combat.group_gain = Mock(return_value={"xp_gain": 7, "reward_payloads": [{"to_char": "reward"}]})
        combat.raw_kill = Mock(return_value=[{"to_room": "cry", "targets": [self.actor]}])
        self.death.auto_loot = Mock(return_value=[{"to_char": "pickup"}])
        self.death.cleanup_flags = Mock()
        combat._check_immunity = Mock(return_value="IS_NORMAL")
        with patch.object(DeathModule.CharacterApi, "is_awake", return_value=False):
            result = combat.damage(self.actor, victim, 1)
        actions = result["post_damage_actions"]
        self.assertIn("DEAD", actions[0]["to_room"])
        self.assertEqual({"to_char": "reward"}, actions[1])
        self.assertEqual("WIZ_MOBDEATHS", actions[2]["wiznet_flag"])
        self.assertEqual("cry", actions[3]["to_room"])
        self.assertEqual("pickup", actions[4]["to_char"])
        self.assertEqual([], result["reward_payloads"])
        combat.build_round_payload(self.actor, victim, room, result)
        self.death.auto_loot.assert_called_once()

    def test_visible_npc_corpse_gate_and_zero_progress_penalty(self):
        self.victim.character_attributes.experience = 0
        self.victim.character_attributes.experience_per_level = 1000
        self.victim.character_attributes.accumulated_experience = 5000
        with patch.object(DeathModule.CharacterAdvancement, "gain_experience") as gain:
            self.death.penalty(self.actor, self.victim, self.room)
        gain.assert_not_called()
        corpse = SimpleNamespace(item_type="corpse_npc", contains=[object()])
        combat = SimpleNamespace(_find_latest_corpse=Mock(return_value=corpse))
        with patch.object(DeathModule.ItemUtil, "can_see_object", return_value=False, create=True):
            self.assertEqual([], self.death.auto_loot(combat, self.actor, self.victim, self.room, set()))

    def test_death_penalty_uses_total_xp_floor_independently_of_progress(self):
        self.victim.level = 10
        self.victim.character_attributes.experience_per_level = 1000
        for total, progress, expected in ((9999, 900, None), (10000, 900, None),
                                          (10301, 0, -150), (10001, 900, 50),
                                          (10076, 1, 0), (11501, 1, -950)):
            with self.subTest(total=total, progress=progress):
                self.victim.character_attributes.accumulated_experience = total
                self.victim.character_attributes.experience = progress
                with patch.object(DeathModule.CharacterAdvancement, "gain_experience") as gain:
                    self.death.penalty(self.actor, self.victim, self.room)
                if expected is None:
                    gain.assert_not_called()
                else:
                    gain.assert_called_once_with(self.victim, expected)

    def test_death_penalty_applies_rom_delta_to_total_xp_through_advancement(self):
        from tests import test_combat_group_rewards as rewards
        self.victim.level = 10
        attrs = self.victim.character_attributes
        attrs.experience_per_level, attrs.accumulated_experience, attrs.experience = 1000, 10301, 900
        with patch.object(DeathModule, "CharacterAdvancement", rewards.Advancement), \
                patch.object(rewards.Advancement, "_hero_level", return_value=60):
            self.death.penalty(self.actor, self.victim, self.room)
        self.assertEqual(10151, attrs.accumulated_experience)
        self.assertEqual(750, attrs.experience)
        self.assertEqual(10, self.victim.level)

    def test_death_cry_part_variants_and_missing_parts(self):
        body_parts = SimpleNamespace(has=lambda flags, bit: bool(flags & bit), value=lambda name: 1)
        for roll, phrase in ((2, "guts"), (3, "head"), (4, "heart"), (5, "arm"), (6, "leg"), (7, "brains")):
            with self.subTest(roll=roll):
                notices = self.death.cry(self.victim, self.room, roll, 1, body_parts)
                self.assertIn(phrase, notices[0]["to_room"])
                fallback = self.death.cry(self.victim, self.room, roll, 0, body_parts)
                self.assertIn("death cry", fallback[0]["to_room"])


if __name__ == "__main__":
    unittest.main()

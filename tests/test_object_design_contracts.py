import unittest
from enum import IntEnum
from dataclasses import asdict
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_update_handler_active_players import Character, build_character_data, Positions
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from api.MobileApi import MobileApi
from game.AnimateEntity import AnimateEntity
from game.AnimateEntity import RegenerationContext
from game.EnumProvider import EnumProvider
from game.StatusFlags import StatusFlags
from mobile.ArmorClass import ArmorClass as MobileArmor
from player.ArmorClass import ArmorClass as PlayerArmor
from skill.Ability import Ability
from skill.AbilityResolver import AbilityResolver
from skill.LearningService import LearningService


class TestObjectDesignContracts(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.object(CharacterApi, 'GameParameters', IntEnum('GameParameters', {'LEVEL_IMMORTAL': 52})))

    def test_bootstrap_wires_shared_exposure_and_learning_services(self):
        from injector import Injector, singleton
        from server.Bootstrapper import Bootstrapper
        from api.SpellApi import SpellApi
        from combat.WeaponHitHandler import WeaponHitHandler
        from game.GameData import GameData
        from util.ElementalExposure import ElementalExposure

        self.addCleanup(Bootstrapper.reset_runtime)
        injector = Injector()
        injector.binder.bind(GameData, to=NS(weapon_hit_effects={}, item_table={}), scope=singleton)
        injector.binder.bind(EnumProvider, to=NS(get=lambda _: None), scope=singleton)
        Bootstrapper._bind_registries(injector)
        Bootstrapper._bind_learning(injector)
        Bootstrapper._bind_handlers(injector)
        Bootstrapper._bind_apis(injector)
        self.assertIs(Ability._learning, injector.get(LearningService))
        self.assertIs(injector.get(ElementalExposure), injector.get(SpellApi).elemental_exposure)
        self.assertIs(injector.get(ElementalExposure), injector.get(WeaponHitHandler).elemental_exposure)
        Bootstrapper.reset_runtime()
        self.assertIsNone(Ability._learning)

    def test_resolver_preserves_namespaces_precedence_and_reload_visibility(self):
        skill = NS(id="shared", name="poison", handler_id="skill.poison")
        spell = NS(id="shared", name="poison", handler_id="spell.poison")
        skills, spells = [skill], [spell]
        def registry(entries, method):
            return NS(**{method: lambda: entries},
                      get_or_none=lambda **kw: next((v for v in entries if v.id == kw["id"]), None))
        resolver = AbilityResolver(registry(skills, "all_skills"), registry(spells, "all_spells"))
        self.assertIs(skill, resolver.by_name(" POISON "))
        self.assertEqual((skill, "skills"), resolver.by_id("shared"))
        self.assertIs(spell, resolver.effect_owner("poison"))
        # Prefix aliases historically do not override spell-first precedence.
        self.assertIs(spell, resolver.effect_owner("skill.poison"))
        self.assertIsNone(resolver.effect_owner("skill.poison", spell_only=True))
        spells.clear()
        self.assertIs(skill, resolver.effect_owner("poison"))
        self.assertIsNone(resolver.effect_owner("poison", spell_only=True))

    def test_learned_instance_methods_keep_exact_prefix_and_creation_contracts(self):
        character = Character.from_json(build_character_data())
        character.skills = [{"name": "swordplay", "level": 12}, {"name": "sword", "level": 40}]
        self.assertEqual("sword", character.get_learned("sword", prefix=True)["name"])
        self.assertEqual("swordplay", character.get_learned("swordp", prefix=True)["name"])
        character.set_learned("sword", 150)
        self.assertEqual(100, character.get_learned("sword")["level"])
        with self.assertRaises(ValueError):
            character.set_learned("missing", 3)
        entry = character.set_learned("heal", -5, collection_name="spells", create=True)
        self.assertEqual({"name": "heal", "level": 0}, entry)
        self.assertEqual([], character.visible_learned_entries(collection_name="spells"))

    def test_learning_service_uses_explicit_random_and_advancement_dependencies(self):
        character = Character.from_json(build_character_data())
        character.level = 20
        character.skills = [{"name": "sword", "level": 40}]
        definition = NS(name="sword", rating_by_class={"mage": 2}, level_by_class={"mage": 1})
        resolver = NS(by_id=lambda _: (definition, "skills"))
        rules = NS(current_stat=lambda entity, name: max(3, min(25, getattr(entity.character_attributes, name))), is_npc=lambda _: False, skill_value_for_class=CharacterApi.skill_value_for_class,
                   get_attribute_bonus=lambda *_: {"learn": 18})
        percent, random, advance = Mock(), Mock(), Mock()
        percent.number_percent.return_value = 1
        random.randint.return_value = 1
        learning = LearningService(resolver, rules, percent, random, advance, Mock())
        learning.check_improve(character, "sword", True)
        self.assertEqual(41, character.get_learned("sword")["level"])
        random.randint.assert_called_once_with(1, 1000)
        advance.assert_called_once_with(character, 4)
        self.assertIn("better at sword", character.take_improve_messages())
        self.assertEqual("", character.take_improve_messages())

    def test_regeneration_keeps_random_order_and_skips_full_resources(self):
        from mobile.Mobile import Mobile

        character = Character.from_json(build_character_data())
        character.skills = [{"name": name, "level": 100} for name in ("fast healing", "meditation")]
        rng = Mock()
        rng.number_percent.side_effect = [10, 20]
        context = RegenerationContext(Positions, NS(), rng)
        room = NS(heal_rate=100, mana_rate=100)
        with patch.object(Ability, "check_improve_by_name") as improve:
            character.regenerate(room, context)
        self.assertEqual(2, rng.number_percent.call_count)
        self.assertEqual(["fast healing", "meditation"], [c.args[1] for c in improve.call_args_list])
        character.hit, character.mana, character.movement = character.max_hit, character.max_mana, character.max_movement
        rng.reset_mock()
        character.regenerate(room, context)
        character.regenerate(None, context)
        rng.number_percent.assert_not_called()
        mobile = Mobile.__new__(Mobile)
        mobile.__dict__.update(level=10, hit=0, max_hit=100, mana=0, max_mana=100,
                               movement=0, max_movement=100, position=8,
                               status_flags=StatusFlags.default())
        mobile.regenerate(room, context)
        self.assertEqual((7, 7, 10), (mobile.hit, mobile.mana, mobile.movement))
        rng.number_percent.assert_not_called()

    def test_armor_contract_preserves_wire_layouts_and_adjustment_reversal(self):
        player = PlayerArmor.from_json(dict(piercing=-11, bashing=20, slashing=30, magic=40))
        mobile = MobileArmor.from_json("{'pierce': -11, 'bash': 20, 'slash': 30, 'exotic': 40}")
        for armor in (player, mobile):
            self.assertEqual([-11, 20, 30, 40], [armor.base_value(k) for k in ("pierce", "bash", "slash", "other")])
            before = asdict(armor)
            armor.adjust_all(-5)
            armor.adjust_all(5)
            self.assertEqual(before, asdict(armor))
        self.assertEqual({"piercing", "bashing", "slashing", "magic"}, set(asdict(player)))
        self.assertEqual({"pierce", "bash", "slash", "exotic"}, set(asdict(mobile)))

    def test_entity_and_facade_keep_their_documented_position_fallbacks(self):
        entity = NS(character_attributes=None, start_pos=Positions.POS_SLEEPING.value)
        self.assertEqual(4, AnimateEntity.position_value(entity, Positions))
        with patch.object(CharacterApi, "positions", Positions, create=True):
            self.assertEqual(8, CharacterApi.position_value(entity))
            CharacterApi.set_position(entity, "POS_RESTING")
            self.assertEqual(5, entity.position)
            self.assertEqual(5, AnimateEntity.position_value(entity, Positions))

    def test_named_flags_share_normalization_and_guarded_writes(self):
        entity = NS(status_flags=StatusFlags.default())
        bits = NS(AFF_TEST=NS(value=4))
        CharacterApi.set_affected_by_name(entity, bits, "AFF_TEST", True)
        self.assertTrue(AnimateEntity.is_affected(entity, bits, "AFF_TEST"))
        AnimateEntity.set_affected(entity, bits, "AFF_TEST", False)
        self.assertFalse(CharacterApi.is_affected_by_name(entity, bits, "AFF_TEST"))
        with self.assertRaises(AttributeError):
            entity.status_flags.affected_by = 4

    def test_global_reset_clears_both_facades_aliases_and_bootstrap_callbacks(self):
        self.addCleanup(GameApi.reset_for_tests)
        data = NS(races={}, item_table={}, weapons={}, attribute_bonuses={}, classes={}, pc_races={}, titles={})
        GameApi.configure(data, EnumProvider({"positions": Positions}))
        registry, weather, effect_reset = object(), object(), Mock()
        for facade in (CharacterApi, MobileApi):
            facade.lazy_load(weather, registry)
            self.assertIs(registry, facade._runtime.registry_service)
            self.assertIs(weather, facade._runtime.weather_handler)
        GameApi.register_runtime_reset(effect_reset)
        GameApi.reset_for_tests()
        effect_reset.assert_called_once_with()
        for facade in (CharacterApi, MobileApi):
            self.assertIsNone(facade._registry_service)
            self.assertIsNone(facade._weather_handler)
            self.assertIsNone(facade.positions)
        GameApi.reset_for_tests()
        effect_reset.assert_called_once_with()

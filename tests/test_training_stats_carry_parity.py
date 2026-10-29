import json
import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi
from api.SpellApi import SpellApi
from combat.CombatHandler import FightHandler
from game.AnimateEntity import RegenerationContext
from item.Effect import Effect
from item.ItemOwnership import ItemOwnership
from player.Character import Character
from player.CharacterAdvancement import CharacterAdvancement
from player.CharacterService import CharacterService
from util.PlayerUtil import PlayerUtil
from interp.commands.Object import Object


class TrainingStatsCarryTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.actor.character_race.who_name = 'human'
        self.actor.character_class.attr_prime = 0
        for name in CharacterApi.STAT_NAMES:
            setattr(self.actor.character_race, 'max_' + name, 18)
        trainer = self.npc()
        trainer.status_flags.set_flag('act', self.enums.get('actBits').ACT_TRAIN)
        self.room.add_mobile_to_room(trainer)
        self.actor.character_attributes.trains = 10

    def affect(self, name, modifier, actor=None, kind='test.stat'):
        actor = actor or self.actor
        return self.effects.affect_to_char(actor, Effect(type=kind, where='TO_AFFECTS', duration=5,
                                                        location='APPLY_' + name[:3].upper(), modifier=modifier))

    def test_prime_training_caps_human_nonhuman_nonprime_and_ceiling(self):
        for race, index, base, expected in [('human', 0, 18, 21), ('elf', 0, 18, 20),
                ('human', 1, 18, 18), ('human', 0, 24, 25)]:
            with self.subTest(race=race, index=index):
                self.actor.character_race.who_name = race
                setattr(self.actor.character_race, 'max_' + CharacterApi.STAT_NAMES[index], base)
                self.assertEqual(expected, CharacterApi.get_max_train(self.actor, index))

    def test_training_at_base_race_max_can_reach_human_prime_max(self):
        self.actor.character_attributes.strength = 18
        for _ in range(3):
            self.attempt('train', 'str')
        self.assertEqual(21, self.actor.character_attributes.strength)
        self.assertEqual(7, self.actor.character_attributes.trains)
        self.attempt('train', 'str')
        self.assertEqual((21, 7), (self.actor.character_attributes.strength, self.actor.character_attributes.trains))

    def test_weaken_cannot_allow_training_at_permanent_cap(self):
        self.actor.character_class.attr_prime = 1
        self.actor.character_attributes.strength = 18
        self.affect('strength', -5)
        self.assertNotIn(' str', PlayerUtil.format_train_options(self.actor))
        self.attempt('train', 'str')
        self.effects.affect_strip(self.actor, 'test.stat')
        self.assertEqual((18, 10), (self.actor.character_attributes.strength, self.actor.character_attributes.trains))

    def test_positive_buff_does_not_block_valid_training(self):
        self.actor.character_attributes.strength = 20
        self.affect('strength', 4)
        self.assertIn(' str', PlayerUtil.format_train_options(self.actor))
        self.attempt('train', 'str')
        self.assertEqual(25, self.actor.character_attributes.strength)
        self.effects.affect_strip(self.actor, 'test.stat')
        self.assertEqual(21, self.actor.character_attributes.strength)

    def test_training_preserves_overlapping_item_and_spell_modifiers_across_save(self):
        self.actor.character_attributes.strength = 19
        ring = item('ring', effects=[dict(where='TO_OBJECT', location='APPLY_STR', modifier=2, duration=-1)])
        self.actor.equip_item(ring, 'finger1')
        self.effects.apply_item_effects(self.actor, ring)
        self.affect('strength', -5)
        self.attempt('train', 'str')
        loaded = Character.from_json(json.loads(json.dumps(CharacterService._serialize_character(self.actor))))
        self.assertEqual(20, CharacterApi.permanent_stat(loaded, 'strength'))
        self.effects.affect_strip(loaded, 'test.stat')
        ItemOwnership(self.effects).detach_carried(loaded, loaded.equipped.finger1)
        self.assertEqual(20, loaded.character_attributes.strength)

    def test_numeric_apply_locations_are_subtracted_from_permanent_stats(self):
        self.actor.character_attributes.dexterity = 17
        self.effects.affect_to_char(self.actor, Effect(where=0, location=int(self.enums.get('applyTypes').APPLY_DEX), modifier=3))
        self.assertEqual(17, CharacterApi.permanent_stat(self.actor, 'dexterity'))

    def test_current_stat_clamps_minimum_race_prime_and_human_limits(self):
        for race, name, raw, expected in [('human', 'strength', 40, 25), ('human', 'intelligence', 40, 23),
                ('elf', 'strength', 40, 24), ('elf', 'intelligence', 40, 22), ('human', 'strength', -10, 3)]:
            with self.subTest(race=race, name=name):
                self.actor.character_race.who_name = race
                setattr(self.actor.character_attributes, name, raw)
                self.assertEqual(expected, CharacterApi.current_stat(self.actor, name))
                self.assertEqual(raw, getattr(self.actor.character_attributes, name))

    def test_training_and_current_stat_immortal_boundary_uses_level_not_trust(self):
        immortal = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        self.actor.trust = int(self.enums.get('gameParameters').IMPLEMENTOR)
        self.actor.level = immortal
        self.actor.character_attributes.intelligence = 40
        self.assertEqual(18, CharacterApi.get_max_train(self.actor, 1))
        self.assertEqual(23, CharacterApi.current_stat(self.actor, 'intelligence'))
        self.actor.level += 1
        self.assertEqual(25, CharacterApi.get_max_train(self.actor, 1))
        self.assertEqual(25, CharacterApi.current_stat(self.actor, 'intelligence'))

    def test_npc_stats_clamp_without_player_race_or_class(self):
        mob = self.npc()
        mob.character_attributes.dexterity = 40
        self.assertEqual(25, CharacterApi.current_stat(mob, 'dexterity'))
        self.assertEqual(25, CharacterApi.get_max_train(mob, 3))

    def test_spell_current_stat_delegates_without_double_prime_bonus(self):
        self.actor.character_race.who_name = 'elf'
        self.actor.character_race.max_strength = 16
        self.actor.character_attributes.strength = 40
        api = SpellApi(self.effects, self.api)
        ctx = NS(victim=self.actor)
        self.assertEqual(22, api.current_stat(ctx, 'strength'))

    def test_regeneration_reads_bounded_stats(self):
        self.actor.character_attributes.dexterity = 40
        self.actor.character_attributes.wisdom = 40
        self.actor.character_attributes.intelligence = 40
        self.actor.character_class.mana_gain = True
        context = RegenerationContext(self.enums.get('positions'), self.enums.get('affectedBy'), NS(number_percent=lambda: 100))
        sleep = CharacterApi.pos_value('POS_SLEEPING')
        self.assertEqual(43, self.actor._base_move_gain(20, sleep, context))
        self.assertEqual(33, self.actor._base_mana_gain(20, sleep, context))

    def test_combat_bonuses_and_advancement_stat_inputs_are_bounded(self):
        self.actor.character_attributes.strength = 40
        self.assertEqual(25, CharacterAdvancement._stat(self.actor, 'strength'))
        expected = CharacterApi.get_attribute_bonus('strength', '25')['todam']
        self.assertEqual(expected, CharacterApi.get_damroll(self.actor))
        self.assertEqual(expected, FightHandler._strength_combat_bonus(self.actor, 'todam'))

    def test_carry_limits_follow_stat_affects_and_level_without_saved_cache_changes(self):
        self.actor.character_attributes.dexterity = 13
        self.actor.character_attributes.strength = 13
        before_count, before_weight = self.actor.max_items(), self.actor.max_weight()
        self.affect('dexterity', 4)
        self.affect('strength', 4, kind='test.str')
        self.actor.level += 1
        self.assertEqual(before_count + 9, self.actor.max_items())
        self.assertGreater(self.actor.max_weight(), before_weight + 25)
        self.effects.affect_strip(self.actor, 'test.stat')
        self.effects.affect_strip(self.actor, 'test.str')
        self.assertEqual(before_count + 1, self.actor.max_items())
        self.assertEqual(before_weight + 25, self.actor.max_weight())

    def test_carry_limit_ignores_legacy_zero_or_large_saved_allowances(self):
        expected = self.actor.max_items(), self.actor.max_weight()
        for value in (0, 99999):
            self.actor.character_attributes.max_items = self.actor.character_attributes.max_weight = value
            self.assertEqual(expected, (self.actor.max_items(), self.actor.max_weight()))

    def test_carry_immortal_and_pet_exceptions(self):
        self.actor.level = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        self.assertEqual((1000, 10000000), (self.actor.max_items(), self.actor.max_weight()))
        mob = self.npc()
        self.assertGreater(mob.max_items(), 0)
        mob.status_flags.set_flag('act', self.enums.get('actBits').ACT_PET)
        self.assertEqual((0, 0), (mob.max_items(), mob.max_weight()))

    def test_give_object_to_real_mobile_succeeds_but_pet_capacity_blocks(self):
        commands = Object.__new__(Object)
        commands.room_registry = self.rooms
        commands.interp_api = self.api
        commands.item_flags = self.enums.get('itemFlags')
        commands._is_shopkeeper = lambda victim: False
        commands._is_money_changer = lambda victim: False
        mob = self.npc()
        self.room.add_mobile_to_room(mob)
        obj = item('gift')
        self.actor.add_item(obj)
        commands.do_give(self.actor, self.ctx('give', 'gift npc'))
        self.assertIn(obj, mob.inventory)
        mob.status_flags.set_flag('act', self.enums.get('actBits').ACT_PET)
        other = item('other')
        self.actor.add_item(other)
        result = commands.do_give(self.actor, self.ctx('give', 'other npc'))
        self.assertTrue(result['blocked_key'])
        self.assertIn(other, self.actor.loot)

    def test_buy_guards_use_dynamic_count_and_weight_not_legacy_zero_fields(self):
        self.actor.character_attributes.max_items = self.actor.character_attributes.max_weight = 0
        for key, quantity, weight in [('quantity_exceeds_allowed', self.actor.max_items() + 1, 1),
                                      ('weight_exceeds_allowed', 1, self.actor.max_weight() + 1)]:
            with self.subTest(key=key):
                context = self.ctx('buy')
                context.buy_is_pet_shop = False
                context.buy_quantity = quantity
                context.buy_item = item('stock', itemType='treasure', weight=weight)
                blocked = self.api.evaluate_guards_only(context, 'buy', guard_filter=lambda guard: guard.message_key == key)
                self.assertEqual(key, blocked['blocked_key'])

    def test_learning_uses_capped_intelligence_bonus(self):
        from skill.Ability import Ability
        self.actor.character_attributes.intelligence = 40
        service = Ability._learning_service()
        with patch.object(CharacterApi, 'get_attribute_bonus', return_value={'learn': 20}) as bonus:
            service.practice_gain(self.actor, 2)
        bonus.assert_called_once_with('intelligence', '23')

    def test_get_rejects_overweight_under_dynamic_limit(self):
        commands = Object.__new__(Object)
        commands.item_flags = self.enums.get('itemFlags')
        commands.wear_flags = self.enums.get('wearFlags')
        commands.WellKnownObjEnums = self.enums.get('wellKnownObjectVnums')
        obj = item('heavy', weight=self.actor.max_weight() + 1)
        context = self.ctx('get', 'heavy')
        self.assertIn("can't carry that much weight", commands._get_item_error(self.actor, context, obj))


if __name__ == '__main__':
    unittest.main()

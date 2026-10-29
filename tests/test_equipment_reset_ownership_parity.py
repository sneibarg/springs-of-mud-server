import json
import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi
from api.MobileApi import MobileApi
from area.AreaHandler import AreaHandler
from area.Room import Room
from combat.CombatHandler import FightHandler
from game.Equipped import Equipped
from item.Effect import Effect
from item.ItemFactory import ItemFactory
from item.ItemOwnership import ItemOwnership
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from mobile.MobileFactory import MobileFactory
from player.Character import Character
from player.CharacterService import CharacterService
from util.WizUtil import WizUtil


class EquipmentOwnershipTests(MovementFixture, unittest.TestCase):
    def wear(self, obj, actor=None):
        actor = actor or self.actor
        actor.add_item(obj)
        return Equipped.wear_item(actor, obj, self.enums.get('wearFlags'), self.enums.get('itemFlags'),
                                  replace=True, effect_handler=self.effects)

    def armor(self, name='armor', slot='torso', values=(10, 7, 4, 2)):
        obj = item(name, itemType='armor', **{f'value{i}': str(v) for i, v in enumerate(values)})
        self.actor.equip_item(obj, slot)
        return obj

    def lamp(self, fuel='10', actor=None):
        actor = actor or self.actor
        lamp = item('lamp-' + actor.id, itemType='light', value2=fuel)
        actor.equip_item(lamp, 'light')
        return lamp

    def test_all_armor_slots_use_rom_multipliers_and_all_categories(self):
        for slot, multiplier in [('torso', 3), ('head', 2), ('legs', 2), ('body', 2),
                ('feet', 1), ('hands', 1), ('arms', 1), ('shield', 1), ('neck1', 1),
                ('neck2', 1), ('waist', 1), ('wrist1', 1), ('wrist2', 1), ('held', 1),
                ('finger1', 0), ('wielded', 0), ('floating_nearby', 0)]:
            with self.subTest(slot=slot):
                self.armor(slot=slot)
                for category, value in zip(('pierce', 'bash', 'slash', 'exotic'), (10, 7, 4, 2)):
                    self.assertEqual(multiplier * value, Equipped.armor_contribution(self.actor, category))
                self.actor.unequip_item(slot)
                self.assertEqual(0, Equipped.armor_contribution(self.actor, 'pierce'))

    def test_combat_and_score_include_base_armor_and_explicit_ac_effect_once(self):
        before = self.actor.armor_class.get_ac(self.actor, 'pierce')
        obj = self.armor()
        obj.effects = [Effect(where='TO_OBJECT', location='APPLY_AC', modifier=-5, duration=-1)]
        self.effects.apply_item_effects(self.actor, obj)
        self.assertEqual(before - 35, self.actor.armor_class.get_ac(self.actor, 'pierce'))
        self.assertEqual(int((before - 35) / 10), FightHandler._victim_ac_for_damage_type(self.actor, 'DAM_PIERCE'))
        self.effects.remove_item_effects(self.actor, obj)
        self.actor.unequip_item('torso')
        self.assertEqual(before, self.actor.armor_class.get_ac(self.actor, 'pierce'))

    def test_armor_save_reload_and_removal_do_not_double_or_drift(self):
        before = self.actor.armor_class.get_ac(self.actor, 'pierce')
        self.armor()
        for _ in range(3):
            self.actor = Character.from_json(json.loads(json.dumps(CharacterService._serialize_character(self.actor))))
            self.assertEqual(before - 30, self.actor.armor_class.get_ac(self.actor, 'pierce'))
        self.actor.unequip_item('torso')
        self.assertEqual(before, self.actor.armor_class.get_ac(self.actor, 'pierce'))

    def test_armor_clone_and_filtered_clone_derive_from_retained_slots(self):
        mob = self.npc()
        mob.hit_dice = mob.mana_dice = mob.damage_dice = Dice(1, 6, 0)
        mob.armor_class = ArmorClass(100, 100, 100, 100)
        mob.max_hit = mob.hit = mob.max_mana = mob.mana = 100
        obj = item('armor', itemType='armor', value0='10')
        mob.equip_item(obj, 'torso')
        clone = MobileFactory.copy_instance(mob, self.enums)
        filtered = MobileFactory.copy_instance(mob, self.enums, item_filter=lambda obj: False, effect_handler=self.effects)
        self.assertEqual(30, Equipped.armor_contribution(clone, 'pierce'))
        self.assertEqual(0, Equipped.armor_contribution(filtered, 'pierce'))
        clone.unequip_item('torso')
        self.assertEqual(30, Equipped.armor_contribution(mob, 'pierce'))

    def test_alignment_rejection_drops_item_without_applying_effects(self):
        for align, flag in [(800, 'ITEM_ANTI_GOOD'), (-800, 'ITEM_ANTI_EVIL'), (0, 'ITEM_ANTI_NEUTRAL')]:
            with self.subTest(flag=flag):
                self.actor.set_alignment(align)
                obj = item(flag, wearFlags=int(self.enums.get('wearFlags').ITEM_WEAR_FINGER),
                           extraFlags=int(self.enums.get('itemFlags')[flag]),
                           effects=[dict(where='TO_OBJECT', location='APPLY_HIT', modifier=25, duration=-1)])
                hp = self.actor.max_hit
                result = self.wear(obj)
                self.assertEqual('zappedItem', result.shared_messages[-1][0])
                self.assertIn(obj.id, self.room.contents)
                self.assertNotIn(obj, self.actor.owned_items())
                self.assertEqual(hp, self.actor.max_hit)

    def test_alignment_failure_after_replacement_leaves_old_ring_in_inventory(self):
        self.actor.set_alignment(800)
        for name in ('old1', 'old2'):
            self.wear(item(name, wearFlags=int(self.enums.get('wearFlags').ITEM_WEAR_FINGER)))
        obj = item('new', wearFlags=int(self.enums.get('wearFlags').ITEM_WEAR_FINGER),
                   extraFlags=int(self.enums.get('itemFlags').ITEM_ANTI_GOOD))
        result = self.wear(obj)
        self.assertEqual(['removed', 'zappedItem'], [key for key, _ in result.shared_messages])
        self.assertIsNone(self.actor.equipped.finger1)
        self.assertTrue(any(obj.id == 'old1' for obj in self.actor.loot))

    def test_no_remove_blocks_replacement_before_alignment_rejection(self):
        self.actor.set_alignment(800)
        for name in ('locked1', 'locked2'):
            self.wear(item(name, wearFlags=int(self.enums.get('wearFlags').ITEM_WEAR_FINGER),
                           extraFlags=int(self.enums.get('itemFlags').ITEM_NOREMOVE)))
        obj = item('new', wearFlags=int(self.enums.get('wearFlags').ITEM_WEAR_FINGER),
                   extraFlags=int(self.enums.get('itemFlags').ITEM_ANTI_GOOD))
        result = self.wear(obj)
        self.assertEqual('noRemove', result.blocked_key)
        self.assertIn(obj, self.actor.loot)
        self.assertNotIn(obj.id, self.room.contents)

    def test_each_equipment_command_has_content_owned_zap_messages(self):
        for command in ('wear', 'wield', 'hold'):
            data = self.command(command)
            self.assertIn('zapped', data.render_message('to_char', 'zapped_item', t='ring'))
            self.assertIn('Tester', data.render_message('to_room', 'zapped_item', c='Tester', t='ring'))

    def test_equipped_light_illuminates_dark_room_and_removal_reverses_it(self):
        self.room.room_flags = int(self.enums.get('roomFlags').ROOM_DARK)
        self.assertTrue(self.room.is_room_dark())
        self.lamp()
        self.assertEqual(1, self.room.light)
        self.assertFalse(self.room.is_room_dark())
        self.actor.unequip_item('light')
        self.assertEqual(0, self.room.light)
        self.assertTrue(self.room.is_room_dark())

    def test_zero_and_infinite_fuel_and_nonlight_slot_behavior(self):
        for fuel, expected in [('0', 0), ('-1', 1), ('10', 1)]:
            with self.subTest(fuel=fuel):
                self.lamp(fuel)
                self.assertEqual(expected, self.room.light)
                self.actor.unequip_item('light')
        self.actor.equip_item(item('rock', itemType='armor'), 'light')
        self.assertEqual(0, self.room.light)

    def test_room_entry_and_departure_are_idempotent_and_transfer_light(self):
        self.lamp()
        self.room.add_player_to_room(self.actor)
        self.assertEqual(1, self.room.light)
        self.attempt('north')
        self.assertEqual((0, 1), (self.room.light, self.destination.light))
        self.room.remove_player_from_room(self.actor)
        self.assertEqual((0, 1), (self.room.light, self.destination.light))
        self.destination.remove_player_from_room(self.actor)
        self.destination.remove_player_from_room(self.actor)
        self.assertEqual(0, self.destination.light)

    def test_light_multiple_carriers_and_base_illumination_are_preserved(self):
        self.room.light = 2
        follower = self.follower()
        self.lamp(actor=follower)
        self.lamp()
        self.assertEqual(4, self.room.light)
        self.actor.unequip_item('light')
        self.room.remove_player_from_room(follower)
        self.assertEqual(2, self.room.light)

    def test_login_loaded_light_counts_once_when_added_to_room(self):
        self.lamp()
        saved = CharacterService._serialize_character(self.actor)
        self.room.remove_player_from_room(self.actor)
        loaded = Character.from_json(json.loads(json.dumps(saved)))
        self.room.add_player_to_room(loaded)
        self.room.add_player_to_room(loaded)
        self.assertEqual(1, self.room.light)
        loaded.unequip_item('light')
        self.assertEqual(0, self.room.light)

    def test_admin_move_does_not_double_transfer_light(self):
        self.lamp()
        WizUtil.move_entity(self.rooms, self.actor, self.destination)
        self.assertEqual((0, 1), (self.room.light, self.destination.light))
        WizUtil.move_entity(self.rooms, self.actor, self.room)
        self.assertEqual((1, 0), (self.room.light, self.destination.light))

    def test_mobile_move_and_extraction_transfer_light_once(self):
        mob = self.npc()
        self.room.add_mobile_to_room(mob)
        lamp = self.lamp(actor=mob)
        MobileApi.move_mobile(self.room, self.destination, mob)
        self.assertEqual((0, 1), (self.room.light, self.destination.light))
        ItemOwnership(self.effects).detach_carried(mob, lamp)
        self.assertEqual(0, self.destination.light)
        self.destination.remove_mobile_from_room(mob)
        self.assertEqual(0, self.destination.light)

    def test_light_expiry_then_detachment_does_not_remove_another_carriers_light(self):
        follower = self.follower()
        self.lamp(actor=follower)
        self.lamp('1')
        result = self.actor.tick_light_source(self.room)
        self.assertEqual(1, self.room.light)
        ItemOwnership(self.effects).detach_carried(self.actor, result['expired_item'])
        self.assertEqual(1, self.room.light)

    def test_occupied_low_level_slot_does_not_discard_new_item(self):
        first = self.lamp()
        second = item('second', itemType='light', value2='10')
        self.actor.add_item(second)
        self.assertIsNone(self.actor.equip_item(second, 'light'))
        self.assertIn(second, self.actor.loot)
        self.assertIs(first, self.actor.equipped.light)
        self.assertEqual(1, self.room.light)


class ResetOwnershipTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.mob = self.npc()
        self.mob.max_hit = self.mob.hit = 100
        self.mob.armor_class = ArmorClass(100, 100, 100, 100)
        self.room.add_mobile_to_room(self.mob)
        self.handler = AreaHandler.__new__(AreaHandler)
        self.handler.room_registry = self.rooms
        self.handler.ItemFlags = self.enums.get('itemFlags')
        self.handler.effect_handler = self.effects
        self.handler._is_shopkeeper = lambda mob: False
        self.handler._count_live_items = lambda vnum: 0
        self.prototypes = {}
        self.handler.item_registry = NS(get=lambda **kw: self.prototypes[kw['vnum']])

    def reset(self, obj, command='E', slot=1):
        self.prototypes[obj.vnum] = obj
        return self.handler._do_mob_item_reset(True, NS(command=command, arg1=obj.vnum, arg2=10, arg3=slot), self.mob)

    def test_consecutive_g_resets_preserve_inventory_and_do_not_equip(self):
        for name in ('one', 'two'):
            self.assertTrue(self.reset(item(name, vnum=name, itemType='potion'), 'G', 0))
        self.assertEqual(2, len(self.mob.inventory))
        self.assertIsNone(self.mob.equipped)

    def test_e_reset_applies_and_reverses_resource_affect(self):
        obj = item('ring', effects=[dict(where='TO_OBJECT', type=-1, duration=-1, location='APPLY_HIT', modifier=25)])
        self.reset(obj)
        self.assertEqual(125, self.mob.max_hit)
        self.assertEqual(1, len(self.mob.effects))
        ring = self.mob.equipped.finger1
        ItemOwnership(self.effects).detach_carried(self.mob, ring)
        self.assertEqual(100, self.mob.max_hit)
        self.assertEqual([], self.mob.effects)

    def test_e_reset_armor_affects_combat_and_fueled_light_illuminates(self):
        self.reset(item('armor', vnum='armor', itemType='armor', value0='10'), slot=5)
        self.assertEqual(30, Equipped.armor_contribution(self.mob, 'pierce'))
        self.reset(item('lamp', vnum='lamp', itemType='light', value2='-1'), slot=0)
        self.assertEqual(1, self.room.light)

    def test_shop_g_stock_is_inventory_and_shop_e_stock_is_effective(self):
        self.handler._is_shopkeeper = lambda mob: True
        obj = item('ring', effects=[dict(where='TO_OBJECT', type=-1, duration=-1, location='APPLY_HIT', modifier=25)])
        self.reset(obj, 'G', 0)
        self.assertEqual(100, self.mob.max_hit)
        self.assertEqual(1, len(self.mob.inventory))
        self.reset(obj, 'E', 1)
        self.assertEqual(125, self.mob.max_hit)
        self.assertTrue(int(self.mob.equipped.finger1.extra_flags) & int(self.enums.get('itemFlags').ITEM_INVENTORY))

    def test_second_e_in_occupied_slot_retains_item_and_does_not_apply_affects(self):
        obj = item('ring', effects=[dict(where='TO_OBJECT', type=-1, duration=-1, location='APPLY_HIT', modifier=25)])
        self.reset(obj)
        self.reset(obj)
        self.assertEqual(125, self.mob.max_hit)
        self.assertEqual(2, len(self.mob.owned_items()))
        self.assertEqual(1, len(self.mob.inventory))

    def test_incompatible_e_reset_drops_in_room_without_effects(self):
        self.mob.set_alignment(800)
        self.reset(item('ring', extraFlags=int(self.enums.get('itemFlags').ITEM_ANTI_GOOD),
                        effects=[dict(where='TO_OBJECT', duration=-1, location='APPLY_HIT', modifier=25)]))
        self.assertEqual(100, self.mob.max_hit)
        self.assertEqual([], self.mob.owned_items())
        self.assertEqual(1, len(self.room.contents))

    def test_mobile_equipment_applies_combat_and_defense_modifiers_once(self):
        before_hitroll = self.mob.hit_roll
        self.mob.max_mana = 100
        effects = [dict(where='TO_OBJECT', duration=-1, location=location, modifier=modifier)
                   for location, modifier in [('APPLY_MANA', 20), ('APPLY_MOVE', 10),
                                               ('APPLY_DAMROLL', 4), ('APPLY_HITROLL', 3), ('APPLY_SAVES', -2)]]
        self.reset(item('buff-ring', effects=effects))
        self.assertEqual((120, 110, 4, before_hitroll + 3, -2),
                         (self.mob.max_mana, self.mob.max_movement, self.mob.dam_roll,
                          self.mob.hit_roll, self.mob.saving_throw))
        ItemOwnership(self.effects).detach_carried(self.mob, self.mob.equipped.finger1)
        self.assertEqual((100, 100, 0, before_hitroll, 0),
                         (self.mob.max_mana, self.mob.max_movement, self.mob.dam_roll,
                          self.mob.hit_roll, self.mob.saving_throw))

    def test_reset_equipment_clone_keeps_affects_once_and_is_independent(self):
        self.mob.hit_dice = self.mob.mana_dice = self.mob.damage_dice = Dice(1, 6, 0)
        self.mob.max_mana = self.mob.mana = 100
        self.reset(item('ring', effects=[dict(where='TO_OBJECT', duration=-1, location='APPLY_HIT', modifier=25)]))
        clone = MobileFactory.copy_instance(self.mob, self.enums, effect_handler=self.effects)
        self.assertEqual(125, clone.max_hit)
        self.assertEqual(1, len(clone.effects))
        ItemOwnership(self.effects).detach_carried(clone, clone.equipped.finger1)
        self.assertEqual(100, clone.max_hit)
        self.assertEqual(125, self.mob.max_hit)

    def test_invalid_e_slot_keeps_inventory_without_crashing(self):
        self.assertTrue(self.reset(item('invalid'), slot=999))
        self.assertEqual(1, len(self.mob.inventory))


if __name__ == '__main__':
    unittest.main()

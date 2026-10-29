import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_shared_gameplay_parity import SharedFixture, item
from api.CharacterApi import CharacterApi
from api.MovementApi import MovementApi
from area.Exit import Exit
from area.Room import Room
from interp.Context import Context
from interp.commands.Movement import Movement
from skill.Ability import Ability


class MovementFixture(SharedFixture):
    def setUp(self):
        super().setUp()
        self.room.vnum = '100'
        self.destination = Room(id='destination', vnum='101', area_id='area', sector_type=0)
        self.temple = Room(id='temple', vnum='3001', area_id='temple-area', sector_type=0)
        self.world = [self.room, self.destination, self.temple]
        self.rooms.all_rooms = lambda: self.world
        self.rooms.get_or_none = lambda **kw: next((room for room in self.world if all(str(getattr(room, key)) == str(value) for key, value in kw.items())), None)
        self.registries.room_registry = self.rooms
        self.fight = NS(stop_fighting=Mock(side_effect=lambda character, **kw: setattr(character, 'fighting', None)),
                        aggressive_entry_rounds=lambda *args: [])
        self.movement = Movement(self.registries, NS(), self.fight, self.enums, self.api, self.skill_api, self.effects)
        self.exit_flags = self.enums.get('exitFlags')
        self.exit = Exit(0, '', 'gate', int(self.exit_flags.EX_ISDOOR), 99, 101, self.destination.id, self.room.id)
        self.reverse = Exit(2, '', 'gate', int(self.exit_flags.EX_ISDOOR), 99, 100, self.room.id, self.destination.id)
        self.room.exits = [self.exit]
        self.destination.exits = [self.reverse]
        self.key = item('key', vnum='99')
        self.actor.loot.append(self.key)

    def ctx(self, name, text='', character=None):
        character = character or self.actor
        context = Context(character=character, command=self.command(name), parameters=[], result=text,
                          room=self.rooms.get_or_none(id=character.room_id))
        context.room_registry = self.rooms
        return context

    def attempt(self, name, text='', character=None):
        return getattr(self.movement, 'do_' + name)(character or self.actor, self.ctx(name, text, character))

    def portal(self, charges=0, gates=0, flags=0):
        portal = item('portal', itemType='portal', value0=str(charges), value1=str(flags),
                      value2=str(gates), value3=self.destination.vnum, value4='99')
        self.room.add_item_to_room(portal)
        return portal

    def follower(self, name='follower'):
        follower = self.character(name)
        follower.master = self.actor
        follower.character_attributes.position = CharacterApi.pos_value('POS_STANDING')
        follower.room_id = self.room.id
        self.room.add_player_to_room(follower)
        return follower

    @staticmethod
    def message_keys(payload):
        return ([payload['message_key']] if payload.get('message_key') else []) + [key for entry in payload.get('payloads', []) for key in MovementFixture.message_keys(entry)]


class TravelRulesTests(MovementFixture, unittest.TestCase):
    def test_affect_flight_allows_air_and_water_without_changing_posture(self):
        self.flag(self.actor, 'AFF_FLYING')
        for sector in ['SECT_AIR', 'SECT_WATER_NOSWIM']:
            self.destination.sector_type = int(getattr(self.enums.get('sectorTypes'), sector))
            state = MovementApi.move_state(self.ctx('north'))
            self.assertFalse(state.air_blocked or state.water_blocked)
        self.assertTrue(CharacterApi.is_flying(self.actor))
        self.assertEqual(CharacterApi.pos_value('POS_STANDING'), CharacterApi.position_value(self.actor))

    def test_closed_pass_door_nopass_and_angel_threshold(self):
        self.exit.exit_flags |= self.exit_flags.EX_CLOSED
        self.flag(self.actor, 'AFF_PASS_DOOR')
        self.assertFalse(MovementApi.move_state(self.ctx('north')).exit_closed)
        self.exit.exit_flags |= self.exit_flags.EX_NOPASS
        self.assertTrue(MovementApi.move_state(self.ctx('north')).exit_closed)
        self.actor.trust = int(self.enums.get('gameParameters').ANGEL)
        self.assertFalse(MovementApi.move_state(self.ctx('north')).exit_closed)

    def test_immortal_water_needs_no_boat(self):
        self.destination.sector_type = int(self.enums.get('sectorTypes').SECT_WATER_NOSWIM)
        self.assertTrue(MovementApi.move_state(self.ctx('north')).water_blocked)
        self.actor.trust = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        self.assertFalse(MovementApi.move_state(self.ctx('north')).water_blocked)

    def test_zero_cost_haste_and_wait_preserve_existing_larger_wait(self):
        self.room.sector_type = 0
        self.flag(self.actor, 'AFF_HASTE')
        self.actor.movement = 0
        self.actor.status_flags.pulse_wait = 5
        self.assertEqual(0, MovementApi.move_state(self.ctx('north')).move_cost)
        self.attempt('north')
        self.assertEqual(self.destination.id, self.actor.room_id)
        self.assertEqual(0, self.actor.movement)
        self.assertEqual(5, self.actor.status_flags.pulse_wait)

    def test_direction_imposes_one_pulse_wait(self):
        self.attempt('north')
        self.assertEqual(1, self.actor.status_flags.pulse_wait)

    def test_room_visibility_and_other_class_guild_reject_before_charge(self):
        initial = self.actor.movement
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_NEWBIES_ONLY)
        self.assertEqual('invalid_exit', self.attempt('north')['blocked_key'])
        self.destination.room_flags = 0
        self.destination.vnum = '3018'
        self.assertEqual('wrong_guild', self.attempt('north')['blocked_key'])
        self.assertEqual(initial, self.actor.movement)

    def test_charm_cannot_leave_master_but_can_follow_moving_master(self):
        follower = self.follower()
        self.flag(follower, 'AFF_CHARM')
        self.assertEqual('charmed_departure', self.attempt('north', character=follower)['blocked_key'])
        self.attempt('north')
        self.assertEqual(self.destination.id, follower.room_id)

    def test_room_owner_can_enter_but_other_players_cannot(self):
        self.destination.owner = self.actor.name
        self.assertFalse(MovementApi.move_state(self.ctx('north')).private_room)
        self.destination.owner = 'somebody else'
        self.assertTrue(MovementApi.move_state(self.ctx('north')).private_room)

    def test_aggressive_npc_follower_stays_out_of_law_room(self):
        mob = self.npc()
        mob.master = self.actor
        mob.status_flags.set_flag('act', self.enums.get('actBits').ACT_AGGRESSIVE)
        self.room.add_mobile_to_room(mob)
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_LAW)
        self.attempt('north')
        self.assertEqual(self.room.id, mob.room_id)


class RecallRulesTests(MovementFixture, unittest.TestCase):
    def test_curse_and_no_recall_leave_resources_and_combat_intact(self):
        self.actor.fighting = self.victim
        self.flag(self.actor, 'AFF_CURSE')
        self.assertIn('no_recall', self.message_keys(self.attempt('recall')))
        self.assertEqual(self.room.id, self.actor.room_id)
        self.fight.stop_fighting.assert_not_called()
        self.flag(self.actor, 'AFF_CURSE', False)
        self.room.room_flags = int(self.enums.get('roomFlags').ROOM_NO_RECALL)
        self.assertIn('no_recall', self.message_keys(self.attempt('recall')))

    def test_combat_failure_strict_endpoint_wait_and_no_cost(self):
        self.actor.fighting = self.victim
        self.actor.set_learned('recall', 90, create=True)
        movement = self.actor.movement
        with patch('random.randint', return_value=71), patch.object(Ability, 'check_improve_by_name') as improve:
            self.assertIn('failed', self.message_keys(self.attempt('recall')))
        improve.assert_called_once_with(self.actor, 'recall', False, 6)
        self.assertEqual(4, self.actor.status_flags.pulse_wait)
        self.assertEqual((self.room.id, movement), (self.actor.room_id, self.actor.movement))

    def test_combat_success_charges_connected_xp_and_halves_move(self):
        self.actor.fighting = self.victim
        self.actor.set_learned('recall', 90, create=True)
        attrs = self.actor.character_attributes
        attrs.accumulated_experience = 20500
        attrs.experience = 500
        context = self.ctx('recall')
        context.conn = NS()
        with patch('random.randint', return_value=72), patch.object(Ability, 'check_improve_by_name'):
            self.movement.do_recall(self.actor, context)
        self.assertEqual(20475, attrs.accumulated_experience)
        self.assertEqual(self.temple.id, self.actor.room_id)
        self.assertEqual(9, self.actor.movement)
        self.fight.stop_fighting.assert_called_once_with(self.actor, both=True)

    def test_linkdead_combat_success_costs_fifty_xp(self):
        self.actor.fighting = self.victim
        self.actor.character_attributes.accumulated_experience = 20500
        with patch('random.randint', return_value=100), patch.object(Ability, 'check_improve_by_name'):
            self.attempt('recall')
        self.assertEqual(20450, self.actor.character_attributes.accumulated_experience)

    def test_pet_recalls_and_non_pet_npc_is_rejected(self):
        pet = self.npc()
        pet.movement = 20
        self.room.add_mobile_to_room(pet)
        self.assertIn('is_pet', self.message_keys(self.attempt('recall', character=pet)))
        pet.status_flags.set_flag('act', self.enums.get('actBits').ACT_PET)
        self.actor.pet = pet
        self.attempt('recall')
        self.assertEqual((self.temple.id, self.temple.id), (self.actor.room_id, pet.room_id))
        self.assertIn(pet.id, self.temple.mobiles)


class LockRulesTests(MovementFixture, unittest.TestCase):
    def test_exit_lock_unlock_open_close_cycle_mirrors_reverse(self):
        for action in ['close', 'lock', 'unlock', 'open']:
            with self.subTest(action=action):
                self.assertTrue(self.attempt(action, 'gate')['lock_succeeded'])
                self.assertEqual(self.exit.exit_flags, self.reverse.exit_flags)
        self.assertFalse(self.exit.exit_flags & self.exit_flags.EX_CLOSED)

    def test_container_cycle_and_portal_use_different_key_fields(self):
        container_flags = self.enums.get('containerState')
        chest = item('chest', value1=str(int(container_flags.CONT_CLOSEABLE)), value2='99')
        self.room.add_item_to_room(chest)
        for action in ['close', 'lock', 'unlock', 'open']:
            self.assertTrue(self.attempt(action, 'chest')['lock_succeeded'])
        portal = self.portal(flags=int(self.exit_flags.EX_ISDOOR))
        for action in ['close', 'lock', 'unlock', 'open']:
            self.assertTrue(self.attempt(action, 'portal')['lock_succeeded'])
        self.assertFalse(int(portal.value1) & self.exit_flags.EX_CLOSED)

    def test_no_close_no_lock_and_non_door_reject(self):
        portal = self.portal(flags=int(self.exit_flags.EX_ISDOOR | self.exit_flags.EX_NOCLOSE))
        self.assertEqual('lock_invalid', self.attempt('close', 'portal')['blocked_key'])
        portal.value1 = str(int(self.exit_flags.EX_ISDOOR | self.exit_flags.EX_CLOSED | self.exit_flags.EX_NOLOCK))
        self.assertEqual('lock_no_keyhole', self.attempt('lock', 'portal')['blocked_key'])
        self.exit.exit_flags = 0
        self.assertEqual('lock_invalid', self.attempt('open', 'gate')['blocked_key'])

    def test_pick_guard_precedes_roll_and_bad_target_but_applies_wait(self):
        guard = self.npc()
        guard.level = 26
        self.room.add_mobile_to_room(guard)
        with patch('random.randint') as roll:
            self.assertEqual('lock_guard', self.attempt('pick', 'missing')['message_key'])
        roll.assert_not_called()
        self.assertEqual(self.skills['pick lock'].beats, self.actor.status_flags.pulse_wait)

    def test_guard_exactly_five_levels_higher_does_not_block_pick_roll(self):
        guard = self.npc()
        guard.level = 25
        self.room.add_mobile_to_room(guard)
        with patch('random.randint', return_value=1) as roll, patch.object(Ability, 'check_improve_by_name'):
            self.attempt('pick', 'missing')
        roll.assert_called_once()

    def test_pick_unlearned_fails_and_exact_proficiency_succeeds(self):
        self.exit.exit_flags |= self.exit_flags.EX_CLOSED | self.exit_flags.EX_LOCKED
        with patch('random.randint', return_value=1), patch.object(Ability, 'check_improve_by_name') as improve:
            self.assertEqual('lock_failed', self.attempt('pick', 'gate')['message_key'])
        improve.assert_called_once_with(self.actor, 'pick lock', False, 2)
        self.actor.set_learned('pick lock', 60, create=True)
        with patch('random.randint', return_value=60), patch.object(Ability, 'check_improve_by_name') as improve:
            self.assertTrue(self.attempt('pick', 'gate')['lock_succeeded'])
        improve.assert_called_once_with(self.actor, 'pick lock', True, 2)

    def test_pick_keyless_pickproof_immortal_exception_only_for_doors(self):
        self.actor.level = 53
        self.actor.set_learned('pick lock', 100, create=True)
        self.exit.key = -1
        self.exit.exit_flags |= self.exit_flags.EX_LOCKED | self.exit_flags.EX_PICKPROOF
        with patch('random.randint', return_value=100), patch.object(Ability, 'check_improve_by_name'):
            self.assertTrue(self.attempt('pick', 'gate')['lock_succeeded'])
            portal = self.portal(flags=int(self.exit_flags.EX_ISDOOR | self.exit_flags.EX_CLOSED | self.exit_flags.EX_PICKPROOF))
            self.assertEqual('lock_failed', self.attempt('pick', 'portal')['blocked_key'])


class PortalRulesTests(MovementFixture, unittest.TestCase):
    def test_fixed_portal_obeys_room_visibility_and_implementor_privacy(self):
        self.portal()
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_NEWBIES_ONLY)
        self.assertIn('doesn_t_seem_go', self.message_keys(self.attempt('enter', 'portal')))
        self.actor.level = 53
        self.destination.owner = 'owner'
        self.destination.room_flags = 0
        self.assertIn('doesn_t_seem_go', self.message_keys(self.attempt('enter', 'portal')))
        self.actor.trust = 60
        self.attempt('enter', 'portal')
        self.assertEqual(self.destination.id, self.actor.room_id)

    def test_random_room_filters_flags_law_visibility_and_keeps_origin_candidate(self):
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_SAFE)
        self.temple.room_flags = int(self.enums.get('roomFlags').ROOM_LAW)
        with patch('random.choice', side_effect=lambda rooms: rooms[0]) as choose:
            self.assertIs(self.room, self.movement._random_room(self.actor))
        self.assertEqual([self.room], choose.call_args.args[0])

    def test_buggy_portal_four_percent_strict_endpoint(self):
        portal = self.portal(gates=int(self.enums.get('gateFlags').GATE_BUGGY))
        with patch('random.randint', return_value=5), patch.object(self.movement, '_random_room') as random_room:
            self.assertIs(self.destination, self.movement._portal_destination(portal, self.room, self.actor))
            random_room.assert_not_called()
        with patch('random.randint', return_value=4), patch.object(self.movement, '_random_room', return_value=self.temple):
            self.assertIs(self.temple, self.movement._portal_destination(portal, self.room, self.actor))

    def test_two_charge_portal_moves_one_follower_then_expires_once(self):
        first, second = self.follower('first'), self.follower('second')
        portal = self.portal(charges=2)
        payload = self.attempt('enter', 'portal')
        self.assertEqual((self.destination.id, self.destination.id, self.room.id), (self.actor.room_id, first.room_id, second.room_id))
        self.assertNotIn(portal.id, self.room.contents)
        self.assertEqual(1, self.message_keys(payload).count('fades_out_existence'))

    def test_unlimited_portal_moves_sleeping_charmed_follower(self):
        follower = self.follower()
        self.flag(follower, 'AFF_CHARM')
        CharacterApi.set_position(follower, 'POS_SLEEPING')
        self.portal()
        self.attempt('enter', 'portal')
        self.assertEqual(self.destination.id, follower.room_id)

    def test_go_with_portal_moves_away_before_followers_can_enter(self):
        follower = self.follower()
        portal = self.portal(gates=int(self.enums.get('gateFlags').GATE_GOWITH))
        self.attempt('enter', 'portal')
        self.assertIn(portal.id, self.destination.contents)
        self.assertEqual(self.room.id, follower.room_id)

    def test_magically_sleeping_charmed_follower_does_not_wake(self):
        follower = self.follower()
        self.flag(follower, 'AFF_CHARM')
        self.flag(follower, 'AFF_SLEEP')
        CharacterApi.set_position(follower, 'POS_SLEEPING')
        self.portal()
        self.attempt('enter', 'portal')
        self.assertEqual(self.room.id, follower.room_id)
        self.assertEqual(CharacterApi.pos_value('POS_SLEEPING'), CharacterApi.position_value(follower))

    def test_invisible_portal_is_not_a_valid_target_without_detection(self):
        portal = self.portal()
        portal.extra_flags = int(self.enums.get('itemFlags').ITEM_INVIS)
        self.assertIn('don_t_see', self.message_keys(self.attempt('enter', 'portal')))
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        self.attempt('enter', 'portal')
        self.assertEqual(self.destination.id, self.actor.room_id)


class PostureAndVisibilityTests(MovementFixture, unittest.TestCase):
    def bed(self, flags=None):
        furniture = self.enums.get('furnitureFlags')
        bed = item('bed', itemType='furniture', value0='1', value2=str(int(flags if flags is not None else furniture.SLEEP_ON | furniture.REST_ON | furniture.SIT_ON | furniture.STAND_ON)), value3='200', value4='150')
        self.room.add_item_to_room(bed)
        return bed

    def test_sleep_on_bed_sets_regeneration_and_stand_detaches(self):
        bed = self.bed()
        self.attempt('sleep', 'bed')
        self.assertIs(bed, self.actor.on)
        self.assertEqual(20, self.actor._apply_furniture_regen_rate(10, 'value3'))
        self.attempt('stand')
        self.assertIsNone(self.actor.on)
        self.assertEqual(10, self.actor._apply_furniture_regen_rate(10, 'value3'))

    def test_capacity_and_unsupported_posture_reject_without_position_change(self):
        bed = self.bed(self.enums.get('furnitureFlags').SLEEP_ON)
        self.assertEqual('posture_invalid', self.attempt('sit', 'bed')['message_key'])
        follower = self.follower()
        follower.on = bed
        self.assertEqual('posture_full', self.attempt('sleep', 'bed')['message_key'])
        self.assertEqual(CharacterApi.pos_value('POS_STANDING'), CharacterApi.position_value(self.actor))

    def test_existing_user_can_reuse_full_furniture(self):
        bed = self.bed()
        self.actor.on = bed
        self.attempt('rest')
        self.assertIs(bed, self.actor.on)
        self.assertEqual(CharacterApi.pos_value('POS_RESTING'), CharacterApi.position_value(self.actor))

    def test_magical_sleep_cannot_wake_and_moving_clears_furniture(self):
        bed = self.bed()
        self.attempt('sleep', 'bed')
        self.flag(self.actor, 'AFF_SLEEP')
        self.assertEqual('can_t_wake_up', self.attempt('stand')['message_key'])
        self.flag(self.actor, 'AFF_SLEEP', False)
        CharacterApi.set_position(self.actor, 'POS_STANDING')
        self.attempt('north')
        self.assertIsNone(self.actor.on)

    def test_removing_furniture_clears_occupants(self):
        bed = self.bed()
        self.actor.on = bed
        self.room.remove_item_from_room(bed)
        self.assertIsNone(self.actor.on)

    def test_visible_strips_all_concealment_effect_records_and_flags(self):
        from item.Effect import Effect
        for effect_type, bit in [('spell.invis', 'AFF_INVISIBLE'), ('spell.mass_invis', 'AFF_INVISIBLE'), ('skill.sneak', 'AFF_SNEAK')]:
            self.effects.affect_to_char(self.actor, Effect(type=effect_type, where='TO_AFFECTS', bitvector=bit))
        self.flag(self.actor, 'AFF_HIDE')
        self.attempt('visible')
        self.assertEqual([], self.actor.effects)
        for flag in ['AFF_HIDE', 'AFF_INVISIBLE', 'AFF_SNEAK']:
            self.assertFalse(CharacterApi.is_affected_by_name(self.actor, self.enums.get('affectedBy'), flag))


if __name__ == '__main__':
    unittest.main()

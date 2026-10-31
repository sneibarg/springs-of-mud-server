import asyncio
import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_movement_rules_parity import MovementFixture
from api.CharacterApi import CharacterApi
from api.MobileApi import MobileApi
from area.Room import Room
from item.Effect import Effect
from item.EffectUpdateHandler import EffectUpdateHandler
from interp.commands.Fight import Fight
from interp.Context import Context
from player.PlayerHandler import PlayerHandler
from mobile.MobileContext import MobileContext
from mobile.MobileHandler import MobileHandler
from skill.Spell import Spell
from devtools.collection_query import load_collections
from tests.test_review_application_fixes import ROOT
from util.WizUtil import WizUtil


class PlagueEntryTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.bus = NS(send_to_character=AsyncMock(), send_to_room=AsyncMock(), text_to_message=lambda text: text)
        self.fight._check_immunity = lambda *args: 'IS_NORMAL'
        self.fight.apply_periodic_damage = AsyncMock()
        self.ticks = EffectUpdateHandler(self.registries, self.enums, self.effects, self.fight, self.bus)
        self.ticks.rng = Mock(number_range=Mock(return_value=7), number_bits=Mock(return_value=0))
        doc = next(d for d in load_collections(ROOT / 'resources/collections', ['spells'])['spells'].documents if d['name'] == 'plague')
        self.spell = Spell.from_json(deepcopy(doc))
        self.registries.spell_registry = NS(all_spells=lambda: [self.spell])
        self.ticks.spell_registry = self.registries.spell_registry
        self.destination.add_player_to_room(self.victim)
        self.victim.room_id = self.destination.id
        Room.configure_entry_handler(self.ticks.room_entered)
        self.addCleanup(Room.configure_entry_handler)
        self.saves = self.enterContext(patch('item.EffectUpdateHandler.EffectUtil.saves_spell', return_value=False))

    def plague(self, level=20, actor=None):
        actor = actor or self.actor
        return self.effects.affect_to_char(actor, Effect(where='TO_AFFECTS', type='spell.plague', level=level,
            duration=10, location='APPLY_STR', modifier=-5, bitvector='AFF_PLAGUE'))

    async def test_walking_infects_before_returning_with_entry_chance_and_no_periodic_drain(self):
        self.plague()
        strength = self.victim.character_attributes.strength
        mana, hit = self.actor.mana, self.actor.hit
        self.attempt('north')
        effect = self.victim.find_effect('spell.plague')
        self.assertEqual((19, 7, -5, 'APPLY_STR'), (effect.level, effect.duration, effect.modifier, effect.location))
        self.assertEqual(strength - 5, self.victim.character_attributes.strength)
        self.assertEqual((mana, hit), (self.actor.mana, self.actor.hit))
        self.ticks.rng.number_bits.assert_called_once_with(6)
        self.saves.assert_any_call(17, self.victim, 'DAM_DISEASE', immunity=self.fight._check_immunity)
        self.fight.apply_periodic_damage.assert_not_awaited()
        await asyncio.sleep(0)
        self.assertTrue(any('hot and feverish' in str(call) for call in self.bus.send_to_character.call_args_list))

    async def test_successful_save_prevents_entry_infection(self):
        self.plague()
        self.saves.return_value = True
        self.attempt('north')
        self.assertIsNone(self.victim.find_effect('spell.plague'))
        self.ticks.rng.number_bits.assert_not_called()

    async def test_nonzero_six_bit_roll_prevents_entry_infection(self):
        self.plague()
        self.ticks.rng.number_bits.return_value = 63
        self.attempt('north')
        self.assertIsNone(self.victim.find_effect('spell.plague'))
        self.ticks.rng.number_bits.assert_called_once_with(6)

    async def test_level_one_plague_does_not_spread(self):
        self.plague(1)
        self.attempt('north')
        self.saves.assert_not_called()
        self.ticks.rng.number_range.assert_not_called()

    async def test_orphan_flag_clears_on_entry_without_spreading(self):
        self.flag(self.actor, 'AFF_PLAGUE')
        self.attempt('north')
        self.assertFalse(self.actor.is_affected(self.enums.get('affectedBy'), 'AFF_PLAGUE'))
        self.assertIsNone(self.victim.find_effect('spell.plague'))

    async def test_immortal_and_already_infected_targets_are_skipped_after_saves(self):
        self.plague()
        self.victim.level = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        self.attempt('north')
        self.assertIsNone(self.victim.find_effect('spell.plague'))
        self.ticks.rng.number_bits.assert_not_called()
        self.assertTrue(self.saves.called)

    async def test_existing_plague_is_not_joined_again(self):
        self.plague()
        original = self.plague(actor=self.victim)
        self.attempt('north')
        self.assertIs(original, self.victim.find_effect('spell.plague'))
        self.assertEqual(1, len(self.victim.effects))
        self.ticks.rng.number_bits.assert_not_called()

    async def test_duplicate_membership_does_not_reroll_exposure(self):
        self.plague()
        self.attempt('north')
        self.saves.reset_mock()
        self.destination.add_player_to_room(self.actor)
        self.saves.assert_not_called()
        await asyncio.sleep(0)

    async def test_portal_and_administrator_relocation_share_entry_hook(self):
        self.plague()
        self.portal()
        self.attempt('enter', 'portal')
        self.assertIsNotNone(self.victim.find_effect('spell.plague'))
        await asyncio.sleep(0)
        self.effects.affect_strip(self.victim, 'spell.plague')
        WizUtil.move_entity(self.rooms, self.actor, self.room)
        WizUtil.move_entity(self.rooms, self.actor, self.destination)
        self.assertIsNotNone(self.victim.find_effect('spell.plague'))
        await asyncio.sleep(0)

    async def test_mobile_entry_infects_players(self):
        mob = self.npc()
        self.plague(actor=mob)
        self.destination.add_mobile_to_room(mob)
        self.assertIsNotNone(self.victim.find_effect('spell.plague'))
        await asyncio.sleep(0)

    async def test_tick_retains_four_bit_probability_and_periodic_damage(self):
        self.plague()
        self.room.remove_player_from_room(self.actor)
        Room.configure_entry_handler()
        self.destination.add_player_to_room(self.actor)
        await self.ticks._tick_plague(self.actor, self.destination)
        self.ticks.rng.number_bits.assert_called_once_with(4)
        self.fight.apply_periodic_damage.assert_awaited_once()

    async def test_room_entry_hook_can_be_reset(self):
        self.plague()
        Room.configure_entry_handler()
        self.attempt('north')
        self.saves.assert_not_called()


class TravelIntegrationTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.mob = self.npc()
        self.room.add_mobile_to_room(self.mob)
        self.mobile_handler = NS(room_registry=self.rooms, exit_flags=self.enums.get('exitFlags'),
            room_flags=self.enums.get('roomFlags'), act_bits=self.enums.get('actBits'), movement_commands=self.movement)
        self.commands = Fight.__new__(Fight)
        self.commands.room_registry, self.commands.interp_api = self.rooms, self.api
        self.commands.fight_handler, self.commands.movement_commands = self.fight, self.movement
        self.commands.AffectBits = self.enums.get('affectedBy')
        self.actor.fighting = self.victim
        self.actor.character_attributes.position = CharacterApi.pos_value('POS_FIGHTING')

    def wander(self):
        ctx = MobileContext(self.mob, self.room, self.mobile_handler)
        return MobileApi._move_mobile_direction(ctx, 0), ctx

    def flee(self):
        with patch('interp.commands.Fight.random.randint', return_value=0):
            return self.commands.do_flee(self.actor, self.ctx('flee'))

    def test_wander_rejects_invisible_and_nonowner_private_room(self):
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_IMP_ONLY)
        self.assertFalse(self.wander()[0])
        self.destination.room_flags = 0
        self.destination.owner = 'someone else'
        self.assertFalse(self.wander()[0])
        self.assertEqual(self.room.id, self.mob.room_id)

    def test_room_owner_npc_can_wander_into_owned_room(self):
        self.destination.owner = self.mob.name
        moved, ctx = self.wander()
        self.assertTrue(moved)
        self.assertEqual(self.destination.id, self.mob.room_id)
        self.assertEqual('north', ctx.payloads[0]['context'].command.name)

    def test_wander_retains_closed_no_mob_stay_area_and_indoor_prefilters(self):
        self.exit.exit_flags |= int(self.enums.get('exitFlags').EX_CLOSED)
        self.assertFalse(self.wander()[0])
        self.exit.exit_flags = 0
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_NO_MOB)
        self.assertFalse(self.wander()[0])
        self.destination.room_flags = 0
        self.mob.status_flags.set_flag('act', self.enums.get('actBits').ACT_STAY_AREA)
        self.destination.area_id = 'other'
        self.assertFalse(self.wander()[0])
        self.destination.area_id = self.room.area_id
        self.mob.status_flags.set_flag('act', self.enums.get('actBits').ACT_OUTDOORS)
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_INDOORS)
        self.assertFalse(self.wander()[0])

    def test_wandering_mobile_brings_eligible_standing_follower(self):
        follower = self.follower()
        follower.master = self.mob
        self.assertTrue(self.wander()[0])
        self.assertEqual(self.destination.id, follower.room_id)
        self.assertEqual(1, follower.status_flags.pulse_wait)

    def test_flee_brings_standing_follower_charges_once_and_preserves_context(self):
        follower = self.follower()
        before = follower.movement
        context = self.ctx('flee')
        with patch('interp.commands.Fight.random.randint', return_value=0):
            payload = self.commands.do_flee(self.actor, context)
        self.assertEqual(self.destination.id, follower.room_id)
        self.assertEqual(before - 1, follower.movement)
        self.assertEqual(1, follower.status_flags.pulse_wait)
        self.assertEqual('flee', context.command.name)
        self.assertEqual('north', payload['payloads'][0]['context'].command.name)
        self.fight.stop_fighting.assert_called_once_with(self.actor, both=True)

    def test_charmed_sleeping_follower_wakes_but_magical_sleep_does_not(self):
        follower = self.follower('ordinary sleeper')
        magical = self.follower('magic sleeper')
        for entity in (follower, magical):
            self.flag(entity, 'AFF_CHARM')
            entity.character_attributes.position = CharacterApi.pos_value('POS_SLEEPING')
        self.flag(magical, 'AFF_SLEEP')
        self.flee()
        self.assertEqual(self.destination.id, follower.room_id)
        self.assertEqual(self.room.id, magical.room_id)

    def test_fighting_charmed_follower_is_not_forced_to_stand(self):
        follower = self.follower()
        follower.fighting = self.mob
        self.flag(follower, 'AFF_CHARM')
        follower.character_attributes.position = CharacterApi.pos_value('POS_FIGHTING')
        self.flee()
        self.assertEqual(self.room.id, follower.room_id)
        self.assertEqual(CharacterApi.pos_value('POS_FIGHTING'), CharacterApi.position_value(follower))

    def test_incapacitated_charmed_follower_cannot_be_stood_up_by_flee(self):
        follower = self.follower()
        self.flag(follower, 'AFF_CHARM')
        follower.character_attributes.position = CharacterApi.pos_value('POS_INCAP')
        self.flee()
        self.assertEqual(self.room.id, follower.room_id)
        self.assertEqual(CharacterApi.pos_value('POS_INCAP'), CharacterApi.position_value(follower))

    def test_exhausted_follower_stays_when_leader_flees(self):
        follower = self.follower()
        follower.movement = 0
        self.flee()
        self.assertEqual(self.destination.id, self.actor.room_id)
        self.assertEqual(self.room.id, follower.room_id)

    def test_aggressive_npc_follower_stays_out_of_law_room(self):
        self.mob.master = self.actor
        self.mob.character_attributes.position = CharacterApi.pos_value('POS_STANDING')
        self.mob.status_flags.set_flag('act', self.enums.get('actBits').ACT_AGGRESSIVE)
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_LAW)
        self.flee()
        self.assertEqual(self.room.id, self.mob.room_id)

    def test_follow_chain_moves_once_without_recursive_cycle(self):
        first = self.follower('first')
        second = self.follower('second')
        second.master = first
        self.actor.master = second
        self.flee()
        self.assertEqual([self.destination.id] * 3, [p.room_id for p in (self.actor, first, second)])


class MobileTravelEmissionTests(unittest.IsolatedAsyncioTestCase):
    async def test_mobile_travel_context_receives_handlers_for_player_followers(self):
        handler = MobileHandler.__new__(MobileHandler)
        handler.handler_service = object()
        handler.player_handler = NS(_emit_standard_payload=AsyncMock())
        context = Context(character=object())
        payload = {'actor': context.character, 'context': context, 'payloads': []}
        await handler._handle_payload(payload)
        self.assertIs(context.handler_service, handler.handler_service)
        handler.player_handler._emit_standard_payload.assert_awaited_once()

    async def test_mobile_payload_preserves_existing_handlers(self):
        handler = MobileHandler.__new__(MobileHandler)
        handler.handler_service = object()
        handler.player_handler = NS(_emit_standard_payload=AsyncMock())
        service = object()
        context = Context(character=object(), handler_service=service)
        await handler._handle_payload({'actor': context.character, 'context': context})
        self.assertIs(service, context.handler_service)

    async def test_npc_destination_does_not_request_room_display(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        context = Context(character=object())
        with patch.object(CharacterApi, 'is_npc', return_value=True):
            await handler._show_room_to_character(context.character, object(), context)

    async def test_mobile_travel_uses_standard_payload_emitter(self):
        handler = MobileHandler.__new__(MobileHandler)
        handler.player_handler = NS(_emit_standard_payload=AsyncMock())
        payload = {'actor': object(), 'context': object(), 'payloads': []}
        await handler._handle_payload(payload)
        handler.player_handler._emit_standard_payload.assert_awaited_once_with(payload['actor'], payload, context=payload['context'])


if __name__ == '__main__':
    unittest.main()

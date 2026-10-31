import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_movement_rules_parity import MovementFixture
from api.CharacterApi import CharacterApi
from interp.Context import Context
from interp.InterpHandler import InterpHandler
from interp.commands.Fight import Fight
from player.PlayerHandler import PlayerHandler
from util.InterpUtil import InterpUtil


class FleeParityTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.commands = Fight.__new__(Fight)
        self.commands.movement_commands = self.movement
        self.commands.room_registry = self.rooms
        self.commands.interp_api = self.api
        self.commands.fight_handler = self.fight
        self.commands.AffectBits = self.enums.get('affectedBy')
        self.actor.fighting = self.victim
        self.actor.character_attributes.position = CharacterApi.pos_value('POS_FIGHTING')
        self.actor.exp = 10000

    def flee(self, actor=None):
        actor = actor or self.actor
        with patch('interp.commands.Fight.random.randint', return_value=0):
            return self.commands.do_flee(actor, self.ctx('flee', character=actor))

    def assert_blocked(self):
        movement = self.actor.movement
        result = self.flee()
        self.assertEqual(self.actor.room_id, self.room.id)
        self.assertIs(self.actor.fighting, self.victim)
        self.assertEqual(self.actor.movement, movement)
        self.assertEqual(self.actor.status_flags.pulse_wait, 0)
        self.assertEqual(result['blocked_key'], 'no_destination')

    def test_zero_movement_hasted_inside_flee_succeeds_and_waits(self):
        self.room.sector_type = self.destination.sector_type = 0
        self.flag(self.actor, 'AFF_HASTE')
        self.actor.movement = 0
        self.actor.on = object()
        self.flee()
        self.assertEqual(self.actor.room_id, self.destination.id)
        self.assertEqual(self.actor.movement, 0)
        self.assertEqual(self.actor.status_flags.pulse_wait, 1)
        self.assertIsNone(self.actor.on)
        self.assertIsNone(self.actor.fighting)
        self.fight.stop_fighting.assert_called_once_with(self.actor, both=True)

    def test_existing_wait_is_preserved(self):
        self.actor.status_flags.pulse_wait = 5
        self.flee()
        self.assertEqual(self.actor.status_flags.pulse_wait, 5)

    def test_invisible_destination_is_rejected(self):
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_NEWBIES_ONLY)
        self.assert_blocked()

    def test_charm_blocks_departure_from_present_master(self):
        self.actor.master = self.victim
        self.flag(self.actor, 'AFF_CHARM')
        self.assert_blocked()

    def test_other_class_guild_is_rejected(self):
        self.destination.vnum = '3018'
        self.exit.to_room_vnum = 3018
        self.assert_blocked()

    def test_owner_can_flee_into_private_room(self):
        self.destination.owner = self.actor.name
        self.flee()
        self.assertEqual(self.actor.room_id, self.destination.id)

    def test_nonowner_cannot_flee_into_private_room(self):
        self.destination.owner = 'someone else'
        self.assert_blocked()

    def test_closed_exit_is_rejected_even_for_trusted_passdoor_actor(self):
        self.actor.trust = int(self.enums.get('gameParameters').IMPLEMENTOR)
        self.flag(self.actor, 'AFF_PASS_DOOR')
        self.exit.exit_flags |= int(self.exit_flags.EX_CLOSED)
        self.assert_blocked()

    def test_insufficient_movement_is_rejected(self):
        self.actor.movement = 0
        self.assert_blocked()

    def test_immortal_needs_no_boat(self):
        self.destination.sector_type = int(self.enums.get('sectorTypes').SECT_WATER_NOSWIM)
        self.actor.trust = int(self.enums.get('gameParameters').IMPLEMENTOR)
        self.flee()
        self.assertEqual(self.actor.room_id, self.destination.id)

    def test_npc_no_mob_destination_is_rejected(self):
        npc = self.npc()
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_NO_MOB)
        with patch('interp.commands.Fight.random.randint', return_value=0):
            self.assertIsNone(self.commands._flee_destination(npc, self.room, self.exit))

    def test_daze_can_reject_all_six_attempts(self):
        self.actor.status_flags.pulse_daze = 4
        with patch('interp.commands.Fight.random.randint', side_effect=[0, 1] * 6) as roll:
            result = self.commands.do_flee(self.actor, self.ctx('flee'))
        self.assertEqual(result['blocked_key'], 'no_destination')
        self.assertEqual(roll.call_count, 12)

    def test_rejected_travel_retries_a_different_exit(self):
        from area.Exit import Exit
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_NEWBIES_ONLY)
        self.room.exits.append(Exit(1, '', '', 0, -1, 3001, self.temple.id, self.room.id))
        with patch('interp.commands.Fight.random.randint', side_effect=[0, 0, 1, 0, 100]):
            self.commands.do_flee(self.actor, self.ctx('flee'))
        self.assertEqual(self.actor.room_id, self.temple.id)


class InputHideParityTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.handler = InterpHandler.__new__(InterpHandler)
        self.handler.registry_service = NS(interp_registry=NS())
        self.handler.interp_registry = NS(all_commands=lambda: [])
        self.handler.social_registry = NS(get_or_none=lambda **kw: None)
        self.handler.social_handler = NS(handle_social=AsyncMock())
        self.handler.message_bus = NS(send_to_character=AsyncMock(), text_to_message=lambda text: text)
        self.handler.command_not_found_message = 'Huh?'
        self.handler.logger = Mock()

    def hidden(self):
        return CharacterApi.is_affected_by_name(self.actor, self.enums.get('affectedBy'), 'AFF_HIDE')

    async def test_unknown_and_frozen_input_break_hide_but_keep_other_effects(self):
        self.flag(self.actor, 'AFF_SNEAK')
        self.flag(self.actor, 'AFF_INVISIBLE')
        for frozen in (False, True):
            self.flag(self.actor, 'AFF_HIDE')
            if frozen:
                self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_FREEZE)
            with patch.object(InterpUtil, 'extract_parameters', side_effect=lambda *args: (None, '')):
                await self.handler.handle_command(None, self.actor, 'unknown')
            self.assertFalse(self.hidden())
        for flag in ('AFF_SNEAK', 'AFF_INVISIBLE'):
            self.assertTrue(CharacterApi.is_affected_by_name(self.actor, self.enums.get('affectedBy'), flag))

    async def test_empty_input_does_not_break_hide(self):
        for text in (None, '', '   '):
            self.flag(self.actor, 'AFF_HIDE')
            await self.handler.handle_command(None, self.actor, text)
            self.assertTrue(self.hidden())

    async def test_known_input_breaks_hide_before_dispatch_and_can_rehide(self):
        self.flag(self.actor, 'AFF_HIDE')
        async def dispatch(*args, **kw):
            self.assertFalse(self.hidden())
            self.flag(self.actor, 'AFF_HIDE')
        self.handler._call_lambda = dispatch
        with patch.object(InterpUtil, 'extract_parameters', return_value=(NS(name='hide'), '')):
            await self.handler.handle_command(None, self.actor, 'hide')
        self.assertTrue(self.hidden())

    async def test_social_input_breaks_hide(self):
        self.flag(self.actor, 'AFF_HIDE')
        self.handler.social_registry.get_or_none = lambda **kw: object()
        with patch.object(InterpUtil, 'extract_parameters', return_value=(None, '')):
            await self.handler.handle_command(None, self.actor, 'smile')
        self.assertFalse(self.hidden())
        self.handler.social_handler.handle_social.assert_awaited_once()

    async def test_nested_unknown_input_breaks_hide_and_empty_input_does_not(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.interp_registry = NS()
        handler.social_registry = self.handler.social_registry
        handler.message_bus = self.handler.message_bus
        context = Context(character=self.actor)
        self.flag(self.actor, 'AFF_HIDE')
        await handler._interpret_nested_command(self.actor, context, ' ')
        self.assertTrue(self.hidden())
        with patch.object(InterpUtil, 'extract_parameters', return_value=(None, '')):
            await handler._interpret_nested_command(self.actor, context, 'unknown')
        self.assertFalse(self.hidden())


if __name__ == '__main__':
    unittest.main()

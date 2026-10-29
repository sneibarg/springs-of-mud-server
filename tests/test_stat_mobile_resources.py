import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock

from tests.test_wiz_identity_targeting_parity import TargetingFixture
from mobile.MobileFactory import MobileFactory
from mobile.Mobile import Mobile
from mobile.Dice import Dice
from mobile.ArmorClass import ArmorClass
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from interp.CommandAccess import CommandAccess
from interp.CommandExecutor import CommandExecutor
from player.PlayerHandler import PlayerHandler


class StatMobileResourceFixture(TargetingFixture):
    def setUp(self):
        super().setUp()
        self.wiz.registry_service = self.registries
        self.prototype = Mobile(
            id='prototype', area_id='area', room_id='', name='guard', sex='1', level=10,
            gold=0, silver=0, vnum='100', short_description='a guard', long_description='A guard is here.',
            description='A guard.', race='human', flags='', alignment='0', group='', dam_type='slash',
            size='medium', material='flesh', hit_roll=3, status_flags=self.actor.status_flags,
            hit_dice=Dice(2, 6, 5), mana_dice=Dice(1, 6, 0), damage_dice=Dice(1, 4, 0),
            armor_class=ArmorClass(pierce=70, slash=60, bash=50, exotic=40))
        self.mobile = MobileFactory.create(self.prototype, self.enums)
        self.mobile.room_id = self.room.id
        self.mobile.area_id = self.room.area_id
        self.room.add_mobile_to_room(self.mobile)


class StatMobileResourceTests(StatMobileResourceFixture, unittest.TestCase):
    def test_new_mobile_has_current_and_maximum_movement(self):
        self.assertEqual((self.mobile.movement, self.mobile.max_movement), (100, 100))

    def test_stat_explicit_and_generic_mobile_targets_render_factory_created_resources(self):
        for argument in ('mob guard', 'guard'):
            with self.subTest(argument=argument):
                context = self.context('stat', argument)
                payload = self.wiz.do_stat(self.actor, context)
                self.assertTrue(context.done)
                self.assertIn('a guard', payload['to_char'])
                self.assertIn('Move: 100/100', payload['to_char'])
                self.assertIn(f'Hit: {self.mobile.hit}/{self.mobile.max_hit}', payload['to_char'])
                self.assertIn(f'Mana: {self.mobile.mana}/{self.mobile.max_mana}', payload['to_char'])

    def test_stat_reflects_current_movement_and_active_maximum_modifier(self):
        handler = EffectHandler(self.enums)
        handler.affect_to_char(self.mobile, Effect(location='APPLY_MOVE', modifier=25))
        self.mobile.movement = 40
        output = self.wiz.do_stat(self.actor, self.context('stat', 'mob guard'))['to_char']
        self.assertIn('Move: 40/125', output)
        handler.affect_remove(self.mobile, self.mobile.effects[0])
        self.assertEqual((self.mobile.movement, self.mobile.max_movement), (40, 100))

    def test_clones_preserve_live_movement_without_mutating_parent_or_new_spawns(self):
        self.mobile.movement, self.mobile.max_movement = 35, 125
        clone = MobileFactory.copy_instance(self.mobile, self.enums)
        fresh = MobileFactory.create(self.prototype, self.enums)
        self.assertEqual((clone.movement, clone.max_movement), (35, 125))
        self.assertEqual((fresh.movement, fresh.max_movement), (100, 100))
        clone.movement = 1
        self.assertEqual(self.mobile.movement, 35)


class StatMobileCommandExecutionTests(StatMobileResourceFixture, unittest.IsolatedAsyncioTestCase):
    async def test_executor_sends_mobile_stat_without_raising(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.wiz_commands = self.wiz
        handler.interp_api = self.api
        handler.message_bus = NS(text_to_message=lambda text: text, send_to_character=AsyncMock(),
                                 connection_manager=self.manager)
        context = self.context('stat', 'mob guard')
        context.handler_service = NS(get_handler=lambda name: self.wiz_handler if name == 'wh' else handler)
        await CommandExecutor.execute(context.command, context, authorization=CommandAccess.check,
                                      message_bus=handler.message_bus)
        handler.message_bus.send_to_character.assert_awaited_once()
        recipient, text = handler.message_bus.send_to_character.await_args.args
        self.assertEqual(recipient, self.actor.id)
        self.assertIn('Move: 100/100', text)


if __name__ == '__main__':
    unittest.main()

import unittest
from enum import IntEnum
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests.test_update_handler_active_players import Room
from api.MobileApi import MobileApi
from mobile.MobileContext import MobileContext
from mobile.MobileHandler import MobileHandler


class PlayerBits(IntEnum):
    PLR_KILLER = 1
    PLR_THIEF = 2


class MobileSpecialRoomAccessTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.room = Room(id='room')
        self.player = SimpleNamespace(id='player', level=10, gold=100, silver=200,
                                      fighting=None, status_flags=SimpleNamespace(act=PlayerBits.PLR_KILLER))
        self.observer = SimpleNamespace(id='observer', level=10, status_flags=SimpleNamespace(act=0))
        self.room.add_player_to_room(self.player)
        self.room.add_player_to_room(self.observer)
        self.actor = SimpleNamespace(id='guard', name='guard', short_description='a guard', vnum='100',
                                     level=10, gold=0, silver=0, fighting=None, special_name='spec_guard')
        self.handler = SimpleNamespace(rng=Mock(number_bits=Mock(return_value=0), number_range=Mock(return_value=10)),
                                       fight_handler=Mock(is_safe=Mock(return_value=(False, '')),
                                                          multi_hit=Mock(return_value={'to_room': 'Attack!', 'to_victim': 'Ouch!'})))
        self.ctx = MobileContext(self.actor, self.room, self.handler)
        self.visibility = patch('api.MobileApi.CharacterApi.can_see', return_value=True)
        self.can_see = self.visibility.start()
        self.addCleanup(self.visibility.stop)

    async def test_reported_guard_lambda_executes_with_real_room(self):
        self.actor.special_function = [
            "lambda ctx: ctx.select_room_criminal(alias='victim', crime_alias='crime', priorities=['PLR_KILLER', 'PLR_THIEF'], visible_only=True)",
            'lambda ctx: ctx.mark_performed()']
        handler = MobileHandler.__new__(MobileHandler)
        handler.logger = Mock()
        handler._flush_context_payloads = AsyncMock()
        with patch('api.MobileApi.CharacterApi.get_enum', return_value=PlayerBits):
            self.assertTrue(await handler.execute_special_function(self.actor, self.room))
        handler.logger.error.assert_not_called()
        self.can_see.assert_called_with(self.actor, self.player, self.room)

    async def test_criminal_selection_and_visibility(self):
        with patch('api.MobileApi.CharacterApi.get_enum', return_value=PlayerBits):
            self.assertIs(MobileApi.select_room_criminal(self.ctx, 'victim', 'crime', ['PLR_KILLER', 'PLR_THIEF']), self.player)
            self.assertEqual(self.ctx.get_alias('crime'), 'KILLER')
            self.can_see.return_value = False
            self.assertIsNone(MobileApi.select_room_criminal(self.ctx, 'victim', 'crime', ['PLR_KILLER']))
            self.assertIsNone(self.ctx.get_alias('victim'))

    async def test_visible_player_and_context_room_recipients(self):
        self.assertIs(MobileApi.select_visible_room_player(self.ctx, 'victim'), self.player)
        self.can_see.assert_called_with(self.actor, self.player, self.room)
        self.assertEqual(self.ctx.room_players(exclude_ids={'player'}), [self.observer])

    async def test_multi_hit_queues_observers_and_victim(self):
        self.ctx.set_alias('victim', self.player)
        with patch('api.MobileApi.CharacterApi.is_npc', return_value=False):
            self.assertTrue(MobileApi.multi_hit(self.ctx, 'victim'))
        self.assertEqual(self.ctx.payloads[0]['targets'], [self.observer])
        self.assertEqual(self.ctx.payloads[0]['to_victim'], 'Ouch!')

    async def test_thief_iterates_room_players(self):
        self.room.remove_player_from_room(self.observer)
        parameters = IntEnum('Parameters', {'LEVEL_IMMORTAL': 100})
        with patch('api.MobileApi.CharacterApi.get_enum', return_value=parameters):
            self.assertTrue(MobileApi.pickpocket_room_player(self.ctx, awake_discovery_check=False))
        self.assertEqual((self.player.gold, self.player.silver), (95, 190))
        self.assertEqual((self.actor.gold, self.actor.silver), (5, 10))
        self.can_see.assert_called_with(self.actor, self.player, self.room)

    async def test_nasty_attack_and_fight_intervention_use_room_members(self):
        with patch('api.MobileApi.CharacterApi.position_value', return_value=8), \
                patch('api.MobileApi.CharacterApi.pos_value', return_value=7), \
                patch.object(MobileApi, 'multi_hit', return_value=True):
            self.assertTrue(MobileApi.nasty_opening_attack(self.ctx, (-2, 2), []))
        self.assertIs(self.ctx.get_alias('victim'), self.player)
        self.player.fighting = self.actor
        self.assertIs(MobileApi.select_room_fight_intervention_target(self.ctx, 'victim'), self.player)

    async def test_combat_target_selectors_include_npcs(self):
        opponent = SimpleNamespace(id='npc', fighting=self.actor,
                                   character_attributes=SimpleNamespace(alignment=-500))
        self.room.add_mobile_to_room(opponent)
        self.assertIs(MobileApi.select_room_combat_victim(self.ctx, 'victim'), opponent)
        opponent.fighting = self.player
        self.assertIs(MobileApi.select_most_evil_fighter(self.ctx, 'victim'), opponent)


if __name__ == '__main__':
    unittest.main()

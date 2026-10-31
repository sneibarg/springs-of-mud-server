"""KICK and RESCUE through bundled guards and real skill/target resolution."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_movement_rules_parity import MovementFixture
from api.FightApi import FightApi
from combat.CombatHandler import FightHandler
from interp.commands.Fight import Fight


class KickRescueTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.actor.character_class.name = 'warrior'
        for name in ('kick', 'rescue'):
            self.actor.set_learned(name, 100, collection_name='skills', create=True)
        self.friend = self.follower('Bob')
        self.foe = self.npc()
        self.room.add_mobile_to_room(self.foe)
        self.handler = NS(is_safe=lambda *a, **kw: (False, ''),
                          check_killer=Mock(return_value={}),
                          damage=Mock(return_value={}), build_round_payload=lambda *a: {},
                          stop_fighting=Mock(side_effect=lambda entity, **kw: setattr(entity, 'fighting', None)),
                          set_fighting=Mock(side_effect=lambda entity, target, room: setattr(entity, 'fighting', target)))
        api = FightApi(self.rooms, self.skill_registry, self.skill_api, self.handler)
        self.commands = Fight(self.registries, self.enums, self.skill_api, api, self.api,
                              self.weather, self.effects, NS())
        self.commands._check_improve = Mock()

    def kick(self, actor=None, roll=1):
        actor = actor or self.actor
        with patch('interp.commands.Fight.random.randint',
                   side_effect=lambda low, high: roll if high == 100 else 9):
            context = self.ctx('kick', character=actor)
            result = self.commands.do_kick(actor, context)
        self.assertTrue(context.done)
        return result

    def fight_friend(self, foe=None):
        foe = foe or self.foe
        self.friend.fighting, foe.fighting = foe, self.friend

    def rescue(self):
        context = self.ctx('rescue', 'Bob')
        result = self.commands.do_rescue(self.actor, context)
        self.assertTrue(context.done)
        return result

    def test_kick_success_and_failure_are_bash_damage(self):
        self.actor.fighting = self.foe
        for roll in (1, 100):
            with self.subTest(roll=roll):
                self.kick(roll=roll)
                self.assertEqual('DAM_BASH', self.handler.damage.call_args.kwargs.get('dam_type'))

    def test_kick_requires_roll_strictly_below_proficiency(self):
        self.actor.fighting = self.foe
        for rating, roll, damage in ((100, 100, 0), (80, 80, 0), (80, 79, 9), (1, 1, 0)):
            with self.subTest(rating=rating, roll=roll):
                self.actor.set_learned('kick', rating, collection_name='skills', create=True)
                self.kick(roll=roll)
                self.assertEqual(damage, self.handler.damage.call_args.args[2])
                self.commands._check_improve.assert_called_with(self.actor, self.skills['kick'], damage > 0, 1)

    def test_npc_without_off_kick_stops_silently_before_wait_or_damage(self):
        self.foe.fighting = self.actor
        payload = self.kick(self.foe)
        self.assertTrue(payload.get('blocked'))
        self.assertFalse(payload.get('to_char'))
        self.assertEqual(0, self.foe.status_flags.pulse_wait)
        self.handler.damage.assert_not_called()
        self.commands._check_improve.assert_not_called()

    def test_off_kick_allows_npc_and_players_do_not_require_flag(self):
        self.foe.fighting = self.actor
        self.foe.status_flags.set_flag('off', self.enums.get('offenseTypes').OFF_KICK)
        self.kick(self.foe)
        self.assertEqual(1, self.handler.damage.call_count)
        self.actor.fighting = self.foe
        self.kick()
        self.assertEqual(2, self.handler.damage.call_count)

    def test_npc_without_off_kick_stays_silent_even_with_safety_fallback(self):
        self.foe.fighting = self.actor
        self.handler.is_safe = lambda *a, **kw: (True, 'Safety fallback')
        payload = self.kick(self.foe)
        self.assertTrue(payload.get('blocked'))
        self.assertFalse(payload.get('to_char'))
        self.handler.damage.assert_not_called()

    def test_rescue_rejects_ungrouped_npc_fight_before_any_side_effect(self):
        self.fight_friend()
        with patch('interp.commands.Fight.random.randint') as roll:
            result = self.rescue()
        self.assertIn('Kill stealing is not permitted.', result.get('to_char', ''))
        self.assertEqual(0, self.actor.status_flags.pulse_wait)
        self.assertIs(self.friend.fighting, self.foe)
        self.assertIs(self.foe.fighting, self.friend)
        self.handler.stop_fighting.assert_not_called()
        self.handler.set_fighting.assert_not_called()
        self.handler.check_killer.assert_not_called()
        self.commands._check_improve.assert_not_called()
        roll.assert_not_called()

    def test_grouped_rescue_still_transfers_combat(self):
        self.friend.leader = self.actor
        self.fight_friend()
        with patch('interp.commands.Fight.random.randint', return_value=1):
            result = self.rescue()
        self.assertFalse(result.get('blocked'))
        self.assertIsNone(self.friend.fighting)
        self.assertIs(self.actor.fighting, self.foe)
        self.assertIs(self.foe.fighting, self.actor)
        self.assertEqual(self.skills['rescue'].beats, self.actor.status_flags.pulse_wait)

    def test_ungrouped_rescue_from_player_opponent_still_allowed(self):
        opponent = self.follower('Carol')
        self.fight_friend(opponent)
        with patch('interp.commands.Fight.random.randint', return_value=1):
            result = self.rescue()
        self.assertFalse(result.get('blocked'))
        self.assertIs(self.actor.fighting, opponent)

    def test_nonfighting_target_keeps_earlier_guard_message(self):
        result = self.rescue()
        self.assertIn('not fighting right now', result.get('to_char', ''))
        self.assertEqual(0, self.actor.status_flags.pulse_wait)

    def real_attribution(self):
        combat = FightHandler.__new__(FightHandler)
        combat.AffectBits = self.enums.get('affectedBy')
        combat.PlayerActBits = self.enums.get('playerActBits')
        combat.character_service = NS(queue_save_character=Mock())
        self.handler.check_killer = Mock(wraps=combat.check_killer)
        return combat.character_service.queue_save_character

    def test_successful_rescue_attributes_killer_before_starting_new_fight(self):
        self.actor.guild = 'rom'
        opponent = self.follower('Carol')
        self.fight_friend(opponent)
        save = self.real_attribution()
        snapshots = []
        save.side_effect = lambda character: snapshots.append(
            (character.fighting, opponent.fighting, self.friend.fighting, character.status_flags.act))
        with patch('interp.commands.Fight.random.randint', return_value=1):
            result = self.rescue()
        killer = int(self.enums.get('playerActBits').PLR_KILLER)
        self.assertTrue(self.actor.status_flags.act & killer)
        self.assertEqual([(None, None, None, self.actor.status_flags.act)], snapshots)
        self.handler.check_killer.assert_called_once_with(self.actor, opponent)
        save.assert_called_once_with(self.actor)
        notice = result['payloads'][-1]
        self.assertIn('You are now a KILLER', notice['to_char'])
        self.assertIn('Carol', notice['to_wiznet'])
        self.assertIs(self.actor, notice['wiznet_actor'])
        self.assertEqual('WIZ_FLAGS', notice['wiznet_flag'])
        self.assertEqual('success', result['payloads'][0]['message_key'])
        self.assertIs(self.actor.fighting, opponent)
        self.assertIs(opponent.fighting, self.actor)

    def test_rescue_preserves_real_attribution_exemptions(self):
        for case in ('npc', 'killer', 'thief', 'immortal', 'unclanned'):
            with self.subTest(case=case):
                self.setUp()
                self.actor.guild = '' if case == 'unclanned' else 'rom'
                opponent = self.foe if case == 'npc' else self.follower('Carol')
                if case == 'npc':
                    self.friend.leader = self.actor
                if case in ('killer', 'thief'):
                    opponent.status_flags.set_flag('act', getattr(self.enums.get('playerActBits'), 'PLR_' + case.upper()))
                if case == 'immortal':
                    self.actor.level = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
                self.fight_friend(opponent)
                save = self.real_attribution()
                with patch('interp.commands.Fight.random.randint', return_value=1):
                    result = self.rescue()
                self.handler.check_killer.assert_called_once_with(self.actor, opponent)
                save.assert_not_called()
                self.assertFalse(self.actor.status_flags.act & int(self.enums.get('playerActBits').PLR_KILLER))
                self.assertEqual(1, len(result['payloads']))
                self.assertIs(self.actor.fighting, opponent)

    def test_failed_rescue_does_not_attribute_or_persist(self):
        self.actor.guild = 'rom'
        self.actor.set_learned('rescue', 50, collection_name='skills', create=True)
        opponent = self.follower('Carol')
        self.fight_friend(opponent)
        save = self.real_attribution()
        with patch('interp.commands.Fight.random.randint', return_value=100):
            result = self.rescue()
        self.assertEqual('failed', result['payloads'][0]['message_key'])
        self.handler.check_killer.assert_not_called()
        save.assert_not_called()
        self.assertIs(self.friend.fighting, opponent)


if __name__ == '__main__':
    unittest.main()

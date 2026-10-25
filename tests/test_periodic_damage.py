import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch
from tests import test_combat_state_effects as fixtures

Runtime = fixtures.Runtime


class PeriodicDamageTests(unittest.TestCase):
    def setUp(self):
        setup = fixtures.TestCombatStateEffects()
        setup.setUp()
        self.handler, self.victim, self.room = setup.handler, setup.victim, setup.room
        self.room.players_in_room = lambda: [self.victim]
        self.handler._check_immunity = Mock(return_value='IS_NORMAL')
        self.handler._reveal_attacker = Mock(return_value={})
        self.handler.dam_message = Mock()
        self.handler.message_bus = SimpleNamespace(send_to_character=AsyncMock(), send_to_room=AsyncMock(),
                                                   text_to_message=lambda text: text)
        self.victim.status_flags.drunk = 0
        self.victim.hit = 100
        self.handler.death_handler = None
        self.handler.escape_handler = None

    def apply(self, amount, kind='DAM_POISON'):
        asyncio.run(self.handler.apply_periodic_damage(self.victim, amount, dt='spell.poison', dam_type=kind))

    def test_typed_immunity_resistance_and_vulnerability(self):
        for immunity, expected in (('IS_IMMUNE', 100), ('IS_RESISTANT', 94), ('IS_VULNERABLE', 87)):
            for kind in ('DAM_POISON', 'DAM_DISEASE'):
                with self.subTest(immunity=immunity, kind=kind):
                    self.victim.hit = 100
                    self.handler._check_immunity.return_value = immunity
                    self.apply(9, kind)
                    self.assertEqual(expected, self.victim.hit)
                    self.handler._check_immunity.assert_called_with(self.victim, kind)
        self.handler.dam_message.assert_not_called()
        self.assertIsNone(self.victim.fighting)

    def test_drunk_sanctuary_and_protection_use_same_damage_reductions(self):
        self.victim.status_flags.drunk = 11
        self.victim.status_flags.affected_by = int(fixtures.Bits.AFF_SANCTUARY | fixtures.Bits.AFF_PROTECT_EVIL)
        with patch.object(Runtime.CharacterApi, 'is_evil', return_value=True, create=True):
            self.apply(20)
        self.assertEqual(93, self.victim.hit)  # 20 -> 18 -> 9 -> 7

    def test_immortal_floor_applies_to_poison_disease_and_bleeding(self):
        self.victim.level = 100
        for kind in ('DAM_POISON', 'DAM_DISEASE', 'DAM_NONE'):
            self.victim.hit = 1
            self.apply(5, kind)
            self.assertEqual(1, self.victim.hit)
        self.assertIsNone(self.victim.fighting)

    def test_lethal_damage_delivers_raw_kill_notices_once(self):
        self.victim.hit = -10
        self.handler.group_gain = Mock(return_value={'xp_gain': 0})
        self.handler.raw_kill = Mock(return_value=[{'to_char': 'death cry'}])
        self.apply(1, 'DAM_NONE')
        self.handler.raw_kill.assert_called_once_with(self.victim)
        self.handler.message_bus.send_to_character.assert_awaited_once_with(self.victim.id, 'death cry')
        self.handler.dam_message.assert_not_called()


if __name__ == '__main__':
    unittest.main()

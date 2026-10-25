import asyncio
import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_update_handler_active_players import Character, build_character_data
from player.CharacterAdvancement import CharacterAdvancement
from player.AdvancementHandler import AdvancementHandler
from skill.Ability import Ability


class AdvancementParityTests(unittest.TestCase):
    def setUp(self):
        self.character = Character.from_json(build_character_data())
        CharacterAdvancement.configure_level_observer()
        self.addCleanup(CharacterAdvancement.configure_level_observer)

    def test_xp_cost_is_recomputed_and_total_floor_preserves_penalty_debt(self):
        ch = self.character
        attrs = ch.character_attributes
        attrs.points, attrs.experience_per_level = 40, 9999
        attrs.accumulated_experience, attrs.experience = 5999, 999
        with patch.object(CharacterAdvancement, 'advance_level', return_value=NS(level=6)):
            gain = CharacterAdvancement.gain_experience(ch, 1)
        self.assertEqual((6, 1000, 6000, 0), (ch.level, attrs.experience_per_level,
                                             attrs.accumulated_experience, attrs.experience))
        self.assertEqual(1, len(gain.levels_gained))
        CharacterAdvancement.gain_experience(ch, -999999)
        self.assertEqual((1000, 0), (attrs.accumulated_experience, attrs.experience))
        CharacterAdvancement.gain_experience(ch, 5999)
        self.assertEqual(6, ch.level)
        self.assertEqual(999, attrs.experience)

    def test_each_level_is_saved_and_notice_is_drained_once(self):
        ch = self.character
        ch.character_attributes.accumulated_experience = 5999
        ch.character_attributes.points = 40
        saves = []
        service = NS(queue_save_character=lambda character: saves.append(character.level))
        recipient = NS(id='admin')
        wiz = Mock(wiznet_targets=Mock(return_value=[recipient]))
        wiz.decorate_wiznet_text.side_effect = lambda recipient, text: '--> ' + text
        bus = Mock(send_to_character=AsyncMock(), text_to_message=lambda text: text)
        handler = AdvancementHandler(service, wiz, bus)
        CharacterAdvancement.configure_level_observer(handler.level_gained)
        with patch.object(CharacterAdvancement, 'advance_level', side_effect=lambda character, hide: NS(level=character.level)):
            CharacterAdvancement.gain_experience(ch, 1001)
        self.assertEqual([6, 7], saves)
        async def flush():
            await handler.flush()
            await handler.flush()
        asyncio.run(flush())
        self.assertEqual(2, bus.send_to_character.await_count)
        self.assertEqual(['--> Tester has attained level 6!', '--> Tester has attained level 7!'],
                         [call.args[1] for call in bus.send_to_character.await_args_list])
        wiz.wiznet_targets.assert_called_with(ch, flag_name='WIZ_LEVELS')

    def test_regeneration_proficiency_respects_eligibility_daze_and_drunk(self):
        ch = self.character
        for skill in ('fast healing', 'meditation'):
            ch.skills = [{'name': skill, 'level': 99}]
            with patch.object(Ability, 'practice_visible', return_value=False):
                self.assertEqual(0, ch._skill_percent(skill))
            with patch.object(Ability, 'practice_visible', return_value=True):
                for daze, drunk, expected in ((0, 10, 99), (1, 10, 66), (0, 11, 89), (1, 11, 59)):
                    ch.status_flags.pulse_daze, ch.status_flags.drunk = daze, drunk
                    self.assertEqual(expected, ch._skill_percent(skill))


if __name__ == '__main__':
    unittest.main()

import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, patch

from tests import test_runtime_factories as runtime
from api.ItemApi import ItemApi
from area.Room import Room
from interp.Context import Context
from item.ItemHandler import ItemHandler
from item.ExtraDescriptionData import ExtraDescriptionData
from player.PlayerHandler import PlayerHandler
from util.InfoUtil import InfoUtil
from util.LookupUtil import LookupUtil


class InfoBoundaryTests(unittest.TestCase):
    def test_keyword_prefix_matching_and_multiword_selection_keep_separate_contracts(self):
        self.assertTrue(LookupUtil.keyword_matches(' SWO ', 'steel sword'))
        self.assertFalse(LookupUtil.keyword_matches('word', 'steel sword'))
        self.assertFalse(LookupUtil.keyword_matches('', 'steel sword'))
        self.assertFalse(LookupUtil.keyword_matches('steel sword', 'sword steel'))
        self.assertTrue(LookupUtil.matches('steel swo', 'sword steel'))

    def test_context_owns_the_requested_match_count(self):
        context = Context(character=None, number=2)
        self.assertFalse(context.register_match())
        self.assertTrue(context.register_match())
        self.assertFalse(context.register_match())
        self.assertEqual(3, context.count)

    def complete(self, operation):
        self.addCleanup(operation.close)
        with self.assertRaises(StopIteration):
            operation.send(None)

    def test_look_counts_item_extras_before_item_names(self):
        item = NS(name='sword steel', extra_description=ExtraDescriptionData(True, 'sword', 'An inscription.'),
                  long_description='A steel sword.', short_description='a sword')
        actor = NS(id='actor', get_items=lambda: [item])
        room = Room()
        handler = ItemHandler.__new__(ItemHandler)
        handler.message_bus = NS(text_to_message=lambda text: text, send_to_character=AsyncMock())
        for argument, expected, count in [('swo', 'An inscription.', 1), ('2.swo', 'A steel sword.', 2)]:
            with self.subTest(argument=argument), patch.object(ItemApi, 'can_see_object', return_value=True):
                context = Context(character=actor, room=room, parameters=[argument])
                self.complete(handler.look_item_or_extra(actor, context))
                handler.message_bus.send_to_character.assert_awaited_with(actor.id, expected + '\r\n')
                self.assertEqual(count, context.count)
                self.assertTrue(context.done)
                self.assertTrue(PlayerHandler._look_item_or_extra_exists(actor, room, argument))

    def test_room_extra_look_uses_the_same_matching_and_counter(self):
        room = Room(extra_description=NS(keyword='mural painting', description='A painted wall.'))
        actor = NS(id='actor', get_items=lambda: [])
        handler = ItemHandler.__new__(ItemHandler)
        handler.message_bus = NS(text_to_message=lambda text: text, send_to_character=AsyncMock())
        context = Context(character=actor, room=room, parameters=['mur'])
        self.complete(handler.look_item_or_extra(actor, context))
        handler.message_bus.send_to_character.assert_awaited_once_with(actor.id, 'A painted wall.\r\n')
        self.assertEqual(1, context.count)
        self.assertTrue(PlayerHandler._look_item_or_extra_exists(actor, room, 'mur'))

    def test_retained_presentation_helpers_preserve_output(self):
        target = NS(name='Guard', short_description='a guard', hit=15, max_hit=100)
        self.assertEqual('a guard looks pretty hurt.', InfoUtil.target_condition_line(target))
        target.max_hit = 0
        self.assertEqual('a guard is bleeding to death.', InfoUtil.target_condition_line(target))
        self.assertEqual('divinely armored against magic', InfoUtil.score_ac_phrase(-101, 'magic'))
        self.assertEqual('saintly', InfoUtil.score_alignment_word(900))


if __name__ == '__main__':
    unittest.main()

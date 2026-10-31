"""WHERE listing and named-search regressions against act_info.c."""
import unittest
from types import SimpleNamespace as NS

from tests.test_movement_rules_parity import MovementFixture
from interp.commands.Info import Info


class WhereParityTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.actor.name = 'Alice'
        self.room.name = 'Town square'
        self.destination.name = 'Market'
        self.destination.area_id = self.room.area_id
        self.info = Info.__new__(Info)
        self.info.room_registry = self.rooms
        self.sessions = [NS(character=self.actor)]
        self.info.session_handler = NS(get_playing_sessions=lambda: self.sessions)

    def where(self, argument=''):
        context = self.ctx('where', argument)
        result = self.info.do_where(self.actor, context)
        self.assertTrue(context.done)
        return result

    def player(self, name='Bob', room=None):
        player = self.character(name)
        player.room_id = (room or self.destination).id
        (room or self.destination).add_player_to_room(player)
        self.sessions.append(NS(character=player))
        return player

    def test_caller_alone_is_listed_once(self):
        text = self.where()
        self.assertIn('Alice', text)
        self.assertIn('Town square', text)
        self.assertEqual(1, text.count('Alice'))
        self.assertNotIn('None', text)

    def test_lists_visible_same_area_players_including_caller(self):
        self.player()
        text = self.where()
        self.assertIn('Alice', text)
        self.assertIn('Bob', text)
        self.assertIn('Market', text)

    def test_named_player_and_missing_player(self):
        self.player()
        self.assertIn('Market', self.where('Bob'))
        self.assertEqual("You didn't find any missing.\r\n", self.where('missing'))

    def test_named_npc_uses_visibility_and_list_mode_excludes_npcs(self):
        mob = self.npc()
        mob.name, mob.short_description = 'guard sentinel', 'a guard'
        self.room.add_mobile_to_room(mob)
        self.assertIn('a guard', self.where('guard'))
        self.sessions.append(NS(character=mob))
        self.assertNotIn('a guard', self.where())
        self.flag(mob, 'AFF_INVISIBLE')
        self.assertIn("didn't find", self.where('guard'))

    def test_player_visibility_uses_observers_room_not_targets_room(self):
        self.player()
        dark = int(self.enums.get('roomFlags').ROOM_DARK)
        self.destination.room_flags = dark
        self.assertIn('Market', self.where('Bob'))
        self.destination.room_flags = 0
        self.room.room_flags = dark
        self.assertNotIn('Bob', self.where())
        self.assertIn("didn't find", self.where('Bob'))

    def test_invisible_player_requires_detection(self):
        player = self.player()
        self.flag(player, 'AFF_INVISIBLE')
        self.assertNotIn('Bob', self.where())
        self.assertIn("didn't find", self.where('Bob'))
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        self.assertIn('Bob', self.where())
        self.assertIn('Bob', self.where('Bob'))

    def test_other_areas_and_nowhere_remain_filtered_from_list(self):
        self.player('Elsewhere', self.temple)
        self.player()
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_NOWHERE)
        text = self.where()
        self.assertNotIn('Elsewhere', text)
        self.assertNotIn('Bob', text)
        self.assertIn("didn't find", self.where('Elsewhere'))
        self.assertIn('Bob', self.where('Bob'))

    def test_owned_room_listing_requires_owner_but_named_search_does_not(self):
        self.player()
        self.destination.owner = 'Carol'
        self.assertNotIn('Bob', self.where())
        self.assertIn('Bob', self.where('Bob'))
        self.destination.owner = 'Carol Alice'
        self.assertIn('Bob', self.where())

    def test_private_room_listing_uses_occupancy_and_solitary_flags(self):
        self.player()
        flags = self.enums.get('roomFlags')
        self.destination.room_flags = int(flags.ROOM_SOLITARY)
        self.assertNotIn('Bob', self.where())
        self.destination.room_flags = int(flags.ROOM_PRIVATE)
        self.assertIn('Bob', self.where())
        self.player('Carol')
        self.assertNotIn('Bob', self.where())
        self.destination.room_flags = int(flags.ROOM_SOLITARY)
        self.assertNotIn('Bob', self.where())
        self.destination.room_flags = int(flags.ROOM_IMP_ONLY)
        self.assertNotIn('Bob', self.where())
        self.destination.room_flags = 0
        self.assertIn('Bob', self.where())

    def test_named_players_remain_concealed_even_with_detection_or_holy_light(self):
        for bit in ('AFF_HIDE', 'AFF_SNEAK'):
            with self.subTest(bit=bit):
                self.setUp()
                player = self.player()
                self.flag(player, bit)
                self.flag(self.actor, 'AFF_DETECT_HIDDEN')
                self.assertIn('Bob', self.where())
                self.assertIn("didn't find", self.where('Bob'))
                self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_HOLYLIGHT)
                self.assertIn("didn't find", self.where('Bob'))

    def test_named_npcs_remain_concealed_with_detection(self):
        for bit in ('AFF_HIDE', 'AFF_SNEAK'):
            with self.subTest(bit=bit):
                self.setUp()
                mob = self.npc()
                mob.name, mob.short_description = 'guard sentinel', 'a guard'
                self.room.add_mobile_to_room(mob)
                self.flag(mob, bit)
                self.flag(self.actor, 'AFF_DETECT_HIDDEN')
                self.assertIn("didn't find", self.where('sentinel'))
                self.assertIn("didn't find", self.where('guard'))

    def test_named_search_finds_linkdead_player_but_list_requires_session(self):
        player = self.player()
        self.sessions.pop()
        self.assertNotIn('Bob', self.where())
        self.assertIn('Market', self.where('Bob'))
        self.flag(player, 'AFF_INVISIBLE')
        self.assertIn("didn't find", self.where('Bob'))

    def test_named_npc_matches_secondary_keywords_and_displays_short_description(self):
        mob = self.npc()
        mob.name, mob.short_description = 'guard sentinel', 'a watchman'
        self.room.add_mobile_to_room(mob)
        self.assertIn('a watchman', self.where('SENT'))
        self.assertIn('a watchman', self.where('guard'))
        self.assertIn("didn't find", self.where('watchman'))


if __name__ == '__main__':
    unittest.main()

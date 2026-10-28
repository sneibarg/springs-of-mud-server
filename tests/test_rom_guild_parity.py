import unittest
from copy import deepcopy

from tests.test_wiz_identity_targeting_parity import TargetingFixture
from tests.test_immortal_priority_parity import mobile_entity
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from game.GameData import GameData


class RomGuildParityTests(TargetingFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.victim = self.player('bob')

    def guild(self, text):
        return self.wiz.do_guild(self.actor, self.context('guild', text))

    def test_catalog_matches_rom_clan_table(self):
        clans = GameApi.clans_map()
        self.assertEqual([entry['name'] for entry in clans.values()], ['', 'loner', 'rom'])
        self.assertEqual([entry['independent'] for entry in clans.values()], [True, True, False])
        self.assertTrue(all(entry['hall'] == 3054 for entry in clans.values()))
        self.assertEqual(clans['1']['whoName'], '[ Loner ] ')

    def test_case_insensitive_prefix_assigns_canonical_name(self):
        for name in ('r', 'RO', 'rom', 'RoM'):
            with self.subTest(name=name):
                result = self.guild(f'bob {name}')
                self.assertEqual(self.victim.guild, 'rom')
                self.assertEqual(result['message_key'], 'add_clan_member')
                self.assertEqual(result['tokens']['g'], 'Rom')
        self.wiz.character_service.queue_save_character.assert_called_with(self.victim)

    def test_independent_clan_uses_catalog_flag_and_canonical_tokens(self):
        result = self.guild('bob lo')
        self.assertEqual(self.victim.guild, 'loner')
        self.assertTrue(CharacterApi.is_clan(self.victim))
        self.assertEqual(result['message_key'], 'add_independent')
        self.assertEqual(result['tokens']['s'], 'loner')
        self.assertEqual(self.command('guild').render_message('to_victim', 'add_independent', s='loner'),
                         'You are now a loner.')

    def test_none_prefixes_remove_membership(self):
        for name in ('n', 'no', 'non', 'none', 'NONE'):
            with self.subTest(name=name):
                self.victim.guild = 'rom'
                result = self.guild(f'bob {name}')
                self.assertEqual(self.victim.guild, '')
                self.assertFalse(CharacterApi.is_clan(self.victim))
                self.assertEqual(result['message_key'], 'removal')

    def test_unknown_names_do_not_change_or_save_membership(self):
        self.victim.guild = 'rom'
        for name in ('invented', 'independent', 'clanless', 'remove', '0', 'romjunk', 'nonejunk'):
            with self.subTest(name=name):
                result = self.guild(f'bob {name}')
                self.assertEqual(result['blocked_key'], 'no_such_clan')
                self.assertEqual(self.victim.guild, 'rom')
        self.wiz.character_service.queue_save_character.assert_not_called()

    def test_syntax_and_target_errors_precede_clan_validation(self):
        for text, expected in (('', 'syntax'), ('bob', 'syntax'), ('missing invented', 'target_missing')):
            self.assertEqual(self.guild(text)['blocked_key'], expected)

    def test_npc_target_assignment_and_removal_do_not_use_player_persistence(self):
        mob = mobile_entity('guard', self.actor.status_flags)
        mob.room_id = self.remote.id
        self.remote.add_mobile_to_room(mob)
        result = self.guild('guard r')
        self.assertIs(result['victim'], mob)
        self.assertEqual(mob.guild, 'rom')
        self.guild('guard n')
        self.assertEqual(mob.guild, '')
        self.wiz.character_service.queue_save_character.assert_not_called()

    def test_parser_honors_quoted_names_and_ignores_trailing_words_like_rom(self):
        self.victim.name = 'royal guard'
        self.guild("'royal guard' rom ignored")
        self.assertEqual(self.victim.guild, 'rom')

    def test_catalog_is_designer_extensible_and_missing_catalog_rejects_names(self):
        document = deepcopy(self.game_document)
        document['clans'] = {'1': {'name': 'hermits', 'independent': True},
                             '2': {'name': 'heroes', 'independent': False}}
        GameApi.configure(GameData.from_json(document), self.enums)
        self.assertEqual(self.guild('bob he')['tokens']['s'], 'hermits')
        self.assertEqual(self.victim.guild, 'hermits')
        self.assertEqual(self.guild('bob hero')['message_key'], 'add_clan_member')
        document.pop('clans')
        GameApi.configure(GameData.from_json(document), self.enums)
        self.assertEqual(self.guild('bob rom')['blocked_key'], 'no_such_clan')
        self.assertEqual(self.guild('bob none')['message_key'], 'removal')


if __name__ == '__main__':
    unittest.main()

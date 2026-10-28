import unittest
from types import SimpleNamespace as NS

from tests.test_wiz_identity_targeting_parity import TargetingFixture
from api.CharacterApi import CharacterApi
from interp.CommandAccess import CommandAccess
from server.handlers.ConnectionHandler import ConnectionHandler


class RomImmortalityThresholdTests(TargetingFixture, unittest.TestCase):
    def test_rom_rank_constants_keep_threshold_distinct_from_named_rank(self):
        parameters = self.enums.get('gameParameters')
        self.assertEqual(int(parameters.MAX_LEVEL), 60)
        self.assertEqual(int(parameters.LEVEL_HERO), 51)
        self.assertEqual(int(parameters.LEVEL_IMMORTAL), 52)
        self.assertEqual(int(parameters.LEVEL_IMMORTAL), int(parameters.AVATAR))
        self.assertEqual(int(parameters.IMMORTAL), 55)

    def test_immortality_and_im_command_access_begin_at_52(self):
        command = self.command('invis')
        self.actor.role = 'player'
        for level in (51, 52, 53, 54, 55):
            with self.subTest(level=level):
                self.actor.level, self.actor.trust = level, 0
                self.assertEqual(CharacterApi.is_immortal(self.actor), level >= 52)
                self.assertEqual(CommandAccess.check(self.actor, command) is None, level >= 52)

    def test_named_immortal_rank_still_requires_55(self):
        command = self.command('invis')
        command.level = 'IMMORTAL'
        self.actor.role = 'player'
        for level in (52, 53, 54, 55):
            with self.subTest(level=level):
                self.actor.level, self.actor.trust = level, 0
                self.assertEqual(CommandAccess.check(self.actor, command) is None, level >= 55)

    def test_trust_override_and_switched_body_use_rom_threshold(self):
        from tests.test_immortal_priority_parity import mobile_entity
        self.actor.level, self.actor.trust, self.actor.role = 51, 52, 'player'
        body = mobile_entity('body', self.actor.status_flags)
        body.context = {'controller_original': self.actor}
        self.assertTrue(CharacterApi.is_immortal(self.actor))
        self.assertTrue(CharacterApi.is_immortal(body))
        self.assertIsNone(CommandAccess.check(body, self.command('invis')))

    def test_wizlock_and_wiznet_use_threshold_without_lowering_ranked_options(self):
        handler = ConnectionHandler.__new__(ConnectionHandler)
        handler.runtime_control = None
        handler.wiz_handler = NS(wizlocked=True)
        handler.registry_service = self.registries
        self.room.remove_player_from_room(self.actor)
        account = NS(banned=False)
        for level in (51, 52, 53, 54):
            with self.subTest(level=level):
                self.actor.level, self.actor.trust, self.actor.role = level, 0, 'player'
                self.assertEqual(handler._login_error(self.actor, account) == '', level >= 52)
                options = self.wiz_handler.wiznet_option_names(self.actor)
                self.assertEqual('newbies' in options, level >= 52)
                self.assertNotIn('spam', options)


if __name__ == '__main__':
    unittest.main()

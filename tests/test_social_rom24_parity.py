"""Social restrictions, observer rendering and NPC reaction boundaries from interp.c."""
import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock

from tests.test_movement_rules_parity import MovementFixture
from tests.test_review_application_fixes import ROOT
from api.CharacterApi import CharacterApi
from devtools.collection_query import load_collections
from interp.Context import Context
from interp.InterpHandler import InterpHandler
from interp.Social import Social
from interp.SocialHandler import SocialHandler
from player.PlayerHandler import PlayerHandler


class SocialParityTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.socials = {}
        for document in load_collections(ROOT / 'resources/collections', ['socials'])['socials'].documents:
            if document['name'] not in ('smile', 'snore'):
                continue
            data = deepcopy(document)
            data['id'] = data.pop('_id')['$oid']
            data.pop('_class', None)
            social = Social.from_json(data)
            cls.socials[social.name] = social

    def setUp(self):
        super().setUp()
        self.actor.name, self.actor.sex = 'Alice', '2'
        self.viewer = self.follower('viewer')
        self.viewer.name = 'Bob'
        self.sessions = NS(get_session_by_character=Mock(return_value=None))
        self.bus = NS(text_to_message=lambda text: text, send_to_character=AsyncMock(),
                      send_to_room=AsyncMock(), session_handler=self.sessions)
        self.registry = NS(get_or_none=lambda **kw: self.socials.get(kw['name']))
        self.handler = SocialHandler(self.bus, self.registry, NS(), NS(get=lambda **kw: self.room))
        self.handler.rng = Mock(number_bits=Mock(return_value=15))

    async def social(self, text, actor=None):
        return await self.handler.handle_social(actor or self.actor, text)

    def texts(self, recipient):
        return [call.args[1] for call in self.bus.send_to_character.call_args_list if call.args[0] == recipient.id]

    def room_texts(self, recipient):
        return [call.args[0].for_recipient(recipient.id) for call in self.bus.send_to_room.call_args_list
                if recipient in call.args[1]]

    def reset_messages(self):
        self.bus.send_to_character.reset_mock()
        self.bus.send_to_room.reset_mock()
        self.handler.rng.number_bits.reset_mock()

    async def test_all_blocked_positions_and_noemote_priority(self):
        for position, notice in [('DEAD', 'Lie still'), ('MORTAL', 'hurt far too bad'),
                                 ('INCAP', 'hurt far too bad'), ('STUNNED', 'too stunned'),
                                 ('SLEEPING', 'In your dreams')]:
            with self.subTest(position=position):
                self.actor.set_position(int(getattr(self.enums.get('positions'), 'POS_' + position)))
                await self.social('smile')
                self.assertIn(notice, self.texts(self.actor)[-1])
                self.bus.send_to_room.assert_not_awaited()
                self.reset_messages()
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOEMOTE)
        await self.social('snore')
        self.assertEqual(['You are anti-social!\r\n'], self.texts(self.actor))

    async def test_sleeping_snore_is_broadcast_but_sleeping_recipients_do_not_receive_act(self):
        self.actor.set_position(int(self.enums.get('positions').POS_SLEEPING))
        await self.social('snore')
        self.assertEqual([], self.texts(self.actor))
        self.assertTrue(self.room_texts(self.viewer))
        self.reset_messages()
        self.viewer.set_position(int(self.enums.get('positions').POS_SLEEPING))
        self.actor.set_position(int(self.enums.get('positions').POS_STANDING))
        await self.social('smile')
        self.assertEqual([], self.room_texts(self.viewer))

    async def test_resting_sitting_and_fighting_can_socialize(self):
        for position in ('POS_RESTING', 'POS_SITTING', 'POS_FIGHTING'):
            self.actor.set_position(int(getattr(self.enums.get('positions'), position)))
            await self.social('smile')
            self.assertEqual('You smile happily.\r\n', self.texts(self.actor)[-1])

    async def test_bundled_pronouns_names_and_self_target_are_rendered(self):
        await self.social('smile Bob ignored')
        self.assertEqual(['You smile at him.\r\n'], self.texts(self.actor))
        self.assertEqual(['Alice smiles at you.\r\n'], self.texts(self.viewer))
        self.reset_messages()
        await self.social('smile self')
        self.assertEqual(['You smile at yourself.\r\n'], self.texts(self.actor))
        self.assertEqual(['Alice smiles at herself.\r\n'], self.room_texts(self.viewer))

    def test_all_pronoun_tokens_and_legacy_name_tokens(self):
        template = '$n $e $m $s / $N $E $M $S / %actor% %target%'
        self.viewer.sex = '1'
        self.assertEqual('Alice she her her / Bob he him his / Alice Bob',
                         self.handler._render(template, self.actor, self.viewer, observer=self.viewer, room=self.room))
        self.viewer.sex = '0'
        self.assertIn('/ Bob it it its /', self.handler._render(
            template, self.actor, self.viewer, observer=self.actor, room=self.room))

    async def test_visibility_varies_by_recipient_and_cloak_is_preserved(self):
        detecting = self.follower('detecting')
        self.flag(self.actor, 'AFF_INVISIBLE')
        self.flag(detecting, 'AFF_DETECT_INVIS')
        await self.social('smile')
        self.assertEqual(['Someone smiles happily.\r\n'], self.room_texts(self.viewer))
        self.assertEqual(['Alice smiles happily.\r\n'], self.room_texts(detecting))
        self.reset_messages()
        await self.social('smile Bob')
        self.assertEqual(['Someone smiles at you.\r\n'], self.texts(self.viewer))
        self.reset_messages()
        self.flag(self.actor, 'AFF_INVISIBLE', False)
        self.actor.cloaked = True
        await self.social('smile')
        self.assertEqual(['Someone smiles happily.\r\n'], self.room_texts(detecting))

    async def test_invisible_target_missing_and_empty_templates_send_no_blank_lines(self):
        self.flag(self.viewer, 'AFF_INVISIBLE')
        await self.social('smile Bob')
        self.assertEqual([self.socials['smile'].char_not_found + '\r\n'], self.texts(self.actor))
        self.bus.send_to_room.assert_not_awaited()
        self.reset_messages()
        blank = Social('blank', 'blank', '', '', '', '', '', '', '', '')
        await self.handler.handle_social(self.actor, 'blank', blank)
        self.bus.send_to_character.assert_not_awaited()
        self.bus.send_to_room.assert_not_awaited()

    def add_npc(self):
        npc = self.npc()
        npc.name, npc.short_description = 'guard', 'a guard'
        self.room.add_mobile_to_room(npc)
        return npc

    async def test_all_sixteen_npc_rolls_mirror_slap_or_remain_silent(self):
        self.add_npc()
        for roll in range(16):
            with self.subTest(roll=roll):
                self.reset_messages()
                self.handler.rng.number_bits.return_value = roll
                await self.social('smile guard')
                self.handler.rng.number_bits.assert_called_once_with(4)
                expected = ['You smile at him.\r\n']
                if roll <= 8:
                    expected.append('A guard smiles at you.\r\n')
                elif roll <= 12:
                    expected.append('A guard slaps you.\r\n')
                self.assertEqual(expected, self.texts(self.actor))
                room_expected = ['Alice beams a smile at a guard.\r\n']
                if roll <= 8:
                    room_expected.append('A guard beams a smile at Alice.\r\n')
                elif roll <= 12:
                    room_expected.append('A guard slaps Alice.\r\n')
                self.assertEqual(room_expected, self.room_texts(self.viewer))

    def test_sparse_social_messages_default_to_empty_without_changing_authored_fields(self):
        social = Social.from_json({'id': 'sparse', 'name': 'snore', 'othersNoArg': '$n snores.'})
        self.assertEqual('$n snores.', social.others_no_arg)
        self.assertEqual('', social.char_no_arg)
        self.assertEqual('', social.char_found)
        self.assertEqual('', social.others_auto)

    async def test_charmed_sleeping_and_controlled_npcs_do_not_roll(self):
        npc = self.add_npc()
        self.flag(npc, 'AFF_CHARM')
        await self.social('smile guard')
        self.handler.rng.number_bits.assert_not_called()
        self.flag(npc, 'AFF_CHARM', False)
        npc.set_position(int(self.enums.get('positions').POS_SLEEPING))
        await self.social('smile guard')
        self.handler.rng.number_bits.assert_not_called()
        npc.set_position(int(self.enums.get('positions').POS_STANDING))
        self.sessions.get_session_by_character.return_value = NS(character=npc)
        await self.social('smile guard')
        self.handler.rng.number_bits.assert_not_called()

    async def test_npc_actor_and_player_target_do_not_trigger_reactions(self):
        npc = self.add_npc()
        npc.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOEMOTE)
        await self.social('smile Alice', actor=npc)
        await self.social('smile Bob')
        await self.social('smile self')
        self.handler.rng.number_bits.assert_not_called()
        self.assertIn('A guard smiles at you.\r\n', self.texts(self.actor))

    async def test_typing_and_nested_interpretation_enforce_the_same_social_rules(self):
        interp = InterpHandler.__new__(InterpHandler)
        interp.interp_registry = NS(get_or_none=lambda **kw: None, all_commands=lambda: [])
        interp.registry_service = NS(interp_registry=interp.interp_registry)
        interp.social_registry, interp.social_handler = self.registry, self.handler
        interp.message_bus = self.bus
        nested = PlayerHandler.__new__(PlayerHandler)
        nested.interp_registry, nested.social_registry, nested.message_bus = interp.interp_registry, self.registry, self.bus
        services = NS(get_handler=lambda name: self.handler if name == 'sh' else None)
        context = Context(character=self.actor, handler_service=services, room=self.room)
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_NOEMOTE)
        await interp.handle_command(None, self.actor, 'smile')
        await nested._interpret_nested_command(self.actor, context, 'smile')
        self.assertEqual(['You are anti-social!\r\n'] * 2, self.texts(self.actor))


if __name__ == '__main__':
    unittest.main()

import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_wiz_identity_targeting_parity import TargetingFixture
from tests.test_immortal_priority_parity import mobile_entity
from api.CharacterApi import CharacterApi
from api.WizSetApi import WizSetApi
from item.ExtraDescriptionData import ExtraDescriptionData
from item.Item import Item
from item.ItemFactory import ItemFactory
from item.ItemHandler import ItemHandler
from player.Character import Character
from player.CharacterService import CharacterService
from player.PlayerHandler import PlayerHandler
from server.session.SessionState import SessionStatus
from util.WizUtil import WizUtil


class FinalFixture(TargetingFixture):
    def setUp(self):
        super().setUp()
        self.wiz.WiznetFlagsEnum = self.enums.get('wiznetFlags')
        self.wiz.registry_service = self.registries

    def connect(self, character, identifier=None, descriptor=42):
        session = self.sessions.create_session(identifier or character.id)
        session.character, session.status = character, SessionStatus.PLAYING
        connection = NS(session_id=session.session_id, close=AsyncMock(),
                        writer=NS(get_extra_info=lambda name: NS(fileno=lambda: descriptor)))
        self.manager.add_connection(connection)
        self.manager.bind_character(character.id, session.session_id)
        return session, connection

    def emitter(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.wiz_handler = self.wiz_handler
        handler.interp_api = self.api
        handler.room_registry = self.rooms
        handler.message_bus = NS(connection_manager=self.manager, text_to_message=lambda text: text,
                                 send_to_character=AsyncMock(), send_to_room=AsyncMock())
        handler._send_prompt = AsyncMock()
        return handler


class FinalCommandTests(FinalFixture, unittest.TestCase):
    def test_visibility_alias_ranges_and_reply_clearing(self):
        for name in ('invis', 'wizinvis', 'incognito'):
            field = 'incog_level' if name == 'incognito' else 'invis_level'
            for argument in ('-1', '1', '61', 'nonsense'):
                with self.subTest(name=name, argument=argument):
                    self.actor.context = {'reply_to': 'bob'}
                    setattr(self.actor.status_flags, field, 0)
                    output = self.wiz.execute(self.actor, self.context(name, argument))
                    self.assertTrue(output['blocked'])
                    self.assertEqual(getattr(self.actor.status_flags, field), 0)
                    self.assertEqual(self.actor.context['reply_to'], 'bob')
            self.actor.context = {'reply_to': 'bob'}
            self.wiz.execute(self.actor, self.context(name, '56'))
            self.assertEqual(getattr(self.actor.status_flags, field), 56)
            self.assertNotIn('reply_to', self.actor.context)
            self.actor.context['reply_to'] = 'bob'
            self.wiz.execute(self.actor, self.context(name, ''))
            self.assertEqual(getattr(self.actor.status_flags, field), 0)
            self.assertEqual(self.actor.context['reply_to'], 'bob')

    def test_advance_requests_save_of_updated_target(self):
        victim = self.player('bob')
        victim.level = 1
        self.registries.item_registry = NS()
        self.registries.skill_registry = NS()
        self.registries.spell_registry = NS()
        self.wiz.wiz_set_api = WizSetApi(self.registries, self.wiz_handler)
        with patch('api.WizSetApi.CharacterAdvancement.advance_level'):
            self.wiz.do_advance(self.actor, self.context('advance', 'bob 2'))
        self.assertEqual(victim.level, 2)
        self.assertEqual(victim.trust, 0)
        self.wiz.character_service.queue_save_character.assert_called_once_with(victim)

    def test_echo_scope_and_trust_provenance(self):
        lower = self.player('lower', room=self.room)
        peer = self.player('peer', room=self.room)
        peer.level = peer.trust = 60
        remote = self.player('remote')
        zoned = self.player('zone', room=self.remote)
        zoned.level = zoned.trust = 60
        from area.Room import Room
        same_area = Room(id='same-area', area_id=self.room.area_id, light=1)
        self.room_list.append(same_area)
        neighbor = self.player('neighbor', room=same_area)
        for character in (self.actor, lower, peer, remote, zoned, neighbor):
            self.connect(character)
        for command, label, expected in (
                ('echo', 'local', {self.actor.id, lower.id, peer.id}),
                ('zecho', 'zone', {self.actor.id, lower.id, peer.id, neighbor.id}),
                ('gecho', 'global', {self.actor.id, lower.id, peer.id, remote.id, zoned.id, neighbor.id})):
            messages = self.wiz.execute(self.actor, self.context(command, 'A decree.'))['target_messages']
            by_id = {entry['id']: entry['text'] for entry in messages}
            self.assertEqual(set(by_id), expected)
            self.assertEqual(by_id[self.actor.id].strip(), f'{label}> A decree.')
            self.assertEqual(by_id[peer.id].strip(), f'{label}> A decree.')
            self.assertEqual(by_id[lower.id].strip(), 'A decree.')

    def test_personal_echo_maximum_level_exception(self):
        peer = self.player('peer')
        peer.level = peer.trust = 60
        for actor_level, expected in ((59, 'personal> hello'), (60, 'hello')):
            self.actor.level = self.actor.trust = actor_level
            output = self.wiz.do_pecho(self.actor, self.context('pecho', 'peer hello'))
            self.assertEqual(output['to_char'].strip(), 'personal> hello')
            self.assertEqual(output['to_victim'].strip(), expected)

    def test_immtalk_masks_invisible_sender_for_lower_immortals(self):
        peer = self.player('peer')
        peer.level = peer.trust = 60
        junior = self.player('junior')
        junior.level = junior.trust = 55
        CharacterApi.set_act_flags(peer, self.enums.get('playerActBits').PLR_HOLYLIGHT)
        self.connect(peer)
        self.connect(junior)
        self.actor.status_flags.invis_level = 60
        output = self.wiz.do_immtalk(self.actor, self.context('immtalk', 'hello'))
        by_id = {entry['id']: entry['text'].strip() for entry in output['target_messages']}
        self.assertEqual(by_id[peer.id], 'actor: hello')
        self.assertEqual(by_id[junior.id], 'Someone: hello')

    def test_wiznet_canonical_name_abbreviations_and_control_priority(self):
        self.actor.context = {}
        newbies = int(self.enums.get('wiznetFlags').WIZ_NEWBIE)
        self.wiz.do_wiznet(self.actor, self.context('wiznet', 'newbies'))
        self.assertTrue(self.actor.context['WiznetFlagsEnum'] & newbies)
        status = self.wiz.do_wiznet(self.actor, self.context('wiznet', 's'))
        self.assertIn('newbies', status['to_char'])
        self.wiz.do_wiznet(self.actor, self.context('wiznet', 'new'))
        self.assertFalse(self.actor.context['WiznetFlagsEnum'] & newbies)
        shown = self.wiz.do_wiznet(self.actor, self.context('wiznet', 'sh'))
        self.assertIn('newbies', shown['to_char'])
        self.wiz.do_wiznet(self.actor, self.context('wiznet', 'o'))
        self.assertTrue(self.actor.context['WiznetFlagsEnum'] & int(self.enums.get('wiznetFlags').WIZ_ON))

    def test_wiznet_prefixes_preserve_table_order_and_trust_checks(self):
        self.actor.context = {}
        self.wiz.do_wiznet(self.actor, self.context('wiznet', 'l'))
        flags = self.actor.context['WiznetFlagsEnum']
        self.assertTrue(flags & int(self.enums.get('wiznetFlags').WIZ_LOGINS))
        self.assertFalse(flags & int(self.enums.get('wiznetFlags').WIZ_LINKS))
        self.actor.level = self.actor.trust = 55
        result = self.wiz.do_wiznet(self.actor, self.context('wiznet', 'sec'))
        self.assertEqual(result['message_key'], 'no_such_option')
        self.assertEqual(self.actor.context['WiznetFlagsEnum'], flags)

    def test_disconnect_missing_target_and_link_dead_target_keep_denials(self):
        self.player('offline')
        for argument, expected in (('9999', 'target_missing'), ('offline', 'null_descriptor')):
            result = self.wiz.do_disconnect(self.actor, self.context('disconnect', argument))
            self.assertEqual(result['blocked_key'], expected)

    def test_command_show_metadata_loads_from_content(self):
        from copy import deepcopy
        from interp.Command import Command
        document = deepcopy(self.documents['invis'])
        document.update(show=False, shortcuts='', usage='', function=[])
        self.assertFalse(Command.from_json(document).show)

    def test_wizhelp_filters_level_enabled_and_show_without_position_filter(self):
        visible = self.command('invis')
        hidden = self.command('invis'); hidden.name = 'hidden'; hidden.show = False
        disabled = self.command('invis'); disabled.name = 'disabled'; disabled.enabled = False
        higher = self.command('invis'); higher.name = 'higher'; higher.level = 'ML'
        self.wiz.interp_registry = NS(all_commands=lambda: [visible, hidden, disabled, higher])
        self.actor.level = self.actor.trust = 55
        self.actor.character_attributes.position = 0
        output = self.wiz.do_wizhelp(self.actor, self.context('wizhelp'))['to_char']
        self.assertIn('invis', output)
        for name in ('hidden', 'disabled', 'higher'):
            self.assertNotIn(name, output)

    def test_movement_transfers_lit_equipment_and_clears_furniture(self):
        light = self.item('torch')
        light.item_type, light.value2 = 'light', '-1'
        self.actor.equip_item(light, 'light')
        self.actor.on = object()
        self.room.light, self.remote.light = 2, 0
        WizUtil.move_entity(self.rooms, self.actor, self.remote)
        self.assertEqual((self.room.light, self.remote.light), (1, 1))
        self.assertIsNone(self.actor.on)
        WizUtil.move_entity(self.rooms, self.actor, self.room)
        self.assertEqual((self.room.light, self.remote.light), (2, 0))

    def test_unlit_equipment_does_not_transfer_light(self):
        light = self.item('torch'); light.item_type, light.value2 = 'light', '0'
        self.actor.equip_item(light, 'light')
        before = self.room.light, self.remote.light
        WizUtil.move_entity(self.rooms, self.actor, self.remote)
        self.assertEqual((self.room.light, self.remote.light), before)

    def test_at_restores_light_and_only_surviving_furniture(self):
        light, seat = self.item('torch'), self.item('seat')
        light.item_type, light.value2 = 'light', '3'
        self.actor.equip_item(light, 'light')
        self.room.add_item_to_room(seat)
        self.actor.on = seat
        self.room.light, self.remote.light = 2, 0
        payload = self.wiz.do_at(self.actor, self.context('at', '2 look'))
        self.assertIs(payload['at_on'], seat)
        self.assertIsNone(self.actor.on)
        handler = self.emitter()
        handler._restore_at_character(self.actor, self.room, payload['at_on'])
        self.assertIs(self.actor.on, seat)
        self.assertEqual((self.room.light, self.remote.light), (2, 0))
        WizUtil.move_entity(self.rooms, self.actor, self.remote)
        self.room.remove_item_from_room(seat)
        handler._restore_at_character(self.actor, self.room, seat)
        self.assertIsNone(self.actor.on)


class FinalAsyncTests(FinalFixture, unittest.IsolatedAsyncioTestCase):
    async def test_numeric_disconnect_closes_pre_auth_connection(self):
        session, connection = self.connect(NS(id='pending'), descriptor=42)
        session.character = None
        session.status = SessionStatus.CONNECTED
        context = self.context('disconnect', '42')
        payload = self.wiz.do_disconnect(self.actor, context)
        self.assertIs(payload['disconnect_connection'], connection)
        await self.emitter()._emit_standard_payload(self.actor, payload, context)
        connection.close.assert_awaited_once()

    async def test_name_disconnect_closes_switched_mobile_session(self):
        body = mobile_entity('body', self.actor.status_flags)
        body.room_id = self.remote.id
        self.remote.add_mobile_to_room(body)
        session, connection = self.connect(body)
        session.metadata['switched_original'] = self.actor
        context = self.context('disconnect', 'body')
        payload = self.wiz.do_disconnect(self.actor, context)
        await self.emitter()._emit_standard_payload(self.actor, payload, context)
        connection.close.assert_awaited_once()

    async def test_slay_emits_slay_then_returned_death_and_corpse_notices(self):
        victim = self.player('bob', room=self.room)
        self.player('witness', room=self.room)
        death = {'to_room': 'A death cry.\r\n', 'targets': [self.actor]}
        corpse = {'to_room': 'An object falls.\r\n', 'targets': [self.actor]}
        self.wiz.fight_handler = NS(raw_kill=Mock(return_value=[death, corpse]))
        context = self.context('slay', 'bob')
        payload = self.wiz.do_slay(self.actor, context)
        self.assertEqual(payload['payloads'][1:], [death, corpse])
        emitter = self.emitter()
        await emitter._handle_standard_command_payload(self.actor, context, payload)
        calls = emitter.message_bus.send_to_room.await_args_list
        self.assertIn('slay', calls[0].args[0].lower())
        self.assertEqual([call.args[0] for call in calls[1:]], ['A death cry.\r\n', 'An object falls.\r\n'])

    async def test_extra_descriptions_preserve_keywords_clone_and_save_round_trip(self):
        item = self.item('chest')
        item.extra_description = ExtraDescriptionData(True, 'hinge', 'An old hinge.')
        self.actor.add_item(item)
        for keyword, text in (('lid', 'A wooden lid.'), ('lock', 'An iron lock.')):
            self.wiz.do_string(self.actor, self.context('string', f'obj chest ed {keyword} {text}'))
        self.assertEqual([entry.keyword for entry in ExtraDescriptionData.entries(item.extra_description)], ['lock', 'lid', 'hinge'])
        clone = ItemFactory.copy_instance(item)
        clone.extra_description.next.description = 'Changed.'
        self.assertEqual(item.extra_description.next.description, 'A wooden lid.')
        snapshot = CharacterService._serialize_character(self.actor)
        restored = Character.from_json(snapshot)
        restored_item = next(value for value in restored.get_items() if value.id == item.id)
        self.assertEqual([entry.keyword for entry in ExtraDescriptionData.entries(restored_item.extra_description)], ['lock', 'lid', 'hinge'])
        handler = ItemHandler.__new__(ItemHandler)
        handler.room_registry = self.rooms
        handler.message_bus = NS(send_to_character=AsyncMock(), text_to_message=lambda text: text)
        for keyword, text in (('lid', 'A wooden lid.'), ('hinge', 'An old hinge.')):
            context = self.context('look', keyword); context.parameters = [keyword]
            self.assertTrue(PlayerHandler._look_item_or_extra_exists(self.actor, self.room, keyword))
            await handler.look_item_or_extra(self.actor, context)
            self.assertEqual(handler.message_bus.send_to_character.await_args.args[1].strip(), text)


if __name__ == '__main__':
    unittest.main()

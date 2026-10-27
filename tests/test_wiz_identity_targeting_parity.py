import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests import test_review_application_fixes as fixtures
from tests.test_immortal_priority_parity import mobile_entity
from tests import test_runtime_factories as item_fixtures
from api.AreaApi import AreaApi
from api.CharacterApi import CharacterApi
from api.WizApi import WizApi
from area.Room import Room
from game.WizHandler import WizHandler
from interp.CommandAccess import CommandAccess
from interp.commands.Wiz import Wiz
from player.CharacterRegistry import CharacterRegistry
from player.PlayerHandler import PlayerHandler
from server.connection.ConnectionManager import ConnectionManager
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus
from util.WizUtil import WizUtil


class TargetingFixture(fixtures.RuntimeFixture):
    def setUp(self):
        super().setUp()
        self.actor.level = self.actor.trust = 60
        self.actor.role = 'immortal'
        CharacterApi.set_act_flags(self.actor, self.enums.get('playerActBits').PLR_HOLYLIGHT)
        self.room.vnum, self.room.name, self.room.light = '1', 'Origin', 1
        self.remote = Room(id='remote', area_id='other', vnum='2', name='Destination', light=1)
        self.room_list = [self.room, self.remote]
        self.rooms = NS(all_rooms=lambda: self.room_list, get_or_none=self.room_lookup)
        self.registry = CharacterRegistry()
        self.registry.register(self.actor)
        self.sessions, self.manager = SessionHandler(), ConnectionManager()
        self.registries = NS(character_registry=self.registry, room_registry=self.rooms)
        self.wiz_handler = WizHandler(self.registries, self.sessions, self.manager)
        self.wiz = Wiz.__new__(Wiz)
        self.wiz.character_registry = self.registry
        self.wiz.room_registry = self.rooms
        self.wiz.interp_api = self.api
        self.wiz.wiz_handler = self.wiz_handler
        self.wiz.CommFlagsEnum = self.enums.get('commFlags')
        self.wiz.PlayerActBitsEnum = self.enums.get('playerActBits')
        self.wiz.character_service = NS(queue_save_character=Mock())

    def room_lookup(self, **kwargs):
        return next((room for room in self.room_list if all(str(getattr(room, name)) == str(value)
                                                          for name, value in kwargs.items())), None)

    def player(self, identifier, name=None, room=None, live=True):
        player = self.character(identifier)
        player.name = name or identifier
        player.room_id = (room or self.remote).id
        self.registry.register(player)
        if live:
            (room or self.remote).add_player_to_room(player)
        return player

    def context(self, name, text=''):
        context = super().context(name, text)
        ph = NS(character_registry=self.registry, room_registry=self.rooms)
        context.handler_service = NS(get_handler=lambda key: self.wiz_handler if key == 'wh' else ph)
        return context

    def lookup(self, selector, **kwargs):
        return WizUtil.find_world_entity(self.registry, self.rooms, selector, observer=self.actor, **kwargs)

    def item(self, identifier, name=None):
        item = item_fixtures.RuntimeFactoryTests().item(identifier)
        item.name = name or identifier
        return item


class WorldTargetingTests(TargetingFixture, unittest.TestCase):
    def test_loaded_mobile_receives_live_room_and_area_identity(self):
        mob = mobile_entity('loaded', self.actor.status_flags)
        mob.room_id, mob.area_id = '', 'prototype-area'
        self.wiz.mobile_registry = NS(get_or_none=lambda **kw: mob)
        with patch('interp.commands.Wiz.MobileFactory.create', return_value=mob):
            self.wiz.do_load(self.actor, self.context('load', 'mob 1'))
        self.assertEqual((mob.room_id, mob.area_id), (self.room.id, self.room.area_id))
        self.assertIs(self.lookup('loaded'), mob)

    def test_cached_offline_retired_and_stale_membership_are_not_world_targets(self):
        self.player('offline', live=False)
        retired = self.player('retired')
        retired.world_retired = True
        stale = self.player('stale')
        stale.room_id = 'missing'
        for name in ('offline', 'retired', 'stale'):
            self.assertIsNone(self.lookup(name))
        self.assertIsNone(WizUtil.find_world_entity(self.registry, None, 'offline'))

    def test_local_priority_visible_ordinals_and_world_fallback(self):
        first = self.player('first', 'royal elite guard', self.room)
        second = self.player('second', 'royal elite guard', self.room)
        remote = self.player('third', 'royal elite guard')
        self.assertIs(self.lookup('roy el'), first)
        self.assertIs(self.lookup('2.guard'), second)
        self.assertIs(self.lookup('3.guard'), remote)
        first.status_flags.invis_level = 61
        self.assertIs(self.lookup('guard'), second)
        self.assertIs(self.lookup('2.guard'), remote)
        self.assertIsNone(self.lookup('0.guard'))

    def test_self_and_role_filters_use_the_actual_observer(self):
        mob = mobile_entity('guard', self.actor.status_flags)
        mob.room_id = self.room.id
        self.room.add_mobile_to_room(mob)
        self.assertIs(self.lookup('guard'), mob)
        self.assertIsNone(self.lookup('guard', include_mobiles=False))
        self.assertIs(self.lookup('self'), self.actor)
        self.assertIsNone(self.lookup('self', include_players=False))

    def test_guards_and_handler_apply_to_same_visible_ordinal(self):
        first = self.player('one', 'guard', self.room)
        second = self.player('two', 'guard', self.room)
        result = self.wiz.do_freeze(self.actor, self.context('freeze', '2.guard'))
        bit = self.enums.get('playerActBits').PLR_FREEZE
        self.assertIs(result['victim'], second)
        self.assertFalse(CharacterApi.is_set(first.status_flags.act, bit))
        self.assertTrue(CharacterApi.is_set(second.status_flags.act, bit))

    def test_hidden_and_offline_targets_are_rejected_before_side_effects(self):
        session = self.sessions.create_session('actor')
        session.character = self.actor
        hidden = self.player('hidden')
        hidden.status_flags.invis_level = 61
        offline = self.player('offline', live=False)
        for command in ('freeze', 'restore', 'deny', 'switch', 'snoop'):
            for name in ('hidden', 'offline'):
                with self.subTest(command=command, target=name):
                    result = self.wiz.execute(self.actor, self.context(command, name))
                    self.assertIn("aren't", result['to_char'])
        self.wiz.character_service.queue_save_character.assert_not_called()
        self.assertFalse(hidden.world_retired)
        self.assertFalse(offline.world_retired)

    def test_force_groups_use_live_pcs_but_preserve_rom_bulk_visibility_rule(self):
        mortal = self.player('mortal')
        hidden_hero = self.player('hero')
        hidden_hero.level = 51
        hidden_hero.status_flags.invis_level = 61
        self.player('offline', live=False)
        mob = mobile_entity('mob', self.actor.status_flags)
        mob.room_id = self.remote.id
        self.remote.add_mobile_to_room(mob)
        for group, expected in (('all', {mortal.id, hidden_hero.id}), ('players', {mortal.id}), ('gods', {hidden_hero.id})):
            view = self.api.build_interp_view(self.context('force', group + ' smile'))
            self.assertEqual({v.id for v in WizApi.force_targets(view)}, expected)

    def test_floor_inventory_worn_then_world_item_search(self):
        floor = self.item('floor', 'gem jewel')
        inventory = self.item('inventory', 'gem jewel')
        worn = self.item('worn', 'gem jewel')
        remote = self.item('remote', 'gem jewel')
        self.room.add_item_to_room(floor)
        self.actor.add_item(inventory)
        self.actor.equip_item(worn, 'head')
        self.remote.add_item_to_room(remote)
        find = lambda token: WizUtil.find_world_item(self.registry, self.rooms, token, observer=self.actor)
        self.assertIs(find('gem'), floor)
        self.room.remove_item_from_room(floor)
        self.assertIs(find('gem'), inventory)
        self.actor.loot.remove(inventory)
        self.assertIs(find('gem'), worn)
        self.actor.unequip_item('head')
        self.actor.loot.clear()
        self.assertIs(find('gem'), remote)

    def test_nested_and_carried_items_are_live_but_offline_inventory_is_not(self):
        carrier = self.player('carrier')
        bag = self.item('bag')
        gem = self.item('gem')
        bag.contains = [gem]
        carrier.add_item(bag)
        offline = self.player('offline', live=False)
        offline.add_item(self.item('lost'))
        self.assertIs(WizUtil.find_world_item(self.registry, self.rooms, 'gem', observer=self.actor), gem)
        self.assertIsNone(WizUtil.find_world_item(self.registry, self.rooms, 'lost', observer=self.actor))

    def test_invisible_items_are_excluded_before_ordinal_counting(self):
        CharacterApi.unset_act_flags(self.actor, self.enums.get('playerActBits').PLR_HOLYLIGHT)
        hidden = self.item('hidden', 'gem')
        hidden.extra_flags = int(self.enums.get('itemFlags').ITEM_INVIS)
        visible = self.item('visible', 'gem')
        self.remote.add_item_to_room(hidden)
        self.remote.add_item_to_room(visible)
        self.assertIs(WizUtil.find_world_item(self.registry, self.rooms, 'gem', observer=self.actor), visible)
        self.assertIsNone(WizUtil.find_world_item(self.registry, self.rooms, '2.gem', observer=self.actor))

    def test_location_adapters_use_visible_live_targets_and_floor_objects(self):
        hidden = self.player('hidden')
        hidden.status_flags.invis_level = 61
        self.player('offline', live=False)
        floor = self.item('obelisk')
        self.remote.add_item_to_room(floor)
        for name, expected in (('hidden', None), ('offline', None), ('obelisk', self.remote), ('2', self.remote)):
            view = self.api.build_interp_view(self.context('goto', name))
            self.assertIs(WizApi.location(view), expected)
        self.remote.remove_item_from_room(floor)
        self.actor.add_item(floor)
        self.assertIsNone(WizApi.location(self.api.build_interp_view(self.context('goto', 'obelisk'))))


class SwitchedIdentityTests(TargetingFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.body = mobile_entity('body', self.actor.status_flags)
        self.body.room_id = self.room.id
        self.room.add_mobile_to_room(self.body)
        self.registry.register(self.body)
        session = self.sessions.create_session('controller')
        session.character = self.actor
        session.status = SessionStatus.PLAYING
        self.manager.add_connection(NS(session_id=session.session_id))
        self.manager.bind_character(self.actor.id, session.session_id)
        self.session = session

    def handler(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.interp_api = self.api
        handler.wiz_handler = self.wiz_handler
        handler.message_bus = NS(connection_manager=self.manager, send_to_character=AsyncMock(), send_to_room=AsyncMock(),
                                 text_to_message=lambda text: text)
        handler._send_prompt = AsyncMock()
        return handler

    async def test_switch_acknowledgment_and_diagnostics_reach_controlled_body(self):
        handler = self.handler()
        context = self.context('switch', 'body')
        payload = self.wiz.do_switch(self.actor, context)
        self.assertIs(context.character, self.body)
        await handler._emit_standard_payload(self.body, payload, context)
        self.assertEqual(handler.message_bus.send_to_character.await_args_list[0].args, (self.body.id, 'Ok.\r\n'))
        await handler._emit_standard_payload(self.body, {'to_char': 'diagnostic\r\n'}, context)
        handler.message_bus.send_to_character.assert_awaited_with(self.body.id, 'diagnostic\r\n')

    async def test_controller_trust_is_shared_by_access_guards_visibility_and_clone_checks(self):
        self.wiz_handler.switch_character(self.actor, self.body)
        self.assertEqual(CharacterApi.get_trust(self.body), 60)
        self.assertIsNone(CommandAccess.check(self.body, self.command('force')))
        context = self.context('force', 'all smile')
        context.character = self.body
        self.assertFalse(WizApi.force_insufficient_level(self.api.build_interp_view(context)))
        self.assertTrue(WizUtil.can_clone_object(self.body, NS(level=60, cost=99999)))
        target = self.player('invisible')
        target.status_flags.invis_level = 59
        self.assertIs(WizUtil.find_world_entity(self.registry, self.rooms, 'invisible', observer=self.body), target)
        self.wiz_handler.return_character(self.body)
        self.assertEqual(CharacterApi.get_trust(self.body), self.body.level)
        self.assertIs(self.session.character, self.actor)
        self.assertIsNone(self.manager.get_connection_by_character(self.body.id))

    async def test_uncontrolled_npc_does_not_receive_player_output(self):
        handler = self.handler()
        await handler._emit_standard_payload(self.body, {'to_char': 'unbound'}, self.context('stat'))
        handler.message_bus.send_to_character.assert_not_awaited()

    async def test_victim_reply_prompts_reach_switched_body(self):
        self.wiz_handler.switch_character(self.actor, self.body)
        handler = self.handler()
        await handler._emit_standard_payload(self.actor, {'to_victim': 'reply', 'victim': self.body}, self.context('pecho'))
        handler.message_bus.send_to_character.assert_awaited_once_with(self.body.id, 'reply')
        handler._send_prompt.assert_awaited_once()

    async def test_cyclic_controller_identity_fails_closed(self):
        self.body.context = {'controller_original': self.actor}
        self.actor.context = {'controller_original': self.body}
        self.assertEqual(CharacterApi.get_trust(self.body), 0)

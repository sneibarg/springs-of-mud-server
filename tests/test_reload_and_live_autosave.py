import unittest
import importlib
from dataclasses import dataclass

from registries import Registry
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

import requests

from tests.test_update_handler_active_players import Character, build_character_data
from area.Area import Area
from area.AreaRegistry import AreaRegistry
from area.Room import Room
from area.RoomRegistry import RoomRegistry
from area.RoomService import RoomService
from game.UpdateHandler import UpdateHandler
from mobile.Mobile import Mobile
from skill.SkillRegistry import SkillRegistry
from skill.SkillService import SkillService
from skill.SpellRegistry import SpellRegistry
from skill.SpellService import SpellService


def ability(name='old', identity='old-id'):
    return dict(id=identity, name=name, kind='skill', handlerId='', target='ignore',
                minPosition='standing', nounDamage='', levelByClass={}, ratingByClass={},
                slot=0, minMana=0, beats=0)


class ReloadSnapshotTests(unittest.TestCase):
    def services(self):
        for cls, registry_cls, name in ((SkillService, SkillRegistry, 'skill'),
                                        (SpellService, SpellRegistry, 'spell'),
                                        (RoomService, RoomRegistry, 'room')):
            service = cls.__new__(cls)
            service.logger = Mock()
            registry = registry_cls()
            setattr(service, name + '_registry', registry)
            setattr(service, name + 's_endpoint', 'https://content.invalid/' + name)
            if name == 'room':
                service.area_registry = AreaRegistry()
                document = dict(id='old-id', vnum='1', name='Old room')
            else:
                document = ability()
            old = service._build_fetch_item(document)
            registry.register(old)
            yield service, registry, old, getattr(service, 'reload_' + name + 's'), document

    def response(self, data):
        return Mock(json=Mock(return_value=data))

    def test_request_failure_preserves_registry_and_reports_failure(self):
        for service, registry, old, reload, _ in self.services():
            with self.subTest(service=type(service).__name__), patch(
                    'server.FetchAndRegisterMixin.requests.get', side_effect=requests.ConnectionError('offline')):
                self.assertIs(False, reload())
                self.assertIs(old, registry.get(id=old.id))
                self.assertEqual(1, len(registry))
                service.logger.info.assert_not_called()

    def test_bad_shape_invalid_later_document_and_conflicts_do_not_publish_partial_results(self):
        for service, registry, old, reload, document in self.services():
            new = dict(document, id='new-id', name='new')
            if isinstance(service, RoomService):
                new['vnum'] = '2'
            for data in ({'error': 'not a list'}, [new, {'unknownField': 123}], [new, deepcopy(new)]):
                with self.subTest(service=type(service).__name__, data=data), patch(
                        'server.FetchAndRegisterMixin.requests.get', return_value=self.response(data)):
                    self.assertIs(False, reload())
                    self.assertEqual(1, len(registry))
                    self.assertIs(old, registry.get(id=old.id))
                    self.assertIsNone(registry.get_or_none(id='new-id'))

    def test_http_json_and_builder_failures_preserve_snapshot(self):
        for service, registry, old, reload, document in self.services():
            failed_http = self.response([])
            failed_http.raise_for_status.side_effect = requests.HTTPError('503')
            invalid_json = self.response([])
            invalid_json.json.side_effect = ValueError('invalid JSON')
            for response in (failed_http, invalid_json):
                with self.subTest(service=type(service).__name__), patch(
                        'server.FetchAndRegisterMixin.requests.get', return_value=response):
                    self.assertFalse(reload())
                    self.assertIs(old, registry.get(id=old.id))
            with patch('server.FetchAndRegisterMixin.requests.get', return_value=self.response([document])), \
                    patch.object(service, '_build_reload_item', return_value=None):
                self.assertFalse(reload())
                self.assertIs(old, registry.get(id=old.id))

    def test_success_replaces_whole_snapshot_and_preserves_injected_registry(self):
        for service, registry, old, reload, document in self.services():
            new = dict(document, id='new-id', name='new')
            with self.subTest(service=type(service).__name__), patch(
                    'server.FetchAndRegisterMixin.requests.get', return_value=self.response([new])):
                self.assertIs(True, reload())
                self.assertIsNone(registry.get_or_none(id=old.id))
                self.assertEqual('new', registry.get(id='new-id').name)
                self.assertEqual(1, len(registry))

    def test_valid_empty_snapshot_is_success(self):
        for service, registry, _, reload, _ in self.services():
            with self.subTest(service=type(service).__name__), patch(
                    'server.FetchAndRegisterMixin.requests.get', return_value=self.response([])):
                self.assertIs(True, reload())
                self.assertEqual(0, len(registry))

    def test_all_other_reload_entrypoints_preserve_existing_registry_on_failure(self):
        services = [('mobile.MobileService', 'MobileService', 'mobile', 'mobiles'),
                    ('item.ItemService', 'ItemService', 'item', 'items'),
                    ('area.ResetService', 'ResetService', 'reset', 'resets'),
                    ('area.ShopService', 'ShopService', 'shop', 'shops'),
                    ('area.SpecialService', 'SpecialService', 'special', 'specials'),
                    ('interp.HelpService', 'HelpService', 'help', 'helps'),
                    ('interp.SocialService', 'SocialService', 'social', 'socials'),
                    ('player.CharacterService', 'CharacterService', 'character', 'characters'),
                    ('player.PlayerService', 'PlayerService', 'player', 'players')]
        @dataclass(frozen=True)
        class Record:
            id: str
        class Records(Registry):
            lookup_attrs = ('id',)
        for module, cls_name, singular, plural in services:
            with self.subTest(service=cls_name):
                cls = getattr(importlib.import_module(module), cls_name)
                service = cls.__new__(cls)
                service.logger = Mock()
                registry = Records()
                old = Record('old')
                registry.register(old)
                setattr(service, singular + '_registry', registry)
                setattr(service, plural + '_endpoint', 'https://content.invalid')
                with patch('server.FetchAndRegisterMixin.requests.get', side_effect=requests.ConnectionError('offline')):
                    self.assertIs(False, getattr(service, 'reload_' + plural)())
                self.assertIs(old, registry.get(id='old'))
                service.logger.info.assert_not_called()

    def test_group_reload_does_not_publish_partial_or_mutate_source(self):
        from skill.GroupRegistry import GroupRegistry
        from skill.GroupType import GroupType
        service = SkillService.__new__(SkillService)
        service.logger = Mock()
        service.group_registry = GroupRegistry()
        old = GroupType.from_json(dict(name='old', rating=[], skills=[], spells=[]))
        service.group_registry.register(old)
        service.groups = {'new': dict(rating=[], skills=[], spells=[]), 'bad': {'invalid': True}}
        source = deepcopy(service.groups)
        self.assertFalse(service.reload_groups())
        self.assertIs(old, service.group_registry.get(name='old'))
        self.assertEqual(source, service.groups)
        del service.groups['bad']
        self.assertTrue(service.reload_groups())
        self.assertIsNone(service.group_registry.get_or_none(name='old'))
        self.assertEqual('new', service.group_registry.get(name='new').name)
        self.assertNotIn('name', service.groups['new'])

    def test_command_reload_stages_generated_summary_and_retains_old_on_failure(self):
        from interp.InterpService import InterpService
        from interp.InterpRegistry import InterpRegistry
        from interp.HelpRegistry import HelpRegistry
        from interp.Command import Command
        service = InterpService.__new__(InterpService)
        service.logger = Mock()
        service.commands_endpoint = 'https://content.invalid'
        service.interp_registry = InterpRegistry()
        service.help_registry = HelpRegistry()
        from interp.HelpEntry import HelpEntry
        service.help_registry.register(HelpEntry('summary-help', 'summary', 'Summary', 0))
        old = service._build_summary_command()
        service.interp_registry.register(old)
        with patch('server.FetchAndRegisterMixin.requests.get', side_effect=requests.ConnectionError('offline')):
            self.assertFalse(service.reload_commands())
        self.assertIs(old, service.interp_registry.get(name='summary'))
        with patch('server.FetchAndRegisterMixin.requests.get', return_value=self.response([])):
            self.assertTrue(service.reload_commands())
        self.assertIsInstance(service.interp_registry.get(name='summary'), Command)
        self.assertEqual(1, len(service.interp_registry))
        current = service.interp_registry.get(name='summary')
        service.help_registry.reset()
        with patch('server.FetchAndRegisterMixin.requests.get', return_value=self.response([])):
            self.assertFalse(service.reload_commands())
        self.assertIs(current, service.interp_registry.get(name='summary'))

    def test_area_reload_leaves_bound_rooms_and_counts_unchanged(self):
        from area.AreaService import AreaService
        service = AreaService.__new__(AreaService)
        service.logger = Mock()
        service.areas_endpoint = 'https://content.invalid'
        service.area_registry = AreaRegistry()
        area = Area(author='builder', name='Old area', id='old')
        room = Room(id='room')
        room.characters['player'] = Character.from_json(build_character_data())
        room.bind_area(area)
        area.rooms = [room]
        service.area_registry.register(area)
        service.registry_service = NS(room_registry=NS(all_rooms=lambda: [room]))
        new = dict(id='new', name='New area', author='builder', suggestedLevelRange='1 10')
        with patch('server.FetchAndRegisterMixin.requests.get', return_value=self.response([new])):
            self.assertFalse(service.reload_areas())
        self.assertIs(area, room.area)
        self.assertIs(area, service.area_registry.get(id='old'))
        self.assertEqual(1, area.number_of_players)

    def test_room_reload_rejects_live_world_and_preserves_all_runtime_state(self):
        service, registry, room, reload, document = list(self.services())[-1]
        area = Area(author='builder', name='Test area', id='area')
        player = Character.from_json(build_character_data())
        room.area_id = area.id
        service.area_registry.register(area)
        room.characters[player.id] = player
        room.mobiles['npc'] = object()
        room.contents['item'] = object()
        room.bind_area(area)
        area.rooms = [room]
        before = (room.characters, room.mobiles, room.contents, room.lock, room.area)
        with patch('server.FetchAndRegisterMixin.requests.get', return_value=self.response([document])):
            self.assertIs(False, reload())
        self.assertIs(room, registry.get(id=room.id))
        self.assertEqual(before, (room.characters, room.mobiles, room.contents, room.lock, room.area))
        self.assertIs(room, area.rooms[0])
        self.assertEqual(1, area.number_of_players)

    def test_room_reload_rejects_malformed_exit(self):
        _, registry, room, reload, document = list(self.services())[-1]
        for data in (dict(document, exits=[{'unknown': 'bad exit'}]), dict(document, exits={}), {}):
            with self.subTest(data=data), patch('server.FetchAndRegisterMixin.requests.get', return_value=self.response([data])):
                self.assertIs(False, reload())
            self.assertIs(room, registry.get(id=room.id))


class LiveAutosaveTests(unittest.IsolatedAsyncioTestCase):
    def handler(self, sessions, rooms):
        handler = UpdateHandler.__new__(UpdateHandler)
        handler.session_handler = NS(get_playing_sessions=lambda: sessions)
        handler.entity_update_handler = NS(room_registry=NS(all_rooms=lambda: rooms))
        handler.character_service = Mock()
        handler.save_cycle = 30
        handler.save_number = 0
        return handler

    async def test_disconnect_retains_save_bucket_eligibility_without_saving_offline_records(self):
        player = Character.from_json(build_character_data('link-dead'))
        room = Room(characters={player.id: player})
        sessions = [NS(character=player)]
        handler = self.handler(sessions, [room])
        handler.save_number = handler._autosave_bucket(player.id)
        sessions.clear()  # Disconnect removes the session, retaining the live room body.
        self.assertEqual([], handler._active_player_characters())
        await handler._autosave_due_characters()
        handler.character_service.queue_save_character.assert_called_once_with(player)
        handler.character_service.reset_mock()
        room.characters.clear()  # Fully leaving the world makes the record ineligible.
        await handler._autosave_due_characters()
        handler.character_service.queue_save_character.assert_not_called()

    async def test_periodic_character_update_queues_link_dead_player_after_tick(self):
        player = Character.from_json(build_character_data('link-dead'))
        room = Room(characters={player.id: player})
        handler = self.handler([], [room])
        handler.save_cycle = 1
        handler.entity_update_handler.enabled = True
        async def tick(active):
            self.assertEqual([], active)
            player.hit = 29
        handler.entity_update_handler.update = AsyncMock(side_effect=tick)
        handler.character_service.queue_save_character.side_effect = lambda character: self.assertEqual(29, character.hit)
        await handler.char_update()
        handler.character_service.queue_save_character.assert_called_once_with(player)

    async def test_possession_original_saved_once_by_id_and_body_never_saved(self):
        original = Character.from_json(build_character_data('original'))
        duplicate = Character.from_json(build_character_data('original'))
        body = Mobile.__new__(Mobile)
        body.context = {'controller_original': original}
        sessions = [NS(character=body, metadata={'switched_original': original}), NS(character=duplicate)]
        room = Room(characters={original.id: original}, mobiles={'body': body})
        handler = self.handler(sessions, [room, room])
        handler.save_number = handler._autosave_bucket(original.id)
        await handler._autosave_due_characters()
        handler.character_service.queue_save_character.assert_called_once_with(original)
        self.assertEqual([duplicate], handler._active_player_characters())

    async def test_possession_original_available_from_session_metadata_outside_room(self):
        original = Character.from_json(build_character_data('original'))
        body = Mobile.__new__(Mobile)
        body.context = {}
        handler = self.handler([NS(character=body, metadata={'switched_original': original})], [])
        handler.save_number = (handler._autosave_bucket(original.id) + 1) % handler.save_cycle
        await handler._autosave_due_characters()
        handler.character_service.queue_save_character.assert_not_called()
        handler.save_number = handler._autosave_bucket(original.id)
        await handler._autosave_due_characters()
        handler.character_service.queue_save_character.assert_called_once_with(original)


if __name__ == '__main__':
    unittest.main()

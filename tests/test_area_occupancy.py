import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests.test_update_handler_active_players import Room
from area.Area import Area
from area.AreaHandler import AreaHandler
from area.AreaService import AreaService
from area.RoomService import RoomService


class AreaOccupancyTests(unittest.TestCase):
    def setUp(self):
        self.area = Area(author='ROM', name='Test', id='area', age=20, empty=True)
        self.room = Room(id='one', area_id='area')
        self.room.bind_area(self.area)
        self.character = SimpleNamespace(id='player')

    def handler(self, school=None):
        handler = AreaHandler.__new__(AreaHandler)
        handler.area_registry = SimpleNamespace(all_areas=lambda: [self.area])
        handler.room_registry = SimpleNamespace(get_or_none=lambda **kw: school)
        handler.WellKnownRoomVnums = SimpleNamespace(ROOM_VNUM_SCHOOL=3700)
        handler._reset_area = Mock()
        handler.wiz_handler = Mock(wiznet_targets=Mock(return_value=[]))
        handler.message_bus = Mock(send_to_character=AsyncMock())
        return handler

    def test_entry_reactivates_empty_area_and_duplicate_entry_does_not_count_twice(self):
        self.room.add_player_to_room(self.character)
        self.assertEqual((self.area.number_of_players, self.area.empty, self.area.age), (1, False, 0))
        self.area.age = 8
        self.room.add_player_to_room(self.character)
        self.assertEqual((self.area.number_of_players, self.area.age), (1, 8))
        self.room.add_mobile_to_room(SimpleNamespace(id='npc'))
        self.assertEqual(self.area.number_of_players, 1)

    def test_reset_notice_follows_reset_before_age_changes_and_uses_wiznet(self):
        self.area.age = 2
        self.area.empty = False
        handler = self.handler()
        recipient = SimpleNamespace(id='admin')
        handler.wiz_handler.wiznet_targets.return_value = [recipient]
        handler.wiz_handler.decorate_wiznet_text.return_value = '--> Test has just been reset.'
        events = []
        handler._reset_area.side_effect = lambda area: events.append(('reset', area.age))
        handler.message_bus.send_to_character.side_effect = lambda *args: events.append(('notice', self.area.age))
        with patch('area.AreaHandler.rng.number_range', return_value=1) as roll:
            asyncio.run(handler.area_update())
        self.assertEqual([('reset', 3), ('notice', 3)], events)
        handler.wiz_handler.wiznet_targets.assert_called_once_with(None, flag_name='WIZ_RESETS')
        handler.wiz_handler.decorate_wiznet_text.assert_called_once_with(recipient, 'Test has just been reset.')
        handler.message_bus.send_to_character.assert_awaited_once_with(
            'admin', handler.message_bus.text_to_message('--> Test has just been reset.'))
        roll.assert_called_once_with(0, 3)
        self.assertEqual((1, True), (self.area.age, self.area.empty))

    def test_first_two_age_pulses_do_not_reset_or_announce(self):
        self.area.age = 0
        self.area.empty = False
        handler = self.handler()
        for age in (1, 2):
            asyncio.run(handler.area_update())
            self.assertEqual(age, self.area.age)
        handler._reset_area.assert_not_called()
        handler.wiz_handler.wiznet_targets.assert_not_called()
        handler.message_bus.send_to_character.assert_not_awaited()

    def test_world_initialization_does_not_announce_periodic_resets(self):
        handler = self.handler()
        handler.initialize_world()
        handler._reset_area.assert_called_once_with(self.area)
        self.assertEqual((0, False), (self.area.age, self.area.empty))
        handler.wiz_handler.wiznet_targets.assert_not_called()

    def test_last_departure_waits_for_reset_before_marking_empty(self):
        self.room.add_player_to_room(self.character)
        self.area.age = 2
        self.room.remove_player_from_room(self.character)
        self.room.remove_player_from_room(self.character)
        self.assertEqual((self.area.number_of_players, self.area.empty), (0, False))
        handler = self.handler()
        with patch('area.AreaHandler.rng.number_range', return_value=1):
            asyncio.run(handler.area_update())
        handler._reset_area.assert_called_once_with(self.area)
        self.assertEqual((self.area.age, self.area.empty), (1, True))

    def test_movement_within_area_and_across_areas(self):
        other_room = Room(id='two', area_id='area')
        other_room.bind_area(self.area)
        other_area = Area(author='ROM', name='Other', id='other', empty=True, age=25)
        destination = Room(id='three', area_id='other')
        destination.bind_area(other_area)
        self.room.add_player_to_room(self.character)
        self.area.age = 7
        self.room.remove_player_from_room(self.character)
        other_room.add_player_to_room(self.character)
        self.assertEqual((self.area.number_of_players, self.area.age), (1, 7))
        other_room.remove_player_from_room(self.character)
        destination.add_player_to_room(self.character)
        self.assertEqual(self.area.number_of_players, 0)
        self.assertEqual((other_area.number_of_players, other_area.empty, other_area.age), (1, False, 0))

    def test_occupied_area_resets_at_fifteen_and_empty_area_at_thirty_one(self):
        self.room.add_player_to_room(self.character)
        handler = self.handler()
        self.area.age = 13
        asyncio.run(handler.area_update())
        handler._reset_area.assert_not_called()
        with patch('area.AreaHandler.rng.number_range', return_value=2):
            asyncio.run(handler.area_update())
        handler._reset_area.assert_called_once_with(self.area)
        self.assertFalse(self.area.empty)
        handler._reset_area.reset_mock()
        self.room.remove_player_from_room(self.character)
        self.area.empty = True
        self.area.age = 29
        asyncio.run(handler.area_update())
        handler._reset_area.assert_not_called()
        asyncio.run(handler.area_update())
        handler._reset_area.assert_called_once_with(self.area)

    def test_school_exception_uses_actual_room_area_not_suggested_level_range(self):
        self.area.empty = False
        self.area.age = 2
        self.area.vnum_range = (3700, 3800)
        handler = self.handler(SimpleNamespace(area_id='different'))
        asyncio.run(handler.area_update())
        self.assertTrue(self.area.empty)
        self.area.empty = False
        self.area.age = 2
        handler = self.handler(SimpleNamespace(area_id=self.area.id))
        asyncio.run(handler.area_update())
        self.assertEqual(self.area.age, 13)
        self.assertFalse(self.area.empty)

    def test_occupied_area_does_not_replenish_ground_objects(self):
        handler = self.handler()
        handler.item_registry = SimpleNamespace(get=lambda **kw: object())
        handler.room_registry = SimpleNamespace(get=lambda **kw: self.room)
        reset = SimpleNamespace(arg1='object', arg3=self.room.id)
        self.room.add_player_to_room(self.character)
        with patch('area.AreaHandler.ItemUtil.create_object') as create:
            self.assertFalse(handler._do_object_reset(reset, self.area))
            create.assert_not_called()
            self.room.remove_player_from_room(self.character)
            create.return_value = SimpleNamespace(id='item')
            self.assertTrue(handler._do_object_reset(reset, self.area))
            self.assertIn('item', self.room.contents)

    def test_room_and_area_service_link_both_load_orders(self):
        room_service = RoomService.__new__(RoomService)
        room_service.area_registry = SimpleNamespace(get_or_none=lambda **kw: None)
        room_service.room_registry = Mock()
        room_service._register_fetch_item(self.room)
        self.room.add_player_to_room(self.character)
        service = AreaService.__new__(AreaService)
        service.registry_service = SimpleNamespace(room_registry=SimpleNamespace(all_rooms=lambda: [self.room]))
        for name in ('reset', 'shop', 'special', 'item', 'mobile'):
            setattr(service, name + '_registry', Mock())
        service.special_registry.all_specials_by_area_id.return_value = []
        service.mobile_registry.all_mobiles_by_area_id.return_value = []
        service._lazy_load(self.area)
        service._lazy_load(self.area)
        self.assertIs(self.room.area, self.area)
        self.assertEqual(self.area.number_of_players, 1)
        new_room = Room(id='new', area_id=self.area.id)
        room_service.area_registry = SimpleNamespace(get_or_none=lambda **kw: self.area)
        room_service._register_fetch_item(new_room)
        self.assertIs(new_room.area, self.area)


if __name__ == '__main__':
    unittest.main()

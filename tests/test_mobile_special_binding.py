import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests import test_mobile_armor_isolation as armor_fixtures
from area.Area import Area
from area.AreaHandler import AreaHandler
from area.AreaService import AreaService
from area.Room import Room
from area.Special import Special
from area.SpecialRegistry import SpecialRegistry
from area.SpecialService import SpecialService
from mobile.MobileHandler import MobileHandler
from mobile.MobileService import MobileService
from mobile.MobileFactory import MobileFactory


class MobileSpecialBindingTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        fixture = armor_fixtures.MobileArmorIsolationTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.prototype, self.enums = fixture.prototype, fixture.enums
        self.specials = SpecialRegistry()
        self.special = Special.from_json({
            'id': 'guard-special', 'areaId': self.prototype.area_id, 'mobVnum': self.prototype.vnum,
            'name': 'spec_guard', 'specialFunction': ['lambda ctx: ctx.mark_performed()']})
        self.specials.register(self.special)
        self.service = MobileService.__new__(MobileService)
        self.service.special_registry = self.specials
        self.service.game_data = SimpleNamespace(races={})
        self.enterContext(patch.object(MobileFactory, "from_data", return_value=self.prototype))
        self.service.logger = Mock()

    async def test_area_loaded_before_mobile_does_not_lose_binding(self):
        area_service = AreaService.__new__(AreaService)
        area_service.registry_service = SimpleNamespace(room_registry=SimpleNamespace(all_rooms=lambda: []))
        for name in ('reset', 'shop', 'item', 'mobile'):
            setattr(area_service, name + '_registry', Mock())
        area_service.mobile_registry.all_mobiles_by_area_id.return_value = []
        area_service.special_registry = self.specials
        area_service._lazy_load(Area(author='ROM', name='Test', id=self.prototype.area_id))
        prototype = self.service._build_fetch_item({})
        self.assertEqual(prototype.special_name, 'spec_guard')
        self.assertEqual(prototype.special_function, self.special.special_function)
        self.assertIsNot(prototype.special_function, self.special.special_function)
        spawned = MobileFactory.create(prototype, self.enums)
        handler = MobileHandler.__new__(MobileHandler)
        handler.logger = Mock()
        handler._flush_context_payloads = AsyncMock()
        self.assertTrue(await handler.execute_special_function(spawned, Room(id='room')))

    async def test_reset_spawn_and_clone_inherit_independent_lambda_lists(self):
        prototype = self.service._build_fetch_item({})
        room = Room(id='room', area_id=prototype.area_id)
        handler = AreaHandler.__new__(AreaHandler)
        handler.mobile_registry = SimpleNamespace(get=lambda **kw: prototype)
        handler.room_registry = SimpleNamespace(get=lambda **kw: room)
        handler.enum_provider = self.enums
        handler._count_live_mobiles = Mock(return_value=0)
        handler._mark_pet_shop_stock_mob = Mock()
        handler._register_live_character = Mock()
        reset = SimpleNamespace(arg1=prototype.vnum, arg2=2, arg3=room.id, arg4=2)
        success, spawned = handler._do_mob_reset(True, reset)
        self.assertTrue(success)
        clone = MobileFactory.copy_instance(spawned, self.enums)
        self.assertEqual(clone.special_name, 'spec_guard')
        self.assertEqual(clone.special_function, self.special.special_function)
        spawned.special_function.clear()
        self.assertEqual(len(clone.special_function), 1)
        self.assertEqual(len(prototype.special_function), 1)
        self.assertEqual(len(self.special.special_function), 1)

    async def test_no_assignment_does_not_borrow_named_library_or_other_area_special(self):
        self.prototype.area_id = 'other-area'
        self.specials.register(Special(id='library', name='spec_guard', special_function=['lambda ctx: ctx.mark_performed()']))
        prototype = self.service._build_fetch_item({})
        self.assertIsNone(prototype.special_name)
        self.assertEqual(prototype.special_function, [])
        spawned = MobileFactory.create(prototype, self.enums)
        handler = MobileHandler.__new__(MobileHandler)
        handler.logger = Mock()
        self.assertFalse(await handler.execute_special_function(spawned, Room(id='room')))

    async def test_each_load_uses_current_special_document(self):
        first = self.service._build_fetch_item({})
        self.special.special_function = ['lambda ctx: ctx.finish()']
        # Freshly built prototypes use the current registry on bulk or individual loads.
        with patch.object(MobileFactory, 'from_data', return_value=MobileFactory.create(first, self.enums)):
            reloaded = self.service._build_fetch_item({})
        self.assertEqual(reloaded.special_function, ['lambda ctx: ctx.finish()'])
        self.assertEqual(first.special_function, ['lambda ctx: ctx.mark_performed()'])

    async def test_reload_rebinds_live_mobiles_prototypes_and_named_delegates(self):
        prototype = self.service._build_fetch_item({})
        room = Room(id='live-room', area_id='away-from-prototype')
        moved = MobileFactory.create(prototype, self.enums)
        overridden = MobileFactory.create(prototype, self.enums)
        unassigned = MobileFactory.create(prototype, self.enums)
        unassigned.vnum = '9999'
        unassigned.bind_special(None)
        delegate = Special(id='delegate', name='spec_delegate', special_function=['lambda ctx: ctx.mark_performed()'])
        override = Special(id='override', name='spec_override', special_function=['lambda ctx: ctx.finish()'])
        self.specials.register(delegate)
        self.specials.register(override)
        overridden.special_override_id = override.id
        overridden.bind_special(override)
        for mobile in (moved, overridden, unassigned):
            room.add_mobile_to_room(mobile)

        reload_service = SpecialService.__new__(SpecialService)
        reload_service.special_registry = self.specials
        reload_service.mobile_registry = SimpleNamespace(all_mobiles=lambda: {prototype})
        reload_service.room_registry = SimpleNamespace(all_rooms=lambda: [room])
        reload_service.specials_endpoint = 'https://content.invalid/specials'
        reload_service.logger = Mock()
        handler = MobileHandler.__new__(MobileHandler)
        handler.logger = Mock()
        handler.special_registry = self.specials
        handler._flush_context_payloads = AsyncMock()

        self.assertTrue(await handler.execute_special_function(moved, room))
        self.assertTrue(handler.execute_special_by_name(moved, 'spec_delegate', room))
        self.assertFalse(await handler.execute_special_function(overridden, room))
        replacement = [
            dict(id=self.special.id, areaId=prototype.area_id, mobVnum=prototype.vnum,
                 name='spec_replacement', specialFunction=['lambda ctx: ctx.finish()']),
            dict(id=delegate.id, name=delegate.name, specialFunction=['lambda ctx: ctx.finish()']),
            dict(id=override.id, name=override.name, specialFunction=['lambda ctx: ctx.mark_performed()']),
            dict(id='new', areaId=prototype.area_id, mobVnum=unassigned.vnum,
                 name='spec_added', specialFunction=['lambda ctx: ctx.mark_performed()']),
        ]
        with patch('server.FetchAndRegisterMixin.requests.get', return_value=Mock(json=Mock(return_value=replacement))):
            self.assertTrue(reload_service.reload_specials())

        self.assertEqual('away-from-prototype', moved.area_id)
        self.assertEqual('spec_replacement', moved.special_name)
        self.assertFalse(await handler.execute_special_function(moved, room))
        self.assertFalse(handler.execute_special_by_name(moved, 'spec_delegate', room))
        self.assertTrue(await handler.execute_special_function(overridden, room))
        self.assertTrue(await handler.execute_special_function(unassigned, room))
        self.assertEqual(['lambda ctx: ctx.finish()'], MobileFactory.create(prototype, self.enums).special_function)

        with patch('server.FetchAndRegisterMixin.requests.get', return_value=Mock(json=Mock(return_value=[{'invalid': True}]))):
            self.assertFalse(reload_service.reload_specials())
        self.assertEqual('spec_replacement', moved.special_name)
        self.assertTrue(await handler.execute_special_function(overridden, room))
        self.assertFalse(handler.execute_special_by_name(moved, 'spec_delegate', room))

        with patch('server.FetchAndRegisterMixin.requests.get', return_value=Mock(json=Mock(return_value=[]))):
            self.assertTrue(reload_service.reload_specials())
        for mobile in (prototype, moved, overridden, unassigned):
            self.assertIsNone(mobile.special_name)
            self.assertEqual([], mobile.special_function)


if __name__ == '__main__':
    unittest.main()

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
from mobile.MobileHandler import MobileHandler
from mobile.MobileService import MobileService
from util.MobileUtil import MobileUtil


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
        self.service._build_mobile = Mock(return_value=self.prototype)
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
        spawned = MobileUtil.create_mobile(prototype, self.enums)
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
        clone = MobileUtil.clone_mobile_instance(spawned, self.enums)
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
        spawned = MobileUtil.create_mobile(prototype, self.enums)
        handler = MobileHandler.__new__(MobileHandler)
        handler.logger = Mock()
        self.assertFalse(await handler.execute_special_function(spawned, Room(id='room')))

    async def test_each_load_uses_current_special_document(self):
        first = self.service._build_fetch_item({})
        self.special.special_function = ['lambda ctx: ctx.finish()']
        # Freshly built prototypes use the current registry on bulk or individual loads.
        with patch.object(self.service, '_build_mobile', return_value=MobileUtil.create_mobile(first, self.enums)):
            reloaded = self.service._build_fetch_item({})
        self.assertEqual(reloaded.special_function, ['lambda ctx: ctx.finish()'])
        self.assertEqual(first.special_function, ['lambda ctx: ctx.mark_performed()'])


if __name__ == '__main__':
    unittest.main()

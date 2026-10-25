import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests.test_update_handler_active_players import Room
from api.MobileApi import MobileApi
from mobile.MobileHandler import MobileHandler
from area.Special import Special
from enum import IntEnum


class ActBits(IntEnum):
    ACT_SCAVENGER = 1


class MobilePulseTests(unittest.IsolatedAsyncioTestCase):
    def handler(self):
        room = Room(id='room', area_id='area', name='Room', vnum='1')
        actor = SimpleNamespace(id='mob', name='scavenger', short_description='a scavenger',
                                vnum='2', room_id='room', area_id='area', inventory=[],
                                status_flags=SimpleNamespace(act=1), gold=0, silver=0, wealth=5000000)
        room.mobiles[actor.id] = actor
        handler = MobileHandler.__new__(MobileHandler)
        handler.logger = Mock()
        handler.act_bits = ActBits
        handler.wear_flags = SimpleNamespace(ITEM_TAKE=SimpleNamespace(value=1))
        handler.room_registry = SimpleNamespace(all_rooms=lambda: [room], get_or_none=lambda **kw: room)
        handler.registry_service = SimpleNamespace(character_registry=SimpleNamespace(playing={}))
        handler.area_registry = Mock(get_or_none=Mock(return_value=SimpleNamespace(empty=False)))
        handler.shop_registry = Mock(find_by_keeper_vnum=Mock(return_value=object()))
        handler.rng = Mock(number_range=Mock(return_value=10), number_bits=Mock(return_value=0))
        handler.execute_special_function = AsyncMock(return_value=False)
        handler._execute_generic_special = AsyncMock()
        handler.message_bus = Mock(send_to_room=AsyncMock())
        return handler, room, actor

    async def test_successful_special_skips_shop_money_and_generic_actions(self):
        handler, room, actor = self.handler()
        handler.execute_special_function.return_value = True
        with patch.object(MobileApi, 'mobile_is_charmed', return_value=False):
            await handler.mobile_update()
        self.assertEqual((0, 0), (actor.gold, actor.silver))
        handler.rng.number_range.assert_not_called()
        handler._execute_generic_special.assert_not_awaited()

    async def test_failed_special_replenishes_even_when_not_standing(self):
        handler, room, actor = self.handler()
        events = []
        handler.execute_special_function.side_effect = lambda *args: events.append('special') or False
        handler.rng.number_range.side_effect = lambda *args: events.append('money roll') or 10
        with patch.object(MobileApi, 'mobile_is_charmed', return_value=False), patch.object(
                MobileApi, 'mobile_is_standing', return_value=False):
            await handler.mobile_update()
        self.assertEqual(['special', 'money roll', 'money roll'], events)
        self.assertEqual((10, 1000), (actor.gold, actor.silver))
        handler._execute_generic_special.assert_not_awaited()

    async def test_collection_scavenge_skips_owned_item_and_announces_best_allowed_item(self):
        handler, room, actor = self.handler()
        viewer = SimpleNamespace(id='viewer', name='Owner')
        room.characters[viewer.id] = viewer
        protected = SimpleNamespace(id='protected', owner='Owner', cost=100, wear_flags=1,
                                    short_description='a protected gem')
        allowed = SimpleNamespace(id='allowed', owner='', cost=10, wear_flags=1,
                                  short_description='a coin')
        room.contents = {obj.id: obj for obj in [protected, allowed]}
        documents = json.loads((Path(__file__).resolve().parents[1] / 'resources/collections/SOMDB.Specials.json').read_text())
        special = Special.from_json(next(doc for doc in documents if doc.get('name') == 'spec_scavenge'))
        handler.special_registry = SimpleNamespace(all_specials=lambda: [special])
        handler._special_library_cache = None
        # Exercise the real generic dispatcher and payload delivery.
        del handler._execute_generic_special
        with patch.object(MobileApi, 'mobile_is_charmed', return_value=False), patch.object(
                MobileApi, 'mobile_is_standing', return_value=True), patch(
                'api.CharacterApi.CharacterApi.is_immortal', return_value=False), patch(
                'api.CharacterApi.CharacterApi.is_npc', side_effect=lambda entity: entity is actor), patch(
                'api.CharacterApi.CharacterApi.is_same_group', return_value=False), patch(
                'api.ItemApi.ItemApi.get_enum', return_value=None):
            await handler.mobile_update()
        self.assertEqual([allowed], actor.inventory)
        self.assertEqual({'protected': protected}, room.contents)
        handler.message_bus.send_to_room.assert_awaited_once_with(
            handler.message_bus.text_to_message('a scavenger gets a coin.\r\n'), [viewer])
        handler.rng.number_bits.assert_called_once_with(6)


if __name__ == '__main__':
    unittest.main()

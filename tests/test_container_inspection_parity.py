"""Container lookup/visibility and inventory quantity regressions from act_info.c."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock

from tests.test_movement_rules_parity import MovementFixture, item
from interp.commands.Info import Info
from item.ItemHandler import ItemHandler
from player.PlayerHandler import PlayerHandler


class ContainerInspectionTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.bus = NS(text_to_message=lambda text: text, send_to_character=AsyncMock())
        rooms = NS(get=lambda **kw: self.rooms.get_or_none(**kw))
        self.handler = ItemHandler(self.bus, NS(room_registry=rooms, item_registry=None))
        self.player = PlayerHandler.__new__(PlayerHandler)
        self.player.room_registry = self.rooms
        self.info = Info.__new__(Info)
        self.info.room_registry = self.rooms
        self.info.interp_api = self.api

    def bag(self, name='bag', **kwargs):
        return item(name, itemType='container', value1='0', **kwargs)

    async def look_in(self, name='bag'):
        self.bus.send_to_character.reset_mock()
        context = self.ctx('look')
        context.parameters = ['in', name]
        self.player._classify_look(self.actor, context)
        denial = await self.info.do_look(self.actor, context)
        if denial is not None:
            return context, denial, denial.get('to_char', '')
        await self.handler.look_in_item(self.actor, context)
        self.assertTrue(context.done)
        return context, None, self.bus.send_to_character.call_args.args[1]

    async def test_invisible_floor_container_is_rejected_until_detected(self):
        bag = self.bag(extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))
        bag.contains = [item('secret treasure')]
        self.room.contents[bag.id] = bag
        _, denial, text = await self.look_in()
        self.assertEqual('target_missing', denial['blocked_key'])
        self.assertNotIn('secret treasure', text)
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        _, denial, text = await self.look_in()
        self.assertIsNone(denial)
        self.assertIn('secret treasure', text)

    async def test_lookup_prefers_floor_then_inventory_then_equipment(self):
        floor, carried, worn = [self.bag('bag ' + location) for location in ('floor', 'carried', 'worn')]
        for bag in (floor, carried, worn):
            bag.contains = [item(bag.name + ' treasure')]
        self.room.contents[floor.id] = floor
        self.actor.loot.append(carried)
        self.actor.equip_item(worn, 'held')
        for expected in (floor, carried, worn):
            context, denial, text = await self.look_in()
            self.assertIsNone(denial)
            self.assertIs(expected, context.look_in_target)
            self.assertIn(expected.contains[0].short(), text)
            if expected is floor:
                self.room.contents.clear()
            elif expected is carried:
                self.actor.loot.remove(carried)

    async def test_ordinals_count_visible_containers_and_share_guard_target(self):
        hidden = self.bag('bag hidden', extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))
        first, second = self.bag('bag first'), self.bag('bag second')
        second.contains = [item('second treasure')]
        self.room.contents = {bag.id: bag for bag in (hidden, first, second)}
        context, denial, text = await self.look_in('2.bag')
        self.assertIsNone(denial)
        self.assertIs(second, context.look_in_target)
        self.assertIn('second treasure', text)
        second.value1 = str(int(self.enums.get('containerState').CONT_CLOSED))
        _, denial, text = await self.look_in('2.bag')
        self.assertEqual('is_closed', denial['blocked_key'])
        self.assertNotIn('second treasure', text)

    async def test_contents_filter_visibility_combine_and_do_not_recurse(self):
        bag = self.bag()
        nested = self.bag('nested bag')
        nested.contains = [item('concealed nested treasure')]
        bag.contains = [item('gem'), item('gem'), nested,
                        item('hidden ring', extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))]
        self.actor.loot.append(bag)
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_COMBINE)
        _, _, text = await self.look_in()
        self.assertIn('( 2) gem', text)
        self.assertIn('nested bag', text)
        self.assertNotIn('concealed nested treasure', text)
        self.assertNotIn('hidden ring', text)
        self.actor.status_flags.unset_flag('comm', self.enums.get('commFlags').COMM_COMBINE)
        _, _, text = await self.look_in()
        self.assertEqual(2, text.count('gem'))
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        _, _, text = await self.look_in()
        self.assertIn('hidden ring', text)

    async def test_hidden_only_contents_are_reported_as_nothing(self):
        bag = self.bag()
        bag.contains = [item('hidden gem', extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))]
        self.actor.loot.append(bag)
        _, _, text = await self.look_in()
        self.assertIn('Nothing.', text)
        self.assertNotIn('hidden gem', text)

    async def test_combined_inventory_counts_one_nine_ten_and_eleven(self):
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_COMBINE)
        for quantity in (1, 2, 9, 10, 11):
            with self.subTest(quantity=quantity):
                self.actor.loot = [item('gem', vnum=str(n)) for n in range(quantity)]
                await self.handler.print_inventory(self.actor)
                text = self.bus.send_to_character.call_args.args[1]
                self.assertEqual(1, text.count('gem'))
                if quantity > 1:
                    self.assertIn(f'({quantity:2d}) gem', text)
                else:
                    self.assertNotIn('( 1)', text)

    async def test_inventory_excludes_hidden_and_worn_and_can_show_uncombined_duplicates(self):
        self.actor.loot = [item('gem'), item('gem'),
                           item('secret', extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))]
        worn = item('worn armor')
        self.actor.equip_item(worn, 'torso')
        self.actor.status_flags.unset_flag('comm', self.enums.get('commFlags').COMM_COMBINE)
        await self.handler.print_inventory(self.actor)
        text = self.bus.send_to_character.call_args.args[1]
        self.assertEqual(2, text.count('gem'))
        self.assertNotIn('secret', text)
        self.assertNotIn('worn armor', text)

    def test_examine_routes_worn_container_through_the_same_lookup(self):
        self.actor.equip_item(self.bag(), 'held')
        result = self.info.do_examine(self.actor, self.ctx('examine', 'bag'))
        self.assertTrue(result['look_in'])


if __name__ == '__main__':
    unittest.main()

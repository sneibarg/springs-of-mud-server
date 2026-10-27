import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests.test_update_handler_active_players import Room
from area.AreaHandler import AreaHandler
from combat.CombatHandler import FightHandler
from game.Equipped import Equipped
from item.ItemFactory import ItemFactory


from item.ItemOwnership import ItemOwnership


class WorldObjectTests(unittest.TestCase):
    def setUp(self):
        self.room = Room(id='room')
        self.registry = SimpleNamespace(all_rooms=lambda: [None, self.room])

    def item(self, vnum, contains=None):
        return SimpleNamespace(id=str(vnum), vnum=str(vnum), contains=contains or [], value1=0)

    def test_ground_and_nested_container_lookup_uses_room_objects(self):
        nested = self.item(2)
        chest = self.item(1, [nested])
        self.room.add_item_to_room(chest)
        self.assertEqual(ItemOwnership(None, self.registry).find_world_vnum('1'), (chest, True))
        self.assertEqual(ItemOwnership(None, self.registry).find_world_vnum('2'), (nested, False))
        self.assertEqual(ItemOwnership(None, self.registry).find_world_vnum('missing'), (None, False))

    def test_lookup_includes_player_and_mobile_inventory_and_equipment(self):
        carried, worn, stock = self.item(1), self.item(2), self.item(3)
        player = SimpleNamespace(id='player', loot=[carried], equipped=Equipped(shield=worn))
        mob = SimpleNamespace(id='mob', inventory=[stock], equipped=None)
        self.room.add_player_to_room(player)
        self.room.add_mobile_to_room(mob)
        for item in (carried, worn, stock):
            with self.subTest(vnum=item.vnum):
                self.assertEqual(ItemOwnership(None, self.registry).find_world_vnum(item.vnum), (item, False))

    def test_put_reset_replenishes_ground_container_even_if_previous_reset_failed(self):
        chest = self.item(1)
        self.room.add_item_to_room(chest)
        handler = AreaHandler.__new__(AreaHandler)
        handler.room_registry = self.registry
        handler.item_registry = SimpleNamespace(get=lambda **kw: self.item(kw['vnum']))
        handler._count_live_items = Mock(return_value=0)
        reset = SimpleNamespace(arg1='2', arg2=10, arg3='1', arg4=2)
        with patch('area.AreaHandler.ItemFactory.create', side_effect=lambda template: self.item(template.vnum)):
            self.assertTrue(handler._do_put_reset(False, reset, SimpleNamespace(number_of_players=0)))
        self.assertEqual([item.vnum for item in chest.contains], ['2', '2'])

    def test_carried_container_requires_successful_previous_reset(self):
        chest = self.item(1)
        self.room.add_mobile_to_room(SimpleNamespace(id='mob', inventory=[chest], equipped=None))
        handler = AreaHandler.__new__(AreaHandler)
        handler.room_registry = self.registry
        handler.item_registry = SimpleNamespace(get=lambda **kw: self.item(kw['vnum']))
        handler._count_live_items = Mock(return_value=0)
        reset = SimpleNamespace(arg1='2', arg2=10, arg3='1', arg4=1)
        with patch('area.AreaHandler.ItemFactory.create', side_effect=lambda template: self.item(template.vnum)):
            self.assertFalse(handler._do_put_reset(False, reset, SimpleNamespace(number_of_players=0)))
            self.assertEqual(chest.contains, [])
            self.assertTrue(handler._do_put_reset(True, reset, SimpleNamespace(number_of_players=0)))


class ShieldBlockTests(unittest.TestCase):
    def setUp(self):
        self.handler = FightHandler.__new__(FightHandler)
        self.handler._defense_skill_percent = Mock(return_value=100)
        self.attacker = SimpleNamespace(level=20)
        self.victim = SimpleNamespace(level=20, equipped=Equipped(shield=object()))

    def test_shield_predicate_reports_actual_equipment(self):
        self.assertTrue(self.victim.equipped.is_shield_equipped())
        self.victim.equipped.shield = None
        self.assertFalse(self.victim.equipped.is_shield_equipped())

    def test_missing_shield_or_sleeping_prevents_roll(self):
        with patch('combat.CombatHandler.CharacterApi.is_awake', return_value=True), \
                patch('combat.CombatHandler.random.randint') as roll:
            for equipped in (None, Equipped()):
                self.victim.equipped = equipped
                self.assertFalse(self.handler.check_shield_block(self.attacker, self.victim))
            roll.assert_not_called()
        self.victim.equipped = Equipped(shield=object())
        with patch('combat.CombatHandler.CharacterApi.is_awake', return_value=False):
            self.assertFalse(self.handler.check_shield_block(self.attacker, self.victim))

    def test_rom_roll_boundary_and_level_adjustment(self):
        # ROM: 100 // 5 + 3 = 23; equality fails, lower rolls block.
        with patch('combat.CombatHandler.CharacterApi.is_awake', return_value=True), \
                patch('combat.CombatHandler.random.randint', side_effect=[22, 23, 27, 28]):
            self.assertTrue(self.handler.check_shield_block(self.attacker, self.victim))
            self.assertFalse(self.handler.check_shield_block(self.attacker, self.victim))
            self.victim.level += 5
            self.assertTrue(self.handler.check_shield_block(self.attacker, self.victim))
            self.assertFalse(self.handler.check_shield_block(self.attacker, self.victim))

    def test_zero_skill_preserves_rom_base_chance(self):
        self.handler._defense_skill_percent.return_value = 0
        with patch('combat.CombatHandler.CharacterApi.is_awake', return_value=True), \
                patch('combat.CombatHandler.random.randint', side_effect=[2, 3]):
            self.assertTrue(self.handler.check_shield_block(self.attacker, self.victim))
            self.assertFalse(self.handler.check_shield_block(self.attacker, self.victim))


if __name__ == '__main__':
    unittest.main()

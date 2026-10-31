"""ROM character inspection, passive peek and score carry-accounting regressions."""
import unittest
from unittest.mock import Mock, patch

from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi
from api.ItemApi import ItemApi
from interp.commands.Info import Info
from skill.Ability import Ability


class InfoInspectionTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.info = Info.__new__(Info)
        self.info.room_registry = self.rooms
        self.info.interp_api = self.api
        self.info.skill_registry = self.skill_registry
        self.info.rng = Mock(number_percent=Mock(return_value=1))
        self.improve = self.enterContext(patch.object(Ability, 'check_improve'))
        self.target = self.follower('Victim')

    def look(self, target=None, actor=None):
        actor = actor or self.actor
        context = self.ctx('look', character=actor)
        context.parameters = [(target or self.target).name]
        result = self.info.look_target(actor, context)
        self.assertTrue(context.done)
        return result

    def learn_peek(self, percent=100):
        self.actor.set_learned('peek', percent, collection_name='skills', create=True)

    def test_look_filters_invisible_equipment_by_observer(self):
        ring = item('secret ring', itemType='armor', extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))
        self.target.equip_item(ring, 'finger1')
        self.assertFalse(ItemApi.can_see_object(self.room, self.actor, ring))
        self.assertNotIn(ring.short(), self.look())
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        self.assertIn(ring.short(), self.look())

    def test_hidden_equipment_does_not_emit_empty_equipment_heading(self):
        ring = item('secret ring', extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))
        self.target.equip_item(ring, 'finger1')
        self.assertNotIn('is using:', self.look())

    def test_peek_success_lists_visible_unworn_roots_and_learns_once(self):
        self.learn_peek()
        gem = item('visible gem')
        hidden = item('hidden gem', extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))
        bag = item('closed bag', itemType='container', value1=str(int(self.enums.get('containerState').CONT_CLOSED)))
        bag.contains = [item('concealed contents')]
        worn = item('worn ring')
        self.target.loot.extend([gem, hidden, bag])
        self.target.equip_item(worn, 'finger1')
        output = self.look()
        inventory = output.split('You peek at the inventory:')[1]
        self.assertIn(gem.short(), inventory)
        self.assertIn(bag.short(), inventory)
        self.assertNotIn(hidden.short(), inventory)
        self.assertNotIn(worn.short(), inventory)
        self.assertNotIn('concealed contents', inventory)
        self.improve.assert_called_once_with(self.actor, self.skills['peek'].id, True, 4)
        self.assertIn(gem, self.target.loot)

    def test_peek_roll_is_strict_and_respects_level_daze_and_drunk(self):
        self.learn_peek(90)
        for level, daze, drunk, threshold in ((20, 0, 0, 90), (20, 1, 0, 60),
                                              (20, 0, 11, 81), (20, 1, 11, 54)):
            self.actor.level = level
            self.actor.status_flags.pulse_daze = daze
            self.actor.status_flags.drunk = drunk
            for roll in (threshold - 1, threshold):
                with self.subTest(daze=daze, drunk=drunk, roll=roll):
                    self.improve.reset_mock()
                    self.info.rng.number_percent.return_value = roll
                    self.assertEqual(roll < threshold, 'You peek at' in self.look())
                    self.assertEqual(int(roll < threshold), self.improve.call_count)
        self.actor.character_class.name = 'cleric'
        self.actor.level = 20  # peek requires cleric level 21
        self.info.rng.number_percent.return_value = 1
        self.assertNotIn('You peek at', self.look())

    def test_unlearned_self_and_npc_actor_do_not_peek_or_learn(self):
        self.assertNotIn('You peek at', self.look())
        self.learn_peek()
        self.info.rng.number_percent.reset_mock()
        self.assertNotIn('You peek at', self.look(self.actor))
        npc = self.npc()
        self.room.add_mobile_to_room(npc)
        self.assertNotIn('You peek at', self.look(self.target, actor=npc))
        self.info.rng.number_percent.assert_not_called()
        self.improve.assert_not_called()

    def test_peek_npc_inventory_and_empty_list_use_authored_heading(self):
        self.learn_peek()
        npc = self.npc()
        npc.name = 'guard'
        npc.hit = npc.max_hit = 100
        self.room.add_mobile_to_room(npc)
        self.skills['peek'].payload.to_char['inventory'] = 'Custom designer heading'
        self.assertIn('Custom designer heading\r\nNothing.', self.look(npc))
        npc.inventory.append(item('npc treasure'))
        self.assertIn('npc treasure', self.look(npc))

    def test_peek_combine_groups_formatted_text_only_when_enabled(self):
        self.learn_peek()
        self.target.loot.extend([item('gem', vnum='1'), item('gem', vnum='2')])
        self.actor.status_flags.unset_flag('comm', self.enums.get('commFlags').COMM_COMBINE)
        self.assertEqual(2, self.look().split('You peek at the inventory:')[1].count('gem'))
        self.actor.status_flags.set_flag('comm', self.enums.get('commFlags').COMM_COMBINE)
        self.assertIn('( 2) gem', self.look())

    def test_score_uses_recursive_equipped_and_coin_weight_without_double_counting(self):
        self.actor.loot.clear()
        bag = item('bag', itemType='container', weight=10, value4='50')
        bag.contains = [item('rock', weight=200)]
        armor = item('armor', itemType='armor', weight=90)
        self.actor.loot.extend([bag, armor])
        self.actor.equip_item(armor, 'torso')
        self.actor.silver, self.actor.gold = 19, 4
        output = self.info.do_score(self.actor, self.ctx('score'))
        self.assertEqual(202, self.actor.carry_weight())
        self.assertIn(f'carrying {self.actor.carry_count()}/{self.actor.max_items()} items with weight 20/', output)


if __name__ == '__main__':
    unittest.main()

"""ROM24 item proficiency, consumption exemptions and staff learning cadence."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_movement_rules_parity import MovementFixture, item
from interp.commands.Object import Object


class ItemActivationFollowupTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.commands = Object.__new__(Object)
        self.commands.interp_api = self.api
        self.commands.room_registry = self.rooms

    def test_item_skills_apply_daze_and_drunk_penalties_with_strict_roll_boundary(self):
        for name in ('scrolls', 'staves', 'wands'):
            self.actor.set_learned(name, 90, collection_name='skills', create=True)
            for daze, drunk, threshold in ((0, 0, 92), (1, 0, 68), (0, 11, 84), (1, 11, 63)):
                self.actor.status_flags.pulse_daze = daze
                self.actor.status_flags.drunk = drunk
                for roll in (threshold - 1, threshold):
                    with self.subTest(skill=name, daze=daze, drunk=drunk, roll=roll), \
                            patch('interp.commands.Object.random.randint', return_value=roll):
                        self.assertEqual(roll < threshold, self.commands._item_skill_check(self.actor, name))

    def test_npc_item_skills_stay_zero_at_all_levels(self):
        npc = self.npc()
        for level in (1, 20, 60):
            npc.level = level
            for name in ('scrolls', 'staves', 'wands'):
                for roll in (19, 20, 50):
                    with self.subTest(level=level, skill=name, roll=roll), \
                            patch('interp.commands.Object.random.randint', return_value=roll):
                        self.assertEqual(roll < 20, self.commands._item_skill_check(npc, name))

    def test_unlearned_and_fully_learned_item_skill_boundaries(self):
        for learned, threshold in ((0, 20), (100, 100)):
            self.actor.set_learned('wands', learned, collection_name='skills', create=True)
            for roll in (threshold - 1, threshold):
                with self.subTest(learned=learned, roll=roll), \
                        patch('interp.commands.Object.random.randint', return_value=roll):
                    self.assertEqual(roll < threshold, self.commands._item_skill_check(self.actor, 'wands'))

    def test_trusted_mortal_eating_and_drinking_replenish_conditions(self):
        self.actor.level, self.actor.trust = 20, 52
        self.actor.status_flags.fullness = self.actor.status_flags.hunger = 10
        self.actor.status_flags.thirst = 0
        food = item('food', itemType='food', value0='2', value1='3', value3='0')
        self.actor.loot.append(food)
        self.commands.do_eat(self.actor, self.ctx('eat', 'food'))
        self.assertEqual((12, 13), (self.actor.status_flags.fullness, self.actor.status_flags.hunger))
        self.assertNotIn(food, self.actor.loot)
        bottle = item('bottle', itemType='drink', value0='10', value1='10', value2='water', value3='0')
        bottle.liquid_affect_data = [0, 2, 10, 3, 4]
        self.actor.loot.append(bottle)
        self.commands.logger = Mock()
        self.commands.do_drink(self.actor, self.ctx('drink', 'bottle'))
        self.assertEqual((14, 4, 19), (self.actor.status_flags.fullness,
                                     self.actor.status_flags.thirst, self.actor.status_flags.hunger))
        self.assertEqual('6', bottle.value1)

    def test_actual_immortal_and_disabled_conditions_remain_exempt(self):
        self.actor.level, self.actor.trust = 52, 0
        self.actor.status_flags.fullness = 10
        self.assertEqual(10, Object._gain_condition(self.actor, 'fullness', 5))
        self.actor.level = 20
        self.actor.status_flags.fullness = -1
        self.assertEqual(-1, Object._gain_condition(self.actor, 'fullness', 5))

    def test_staff_improvement_follows_each_eligible_cast_and_skips_other_side(self):
        spell = NS(name='armor', handler_id='spell.armor', target='CHAR_DEFENSIVE')
        self.commands.spell_registry = NS(all_spells=lambda: [spell])
        self.commands._item_skill_check = Mock(return_value=True)
        events = []
        self.commands._cast_item_spell = Mock(side_effect=lambda *args, **kw: events.append('cast') or [])
        self.commands._improve_item_skill = Mock(side_effect=lambda *args: events.append('improve'))
        staff = item('staff', itemType='staff', value2='3', value3='armor', level=1)
        self.actor.equip_item(staff, 'held')
        self.follower('ally')
        npc = self.npc()
        self.room.add_mobile_to_room(npc)
        self.commands.do_brandish(self.actor, self.ctx('brandish'))
        self.assertEqual(['cast', 'improve', 'cast', 'improve'], events)
        self.assertEqual('2', staff.value2)


if __name__ == '__main__':
    unittest.main()

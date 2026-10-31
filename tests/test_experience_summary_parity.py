"""ROM WORTH/REPORT/GROUP summaries using live advancement and visibility."""
import unittest
from types import SimpleNamespace as NS

from tests.test_movement_rules_parity import MovementFixture
from interp.commands.Info import Info
from interp.commands.Communications import Communications
from player.CharacterAdvancement import CharacterAdvancement


class ExperienceSummaryTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.actor.name = 'Alice'
        self.info = Info.__new__(Info)
        self.info.room_registry = self.rooms
        self.commands = Communications(self.registries, NS(), NS(), self.enums, self.api)
        self.actor.level = 20
        self.actor.character_attributes.points = 40
        self.actor.character_race.class_mult = 100
        CharacterAdvancement.reset_experience_for_points(self.actor)
        CharacterAdvancement.gain_experience(self.actor, 250)

    def worth(self, character=None):
        character = character or self.actor
        context = self.ctx('worth', character=character)
        text = self.info.do_worth(character, context)
        self.assertTrue(context.done)
        return text

    def group(self, character=None):
        return self.commands.execute(self.ctx('group', character=character))['to_char']

    def test_worth_uses_total_and_next_threshold_without_mutating_progress(self):
        self.actor.experience_per_level = 9999
        self.assertIn('20250 experience (750 exp to level)', self.worth())
        self.assertEqual((250, 20250, 9999), (self.actor.experience,
                         self.actor.accumulated_experience, self.actor.experience_per_level))

    def test_worth_retains_experience_debt_after_loss(self):
        CharacterAdvancement.gain_experience(self.actor, -1250)
        self.assertEqual(0, self.actor.experience)
        self.assertIn('19000 experience (2000 exp to level)', self.worth())

    def test_worth_recomputes_creation_point_and_race_cost(self):
        self.actor.character_attributes.points = 50
        self.actor.character_race.class_mult = 120
        self.assertIn('20250 experience (17550 exp to level)', self.worth())

    def test_npc_worth_still_shows_only_currency(self):
        mob = self.npc()
        self.assertEqual(f'You have {mob.gold} gold and {mob.silver} silver.\r\n', self.worth(mob))

    def test_report_announces_total_to_actor_and_room(self):
        payload = self.info.do_report(self.actor)
        self.assertIn('20250 xp.', payload['to_char'])
        self.assertIn('20250 xp.', payload['to_room'])

    def test_group_rows_show_total_xp_for_each_player(self):
        bob = self.follower('Bob')
        bob.leader = self.actor
        bob.accumulated_experience, bob.experience = 5555, 555
        text = self.group()
        self.assertIn('20250 xp', text)
        self.assertIn('5555 xp', text)

    def test_group_names_respect_observer_visibility_and_detection(self):
        bob = self.follower('Bob')
        bob.leader = self.actor
        self.flag(bob, 'AFF_INVISIBLE')
        self.assertNotIn('Bob', self.group())
        self.assertIn('Someone', self.group())
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        self.assertIn('Bob', self.group())
        self.flag(self.actor, 'AFF_INVISIBLE')
        self.assertTrue(self.group(bob).startswith("someone's group:"))
        self.assertNotIn('Alice', self.group(bob))

    def test_group_uses_npc_short_description_and_keeps_stats(self):
        mob = self.npc()
        mob.name, mob.short_description = 'guard sentinel', 'a sentinel'
        mob.leader = self.actor
        self.room.add_mobile_to_room(mob)
        text = self.group()
        self.assertIn('A sentinel', text)
        self.assertNotIn('guard sentinel', text)
        self.assertIn('Mob', text)
        self.assertIn('0 xp', text)


if __name__ == '__main__':
    unittest.main()

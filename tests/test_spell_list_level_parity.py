import re
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

from tests.test_review_application_fixes import RuntimeFixture
from src.devtools.collection_query import load_collections
from interp.commands.Info import Info
from skill.Spell import Spell
from skill.SpellRegistry import SpellRegistry
from skill.Skill import Skill
from skill.SkillRegistry import SkillRegistry


class SpellListLevelParityTests(RuntimeFixture, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        collections = load_collections(Path(__file__).resolve().parents[1] / 'resources/collections',
                                       ['spells', 'skills'])
        cls.spell_documents = collections['spells'].documents
        cls.skill_documents = collections['skills'].documents

    def setUp(self):
        super().setUp()
        self.info = Info.__new__(Info)
        self.info.interp_api = self.api
        self.info.spell_registry = SpellRegistry()
        self.info.skill_registry = SkillRegistry()
        for document in self.spell_documents:
            self.info.spell_registry.register(Spell.from_json(document))
        for document in self.skill_documents:
            self.info.skill_registry.register(Skill.from_json(document))
        self.actor.character_class.name = 'mage'
        self.actor.level = 30
        self.actor.spells = [{'name': name, 'level': learned} for name, learned in
                             [('fireball', 5), ('armor', 90), ('magic missile', 60), ('bless', 100)]]

    def spells(self, argument=''):
        context = self.context('spells', argument)
        output = self.info.do_spells(self.actor, context)
        self.assertTrue(context.done)
        return output

    @staticmethod
    def headings(output):
        return [int(level) for level in re.findall(r'Level\s+(\d+):', output)]

    def test_real_documents_load_with_complete_class_metadata(self):
        self.assertEqual(len(self.spell_documents), 97)
        for document in self.spell_documents:
            for field in ('levelByClass', 'ratingByClass'):
                self.assertEqual(set(document[field]), {'mage', 'cleric', 'thief', 'warrior'})
                self.assertTrue(all(isinstance(value, int) for value in document[field].values()))
        armor = self.info.spell_registry.get(name='armor')
        self.assertEqual(armor.level_by_class, {'mage': 7, 'cleric': 2, 'thief': 10, 'warrior': 5})
        self.assertEqual(armor.rating_by_class, {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2})

    def test_default_listing_orders_class_levels_not_registry_order_or_proficiency(self):
        output = self.spells()
        self.assertEqual(self.headings(output), [1, 7, 22])
        self.assertLess(output.index('magic missile'), output.index('armor'))
        self.assertLess(output.index('armor'), output.index('fireball'))
        self.assertNotIn('bless', output)
        self.assertIn('  5 mana', output)

    def test_class_changes_select_the_corresponding_rom_requirements(self):
        self.actor.character_class.name = 'cleric'
        output = self.spells()
        self.assertEqual(self.headings(output), [2, 7])
        self.assertIn('armor', output)
        self.assertIn('bless', output)
        self.assertNotIn('magic missile', output)
        self.assertNotIn('fireball', output)

    def test_default_hides_future_spells_but_all_shows_them_as_unavailable(self):
        self.actor.level = 7
        self.assertEqual(self.headings(self.spells()), [1, 7])
        output = self.spells('all')
        self.assertEqual(self.headings(output), [1, 7, 22])
        self.assertRegex(output, r'fireball\s+n/a')
        self.assertNotIn('bless', output)

    def test_numeric_filters_apply_to_required_levels(self):
        self.assertEqual(self.headings(self.spells('7')), [1, 7])
        self.assertEqual(self.headings(self.spells('7 22')), [7, 22])
        self.assertIn('No spells found.', self.spells('8 21'))

    def test_every_populated_level_is_printed_once_for_full_collection(self):
        self.actor.level = 51
        self.actor.spells = [{'name': document['name'], 'level': 1} for document in reversed(self.spell_documents)]
        output = self.spells()
        expected = sorted({document['levelByClass']['mage'] for document in self.spell_documents
                           if 1 <= document['levelByClass']['mage'] <= 51})
        self.assertEqual(self.headings(output), expected)
        self.assertGreater(len(expected), 10)

    def test_missing_definition_or_class_map_does_not_fall_back_to_level_one(self):
        self.actor.spells = [{'name': 'unknown', 'level': 100}, {'name': 'broken', 'level': 100}]
        self.info.spell_registry = NS(all_spells=lambda: [NS(name='broken', level_by_class={}, min_mana=5)])
        self.assertIn('No spells found.', self.spells('all'))

    def test_zero_proficiency_is_not_listed(self):
        self.actor.spells = [{'name': 'magic missile', 'level': 0}, {'name': 'armor', 'level': 1}]
        output = self.spells()
        self.assertEqual(self.headings(output), [7])
        self.assertNotIn('magic missile', output)

    def test_shared_skill_listing_keeps_level_order(self):
        self.actor.character_class.name = 'thief'
        self.actor.skills = [{'name': 'second attack', 'level': 10}, {'name': 'dagger', 'level': 90}]
        output = self.info.do_skills(self.actor, self.context('skills', 'all'))
        self.assertEqual(self.headings(output), [1, 12])


if __name__ == '__main__':
    unittest.main()

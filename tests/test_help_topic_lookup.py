import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock

from tests.test_review_application_fixes import RuntimeFixture
from src.devtools.collection_query import load_collections
from interp.HelpEntry import HelpEntry
from interp.HelpRegistry import HelpRegistry
from interp.InterpRegistry import InterpRegistry
from interp.InterpService import InterpService
from interp.commands.Info import Info
from player.PlayerHandler import PlayerHandler


class HelpFixture(RuntimeFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.help_documents = load_collections(Path(__file__).resolve().parents[1] / 'resources/collections',
                                             ['helps'])['helps'].documents

    def setUp(self):
        super().setUp()
        self.helps = HelpRegistry()
        for document in self.help_documents:
            self.helps.register(HelpEntry.from_json(document))
        self.commands = InterpRegistry()
        self.service = InterpService.__new__(InterpService)
        self.service.interp_registry = self.commands
        self.service.help_registry = self.helps
        for name in self.documents:
            document = deepcopy(self.documents[name])
            for key, value in [('shortcuts', ''), ('usage', ''), ('function', [])]:
                document.setdefault(key, value)
            self.commands.register(self.service._build_fetch_item(document))
        self.commands.register(self.service._build_summary_command())
        self.info = Info.__new__(Info)
        self.info.help_registry = self.helps
        self.info.interp_registry = self.commands

    @staticmethod
    def rendered(entry, topic):
        return (entry.keyword + '\n\r' if entry.level >= 0 and topic != 'imotd' else '') + entry.text.removeprefix('.')


class HelpTopicLookupTests(HelpFixture, unittest.TestCase):
    def test_collection_has_unique_explicit_topics_and_valid_document_boundaries(self):
        topics = {}
        self.assertEqual(len(self.help_documents), 171)
        for document in self.help_documents:
            self.assertEqual(document['keyword'], document['keyword'].upper())
            self.assertNotIn('~', document['keyword'])
            self.assertTrue(document['topics'])
            self.assertGreater(len(document['text']), 20)
            for topic in document['topics']:
                self.assertNotIn(topic, topics)
                topics[topic] = document['_id']['$oid']

    def test_every_topic_returns_exactly_its_document(self):
        for entry in self.helps.all_helps():
            for topic in entry.lookup_topics():
                with self.subTest(topic=topic):
                    self.assertIs(self.helps.find_topic(topic), entry)
                    self.assertEqual(self.info.do_help(topic), self.rendered(entry, topic))

    def test_each_command_gets_only_the_exact_associated_document(self):
        for command in self.commands.all_commands():
            if command.help is not None:
                with self.subTest(command=command.name):
                    self.assertEqual(self.info.do_help(command.name), self.rendered(command.help, command.name))

    def test_common_words_and_prefixes_do_not_search_help_prose(self):
        for query in ('command', 'character', 'castl', 'mem', 'the', 'chara'):
            with self.subTest(query=query):
                self.assertEqual(self.info.do_help(query), 'No help on that word.\n\r')
        self.assertEqual(self.info.do_help('cast'), self.rendered(self.helps.find_topic('cast'), 'cast'))

    def test_shared_command_aliases_and_punctuation_resolve_one_document(self):
        for alias, canonical in [('get', 'put'), ('inv', 'inventory'), (':', 'immtalk'), ('!', '!'), ('/', 'recall')]:
            with self.subTest(alias=alias):
                self.assertEqual(self.info.do_help(alias), self.info.do_help(canonical))

    def test_command_spell_collisions_have_explicit_disambiguation(self):
        for command, spell in [('sleep', 'sleep spell'), ('teleport', 'teleport spell'), ('invis', 'invisibility')]:
            with self.subTest(command=command):
                self.assertIs(self.commands.get(name=command).help, self.helps.find_topic(command))
                self.assertNotEqual(self.info.do_help(command), self.info.do_help(spell))
                self.assertIn('cast', self.info.do_help(spell).lower())

    def test_multiword_topics_require_exact_phrase_not_individual_word_prefixes(self):
        result = self.info.do_help("  'CURE   LIGHT'  ")
        self.assertEqual(result, self.info.do_help('cure light'))
        self.assertIn("cast 'cure light'", result.lower())
        for query in ('cure lig', 'light cure', 'light'):
            self.assertEqual(self.info.do_help(query), 'No help on that word.\n\r')

    def test_no_argument_summary_and_non_command_topics_are_available(self):
        self.assertEqual(self.info.do_help(''), self.info.do_help('summary'))
        self.assertIn('original game idea', self.info.do_help('diku').lower())
        self.assertNotEqual(self.info.do_help('motd'), self.info.do_help('imotd'))
        self.assertIn('welcome immortal', self.info.do_help('imotd').lower())

    def test_repaired_records_have_real_content_not_next_documents_header(self):
        for topic, phrase in [('clone', 'duplicates an object'), ('memory', 'size of your mud'),
                              ('armor', 'armor class'), ('affects', 'spells affecting'), ('clan', 'collection of players')]:
            self.assertIn(phrase, self.info.do_help(topic).lower())

    def test_explicit_topics_restrict_keyword_fallback(self):
        registry = HelpRegistry()
        registry.register(HelpEntry('restricted', 'HELP CAST', 'Restricted content', 0, ['only this']))
        self.assertIsNone(registry.find_topic('help'))
        self.assertIsNone(registry.find_topic('cast'))
        self.assertIsNotNone(registry.find_topic('only this'))
        self.service.help_registry = registry
        command = NS(name='cast', help=None)
        self.service._assign_help_to_command(command)
        self.assertIsNone(command.help)

    def test_info_injection_uses_the_shared_help_registry(self):
        from injector import Injector
        from game.RegistryService import RegistryService
        from game.WeatherHandler import WeatherHandler
        from game.EnumProvider import EnumProvider
        from api.InterpApi import InterpApi
        from server.session.SessionHandler import SessionHandler
        injector = Injector()
        registries = NS(interp_registry=self.commands, area_registry=NS(), room_registry=self.rooms,
                        skill_registry=NS(), spell_registry=NS())
        for dependency, value in [(RegistryService, registries), (SessionHandler, SessionHandler()),
                                  (WeatherHandler, NS()), (EnumProvider, self.enums),
                                  (InterpApi, self.api), (HelpRegistry, self.helps)]:
            injector.binder.bind(dependency, to=value)
        info = injector.get(Info)
        self.assertIs(info.help_registry, self.helps)
        self.assertEqual(info.do_help('cast'), self.info.do_help('cast'))

    def test_legacy_titles_support_quoted_aliases_but_never_malformed_prose(self):
        self.assertEqual(HelpEntry('legacy', "CAST 'CURE LIGHT'", 'text', 0).lookup_topics(), {'cast', 'cure light'})
        self.assertEqual(HelpEntry('bad', 'cast\nThis body mentions other commands', '0 NEXT', 0).lookup_topics(), set())

    def test_duplicate_remote_topics_choose_one_stable_document(self):
        entries = [HelpEntry('b', 'OTHER TOPICS', 'Other content', 0, ['help']),
                   HelpEntry('a', 'HELP', 'Correct content', 0, ['help'])]
        for sequence in (entries, list(reversed(entries))):
            registry = HelpRegistry()
            for entry in sequence:
                registry.register(entry)
            self.assertEqual(registry.find_topic('help').id, 'a')

    def test_help_model_preserves_source_ids_and_does_not_mutate_wire_document(self):
        document = deepcopy(self.help_documents[0])
        before = deepcopy(document)
        first, second = HelpEntry.from_json(document), HelpEntry.from_json(document)
        self.assertEqual(first.id, before['_id']['$oid'])
        self.assertEqual(first.id, second.id)
        self.assertEqual(document, before)

    def test_help_reload_is_used_without_stale_command_attachment(self):
        old = self.commands.get(name='help').help
        self.helps.reset()
        replacement = HelpEntry('replacement', 'HELP', 'Updated help.', 0, ['help'])
        self.helps.register(replacement)
        self.assertIsNot(old, replacement)
        self.assertEqual(self.info.do_help('help'), 'HELP\n\rUpdated help.')
        self.helps.reset()
        self.assertEqual(self.info.do_help('help'), 'No help on that word.\n\r')


class HelpCommandEmissionTests(HelpFixture, unittest.IsolatedAsyncioTestCase):
    async def test_help_command_sends_one_message_with_one_document(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.info_commands = self.info
        handler.message_bus = NS(send_to_character=AsyncMock(), text_to_message=lambda value: value)
        context = self.context('help', 'cast')
        await handler.do_help(self.actor, context)
        handler.message_bus.send_to_character.assert_awaited_once_with(self.actor.id, self.info.do_help('cast'))
        self.assertTrue(context.done)


if __name__ == '__main__':
    unittest.main()

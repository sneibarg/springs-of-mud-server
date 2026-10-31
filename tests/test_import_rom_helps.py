import unittest

from src.devtools.import_rom_helps import parse_helps, plan_import, topic_names


class RomHelpImportTests(unittest.TestCase):
    def test_parser_respects_tilde_boundaries_and_stops_at_sentinel(self):
        records = parse_helps("#HELPS\n-1 KICK~\nA kick.\n\nMore text.\n~\n0 'SHIELD BLOCK'~\nBlock.\n~\n0 $~\n#$")
        self.assertEqual([{'keyword': 'KICK', 'level': -1, 'text': 'A kick.\n\nMore text.'},
                          {'keyword': "'SHIELD BLOCK'", 'level': 0, 'text': 'Block.'}], records)
        self.assertEqual([], parse_helps('#ROOMS\n'))

    def test_parser_rejects_truncated_records(self):
        with self.assertRaises(ValueError):
            parse_helps('#HELPS\n0 KICK~\nunfinished')

    def test_topics_preserve_quoted_aliases_and_exact_ability_phrases(self):
        self.assertEqual(['dirt', 'dirt kicking'], topic_names("DIRT 'DIRT KICKING'"))
        self.assertEqual(['mass healing'], topic_names('MASS HEALING', {'mass healing'}))

    def test_import_preserves_existing_documents_disambiguation_and_is_idempotent(self):
        original = [{'_id': {'$oid': 'existing'}, 'keyword': 'SLEEP', 'level': 0,
                     'text': 'Authored command help.', 'topics': ['sleep']}]
        sources = [('group.are', [{'keyword': 'SLEEP', 'level': -1, 'text': 'Other content.'},
                                 {'keyword': 'KICK SLEEP', 'level': -1, 'text': 'Kick text.'}])]
        result, additions = plan_import(original, sources)
        self.assertEqual(original, result[:1])
        self.assertEqual(['kick'], result[1]['topics'])
        self.assertEqual('Kick text.', result[1]['text'])
        self.assertEqual(1, len(additions))
        rerun, additions = plan_import(result, sources)
        self.assertEqual([], additions)
        self.assertEqual(result, rerun)
        self.assertEqual(1, len(original))

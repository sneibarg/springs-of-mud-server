import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from interp.Command import Command
from skill.Ability import Ability
from skill.Skill import Skill
from skill.Spell import Spell


def guard(predicate):
    return dict(predicate=predicate, channel='', message_key='', fallback='', token_factory='')


class GuardNormalizationTests(unittest.TestCase):
    def assert_loaders(self, raw, expected):
        for model in (Command, Skill, Spell):
            for as_json in (False, True):
                with self.subTest(model=model.__name__, as_json=as_json, guards=raw):
                    if model is Command:
                        document = dict(name='test', shortcuts='', role='player', position='standing',
                                        enabled=True, lambdas=[], function=[], usage='', level=0, maxArguments=0)
                    else:
                        document = dict(id='test', name='test', kind='skill', handlerId='', target='ignore',
                                        minPosition='standing', nounDamage='', levelByClass={}, ratingByClass={},
                                        slot=0, minMana=0, beats=0)
                    if raw is not OMITTED:
                        document['guards'] = deepcopy(raw)
                    source = deepcopy(document.get('guards'))
                    loaded = model.from_json(json.dumps(document) if as_json else document)
                    # Skill's existing loader passes its base payload through
                    # normalization again, filling defaults on string shorthand.
                    wanted = [dict(channel='', message_key='', fallback='', token_factory='', **entry)
                              if model is Skill and set(entry) == {'predicate'} else entry for entry in expected]
                    self.assertEqual(wanted, loaded.guards)
                    self.assertEqual(source, document.get('guards'))

    def test_omitted_and_non_list_containers_produce_no_guards(self):
        for raw in (OMITTED, None, '', 'lambda v: True', {}, {'predicate': 'test'}, 7, False):
            self.assert_loaders(raw, [])

    def test_string_shorthand_is_trimmed_and_blank_entries_are_skipped(self):
        self.assert_loaders(['  lambda v: True  ', '', ' \t ', 'lambda v: False'],
                            [{'predicate': 'lambda v: True'}, {'predicate': 'lambda v: False'}])

    def test_camel_case_fields_and_payload_message_keys_are_normalized(self):
        expected = dict(predicate='lambda v: True', channel='to_char', message_key='cannot_cast',
                        fallback=' Keep whitespace. ', token_factory='lambda v: {"n": 1}')
        self.assert_loaders([dict(predicate=' lambda v: True ', channel=' to_char ', messageKey=' cannotCast ',
                                 fallback=' Keep whitespace. ', tokenFactory=' lambda v: {"n": 1} ')], [expected])

    def test_snake_case_and_lambda_alias_keep_optional_defaults(self):
        self.assert_loaders([{'lambda': ' lambda v: True ', 'message_key': 'already_snake'},
                             {'predicate': 'lambda v: False'}],
                            [dict(predicate='lambda v: True', channel='', message_key='already_snake',
                                  fallback='', token_factory=''), guard('lambda v: False')])

    def test_null_optional_fields_and_unknown_fields(self):
        self.assert_loaders([dict(predicate='valid', channel=None, messageKey=None, fallback=None,
                                 tokenFactory=None, futureField='ignored')], [guard('valid')])

    def test_malformed_entries_are_skipped_without_discarding_valid_neighbors(self):
        self.assert_loaders([None, 2, False, [], {}, {'messageKey': 'noPredicate'},
                             {'predicate': '  '}, {'predicate': None, 'lambda': 'ignored'}, ' valid '],
                            [{'predicate': 'valid'}])

    def test_predicate_field_takes_precedence_over_lambda_alias(self):
        self.assert_loaders([{'predicate': 'primary', 'lambda': 'secondary'}], [guard('primary')])

    def test_normalizers_do_not_mutate_input_or_share_results(self):
        source = [{'predicate': ' valid ', 'messageKey': 'noTarget'}]
        before = deepcopy(source)
        for model in (Command, Ability):
            first = model._normalize_checks(source)
            first[0]['predicate'] = 'changed'
            second = model._normalize_checks(source)
            self.assertEqual('valid', second[0]['predicate'])
            self.assertEqual('no_target', second[0]['message_key'])
        self.assertEqual(before, source)


OMITTED = object()


if __name__ == '__main__':
    unittest.main()

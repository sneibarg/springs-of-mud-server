"""Authored spec_lookup outcomes and reviewed completion disposition."""
from spec_name_completion import NAMES, check_source

EDGE_CASES = (
    ('one-letter-first-match', 's', 'spec_breath_any'),
    ('common-prefix-first-match', 'spec_', 'spec_breath_any'),
    ('ambiguous-cast-first-adept', 'spec_cast', 'spec_cast_adept'),
    ('ambiguous-breath-f-first-fire', 'spec_breath_f', 'spec_breath_fire'),
    ('uppercase-last-match', 'SPEC_PATROLMAN', 'spec_patrolman'),
    ('same-first-letter-no-prefix', 'sz', 'C NULL'),
    ('longer-than-complete-name', 'spec_patrolman_extra', 'C NULL'),
    ('trailing-space-not-trimmed', 'spec_patrolman ', 'C NULL'),
    ('leading-space-not-trimmed', ' spec_patrolman', 'C NULL'),
    ('embedded-space-not-tokenized', 'spec patrolman', 'C NULL'),
    ('whitespace-only', ' ', 'C NULL'),
    ('nonascii-first-byte', '\u00e9', 'C NULL'),
)


def extend_cases(add, cases, source):
    check_source(source)
    for name in NAMES[1:-1]:
        add('special.c', 'spec_lookup', 'registered-' + name,
            {'arguments': {'name': name}}, {'return_function_pointer': name}, needle='LOWER(name[0])')
    for suffix, name, result in EDGE_CASES:
        add('special.c', 'spec_lookup', suffix, {'arguments': {'name': name}},
            {'return_function_pointer': result}, needle='LOWER(name[0])')
    for case in cases:
        if not case['id'].startswith('special.spec_lookup.'):
            continue
        name = case['fixture']['arguments']['name']
        result = case['expected']['return_function_pointer']
        k = None if result == 'C NULL' else NAMES.index(result)
        visited = list(range(22 if k is None else k + 1))
        calls = visited if name[:1] in ('s', 'S') else []
        case['entry'] = {
            'function': 'spec_lookup', 'route': 'Direct call; callers load_specials and do_string are separately audited.',
            'caller_prerequisites': 'Non-NULL, readable NUL-terminated byte string, immutable checkout table. No actor/world/trust or command-parser prerequisite. Non-ASCII fixture is byte 0xE9 followed by NUL, not UTF-8 encoding.',
            'return_domain': 'Registered SPEC_FUN pointer or C NULL; never invokes returned procedure.',
        }
        case['fixture']['table'] = {'entries_in_order': list(NAMES), 'sentinel_index': 22,
                                   'sentinel': {'name': 'C NULL', 'function': 'C NULL'}}
        case['controls'] = {
            'str_prefix': 'Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.',
            'LOWER': 'Actual merc.h macro folds A..Z only; no locale or Unicode normalization.',
            'randomness': 'None; no callback, allocator, clock or I/O.',
        }
        case['expected'].update({
            'loop_guard_indices_in_order': list(range(23 if k is None else k + 1)),
            'first_character_comparisons_in_order': visited,
            'str_prefix_table_indices_in_order': calls,
            'str_prefix_returns_in_order': [False if i == k else True for i in calls],
            'return_pointer_identity': 'C NULL' if k is None else f'spec_table[{k}].function',
            'unchanged': ['input bytes', 'table', 'all caller and world state'],
            'forbidden': ['compare sentinel name bytes', 'invoke returned procedure', 'messages', 'allocation/free', 'random draws', 'trim or tokenize input'],
        })
        case['source_refs'] = [{'file': 'src/special.c', 'function': 'spec_lookup', 'line': ln}
                               for ln in (103, 105, 106, 110 if k is None else 107)]
        if calls:
            case['source_refs'].append({'file': 'src/db.c', 'function': 'str_prefix', 'line': 3178})
        case['branch_ids'] = [case['id'] + '.path'] + [f'special.spec_lookup.{s}' for s in
            ('for.001', 'if.001', 'and.001', 'return.002' if k is None else 'return.001')]
        case['adaptation'] = {'Python': 'MobileHandler._special_library stores normalized designer names and behavior sequences. Use a symbolic registry fixture to test C prefix-selection semantics; do not assume Python implements them or execute any special.', 'approved_overrides': []}


def validate_cases(cases):
    selected = [c for c in cases if c['id'].startswith('special.spec_lookup.')]
    assert len(selected) == 37
    by_input = {c['fixture']['arguments']['name']: c for c in selected}
    for name in NAMES:
        assert by_input[name]['expected']['return_function_pointer'] == name
    for _, name, result in EDGE_CASES:
        assert by_input[name]['expected']['return_function_pointer'] == result
    for case in selected:
        assert case['status'] == 'specified' and not case['open_questions']
        name = case['fixture']['arguments']['name']
        expected = case['expected']
        result = expected['return_function_pointer']
        k = None if result == 'C NULL' else NAMES.index(result)
        visited = list(range(22 if k is None else k + 1))
        assert expected['loop_guard_indices_in_order'] == list(range(23 if k is None else k + 1))
        assert expected['first_character_comparisons_in_order'] == visited
        calls = visited if name[:1] in ('s', 'S') else []
        assert expected['str_prefix_table_indices_in_order'] == calls
        assert expected['str_prefix_returns_in_order'] == [False if i == k else True for i in calls]
    return len(selected)


def complete(functions, cases, source):
    check_source(source)
    count = validate_cases(cases)
    fn = next(f for f in functions if (f['file'], f['name']) == ('src/special.c', 'spec_lookup'))
    assert {(r['file'], r['line']) for r in fn['entry_routes']} == {
        ('src/act_wiz.c', 3792), ('src/db.c', 1081), ('src/merc.h', 2304)}
    assert all(b['disposition'] == 'specified' and b['case_ids'] for b in fn['branch_ledger'])
    fn.pop('local_ledger_review', None)
    fn['status'] = 'traced'
    fn['completion_review'] = {
        'status': 'complete', 'evidence': 'static_trace', 'case_count': count,
        'notes': 'spec-lookup-completion.md',
        'coverage': 'All 22 full names; first/interior/last matches; ambiguous prefixes; ASCII case; first-character short circuit; failed prefix continuation; empty/missing/longer/whitespace/non-ASCII input; sentinel termination; no side effects.',
        'entry_contract': 'Non-NULL readable NUL-terminated bytes. No inherited command authorization.',
        'dependencies': ['Immutable spec_table at special.c:69', 'LOWER at merc.h:1799: ASCII arithmetic only', 'str_prefix at db.c:3164: traced mismatch/terminator paths; its NULL logging guards are unreachable under this entry contract and table invariant.'],
        'entry_routes': [
            {'file': 'src/db.c', 'line': 1081, 'caller': 'load_specials', 'disposition': 'reviewed', 'contract': 'Boot SPECIALS M records pass fread_word output. Assign lookup result first; NULL logs prototype vnum and exits(1). Successful pointer retained on prototype.'},
            {'file': 'src/act_wiz.c', 'line': 3792, 'caller': 'do_string', 'disposition': 'reviewed', 'contract': 'Required fields, character/mobile type and victim lookup precede zone=NULL; spec branch requires NPC. Raw remaining argument after smash_tilde is passed. Assignment precedes failure message, clearing existing spec_fun on miss.'},
            {'file': 'src/interp.c', 'line': 338, 'caller': 'interpret', 'disposition': 'reviewed', 'contract': 'string command requires L5=55 trust and POS_DEAD, LOG_ALWAYS; freeze gate applies. Direct/internal calls do not inherit interpreter authorization.'},
            {'file': 'src/merc.h', 'line': 2304, 'disposition': 'declaration_only'},
        ],
        'bounded_loop_dispositions': {
            'zero_iterations': 'Unreachable: first table name is non-NULL.',
            'one_or_multiple': 'First/full/prefix returns and every interior/last full name are specified.',
            'all_miss': 'All 22 rows visited, sentinel stops before name[0] access.',
            'mutation_recursion': 'No writes, callbacks or recursion; table immutable.',
        },
        'limitations': ['NULL or invalid input storage violates entry precondition; name[0] is read before str_prefix can validate NULL. No portable failure result is asserted.', 'ASCII macro semantics are not Unicode case folding.'],
        'remaining_gaps': [],
    }

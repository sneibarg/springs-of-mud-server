"""Reviewed, finite spec_name contract. Expectations are authored, not inferred."""
import hashlib
import re

NAMES = (
    'spec_breath_any', 'spec_breath_acid', 'spec_breath_fire',
    'spec_breath_frost', 'spec_breath_gas', 'spec_breath_lightning',
    'spec_cast_adept', 'spec_cast_cleric', 'spec_cast_judge', 'spec_cast_mage',
    'spec_cast_undead', 'spec_executioner', 'spec_fido', 'spec_guard',
    'spec_janitor', 'spec_mayor', 'spec_poison', 'spec_thief', 'spec_nasty',
    'spec_troll_member', 'spec_ogre_member', 'spec_patrolman',
)
SOURCE_HASH = '78e00c637522c18be0626547577cfa6ddcee0ac68206772d3c0409f361cdd2b6'


def check_source(source):
    raw = (source / 'src/special.c').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_HASH, 'Re-review spec_name before retaining its completed disposition.'
    text = raw.decode('latin1')
    table = text.split('spec_table[] =', 1)[1].split('};', 1)[0]
    assert re.findall(r'\{\s*"([^"]+)"\s*,\s*(\w+)\s*\}', table) == [(n, n) for n in NAMES]
    assert re.search(r'\{\s*NULL\s*,\s*NULL\s*\}\s*$', table.strip())


def extend_cases(add, cases, source):
    check_source(source)
    for name in NAMES[1:-1]:
        add('special.c', 'spec_name', 'registered-' + name,
            {'arguments': {'function': name}}, {'returned_name': name}, needle='function == spec_table')
    for case in cases:
        if not case['id'].startswith('special.spec_name.'):
            continue
        name = case['expected']['returned_name']
        match = None if name == 'C NULL' else NAMES.index(name)
        case['entry'] = {
            'route': 'Direct spec_name(SPEC_FUN *function); also called by do_mstat at act_wiz.c:1703.',
            'function': 'spec_name',
            'caller_prerequisites': 'A valid compatible function pointer or C NULL. The immutable checkout table is intact. No actor, trust, room, descriptor, world or special-procedure invocation is needed.',
            'return_domain': 'Borrowed table name pointer, or C NULL. Never a newly allocated string.',
        }
        case['fixture']['table'] = {'entries_in_order': list(NAMES), 'sentinel_index': 22,
                                   'sentinel': {'name': 'C NULL', 'function': 'C NULL'}}
        case['fixture']['identity_contract'] = 'Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table.'
        case['controls'] = {'collaborators': 'None: execute the real function and immutable table.',
                            'randomness': 'None; no RNG, clock, allocator, I/O or callback is invoked.'}
        case['expected'].update({
            'return_pointer': 'C NULL' if match is None else f'spec_table[{match}].name (same pointer, not a copy)',
            'equality_comparisons_in_order': list(range(22 if match is None else match + 1)),
            'loop_guard_indices_in_order': list(range(23 if match is None else match + 1)),
            'sentinel_function_compared_to_argument': False,
            'unchanged': ['table', 'all names', 'all caller and world state'],
            'forbidden': ['invoke input function', 'invoke any table function', 'allocation/free', 'messages to any recipient', 'random draws', 'read beyond sentinel'],
        })
        case['source_refs'] = [{'file': 'src/special.c', 'function': 'spec_name', 'line': ln}
                               for ln in (117, 119, 120 if match is not None else 123)]
        case['branch_ids'] = [case['id'] + '.path'] + [f'special.spec_name.{site}' for site in
            ('for.001', 'if.001', 'return.002' if match is None else 'return.001')]
        case['adaptation'] = {'Python': 'Mobile.special_name already stores the neutral identity; assert names/absence at a metadata boundary, without executing MobileHandler special behavior. No reverse callable lookup API is assumed.',
                              'approved_overrides': []}


def complete(functions, cases, source):
    check_source(source)
    fn = next(f for f in functions if (f['file'], f['name']) == ('src/special.c', 'spec_name'))
    selected = [c for c in cases if c['id'].startswith('special.spec_name.')]
    assert len(selected) == 24
    assert all(c['status'] == 'specified' and not c['open_questions'] for c in selected)
    assert {c['expected']['returned_name'] for c in selected} == set(NAMES) | {'C NULL'}
    assert all(b['disposition'] == 'specified' and b['case_ids'] for b in fn['branch_ledger'])
    # Entry references were inspected, not merely accepted from the lexical scanner.
    assert {(r['file'], r['line']) for r in fn['entry_routes']} == {('src/act_wiz.c', 1703), ('src/merc.h', 2305)}
    fn.pop('local_ledger_review', None)
    fn['status'] = 'traced'
    fn['completion_review'] = {
        'status': 'complete', 'evidence': 'static_trace', 'case_count': 24,
        'notes': 'spec-name-completion.md',
        'coverage': 'All 22 immutable table mappings, first/interior/last return, all-miss termination, NULL input, compatible nonmember input, sentinel exclusion, borrowed pointer identity, absence of side effects.',
        'entry_contract': 'Any valid SPEC_FUN pointer or C NULL; no inherited authorization or world-state prerequisite.',
        'dependencies': ['spec_table: 22 distinct registered functions followed by {NULL,NULL}; no callees or conditionally compiled alternatives in this function/table.'],
        'entry_routes': [
            {'file': 'src/act_wiz.c', 'line': 1700, 'caller': 'do_mstat', 'disposition': 'reviewed',
             'guard': 'Victim found; diagnostic output reaches NPC && spec_fun != 0. No membership check. Helper return is formatted then sent to inspecting actor.'},
            {'file': 'src/act_wiz.c', 'line': 1071, 'caller': 'do_stat', 'disposition': 'reviewed',
             'route': 'stat mob/char dispatches do_mstat through do_function; generic stat prefers object lookup, then character lookup at line 1087.'},
            {'file': 'src/interp.c', 'line': 337, 'caller': 'interpret', 'disposition': 'reviewed',
             'route': 'stat command requires trust >= IM=52 and POS_DEAD; frozen PC rejected earlier. No separate mstat command table entry. Internal do_function bypasses interpreter gates.'},
            {'file': 'src/merc.h', 'line': 2305, 'disposition': 'declaration_only'},
        ],
        'bounded_loop_dispositions': {
            'zero_iterations': 'Unreachable for the immutable checkout table: entry zero is non-null.',
            'one_iteration': 'first-function returns at entry zero.',
            'multiple_iterations': 'Every interior/last entry specified; missing/NULL inputs compare all 22 and stop before comparing sentinel.',
            'duplicate_pointer_first_match': 'Table has no duplicate functions; mutation of the const table is not a defined alternative. The source returns immediately on first equality.',
            'recursion_reentry': 'No recursion, callbacks or mutable static state.'},
        'remaining_gaps': [],
        'caller_limitation': 'A forged but valid unregistered procedure passes do_mstat non-null guard; spec_name returns NULL and caller sprintf %s has no portable outcome. This does not make the helper result ambiguous or mark do_mstat complete.',
    }

"""Finite clan-table contract and caller audit for is_same_clan."""
import hashlib

HASHES = {
    'src/handler.c': '0e95a3bd6480448855bba8d7cae6b6f8b5aad3d2be2738a21cd58571f7bf2261',
    'src/tables.c': 'ee69d8e2e1a7f78420f3f48c652fccd6db32d5c761eca17dad2ff56c720b6e33',
}
MATRIX = ((False, False, False), (False, False, False), (False, False, True))


def check_source(source):
    for path, digest in HASHES.items():
        assert hashlib.sha256((source / path).read_bytes()).hexdigest() == digest, path


def extend_cases(add, cases, source):
    check_source(source)
    original = {(0, 0), (1, 1), (2, 2), (2, 1)}
    for a in range(3):
        for b in range(3):
            if (a, b) not in original:
                add('handler.c', 'is_same_clan', f'clans-{a}-{b}',
                    {'actor': {'clan': a}, 'victim': {'clan': b}}, {'return': MATRIX[a][b]}, needle='independent')
    for clan in range(3):
        add('handler.c', 'is_same_clan', f'self-clan-{clan}',
            {'actor': {'id': 'ch', 'clan': clan}, 'victim': {'same_entity_as': 'ch'}},
            {'return': clan == 2}, needle='independent')
    for a, b in [('NPC', 'PC'), ('PC', 'NPC'), ('NPC', 'NPC')]:
        add('handler.c', 'is_same_clan', f'kinds-{a.lower()}-{b.lower()}',
            {'actor': {'clan': 2, 'kind': a}, 'victim': {'clan': 2, 'kind': b}},
            {'return': True}, needle='independent')
    for clan in (0, 1):
        add('handler.c', 'is_same_clan', f'independent-{clan}-null-victim',
            {'actor': {'clan': clan}, 'victim': {'C_NULL': True}}, {'return': False}, needle='independent')
    for clan in (-1, 3):
        add('handler.c', 'is_same_clan', f'victim-clan-outside-table-{clan}',
            {'actor': {'clan': 2}, 'victim': {'clan': clan}}, {'return': False}, needle='return (ch->clan')
    for case in cases:
        if not case['id'].startswith('handler.is_same_clan.'):
            continue
        independent = case['fixture']['actor']['clan'] in (0, 1)
        case['fixture']['actor'].setdefault('kind', 'PC')
        if 'clan' in case['fixture']['victim']:
            case['fixture']['victim'].setdefault('kind', 'PC')
        case['fixture']['table'] = {'MAX_CLAN': 3, 'rows': [
            {'index': 0, 'name': '', 'independent': True},
            {'index': 1, 'name': 'loner', 'independent': True},
            {'index': 2, 'name': 'rom', 'independent': False}]}
        case['entry'] = {'function': 'is_same_clan', 'route': 'Direct helper call; caller guards are not inherited.',
                         'caller_prerequisites': 'Readable actor with clan index 0..2. Victim must be readable only when actor clan is 2; its clan is compared as an integer, never used as a table index.',
                         'return_domain': 'C Boolean; not an ownership or authorization operation.'}
        case['controls'] = {'collaborators': 'None. Read the real immutable clan table.', 'randomness': 'None.'}
        case['expected'].update({'ordered_reads': ['actor.clan', 'clan_table[actor.clan].independent'] +
                               ([] if independent else ['compare actor.clan and victim.clan; operand read order unspecified']),
                                'victim_read': not independent, 'unchanged': ['all entities and table'],
                                'forbidden': ['messages', 'random draws', 'allocation', 'clan mutation', 'trust or kind checks'] +
                                (['dereference victim'] if independent else [])})
        case['branch_ids'] = [case['id'] + '.path', 'handler.is_same_clan.if.001',
                              'handler.is_same_clan.return.001' if independent else 'handler.is_same_clan.return.002']
        case['source_refs'] = [{'file': 'src/handler.c', 'function': 'is_same_clan', 'line': ln}
                               for ln in (335, 336 if independent else 338)]
        case['adaptation'] = {'Python': 'Use guild metadata in CharacterApi.is_clan as the membership boundary, but keep independent-clan rejection explicit. No same-clan Python helper was found; no parity or runtime change is claimed.', 'approved_overrides': []}


def validate_cases(cases):
    selected = [c for c in cases if c['id'].startswith('handler.is_same_clan.')]
    assert len(selected) == 19
    by_id = {c['id']: c for c in selected}
    for a in range(3):
        for b in range(3):
            assert by_id[f'handler.is_same_clan.clans-{a}-{b}']['expected']['return'] is MATRIX[a][b]
    for case in selected:
        a, victim = case['fixture']['actor']['clan'], case['fixture']['victim']
        expected = False if a in (0, 1) else (a == (a if 'same_entity_as' in victim else victim['clan']))
        assert case['status'] == 'specified' and not case['open_questions']
        assert case['expected']['return'] is expected
        assert case['expected']['victim_read'] is (a == 2)
    return len(selected)


def complete(functions, cases, source):
    check_source(source)
    count = validate_cases(cases)
    fn = next(f for f in functions if (f['file'], f['name']) == ('src/handler.c', 'is_same_clan'))
    assert {(r['file'], r['line']) for r in fn['entry_routes']} == {
        ('src/act_comm.c', 697), ('src/fight.c', 898), ('src/magic.c', 2898),
        ('src/magic2.c', 74), ('src/magic2.c', 127), ('src/merc.h', 2200)}
    assert all(b['disposition'] == 'specified' and b['case_ids'] for b in fn['branch_ledger'])
    fn.pop('local_ledger_review', None)
    fn['status'] = 'traced'
    fn['completion_review'] = {
        'status': 'complete', 'evidence': 'static_trace', 'case_count': count,
        'notes': 'same-clan-completion.md', 'remaining_gaps': [],
        'coverage': 'Complete 3x3 clan matrix, self identity, NPC/PC combinations, independent actor skips NULL victim, victim clan is not a table index.',
        'dependencies': ['clan_table[3] in tables.c:42; no callees, macros, randomness or conditional compilation in helper.'],
        'entry_routes': [
            {'file': 'src/act_comm.c', 'line': 697, 'caller': 'do_clantalk', 'disposition': 'reviewed', 'contract': 'Sender must be nonindependent clan member, sending nonempty input with channels enabled. Recipient descriptor playing and not sender; later NOCLAN/QUIET checks further restrict delivery.'},
            {'file': 'src/fight.c', 'line': 898, 'caller': 'damage', 'disposition': 'reviewed', 'contract': 'After raw_kill; only distinct attacker and non-NPC attacker reach comparison. False removes victim KILLER if present, otherwise THIEF. Helper reads then-current clan fields, not pre-death snapshots.'},
            {'file': 'src/magic.c', 'line': 2898, 'caller': 'spell_gate', 'disposition': 'reviewed', 'contract': 'Nonzero victim clan enables comparison after earlier travel guards; false fails before later hero/NPC saving guards and movement.'},
            {'file': 'src/magic2.c', 'line': 74, 'caller': 'spell_portal', 'disposition': 'reviewed', 'contract': 'Final travel guard checks nonzero victim clan and helper; false fails before component lookup/consumption.'},
            {'file': 'src/magic2.c', 'line': 127, 'caller': 'spell_nexus', 'disposition': 'reviewed', 'contract': 'Same final clan guard after destination/origin visibility, room, level and NPC save guards; false fails before component lookup/consumption.'},
            {'file': 'src/merc.h', 'line': 2200, 'disposition': 'declaration_only'},
        ],
        'limitations': ['Actor NULL/out-of-table actor clan, or NULL victim when actor clan is 2, violates the read preconditions; no portable result.', 'Full caller behavior and lifecycle remain independent report items.'],
    }

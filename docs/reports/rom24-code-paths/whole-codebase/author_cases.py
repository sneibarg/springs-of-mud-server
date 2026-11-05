"""Explicitly authored behavioral cases. Parameter rows are concrete, not placeholders."""
import json
from build_report import OUT, SOURCE, inventory, ref

_, functions = inventory()
index = {(f['file'], f['name']): f for f in functions}
cases = []


def add(file, fn, suffix, fixture, expected, needle=None, controls=None, action=None, questions=None, blocked=False):
    file = 'src/' + file
    f = index[file, fn]
    lines = (SOURCE / file).read_text(encoding='latin1').splitlines()
    ln = f['line']
    if needle:
        ln = next(i + 1 for i in range(f['line'] - 1, f['end_line']) if needle in lines[i])
    cid = f'{file[4:-2]}.{fn}.{suffix}'
    cases.append({'id': cid, 'title': suffix.replace('-', ' '), 'status': 'blocked' if blocked else 'specified',
        'branch_ids': [cid + '.path'], 'source_refs': [ref(file, fn, ln)],
        'entry': {'route': 'direct function call', 'function': fn,
                  'caller_prerequisites': 'Valid pointers, NUL-terminated strings, sufficient buffers and consistent linked lists unless explicitly overridden. Direct call does not imply interpreter authorization.',
                  'return_domain': 'C function return, with void represented by completion'},
        'fixture': fixture,
        'controls': controls or {'randomness': 'No random calls on this path.', 'collaborators': 'Record output and mutations; no actor/target state beyond the specified dependency contract affects this path.'},
        'action': action or f'Invoke {fn} with the fixture arguments once.',
        'expected': expected, 'evidence': 'static_trace', 'open_questions': questions or []})


# String utilities: inverted comparison semantics and C division.
for fn, rows in {
    'str_cmp': [('empty-equal', '', '', False), ('ascii-case-equal', 'ROM', 'rom', False), ('first-mismatch', 'cat', 'bat', True), ('left-shorter', 'ca', 'cat', True), ('right-shorter', 'cat', 'ca', True)],
    'str_prefix': [('empty-prefix', '', 'rom', False), ('both-empty', '', '', False), ('ascii-case-prefix', 'RO', 'rom', False), ('equal', 'rom', 'ROM', False), ('longer-than-candidate', 'roms', 'rom', True), ('first-mismatch', 'x', 'rom', True)],
    'str_infix': [('empty-needle', '', 'rom', False), ('longer-needle', 'roms', 'rom', True), ('interior-case-insensitive', 'OM', 'romance', False), ('end-match', 'ce', 'romance', False), ('no-match', 'zz', 'romance', True)],
    'str_suffix': [('empty-suffix', '', 'rom', False), ('case-suffix', 'OM', 'rom', False), ('equal', 'ROM', 'rom', False), ('longer', 'room', 'rom', True), ('wrong-suffix', 'ro', 'rom', True)],
}.items():
    for suffix, a, b, result in rows:
        add('db.c', fn, suffix, {'arguments': {'astr': a, 'bstr': b}}, {'return': result, 'unchanged': ['both input strings'], 'forbidden': ['messages', 'random draws']})
for fn, label in [('str_cmp', 'Str_cmp'), ('str_prefix', 'Strn_cmp')]:
    for suffix, a, b, msg in [('null-left', None, 'x', 'astr'), ('null-right', 'x', None, 'bstr'), ('both-null-left-dominates', None, None, 'astr')]:
        add('db.c', fn, suffix, {'arguments': {'astr': {'C_NULL': True} if a is None else a, 'bstr': {'C_NULL': True} if b is None else b}},
            {'return': True, 'ordered_events': [{'call': 'bug', 'arguments': [f'{label}: null {msg}.', 0]}], 'forbidden': ['dereference NULL', 'second bug call']},
            needle='astr == NULL' if a is None else 'bstr == NULL', controls={'bug': 'Recording collaborator; logging internals are outside this helper-boundary case.', 'randomness': 'none'})
for suffix, value, result in [('empty', '', ''), ('no-tilde', 'abc', 'abc'), ('one', 'a~b', 'a-b'), ('multiple', '~~a~', '--a-')]:
    add('db.c', 'smash_tilde', suffix, {'arguments': {'str': value}}, {'return': 'void', 'resulting_string': result, 'forbidden': ['allocation', 'messages']}, needle="*str == '~'")
for suffix, value, result in [('empty', '', ''), ('mixed', 'hELLO ROM', 'Hello rom'), ('nonletter-first', '1ROM', '1rom')]:
    add('db.c', 'capitalize', suffix, {'arguments': {'str': value}}, {'result_string': result, 'unchanged': ['input string'], 'storage': 'Shared static buffer, not a fresh caller-owned allocation.'}, needle='strcap[0]')
for suffix, level, low, high, result in [('zero', 0, 10, 42, 10), ('endpoint', 32, 10, 42, 42), ('positive-fraction', 1, 10, 11, 10), ('negative-fraction-truncates-to-zero', 1, 10, 9, 10), ('negative-level', -1, 10, 11, 10), ('extrapolates', 64, 10, 42, 74)]:
    add('db.c', 'interpolate', suffix, {'arguments': {'level': level, 'value_00': low, 'value_32': high}}, {'return': result, 'arithmetic': 'Signed integer division truncates toward zero; no clamping.'}, needle='return value_00')

# one_argument consumes only literal spaces as the unquoted delimiter, then skips isspace.
for suffix, text, token, rest in [('empty', '', '', ''), ('leading-spaces', '  LOOK  North', 'look', 'North'), ('single-quotes', "'Two Words' tail", 'two words', 'tail'), ('double-quotes', '"Two Words" tail', 'two words', 'tail'), ('unclosed-quote', "'Two Words", 'two words', ''), ('empty-quoted-token', "'' tail", '', 'tail'), ('embedded-tab', 'look\tnorth rest', 'look\tnorth', 'rest'), ('trailing-whitespace', 'look \t\n north', 'look', 'north')]:
    add('interp.c', 'one_argument', suffix, {'arguments': {'argument': text, 'arg_first': 'writable output array of at least 256 bytes'}, 'locale': 'C/ASCII for isspace and LOWER'},
        {'output_token': token, 'returned_remainder': rest, 'unchanged': ['input bytes'], 'forbidden': ['messages', 'randomness']}, needle="cEnd = ' '")

# Table lookups: concrete checkout values, first ambiguous match wins.
for fn, rows in {
    'position_lookup': [('standing-full', 'standing', 8), ('ambiguous-s-first-stunned', 's', 3), ('case-insensitive', 'SLEEP', 4), ('empty', '', -1), ('missing', 'z', -1), ('longer', 'standings', -1)],
    'sex_lookup': [('none', 'n', 0), ('male', 'M', 1), ('female', 'fem', 2), ('last-entry', 'either', 3), ('empty', '', -1), ('missing', 'z', -1)],
    'size_lookup': [('tiny', 't', 0), ('small', 'SM', 1), ('medium', 'm', 2), ('large', 'l', 3), ('huge', 'h', 4), ('last-entry', 'g', 5), ('empty', '', -1), ('missing', 'z', -1)],
    'clan_lookup': [('loner', 'L', 1), ('rom', 'ro', 2), ('empty-matches-entry-zero', '', 0), ('unknown-indistinguishable-from-zero', 'z', 0)],
}.items():
    for suffix, name, result in rows:
        add('lookup.c', fn, suffix, {'arguments': {'name': name}, 'table': 'Unmodified src/tables.c for this snapshot.'},
            {'return': result, 'lookup': 'ASCII case-insensitive prefix; source table order determines first match.', 'forbidden': ['messages', 'mutation']}, needle='LOWER(name[0])')
for suffix, name, table, result in [
    ('empty-table', 'a', [], 0), ('first-of-multiple-prefixes', 'al', [['alpha', 2, False], ['alpine', 4, True]], 2),
    ('case-insensitive', 'ALP', [['alpha', 2, False]], 2), ('nonsettable-still-found', 'alpha', [['alpha', 2, False]], 2),
    ('skip-nonmatch', 'b', [['alpha', 2, True], ['beta', 4, True]], 4), ('unknown', 'z', [['alpha', 2, True]], 0),
    ('empty-name-does-not-match-nonempty', '', [['alpha', 2, True]], 0)]:
    add('lookup.c', 'flag_lookup', suffix, {'arguments': {'name': name, 'flag_table': table}, 'table_contract': 'Each row is [name,bit,settable], followed by a name=C NULL sentinel.'}, {'return': result, 'unchanged': ['table'], 'forbidden': ['messages']}, needle='LOWER(name[0])')

# Random adapters are tested with scripted underlying draws, never with a statistical pass criterion.
for suffix, lo, hi, draws, result in [('both-zero', 0, 0, [], 0), ('equal', 7, 7, [], 7), ('reversed', 9, 4, [], 9), ('lower-end', 10, 12, [0], 10), ('upper-end', 10, 12, [2], 12), ('reject-equality-then-accept', 10, 12, [3, 1], 11), ('multiple-rejections', 10, 14, [7, 5, 4], 14), ('negative-domain', -2, 0, [2], 0)]:
    add('db.c', 'number_range', suffix, {'arguments': {'from': lo, 'to': hi}}, {'return': result, 'number_mm_calls': len(draws), 'ordered_consumed_draws': draws}, needle='to = to - from + 1', controls={'number_mm': {'kind': 'stubbed entropy boundary', 'ordered_returns': draws}, 'other_random_calls': 'forbidden'})
for fn, rows in {'number_percent': [('lower', [0], 1), ('upper', [99], 100), ('reject-100', [100, 99], 100), ('reject-127', [127, 0], 1), ('mask-before-test', [128], 1)], 'number_door': [('lower', [0], 0), ('upper', [5], 5), ('reject-six-seven', [6, 7, 2], 2), ('mask-before-test', [8], 0)]}.items():
    for suffix, draws, result in rows:
        add('db.c', fn, suffix, {'arguments': {}}, {'return': result, 'number_mm_calls': len(draws), 'ordered_consumed_draws': draws}, needle='while', controls={'number_mm': {'kind': 'stubbed entropy boundary', 'ordered_returns': draws}})
for width, raw, result in [(0, 255, 0), (1, 2, 0), (2, 7, 3), (3, 5, 5)]:
    add('db.c', 'number_bits', f'width-{width}-raw-{raw}', {'arguments': {'width': width}}, {'return': result, 'number_mm_calls': 1}, needle='return number_mm', controls={'number_mm': {'ordered_returns': [raw], 'kind': 'stubbed entropy boundary'}})
for number, bit, result in [(10, 0, 9), (10, 1, 10), (10, 2, 10), (10, 3, 11), (1, 0, 1), (0, 3, 1), (-2, 1, 1)]:
    add('db.c', 'number_fuzzy', f'number-{number}-bits-{bit}', {'arguments': {'number': number}}, {'return': result, 'number_bits_calls': [{'width': 2}]}, needle='switch', controls={'number_bits': {'kind': 'stubbed helper boundary; bit masking separately specified', 'ordered_returns': [bit]}})
for suffix, number, size, draws, result in [('size-zero', 5, 0, [], 0), ('size-one', 5, 1, [], 5), ('size-one-negative-count-quirk', -2, 1, [], -2), ('zero-dice', 0, 6, [], 0), ('negative-count', -2, 6, [], 0), ('one-die', 1, 6, [6], 6), ('multiple', 3, 6, [1, 6, 3], 10)]:
    add('db.c', 'dice', suffix, {'arguments': {'number': number, 'size': size}}, {'return': result, 'ordered_number_range_calls': [{'from': 1, 'to': size, 'returns': n} for n in draws]}, needle='switch', controls={'number_range': {'kind': 'stubbed helper boundary; separately specified', 'ordered_returns': draws}})

# Trust, darkness and room privacy are dependency contracts used by scan and travel.
for suffix, actor, result in [('pc-level', {'kind': 'PC', 'level': 30, 'trust': 0, 'desc': None}, 30), ('explicit-trust', {'kind': 'PC', 'level': 10, 'trust': 55, 'desc': None}, 55), ('npc-below-hero', {'kind': 'NPC', 'level': 50, 'trust': 0, 'desc': None}, 50), ('npc-at-hero-capped', {'kind': 'NPC', 'level': 51, 'trust': 0, 'desc': None}, 50), ('npc-above-hero-capped', {'kind': 'NPC', 'level': 60, 'trust': 0, 'desc': None}, 50), ('npc-explicit-trust-before-cap', {'kind': 'NPC', 'level': 60, 'trust': 58, 'desc': None}, 58), ('switched-original-controls', {'kind': 'NPC', 'level': 60, 'trust': 58, 'desc': {'original': {'kind': 'PC', 'level': 20, 'trust': 0}}}, 20)]:
    add('handler.c', 'get_trust', suffix, {'actor': actor, 'constants': {'LEVEL_HERO': 51}}, {'return': result, 'unchanged': ['actor and descriptor']}, needle='ch->desc != NULL')
for suffix, light, flags, sector, sun, result in [('positive-light-beats-dark', 1, ['ROOM_DARK'], 'SECT_FIELD', 'SUN_DARK', False), ('zero-light-dark-flag', 0, ['ROOM_DARK'], 'SECT_CITY', 'SUN_LIGHT', True), ('negative-light-dark-flag', -1, ['ROOM_DARK'], 'SECT_INSIDE', 'SUN_LIGHT', True), ('inside-at-night', 0, [], 'SECT_INSIDE', 'SUN_DARK', False), ('city-at-night', 0, [], 'SECT_CITY', 'SUN_DARK', False), ('field-at-sunset', 0, [], 'SECT_FIELD', 'SUN_SET', True), ('field-at-night', 0, [], 'SECT_FIELD', 'SUN_DARK', True), ('field-day', 0, [], 'SECT_FIELD', 'SUN_LIGHT', False), ('field-sunrise', 0, [], 'SECT_FIELD', 'SUN_RISE', False)]:
    add('handler.c', 'room_is_dark', suffix, {'room': {'light': light, 'room_flags': flags, 'sector_type': sector}, 'weather_info': {'sunlight': sun}}, {'return': result, 'unchanged': ['room and weather']}, needle='light > 0')
for suffix, owner, flags, count, result in [('owned-empty', 'Alice', [], 0, True), ('null-owner-empty', None, [], 0, False), ('empty-owner-empty', '', [], 0, False), ('private-one', '', ['ROOM_PRIVATE'], 1, False), ('private-two', '', ['ROOM_PRIVATE'], 2, True), ('private-three', '', ['ROOM_PRIVATE'], 3, True), ('solitary-zero', '', ['ROOM_SOLITARY'], 0, False), ('solitary-one', '', ['ROOM_SOLITARY'], 1, True), ('imp-empty', '', ['ROOM_IMP_ONLY'], 0, True), ('public-many', '', [], 3, False)]:
    add('handler.c', 'room_is_private', suffix, {'room': {'owner': {'C_NULL': True} if owner is None else owner, 'room_flags': flags, 'people': [{'id': f'p{i}', 'kind': 'NPC' if i % 2 else 'PC'} for i in range(count)]}}, {'return': result, 'unchanged': ['all room occupants and room']}, needle='owner != NULL')
for clan in [0, 1, 2]:
    add('handler.c', 'is_clan', f'clan-{clan}', {'actor': {'clan': clan}}, {'return_raw': clan, 'truth_value': bool(clan)}, needle='return ch->clan')
for a, b, result in [(0, 0, False), (1, 1, False), (2, 2, True), (2, 1, False)]:
    add('handler.c', 'is_same_clan', f'clans-{a}-{b}', {'actor': {'clan': a}, 'victim': {'clan': b}, 'table': 'src/tables.c clans 0 and 1 independent, 2 not independent'}, {'return': result}, needle='independent')

# Flags: each case calls the helper directly, so the command's trust guard is not implied.
base_flag = {'actor': {'id': 'admin', 'kind': 'PC'}, 'victim': {'id': 'bob', 'kind': 'NPC', 'act': ['ACT_IS_NPC', 'ACT_SENTINEL'], 'zone': 'zone-A'}, 'lookup': 'get_char_world returns bob for bob', 'flags': 'src/tables.c; symbolic A=1 B=2 C=4'}
for suffix, arg, msg in [('no-arguments', '', 'Syntax:\n\r'), ('missing-target', 'mob', 'What do you wish to set flags on?\n\r'), ('missing-field', 'mob bob', 'You need to specify a flag to set.\n\r'), ('missing-flags', 'mob bob act', 'Which flags do you wish to change?\n\r')]:
    expected = {'return': 'void', 'first_message': {'recipient': 'admin', 'text': msg}, 'unchanged': ['victim flags', 'victim zone'], 'forbidden': ['world lookup', 'flag mutation']}
    if not arg:
        expected['remaining_messages'] = ['  flag mob  <name> <field> <flags>\n\r', '  flag char <name> <field> <flags>\n\r', '  mob  flags: act,aff,off,imm,res,vuln,form,part\n\r', '  char flags: plr,comm,aff,imm,res,vuln,\n\r', '  +: add flag, -: remove flag, = set equal to\n\r', '  otherwise flag toggles the flags listed.\n\r']
    add('flags.c', 'do_flag', suffix, {**base_flag, 'argument': arg}, expected, needle="arg1[0] == '\\0'")
for suffix, arg, kind, msg in [('missing-world-target', 'mob missing act sentinel', 'NPC', "You can't find them.\n\r"), ('act-on-pc', 'mob bob act sentinel', 'PC', 'Use plr for PCs.\n\r'), ('plr-on-npc', 'char bob plr permit', 'NPC', 'Use act for NPCs.\n\r'), ('form-on-pc', 'char bob form animal', 'PC', "Form can't be set on PCs.\n\r"), ('parts-on-pc', 'char bob parts head', 'PC', "Parts can't be set on PCs.\n\r"), ('comm-on-npc', 'mob bob comm quiet', 'NPC', "Comm can't be set on NPCs.\n\r"), ('unsupported-off-field', 'mob bob off bash', 'NPC', "That's not an acceptable flag.\n\r")]:
    add('flags.c', 'do_flag', suffix, {**base_flag, 'argument': arg, 'victim': {**base_flag['victim'], 'kind': kind, 'act': ['ACT_IS_NPC'] if kind == 'NPC' else []}},
        {'return': 'void', 'messages': [{'recipient': 'admin', 'text': msg}], 'unchanged': ['victim flags', 'victim zone']}, needle='victim = get_char_world', controls={'get_char_world': {'kind': 'stubbed world-lookup boundary', 'returns': 'C NULL' if suffix == 'missing-world-target' else 'bob'}, 'randomness': 'none'})
for suffix, arg, act, zone, msg in [('unknown-type-silent', 'object bob act sentinel', ['ACT_IS_NPC', 'ACT_SENTINEL'], 'zone-A', None), ('invalid-word-clears-zone', 'mob bob act + nosuchflag', ['ACT_IS_NPC', 'ACT_SENTINEL'], None, "That flag doesn't exist!\n\r"), ('valid-then-invalid-atomic-flags', 'mob bob act + scavenger nosuchflag', ['ACT_IS_NPC', 'ACT_SENTINEL'], None, "That flag doesn't exist!\n\r"), ('add', 'mob bob act + scavenger', ['ACT_IS_NPC', 'ACT_SENTINEL', 'ACT_SCAVENGER'], None, None), ('remove', 'mob bob act - sentinel', ['ACT_IS_NPC'], None, None), ('toggle-present', 'mob bob act sentinel', ['ACT_IS_NPC'], None, None), ('toggle-absent', 'mob bob act scavenger', ['ACT_IS_NPC', 'ACT_SENTINEL', 'ACT_SCAVENGER'], None, None), ('equal-preserves-npc', 'mob bob act = scavenger', ['ACT_IS_NPC', 'ACT_SCAVENGER'], None, None), ('nonsettable-present-preserved', 'mob bob act - npc', ['ACT_IS_NPC', 'ACT_SENTINEL'], None, None), ('duplicate-toggle-only-once', 'mob bob act sentinel sentinel', ['ACT_IS_NPC'], None, None), ('type-label-does-not-restrict-kind', 'char bob act + scavenger', ['ACT_IS_NPC', 'ACT_SENTINEL', 'ACT_SCAVENGER'], None, None), ('operator-alone', 'mob bob act =', ['ACT_IS_NPC', 'ACT_SENTINEL'], 'zone-A', 'Which flags do you wish to change?\n\r')]:
    add('flags.c', 'do_flag', suffix, {**base_flag, 'argument': arg}, {'return': 'void', 'result': {'bob.act': act, 'bob.zone': {'C_NULL': True} if zone is None else zone}, 'messages': [] if msg is None else [{'recipient': 'admin', 'text': msg}], 'forbidden': ['messages to bob or bystanders', 'changes to other flag fields']}, needle="type = argument[0]")
add('flags.c', 'do_flag', 'nonsettable-absent-can-be-added-reference-quirk', {**base_flag, 'argument': 'char bob plr + holylight', 'victim': {'id': 'bob', 'kind': 'PC', 'act': [], 'zone': 'zone-A'}}, {'return': 'void', 'result': {'bob.act': ['PLR_HOLYLIGHT'], 'bob.zone': {'C_NULL': True}}, 'messages': [], 'quirk': 'settable=false only protects a bit already present in old; it does not reject adding an absent bit.'}, needle='!flag_table[pos].settable')

# Alias helper paths. Recording interpret boundary distinguishes original owner and active body.
alias_base = {'descriptor': {'character': 'body', 'original': 'owner'}, 'owner': {'id': 'owner', 'kind': 'PC', 'prefix': '', 'aliases': [['x', 'look'], ['xx', 'north']]}, 'body': {'id': 'body', 'kind': 'NPC'}}
for suffix, arg, owner_overrides, command, messages in [
    ('exact-first-word', 'x sword', {}, 'look sword', []), ('no-recursive-expansion', 'x', {'aliases': [['x', 'xx'], ['xx', 'north']]}, 'xx ', []),
    ('prefix-not-exact-alias', 'xyz sword', {}, 'xyz sword', []), ('input-lowercases-first-word-only', 'X Sword', {}, 'look Sword', []),
    ('protected-alias-command', 'alias x look', {}, 'alias x look', []), ('protected-una-prefix', 'unacceptable x', {}, 'unacceptable x', []),
    ('prefix-precedes-alias', 'sword', {'prefix': 'x'}, 'look sword', []), ('prefix-command-bypasses-prefix', 'prefix abc', {'prefix': 'x'}, 'prefix abc', []),
    ('no-aliases', 'x', {'aliases': []}, 'x', []), ('original-npc-bypasses-alias', 'x', {'kind': 'NPC'}, 'x', [])]:
    add('alias.c', 'substitute_alias', suffix, {**alias_base, 'owner': {**alias_base['owner'], **owner_overrides}, 'argument': arg},
        {'ordered_events': messages + [{'call': 'interpret', 'actor': 'body', 'argument': command}], 'unchanged': ['alias definitions', 'prefix', 'owner/body gameplay state at this boundary'], 'forbidden': ['recursive substitute_alias call']}, needle='ch = d->original', controls={'interpret': 'Recording boundary only; gameplay side effects of interpreted command specified separately.', 'randomness': 'none'})
add('alias.c', 'substitute_alias', 'replacement-truncates-at-255', {**alias_base, 'owner': {**alias_base['owner'], 'aliases': [['x', 'a' * 254]]}, 'argument': 'x bc'},
    {'ordered_events': [{'call': 'send_to_char', 'recipient': 'owner', 'text': 'Alias substitution too long. Truncated.\r\n'}, {'call': 'interpret', 'actor': 'body', 'argument': 'a' * 254 + ' '}], 'result_length': 255}, needle='strlen(buf) > MAX_INPUT_LENGTH - 1', controls={'interpret': 'Recording collaborator; do not dispatch gameplay.', 'randomness': 'none'})
add('alias.c', 'substitute_alias', 'prefix-overflow-boundary-undefined', {**alias_base, 'owner': {**alias_base['owner'], 'prefix': 'a' * 255}, 'argument': 'x'},
    {'portable_oracle': 'Unavailable: strlen(prefix)+strlen(argument)==256 passes the >256 guard, but sprintf writes 258 bytes into prefix[256].'}, needle='strlen(ch->prefix) + strlen(argument)', blocked=True, questions=['Undefined stack write. Choose a target validation policy separately; do not reproduce an accidental C outcome.'])
add('alias.c', 'do_alia', 'requires-full-name', {'actor': {'id': 'ch'}, 'argument': ''}, {'messages': [{'recipient': 'ch', 'text': "I'm sorry, alias must be entered in full.\n\r"}], 'return': 'void'}, needle='send_to_char')
for suffix, argument, aliases, result, msg in [('no-aliases', '', [], [], 'You have no aliases defined.\n\r'), ('reserved-alias', 'alias look', [], [], 'Sorry, that word is reserved.\n\r'), ('reserved-una-prefix', 'unacceptable look', [], [], 'Sorry, that word is reserved.\n\r'), ('undefined-query', 'x', [], [], 'That alias is not defined.\n\r'), ('defined-query', 'x', [['x', 'look']], [['x', 'look']], "x aliases to 'look'.\n\r"), ('add', 'x look', [], [['x', 'look']], "x is now aliased to 'look'.\n\r"), ('redefine', 'x north', [['x', 'look']], [['x', 'north']], "x is now realiased to 'north'.\n\r"), ('delete-abbreviation-rejected', 'x del', [], [], 'That shall not be done!\n\r'), ('prefix-abbreviation-rejected', 'x pre', [], [], 'That shall not be done!\n\r'), ('full-delete-plus-argument-allowed-quirk', 'x delete yes', [], [['x', 'delete yes']], "x is now aliased to 'delete yes'.\n\r"), ('tilde-sanitized', 'x look~', [], [['x', 'look-']], "x is now aliased to 'look-'.\n\r")]:
    add('alias.c', 'do_alias', suffix, {'actor': {'id': 'ch', 'kind': 'PC', 'desc': None, 'aliases': aliases}, 'argument': argument}, {'result_aliases': result, 'messages': [{'recipient': 'ch', 'text': msg}], 'return': 'void', 'forbidden': ['interpret command', 'messages to bystanders']}, needle='smash_tilde(argument)')
add('alias.c', 'do_alias', 'at-five-alias-limit', {'actor': {'id': 'ch', 'kind': 'PC', 'desc': None, 'aliases': [[n, 'look'] for n in ['a', 'b', 'c', 'd', 'e']]}, 'argument': 'f north'}, {'messages': [{'recipient': 'ch', 'text': 'Sorry, you have reached the alias limit.\n\r'}], 'unchanged': ['all five aliases'], 'forbidden': ['sixth alias']}, needle='pos >= MAX_ALIAS')
for suffix, argument, aliases, result, msg in [('missing-name', '', [['a', 'look']], [['a', 'look']], 'Unalias what?\n\r'), ('not-found', 'z', [['a', 'look']], [['a', 'look']], 'No alias of that name to remove.\n\r'), ('remove-only', 'a', [['a', 'look']], [], 'Alias removed.\n\r'), ('remove-first-shifts-all', 'a', [['a', 'look'], ['b', 'north'], ['c', 'south']], [['b', 'north'], ['c', 'south']], 'Alias removed.\n\r'), ('remove-middle-shifts-tail', 'b', [['a', 'look'], ['b', 'north'], ['c', 'south']], [['a', 'look'], ['c', 'south']], 'Alias removed.\n\r'), ('remove-last', 'c', [['a', 'look'], ['c', 'south']], [['a', 'look']], 'Alias removed.\n\r')]:
    add('alias.c', 'do_unalias', suffix, {'actor': {'id': 'ch', 'kind': 'PC', 'desc': None, 'aliases': aliases}, 'argument': argument}, {'messages': [{'recipient': 'ch', 'text': msg}], 'result_aliases': result, 'tail_slots': 'C NULL after last occupied slot', 'forbidden': ['interpret command']}, needle='one_argument(argument,arg)')

add('alias.c', 'substitute_alias', 'active-owner-prefix-over-limit',
    {'descriptor': {'character': 'ch', 'original': None},
     'actor': {'id': 'ch', 'kind': 'PC', 'prefix': 'a' * 255, 'aliases': []}, 'argument': 'go'},
    {'ordered_events': [{'call': 'send_to_char', 'recipient': 'ch', 'text': 'Line to long, prefix not processed.\r\n'},
                        {'call': 'interpret', 'actor': 'ch', 'argument': 'go'}]},
    needle='Line to long', controls={'interpret': 'Record dispatch without executing gameplay.'})
add('alias.c', 'substitute_alias', 'five-nonmatching-slots',
    {**alias_base, 'owner': {**alias_base['owner'], 'aliases': [[n, 'look'] for n in 'abcde']}, 'argument': 'z'},
    {'ordered_events': [{'call': 'interpret', 'actor': 'body', 'argument': 'z'}],
     'forbidden': ['one_argument', 'message', 'alias mutation']},
    needle='alias < MAX_ALIAS', controls={'interpret': 'Record dispatch without executing gameplay.'})

for fn in ('do_alias', 'do_unalias'):
    add('alias.c', fn, 'npc-without-original-returns',
        {'actor': {'id': 'ch', 'kind': 'NPC', 'desc': {'original': None}, 'pcdata': None}, 'argument': 'x look'},
        {'messages': [], 'forbidden': ['alias slot access', 'one_argument'], 'unchanged': ['alias state']},
        needle='IS_NPC(rch)')

for suffix, aliases, texts in [
    ('list-two', [['x', 'look'], ['y', 'north']], ['    x:  look\n\r', '    y:  north\n\r']),
    ('list-stops-at-null-replacement', [['x', 'look'], ['y', None], ['z', 'south']], ['    x:  look\n\r']),
    ('list-five', [[n, 'look'] for n in 'abcde'], [f'    {n}:  look\n\r' for n in 'abcde']),
]:
    add('alias.c', 'do_alias', suffix,
        {'actor': {'id': 'ch', 'kind': 'PC', 'desc': None, 'aliases': aliases}, 'argument': ''},
        {'messages': [{'recipient': 'ch', 'text': text} for text in ['Your current aliases are:\n\r', *texts]],
         'unchanged': ['alias slots']}, needle='Your current aliases')
add('alias.c', 'do_alias', 'switched-owner-edited-active-body-notified',
    {'actor': {'id': 'body', 'kind': 'NPC', 'desc': {'original': 'owner'}},
     'owner': {'id': 'owner', 'kind': 'PC', 'aliases': [['x', 'look']]}, 'argument': 'X north'},
    {'result_aliases': {'owner': [['x', 'north']]},
     'messages': [{'recipient': 'body', 'text': "x is now realiased to 'north'.\n\r"}],
     'forbidden': ['mutate body aliases', 'send to owner']}, needle='rch = ch->desc->original')
add('alias.c', 'do_alias', 'query-stops-at-null-replacement',
    {'actor': {'id': 'ch', 'kind': 'PC', 'desc': None, 'aliases': [['x', None], ['y', 'look']]}, 'argument': 'y'},
    {'messages': [{'recipient': 'ch', 'text': 'That alias is not defined.\n\r'}], 'unchanged': ['alias slots']},
    needle='That alias is not defined')
add('alias.c', 'do_unalias', 'switched-owner-first-of-duplicate-names',
    {'actor': {'id': 'body', 'kind': 'NPC', 'desc': {'original': 'owner'}},
     'owner': {'id': 'owner', 'kind': 'PC', 'aliases': [['x', 'look'], ['x', 'north'], ['y', 'south']]}, 'argument': 'X ignored'},
    {'result_aliases': {'owner': [['x', 'north'], ['y', 'south']]},
     'messages': [{'recipient': 'body', 'text': 'Alias removed.\n\r'}],
     'forbidden': ['second deletion', 'send to owner']}, needle='if (found)')

# Each row connects a representative execution to the lexical sites it visits.
alias_sites = {
    'substitute_alias': {
        'exact-first-word': 'ternary.001 if.001 if.003 or.001 or.002 or.003 or.004 for.001 if.004 if.005 if.006 if.007 break.002',
        'prefix-not-exact-alias': 'for.001 if.004 if.005 if.006 break.001',
        'prefix-precedes-alias': 'if.001 and.001 if.002',
        'active-owner-prefix-over-limit': 'ternary.001 if.001 and.001 if.002 if.003 or.001 or.002 return.001',
        'replacement-truncates-at-255': 'if.007 break.002',
        'protected-alias-command': 'if.003 or.002 or.003 return.001',
        'protected-una-prefix': 'if.003 or.003 or.004 return.001',
        'prefix-command-bypasses-prefix': 'if.001 and.001 or.004 return.001',
        'original-npc-bypasses-alias': 'if.003 or.001 return.001',
        'five-nonmatching-slots': 'for.001 if.004 if.005',
    },
    'do_alia': {'requires-full-name': 'return.001'},
    'do_alias': {
        'npc-without-original-returns': 'if.001 ternary.001 if.002 return.001',
        'no-aliases': 'if.003 if.004 return.002',
        'list-two': 'if.004 for.001 if.005 or.001 break.001 return.003',
        'list-stops-at-null-replacement': 'for.001 if.005 or.001 break.001 return.003',
        'reserved-alias': 'if.006 or.002 return.004',
        'reserved-una-prefix': 'if.006 or.002 return.004',
        'defined-query': 'if.007 for.002 if.008 or.003 if.009 return.005',
        'undefined-query': 'if.007 for.002 if.008 or.003 break.002 return.006',
        'query-stops-at-null-replacement': 'if.008 or.003 break.002 return.006',
        'delete-abbreviation-rejected': 'if.010 or.004 return.007',
        'prefix-abbreviation-rejected': 'if.010 or.004 return.007',
        'switched-owner-edited-active-body-notified': 'ternary.001 for.003 if.011 if.012 return.008',
        'at-five-alias-limit': 'for.003 if.011 if.012 if.013 return.009',
        'add': 'for.003 if.011 break.003 if.013',
    },
    'do_unalias': {
        'npc-without-original-returns': 'if.001 ternary.001 if.002 return.001',
        'missing-name': 'if.003 return.002',
        'not-found': 'for.001 if.004 break.001 if.005 if.006 if.007',
        'remove-first-shifts-all': 'for.001 if.004 if.005 continue.001 if.006 if.007',
        'switched-owner-first-of-duplicate-names': 'ternary.001 if.005 continue.001 if.006 if.007',
    },
}
for case in cases:
    file, fn, suffix = case['id'].split('.', 2)
    if file == 'alias':
        case['branch_ids'].extend(f'alias.{fn}.{site}' for site in alias_sites[fn].get(suffix, '').split())

# Scan boundary: do_scan is not present in this checkout's command table.
add('scan.c', 'do_scan', 'invalid-direction', {'actor': {'id': 'ch', 'in_room': 'A'}, 'argument': 'northeast'}, {'messages': [{'recipient': 'ch', 'text': 'Which way do you want to scan?\n\r'}], 'forbidden': ['scan_list', 'room messages', 'movement']}, needle='Which way')
add('scan.c', 'do_scan', 'around-includes-current-and-each-exit', {'actor': {'id': 'ch', 'in_room': 'A'}, 'argument': '', 'rooms': {'A': {'exit': {'north': {'to_room': 'B', 'flags': ['EX_CLOSED']}, 'east': {'to_room': 'B', 'flags': []}}}}}, {'ordered_events': [{'act': '$n looks all around.', 'channel': 'TO_ROOM'}, {'send_to_char': 'Looking around you see:\n\r', 'recipient': 'ch'}, {'scan_list': ['A', 'ch', 0, -1]}, {'scan_list': ['B', 'ch', 1, 0]}, {'scan_list': ['B', 'ch', 1, 1]}], 'forbidden': ['exit closed check', 'deduplication of same destination', 'movement']}, needle="arg1[0] == '\\0'", controls={'scan_list': 'Recording helper boundary; separate cases trace occupant filtering.', 'randomness': 'none'})
for suffix, argument, door in [('north-short', 'n', 0), ('north-long', 'north', 0), ('east-short', 'e', 1), ('south-short', 's', 2), ('west-short', 'w', 3), ('up-short', 'u', 4), ('down-short', 'd', 5)]:
    add('scan.c', 'do_scan', suffix, {'actor': {'id': 'ch', 'in_room': 'A'}, 'argument': argument, 'rooms': {'A': {'selected_exit': 'B'}, 'B': {'selected_exit': 'C'}, 'C': {'selected_exit': 'D'}, 'D': {'selected_exit': 'E'}}},
        {'ordered_events': [{'act': 'You peer intently $T.', 'channel': 'TO_CHAR'}, {'act': '$n peers intently $T.', 'channel': 'TO_ROOM'}, {'scan_list': ['B', 'ch', 1, door]}, {'scan_list': ['C', 'ch', 2, door]}, {'scan_list': ['D', 'ch', 3, door]}], 'forbidden': ['scan fourth room E', 'send formatted Looking direction header; it is only sprintf into buf', 'movement']}, needle='for (depth = 1', controls={'scan_list': 'Recording helper boundary; occupant filtering specified separately.', 'randomness': 'none'})
add('scan.c', 'scan_list', 'null-room', {'arguments': {'scan_room': {'C_NULL': True}, 'ch': 'ch', 'depth': 1, 'door': 0}}, {'return': 'void', 'forbidden': ['can_see', 'scan_char', 'get_trust', 'messages']}, needle='scan_room == NULL')
for suffix, occupants, trust, visible, calls in [('empty', [], 10, {}, []), ('self-skipped', [{'id': 'ch', 'kind': 'PC', 'invis_level': 0}], 10, {}, []), ('pc-invis-too-high', [{'id': 'v', 'kind': 'PC', 'invis_level': 11}], 10, {}, []), ('pc-invis-equality-visible', [{'id': 'v', 'kind': 'PC', 'invis_level': 10}], 10, {'v': True}, ['v']), ('npc-bypasses-pre-filter', [{'id': 'v', 'kind': 'NPC', 'invis_level': 99}], 10, {'v': True}, ['v']), ('can-see-false', [{'id': 'v', 'kind': 'PC', 'invis_level': 0}], 10, {'v': False}, []), ('multiple-in-list-order', [{'id': 'a', 'kind': 'PC', 'invis_level': 0}, {'id': 'b', 'kind': 'NPC', 'invis_level': 0}], 10, {'a': True, 'b': True}, ['a', 'b'])]:
    add('scan.c', 'scan_list', suffix, {'actor': {'id': 'ch'}, 'scan_room': {'people_in_list_order': occupants}, 'arguments': {'depth': 2, 'door': 0}}, {'scan_char_calls_in_order': [{'victim': v, 'ch': 'ch', 'depth': 2, 'door': 0} for v in calls], 'can_see_calls': list(visible), 'unchanged': ['room list and all entities']}, needle='rch == ch', controls={'get_trust': {'kind': 'stubbed helper; get_trust independently specified', 'returns': trust}, 'can_see': {'kind': 'stubbed visibility boundary; internal random draws belong to can_see cases', 'returns_by_victim': visible}, 'scan_char': 'Recording helper boundary; formatting contract separate.'})
for depth, phrase in [(1, 'nearby to the north.'), (2, 'not far north.'), (3, 'off in the distance north.')]:
    add('scan.c', 'scan_char', f'depth-{depth}', {'victim': {'id': 'v'}, 'actor': {'id': 'ch'}, 'arguments': {'depth': depth, 'door': 0}}, {'messages': [{'recipient': 'ch', 'text': 'A guard, ' + phrase + '\n\r'}], 'forbidden': ['messages to victim or observers', 'movement']}, needle='sprintf(buf2', controls={'PERS': 'Formatting boundary returns A guard; visibility/name helpers not bypassed in their own cases.', 'dir_name[0]': 'north', 'randomness': 'none'})
add('scan.c', 'scan_char', 'around-depth-zero-negative-door-undefined', {'arguments': {'depth': 0, 'door': -1}, 'victim': 'v', 'actor': 'ch'}, {'portable_oracle': 'Unavailable: dir_name[-1] is evaluated as a sprintf argument even though distance[0] contains no conversion.'}, needle='sprintf(buf2', blocked=True, questions=['do_scan around invokes this state for visible occupants in the current room. Define a safe target behavior explicitly; C out-of-bounds access is not portable.'])

# Spell farsight uses do_function, not interpret, and only checks blindness locally.
add('magic2.c', 'spell_farsight', 'blind-rejects-before-scan', {'actor': {'id': 'ch', 'affected_by': ['AFF_BLIND']}, 'target_name': 'north', 'arguments': {'sn': 0, 'level': 1, 'vo': {'C_NULL': True}, 'target': 0}}, {'messages': [{'recipient': 'ch', 'text': 'Maybe it would help if you could see?\n\r'}], 'forbidden': ['do_function', 'scan', 'movement']}, needle='IS_AFFECTED')
add('magic2.c', 'spell_farsight', 'delegates-raw-target-name', {'actor': {'id': 'ch', 'affected_by': [], 'position': 'POS_SLEEPING'}, 'target_name': 'north', 'arguments': {'sn': 0, 'level': 1, 'vo': {'C_NULL': True}, 'target': 0}}, {'ordered_events': [{'call': 'do_function', 'arguments': ['ch', '&do_scan', 'north']}], 'forbidden': ['local position check', 'interpret', 'local resource charge']}, needle='do_function', controls={'do_function': 'Recording wrapper boundary; wrapper duplicates string, invokes handler and frees copy; does not enforce command-table position.'})

# Room permission boundaries: trust differs from level; HEROES_ONLY uses immortality.
room_actor = {'id': 'ch', 'kind': 'PC', 'level': 10, 'trust': 0, 'clan': 0, 'desc': None}
for suffix, actor_updates, room_flags, room_clan, result in [
    ('ordinary-room', {}, [], 0, True), ('imp-below', {'level': 59}, ['ROOM_IMP_ONLY'], 0, False),
    ('imp-at-max', {'level': 60}, ['ROOM_IMP_ONLY'], 0, True), ('gods-below', {'level': 51}, ['ROOM_GODS_ONLY'], 0, False),
    ('gods-at-immortal', {'level': 52}, ['ROOM_GODS_ONLY'], 0, True), ('heroes-hero-still-denied', {'level': 51}, ['ROOM_HEROES_ONLY'], 0, False),
    ('heroes-at-immortal', {'level': 52}, ['ROOM_HEROES_ONLY'], 0, True), ('newbie-at-five', {'level': 5}, ['ROOM_NEWBIES_ONLY'], 0, True),
    ('newbie-at-six', {'level': 6}, ['ROOM_NEWBIES_ONLY'], 0, False), ('newbie-immortal-exception', {'level': 52}, ['ROOM_NEWBIES_ONLY'], 0, True),
    ('clan-mismatch', {}, [], 2, False), ('clan-matches', {'clan': 2}, [], 2, True), ('clan-immortal-exception', {'level': 52}, [], 2, True),
    ('trust-qualifies-low-level', {'level': 1, 'trust': 52}, ['ROOM_GODS_ONLY'], 0, True),
    ('npc-level-sixty-not-immortal', {'kind': 'NPC', 'level': 60}, ['ROOM_GODS_ONLY'], 0, False),
    ('safe-and-no-recall-do-not-hide-room', {}, ['ROOM_SAFE', 'ROOM_NO_RECALL'], 0, True)]:
    add('handler.c', 'can_see_room', suffix, {'actor': {**room_actor, **actor_updates}, 'room': {'room_flags': room_flags, 'clan': room_clan}, 'constants': {'MAX_LEVEL': 60, 'LEVEL_IMMORTAL': 52}}, {'return': result, 'unchanged': ['room and character'], 'forbidden': ['messages', 'random draws']}, needle='ROOM_IMP_ONLY')

see_actor = {'id': 'ch', 'kind': 'PC', 'level': 20, 'trust': 0, 'act': [], 'affected_by': [], 'in_room': 'A', 'desc': None}
see_victim = {'id': 'v', 'kind': 'PC', 'level': 10, 'invis_level': 0, 'incog_level': 0, 'affected_by': [], 'fighting': None, 'in_room': 'A'}
for suffix, actor_updates, victim_updates, dark, rolls, result in [
    ('ordinary-visible', {}, {}, False, [], True), ('self-before-blindness', {'affected_by': ['AFF_BLIND']}, {'id': 'ch', 'invis_level': 99}, True, [], True),
    ('invis-level-above-trust', {}, {'invis_level': 21}, False, [], False), ('invis-level-equal-trust', {}, {'invis_level': 20}, False, [], True),
    ('holylight-does-not-beat-wizinvis', {'act': ['PLR_HOLYLIGHT']}, {'invis_level': 21}, False, [], False),
    ('incognito-same-room', {}, {'incog_level': 99}, False, [], True), ('incognito-other-room', {}, {'incog_level': 21, 'in_room': 'B'}, False, [], False),
    ('incognito-equal-trust-other-room', {}, {'incog_level': 20, 'in_room': 'B'}, False, [], True),
    ('holylight-beats-blindness', {'act': ['PLR_HOLYLIGHT'], 'affected_by': ['AFF_BLIND']}, {}, True, [], True),
    ('immortal-npc-beats-blindness', {'kind': 'NPC', 'trust': 52, 'affected_by': ['AFF_BLIND']}, {}, True, [], True),
    ('blind-denies', {'affected_by': ['AFF_BLIND']}, {}, False, [], False), ('dark-denies', {}, {}, True, [], False),
    ('infrared-beats-dark', {'affected_by': ['AFF_INFRARED']}, {}, True, [], True),
    ('invisible-denies', {}, {'affected_by': ['AFF_INVISIBLE']}, False, [], False),
    ('detect-invisible', {'affected_by': ['AFF_DETECT_INVIS']}, {'affected_by': ['AFF_INVISIBLE']}, False, [], True),
    ('sneak-roll-below-thirty', {}, {'affected_by': ['AFF_SNEAK']}, False, [29], False),
    ('sneak-roll-equal-thirty', {}, {'affected_by': ['AFF_SNEAK']}, False, [30], True),
    ('sneak-roll-above-thirty', {}, {'affected_by': ['AFF_SNEAK']}, False, [31], True),
    ('sneak-fighting-skips-roll', {}, {'affected_by': ['AFF_SNEAK'], 'fighting': 'enemy'}, False, [], True),
    ('sneak-detect-hidden-skips-roll', {'affected_by': ['AFF_DETECT_HIDDEN']}, {'affected_by': ['AFF_SNEAK']}, False, [], True),
    ('hide-without-detection', {}, {'affected_by': ['AFF_HIDE']}, False, [], False),
    ('hide-while-fighting-visible', {}, {'affected_by': ['AFF_HIDE'], 'fighting': 'enemy'}, False, [], True),
    ('hide-with-detection-visible', {'affected_by': ['AFF_DETECT_HIDDEN']}, {'affected_by': ['AFF_HIDE']}, False, [], True),
    ('sneak-roll-succeeds-but-hide-denies', {}, {'affected_by': ['AFF_SNEAK', 'AFF_HIDE']}, False, [30], False)]:
    add('handler.c', 'can_see', suffix, {'actor': {**see_actor, **actor_updates}, 'victim': {**see_victim, **victim_updates}, 'identity': 'victim aliases actor exactly when id=ch; actor state then applies', 'skill_and_stats': {'victim.gsn_sneak': 40, 'victim.STAT_DEX': 10, 'actor.STAT_INT': 10}}, {'return': result, 'ordered_number_percent_returns': rolls, 'sneak_chance_when_used': '40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30', 'unchanged': ['actor, victim, rooms'], 'forbidden': ['messages', 'unscripted random draws']}, needle='ch == victim', controls={'room_is_dark': {'kind': 'stubbed helper; independently specified', 'returns': dark}, 'get_skill': {'kind': 'stubbed skill calculation boundary', 'returns': 40}, 'get_curr_stat': {'victim.STAT_DEX': 10, 'actor.STAT_INT': 10}, 'number_percent': {'kind': 'scripted helper; independently specified', 'ordered_returns': rolls}, 'get_trust': 'Real contract independently specified, actor level/trust/descriptor above.'})
for suffix, actor_updates, obj_updates, dark, result in [
    ('ordinary', {}, {}, False, True), ('holylight-beats-death', {'act': ['PLR_HOLYLIGHT']}, {'extra_flags': ['ITEM_VIS_DEATH']}, True, True),
    ('death-hidden', {}, {'extra_flags': ['ITEM_VIS_DEATH']}, False, False), ('blind-nonpotion', {'affected_by': ['AFF_BLIND']}, {}, False, False),
    ('blind-potion-exception', {'affected_by': ['AFF_BLIND']}, {'item_type': 'ITEM_POTION'}, False, True),
    ('lit-light-before-invis-dark', {}, {'item_type': 'ITEM_LIGHT', 'value[2]': 1, 'extra_flags': ['ITEM_INVIS']}, True, True),
    ('infinite-light-negative-duration', {}, {'item_type': 'ITEM_LIGHT', 'value[2]': -1}, True, True),
    ('unlit-light-in-dark', {}, {'item_type': 'ITEM_LIGHT', 'value[2]': 0}, True, False),
    ('invisible-glow-still-hidden', {}, {'extra_flags': ['ITEM_INVIS', 'ITEM_GLOW']}, False, False),
    ('detect-invis', {'affected_by': ['AFF_DETECT_INVIS']}, {'extra_flags': ['ITEM_INVIS']}, False, True),
    ('glow-beats-dark', {}, {'extra_flags': ['ITEM_GLOW']}, True, True), ('dark-without-vision', {}, {}, True, False),
    ('infrared-does-not-suffice-for-objects', {'affected_by': ['AFF_INFRARED']}, {}, True, False),
    ('dark-vision-for-objects', {'affected_by': ['AFF_DARK_VISION']}, {}, True, True)]:
    add('handler.c', 'can_see_obj', suffix, {'actor': {**see_actor, **actor_updates}, 'object': {'id': 'o', 'item_type': 'ITEM_WEAPON', 'extra_flags': [], 'value[2]': 0, **obj_updates}}, {'return': result, 'unchanged': ['actor and object'], 'forbidden': ['messages', 'random draws']}, needle='PLR_HOLYLIGHT', controls={'room_is_dark': {'kind': 'stubbed helper; independently specified', 'returns': dark}, 'other_dependencies': 'Flag macros only.'})
for suffix, kind, level, trust, flags, result in [('normal-object', 'PC', 1, 0, [], True), ('nodrop-mortal', 'PC', 51, 0, ['ITEM_NODROP'], False), ('nodrop-immortal', 'PC', 52, 0, ['ITEM_NODROP'], True), ('trust-alone-insufficient', 'PC', 1, 60, ['ITEM_NODROP'], False), ('npc-no-exception', 'NPC', 60, 60, ['ITEM_NODROP'], False)]:
    add('handler.c', 'can_drop_obj', suffix, {'actor': {'kind': kind, 'level': level, 'trust': trust}, 'object': {'extra_flags': flags}}, {'return': result, 'unchanged': ['actor and object']}, needle='ITEM_NODROP')

# Portal/nexus guard and resource ordering at explicit collaborator boundaries.
travel_actor = {'id': 'ch', 'kind': 'PC', 'level': 40, 'trust': 0, 'desc': None, 'clan': 0, 'in_room': 'A', 'held_item': {'id': 'stone', 'item_type': 'ITEM_WARP_STONE'}}
travel_victim = {'id': 'v', 'kind': 'PC', 'level': 20, 'clan': 0, 'in_room': 'B', 'imm_flags': []}
travel_rooms = {'A': {'vnum': 100, 'room_flags': [], 'clan': 0, 'people': ['ch', 'observer-A']}, 'B': {'vnum': 200, 'room_flags': [], 'clan': 0, 'people': ['v', 'observer-B']}}
for fn in ['spell_portal', 'spell_nexus']:
    for suffix, change in [('no-victim', {'lookup_returns': 'C NULL'}), ('self-target', {'lookup_returns': 'ch'}), ('victim-no-room', {'victim': {'in_room': None}}), ('room-not-visible', {'can_see_room': False}), ('destination-safe', {'destination_flag': 'ROOM_SAFE'}), ('destination-private', {'destination_flag': 'ROOM_PRIVATE'}), ('destination-solitary', {'destination_flag': 'ROOM_SOLITARY'}), ('destination-no-recall', {'destination_flag': 'ROOM_NO_RECALL'}), ('origin-no-recall', {'origin_flag': 'ROOM_NO_RECALL'}), ('victim-level-at-spell-plus-three', {'victim': {'level': 43}}), ('hero-pc-regardless-of-trust', {'victim': {'level': 51, 'trust': 0}, 'level': 60}), ('npc-summon-immune', {'victim': {'kind': 'NPC', 'imm_flags': ['IMM_SUMMON']}}), ('npc-saves', {'victim': {'kind': 'NPC'}, 'saves_spell': True}), ('clan-mismatch', {'victim': {'clan': 2}})]:
        actor = dict(travel_actor)
        victim = {**travel_victim, **change.get('victim', {})}
        rooms = json.loads(json.dumps(travel_rooms))
        if 'destination_flag' in change:
            rooms['B']['room_flags'].append(change['destination_flag'])
        if 'origin_flag' in change:
            rooms['A']['room_flags'].append(change['origin_flag'])
        add('magic2.c', fn, suffix, {'actor': actor, 'victim': victim, 'rooms': rooms, 'target_name': 'v', 'arguments': {'sn': 1, 'level': change.get('level', 40), 'vo': None, 'target': 0}},
            {'messages': [{'recipient': 'ch', 'text': 'You failed.\n\r'}], 'unchanged': ['held stone and ownership', 'all rooms and characters'], 'forbidden': ['get_eq_char', 'extract_obj', 'create_object', 'movement', 'local mana/wait changes']}, needle='victim = get_char_world',
            controls={'get_char_world': {'kind': 'stubbed lookup boundary', 'returns': change.get('lookup_returns', 'v')}, 'can_see_room': {'kind': 'helper boundary; separately specified', 'returns': change.get('can_see_room', True)}, 'saves_spell': {'kind': 'spell-save boundary', 'returns': change.get('saves_spell', False), 'calls': 1 if suffix == 'npc-saves' else 0}, 'is_clan/is_same_clan': 'Real contracts with snapshot clan table, separately specified.', 'randomness': 'No direct random draw in spell; saving helper is scripted.'})
    for suffix, immortal, held, succeeds in [('mortal-no-component', False, None, False), ('mortal-wrong-component', False, {'id': 'sword', 'item_type': 'ITEM_WEAPON'}, False), ('immortal-no-component', True, None, True), ('immortal-wrong-component', True, {'id': 'sword', 'item_type': 'ITEM_WEAPON'}, True)]:
        add('magic2.c', fn, suffix, {'actor': {**travel_actor, 'level': 52 if immortal else 40, 'held_item': held}, 'victim': travel_victim, 'rooms': travel_rooms, 'target_name': 'v', 'arguments': {'sn': 1, 'level': 40, 'vo': None, 'target': 0}},
            {'outcome': 'continue to portal creation' if succeeds else 'return with component failure', 'messages_before_creation': [] if succeeds else [{'recipient': 'ch', 'text': 'You lack the proper component for this spell.\n\r'}], 'unchanged': ['wrong held item, if present'], 'extract_obj_calls': 0, 'create_object_calls': (2 if fn == 'spell_nexus' else 1) if succeeds else 0}, needle='stone = get_eq_char', controls={'world_lookup': 'v', 'can_see_room': True, 'saves_spell_calls': 0, 'get_eq_char(WEAR_HOLD)': held, 'create_object/obj_to_room/act': 'Recording boundaries; creation suffix cases specify full ordered contract.'})
    for level, timer in ([(24, 2), (25, 3), (49, 3), (50, 4)] if fn == 'spell_portal' else [(9, 1), (10, 2), (19, 2), (20, 3)]):
        # Keep victim below level+3 for low-level nexus cases.
        victim = {**travel_victim, 'level': 1}
        events = [{'act': 'You draw upon the power of $p.', 'channel': 'TO_CHAR', 'object': 'stone'}, {'act': 'It flares brightly and vanishes!', 'channel': 'TO_CHAR', 'object': 'stone'}, {'extract_obj': 'stone'}, {'create_object': {'index_vnum': 25, 'level': 0, 'id': 'portal-1'}}, {'set': {'portal-1.timer': timer, 'portal-1.value[3]': 200}}, {'obj_to_room': ['portal-1', 'A']}, {'act': '$p rises up from the ground.', 'channel': 'TO_ROOM', 'anchor': 'ch'}, {'act': '$p rises up before you.', 'channel': 'TO_CHAR', 'anchor': 'ch'}]
        if fn == 'spell_nexus':
            events += [{'create_object': {'index_vnum': 25, 'level': 0, 'id': 'portal-2'}}, {'set': {'portal-2.timer': timer, 'portal-2.value[3]': 100}}, {'obj_to_room': ['portal-2', 'B']}, {'act': '$p rises up from the ground.', 'channel': 'TO_ROOM', 'anchor': 'v'}, {'act': '$p rises up from the ground.', 'channel': 'TO_CHAR', 'anchor': 'v'}]
        add('magic2.c', fn, f'success-level-{level}', {'actor': travel_actor, 'victim': victim, 'rooms': travel_rooms, 'target_name': 'v', 'arguments': {'sn': 1, 'level': level, 'vo': None, 'target': 0}}, {'ordered_events': events, 'result': {'stone': 'extracted', 'characters_in_rooms': 'unchanged'}, 'forbidden': ['movement', 'additional mana/wait charges in this function', 'backlink portal' if fn == 'spell_portal' else 'third portal']}, needle='portal->timer', controls={'get_char_world': 'v', 'can_see_room': True, 'get_eq_char(WEAR_HOLD)': 'stone', 'create_object': 'Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.', 'extract_obj': 'Record component consumption; internals of unequip/extraction remain separate pending dependencies.', 'act': 'Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.', 'randomness': 'none; victim is PC'})
add('magic2.c', 'spell_nexus', 'same-room-one-portal', {'actor': travel_actor, 'victim': {**travel_victim, 'in_room': 'A'}, 'rooms': travel_rooms, 'target_name': 'v', 'arguments': {'sn': 1, 'level': 40, 'vo': None, 'target': 0}}, {'create_object_calls': 1, 'portal': {'in_room': 'A', 'value[3]': 100, 'timer': 5}, 'stone': 'consumed before creation', 'forbidden': ['return portal creation', 'destination-anchor messages']}, needle='to_room == from_room', controls={'get_char_world': 'v', 'can_see_room': True, 'create_object/act/extract_obj': 'Recording boundaries as in nexus success cases.', 'randomness': 'none'})
add('magic2.c', 'spell_nexus', 'safe-origin-denies', {'actor': travel_actor, 'victim': travel_victim, 'rooms': {**travel_rooms, 'A': {**travel_rooms['A'], 'room_flags': ['ROOM_SAFE']}}, 'target_name': 'v', 'arguments': {'sn': 1, 'level': 40, 'vo': None, 'target': 0}}, {'messages': [{'recipient': 'ch', 'text': 'You failed.\n\r'}], 'unchanged': ['stone', 'all entities'], 'forbidden': ['component lookup', 'creation']}, needle='IS_SET(from_room->room_flags,ROOM_SAFE)', controls={'get_char_world': 'v', 'can_see_room': True, 'saves_spell_calls': 0})

add('magic2.c', 'spell_nexus', 'origin-invisible-after-visible-destination',
    {'actor': travel_actor, 'victim': travel_victim, 'rooms': travel_rooms, 'target_name': 'v',
     'arguments': {'sn': 1, 'level': 40, 'vo': None, 'target': 0}},
    {'ordered_events': [{'get_char_world': ['ch', 'v']}, {'can_see_room': ['ch', 'B']},
                        {'can_see_room': ['ch', 'A']}, {'send_to_char': 'You failed.\n\r', 'recipient': 'ch'}],
     'forbidden': ['saves_spell', 'get_eq_char', 'extract_obj', 'create_object']},
    needle='!can_see_room(ch,from_room)',
    controls={'get_char_world': 'v', 'can_see_room': {'ordered_returns': [True, False]}})
add('magic2.c', 'spell_nexus', 'empty-destination-people-skips-announcements',
    {'actor': {**travel_actor, 'level': 52, 'held_item': None}, 'victim': travel_victim,
     'rooms': {**travel_rooms, 'B': {**travel_rooms['B'], 'people': []}}, 'target_name': 'v',
     'arguments': {'sn': 1, 'level': 40, 'vo': None, 'target': 0},
     'invariant_override': 'The lookup returns v with in_room B although B has no linked occupants.'},
    {'ordered_events': [
        {'obj_to_room': ['portal-1', 'A'], 'timer': 5, 'value[3]': 200},
        {'act': '$p rises up from the ground.', 'channel': 'TO_ROOM', 'anchor': 'ch'},
        {'act': '$p rises up before you.', 'channel': 'TO_CHAR', 'anchor': 'ch'},
        {'obj_to_room': ['portal-2', 'B'], 'timer': 5, 'value[3]': 100}],
     'forbidden': ['destination act', 'extract_obj', 'movement']},
    needle='to_room->people != NULL',
    controls={'get_char_world': 'Script v at the lookup boundary.', 'can_see_room': {'ordered_returns': [True, True]},
              'create_object': 'Return portal-1 then portal-2.', 'act': 'Record template and recipient channel.'})

travel_guard_order = [
    'no-victim', 'self-target', 'victim-no-room', 'room-not-visible', 'destination-safe',
    'destination-private', 'destination-solitary', 'destination-no-recall', 'origin-no-recall',
    'victim-level-at-spell-plus-three', 'hero-pc-regardless-of-trust', 'npc-summon-immune',
    'npc-saves', 'clan-mismatch',
]
nexus_guard_order = travel_guard_order.copy()
nexus_guard_order.insert(4, 'origin-invisible-after-visible-destination')
nexus_guard_order.insert(6, 'safe-origin-denies')
for case in cases:
    file, fn, suffix = case['id'].split('.', 2)
    if file != 'magic2':
        continue
    if fn == 'spell_farsight':
        sites = ['if.001']
        if suffix == 'blind-rejects-before-scan':
            sites.append('return.001')
    else:
        nexus = fn == 'spell_nexus'
        guards = nexus_guard_order if nexus else travel_guard_order
        if suffix in guards:
            stop = guards.index(suffix)
            sites = ['if.001', 'return.001']
            if stop:
                sites.append(f'or.{stop:03}')
            if suffix in guards[-4:]:
                sites.append(f'and.{guards[-4:].index(suffix) + 1:03}')
            visibility_calls = [] if stop < 3 else ['B']
            if nexus and stop > 3:
                visibility_calls.append('A')
            case['expected']['can_see_room_calls_in_order'] = visibility_calls
            branch = next(b for b in index['src/magic2.c', fn]['branch_ledger']
                          if b['id'] == f'magic2.{fn}.' + (f'or.{stop:03}' if stop else 'if.001'))
            if branch['source_ref'] not in case['source_refs']:
                case['source_refs'].append(branch['source_ref'])
        else:
            sites = ['if.001', 'if.002', 'and.005']
            if suffix.startswith('mortal-'):
                sites += [f'or.{len(guards):03}', 'return.002']
            else:
                sites += ['if.003', 'and.006']
                if nexus:
                    sites += ['if.004', 'return.003' if suffix == 'same-room-one-portal' else 'if.005']
    case['branch_ids'].extend(f'magic2.{fn}.{site}' for site in sites)

# Healer economics: the menu's serious price differs from the charged amount.
heal_base = {'actor': {'id': 'ch', 'kind': 'PC', 'in_room': 'A', 'gold': 100, 'silver': 0, 'wait': 0, 'mana': 10, 'max_mana': 100}, 'healer': {'id': 'h', 'kind': 'NPC', 'act': ['ACT_IS_NPC', 'ACT_IS_HEALER'], 'level': 30, 'gold': 0, 'silver': 0}, 'room': {'id': 'A', 'people_in_order': ['ch', 'h']}}
add('healer.c', 'do_heal', 'no-healer-before-argument-parsing', {**heal_base, 'room': {'id': 'A', 'people_in_order': ['ch']}, 'argument': 'nonsense'}, {'messages': [{'recipient': 'ch', 'text': "You can't do that here.\n\r"}], 'unchanged': ['gold, silver, wait, mana'], 'forbidden': ['one_argument', 'skill_lookup', 'spell call']}, needle='mob == NULL')
add('healer.c', 'do_heal', 'price-menu', {**heal_base, 'argument': ''}, {'ordered_events': [{'act': "$N says 'I offer the following spells:'", 'channel': 'TO_CHAR', 'actor': 'ch', 'victim': 'h'}], 'subsequent_send_to_char_in_order': ['  light: cure light wounds      10 gold\n\r', '  serious: cure serious wounds  15 gold\n\r', '  critic: cure critical wounds  25 gold\n\r', '  heal: healing spell\t      50 gold\n\r', '  blind: cure blindness         20 gold\n\r', '  disease: cure disease         15 gold\n\r', '  poison:  cure poison\t      25 gold\n\r', '  uncurse: remove curse\t      50 gold\n\r', '  refresh: restore movement      5 gold\n\r', '  mana:  restore mana\t      10 gold\n\r', ' Type heal <type> to be healed.\n\r'], 'unchanged': ['currencies, wait, mana'], 'forbidden': ['spell execution', 'dice']}, needle="arg[0] == '\\0'")
add('healer.c', 'do_heal', 'unknown-service', {**heal_base, 'argument': 'nonsense'}, {'act_calls': [{'template': "$N says 'Type 'heal' for a list of spells.'", 'channel': 'TO_CHAR', 'actor': 'ch', 'victim': 'h'}], 'unchanged': ['currencies, wait, mana'], 'forbidden': ['deduct_cost', 'spell', 'dice']}, needle="Type 'heal'")
services = [('light', 'cure light', 'spell_cure_light', 1000, 'judicandus dies'), ('serious', 'cure serious', 'spell_cure_serious', 1600, 'judicandus gzfuajg'), ('critical', 'cure critical', 'spell_cure_critical', 2500, 'judicandus qfuhuqar'), ('heal', 'heal', 'spell_heal', 5000, 'pzar'), ('blindness', 'cure blindness', 'spell_cure_blindness', 2000, 'judicandus noselacri'), ('disease', 'cure disease', 'spell_cure_disease', 1500, 'judicandus eugzagz'), ('poison', 'cure poison', 'spell_cure_poison', 2500, 'judicandus sausabru'), ('uncurse', 'remove curse', 'spell_remove_curse', 5000, 'candussido judifgz'), ('curse', 'remove curse', 'spell_remove_curse', 5000, 'candussido judifgz'), ('refresh', 'refresh', 'spell_refresh', 500, 'candusima'), ('moves', 'refresh', 'spell_refresh', 500, 'candusima')]
for service, lookup, spell, cost, words in services:
    for enough in [False, True]:
        balance = cost if enough else cost - 1
        actor = {**heal_base['actor'], 'gold': 0, 'silver': balance}
        events = [{'skill_lookup': lookup, 'returns': 7}]
        if enough:
            events += [{'wait': {'ch': 12}}, {'deduct_cost': ['ch', cost]}, {'healer_currency_credit': {'gold': cost // 100, 'silver': cost % 100}}, {'act': "$n utters the words '$T'.", 'channel': 'TO_ROOM', 'actor': 'h', 'words': words}, {'spell_call': {'function': spell, 'sn': 7, 'level': 30, 'caster': 'h', 'target': 'ch', 'target_type': 'TARGET_CHAR'}}]
        else:
            events += [{'act': "$N says 'You do not have enough gold for my services.'", 'channel': 'TO_CHAR', 'actor': 'ch', 'victim': 'h'}]
        add('healer.c', 'do_heal', service + ('-exact-price' if enough else '-one-silver-short'), {**heal_base, 'actor': actor, 'argument': service}, {'ordered_events': events, 'post_balance_if_enough': {'ch.gold': 0, 'ch.silver': 0} if enough else 'unchanged', 'forbidden': [] if enough else ['WAIT_STATE', 'deduct_cost', 'healer credit', 'spell execution']}, needle='if (cost >', controls={'skill_lookup': {'kind': 'stubbed skill-index boundary', 'returns': 7}, 'spell': 'Recording behavior boundary; the selected healing spell internals remain separate pending paths.', 'deduct_cost': 'Use independent currency contract, specified below.', 'act': 'Record template, substitutions and channel; delivery rendering remains separate.', 'randomness': 'No direct random draws on non-mana path.'})
for suffix, mana, max_mana, wait, roll, result in [('uncapped', 10, 100, 0, 2, 22), ('capped', 95, 100, 0, 16, 100), ('existing-wait-preserved', 10, 100, 20, 2, 22)]:
    add('healer.c', 'do_heal', 'mana-' + suffix, {**heal_base, 'actor': {**heal_base['actor'], 'gold': 10, 'mana': mana, 'max_mana': max_mana, 'wait': wait}, 'argument': 'mana'}, {'ordered_events': [{'wait': max(wait, 12)}, {'deduct_cost': ['ch', 1000]}, {'healer_currency_credit': {'gold': 10, 'silver': 0}}, {'act': "$n utters the words '$T'.", 'actor': 'h', 'channel': 'TO_ROOM', 'words': 'energizer'}, {'dice': [2, 8], 'returns': roll}, {'mana_result': result}, {'send_to_char': 'A warm glow passes through you.\n\r', 'recipient': 'ch'}], 'forbidden': ['skill_lookup', 'spell function call']}, needle='spell == NULL', controls={'dice': {'kind': 'scripted helper; separately specified', 'returns': roll}, 'deduct_cost': 'Independently specified currency contract.', 'randomness': 'Only dice(2,8) boundary consumes scripted randomness.'})
add('healer.c', 'do_heal', 'missing-skill-index-still-charges', {**heal_base, 'argument': 'light'}, {'ordered_events': [{'skill_lookup': 'cure light', 'returns': -1}, {'wait': 12}, {'deduct_cost': ['ch', 1000]}, {'healer_currency_credit': {'gold': 10, 'silver': 0}}, {'act': "$n utters the words '$T'.", 'channel': 'TO_ROOM', 'actor': 'h', 'words': 'judicandus dies'}], 'return': 'void', 'forbidden': ['spell function call', 'refund']}, needle='if (sn == -1)', controls={'skill_lookup': {'kind': 'failure injection at lookup boundary', 'returns': -1}, 'spell': 'Record calls; none permitted.'})
for suffix, gold, silver, cost, out_gold, out_silver, bug in [('silver-only', 2, 170, 100, 2, 70, None), ('gold-exact', 2, 0, 100, 1, 0, None), ('gold-change', 1, 0, 1, 0, 99, None), ('mixed-change', 2, 50, 170, 0, 80, None), ('zero', 2, 50, 0, 2, 50, None), ('negative-cost-credits', 2, 50, -20, 2, 70, None), ('insufficient-gold-clamped', 0, 10, 100, 0, 10, ['deduct costs: gold %d < 0', -1])]:
    add('handler.c', 'deduct_cost', suffix, {'actor': {'gold': gold, 'silver': silver}, 'arguments': {'cost': cost}}, {'result': {'gold': out_gold, 'silver': out_silver}, 'bug_calls': [] if bug is None else [bug], 'forbidden': ['messages', 'random draws']}, needle='silver = UMIN', controls={'bug': 'Recording logging boundary; no changes beyond this function.'})

# Save probability is strict less-than after clamp, not <=.
for suffix, dis, spell, duration, roll, result, threshold in [('equal-level-below', 20, 20, 1, 49, True, 50), ('equal-level-equality', 20, 20, 1, 50, False, 50), ('permanent-adds-five', 20, 20, -1, 74, True, 75), ('permanent-threshold', 20, 20, -1, 75, False, 75), ('lower-cap-below', 100, 1, 0, 4, True, 5), ('lower-cap-equality', 100, 1, 0, 5, False, 5), ('upper-cap-below', 1, 100, 0, 94, True, 95), ('upper-cap-equality', 1, 100, 0, 95, False, 95)]:
    add('magic.c', 'saves_dispel', suffix, {'arguments': {'dis_level': dis, 'spell_level': spell, 'duration': duration}}, {'return': result, 'save_threshold': threshold, 'number_percent_calls': 1}, needle='save = 50', controls={'number_percent': {'kind': 'scripted helper; independently specified', 'ordered_returns': [roll]}})
for suffix, victim_updates, immunity, roll, result, threshold in [('normal-below', {}, 'IS_NORMAL', 49, True, 50), ('normal-equality', {}, 'IS_NORMAL', 50, False, 50), ('immune-no-roll', {}, 'IS_IMMUNE', None, True, None), ('resistant-below', {}, 'IS_RESISTANT', 51, True, 52), ('resistant-equality', {}, 'IS_RESISTANT', 52, False, 52), ('vulnerable-equality', {}, 'IS_VULNERABLE', 48, False, 48), ('berserk-adds-half-level', {'affected_by': ['AFF_BERSERK']}, 'IS_NORMAL', 59, True, 60), ('negative-saving-throw-improves', {'saving_throw': -2}, 'IS_NORMAL', 53, True, 54), ('positive-saving-throw-weakens', {'saving_throw': 2}, 'IS_NORMAL', 46, False, 46), ('mana-class-nine-tenths', {'kind': 'PC', 'class_fMana': True}, 'IS_NORMAL', 45, False, 45), ('mana-class-integer-truncation', {'kind': 'PC', 'class_fMana': True, 'saving_throw': 1}, 'IS_NORMAL', 43, False, 43), ('lower-cap', {'saving_throw': 100}, 'IS_NORMAL', 5, False, 5), ('upper-cap', {'saving_throw': -100}, 'IS_NORMAL', 95, False, 95)]:
    add('magic.c', 'saves_spell', suffix, {'victim': {'id': 'v', 'kind': 'NPC', 'level': 20, 'saving_throw': 0, 'affected_by': [], 'class_fMana': False, **victim_updates}, 'arguments': {'level': 20, 'dam_type': 'DAM_FIRE'}, 'class_contract': 'class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary.'}, {'return': result, 'threshold_after_clamp': threshold, 'number_percent_calls': 0 if roll is None else 1, 'unchanged': ['victim']}, needle='save = 50', controls={'check_immune': {'kind': 'stubbed helper boundary', 'returns': immunity}, 'number_percent': {'kind': 'scripted helper; independently specified', 'ordered_returns': [] if roll is None else [roll]}})

# Ban matching preserves the checkout's surprising BOTH-flags strstr direction.
for suffix, site, bans, result in [('empty-list', 'EXAMPLE.COM', [], False), ('type-not-set', 'example.com', [{'name': 'example.com', 'flags': ['BAN_SUFFIX']}], False), ('exact-without-prefix-suffix-does-not-match', 'example.com', [{'name': 'example.com', 'flags': ['BAN_ALL']}], False), ('prefix-flag-tests-host-suffix', 'Host.Example.COM', [{'name': 'example.com', 'flags': ['BAN_ALL', 'BAN_PREFIX']}], True), ('suffix-flag-tests-host-prefix', 'HOST.example.com', [{'name': 'host', 'flags': ['BAN_ALL', 'BAN_SUFFIX']}], True), ('both-flags-host-contained-in-pattern', 'Example.COM', [{'name': 'xxexample.comyy', 'flags': ['BAN_ALL', 'BAN_PREFIX', 'BAN_SUFFIX']}], True), ('both-flags-do-not-match-interior-pattern-in-host', 'xxexample.comyy', [{'name': 'example.com', 'flags': ['BAN_ALL', 'BAN_PREFIX', 'BAN_SUFFIX']}], False), ('later-entry-matches', 'host.example.com', [{'name': 'other', 'flags': ['BAN_ALL', 'BAN_SUFFIX']}, {'name': 'example.com', 'flags': ['BAN_ALL', 'BAN_PREFIX']}], True)]:
    add('ban.c', 'check_ban', suffix, {'arguments': {'site': site, 'type': 'BAN_ALL'}, 'ban_list_in_order': bans}, {'return': result, 'unchanged': ['site and ban list'], 'forbidden': ['messages', 'persistence writes', 'random draws']}, needle='strcpy(host,capitalize(site))', controls={'capitalize/str_prefix/str_suffix': 'Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host.'})

# Ban persistence under the Unix NULL_FILE definition. Calls to the file
# interface are observable even when there is no final ban.txt.
for suffix, rows, lines in [
    ('empty', [], []),
    ('temporary-only', [['temp', 56, ['BAN_ALL']]], []),
    ('permanent-in-list-order', [
        ['alpha', 56, ['BAN_PREFIX', 'BAN_ALL', 'BAN_PERMANENT']],
        ['temp', 56, ['BAN_ALL']],
        ['beta', 60, ['BAN_SUFFIX', 'BAN_PERMIT', 'BAN_PERMANENT']],
    ], ['alpha'.ljust(20) + ' 56 BDF\n', 'beta'.ljust(20) + ' 60 AEF\n']),
]:
    add('ban.c', 'save_bans', suffix, {'ban_list': rows, 'fpReserve': 'R0', 'existing_ban_file': 'old\n'},
        {'ordered_events': [{'fclose': 'R0'}, {'fopen': ['ban.txt', 'w']},
                            *[{'write': ['W', line]} for line in lines], {'fclose': 'W'},
                            {'fopen': ['/dev/null', 'r']},
                            *([] if lines else [{'unlink': 'ban.txt'}])],
         'fpReserve': 'R1', 'final_ban_file': ''.join(lines) if lines else None, 'unchanged': ['ban_list']},
        needle='if (!found)', controls={'fopen': {'ordered_returns': ['W', 'R1']},
                                        'writes_close_and_unlink': 'Succeed where called.',
                                        'print_flags': 'Script BDF then AEF for the two permanent rows. Isolate the serializer signed-shift platform issue.'})
add('ban.c', 'save_bans', 'open-failure-permanent-row-undefined',
    {'ban_list': [['alpha', 56, ['BAN_ALL', 'BAN_PERMANENT']]], 'fpReserve': 'R0'},
    {'defined_prefix': [{'fclose': 'R0'}, {'fopen': ['ban.txt', 'w']}, {'perror': 'ban.txt'}],
     'portable_oracle': 'Unavailable after the diagnostic because fprintf receives a null stream.'},
    needle='perror', controls={'fopen': {'ordered_returns': [None]}}, blocked=True,
    questions=['The source continues after the failed open. A portable fixture cannot assert the resulting process state.'])
add('ban.c', 'save_bans', 'open-failure-without-permanent-row-undefined',
    {'ban_list': [], 'fpReserve': 'R0'},
    {'defined_prefix': [{'fclose': 'R0'}, {'fopen': ['ban.txt', 'w']}, {'perror': 'ban.txt'}],
     'portable_oracle': 'Unavailable after the diagnostic because fclose receives a null stream.'},
    needle='perror', controls={'fopen': {'ordered_returns': [None]}}, blocked=True,
    questions=['The failed open does not branch around fclose.'])

add('ban.c', 'load_bans', 'missing-file',
    {'ban_list': [], 'file': None},
    {'ordered_events': [{'fopen': ['ban.txt', 'r']}], 'unchanged': ['ban_list'],
     'forbidden': ['new_ban', 'fclose', 'read']},
    needle='fopen', controls={'fopen': {'ordered_returns': [None]}})
add('ban.c', 'load_bans', 'loads-two-rows-in-file-order',
    {'ban_list': [], 'file': 'alpha 56 BDF\nbeta 60 AEF\n'},
    {'result_list': [['alpha', 56, ['BAN_PREFIX', 'BAN_ALL', 'BAN_PERMANENT']],
                     ['beta', 60, ['BAN_SUFFIX', 'BAN_PERMIT', 'BAN_PERMANENT']]],
     'ordered_events': ['Open ban.txt for reading', 'Allocate and link alpha as head',
                        'Allocate and append beta', 'Close file after EOF'], 'forbidden': ['save_bans']},
    needle='if (ban_list == NULL)', controls={'fopen': 'Succeed; use the real parser on fixture bytes.'})
add('ban.c', 'load_bans', 'nonempty-list-first-append-undefined',
    {'ban_list': [['old', 56, ['BAN_ALL']]], 'file': 'alpha 56 BDF\n'},
    {'defined_prefix': ['Open file and parse alpha row'], 'portable_oracle': 'ban_last is still NULL on first append.'},
    needle='ban_last->next', controls={'fopen': 'Succeed; use the real parser on fixture bytes.'}, blocked=True,
    questions=['The boot caller starts with an empty global list. A later direct call with existing entries dereferences NULL.'])

ban_actor = {'id': 'ch', 'kind': 'PC', 'level': 56, 'trust': 0, 'desc': None}
ban_a = ['alpha', 56, ['BAN_ALL']]
ban_b = ['beta', 55, ['BAN_NEWBIES']]
for suffix, argument, rows, remaining, message, sites in [
    ('missing-name', '', [ban_a], [ban_a], 'Remove which site from the ban list?', 'if.001 return.001'),
    ('missing-entry', 'z', [ban_a, ban_b], [ban_a, ban_b], 'Site is not banned.', 'for.001 if.002 return.004'),
    ('higher-trust', 'alpha', [['alpha', 57, ['BAN_ALL']]], [['alpha', 57, ['BAN_ALL']]],
     'You are not powerful enough to lift that ban.', 'if.002 if.003 return.002'),
    ('remove-head-at-equal-trust', 'ALPHA ignored', [ban_a, ban_b], [ban_b], 'Ban on alpha lifted.',
     'if.003 if.004 return.003'),
    ('remove-interior', 'beta', [ban_a, ban_b, ['gamma', 55, ['BAN_ALL']]], [ban_a, ['gamma', 55, ['BAN_ALL']]],
     'Ban on beta lifted.', 'if.004 return.003'),
]:
    removed = suffix.startswith('remove-')
    events = [{'send_to_char': message + '\n\r', 'recipient': 'ch'}]
    if removed:
        events = [{'free_ban': 'alpha' if 'head' in suffix else 'beta'}, *events, {'save_bans': remaining}]
    add('ban.c', 'do_allow', suffix, {'actor': ban_actor, 'argument': argument, 'ban_list': rows},
        {'result_list': remaining, 'ordered_events': events,
         'forbidden': [] if removed else ['free_ban', 'save_bans']},
        needle='if ( arg[0]', controls={'save_bans': 'Record the list at persistence boundary.'})
    cases[-1]['branch_ids'].extend(f'ban.do_allow.{site}' for site in sites.split())

for fn, permanent in [('do_ban', False), ('do_permban', True)]:
    add('ban.c', fn, 'dispatch-unchanged-argument',
        {'actor': ban_actor, 'argument': '*Alpha* n'},
        {'ordered_events': [{'ban_site': ['ch', '*Alpha* n', permanent]}]},
        needle='ban_site(ch', controls={'ban_site': 'Recording boundary.'})
    cases[-1]['branch_ids'].append(f'ban.{fn}.entry')

for suffix, argument, permanent, rows, flags, text, sites in [
    ('no-sites', '', False, [], [], 'No sites banned at this time.', 'if.001 if.002 return.001'),
    ('invalid-type-before-pattern', '* invalid', False, [], [], 'Acceptable ban types are all, newbies, and permit.',
     'if.003 or.001 if.004 if.005 return.003'),
    ('double-star-empty-name', '**', False, [], [], 'You have to ban SOMETHING.',
     'if.006 if.007 if.008 return.004'),
    ('higher-trust', 'ALPHA a', True, [['alpha', 57, ['BAN_ALL']]], [],
     'That ban was set by a higher power.', 'for.002 if.009 if.010 return.005'),
    ('plain-default-type', 'alpha', False, [ban_b], ['BAN_ALL'], 'alpha has been banned.',
     'if.003 or.001 if.006 if.007 if.008 for.002 if.009 if.012 if.013 if.014 return.006'),
    ('both-wildcards-permanent-newbies', '*Alpha* n', True, [],
     ['BAN_NEWBIES', 'BAN_PREFIX', 'BAN_SUFFIX', 'BAN_PERMANENT'], 'alpha has been banned.',
     'if.004 if.006 if.007 if.012 if.013 if.014 return.006'),
    ('suffix-permit', 'alpha* p', False, [], ['BAN_PERMIT', 'BAN_SUFFIX'], 'alpha has been banned.',
     'if.005 if.006 if.007 if.012 if.013 if.014 return.006'),
]:
    result = ([['alpha', 56, flags], *rows] if flags else rows)
    events = [{'send_to_char': text + '\n\r', 'recipient': 'ch'}]
    if flags:
        events = [{'new_ban': ['alpha', 56, flags]}, {'save_bans': result}, *events]
    add('ban.c', 'ban_site', suffix, {'actor': ban_actor, 'argument': argument, 'fPerm': permanent, 'ban_list': rows},
        {'result_list': result, 'ordered_events': events, 'forbidden': [] if flags else ['new_ban', 'save_bans']},
        needle='argument = one_argument', controls={'save_bans': 'Record the list at persistence boundary.'})
    cases[-1]['branch_ids'].extend(f'ban.ban_site.{site}' for site in sites.split())

listing_rows = [
    ['alpha', 56, ['BAN_PREFIX', 'BAN_SUFFIX', 'BAN_NEWBIES', 'BAN_PERMIT', 'BAN_PERMANENT']],
    ['beta', 55, ['BAN_SUFFIX', 'BAN_PERMIT']], ['gamma', 54, ['BAN_ALL']], ['delta', 53, []],
]
listing_text = 'Banned sites  level  type     status\n\r' + ''.join(
    f'{pattern:<12}    {level:<3}  {kind:<7}  {status}\n\r'
    for pattern, level, kind, status in [
        ('*alpha*', 56, 'newbies', 'perm'), ('beta*', 55, 'permit', 'temp'),
        ('gamma', 54, 'all', 'temp'), ('delta', 53, '', 'temp'),
    ]
)
add('ban.c', 'ban_site', 'list-formats-wildcards-and-type-precedence',
    {'actor': ban_actor, 'argument': '', 'fPerm': False, 'ban_list': listing_rows},
    {'ordered_events': [{'page_to_char': listing_text, 'recipient': 'ch'}, {'free_buf': 'listing'}],
     'unchanged': ['ban_list'], 'forbidden': ['save_bans', 'new_ban']},
    needle='if ( arg1[0]', controls={'buffer': 'Record append order and concatenate all entries within capacity.'})
cases[-1]['branch_ids'].extend(f'ban.ban_site.{site}' for site in
    'if.001 if.002 for.001 ternary.001 ternary.002 ternary.003 ternary.004 ternary.005 ternary.006 return.002'.split())

for suffix, rows, remaining in [
    ('head', [ban_a, ban_b], [ban_b]), ('interior', [ban_b, ban_a], [ban_b]),
]:
    result = [['alpha', 56, ['BAN_PERMIT']], *remaining]
    add('ban.c', 'ban_site', f'replace-{suffix}-with-empty-free-list',
        {'actor': ban_actor, 'argument': 'alpha p', 'fPerm': False, 'ban_list': rows, 'ban_free': []},
        {'result_list': result, 'ordered_events': [
            {'free_ban': 'old alpha'}, {'new_ban': 'reuses old alpha record'}, {'save_bans': result},
            {'send_to_char': 'alpha has been banned.\n\r', 'recipient': 'ch'}]},
        needle='if (prev == NULL)', controls={'save_bans': 'Record the list at persistence boundary.'})
    cases[-1]['branch_ids'].extend(['ban.ban_site.if.010', 'ban.ban_site.if.011'])

add('ban.c', 'ban_site', 'single-star-empty-name-index-undefined',
    {'actor': ban_actor, 'argument': '*', 'fPerm': False, 'ban_list': []},
    {'portable_oracle': 'After consuming the leading star, strlen(name) is zero. The unsigned subtraction wraps and the computed array index lies outside arg1.'},
    needle='name[strlen(name) - 1]', blocked=True,
    questions=['The empty-pattern diagnostic comes after the out-of-bounds expression.'])

ban_sites = {
    'save_bans': {
        'empty': 'if.001 for.001 if.003', 'temporary-only': 'for.001 if.002 if.003',
        'permanent-in-list-order': 'if.001 for.001 if.002 if.003',
        'open-failure-permanent-row-undefined': 'if.001 for.001 if.002',
    },
    'load_bans': {
        'missing-file': 'if.001 return.001',
        'loads-two-rows-in-file-order': 'if.001 for.001 if.002 return.002 if.003',
        'nonempty-list-first-append-undefined': 'if.003',
    },
    'check_ban': {
        'empty-list': 'for.001 return.004', 'type-not-set': 'if.001 continue.001',
        'exact-without-prefix-suffix-does-not-match': 'if.002 and.001 if.003 and.003 if.004 and.004 return.004',
        'prefix-flag-tests-host-suffix': 'if.002 and.002 if.003 and.003 return.002',
        'suffix-flag-tests-host-prefix': 'if.004 and.004 return.003',
        'both-flags-host-contained-in-pattern': 'if.002 and.001 and.002 return.001',
        'both-flags-do-not-match-interior-pattern-in-host': 'if.002 and.002 if.003 and.003 if.004 and.004 return.004',
    },
}
for case in cases:
    file, fn, suffix = case['id'].split('.', 2)
    if file == 'ban' and fn in ban_sites:
        case['branch_ids'].extend(f'ban.{fn}.{site}' for site in ban_sites[fn].get(suffix, '').split())

# Scheduler counters start at zero and use fixed intervals in this checkout.
for n in [1, 2, 12, 13, 16, 17, 24, 25, 240, 241, 480, 481]:
    periods = {'area_update': 480, 'song_update': 24, 'mobile_update': 16, 'violence_update': 12, 'point_group': 240}
    schedules = {name: list(range(1, n + 1, period)) for name, period in periods.items()}
    add('update.c', 'update_handler', f'fresh-process-through-call-{n}', {'static_counters_initial': {'pulse_area': 0, 'pulse_music': 0, 'pulse_mobile': 0, 'pulse_violence': 0, 'pulse_point': 0}, 'units': 'One invocation per game-loop pulse; PULSE_PER_SECOND=4.'},
        {'call_indices_by_event': schedules, 'point_group_order': ['wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)', 'pulse_point reset', 'weather_update', 'char_update', 'obj_update'], 'same_invocation_group_order': ['area_update', 'song_update', 'mobile_update', 'violence_update', 'point_group', 'aggr_update', 'tail_chain'], 'every_invocation': ['aggr_update', 'tail_chain'], 'counter_result': {name: period - ((n - 1) % period) for name, period in [('pulse_area', 480), ('pulse_music', 24), ('pulse_mobile', 16), ('pulse_violence', 12), ('pulse_point', 240)]}, 'forbidden': ['number_range calls to randomize tick or area interval']}, needle='static  int', controls={'scheduled_helpers': 'Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.', 'wiznet': 'Record message/channel/flags without network delivery.', 'randomness': 'No random calls in this wrapper; interval randomizers are commented out.'}, action=f'In a fresh scheduler state, invoke update_handler {n} times sequentially; retain counters between invocations.')

# Random destination sampling: bounded rejection classes plus explicit absence of retry cap.
for suffix, actor_kind, aggressive, room_flag, private, visible in [('missing-index', 'PC', False, None, False, True), ('invisible', 'PC', False, None, False, False), ('private-helper', 'PC', False, None, True, True), ('private-flag', 'PC', False, 'ROOM_PRIVATE', False, True), ('solitary-flag', 'PC', False, 'ROOM_SOLITARY', False, True), ('safe-flag', 'PC', False, 'ROOM_SAFE', False, True), ('law-denies-ordinary-pc', 'PC', False, 'ROOM_LAW', False, True)]:
    add('act_enter.c', 'get_random_room', 'reject-' + suffix, {'actor': {'id': 'ch', 'kind': actor_kind, 'act': ['ACT_AGGRESSIVE'] if aggressive else []}, 'candidate': {'id': 'bad', 'room_flags': [room_flag] if room_flag else []}, 'accepted': {'id': 'good', 'room_flags': []}}, {'ordered_sampling': [{'number_range': [0, 65535], 'returns': 1}, {'get_room_index': 1, 'returns': 'C NULL' if suffix == 'missing-index' else 'bad'}, {'number_range': [0, 65535], 'returns': 2}, {'get_room_index': 2, 'returns': 'good'}], 'return': 'good', 'unchanged': ['actor, rooms'], 'forbidden': ['movement', 'messages']}, needle='room = get_room_index', controls={'number_range': {'kind': 'scripted helper; independently specified', 'ordered_returns': [1, 2]}, 'get_room_index': {'1': 'C NULL' if suffix == 'missing-index' else 'bad', '2': 'good'}, 'can_see_room': {'bad': visible, 'good': True}, 'room_is_private': {'bad': private, 'good': False}, 'helper_boundaries': 'Lookup and room permission collaborators are recorded/scripted; private and visible contracts independently specified.'})
for suffix, kind, flags in [('npc-law-allowed-even-aggressive', 'NPC', ['ACT_IS_NPC', 'ACT_AGGRESSIVE']), ('pc-aggressive-bit-law-allowed', 'PC', ['ACT_AGGRESSIVE']), ('ordinary-room-first-draw', 'PC', [])]:
    add('act_enter.c', 'get_random_room', suffix, {'actor': {'kind': kind, 'act': flags}, 'room': {'id': 'R', 'room_flags': [] if suffix == 'ordinary-room-first-draw' else ['ROOM_LAW']}}, {'return': 'R', 'number_range_calls': 1, 'unchanged': ['all entities']}, needle='IS_NPC(ch) ||', controls={'number_range': {'kind': 'scripted helper', 'ordered_returns': [1]}, 'get_room_index(1)': 'R', 'can_see_room': True, 'room_is_private': False})

for case in cases:
    if not case['id'].startswith('act_enter.get_random_room.'):
        continue
    suffix = case['id'].split('.', 2)[2]
    sites = ['for.001', 'if.001', 'if.002', 'and.001', 'and.002', 'and.003',
             'and.004', 'and.005', 'or.001', 'or.002', 'break.001', 'return.001']
    if suffix == 'npc-law-allowed-even-aggressive':
        sites.remove('or.002')
    case['branch_ids'].extend(f'act_enter.get_random_room.{site}' for site in sites)
    if suffix.startswith('reject-'):
        case['expected']['can_see_room_calls_in_order'] = ['good'] if suffix == 'reject-missing-index' else ['bad', 'good']
        case['expected']['room_is_private_calls_in_order'] = (
            ['good'] if suffix in {'reject-missing-index', 'reject-invisible'} else ['bad', 'good'])

enter_base = {'actor': {'id': 'ch', 'kind': 'PC', 'level': 30, 'trust': 0, 'desc': None, 'fighting': None, 'in_room': 'A', 'affected_by': [], 'act': []}, 'room': {'id': 'A', 'room_flags': []}, 'portal': {'id': 'P', 'item_type': 'ITEM_PORTAL', 'value': [0, 0, 0, 200, 0], 'in_room': 'A'}, 'argument': 'portal'}
for suffix, actor_changes, portal_changes, arg, msg in [('fighting-silent', {'fighting': 'enemy'}, {}, 'portal', None), ('empty-argument', {}, {}, '', "Nope, can't do it.\n\r"), ('no-object', {}, {}, 'missing', "You don't see that here.\n\r"), ('not-a-portal', {}, {'item_type': 'ITEM_WEAPON'}, 'portal', "You can't seem to find a way in.\n\r"), ('closed-mortal', {}, {'value': [0, ['EX_CLOSED'], [], 200, 0]}, 'portal', "You can't seem to find a way in.\n\r"), ('cursed-mortal', {'affected_by': ['AFF_CURSE']}, {}, 'portal', 'Something prevents you from leaving...\n\r')]:
    add('act_enter.c', 'do_enter', suffix, {**enter_base, 'actor': {**enter_base['actor'], **actor_changes}, 'portal': {**enter_base['portal'], **portal_changes}, 'argument': arg}, {'messages': [] if msg is None else [{'recipient': 'ch', 'text': msg}], 'unchanged': ['room membership', 'portal values and ownership', 'actor resources'], 'forbidden': ['get_random_room', 'destination room lookup', 'movement', 'charge use', 'follower recursion']}, needle='ch->fighting != NULL', controls={'get_obj_list': {'kind': 'object lookup boundary', 'returns': 'C NULL' if suffix == 'no-object' else 'P', 'calls': 0 if suffix in ['fighting-silent', 'empty-argument'] else 1}, 'get_trust': 'Real helper contract with actor level/trust/descriptor above.'})

for suffix, flags, stored, roll, destination, selected, final_vnum in [
    ('random-flag-records-before-origin-rejection', ['GATE_RANDOM', 'GATE_BUGGY'], 200, None, 'A', 'get_random_room', 100),
    ('minus-one-records-before-origin-rejection', ['GATE_BUGGY'], -1, None, 'A', 'get_random_room', 100),
    ('buggy-four-uses-random-without-recording', ['GATE_BUGGY'], 200, 4, 'A', 'get_random_room', 200),
    ('buggy-five-uses-index', ['GATE_BUGGY'], 200, 5, None, 'get_room_index', 200),
    ('fixed-portal-skips-percent', [], 200, None, None, 'get_room_index', 200),
]:
    events = [{'get_obj_list': ['ch', 'portal', 'A.contents']}]
    if roll is not None:
        events.append({'number_percent': roll})
    events.append({selected: 'ch' if selected == 'get_random_room' else 200, 'returns': destination})
    if final_vnum != stored:
        events.append({'set': {'P.value[3]': final_vnum}})
    events.append({'act': "$p doesn't seem to go anywhere.", 'channel': 'TO_CHAR', 'actor': 'ch', 'object': 'P'})
    add('act_enter.c', 'do_enter', suffix,
        {**enter_base, 'room': {**enter_base['room'], 'vnum': 100, 'contents': ['P']},
         'portal': {**enter_base['portal'], 'value': [0, 0, flags, stored, 0]}},
        {'ordered_events': events, 'P.value[3]': final_vnum,
         'forbidden': ['can_see_room', 'room_is_private', 'movement', 'charge mutation', 'follower dispatch']},
        needle='GATE_RANDOM', controls={'get_obj_list': 'P', selected: destination,
                                        'number_percent': {'ordered_returns': [] if roll is None else [roll]}})
    sites = ['if.006', 'or.003', 'if.008', 'or.004', 'return.005']
    if 'GATE_RANDOM' not in flags and stored != -1:
        sites += ['if.007', 'and.004']
    cases[-1]['branch_ids'].extend(f'act_enter.do_enter.{site}' for site in sites)

for suffix, charge, gate_flags, after in [
    ('unlimited-stationary-portal', 0, [], 0),
    ('charged-portal-goes-with-actor', 2, ['GATE_GOWITH', 'GATE_NORMAL_EXIT'], 1),
    ('last-charge-fades-after-look', 1, [], -1),
]:
    normal = 'GATE_NORMAL_EXIT' in gate_flags
    events = [
        {'act': '$n steps into $p.', 'channel': 'TO_ROOM', 'anchor': 'ch', 'room': 'A'},
        {'act': 'You enter $p.' if normal else 'You walk through $p and find yourself somewhere else...',
         'channel': 'TO_CHAR', 'anchor': 'ch'},
        {'char_from_room': 'ch'}, {'char_to_room': ['ch', 'B']},
    ]
    if 'GATE_GOWITH' in gate_flags:
        events += [{'obj_from_room': 'P'}, {'obj_to_room': ['P', 'B']}]
    events += [{'act': '$n has arrived.' if normal else '$n has arrived through $p.',
                'channel': 'TO_ROOM', 'anchor': 'ch', 'room': 'B'},
               {'do_function': ['ch', 'do_look', 'auto'], 'charge_during_look': charge}]
    if charge > 0:
        events.append({'set': {'P.value[0]': charge - 1}})
        if after == -1:
            events += [{'set': {'P.value[0]': -1}},
                       {'act': '$p fades out of existence.', 'channel': 'TO_CHAR', 'anchor': 'ch'},
                       {'extract_obj': 'P'}]
    add('act_enter.c', 'do_enter', suffix,
        {**enter_base, 'room': {**enter_base['room'], 'vnum': 100, 'people': ['ch'], 'contents': ['P']},
         'destination': {'id': 'B', 'vnum': 200, 'people': [], 'room_flags': []},
         'portal': {**enter_base['portal'], 'value': [charge, 0, gate_flags, 200, 0]}},
        {'ordered_events_after_destination_resolution': events, 'ch.in_room': 'B',
         'portal_final_state': 'extracted' if after == -1 else {'value[0]': after, 'in_room': 'B' if normal else 'A'},
         'forbidden': ['follower dispatch', 'number_percent']},
        needle='char_from_room(ch)', controls={'get_obj_list': 'P', 'get_room_index(200)': 'B',
                                               'can_see_room': True, 'room_is_private': False,
                                               'act/do_function': 'Record delivery boundaries. do_look does not mutate the fixture.'})
    sites = ['or.005', 'or.006', 'and.005', 'if.009', 'and.006', 'and.007',
             'if.010', 'if.011', 'if.012', 'if.013', 'if.015', 'for.001',
             'if.020', 'and.013', 'return.008']
    if charge > 0:
        sites.append('if.014')
    if after == -1:
        sites += ['if.021', 'if.022']
    cases[-1]['branch_ids'].extend(f'act_enter.do_enter.{site}' for site in sites)

enter_early_sites = {
    'fighting-silent': 'if.001 return.001',
    'empty-argument': 'if.001 if.002 return.009',
    'no-object': 'if.002 if.003 return.002',
    'not-a-portal': 'if.003 if.004 or.001 return.003',
    'closed-mortal': 'if.004 or.001 and.001 return.003',
    'cursed-mortal': 'if.005 and.002 and.003 or.002 return.004',
}
for case in cases:
    file, fn, suffix = case['id'].split('.', 2)
    if file == 'act_enter' and fn == 'do_enter' and suffix in enter_early_sites:
        case['branch_ids'].extend(f'act_enter.do_enter.{site}' for site in enter_early_sites[suffix].split())

def portal_follower_case(suffix, follower, events, final, sites, *, charge=0, flags=(), law=False):
    add('act_enter.c', 'do_enter', suffix,
        {**enter_base, 'actor': {**enter_base['actor'], 'position': 'POS_STANDING'},
         'room': {**enter_base['room'], 'vnum': 100, 'people': ['ch', 'f', 'observer'], 'contents': ['P']},
         'destination': {'id': 'B', 'vnum': 200, 'people': [], 'room_flags': ['ROOM_LAW'] if law else []},
         'portal': {**enter_base['portal'], 'name': 'portal', 'contains': [], 'value': [charge, 0, list(flags), 200, 0]},
         'follower': {'id': 'f', 'kind': 'PC', 'master': 'ch', 'in_room': 'A', 'fighting': None,
                      'position': 'POS_STANDING', 'affected_by': [], 'act': [], 'on': None, **follower},
         'observer': {'id': 'observer', 'kind': 'PC', 'master': None, 'position': 'POS_STANDING'}},
        {'ordered_events_after_leader_move_and_look': events, 'ch.in_room': 'B',
         'unchanged': ['observer stays in A'], **final},
        needle='for ( fch = old_room->people',
        controls={'room_graph': 'Resolve fixed destination B. Both actors can see B. It is not private.',
                  'object_lookup': 'Visible keyword lookup in each actor’s current room. P is the only matching item.',
                  'do_look': 'Record the automatic look without mutation.',
                  'messages': 'Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.',
                  'stand_and_enter': 'Use real do_function dispatch and the real do_stand/do_enter paths.',
                  'extraction': 'P starts valid at the object-list head with prototype count 1 and no children.'})
    cases[-1]['branch_ids'].extend(f'act_enter.do_enter.{site}' for site in sites.split())


follow = [{'act': 'You follow $N.', 'channel': 'TO_CHAR', 'anchor': 'f', 'victim': 'ch'},
          {'do_function': ['f', 'do_enter', 'portal']}]
cross = [{'act': '$n steps into $p.', 'channel': 'TO_ROOM', 'anchor': 'f', 'room': 'A'},
         {'act': 'You walk through $p and find yourself somewhere else...', 'channel': 'TO_CHAR', 'anchor': 'f'},
         {'char_from_room': 'f'}, {'char_to_room': ['f', 'B']},
         {'act': '$n has arrived through $p.', 'channel': 'TO_ROOM', 'anchor': 'f', 'room': 'B'},
         {'do_function': ['f', 'do_look', 'auto']}]
portal_follower_case('standing-follower-reenters-by-keyword', {}, follow + cross,
                     {'f.in_room': 'B', 'P.in_room': 'A', 'P.value[0]': 0},
                     'if.016 or.007 if.017 and.008 if.018 and.010 if.019 and.011')
portal_follower_case('sitting-charmed-follower-stands-before-entry',
                     {'position': 'POS_SITTING', 'affected_by': ['AFF_CHARM'], 'on': 'bench'},
                     [{'do_function': ['f', 'do_stand', '']}, {'send_to_char': 'You stand up.\n\r', 'recipient': 'f'},
                      {'act': '$n stands up.', 'channel': 'TO_ROOM', 'anchor': 'f', 'room': 'A'},
                      {'set': {'f.position': 'POS_STANDING', 'f.on': None}}, *follow, *cross],
                     {'f.in_room': 'B', 'f.position': 'POS_STANDING', 'f.on': None, 'P.value[0]': 0},
                     'if.017 and.008 and.009 if.018')
portal_follower_case('magical-sleep-prevents-charmed-follower-entry',
                     {'position': 'POS_SLEEPING', 'affected_by': ['AFF_CHARM', 'AFF_SLEEP']},
                     [{'do_function': ['f', 'do_stand', '']}, {'send_to_char': "You can't wake up!\n\r", 'recipient': 'f'}],
                     {'f.in_room': 'A', 'f.position': 'POS_SLEEPING', 'P.value[0]': 0}, 'if.017 and.009 if.018')
portal_follower_case('uncharmed-sitting-follower-stays', {'position': 'POS_SITTING'}, [],
                     {'f.in_room': 'A', 'f.position': 'POS_SITTING', 'P.value[0]': 0}, 'if.017 and.008 if.018')
portal_follower_case('fighting-follower-gets-follow-notice-before-silent-return',
                     {'fighting': 'observer'}, follow,
                     {'f.in_room': 'A', 'f.fighting': 'observer', 'P.value[0]': 0},
                     'if.018 if.001 return.001')
portal_follower_case('aggressive-npc-follower-denied-by-city', {'kind': 'NPC', 'act': ['ACT_AGGRESSIVE']},
                     [{'act': "You can't bring $N into the city.", 'channel': 'TO_CHAR', 'anchor': 'ch', 'victim': 'f'},
                      {'act': "You aren't allowed in the city.", 'channel': 'TO_CHAR', 'anchor': 'f'}],
                     {'f.in_room': 'A', 'P.value[0]': 0}, 'if.019 and.011 and.012 continue.002', law=True)
portal_follower_case('moved-portal-follower-repeats-lookup-in-old-room', {},
                     [*follow, {'send_to_char': "You don't see that here.\n\r", 'recipient': 'f'}],
                     {'f.in_room': 'A', 'P.in_room': 'B', 'P.value[0]': 0},
                     'if.011 if.018 if.003 return.002', flags=['GATE_GOWITH'])
portal_follower_case('last-charge-skips-follower-and-notifies-origin', {},
                     [{'set': {'P.value[0]': 0}}, {'set': {'P.value[0]': -1}},
                      {'act': '$p fades out of existence.', 'channel': 'TO_CHAR', 'anchor': 'ch'},
                      {'act': '$p fades out of existence.', 'channel': 'TO_CHAR', 'anchor': 'f'},
                      {'act': '$p fades out of existence.', 'channel': 'TO_ROOM', 'anchor': 'f'},
                      {'extract_obj': 'P'}],
                     {'f.in_room': 'A', 'portal_final_state': 'removed from A and the world list, prototype count 0'},
                     'if.014 if.016 or.007 continue.001 if.020 if.021 if.022', charge=1)

add('act_enter.c', 'do_enter', 'nested-last-charge-leaves-outer-frame-with-recycled-portal',
    {**enter_base, 'room': {**enter_base['room'], 'vnum': 100, 'people': ['ch', 'f', 'observer'], 'contents': ['P']},
     'destination': {'id': 'B', 'vnum': 200, 'people': [], 'room_flags': []},
     'follower': {'id': 'f', 'kind': 'PC', 'master': 'ch', 'position': 'POS_STANDING', 'in_room': 'A', 'fighting': None},
     'observer': {'id': 'observer', 'master': None, 'position': 'POS_STANDING'},
     'portal': {**enter_base['portal'], 'name': 'portal', 'value': [2, 0, [], 200, 0], 'contains': [],
                'short_descr_storage': 'Shared db string space', 'short_descr': 'a shimmering portal'},
     'leader_connection': {'descriptor': 'connected', 'position': 'POS_STANDING'}},
    {'ordered_events': ['Leader moves and looks, then charge 2 becomes 1', 'Follower receives follow notice and reenters',
                        'Follower moves and looks, then charge 1 becomes 0 then -1',
                        'Nested fade act calls anchor on f for TO_CHAR, then observer for TO_CHAR and TO_ROOM',
                        'Nested extract_obj removes P from room and world list, decrements prototype count and recycles P',
                        'Outer frame skips observer, then repeats fade act calls anchored on ch and observer',
                        'Outer extract_obj finds no P in the world list and logs Extract_obj: obj 25 not found.'],
     'final': {'ch.in_room': 'B', 'f.in_room': 'B', 'observer.in_room': 'A', 'prototype.count': 0,
               'portal': 'invalid and on recycle list once'}},
    needle='if (portal != NULL && portal->value[0] == -1)',
    controls={'visibility': 'Both actors see B. The connected leader passes act position filtering and can_see_obj for P.',
              'room_private': False, 'look': 'No mutation', 'object_reuse': 'No allocation reuses P after nested extraction.',
              'object_list': 'P starts valid as the only world object, vnum 25, with prototype count 1.',
              'messages': 'Record act calls without expansion. Shared description is preserved by free_string.'},
)
cases[-1]['branch_ids'].extend(f'act_enter.do_enter.{site}' for site in
    'if.016 or.007 continue.001 if.020 and.013 if.021 if.022'.split())
for file, fn, needle in [
    ('handler.c', 'extract_obj', 'not found'),
    ('recycle.c', 'free_obj', 'INVALIDATE(obj)'),
    ('db.c', 'free_string', 'pstr >= string_space'),
]:
    function = index['src/' + file, fn]
    lines = (SOURCE / 'src' / file).read_text(encoding='latin1').splitlines()
    line = next(i + 1 for i in range(function['line'] - 1, function['end_line']) if needle in lines[i])
    cases[-1]['source_refs'].append(ref('src/' + file, fn, line))

for suffix, actor_flags, destination_flags, visible, private, expected, sites in [
    ('destination-invisible-before-privacy', {}, [], False, True,
     {'act': "$p doesn't seem to go anywhere.", 'channel': 'TO_CHAR', 'anchor': 'ch'},
     'or.005 return.005'),
    ('private-destination-rejects-trust-59', {'trust': 59}, [], True, True,
     {'act': "$p doesn't seem to go anywhere.", 'channel': 'TO_CHAR', 'anchor': 'ch'},
     'or.006 and.005 return.005'),
    ('aggressive-npc-directly-rejected-by-law', {'kind': 'NPC', 'act': ['ACT_IS_NPC', 'ACT_AGGRESSIVE']},
     ['ROOM_LAW'], True, False, {'send_to_char': 'Something prevents you from leaving...\n\r', 'recipient': 'ch'},
     'if.009 and.006 and.007 return.006'),
]:
    add('act_enter.c', 'do_enter', suffix,
        {**enter_base, 'actor': {**enter_base['actor'], **actor_flags},
         'destination': {'id': 'B', 'vnum': 200, 'room_flags': destination_flags}},
        {'ordered_events_after_lookup': [expected],
         'room_is_private_calls': ['B'] if visible else [],
         'unchanged': ['ch.in_room', 'P.in_room', 'P.value[0]'],
         'forbidden': ['move', 'do_look', 'extract_obj', 'follow dispatch']},
        needle='if (location == NULL', controls={'get_obj_list': 'P', 'get_room_index(200)': 'B',
                                                  'can_see_room': visible, 'room_is_private': private})
    cases[-1]['branch_ids'].extend(f'act_enter.do_enter.{site}' for site in sites.split())

# Distinguish a mismatched initial (no prefix comparison) from a matching
# initial with a failed prefix comparison (continue to the next row).
add('lookup.c', 'flag_lookup', 'same-initial-failed-prefix-continues',
    {'arguments': {'name': 'al', 'flag_table': [['amber', 2, True], ['alpha', 4, True], [None, 0, False]]}},
    {'return': 4, 'prefix_comparisons': [['al', 'amber'], ['al', 'alpha']], 'unchanged': ['table']},
    needle='!str_prefix')
add('lookup.c', 'flag_lookup', 'different-initial-skips-prefix-comparison',
    {'arguments': {'name': 'al', 'flag_table': [['beta', 2, True], [None, 0, False]]}},
    {'return': 0, 'prefix_comparisons': [], 'unchanged': ['table']},
    needle='LOWER(name[0])')
for fn, name, first, failure in [
    ('clan_lookup', 'lx', 'loner', 0), ('position_lookup', 'dx', 'dead', -1),
    ('sex_lookup', 'nx', 'none', -1), ('size_lookup', 'tx', 'tiny', -1),
]:
    add('lookup.c', fn, 'same-initial-failed-prefix', {'arguments': {'name': name}, 'table': 'Snapshot tables.c'},
        {'return': failure, 'prefix_comparisons': [[name, first]], 'unchanged': ['table']}, needle='!str_prefix')

lookup_misses = {
    'flag_lookup': {'empty-table', 'unknown', 'empty-name-does-not-match-nonempty', 'different-initial-skips-prefix-comparison'},
    'clan_lookup': {'unknown-indistinguishable-from-zero', 'same-initial-failed-prefix'},
    'position_lookup': {'empty', 'missing', 'longer', 'same-initial-failed-prefix'},
    'sex_lookup': {'empty', 'missing', 'same-initial-failed-prefix'},
    'size_lookup': {'empty', 'missing', 'same-initial-failed-prefix'},
}
for case in cases:
    file, fn, suffix = case['id'].split('.', 2)
    if file != 'lookup':
        continue
    sites = ['for.001']
    if suffix != 'empty-table':
        sites += ['if.001', 'and.001']
    sites.append('return.002' if suffix in lookup_misses[fn] else 'return.001')
    case['branch_ids'].extend(f'lookup.{fn}.{site}' for site in sites)

# Directional scanning advances only through the selected exit, even closed.
# When an exit is absent, the remaining iterations stay in the same room.
for door, direction in enumerate(('north', 'east', 'south', 'west', 'up', 'down')):
    for hops in (0, 1, 2):
        rooms = 'ABCD'
        exits = {rooms[i]: {'exit': {direction: {'to_room': rooms[i + 1], 'flags': ['EX_CLOSED']}}
                            if i < hops else {}} for i in range(hops + 1)}
        add('scan.c', 'do_scan', f'{direction}-long-with-{hops}-hops',
            {'actor': {'id': 'ch', 'in_room': 'A'}, 'argument': direction.upper() + ' ignored', 'rooms': exits},
            {'ordered_events': [
                {'act': 'You peer intently $T.', 'channel': 'TO_CHAR', 'arg2': direction},
                {'act': '$n peers intently $T.', 'channel': 'TO_ROOM', 'arg2': direction},
                *[{'scan_list': [rooms[i], 'ch', i, door]} for i in range(1, hops + 1)]],
             'unchanged': ['room membership', 'exits'],
             'forbidden': ['send formatted direction header', 'inspect other directions', 'random draws']},
            needle='for (depth = 1', controls={'scan_list': 'Record helper calls without rendering occupants.'})

add('scan.c', 'do_scan', 'null-exit-destination-fails-next-iteration',
    {'actor': {'id': 'ch', 'in_room': 'A'}, 'argument': 'n',
     'rooms': {'A': {'exit': {'north': {'to_room': None}}}}},
    {'defined_prefix': ['Emit directional acts', 'Call scan_list(NULL, ch, 1, 0), which returns immediately'],
     'portable_oracle': 'Unavailable after first hop. Depth two reads exit through a null scan_room.'},
    needle='pExit = scan_room->exit', blocked=True,
    questions=['The fixture tests a malformed exit. Establish loader invariants before treating this path as reachable in a loaded world.'])

add('scan.c', 'scan_char', 'pers-rechecks-visibility',
    {'arguments': {'victim': 'v', 'ch': 'ch', 'depth': 1, 'door': 0}, 'victim': {'kind': 'NPC', 'short_descr': 'a guard'}},
    {'ordered_events': [{'can_see': ['ch', 'v']}, {'send_to_char': 'someone, nearby to the north.\n\r', 'recipient': 'ch'}]},
    needle='PERS(victim', controls={'can_see': {'ordered_returns': [False]}, 'PERS': 'Evaluate the real macro.'})

for kind, name, rendered in [('NPC', 'a guard', 'a guard'), ('PC', 'Mira', 'Mira')]:
    add('scan.c', 'scan_char', f'pers-visible-{kind.lower()}',
        {'arguments': {'victim': 'v', 'ch': 'ch', 'depth': 0, 'door': 0},
         'victim': {'kind': kind, 'name': name if kind == 'PC' else 'guard',
                    'short_descr': name if kind == 'NPC' else 'unused'}},
        {'ordered_events': [{'can_see': ['ch', 'v']},
                            {'send_to_char': rendered + ', right here.\n\r', 'recipient': 'ch'}]},
        needle='PERS(victim', controls={'can_see': {'ordered_returns': [True]}, 'PERS': 'Evaluate the real macro.'})

add('scan.c', 'do_scan', 'around-null-destination-is-safe',
    {'actor': {'id': 'ch', 'in_room': 'A'}, 'argument': '',
     'rooms': {'A': {'exit': {'north': {'to_room': None}}, 'people_in_list_order': ['ch']}}},
    {'ordered_events': [{'act': '$n looks all around.', 'channel': 'TO_ROOM'},
                        {'send_to_char': 'Looking around you see:\n\r', 'recipient': 'ch'},
                        {'scan_list': ['A', 'ch', 0, -1]}, {'scan_list': [None, 'ch', 1, 0]}],
     'forbidden': ['scan_char', 'dereference null destination', 'movement']},
    needle='scan_list(pExit->u1.to_room', controls={'scan_list': 'Run the helper and record calls.'})

for case in cases:
    file, fn, suffix = case['id'].split('.', 2)
    if file != 'scan' or case['status'] == 'blocked':
        continue
    if fn == 'do_scan':
        sites = ['if.001']
        if suffix.startswith('around-'):
            sites += ['for.001', 'if.002', 'return.001']
        else:
            directions = ('north', 'east', 'south', 'west', 'up', 'down')
            invalid = suffix == 'invalid-direction'
            visited = 6 if invalid else directions.index(suffix.split('-')[0]) + 1
            for step in range(visited):
                sites += [f'if.{step + 3:03}', f'or.{step + 1:03}']
            sites += ['return.002'] if invalid else ['for.002', 'if.009', 'return.003']
    elif fn == 'scan_list':
        sites = ['if.001']
        if suffix == 'null-room':
            sites += ['return.001']
        else:
            sites += ['for.001', 'return.002']
            if suffix != 'empty':
                sites.append('if.002')
            if suffix == 'self-skipped':
                sites.append('continue.001')
            elif suffix != 'empty':
                sites += ['if.003', 'and.001']
                sites.append('continue.002' if suffix == 'pc-invis-too-high' else 'if.004')
    else:
        sites = ['return.001']
    case['branch_ids'].extend(f'scan.{fn}.{site}' for site in sites)

# Dispatch helpers return function pointers and preserve table ordering.
for suffix, name, function in [('first-full', 'spec_breath_any', 'spec_breath_any'), ('ambiguous-prefix-first', 'SPEC_BREATH', 'spec_breath_any'), ('last-full', 'spec_patrolman', 'spec_patrolman'), ('unknown', 'no_such_special', 'C NULL'), ('empty', '', 'C NULL')]:
    add('special.c', 'spec_lookup', suffix, {'arguments': {'name': name}, 'table': 'src/special.c spec_table in snapshot order, terminated by NULL name'}, {'return_function_pointer': function, 'forbidden': ['invoke returned function', 'messages', 'random draws']}, needle='LOWER(name[0])')
for suffix, function, name in [('first-function', 'spec_breath_any', 'spec_breath_any'), ('last-function', 'spec_patrolman', 'spec_patrolman'), ('null-function', 'C NULL', 'C NULL'), ('unregistered-function', 'unregistered_valid_function_pointer', 'C NULL')]:
    add('special.c', 'spec_name', suffix, {'arguments': {'function': function}, 'table': 'src/special.c spec_table'}, {'returned_name': name, 'forbidden': ['invoke function', 'messages']}, needle='function == spec_table')

from continuation_cases import extend_cases
extend_cases(add, cases)
from spec_name_completion import extend_cases as complete_spec_name_cases
complete_spec_name_cases(add, cases, SOURCE)

(OUT / 'cases.json').write_text(json.dumps({'schema_version': 1, 'cases': cases}, indent=2) + '\n', encoding='utf8')
print(f'Authored {len(cases)} cases')

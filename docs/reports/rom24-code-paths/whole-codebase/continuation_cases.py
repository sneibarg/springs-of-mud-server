"""Manually traced continuation; lexical links denote exercised sites, not MC/DC."""


def extend_cases(add, cases):
    from portal_continuation import extend_portal_cases
    extend_portal_cases(add, cases)
    for suffix, actor, result in [
        ('descriptor-without-original', {'kind': 'PC', 'level': 20, 'trust': 0, 'desc': {'original': None}}, 20),
        ('negative-trust-is-explicit', {'kind': 'PC', 'level': 20, 'trust': -1, 'desc': None}, -1),
        ('switched-original-trust-wins', {'kind': 'NPC', 'level': 60, 'trust': 60, 'desc': {'original': {'kind': 'PC', 'level': 20, 'trust': 55}}}, 55),
    ]:
        add('handler.c', 'get_trust', suffix, {'actor': actor}, {'return': result, 'unchanged': ['actor, original and descriptor']}, needle='ch->desc != NULL')
    for suffix, flags, people in [('private-zero', ['ROOM_PRIVATE'], []), ('private-and-solitary-one', ['ROOM_PRIVATE', 'ROOM_SOLITARY'], ['p'])]:
        add('handler.c', 'room_is_private', suffix, {'room': {'owner': '', 'room_flags': flags, 'people': people}},
            {'return': bool(people), 'unchanged': ['room and occupants']}, needle='count = 0')
    for suffix, text, token, rest in [
        ('whitespace-only', ' \t\r\n', '', ''),
        ('tab-leading', '\tLOOK north', 'look', 'north'),
        ('quote-followed-without-space', "'LOOK'north", 'look', 'north'),
        ('embedded-quote-unquoted', 'ab"cd tail', 'ab"cd', 'tail'),
        ('quoted-tab-preserved', '"a\tb" tail', 'a\tb', 'tail'),
        ('one-character-token', 'A', 'a', ''),
        ('max-fitting-token', 'A' * 255, 'a' * 255, ''),
    ]:
        add('interp.c', 'one_argument', suffix,
            {'arguments': {'argument': text, 'arg_first': '256-byte writable output buffer'}, 'locale': 'C locale, ASCII input'},
            {'output_token': token, 'returned_remainder': rest, 'unchanged': ['input bytes'], 'forbidden': ['messages', 'random draws']},
            needle="cEnd = ' '")
    add('interp.c', 'one_argument', 'output-buffer-overflow',
        {'arguments': {'argument': 'a' * 256, 'arg_first': '256-byte writable output buffer'}},
        {'limitation': 'Terminating NUL writes index 256 out of bounds; no portable return.'},
        needle="*arg_first = '\\0'", blocked=True,
        questions=['No capacity argument exists; callers must provide token length plus one bytes.'])

    for suffix, updates, immune, roll, threshold, result in [
        ('nonmana-pc', {'kind': 'PC', 'class_fMana': False}, 'IS_NORMAL', 49, 50, True),
        ('npc-does-not-index-class', {'kind': 'NPC', 'class': -1}, 'IS_NORMAL', 49, 50, True),
        ('berserk-odd-level-truncation', {'level': 21, 'affected_by': ['AFF_BERSERK']}, 'IS_NORMAL', 64, 65, True),
        ('vulnerable-below', {}, 'IS_VULNERABLE', 47, 48, True),
        ('mana-before-upper-clamp', {'kind': 'PC', 'class_fMana': True, 'saving_throw': -25}, 'IS_NORMAL', 90, 90, False),
        ('mana-negative-before-lower-clamp', {'kind': 'PC', 'class_fMana': True, 'saving_throw': 26}, 'IS_NORMAL', 4, 5, True),
        ('upper-cap-last-success', {'saving_throw': -100}, 'IS_NORMAL', 94, 95, True),
        ('immune-skips-invalid-class', {'kind': 'PC', 'class': -1}, 'IS_IMMUNE', None, None, True),
    ]:
        add('magic.c', 'saves_spell', suffix,
            {'arguments': {'level': 20, 'dam_type': 'DAM_FIRE'},
             'victim': {'kind': 'NPC', 'level': 20, 'saving_throw': 0, 'affected_by': [], 'class_fMana': False, **updates}},
            {'return': result, 'threshold_after_clamp': threshold, 'number_percent_calls': 0 if roll is None else 1, 'unchanged': ['victim'],
             'forbidden': ['class_table access'] if 'class' in updates else []},
            needle='save = 50', controls={'check_immune': {'returns': immune, 'kind': 'recorded helper boundary'},
                                        'number_percent': {'ordered_returns': [] if roll is None else [roll]},
                                        'class_table': 'Explicit class_fMana fixture where accessed.'})

    for suffix, field, member, word, mask, kind in [
        ('aff-field', 'aff', 'affected_by', 'blind', 1, 'PC'),
        ('immunity-field', 'immunity', 'imm_flags', 'fire', 128, 'PC'),
        ('resist-field', 'resist', 'res_flags', 'fire', 128, 'PC'),
        ('vuln-field', 'vuln', 'vuln_flags', 'fire', 128, 'PC'),
        ('form-field', 'form', 'form', 'edible', 1, 'NPC'),
        ('parts-field', 'parts', 'parts', 'head', 1, 'NPC'),
        ('comm-field', 'comm', 'comm', 'quiet', 1, 'PC'),
        ('plr-field', 'plr', 'act', 'permit', 1048576, 'PC'),
        ('ambiguous-a-selects-act', 'a', 'act', 'sentinel', 2, 'NPC'),
    ]:
        add('flags.c', 'do_flag', suffix,
            {'actor': {'id': 'admin', 'kind': 'PC', 'level': 1, 'trust': 0},
             'argument': f'char bob {field} + {word}',
             'victim': {'id': 'bob', 'kind': kind, 'zone': 'zone-A', 'all_flag_fields': 0, 'act': 1 if kind == 'NPC' else 0},
             'tables': 'Unmodified src/tables.c flag tables.'},
            {'result': {f'bob.{member}': mask | (1 if member == 'act' and kind == 'NPC' else 0), 'bob.zone': None},
             'unchanged': ['all unselected flag fields', 'actor'], 'forbidden': ['messages', 'trust check', 'persistence']},
            needle='old = *flag', controls={'get_char_world': 'Returns bob; world lookup is a recording boundary.', 'flag_lookup': 'Use real table lookup.'})
    add('flags.c', 'do_flag', 'operator-attached-consumes-word',
        {'argument': 'mob bob act +sentinel', 'actor': {'id': 'admin'}, 'victim': {'id': 'bob', 'act': 1, 'zone': 'zone-A'}},
        {'messages': [{'recipient': 'admin', 'text': 'Which flags do you wish to change?\n\r'}],
         'unchanged': ['bob.act', 'bob.zone'], 'forbidden': ['get_char_world']}, needle="type == '='")

    for fn, suffix, expected in [
        ('substitute_alias', 'loaded-uppercase-not-substituted', {'interpret': {'actor': 'ch', 'argument': 'X'}, 'unchanged': ['aliases']}),
        ('do_alias', 'loaded-uppercase-query-found', {'messages': [{'recipient': 'ch', 'text': "X aliases to 'look'.\n\r"}], 'unchanged': ['aliases']}),
        ('do_unalias', 'loaded-uppercase-not-removed', {'messages': [{'recipient': 'ch', 'text': 'No alias of that name to remove.\n\r'}], 'unchanged': ['aliases']}),
    ]:
        add('alias.c', fn, suffix,
            {'argument': 'X', 'descriptor': {'character': 'ch', 'original': None},
             'actor': {'id': 'ch', 'kind': 'PC', 'prefix': '', 'desc': 'descriptor', 'aliases': [['X', 'look']]},
             'storage': 'Remaining four slots NULL. A saved Alias X look~ record is loaded without normalizing X.'},
            expected, needle='strcmp' if fn != 'do_alias' else 'if (!str_cmp(arg',
            controls={'interpret': 'Recording boundary.', 'string_helpers': 'Real ASCII parsing and comparison.'})
        cases[-1]['source_refs'].append({'file': 'src/save.c', 'function': 'fread_char', 'line': 784})

    for suffix, a, b, result, calls in [
        ('first-character-match-rest-mismatch', 'ab', 'ac', True, ['ac']),
        ('retry-after-partial-match', 'ab', 'acab', False, ['acab', 'ab']),
        ('one-character', 'a', 'A', False, ['A']),
        ('empty-both', '', '', False, []),
    ]:
        add('db.c', 'str_infix', suffix, {'arguments': {'astr': a, 'bstr': b}},
            {'return': result, 'ordered_str_prefix_candidates': calls,
             'unchanged': ['input strings'], 'forbidden': ['output', 'random draws']},
            needle="c0 = LOWER", controls={'str_prefix': 'Execute real helper; record candidate arguments.'})
    add('db.c', 'capitalize', 'shared-buffer-overwritten',
        {'first_input': 'HELLO', 'second_input': 'x'},
        {'ordered_results': ['Hello', 'X'], 'pointer_identity': 'Both returns identify the same static array.',
         'first_pointer_after_second_call': 'X', 'unchanged': ['both input arrays']},
        needle='static char strcap', action='Call capitalize("HELLO"), retain its pointer, then call capitalize("x").')
    add('db.c', 'capitalize', 'maximum-fitting-input', {'arguments': {'str': 'a' * 4607}},
        {'result_string': 'A' + 'a' * 4606, 'terminator_index': 4607}, needle='strcap[i]')
    add('db.c', 'capitalize', 'static-buffer-overflow', {'arguments': {'str': 'a' * 4608}},
        {'limitation': 'The terminating NUL is written beyond the 4608-byte static array; no portable result.'},
        needle="strcap[i] = '\\0'", blocked=True,
        questions=['Undefined out-of-bounds write. A target length policy needs a separate decision.'])
    for suffix, lo, hi, draws, result in [
        ('zero-lower-nonzero-upper', 0, 1, [1], 1),
        ('power-loop-zero-iterations', 5, 6, [2], 5),
        ('exact-power-domain', 1, 4, [3], 4),
    ]:
        add('db.c', 'number_range', suffix, {'arguments': {'from': lo, 'to': hi}},
            {'return': result, 'ordered_consumed_draws': draws, 'number_mm_calls': len(draws)},
            needle='for ( power', controls={'number_mm': {'kind': 'entropy boundary', 'ordered_returns': draws}})
    add('db.c', 'dice', 'negative-size', {'arguments': {'number': 2, 'size': -3}},
        {'return': 2, 'ordered_number_range_calls': [[1, -3], [1, -3]], 'number_mm_calls': 0},
        needle='sum += number_range', controls={'number_range': 'Run real helper: reversed domain returns 1 without entropy.'})
    for width in [-1, 31, 32]:
        add('db.c', 'number_bits', f'invalid-shift-{width}',
            {'arguments': {'width': width}, 'platform': '32-bit signed int'},
            {'limitation': 'Negative shift, unrepresentable signed left shift, or shift at type width; no portable return.'},
            needle='return number_mm', blocked=True,
            controls={'number_mm': 'Returns 0; operand evaluation order is unspecified.'},
            questions=['Undefined shift; the C helper does not validate the width.'])
    # These values expose different overflow operations, without asserting machine wraparound.
    for fn, suffix, args, needle in [
        ('number_range', 'domain-subtraction-overflow', {'from': -2147483648, 'to': 2147483647}, 'to = to - from'),
        ('number_range', 'power-growth-overflow', {'from': 0, 'to': 1073741824}, 'power <<= 1'),
        ('number_fuzzy', 'increment-overflow', {'number': 2147483647}, 'case 3:'),
        ('interpolate', 'product-overflow', {'level': 2147483647, 'value_00': 0, 'value_32': 2}, 'return value_00'),
    ]:
        add('db.c', fn, suffix, {'arguments': args, 'platform': '32-bit signed int'},
            {'limitation': 'Signed overflow has no portable result; do not assert wrapped arithmetic.'},
            needle=needle, blocked=True, controls={'number_bits': 'Returns 3 if called.', 'number_mm': 'Must not be reached before the identified overflow.'},
            questions=['Undefined signed arithmetic outside the safe direct-helper domain.'])

    # Follow the actual stdio parsers rather than assuming well-formed ban records.
    parser_platform = 'C locale, 8-bit signed char with EOF=-1 preserved when stored in char; successful file open and allocations.'
    for suffix, content, expected in [
        ('empty-file-parser-exits', '', {'ordered_events': ['new_ban', 'fread_word fills its buffer with EOF bytes', 'bug("Fread_word: word too long.",0)', 'exit(1)'], 'forbidden': ['append ban', 'normal return']}),
        ('whitespace-only-parser-exits', ' \t\n', {'ordered_events': ['new_ban', 'fread_word skips initial whitespace then fills buffer with EOF bytes', 'bug("Fread_word: word too long.",0)', 'exit(1)'], 'forbidden': ['append ban', 'normal return']}),
        ('bad-level-parser-exits', 'example.org x A\n', {'ordered_events': ['new_ban', 'store name example.org', 'bug("Fread_number: bad format.",0)', 'exit(1)'], 'forbidden': ['append ban', 'normal return']}),
        ('no-final-newline-does-not-terminate', 'example.org 10 A', {'ordered_events': ['new_ban', 'store name example.org', 'store level 10', 'store ban_flags 1', 'fread_to_eol repeatedly reads EOF'], 'control': 'No return: EOF is neither newline nor carriage return.', 'forbidden': ['append ban', 'fclose', 'next allocation']}),
        ('trailing-spaces-create-phantom-record', 'example.org 10 A\n  ', {'ordered_events': ['append first record example.org, level 10, flags 1', 'new_ban for second record', 'bug("Fread_word: word too long.",0)', 'exit(1)'], 'ban_list_before_exit': ['example.org'], 'forbidden': ['append second record', 'normal return']}),
        ('invalid-flag-character-is-zero', 'example.org 10 ?\n', {'ordered_events': ['new_ban', 'store name example.org', 'store level 10', 'fread_flag returns 0 and pushes back ?', 'fread_to_eol consumes ? and newline, then reads EOF', 'append record', 'fclose', 'return'], 'ban_list': [{'name': 'example.org', 'level': 10, 'ban_flags': 0}]}),
        ('duplicate-letter-flags-add', 'example.org 10 AA\n', {'ordered_events': ['new_ban', 'parse name example.org, level 10, flags 2', 'append record', 'fclose', 'return'], 'ban_list': [{'name': 'example.org', 'level': 10, 'ban_flags': 2}], 'quirk': 'Flag letters are added, not bitwise ORed.'}),
    ]:
        add('ban.c', 'load_bans', suffix,
            {'file_bytes': content, 'ban_list': [], 'ban_free': [], 'platform': parser_platform}, expected,
            needle='pban->name = str_dup',
            controls={'parsers': 'Run fread_word, fread_number, fread_flag, flag_convert and fread_to_eol; no parser stubs.', 'allocation': 'Successful recording boundary.', 'stdio': 'Byte stream with persistent EOF; exit is captured as termination, not return.'})
        cases[-1]['source_refs'] += [
            {'file': 'src/db.c', 'function': fn, 'line': ln}
            for fn, ln in [('fread_word', 2524), ('fread_number', 2166), ('fread_flag', 2214), ('fread_to_eol', 2499)]]

    # A recycled name can remain readable when it belongs to the shared string arena.
    add('ban.c', 'ban_site', 'replacement-walks-recycle-list',
        {'actor': {'id': 'admin', 'trust': 60}, 'argument': 'example.org all', 'fPerm': False,
         'ban_list': [{'id': 'old', 'name': 'example.org', 'level': 60, 'valid': True, 'next': 'tail'},
                      {'id': 'tail', 'name': 'unrelated.org', 'level': 60, 'valid': True, 'next': None}],
         'ban_free': [{'id': 'free1', 'name': 'recycled.org', 'valid': False, 'next': None}],
         'string_storage': 'All existing names are immutable shared database strings; free_string leaves these bytes unchanged.'},
        {'ordered_events': ['unlink old; live head becomes tail', 'free_ban(old) changes old.next to free1 and free-list head to old', 'replacement loop compares free1.name, then terminates without visiting tail', 'new_ban reuses old and leaves free1 as free-list head', 'assign new name, level 60 and BAN_ALL', 'prepend old before tail', 'save_bans', 'send example.org has been banned.\n\r to admin'],
         'result_list': ['old', 'tail'], 'result_free_list': ['free1'], 'forbidden': ['compare tail.name', 'message to other characters']},
        needle='free_ban(pban)', controls={'get_trust': 'Returns 60.', 'save_bans': 'Recording persistence boundary.', 'recycler': 'Execute new_ban/free_ban; allocation succeeds.', 'str_dup': 'Allocation boundary returns an owned copy of the requested name; do not execute unrelated-pointer ordering comparisons in the allocator.'})
    cases[-1]['source_refs'] += [{'file': 'src/recycle.c', 'function': 'free_ban', 'line': 98}, {'file': 'src/recycle.c', 'function': 'new_ban', 'line': 79}]

    reconcile_helpers(cases)
    # Reconcile only the sites executed by each concrete case; blocked paths retain semantic IDs.
    for case in cases:
        file, fn, suffix = case['id'].split('.', 2)
        if file != 'db' or case['status'] != 'specified':
            continue
        args = case['fixture'].get('arguments', {})
        sites = []
        if fn in ('str_cmp', 'str_prefix'):
            sites = ['if.001']
            if suffix in ('null-left', 'both-null-left-dominates'):
                sites += ['return.001']
            else:
                sites += ['if.002']
                if suffix == 'null-right':
                    sites += ['return.002']
                else:
                    sites += ['for.001']
                    if fn == 'str_cmp':
                        sites += ['or.001']
                    if args['astr'] or (fn == 'str_cmp' and args['bstr']):
                        sites += ['if.003']
                    sites += ['return.003' if case['expected']['return'] else 'return.004']
        elif fn == 'str_infix':
            sites = ['if.001']
            if not args['astr']:
                sites += ['return.001']
            else:
                sites += ['for.001']
                if len(args['astr']) <= len(args['bstr']):
                    sites += ['if.002', 'and.001']
                sites += ['return.003' if case['expected']['return'] else 'return.002']
        elif fn == 'str_suffix':
            sites = ['if.001', 'and.001', 'return.002' if case['expected']['return'] else 'return.001']
        elif fn == 'number_range':
            sites = ['if.001', 'and.001']
            if args['from'] == args['to'] == 0:
                sites += ['return.001']
            else:
                sites += ['if.002']
                sites += ['return.002'] if args['to'] <= args['from'] else ['for.001', 'while.001', 'return.003']
        elif fn in ('number_percent', 'number_door'):
            sites = ['while.001', 'return.001']
        elif fn in ('number_bits', 'interpolate'):
            sites = ['return.001']
        elif fn == 'number_fuzzy':
            sites = ['switch.001', 'return.001']
            draw = case['controls']['number_bits']['ordered_returns'][0]
            if draw in (0, 3):
                n = 1 if draw == 0 else 2
                sites += [f'case.{n:03}', f'break.{n:03}']
        elif fn == 'dice':
            sites = ['switch.001']
            if args['size'] in (0, 1):
                n = args['size'] + 1
                sites += [f'case.{n:03}', f'return.{n:03}']
            else:
                sites += ['for.001', 'return.003']
        elif fn == 'capitalize':
            sites = ['for.001', 'return.001']
        elif fn == 'smash_tilde':
            sites = ['for.001', 'return.001']
            if args['str']:
                sites += ['if.001']
        case['branch_ids'].extend(f'db.{fn}.{s}' for s in sites)


def reconcile_helpers(cases):
    for case in cases:
        file, fn, suffix = case['id'].split('.', 2)
        if case['status'] != 'specified':
            continue
        fixture = case['fixture']
        sites = []
        if file == 'interp' and fn == 'one_argument':
            text = fixture['arguments']['argument'].lstrip()
            sites = ['while.001', 'if.001', 'or.001', 'while.002', 'while.003', 'return.001']
            quoted = bool(text and text[0] in "\"'")
            body = text[1:] if quoted else text
            if body:
                sites += ['if.002']
            if (text[0] if quoted else ' ') in body:
                sites += ['break.001']
        elif file == 'magic' and fn == 'saves_dispel':
            sites = ['if.001', 'return.001']
        elif file == 'magic' and fn == 'saves_spell':
            sites = ['if.001', 'switch.001']
            immune = case['controls']['check_immune']['returns']
            if immune == 'IS_IMMUNE':
                sites += ['case.001', 'return.001']
            else:
                if immune in ('IS_RESISTANT', 'IS_VULNERABLE'):
                    n = 2 if immune == 'IS_RESISTANT' else 3
                    sites += [f'case.{n:03}', f'break.{n - 1:03}']
                sites += ['if.002', 'and.001', 'return.002']
        elif file == 'special' and fn in ('spec_lookup', 'spec_name'):
            sites = ['for.001', 'if.001']
            if fn == 'spec_lookup':
                sites += ['and.001']
                result = case['expected']['return_function_pointer']
            else:
                result = case['expected']['returned_name']
            sites += ['return.002' if result == 'C NULL' else 'return.001']
        elif file == 'handler':
            if fn == 'is_clan':
                sites = ['return.001']
            elif fn == 'is_same_clan':
                sites = ['if.001', 'return.001' if fixture['actor']['clan'] in (0, 1) else 'return.002']
            elif fn == 'get_trust':
                actor = fixture['actor']
                sites = ['if.001', 'and.001', 'if.002']
                if actor.get('desc') and actor['desc'].get('original'):
                    actor = actor['desc']['original']
                if actor['trust']:
                    sites += ['return.001']
                else:
                    sites += ['if.003', 'and.002', 'return.002' if actor['kind'] == 'NPC' and actor['level'] >= 51 else 'return.003']
            elif fn == 'can_drop_obj':
                sites = ['if.001']
                if 'ITEM_NODROP' not in fixture['object']['extra_flags']:
                    sites += ['return.001']
                else:
                    sites += ['if.002', 'and.001', 'return.002' if case['expected']['return'] else 'return.003']
            elif fn == 'deduct_cost':
                sites = ['if.001', 'if.002', 'if.003']
            elif fn == 'room_is_dark':
                room = fixture['room']
                sites = ['if.001']
                if room['light'] > 0:
                    sites += ['return.001']
                else:
                    sites += ['if.002']
                    if 'ROOM_DARK' in room['room_flags']:
                        sites += ['return.002']
                    else:
                        sites += ['if.003', 'or.001']
                        if room['sector_type'] in ('SECT_INSIDE', 'SECT_CITY'):
                            sites += ['return.003']
                        else:
                            sites += ['if.004', 'or.002', 'return.004' if case['expected']['return'] else 'return.005']
            elif fn == 'room_is_private':
                room = fixture['room']
                sites = ['if.001', 'and.001']
                owner = room['owner']
                if owner and not isinstance(owner, dict):
                    sites += ['return.001']
                else:
                    sites += ['for.001', 'if.002', 'and.002']
                    flags, count = room['room_flags'], len(room['people'])
                    if 'ROOM_PRIVATE' in flags and count >= 2:
                        sites += ['return.002']
                    else:
                        sites += ['if.003', 'and.003']
                        if 'ROOM_SOLITARY' in flags and count >= 1:
                            sites += ['return.003']
                        else:
                            sites += ['if.004', 'return.004' if 'ROOM_IMP_ONLY' in flags else 'return.005']
        case['branch_ids'].extend(f'{file}.{fn}.{s}' for s in sites)

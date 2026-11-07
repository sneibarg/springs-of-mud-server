"""Source-reviewed room darkness truth table and six caller contracts."""
import hashlib

HASHES = {
    'src/handler.c': '0e95a3bd6480448855bba8d7cae6b6f8b5aad3d2be2738a21cd58571f7bf2261',
    'src/merc.h': '080da51df18acf5fac5540cbe03dea9d44aeda7cb47e920a928a28fad83e7937',
}
SUNS = ('SUN_DARK', 'SUN_RISE', 'SUN_LIGHT', 'SUN_SET')
SECTORS = ('SECT_INSIDE', 'SECT_CITY', 'SECT_FIELD', 'SECT_FOREST', 'SECT_HILLS',
           'SECT_MOUNTAIN', 'SECT_WATER_SWIM', 'SECT_WATER_NOSWIM', 'SECT_UNUSED', 'SECT_AIR', 'SECT_DESERT')
DAY_ROWS = ((False, False, False, False), (False, False, False, False)) + ((True, False, False, True),) * 9


def check_source(source):
    for path, digest in HASHES.items():
        assert hashlib.sha256((source / path).read_bytes()).hexdigest() == digest, path


def extend_cases(add, cases, source):
    check_source(source)
    existing = {(c['fixture']['room']['sector_type'], c['fixture']['weather_info']['sunlight'])
                for c in cases if c['id'].startswith('handler.room_is_dark.')
                and c['fixture']['room']['light'] == 0 and not c['fixture']['room']['room_flags']}

    def new(suffix, light, flags, sector, sun, result):
        add('handler.c', 'room_is_dark', suffix,
            {'room': {'light': light, 'room_flags': flags, 'sector_type': sector}, 'weather_info': {'sunlight': sun}},
            {'return': result}, needle='light > 0')

    for i, sector in enumerate(SECTORS):
        for j, sun in enumerate(SUNS):
            if (sector, sun) not in existing:
                new(f'matrix-{sector.lower()}-{sun.lower()}', 0, [], sector, sun, DAY_ROWS[i][j])
    for light, result in [(-32768, True), (-1, True), (0, True), (1, False), (32767, False)]:
        new(f'light-boundary-{light}-dark-inside', light, ['ROOM_DARK'], 'SECT_INSIDE', 'SUN_LIGHT', result)
    for light in (-32768, -1):
        for sun, result in [('SUN_LIGHT', False), ('SUN_DARK', True)]:
            new(f'negative-light-{light}-{sun.lower()}', light, [], 'SECT_FIELD', sun, result)
    new('unrelated-flag-does-not-light-room', 0, ['ROOM_SAFE'], 'SECT_FIELD', 'SUN_DARK', True)
    new('unknown-sunlight-falls-through', 0, [], 'SECT_FIELD', 99, False)
    new('unknown-sector-uses-weather', 0, [], 99, 'SUN_DARK', True)

    for case in cases:
        if not case['id'].startswith('handler.room_is_dark.'):
            continue
        room = case['fixture']['room']
        sites, reads = ['if.001'], ['room.light']
        if room['light'] > 0:
            result_site, ln = 'return.001', 2359
        else:
            sites += ['if.002']
            reads += ['room.room_flags']
            if 'ROOM_DARK' in room['room_flags']:
                result_site, ln = 'return.002', 2362
            else:
                sites += ['if.003', 'or.001']
                reads += ['room.sector_type']
                if room['sector_type'] in ('SECT_INSIDE', 'SECT_CITY'):
                    result_site, ln = 'return.003', 2366
                else:
                    sites += ['if.004', 'or.002']
                    reads += ['weather_info.sunlight']
                    result_site, ln = ('return.004', 2370) if case['expected']['return'] else ('return.005', 2372)
        case['branch_ids'] = [case['id'] + '.path'] + [f'handler.room_is_dark.{s}' for s in sites + [result_site]]
        case['source_refs'] = [{'file': 'src/handler.c', 'function': 'room_is_dark', 'line': n} for n in (2358, ln)]
        case['entry'] = {'function': 'room_is_dark', 'route': 'Direct helper call.',
                         'caller_prerequisites': 'Non-NULL readable room. Field values and global sunlight are explicit. No actor, position, vision effect, descriptor or trust requirement.',
                         'return_domain': 'Boolean environmental darkness, not actor visibility.'}
        case['controls'] = {'collaborators': 'No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.',
                            'weather': 'Fixed global sunlight; no scheduler invocation or wall-clock lookup.', 'randomness': 'None.'}
        case['expected'].update({'read_dependencies_in_order': reads,
                                 'unchanged': ['room', 'weather', 'all entities'],
                                 'forbidden': ['messages', 'allocation', 'RNG', 'clock reads', 'actor visibility checks', 'writes'],
                                 'unread_dependencies': [f for f in ('room.room_flags', 'room.sector_type', 'weather_info.sunlight') if f not in reads]})
        case['adaptation'] = {'Python': 'area.Room.is_room_dark, with explicit room fields, enums and controlled CharacterApi._weather provider; assert Boolean and no world mutations. Do not inherit actor vision rules.', 'approved_overrides': []}


def validate_cases(cases):
    selected = [c for c in cases if c['id'].startswith('handler.room_is_dark.')]
    assert len(selected) == 59
    for i, sector in enumerate(SECTORS):
        for j, sun in enumerate(SUNS):
            matches = [c for c in selected if c['fixture']['room'] == {'light': 0, 'room_flags': [], 'sector_type': sector}
                       and c['fixture']['weather_info']['sunlight'] == sun]
            assert len(matches) == 1 and matches[0]['expected']['return'] is DAY_ROWS[i][j]
    assert all(c['status'] == 'specified' and not c['open_questions'] for c in selected)
    return len(selected)


def complete(functions, cases, source):
    check_source(source)
    count = validate_cases(cases)
    fn = next(f for f in functions if (f['file'], f['name']) == ('src/handler.c', 'room_is_dark'))
    assert {(r['file'], r['line']) for r in fn['entry_routes']} == {
        ('src/act_info.c', 510), ('src/act_info.c', 1013), ('src/act_info.c', 1356),
        ('src/comm.c', 1423), ('src/handler.c', 2462), ('src/handler.c', 2518), ('src/merc.h', 2250)}
    assert all(b['disposition'] == 'specified' and b['case_ids'] for b in fn['branch_ledger'])
    fn.pop('local_ledger_review', None)
    fn['status'] = 'traced'
    fn['completion_review'] = {'status': 'complete', 'evidence': 'static_trace', 'case_count': count,
        'notes': 'darkness-completion.md', 'remaining_gaps': [],
        'coverage': 'All 11 sectors by all four sun states; strict light boundary and signed extremes; dark flag precedence; unrelated flags; nonenum scalar fallthrough; ordered dependency reads.',
        'dependencies': ['merc.h IS_SET, ROOM_DARK, SECT_INSIDE/CITY and SUN_SET/DARK constants; global weather_info.sunlight. No callees.'],
        'entry_routes': [
            {'file': 'src/act_info.c', 'line': 510, 'caller': 'show_char_to_char', 'disposition': 'reviewed', 'contract': 'After self/trust skips and failed can_see; darkness and target AFF_INFRARED emit glowing-eyes message to observer.'},
            {'file': 'src/act_info.c', 'line': 1013, 'caller': 'do_look', 'disposition': 'reviewed', 'contract': 'After descriptor, position, blindness guards; non-NPC without holylight checks darkness, prints pitch black, lists characters and returns before parsing input.'},
            {'file': 'src/act_info.c', 'line': 1356, 'caller': 'do_exits', 'disposition': 'reviewed', 'contract': 'Non-auto mode only, for existing non-NULL visible open destinations; selects Too dark to tell versus destination name.'},
            {'file': 'src/comm.c', 'line': 1423, 'caller': 'bust_a_prompt', 'disposition': 'reviewed', 'contract': '%r with a room, no PC holylight bypass, and not blind; picks room name versus darkness.'},
            {'file': 'src/handler.c', 'line': 2462, 'caller': 'can_see', 'disposition': 'reviewed', 'contract': 'After self/trust/incognito/holylight/immortal-NPC/blindness gates; darkness denies without AFF_INFRARED.'},
            {'file': 'src/handler.c', 'line': 2518, 'caller': 'can_see_obj', 'disposition': 'reviewed', 'contract': 'After holylight/death visibility/blindness/potion/light/invisibility/glow gates; darkness denies without AFF_DARK_VISION.'},
            {'file': 'src/merc.h', 'line': 2250, 'disposition': 'declaration_only'},
        ],
        'limitations': ['NULL room violates the immediate room.light read precondition.', 'Full visibility/network/scheduler behavior belongs to independent caller reports.'],
    }

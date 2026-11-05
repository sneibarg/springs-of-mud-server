"""Portal lookup and nested linked-list mutation traces, at message-call boundaries."""


def extend_portal_cases(add, cases):
    actor = {'kind': 'PC', 'level': 30, 'trust': 0, 'desc': None, 'fighting': None,
             'position': 'POS_STANDING', 'affected_by': [], 'act': [], 'on': None,
             'equipment': [], 'in_room': 'A'}
    portal = {'item_type': 'ITEM_PORTAL', 'name': 'portal', 'extra_flags': [],
              'value': [0, 0, 0, 200, 0], 'in_room': 'A', 'contains': []}
    controls = {
        'lookup': 'Execute get_obj_list, number_argument, is_name, one_argument and can_see_obj; all rooms lit. Resolve vnums 100/200/300 to A/B/C. No room is private.',
        'movement': 'Execute char_from_room/char_to_room: unlink and clear next pointer, then prepend to destination people. No lights, plague or equipped objects.',
        'do_function': 'Execute actual dispatcher and recursive do_enter; automatic do_look is a recording boundary without mutation.',
        'messages': 'Record act template, actor, object, target and channel; delivery/rendering are separate pending contracts.',
        'randomness': 'No random calls permitted.',
    }

    def cross(who, gate, origin, destination):
        return [
            {'act': '$n steps into $p.', 'actor': who, 'object': gate, 'channel': 'TO_ROOM', 'room': origin},
            {'act': 'You walk through $p and find yourself somewhere else...', 'actor': who, 'object': gate, 'channel': 'TO_CHAR'},
            {'char_from_room': who}, {'char_to_room': [who, destination]},
            {'act': '$n has arrived through $p.', 'actor': who, 'object': gate, 'channel': 'TO_ROOM', 'room': destination},
            {'do_function': [who, 'do_look', 'auto']},
        ]

    def follow(who, leader, argument='portal'):
        return [{'act': 'You follow $N.', 'actor': who, 'victim': leader, 'channel': 'TO_CHAR'},
                {'do_function': [who, 'do_enter', argument]}]

    room_base = {'room_flags': [], 'light': 1, 'owner': '', 'sector_type': 'SECT_INSIDE'}
    rooms = {'A': {**room_base, 'vnum': 100, 'people': ['ch', 'f', 'g', 'observer'], 'contents': ['P'], 'area': 'areaA'},
             'B': {**room_base, 'vnum': 200, 'people': [], 'contents': [], 'area': 'areaB'}}
    add('act_enter.c', 'do_enter', 'grandchild-mutation-revisits-moved-follower',
        {'argument': 'portal', 'actor': 'ch', 'rooms': rooms,
         'characters': {'ch': {**actor, 'master': None}, 'f': {**actor, 'master': 'ch'},
                        'g': {**actor, 'master': 'f'}, 'observer': {**actor, 'master': None}},
         'objects': {'P': portal}, 'areas': {'areaA': {'nplayer': 4, 'empty': False, 'age': 10},
                                           'areaB': {'nplayer': 0, 'empty': False, 'age': 10}}},
        {'ordered_events': [*cross('ch', 'P', 'A', 'B'), *follow('f', 'ch'), *cross('f', 'P', 'A', 'B'),
                            *follow('g', 'f'), *cross('g', 'P', 'A', 'B'), *follow('f', 'ch'),
                            {'send_to_char': "You don't see that here.\n\r", 'recipient': 'f'}],
         'outer_loop_visited_ids': ['f', 'g', 'f', 'ch'],
         'explanation': 'Outer cached next is g. Recursive f moves g; g.next_in_room becomes f in B. Returning outer frame resumes g and follows its new link to f, then ch.',
         'final_people': {'A': ['observer'], 'B': ['g', 'f', 'ch']},
         'final_area_nplayer': {'areaA': 1, 'areaB': 3},
         'unchanged': ['room light', 'area ages and empty flags', 'P remains in A with zero unlimited charges', 'master pointers'],
         'forbidden': ['portal extraction', 'extra movement after g enters B', 'do_stand', 'random draws']},
        needle='fch_next = fch->next_in_room', controls=controls)
    cases[-1]['branch_ids'] += ['act_enter.do_enter.for.001', 'act_enter.do_enter.if.018', 'act_enter.do_enter.if.003', 'act_enter.do_enter.return.002']
    cases[-1]['source_refs'] += [
        {'file': 'src/handler.c', 'function': 'char_from_room', 'line': 1367},
        {'file': 'src/handler.c', 'function': 'char_to_room', 'line': 1395},
        {'file': 'src/handler.c', 'function': 'get_obj_list', 'line': 2100},
    ]

    for suffix, argument, q_type, outcome in [
        ('moved-gate-exposes-nonportal-name-match', 'portal', 'ITEM_WEAPON', "You can't seem to find a way in.\n\r"),
        ('ordinal-repeated-after-gate-moves', '2.portal', 'ITEM_PORTAL', "You don't see that here.\n\r"),
    ]:
        first_order = ['Q', 'P'] if argument.startswith('2.') else ['P', 'Q']
        lead_events = cross('ch', 'P', 'A', 'B')
        lead_events[4:4] = [{'obj_from_room': 'P'}, {'obj_to_room': ['P', 'B']}]
        add('act_enter.c', 'do_enter', suffix,
            {'argument': argument, 'actor': 'ch',
             'characters': {'ch': {**actor, 'master': None}, 'f': {**actor, 'master': 'ch'}, 'observer': {**actor, 'master': None}},
             'rooms': {'A': {**rooms['A'], 'people': ['ch', 'f', 'observer'], 'contents': first_order}, 'B': rooms['B']},
             'areas': {'areaA': {'nplayer': 3, 'empty': False, 'age': 10}, 'areaB': {'nplayer': 0, 'empty': False, 'age': 10}},
             'objects': {'P': {**portal, 'value': [0, 0, ['GATE_GOWITH'], 200, 0]},
                         'Q': {**portal, 'item_type': q_type}}},
            {'ordered_events': [*lead_events, *follow('f', 'ch', argument), {'send_to_char': outcome, 'recipient': 'f'}],
             'lookup_results_in_order': ['P', None if argument.startswith('2.') else 'Q'],
             'final_people': {'A': ['f', 'observer'], 'B': ['ch']}, 'final_contents': {'A': ['Q'], 'B': ['P']},
             'final_area_nplayer': {'areaA': 2, 'areaB': 1},
             'unchanged': ['both charge fields remain zero', 'master pointers', 'Q location', 'room light'],
             'forbidden': ['follower movement', 'portal extraction', 'random draws']},
            needle='get_obj_list( ch, argument', controls=controls)
        cases[-1]['source_refs'] += [
            {'file': 'src/handler.c', 'function': 'get_obj_list', 'line': 2096},
            {'file': 'src/handler.c', 'function': 'is_name', 'line': 809},
            {'file': 'src/interp.c', 'function': 'number_argument', 'line': 663},
        ]

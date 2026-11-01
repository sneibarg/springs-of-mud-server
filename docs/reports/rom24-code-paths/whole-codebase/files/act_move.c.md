# src/act_move.c

Role: translation_unit. Disposition: **pending**. SHA-256: `06b4d6632a4e637d787b555182f1acf599fe435dac01adc71f21bce17e733498`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## move_char

[Source line 65](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:65); ends at line 235. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- move_char: `src/act_move.c:230` (lexical_call_candidate).
- do_north: `src/act_move.c:241` (lexical_call_candidate).
- do_east: `src/act_move.c:249` (lexical_call_candidate).
- do_south: `src/act_move.c:257` (lexical_call_candidate).
- do_west: `src/act_move.c:265` (lexical_call_candidate).
- do_up: `src/act_move.c:273` (lexical_call_candidate).
- do_down: `src/act_move.c:281` (lexical_call_candidate).
- do_flee: `src/fight.c:2832` (lexical_call_candidate).
- spec_mayor: `src/special.c:919` (lexical_call_candidate).
- mobile_update: `src/update.c:455` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2085` (declaration_or_dispatch_reference).

Dependencies: `bug`, `can_see_room`, `send_to_char`, `IS_SET`, `IS_AFFECTED`, `IS_TRUSTED`, `act`, `is_room_owner`, `room_is_private`, `IS_NPC`, `IS_IMMORTAL`, `UMIN`, `WAIT_STATE`, `char_from_room`, `char_to_room`, `do_function`, `move_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.move_char.if.001` | 73 | `if ( door < 0 \|\| door > 5 )` |  | pending |
| `act_move.move_char.or.001` | 73 | `\|\| door > 5 )` |  | pending |
| `act_move.move_char.return.001` | 76 | `return;` |  | pending |
| `act_move.move_char.if.002` | 80 | `if ( ( pexit   = in_room->exit[door] ) == NULL     \|\|   ( to_room = pexit->u1.to_room   ) == NULL      \|\|	 !can_see_room(ch,pexit->u1.to_room))` |  | pending |
| `act_move.move_char.or.002` | 81 | `\|\|   ( to_room = pexit->u1.to_room   ) == NULL` |  | pending |
| `act_move.move_char.or.003` | 82 | `\|\|	 !can_see_room(ch,pexit->u1.to_room))` |  | pending |
| `act_move.move_char.return.002` | 85 | `return;` |  | pending |
| `act_move.move_char.if.003` | 88 | `if (IS_SET(pexit->exit_info, EX_CLOSED)     &&  (!IS_AFFECTED(ch, AFF_PASS_DOOR) \|\| IS_SET(pexit->exit_info,EX_NOPASS))     &&   !IS_TRUSTED(ch,ANGEL))` |  | pending |
| `act_move.move_char.and.001` | 89 | `&&  (!IS_AFFECTED(ch, AFF_PASS_DOOR) \|\| IS_SET(pexit->exit_info,EX_NOPASS))` |  | pending |
| `act_move.move_char.or.004` | 89 | `\|\| IS_SET(pexit->exit_info,EX_NOPASS))` |  | pending |
| `act_move.move_char.and.002` | 90 | `&&   !IS_TRUSTED(ch,ANGEL))` |  | pending |
| `act_move.move_char.return.003` | 93 | `return;` |  | pending |
| `act_move.move_char.if.004` | 96 | `if ( IS_AFFECTED(ch, AFF_CHARM)     &&   ch->master != NULL     &&   in_room == ch->master->in_room )` |  | pending |
| `act_move.move_char.and.003` | 97 | `&&   ch->master != NULL` |  | pending |
| `act_move.move_char.and.004` | 98 | `&&   in_room == ch->master->in_room )` |  | pending |
| `act_move.move_char.return.004` | 101 | `return;` |  | pending |
| `act_move.move_char.if.005` | 104 | `if ( !is_room_owner(ch,to_room) && room_is_private( to_room ) )` |  | pending |
| `act_move.move_char.and.005` | 104 | `&& room_is_private( to_room ) )` |  | pending |
| `act_move.move_char.return.005` | 107 | `return;` |  | pending |
| `act_move.move_char.if.006` | 110 | `if ( !IS_NPC(ch) )` |  | pending |
| `act_move.move_char.for.001` | 115 | `for ( iClass = 0; iClass < MAX_CLASS; iClass++ )` |  | pending |
| `act_move.move_char.for.002` | 117 | `for ( iGuild = 0; iGuild < MAX_GUILD; iGuild ++)` |  | pending |
| `act_move.move_char.if.007` | 119 | `if ( iClass != ch->class 	    	&&   to_room->vnum == class_table[iClass].guild[iGuild] )` |  | pending |
| `act_move.move_char.and.006` | 120 | `&&   to_room->vnum == class_table[iClass].guild[iGuild] )` |  | pending |
| `act_move.move_char.return.006` | 123 | `return;` |  | pending |
| `act_move.move_char.if.008` | 128 | `if ( in_room->sector_type == SECT_AIR 	\|\|   to_room->sector_type == SECT_AIR )` |  | pending |
| `act_move.move_char.or.005` | 129 | `\|\|   to_room->sector_type == SECT_AIR )` |  | pending |
| `act_move.move_char.if.009` | 131 | `if ( !IS_AFFECTED(ch, AFF_FLYING) && !IS_IMMORTAL(ch))` |  | pending |
| `act_move.move_char.and.007` | 131 | `&& !IS_IMMORTAL(ch))` |  | pending |
| `act_move.move_char.return.007` | 134 | `return;` |  | pending |
| `act_move.move_char.if.010` | 138 | `if (( in_room->sector_type == SECT_WATER_NOSWIM 	\|\|    to_room->sector_type == SECT_WATER_NOSWIM )   	&&    !IS_AFFECTED(ch,AFF_FLYING))` |  | pending |
| `act_move.move_char.or.006` | 139 | `\|\|    to_room->sector_type == SECT_WATER_NOSWIM )` |  | pending |
| `act_move.move_char.and.008` | 140 | `&&    !IS_AFFECTED(ch,AFF_FLYING))` |  | pending |
| `act_move.move_char.if.011` | 150 | `if (IS_IMMORTAL(ch))` |  | pending |
| `act_move.move_char.for.003` | 153 | `for ( obj = ch->carrying; obj != NULL; obj = obj->next_content )` |  | pending |
| `act_move.move_char.if.012` | 155 | `if ( obj->item_type == ITEM_BOAT )` |  | pending |
| `act_move.move_char.break.001` | 158 | `break;` |  | pending |
| `act_move.move_char.if.013` | 161 | `if ( !found )` |  | pending |
| `act_move.move_char.return.008` | 164 | `return;` |  | pending |
| `act_move.move_char.if.014` | 176 | `if (IS_AFFECTED(ch,AFF_FLYING) \|\| IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `act_move.move_char.or.007` | 176 | `\|\| IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `act_move.move_char.if.015` | 179 | `if (IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `act_move.move_char.if.016` | 182 | `if ( ch->move < move )` |  | pending |
| `act_move.move_char.return.009` | 185 | `return;` |  | pending |
| `act_move.move_char.if.017` | 192 | `if ( !IS_AFFECTED(ch, AFF_SNEAK)     &&   ch->invis_level < LEVEL_HERO)` |  | pending |
| `act_move.move_char.and.009` | 193 | `&&   ch->invis_level < LEVEL_HERO)` |  | pending |
| `act_move.move_char.if.018` | 198 | `if ( !IS_AFFECTED(ch, AFF_SNEAK)     &&   ch->invis_level < LEVEL_HERO)` |  | pending |
| `act_move.move_char.and.010` | 199 | `&&   ch->invis_level < LEVEL_HERO)` |  | pending |
| `act_move.move_char.if.019` | 204 | `if (in_room == to_room)` |  | pending |
| `act_move.move_char.return.010` | 205 | `return;` |  | pending |
| `act_move.move_char.for.004` | 207 | `for ( fch = in_room->people; fch != NULL; fch = fch_next )` |  | pending |
| `act_move.move_char.if.020` | 211 | `if ( fch->master == ch && IS_AFFECTED(fch,AFF_CHARM)  	&&   fch->position < POS_STANDING)` |  | pending |
| `act_move.move_char.and.011` | 211 | `&& IS_AFFECTED(fch,AFF_CHARM)` |  | pending |
| `act_move.move_char.and.012` | 212 | `&&   fch->position < POS_STANDING)` |  | pending |
| `act_move.move_char.if.021` | 215 | `if ( fch->master == ch && fch->position == POS_STANDING  	&&   can_see_room(fch,to_room))` |  | pending |
| `act_move.move_char.and.013` | 215 | `&& fch->position == POS_STANDING` |  | pending |
| `act_move.move_char.and.014` | 216 | `&&   can_see_room(fch,to_room))` |  | pending |
| `act_move.move_char.if.022` | 219 | `if (IS_SET(ch->in_room->room_flags,ROOM_LAW) 	    &&  (IS_NPC(fch) && IS_SET(fch->act,ACT_AGGRESSIVE)))` |  | pending |
| `act_move.move_char.and.015` | 220 | `&&  (IS_NPC(fch) && IS_SET(fch->act,ACT_AGGRESSIVE)))` |  | pending |
| `act_move.move_char.and.016` | 220 | `&& IS_SET(fch->act,ACT_AGGRESSIVE)))` |  | pending |
| `act_move.move_char.continue.001` | 226 | `continue;` |  | pending |
| `act_move.move_char.return.011` | 234 | `return;` |  | pending |

## do_north

[Source line 239](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:239); ends at line 243. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:69` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:179` (declaration_or_dispatch_reference).

Dependencies: `move_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_north.return.001` | 242 | `return;` |  | pending |

## do_east

[Source line 247](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:247); ends at line 251. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:70` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:120` (declaration_or_dispatch_reference).

Dependencies: `move_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_east.return.001` | 250 | `return;` |  | pending |

## do_south

[Source line 255](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:255); ends at line 259. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:71` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:256` (declaration_or_dispatch_reference).

Dependencies: `move_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_south.return.001` | 258 | `return;` |  | pending |

## do_west

[Source line 263](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:263); ends at line 267. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:72` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:286` (declaration_or_dispatch_reference).

Dependencies: `move_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_west.return.001` | 266 | `return;` |  | pending |

## do_up

[Source line 271](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:271); ends at line 275. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:73` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:278` (declaration_or_dispatch_reference).

Dependencies: `move_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_up.return.001` | 274 | `return;` |  | pending |

## do_down

[Source line 279](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:279); ends at line 283. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:74` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:116` (declaration_or_dispatch_reference).

Dependencies: `move_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_down.return.001` | 282 | `return;` |  | pending |

## find_door

[Source line 287](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:287); ends at line 325. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_open: `src/act_move.c:388` (lexical_call_candidate).
- do_close: `src/act_move.c:476` (lexical_call_candidate).
- do_lock: `src/act_move.c:597` (lexical_call_candidate).
- do_unlock: `src/act_move.c:705` (lexical_call_candidate).
- do_pick: `src/act_move.c:834` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_move.c:60` (declaration_or_dispatch_reference).

Dependencies: `str_cmp`, `IS_SET`, `is_name`, `act`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.find_door.if.001` | 292 | `if ( !str_cmp( arg, "n" ) \|\| !str_cmp( arg, "north" ) )` |  | pending |
| `act_move.find_door.or.001` | 292 | `\|\| !str_cmp( arg, "north" ) ) door = 0;` |  | pending |
| `act_move.find_door.if.002` | 293 | `if ( !str_cmp( arg, "e" ) \|\| !str_cmp( arg, "east"  ) )` |  | pending |
| `act_move.find_door.or.002` | 293 | `\|\| !str_cmp( arg, "east"  ) ) door = 1;` |  | pending |
| `act_move.find_door.if.003` | 294 | `if ( !str_cmp( arg, "s" ) \|\| !str_cmp( arg, "south" ) )` |  | pending |
| `act_move.find_door.or.003` | 294 | `\|\| !str_cmp( arg, "south" ) ) door = 2;` |  | pending |
| `act_move.find_door.if.004` | 295 | `if ( !str_cmp( arg, "w" ) \|\| !str_cmp( arg, "west"  ) )` |  | pending |
| `act_move.find_door.or.004` | 295 | `\|\| !str_cmp( arg, "west"  ) ) door = 3;` |  | pending |
| `act_move.find_door.if.005` | 296 | `if ( !str_cmp( arg, "u" ) \|\| !str_cmp( arg, "up"    ) )` |  | pending |
| `act_move.find_door.or.005` | 296 | `\|\| !str_cmp( arg, "up"    ) ) door = 4;` |  | pending |
| `act_move.find_door.if.006` | 297 | `if ( !str_cmp( arg, "d" ) \|\| !str_cmp( arg, "down"  ) )` |  | pending |
| `act_move.find_door.or.006` | 297 | `\|\| !str_cmp( arg, "down"  ) ) door = 5;` |  | pending |
| `act_move.find_door.for.001` | 300 | `for ( door = 0; door <= 5; door++ )` |  | pending |
| `act_move.find_door.if.007` | 302 | `if ( ( pexit = ch->in_room->exit[door] ) != NULL 	    &&   IS_SET(pexit->exit_info, EX_ISDOOR) 	    &&   pexit->keyword != NULL 	    &&   is_name( arg, pexit->keyword ) )` |  | pending |
| `act_move.find_door.and.001` | 303 | `&&   IS_SET(pexit->exit_info, EX_ISDOOR)` |  | pending |
| `act_move.find_door.and.002` | 304 | `&&   pexit->keyword != NULL` |  | pending |
| `act_move.find_door.and.003` | 305 | `&&   is_name( arg, pexit->keyword ) )` |  | pending |
| `act_move.find_door.return.001` | 306 | `return door;` |  | pending |
| `act_move.find_door.return.002` | 309 | `return -1;` |  | pending |
| `act_move.find_door.if.008` | 312 | `if ( ( pexit = ch->in_room->exit[door] ) == NULL )` |  | pending |
| `act_move.find_door.return.003` | 315 | `return -1;` |  | pending |
| `act_move.find_door.if.009` | 318 | `if ( !IS_SET(pexit->exit_info, EX_ISDOOR) )` |  | pending |
| `act_move.find_door.return.004` | 321 | `return -1;` |  | pending |
| `act_move.find_door.return.005` | 324 | `return door;` |  | pending |

## do_open

[Source line 329](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:329); ends at line 419. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_mayor: `src/special.c:962` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:218` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:186` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_here`, `IS_SET`, `REMOVE_BIT`, `act`, `find_door`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_open.if.001` | 337 | `if ( arg[0] == '\0' )` |  | pending |
| `act_move.do_open.return.001` | 340 | `return;` |  | pending |
| `act_move.do_open.if.002` | 343 | `if ( ( obj = get_obj_here( ch, arg ) ) != NULL )` |  | pending |
| `act_move.do_open.if.003` | 346 | `if (obj->item_type == ITEM_PORTAL)` |  | pending |
| `act_move.do_open.if.004` | 348 | `if (!IS_SET(obj->value[1], EX_ISDOOR))` |  | pending |
| `act_move.do_open.return.002` | 351 | `return;` |  | pending |
| `act_move.do_open.if.005` | 354 | `if (!IS_SET(obj->value[1], EX_CLOSED))` |  | pending |
| `act_move.do_open.return.003` | 357 | `return;` |  | pending |
| `act_move.do_open.if.006` | 360 | `if (IS_SET(obj->value[1], EX_LOCKED))` |  | pending |
| `act_move.do_open.return.004` | 363 | `return;` |  | pending |
| `act_move.do_open.return.005` | 369 | `return;` |  | pending |
| `act_move.do_open.if.007` | 373 | `if ( obj->item_type != ITEM_CONTAINER)` |  | pending |
| `act_move.do_open.return.006` | 374 | `return;` |  | pending |
| `act_move.do_open.if.008` | 375 | `if ( !IS_SET(obj->value[1], CONT_CLOSED) )` |  | pending |
| `act_move.do_open.return.007` | 376 | `return;` |  | pending |
| `act_move.do_open.if.009` | 377 | `if ( !IS_SET(obj->value[1], CONT_CLOSEABLE) )` |  | pending |
| `act_move.do_open.return.008` | 378 | `return;` |  | pending |
| `act_move.do_open.if.010` | 379 | `if ( IS_SET(obj->value[1], CONT_LOCKED) )` |  | pending |
| `act_move.do_open.return.009` | 380 | `return;` |  | pending |
| `act_move.do_open.return.010` | 385 | `return;` |  | pending |
| `act_move.do_open.if.011` | 388 | `if ( ( door = find_door( ch, arg ) ) >= 0 )` |  | pending |
| `act_move.do_open.if.012` | 396 | `if ( !IS_SET(pexit->exit_info, EX_CLOSED) )` |  | pending |
| `act_move.do_open.return.011` | 397 | `return;` |  | pending |
| `act_move.do_open.if.013` | 398 | `if (  IS_SET(pexit->exit_info, EX_LOCKED) )` |  | pending |
| `act_move.do_open.return.012` | 399 | `return;` |  | pending |
| `act_move.do_open.if.014` | 406 | `if ( ( to_room   = pexit->u1.to_room            ) != NULL 	&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != NULL 	&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_open.and.001` | 407 | `&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != NULL` |  | pending |
| `act_move.do_open.and.002` | 408 | `&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_open.for.001` | 413 | `for ( rch = to_room->people; rch != NULL; rch = rch->next_in_room )` |  | pending |
| `act_move.do_open.return.013` | 418 | `return;` |  | pending |

## do_close

[Source line 423](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:423); ends at line 505. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_mayor: `src/special.c:966` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:207` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:100` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_here`, `IS_SET`, `SET_BIT`, `act`, `find_door`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_close.if.001` | 431 | `if ( arg[0] == '\0' )` |  | pending |
| `act_move.do_close.return.001` | 434 | `return;` |  | pending |
| `act_move.do_close.if.002` | 437 | `if ( ( obj = get_obj_here( ch, arg ) ) != NULL )` |  | pending |
| `act_move.do_close.if.003` | 440 | `if (obj->item_type == ITEM_PORTAL)` |  | pending |
| `act_move.do_close.if.004` | 443 | `if (!IS_SET(obj->value[1],EX_ISDOOR) 	    \|\|   IS_SET(obj->value[1],EX_NOCLOSE))` |  | pending |
| `act_move.do_close.or.001` | 444 | `\|\|   IS_SET(obj->value[1],EX_NOCLOSE))` |  | pending |
| `act_move.do_close.return.002` | 447 | `return;` |  | pending |
| `act_move.do_close.if.005` | 450 | `if (IS_SET(obj->value[1],EX_CLOSED))` |  | pending |
| `act_move.do_close.return.003` | 453 | `return;` |  | pending |
| `act_move.do_close.return.004` | 459 | `return;` |  | pending |
| `act_move.do_close.if.006` | 463 | `if ( obj->item_type != ITEM_CONTAINER )` |  | pending |
| `act_move.do_close.return.005` | 464 | `return;` |  | pending |
| `act_move.do_close.if.007` | 465 | `if ( IS_SET(obj->value[1], CONT_CLOSED) )` |  | pending |
| `act_move.do_close.return.006` | 466 | `return;` |  | pending |
| `act_move.do_close.if.008` | 467 | `if ( !IS_SET(obj->value[1], CONT_CLOSEABLE) )` |  | pending |
| `act_move.do_close.return.007` | 468 | `return;` |  | pending |
| `act_move.do_close.return.008` | 473 | `return;` |  | pending |
| `act_move.do_close.if.009` | 476 | `if ( ( door = find_door( ch, arg ) ) >= 0 )` |  | pending |
| `act_move.do_close.if.010` | 484 | `if ( IS_SET(pexit->exit_info, EX_CLOSED) )` |  | pending |
| `act_move.do_close.return.009` | 485 | `return;` |  | pending |
| `act_move.do_close.if.011` | 492 | `if ( ( to_room   = pexit->u1.to_room            ) != NULL 	&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != 0 	&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_close.and.001` | 493 | `&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != 0` |  | pending |
| `act_move.do_close.and.002` | 494 | `&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_close.for.001` | 499 | `for ( rch = to_room->people; rch != NULL; rch = rch->next_in_room )` |  | pending |
| `act_move.do_close.return.010` | 504 | `return;` |  | pending |

## has_key

[Source line 509](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:509); ends at line 520. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_lock: `src/act_move.c:561` (lexical_call_candidate).
- do_lock: `src/act_move.c:586` (lexical_call_candidate).
- do_lock: `src/act_move.c:609` (lexical_call_candidate).
- do_unlock: `src/act_move.c:669` (lexical_call_candidate).
- do_unlock: `src/act_move.c:694` (lexical_call_candidate).
- do_unlock: `src/act_move.c:717` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_move.c:61` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.has_key.for.001` | 513 | `for ( obj = ch->carrying; obj != NULL; obj = obj->next_content )` |  | pending |
| `act_move.has_key.if.001` | 515 | `if ( obj->pIndexData->vnum == key )` |  | pending |
| `act_move.has_key.return.001` | 516 | `return TRUE;` |  | pending |
| `act_move.has_key.return.002` | 519 | `return FALSE;` |  | pending |

## do_lock

[Source line 524](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:524); ends at line 628. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:217` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:160` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_here`, `IS_SET`, `has_key`, `SET_BIT`, `act`, `find_door`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_lock.if.001` | 532 | `if ( arg[0] == '\0' )` |  | pending |
| `act_move.do_lock.return.001` | 535 | `return;` |  | pending |
| `act_move.do_lock.if.002` | 538 | `if ( ( obj = get_obj_here( ch, arg ) ) != NULL )` |  | pending |
| `act_move.do_lock.if.003` | 541 | `if (obj->item_type == ITEM_PORTAL)` |  | pending |
| `act_move.do_lock.if.004` | 543 | `if (!IS_SET(obj->value[1],EX_ISDOOR) 	    \|\|  IS_SET(obj->value[1],EX_NOCLOSE))` |  | pending |
| `act_move.do_lock.or.001` | 544 | `\|\|  IS_SET(obj->value[1],EX_NOCLOSE))` |  | pending |
| `act_move.do_lock.return.002` | 547 | `return;` |  | pending |
| `act_move.do_lock.if.005` | 549 | `if (!IS_SET(obj->value[1],EX_CLOSED))` |  | pending |
| `act_move.do_lock.return.003` | 552 | `return;` |  | pending |
| `act_move.do_lock.if.006` | 555 | `if (obj->value[4] < 0 \|\| IS_SET(obj->value[1],EX_NOLOCK))` |  | pending |
| `act_move.do_lock.or.002` | 555 | `\|\| IS_SET(obj->value[1],EX_NOLOCK))` |  | pending |
| `act_move.do_lock.return.004` | 558 | `return;` |  | pending |
| `act_move.do_lock.if.007` | 561 | `if (!has_key(ch,obj->value[4]))` |  | pending |
| `act_move.do_lock.return.005` | 564 | `return;` |  | pending |
| `act_move.do_lock.if.008` | 567 | `if (IS_SET(obj->value[1],EX_LOCKED))` |  | pending |
| `act_move.do_lock.return.006` | 570 | `return;` |  | pending |
| `act_move.do_lock.return.007` | 576 | `return;` |  | pending |
| `act_move.do_lock.if.009` | 580 | `if ( obj->item_type != ITEM_CONTAINER )` |  | pending |
| `act_move.do_lock.return.008` | 581 | `return;` |  | pending |
| `act_move.do_lock.if.010` | 582 | `if ( !IS_SET(obj->value[1], CONT_CLOSED) )` |  | pending |
| `act_move.do_lock.return.009` | 583 | `return;` |  | pending |
| `act_move.do_lock.if.011` | 584 | `if ( obj->value[2] < 0 )` |  | pending |
| `act_move.do_lock.return.010` | 585 | `return;` |  | pending |
| `act_move.do_lock.if.012` | 586 | `if ( !has_key( ch, obj->value[2] ) )` |  | pending |
| `act_move.do_lock.return.011` | 587 | `return;` |  | pending |
| `act_move.do_lock.if.013` | 588 | `if ( IS_SET(obj->value[1], CONT_LOCKED) )` |  | pending |
| `act_move.do_lock.return.012` | 589 | `return;` |  | pending |
| `act_move.do_lock.return.013` | 594 | `return;` |  | pending |
| `act_move.do_lock.if.014` | 597 | `if ( ( door = find_door( ch, arg ) ) >= 0 )` |  | pending |
| `act_move.do_lock.if.015` | 605 | `if ( !IS_SET(pexit->exit_info, EX_CLOSED) )` |  | pending |
| `act_move.do_lock.return.014` | 606 | `return;` |  | pending |
| `act_move.do_lock.if.016` | 607 | `if ( pexit->key < 0 )` |  | pending |
| `act_move.do_lock.return.015` | 608 | `return;` |  | pending |
| `act_move.do_lock.if.017` | 609 | `if ( !has_key( ch, pexit->key) )` |  | pending |
| `act_move.do_lock.return.016` | 610 | `return;` |  | pending |
| `act_move.do_lock.if.018` | 611 | `if ( IS_SET(pexit->exit_info, EX_LOCKED) )` |  | pending |
| `act_move.do_lock.return.017` | 612 | `return;` |  | pending |
| `act_move.do_lock.if.019` | 619 | `if ( ( to_room   = pexit->u1.to_room            ) != NULL 	&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != 0 	&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_lock.and.001` | 620 | `&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != 0` |  | pending |
| `act_move.do_lock.and.002` | 621 | `&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_lock.return.018` | 627 | `return;` |  | pending |

## do_unlock

[Source line 632](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:632); ends at line 736. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:103` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:276` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_here`, `IS_SET`, `has_key`, `REMOVE_BIT`, `act`, `find_door`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_unlock.if.001` | 640 | `if ( arg[0] == '\0' )` |  | pending |
| `act_move.do_unlock.return.001` | 643 | `return;` |  | pending |
| `act_move.do_unlock.if.002` | 646 | `if ( ( obj = get_obj_here( ch, arg ) ) != NULL )` |  | pending |
| `act_move.do_unlock.if.003` | 649 | `if (obj->item_type == ITEM_PORTAL)` |  | pending |
| `act_move.do_unlock.if.004` | 651 | `if (!IS_SET(obj->value[1],EX_ISDOOR))` |  | pending |
| `act_move.do_unlock.return.002` | 654 | `return;` |  | pending |
| `act_move.do_unlock.if.005` | 657 | `if (!IS_SET(obj->value[1],EX_CLOSED))` |  | pending |
| `act_move.do_unlock.return.003` | 660 | `return;` |  | pending |
| `act_move.do_unlock.if.006` | 663 | `if (obj->value[4] < 0)` |  | pending |
| `act_move.do_unlock.return.004` | 666 | `return;` |  | pending |
| `act_move.do_unlock.if.007` | 669 | `if (!has_key(ch,obj->value[4]))` |  | pending |
| `act_move.do_unlock.return.005` | 672 | `return;` |  | pending |
| `act_move.do_unlock.if.008` | 675 | `if (!IS_SET(obj->value[1],EX_LOCKED))` |  | pending |
| `act_move.do_unlock.return.006` | 678 | `return;` |  | pending |
| `act_move.do_unlock.return.007` | 684 | `return;` |  | pending |
| `act_move.do_unlock.if.009` | 688 | `if ( obj->item_type != ITEM_CONTAINER )` |  | pending |
| `act_move.do_unlock.return.008` | 689 | `return;` |  | pending |
| `act_move.do_unlock.if.010` | 690 | `if ( !IS_SET(obj->value[1], CONT_CLOSED) )` |  | pending |
| `act_move.do_unlock.return.009` | 691 | `return;` |  | pending |
| `act_move.do_unlock.if.011` | 692 | `if ( obj->value[2] < 0 )` |  | pending |
| `act_move.do_unlock.return.010` | 693 | `return;` |  | pending |
| `act_move.do_unlock.if.012` | 694 | `if ( !has_key( ch, obj->value[2] ) )` |  | pending |
| `act_move.do_unlock.return.011` | 695 | `return;` |  | pending |
| `act_move.do_unlock.if.013` | 696 | `if ( !IS_SET(obj->value[1], CONT_LOCKED) )` |  | pending |
| `act_move.do_unlock.return.012` | 697 | `return;` |  | pending |
| `act_move.do_unlock.return.013` | 702 | `return;` |  | pending |
| `act_move.do_unlock.if.014` | 705 | `if ( ( door = find_door( ch, arg ) ) >= 0 )` |  | pending |
| `act_move.do_unlock.if.015` | 713 | `if ( !IS_SET(pexit->exit_info, EX_CLOSED) )` |  | pending |
| `act_move.do_unlock.return.014` | 714 | `return;` |  | pending |
| `act_move.do_unlock.if.016` | 715 | `if ( pexit->key < 0 )` |  | pending |
| `act_move.do_unlock.return.015` | 716 | `return;` |  | pending |
| `act_move.do_unlock.if.017` | 717 | `if ( !has_key( ch, pexit->key) )` |  | pending |
| `act_move.do_unlock.return.016` | 718 | `return;` |  | pending |
| `act_move.do_unlock.if.018` | 719 | `if ( !IS_SET(pexit->exit_info, EX_LOCKED) )` |  | pending |
| `act_move.do_unlock.return.017` | 720 | `return;` |  | pending |
| `act_move.do_unlock.if.019` | 727 | `if ( ( to_room   = pexit->u1.to_room            ) != NULL 	&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != NULL 	&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_unlock.and.001` | 728 | `&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != NULL` |  | pending |
| `act_move.do_unlock.and.002` | 729 | `&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_unlock.return.018` | 735 | `return;` |  | pending |

## do_pick

[Source line 740](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:740); ends at line 866. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:219` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:198` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `WAIT_STATE`, `IS_NPC`, `IS_AWAKE`, `act`, `number_percent`, `get_skill`, `check_improve`, `get_obj_here`, `IS_SET`, `REMOVE_BIT`, `find_door`, `IS_IMMORTAL`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_pick.if.001` | 749 | `if ( arg[0] == '\0' )` |  | pending |
| `act_move.do_pick.return.001` | 752 | `return;` |  | pending |
| `act_move.do_pick.for.001` | 758 | `for ( gch = ch->in_room->people; gch; gch = gch->next_in_room )` |  | pending |
| `act_move.do_pick.if.002` | 760 | `if ( IS_NPC(gch) && IS_AWAKE(gch) && ch->level + 5 < gch->level )` |  | pending |
| `act_move.do_pick.and.001` | 760 | `&& IS_AWAKE(gch) && ch->level + 5 < gch->level )` |  | pending |
| `act_move.do_pick.and.002` | 760 | `&& ch->level + 5 < gch->level )` |  | pending |
| `act_move.do_pick.return.002` | 764 | `return;` |  | pending |
| `act_move.do_pick.if.003` | 768 | `if ( !IS_NPC(ch) && number_percent( ) > get_skill(ch,gsn_pick_lock))` |  | pending |
| `act_move.do_pick.and.003` | 768 | `&& number_percent( ) > get_skill(ch,gsn_pick_lock))` |  | pending |
| `act_move.do_pick.return.003` | 772 | `return;` |  | pending |
| `act_move.do_pick.if.004` | 775 | `if ( ( obj = get_obj_here( ch, arg ) ) != NULL )` |  | pending |
| `act_move.do_pick.if.005` | 778 | `if (obj->item_type == ITEM_PORTAL)` |  | pending |
| `act_move.do_pick.if.006` | 780 | `if (!IS_SET(obj->value[1],EX_ISDOOR))` |  | pending |
| `act_move.do_pick.return.004` | 783 | `return;` |  | pending |
| `act_move.do_pick.if.007` | 786 | `if (!IS_SET(obj->value[1],EX_CLOSED))` |  | pending |
| `act_move.do_pick.return.005` | 789 | `return;` |  | pending |
| `act_move.do_pick.if.008` | 792 | `if (obj->value[4] < 0)` |  | pending |
| `act_move.do_pick.return.006` | 795 | `return;` |  | pending |
| `act_move.do_pick.if.009` | 798 | `if (IS_SET(obj->value[1],EX_PICKPROOF))` |  | pending |
| `act_move.do_pick.return.007` | 801 | `return;` |  | pending |
| `act_move.do_pick.return.008` | 808 | `return;` |  | pending |
| `act_move.do_pick.if.010` | 816 | `if ( obj->item_type != ITEM_CONTAINER )` |  | pending |
| `act_move.do_pick.return.009` | 817 | `return;` |  | pending |
| `act_move.do_pick.if.011` | 818 | `if ( !IS_SET(obj->value[1], CONT_CLOSED) )` |  | pending |
| `act_move.do_pick.return.010` | 819 | `return;` |  | pending |
| `act_move.do_pick.if.012` | 820 | `if ( obj->value[2] < 0 )` |  | pending |
| `act_move.do_pick.return.011` | 821 | `return;` |  | pending |
| `act_move.do_pick.if.013` | 822 | `if ( !IS_SET(obj->value[1], CONT_LOCKED) )` |  | pending |
| `act_move.do_pick.return.012` | 823 | `return;` |  | pending |
| `act_move.do_pick.if.014` | 824 | `if ( IS_SET(obj->value[1], CONT_PICKPROOF) )` |  | pending |
| `act_move.do_pick.return.013` | 825 | `return;` |  | pending |
| `act_move.do_pick.return.014` | 831 | `return;` |  | pending |
| `act_move.do_pick.if.015` | 834 | `if ( ( door = find_door( ch, arg ) ) >= 0 )` |  | pending |
| `act_move.do_pick.if.016` | 842 | `if ( !IS_SET(pexit->exit_info, EX_CLOSED) && !IS_IMMORTAL(ch))` |  | pending |
| `act_move.do_pick.and.004` | 842 | `&& !IS_IMMORTAL(ch))` |  | pending |
| `act_move.do_pick.return.015` | 843 | `return;` |  | pending |
| `act_move.do_pick.if.017` | 844 | `if ( pexit->key < 0 && !IS_IMMORTAL(ch))` |  | pending |
| `act_move.do_pick.and.005` | 844 | `&& !IS_IMMORTAL(ch))` |  | pending |
| `act_move.do_pick.return.016` | 845 | `return;` |  | pending |
| `act_move.do_pick.if.018` | 846 | `if ( !IS_SET(pexit->exit_info, EX_LOCKED) )` |  | pending |
| `act_move.do_pick.return.017` | 847 | `return;` |  | pending |
| `act_move.do_pick.if.019` | 848 | `if ( IS_SET(pexit->exit_info, EX_PICKPROOF) && !IS_IMMORTAL(ch))` |  | pending |
| `act_move.do_pick.and.006` | 848 | `&& !IS_IMMORTAL(ch))` |  | pending |
| `act_move.do_pick.return.018` | 849 | `return;` |  | pending |
| `act_move.do_pick.if.020` | 857 | `if ( ( to_room   = pexit->u1.to_room            ) != NULL 	&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != NULL 	&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_pick.and.007` | 858 | `&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != NULL` |  | pending |
| `act_move.do_pick.and.008` | 859 | `&&   pexit_rev->u1.to_room == ch->in_room )` |  | pending |
| `act_move.do_pick.return.019` | 865 | `return;` |  | pending |

## do_stand

[Source line 871](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:871); ends at line 971. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:175` (function_symbol_reference_candidate).
- move_char: `src/act_move.c:213` (function_symbol_reference_candidate).
- do_wake: `src/act_move.c:1314` (function_symbol_reference_candidate).
- do_wake: `src/act_move.c:1329` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:101` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:261` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_obj_list`, `IS_SET`, `count_users`, `act_new`, `IS_AFFECTED`, `act`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_stand.if.001` | 875 | `if (argument[0] != '\0')` |  | pending |
| `act_move.do_stand.if.002` | 877 | `if (ch->position == POS_FIGHTING)` |  | pending |
| `act_move.do_stand.return.001` | 880 | `return;` |  | pending |
| `act_move.do_stand.if.003` | 883 | `if (obj == NULL)` |  | pending |
| `act_move.do_stand.return.002` | 886 | `return;` |  | pending |
| `act_move.do_stand.if.004` | 888 | `if (obj->item_type != ITEM_FURNITURE 	\|\|  (!IS_SET(obj->value[2],STAND_AT) 	&&   !IS_SET(obj->value[2],STAND_ON) 	&&   !IS_SET(obj->value[2],STAND_IN)))` |  | pending |
| `act_move.do_stand.or.001` | 889 | `\|\|  (!IS_SET(obj->value[2],STAND_AT)` |  | pending |
| `act_move.do_stand.and.001` | 890 | `&&   !IS_SET(obj->value[2],STAND_ON)` |  | pending |
| `act_move.do_stand.and.002` | 891 | `&&   !IS_SET(obj->value[2],STAND_IN)))` |  | pending |
| `act_move.do_stand.return.003` | 894 | `return;` |  | pending |
| `act_move.do_stand.if.005` | 896 | `if (ch->on != obj && count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_stand.and.003` | 896 | `&& count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_stand.return.004` | 900 | `return;` |  | pending |
| `act_move.do_stand.switch.001` | 905 | `switch ( ch->position )` |  | pending |
| `act_move.do_stand.case.001` | 907 | `case POS_SLEEPING:` |  | pending |
| `act_move.do_stand.if.006` | 908 | `if ( IS_AFFECTED(ch, AFF_SLEEP) )` |  | pending |
| `act_move.do_stand.return.005` | 909 | `return;` |  | pending |
| `act_move.do_stand.if.007` | 911 | `if (obj == NULL)` |  | pending |
| `act_move.do_stand.if.008` | 917 | `if (IS_SET(obj->value[2],STAND_AT))` |  | pending |
| `act_move.do_stand.if.009` | 922 | `if (IS_SET(obj->value[2],STAND_ON))` |  | pending |
| `act_move.do_stand.break.001` | 934 | `break;` |  | pending |
| `act_move.do_stand.case.002` | 936 | `case POS_RESTING: case POS_SITTING:` |  | pending |
| `act_move.do_stand.case.003` | 936 | `case POS_SITTING:` |  | pending |
| `act_move.do_stand.if.010` | 937 | `if (obj == NULL)` |  | pending |
| `act_move.do_stand.if.011` | 943 | `if (IS_SET(obj->value[2],STAND_AT))` |  | pending |
| `act_move.do_stand.if.012` | 948 | `if (IS_SET(obj->value[2],STAND_ON))` |  | pending |
| `act_move.do_stand.break.002` | 959 | `break;` |  | pending |
| `act_move.do_stand.case.004` | 961 | `case POS_STANDING:` |  | pending |
| `act_move.do_stand.break.003` | 963 | `break;` |  | pending |
| `act_move.do_stand.case.005` | 965 | `case POS_FIGHTING:` |  | pending |
| `act_move.do_stand.break.004` | 967 | `break;` |  | pending |
| `act_move.do_stand.return.006` | 970 | `return;` |  | pending |

## do_rest

[Source line 975](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:975); ends at line 1107. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:98` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:228` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_obj_list`, `IS_SET`, `count_users`, `act_new`, `IS_AFFECTED`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_rest.if.001` | 979 | `if (ch->position == POS_FIGHTING)` |  | pending |
| `act_move.do_rest.return.001` | 982 | `return;` |  | pending |
| `act_move.do_rest.if.002` | 986 | `if (argument[0] != '\0')` |  | pending |
| `act_move.do_rest.if.003` | 989 | `if (obj == NULL)` |  | pending |
| `act_move.do_rest.return.002` | 992 | `return;` |  | pending |
| `act_move.do_rest.if.004` | 997 | `if (obj != NULL)` |  | pending |
| `act_move.do_rest.if.005` | 999 | `if (obj->item_type != ITEM_FURNITURE     	\|\|  (!IS_SET(obj->value[2],REST_ON)     	&&   !IS_SET(obj->value[2],REST_IN)     	&&   !IS_SET(obj->value[2],REST_AT)))` |  | pending |
| `act_move.do_rest.or.001` | 1000 | `\|\|  (!IS_SET(obj->value[2],REST_ON)` |  | pending |
| `act_move.do_rest.and.001` | 1001 | `&&   !IS_SET(obj->value[2],REST_IN)` |  | pending |
| `act_move.do_rest.and.002` | 1002 | `&&   !IS_SET(obj->value[2],REST_AT)))` |  | pending |
| `act_move.do_rest.return.003` | 1005 | `return;` |  | pending |
| `act_move.do_rest.if.006` | 1008 | `if (obj != NULL && ch->on != obj && count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_rest.and.003` | 1008 | `&& ch->on != obj && count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_rest.and.004` | 1008 | `&& count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_rest.return.004` | 1011 | `return;` |  | pending |
| `act_move.do_rest.switch.001` | 1017 | `switch ( ch->position )` |  | pending |
| `act_move.do_rest.case.001` | 1019 | `case POS_SLEEPING:` |  | pending |
| `act_move.do_rest.if.007` | 1020 | `if (IS_AFFECTED(ch,AFF_SLEEP))` |  | pending |
| `act_move.do_rest.return.005` | 1023 | `return;` |  | pending |
| `act_move.do_rest.if.008` | 1026 | `if (obj == NULL)` |  | pending |
| `act_move.do_rest.if.009` | 1031 | `if (IS_SET(obj->value[2],REST_AT))` |  | pending |
| `act_move.do_rest.if.010` | 1037 | `if (IS_SET(obj->value[2],REST_ON))` |  | pending |
| `act_move.do_rest.break.001` | 1050 | `break;` |  | pending |
| `act_move.do_rest.case.002` | 1052 | `case POS_RESTING:` |  | pending |
| `act_move.do_rest.break.002` | 1054 | `break;` |  | pending |
| `act_move.do_rest.case.003` | 1056 | `case POS_STANDING:` |  | pending |
| `act_move.do_rest.if.011` | 1057 | `if (obj == NULL)` |  | pending |
| `act_move.do_rest.if.012` | 1062 | `if (IS_SET(obj->value[2],REST_AT))` |  | pending |
| `act_move.do_rest.if.013` | 1067 | `if (IS_SET(obj->value[2],REST_ON))` |  | pending |
| `act_move.do_rest.break.003` | 1078 | `break;` |  | pending |
| `act_move.do_rest.case.004` | 1080 | `case POS_SITTING:` |  | pending |
| `act_move.do_rest.if.014` | 1081 | `if (obj == NULL)` |  | pending |
| `act_move.do_rest.if.015` | 1086 | `if (IS_SET(obj->value[2],REST_AT))` |  | pending |
| `act_move.do_rest.if.016` | 1091 | `if (IS_SET(obj->value[2],REST_ON))` |  | pending |
| `act_move.do_rest.break.004` | 1102 | `break;` |  | pending |
| `act_move.do_rest.return.006` | 1106 | `return;` |  | pending |

## do_sit

[Source line 1110](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1110); ends at line 1227. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:99` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:246` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_obj_list`, `IS_SET`, `count_users`, `act_new`, `IS_AFFECTED`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_sit.if.001` | 1114 | `if (ch->position == POS_FIGHTING)` |  | pending |
| `act_move.do_sit.return.001` | 1117 | `return;` |  | pending |
| `act_move.do_sit.if.002` | 1121 | `if (argument[0] != '\0')` |  | pending |
| `act_move.do_sit.if.003` | 1124 | `if (obj == NULL)` |  | pending |
| `act_move.do_sit.return.002` | 1127 | `return;` |  | pending |
| `act_move.do_sit.if.004` | 1132 | `if (obj != NULL)` |  | pending |
| `act_move.do_sit.if.005` | 1134 | `if (obj->item_type != ITEM_FURNITURE 	\|\|  (!IS_SET(obj->value[2],SIT_ON) 	&&   !IS_SET(obj->value[2],SIT_IN) 	&&   !IS_SET(obj->value[2],SIT_AT)))` |  | pending |
| `act_move.do_sit.or.001` | 1135 | `\|\|  (!IS_SET(obj->value[2],SIT_ON)` |  | pending |
| `act_move.do_sit.and.001` | 1136 | `&&   !IS_SET(obj->value[2],SIT_IN)` |  | pending |
| `act_move.do_sit.and.002` | 1137 | `&&   !IS_SET(obj->value[2],SIT_AT)))` |  | pending |
| `act_move.do_sit.return.003` | 1140 | `return;` |  | pending |
| `act_move.do_sit.if.006` | 1143 | `if (obj != NULL && ch->on != obj && count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_sit.and.003` | 1143 | `&& ch->on != obj && count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_sit.and.004` | 1143 | `&& count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_sit.return.004` | 1146 | `return;` |  | pending |
| `act_move.do_sit.switch.001` | 1151 | `switch (ch->position)` |  | pending |
| `act_move.do_sit.case.001` | 1153 | `case POS_SLEEPING:` |  | pending |
| `act_move.do_sit.if.007` | 1154 | `if (IS_AFFECTED(ch,AFF_SLEEP))` |  | pending |
| `act_move.do_sit.return.005` | 1157 | `return;` |  | pending |
| `act_move.do_sit.if.008` | 1160 | `if (obj == NULL)` |  | pending |
| `act_move.do_sit.if.009` | 1165 | `if (IS_SET(obj->value[2],SIT_AT))` |  | pending |
| `act_move.do_sit.if.010` | 1170 | `if (IS_SET(obj->value[2],SIT_ON))` |  | pending |
| `act_move.do_sit.break.001` | 1182 | `break;` |  | pending |
| `act_move.do_sit.case.002` | 1183 | `case POS_RESTING:` |  | pending |
| `act_move.do_sit.if.011` | 1184 | `if (obj == NULL)` |  | pending |
| `act_move.do_sit.if.012` | 1186 | `if (IS_SET(obj->value[2],SIT_AT))` |  | pending |
| `act_move.do_sit.if.013` | 1192 | `if (IS_SET(obj->value[2],SIT_ON))` |  | pending |
| `act_move.do_sit.break.002` | 1198 | `break;` |  | pending |
| `act_move.do_sit.case.003` | 1199 | `case POS_SITTING:` |  | pending |
| `act_move.do_sit.break.003` | 1201 | `break;` |  | pending |
| `act_move.do_sit.case.004` | 1202 | `case POS_STANDING:` |  | pending |
| `act_move.do_sit.if.014` | 1203 | `if (obj == NULL)` |  | pending |
| `act_move.do_sit.if.015` | 1208 | `if (IS_SET(obj->value[2],SIT_AT))` |  | pending |
| `act_move.do_sit.if.016` | 1213 | `if (IS_SET(obj->value[2],SIT_ON))` |  | pending |
| `act_move.do_sit.break.004` | 1224 | `break;` |  | pending |
| `act_move.do_sit.return.006` | 1226 | `return;` |  | pending |

## do_sleep

[Source line 1230](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1230); ends at line 1303. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:269` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:250` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `act`, `get_obj_list`, `IS_SET`, `count_users`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_sleep.switch.001` | 1234 | `switch ( ch->position )` |  | pending |
| `act_move.do_sleep.case.001` | 1236 | `case POS_SLEEPING:` |  | pending |
| `act_move.do_sleep.break.001` | 1238 | `break;` |  | pending |
| `act_move.do_sleep.case.002` | 1240 | `case POS_RESTING:` |  | pending |
| `act_move.do_sleep.case.003` | 1241 | `case POS_SITTING:` |  | pending |
| `act_move.do_sleep.case.004` | 1242 | `case POS_STANDING:` |  | pending |
| `act_move.do_sleep.if.001` | 1243 | `if (argument[0] == '\0' && ch->on == NULL)` |  | pending |
| `act_move.do_sleep.and.001` | 1243 | `&& ch->on == NULL)` |  | pending |
| `act_move.do_sleep.if.002` | 1251 | `if (argument[0] == '\0')` |  | pending |
| `act_move.do_sleep.if.003` | 1256 | `if (obj == NULL)` |  | pending |
| `act_move.do_sleep.return.001` | 1259 | `return;` |  | pending |
| `act_move.do_sleep.if.004` | 1261 | `if (obj->item_type != ITEM_FURNITURE 	    \|\|  (!IS_SET(obj->value[2],SLEEP_ON)  	    &&   !IS_SET(obj->value[2],SLEEP_IN) 	    &&	 !IS_SET(obj->value[2],SLEEP_AT)))` |  | pending |
| `act_move.do_sleep.or.001` | 1262 | `\|\|  (!IS_SET(obj->value[2],SLEEP_ON)` |  | pending |
| `act_move.do_sleep.and.002` | 1263 | `&&   !IS_SET(obj->value[2],SLEEP_IN)` |  | pending |
| `act_move.do_sleep.and.003` | 1264 | `&&	 !IS_SET(obj->value[2],SLEEP_AT)))` |  | pending |
| `act_move.do_sleep.return.002` | 1267 | `return;` |  | pending |
| `act_move.do_sleep.if.005` | 1270 | `if (ch->on != obj && count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_sleep.and.004` | 1270 | `&& count_users(obj) >= obj->value[0])` |  | pending |
| `act_move.do_sleep.return.003` | 1274 | `return;` |  | pending |
| `act_move.do_sleep.if.006` | 1278 | `if (IS_SET(obj->value[2],SLEEP_AT))` |  | pending |
| `act_move.do_sleep.if.007` | 1283 | `if (IS_SET(obj->value[2],SLEEP_ON))` |  | pending |
| `act_move.do_sleep.break.002` | 1295 | `break;` |  | pending |
| `act_move.do_sleep.case.005` | 1297 | `case POS_FIGHTING:` |  | pending |
| `act_move.do_sleep.break.003` | 1299 | `break;` |  | pending |
| `act_move.do_sleep.return.004` | 1302 | `return;` |  | pending |

## do_wake

[Source line 1307](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1307); ends at line 1331. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_steal: `src/act_obj.c:2216` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:275` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:283` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `do_function`, `IS_AWAKE`, `send_to_char`, `get_char_room`, `act`, `IS_AFFECTED`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_wake.if.001` | 1313 | `if ( arg[0] == '\0' )` |  | pending |
| `act_move.do_wake.return.001` | 1314 | `return;` |  | pending |
| `act_move.do_wake.if.002` | 1316 | `if ( !IS_AWAKE(ch) )` |  | pending |
| `act_move.do_wake.return.002` | 1317 | `return;` |  | pending |
| `act_move.do_wake.if.003` | 1319 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `act_move.do_wake.return.003` | 1320 | `return;` |  | pending |
| `act_move.do_wake.if.004` | 1322 | `if ( IS_AWAKE(victim) )` |  | pending |
| `act_move.do_wake.return.004` | 1323 | `return;` |  | pending |
| `act_move.do_wake.if.005` | 1325 | `if ( IS_AFFECTED(victim, AFF_SLEEP) )` |  | pending |
| `act_move.do_wake.return.005` | 1326 | `return;` |  | pending |
| `act_move.do_wake.return.006` | 1330 | `return;` |  | pending |

## do_sneak

[Source line 1335](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1335); ends at line 1361. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:270` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:253` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `affect_strip`, `IS_AFFECTED`, `number_percent`, `get_skill`, `check_improve`, `affect_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_sneak.if.001` | 1342 | `if (IS_AFFECTED(ch,AFF_SNEAK))` |  | pending |
| `act_move.do_sneak.return.001` | 1343 | `return;` |  | pending |
| `act_move.do_sneak.if.002` | 1345 | `if ( number_percent( ) < get_skill(ch,gsn_sneak))` |  | pending |
| `act_move.do_sneak.return.002` | 1360 | `return;` |  | pending |

## do_hide

[Source line 1365](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1365); ends at line 1381. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:260` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:147` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `IS_AFFECTED`, `REMOVE_BIT`, `number_percent`, `get_skill`, `SET_BIT`, `check_improve`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_hide.if.001` | 1369 | `if ( IS_AFFECTED(ch, AFF_HIDE) )` |  | pending |
| `act_move.do_hide.if.002` | 1372 | `if ( number_percent( ) < get_skill(ch,gsn_hide))` |  | pending |
| `act_move.do_hide.return.001` | 1380 | `return;` |  | pending |

## do_visible

[Source line 1388](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1388); ends at line 1398. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:274` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:280` (declaration_or_dispatch_reference).

Dependencies: `affect_strip`, `REMOVE_BIT`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_visible.return.001` | 1397 | `return;` |  | pending |

## do_recall

[Source line 1402](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1402); ends at line 1467. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_recall: `src/act_move.c:1464` (function_symbol_reference_candidate).
- damage: `src/fight.c:959` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:265` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:266` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:219` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `act`, `get_room_index`, `IS_AFFECTED`, `get_skill`, `number_percent`, `check_improve`, `WAIT_STATE`, `sprintf`, `gain_exp`, `stop_fighting`, `char_from_room`, `char_to_room`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_recall.if.001` | 1408 | `if (IS_NPC(ch) && !IS_SET(ch->act,ACT_PET))` |  | pending |
| `act_move.do_recall.and.001` | 1408 | `&& !IS_SET(ch->act,ACT_PET))` |  | pending |
| `act_move.do_recall.return.001` | 1411 | `return;` |  | pending |
| `act_move.do_recall.if.002` | 1416 | `if ( ( location = get_room_index( ROOM_VNUM_TEMPLE ) ) == NULL )` |  | pending |
| `act_move.do_recall.return.002` | 1419 | `return;` |  | pending |
| `act_move.do_recall.if.003` | 1422 | `if ( ch->in_room == location )` |  | pending |
| `act_move.do_recall.return.003` | 1423 | `return;` |  | pending |
| `act_move.do_recall.if.004` | 1425 | `if ( IS_SET(ch->in_room->room_flags, ROOM_NO_RECALL)     \|\|   IS_AFFECTED(ch, AFF_CURSE))` |  | pending |
| `act_move.do_recall.or.001` | 1426 | `\|\|   IS_AFFECTED(ch, AFF_CURSE))` |  | pending |
| `act_move.do_recall.return.004` | 1429 | `return;` |  | pending |
| `act_move.do_recall.if.005` | 1432 | `if ( ( victim = ch->fighting ) != NULL )` |  | pending |
| `act_move.do_recall.if.006` | 1438 | `if ( number_percent() < 80 * skill / 100 )` |  | pending |
| `act_move.do_recall.return.005` | 1444 | `return;` |  | pending |
| `act_move.do_recall.ternary.001` | 1447 | `? 25 : 50;` |  | pending |
| `act_move.do_recall.if.007` | 1463 | `if (ch->pet != NULL)` |  | pending |
| `act_move.do_recall.return.006` | 1466 | `return;` |  | pending |

## do_train

[Source line 1471](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1471); ends at line 1640. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:273` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:270` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `sprintf`, `str_cmp`, `strcpy`, `get_max_train`, `strcat`, `strlen`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_move.do_train.if.001` | 1479 | `if ( IS_NPC(ch) )` |  | pending |
| `act_move.do_train.return.001` | 1480 | `return;` |  | pending |
| `act_move.do_train.for.001` | 1485 | `for ( mob = ch->in_room->people; mob; mob = mob->next_in_room )` |  | pending |
| `act_move.do_train.if.002` | 1487 | `if ( IS_NPC(mob) && IS_SET(mob->act, ACT_TRAIN) )` |  | pending |
| `act_move.do_train.and.001` | 1487 | `&& IS_SET(mob->act, ACT_TRAIN) )` |  | pending |
| `act_move.do_train.break.001` | 1488 | `break;` |  | pending |
| `act_move.do_train.if.003` | 1491 | `if ( mob == NULL )` |  | pending |
| `act_move.do_train.return.002` | 1494 | `return;` |  | pending |
| `act_move.do_train.if.004` | 1497 | `if ( argument[0] == '\0' )` |  | pending |
| `act_move.do_train.if.005` | 1506 | `if ( !str_cmp( argument, "str" ) )` |  | pending |
| `act_move.do_train.if.006` | 1508 | `if ( class_table[ch->class].attr_prime == STAT_STR )` |  | pending |
| `act_move.do_train.if.007` | 1514 | `if ( !str_cmp( argument, "int" ) )` |  | pending |
| `act_move.do_train.if.008` | 1516 | `if ( class_table[ch->class].attr_prime == STAT_INT )` |  | pending |
| `act_move.do_train.if.009` | 1522 | `if ( !str_cmp( argument, "wis" ) )` |  | pending |
| `act_move.do_train.if.010` | 1524 | `if ( class_table[ch->class].attr_prime == STAT_WIS )` |  | pending |
| `act_move.do_train.if.011` | 1530 | `if ( !str_cmp( argument, "dex" ) )` |  | pending |
| `act_move.do_train.if.012` | 1532 | `if ( class_table[ch->class].attr_prime == STAT_DEX )` |  | pending |
| `act_move.do_train.if.013` | 1538 | `if ( !str_cmp( argument, "con" ) )` |  | pending |
| `act_move.do_train.if.014` | 1540 | `if ( class_table[ch->class].attr_prime == STAT_CON )` |  | pending |
| `act_move.do_train.if.015` | 1546 | `if ( !str_cmp(argument, "hp" ) )` |  | pending |
| `act_move.do_train.if.016` | 1549 | `if ( !str_cmp(argument, "mana" ) )` |  | pending |
| `act_move.do_train.if.017` | 1555 | `if ( ch->perm_stat[STAT_STR] < get_max_train(ch,STAT_STR))` |  | pending |
| `act_move.do_train.if.018` | 1557 | `if ( ch->perm_stat[STAT_INT] < get_max_train(ch,STAT_INT))` |  | pending |
| `act_move.do_train.if.019` | 1559 | `if ( ch->perm_stat[STAT_WIS] < get_max_train(ch,STAT_WIS))` |  | pending |
| `act_move.do_train.if.020` | 1561 | `if ( ch->perm_stat[STAT_DEX] < get_max_train(ch,STAT_DEX))` |  | pending |
| `act_move.do_train.if.021` | 1563 | `if ( ch->perm_stat[STAT_CON] < get_max_train(ch,STAT_CON))` |  | pending |
| `act_move.do_train.if.022` | 1567 | `if ( buf[strlen(buf)-1] != ':' )` |  | pending |
| `act_move.do_train.ternary.001` | 1579 | `? "big stud" :` |  | pending |
| `act_move.do_train.ternary.002` | 1580 | `? "hot babe" :` |  | pending |
| `act_move.do_train.return.003` | 1585 | `return;` |  | pending |
| `act_move.do_train.if.023` | 1588 | `if (!str_cmp("hp",argument))` |  | pending |
| `act_move.do_train.if.024` | 1590 | `if ( cost > ch->train )` |  | pending |
| `act_move.do_train.return.004` | 1593 | `return;` |  | pending |
| `act_move.do_train.return.005` | 1602 | `return;` |  | pending |
| `act_move.do_train.if.025` | 1605 | `if (!str_cmp("mana",argument))` |  | pending |
| `act_move.do_train.if.026` | 1607 | `if ( cost > ch->train )` |  | pending |
| `act_move.do_train.return.006` | 1610 | `return;` |  | pending |
| `act_move.do_train.return.007` | 1619 | `return;` |  | pending |
| `act_move.do_train.if.027` | 1622 | `if ( ch->perm_stat[stat]  >= get_max_train(ch,stat) )` |  | pending |
| `act_move.do_train.return.008` | 1625 | `return;` |  | pending |
| `act_move.do_train.if.028` | 1628 | `if ( cost > ch->train )` |  | pending |
| `act_move.do_train.return.009` | 1631 | `return;` |  | pending |
| `act_move.do_train.return.010` | 1639 | `return;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#include <time.h>` — pending configuration/reachability review.
- Line 31: `#else` — pending configuration/reachability review.
- Line 32: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 33: `#include <sys/time.h>` — pending configuration/reachability review.
- Line 34: `#endif` — pending configuration/reachability review.
- Line 35: `#include <stdio.h>` — pending configuration/reachability review.
- Line 36: `#include <string.h>` — pending configuration/reachability review.
- Line 37: `#include "merc.h"` — pending configuration/reachability review.
- Line 38: `#include "interp.h"` — pending configuration/reachability review.

## Static tables

- `dir_name` at line 40 — pending entry/termination review.
- `rev_dir` at line 45 — pending entry/termination review.
- `movement_loss` at line 50 — pending entry/termination review.

## Commented code candidates


# src/act_info.c

Role: translation_unit. Disposition: **pending**. SHA-256: `9ca4e85047262e11356746330cf8728cfb1395171ec9de4d066d1b3ad07d3c2b`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## format_obj_to_char

[Source line 87](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:87); ends at line 119. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_list_to_char: `src/act_info.c:162` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:475` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2131` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_info.c:76` (declaration_or_dispatch_reference).

Dependencies: `IS_OBJ_STAT`, `strcat`, `IS_AFFECTED`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.format_obj_to_char.if.001` | 93 | `if ((fShort && (obj->short_descr == NULL \|\| obj->short_descr[0] == '\0'))     \|\|  (obj->description == NULL \|\| obj->description[0] == '\0'))` |  | pending |
| `act_info.format_obj_to_char.and.001` | 93 | `&& (obj->short_descr == NULL \|\| obj->short_descr[0] == '\0'))` |  | pending |
| `act_info.format_obj_to_char.or.001` | 93 | `\|\| obj->short_descr[0] == '\0'))` |  | pending |
| `act_info.format_obj_to_char.or.002` | 94 | `\|\|  (obj->description == NULL \|\| obj->description[0] == '\0'))` |  | pending |
| `act_info.format_obj_to_char.or.003` | 94 | `\|\| obj->description[0] == '\0'))` |  | pending |
| `act_info.format_obj_to_char.return.001` | 95 | `return buf;` |  | pending |
| `act_info.format_obj_to_char.if.002` | 97 | `if ( IS_OBJ_STAT(obj, ITEM_INVIS)     )` |  | pending |
| `act_info.format_obj_to_char.if.003` | 98 | `if ( IS_AFFECTED(ch, AFF_DETECT_EVIL)          && IS_OBJ_STAT(obj, ITEM_EVIL)   )` |  | pending |
| `act_info.format_obj_to_char.and.002` | 99 | `&& IS_OBJ_STAT(obj, ITEM_EVIL)   )   strcat( buf, "(Red Aura) "  );` |  | pending |
| `act_info.format_obj_to_char.if.004` | 100 | `if (IS_AFFECTED(ch, AFF_DETECT_GOOD)     &&  IS_OBJ_STAT(obj,ITEM_BLESS))` |  | pending |
| `act_info.format_obj_to_char.and.003` | 101 | `&&  IS_OBJ_STAT(obj,ITEM_BLESS))	      strcat(buf,"(Blue Aura) "	);` |  | pending |
| `act_info.format_obj_to_char.if.005` | 102 | `if ( IS_AFFECTED(ch, AFF_DETECT_MAGIC)          && IS_OBJ_STAT(obj, ITEM_MAGIC)  )` |  | pending |
| `act_info.format_obj_to_char.and.004` | 103 | `&& IS_OBJ_STAT(obj, ITEM_MAGIC)  )   strcat( buf, "(Magical) "   );` |  | pending |
| `act_info.format_obj_to_char.if.006` | 104 | `if ( IS_OBJ_STAT(obj, ITEM_GLOW)      )` |  | pending |
| `act_info.format_obj_to_char.if.007` | 105 | `if ( IS_OBJ_STAT(obj, ITEM_HUM)       )` |  | pending |
| `act_info.format_obj_to_char.if.008` | 107 | `if ( fShort )` |  | pending |
| `act_info.format_obj_to_char.if.009` | 109 | `if ( obj->short_descr != NULL )` |  | pending |
| `act_info.format_obj_to_char.if.010` | 114 | `if ( obj->description != NULL)` |  | pending |
| `act_info.format_obj_to_char.return.002` | 118 | `return buf;` |  | pending |

## show_list_to_char

[Source line 127](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:127); ends at line 239. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_char_to_char_1: `src/act_info.c:486` (lexical_call_candidate).
- do_look: `src/act_info.c:1051` (lexical_call_candidate).
- do_look: `src/act_info.c:1105` (lexical_call_candidate).
- do_inventory: `src/act_info.c:2109` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_info.c:78` (declaration_or_dispatch_reference).

Dependencies: `new_buf`, `alloc_mem`, `can_see_obj`, `format_obj_to_char`, `IS_NPC`, `IS_SET`, `strcmp`, `str_dup`, `free_string`, `sprintf`, `add_buf`, `send_to_char`, `page_to_char`, `buf_string`, `free_buf`, `free_mem`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.show_list_to_char.if.001` | 140 | `if ( ch->desc == NULL )` |  | pending |
| `act_info.show_list_to_char.return.001` | 141 | `return;` |  | pending |
| `act_info.show_list_to_char.for.001` | 149 | `for ( obj = list; obj != NULL; obj = obj->next_content )` |  | pending |
| `act_info.show_list_to_char.for.002` | 158 | `for ( obj = list; obj != NULL; obj = obj->next_content )` |  | pending |
| `act_info.show_list_to_char.if.002` | 160 | `if ( obj->wear_loc == WEAR_NONE && can_see_obj( ch, obj ))` |  | pending |
| `act_info.show_list_to_char.and.001` | 160 | `&& can_see_obj( ch, obj ))` |  | pending |
| `act_info.show_list_to_char.if.003` | 166 | `if ( IS_NPC(ch) \|\| IS_SET(ch->comm, COMM_COMBINE) )` |  | pending |
| `act_info.show_list_to_char.or.001` | 166 | `\|\| IS_SET(ch->comm, COMM_COMBINE) )` |  | pending |
| `act_info.show_list_to_char.for.003` | 172 | `for ( iShow = nShow - 1; iShow >= 0; iShow-- )` |  | pending |
| `act_info.show_list_to_char.if.004` | 174 | `if ( !strcmp( prgpstrShow[iShow], pstrShow ) )` |  | pending |
| `act_info.show_list_to_char.break.001` | 178 | `break;` |  | pending |
| `act_info.show_list_to_char.if.005` | 186 | `if ( !fCombine )` |  | pending |
| `act_info.show_list_to_char.for.004` | 198 | `for ( iShow = 0; iShow < nShow; iShow++ )` |  | pending |
| `act_info.show_list_to_char.if.006` | 200 | `if (prgpstrShow[iShow][0] == '\0')` |  | pending |
| `act_info.show_list_to_char.continue.001` | 203 | `continue;` |  | pending |
| `act_info.show_list_to_char.if.007` | 206 | `if ( IS_NPC(ch) \|\| IS_SET(ch->comm, COMM_COMBINE) )` |  | pending |
| `act_info.show_list_to_char.or.002` | 206 | `\|\| IS_SET(ch->comm, COMM_COMBINE) )` |  | pending |
| `act_info.show_list_to_char.if.008` | 208 | `if ( prgnShow[iShow] != 1 )` |  | pending |
| `act_info.show_list_to_char.if.009` | 223 | `if ( fShowNothing && nShow == 0 )` |  | pending |
| `act_info.show_list_to_char.and.002` | 223 | `&& nShow == 0 )` |  | pending |
| `act_info.show_list_to_char.if.010` | 225 | `if ( IS_NPC(ch) \|\| IS_SET(ch->comm, COMM_COMBINE) )` |  | pending |
| `act_info.show_list_to_char.or.003` | 225 | `\|\| IS_SET(ch->comm, COMM_COMBINE) )` |  | pending |
| `act_info.show_list_to_char.return.002` | 238 | `return;` |  | pending |

## show_char_to_char_0

[Source line 243](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:243); ends at line 403. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_char_to_char: `src/act_info.c:508` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_info.c:80` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `strcat`, `IS_AFFECTED`, `IS_EVIL`, `IS_GOOD`, `IS_NPC`, `send_to_char`, `PERS`, `sprintf`, `UPPER`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.show_char_to_char_0.if.001` | 249 | `if ( IS_SET(victim->comm,COMM_AFK	  )   )` |  | pending |
| `act_info.show_char_to_char_0.if.002` | 250 | `if ( IS_AFFECTED(victim, AFF_INVISIBLE)   )` |  | pending |
| `act_info.show_char_to_char_0.if.003` | 251 | `if ( victim->invis_level >= LEVEL_HERO    )` |  | pending |
| `act_info.show_char_to_char_0.if.004` | 252 | `if ( IS_AFFECTED(victim, AFF_HIDE)        )` |  | pending |
| `act_info.show_char_to_char_0.if.005` | 253 | `if ( IS_AFFECTED(victim, AFF_CHARM)       )` |  | pending |
| `act_info.show_char_to_char_0.if.006` | 254 | `if ( IS_AFFECTED(victim, AFF_PASS_DOOR)   )` |  | pending |
| `act_info.show_char_to_char_0.if.007` | 255 | `if ( IS_AFFECTED(victim, AFF_FAERIE_FIRE) )` |  | pending |
| `act_info.show_char_to_char_0.if.008` | 256 | `if ( IS_EVIL(victim)     &&   IS_AFFECTED(ch, AFF_DETECT_EVIL)     )` |  | pending |
| `act_info.show_char_to_char_0.and.001` | 257 | `&&   IS_AFFECTED(ch, AFF_DETECT_EVIL)     ) strcat( buf, "(Red Aura) "   );` |  | pending |
| `act_info.show_char_to_char_0.if.009` | 258 | `if ( IS_GOOD(victim)     &&   IS_AFFECTED(ch, AFF_DETECT_GOOD)     )` |  | pending |
| `act_info.show_char_to_char_0.and.002` | 259 | `&&   IS_AFFECTED(ch, AFF_DETECT_GOOD)     ) strcat( buf, "(Golden Aura) ");` |  | pending |
| `act_info.show_char_to_char_0.if.010` | 260 | `if ( IS_AFFECTED(victim, AFF_SANCTUARY)   )` |  | pending |
| `act_info.show_char_to_char_0.if.011` | 261 | `if ( !IS_NPC(victim) && IS_SET(victim->act, PLR_KILLER ) )` |  | pending |
| `act_info.show_char_to_char_0.and.003` | 261 | `&& IS_SET(victim->act, PLR_KILLER ) )` |  | pending |
| `act_info.show_char_to_char_0.if.012` | 263 | `if ( !IS_NPC(victim) && IS_SET(victim->act, PLR_THIEF  ) )` |  | pending |
| `act_info.show_char_to_char_0.and.004` | 263 | `&& IS_SET(victim->act, PLR_THIEF  ) )` |  | pending |
| `act_info.show_char_to_char_0.if.013` | 265 | `if ( victim->position == victim->start_pos && victim->long_descr[0] != '\0' )` |  | pending |
| `act_info.show_char_to_char_0.and.005` | 265 | `&& victim->long_descr[0] != '\0' )` |  | pending |
| `act_info.show_char_to_char_0.return.001` | 269 | `return;` |  | pending |
| `act_info.show_char_to_char_0.if.014` | 273 | `if ( !IS_NPC(victim) && !IS_SET(ch->comm, COMM_BRIEF)      &&   victim->position == POS_STANDING && ch->on == NULL )` |  | pending |
| `act_info.show_char_to_char_0.and.006` | 273 | `&& !IS_SET(ch->comm, COMM_BRIEF)` |  | pending |
| `act_info.show_char_to_char_0.and.007` | 274 | `&&   victim->position == POS_STANDING && ch->on == NULL )` |  | pending |
| `act_info.show_char_to_char_0.and.008` | 274 | `&& ch->on == NULL )` |  | pending |
| `act_info.show_char_to_char_0.switch.001` | 277 | `switch ( victim->position )` |  | pending |
| `act_info.show_char_to_char_0.case.001` | 279 | `case POS_DEAD:     strcat( buf, " is DEAD!!" );` |  | pending |
| `act_info.show_char_to_char_0.break.001` | 279 | `break;` |  | pending |
| `act_info.show_char_to_char_0.case.002` | 280 | `case POS_MORTAL:   strcat( buf, " is mortally wounded." );` |  | pending |
| `act_info.show_char_to_char_0.break.002` | 280 | `break;` |  | pending |
| `act_info.show_char_to_char_0.case.003` | 281 | `case POS_INCAP:    strcat( buf, " is incapacitated." );` |  | pending |
| `act_info.show_char_to_char_0.break.003` | 281 | `break;` |  | pending |
| `act_info.show_char_to_char_0.case.004` | 282 | `case POS_STUNNED:  strcat( buf, " is lying here stunned." );` |  | pending |
| `act_info.show_char_to_char_0.break.004` | 282 | `break;` |  | pending |
| `act_info.show_char_to_char_0.case.005` | 283 | `case POS_SLEEPING:` |  | pending |
| `act_info.show_char_to_char_0.if.015` | 284 | `if (victim->on != NULL)` |  | pending |
| `act_info.show_char_to_char_0.if.016` | 286 | `if (IS_SET(victim->on->value[2],SLEEP_AT))` |  | pending |
| `act_info.show_char_to_char_0.if.017` | 292 | `if (IS_SET(victim->on->value[2],SLEEP_ON))` |  | pending |
| `act_info.show_char_to_char_0.break.005` | 307 | `break;` |  | pending |
| `act_info.show_char_to_char_0.case.006` | 308 | `case POS_RESTING:` |  | pending |
| `act_info.show_char_to_char_0.if.018` | 309 | `if (victim->on != NULL)` |  | pending |
| `act_info.show_char_to_char_0.if.019` | 311 | `if (IS_SET(victim->on->value[2],REST_AT))` |  | pending |
| `act_info.show_char_to_char_0.if.020` | 317 | `if (IS_SET(victim->on->value[2],REST_ON))` |  | pending |
| `act_info.show_char_to_char_0.break.006` | 332 | `break;` |  | pending |
| `act_info.show_char_to_char_0.case.007` | 333 | `case POS_SITTING:` |  | pending |
| `act_info.show_char_to_char_0.if.021` | 334 | `if (victim->on != NULL)` |  | pending |
| `act_info.show_char_to_char_0.if.022` | 336 | `if (IS_SET(victim->on->value[2],SIT_AT))` |  | pending |
| `act_info.show_char_to_char_0.if.023` | 342 | `if (IS_SET(victim->on->value[2],SIT_ON))` |  | pending |
| `act_info.show_char_to_char_0.break.007` | 357 | `break;` |  | pending |
| `act_info.show_char_to_char_0.case.008` | 358 | `case POS_STANDING:` |  | pending |
| `act_info.show_char_to_char_0.if.024` | 359 | `if (victim->on != NULL)` |  | pending |
| `act_info.show_char_to_char_0.if.025` | 361 | `if (IS_SET(victim->on->value[2],STAND_AT))` |  | pending |
| `act_info.show_char_to_char_0.if.026` | 367 | `if (IS_SET(victim->on->value[2],STAND_ON))` |  | pending |
| `act_info.show_char_to_char_0.break.008` | 382 | `break;` |  | pending |
| `act_info.show_char_to_char_0.case.009` | 383 | `case POS_FIGHTING:` |  | pending |
| `act_info.show_char_to_char_0.if.027` | 385 | `if ( victim->fighting == NULL )` |  | pending |
| `act_info.show_char_to_char_0.if.028` | 387 | `if ( victim->fighting == ch )` |  | pending |
| `act_info.show_char_to_char_0.if.029` | 389 | `if ( victim->in_room == victim->fighting->in_room )` |  | pending |
| `act_info.show_char_to_char_0.break.009` | 396 | `break;` |  | pending |
| `act_info.show_char_to_char_0.return.002` | 402 | `return;` |  | pending |

## show_char_to_char_1

[Source line 407](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:407); ends at line 490. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_look: `src/act_info.c:1113` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_info.c:81` (declaration_or_dispatch_reference).

Dependencies: `can_see`, `act`, `send_to_char`, `strcpy`, `PERS`, `strcat`, `UPPER`, `get_eq_char`, `can_see_obj`, `format_obj_to_char`, `IS_NPC`, `number_percent`, `get_skill`, `check_improve`, `show_list_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.show_char_to_char_1.if.001` | 415 | `if ( can_see( victim, ch ) )` |  | pending |
| `act_info.show_char_to_char_1.if.002` | 417 | `if (ch == victim)` |  | pending |
| `act_info.show_char_to_char_1.if.003` | 426 | `if ( victim->description[0] != '\0' )` |  | pending |
| `act_info.show_char_to_char_1.if.004` | 435 | `if ( victim->max_hit > 0 )` |  | pending |
| `act_info.show_char_to_char_1.if.005` | 442 | `if (percent >= 100)` |  | pending |
| `act_info.show_char_to_char_1.if.006` | 444 | `if (percent >= 90)` |  | pending |
| `act_info.show_char_to_char_1.if.007` | 446 | `if (percent >= 75)` |  | pending |
| `act_info.show_char_to_char_1.if.008` | 448 | `if (percent >=  50)` |  | pending |
| `act_info.show_char_to_char_1.if.009` | 450 | `if (percent >= 30)` |  | pending |
| `act_info.show_char_to_char_1.if.010` | 452 | `if (percent >= 15)` |  | pending |
| `act_info.show_char_to_char_1.if.011` | 454 | `if (percent >= 0 )` |  | pending |
| `act_info.show_char_to_char_1.for.001` | 463 | `for ( iWear = 0; iWear < MAX_WEAR; iWear++ )` |  | pending |
| `act_info.show_char_to_char_1.if.012` | 465 | `if ( ( obj = get_eq_char( victim, iWear ) ) != NULL 	&&   can_see_obj( ch, obj ) )` |  | pending |
| `act_info.show_char_to_char_1.and.001` | 466 | `&&   can_see_obj( ch, obj ) )` |  | pending |
| `act_info.show_char_to_char_1.if.013` | 468 | `if ( !found )` |  | pending |
| `act_info.show_char_to_char_1.if.014` | 480 | `if ( victim != ch     &&   !IS_NPC(ch)     &&   number_percent( ) < get_skill(ch,gsn_peek))` |  | pending |
| `act_info.show_char_to_char_1.and.002` | 481 | `&&   !IS_NPC(ch)` |  | pending |
| `act_info.show_char_to_char_1.and.003` | 482 | `&&   number_percent( ) < get_skill(ch,gsn_peek))` |  | pending |
| `act_info.show_char_to_char_1.return.001` | 489 | `return;` |  | pending |

## show_char_to_char

[Source line 494](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:494); ends at line 518. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_look: `src/act_info.c:1016` (lexical_call_candidate).
- do_look: `src/act_info.c:1052` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_info.c:82` (declaration_or_dispatch_reference).

Dependencies: `get_trust`, `can_see`, `show_char_to_char_0`, `room_is_dark`, `IS_AFFECTED`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.show_char_to_char.for.001` | 498 | `for ( rch = list; rch != NULL; rch = rch->next_in_room )` |  | pending |
| `act_info.show_char_to_char.if.001` | 500 | `if ( rch == ch )` |  | pending |
| `act_info.show_char_to_char.continue.001` | 501 | `continue;` |  | pending |
| `act_info.show_char_to_char.if.002` | 503 | `if ( get_trust(ch) < rch->invis_level)` |  | pending |
| `act_info.show_char_to_char.continue.002` | 504 | `continue;` |  | pending |
| `act_info.show_char_to_char.if.003` | 506 | `if ( can_see( ch, rch ) )` |  | pending |
| `act_info.show_char_to_char.if.004` | 510 | `if ( room_is_dark( ch->in_room ) 	&&        IS_AFFECTED(rch, AFF_INFRARED ) )` |  | pending |
| `act_info.show_char_to_char.and.001` | 511 | `&&        IS_AFFECTED(rch, AFF_INFRARED ) )` |  | pending |
| `act_info.show_char_to_char.return.001` | 517 | `return;` |  | pending |

## check_blind

[Source line 522](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:522); ends at line 535. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_look: `src/act_info.c:1008` (lexical_call_candidate).
- do_exits: `src/act_info.c:1328` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_info.c:83` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `IS_AFFECTED`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.check_blind.if.001` | 525 | `if (!IS_NPC(ch) && IS_SET(ch->act,PLR_HOLYLIGHT))` |  | pending |
| `act_info.check_blind.and.001` | 525 | `&& IS_SET(ch->act,PLR_HOLYLIGHT))` |  | pending |
| `act_info.check_blind.return.001` | 526 | `return TRUE;` |  | pending |
| `act_info.check_blind.if.002` | 528 | `if ( IS_AFFECTED(ch, AFF_BLIND) )` |  | pending |
| `act_info.check_blind.return.002` | 531 | `return FALSE;` |  | pending |
| `act_info.check_blind.return.003` | 534 | `return TRUE;` |  | pending |

## do_scroll

[Source line 538](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:538); ends at line 583. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:169` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:239` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `sprintf`, `is_number`, `atoi`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_scroll.if.001` | 546 | `if (arg[0] == '\0')` |  | pending |
| `act_info.do_scroll.if.002` | 548 | `if (ch->lines == 0)` |  | pending |
| `act_info.do_scroll.return.001` | 556 | `return;` |  | pending |
| `act_info.do_scroll.if.003` | 559 | `if (!is_number(arg))` |  | pending |
| `act_info.do_scroll.return.002` | 562 | `return;` |  | pending |
| `act_info.do_scroll.if.004` | 567 | `if (lines == 0)` |  | pending |
| `act_info.do_scroll.return.003` | 571 | `return;` |  | pending |
| `act_info.do_scroll.if.005` | 574 | `if (lines < 10 \|\| lines > 100)` |  | pending |
| `act_info.do_scroll.or.001` | 574 | `\|\| lines > 100)` |  | pending |
| `act_info.do_scroll.return.004` | 577 | `return;` |  | pending |

## do_socials

[Source line 586](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:586); ends at line 605. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:132` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:255` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_socials.for.001` | 594 | `for (iSocial = 0; social_table[iSocial].name[0] != '\0'; iSocial++)` |  | pending |
| `act_info.do_socials.if.001` | 598 | `if (++col % 6 == 0)` |  | pending |
| `act_info.do_socials.if.002` | 602 | `if ( col % 6 != 0)` |  | pending |
| `act_info.do_socials.return.001` | 604 | `return;` |  | pending |

## do_motd

[Source line 611](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:611); ends at line 614. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:125` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:169` (declaration_or_dispatch_reference).

Dependencies: `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_motd.entry` | 611 | `Straight-line entry` |  | pending |

## do_imotd

[Source line 616](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:616); ends at line 619. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:348` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:153` (declaration_or_dispatch_reference).

Dependencies: `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_imotd.entry` | 616 | `Straight-line entry` |  | pending |

## do_rules

[Source line 621](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:621); ends at line 624. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:129` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:233` (declaration_or_dispatch_reference).

Dependencies: `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_rules.entry` | 621 | `Straight-line entry` |  | pending |

## do_story

[Source line 626](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:626); ends at line 629. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:135` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:264` (declaration_or_dispatch_reference).

Dependencies: `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_story.entry` | 626 | `Straight-line entry` |  | pending |

## do_wizlist

[Source line 631](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:631); ends at line 634. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:141` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:293` (declaration_or_dispatch_reference).

Dependencies: `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_wizlist.entry` | 631 | `Straight-line entry` |  | pending |

## do_autolist

[Source line 639](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:639); ends at line 716. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:149` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:82` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `send_to_char`, `IS_SET`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_autolist.if.001` | 642 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_autolist.return.001` | 643 | `return;` |  | pending |
| `act_info.do_autolist.if.002` | 649 | `if (IS_SET(ch->act,PLR_AUTOASSIST))` |  | pending |
| `act_info.do_autolist.if.003` | 655 | `if (IS_SET(ch->act,PLR_AUTOEXIT))` |  | pending |
| `act_info.do_autolist.if.004` | 661 | `if (IS_SET(ch->act,PLR_AUTOGOLD))` |  | pending |
| `act_info.do_autolist.if.005` | 667 | `if (IS_SET(ch->act,PLR_AUTOLOOT))` |  | pending |
| `act_info.do_autolist.if.006` | 673 | `if (IS_SET(ch->act,PLR_AUTOSAC))` |  | pending |
| `act_info.do_autolist.if.007` | 679 | `if (IS_SET(ch->act,PLR_AUTOSPLIT))` |  | pending |
| `act_info.do_autolist.if.008` | 685 | `if (IS_SET(ch->comm,COMM_COMPACT))` |  | pending |
| `act_info.do_autolist.if.009` | 691 | `if (IS_SET(ch->comm,COMM_PROMPT))` |  | pending |
| `act_info.do_autolist.if.010` | 697 | `if (IS_SET(ch->comm,COMM_COMBINE))` |  | pending |
| `act_info.do_autolist.if.011` | 702 | `if (!IS_SET(ch->act,PLR_CANLOOT))` |  | pending |
| `act_info.do_autolist.if.012` | 707 | `if (IS_SET(ch->act,PLR_NOSUMMON))` |  | pending |
| `act_info.do_autolist.if.013` | 712 | `if (IS_SET(ch->act,PLR_NOFOLLOW))` |  | pending |

## do_autoassist

[Source line 718](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:718); ends at line 733. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:150` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:79` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_autoassist.if.001` | 720 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_autoassist.return.001` | 721 | `return;` |  | pending |
| `act_info.do_autoassist.if.002` | 723 | `if (IS_SET(ch->act,PLR_AUTOASSIST))` |  | pending |

## do_autoexit

[Source line 735](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:735); ends at line 750. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:151` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:80` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_autoexit.if.001` | 737 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_autoexit.return.001` | 738 | `return;` |  | pending |
| `act_info.do_autoexit.if.002` | 740 | `if (IS_SET(ch->act,PLR_AUTOEXIT))` |  | pending |

## do_autogold

[Source line 752](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:752); ends at line 767. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:152` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:81` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_autogold.if.001` | 754 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_autogold.return.001` | 755 | `return;` |  | pending |
| `act_info.do_autogold.if.002` | 757 | `if (IS_SET(ch->act,PLR_AUTOGOLD))` |  | pending |

## do_autoloot

[Source line 769](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:769); ends at line 784. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:153` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:83` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_autoloot.if.001` | 771 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_autoloot.return.001` | 772 | `return;` |  | pending |
| `act_info.do_autoloot.if.002` | 774 | `if (IS_SET(ch->act,PLR_AUTOLOOT))` |  | pending |

## do_autosac

[Source line 786](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:786); ends at line 801. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:154` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:84` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_autosac.if.001` | 788 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_autosac.return.001` | 789 | `return;` |  | pending |
| `act_info.do_autosac.if.002` | 791 | `if (IS_SET(ch->act,PLR_AUTOSAC))` |  | pending |

## do_autosplit

[Source line 803](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:803); ends at line 818. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:155` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:85` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_autosplit.if.001` | 805 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_autosplit.return.001` | 806 | `return;` |  | pending |
| `act_info.do_autosplit.if.002` | 808 | `if (IS_SET(ch->act,PLR_AUTOSPLIT))` |  | pending |

## do_brief

[Source line 820](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:820); ends at line 832. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:156` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:93` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_brief.if.001` | 822 | `if (IS_SET(ch->comm,COMM_BRIEF))` |  | pending |

## do_compact

[Source line 834](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:834); ends at line 846. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:159` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:103` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_compact.if.001` | 836 | `if (IS_SET(ch->comm,COMM_COMPACT))` |  | pending |

## do_show

[Source line 848](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:848); ends at line 860. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:133` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:243` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_show.if.001` | 850 | `if (IS_SET(ch->comm,COMM_SHOW_AFFECTS))` |  | pending |

## do_prompt

[Source line 862](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:862); ends at line 899. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:168` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:206` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `strcmp`, `strcpy`, `strlen`, `smash_tilde`, `str_suffix`, `strcat`, `free_string`, `str_dup`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_prompt.if.001` | 866 | `if ( argument[0] == '\0' )` |  | pending |
| `act_info.do_prompt.if.002` | 868 | `if (IS_SET(ch->comm,COMM_PROMPT))` |  | pending |
| `act_info.do_prompt.return.001` | 878 | `return;` |  | pending |
| `act_info.do_prompt.if.003` | 881 | `if( !strcmp( argument, "all" ) )` |  | pending |
| `act_info.do_prompt.if.004` | 885 | `if ( strlen(argument) > 50 )` |  | pending |
| `act_info.do_prompt.if.005` | 889 | `if (str_suffix("%c",buf))` |  | pending |
| `act_info.do_prompt.return.002` | 898 | `return;` |  | pending |

## do_combine

[Source line 901](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:901); ends at line 913. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:158` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:102` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_combine.if.001` | 903 | `if (IS_SET(ch->comm,COMM_COMBINE))` |  | pending |

## do_noloot

[Source line 915](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:915); ends at line 930. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:164` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:178` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_noloot.if.001` | 917 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_noloot.return.001` | 918 | `return;` |  | pending |
| `act_info.do_noloot.if.002` | 920 | `if (IS_SET(ch->act,PLR_CANLOOT))` |  | pending |

## do_nofollow

[Source line 932](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:932); ends at line 948. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:163` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:177` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `die_follower`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_nofollow.if.001` | 934 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_nofollow.return.001` | 935 | `return;` |  | pending |
| `act_info.do_nofollow.if.002` | 937 | `if (IS_SET(ch->act,PLR_NOFOLLOW))` |  | pending |

## do_nosummon

[Source line 950](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:950); ends at line 978. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:165` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:181` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_nosummon.if.001` | 952 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_nosummon.if.002` | 954 | `if (IS_SET(ch->imm_flags,IMM_SUMMON))` |  | pending |
| `act_info.do_nosummon.if.003` | 967 | `if (IS_SET(ch->act,PLR_NOSUMMON))` |  | pending |

## do_look

[Source line 980](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:980); ends at line 1239. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:151` (function_symbol_reference_candidate).
- do_read: `src/act_info.c:1244` (function_symbol_reference_candidate).
- do_examine: `src/act_info.c:1261` (function_symbol_reference_candidate).
- do_examine: `src/act_info.c:1305` (function_symbol_reference_candidate).
- move_char: `src/act_move.c:202` (function_symbol_reference_candidate).
- do_stand: `src/act_move.c:933` (function_symbol_reference_candidate).
- do_recall: `src/act_move.c:1461` (function_symbol_reference_candidate).
- do_transfer: `src/act_wiz.c:857` (function_symbol_reference_candidate).
- do_goto: `src/act_wiz.c:976` (function_symbol_reference_candidate).
- do_violate: `src/act_wiz.c:1032` (function_symbol_reference_candidate).
- nanny: `src/comm.c:2118` (function_symbol_reference_candidate).
- spell_gate: `src/magic.c:2917` (function_symbol_reference_candidate).
- spell_gate: `src/magic.c:2926` (function_symbol_reference_candidate).
- spell_summon: `src/magic.c:4346` (function_symbol_reference_candidate).
- spell_teleport: `src/magic.c:4377` (function_symbol_reference_candidate).
- spell_word_of_recall: `src/magic.c:4461` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:93` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:162` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `check_blind`, `IS_NPC`, `IS_SET`, `room_is_dark`, `show_char_to_char`, `one_argument`, `number_argument`, `str_cmp`, `IS_IMMORTAL`, `sprintf`, `do_function`, `show_list_to_char`, `get_obj_here`, `act`, `get_char_room`, `show_char_to_char_1`, `can_see_obj`, `get_extra_descr`, `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_look.if.001` | 993 | `if ( ch->desc == NULL )` |  | pending |
| `act_info.do_look.return.001` | 994 | `return;` |  | pending |
| `act_info.do_look.if.002` | 996 | `if ( ch->position < POS_SLEEPING )` |  | pending |
| `act_info.do_look.return.002` | 999 | `return;` |  | pending |
| `act_info.do_look.if.003` | 1002 | `if ( ch->position == POS_SLEEPING )` |  | pending |
| `act_info.do_look.return.003` | 1005 | `return;` |  | pending |
| `act_info.do_look.if.004` | 1008 | `if ( !check_blind( ch ) )` |  | pending |
| `act_info.do_look.return.004` | 1009 | `return;` |  | pending |
| `act_info.do_look.if.005` | 1011 | `if ( !IS_NPC(ch)     &&   !IS_SET(ch->act, PLR_HOLYLIGHT)     &&   room_is_dark( ch->in_room ) )` |  | pending |
| `act_info.do_look.and.001` | 1012 | `&&   !IS_SET(ch->act, PLR_HOLYLIGHT)` |  | pending |
| `act_info.do_look.and.002` | 1013 | `&&   room_is_dark( ch->in_room ) )` |  | pending |
| `act_info.do_look.return.005` | 1017 | `return;` |  | pending |
| `act_info.do_look.if.006` | 1025 | `if ( arg1[0] == '\0' \|\| !str_cmp( arg1, "auto" ) )` |  | pending |
| `act_info.do_look.or.001` | 1025 | `\|\| !str_cmp( arg1, "auto" ) )` |  | pending |
| `act_info.do_look.if.007` | 1030 | `if (IS_IMMORTAL(ch) && (IS_NPC(ch) \|\| IS_SET(ch->act,PLR_HOLYLIGHT)))` |  | pending |
| `act_info.do_look.and.003` | 1030 | `&& (IS_NPC(ch) \|\| IS_SET(ch->act,PLR_HOLYLIGHT)))` |  | pending |
| `act_info.do_look.or.002` | 1030 | `\|\| IS_SET(ch->act,PLR_HOLYLIGHT)))` |  | pending |
| `act_info.do_look.if.008` | 1038 | `if ( arg1[0] == '\0' 	\|\| ( !IS_NPC(ch) && !IS_SET(ch->comm, COMM_BRIEF) ) )` |  | pending |
| `act_info.do_look.or.003` | 1039 | `\|\| ( !IS_NPC(ch) && !IS_SET(ch->comm, COMM_BRIEF) ) )` |  | pending |
| `act_info.do_look.and.004` | 1039 | `&& !IS_SET(ch->comm, COMM_BRIEF) ) )` |  | pending |
| `act_info.do_look.if.009` | 1045 | `if ( !IS_NPC(ch) && IS_SET(ch->act, PLR_AUTOEXIT) )` |  | pending |
| `act_info.do_look.and.005` | 1045 | `&& IS_SET(ch->act, PLR_AUTOEXIT) )` |  | pending |
| `act_info.do_look.return.006` | 1053 | `return;` |  | pending |
| `act_info.do_look.if.010` | 1056 | `if ( !str_cmp( arg1, "i" ) \|\| !str_cmp(arg1, "in")  \|\| !str_cmp(arg1,"on"))` |  | pending |
| `act_info.do_look.or.004` | 1056 | `\|\| !str_cmp(arg1, "in")  \|\| !str_cmp(arg1,"on"))` |  | pending |
| `act_info.do_look.or.005` | 1056 | `\|\| !str_cmp(arg1,"on"))` |  | pending |
| `act_info.do_look.if.011` | 1059 | `if ( arg2[0] == '\0' )` |  | pending |
| `act_info.do_look.return.007` | 1062 | `return;` |  | pending |
| `act_info.do_look.if.012` | 1065 | `if ( ( obj = get_obj_here( ch, arg2 ) ) == NULL )` |  | pending |
| `act_info.do_look.return.008` | 1068 | `return;` |  | pending |
| `act_info.do_look.switch.001` | 1071 | `switch ( obj->item_type )` |  | pending |
| `act_info.do_look.default.001` | 1073 | `default:` |  | pending |
| `act_info.do_look.break.001` | 1075 | `break;` |  | pending |
| `act_info.do_look.case.001` | 1077 | `case ITEM_DRINK_CON:` |  | pending |
| `act_info.do_look.if.013` | 1078 | `if ( obj->value[1] <= 0 )` |  | pending |
| `act_info.do_look.break.002` | 1081 | `break;` |  | pending |
| `act_info.do_look.ternary.001` | 1086 | `? "less than half-" :` |  | pending |
| `act_info.do_look.ternary.002` | 1088 | `? "about half-"     : "more than half-",` |  | pending |
| `act_info.do_look.break.003` | 1093 | `break;` |  | pending |
| `act_info.do_look.case.002` | 1095 | `case ITEM_CONTAINER:` |  | pending |
| `act_info.do_look.case.003` | 1096 | `case ITEM_CORPSE_NPC:` |  | pending |
| `act_info.do_look.case.004` | 1097 | `case ITEM_CORPSE_PC:` |  | pending |
| `act_info.do_look.if.014` | 1098 | `if ( IS_SET(obj->value[1], CONT_CLOSED) )` |  | pending |
| `act_info.do_look.break.004` | 1101 | `break;` |  | pending |
| `act_info.do_look.break.005` | 1106 | `break;` |  | pending |
| `act_info.do_look.return.009` | 1108 | `return;` |  | pending |
| `act_info.do_look.if.015` | 1111 | `if ( ( victim = get_char_room( ch, arg1 ) ) != NULL )` |  | pending |
| `act_info.do_look.return.010` | 1114 | `return;` |  | pending |
| `act_info.do_look.for.001` | 1117 | `for ( obj = ch->carrying; obj != NULL; obj = obj->next_content )` |  | pending |
| `act_info.do_look.if.016` | 1119 | `if ( can_see_obj( ch, obj ) )` |  | pending |
| `act_info.do_look.if.017` | 1122 | `if ( pdesc != NULL )` |  | pending |
| `act_info.do_look.if.018` | 1123 | `if (++count == number)` |  | pending |
| `act_info.do_look.return.011` | 1126 | `return;` |  | pending |
| `act_info.do_look.continue.001` | 1128 | `continue;` |  | pending |
| `act_info.do_look.if.019` | 1131 | `if ( pdesc != NULL )` |  | pending |
| `act_info.do_look.if.020` | 1132 | `if (++count == number)` |  | pending |
| `act_info.do_look.return.012` | 1135 | `return;` |  | pending |
| `act_info.do_look.continue.002` | 1137 | `continue;` |  | pending |
| `act_info.do_look.if.021` | 1139 | `if ( is_name( arg3, obj->name ) )` |  | pending |
| `act_info.do_look.if.022` | 1140 | `if (++count == number)` |  | pending |
| `act_info.do_look.return.013` | 1144 | `return;` |  | pending |
| `act_info.do_look.for.002` | 1149 | `for ( obj = ch->in_room->contents; obj != NULL; obj = obj->next_content )` |  | pending |
| `act_info.do_look.if.023` | 1151 | `if ( can_see_obj( ch, obj ) )` |  | pending |
| `act_info.do_look.if.024` | 1154 | `if ( pdesc != NULL )` |  | pending |
| `act_info.do_look.if.025` | 1155 | `if (++count == number)` |  | pending |
| `act_info.do_look.return.014` | 1158 | `return;` |  | pending |
| `act_info.do_look.if.026` | 1162 | `if ( pdesc != NULL )` |  | pending |
| `act_info.do_look.if.027` | 1163 | `if (++count == number)` |  | pending |
| `act_info.do_look.return.015` | 1166 | `return;` |  | pending |
| `act_info.do_look.if.028` | 1169 | `if ( is_name( arg3, obj->name ) )` |  | pending |
| `act_info.do_look.if.029` | 1170 | `if (++count == number)` |  | pending |
| `act_info.do_look.return.016` | 1174 | `return;` |  | pending |
| `act_info.do_look.if.030` | 1180 | `if (pdesc != NULL)` |  | pending |
| `act_info.do_look.if.031` | 1182 | `if (++count == number)` |  | pending |
| `act_info.do_look.return.017` | 1185 | `return;` |  | pending |
| `act_info.do_look.if.032` | 1189 | `if (count > 0 && count != number)` |  | pending |
| `act_info.do_look.and.006` | 1189 | `&& count != number)` |  | pending |
| `act_info.do_look.if.033` | 1191 | `if (count == 1)` |  | pending |
| `act_info.do_look.return.018` | 1197 | `return;` |  | pending |
| `act_info.do_look.if.034` | 1200 | `if ( !str_cmp( arg1, "n" ) \|\| !str_cmp( arg1, "north" ) )` |  | pending |
| `act_info.do_look.or.006` | 1200 | `\|\| !str_cmp( arg1, "north" ) ) door = 0;` |  | pending |
| `act_info.do_look.if.035` | 1201 | `if ( !str_cmp( arg1, "e" ) \|\| !str_cmp( arg1, "east"  ) )` |  | pending |
| `act_info.do_look.or.007` | 1201 | `\|\| !str_cmp( arg1, "east"  ) ) door = 1;` |  | pending |
| `act_info.do_look.if.036` | 1202 | `if ( !str_cmp( arg1, "s" ) \|\| !str_cmp( arg1, "south" ) )` |  | pending |
| `act_info.do_look.or.008` | 1202 | `\|\| !str_cmp( arg1, "south" ) ) door = 2;` |  | pending |
| `act_info.do_look.if.037` | 1203 | `if ( !str_cmp( arg1, "w" ) \|\| !str_cmp( arg1, "west"  ) )` |  | pending |
| `act_info.do_look.or.009` | 1203 | `\|\| !str_cmp( arg1, "west"  ) ) door = 3;` |  | pending |
| `act_info.do_look.if.038` | 1204 | `if ( !str_cmp( arg1, "u" ) \|\| !str_cmp( arg1, "up"    ) )` |  | pending |
| `act_info.do_look.or.010` | 1204 | `\|\| !str_cmp( arg1, "up"    ) ) door = 4;` |  | pending |
| `act_info.do_look.if.039` | 1205 | `if ( !str_cmp( arg1, "d" ) \|\| !str_cmp( arg1, "down"  ) )` |  | pending |
| `act_info.do_look.or.011` | 1205 | `\|\| !str_cmp( arg1, "down"  ) ) door = 5;` |  | pending |
| `act_info.do_look.return.019` | 1209 | `return;` |  | pending |
| `act_info.do_look.if.040` | 1213 | `if ( ( pexit = ch->in_room->exit[door] ) == NULL )` |  | pending |
| `act_info.do_look.return.020` | 1216 | `return;` |  | pending |
| `act_info.do_look.if.041` | 1219 | `if ( pexit->description != NULL && pexit->description[0] != '\0' )` |  | pending |
| `act_info.do_look.and.007` | 1219 | `&& pexit->description[0] != '\0' )` |  | pending |
| `act_info.do_look.if.042` | 1224 | `if ( pexit->keyword    != NULL     &&   pexit->keyword[0] != '\0'     &&   pexit->keyword[0] != ' ' )` |  | pending |
| `act_info.do_look.and.008` | 1225 | `&&   pexit->keyword[0] != '\0'` |  | pending |
| `act_info.do_look.and.009` | 1226 | `&&   pexit->keyword[0] != ' ' )` |  | pending |
| `act_info.do_look.if.043` | 1228 | `if ( IS_SET(pexit->exit_info, EX_CLOSED) )` |  | pending |
| `act_info.do_look.if.044` | 1232 | `if ( IS_SET(pexit->exit_info, EX_ISDOOR) )` |  | pending |
| `act_info.do_look.return.021` | 1238 | `return;` |  | pending |

## do_read

[Source line 1242](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1242); ends at line 1245. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:127` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:216` (declaration_or_dispatch_reference).

Dependencies: `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_read.entry` | 1242 | `Straight-line entry` |  | pending |

## do_examine

[Source line 1247](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1247); ends at line 1310. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:120` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:127` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `do_function`, `get_obj_here`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_examine.if.001` | 1255 | `if ( arg[0] == '\0' )` |  | pending |
| `act_info.do_examine.return.001` | 1258 | `return;` |  | pending |
| `act_info.do_examine.if.002` | 1263 | `if ( ( obj = get_obj_here( ch, arg ) ) != NULL )` |  | pending |
| `act_info.do_examine.switch.001` | 1265 | `switch ( obj->item_type )` |  | pending |
| `act_info.do_examine.default.001` | 1267 | `default:` |  | pending |
| `act_info.do_examine.break.001` | 1268 | `break;` |  | pending |
| `act_info.do_examine.case.001` | 1270 | `case ITEM_JUKEBOX:` |  | pending |
| `act_info.do_examine.break.002` | 1272 | `break;` |  | pending |
| `act_info.do_examine.case.002` | 1274 | `case ITEM_MONEY:` |  | pending |
| `act_info.do_examine.if.003` | 1275 | `if (obj->value[0] == 0)` |  | pending |
| `act_info.do_examine.if.004` | 1277 | `if (obj->value[1] == 0)` |  | pending |
| `act_info.do_examine.if.005` | 1279 | `if (obj->value[1] == 1)` |  | pending |
| `act_info.do_examine.if.006` | 1285 | `if (obj->value[1] == 0)` |  | pending |
| `act_info.do_examine.if.007` | 1287 | `if (obj->value[0] == 1)` |  | pending |
| `act_info.do_examine.break.003` | 1298 | `break;` |  | pending |
| `act_info.do_examine.case.003` | 1300 | `case ITEM_DRINK_CON:` |  | pending |
| `act_info.do_examine.case.004` | 1301 | `case ITEM_CONTAINER:` |  | pending |
| `act_info.do_examine.case.005` | 1302 | `case ITEM_CORPSE_NPC:` |  | pending |
| `act_info.do_examine.case.006` | 1303 | `case ITEM_CORPSE_PC:` |  | pending |
| `act_info.do_examine.return.002` | 1309 | `return;` |  | pending |

## do_exits

[Source line 1317](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1317); ends at line 1377. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_look: `src/act_info.c:1048` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:85` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:128` (declaration_or_dispatch_reference).

Dependencies: `str_cmp`, `check_blind`, `sprintf`, `IS_IMMORTAL`, `can_see_room`, `IS_SET`, `strcat`, `strlen`, `capitalize`, `room_is_dark`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_exits.if.001` | 1328 | `if ( !check_blind( ch ) )` |  | pending |
| `act_info.do_exits.return.001` | 1329 | `return;` |  | pending |
| `act_info.do_exits.if.002` | 1331 | `if (fAuto)` |  | pending |
| `act_info.do_exits.if.003` | 1333 | `if (IS_IMMORTAL(ch))` |  | pending |
| `act_info.do_exits.for.001` | 1339 | `for ( door = 0; door <= 5; door++ )` |  | pending |
| `act_info.do_exits.if.004` | 1341 | `if ( ( pexit = ch->in_room->exit[door] ) != NULL 	&&   pexit->u1.to_room != NULL 	&&   can_see_room(ch,pexit->u1.to_room)  	&&   !IS_SET(pexit->exit_info, EX_CLOSED) )` |  | pending |
| `act_info.do_exits.and.001` | 1342 | `&&   pexit->u1.to_room != NULL` |  | pending |
| `act_info.do_exits.and.002` | 1343 | `&&   can_see_room(ch,pexit->u1.to_room)` |  | pending |
| `act_info.do_exits.and.003` | 1344 | `&&   !IS_SET(pexit->exit_info, EX_CLOSED) )` |  | pending |
| `act_info.do_exits.if.005` | 1347 | `if ( fAuto )` |  | pending |
| `act_info.do_exits.ternary.001` | 1357 | `?  "Too dark to tell"` |  | pending |
| `act_info.do_exits.if.006` | 1360 | `if (IS_IMMORTAL(ch))` |  | pending |
| `act_info.do_exits.if.007` | 1369 | `if ( !found )` |  | pending |
| `act_info.do_exits.ternary.002` | 1370 | `? " none" : "None.\n\r" );` |  | pending |
| `act_info.do_exits.if.008` | 1372 | `if ( fAuto )` |  | pending |
| `act_info.do_exits.return.002` | 1376 | `return;` |  | pending |

## do_worth

[Source line 1379](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1379); ends at line 1399. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:142` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:295` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `sprintf`, `send_to_char`, `exp_per_level`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_worth.if.001` | 1383 | `if (IS_NPC(ch))` |  | pending |
| `act_info.do_worth.return.001` | 1388 | `return;` |  | pending |
| `act_info.do_worth.return.002` | 1398 | `return;` |  | pending |

## do_score

[Source line 1402](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1402); ends at line 1621. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:130` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:238` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `IS_NPC`, `get_age`, `send_to_char`, `get_trust`, `can_carry_n`, `get_carry_weight`, `can_carry_w`, `get_curr_stat`, `exp_per_level`, `GET_AC`, `case`, `IS_IMMORTAL`, `IS_SET`, `GET_HITROLL`, `GET_DAMROLL`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_score.ternary.001` | 1410 | `? "" : ch->pcdata->title,` |  | pending |
| `act_info.do_score.if.001` | 1415 | `if ( get_trust( ch ) != ch->level )` |  | pending |
| `act_info.do_score.ternary.002` | 1424 | `? "sexless" : ch->sex == 1 ? "male" : "female",` |  | pending |
| `act_info.do_score.ternary.003` | 1424 | `? "male" : "female",` |  | pending |
| `act_info.do_score.ternary.004` | 1425 | `? "mobile" : class_table[ch->class].name);` |  | pending |
| `act_info.do_score.if.002` | 1467 | `if (!IS_NPC(ch) && ch->level < LEVEL_HERO)` |  | pending |
| `act_info.do_score.and.001` | 1467 | `&& ch->level < LEVEL_HERO)` |  | pending |
| `act_info.do_score.if.003` | 1478 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_DRUNK]   > 10 )` |  | pending |
| `act_info.do_score.and.002` | 1478 | `&& ch->pcdata->condition[COND_DRUNK]   > 10 )` |  | pending |
| `act_info.do_score.if.004` | 1480 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_THIRST] ==  0 )` |  | pending |
| `act_info.do_score.and.003` | 1480 | `&& ch->pcdata->condition[COND_THIRST] ==  0 )` |  | pending |
| `act_info.do_score.if.005` | 1482 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_HUNGER]   ==  0 )` |  | pending |
| `act_info.do_score.and.004` | 1482 | `&& ch->pcdata->condition[COND_HUNGER]   ==  0 )` |  | pending |
| `act_info.do_score.switch.001` | 1485 | `switch ( ch->position )` |  | pending |
| `act_info.do_score.case.001` | 1487 | `case POS_DEAD:` |  | pending |
| `act_info.do_score.break.001` | 1489 | `break;` |  | pending |
| `act_info.do_score.case.002` | 1490 | `case POS_MORTAL:` |  | pending |
| `act_info.do_score.break.002` | 1492 | `break;` |  | pending |
| `act_info.do_score.case.003` | 1493 | `case POS_INCAP:` |  | pending |
| `act_info.do_score.break.003` | 1495 | `break;` |  | pending |
| `act_info.do_score.case.004` | 1496 | `case POS_STUNNED:` |  | pending |
| `act_info.do_score.break.004` | 1498 | `break;` |  | pending |
| `act_info.do_score.case.005` | 1499 | `case POS_SLEEPING:` |  | pending |
| `act_info.do_score.break.005` | 1501 | `break;` |  | pending |
| `act_info.do_score.case.006` | 1502 | `case POS_RESTING:` |  | pending |
| `act_info.do_score.break.006` | 1504 | `break;` |  | pending |
| `act_info.do_score.case.007` | 1505 | `case POS_SITTING:` |  | pending |
| `act_info.do_score.break.007` | 1507 | `break;` |  | pending |
| `act_info.do_score.case.008` | 1508 | `case POS_STANDING:` |  | pending |
| `act_info.do_score.break.008` | 1510 | `break;` |  | pending |
| `act_info.do_score.case.009` | 1511 | `case POS_FIGHTING:` |  | pending |
| `act_info.do_score.break.009` | 1513 | `break;` |  | pending |
| `act_info.do_score.if.006` | 1518 | `if (ch->level >= 25)` |  | pending |
| `act_info.do_score.for.001` | 1528 | `for (i = 0; i < 4; i++)` |  | pending |
| `act_info.do_score.switch.002` | 1532 | `switch(i)` |  | pending |
| `act_info.do_score.case.010` | 1534 | `case(AC_PIERCE):	temp = "piercing";` |  | pending |
| `act_info.do_score.break.010` | 1534 | `break;` |  | pending |
| `act_info.do_score.case.011` | 1535 | `case(AC_BASH):	temp = "bashing";` |  | pending |
| `act_info.do_score.break.011` | 1535 | `break;` |  | pending |
| `act_info.do_score.case.012` | 1536 | `case(AC_SLASH):	temp = "slashing";` |  | pending |
| `act_info.do_score.break.012` | 1536 | `break;` |  | pending |
| `act_info.do_score.case.013` | 1537 | `case(AC_EXOTIC):	temp = "magic";` |  | pending |
| `act_info.do_score.break.013` | 1537 | `break;` |  | pending |
| `act_info.do_score.default.001` | 1538 | `default:		temp = "error";` |  | pending |
| `act_info.do_score.break.014` | 1538 | `break;` |  | pending |
| `act_info.do_score.if.007` | 1543 | `if      (GET_AC(ch,i) >=  101 )` |  | pending |
| `act_info.do_score.if.008` | 1545 | `if (GET_AC(ch,i) >= 80)` |  | pending |
| `act_info.do_score.if.009` | 1547 | `if (GET_AC(ch,i) >= 60)` |  | pending |
| `act_info.do_score.if.010` | 1549 | `if (GET_AC(ch,i) >= 40)` |  | pending |
| `act_info.do_score.if.011` | 1551 | `if (GET_AC(ch,i) >= 20)` |  | pending |
| `act_info.do_score.if.012` | 1553 | `if (GET_AC(ch,i) >= 0)` |  | pending |
| `act_info.do_score.if.013` | 1555 | `if (GET_AC(ch,i) >= -20)` |  | pending |
| `act_info.do_score.if.014` | 1557 | `if (GET_AC(ch,i) >= -40)` |  | pending |
| `act_info.do_score.if.015` | 1559 | `if (GET_AC(ch,i) >= -60)` |  | pending |
| `act_info.do_score.if.016` | 1561 | `if (GET_AC(ch,i) >= -80)` |  | pending |
| `act_info.do_score.if.017` | 1563 | `if (GET_AC(ch,i) >= -100)` |  | pending |
| `act_info.do_score.if.018` | 1573 | `if ( IS_IMMORTAL(ch))` |  | pending |
| `act_info.do_score.if.019` | 1576 | `if (IS_SET(ch->act,PLR_HOLYLIGHT))` |  | pending |
| `act_info.do_score.if.020` | 1581 | `if (ch->invis_level)` |  | pending |
| `act_info.do_score.if.021` | 1587 | `if (ch->incog_level)` |  | pending |
| `act_info.do_score.if.022` | 1595 | `if ( ch->level >= 15 )` |  | pending |
| `act_info.do_score.if.023` | 1602 | `if ( ch->level >= 10 )` |  | pending |
| `act_info.do_score.if.024` | 1609 | `if ( ch->alignment >  900 )` |  | pending |
| `act_info.do_score.if.025` | 1610 | `if ( ch->alignment >  700 )` |  | pending |
| `act_info.do_score.if.026` | 1611 | `if ( ch->alignment >  350 )` |  | pending |
| `act_info.do_score.if.027` | 1612 | `if ( ch->alignment >  100 )` |  | pending |
| `act_info.do_score.if.028` | 1613 | `if ( ch->alignment > -100 )` |  | pending |
| `act_info.do_score.if.029` | 1614 | `if ( ch->alignment > -350 )` |  | pending |
| `act_info.do_score.if.030` | 1615 | `if ( ch->alignment > -700 )` |  | pending |
| `act_info.do_score.if.031` | 1616 | `if ( ch->alignment > -900 )` |  | pending |
| `act_info.do_score.if.032` | 1619 | `if (IS_SET(ch->comm,COMM_SHOW_AFFECTS))` |  | pending |

## do_affects

[Source line 1623](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1623); ends at line 1665. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_score: `src/act_info.c:1620` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:110` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:70` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `sprintf`, `affect_loc_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_affects.if.001` | 1628 | `if ( ch->affected != NULL )` |  | pending |
| `act_info.do_affects.for.001` | 1631 | `for ( paf = ch->affected; paf != NULL; paf = paf->next )` |  | pending |
| `act_info.do_affects.if.002` | 1633 | `if (paf_last != NULL && paf->type == paf_last->type)` |  | pending |
| `act_info.do_affects.and.001` | 1633 | `&& paf->type == paf_last->type)` |  | pending |
| `act_info.do_affects.if.003` | 1634 | `if (ch->level >= 20)` |  | pending |
| `act_info.do_affects.continue.001` | 1637 | `continue;` |  | pending |
| `act_info.do_affects.if.004` | 1643 | `if ( ch->level >= 20 )` |  | pending |
| `act_info.do_affects.if.005` | 1650 | `if ( paf->duration == -1 )` |  | pending |
| `act_info.do_affects.return.001` | 1664 | `return;` |  | pending |

## do_time

[Source line 1683](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1683); ends at line 1713. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:136` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:268` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `send_to_char`, `ctime`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_time.if.001` | 1692 | `if ( day > 4 && day <  20 )` |  | pending |
| `act_info.do_time.and.001` | 1692 | `&& day <  20 ) suf = "th";` |  | pending |
| `act_info.do_time.if.002` | 1693 | `if ( day % 10 ==  1       )` |  | pending |
| `act_info.do_time.if.003` | 1694 | `if ( day % 10 ==  2       )` |  | pending |
| `act_info.do_time.if.004` | 1695 | `if ( day % 10 ==  3       )` |  | pending |
| `act_info.do_time.ternary.001` | 1700 | `? 12 : time_info.hour %12,` |  | pending |
| `act_info.do_time.ternary.002` | 1701 | `? "pm" : "am",` |  | pending |
| `act_info.do_time.return.001` | 1712 | `return;` |  | pending |

## do_weather

[Source line 1717](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1717); ends at line 1743. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:138` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:285` (declaration_or_dispatch_reference).

Dependencies: `IS_OUTSIDE`, `send_to_char`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_weather.if.001` | 1729 | `if ( !IS_OUTSIDE(ch) )` |  | pending |
| `act_info.do_weather.return.001` | 1732 | `return;` |  | pending |
| `act_info.do_weather.ternary.001` | 1738 | `? "a warm southerly breeze blows"` |  | pending |
| `act_info.do_weather.return.002` | 1742 | `return;` |  | pending |

## do_help

[Source line 1745](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1745); ends at line 1807. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_motd: `src/act_info.c:613` (function_symbol_reference_candidate).
- do_imotd: `src/act_info.c:618` (function_symbol_reference_candidate).
- do_rules: `src/act_info.c:623` (function_symbol_reference_candidate).
- do_story: `src/act_info.c:628` (function_symbol_reference_candidate).
- do_wizlist: `src/act_info.c:633` (function_symbol_reference_candidate).
- do_credits: `src/act_info.c:2251` (function_symbol_reference_candidate).
- nanny: `src/comm.c:1673` (function_symbol_reference_candidate).
- nanny: `src/comm.c:1678` (function_symbol_reference_candidate).
- nanny: `src/comm.c:1816` (function_symbol_reference_candidate).
- nanny: `src/comm.c:1818` (function_symbol_reference_candidate).
- nanny: `src/comm.c:1949` (function_symbol_reference_candidate).
- nanny: `src/comm.c:1953` (function_symbol_reference_candidate).
- nanny: `src/comm.c:1999` (function_symbol_reference_candidate).
- nanny: `src/comm.c:2053` (function_symbol_reference_candidate).
- nanny: `src/comm.c:2058` (function_symbol_reference_candidate).
- nanny: `src/comm.c:2101` (function_symbol_reference_candidate).
- parse_gen_groups: `src/skills.c:675` (function_symbol_reference_candidate).
- parse_gen_groups: `src/skills.c:679` (function_symbol_reference_candidate).
- parse_gen_groups: `src/skills.c:804` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:122` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:146` (declaration_or_dispatch_reference).

Dependencies: `new_buf`, `one_argument`, `strcat`, `get_trust`, `is_name`, `add_buf`, `str_cmp`, `send_to_char`, `page_to_char`, `buf_string`, `free_buf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_help.if.001` | 1755 | `if ( argument[0] == '\0' )` |  | pending |
| `act_info.do_help.while.001` | 1760 | `while (argument[0] != '\0' )` |  | pending |
| `act_info.do_help.if.002` | 1763 | `if (argall[0] != '\0')` |  | pending |
| `act_info.do_help.for.001` | 1768 | `for ( pHelp = help_first; pHelp != NULL; pHelp = pHelp->next )` |  | pending |
| `act_info.do_help.ternary.001` | 1770 | `? -1 * pHelp->level - 1 : pHelp->level;` |  | pending |
| `act_info.do_help.if.003` | 1772 | `if (level > get_trust( ch ) )` |  | pending |
| `act_info.do_help.continue.001` | 1773 | `continue;` |  | pending |
| `act_info.do_help.if.004` | 1775 | `if ( is_name( argall, pHelp->keyword ) )` |  | pending |
| `act_info.do_help.if.005` | 1778 | `if (found)` |  | pending |
| `act_info.do_help.if.006` | 1781 | `if ( pHelp->level >= 0 && str_cmp( argall, "imotd" ) )` |  | pending |
| `act_info.do_help.and.001` | 1781 | `&& str_cmp( argall, "imotd" ) )` |  | pending |
| `act_info.do_help.if.007` | 1790 | `if ( pHelp->text[0] == '.' )` |  | pending |
| `act_info.do_help.if.008` | 1796 | `if (ch->desc != NULL && ch->desc->connected != CON_PLAYING  	    &&  		    ch->desc->connected != CON_GEN_GROUPS)` |  | pending |
| `act_info.do_help.and.002` | 1796 | `&& ch->desc->connected != CON_PLAYING` |  | pending |
| `act_info.do_help.and.003` | 1797 | `&&  		    ch->desc->connected != CON_GEN_GROUPS)` |  | pending |
| `act_info.do_help.break.001` | 1798 | `break;` |  | pending |
| `act_info.do_help.if.009` | 1802 | `if (!found)` |  | pending |

## do_whois

[Source line 1811](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1811); ends at line 1886. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:140` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:289` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `new_buf`, `can_see`, `str_prefix`, `sprintf`, `IS_SET`, `IS_NPC`, `add_buf`, `page_to_char`, `buf_string`, `free_buf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_whois.if.001` | 1821 | `if (arg[0] == '\0')` |  | pending |
| `act_info.do_whois.return.001` | 1824 | `return;` |  | pending |
| `act_info.do_whois.for.001` | 1829 | `for (d = descriptor_list; d != NULL; d = d->next)` |  | pending |
| `act_info.do_whois.if.002` | 1834 | `if (d->connected != CON_PLAYING \|\| !can_see(ch,d->character))` |  | pending |
| `act_info.do_whois.or.001` | 1834 | `\|\| !can_see(ch,d->character))` |  | pending |
| `act_info.do_whois.continue.001` | 1835 | `continue;` |  | pending |
| `act_info.do_whois.ternary.001` | 1837 | `? d->original : d->character;` |  | pending |
| `act_info.do_whois.if.003` | 1839 | `if (!can_see(ch,wch))` |  | pending |
| `act_info.do_whois.continue.002` | 1840 | `continue;` |  | pending |
| `act_info.do_whois.if.004` | 1842 | `if (!str_prefix(arg,wch->name))` |  | pending |
| `act_info.do_whois.switch.001` | 1848 | `switch(wch->level)` |  | pending |
| `act_info.do_whois.case.001` | 1850 | `case MAX_LEVEL - 0 : class = "IMP";` |  | pending |
| `act_info.do_whois.break.001` | 1850 | `break;` |  | pending |
| `act_info.do_whois.case.002` | 1851 | `case MAX_LEVEL - 1 : class = "CRE";` |  | pending |
| `act_info.do_whois.break.002` | 1851 | `break;` |  | pending |
| `act_info.do_whois.case.003` | 1852 | `case MAX_LEVEL - 2 : class = "SUP";` |  | pending |
| `act_info.do_whois.break.003` | 1852 | `break;` |  | pending |
| `act_info.do_whois.case.004` | 1853 | `case MAX_LEVEL - 3 : class = "DEI";` |  | pending |
| `act_info.do_whois.break.004` | 1853 | `break;` |  | pending |
| `act_info.do_whois.case.005` | 1854 | `case MAX_LEVEL - 4 : class = "GOD";` |  | pending |
| `act_info.do_whois.break.005` | 1854 | `break;` |  | pending |
| `act_info.do_whois.case.006` | 1855 | `case MAX_LEVEL - 5 : class = "IMM";` |  | pending |
| `act_info.do_whois.break.006` | 1855 | `break;` |  | pending |
| `act_info.do_whois.case.007` | 1856 | `case MAX_LEVEL - 6 : class = "DEM";` |  | pending |
| `act_info.do_whois.break.007` | 1856 | `break;` |  | pending |
| `act_info.do_whois.case.008` | 1857 | `case MAX_LEVEL - 7 : class = "ANG";` |  | pending |
| `act_info.do_whois.break.008` | 1857 | `break;` |  | pending |
| `act_info.do_whois.case.009` | 1858 | `case MAX_LEVEL - 8 : class = "AVA";` |  | pending |
| `act_info.do_whois.break.009` | 1858 | `break;` |  | pending |
| `act_info.do_whois.ternary.002` | 1864 | `? pc_race_table[wch->race].who_name` |  | pending |
| `act_info.do_whois.ternary.003` | 1867 | `? "(Incog) ": "",` |  | pending |
| `act_info.do_whois.ternary.004` | 1868 | `? "(Wizi) " : "",` |  | pending |
| `act_info.do_whois.ternary.005` | 1870 | `? "[AFK] " : "",` |  | pending |
| `act_info.do_whois.ternary.006` | 1871 | `? "(KILLER) " : "",` |  | pending |
| `act_info.do_whois.ternary.007` | 1872 | `? "(THIEF) " : "",` |  | pending |
| `act_info.do_whois.ternary.008` | 1873 | `? "" : wch->pcdata->title);` |  | pending |
| `act_info.do_whois.if.005` | 1878 | `if (!found)` |  | pending |
| `act_info.do_whois.return.002` | 1881 | `return;` |  | pending |

## do_who

[Source line 1892](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1892); ends at line 2080. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:139` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:288` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `is_number`, `atoi`, `send_to_char`, `str_prefix`, `class_lookup`, `race_lookup`, `clan_lookup`, `new_buf`, `can_see`, `is_clan`, `sprintf`, `IS_SET`, `IS_NPC`, `add_buf`, `page_to_char`, `buf_string`, `free_buf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_who.for.001` | 1919 | `for ( iClass = 0; iClass < MAX_CLASS; iClass++ )` |  | pending |
| `act_info.do_who.for.002` | 1921 | `for ( iRace = 0; iRace < MAX_PC_RACE; iRace++ )` |  | pending |
| `act_info.do_who.for.003` | 1923 | `for (iClan = 0; iClan < MAX_CLAN; iClan++)` |  | pending |
| `act_info.do_who.for.004` | 1930 | `for ( ;; )` |  | pending |
| `act_info.do_who.if.001` | 1935 | `if ( arg[0] == '\0' )` |  | pending |
| `act_info.do_who.break.001` | 1936 | `break;` |  | pending |
| `act_info.do_who.if.002` | 1938 | `if ( is_number( arg ) )` |  | pending |
| `act_info.do_who.switch.001` | 1940 | `switch ( ++nNumber )` |  | pending |
| `act_info.do_who.case.001` | 1942 | `case 1: iLevelLower = atoi( arg );` |  | pending |
| `act_info.do_who.break.002` | 1942 | `break;` |  | pending |
| `act_info.do_who.case.002` | 1943 | `case 2: iLevelUpper = atoi( arg );` |  | pending |
| `act_info.do_who.break.003` | 1943 | `break;` |  | pending |
| `act_info.do_who.default.001` | 1944 | `default:` |  | pending |
| `act_info.do_who.return.001` | 1946 | `return;` |  | pending |
| `act_info.do_who.if.003` | 1955 | `if (!str_prefix(arg,"immortals"))` |  | pending |
| `act_info.do_who.if.004` | 1962 | `if (iClass == -1)` |  | pending |
| `act_info.do_who.if.005` | 1966 | `if (iRace == 0 \|\| iRace >= MAX_PC_RACE)` |  | pending |
| `act_info.do_who.or.001` | 1966 | `\|\| iRace >= MAX_PC_RACE)` |  | pending |
| `act_info.do_who.if.006` | 1968 | `if (!str_prefix(arg,"clan"))` |  | pending |
| `act_info.do_who.if.007` | 1973 | `if (iClan)` |  | pending |
| `act_info.do_who.return.002` | 1983 | `return;` |  | pending |
| `act_info.do_who.for.005` | 2008 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_info.do_who.if.008` | 2017 | `if ( d->connected != CON_PLAYING \|\| !can_see( ch, d->character ) )` |  | pending |
| `act_info.do_who.or.002` | 2017 | `\|\| !can_see( ch, d->character ) )` |  | pending |
| `act_info.do_who.continue.001` | 2018 | `continue;` |  | pending |
| `act_info.do_who.ternary.001` | 2020 | `? d->original : d->character;` |  | pending |
| `act_info.do_who.if.009` | 2022 | `if (!can_see(ch,wch))` |  | pending |
| `act_info.do_who.continue.002` | 2023 | `continue;` |  | pending |
| `act_info.do_who.if.010` | 2025 | `if ( wch->level < iLevelLower         \|\|   wch->level > iLevelUpper         \|\| ( fImmortalOnly  && wch->level < LEVEL_IMMORTAL )         \|\| ( fClassRestrict && !rgfClass[wch->class] )         \|\| ( fRaceRestrict && !rgfRace[wch->race])  	\|\| ( fClan && !is_clan(wch)) 	\|\| ( fClanRestrict && !rgfClan[wch->clan]))` |  | pending |
| `act_info.do_who.or.003` | 2026 | `\|\|   wch->level > iLevelUpper` |  | pending |
| `act_info.do_who.or.004` | 2027 | `\|\| ( fImmortalOnly  && wch->level < LEVEL_IMMORTAL )` |  | pending |
| `act_info.do_who.and.001` | 2027 | `&& wch->level < LEVEL_IMMORTAL )` |  | pending |
| `act_info.do_who.or.005` | 2028 | `\|\| ( fClassRestrict && !rgfClass[wch->class] )` |  | pending |
| `act_info.do_who.and.002` | 2028 | `&& !rgfClass[wch->class] )` |  | pending |
| `act_info.do_who.or.006` | 2029 | `\|\| ( fRaceRestrict && !rgfRace[wch->race])` |  | pending |
| `act_info.do_who.and.003` | 2029 | `&& !rgfRace[wch->race])` |  | pending |
| `act_info.do_who.or.007` | 2030 | `\|\| ( fClan && !is_clan(wch))` |  | pending |
| `act_info.do_who.and.004` | 2030 | `&& !is_clan(wch))` |  | pending |
| `act_info.do_who.or.008` | 2031 | `\|\| ( fClanRestrict && !rgfClan[wch->clan]))` |  | pending |
| `act_info.do_who.and.005` | 2031 | `&& !rgfClan[wch->clan]))` |  | pending |
| `act_info.do_who.continue.003` | 2032 | `continue;` |  | pending |
| `act_info.do_who.switch.002` | 2040 | `switch ( wch->level )` |  | pending |
| `act_info.do_who.default.002` | 2042 | `default: break;` |  | pending |
| `act_info.do_who.break.004` | 2042 | `break;` |  | pending |
| `act_info.do_who.case.003` | 2044 | `case MAX_LEVEL - 0 : class = "IMP";` |  | pending |
| `act_info.do_who.break.005` | 2044 | `break;` |  | pending |
| `act_info.do_who.case.004` | 2045 | `case MAX_LEVEL - 1 : class = "CRE";` |  | pending |
| `act_info.do_who.break.006` | 2045 | `break;` |  | pending |
| `act_info.do_who.case.005` | 2046 | `case MAX_LEVEL - 2 : class = "SUP";` |  | pending |
| `act_info.do_who.break.007` | 2046 | `break;` |  | pending |
| `act_info.do_who.case.006` | 2047 | `case MAX_LEVEL - 3 : class = "DEI";` |  | pending |
| `act_info.do_who.break.008` | 2047 | `break;` |  | pending |
| `act_info.do_who.case.007` | 2048 | `case MAX_LEVEL - 4 : class = "GOD";` |  | pending |
| `act_info.do_who.break.009` | 2048 | `break;` |  | pending |
| `act_info.do_who.case.008` | 2049 | `case MAX_LEVEL - 5 : class = "IMM";` |  | pending |
| `act_info.do_who.break.010` | 2049 | `break;` |  | pending |
| `act_info.do_who.case.009` | 2050 | `case MAX_LEVEL - 6 : class = "DEM";` |  | pending |
| `act_info.do_who.break.011` | 2050 | `break;` |  | pending |
| `act_info.do_who.case.010` | 2051 | `case MAX_LEVEL - 7 : class = "ANG";` |  | pending |
| `act_info.do_who.break.012` | 2051 | `break;` |  | pending |
| `act_info.do_who.case.011` | 2052 | `case MAX_LEVEL - 8 : class = "AVA";` |  | pending |
| `act_info.do_who.break.013` | 2052 | `break;` |  | pending |
| `act_info.do_who.ternary.002` | 2061 | `? pc_race_table[wch->race].who_name` |  | pending |
| `act_info.do_who.ternary.003` | 2064 | `? "(Incog) " : "",` |  | pending |
| `act_info.do_who.ternary.004` | 2065 | `? "(Wizi) " : "",` |  | pending |
| `act_info.do_who.ternary.005` | 2067 | `? "[AFK] " : "",` |  | pending |
| `act_info.do_who.ternary.006` | 2068 | `? "(KILLER) " : "",` |  | pending |
| `act_info.do_who.ternary.007` | 2069 | `? "(THIEF) "  : "",` |  | pending |
| `act_info.do_who.ternary.008` | 2071 | `? "" : wch->pcdata->title );` |  | pending |
| `act_info.do_who.return.003` | 2079 | `return;` |  | pending |

## do_count

[Source line 2082](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2082); ends at line 2104. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:117` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:106` (declaration_or_dispatch_reference).

Dependencies: `can_see`, `UMAX`, `sprintf`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_count.for.001` | 2090 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_info.do_count.if.001` | 2091 | `if ( d->connected == CON_PLAYING && can_see( ch, d->character ) )` |  | pending |
| `act_info.do_count.and.001` | 2091 | `&& can_see( ch, d->character ) )` |  | pending |
| `act_info.do_count.if.002` | 2096 | `if (max_on == count)` |  | pending |

## do_inventory

[Source line 2106](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2106); ends at line 2111. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:91` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:154` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `show_list_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_inventory.return.001` | 2110 | `return;` |  | pending |

## do_equipment

[Source line 2115](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2115); ends at line 2145. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:119` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:126` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_eq_char`, `can_see_obj`, `format_obj_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_equipment.for.001` | 2123 | `for ( iWear = 0; iWear < MAX_WEAR; iWear++ )` |  | pending |
| `act_info.do_equipment.if.001` | 2125 | `if ( ( obj = get_eq_char( ch, iWear ) ) == NULL )` |  | pending |
| `act_info.do_equipment.continue.001` | 2126 | `continue;` |  | pending |
| `act_info.do_equipment.if.002` | 2129 | `if ( can_see_obj( ch, obj ) )` |  | pending |
| `act_info.do_equipment.if.003` | 2141 | `if ( !found )` |  | pending |
| `act_info.do_equipment.return.001` | 2144 | `return;` |  | pending |

## do_compare

[Source line 2149](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2149); ends at line 2245. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:115` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:104` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_carry`, `can_see_obj`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_compare.if.001` | 2161 | `if ( arg1[0] == '\0' )` |  | pending |
| `act_info.do_compare.return.001` | 2164 | `return;` |  | pending |
| `act_info.do_compare.if.002` | 2167 | `if ( ( obj1 = get_obj_carry( ch, arg1, ch ) ) == NULL )` |  | pending |
| `act_info.do_compare.return.002` | 2170 | `return;` |  | pending |
| `act_info.do_compare.if.003` | 2173 | `if (arg2[0] == '\0')` |  | pending |
| `act_info.do_compare.for.001` | 2175 | `for (obj2 = ch->carrying; obj2 != NULL; obj2 = obj2->next_content)` |  | pending |
| `act_info.do_compare.if.004` | 2177 | `if (obj2->wear_loc != WEAR_NONE 	    &&  can_see_obj(ch,obj2) 	    &&  obj1->item_type == obj2->item_type 	    &&  (obj1->wear_flags & obj2->wear_flags & ~ITEM_TAKE) != 0 )` |  | pending |
| `act_info.do_compare.and.001` | 2178 | `&&  can_see_obj(ch,obj2)` |  | pending |
| `act_info.do_compare.and.002` | 2179 | `&&  obj1->item_type == obj2->item_type` |  | pending |
| `act_info.do_compare.and.003` | 2180 | `&&  (obj1->wear_flags & obj2->wear_flags & ~ITEM_TAKE) != 0 )` |  | pending |
| `act_info.do_compare.break.001` | 2181 | `break;` |  | pending |
| `act_info.do_compare.if.005` | 2184 | `if (obj2 == NULL)` |  | pending |
| `act_info.do_compare.return.003` | 2187 | `return;` |  | pending |
| `act_info.do_compare.if.006` | 2191 | `if ( (obj2 = get_obj_carry(ch,arg2,ch) ) == NULL )` |  | pending |
| `act_info.do_compare.return.004` | 2194 | `return;` |  | pending |
| `act_info.do_compare.if.007` | 2201 | `if ( obj1 == obj2 )` |  | pending |
| `act_info.do_compare.if.008` | 2205 | `if ( obj1->item_type != obj2->item_type )` |  | pending |
| `act_info.do_compare.switch.001` | 2211 | `switch ( obj1->item_type )` |  | pending |
| `act_info.do_compare.default.001` | 2213 | `default:` |  | pending |
| `act_info.do_compare.break.002` | 2215 | `break;` |  | pending |
| `act_info.do_compare.case.001` | 2217 | `case ITEM_ARMOR:` |  | pending |
| `act_info.do_compare.break.003` | 2220 | `break;` |  | pending |
| `act_info.do_compare.case.002` | 2222 | `case ITEM_WEAPON:` |  | pending |
| `act_info.do_compare.if.009` | 2223 | `if (obj1->pIndexData->new_format)` |  | pending |
| `act_info.do_compare.if.010` | 2228 | `if (obj2->pIndexData->new_format)` |  | pending |
| `act_info.do_compare.break.004` | 2232 | `break;` |  | pending |
| `act_info.do_compare.if.011` | 2236 | `if ( msg == NULL )` |  | pending |
| `act_info.do_compare.if.012` | 2238 | `if ( value1 == value2 )` |  | pending |
| `act_info.do_compare.if.013` | 2239 | `if ( value1  > value2 )` |  | pending |
| `act_info.do_compare.return.005` | 2244 | `return;` |  | pending |

## do_credits

[Source line 2249](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2249); ends at line 2253. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:118` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:107` (declaration_or_dispatch_reference).

Dependencies: `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_credits.return.001` | 2252 | `return;` |  | pending |

## do_where

[Source line 2257](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2257); ends at line 2316. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:276` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:287` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `IS_NPC`, `IS_SET`, `is_room_owner`, `room_is_private`, `can_see`, `sprintf`, `IS_AFFECTED`, `is_name`, `PERS`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_where.if.001` | 2267 | `if ( arg[0] == '\0' )` |  | pending |
| `act_info.do_where.for.001` | 2271 | `for ( d = descriptor_list; d; d = d->next )` |  | pending |
| `act_info.do_where.if.002` | 2273 | `if ( d->connected == CON_PLAYING 	    && ( victim = d->character ) != NULL 	    &&   !IS_NPC(victim) 	    &&   victim->in_room != NULL 	    &&   !IS_SET(victim->in_room->room_flags,ROOM_NOWHERE)  	    &&   (is_room_owner(ch,victim->in_room)  	    \|\|    !room_is_private(victim->in_room)) 	    &&   victim->in_room->area == ch->in_room->area 	    &&   can_see( ch, victim ) )` |  | pending |
| `act_info.do_where.and.001` | 2274 | `&& ( victim = d->character ) != NULL` |  | pending |
| `act_info.do_where.and.002` | 2275 | `&&   !IS_NPC(victim)` |  | pending |
| `act_info.do_where.and.003` | 2276 | `&&   victim->in_room != NULL` |  | pending |
| `act_info.do_where.and.004` | 2277 | `&&   !IS_SET(victim->in_room->room_flags,ROOM_NOWHERE)` |  | pending |
| `act_info.do_where.and.005` | 2278 | `&&   (is_room_owner(ch,victim->in_room)` |  | pending |
| `act_info.do_where.or.001` | 2279 | `\|\|    !room_is_private(victim->in_room))` |  | pending |
| `act_info.do_where.and.006` | 2280 | `&&   victim->in_room->area == ch->in_room->area` |  | pending |
| `act_info.do_where.and.007` | 2281 | `&&   can_see( ch, victim ) )` |  | pending |
| `act_info.do_where.if.003` | 2289 | `if ( !found )` |  | pending |
| `act_info.do_where.for.002` | 2295 | `for ( victim = char_list; victim != NULL; victim = victim->next )` |  | pending |
| `act_info.do_where.if.004` | 2297 | `if ( victim->in_room != NULL 	    &&   victim->in_room->area == ch->in_room->area 	    &&   !IS_AFFECTED(victim, AFF_HIDE) 	    &&   !IS_AFFECTED(victim, AFF_SNEAK) 	    &&   can_see( ch, victim ) 	    &&   is_name( arg, victim->name ) )` |  | pending |
| `act_info.do_where.and.008` | 2298 | `&&   victim->in_room->area == ch->in_room->area` |  | pending |
| `act_info.do_where.and.009` | 2299 | `&&   !IS_AFFECTED(victim, AFF_HIDE)` |  | pending |
| `act_info.do_where.and.010` | 2300 | `&&   !IS_AFFECTED(victim, AFF_SNEAK)` |  | pending |
| `act_info.do_where.and.011` | 2301 | `&&   can_see( ch, victim )` |  | pending |
| `act_info.do_where.and.012` | 2302 | `&&   is_name( arg, victim->name ) )` |  | pending |
| `act_info.do_where.break.001` | 2308 | `break;` |  | pending |
| `act_info.do_where.if.005` | 2311 | `if ( !found )` |  | pending |
| `act_info.do_where.return.001` | 2315 | `return;` |  | pending |

## do_consider

[Source line 2321](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2321); ends at line 2360. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:116` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:105` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_room`, `is_safe`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_consider.if.001` | 2330 | `if ( arg[0] == '\0' )` |  | pending |
| `act_info.do_consider.return.001` | 2333 | `return;` |  | pending |
| `act_info.do_consider.if.002` | 2336 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `act_info.do_consider.return.002` | 2339 | `return;` |  | pending |
| `act_info.do_consider.if.003` | 2342 | `if (is_safe(ch,victim))` |  | pending |
| `act_info.do_consider.return.003` | 2345 | `return;` |  | pending |
| `act_info.do_consider.if.004` | 2350 | `if ( diff <= -10 )` |  | pending |
| `act_info.do_consider.if.005` | 2351 | `if ( diff <=  -5 )` |  | pending |
| `act_info.do_consider.if.006` | 2352 | `if ( diff <=  -2 )` |  | pending |
| `act_info.do_consider.if.007` | 2353 | `if ( diff <=   1 )` |  | pending |
| `act_info.do_consider.if.008` | 2354 | `if ( diff <=   4 )` |  | pending |
| `act_info.do_consider.if.009` | 2355 | `if ( diff <=   9 )` |  | pending |
| `act_info.do_consider.return.004` | 2359 | `return;` |  | pending |

## set_title

[Source line 2364](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2364); ends at line 2387. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_title: `src/act_info.c:2406` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3780` (lexical_call_candidate).
- nanny: `src/comm.c:2094` (lexical_call_candidate).
- advance_level: `src/update.c:74` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2082` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `bug`, `strcpy`, `free_string`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.set_title.if.001` | 2368 | `if ( IS_NPC(ch) )` |  | pending |
| `act_info.set_title.return.001` | 2371 | `return;` |  | pending |
| `act_info.set_title.if.002` | 2374 | `if ( title[0] != '.' && title[0] != ',' && title[0] != '!' && title[0] != '?' )` |  | pending |
| `act_info.set_title.and.001` | 2374 | `&& title[0] != ',' && title[0] != '!' && title[0] != '?' )` |  | pending |
| `act_info.set_title.and.002` | 2374 | `&& title[0] != '!' && title[0] != '?' )` |  | pending |
| `act_info.set_title.and.003` | 2374 | `&& title[0] != '?' )` |  | pending |
| `act_info.set_title.return.002` | 2386 | `return;` |  | pending |

## do_title

[Source line 2391](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2391); ends at line 2408. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:170` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:269` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `send_to_char`, `strlen`, `smash_tilde`, `set_title`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_title.if.001` | 2393 | `if ( IS_NPC(ch) )` |  | pending |
| `act_info.do_title.return.001` | 2394 | `return;` |  | pending |
| `act_info.do_title.if.002` | 2396 | `if ( argument[0] == '\0' )` |  | pending |
| `act_info.do_title.return.002` | 2399 | `return;` |  | pending |
| `act_info.do_title.if.003` | 2402 | `if ( strlen(argument) > 45 )` |  | pending |

## do_description

[Source line 2412](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2412); ends at line 2486. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:160` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:112` (declaration_or_dispatch_reference).

Dependencies: `smash_tilde`, `send_to_char`, `strcpy`, `strlen`, `free_string`, `str_dup`, `strcat`, `isspace`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_description.if.001` | 2416 | `if ( argument[0] != '\0' )` |  | pending |
| `act_info.do_description.if.002` | 2421 | `if (argument[0] == '-')` |  | pending |
| `act_info.do_description.if.003` | 2426 | `if (ch->description == NULL \|\| ch->description[0] == '\0')` |  | pending |
| `act_info.do_description.or.001` | 2426 | `\|\| ch->description[0] == '\0')` |  | pending |
| `act_info.do_description.return.001` | 2429 | `return;` |  | pending |
| `act_info.do_description.for.001` | 2434 | `for (len = strlen(buf); len > 0; len--)` |  | pending |
| `act_info.do_description.if.004` | 2436 | `if (buf[len] == '\r')` |  | pending |
| `act_info.do_description.if.005` | 2438 | `if (!found)` |  | pending |
| `act_info.do_description.if.006` | 2440 | `if (len > 0)` |  | pending |
| `act_info.do_description.ternary.001` | 2450 | `? ch->description :` |  | pending |
| `act_info.do_description.return.002` | 2452 | `return;` |  | pending |
| `act_info.do_description.return.003` | 2460 | `return;` |  | pending |
| `act_info.do_description.if.007` | 2462 | `if ( argument[0] == '+' )` |  | pending |
| `act_info.do_description.if.008` | 2464 | `if ( ch->description != NULL )` |  | pending |
| `act_info.do_description.while.001` | 2467 | `while ( isspace(*argument) )` |  | pending |
| `act_info.do_description.if.009` | 2471 | `if ( strlen(buf) >= 1024)` |  | pending |
| `act_info.do_description.return.004` | 2474 | `return;` |  | pending |
| `act_info.do_description.ternary.002` | 2484 | `? ch->description : "(None).\n\r", ch );` |  | pending |
| `act_info.do_description.return.005` | 2485 | `return;` |  | pending |

## do_report

[Source line 2490](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2490); ends at line 2512. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:128` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:226` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `send_to_char`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_report.return.001` | 2511 | `return;` |  | pending |

## do_practice

[Source line 2516](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2516); ends at line 2622. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:97` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:203` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `sprintf`, `send_to_char`, `IS_AWAKE`, `IS_SET`, `find_spell`, `get_curr_stat`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_practice.if.001` | 2521 | `if ( IS_NPC(ch) )` |  | pending |
| `act_info.do_practice.return.001` | 2522 | `return;` |  | pending |
| `act_info.do_practice.if.002` | 2524 | `if ( argument[0] == '\0' )` |  | pending |
| `act_info.do_practice.for.001` | 2529 | `for ( sn = 0; sn < MAX_SKILL; sn++ )` |  | pending |
| `act_info.do_practice.if.003` | 2531 | `if ( skill_table[sn].name == NULL )` |  | pending |
| `act_info.do_practice.break.001` | 2532 | `break;` |  | pending |
| `act_info.do_practice.if.004` | 2533 | `if ( ch->level < skill_table[sn].skill_level[ch->class]  	      \|\| ch->pcdata->learned[sn] < 1 /* skill is not known */)` |  | pending |
| `act_info.do_practice.or.001` | 2534 | `\|\| ch->pcdata->learned[sn] < 1 /* skill is not known */)` |  | pending |
| `act_info.do_practice.continue.001` | 2535 | `continue;` |  | pending |
| `act_info.do_practice.if.005` | 2540 | `if ( ++col % 3 == 0 )` |  | pending |
| `act_info.do_practice.if.006` | 2544 | `if ( col % 3 != 0 )` |  | pending |
| `act_info.do_practice.if.007` | 2556 | `if ( !IS_AWAKE(ch) )` |  | pending |
| `act_info.do_practice.return.002` | 2559 | `return;` |  | pending |
| `act_info.do_practice.for.002` | 2562 | `for ( mob = ch->in_room->people; mob != NULL; mob = mob->next_in_room )` |  | pending |
| `act_info.do_practice.if.008` | 2564 | `if ( IS_NPC(mob) && IS_SET(mob->act, ACT_PRACTICE) )` |  | pending |
| `act_info.do_practice.and.001` | 2564 | `&& IS_SET(mob->act, ACT_PRACTICE) )` |  | pending |
| `act_info.do_practice.break.002` | 2565 | `break;` |  | pending |
| `act_info.do_practice.if.009` | 2568 | `if ( mob == NULL )` |  | pending |
| `act_info.do_practice.return.003` | 2571 | `return;` |  | pending |
| `act_info.do_practice.if.010` | 2574 | `if ( ch->practice <= 0 )` |  | pending |
| `act_info.do_practice.return.004` | 2577 | `return;` |  | pending |
| `act_info.do_practice.if.011` | 2580 | `if ( ( sn = find_spell( ch,argument ) ) < 0 	\|\| ( !IS_NPC(ch) 	&&   (ch->level < skill_table[sn].skill_level[ch->class]   	\|\|    ch->pcdata->learned[sn] < 1 /* skill is not known */ 	\|\|    skill_table[sn].rating[ch->class] == 0)))` |  | pending |
| `act_info.do_practice.or.002` | 2581 | `\|\| ( !IS_NPC(ch)` |  | pending |
| `act_info.do_practice.and.002` | 2582 | `&&   (ch->level < skill_table[sn].skill_level[ch->class]` |  | pending |
| `act_info.do_practice.or.003` | 2583 | `\|\|    ch->pcdata->learned[sn] < 1 /* skill is not known */` |  | pending |
| `act_info.do_practice.or.004` | 2584 | `\|\|    skill_table[sn].rating[ch->class] == 0)))` |  | pending |
| `act_info.do_practice.return.005` | 2587 | `return;` |  | pending |
| `act_info.do_practice.ternary.001` | 2590 | `? 100 : class_table[ch->class].skill_adept;` |  | pending |
| `act_info.do_practice.if.012` | 2592 | `if ( ch->pcdata->learned[sn] >= adept )` |  | pending |
| `act_info.do_practice.if.013` | 2604 | `if ( ch->pcdata->learned[sn] < adept )` |  | pending |
| `act_info.do_practice.return.006` | 2621 | `return;` |  | pending |

## do_wimpy

[Source line 2629](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2629); ends at line 2658. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:172` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:290` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `atoi`, `send_to_char`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_wimpy.if.001` | 2637 | `if ( arg[0] == '\0' )` |  | pending |
| `act_info.do_wimpy.if.002` | 2642 | `if ( wimpy < 0 )` |  | pending |
| `act_info.do_wimpy.return.001` | 2645 | `return;` |  | pending |
| `act_info.do_wimpy.if.003` | 2648 | `if ( wimpy > ch->max_hit/2 )` |  | pending |
| `act_info.do_wimpy.return.002` | 2651 | `return;` |  | pending |
| `act_info.do_wimpy.return.003` | 2657 | `return;` |  | pending |

## do_password

[Source line 2662](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2662); ends at line 2755. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:167` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:193` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `isspace`, `send_to_char`, `strcmp`, `crypt`, `WAIT_STATE`, `strlen`, `free_string`, `str_dup`, `save_char_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_info.do_password.if.001` | 2671 | `if ( IS_NPC(ch) )` |  | pending |
| `act_info.do_password.return.001` | 2672 | `return;` |  | pending |
| `act_info.do_password.while.001` | 2679 | `while ( isspace(*argument) )` |  | pending |
| `act_info.do_password.if.002` | 2683 | `if ( *argument == '\'' \|\| *argument == '"' )` |  | pending |
| `act_info.do_password.or.001` | 2683 | `\|\| *argument == '"' )` |  | pending |
| `act_info.do_password.while.002` | 2686 | `while ( *argument != '\0' )` |  | pending |
| `act_info.do_password.if.003` | 2688 | `if ( *argument == cEnd )` |  | pending |
| `act_info.do_password.break.001` | 2691 | `break;` |  | pending |
| `act_info.do_password.while.003` | 2698 | `while ( isspace(*argument) )` |  | pending |
| `act_info.do_password.if.004` | 2702 | `if ( *argument == '\'' \|\| *argument == '"' )` |  | pending |
| `act_info.do_password.or.002` | 2702 | `\|\| *argument == '"' )` |  | pending |
| `act_info.do_password.while.004` | 2705 | `while ( *argument != '\0' )` |  | pending |
| `act_info.do_password.if.005` | 2707 | `if ( *argument == cEnd )` |  | pending |
| `act_info.do_password.break.002` | 2710 | `break;` |  | pending |
| `act_info.do_password.if.006` | 2716 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' )` |  | pending |
| `act_info.do_password.or.003` | 2716 | `\|\| arg2[0] == '\0' )` |  | pending |
| `act_info.do_password.return.002` | 2719 | `return;` |  | pending |
| `act_info.do_password.if.007` | 2722 | `if ( strcmp( crypt( arg1, ch->pcdata->pwd ), ch->pcdata->pwd ) )` |  | pending |
| `act_info.do_password.return.003` | 2726 | `return;` |  | pending |
| `act_info.do_password.if.008` | 2729 | `if ( strlen(arg2) < 5 )` |  | pending |
| `act_info.do_password.return.004` | 2733 | `return;` |  | pending |
| `act_info.do_password.for.001` | 2740 | `for ( p = pwdnew; *p != '\0'; p++ )` |  | pending |
| `act_info.do_password.if.009` | 2742 | `if ( *p == '~' )` |  | pending |
| `act_info.do_password.return.005` | 2746 | `return;` |  | pending |
| `act_info.do_password.return.006` | 2754 | `return;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#include <sys/time.h>` — pending configuration/reachability review.
- Line 33: `#endif` — pending configuration/reachability review.
- Line 34: `#include <stdio.h>` — pending configuration/reachability review.
- Line 35: `#include <string.h>` — pending configuration/reachability review.
- Line 36: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 37: `#include <ctype.h>` — pending configuration/reachability review.
- Line 38: `#include <time.h>` — pending configuration/reachability review.
- Line 39: `#include "merc.h"` — pending configuration/reachability review.
- Line 40: `#include "interp.h"` — pending configuration/reachability review.
- Line 41: `#include "magic.h"` — pending configuration/reachability review.
- Line 42: `#include "recycle.h"` — pending configuration/reachability review.
- Line 43: `#include "tables.h"` — pending configuration/reachability review.
- Line 44: `#include "lookup.h"` — pending configuration/reachability review.

## Static tables

- `where_name` at line 46 — pending entry/termination review.
- `day_name` at line 1669 — pending entry/termination review.
- `month_name` at line 1675 — pending entry/termination review.
- `sky_look` at line 1721 — pending entry/termination review.

## Commented code candidates


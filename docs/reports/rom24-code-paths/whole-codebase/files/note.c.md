# src/note.c

Role: translation_unit. Disposition: **pending**. SHA-256: `27b94bb1cf2e9bdf725f6d617067bef4fd67daf3efde51d2bdefa9b1d54bc0da`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## count_spool

[Source line 61](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:61); ends at line 71. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_unread: `src/note.c:82` (lexical_call_candidate).
- do_unread: `src/note.c:89` (lexical_call_candidate).
- do_unread: `src/note.c:96` (lexical_call_candidate).
- do_unread: `src/note.c:103` (lexical_call_candidate).
- do_unread: `src/note.c:110` (lexical_call_candidate).

Dependencies: `hide_note`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.count_spool.for.001` | 66 | `for (pnote = spool; pnote != NULL; pnote = pnote->next)` |  | pending |
| `note.count_spool.if.001` | 67 | `if (!hide_note(ch,pnote))` |  | pending |
| `note.count_spool.return.001` | 70 | `return count;` |  | pending |

## do_unread

[Source line 73](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:73); ends at line 120. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:2129` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:200` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:277` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `count_spool`, `sprintf`, `send_to_char`, `IS_TRUSTED`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.do_unread.if.001` | 79 | `if (IS_NPC(ch))` |  | pending |
| `note.do_unread.return.001` | 80 | `return;` |  | pending |
| `note.do_unread.if.002` | 82 | `if ((count = count_spool(ch,news_list)) > 0)` |  | pending |
| `note.do_unread.ternary.001` | 86 | `? "are" : "is",count, count > 1 ? "s" : "");` |  | pending |
| `note.do_unread.ternary.002` | 86 | `? "s" : "");` |  | pending |
| `note.do_unread.if.003` | 89 | `if ((count = count_spool(ch,changes_list)) > 0)` |  | pending |
| `note.do_unread.ternary.003` | 93 | `? "are" : "is", count, count > 1 ? "s" : "");` |  | pending |
| `note.do_unread.ternary.004` | 93 | `? "s" : "");` |  | pending |
| `note.do_unread.if.004` | 96 | `if ((count = count_spool(ch,note_list)) > 0)` |  | pending |
| `note.do_unread.ternary.005` | 100 | `? "s" : "");` |  | pending |
| `note.do_unread.if.005` | 103 | `if ((count = count_spool(ch,idea_list)) > 0)` |  | pending |
| `note.do_unread.ternary.006` | 107 | `? "s" : "");` |  | pending |
| `note.do_unread.if.006` | 110 | `if (IS_TRUSTED(ch,ANGEL) && (count = count_spool(ch,penalty_list)) > 0)` |  | pending |
| `note.do_unread.and.001` | 110 | `&& (count = count_spool(ch,penalty_list)) > 0)` |  | pending |
| `note.do_unread.ternary.007` | 114 | `? "penalties have" : "penalty has");` |  | pending |
| `note.do_unread.if.007` | 118 | `if (!found)` |  | pending |

## do_note

[Source line 122](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:122); ends at line 125. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:190` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:182` (declaration_or_dispatch_reference).

Dependencies: `parse_note`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.do_note.entry` | 122 | `Straight-line entry` |  | pending |

## do_idea

[Source line 127](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:127); ends at line 130. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:123` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:149` (declaration_or_dispatch_reference).

Dependencies: `parse_note`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.do_idea.entry` | 127 | `Straight-line entry` |  | pending |

## do_penalty

[Source line 132](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:132); ends at line 135. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:333` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:196` (declaration_or_dispatch_reference).

Dependencies: `parse_note`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.do_penalty.entry` | 132 | `Straight-line entry` |  | pending |

## do_news

[Source line 137](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:137); ends at line 140. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:126` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:174` (declaration_or_dispatch_reference).

Dependencies: `parse_note`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.do_news.entry` | 137 | `Straight-line entry` |  | pending |

## do_changes

[Source line 142](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:142); ends at line 145. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:113` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:97` (declaration_or_dispatch_reference).

Dependencies: `parse_note`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.do_changes.entry` | 142 | `Straight-line entry` |  | pending |

## save_notes

[Source line 147](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:147); ends at line 199. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- note_remove: `src/note.c:464` (lexical_call_candidate).

Dependencies: `fclose`, `fopen`, `perror`, `fprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.save_notes.switch.001` | 153 | `switch (type)` |  | pending |
| `note.save_notes.default.001` | 155 | `default:` |  | pending |
| `note.save_notes.return.001` | 156 | `return;` |  | pending |
| `note.save_notes.case.001` | 157 | `case NOTE_NOTE:` |  | pending |
| `note.save_notes.break.001` | 160 | `break;` |  | pending |
| `note.save_notes.case.002` | 161 | `case NOTE_IDEA:` |  | pending |
| `note.save_notes.break.002` | 164 | `break;` |  | pending |
| `note.save_notes.case.003` | 165 | `case NOTE_PENALTY:` |  | pending |
| `note.save_notes.break.003` | 168 | `break;` |  | pending |
| `note.save_notes.case.004` | 169 | `case NOTE_NEWS:` |  | pending |
| `note.save_notes.break.004` | 172 | `break;` |  | pending |
| `note.save_notes.case.005` | 173 | `case NOTE_CHANGES:` |  | pending |
| `note.save_notes.break.005` | 176 | `break;` |  | pending |
| `note.save_notes.if.001` | 180 | `if ( ( fp = fopen( name, "w" ) ) == NULL )` |  | pending |
| `note.save_notes.for.001` | 186 | `for ( ; pnote != NULL; pnote = pnote->next )` |  | pending |
| `note.save_notes.return.002` | 197 | `return;` |  | pending |

## load_notes

[Source line 200](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:200); ends at line 207. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:383` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:223` (declaration_or_dispatch_reference).

Dependencies: `load_thread`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.load_notes.entry` | 200 | `Straight-line entry` |  | pending |

## load_thread

[Source line 209](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:209); ends at line 282. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_notes: `src/note.c:202` (lexical_call_candidate).
- load_notes: `src/note.c:203` (lexical_call_candidate).
- load_notes: `src/note.c:204` (lexical_call_candidate).
- load_notes: `src/note.c:205` (lexical_call_candidate).
- load_notes: `src/note.c:206` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/note.c:51` (declaration_or_dispatch_reference).

Dependencies: `fopen`, `getc`, `feof`, `fclose`, `isspace`, `ungetc`, `alloc_perm`, `str_cmp`, `fread_word`, `fread_string`, `fread_number`, `free_note`, `strcpy`, `bug`, `exit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.load_thread.if.001` | 214 | `if ( ( fp = fopen( name, "r" ) ) == NULL )` |  | pending |
| `note.load_thread.return.001` | 215 | `return;` |  | pending |
| `note.load_thread.for.001` | 218 | `for ( ; ; )` |  | pending |
| `note.load_thread.if.002` | 226 | `if ( feof(fp) )` |  | pending |
| `note.load_thread.return.002` | 229 | `return;` |  | pending |
| `note.load_thread.while.001` | 232 | `while ( isspace(letter) )` |  | pending |
| `note.load_thread.if.003` | 237 | `if ( str_cmp( fread_word( fp ), "sender" ) )` |  | pending |
| `note.load_thread.break.001` | 238 | `break;` |  | pending |
| `note.load_thread.if.004` | 241 | `if ( str_cmp( fread_word( fp ), "date" ) )` |  | pending |
| `note.load_thread.break.002` | 242 | `break;` |  | pending |
| `note.load_thread.if.005` | 245 | `if ( str_cmp( fread_word( fp ), "stamp" ) )` |  | pending |
| `note.load_thread.break.003` | 246 | `break;` |  | pending |
| `note.load_thread.if.006` | 249 | `if ( str_cmp( fread_word( fp ), "to" ) )` |  | pending |
| `note.load_thread.break.004` | 250 | `break;` |  | pending |
| `note.load_thread.if.007` | 253 | `if ( str_cmp( fread_word( fp ), "subject" ) )` |  | pending |
| `note.load_thread.break.005` | 254 | `break;` |  | pending |
| `note.load_thread.if.008` | 257 | `if ( str_cmp( fread_word( fp ), "text" ) )` |  | pending |
| `note.load_thread.break.006` | 258 | `break;` |  | pending |
| `note.load_thread.if.009` | 261 | `if (free_time && pnote->date_stamp < current_time - free_time)` |  | pending |
| `note.load_thread.and.001` | 261 | `&& pnote->date_stamp < current_time - free_time)` |  | pending |
| `note.load_thread.continue.001` | 264 | `continue;` |  | pending |
| `note.load_thread.if.010` | 269 | `if (*list == NULL)` |  | pending |
| `note.load_thread.return.003` | 281 | `return;` |  | pending |

## append_note

[Source line 284](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:284); ends at line 341. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- parse_note: `src/note.c:952` (lexical_call_candidate).

Dependencies: `fclose`, `fopen`, `perror`, `fprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.append_note.switch.001` | 291 | `switch(pnote->type)` |  | pending |
| `note.append_note.default.001` | 293 | `default:` |  | pending |
| `note.append_note.return.001` | 294 | `return;` |  | pending |
| `note.append_note.case.001` | 295 | `case NOTE_NOTE:` |  | pending |
| `note.append_note.break.001` | 298 | `break;` |  | pending |
| `note.append_note.case.002` | 299 | `case NOTE_IDEA:` |  | pending |
| `note.append_note.break.002` | 302 | `break;` |  | pending |
| `note.append_note.case.003` | 303 | `case NOTE_PENALTY:` |  | pending |
| `note.append_note.break.003` | 306 | `break;` |  | pending |
| `note.append_note.case.004` | 307 | `case NOTE_NEWS:` |  | pending |
| `note.append_note.break.004` | 310 | `break;` |  | pending |
| `note.append_note.case.005` | 311 | `case NOTE_CHANGES:` |  | pending |
| `note.append_note.break.005` | 314 | `break;` |  | pending |
| `note.append_note.if.001` | 317 | `if (*list == NULL)` |  | pending |
| `note.append_note.for.001` | 321 | `for ( last = *list; last->next != NULL; last = last->next)` |  | pending |
| `note.append_note.if.002` | 326 | `if ( ( fp = fopen(name, "a" ) ) == NULL )` |  | pending |

## is_note_to

[Source line 343](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:343); ends at line 361. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- hide_note: `src/note.c:503` (lexical_call_candidate).
- parse_note: `src/note.c:612` (lexical_call_candidate).
- parse_note: `src/note.c:634` (lexical_call_candidate).
- parse_note: `src/note.c:660` (lexical_call_candidate).
- parse_note: `src/note.c:705` (lexical_call_candidate).
- parse_note: `src/note.c:730` (lexical_call_candidate).

Dependencies: `str_cmp`, `is_exact_name`, `IS_IMMORTAL`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.is_note_to.if.001` | 345 | `if ( !str_cmp( ch->name, pnote->sender ) )` |  | pending |
| `note.is_note_to.return.001` | 346 | `return TRUE;` |  | pending |
| `note.is_note_to.if.002` | 348 | `if ( is_exact_name( "all", pnote->to_list ) )` |  | pending |
| `note.is_note_to.return.002` | 349 | `return TRUE;` |  | pending |
| `note.is_note_to.if.003` | 351 | `if ( IS_IMMORTAL(ch) && is_exact_name( "immortal", pnote->to_list ) )` |  | pending |
| `note.is_note_to.and.001` | 351 | `&& is_exact_name( "immortal", pnote->to_list ) )` |  | pending |
| `note.is_note_to.return.003` | 352 | `return TRUE;` |  | pending |
| `note.is_note_to.if.004` | 354 | `if (ch->clan && is_exact_name(clan_table[ch->clan].name,pnote->to_list))` |  | pending |
| `note.is_note_to.and.002` | 354 | `&& is_exact_name(clan_table[ch->clan].name,pnote->to_list))` |  | pending |
| `note.is_note_to.return.004` | 355 | `return TRUE;` |  | pending |
| `note.is_note_to.if.005` | 357 | `if (is_exact_name( ch->name, pnote->to_list ) )` |  | pending |
| `note.is_note_to.return.005` | 358 | `return TRUE;` |  | pending |
| `note.is_note_to.return.006` | 360 | `return FALSE;` |  | pending |

## note_attach

[Source line 365](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:365); ends at line 383. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- parse_note: `src/note.c:777` (lexical_call_candidate).
- parse_note: `src/note.c:808` (lexical_call_candidate).
- parse_note: `src/note.c:851` (lexical_call_candidate).
- parse_note: `src/note.c:867` (lexical_call_candidate).

Dependencies: `new_note`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.note_attach.if.001` | 369 | `if ( ch->pnote != NULL )` |  | pending |
| `note.note_attach.return.001` | 370 | `return;` |  | pending |
| `note.note_attach.return.002` | 382 | `return;` |  | pending |

## note_remove

[Source line 387](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:387); ends at line 467. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- parse_note: `src/note.c:707` (lexical_call_candidate).
- parse_note: `src/note.c:732` (lexical_call_candidate).

Dependencies: `one_argument`, `str_cmp`, `strcat`, `free_string`, `str_dup`, `bug`, `save_notes`, `free_note`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.note_remove.if.001` | 395 | `if (!delete)` |  | pending |
| `note.note_remove.while.001` | 400 | `while ( *to_list != '\0' )` |  | pending |
| `note.note_remove.if.002` | 403 | `if ( to_one[0] != '\0' && str_cmp( ch->name, to_one ) )` |  | pending |
| `note.note_remove.and.001` | 403 | `&& str_cmp( ch->name, to_one ) )` |  | pending |
| `note.note_remove.if.003` | 410 | `if ( str_cmp( ch->name, pnote->sender ) && to_new[0] != '\0' )` |  | pending |
| `note.note_remove.and.002` | 410 | `&& to_new[0] != '\0' )` |  | pending |
| `note.note_remove.return.001` | 414 | `return;` |  | pending |
| `note.note_remove.switch.001` | 419 | `switch(pnote->type)` |  | pending |
| `note.note_remove.default.001` | 421 | `default:` |  | pending |
| `note.note_remove.return.002` | 422 | `return;` |  | pending |
| `note.note_remove.case.001` | 423 | `case NOTE_NOTE:` |  | pending |
| `note.note_remove.break.001` | 425 | `break;` |  | pending |
| `note.note_remove.case.002` | 426 | `case NOTE_IDEA:` |  | pending |
| `note.note_remove.break.002` | 428 | `break;` |  | pending |
| `note.note_remove.case.003` | 429 | `case NOTE_PENALTY:` |  | pending |
| `note.note_remove.break.003` | 431 | `break;` |  | pending |
| `note.note_remove.case.004` | 432 | `case NOTE_NEWS:` |  | pending |
| `note.note_remove.break.004` | 434 | `break;` |  | pending |
| `note.note_remove.case.005` | 435 | `case NOTE_CHANGES:` |  | pending |
| `note.note_remove.break.005` | 437 | `break;` |  | pending |
| `note.note_remove.if.004` | 443 | `if ( pnote == *list )` |  | pending |
| `note.note_remove.for.001` | 449 | `for ( prev = *list; prev != NULL; prev = prev->next )` |  | pending |
| `note.note_remove.if.005` | 451 | `if ( prev->next == pnote )` |  | pending |
| `note.note_remove.break.006` | 452 | `break;` |  | pending |
| `note.note_remove.if.006` | 455 | `if ( prev == NULL )` |  | pending |
| `note.note_remove.return.003` | 458 | `return;` |  | pending |
| `note.note_remove.return.004` | 466 | `return;` |  | pending |

## hide_note

[Source line 469](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:469); ends at line 507. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- count_spool: `src/note.c:67` (lexical_call_candidate).
- parse_note: `src/note.c:599` (lexical_call_candidate).
- parse_note: `src/note.c:663` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/note.c:53` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `str_cmp`, `is_note_to`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.hide_note.if.001` | 473 | `if (IS_NPC(ch))` |  | pending |
| `note.hide_note.return.001` | 474 | `return TRUE;` |  | pending |
| `note.hide_note.switch.001` | 476 | `switch (pnote->type)` |  | pending |
| `note.hide_note.default.001` | 478 | `default:` |  | pending |
| `note.hide_note.return.002` | 479 | `return TRUE;` |  | pending |
| `note.hide_note.case.001` | 480 | `case NOTE_NOTE:` |  | pending |
| `note.hide_note.break.001` | 482 | `break;` |  | pending |
| `note.hide_note.case.002` | 483 | `case NOTE_IDEA:` |  | pending |
| `note.hide_note.break.002` | 485 | `break;` |  | pending |
| `note.hide_note.case.003` | 486 | `case NOTE_PENALTY:` |  | pending |
| `note.hide_note.break.003` | 488 | `break;` |  | pending |
| `note.hide_note.case.004` | 489 | `case NOTE_NEWS:` |  | pending |
| `note.hide_note.break.004` | 491 | `break;` |  | pending |
| `note.hide_note.case.005` | 492 | `case NOTE_CHANGES:` |  | pending |
| `note.hide_note.break.005` | 494 | `break;` |  | pending |
| `note.hide_note.if.002` | 497 | `if (pnote->date_stamp <= last_read)` |  | pending |
| `note.hide_note.return.003` | 498 | `return TRUE;` |  | pending |
| `note.hide_note.if.003` | 500 | `if (!str_cmp(ch->name,pnote->sender))` |  | pending |
| `note.hide_note.return.004` | 501 | `return TRUE;` |  | pending |
| `note.hide_note.if.004` | 503 | `if (!is_note_to(ch,pnote))` |  | pending |
| `note.hide_note.return.005` | 504 | `return TRUE;` |  | pending |
| `note.hide_note.return.006` | 506 | `return FALSE;` |  | pending |

## update_read

[Source line 509](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:509); ends at line 538. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- parse_note: `src/note.c:609` (lexical_call_candidate).
- parse_note: `src/note.c:645` (lexical_call_candidate).

Dependencies: `IS_NPC`, `UMAX`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.update_read.if.001` | 513 | `if (IS_NPC(ch))` |  | pending |
| `note.update_read.return.001` | 514 | `return;` |  | pending |
| `note.update_read.switch.001` | 518 | `switch (pnote->type)` |  | pending |
| `note.update_read.default.001` | 520 | `default:` |  | pending |
| `note.update_read.return.002` | 521 | `return;` |  | pending |
| `note.update_read.case.001` | 522 | `case NOTE_NOTE:` |  | pending |
| `note.update_read.break.001` | 524 | `break;` |  | pending |
| `note.update_read.case.002` | 525 | `case NOTE_IDEA:` |  | pending |
| `note.update_read.break.002` | 527 | `break;` |  | pending |
| `note.update_read.case.003` | 528 | `case NOTE_PENALTY:` |  | pending |
| `note.update_read.break.003` | 530 | `break;` |  | pending |
| `note.update_read.case.004` | 531 | `case NOTE_NEWS:` |  | pending |
| `note.update_read.break.004` | 533 | `break;` |  | pending |
| `note.update_read.case.005` | 534 | `case NOTE_CHANGES:` |  | pending |
| `note.update_read.break.005` | 536 | `break;` |  | pending |

## parse_note

[Source line 540](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:540); ends at line 959. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_note: `src/note.c:124` (lexical_call_candidate).
- do_idea: `src/note.c:129` (lexical_call_candidate).
- do_penalty: `src/note.c:134` (lexical_call_candidate).
- do_news: `src/note.c:139` (lexical_call_candidate).
- do_changes: `src/note.c:144` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/note.c:52` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `one_argument`, `smash_tilde`, `str_prefix`, `str_cmp`, `hide_note`, `sprintf`, `send_to_char`, `page_to_char`, `update_read`, `is_note_to`, `is_number`, `atoi`, `note_remove`, `get_trust`, `IS_TRUSTED`, `note_attach`, `strlen`, `new_buf`, `add_buf`, `free_string`, `str_dup`, `buf_string`, `free_buf`, `strcpy`, `free_note`, `ctime`, `append_note`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `note.parse_note.if.001` | 551 | `if ( IS_NPC(ch) )` |  | pending |
| `note.parse_note.return.001` | 552 | `return;` |  | pending |
| `note.parse_note.switch.001` | 554 | `switch(type)` |  | pending |
| `note.parse_note.default.001` | 556 | `default:` |  | pending |
| `note.parse_note.return.002` | 557 | `return;` |  | pending |
| `note.parse_note.case.001` | 558 | `case NOTE_NOTE:` |  | pending |
| `note.parse_note.break.001` | 561 | `break;` |  | pending |
| `note.parse_note.case.002` | 562 | `case NOTE_IDEA:` |  | pending |
| `note.parse_note.break.002` | 565 | `break;` |  | pending |
| `note.parse_note.case.003` | 566 | `case NOTE_PENALTY:` |  | pending |
| `note.parse_note.break.003` | 569 | `break;` |  | pending |
| `note.parse_note.case.004` | 570 | `case NOTE_NEWS:` |  | pending |
| `note.parse_note.break.004` | 573 | `break;` |  | pending |
| `note.parse_note.case.005` | 574 | `case NOTE_CHANGES:` |  | pending |
| `note.parse_note.break.005` | 577 | `break;` |  | pending |
| `note.parse_note.if.002` | 583 | `if ( arg[0] == '\0' \|\| !str_prefix( arg, "read" ) )` |  | pending |
| `note.parse_note.or.001` | 583 | `\|\| !str_prefix( arg, "read" ) )` |  | pending |
| `note.parse_note.if.003` | 587 | `if ( !str_cmp( argument, "all" ) )` |  | pending |
| `note.parse_note.if.004` | 593 | `if ( argument[0] == '\0' \|\| !str_prefix(argument, "next"))` |  | pending |
| `note.parse_note.or.002` | 593 | `\|\| !str_prefix(argument, "next"))` |  | pending |
| `note.parse_note.for.001` | 597 | `for ( pnote = *list; pnote != NULL; pnote = pnote->next)` |  | pending |
| `note.parse_note.if.005` | 599 | `if (!hide_note(ch,pnote))` |  | pending |
| `note.parse_note.return.003` | 610 | `return;` |  | pending |
| `note.parse_note.if.006` | 612 | `if (is_note_to(ch,pnote))` |  | pending |
| `note.parse_note.return.004` | 617 | `return;` |  | pending |
| `note.parse_note.if.007` | 620 | `if ( is_number( argument ) )` |  | pending |
| `note.parse_note.return.005` | 628 | `return;` |  | pending |
| `note.parse_note.for.002` | 632 | `for ( pnote = *list; pnote != NULL; pnote = pnote->next )` |  | pending |
| `note.parse_note.if.008` | 634 | `if ( is_note_to( ch, pnote ) && ( vnum++ == anum \|\| fAll ) )` |  | pending |
| `note.parse_note.and.001` | 634 | `&& ( vnum++ == anum \|\| fAll ) )` |  | pending |
| `note.parse_note.or.003` | 634 | `\|\| fAll ) )` |  | pending |
| `note.parse_note.return.006` | 646 | `return;` |  | pending |
| `note.parse_note.return.007` | 652 | `return;` |  | pending |
| `note.parse_note.if.009` | 655 | `if ( !str_prefix( arg, "list" ) )` |  | pending |
| `note.parse_note.for.003` | 658 | `for ( pnote = *list; pnote != NULL; pnote = pnote->next )` |  | pending |
| `note.parse_note.if.010` | 660 | `if ( is_note_to( ch, pnote ) )` |  | pending |
| `note.parse_note.ternary.001` | 663 | `? " " : "N",` |  | pending |
| `note.parse_note.if.011` | 669 | `if (!vnum)` |  | pending |
| `note.parse_note.switch.002` | 671 | `switch(type)` |  | pending |
| `note.parse_note.case.006` | 673 | `case NOTE_NOTE:` |  | pending |
| `note.parse_note.break.006` | 675 | `break;` |  | pending |
| `note.parse_note.case.007` | 676 | `case NOTE_IDEA:` |  | pending |
| `note.parse_note.break.007` | 678 | `break;` |  | pending |
| `note.parse_note.case.008` | 679 | `case NOTE_PENALTY:` |  | pending |
| `note.parse_note.break.008` | 681 | `break;` |  | pending |
| `note.parse_note.case.009` | 682 | `case NOTE_NEWS:` |  | pending |
| `note.parse_note.break.009` | 684 | `break;` |  | pending |
| `note.parse_note.case.010` | 685 | `case NOTE_CHANGES:` |  | pending |
| `note.parse_note.break.010` | 687 | `break;` |  | pending |
| `note.parse_note.return.008` | 690 | `return;` |  | pending |
| `note.parse_note.if.012` | 693 | `if ( !str_prefix( arg, "remove" ) )` |  | pending |
| `note.parse_note.if.013` | 695 | `if ( !is_number( argument ) )` |  | pending |
| `note.parse_note.return.009` | 698 | `return;` |  | pending |
| `note.parse_note.for.004` | 703 | `for ( pnote = *list; pnote != NULL; pnote = pnote->next )` |  | pending |
| `note.parse_note.if.014` | 705 | `if ( is_note_to( ch, pnote ) && vnum++ == anum )` |  | pending |
| `note.parse_note.and.002` | 705 | `&& vnum++ == anum )` |  | pending |
| `note.parse_note.return.010` | 709 | `return;` |  | pending |
| `note.parse_note.return.011` | 715 | `return;` |  | pending |
| `note.parse_note.if.015` | 718 | `if ( !str_prefix( arg, "delete" ) && get_trust(ch) >= MAX_LEVEL - 1)` |  | pending |
| `note.parse_note.and.003` | 718 | `&& get_trust(ch) >= MAX_LEVEL - 1)` |  | pending |
| `note.parse_note.if.016` | 720 | `if ( !is_number( argument ) )` |  | pending |
| `note.parse_note.return.012` | 723 | `return;` |  | pending |
| `note.parse_note.for.005` | 728 | `for ( pnote = *list; pnote != NULL; pnote = pnote->next )` |  | pending |
| `note.parse_note.if.017` | 730 | `if ( is_note_to( ch, pnote ) && vnum++ == anum )` |  | pending |
| `note.parse_note.and.004` | 730 | `&& vnum++ == anum )` |  | pending |
| `note.parse_note.return.013` | 734 | `return;` |  | pending |
| `note.parse_note.return.014` | 740 | `return;` |  | pending |
| `note.parse_note.if.018` | 743 | `if (!str_prefix(arg,"catchup"))` |  | pending |
| `note.parse_note.switch.003` | 745 | `switch(type)` |  | pending |
| `note.parse_note.case.011` | 747 | `case NOTE_NOTE:` |  | pending |
| `note.parse_note.break.011` | 749 | `break;` |  | pending |
| `note.parse_note.case.012` | 750 | `case NOTE_IDEA:` |  | pending |
| `note.parse_note.break.012` | 752 | `break;` |  | pending |
| `note.parse_note.case.013` | 753 | `case NOTE_PENALTY:` |  | pending |
| `note.parse_note.break.013` | 755 | `break;` |  | pending |
| `note.parse_note.case.014` | 756 | `case NOTE_NEWS:` |  | pending |
| `note.parse_note.break.014` | 758 | `break;` |  | pending |
| `note.parse_note.case.015` | 759 | `case NOTE_CHANGES:` |  | pending |
| `note.parse_note.break.015` | 761 | `break;` |  | pending |
| `note.parse_note.return.015` | 763 | `return;` |  | pending |
| `note.parse_note.if.019` | 767 | `if ((type == NOTE_NEWS && !IS_TRUSTED(ch,ANGEL))     \|\|  (type == NOTE_CHANGES && !IS_TRUSTED(ch,CREATOR)))` |  | pending |
| `note.parse_note.and.005` | 767 | `&& !IS_TRUSTED(ch,ANGEL))` |  | pending |
| `note.parse_note.or.004` | 768 | `\|\|  (type == NOTE_CHANGES && !IS_TRUSTED(ch,CREATOR)))` |  | pending |
| `note.parse_note.and.006` | 768 | `&& !IS_TRUSTED(ch,CREATOR)))` |  | pending |
| `note.parse_note.return.016` | 772 | `return;` |  | pending |
| `note.parse_note.if.020` | 775 | `if ( !str_cmp( arg, "+" ) )` |  | pending |
| `note.parse_note.if.021` | 778 | `if (ch->pnote->type != type)` |  | pending |
| `note.parse_note.return.017` | 782 | `return;` |  | pending |
| `note.parse_note.if.022` | 785 | `if (strlen(ch->pnote->text)+strlen(argument) >= 4096)` |  | pending |
| `note.parse_note.return.018` | 788 | `return;` |  | pending |
| `note.parse_note.return.019` | 800 | `return;` |  | pending |
| `note.parse_note.if.023` | 803 | `if (!str_cmp(arg,"-"))` |  | pending |
| `note.parse_note.if.024` | 809 | `if (ch->pnote->type != type)` |  | pending |
| `note.parse_note.return.020` | 813 | `return;` |  | pending |
| `note.parse_note.if.025` | 816 | `if (ch->pnote->text == NULL \|\| ch->pnote->text[0] == '\0')` |  | pending |
| `note.parse_note.or.005` | 816 | `\|\| ch->pnote->text[0] == '\0')` |  | pending |
| `note.parse_note.return.021` | 819 | `return;` |  | pending |
| `note.parse_note.for.006` | 824 | `for (len = strlen(buf); len > 0; len--)` |  | pending |
| `note.parse_note.if.026` | 826 | `if (buf[len] == '\r')` |  | pending |
| `note.parse_note.if.027` | 828 | `if (!found)` |  | pending |
| `note.parse_note.if.028` | 830 | `if (len > 0)` |  | pending |
| `note.parse_note.return.022` | 839 | `return;` |  | pending |
| `note.parse_note.return.023` | 846 | `return;` |  | pending |
| `note.parse_note.if.029` | 849 | `if ( !str_prefix( arg, "subject" ) )` |  | pending |
| `note.parse_note.if.030` | 852 | `if (ch->pnote->type != type)` |  | pending |
| `note.parse_note.return.024` | 856 | `return;` |  | pending |
| `note.parse_note.return.025` | 862 | `return;` |  | pending |
| `note.parse_note.if.031` | 865 | `if ( !str_prefix( arg, "to" ) )` |  | pending |
| `note.parse_note.if.032` | 868 | `if (ch->pnote->type != type)` |  | pending |
| `note.parse_note.return.026` | 872 | `return;` |  | pending |
| `note.parse_note.return.027` | 877 | `return;` |  | pending |
| `note.parse_note.if.033` | 880 | `if ( !str_prefix( arg, "clear" ) )` |  | pending |
| `note.parse_note.if.034` | 882 | `if ( ch->pnote != NULL )` |  | pending |
| `note.parse_note.return.028` | 889 | `return;` |  | pending |
| `note.parse_note.if.035` | 892 | `if ( !str_prefix( arg, "show" ) )` |  | pending |
| `note.parse_note.if.036` | 894 | `if ( ch->pnote == NULL )` |  | pending |
| `note.parse_note.return.029` | 897 | `return;` |  | pending |
| `note.parse_note.if.037` | 900 | `if (ch->pnote->type != type)` |  | pending |
| `note.parse_note.return.030` | 903 | `return;` |  | pending |
| `note.parse_note.return.031` | 913 | `return;` |  | pending |
| `note.parse_note.if.038` | 916 | `if ( !str_prefix( arg, "post" ) \|\| !str_prefix(arg, "send"))` |  | pending |
| `note.parse_note.or.006` | 916 | `\|\| !str_prefix(arg, "send"))` |  | pending |
| `note.parse_note.if.039` | 920 | `if ( ch->pnote == NULL )` |  | pending |
| `note.parse_note.return.032` | 923 | `return;` |  | pending |
| `note.parse_note.if.040` | 926 | `if (ch->pnote->type != type)` |  | pending |
| `note.parse_note.return.033` | 929 | `return;` |  | pending |
| `note.parse_note.if.041` | 932 | `if (!str_cmp(ch->pnote->to_list,""))` |  | pending |
| `note.parse_note.return.034` | 937 | `return;` |  | pending |
| `note.parse_note.if.042` | 940 | `if (!str_cmp(ch->pnote->subject,""))` |  | pending |
| `note.parse_note.return.035` | 943 | `return;` |  | pending |
| `note.parse_note.return.036` | 954 | `return;` |  | pending |
| `note.parse_note.return.037` | 958 | `return;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#include <sys/time.h>` — pending configuration/reachability review.
- Line 33: `#endif` — pending configuration/reachability review.
- Line 34: `#include <ctype.h>` — pending configuration/reachability review.
- Line 35: `#include <stdio.h>` — pending configuration/reachability review.
- Line 36: `#include <string.h>` — pending configuration/reachability review.
- Line 37: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 38: `#include <time.h>` — pending configuration/reachability review.
- Line 39: `#include "merc.h"` — pending configuration/reachability review.
- Line 40: `#include "recycle.h"` — pending configuration/reachability review.
- Line 41: `#include "tables.h"` — pending configuration/reachability review.
- Line 44: `#if !defined(macintosh)` — pending configuration/reachability review.
- Line 46: `#endif` — pending configuration/reachability review.

## Static tables


## Commented code candidates


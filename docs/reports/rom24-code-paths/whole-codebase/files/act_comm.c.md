# src/act_comm.c

Role: translation_unit. Disposition: **pending**. SHA-256: `ddb62f65bcb6001c5d03bd11bab3dafd2274b03d504b740a4b9be95062a10449`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## do_delet

[Source line 46](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:46); ends at line 49. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:161` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:109` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_delet.entry` | 46 | `Straight-line entry` |  | pending |

## do_delete

[Source line 51](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:51); ends at line 89. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:162` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:110` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `send_to_char`, `sprintf`, `capitalize`, `wiznet`, `stop_fighting`, `do_function`, `unlink`, `get_trust`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_delete.if.001` | 55 | `if (IS_NPC(ch))` |  | pending |
| `act_comm.do_delete.return.001` | 56 | `return;` |  | pending |
| `act_comm.do_delete.if.002` | 58 | `if (ch->pcdata->confirm_delete)` |  | pending |
| `act_comm.do_delete.if.003` | 60 | `if (argument[0] != '\0')` |  | pending |
| `act_comm.do_delete.return.002` | 64 | `return;` |  | pending |
| `act_comm.do_delete.return.003` | 73 | `return;` |  | pending |
| `act_comm.do_delete.if.004` | 77 | `if (argument[0] != '\0')` |  | pending |
| `act_comm.do_delete.return.004` | 80 | `return;` |  | pending |

## do_channels

[Source line 94](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:94); ends at line 200. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:84` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:98` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `IS_SET`, `IS_IMMORTAL`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_channels.if.001` | 103 | `if (!IS_SET(ch->comm,COMM_NOGOSSIP))` |  | pending |
| `act_comm.do_channels.if.002` | 109 | `if (!IS_SET(ch->comm,COMM_NOAUCTION))` |  | pending |
| `act_comm.do_channels.if.003` | 115 | `if (!IS_SET(ch->comm,COMM_NOMUSIC))` |  | pending |
| `act_comm.do_channels.if.004` | 121 | `if (!IS_SET(ch->comm,COMM_NOQUESTION))` |  | pending |
| `act_comm.do_channels.if.005` | 127 | `if (!IS_SET(ch->comm,COMM_NOQUOTE))` |  | pending |
| `act_comm.do_channels.if.006` | 133 | `if (!IS_SET(ch->comm,COMM_NOGRATS))` |  | pending |
| `act_comm.do_channels.if.007` | 138 | `if (IS_IMMORTAL(ch))` |  | pending |
| `act_comm.do_channels.if.008` | 141 | `if(!IS_SET(ch->comm,COMM_NOWIZ))` |  | pending |
| `act_comm.do_channels.if.009` | 148 | `if (!IS_SET(ch->comm,COMM_SHOUTSOFF))` |  | pending |
| `act_comm.do_channels.if.010` | 154 | `if (!IS_SET(ch->comm,COMM_DEAF))` |  | pending |
| `act_comm.do_channels.if.011` | 160 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |
| `act_comm.do_channels.if.012` | 165 | `if (IS_SET(ch->comm,COMM_AFK))` |  | pending |
| `act_comm.do_channels.if.013` | 168 | `if (IS_SET(ch->comm,COMM_SNOOP_PROOF))` |  | pending |
| `act_comm.do_channels.if.014` | 171 | `if (ch->lines != PAGELEN)` |  | pending |
| `act_comm.do_channels.if.015` | 173 | `if (ch->lines)` |  | pending |
| `act_comm.do_channels.if.016` | 182 | `if (ch->prompt != NULL)` |  | pending |
| `act_comm.do_channels.if.017` | 188 | `if (IS_SET(ch->comm,COMM_NOSHOUT))` |  | pending |
| `act_comm.do_channels.if.018` | 191 | `if (IS_SET(ch->comm,COMM_NOTELL))` |  | pending |
| `act_comm.do_channels.if.019` | 194 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_channels.if.020` | 197 | `if (IS_SET(ch->comm,COMM_NOEMOTE))` |  | pending |

## do_deaf

[Source line 204](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:204); ends at line 217. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:180` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:108` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_deaf.if.001` | 207 | `if (IS_SET(ch->comm,COMM_DEAF))` |  | pending |

## do_quiet

[Source line 221](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:221); ends at line 233. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:194` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:213` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_quiet.if.001` | 223 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |

## do_afk

[Source line 237](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:237); ends at line 249. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:177` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:71` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_afk.if.001` | 239 | `if (IS_SET(ch->comm,COMM_AFK))` |  | pending |

## do_replay

[Source line 251](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:251); ends at line 267. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:196` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:224` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `send_to_char`, `buf_string`, `page_to_char`, `clear_buf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_replay.if.001` | 253 | `if (IS_NPC(ch))` |  | pending |
| `act_comm.do_replay.return.001` | 256 | `return;` |  | pending |
| `act_comm.do_replay.if.002` | 259 | `if (buf_string(ch->pcdata->buffer)[0] == '\0')` |  | pending |
| `act_comm.do_replay.return.002` | 262 | `return;` |  | pending |

## do_auction

[Source line 270](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:270); ends at line 322. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:82` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:78` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_auction.if.001` | 275 | `if (argument[0] == '\0' )` |  | pending |
| `act_comm.do_auction.if.002` | 277 | `if (IS_SET(ch->comm,COMM_NOAUCTION))` |  | pending |
| `act_comm.do_auction.if.003` | 290 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |
| `act_comm.do_auction.return.001` | 293 | `return;` |  | pending |
| `act_comm.do_auction.if.004` | 296 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_auction.return.002` | 299 | `return;` |  | pending |
| `act_comm.do_auction.for.001` | 307 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_auction.ternary.001` | 311 | `? d->original : d->character;` |  | pending |
| `act_comm.do_auction.if.005` | 313 | `if ( d->connected == CON_PLAYING && 	     d->character != ch && 	     !IS_SET(victim->comm,COMM_NOAUCTION) && 	     !IS_SET(victim->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_auction.and.001` | 313 | `&&` |  | pending |
| `act_comm.do_auction.and.002` | 314 | `&&` |  | pending |
| `act_comm.do_auction.and.003` | 315 | `&&` |  | pending |

## do_gossip

[Source line 325](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:325); ends at line 378. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:183` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:184` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:138` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_gossip.if.001` | 330 | `if (argument[0] == '\0' )` |  | pending |
| `act_comm.do_gossip.if.002` | 332 | `if (IS_SET(ch->comm,COMM_NOGOSSIP))` |  | pending |
| `act_comm.do_gossip.if.003` | 345 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |
| `act_comm.do_gossip.return.001` | 348 | `return;` |  | pending |
| `act_comm.do_gossip.if.004` | 351 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_gossip.return.002` | 354 | `return;` |  | pending |
| `act_comm.do_gossip.for.001` | 362 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_gossip.ternary.001` | 366 | `? d->original : d->character;` |  | pending |
| `act_comm.do_gossip.if.005` | 368 | `if ( d->connected == CON_PLAYING &&              d->character != ch &&              !IS_SET(victim->comm,COMM_NOGOSSIP) &&              !IS_SET(victim->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_gossip.and.001` | 368 | `&&` |  | pending |
| `act_comm.do_gossip.and.002` | 369 | `&&` |  | pending |
| `act_comm.do_gossip.and.003` | 370 | `&&` |  | pending |

## do_grats

[Source line 380](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:380); ends at line 433. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:186` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:140` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_grats.if.001` | 385 | `if (argument[0] == '\0' )` |  | pending |
| `act_comm.do_grats.if.002` | 387 | `if (IS_SET(ch->comm,COMM_NOGRATS))` |  | pending |
| `act_comm.do_grats.if.003` | 400 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |
| `act_comm.do_grats.return.001` | 403 | `return;` |  | pending |
| `act_comm.do_grats.if.004` | 406 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_grats.return.002` | 409 | `return;` |  | pending |
| `act_comm.do_grats.for.001` | 417 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_grats.ternary.001` | 421 | `? d->original : d->character;` |  | pending |
| `act_comm.do_grats.if.005` | 423 | `if ( d->connected == CON_PLAYING &&              d->character != ch &&              !IS_SET(victim->comm,COMM_NOGRATS) &&              !IS_SET(victim->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_grats.and.001` | 423 | `&&` |  | pending |
| `act_comm.do_grats.and.002` | 424 | `&&` |  | pending |
| `act_comm.do_grats.and.003` | 425 | `&&` |  | pending |

## do_quote

[Source line 435](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:435); ends at line 488. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:193` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:215` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_quote.if.001` | 440 | `if (argument[0] == '\0' )` |  | pending |
| `act_comm.do_quote.if.002` | 442 | `if (IS_SET(ch->comm,COMM_NOQUOTE))` |  | pending |
| `act_comm.do_quote.if.003` | 455 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |
| `act_comm.do_quote.return.001` | 458 | `return;` |  | pending |
| `act_comm.do_quote.if.004` | 461 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_quote.return.002` | 464 | `return;` |  | pending |
| `act_comm.do_quote.for.001` | 472 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_quote.ternary.001` | 476 | `? d->original : d->character;` |  | pending |
| `act_comm.do_quote.if.005` | 478 | `if ( d->connected == CON_PLAYING &&              d->character != ch &&              !IS_SET(victim->comm,COMM_NOQUOTE) &&              !IS_SET(victim->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_quote.and.001` | 478 | `&&` |  | pending |
| `act_comm.do_quote.and.002` | 479 | `&&` |  | pending |
| `act_comm.do_quote.and.003` | 480 | `&&` |  | pending |

## do_question

[Source line 491](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:491); ends at line 543. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:192` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:211` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_question.if.001` | 496 | `if (argument[0] == '\0' )` |  | pending |
| `act_comm.do_question.if.002` | 498 | `if (IS_SET(ch->comm,COMM_NOQUESTION))` |  | pending |
| `act_comm.do_question.if.003` | 511 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |
| `act_comm.do_question.return.001` | 514 | `return;` |  | pending |
| `act_comm.do_question.if.004` | 517 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_question.return.002` | 520 | `return;` |  | pending |
| `act_comm.do_question.for.001` | 527 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_question.ternary.001` | 531 | `? d->original : d->character;` |  | pending |
| `act_comm.do_question.if.005` | 533 | `if ( d->connected == CON_PLAYING &&              d->character != ch &&              !IS_SET(victim->comm,COMM_NOQUESTION) &&              !IS_SET(victim->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_question.and.001` | 533 | `&&` |  | pending |
| `act_comm.do_question.and.002` | 534 | `&&` |  | pending |
| `act_comm.do_question.and.003` | 535 | `&&` |  | pending |

## do_answer

[Source line 546](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:546); ends at line 598. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:178` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:75` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_answer.if.001` | 551 | `if (argument[0] == '\0' )` |  | pending |
| `act_comm.do_answer.if.002` | 553 | `if (IS_SET(ch->comm,COMM_NOQUESTION))` |  | pending |
| `act_comm.do_answer.if.003` | 566 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |
| `act_comm.do_answer.return.001` | 569 | `return;` |  | pending |
| `act_comm.do_answer.if.004` | 572 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_answer.return.002` | 575 | `return;` |  | pending |
| `act_comm.do_answer.for.001` | 582 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_answer.ternary.001` | 586 | `? d->original : d->character;` |  | pending |
| `act_comm.do_answer.if.005` | 588 | `if ( d->connected == CON_PLAYING &&              d->character != ch &&              !IS_SET(victim->comm,COMM_NOQUESTION) &&              !IS_SET(victim->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_answer.and.001` | 588 | `&&` |  | pending |
| `act_comm.do_answer.and.002` | 589 | `&&` |  | pending |
| `act_comm.do_answer.and.003` | 590 | `&&` |  | pending |

## do_music

[Source line 601](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:601); ends at line 654. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:95` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:172` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_music.if.001` | 606 | `if (argument[0] == '\0' )` |  | pending |
| `act_comm.do_music.if.002` | 608 | `if (IS_SET(ch->comm,COMM_NOMUSIC))` |  | pending |
| `act_comm.do_music.if.003` | 621 | `if (IS_SET(ch->comm,COMM_QUIET))` |  | pending |
| `act_comm.do_music.return.001` | 624 | `return;` |  | pending |
| `act_comm.do_music.if.004` | 627 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_music.return.002` | 630 | `return;` |  | pending |
| `act_comm.do_music.for.001` | 638 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_music.ternary.001` | 642 | `? d->original : d->character;` |  | pending |
| `act_comm.do_music.if.005` | 644 | `if ( d->connected == CON_PLAYING &&              d->character != ch &&              !IS_SET(victim->comm,COMM_NOMUSIC) &&              !IS_SET(victim->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_music.and.001` | 644 | `&&` |  | pending |
| `act_comm.do_music.and.002` | 645 | `&&` |  | pending |
| `act_comm.do_music.and.003` | 646 | `&&` |  | pending |

## do_clantalk

[Source line 657](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:657); ends at line 706. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:94` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:152` (declaration_or_dispatch_reference).

Dependencies: `is_clan`, `send_to_char`, `IS_SET`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `is_same_clan`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_clantalk.if.001` | 662 | `if (!is_clan(ch) \|\| clan_table[ch->clan].independent)` |  | pending |
| `act_comm.do_clantalk.or.001` | 662 | `\|\| clan_table[ch->clan].independent)` |  | pending |
| `act_comm.do_clantalk.return.001` | 665 | `return;` |  | pending |
| `act_comm.do_clantalk.if.002` | 667 | `if ( argument[0] == '\0' )` |  | pending |
| `act_comm.do_clantalk.if.003` | 669 | `if (IS_SET(ch->comm,COMM_NOCLAN))` |  | pending |
| `act_comm.do_clantalk.return.002` | 679 | `return;` |  | pending |
| `act_comm.do_clantalk.if.004` | 682 | `if (IS_SET(ch->comm,COMM_NOCHANNELS))` |  | pending |
| `act_comm.do_clantalk.return.003` | 685 | `return;` |  | pending |
| `act_comm.do_clantalk.for.001` | 693 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_clantalk.if.005` | 695 | `if ( d->connected == CON_PLAYING &&              d->character != ch && 	     is_same_clan(ch,d->character) &&              !IS_SET(d->character->comm,COMM_NOCLAN) && 	     !IS_SET(d->character->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_clantalk.and.001` | 695 | `&&` |  | pending |
| `act_comm.do_clantalk.and.002` | 696 | `&&` |  | pending |
| `act_comm.do_clantalk.and.003` | 697 | `&&` |  | pending |
| `act_comm.do_clantalk.and.004` | 698 | `&&` |  | pending |
| `act_comm.do_clantalk.return.004` | 705 | `return;` |  | pending |

## do_immtalk

[Source line 708](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:708); ends at line 743. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:347` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:349` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:150` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `sprintf`, `act_new`, `IS_IMMORTAL`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_immtalk.if.001` | 713 | `if ( argument[0] == '\0' )` |  | pending |
| `act_comm.do_immtalk.if.002` | 715 | `if (IS_SET(ch->comm,COMM_NOWIZ))` |  | pending |
| `act_comm.do_immtalk.return.001` | 725 | `return;` |  | pending |
| `act_comm.do_immtalk.for.001` | 732 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_immtalk.if.003` | 734 | `if ( d->connected == CON_PLAYING &&  	     IS_IMMORTAL(d->character) &&               !IS_SET(d->character->comm,COMM_NOWIZ) )` |  | pending |
| `act_comm.do_immtalk.and.001` | 734 | `&&` |  | pending |
| `act_comm.do_immtalk.and.002` | 735 | `&&` |  | pending |
| `act_comm.do_immtalk.return.002` | 742 | `return;` |  | pending |

## do_say

[Source line 747](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:747); ends at line 758. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- find_keeper: `src/act_obj.c:2356` (function_symbol_reference_candidate).
- find_keeper: `src/act_obj.c:2362` (function_symbol_reference_candidate).
- find_keeper: `src/act_obj.c:2371` (function_symbol_reference_candidate).
- do_gain: `src/skills.c:71` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:197` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:198` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:236` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_say.if.001` | 749 | `if ( argument[0] == '\0' )` |  | pending |
| `act_comm.do_say.return.001` | 752 | `return;` |  | pending |
| `act_comm.do_say.return.002` | 757 | `return;` |  | pending |

## do_shout

[Source line 762](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:762); ends at line 808. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:199` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:242` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `WAIT_STATE`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_shout.if.001` | 766 | `if (argument[0] == '\0' )` |  | pending |
| `act_comm.do_shout.if.002` | 768 | `if (IS_SET(ch->comm,COMM_SHOUTSOFF))` |  | pending |
| `act_comm.do_shout.return.001` | 778 | `return;` |  | pending |
| `act_comm.do_shout.if.003` | 781 | `if ( IS_SET(ch->comm, COMM_NOSHOUT) )` |  | pending |
| `act_comm.do_shout.return.002` | 784 | `return;` |  | pending |
| `act_comm.do_shout.for.001` | 792 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_shout.ternary.001` | 796 | `? d->original : d->character;` |  | pending |
| `act_comm.do_shout.if.004` | 798 | `if ( d->connected == CON_PLAYING && 	     d->character != ch && 	     !IS_SET(victim->comm, COMM_SHOUTSOFF) && 	     !IS_SET(victim->comm, COMM_QUIET) )` |  | pending |
| `act_comm.do_shout.and.001` | 798 | `&&` |  | pending |
| `act_comm.do_shout.and.002` | 799 | `&&` |  | pending |
| `act_comm.do_shout.and.003` | 800 | `&&` |  | pending |
| `act_comm.do_shout.return.003` | 807 | `return;` |  | pending |

## do_tell

[Source line 812](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:812); ends at line 898. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:102` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:267` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `one_argument`, `get_char_world`, `IS_NPC`, `act`, `sprintf`, `PERS`, `UPPER`, `add_buf`, `IS_IMMORTAL`, `IS_AWAKE`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_tell.if.001` | 817 | `if ( IS_SET(ch->comm, COMM_NOTELL) \|\| IS_SET(ch->comm,COMM_DEAF))` |  | pending |
| `act_comm.do_tell.or.001` | 817 | `\|\| IS_SET(ch->comm,COMM_DEAF))` |  | pending |
| `act_comm.do_tell.return.001` | 820 | `return;` |  | pending |
| `act_comm.do_tell.if.002` | 823 | `if ( IS_SET(ch->comm, COMM_QUIET) )` |  | pending |
| `act_comm.do_tell.return.002` | 826 | `return;` |  | pending |
| `act_comm.do_tell.if.003` | 829 | `if (IS_SET(ch->comm,COMM_DEAF))` |  | pending |
| `act_comm.do_tell.return.003` | 832 | `return;` |  | pending |
| `act_comm.do_tell.if.004` | 837 | `if ( arg[0] == '\0' \|\| argument[0] == '\0' )` |  | pending |
| `act_comm.do_tell.or.002` | 837 | `\|\| argument[0] == '\0' )` |  | pending |
| `act_comm.do_tell.return.004` | 840 | `return;` |  | pending |
| `act_comm.do_tell.if.005` | 847 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL     \|\| ( IS_NPC(victim) && victim->in_room != ch->in_room ) )` |  | pending |
| `act_comm.do_tell.or.003` | 848 | `\|\| ( IS_NPC(victim) && victim->in_room != ch->in_room ) )` |  | pending |
| `act_comm.do_tell.and.001` | 848 | `&& victim->in_room != ch->in_room ) )` |  | pending |
| `act_comm.do_tell.return.005` | 851 | `return;` |  | pending |
| `act_comm.do_tell.if.006` | 854 | `if ( victim->desc == NULL && !IS_NPC(victim))` |  | pending |
| `act_comm.do_tell.and.002` | 854 | `&& !IS_NPC(victim))` |  | pending |
| `act_comm.do_tell.return.006` | 861 | `return;` |  | pending |
| `act_comm.do_tell.if.007` | 864 | `if ( !(IS_IMMORTAL(ch) && ch->level > LEVEL_IMMORTAL) && !IS_AWAKE(victim) )` |  | pending |
| `act_comm.do_tell.and.003` | 864 | `&& ch->level > LEVEL_IMMORTAL) && !IS_AWAKE(victim) )` |  | pending |
| `act_comm.do_tell.and.004` | 864 | `&& !IS_AWAKE(victim) )` |  | pending |
| `act_comm.do_tell.return.007` | 867 | `return;` |  | pending |
| `act_comm.do_tell.if.008` | 870 | `if ((IS_SET(victim->comm,COMM_QUIET) \|\| IS_SET(victim->comm,COMM_DEAF))     && !IS_IMMORTAL(ch))` |  | pending |
| `act_comm.do_tell.or.004` | 870 | `\|\| IS_SET(victim->comm,COMM_DEAF))` |  | pending |
| `act_comm.do_tell.and.005` | 871 | `&& !IS_IMMORTAL(ch))` |  | pending |
| `act_comm.do_tell.return.008` | 874 | `return;` |  | pending |
| `act_comm.do_tell.if.009` | 877 | `if (IS_SET(victim->comm,COMM_AFK))` |  | pending |
| `act_comm.do_tell.if.010` | 879 | `if (IS_NPC(victim))` |  | pending |
| `act_comm.do_tell.return.009` | 882 | `return;` |  | pending |
| `act_comm.do_tell.return.010` | 890 | `return;` |  | pending |
| `act_comm.do_tell.return.011` | 897 | `return;` |  | pending |

## do_reply

[Source line 902](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:902); ends at line 970. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:195` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:225` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `IS_NPC`, `act`, `sprintf`, `PERS`, `UPPER`, `add_buf`, `IS_IMMORTAL`, `IS_AWAKE`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_reply.if.001` | 907 | `if ( IS_SET(ch->comm, COMM_NOTELL) )` |  | pending |
| `act_comm.do_reply.return.001` | 910 | `return;` |  | pending |
| `act_comm.do_reply.if.002` | 913 | `if ( ( victim = ch->reply ) == NULL )` |  | pending |
| `act_comm.do_reply.return.002` | 916 | `return;` |  | pending |
| `act_comm.do_reply.if.003` | 919 | `if ( victim->desc == NULL && !IS_NPC(victim))` |  | pending |
| `act_comm.do_reply.and.001` | 919 | `&& !IS_NPC(victim))` |  | pending |
| `act_comm.do_reply.return.003` | 926 | `return;` |  | pending |
| `act_comm.do_reply.if.004` | 929 | `if ( !IS_IMMORTAL(ch) && !IS_AWAKE(victim) )` |  | pending |
| `act_comm.do_reply.and.002` | 929 | `&& !IS_AWAKE(victim) )` |  | pending |
| `act_comm.do_reply.return.004` | 932 | `return;` |  | pending |
| `act_comm.do_reply.if.005` | 935 | `if ((IS_SET(victim->comm,COMM_QUIET) \|\| IS_SET(victim->comm,COMM_DEAF))     &&  !IS_IMMORTAL(ch) && !IS_IMMORTAL(victim))` |  | pending |
| `act_comm.do_reply.or.001` | 935 | `\|\| IS_SET(victim->comm,COMM_DEAF))` |  | pending |
| `act_comm.do_reply.and.003` | 936 | `&&  !IS_IMMORTAL(ch) && !IS_IMMORTAL(victim))` |  | pending |
| `act_comm.do_reply.and.004` | 936 | `&& !IS_IMMORTAL(victim))` |  | pending |
| `act_comm.do_reply.return.005` | 939 | `return;` |  | pending |
| `act_comm.do_reply.if.006` | 942 | `if (!IS_IMMORTAL(victim) && !IS_AWAKE(ch))` |  | pending |
| `act_comm.do_reply.and.005` | 942 | `&& !IS_AWAKE(ch))` |  | pending |
| `act_comm.do_reply.return.006` | 945 | `return;` |  | pending |
| `act_comm.do_reply.if.007` | 948 | `if (IS_SET(victim->comm,COMM_AFK))` |  | pending |
| `act_comm.do_reply.if.008` | 950 | `if (IS_NPC(victim))` |  | pending |
| `act_comm.do_reply.return.007` | 954 | `return;` |  | pending |
| `act_comm.do_reply.return.008` | 962 | `return;` |  | pending |
| `act_comm.do_reply.return.009` | 969 | `return;` |  | pending |

## do_yell

[Source line 974](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:974); ends at line 1005. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_steal: `src/act_obj.c:2218` (function_symbol_reference_candidate).
- do_murder: `src/fight.c:2719` (function_symbol_reference_candidate).
- spec_executioner: `src/special.c:751` (function_symbol_reference_candidate).
- spec_guard: `src/special.c:832` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:201` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:296` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_yell.if.001` | 978 | `if ( IS_SET(ch->comm, COMM_NOSHOUT) )` |  | pending |
| `act_comm.do_yell.return.001` | 981 | `return;` |  | pending |
| `act_comm.do_yell.if.002` | 984 | `if ( argument[0] == '\0' )` |  | pending |
| `act_comm.do_yell.return.002` | 987 | `return;` |  | pending |
| `act_comm.do_yell.for.001` | 992 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_comm.do_yell.if.003` | 994 | `if ( d->connected == CON_PLAYING 	&&   d->character != ch 	&&   d->character->in_room != NULL 	&&   d->character->in_room->area == ch->in_room->area          &&   !IS_SET(d->character->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_yell.and.001` | 995 | `&&   d->character != ch` |  | pending |
| `act_comm.do_yell.and.002` | 996 | `&&   d->character->in_room != NULL` |  | pending |
| `act_comm.do_yell.and.003` | 997 | `&&   d->character->in_room->area == ch->in_room->area` |  | pending |
| `act_comm.do_yell.and.004` | 998 | `&&   !IS_SET(d->character->comm,COMM_QUIET) )` |  | pending |
| `act_comm.do_yell.return.003` | 1004 | `return;` |  | pending |

## do_emote

[Source line 1008](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1008); ends at line 1025. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- check_assist: `src/fight.c:114` (function_symbol_reference_candidate).
- check_assist: `src/fight.c:174` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:181` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:185` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:123` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_emote.if.001` | 1010 | `if ( !IS_NPC(ch) && IS_SET(ch->comm, COMM_NOEMOTE) )` |  | pending |
| `act_comm.do_emote.and.001` | 1010 | `&& IS_SET(ch->comm, COMM_NOEMOTE) )` |  | pending |
| `act_comm.do_emote.return.001` | 1013 | `return;` |  | pending |
| `act_comm.do_emote.if.002` | 1016 | `if ( argument[0] == '\0' )` |  | pending |
| `act_comm.do_emote.return.002` | 1019 | `return;` |  | pending |
| `act_comm.do_emote.return.003` | 1024 | `return;` |  | pending |

## do_pmote

[Source line 1028](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1028); ends at line 1110. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:182` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:200` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `act`, `strstr`, `strcpy`, `strlen`, `strcat`, `strncat`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_pmote.if.001` | 1035 | `if ( !IS_NPC(ch) && IS_SET(ch->comm, COMM_NOEMOTE) )` |  | pending |
| `act_comm.do_pmote.and.001` | 1035 | `&& IS_SET(ch->comm, COMM_NOEMOTE) )` |  | pending |
| `act_comm.do_pmote.return.001` | 1038 | `return;` |  | pending |
| `act_comm.do_pmote.if.002` | 1041 | `if ( argument[0] == '\0' )` |  | pending |
| `act_comm.do_pmote.return.002` | 1044 | `return;` |  | pending |
| `act_comm.do_pmote.for.001` | 1049 | `for (vch = ch->in_room->people; vch != NULL; vch = vch->next_in_room)` |  | pending |
| `act_comm.do_pmote.if.003` | 1051 | `if (vch->desc == NULL \|\| vch == ch)` |  | pending |
| `act_comm.do_pmote.or.001` | 1051 | `\|\| vch == ch)` |  | pending |
| `act_comm.do_pmote.continue.001` | 1052 | `continue;` |  | pending |
| `act_comm.do_pmote.if.004` | 1054 | `if ((letter = strstr(argument,vch->name)) == NULL)` |  | pending |
| `act_comm.do_pmote.continue.002` | 1057 | `continue;` |  | pending |
| `act_comm.do_pmote.for.002` | 1065 | `for (; *letter != '\0'; letter++)` |  | pending |
| `act_comm.do_pmote.if.005` | 1067 | `if (*letter == '\'' && matches == strlen(vch->name))` |  | pending |
| `act_comm.do_pmote.and.002` | 1067 | `&& matches == strlen(vch->name))` |  | pending |
| `act_comm.do_pmote.continue.003` | 1070 | `continue;` |  | pending |
| `act_comm.do_pmote.if.006` | 1073 | `if (*letter == 's' && matches == strlen(vch->name))` |  | pending |
| `act_comm.do_pmote.and.003` | 1073 | `&& matches == strlen(vch->name))` |  | pending |
| `act_comm.do_pmote.continue.004` | 1076 | `continue;` |  | pending |
| `act_comm.do_pmote.if.007` | 1079 | `if (matches == strlen(vch->name))` |  | pending |
| `act_comm.do_pmote.if.008` | 1084 | `if (*letter == *name)` |  | pending |
| `act_comm.do_pmote.if.009` | 1088 | `if (matches == strlen(vch->name))` |  | pending |
| `act_comm.do_pmote.continue.005` | 1093 | `continue;` |  | pending |
| `act_comm.do_pmote.continue.006` | 1096 | `continue;` |  | pending |
| `act_comm.do_pmote.return.003` | 1109 | `return;` |  | pending |

## do_pose

[Source line 1347](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1347); ends at line 1362. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:191` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:201` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `UMIN`, `number_range`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_pose.if.001` | 1352 | `if ( IS_NPC(ch) )` |  | pending |
| `act_comm.do_pose.return.001` | 1353 | `return;` |  | pending |
| `act_comm.do_pose.return.002` | 1361 | `return;` |  | pending |

## do_bug

[Source line 1366](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1366); ends at line 1371. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:112` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:94` (declaration_or_dispatch_reference).

Dependencies: `append_file`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_bug.return.001` | 1370 | `return;` |  | pending |

## do_typo

[Source line 1373](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1373); ends at line 1378. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:137` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:274` (declaration_or_dispatch_reference).

Dependencies: `append_file`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_typo.return.001` | 1377 | `return;` |  | pending |

## do_rent

[Source line 1380](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1380); ends at line 1384. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:267` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:223` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_rent.return.001` | 1383 | `return;` |  | pending |

## do_qui

[Source line 1387](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1387); ends at line 1391. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:263` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:212` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_qui.return.001` | 1390 | `return;` |  | pending |

## do_quit

[Source line 1395](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1395); ends at line 1446. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_delete: `src/act_comm.c:71` (function_symbol_reference_candidate).
- do_deny: `src/act_wiz.c:535` (function_symbol_reference_candidate).
- char_update: `src/update.c:835` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:264` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:214` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `send_to_char`, `act`, `sprintf`, `log_string`, `wiznet`, `get_trust`, `save_char_obj`, `extract_char`, `close_socket`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_quit.if.001` | 1400 | `if ( IS_NPC(ch) )` |  | pending |
| `act_comm.do_quit.return.001` | 1401 | `return;` |  | pending |
| `act_comm.do_quit.if.002` | 1403 | `if ( ch->position == POS_FIGHTING )` |  | pending |
| `act_comm.do_quit.return.002` | 1406 | `return;` |  | pending |
| `act_comm.do_quit.if.003` | 1409 | `if ( ch->position  < POS_STUNNED  )` |  | pending |
| `act_comm.do_quit.return.003` | 1412 | `return;` |  | pending |
| `act_comm.do_quit.if.004` | 1428 | `if ( d != NULL )` |  | pending |
| `act_comm.do_quit.for.001` | 1432 | `for (d = descriptor_list; d != NULL; d = d_next)` |  | pending |
| `act_comm.do_quit.ternary.001` | 1437 | `? d->original : d->character;` |  | pending |
| `act_comm.do_quit.if.005` | 1438 | `if (tch && tch->id == id)` |  | pending |
| `act_comm.do_quit.and.001` | 1438 | `&& tch->id == id)` |  | pending |
| `act_comm.do_quit.return.004` | 1445 | `return;` |  | pending |

## do_save

[Source line 1450](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1450); ends at line 1459. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:268` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:235` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `save_char_obj`, `send_to_char`, `WAIT_STATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_save.if.001` | 1452 | `if ( IS_NPC(ch) )` |  | pending |
| `act_comm.do_save.return.001` | 1453 | `return;` |  | pending |
| `act_comm.do_save.return.002` | 1458 | `return;` |  | pending |

## do_follow

[Source line 1463](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1463); ends at line 1514. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:255` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:132` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_room`, `IS_AFFECTED`, `act`, `stop_follower`, `IS_NPC`, `IS_SET`, `IS_IMMORTAL`, `REMOVE_BIT`, `add_follower`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_follow.if.001` | 1471 | `if ( arg[0] == '\0' )` |  | pending |
| `act_comm.do_follow.return.001` | 1474 | `return;` |  | pending |
| `act_comm.do_follow.if.002` | 1477 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `act_comm.do_follow.return.002` | 1480 | `return;` |  | pending |
| `act_comm.do_follow.if.003` | 1483 | `if ( IS_AFFECTED(ch, AFF_CHARM) && ch->master != NULL )` |  | pending |
| `act_comm.do_follow.and.001` | 1483 | `&& ch->master != NULL )` |  | pending |
| `act_comm.do_follow.return.003` | 1486 | `return;` |  | pending |
| `act_comm.do_follow.if.004` | 1489 | `if ( victim == ch )` |  | pending |
| `act_comm.do_follow.if.005` | 1491 | `if ( ch->master == NULL )` |  | pending |
| `act_comm.do_follow.return.004` | 1494 | `return;` |  | pending |
| `act_comm.do_follow.return.005` | 1497 | `return;` |  | pending |
| `act_comm.do_follow.if.006` | 1500 | `if (!IS_NPC(victim) && IS_SET(victim->act,PLR_NOFOLLOW) && !IS_IMMORTAL(ch))` |  | pending |
| `act_comm.do_follow.and.002` | 1500 | `&& IS_SET(victim->act,PLR_NOFOLLOW) && !IS_IMMORTAL(ch))` |  | pending |
| `act_comm.do_follow.and.003` | 1500 | `&& !IS_IMMORTAL(ch))` |  | pending |
| `act_comm.do_follow.return.006` | 1504 | `return;` |  | pending |
| `act_comm.do_follow.if.007` | 1509 | `if ( ch->master != NULL )` |  | pending |
| `act_comm.do_follow.return.007` | 1513 | `return;` |  | pending |

## add_follower

[Source line 1517](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1517); ends at line 1534. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_follow: `src/act_comm.c:1512` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2605` (lexical_call_candidate).
- spell_charm_person: `src/magic.c:1343` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2072` (declaration_or_dispatch_reference).

Dependencies: `bug`, `can_see`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.add_follower.if.001` | 1519 | `if ( ch->master != NULL )` |  | pending |
| `act_comm.add_follower.return.001` | 1522 | `return;` |  | pending |
| `act_comm.add_follower.if.002` | 1528 | `if ( can_see( master, ch ) )` |  | pending |
| `act_comm.add_follower.return.002` | 1533 | `return;` |  | pending |

## stop_follower

[Source line 1538](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1538); ends at line 1563. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_follow: `src/act_comm.c:1496` (lexical_call_candidate).
- do_follow: `src/act_comm.c:1510` (lexical_call_candidate).
- nuke_pets: `src/act_comm.c:1572` (lexical_call_candidate).
- die_follower: `src/act_comm.c:1592` (lexical_call_candidate).
- die_follower: `src/act_comm.c:1600` (lexical_call_candidate).
- damage: `src/fight.c:740` (lexical_call_candidate).
- check_killer: `src/fight.c:1232` (lexical_call_candidate).
- spell_charm_person: `src/magic.c:1342` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2073` (declaration_or_dispatch_reference).

Dependencies: `bug`, `IS_AFFECTED`, `REMOVE_BIT`, `affect_strip`, `can_see`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.stop_follower.if.001` | 1540 | `if ( ch->master == NULL )` |  | pending |
| `act_comm.stop_follower.return.001` | 1543 | `return;` |  | pending |
| `act_comm.stop_follower.if.002` | 1546 | `if ( IS_AFFECTED(ch, AFF_CHARM) )` |  | pending |
| `act_comm.stop_follower.if.003` | 1552 | `if ( can_see( ch->master, ch ) && ch->in_room != NULL)` |  | pending |
| `act_comm.stop_follower.and.001` | 1552 | `&& ch->in_room != NULL)` |  | pending |
| `act_comm.stop_follower.if.004` | 1557 | `if (ch->master->pet == ch)` |  | pending |
| `act_comm.stop_follower.return.002` | 1562 | `return;` |  | pending |

## nuke_pets

[Source line 1566](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1566); ends at line 1580. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- extract_char: `src/handler.c:1939` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2074` (declaration_or_dispatch_reference).

Dependencies: `stop_follower`, `act`, `extract_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.nuke_pets.if.001` | 1570 | `if ((pet = ch->pet) != NULL)` |  | pending |
| `act_comm.nuke_pets.if.002` | 1573 | `if (pet->in_room != NULL)` |  | pending |
| `act_comm.nuke_pets.return.001` | 1579 | `return;` |  | pending |

## die_follower

[Source line 1584](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1584); ends at line 1606. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_nofollow: `src/act_info.c:946` (lexical_call_candidate).
- extract_char: `src/handler.c:1944` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2075` (declaration_or_dispatch_reference).

Dependencies: `stop_follower`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.die_follower.if.001` | 1588 | `if ( ch->master != NULL )` |  | pending |
| `act_comm.die_follower.if.002` | 1590 | `if (ch->master->pet == ch)` |  | pending |
| `act_comm.die_follower.for.001` | 1597 | `for ( fch = char_list; fch != NULL; fch = fch->next )` |  | pending |
| `act_comm.die_follower.if.003` | 1599 | `if ( fch->master == ch )` |  | pending |
| `act_comm.die_follower.if.004` | 1601 | `if ( fch->leader == ch )` |  | pending |
| `act_comm.die_follower.return.001` | 1605 | `return;` |  | pending |

## do_order

[Source line 1610](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1610); ends at line 1693. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:96` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:187` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `str_cmp`, `send_to_char`, `IS_AFFECTED`, `get_char_room`, `IS_IMMORTAL`, `sprintf`, `act`, `interpret`, `WAIT_STATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_order.if.001` | 1623 | `if (!str_cmp(arg2,"delete"))` |  | pending |
| `act_comm.do_order.return.001` | 1626 | `return;` |  | pending |
| `act_comm.do_order.if.002` | 1629 | `if ( arg[0] == '\0' \|\| argument[0] == '\0' )` |  | pending |
| `act_comm.do_order.or.001` | 1629 | `\|\| argument[0] == '\0' )` |  | pending |
| `act_comm.do_order.return.002` | 1632 | `return;` |  | pending |
| `act_comm.do_order.if.003` | 1635 | `if ( IS_AFFECTED( ch, AFF_CHARM ) )` |  | pending |
| `act_comm.do_order.return.003` | 1638 | `return;` |  | pending |
| `act_comm.do_order.if.004` | 1641 | `if ( !str_cmp( arg, "all" ) )` |  | pending |
| `act_comm.do_order.if.005` | 1649 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `act_comm.do_order.return.004` | 1652 | `return;` |  | pending |
| `act_comm.do_order.if.006` | 1655 | `if ( victim == ch )` |  | pending |
| `act_comm.do_order.return.005` | 1658 | `return;` |  | pending |
| `act_comm.do_order.if.007` | 1661 | `if (!IS_AFFECTED(victim, AFF_CHARM) \|\| victim->master != ch  	\|\|  (IS_IMMORTAL(victim) && victim->trust >= ch->trust))` |  | pending |
| `act_comm.do_order.or.002` | 1661 | `\|\| victim->master != ch` |  | pending |
| `act_comm.do_order.or.003` | 1662 | `\|\|  (IS_IMMORTAL(victim) && victim->trust >= ch->trust))` |  | pending |
| `act_comm.do_order.and.001` | 1662 | `&& victim->trust >= ch->trust))` |  | pending |
| `act_comm.do_order.return.006` | 1665 | `return;` |  | pending |
| `act_comm.do_order.for.001` | 1670 | `for ( och = ch->in_room->people; och != NULL; och = och_next )` |  | pending |
| `act_comm.do_order.if.008` | 1674 | `if ( IS_AFFECTED(och, AFF_CHARM) 	&&   och->master == ch 	&& ( fAll \|\| och == victim ) )` |  | pending |
| `act_comm.do_order.and.002` | 1675 | `&&   och->master == ch` |  | pending |
| `act_comm.do_order.and.003` | 1676 | `&& ( fAll \|\| och == victim ) )` |  | pending |
| `act_comm.do_order.or.004` | 1676 | `\|\| och == victim ) )` |  | pending |
| `act_comm.do_order.if.009` | 1685 | `if ( found )` |  | pending |
| `act_comm.do_order.return.007` | 1692 | `return;` |  | pending |

## do_group

[Source line 1697](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1697); ends at line 1781. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:88` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:141` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `sprintf`, `PERS`, `send_to_char`, `is_same_group`, `IS_NPC`, `capitalize`, `get_char_room`, `act_new`, `IS_AFFECTED`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_group.if.001` | 1705 | `if ( arg[0] == '\0' )` |  | pending |
| `act_comm.do_group.ternary.001` | 1710 | `? ch->leader : ch;` |  | pending |
| `act_comm.do_group.for.001` | 1714 | `for ( gch = char_list; gch != NULL; gch = gch->next )` |  | pending |
| `act_comm.do_group.if.002` | 1716 | `if ( is_same_group( gch, ch ) )` |  | pending |
| `act_comm.do_group.ternary.002` | 1721 | `? "Mob" : class_table[gch->class].who_name,` |  | pending |
| `act_comm.do_group.return.001` | 1730 | `return;` |  | pending |
| `act_comm.do_group.if.003` | 1733 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `act_comm.do_group.return.002` | 1736 | `return;` |  | pending |
| `act_comm.do_group.if.004` | 1739 | `if ( ch->master != NULL \|\| ( ch->leader != NULL && ch->leader != ch ) )` |  | pending |
| `act_comm.do_group.or.001` | 1739 | `\|\| ( ch->leader != NULL && ch->leader != ch ) )` |  | pending |
| `act_comm.do_group.and.001` | 1739 | `&& ch->leader != ch ) )` |  | pending |
| `act_comm.do_group.return.003` | 1742 | `return;` |  | pending |
| `act_comm.do_group.if.005` | 1745 | `if ( victim->master != ch && ch != victim )` |  | pending |
| `act_comm.do_group.and.002` | 1745 | `&& ch != victim )` |  | pending |
| `act_comm.do_group.return.004` | 1748 | `return;` |  | pending |
| `act_comm.do_group.if.006` | 1751 | `if (IS_AFFECTED(victim,AFF_CHARM))` |  | pending |
| `act_comm.do_group.return.005` | 1754 | `return;` |  | pending |
| `act_comm.do_group.if.007` | 1757 | `if (IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `act_comm.do_group.return.006` | 1761 | `return;` |  | pending |
| `act_comm.do_group.if.008` | 1764 | `if ( is_same_group( victim, ch ) && ch != victim )` |  | pending |
| `act_comm.do_group.and.003` | 1764 | `&& ch != victim )` |  | pending |
| `act_comm.do_group.return.007` | 1773 | `return;` |  | pending |
| `act_comm.do_group.return.008` | 1780 | `return;` |  | pending |

## do_split

[Source line 1788](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1788); ends at line 1904. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- get_obj: `src/act_obj.c:176` (function_symbol_reference_candidate).
- do_sacrifice: `src/act_obj.c:1827` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:271` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:259` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `atoi`, `is_same_group`, `IS_AFFECTED`, `sprintf`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_split.if.001` | 1801 | `if ( arg1[0] == '\0' )` |  | pending |
| `act_comm.do_split.return.001` | 1804 | `return;` |  | pending |
| `act_comm.do_split.if.002` | 1809 | `if (arg2[0] != '\0')` |  | pending |
| `act_comm.do_split.if.003` | 1812 | `if ( amount_gold < 0 \|\| amount_silver < 0)` |  | pending |
| `act_comm.do_split.or.001` | 1812 | `\|\| amount_silver < 0)` |  | pending |
| `act_comm.do_split.return.002` | 1815 | `return;` |  | pending |
| `act_comm.do_split.if.004` | 1818 | `if ( amount_gold == 0 && amount_silver == 0 )` |  | pending |
| `act_comm.do_split.and.001` | 1818 | `&& amount_silver == 0 )` |  | pending |
| `act_comm.do_split.return.003` | 1821 | `return;` |  | pending |
| `act_comm.do_split.if.005` | 1824 | `if ( ch->gold <  amount_gold \|\| ch->silver < amount_silver)` |  | pending |
| `act_comm.do_split.or.002` | 1824 | `\|\| ch->silver < amount_silver)` |  | pending |
| `act_comm.do_split.return.004` | 1827 | `return;` |  | pending |
| `act_comm.do_split.for.001` | 1831 | `for ( gch = ch->in_room->people; gch != NULL; gch = gch->next_in_room )` |  | pending |
| `act_comm.do_split.if.006` | 1833 | `if ( is_same_group( gch, ch ) && !IS_AFFECTED(gch,AFF_CHARM))` |  | pending |
| `act_comm.do_split.and.002` | 1833 | `&& !IS_AFFECTED(gch,AFF_CHARM))` |  | pending |
| `act_comm.do_split.if.007` | 1837 | `if ( members < 2 )` |  | pending |
| `act_comm.do_split.return.005` | 1840 | `return;` |  | pending |
| `act_comm.do_split.if.008` | 1849 | `if ( share_gold == 0 && share_silver == 0 )` |  | pending |
| `act_comm.do_split.and.003` | 1849 | `&& share_silver == 0 )` |  | pending |
| `act_comm.do_split.return.006` | 1852 | `return;` |  | pending |
| `act_comm.do_split.if.009` | 1860 | `if (share_silver > 0)` |  | pending |
| `act_comm.do_split.if.010` | 1868 | `if (share_gold > 0)` |  | pending |
| `act_comm.do_split.if.011` | 1876 | `if (share_gold == 0)` |  | pending |
| `act_comm.do_split.if.012` | 1881 | `if (share_silver == 0)` |  | pending |
| `act_comm.do_split.for.002` | 1893 | `for ( gch = ch->in_room->people; gch != NULL; gch = gch->next_in_room )` |  | pending |
| `act_comm.do_split.if.013` | 1895 | `if ( gch != ch && is_same_group(gch,ch) && !IS_AFFECTED(gch,AFF_CHARM))` |  | pending |
| `act_comm.do_split.and.004` | 1895 | `&& is_same_group(gch,ch) && !IS_AFFECTED(gch,AFF_CHARM))` |  | pending |
| `act_comm.do_split.and.005` | 1895 | `&& !IS_AFFECTED(gch,AFF_CHARM))` |  | pending |
| `act_comm.do_split.return.007` | 1903 | `return;` |  | pending |

## do_gtell

[Source line 1908](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1908); ends at line 1932. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:187` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:188` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:143` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `IS_SET`, `is_same_group`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_gtell.if.001` | 1912 | `if ( argument[0] == '\0' )` |  | pending |
| `act_comm.do_gtell.return.001` | 1915 | `return;` |  | pending |
| `act_comm.do_gtell.if.002` | 1918 | `if ( IS_SET( ch->comm, COMM_NOTELL ) )` |  | pending |
| `act_comm.do_gtell.return.002` | 1921 | `return;` |  | pending |
| `act_comm.do_gtell.for.001` | 1924 | `for ( gch = char_list; gch != NULL; gch = gch->next )` |  | pending |
| `act_comm.do_gtell.if.003` | 1926 | `if ( is_same_group( gch, ch ) )` |  | pending |
| `act_comm.do_gtell.return.003` | 1931 | `return;` |  | pending |

## do_commands

[Source line 1934](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1934); ends at line 1957. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:114` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:101` (declaration_or_dispatch_reference).

Dependencies: `get_trust`, `sprintf`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_commands.for.001` | 1941 | `for ( cmd = 0; cmd_table[cmd].name[0] != '\0'; cmd++ )` |  | pending |
| `act_comm.do_commands.if.001` | 1943 | `if ( cmd_table[cmd].level <  LEVEL_HERO         &&   cmd_table[cmd].level <= get_trust( ch )    &&   cmd_table[cmd].show)` |  | pending |
| `act_comm.do_commands.and.001` | 1944 | `&&   cmd_table[cmd].level <= get_trust( ch )` |  | pending |
| `act_comm.do_commands.and.002` | 1945 | `&&   cmd_table[cmd].show)` |  | pending |
| `act_comm.do_commands.if.002` | 1949 | `if ( ++col % 6 == 0 )` |  | pending |
| `act_comm.do_commands.if.003` | 1954 | `if ( col % 6 != 0 )` |  | pending |
| `act_comm.do_commands.return.001` | 1956 | `return;` |  | pending |

## do_wizhelp

[Source line 1959](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1959); ends at line 1982. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:105` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:291` (declaration_or_dispatch_reference).

Dependencies: `get_trust`, `sprintf`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.do_wizhelp.for.001` | 1966 | `for ( cmd = 0; cmd_table[cmd].name[0] != '\0'; cmd++ )` |  | pending |
| `act_comm.do_wizhelp.if.001` | 1968 | `if ( cmd_table[cmd].level >= LEVEL_HERO         &&   cmd_table[cmd].level <= get_trust( ch )          &&   cmd_table[cmd].show)` |  | pending |
| `act_comm.do_wizhelp.and.001` | 1969 | `&&   cmd_table[cmd].level <= get_trust( ch )` |  | pending |
| `act_comm.do_wizhelp.and.002` | 1970 | `&&   cmd_table[cmd].show)` |  | pending |
| `act_comm.do_wizhelp.if.002` | 1974 | `if ( ++col % 6 == 0 )` |  | pending |
| `act_comm.do_wizhelp.if.003` | 1979 | `if ( col % 6 != 0 )` |  | pending |
| `act_comm.do_wizhelp.return.001` | 1981 | `return;` |  | pending |

## is_same_group

[Source line 1991](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1991); ends at line 1999. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_group: `src/act_comm.c:1716` (lexical_call_candidate).
- do_group: `src/act_comm.c:1764` (lexical_call_candidate).
- do_split: `src/act_comm.c:1833` (lexical_call_candidate).
- do_split: `src/act_comm.c:1895` (lexical_call_candidate).
- do_gtell: `src/act_comm.c:1926` (lexical_call_candidate).
- can_loot: `src/act_obj.c:82` (lexical_call_candidate).
- get_obj: `src/act_obj.c:169` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1820` (lexical_call_candidate).
- check_assist: `src/fight.c:124` (lexical_call_candidate).
- check_assist: `src/fight.c:164` (lexical_call_candidate).
- is_safe_spell: `src/fight.c:1137` (lexical_call_candidate).
- is_safe_spell: `src/fight.c:1143` (lexical_call_candidate).
- is_safe_spell: `src/fight.c:1166` (lexical_call_candidate).
- group_gain: `src/fight.c:1713` (lexical_call_candidate).
- group_gain: `src/fight.c:1734` (lexical_call_candidate).
- do_bash: `src/fight.c:2258` (lexical_call_candidate).
- do_dirt: `src/fight.c:2389` (lexical_call_candidate).
- do_trip: `src/fight.c:2511` (lexical_call_candidate).
- do_kill: `src/fight.c:2628` (lexical_call_candidate).
- do_murder: `src/fight.c:2696` (lexical_call_candidate).
- do_backstab: `src/fight.c:2764` (lexical_call_candidate).
- do_rescue: `src/fight.c:2906` (lexical_call_candidate).
- is_friend: `src/handler.c:52` (lexical_call_candidate).
- spell_mass_invis: `src/magic.c:3698` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2076` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_comm.is_same_group.if.001` | 1993 | `if ( ach == NULL \|\| bch == NULL)` |  | pending |
| `act_comm.is_same_group.or.001` | 1993 | `\|\| bch == NULL)` |  | pending |
| `act_comm.is_same_group.return.001` | 1994 | `return FALSE;` |  | pending |
| `act_comm.is_same_group.if.002` | 1996 | `if ( ach->leader != NULL )` |  | pending |
| `act_comm.is_same_group.if.003` | 1997 | `if ( bch->leader != NULL )` |  | pending |
| `act_comm.is_same_group.return.002` | 1998 | `return ach == bch;` |  | pending |

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
- Line 37: `#include <time.h>` — pending configuration/reachability review.
- Line 38: `#include <unistd.h>` — pending configuration/reachability review.
- Line 39: `#include "merc.h"` — pending configuration/reachability review.
- Line 40: `#include "interp.h"` — pending configuration/reachability review.
- Line 41: `#include "recycle.h"` — pending configuration/reachability review.
- Line 42: `#include "tables.h"` — pending configuration/reachability review.

## Static tables

- `pose_table` at line 1121 — pending entry/termination review.

## Commented code candidates


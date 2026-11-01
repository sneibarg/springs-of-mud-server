# src/act_wiz.c

Role: translation_unit. Disposition: **pending**. SHA-256: `5d1aef421c3a2190aab5b56f0b2abb9c11c44600633dbc58a6abd9e30db7fe8b`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## do_wiznet

[Source line 49](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:49); ends at line 151. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:346` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:294` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `send_to_char`, `REMOVE_BIT`, `SET_BIT`, `str_prefix`, `strcat`, `get_trust`, `wiznet_lookup`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_wiznet.if.001` | 54 | `if ( argument[0] == '\0' )` |  | pending |
| `act_wiz.do_wiznet.if.002` | 56 | `if (IS_SET(ch->wiznet,WIZ_ON))` |  | pending |
| `act_wiz.do_wiznet.return.001` | 66 | `return;` |  | pending |
| `act_wiz.do_wiznet.if.003` | 69 | `if (!str_prefix(argument,"on"))` |  | pending |
| `act_wiz.do_wiznet.return.002` | 73 | `return;` |  | pending |
| `act_wiz.do_wiznet.if.004` | 76 | `if (!str_prefix(argument,"off"))` |  | pending |
| `act_wiz.do_wiznet.return.003` | 80 | `return;` |  | pending |
| `act_wiz.do_wiznet.if.005` | 84 | `if (!str_prefix(argument,"status"))` |  | pending |
| `act_wiz.do_wiznet.if.006` | 88 | `if (!IS_SET(ch->wiznet,WIZ_ON))` |  | pending |
| `act_wiz.do_wiznet.for.001` | 91 | `for (flag = 0; wiznet_table[flag].name != NULL; flag++)` |  | pending |
| `act_wiz.do_wiznet.if.007` | 92 | `if (IS_SET(ch->wiznet,wiznet_table[flag].flag))` |  | pending |
| `act_wiz.do_wiznet.return.004` | 102 | `return;` |  | pending |
| `act_wiz.do_wiznet.if.008` | 105 | `if (!str_prefix(argument,"show"))` |  | pending |
| `act_wiz.do_wiznet.for.002` | 110 | `for (flag = 0; wiznet_table[flag].name != NULL; flag++)` |  | pending |
| `act_wiz.do_wiznet.if.009` | 112 | `if (wiznet_table[flag].level <= get_trust(ch))` |  | pending |
| `act_wiz.do_wiznet.return.005` | 123 | `return;` |  | pending |
| `act_wiz.do_wiznet.if.010` | 128 | `if (flag == -1 \|\| get_trust(ch) < wiznet_table[flag].level)` |  | pending |
| `act_wiz.do_wiznet.or.001` | 128 | `\|\| get_trust(ch) < wiznet_table[flag].level)` |  | pending |
| `act_wiz.do_wiznet.return.006` | 131 | `return;` |  | pending |
| `act_wiz.do_wiznet.if.011` | 134 | `if (IS_SET(ch->wiznet,wiznet_table[flag].flag))` |  | pending |
| `act_wiz.do_wiznet.return.007` | 140 | `return;` |  | pending |
| `act_wiz.do_wiznet.return.008` | 148 | `return;` |  | pending |

## wiznet

[Source line 153](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:153); ends at line 175. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_delete: `src/act_comm.c:69` (lexical_call_candidate).
- do_delete: `src/act_comm.c:88` (lexical_call_candidate).
- do_quit: `src/act_comm.c:1419` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1832` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2229` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:56` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:59` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:64` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:72` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:79` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:88` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:92` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:134` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:139` (function_symbol_reference_candidate).
- do_wiznet: `src/act_wiz.c:147` (function_symbol_reference_candidate).
- wiznet: `src/act_wiz.c:162` (function_symbol_reference_candidate).
- wiznet: `src/act_wiz.c:163` (function_symbol_reference_candidate).
- wiznet: `src/act_wiz.c:164` (function_symbol_reference_candidate).
- wiznet: `src/act_wiz.c:168` (function_symbol_reference_candidate).
- do_nochannels: `src/act_wiz.c:327` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:336` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:531` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2126` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2171` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2232` (lexical_call_candidate).
- do_return: `src/act_wiz.c:2272` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2380` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2424` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2486` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2538` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2784` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2837` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2880` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2888` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2989` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2997` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3042` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3050` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3089` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3097` (lexical_call_candidate).
- do_wizlock: `src/act_wiz.c:3128` (lexical_call_candidate).
- do_wizlock: `src/act_wiz.c:3133` (lexical_call_candidate).
- do_newlock: `src/act_wiz.c:3149` (lexical_call_candidate).
- do_newlock: `src/act_wiz.c:3154` (lexical_call_candidate).
- close_socket: `src/comm.c:993` (lexical_call_candidate).
- read_from_buffer: `src/comm.c:1174` (lexical_call_candidate).
- read_from_buffer: `src/comm.c:1177` (lexical_call_candidate).
- read_from_buffer: `src/comm.c:1180` (lexical_call_candidate).
- nanny: `src/comm.c:1669` (lexical_call_candidate).
- nanny: `src/comm.c:1910` (lexical_call_candidate).
- nanny: `src/comm.c:1911` (lexical_call_candidate).
- nanny: `src/comm.c:2120` (lexical_call_candidate).
- check_reconnect: `src/comm.c:2274` (lexical_call_candidate).
- area_update: `src/db.c:1194` (lexical_call_candidate).
- damage: `src/fight.c:892` (lexical_call_candidate).
- damage: `src/fight.c:894` (lexical_call_candidate).
- check_killer: `src/fight.c:1253` (lexical_call_candidate).
- interpret: `src/interp.c:443` (lexical_call_candidate).
- fwrite_char: `src/save.c:220` (function_symbol_reference_candidate).
- fwrite_char: `src/save.c:221` (function_symbol_reference_candidate).
- fread_char: `src/save.c:1117` (function_symbol_reference_candidate).
- gain_exp: `src/update.c:134` (lexical_call_candidate).
- update_handler: `src/update.c:1116` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:1409` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2093` (declaration_or_dispatch_reference).

Dependencies: `IS_IMMORTAL`, `IS_SET`, `get_trust`, `send_to_char`, `act_new`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.wiznet.for.001` | 158 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_wiz.wiznet.if.001` | 160 | `if (d->connected == CON_PLAYING 	&&  IS_IMMORTAL(d->character)  	&&  IS_SET(d->character->wiznet,WIZ_ON)  	&&  (!flag \|\| IS_SET(d->character->wiznet,flag)) 	&&  (!flag_skip \|\| !IS_SET(d->character->wiznet,flag_skip)) 	&&  get_trust(d->character) >= min_level 	&&  d->character != ch)` |  | pending |
| `act_wiz.wiznet.and.001` | 161 | `&&  IS_IMMORTAL(d->character)` |  | pending |
| `act_wiz.wiznet.and.002` | 162 | `&&  IS_SET(d->character->wiznet,WIZ_ON)` |  | pending |
| `act_wiz.wiznet.and.003` | 163 | `&&  (!flag \|\| IS_SET(d->character->wiznet,flag))` |  | pending |
| `act_wiz.wiznet.or.001` | 163 | `\|\| IS_SET(d->character->wiznet,flag))` |  | pending |
| `act_wiz.wiznet.and.004` | 164 | `&&  (!flag_skip \|\| !IS_SET(d->character->wiznet,flag_skip))` |  | pending |
| `act_wiz.wiznet.or.002` | 164 | `\|\| !IS_SET(d->character->wiznet,flag_skip))` |  | pending |
| `act_wiz.wiznet.and.005` | 165 | `&&  get_trust(d->character) >= min_level` |  | pending |
| `act_wiz.wiznet.and.006` | 166 | `&&  d->character != ch)` |  | pending |
| `act_wiz.wiznet.if.002` | 168 | `if (IS_SET(d->character->wiznet,WIZ_PREFIX))` |  | pending |
| `act_wiz.wiznet.return.001` | 174 | `return;` |  | pending |

## do_guild

[Source line 177](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:177); ends at line 229. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:89` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:144` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `str_prefix`, `clan_lookup`, `sprintf`, `capitalize`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_guild.if.001` | 187 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' )` |  | pending |
| `act_wiz.do_guild.or.001` | 187 | `\|\| arg2[0] == '\0' )` |  | pending |
| `act_wiz.do_guild.return.001` | 190 | `return;` |  | pending |
| `act_wiz.do_guild.if.002` | 192 | `if ( ( victim = get_char_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_guild.return.002` | 195 | `return;` |  | pending |
| `act_wiz.do_guild.if.003` | 198 | `if (!str_prefix(arg2,"none"))` |  | pending |
| `act_wiz.do_guild.return.003` | 203 | `return;` |  | pending |
| `act_wiz.do_guild.if.004` | 206 | `if ((clan = clan_lookup(arg2)) == 0)` |  | pending |
| `act_wiz.do_guild.return.004` | 209 | `return;` |  | pending |
| `act_wiz.do_guild.if.005` | 212 | `if (clan_table[clan].independent)` |  | pending |

## do_outfit

[Source line 232](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:232); ends at line 291. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:2096` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:166` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:190` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `send_to_char`, `get_eq_char`, `create_object`, `get_obj_index`, `obj_to_char`, `equip_char`, `IS_WEAPON_STAT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_outfit.if.001` | 237 | `if (ch->level > 5 \|\| IS_NPC(ch))` |  | pending |
| `act_wiz.do_outfit.or.001` | 237 | `\|\| IS_NPC(ch))` |  | pending |
| `act_wiz.do_outfit.return.001` | 240 | `return;` |  | pending |
| `act_wiz.do_outfit.if.002` | 243 | `if ( ( obj = get_eq_char( ch, WEAR_LIGHT ) ) == NULL )` |  | pending |
| `act_wiz.do_outfit.if.003` | 251 | `if ( ( obj = get_eq_char( ch, WEAR_BODY ) ) == NULL )` |  | pending |
| `act_wiz.do_outfit.if.004` | 260 | `if ((obj = get_eq_char(ch,WEAR_WIELD)) == NULL)` |  | pending |
| `act_wiz.do_outfit.for.001` | 265 | `for (i = 0; weapon_table[i].name != NULL; i++)` |  | pending |
| `act_wiz.do_outfit.if.005` | 267 | `if (ch->pcdata->learned[sn] <  		ch->pcdata->learned[*weapon_table[i].gsn])` |  | pending |
| `act_wiz.do_outfit.if.006` | 280 | `if (((obj = get_eq_char(ch,WEAR_WIELD)) == NULL      \|\|   !IS_WEAPON_STAT(obj,WEAPON_TWO_HANDS))      &&  (obj = get_eq_char( ch, WEAR_SHIELD ) ) == NULL )` |  | pending |
| `act_wiz.do_outfit.or.002` | 281 | `\|\|   !IS_WEAPON_STAT(obj,WEAPON_TWO_HANDS))` |  | pending |
| `act_wiz.do_outfit.and.001` | 282 | `&&  (obj = get_eq_char( ch, WEAR_SHIELD ) ) == NULL )` |  | pending |

## do_nochannels

[Source line 295](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:295); ends at line 340. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:307` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:175` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `get_trust`, `IS_SET`, `REMOVE_BIT`, `sprintf`, `wiznet`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_nochannels.if.001` | 302 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_nochannels.return.001` | 305 | `return;` |  | pending |
| `act_wiz.do_nochannels.if.002` | 308 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_nochannels.return.002` | 311 | `return;` |  | pending |
| `act_wiz.do_nochannels.if.003` | 314 | `if ( get_trust( victim ) >= get_trust( ch ) )` |  | pending |
| `act_wiz.do_nochannels.return.003` | 317 | `return;` |  | pending |
| `act_wiz.do_nochannels.if.004` | 320 | `if ( IS_SET(victim->comm, COMM_NOCHANNELS) )` |  | pending |
| `act_wiz.do_nochannels.return.004` | 339 | `return;` |  | pending |

## do_smote

[Source line 343](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:343); ends at line 434. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:350` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:252` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `strstr`, `strcpy`, `strlen`, `strcat`, `strncat`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_smote.if.001` | 350 | `if ( !IS_NPC(ch) && IS_SET(ch->comm, COMM_NOEMOTE) )` |  | pending |
| `act_wiz.do_smote.and.001` | 350 | `&& IS_SET(ch->comm, COMM_NOEMOTE) )` |  | pending |
| `act_wiz.do_smote.return.001` | 353 | `return;` |  | pending |
| `act_wiz.do_smote.if.002` | 356 | `if ( argument[0] == '\0' )` |  | pending |
| `act_wiz.do_smote.return.002` | 359 | `return;` |  | pending |
| `act_wiz.do_smote.if.003` | 362 | `if (strstr(argument,ch->name) == NULL)` |  | pending |
| `act_wiz.do_smote.return.003` | 365 | `return;` |  | pending |
| `act_wiz.do_smote.for.001` | 371 | `for (vch = ch->in_room->people; vch != NULL; vch = vch->next_in_room)` |  | pending |
| `act_wiz.do_smote.if.004` | 373 | `if (vch->desc == NULL \|\| vch == ch)` |  | pending |
| `act_wiz.do_smote.or.001` | 373 | `\|\| vch == ch)` |  | pending |
| `act_wiz.do_smote.continue.001` | 374 | `continue;` |  | pending |
| `act_wiz.do_smote.if.005` | 376 | `if ((letter = strstr(argument,vch->name)) == NULL)` |  | pending |
| `act_wiz.do_smote.continue.002` | 380 | `continue;` |  | pending |
| `act_wiz.do_smote.for.002` | 388 | `for (; *letter != '\0'; letter++)` |  | pending |
| `act_wiz.do_smote.if.006` | 390 | `if (*letter == '\'' && matches == strlen(vch->name))` |  | pending |
| `act_wiz.do_smote.and.002` | 390 | `&& matches == strlen(vch->name))` |  | pending |
| `act_wiz.do_smote.continue.003` | 393 | `continue;` |  | pending |
| `act_wiz.do_smote.if.007` | 396 | `if (*letter == 's' && matches == strlen(vch->name))` |  | pending |
| `act_wiz.do_smote.and.003` | 396 | `&& matches == strlen(vch->name))` |  | pending |
| `act_wiz.do_smote.continue.004` | 399 | `continue;` |  | pending |
| `act_wiz.do_smote.if.008` | 402 | `if (matches == strlen(vch->name))` |  | pending |
| `act_wiz.do_smote.if.009` | 407 | `if (*letter == *name)` |  | pending |
| `act_wiz.do_smote.if.010` | 411 | `if (matches == strlen(vch->name))` |  | pending |
| `act_wiz.do_smote.continue.005` | 416 | `continue;` |  | pending |
| `act_wiz.do_smote.continue.006` | 419 | `continue;` |  | pending |
| `act_wiz.do_smote.return.004` | 433 | `return;` |  | pending |

## do_bamfin

[Source line 436](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:436); ends at line 464. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:321` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:87` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `smash_tilde`, `sprintf`, `send_to_char`, `strstr`, `free_string`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_bamfin.if.001` | 440 | `if ( !IS_NPC(ch) )` |  | pending |
| `act_wiz.do_bamfin.if.002` | 444 | `if (argument[0] == '\0')` |  | pending |
| `act_wiz.do_bamfin.return.001` | 448 | `return;` |  | pending |
| `act_wiz.do_bamfin.if.003` | 451 | `if ( strstr(argument,ch->name) == NULL)` |  | pending |
| `act_wiz.do_bamfin.return.002` | 454 | `return;` |  | pending |
| `act_wiz.do_bamfin.return.003` | 463 | `return;` |  | pending |

## do_bamfout

[Source line 466](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:466); ends at line 494. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:322` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:88` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `smash_tilde`, `sprintf`, `send_to_char`, `strstr`, `free_string`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_bamfout.if.001` | 470 | `if ( !IS_NPC(ch) )` |  | pending |
| `act_wiz.do_bamfout.if.002` | 474 | `if (argument[0] == '\0')` |  | pending |
| `act_wiz.do_bamfout.return.001` | 478 | `return;` |  | pending |
| `act_wiz.do_bamfout.if.003` | 481 | `if ( strstr(argument,ch->name) == NULL)` |  | pending |
| `act_wiz.do_bamfout.return.002` | 484 | `return;` |  | pending |
| `act_wiz.do_bamfout.return.003` | 493 | `return;` |  | pending |

## do_deny

[Source line 498](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:498); ends at line 538. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:290` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:111` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `IS_NPC`, `get_trust`, `SET_BIT`, `sprintf`, `wiznet`, `save_char_obj`, `stop_fighting`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_deny.if.001` | 504 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_deny.return.001` | 507 | `return;` |  | pending |
| `act_wiz.do_deny.if.002` | 510 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_deny.return.002` | 513 | `return;` |  | pending |
| `act_wiz.do_deny.if.003` | 516 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_deny.return.003` | 519 | `return;` |  | pending |
| `act_wiz.do_deny.if.004` | 522 | `if ( get_trust( victim ) >= get_trust( ch ) )` |  | pending |
| `act_wiz.do_deny.return.004` | 525 | `return;` |  | pending |
| `act_wiz.do_deny.return.005` | 537 | `return;` |  | pending |

## do_disconnect

[Source line 542](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:542); ends at line 596. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:291` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:115` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `is_number`, `atoi`, `close_socket`, `get_char_world`, `act`, `bug`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_disconnect.if.001` | 549 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_disconnect.return.001` | 552 | `return;` |  | pending |
| `act_wiz.do_disconnect.if.002` | 555 | `if (is_number(arg))` |  | pending |
| `act_wiz.do_disconnect.for.001` | 560 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_wiz.do_disconnect.if.003` | 562 | `if ( d->descriptor == desc )` |  | pending |
| `act_wiz.do_disconnect.return.002` | 566 | `return;` |  | pending |
| `act_wiz.do_disconnect.if.004` | 571 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_disconnect.return.003` | 574 | `return;` |  | pending |
| `act_wiz.do_disconnect.if.005` | 577 | `if ( victim->desc == NULL )` |  | pending |
| `act_wiz.do_disconnect.return.004` | 580 | `return;` |  | pending |
| `act_wiz.do_disconnect.for.002` | 583 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_wiz.do_disconnect.if.006` | 585 | `if ( d == victim->desc )` |  | pending |
| `act_wiz.do_disconnect.return.005` | 589 | `return;` |  | pending |
| `act_wiz.do_disconnect.return.006` | 595 | `return;` |  | pending |

## do_pardon

[Source line 600](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:600); ends at line 651. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:312` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:192` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `IS_NPC`, `str_cmp`, `IS_SET`, `REMOVE_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_pardon.if.001` | 609 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' )` |  | pending |
| `act_wiz.do_pardon.or.001` | 609 | `\|\| arg2[0] == '\0' )` |  | pending |
| `act_wiz.do_pardon.return.001` | 612 | `return;` |  | pending |
| `act_wiz.do_pardon.if.002` | 615 | `if ( ( victim = get_char_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_pardon.return.002` | 618 | `return;` |  | pending |
| `act_wiz.do_pardon.if.003` | 621 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_pardon.return.003` | 624 | `return;` |  | pending |
| `act_wiz.do_pardon.if.004` | 627 | `if ( !str_cmp( arg2, "killer" ) )` |  | pending |
| `act_wiz.do_pardon.if.005` | 629 | `if ( IS_SET(victim->act, PLR_KILLER) )` |  | pending |
| `act_wiz.do_pardon.return.004` | 635 | `return;` |  | pending |
| `act_wiz.do_pardon.if.006` | 638 | `if ( !str_cmp( arg2, "thief" ) )` |  | pending |
| `act_wiz.do_pardon.if.007` | 640 | `if ( IS_SET(victim->act, PLR_THIEF) )` |  | pending |
| `act_wiz.do_pardon.return.005` | 646 | `return;` |  | pending |
| `act_wiz.do_pardon.return.006` | 650 | `return;` |  | pending |

## do_echo

[Source line 655](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:655); ends at line 677. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_reboot: `src/act_wiz.c:2015` (function_symbol_reference_candidate).
- do_shutdown: `src/act_wiz.c:2050` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:323` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:122` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_trust`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_echo.if.001` | 659 | `if ( argument[0] == '\0' )` |  | pending |
| `act_wiz.do_echo.return.001` | 662 | `return;` |  | pending |
| `act_wiz.do_echo.for.001` | 665 | `for ( d = descriptor_list; d; d = d->next )` |  | pending |
| `act_wiz.do_echo.if.002` | 667 | `if ( d->connected == CON_PLAYING )` |  | pending |
| `act_wiz.do_echo.if.003` | 669 | `if (get_trust(d->character) >= get_trust(ch))` |  | pending |
| `act_wiz.do_echo.return.002` | 676 | `return;` |  | pending |

## do_recho

[Source line 681](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:681); ends at line 705. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:334` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:220` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_trust`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_recho.if.001` | 685 | `if ( argument[0] == '\0' )` |  | pending |
| `act_wiz.do_recho.return.001` | 689 | `return;` |  | pending |
| `act_wiz.do_recho.for.001` | 692 | `for ( d = descriptor_list; d; d = d->next )` |  | pending |
| `act_wiz.do_recho.if.002` | 694 | `if ( d->connected == CON_PLAYING 	&&   d->character->in_room == ch->in_room )` |  | pending |
| `act_wiz.do_recho.and.001` | 695 | `&&   d->character->in_room == ch->in_room )` |  | pending |
| `act_wiz.do_recho.if.003` | 697 | `if (get_trust(d->character) >= get_trust(ch))` |  | pending |
| `act_wiz.do_recho.return.002` | 704 | `return;` |  | pending |

## do_zecho

[Source line 707](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:707); ends at line 729. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:342` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:298` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_trust`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_zecho.if.001` | 711 | `if (argument[0] == '\0')` |  | pending |
| `act_wiz.do_zecho.return.001` | 714 | `return;` |  | pending |
| `act_wiz.do_zecho.for.001` | 717 | `for (d = descriptor_list; d; d = d->next)` |  | pending |
| `act_wiz.do_zecho.if.002` | 719 | `if (d->connected == CON_PLAYING 	&&  d->character->in_room != NULL && ch->in_room != NULL 	&&  d->character->in_room->area == ch->in_room->area)` |  | pending |
| `act_wiz.do_zecho.and.001` | 720 | `&&  d->character->in_room != NULL && ch->in_room != NULL` |  | pending |
| `act_wiz.do_zecho.and.002` | 720 | `&& ch->in_room != NULL` |  | pending |
| `act_wiz.do_zecho.and.003` | 721 | `&&  d->character->in_room->area == ch->in_room->area)` |  | pending |
| `act_wiz.do_zecho.if.003` | 723 | `if (get_trust(d->character) >= get_trust(ch))` |  | pending |

## do_pecho

[Source line 731](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:731); ends at line 758. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:311` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:195` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `get_trust`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_pecho.if.001` | 738 | `if ( argument[0] == '\0' \|\| arg[0] == '\0' )` |  | pending |
| `act_wiz.do_pecho.or.001` | 738 | `\|\| arg[0] == '\0' )` |  | pending |
| `act_wiz.do_pecho.return.001` | 741 | `return;` |  | pending |
| `act_wiz.do_pecho.if.002` | 744 | `if  ( (victim = get_char_world(ch, arg) ) == NULL )` |  | pending |
| `act_wiz.do_pecho.return.002` | 747 | `return;` |  | pending |
| `act_wiz.do_pecho.if.003` | 750 | `if (get_trust(victim) >= get_trust(ch) && get_trust(ch) != MAX_LEVEL)` |  | pending |
| `act_wiz.do_pecho.and.001` | 750 | `&& get_trust(ch) != MAX_LEVEL)` |  | pending |

## find_location

[Source line 761](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:761); ends at line 776. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_transfer: `src/act_wiz.c:823` (lexical_call_candidate).
- do_at: `src/act_wiz.c:879` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:930` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:991` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1091` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1111` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:3998` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_wiz.c:47` (declaration_or_dispatch_reference).

Dependencies: `is_number`, `get_room_index`, `atoi`, `get_char_world`, `get_obj_world`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.find_location.if.001` | 766 | `if ( is_number(arg) )` |  | pending |
| `act_wiz.find_location.return.001` | 767 | `return get_room_index( atoi( arg ) );` |  | pending |
| `act_wiz.find_location.if.002` | 769 | `if ( ( victim = get_char_world( ch, arg ) ) != NULL )` |  | pending |
| `act_wiz.find_location.return.002` | 770 | `return victim->in_room;` |  | pending |
| `act_wiz.find_location.if.003` | 772 | `if ( ( obj = get_obj_world( ch, arg ) ) != NULL )` |  | pending |
| `act_wiz.find_location.return.003` | 773 | `return obj->in_room;` |  | pending |
| `act_wiz.find_location.return.004` | 775 | `return NULL;` |  | pending |

## do_transfer

[Source line 780](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:780); ends at line 859. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_transfer: `src/act_wiz.c:808` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:317` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:318` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:271` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `can_see`, `sprintf`, `do_function`, `find_location`, `is_room_owner`, `room_is_private`, `get_trust`, `get_char_world`, `stop_fighting`, `act`, `char_from_room`, `char_to_room`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_transfer.if.001` | 791 | `if ( arg1[0] == '\0' )` |  | pending |
| `act_wiz.do_transfer.return.001` | 794 | `return;` |  | pending |
| `act_wiz.do_transfer.if.002` | 797 | `if ( !str_cmp( arg1, "all" ) )` |  | pending |
| `act_wiz.do_transfer.for.001` | 799 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_wiz.do_transfer.if.003` | 801 | `if ( d->connected == CON_PLAYING 	    &&   d->character != ch 	    &&   d->character->in_room != NULL 	    &&   can_see( ch, d->character ) )` |  | pending |
| `act_wiz.do_transfer.and.001` | 802 | `&&   d->character != ch` |  | pending |
| `act_wiz.do_transfer.and.002` | 803 | `&&   d->character->in_room != NULL` |  | pending |
| `act_wiz.do_transfer.and.003` | 804 | `&&   can_see( ch, d->character ) )` |  | pending |
| `act_wiz.do_transfer.return.002` | 811 | `return;` |  | pending |
| `act_wiz.do_transfer.if.004` | 817 | `if ( arg2[0] == '\0' )` |  | pending |
| `act_wiz.do_transfer.if.005` | 823 | `if ( ( location = find_location( ch, arg2 ) ) == NULL )` |  | pending |
| `act_wiz.do_transfer.return.003` | 826 | `return;` |  | pending |
| `act_wiz.do_transfer.if.006` | 829 | `if ( !is_room_owner(ch,location) && room_is_private( location )  	&&  get_trust(ch) < MAX_LEVEL)` |  | pending |
| `act_wiz.do_transfer.and.004` | 829 | `&& room_is_private( location )` |  | pending |
| `act_wiz.do_transfer.and.005` | 830 | `&&  get_trust(ch) < MAX_LEVEL)` |  | pending |
| `act_wiz.do_transfer.return.004` | 833 | `return;` |  | pending |
| `act_wiz.do_transfer.if.007` | 837 | `if ( ( victim = get_char_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_transfer.return.005` | 840 | `return;` |  | pending |
| `act_wiz.do_transfer.if.008` | 843 | `if ( victim->in_room == NULL )` |  | pending |
| `act_wiz.do_transfer.return.006` | 846 | `return;` |  | pending |
| `act_wiz.do_transfer.if.009` | 849 | `if ( victim->fighting != NULL )` |  | pending |
| `act_wiz.do_transfer.if.010` | 855 | `if ( ch != victim )` |  | pending |

## do_at

[Source line 863](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:863); ends at line 914. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:80` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:77` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `find_location`, `is_room_owner`, `room_is_private`, `get_trust`, `char_from_room`, `char_to_room`, `interpret`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_at.if.001` | 873 | `if ( arg[0] == '\0' \|\| argument[0] == '\0' )` |  | pending |
| `act_wiz.do_at.or.001` | 873 | `\|\| argument[0] == '\0' )` |  | pending |
| `act_wiz.do_at.return.001` | 876 | `return;` |  | pending |
| `act_wiz.do_at.if.002` | 879 | `if ( ( location = find_location( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_at.return.002` | 882 | `return;` |  | pending |
| `act_wiz.do_at.if.003` | 885 | `if (!is_room_owner(ch,location) && room_is_private( location )      &&  get_trust(ch) < MAX_LEVEL)` |  | pending |
| `act_wiz.do_at.and.001` | 885 | `&& room_is_private( location )` |  | pending |
| `act_wiz.do_at.and.002` | 886 | `&&  get_trust(ch) < MAX_LEVEL)` |  | pending |
| `act_wiz.do_at.return.003` | 889 | `return;` |  | pending |
| `act_wiz.do_at.for.001` | 902 | `for ( wch = char_list; wch != NULL; wch = wch->next )` |  | pending |
| `act_wiz.do_at.if.004` | 904 | `if ( wch == ch )` |  | pending |
| `act_wiz.do_at.break.001` | 909 | `break;` |  | pending |
| `act_wiz.do_at.return.004` | 913 | `return;` |  | pending |

## do_goto

[Source line 918](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:918); ends at line 978. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:87` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:139` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `find_location`, `is_room_owner`, `room_is_private`, `get_trust`, `stop_fighting`, `act`, `char_from_room`, `char_to_room`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_goto.if.001` | 924 | `if ( argument[0] == '\0' )` |  | pending |
| `act_wiz.do_goto.return.001` | 927 | `return;` |  | pending |
| `act_wiz.do_goto.if.002` | 930 | `if ( ( location = find_location( ch, argument ) ) == NULL )` |  | pending |
| `act_wiz.do_goto.return.002` | 933 | `return;` |  | pending |
| `act_wiz.do_goto.for.001` | 937 | `for ( rch = location->people; rch != NULL; rch = rch->next_in_room )` |  | pending |
| `act_wiz.do_goto.if.003` | 940 | `if (!is_room_owner(ch,location) && room_is_private(location)      &&  (count > 1 \|\| get_trust(ch) < MAX_LEVEL))` |  | pending |
| `act_wiz.do_goto.and.001` | 940 | `&& room_is_private(location)` |  | pending |
| `act_wiz.do_goto.and.002` | 941 | `&&  (count > 1 \|\| get_trust(ch) < MAX_LEVEL))` |  | pending |
| `act_wiz.do_goto.or.001` | 941 | `\|\| get_trust(ch) < MAX_LEVEL))` |  | pending |
| `act_wiz.do_goto.return.003` | 944 | `return;` |  | pending |
| `act_wiz.do_goto.if.004` | 947 | `if ( ch->fighting != NULL )` |  | pending |
| `act_wiz.do_goto.for.002` | 950 | `for (rch = ch->in_room->people; rch != NULL; rch = rch->next_in_room)` |  | pending |
| `act_wiz.do_goto.if.005` | 952 | `if (get_trust(rch) >= ch->invis_level)` |  | pending |
| `act_wiz.do_goto.if.006` | 954 | `if (ch->pcdata != NULL && ch->pcdata->bamfout[0] != '\0')` |  | pending |
| `act_wiz.do_goto.and.003` | 954 | `&& ch->pcdata->bamfout[0] != '\0')` |  | pending |
| `act_wiz.do_goto.for.003` | 965 | `for (rch = ch->in_room->people; rch != NULL; rch = rch->next_in_room)` |  | pending |
| `act_wiz.do_goto.if.007` | 967 | `if (get_trust(rch) >= ch->invis_level)` |  | pending |
| `act_wiz.do_goto.if.008` | 969 | `if (ch->pcdata != NULL && ch->pcdata->bamfin[0] != '\0')` |  | pending |
| `act_wiz.do_goto.and.004` | 969 | `&& ch->pcdata->bamfin[0] != '\0')` |  | pending |
| `act_wiz.do_goto.return.004` | 977 | `return;` |  | pending |

## do_violate

[Source line 980](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:980); ends at line 1034. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:286` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:281` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `find_location`, `room_is_private`, `stop_fighting`, `get_trust`, `act`, `char_from_room`, `char_to_room`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_violate.if.001` | 985 | `if ( argument[0] == '\0' )` |  | pending |
| `act_wiz.do_violate.return.001` | 988 | `return;` |  | pending |
| `act_wiz.do_violate.if.002` | 991 | `if ( ( location = find_location( ch, argument ) ) == NULL )` |  | pending |
| `act_wiz.do_violate.return.002` | 994 | `return;` |  | pending |
| `act_wiz.do_violate.if.003` | 997 | `if (!room_is_private( location ))` |  | pending |
| `act_wiz.do_violate.return.003` | 1000 | `return;` |  | pending |
| `act_wiz.do_violate.if.004` | 1003 | `if ( ch->fighting != NULL )` |  | pending |
| `act_wiz.do_violate.for.001` | 1006 | `for (rch = ch->in_room->people; rch != NULL; rch = rch->next_in_room)` |  | pending |
| `act_wiz.do_violate.if.005` | 1008 | `if (get_trust(rch) >= ch->invis_level)` |  | pending |
| `act_wiz.do_violate.if.006` | 1010 | `if (ch->pcdata != NULL && ch->pcdata->bamfout[0] != '\0')` |  | pending |
| `act_wiz.do_violate.and.001` | 1010 | `&& ch->pcdata->bamfout[0] != '\0')` |  | pending |
| `act_wiz.do_violate.for.002` | 1021 | `for (rch = ch->in_room->people; rch != NULL; rch = rch->next_in_room)` |  | pending |
| `act_wiz.do_violate.if.007` | 1023 | `if (get_trust(rch) >= ch->invis_level)` |  | pending |
| `act_wiz.do_violate.if.008` | 1025 | `if (ch->pcdata != NULL && ch->pcdata->bamfin[0] != '\0')` |  | pending |
| `act_wiz.do_violate.and.002` | 1025 | `&& ch->pcdata->bamfin[0] != '\0')` |  | pending |
| `act_wiz.do_violate.return.004` | 1033 | `return;` |  | pending |

## do_stat

[Source line 1038](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1038); ends at line 1099. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:337` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:262` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `do_function`, `get_obj_world`, `get_char_world`, `find_location`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_stat.if.001` | 1047 | `if ( arg[0] == '\0')` |  | pending |
| `act_wiz.do_stat.return.001` | 1054 | `return;` |  | pending |
| `act_wiz.do_stat.if.002` | 1057 | `if (!str_cmp(arg,"room"))` |  | pending |
| `act_wiz.do_stat.return.002` | 1060 | `return;` |  | pending |
| `act_wiz.do_stat.if.003` | 1063 | `if (!str_cmp(arg,"obj"))` |  | pending |
| `act_wiz.do_stat.return.003` | 1066 | `return;` |  | pending |
| `act_wiz.do_stat.if.004` | 1069 | `if(!str_cmp(arg,"char")  \|\| !str_cmp(arg,"mob"))` |  | pending |
| `act_wiz.do_stat.or.001` | 1069 | `\|\| !str_cmp(arg,"mob"))` |  | pending |
| `act_wiz.do_stat.return.004` | 1072 | `return;` |  | pending |
| `act_wiz.do_stat.if.005` | 1078 | `if (obj != NULL)` |  | pending |
| `act_wiz.do_stat.return.005` | 1081 | `return;` |  | pending |
| `act_wiz.do_stat.if.006` | 1085 | `if (victim != NULL)` |  | pending |
| `act_wiz.do_stat.return.006` | 1088 | `return;` |  | pending |
| `act_wiz.do_stat.if.007` | 1092 | `if (location != NULL)` |  | pending |
| `act_wiz.do_stat.return.007` | 1095 | `return;` |  | pending |

## do_rstat

[Source line 1101](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1101); ends at line 1200. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_stat: `src/act_wiz.c:1059` (function_symbol_reference_candidate).
- do_stat: `src/act_wiz.c:1094` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:232` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `find_location`, `send_to_char`, `is_room_owner`, `room_is_private`, `IS_TRUSTED`, `sprintf`, `can_see`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_rstat.ternary.001` | 1111 | `? ch->in_room : find_location( ch, arg );` |  | pending |
| `act_wiz.do_rstat.if.001` | 1112 | `if ( location == NULL )` |  | pending |
| `act_wiz.do_rstat.return.001` | 1115 | `return;` |  | pending |
| `act_wiz.do_rstat.if.002` | 1118 | `if (!is_room_owner(ch,location) && ch->in_room != location      &&  room_is_private( location ) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_rstat.and.001` | 1118 | `&& ch->in_room != location` |  | pending |
| `act_wiz.do_rstat.and.002` | 1119 | `&&  room_is_private( location ) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_rstat.and.003` | 1119 | `&& !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_rstat.return.002` | 1122 | `return;` |  | pending |
| `act_wiz.do_rstat.if.003` | 1145 | `if ( location->extra_descr != NULL )` |  | pending |
| `act_wiz.do_rstat.for.001` | 1150 | `for ( ed = location->extra_descr; ed; ed = ed->next )` |  | pending |
| `act_wiz.do_rstat.if.004` | 1153 | `if ( ed->next != NULL )` |  | pending |
| `act_wiz.do_rstat.for.002` | 1160 | `for ( rch = location->people; rch; rch = rch->next_in_room )` |  | pending |
| `act_wiz.do_rstat.if.005` | 1162 | `if (can_see(ch,rch))` |  | pending |
| `act_wiz.do_rstat.for.003` | 1171 | `for ( obj = location->contents; obj; obj = obj->next_content )` |  | pending |
| `act_wiz.do_rstat.for.004` | 1179 | `for ( door = 0; door <= 5; door++ )` |  | pending |
| `act_wiz.do_rstat.if.006` | 1183 | `if ( ( pexit = location->exit[door] ) != NULL )` |  | pending |
| `act_wiz.do_rstat.ternary.002` | 1189 | `? -1 : pexit->u1.to_room->vnum),` |  | pending |
| `act_wiz.do_rstat.ternary.003` | 1194 | `? pexit->description : "(none).\n\r" );` |  | pending |
| `act_wiz.do_rstat.return.003` | 1199 | `return;` |  | pending |

## do_ostat

[Source line 1204](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1204); ends at line 1520. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_stat: `src/act_wiz.c:1065` (function_symbol_reference_candidate).
- do_stat: `src/act_wiz.c:1080` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:189` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_world`, `sprintf`, `item_name`, `wear_bit_name`, `extra_bit_name`, `get_obj_number`, `get_obj_weight`, `get_true_weight`, `can_see`, `case`, `weapon_bit_name`, `cont_bit_name`, `affect_loc_name`, `affect_bit_name`, `imm_bit_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_ostat.if.001` | 1213 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_ostat.return.001` | 1216 | `return;` |  | pending |
| `act_wiz.do_ostat.if.002` | 1219 | `if ( ( obj = get_obj_world( ch, argument ) ) == NULL )` |  | pending |
| `act_wiz.do_ostat.return.002` | 1222 | `return;` |  | pending |
| `act_wiz.do_ostat.ternary.001` | 1230 | `? "new" : "old",` |  | pending |
| `act_wiz.do_ostat.ternary.002` | 1253 | `?        0 : obj->in_room->vnum,` |  | pending |
| `act_wiz.do_ostat.ternary.003` | 1254 | `? "(none)" : obj->in_obj->short_descr,` |  | pending |
| `act_wiz.do_ostat.ternary.004` | 1255 | `? "(none)" :` |  | pending |
| `act_wiz.do_ostat.ternary.005` | 1256 | `? obj->carried_by->name` |  | pending |
| `act_wiz.do_ostat.switch.001` | 1268 | `switch ( obj->item_type )` |  | pending |
| `act_wiz.do_ostat.case.001` | 1270 | `case ITEM_SCROLL:` |  | pending |
| `act_wiz.do_ostat.case.002` | 1271 | `case ITEM_POTION:` |  | pending |
| `act_wiz.do_ostat.case.003` | 1272 | `case ITEM_PILL:` |  | pending |
| `act_wiz.do_ostat.if.003` | 1276 | `if ( obj->value[1] >= 0 && obj->value[1] < MAX_SKILL )` |  | pending |
| `act_wiz.do_ostat.and.001` | 1276 | `&& obj->value[1] < MAX_SKILL )` |  | pending |
| `act_wiz.do_ostat.if.004` | 1283 | `if ( obj->value[2] >= 0 && obj->value[2] < MAX_SKILL )` |  | pending |
| `act_wiz.do_ostat.and.002` | 1283 | `&& obj->value[2] < MAX_SKILL )` |  | pending |
| `act_wiz.do_ostat.if.005` | 1290 | `if ( obj->value[3] >= 0 && obj->value[3] < MAX_SKILL )` |  | pending |
| `act_wiz.do_ostat.and.003` | 1290 | `&& obj->value[3] < MAX_SKILL )` |  | pending |
| `act_wiz.do_ostat.if.006` | 1297 | `if (obj->value[4] >= 0 && obj->value[4] < MAX_SKILL)` |  | pending |
| `act_wiz.do_ostat.and.004` | 1297 | `&& obj->value[4] < MAX_SKILL)` |  | pending |
| `act_wiz.do_ostat.break.001` | 1305 | `break;` |  | pending |
| `act_wiz.do_ostat.case.004` | 1307 | `case ITEM_WAND:` |  | pending |
| `act_wiz.do_ostat.case.005` | 1308 | `case ITEM_STAFF:` |  | pending |
| `act_wiz.do_ostat.if.007` | 1313 | `if ( obj->value[3] >= 0 && obj->value[3] < MAX_SKILL )` |  | pending |
| `act_wiz.do_ostat.and.005` | 1313 | `&& obj->value[3] < MAX_SKILL )` |  | pending |
| `act_wiz.do_ostat.break.002` | 1321 | `break;` |  | pending |
| `act_wiz.do_ostat.case.006` | 1323 | `case ITEM_DRINK_CON:` |  | pending |
| `act_wiz.do_ostat.break.003` | 1328 | `break;` |  | pending |
| `act_wiz.do_ostat.case.007` | 1331 | `case ITEM_WEAPON:` |  | pending |
| `act_wiz.do_ostat.switch.002` | 1333 | `switch (obj->value[0])` |  | pending |
| `act_wiz.do_ostat.case.008` | 1335 | `case(WEAPON_EXOTIC):` |  | pending |
| `act_wiz.do_ostat.break.004` | 1337 | `break;` |  | pending |
| `act_wiz.do_ostat.case.009` | 1338 | `case(WEAPON_SWORD):` |  | pending |
| `act_wiz.do_ostat.break.005` | 1340 | `break;` |  | pending |
| `act_wiz.do_ostat.case.010` | 1341 | `case(WEAPON_DAGGER):` |  | pending |
| `act_wiz.do_ostat.break.006` | 1343 | `break;` |  | pending |
| `act_wiz.do_ostat.case.011` | 1344 | `case(WEAPON_SPEAR):` |  | pending |
| `act_wiz.do_ostat.break.007` | 1346 | `break;` |  | pending |
| `act_wiz.do_ostat.case.012` | 1347 | `case(WEAPON_MACE):` |  | pending |
| `act_wiz.do_ostat.break.008` | 1349 | `break;` |  | pending |
| `act_wiz.do_ostat.case.013` | 1350 | `case(WEAPON_AXE):` |  | pending |
| `act_wiz.do_ostat.break.009` | 1352 | `break;` |  | pending |
| `act_wiz.do_ostat.case.014` | 1353 | `case(WEAPON_FLAIL):` |  | pending |
| `act_wiz.do_ostat.break.010` | 1355 | `break;` |  | pending |
| `act_wiz.do_ostat.case.015` | 1356 | `case(WEAPON_WHIP):` |  | pending |
| `act_wiz.do_ostat.break.011` | 1358 | `break;` |  | pending |
| `act_wiz.do_ostat.case.016` | 1359 | `case(WEAPON_POLEARM):` |  | pending |
| `act_wiz.do_ostat.break.012` | 1361 | `break;` |  | pending |
| `act_wiz.do_ostat.default.001` | 1362 | `default:` |  | pending |
| `act_wiz.do_ostat.break.013` | 1364 | `break;` |  | pending |
| `act_wiz.do_ostat.if.008` | 1366 | `if (obj->pIndexData->new_format)` |  | pending |
| `act_wiz.do_ostat.and.006` | 1377 | `&& obj->value[3] < MAX_DAMAGE_MESSAGE) ?` |  | pending |
| `act_wiz.do_ostat.ternary.006` | 1377 | `?` |  | pending |
| `act_wiz.do_ostat.if.009` | 1381 | `if (obj->value[4])` |  | pending |
| `act_wiz.do_ostat.break.014` | 1387 | `break;` |  | pending |
| `act_wiz.do_ostat.case.017` | 1389 | `case ITEM_ARMOR:` |  | pending |
| `act_wiz.do_ostat.break.015` | 1394 | `break;` |  | pending |
| `act_wiz.do_ostat.case.018` | 1396 | `case ITEM_CONTAINER:` |  | pending |
| `act_wiz.do_ostat.if.010` | 1400 | `if (obj->value[4] != 100)` |  | pending |
| `act_wiz.do_ostat.break.016` | 1406 | `break;` |  | pending |
| `act_wiz.do_ostat.if.011` | 1410 | `if ( obj->extra_descr != NULL \|\| obj->pIndexData->extra_descr != NULL )` |  | pending |
| `act_wiz.do_ostat.or.001` | 1410 | `\|\| obj->pIndexData->extra_descr != NULL )` |  | pending |
| `act_wiz.do_ostat.for.001` | 1416 | `for ( ed = obj->extra_descr; ed != NULL; ed = ed->next )` |  | pending |
| `act_wiz.do_ostat.if.012` | 1419 | `if ( ed->next != NULL )` |  | pending |
| `act_wiz.do_ostat.for.002` | 1423 | `for ( ed = obj->pIndexData->extra_descr; ed != NULL; ed = ed->next )` |  | pending |
| `act_wiz.do_ostat.if.013` | 1426 | `if ( ed->next != NULL )` |  | pending |
| `act_wiz.do_ostat.for.003` | 1433 | `for ( paf = obj->affected; paf != NULL; paf = paf->next )` |  | pending |
| `act_wiz.do_ostat.if.014` | 1438 | `if ( paf->duration > -1)` |  | pending |
| `act_wiz.do_ostat.if.015` | 1443 | `if (paf->bitvector)` |  | pending |
| `act_wiz.do_ostat.switch.003` | 1445 | `switch(paf->where)` |  | pending |
| `act_wiz.do_ostat.case.019` | 1447 | `case TO_AFFECTS:` |  | pending |
| `act_wiz.do_ostat.break.017` | 1450 | `break;` |  | pending |
| `act_wiz.do_ostat.case.020` | 1451 | `case TO_WEAPON:` |  | pending |
| `act_wiz.do_ostat.break.018` | 1454 | `break;` |  | pending |
| `act_wiz.do_ostat.case.021` | 1455 | `case TO_OBJECT:` |  | pending |
| `act_wiz.do_ostat.break.019` | 1458 | `break;` |  | pending |
| `act_wiz.do_ostat.case.022` | 1459 | `case TO_IMMUNE:` |  | pending |
| `act_wiz.do_ostat.break.020` | 1462 | `break;` |  | pending |
| `act_wiz.do_ostat.case.023` | 1463 | `case TO_RESIST:` |  | pending |
| `act_wiz.do_ostat.break.021` | 1466 | `break;` |  | pending |
| `act_wiz.do_ostat.case.024` | 1467 | `case TO_VULN:` |  | pending |
| `act_wiz.do_ostat.break.022` | 1470 | `break;` |  | pending |
| `act_wiz.do_ostat.default.002` | 1471 | `default:` |  | pending |
| `act_wiz.do_ostat.break.023` | 1474 | `break;` |  | pending |
| `act_wiz.do_ostat.if.016` | 1480 | `if (!obj->enchanted)` |  | pending |
| `act_wiz.do_ostat.for.004` | 1481 | `for ( paf = obj->pIndexData->affected; paf != NULL; paf = paf->next )` |  | pending |
| `act_wiz.do_ostat.if.017` | 1486 | `if (paf->bitvector)` |  | pending |
| `act_wiz.do_ostat.switch.004` | 1488 | `switch(paf->where)` |  | pending |
| `act_wiz.do_ostat.case.025` | 1490 | `case TO_AFFECTS:` |  | pending |
| `act_wiz.do_ostat.break.024` | 1493 | `break;` |  | pending |
| `act_wiz.do_ostat.case.026` | 1494 | `case TO_OBJECT:` |  | pending |
| `act_wiz.do_ostat.break.025` | 1497 | `break;` |  | pending |
| `act_wiz.do_ostat.case.027` | 1498 | `case TO_IMMUNE:` |  | pending |
| `act_wiz.do_ostat.break.026` | 1501 | `break;` |  | pending |
| `act_wiz.do_ostat.case.028` | 1502 | `case TO_RESIST:` |  | pending |
| `act_wiz.do_ostat.break.027` | 1505 | `break;` |  | pending |
| `act_wiz.do_ostat.case.029` | 1506 | `case TO_VULN:` |  | pending |
| `act_wiz.do_ostat.break.028` | 1509 | `break;` |  | pending |
| `act_wiz.do_ostat.default.003` | 1510 | `default:` |  | pending |
| `act_wiz.do_ostat.break.029` | 1513 | `break;` |  | pending |
| `act_wiz.do_ostat.return.003` | 1519 | `return;` |  | pending |

## do_mstat

[Source line 1524](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1524); ends at line 1722. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_stat: `src/act_wiz.c:1071` (function_symbol_reference_candidate).
- do_stat: `src/act_wiz.c:1087` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:167` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `sprintf`, `IS_NPC`, `get_curr_stat`, `GET_AC`, `GET_HITROLL`, `GET_DAMROLL`, `get_carry_weight`, `get_age`, `act_bit_name`, `comm_bit_name`, `off_bit_name`, `imm_bit_name`, `form_bit_name`, `part_bit_name`, `affect_bit_name`, `spec_name`, `affect_loc_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_mstat.if.001` | 1533 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_mstat.return.001` | 1536 | `return;` |  | pending |
| `act_wiz.do_mstat.if.002` | 1539 | `if ( ( victim = get_char_world( ch, argument ) ) == NULL )` |  | pending |
| `act_wiz.do_mstat.return.002` | 1542 | `return;` |  | pending |
| `act_wiz.do_mstat.ternary.001` | 1551 | `? victim->pIndexData->vnum : 0,` |  | pending |
| `act_wiz.do_mstat.ternary.002` | 1552 | `? victim->pIndexData->new_format ? "new" : "old" : "pc",` |  | pending |
| `act_wiz.do_mstat.ternary.003` | 1552 | `? "new" : "old" : "pc",` |  | pending |
| `act_wiz.do_mstat.ternary.004` | 1554 | `? victim->group : 0, sex_table[victim->sex].name,` |  | pending |
| `act_wiz.do_mstat.ternary.005` | 1555 | `?        0 : victim->in_room->vnum` |  | pending |
| `act_wiz.do_mstat.if.003` | 1559 | `if (IS_NPC(victim))` |  | pending |
| `act_wiz.do_mstat.ternary.006` | 1584 | `? 0 : victim->practice );` |  | pending |
| `act_wiz.do_mstat.ternary.007` | 1590 | `? "mobile" : class_table[victim->class].name,` |  | pending |
| `act_wiz.do_mstat.if.004` | 1607 | `if (IS_NPC(victim) && victim->pIndexData->new_format)` |  | pending |
| `act_wiz.do_mstat.and.001` | 1607 | `&& victim->pIndexData->new_format)` |  | pending |
| `act_wiz.do_mstat.ternary.008` | 1615 | `? victim->fighting->name : "(none)" );` |  | pending |
| `act_wiz.do_mstat.if.005` | 1618 | `if ( !IS_NPC(victim) )` |  | pending |
| `act_wiz.do_mstat.if.006` | 1634 | `if (!IS_NPC(victim))` |  | pending |
| `act_wiz.do_mstat.if.007` | 1648 | `if (victim->comm)` |  | pending |
| `act_wiz.do_mstat.if.008` | 1654 | `if (IS_NPC(victim) && victim->off_flags)` |  | pending |
| `act_wiz.do_mstat.and.002` | 1654 | `&& victim->off_flags)` |  | pending |
| `act_wiz.do_mstat.if.009` | 1660 | `if (victim->imm_flags)` |  | pending |
| `act_wiz.do_mstat.if.010` | 1666 | `if (victim->res_flags)` |  | pending |
| `act_wiz.do_mstat.if.011` | 1672 | `if (victim->vuln_flags)` |  | pending |
| `act_wiz.do_mstat.if.012` | 1682 | `if (victim->affected_by)` |  | pending |
| `act_wiz.do_mstat.ternary.009` | 1690 | `? victim->master->name   : "(none)",` |  | pending |
| `act_wiz.do_mstat.ternary.010` | 1691 | `? victim->leader->name   : "(none)",` |  | pending |
| `act_wiz.do_mstat.ternary.011` | 1692 | `? victim->pet->name	     : "(none)");` |  | pending |
| `act_wiz.do_mstat.ternary.012` | 1697 | `? victim->long_descr : "(none)\n\r" );` |  | pending |
| `act_wiz.do_mstat.if.013` | 1700 | `if ( IS_NPC(victim) && victim->spec_fun != 0 )` |  | pending |
| `act_wiz.do_mstat.and.003` | 1700 | `&& victim->spec_fun != 0 )` |  | pending |
| `act_wiz.do_mstat.for.001` | 1707 | `for ( paf = victim->affected; paf != NULL; paf = paf->next )` |  | pending |
| `act_wiz.do_mstat.return.003` | 1721 | `return;` |  | pending |

## do_vnum

[Source line 1726](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1726); ends at line 1762. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:341` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:282` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_vnum.if.001` | 1733 | `if (arg[0] == '\0')` |  | pending |
| `act_wiz.do_vnum.return.001` | 1739 | `return;` |  | pending |
| `act_wiz.do_vnum.if.002` | 1742 | `if (!str_cmp(arg,"obj"))` |  | pending |
| `act_wiz.do_vnum.return.002` | 1745 | `return;` |  | pending |
| `act_wiz.do_vnum.if.003` | 1748 | `if (!str_cmp(arg,"mob") \|\| !str_cmp(arg,"char"))` |  | pending |
| `act_wiz.do_vnum.or.001` | 1748 | `\|\| !str_cmp(arg,"char"))` |  | pending |
| `act_wiz.do_vnum.return.003` | 1751 | `return;` |  | pending |
| `act_wiz.do_vnum.if.004` | 1754 | `if (!str_cmp(arg,"skill") \|\| !str_cmp(arg,"spell"))` |  | pending |
| `act_wiz.do_vnum.or.002` | 1754 | `\|\| !str_cmp(arg,"spell"))` |  | pending |
| `act_wiz.do_vnum.return.004` | 1757 | `return;` |  | pending |

## do_mfind

[Source line 1765](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1765); ends at line 1812. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_vnum: `src/act_wiz.c:1750` (function_symbol_reference_candidate).
- do_vnum: `src/act_wiz.c:1760` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:164` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_mob_index`, `is_name`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_mfind.if.001` | 1777 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_mfind.return.001` | 1780 | `return;` |  | pending |
| `act_wiz.do_mfind.for.001` | 1793 | `for ( vnum = 0; nMatch < top_mob_index; vnum++ )` |  | pending |
| `act_wiz.do_mfind.if.002` | 1795 | `if ( ( pMobIndex = get_mob_index( vnum ) ) != NULL )` |  | pending |
| `act_wiz.do_mfind.if.003` | 1798 | `if ( fAll \|\| is_name( argument, pMobIndex->player_name ) )` |  | pending |
| `act_wiz.do_mfind.or.001` | 1798 | `\|\| is_name( argument, pMobIndex->player_name ) )` |  | pending |
| `act_wiz.do_mfind.if.004` | 1808 | `if ( !found )` |  | pending |
| `act_wiz.do_mfind.return.002` | 1811 | `return;` |  | pending |

## do_ofind

[Source line 1816](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1816); ends at line 1863. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_vnum: `src/act_wiz.c:1744` (function_symbol_reference_candidate).
- do_vnum: `src/act_wiz.c:1761` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:184` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_index`, `is_name`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_ofind.if.001` | 1828 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_ofind.return.001` | 1831 | `return;` |  | pending |
| `act_wiz.do_ofind.for.001` | 1844 | `for ( vnum = 0; nMatch < top_obj_index; vnum++ )` |  | pending |
| `act_wiz.do_ofind.if.002` | 1846 | `if ( ( pObjIndex = get_obj_index( vnum ) ) != NULL )` |  | pending |
| `act_wiz.do_ofind.if.003` | 1849 | `if ( fAll \|\| is_name( argument, pObjIndex->name ) )` |  | pending |
| `act_wiz.do_ofind.or.001` | 1849 | `\|\| is_name( argument, pObjIndex->name ) )` |  | pending |
| `act_wiz.do_ofind.if.004` | 1859 | `if ( !found )` |  | pending |
| `act_wiz.do_ofind.return.002` | 1862 | `return;` |  | pending |

## do_owhere

[Source line 1866](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1866); ends at line 1924. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:331` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:191` (declaration_or_dispatch_reference).

Dependencies: `new_buf`, `send_to_char`, `can_see_obj`, `is_name`, `can_see`, `sprintf`, `PERS`, `can_see_room`, `UPPER`, `add_buf`, `page_to_char`, `buf_string`, `free_buf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_owhere.if.001` | 1881 | `if (argument[0] == '\0')` |  | pending |
| `act_wiz.do_owhere.return.001` | 1884 | `return;` |  | pending |
| `act_wiz.do_owhere.for.001` | 1887 | `for ( obj = object_list; obj != NULL; obj = obj->next )` |  | pending |
| `act_wiz.do_owhere.if.002` | 1889 | `if ( !can_see_obj( ch, obj ) \|\| !is_name( argument, obj->name )         \|\|   ch->level < obj->level)` |  | pending |
| `act_wiz.do_owhere.or.001` | 1889 | `\|\| !is_name( argument, obj->name )` |  | pending |
| `act_wiz.do_owhere.or.002` | 1890 | `\|\|   ch->level < obj->level)` |  | pending |
| `act_wiz.do_owhere.continue.001` | 1891 | `continue;` |  | pending |
| `act_wiz.do_owhere.for.002` | 1896 | `for ( in_obj = obj; in_obj->in_obj != NULL; in_obj = in_obj->in_obj )` |  | pending |
| `act_wiz.do_owhere.if.003` | 1899 | `if ( in_obj->carried_by != NULL && can_see(ch,in_obj->carried_by) 	&&   in_obj->carried_by->in_room != NULL)` |  | pending |
| `act_wiz.do_owhere.and.001` | 1899 | `&& can_see(ch,in_obj->carried_by)` |  | pending |
| `act_wiz.do_owhere.and.002` | 1900 | `&&   in_obj->carried_by->in_room != NULL)` |  | pending |
| `act_wiz.do_owhere.if.004` | 1904 | `if (in_obj->in_room != NULL && can_see_room(ch,in_obj->in_room))` |  | pending |
| `act_wiz.do_owhere.and.003` | 1904 | `&& can_see_room(ch,in_obj->in_room))` |  | pending |
| `act_wiz.do_owhere.if.005` | 1914 | `if (number >= max_found)` |  | pending |
| `act_wiz.do_owhere.break.001` | 1915 | `break;` |  | pending |
| `act_wiz.do_owhere.if.006` | 1918 | `if ( !found )` |  | pending |

## do_mwhere

[Source line 1927](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1927); ends at line 1993. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:330` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:168` (declaration_or_dispatch_reference).

Dependencies: `new_buf`, `can_see`, `can_see_room`, `sprintf`, `add_buf`, `page_to_char`, `buf_string`, `free_buf`, `is_name`, `IS_NPC`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_mwhere.if.001` | 1935 | `if ( argument[0] == '\0' )` |  | pending |
| `act_wiz.do_mwhere.for.001` | 1942 | `for (d = descriptor_list; d != NULL; d = d->next)` |  | pending |
| `act_wiz.do_mwhere.if.002` | 1944 | `if (d->character != NULL && d->connected == CON_PLAYING 	    &&  d->character->in_room != NULL && can_see(ch,d->character) 	    &&  can_see_room(ch,d->character->in_room))` |  | pending |
| `act_wiz.do_mwhere.and.001` | 1944 | `&& d->connected == CON_PLAYING` |  | pending |
| `act_wiz.do_mwhere.and.002` | 1945 | `&&  d->character->in_room != NULL && can_see(ch,d->character)` |  | pending |
| `act_wiz.do_mwhere.and.003` | 1945 | `&& can_see(ch,d->character)` |  | pending |
| `act_wiz.do_mwhere.and.004` | 1946 | `&&  can_see_room(ch,d->character->in_room))` |  | pending |
| `act_wiz.do_mwhere.if.003` | 1950 | `if (d->original != NULL)` |  | pending |
| `act_wiz.do_mwhere.return.001` | 1964 | `return;` |  | pending |
| `act_wiz.do_mwhere.for.002` | 1969 | `for ( victim = char_list; victim != NULL; victim = victim->next )` |  | pending |
| `act_wiz.do_mwhere.if.004` | 1971 | `if ( victim->in_room != NULL 	&&   is_name( argument, victim->name ) )` |  | pending |
| `act_wiz.do_mwhere.and.005` | 1972 | `&&   is_name( argument, victim->name ) )` |  | pending |
| `act_wiz.do_mwhere.ternary.001` | 1977 | `? victim->pIndexData->vnum : 0,` |  | pending |
| `act_wiz.do_mwhere.ternary.002` | 1978 | `? victim->short_descr : victim->name,` |  | pending |
| `act_wiz.do_mwhere.if.005` | 1985 | `if ( !found )` |  | pending |
| `act_wiz.do_mwhere.return.002` | 1992 | `return;` |  | pending |

## do_reboo

[Source line 1997](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1997); ends at line 2001. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:296` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:217` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_reboo.return.001` | 2000 | `return;` |  | pending |

## do_reboot

[Source line 2005](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2005); ends at line 2029. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:297` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:218` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `do_function`, `save_char_obj`, `close_socket`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_reboot.if.001` | 2012 | `if (ch->invis_level < LEVEL_HERO)` |  | pending |
| `act_wiz.do_reboot.for.001` | 2019 | `for ( d = descriptor_list; d != NULL; d = d_next )` |  | pending |
| `act_wiz.do_reboot.ternary.001` | 2022 | `? d->original : d->character;` |  | pending |
| `act_wiz.do_reboot.if.002` | 2023 | `if (vch != NULL)` |  | pending |
| `act_wiz.do_reboot.return.001` | 2028 | `return;` |  | pending |

## do_shutdow

[Source line 2031](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2031); ends at line 2035. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:299` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:244` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_shutdow.return.001` | 2034 | `return;` |  | pending |

## do_shutdown

[Source line 2037](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2037); ends at line 2062. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:300` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:245` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `append_file`, `strcat`, `do_function`, `save_char_obj`, `close_socket`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_shutdown.if.001` | 2044 | `if (ch->invis_level < LEVEL_HERO)` |  | pending |
| `act_wiz.do_shutdown.if.002` | 2048 | `if (ch->invis_level < LEVEL_HERO)` |  | pending |
| `act_wiz.do_shutdown.for.001` | 2053 | `for ( d = descriptor_list; d != NULL; d = d_next)` |  | pending |
| `act_wiz.do_shutdown.ternary.001` | 2056 | `? d->original : d->character;` |  | pending |
| `act_wiz.do_shutdown.if.003` | 2057 | `if (vch != NULL)` |  | pending |
| `act_wiz.do_shutdown.return.001` | 2061 | `return;` |  | pending |

## do_protect

[Source line 2064](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2064); ends at line 2092. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:295` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:207` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_char_world`, `IS_SET`, `act_new`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_protect.if.001` | 2068 | `if (argument[0] == '\0')` |  | pending |
| `act_wiz.do_protect.return.001` | 2071 | `return;` |  | pending |
| `act_wiz.do_protect.if.002` | 2074 | `if ((victim = get_char_world(ch,argument)) == NULL)` |  | pending |
| `act_wiz.do_protect.return.002` | 2077 | `return;` |  | pending |
| `act_wiz.do_protect.if.003` | 2080 | `if (IS_SET(victim->comm,COMM_SNOOP_PROOF))` |  | pending |

## do_snoop

[Source line 2096](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2096); ends at line 2174. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:336` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:254` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `wiznet`, `get_trust`, `is_room_owner`, `room_is_private`, `IS_TRUSTED`, `IS_SET`, `sprintf`, `IS_NPC`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_snoop.if.001` | 2105 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_snoop.return.001` | 2108 | `return;` |  | pending |
| `act_wiz.do_snoop.if.002` | 2111 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_snoop.return.002` | 2114 | `return;` |  | pending |
| `act_wiz.do_snoop.if.003` | 2117 | `if ( victim->desc == NULL )` |  | pending |
| `act_wiz.do_snoop.return.003` | 2120 | `return;` |  | pending |
| `act_wiz.do_snoop.if.004` | 2123 | `if ( victim == ch )` |  | pending |
| `act_wiz.do_snoop.for.001` | 2128 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_wiz.do_snoop.if.005` | 2130 | `if ( d->snoop_by == ch->desc )` |  | pending |
| `act_wiz.do_snoop.return.004` | 2133 | `return;` |  | pending |
| `act_wiz.do_snoop.if.006` | 2136 | `if ( victim->desc->snoop_by != NULL )` |  | pending |
| `act_wiz.do_snoop.return.005` | 2139 | `return;` |  | pending |
| `act_wiz.do_snoop.if.007` | 2142 | `if (!is_room_owner(ch,victim->in_room) && ch->in_room != victim->in_room      &&  room_is_private(victim->in_room) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_snoop.and.001` | 2142 | `&& ch->in_room != victim->in_room` |  | pending |
| `act_wiz.do_snoop.and.002` | 2143 | `&&  room_is_private(victim->in_room) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_snoop.and.003` | 2143 | `&& !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_snoop.return.006` | 2146 | `return;` |  | pending |
| `act_wiz.do_snoop.if.008` | 2149 | `if ( get_trust( victim ) >= get_trust( ch )      \|\|   IS_SET(victim->comm,COMM_SNOOP_PROOF))` |  | pending |
| `act_wiz.do_snoop.or.001` | 2150 | `\|\|   IS_SET(victim->comm,COMM_SNOOP_PROOF))` |  | pending |
| `act_wiz.do_snoop.return.007` | 2153 | `return;` |  | pending |
| `act_wiz.do_snoop.if.009` | 2156 | `if ( ch->desc != NULL )` |  | pending |
| `act_wiz.do_snoop.for.002` | 2158 | `for ( d = ch->desc->snoop_by; d != NULL; d = d->snoop_by )` |  | pending |
| `act_wiz.do_snoop.if.010` | 2160 | `if ( d->character == victim \|\| d->original == victim )` |  | pending |
| `act_wiz.do_snoop.or.002` | 2160 | `\|\| d->original == victim )` |  | pending |
| `act_wiz.do_snoop.return.008` | 2163 | `return;` |  | pending |
| `act_wiz.do_snoop.ternary.001` | 2170 | `? victim->short_descr : victim->name));` |  | pending |
| `act_wiz.do_snoop.return.009` | 2173 | `return;` |  | pending |

## do_switch

[Source line 2178](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2178); ends at line 2245. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:339` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:266` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `IS_NPC`, `is_room_owner`, `room_is_private`, `IS_TRUSTED`, `sprintf`, `wiznet`, `get_trust`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_switch.if.001` | 2185 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_switch.return.001` | 2188 | `return;` |  | pending |
| `act_wiz.do_switch.if.002` | 2191 | `if ( ch->desc == NULL )` |  | pending |
| `act_wiz.do_switch.return.002` | 2192 | `return;` |  | pending |
| `act_wiz.do_switch.if.003` | 2194 | `if ( ch->desc->original != NULL )` |  | pending |
| `act_wiz.do_switch.return.003` | 2197 | `return;` |  | pending |
| `act_wiz.do_switch.if.004` | 2200 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_switch.return.004` | 2203 | `return;` |  | pending |
| `act_wiz.do_switch.if.005` | 2206 | `if ( victim == ch )` |  | pending |
| `act_wiz.do_switch.return.005` | 2209 | `return;` |  | pending |
| `act_wiz.do_switch.if.006` | 2212 | `if (!IS_NPC(victim))` |  | pending |
| `act_wiz.do_switch.return.006` | 2215 | `return;` |  | pending |
| `act_wiz.do_switch.if.007` | 2218 | `if (!is_room_owner(ch,victim->in_room) && ch->in_room != victim->in_room      &&  room_is_private(victim->in_room) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_switch.and.001` | 2218 | `&& ch->in_room != victim->in_room` |  | pending |
| `act_wiz.do_switch.and.002` | 2219 | `&&  room_is_private(victim->in_room) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_switch.and.003` | 2219 | `&& !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_switch.return.007` | 2222 | `return;` |  | pending |
| `act_wiz.do_switch.if.008` | 2225 | `if ( victim->desc != NULL )` |  | pending |
| `act_wiz.do_switch.return.008` | 2228 | `return;` |  | pending |
| `act_wiz.do_switch.if.009` | 2239 | `if (ch->prompt != NULL)` |  | pending |
| `act_wiz.do_switch.return.009` | 2244 | `return;` |  | pending |

## do_return

[Source line 2249](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2249); ends at line 2278. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- extract_char: `src/handler.c:1969` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:335` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:230` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `free_string`, `sprintf`, `wiznet`, `get_trust`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_return.if.001` | 2253 | `if ( ch->desc == NULL )` |  | pending |
| `act_wiz.do_return.return.001` | 2254 | `return;` |  | pending |
| `act_wiz.do_return.if.002` | 2256 | `if ( ch->desc->original == NULL )` |  | pending |
| `act_wiz.do_return.return.002` | 2259 | `return;` |  | pending |
| `act_wiz.do_return.if.003` | 2265 | `if (ch->prompt != NULL)` |  | pending |
| `act_wiz.do_return.return.003` | 2277 | `return;` |  | pending |

## obj_check

[Source line 2281](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2281); ends at line 2291. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- recursive_clone: `src/act_wiz.c:2301` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2363` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2411` (lexical_call_candidate).

Dependencies: `IS_TRUSTED`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.obj_check.if.001` | 2283 | `if (IS_TRUSTED(ch,GOD) 	\|\| (IS_TRUSTED(ch,IMMORTAL) && obj->level <= 20 && obj->cost <= 1000) 	\|\| (IS_TRUSTED(ch,DEMI)	    && obj->level <= 10 && obj->cost <= 500) 	\|\| (IS_TRUSTED(ch,ANGEL)    && obj->level <=  5 && obj->cost <= 250) 	\|\| (IS_TRUSTED(ch,AVATAR)   && obj->level ==  0 && obj->cost <= 100))` |  | pending |
| `act_wiz.obj_check.or.001` | 2284 | `\|\| (IS_TRUSTED(ch,IMMORTAL) && obj->level <= 20 && obj->cost <= 1000)` |  | pending |
| `act_wiz.obj_check.and.001` | 2284 | `&& obj->level <= 20 && obj->cost <= 1000)` |  | pending |
| `act_wiz.obj_check.and.002` | 2284 | `&& obj->cost <= 1000)` |  | pending |
| `act_wiz.obj_check.or.002` | 2285 | `\|\| (IS_TRUSTED(ch,DEMI)	    && obj->level <= 10 && obj->cost <= 500)` |  | pending |
| `act_wiz.obj_check.and.003` | 2285 | `&& obj->level <= 10 && obj->cost <= 500)` |  | pending |
| `act_wiz.obj_check.and.004` | 2285 | `&& obj->cost <= 500)` |  | pending |
| `act_wiz.obj_check.or.003` | 2286 | `\|\| (IS_TRUSTED(ch,ANGEL)    && obj->level <=  5 && obj->cost <= 250)` |  | pending |
| `act_wiz.obj_check.and.005` | 2286 | `&& obj->level <=  5 && obj->cost <= 250)` |  | pending |
| `act_wiz.obj_check.and.006` | 2286 | `&& obj->cost <= 250)` |  | pending |
| `act_wiz.obj_check.or.004` | 2287 | `\|\| (IS_TRUSTED(ch,AVATAR)   && obj->level ==  0 && obj->cost <= 100))` |  | pending |
| `act_wiz.obj_check.and.007` | 2287 | `&& obj->level ==  0 && obj->cost <= 100))` |  | pending |
| `act_wiz.obj_check.and.008` | 2287 | `&& obj->cost <= 100))` |  | pending |
| `act_wiz.obj_check.return.001` | 2288 | `return TRUE;` |  | pending |
| `act_wiz.obj_check.return.002` | 2290 | `return FALSE;` |  | pending |

## recursive_clone

[Source line 2294](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2294); ends at line 2309. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- recursive_clone: `src/act_wiz.c:2306` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2376` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2415` (lexical_call_candidate).

Dependencies: `obj_check`, `create_object`, `clone_object`, `obj_to_obj`, `recursive_clone`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.recursive_clone.for.001` | 2299 | `for (c_obj = obj->contains; c_obj != NULL; c_obj = c_obj->next_content)` |  | pending |
| `act_wiz.recursive_clone.if.001` | 2301 | `if (obj_check(ch,c_obj))` |  | pending |

## do_clone

[Source line 2312](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2312); ends at line 2427. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:344` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:99` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_prefix`, `get_obj_here`, `get_char_room`, `obj_check`, `create_object`, `clone_object`, `obj_to_char`, `obj_to_room`, `recursive_clone`, `act`, `wiznet`, `get_trust`, `IS_NPC`, `IS_TRUSTED`, `create_mobile`, `clone_mobile`, `char_to_room`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_clone.if.001` | 2321 | `if (arg[0] == '\0')` |  | pending |
| `act_wiz.do_clone.return.001` | 2324 | `return;` |  | pending |
| `act_wiz.do_clone.if.002` | 2327 | `if (!str_prefix(arg,"object"))` |  | pending |
| `act_wiz.do_clone.if.003` | 2331 | `if (obj == NULL)` |  | pending |
| `act_wiz.do_clone.return.002` | 2334 | `return;` |  | pending |
| `act_wiz.do_clone.if.004` | 2337 | `if (!str_prefix(arg,"mobile") \|\| !str_prefix(arg,"character"))` |  | pending |
| `act_wiz.do_clone.or.001` | 2337 | `\|\| !str_prefix(arg,"character"))` |  | pending |
| `act_wiz.do_clone.if.005` | 2341 | `if (mob == NULL)` |  | pending |
| `act_wiz.do_clone.return.003` | 2344 | `return;` |  | pending |
| `act_wiz.do_clone.if.006` | 2351 | `if (mob == NULL && obj == NULL)` |  | pending |
| `act_wiz.do_clone.and.001` | 2351 | `&& obj == NULL)` |  | pending |
| `act_wiz.do_clone.return.004` | 2354 | `return;` |  | pending |
| `act_wiz.do_clone.if.007` | 2359 | `if (obj != NULL)` |  | pending |
| `act_wiz.do_clone.if.008` | 2363 | `if (!obj_check(ch,obj))` |  | pending |
| `act_wiz.do_clone.return.005` | 2367 | `return;` |  | pending |
| `act_wiz.do_clone.if.009` | 2372 | `if (obj->carried_by != NULL)` |  | pending |
| `act_wiz.do_clone.return.006` | 2381 | `return;` |  | pending |
| `act_wiz.do_clone.if.010` | 2383 | `if (mob != NULL)` |  | pending |
| `act_wiz.do_clone.if.011` | 2389 | `if (!IS_NPC(mob))` |  | pending |
| `act_wiz.do_clone.return.007` | 2392 | `return;` |  | pending |
| `act_wiz.do_clone.if.012` | 2395 | `if ((mob->level > 20 && !IS_TRUSTED(ch,GOD)) 	\|\|  (mob->level > 10 && !IS_TRUSTED(ch,IMMORTAL)) 	\|\|  (mob->level >  5 && !IS_TRUSTED(ch,DEMI)) 	\|\|  (mob->level >  0 && !IS_TRUSTED(ch,ANGEL)) 	\|\|  !IS_TRUSTED(ch,AVATAR))` |  | pending |
| `act_wiz.do_clone.and.002` | 2395 | `&& !IS_TRUSTED(ch,GOD))` |  | pending |
| `act_wiz.do_clone.or.002` | 2396 | `\|\|  (mob->level > 10 && !IS_TRUSTED(ch,IMMORTAL))` |  | pending |
| `act_wiz.do_clone.and.003` | 2396 | `&& !IS_TRUSTED(ch,IMMORTAL))` |  | pending |
| `act_wiz.do_clone.or.003` | 2397 | `\|\|  (mob->level >  5 && !IS_TRUSTED(ch,DEMI))` |  | pending |
| `act_wiz.do_clone.and.004` | 2397 | `&& !IS_TRUSTED(ch,DEMI))` |  | pending |
| `act_wiz.do_clone.or.004` | 2398 | `\|\|  (mob->level >  0 && !IS_TRUSTED(ch,ANGEL))` |  | pending |
| `act_wiz.do_clone.and.005` | 2398 | `&& !IS_TRUSTED(ch,ANGEL))` |  | pending |
| `act_wiz.do_clone.or.005` | 2399 | `\|\|  !IS_TRUSTED(ch,AVATAR))` |  | pending |
| `act_wiz.do_clone.return.008` | 2403 | `return;` |  | pending |
| `act_wiz.do_clone.for.001` | 2409 | `for (obj = mob->carrying; obj != NULL; obj = obj->next_content)` |  | pending |
| `act_wiz.do_clone.if.013` | 2411 | `if (obj_check(ch,obj))` |  | pending |
| `act_wiz.do_clone.return.009` | 2425 | `return;` |  | pending |

## do_load

[Source line 2431](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2431); ends at line 2458. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_load: `src/act_wiz.c:2457` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:305` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:159` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_load.if.001` | 2437 | `if (arg[0] == '\0')` |  | pending |
| `act_wiz.do_load.return.001` | 2442 | `return;` |  | pending |
| `act_wiz.do_load.if.002` | 2445 | `if (!str_cmp(arg,"mob") \|\| !str_cmp(arg,"char"))` |  | pending |
| `act_wiz.do_load.or.001` | 2445 | `\|\| !str_cmp(arg,"char"))` |  | pending |
| `act_wiz.do_load.return.002` | 2448 | `return;` |  | pending |
| `act_wiz.do_load.if.003` | 2451 | `if (!str_cmp(arg,"obj"))` |  | pending |
| `act_wiz.do_load.return.003` | 2454 | `return;` |  | pending |

## do_mload

[Source line 2461](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2461); ends at line 2489. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_load: `src/act_wiz.c:2447` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:165` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `is_number`, `send_to_char`, `get_mob_index`, `atoi`, `create_mobile`, `char_to_room`, `act`, `sprintf`, `wiznet`, `get_trust`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_mload.if.001` | 2470 | `if ( arg[0] == '\0' \|\| !is_number(arg) )` |  | pending |
| `act_wiz.do_mload.or.001` | 2470 | `\|\| !is_number(arg) )` |  | pending |
| `act_wiz.do_mload.return.001` | 2473 | `return;` |  | pending |
| `act_wiz.do_mload.if.002` | 2476 | `if ( ( pMobIndex = get_mob_index( atoi( arg ) ) ) == NULL )` |  | pending |
| `act_wiz.do_mload.return.002` | 2479 | `return;` |  | pending |
| `act_wiz.do_mload.return.003` | 2488 | `return;` |  | pending |

## do_oload

[Source line 2493](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2493); ends at line 2541. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_load: `src/act_wiz.c:2453` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:185` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `is_number`, `send_to_char`, `get_trust`, `atoi`, `get_obj_index`, `create_object`, `CAN_WEAR`, `obj_to_char`, `obj_to_room`, `act`, `wiznet`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_oload.if.001` | 2503 | `if ( arg1[0] == '\0' \|\| !is_number(arg1))` |  | pending |
| `act_wiz.do_oload.or.001` | 2503 | `\|\| !is_number(arg1))` |  | pending |
| `act_wiz.do_oload.return.001` | 2506 | `return;` |  | pending |
| `act_wiz.do_oload.if.002` | 2511 | `if ( arg2[0] != '\0')` |  | pending |
| `act_wiz.do_oload.if.003` | 2513 | `if (!is_number(arg2))` |  | pending |
| `act_wiz.do_oload.return.002` | 2516 | `return;` |  | pending |
| `act_wiz.do_oload.if.004` | 2519 | `if (level < 0 \|\| level > get_trust(ch))` |  | pending |
| `act_wiz.do_oload.or.002` | 2519 | `\|\| level > get_trust(ch))` |  | pending |
| `act_wiz.do_oload.return.003` | 2522 | `return;` |  | pending |
| `act_wiz.do_oload.if.005` | 2526 | `if ( ( pObjIndex = get_obj_index( atoi( arg1 ) ) ) == NULL )` |  | pending |
| `act_wiz.do_oload.return.004` | 2529 | `return;` |  | pending |
| `act_wiz.do_oload.if.006` | 2533 | `if ( CAN_WEAR(obj, ITEM_TAKE) )` |  | pending |
| `act_wiz.do_oload.return.005` | 2540 | `return;` |  | pending |

## do_purge

[Source line 2545](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2545); ends at line 2619. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:313` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:208` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `IS_NPC`, `IS_SET`, `extract_char`, `IS_OBJ_STAT`, `extract_obj`, `act`, `send_to_char`, `get_char_world`, `get_trust`, `sprintf`, `save_char_obj`, `close_socket`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_purge.if.001` | 2555 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_purge.for.001` | 2561 | `for ( victim = ch->in_room->people; victim != NULL; victim = vnext )` |  | pending |
| `act_wiz.do_purge.if.002` | 2564 | `if ( IS_NPC(victim) && !IS_SET(victim->act,ACT_NOPURGE)  	    &&   victim != ch /* safety precaution */ )` |  | pending |
| `act_wiz.do_purge.and.001` | 2564 | `&& !IS_SET(victim->act,ACT_NOPURGE)` |  | pending |
| `act_wiz.do_purge.and.002` | 2565 | `&&   victim != ch /* safety precaution */ )` |  | pending |
| `act_wiz.do_purge.for.002` | 2569 | `for ( obj = ch->in_room->contents; obj != NULL; obj = obj_next )` |  | pending |
| `act_wiz.do_purge.if.003` | 2572 | `if (!IS_OBJ_STAT(obj,ITEM_NOPURGE))` |  | pending |
| `act_wiz.do_purge.return.001` | 2578 | `return;` |  | pending |
| `act_wiz.do_purge.if.004` | 2581 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_purge.return.002` | 2584 | `return;` |  | pending |
| `act_wiz.do_purge.if.005` | 2587 | `if ( !IS_NPC(victim) )` |  | pending |
| `act_wiz.do_purge.if.006` | 2590 | `if (ch == victim)` |  | pending |
| `act_wiz.do_purge.return.003` | 2593 | `return;` |  | pending |
| `act_wiz.do_purge.if.007` | 2596 | `if (get_trust(ch) <= get_trust(victim))` |  | pending |
| `act_wiz.do_purge.return.004` | 2601 | `return;` |  | pending |
| `act_wiz.do_purge.if.008` | 2606 | `if (victim->level > 1)` |  | pending |
| `act_wiz.do_purge.if.009` | 2610 | `if ( d != NULL )` |  | pending |
| `act_wiz.do_purge.return.005` | 2613 | `return;` |  | pending |
| `act_wiz.do_purge.return.006` | 2618 | `return;` |  | pending |

## do_advance

[Source line 2623](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2623); ends at line 2710. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:283` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:69` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `is_number`, `send_to_char`, `get_char_world`, `IS_NPC`, `atoi`, `sprintf`, `get_trust`, `exp_per_level`, `advance_level`, `UMAX`, `save_char_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_advance.if.001` | 2635 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' \|\| !is_number( arg2 ) )` |  | pending |
| `act_wiz.do_advance.or.001` | 2635 | `\|\| arg2[0] == '\0' \|\| !is_number( arg2 ) )` |  | pending |
| `act_wiz.do_advance.or.002` | 2635 | `\|\| !is_number( arg2 ) )` |  | pending |
| `act_wiz.do_advance.return.001` | 2638 | `return;` |  | pending |
| `act_wiz.do_advance.if.002` | 2641 | `if ( ( victim = get_char_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_advance.return.002` | 2644 | `return;` |  | pending |
| `act_wiz.do_advance.if.003` | 2647 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_advance.return.003` | 2650 | `return;` |  | pending |
| `act_wiz.do_advance.if.004` | 2653 | `if ( ( level = atoi( arg2 ) ) < 1 \|\| level > MAX_LEVEL )` |  | pending |
| `act_wiz.do_advance.or.003` | 2653 | `\|\| level > MAX_LEVEL )` |  | pending |
| `act_wiz.do_advance.return.004` | 2657 | `return;` |  | pending |
| `act_wiz.do_advance.if.005` | 2660 | `if ( level > get_trust( ch ) )` |  | pending |
| `act_wiz.do_advance.return.005` | 2663 | `return;` |  | pending |
| `act_wiz.do_advance.if.006` | 2673 | `if ( level <= victim->level )` |  | pending |
| `act_wiz.do_advance.for.001` | 2698 | `for ( iLevel = victim->level ; iLevel < level; iLevel++ )` |  | pending |
| `act_wiz.do_advance.return.006` | 2709 | `return;` |  | pending |

## do_trust

[Source line 2714](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2714); ends at line 2752. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:285` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:273` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `is_number`, `send_to_char`, `get_char_world`, `atoi`, `sprintf`, `get_trust`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_trust.if.001` | 2725 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' \|\| !is_number( arg2 ) )` |  | pending |
| `act_wiz.do_trust.or.001` | 2725 | `\|\| arg2[0] == '\0' \|\| !is_number( arg2 ) )` |  | pending |
| `act_wiz.do_trust.or.002` | 2725 | `\|\| !is_number( arg2 ) )` |  | pending |
| `act_wiz.do_trust.return.001` | 2728 | `return;` |  | pending |
| `act_wiz.do_trust.if.002` | 2731 | `if ( ( victim = get_char_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_trust.return.002` | 2734 | `return;` |  | pending |
| `act_wiz.do_trust.if.003` | 2737 | `if ( ( level = atoi( arg2 ) ) < 0 \|\| level > MAX_LEVEL )` |  | pending |
| `act_wiz.do_trust.or.003` | 2737 | `\|\| level > MAX_LEVEL )` |  | pending |
| `act_wiz.do_trust.return.003` | 2741 | `return;` |  | pending |
| `act_wiz.do_trust.if.004` | 2744 | `if ( level > get_trust( ch ) )` |  | pending |
| `act_wiz.do_trust.return.004` | 2747 | `return;` |  | pending |
| `act_wiz.do_trust.return.005` | 2751 | `return;` |  | pending |

## do_restore

[Source line 2756](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2756); ends at line 2840. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:314` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:229` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `str_cmp`, `affect_strip`, `update_pos`, `act`, `sprintf`, `wiznet`, `get_trust`, `send_to_char`, `IS_NPC`, `get_char_world`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_restore.if.001` | 2764 | `if (arg[0] == '\0' \|\| !str_cmp(arg,"room"))` |  | pending |
| `act_wiz.do_restore.or.001` | 2764 | `\|\| !str_cmp(arg,"room"))` |  | pending |
| `act_wiz.do_restore.for.001` | 2768 | `for (vch = ch->in_room->people; vch != NULL; vch = vch->next_in_room)` |  | pending |
| `act_wiz.do_restore.return.001` | 2787 | `return;` |  | pending |
| `act_wiz.do_restore.if.002` | 2791 | `if ( get_trust(ch) >=  MAX_LEVEL - 1 && !str_cmp(arg,"all"))` |  | pending |
| `act_wiz.do_restore.and.001` | 2791 | `&& !str_cmp(arg,"all"))` |  | pending |
| `act_wiz.do_restore.for.002` | 2795 | `for (d = descriptor_list; d != NULL; d = d->next)` |  | pending |
| `act_wiz.do_restore.if.003` | 2799 | `if (victim == NULL \|\| IS_NPC(victim))` |  | pending |
| `act_wiz.do_restore.or.002` | 2799 | `\|\| IS_NPC(victim))` |  | pending |
| `act_wiz.do_restore.continue.001` | 2800 | `continue;` |  | pending |
| `act_wiz.do_restore.if.004` | 2812 | `if (victim->in_room != NULL)` |  | pending |
| `act_wiz.do_restore.return.002` | 2816 | `return;` |  | pending |
| `act_wiz.do_restore.if.005` | 2819 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_restore.return.003` | 2822 | `return;` |  | pending |
| `act_wiz.do_restore.ternary.001` | 2836 | `? victim->short_descr : victim->name);` |  | pending |
| `act_wiz.do_restore.return.004` | 2839 | `return;` |  | pending |

## do_freeze

[Source line 2843](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2843); ends at line 2894. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:293` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:134` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `IS_NPC`, `get_trust`, `IS_SET`, `REMOVE_BIT`, `sprintf`, `wiznet`, `SET_BIT`, `save_char_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_freeze.if.001` | 2850 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_freeze.return.001` | 2853 | `return;` |  | pending |
| `act_wiz.do_freeze.if.002` | 2856 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_freeze.return.002` | 2859 | `return;` |  | pending |
| `act_wiz.do_freeze.if.003` | 2862 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_freeze.return.003` | 2865 | `return;` |  | pending |
| `act_wiz.do_freeze.if.004` | 2868 | `if ( get_trust( victim ) >= get_trust( ch ) )` |  | pending |
| `act_wiz.do_freeze.return.004` | 2871 | `return;` |  | pending |
| `act_wiz.do_freeze.if.005` | 2874 | `if ( IS_SET(victim->act, PLR_FREEZE) )` |  | pending |
| `act_wiz.do_freeze.return.005` | 2893 | `return;` |  | pending |

## do_log

[Source line 2898](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2898); ends at line 2953. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:328` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:161` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `get_char_world`, `IS_NPC`, `IS_SET`, `REMOVE_BIT`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_log.if.001` | 2905 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_log.return.001` | 2908 | `return;` |  | pending |
| `act_wiz.do_log.if.002` | 2911 | `if ( !str_cmp( arg, "all" ) )` |  | pending |
| `act_wiz.do_log.if.003` | 2913 | `if ( fLogAll )` |  | pending |
| `act_wiz.do_log.return.002` | 2923 | `return;` |  | pending |
| `act_wiz.do_log.if.004` | 2926 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_log.return.003` | 2929 | `return;` |  | pending |
| `act_wiz.do_log.if.005` | 2932 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_log.return.004` | 2935 | `return;` |  | pending |
| `act_wiz.do_log.if.006` | 2941 | `if ( IS_SET(victim->act, PLR_LOG) )` |  | pending |
| `act_wiz.do_log.return.005` | 2952 | `return;` |  | pending |

## do_noemote

[Source line 2957](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2957); ends at line 3001. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:308` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:176` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `get_trust`, `IS_SET`, `REMOVE_BIT`, `sprintf`, `wiznet`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_noemote.if.001` | 2964 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_noemote.return.001` | 2967 | `return;` |  | pending |
| `act_wiz.do_noemote.if.002` | 2970 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_noemote.return.002` | 2973 | `return;` |  | pending |
| `act_wiz.do_noemote.if.003` | 2977 | `if ( get_trust( victim ) >= get_trust( ch ) )` |  | pending |
| `act_wiz.do_noemote.return.003` | 2980 | `return;` |  | pending |
| `act_wiz.do_noemote.if.004` | 2983 | `if ( IS_SET(victim->comm, COMM_NOEMOTE) )` |  | pending |
| `act_wiz.do_noemote.return.004` | 3000 | `return;` |  | pending |

## do_noshout

[Source line 3005](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3005); ends at line 3054. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:309` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:180` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `IS_NPC`, `get_trust`, `IS_SET`, `REMOVE_BIT`, `sprintf`, `wiznet`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_noshout.if.001` | 3012 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_noshout.return.001` | 3015 | `return;` |  | pending |
| `act_wiz.do_noshout.if.002` | 3018 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_noshout.return.002` | 3021 | `return;` |  | pending |
| `act_wiz.do_noshout.if.003` | 3024 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_noshout.return.003` | 3027 | `return;` |  | pending |
| `act_wiz.do_noshout.if.004` | 3030 | `if ( get_trust( victim ) >= get_trust( ch ) )` |  | pending |
| `act_wiz.do_noshout.return.004` | 3033 | `return;` |  | pending |
| `act_wiz.do_noshout.if.005` | 3036 | `if ( IS_SET(victim->comm, COMM_NOSHOUT) )` |  | pending |
| `act_wiz.do_noshout.return.005` | 3053 | `return;` |  | pending |

## do_notell

[Source line 3058](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3058); ends at line 3101. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:310` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:183` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `get_trust`, `IS_SET`, `REMOVE_BIT`, `sprintf`, `wiznet`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_notell.if.001` | 3065 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_notell.return.001` | 3068 | `return;` |  | pending |
| `act_wiz.do_notell.if.002` | 3071 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_notell.return.002` | 3074 | `return;` |  | pending |
| `act_wiz.do_notell.if.003` | 3077 | `if ( get_trust( victim ) >= get_trust( ch ) )` |  | pending |
| `act_wiz.do_notell.return.003` | 3080 | `return;` |  | pending |
| `act_wiz.do_notell.if.004` | 3083 | `if ( IS_SET(victim->comm, COMM_NOTELL) )` |  | pending |
| `act_wiz.do_notell.return.004` | 3100 | `return;` |  | pending |

## do_peace

[Source line 3105](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3105); ends at line 3119. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:332` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:194` (declaration_or_dispatch_reference).

Dependencies: `stop_fighting`, `IS_NPC`, `IS_SET`, `REMOVE_BIT`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_peace.for.001` | 3109 | `for ( rch = ch->in_room->people; rch != NULL; rch = rch->next_in_room )` |  | pending |
| `act_wiz.do_peace.if.001` | 3111 | `if ( rch->fighting != NULL )` |  | pending |
| `act_wiz.do_peace.if.002` | 3113 | `if (IS_NPC(rch) && IS_SET(rch->act,ACT_AGGRESSIVE))` |  | pending |
| `act_wiz.do_peace.and.001` | 3113 | `&& IS_SET(rch->act,ACT_AGGRESSIVE))` |  | pending |
| `act_wiz.do_peace.return.001` | 3118 | `return;` |  | pending |

## do_wizlock

[Source line 3121](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3121); ends at line 3138. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:302` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:292` (declaration_or_dispatch_reference).

Dependencies: `wiznet`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_wizlock.if.001` | 3126 | `if ( wizlock )` |  | pending |
| `act_wiz.do_wizlock.return.001` | 3137 | `return;` |  | pending |

## do_newlock

[Source line 3142](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3142); ends at line 3159. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:306` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:173` (declaration_or_dispatch_reference).

Dependencies: `wiznet`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_newlock.if.001` | 3147 | `if ( newlock )` |  | pending |
| `act_wiz.do_newlock.return.001` | 3158 | `return;` |  | pending |

## do_slookup

[Source line 3162](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3162); ends at line 3200. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_vnum: `src/act_wiz.c:1756` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:251` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `sprintf`, `skill_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_slookup.if.001` | 3169 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_slookup.return.001` | 3172 | `return;` |  | pending |
| `act_wiz.do_slookup.if.002` | 3175 | `if ( !str_cmp( arg, "all" ) )` |  | pending |
| `act_wiz.do_slookup.for.001` | 3177 | `for ( sn = 0; sn < MAX_SKILL; sn++ )` |  | pending |
| `act_wiz.do_slookup.if.003` | 3179 | `if ( skill_table[sn].name == NULL )` |  | pending |
| `act_wiz.do_slookup.break.001` | 3180 | `break;` |  | pending |
| `act_wiz.do_slookup.if.004` | 3188 | `if ( ( sn = skill_lookup( arg ) ) < 0 )` |  | pending |
| `act_wiz.do_slookup.return.002` | 3191 | `return;` |  | pending |
| `act_wiz.do_slookup.return.003` | 3199 | `return;` |  | pending |

## do_set

[Source line 3204](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3204); ends at line 3245. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_set: `src/act_wiz.c:3244` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:298` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:241` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_prefix`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_set.if.001` | 3210 | `if (arg[0] == '\0')` |  | pending |
| `act_wiz.do_set.return.001` | 3217 | `return;` |  | pending |
| `act_wiz.do_set.if.002` | 3220 | `if (!str_prefix(arg,"mobile") \|\| !str_prefix(arg,"character"))` |  | pending |
| `act_wiz.do_set.or.001` | 3220 | `\|\| !str_prefix(arg,"character"))` |  | pending |
| `act_wiz.do_set.return.002` | 3223 | `return;` |  | pending |
| `act_wiz.do_set.if.003` | 3226 | `if (!str_prefix(arg,"skill") \|\| !str_prefix(arg,"spell"))` |  | pending |
| `act_wiz.do_set.or.002` | 3226 | `\|\| !str_prefix(arg,"spell"))` |  | pending |
| `act_wiz.do_set.return.003` | 3229 | `return;` |  | pending |
| `act_wiz.do_set.if.004` | 3232 | `if (!str_prefix(arg,"object"))` |  | pending |
| `act_wiz.do_set.return.004` | 3235 | `return;` |  | pending |
| `act_wiz.do_set.if.005` | 3238 | `if (!str_prefix(arg,"room"))` |  | pending |
| `act_wiz.do_set.return.005` | 3241 | `return;` |  | pending |

## do_sset

[Source line 3248](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3248); ends at line 3321. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_set: `src/act_wiz.c:3228` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:260` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_world`, `IS_NPC`, `str_cmp`, `skill_lookup`, `is_number`, `atoi`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_sset.if.001` | 3262 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_sset.or.001` | 3262 | `\|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_sset.or.002` | 3262 | `\|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_sset.return.001` | 3268 | `return;` |  | pending |
| `act_wiz.do_sset.if.002` | 3271 | `if ( ( victim = get_char_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_sset.return.002` | 3274 | `return;` |  | pending |
| `act_wiz.do_sset.if.003` | 3277 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_sset.return.003` | 3280 | `return;` |  | pending |
| `act_wiz.do_sset.if.004` | 3285 | `if ( !fAll && ( sn = skill_lookup( arg2 ) ) < 0 )` |  | pending |
| `act_wiz.do_sset.and.001` | 3285 | `&& ( sn = skill_lookup( arg2 ) ) < 0 )` |  | pending |
| `act_wiz.do_sset.return.004` | 3288 | `return;` |  | pending |
| `act_wiz.do_sset.if.005` | 3294 | `if ( !is_number( arg3 ) )` |  | pending |
| `act_wiz.do_sset.return.005` | 3297 | `return;` |  | pending |
| `act_wiz.do_sset.if.006` | 3301 | `if ( value < 0 \|\| value > 100 )` |  | pending |
| `act_wiz.do_sset.or.003` | 3301 | `\|\| value > 100 )` |  | pending |
| `act_wiz.do_sset.return.006` | 3304 | `return;` |  | pending |
| `act_wiz.do_sset.if.007` | 3307 | `if ( fAll )` |  | pending |
| `act_wiz.do_sset.for.001` | 3309 | `for ( sn = 0; sn < MAX_SKILL; sn++ )` |  | pending |
| `act_wiz.do_sset.if.008` | 3311 | `if ( skill_table[sn].name != NULL )` |  | pending |
| `act_wiz.do_sset.return.007` | 3320 | `return;` |  | pending |

## do_mset

[Source line 3324](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3324); ends at line 3698. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_set: `src/act_wiz.c:3222` (function_symbol_reference_candidate).
- do_mset: `src/act_wiz.c:3696` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:166` (declaration_or_dispatch_reference).

Dependencies: `smash_tilde`, `one_argument`, `strcpy`, `send_to_char`, `get_char_world`, `is_number`, `atoi`, `str_cmp`, `get_max_train`, `sprintf`, `str_prefix`, `IS_NPC`, `class_lookup`, `strcat`, `race_lookup`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_mset.if.001` | 3338 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_mset.or.001` | 3338 | `\|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_mset.or.002` | 3338 | `\|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_mset.return.001` | 3346 | `return;` |  | pending |
| `act_wiz.do_mset.if.002` | 3349 | `if ( ( victim = get_char_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_mset.return.002` | 3352 | `return;` |  | pending |
| `act_wiz.do_mset.ternary.001` | 3361 | `? atoi( arg3 ) : -1;` |  | pending |
| `act_wiz.do_mset.if.003` | 3366 | `if ( !str_cmp( arg2, "str" ) )` |  | pending |
| `act_wiz.do_mset.if.004` | 3368 | `if ( value < 3 \|\| value > get_max_train(victim,STAT_STR) )` |  | pending |
| `act_wiz.do_mset.or.003` | 3368 | `\|\| value > get_max_train(victim,STAT_STR) )` |  | pending |
| `act_wiz.do_mset.return.003` | 3374 | `return;` |  | pending |
| `act_wiz.do_mset.return.004` | 3378 | `return;` |  | pending |
| `act_wiz.do_mset.if.005` | 3381 | `if ( !str_cmp( arg2, "int" ) )` |  | pending |
| `act_wiz.do_mset.if.006` | 3383 | `if ( value < 3 \|\| value > get_max_train(victim,STAT_INT) )` |  | pending |
| `act_wiz.do_mset.or.004` | 3383 | `\|\| value > get_max_train(victim,STAT_INT) )` |  | pending |
| `act_wiz.do_mset.return.005` | 3389 | `return;` |  | pending |
| `act_wiz.do_mset.return.006` | 3393 | `return;` |  | pending |
| `act_wiz.do_mset.if.007` | 3396 | `if ( !str_cmp( arg2, "wis" ) )` |  | pending |
| `act_wiz.do_mset.if.008` | 3398 | `if ( value < 3 \|\| value > get_max_train(victim,STAT_WIS) )` |  | pending |
| `act_wiz.do_mset.or.005` | 3398 | `\|\| value > get_max_train(victim,STAT_WIS) )` |  | pending |
| `act_wiz.do_mset.return.007` | 3403 | `return;` |  | pending |
| `act_wiz.do_mset.return.008` | 3407 | `return;` |  | pending |
| `act_wiz.do_mset.if.009` | 3410 | `if ( !str_cmp( arg2, "dex" ) )` |  | pending |
| `act_wiz.do_mset.if.010` | 3412 | `if ( value < 3 \|\| value > get_max_train(victim,STAT_DEX) )` |  | pending |
| `act_wiz.do_mset.or.006` | 3412 | `\|\| value > get_max_train(victim,STAT_DEX) )` |  | pending |
| `act_wiz.do_mset.return.009` | 3418 | `return;` |  | pending |
| `act_wiz.do_mset.return.010` | 3422 | `return;` |  | pending |
| `act_wiz.do_mset.if.011` | 3425 | `if ( !str_cmp( arg2, "con" ) )` |  | pending |
| `act_wiz.do_mset.if.012` | 3427 | `if ( value < 3 \|\| value > get_max_train(victim,STAT_CON) )` |  | pending |
| `act_wiz.do_mset.or.007` | 3427 | `\|\| value > get_max_train(victim,STAT_CON) )` |  | pending |
| `act_wiz.do_mset.return.011` | 3433 | `return;` |  | pending |
| `act_wiz.do_mset.return.012` | 3437 | `return;` |  | pending |
| `act_wiz.do_mset.if.013` | 3440 | `if ( !str_prefix( arg2, "sex" ) )` |  | pending |
| `act_wiz.do_mset.if.014` | 3442 | `if ( value < 0 \|\| value > 2 )` |  | pending |
| `act_wiz.do_mset.or.008` | 3442 | `\|\| value > 2 )` |  | pending |
| `act_wiz.do_mset.return.013` | 3445 | `return;` |  | pending |
| `act_wiz.do_mset.if.015` | 3448 | `if (!IS_NPC(victim))` |  | pending |
| `act_wiz.do_mset.return.014` | 3450 | `return;` |  | pending |
| `act_wiz.do_mset.if.016` | 3453 | `if ( !str_prefix( arg2, "class" ) )` |  | pending |
| `act_wiz.do_mset.if.017` | 3457 | `if (IS_NPC(victim))` |  | pending |
| `act_wiz.do_mset.return.015` | 3460 | `return;` |  | pending |
| `act_wiz.do_mset.if.018` | 3464 | `if ( class == -1 )` |  | pending |
| `act_wiz.do_mset.for.001` | 3469 | `for ( class = 0; class < MAX_CLASS; class++ )` |  | pending |
| `act_wiz.do_mset.if.019` | 3471 | `if ( class > 0 )` |  | pending |
| `act_wiz.do_mset.return.016` | 3478 | `return;` |  | pending |
| `act_wiz.do_mset.return.017` | 3482 | `return;` |  | pending |
| `act_wiz.do_mset.if.020` | 3485 | `if ( !str_prefix( arg2, "level" ) )` |  | pending |
| `act_wiz.do_mset.if.021` | 3487 | `if ( !IS_NPC(victim) )` |  | pending |
| `act_wiz.do_mset.return.018` | 3490 | `return;` |  | pending |
| `act_wiz.do_mset.if.022` | 3493 | `if ( value < 0 \|\| value > MAX_LEVEL )` |  | pending |
| `act_wiz.do_mset.or.009` | 3493 | `\|\| value > MAX_LEVEL )` |  | pending |
| `act_wiz.do_mset.return.019` | 3497 | `return;` |  | pending |
| `act_wiz.do_mset.return.020` | 3500 | `return;` |  | pending |
| `act_wiz.do_mset.if.023` | 3503 | `if ( !str_prefix( arg2, "gold" ) )` |  | pending |
| `act_wiz.do_mset.return.021` | 3506 | `return;` |  | pending |
| `act_wiz.do_mset.if.024` | 3509 | `if ( !str_prefix(arg2, "silver" ) )` |  | pending |
| `act_wiz.do_mset.return.022` | 3512 | `return;` |  | pending |
| `act_wiz.do_mset.if.025` | 3515 | `if ( !str_prefix( arg2, "hp" ) )` |  | pending |
| `act_wiz.do_mset.if.026` | 3517 | `if ( value < -10 \|\| value > 30000 )` |  | pending |
| `act_wiz.do_mset.or.010` | 3517 | `\|\| value > 30000 )` |  | pending |
| `act_wiz.do_mset.return.023` | 3520 | `return;` |  | pending |
| `act_wiz.do_mset.if.027` | 3523 | `if (!IS_NPC(victim))` |  | pending |
| `act_wiz.do_mset.return.024` | 3525 | `return;` |  | pending |
| `act_wiz.do_mset.if.028` | 3528 | `if ( !str_prefix( arg2, "mana" ) )` |  | pending |
| `act_wiz.do_mset.if.029` | 3530 | `if ( value < 0 \|\| value > 30000 )` |  | pending |
| `act_wiz.do_mset.or.011` | 3530 | `\|\| value > 30000 )` |  | pending |
| `act_wiz.do_mset.return.025` | 3533 | `return;` |  | pending |
| `act_wiz.do_mset.if.030` | 3536 | `if (!IS_NPC(victim))` |  | pending |
| `act_wiz.do_mset.return.026` | 3538 | `return;` |  | pending |
| `act_wiz.do_mset.if.031` | 3541 | `if ( !str_prefix( arg2, "move" ) )` |  | pending |
| `act_wiz.do_mset.if.032` | 3543 | `if ( value < 0 \|\| value > 30000 )` |  | pending |
| `act_wiz.do_mset.or.012` | 3543 | `\|\| value > 30000 )` |  | pending |
| `act_wiz.do_mset.return.027` | 3546 | `return;` |  | pending |
| `act_wiz.do_mset.if.033` | 3549 | `if (!IS_NPC(victim))` |  | pending |
| `act_wiz.do_mset.return.028` | 3551 | `return;` |  | pending |
| `act_wiz.do_mset.if.034` | 3554 | `if ( !str_prefix( arg2, "practice" ) )` |  | pending |
| `act_wiz.do_mset.if.035` | 3556 | `if ( value < 0 \|\| value > 250 )` |  | pending |
| `act_wiz.do_mset.or.013` | 3556 | `\|\| value > 250 )` |  | pending |
| `act_wiz.do_mset.return.029` | 3559 | `return;` |  | pending |
| `act_wiz.do_mset.return.030` | 3562 | `return;` |  | pending |
| `act_wiz.do_mset.if.036` | 3565 | `if ( !str_prefix( arg2, "train" ))` |  | pending |
| `act_wiz.do_mset.if.037` | 3567 | `if (value < 0 \|\| value > 50 )` |  | pending |
| `act_wiz.do_mset.or.014` | 3567 | `\|\| value > 50 )` |  | pending |
| `act_wiz.do_mset.return.031` | 3570 | `return;` |  | pending |
| `act_wiz.do_mset.return.032` | 3573 | `return;` |  | pending |
| `act_wiz.do_mset.if.038` | 3576 | `if ( !str_prefix( arg2, "align" ) )` |  | pending |
| `act_wiz.do_mset.if.039` | 3578 | `if ( value < -1000 \|\| value > 1000 )` |  | pending |
| `act_wiz.do_mset.or.015` | 3578 | `\|\| value > 1000 )` |  | pending |
| `act_wiz.do_mset.return.033` | 3581 | `return;` |  | pending |
| `act_wiz.do_mset.return.034` | 3584 | `return;` |  | pending |
| `act_wiz.do_mset.if.040` | 3587 | `if ( !str_prefix( arg2, "thirst" ) )` |  | pending |
| `act_wiz.do_mset.if.041` | 3589 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_mset.return.035` | 3592 | `return;` |  | pending |
| `act_wiz.do_mset.if.042` | 3595 | `if ( value < -1 \|\| value > 100 )` |  | pending |
| `act_wiz.do_mset.or.016` | 3595 | `\|\| value > 100 )` |  | pending |
| `act_wiz.do_mset.return.036` | 3598 | `return;` |  | pending |
| `act_wiz.do_mset.return.037` | 3602 | `return;` |  | pending |
| `act_wiz.do_mset.if.043` | 3605 | `if ( !str_prefix( arg2, "drunk" ) )` |  | pending |
| `act_wiz.do_mset.if.044` | 3607 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_mset.return.038` | 3610 | `return;` |  | pending |
| `act_wiz.do_mset.if.045` | 3613 | `if ( value < -1 \|\| value > 100 )` |  | pending |
| `act_wiz.do_mset.or.017` | 3613 | `\|\| value > 100 )` |  | pending |
| `act_wiz.do_mset.return.039` | 3616 | `return;` |  | pending |
| `act_wiz.do_mset.return.040` | 3620 | `return;` |  | pending |
| `act_wiz.do_mset.if.046` | 3623 | `if ( !str_prefix( arg2, "full" ) )` |  | pending |
| `act_wiz.do_mset.if.047` | 3625 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_mset.return.041` | 3628 | `return;` |  | pending |
| `act_wiz.do_mset.if.048` | 3631 | `if ( value < -1 \|\| value > 100 )` |  | pending |
| `act_wiz.do_mset.or.018` | 3631 | `\|\| value > 100 )` |  | pending |
| `act_wiz.do_mset.return.042` | 3634 | `return;` |  | pending |
| `act_wiz.do_mset.return.043` | 3638 | `return;` |  | pending |
| `act_wiz.do_mset.if.049` | 3641 | `if ( !str_prefix( arg2, "hunger" ) )` |  | pending |
| `act_wiz.do_mset.if.050` | 3643 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_mset.return.044` | 3646 | `return;` |  | pending |
| `act_wiz.do_mset.if.051` | 3649 | `if ( value < -1 \|\| value > 100 )` |  | pending |
| `act_wiz.do_mset.or.019` | 3649 | `\|\| value > 100 )` |  | pending |
| `act_wiz.do_mset.return.045` | 3652 | `return;` |  | pending |
| `act_wiz.do_mset.return.046` | 3656 | `return;` |  | pending |
| `act_wiz.do_mset.if.052` | 3659 | `if (!str_prefix( arg2, "race" ) )` |  | pending |
| `act_wiz.do_mset.if.053` | 3665 | `if ( race == 0)` |  | pending |
| `act_wiz.do_mset.return.047` | 3668 | `return;` |  | pending |
| `act_wiz.do_mset.if.054` | 3671 | `if (!IS_NPC(victim) && !race_table[race].pc_race)` |  | pending |
| `act_wiz.do_mset.and.001` | 3671 | `&& !race_table[race].pc_race)` |  | pending |
| `act_wiz.do_mset.return.048` | 3674 | `return;` |  | pending |
| `act_wiz.do_mset.return.049` | 3678 | `return;` |  | pending |
| `act_wiz.do_mset.if.055` | 3681 | `if (!str_prefix(arg2,"group"))` |  | pending |
| `act_wiz.do_mset.if.056` | 3683 | `if (!IS_NPC(victim))` |  | pending |
| `act_wiz.do_mset.return.050` | 3686 | `return;` |  | pending |
| `act_wiz.do_mset.return.051` | 3689 | `return;` |  | pending |
| `act_wiz.do_mset.return.052` | 3697 | `return;` |  | pending |

## do_string

[Source line 3700](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3700); ends at line 3860. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_string: `src/act_wiz.c:3859` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:338` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:265` (declaration_or_dispatch_reference).

Dependencies: `smash_tilde`, `one_argument`, `strcpy`, `send_to_char`, `str_prefix`, `get_char_world`, `IS_NPC`, `free_string`, `str_dup`, `strcat`, `set_title`, `spec_lookup`, `get_obj_world`, `new_extra_descr`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_string.if.001` | 3715 | `if ( type[0] == '\0' \|\| arg1[0] == '\0' \|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_string.or.001` | 3715 | `\|\| arg1[0] == '\0' \|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_string.or.002` | 3715 | `\|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_string.or.003` | 3715 | `\|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_string.return.001` | 3722 | `return;` |  | pending |
| `act_wiz.do_string.if.002` | 3725 | `if (!str_prefix(type,"character") \|\| !str_prefix(type,"mobile"))` |  | pending |
| `act_wiz.do_string.or.004` | 3725 | `\|\| !str_prefix(type,"mobile"))` |  | pending |
| `act_wiz.do_string.if.003` | 3727 | `if ( ( victim = get_char_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_string.return.002` | 3730 | `return;` |  | pending |
| `act_wiz.do_string.if.004` | 3738 | `if ( !str_prefix( arg2, "name" ) )` |  | pending |
| `act_wiz.do_string.if.005` | 3740 | `if ( !IS_NPC(victim) )` |  | pending |
| `act_wiz.do_string.return.003` | 3743 | `return;` |  | pending |
| `act_wiz.do_string.return.004` | 3747 | `return;` |  | pending |
| `act_wiz.do_string.if.006` | 3750 | `if ( !str_prefix( arg2, "description" ) )` |  | pending |
| `act_wiz.do_string.return.005` | 3754 | `return;` |  | pending |
| `act_wiz.do_string.if.007` | 3757 | `if ( !str_prefix( arg2, "short" ) )` |  | pending |
| `act_wiz.do_string.return.006` | 3761 | `return;` |  | pending |
| `act_wiz.do_string.if.008` | 3764 | `if ( !str_prefix( arg2, "long" ) )` |  | pending |
| `act_wiz.do_string.return.007` | 3769 | `return;` |  | pending |
| `act_wiz.do_string.if.009` | 3772 | `if ( !str_prefix( arg2, "title" ) )` |  | pending |
| `act_wiz.do_string.if.010` | 3774 | `if ( IS_NPC(victim) )` |  | pending |
| `act_wiz.do_string.return.008` | 3777 | `return;` |  | pending |
| `act_wiz.do_string.return.009` | 3781 | `return;` |  | pending |
| `act_wiz.do_string.if.011` | 3784 | `if ( !str_prefix( arg2, "spec" ) )` |  | pending |
| `act_wiz.do_string.if.012` | 3786 | `if ( !IS_NPC(victim) )` |  | pending |
| `act_wiz.do_string.return.010` | 3789 | `return;` |  | pending |
| `act_wiz.do_string.if.013` | 3792 | `if ( ( victim->spec_fun = spec_lookup( arg3 ) ) == 0 )` |  | pending |
| `act_wiz.do_string.return.011` | 3795 | `return;` |  | pending |
| `act_wiz.do_string.return.012` | 3798 | `return;` |  | pending |
| `act_wiz.do_string.if.014` | 3802 | `if (!str_prefix(type,"object"))` |  | pending |
| `act_wiz.do_string.if.015` | 3806 | `if ( ( obj = get_obj_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_string.return.013` | 3809 | `return;` |  | pending |
| `act_wiz.do_string.if.016` | 3812 | `if ( !str_prefix( arg2, "name" ) )` |  | pending |
| `act_wiz.do_string.return.014` | 3816 | `return;` |  | pending |
| `act_wiz.do_string.if.017` | 3819 | `if ( !str_prefix( arg2, "short" ) )` |  | pending |
| `act_wiz.do_string.return.015` | 3823 | `return;` |  | pending |
| `act_wiz.do_string.if.018` | 3826 | `if ( !str_prefix( arg2, "long" ) )` |  | pending |
| `act_wiz.do_string.return.016` | 3830 | `return;` |  | pending |
| `act_wiz.do_string.if.019` | 3833 | `if ( !str_prefix( arg2, "ed" ) \|\| !str_prefix( arg2, "extended"))` |  | pending |
| `act_wiz.do_string.or.005` | 3833 | `\|\| !str_prefix( arg2, "extended"))` |  | pending |
| `act_wiz.do_string.if.020` | 3838 | `if ( argument == NULL )` |  | pending |
| `act_wiz.do_string.return.017` | 3842 | `return;` |  | pending |
| `act_wiz.do_string.return.018` | 3853 | `return;` |  | pending |

## do_oset

[Source line 3864](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3864); ends at line 3972. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_set: `src/act_wiz.c:3234` (function_symbol_reference_candidate).
- do_oset: `src/act_wiz.c:3970` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:188` (declaration_or_dispatch_reference).

Dependencies: `smash_tilde`, `one_argument`, `strcpy`, `send_to_char`, `get_obj_world`, `atoi`, `str_cmp`, `UMIN`, `str_prefix`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_oset.if.001` | 3877 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_oset.or.001` | 3877 | `\|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_oset.or.002` | 3877 | `\|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_oset.return.001` | 3884 | `return;` |  | pending |
| `act_wiz.do_oset.if.002` | 3887 | `if ( ( obj = get_obj_world( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_oset.return.002` | 3890 | `return;` |  | pending |
| `act_wiz.do_oset.if.003` | 3901 | `if ( !str_cmp( arg2, "value0" ) \|\| !str_cmp( arg2, "v0" ) )` |  | pending |
| `act_wiz.do_oset.or.003` | 3901 | `\|\| !str_cmp( arg2, "v0" ) )` |  | pending |
| `act_wiz.do_oset.return.003` | 3904 | `return;` |  | pending |
| `act_wiz.do_oset.if.004` | 3907 | `if ( !str_cmp( arg2, "value1" ) \|\| !str_cmp( arg2, "v1" ) )` |  | pending |
| `act_wiz.do_oset.or.004` | 3907 | `\|\| !str_cmp( arg2, "v1" ) )` |  | pending |
| `act_wiz.do_oset.return.004` | 3910 | `return;` |  | pending |
| `act_wiz.do_oset.if.005` | 3913 | `if ( !str_cmp( arg2, "value2" ) \|\| !str_cmp( arg2, "v2" ) )` |  | pending |
| `act_wiz.do_oset.or.005` | 3913 | `\|\| !str_cmp( arg2, "v2" ) )` |  | pending |
| `act_wiz.do_oset.return.005` | 3916 | `return;` |  | pending |
| `act_wiz.do_oset.if.006` | 3919 | `if ( !str_cmp( arg2, "value3" ) \|\| !str_cmp( arg2, "v3" ) )` |  | pending |
| `act_wiz.do_oset.or.006` | 3919 | `\|\| !str_cmp( arg2, "v3" ) )` |  | pending |
| `act_wiz.do_oset.return.006` | 3922 | `return;` |  | pending |
| `act_wiz.do_oset.if.007` | 3925 | `if ( !str_cmp( arg2, "value4" ) \|\| !str_cmp( arg2, "v4" ) )` |  | pending |
| `act_wiz.do_oset.or.007` | 3925 | `\|\| !str_cmp( arg2, "v4" ) )` |  | pending |
| `act_wiz.do_oset.return.007` | 3928 | `return;` |  | pending |
| `act_wiz.do_oset.if.008` | 3931 | `if ( !str_prefix( arg2, "extra" ) )` |  | pending |
| `act_wiz.do_oset.return.008` | 3934 | `return;` |  | pending |
| `act_wiz.do_oset.if.009` | 3937 | `if ( !str_prefix( arg2, "wear" ) )` |  | pending |
| `act_wiz.do_oset.return.009` | 3940 | `return;` |  | pending |
| `act_wiz.do_oset.if.010` | 3943 | `if ( !str_prefix( arg2, "level" ) )` |  | pending |
| `act_wiz.do_oset.return.010` | 3946 | `return;` |  | pending |
| `act_wiz.do_oset.if.011` | 3949 | `if ( !str_prefix( arg2, "weight" ) )` |  | pending |
| `act_wiz.do_oset.return.011` | 3952 | `return;` |  | pending |
| `act_wiz.do_oset.if.012` | 3955 | `if ( !str_prefix( arg2, "cost" ) )` |  | pending |
| `act_wiz.do_oset.return.012` | 3958 | `return;` |  | pending |
| `act_wiz.do_oset.if.013` | 3961 | `if ( !str_prefix( arg2, "timer" ) )` |  | pending |
| `act_wiz.do_oset.return.013` | 3964 | `return;` |  | pending |
| `act_wiz.do_oset.return.014` | 3971 | `return;` |  | pending |

## do_rset

[Source line 3976](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3976); ends at line 4041. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_set: `src/act_wiz.c:3240` (function_symbol_reference_candidate).
- do_rset: `src/act_wiz.c:4039` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:231` (declaration_or_dispatch_reference).

Dependencies: `smash_tilde`, `one_argument`, `strcpy`, `send_to_char`, `find_location`, `is_room_owner`, `room_is_private`, `IS_TRUSTED`, `is_number`, `atoi`, `str_prefix`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_rset.if.001` | 3989 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_rset.or.001` | 3989 | `\|\| arg2[0] == '\0' \|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_rset.or.002` | 3989 | `\|\| arg3[0] == '\0' )` |  | pending |
| `act_wiz.do_rset.return.001` | 3995 | `return;` |  | pending |
| `act_wiz.do_rset.if.002` | 3998 | `if ( ( location = find_location( ch, arg1 ) ) == NULL )` |  | pending |
| `act_wiz.do_rset.return.002` | 4001 | `return;` |  | pending |
| `act_wiz.do_rset.if.003` | 4004 | `if (!is_room_owner(ch,location) && ch->in_room != location      &&  room_is_private(location) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_rset.and.001` | 4004 | `&& ch->in_room != location` |  | pending |
| `act_wiz.do_rset.and.002` | 4005 | `&&  room_is_private(location) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_rset.and.003` | 4005 | `&& !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_rset.return.003` | 4008 | `return;` |  | pending |
| `act_wiz.do_rset.if.004` | 4014 | `if ( !is_number( arg3 ) )` |  | pending |
| `act_wiz.do_rset.return.004` | 4017 | `return;` |  | pending |
| `act_wiz.do_rset.if.005` | 4024 | `if ( !str_prefix( arg2, "flags" ) )` |  | pending |
| `act_wiz.do_rset.return.005` | 4027 | `return;` |  | pending |
| `act_wiz.do_rset.if.006` | 4030 | `if ( !str_prefix( arg2, "sector" ) )` |  | pending |
| `act_wiz.do_rset.return.006` | 4033 | `return;` |  | pending |
| `act_wiz.do_rset.return.007` | 4040 | `return;` |  | pending |

## do_sockets

[Source line 4045](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4045); ends at line 4083. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:100` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:257` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `can_see`, `is_name`, `sprintf`, `strlen`, `send_to_char`, `strcat`, `page_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_sockets.for.001` | 4057 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `act_wiz.do_sockets.if.001` | 4059 | `if ( d->character != NULL && can_see( ch, d->character )  	&& (arg[0] == '\0' \|\| is_name(arg,d->character->name) 			   \|\| (d->original && is_name(arg,d->original->name))))` |  | pending |
| `act_wiz.do_sockets.and.001` | 4059 | `&& can_see( ch, d->character )` |  | pending |
| `act_wiz.do_sockets.and.002` | 4060 | `&& (arg[0] == '\0' \|\| is_name(arg,d->character->name)` |  | pending |
| `act_wiz.do_sockets.or.001` | 4060 | `\|\| is_name(arg,d->character->name)` |  | pending |
| `act_wiz.do_sockets.or.002` | 4061 | `\|\| (d->original && is_name(arg,d->original->name))))` |  | pending |
| `act_wiz.do_sockets.and.003` | 4061 | `&& is_name(arg,d->original->name))))` |  | pending |
| `act_wiz.do_sockets.ternary.001` | 4067 | `? d->original->name  :` |  | pending |
| `act_wiz.do_sockets.ternary.002` | 4068 | `? d->character->name : "(none)",` |  | pending |
| `act_wiz.do_sockets.if.002` | 4073 | `if (count == 0)` |  | pending |
| `act_wiz.do_sockets.return.001` | 4076 | `return;` |  | pending |
| `act_wiz.do_sockets.ternary.003` | 4079 | `? "" : "s" );` |  | pending |
| `act_wiz.do_sockets.return.002` | 4082 | `return;` |  | pending |

## do_force

[Source line 4090](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4090); ends at line 4224. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:304` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:133` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `sprintf`, `get_trust`, `IS_NPC`, `act`, `interpret`, `get_char_world`, `is_room_owner`, `room_is_private`, `IS_TRUSTED`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_force.if.001` | 4098 | `if ( arg[0] == '\0' \|\| argument[0] == '\0' )` |  | pending |
| `act_wiz.do_force.or.001` | 4098 | `\|\| argument[0] == '\0' )` |  | pending |
| `act_wiz.do_force.return.001` | 4101 | `return;` |  | pending |
| `act_wiz.do_force.if.002` | 4106 | `if (!str_cmp(arg2,"delete"))` |  | pending |
| `act_wiz.do_force.return.002` | 4109 | `return;` |  | pending |
| `act_wiz.do_force.if.003` | 4114 | `if ( !str_cmp( arg, "all" ) )` |  | pending |
| `act_wiz.do_force.if.004` | 4119 | `if (get_trust(ch) < MAX_LEVEL - 3)` |  | pending |
| `act_wiz.do_force.return.003` | 4122 | `return;` |  | pending |
| `act_wiz.do_force.for.001` | 4125 | `for ( vch = char_list; vch != NULL; vch = vch_next )` |  | pending |
| `act_wiz.do_force.if.005` | 4129 | `if ( !IS_NPC(vch) && get_trust( vch ) < get_trust( ch ) )` |  | pending |
| `act_wiz.do_force.and.001` | 4129 | `&& get_trust( vch ) < get_trust( ch ) )` |  | pending |
| `act_wiz.do_force.if.006` | 4136 | `if (!str_cmp(arg,"players"))` |  | pending |
| `act_wiz.do_force.if.007` | 4141 | `if (get_trust(ch) < MAX_LEVEL - 2)` |  | pending |
| `act_wiz.do_force.return.004` | 4144 | `return;` |  | pending |
| `act_wiz.do_force.for.002` | 4147 | `for ( vch = char_list; vch != NULL; vch = vch_next )` |  | pending |
| `act_wiz.do_force.if.008` | 4151 | `if ( !IS_NPC(vch) && get_trust( vch ) < get_trust( ch )  	    &&	 vch->level < LEVEL_HERO)` |  | pending |
| `act_wiz.do_force.and.002` | 4151 | `&& get_trust( vch ) < get_trust( ch )` |  | pending |
| `act_wiz.do_force.and.003` | 4152 | `&&	 vch->level < LEVEL_HERO)` |  | pending |
| `act_wiz.do_force.if.009` | 4159 | `if (!str_cmp(arg,"gods"))` |  | pending |
| `act_wiz.do_force.if.010` | 4164 | `if (get_trust(ch) < MAX_LEVEL - 2)` |  | pending |
| `act_wiz.do_force.return.005` | 4167 | `return;` |  | pending |
| `act_wiz.do_force.for.003` | 4170 | `for ( vch = char_list; vch != NULL; vch = vch_next )` |  | pending |
| `act_wiz.do_force.if.011` | 4174 | `if ( !IS_NPC(vch) && get_trust( vch ) < get_trust( ch )             &&   vch->level >= LEVEL_HERO)` |  | pending |
| `act_wiz.do_force.and.004` | 4174 | `&& get_trust( vch ) < get_trust( ch )` |  | pending |
| `act_wiz.do_force.and.005` | 4175 | `&&   vch->level >= LEVEL_HERO)` |  | pending |
| `act_wiz.do_force.if.012` | 4186 | `if ( ( victim = get_char_world( ch, arg ) ) == NULL )` |  | pending |
| `act_wiz.do_force.return.006` | 4189 | `return;` |  | pending |
| `act_wiz.do_force.if.013` | 4192 | `if ( victim == ch )` |  | pending |
| `act_wiz.do_force.return.007` | 4195 | `return;` |  | pending |
| `act_wiz.do_force.if.014` | 4198 | `if (!is_room_owner(ch,victim->in_room)  	&&  ch->in_room != victim->in_room          &&  room_is_private(victim->in_room) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_force.and.006` | 4199 | `&&  ch->in_room != victim->in_room` |  | pending |
| `act_wiz.do_force.and.007` | 4200 | `&&  room_is_private(victim->in_room) && !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_force.and.008` | 4200 | `&& !IS_TRUSTED(ch,IMPLEMENTOR))` |  | pending |
| `act_wiz.do_force.return.008` | 4203 | `return;` |  | pending |
| `act_wiz.do_force.if.015` | 4206 | `if ( get_trust( victim ) >= get_trust( ch ) )` |  | pending |
| `act_wiz.do_force.return.009` | 4209 | `return;` |  | pending |
| `act_wiz.do_force.if.016` | 4212 | `if ( !IS_NPC(victim) && get_trust(ch) < MAX_LEVEL -3)` |  | pending |
| `act_wiz.do_force.and.009` | 4212 | `&& get_trust(ch) < MAX_LEVEL -3)` |  | pending |
| `act_wiz.do_force.return.010` | 4215 | `return;` |  | pending |
| `act_wiz.do_force.return.011` | 4223 | `return;` |  | pending |

## do_invis

[Source line 4231](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4231); ends at line 4273. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:327` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:340` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:155` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `act`, `send_to_char`, `get_trust`, `atoi`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_invis.if.001` | 4239 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_invis.if.002` | 4242 | `if ( ch->invis_level)` |  | pending |
| `act_wiz.do_invis.if.003` | 4258 | `if (level < 2 \|\| level > get_trust(ch))` |  | pending |
| `act_wiz.do_invis.or.001` | 4258 | `\|\| level > get_trust(ch))` |  | pending |
| `act_wiz.do_invis.return.001` | 4261 | `return;` |  | pending |
| `act_wiz.do_invis.return.002` | 4272 | `return;` |  | pending |

## do_incognito

[Source line 4276](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4276); ends at line 4318. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:326` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:151` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `act`, `send_to_char`, `get_trust`, `atoi`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_incognito.if.001` | 4284 | `if ( arg[0] == '\0' )` |  | pending |
| `act_wiz.do_incognito.if.002` | 4287 | `if ( ch->incog_level)` |  | pending |
| `act_wiz.do_incognito.if.003` | 4303 | `if (level < 2 \|\| level > get_trust(ch))` |  | pending |
| `act_wiz.do_incognito.or.001` | 4303 | `\|\| level > get_trust(ch))` |  | pending |
| `act_wiz.do_incognito.return.001` | 4306 | `return;` |  | pending |
| `act_wiz.do_incognito.return.002` | 4317 | `return;` |  | pending |

## do_holylight

[Source line 4322](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4322); ends at line 4339. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:325` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:148` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `REMOVE_BIT`, `send_to_char`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_holylight.if.001` | 4324 | `if ( IS_NPC(ch) )` |  | pending |
| `act_wiz.do_holylight.return.001` | 4325 | `return;` |  | pending |
| `act_wiz.do_holylight.if.002` | 4327 | `if ( IS_SET(ch->act, PLR_HOLYLIGHT) )` |  | pending |
| `act_wiz.do_holylight.return.002` | 4338 | `return;` |  | pending |

## do_prefi

[Source line 4343](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4343); ends at line 4347. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:351` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:204` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_prefi.return.001` | 4346 | `return;` |  | pending |

## do_prefix

[Source line 4349](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4349); ends at line 4378. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:352` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:205` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `free_string`, `str_dup`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_wiz.do_prefix.if.001` | 4353 | `if (argument[0] == '\0')` |  | pending |
| `act_wiz.do_prefix.if.002` | 4355 | `if (ch->prefix[0] == '\0')` |  | pending |
| `act_wiz.do_prefix.return.001` | 4358 | `return;` |  | pending |
| `act_wiz.do_prefix.return.002` | 4364 | `return;` |  | pending |
| `act_wiz.do_prefix.if.003` | 4367 | `if (ch->prefix[0] != '\0')` |  | pending |

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
- Line 37: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 38: `#include "merc.h"` — pending configuration/reachability review.
- Line 39: `#include "interp.h"` — pending configuration/reachability review.
- Line 40: `#include "recycle.h"` — pending configuration/reachability review.
- Line 41: `#include "tables.h"` — pending configuration/reachability review.
- Line 42: `#include "lookup.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


# src/interp.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `97305b6e1664c0d2abdb58418a6240c3febfadc06562584bc132e1e3200000e9`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## interpret

[Source line 367](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:367); ends at line 511. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_order: `src/act_comm.c:1681` (lexical_call_candidate).
- do_at: `src/act_wiz.c:896` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4132` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4155` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4178` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4219` (lexical_call_candidate).
- substitute_alias: `src/alias.c:64` (lexical_call_candidate).
- substitute_alias: `src/alias.c:95` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2272` (declaration_or_dispatch_reference).

Dependencies: `isspace`, `REMOVE_BIT`, `IS_NPC`, `IS_SET`, `send_to_char`, `strcpy`, `isalpha`, `isdigit`, `one_argument`, `get_trust`, `str_prefix`, `sprintf`, `wiznet`, `log_string`, `write_to_buffer`, `check_social`, `tail_chain`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.interpret.while.001` | 378 | `while ( isspace(*argument) )` |  | pending |
| `interp.interpret.if.001` | 380 | `if ( argument[0] == '\0' )` |  | pending |
| `interp.interpret.return.001` | 381 | `return;` |  | pending |
| `interp.interpret.if.002` | 391 | `if ( !IS_NPC(ch) && IS_SET(ch->act, PLR_FREEZE) )` |  | pending |
| `interp.interpret.and.001` | 391 | `&& IS_SET(ch->act, PLR_FREEZE) )` |  | pending |
| `interp.interpret.return.002` | 394 | `return;` |  | pending |
| `interp.interpret.if.003` | 403 | `if ( !isalpha(argument[0]) && !isdigit(argument[0]) )` |  | pending |
| `interp.interpret.and.002` | 403 | `&& !isdigit(argument[0]) )` |  | pending |
| `interp.interpret.while.002` | 408 | `while ( isspace(*argument) )` |  | pending |
| `interp.interpret.for.001` | 421 | `for ( cmd = 0; cmd_table[cmd].name[0] != '\0'; cmd++ )` |  | pending |
| `interp.interpret.if.004` | 423 | `if ( command[0] == cmd_table[cmd].name[0] 	&&   !str_prefix( command, cmd_table[cmd].name ) 	&&   cmd_table[cmd].level <= trust )` |  | pending |
| `interp.interpret.and.003` | 424 | `&&   !str_prefix( command, cmd_table[cmd].name )` |  | pending |
| `interp.interpret.and.004` | 425 | `&&   cmd_table[cmd].level <= trust )` |  | pending |
| `interp.interpret.break.001` | 428 | `break;` |  | pending |
| `interp.interpret.if.005` | 435 | `if ( cmd_table[cmd].log == LOG_NEVER )` |  | pending |
| `interp.interpret.if.006` | 438 | `if ( ( !IS_NPC(ch) && IS_SET(ch->act, PLR_LOG) )     \|\|   fLogAll     \|\|   cmd_table[cmd].log == LOG_ALWAYS )` |  | pending |
| `interp.interpret.and.005` | 438 | `&& IS_SET(ch->act, PLR_LOG) )` |  | pending |
| `interp.interpret.or.001` | 439 | `\|\|   fLogAll` |  | pending |
| `interp.interpret.or.002` | 440 | `\|\|   cmd_table[cmd].log == LOG_ALWAYS )` |  | pending |
| `interp.interpret.if.007` | 447 | `if ( ch->desc != NULL && ch->desc->snoop_by != NULL )` |  | pending |
| `interp.interpret.and.006` | 447 | `&& ch->desc->snoop_by != NULL )` |  | pending |
| `interp.interpret.if.008` | 454 | `if ( !found )` |  | pending |
| `interp.interpret.if.009` | 459 | `if ( !check_social( ch, command, argument ) )` |  | pending |
| `interp.interpret.return.003` | 461 | `return;` |  | pending |
| `interp.interpret.if.010` | 467 | `if ( ch->position < cmd_table[cmd].position )` |  | pending |
| `interp.interpret.switch.001` | 469 | `switch( ch->position )` |  | pending |
| `interp.interpret.case.001` | 471 | `case POS_DEAD:` |  | pending |
| `interp.interpret.break.002` | 473 | `break;` |  | pending |
| `interp.interpret.case.002` | 475 | `case POS_MORTAL:` |  | pending |
| `interp.interpret.case.003` | 476 | `case POS_INCAP:` |  | pending |
| `interp.interpret.break.003` | 478 | `break;` |  | pending |
| `interp.interpret.case.004` | 480 | `case POS_STUNNED:` |  | pending |
| `interp.interpret.break.004` | 482 | `break;` |  | pending |
| `interp.interpret.case.005` | 484 | `case POS_SLEEPING:` |  | pending |
| `interp.interpret.break.005` | 486 | `break;` |  | pending |
| `interp.interpret.case.006` | 488 | `case POS_RESTING:` |  | pending |
| `interp.interpret.break.006` | 490 | `break;` |  | pending |
| `interp.interpret.case.007` | 492 | `case POS_SITTING:` |  | pending |
| `interp.interpret.break.007` | 494 | `break;` |  | pending |
| `interp.interpret.case.008` | 496 | `case POS_FIGHTING:` |  | pending |
| `interp.interpret.break.008` | 498 | `break;` |  | pending |
| `interp.interpret.return.004` | 501 | `return;` |  | pending |
| `interp.interpret.return.005` | 510 | `return;` |  | pending |

## do_function

[Source line 514](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:514); ends at line 526. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_delete: `src/act_comm.c:71` (lexical_call_candidate).
- do_enter: `src/act_enter.c:151` (lexical_call_candidate).
- do_enter: `src/act_enter.c:175` (lexical_call_candidate).
- do_enter: `src/act_enter.c:191` (lexical_call_candidate).
- do_motd: `src/act_info.c:613` (lexical_call_candidate).
- do_imotd: `src/act_info.c:618` (lexical_call_candidate).
- do_rules: `src/act_info.c:623` (lexical_call_candidate).
- do_story: `src/act_info.c:628` (lexical_call_candidate).
- do_wizlist: `src/act_info.c:633` (lexical_call_candidate).
- do_look: `src/act_info.c:1048` (lexical_call_candidate).
- do_read: `src/act_info.c:1244` (lexical_call_candidate).
- do_examine: `src/act_info.c:1261` (lexical_call_candidate).
- do_examine: `src/act_info.c:1271` (lexical_call_candidate).
- do_examine: `src/act_info.c:1305` (lexical_call_candidate).
- do_score: `src/act_info.c:1620` (lexical_call_candidate).
- do_credits: `src/act_info.c:2251` (lexical_call_candidate).
- move_char: `src/act_move.c:202` (lexical_call_candidate).
- move_char: `src/act_move.c:213` (lexical_call_candidate).
- do_stand: `src/act_move.c:933` (lexical_call_candidate).
- do_wake: `src/act_move.c:1314` (lexical_call_candidate).
- do_wake: `src/act_move.c:1329` (lexical_call_candidate).
- do_recall: `src/act_move.c:1461` (lexical_call_candidate).
- do_recall: `src/act_move.c:1464` (lexical_call_candidate).
- get_obj: `src/act_obj.c:176` (lexical_call_candidate).
- do_give: `src/act_obj.c:746` (lexical_call_candidate).
- do_give: `src/act_obj.c:752` (lexical_call_candidate).
- do_give: `src/act_obj.c:757` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1827` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2216` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2218` (lexical_call_candidate).
- find_keeper: `src/act_obj.c:2356` (lexical_call_candidate).
- find_keeper: `src/act_obj.c:2362` (lexical_call_candidate).
- find_keeper: `src/act_obj.c:2371` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:535` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:808` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:857` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:976` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:1032` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1059` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1065` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1071` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1080` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1087` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1094` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1744` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1750` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1756` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1760` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1761` (lexical_call_candidate).
- do_reboot: `src/act_wiz.c:2015` (lexical_call_candidate).
- do_shutdown: `src/act_wiz.c:2050` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2447` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2453` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2457` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3222` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3228` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3234` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3240` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3244` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3696` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3859` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3970` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4039` (lexical_call_candidate).
- nanny: `src/comm.c:1673` (lexical_call_candidate).
- nanny: `src/comm.c:1678` (lexical_call_candidate).
- nanny: `src/comm.c:1816` (lexical_call_candidate).
- nanny: `src/comm.c:1818` (lexical_call_candidate).
- nanny: `src/comm.c:1949` (lexical_call_candidate).
- nanny: `src/comm.c:1952` (lexical_call_candidate).
- nanny: `src/comm.c:1953` (lexical_call_candidate).
- nanny: `src/comm.c:1999` (lexical_call_candidate).
- nanny: `src/comm.c:2053` (lexical_call_candidate).
- nanny: `src/comm.c:2058` (lexical_call_candidate).
- nanny: `src/comm.c:2096` (lexical_call_candidate).
- nanny: `src/comm.c:2101` (lexical_call_candidate).
- nanny: `src/comm.c:2118` (lexical_call_candidate).
- nanny: `src/comm.c:2129` (lexical_call_candidate).
- check_assist: `src/fight.c:114` (lexical_call_candidate).
- check_assist: `src/fight.c:174` (lexical_call_candidate).
- mob_hit: `src/fight.c:328` (lexical_call_candidate).
- mob_hit: `src/fight.c:333` (lexical_call_candidate).
- mob_hit: `src/fight.c:342` (lexical_call_candidate).
- mob_hit: `src/fight.c:347` (lexical_call_candidate).
- mob_hit: `src/fight.c:352` (lexical_call_candidate).
- mob_hit: `src/fight.c:364` (lexical_call_candidate).
- mob_hit: `src/fight.c:376` (lexical_call_candidate).
- damage: `src/fight.c:919` (lexical_call_candidate).
- damage: `src/fight.c:929` (lexical_call_candidate).
- damage: `src/fight.c:941` (lexical_call_candidate).
- damage: `src/fight.c:959` (lexical_call_candidate).
- damage: `src/fight.c:974` (lexical_call_candidate).
- damage: `src/fight.c:983` (lexical_call_candidate).
- do_murder: `src/fight.c:2719` (lexical_call_candidate).
- extract_char: `src/handler.c:1969` (lexical_call_candidate).
- spell_gate: `src/magic.c:2917` (lexical_call_candidate).
- spell_gate: `src/magic.c:2926` (lexical_call_candidate).
- spell_summon: `src/magic.c:4346` (lexical_call_candidate).
- spell_teleport: `src/magic.c:4377` (lexical_call_candidate).
- spell_word_of_recall: `src/magic.c:4461` (lexical_call_candidate).
- spell_farsight: `src/magic2.c:52` (lexical_call_candidate).
- do_gain: `src/skills.c:71` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:675` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:679` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:804` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:822` (lexical_call_candidate).
- spec_nasty: `src/special.c:340` (lexical_call_candidate).
- spec_nasty: `src/special.c:343` (lexical_call_candidate).
- spec_nasty: `src/special.c:370` (lexical_call_candidate).
- spec_executioner: `src/special.c:751` (lexical_call_candidate).
- spec_guard: `src/special.c:832` (lexical_call_candidate).
- spec_mayor: `src/special.c:962` (lexical_call_candidate).
- spec_mayor: `src/special.c:966` (lexical_call_candidate).
- char_update: `src/update.c:835` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/interp.h:31` (declaration_or_dispatch_reference).

Dependencies: `str_dup`, `free_string`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.do_function.entry` | 514 | `Straight-line entry` |  | pending |

## check_social

[Source line 528](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:528); ends at line 633. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- interpret: `src/interp.c:459` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/interp.c:42` (declaration_or_dispatch_reference).

Dependencies: `str_prefix`, `IS_NPC`, `IS_SET`, `send_to_char`, `str_cmp`, `one_argument`, `act`, `get_char_room`, `IS_AFFECTED`, `IS_AWAKE`, `number_bits`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.check_social.for.001` | 536 | `for ( cmd = 0; social_table[cmd].name[0] != '\0'; cmd++ )` |  | pending |
| `interp.check_social.if.001` | 538 | `if ( command[0] == social_table[cmd].name[0] 	&&   !str_prefix( command, social_table[cmd].name ) )` |  | pending |
| `interp.check_social.and.001` | 539 | `&&   !str_prefix( command, social_table[cmd].name ) )` |  | pending |
| `interp.check_social.break.001` | 542 | `break;` |  | pending |
| `interp.check_social.if.002` | 546 | `if ( !found )` |  | pending |
| `interp.check_social.return.001` | 547 | `return FALSE;` |  | pending |
| `interp.check_social.if.003` | 549 | `if ( !IS_NPC(ch) && IS_SET(ch->comm, COMM_NOEMOTE) )` |  | pending |
| `interp.check_social.and.002` | 549 | `&& IS_SET(ch->comm, COMM_NOEMOTE) )` |  | pending |
| `interp.check_social.return.002` | 552 | `return TRUE;` |  | pending |
| `interp.check_social.switch.001` | 555 | `switch ( ch->position )` |  | pending |
| `interp.check_social.case.001` | 557 | `case POS_DEAD:` |  | pending |
| `interp.check_social.return.003` | 559 | `return TRUE;` |  | pending |
| `interp.check_social.case.002` | 561 | `case POS_INCAP:` |  | pending |
| `interp.check_social.case.003` | 562 | `case POS_MORTAL:` |  | pending |
| `interp.check_social.return.004` | 564 | `return TRUE;` |  | pending |
| `interp.check_social.case.004` | 566 | `case POS_STUNNED:` |  | pending |
| `interp.check_social.return.005` | 568 | `return TRUE;` |  | pending |
| `interp.check_social.case.005` | 570 | `case POS_SLEEPING:` |  | pending |
| `interp.check_social.if.004` | 575 | `if ( !str_cmp( social_table[cmd].name, "snore" ) )` |  | pending |
| `interp.check_social.break.002` | 576 | `break;` |  | pending |
| `interp.check_social.return.006` | 578 | `return TRUE;` |  | pending |
| `interp.check_social.if.005` | 584 | `if ( arg[0] == '\0' )` |  | pending |
| `interp.check_social.if.006` | 589 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `interp.check_social.if.007` | 593 | `if ( victim == ch )` |  | pending |
| `interp.check_social.if.008` | 604 | `if ( !IS_NPC(ch) && IS_NPC(victim) 	&&   !IS_AFFECTED(victim, AFF_CHARM) 	&&   IS_AWAKE(victim)  	&&   victim->desc == NULL)` |  | pending |
| `interp.check_social.and.003` | 604 | `&& IS_NPC(victim)` |  | pending |
| `interp.check_social.and.004` | 605 | `&&   !IS_AFFECTED(victim, AFF_CHARM)` |  | pending |
| `interp.check_social.and.005` | 606 | `&&   IS_AWAKE(victim)` |  | pending |
| `interp.check_social.and.006` | 607 | `&&   victim->desc == NULL)` |  | pending |
| `interp.check_social.switch.002` | 609 | `switch ( number_bits( 4 ) )` |  | pending |
| `interp.check_social.case.006` | 611 | `case 0:` |  | pending |
| `interp.check_social.case.007` | 613 | `case 1: case 2: case 3: case 4:` |  | pending |
| `interp.check_social.case.008` | 613 | `case 2: case 3: case 4:` |  | pending |
| `interp.check_social.case.009` | 613 | `case 3: case 4:` |  | pending |
| `interp.check_social.case.010` | 613 | `case 4:` |  | pending |
| `interp.check_social.case.011` | 614 | `case 5: case 6: case 7: case 8:` |  | pending |
| `interp.check_social.case.012` | 614 | `case 6: case 7: case 8:` |  | pending |
| `interp.check_social.case.013` | 614 | `case 7: case 8:` |  | pending |
| `interp.check_social.case.014` | 614 | `case 8:` |  | pending |
| `interp.check_social.break.003` | 621 | `break;` |  | pending |
| `interp.check_social.case.015` | 623 | `case 9: case 10: case 11: case 12:` |  | pending |
| `interp.check_social.case.016` | 623 | `case 10: case 11: case 12:` |  | pending |
| `interp.check_social.case.017` | 623 | `case 11: case 12:` |  | pending |
| `interp.check_social.case.018` | 623 | `case 12:` |  | pending |
| `interp.check_social.break.004` | 627 | `break;` |  | pending |
| `interp.check_social.return.007` | 632 | `return TRUE;` |  | pending |

## is_number

[Source line 640](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:640); ends at line 656. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_scroll: `src/act_info.c:559` (lexical_call_candidate).
- do_who: `src/act_info.c:1938` (lexical_call_candidate).
- do_drop: `src/act_obj.c:505` (lexical_call_candidate).
- do_give: `src/act_obj.c:671` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:555` (lexical_call_candidate).
- find_location: `src/act_wiz.c:766` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2470` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2503` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2513` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2635` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2725` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3294` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3361` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4014` (lexical_call_candidate).
- main: `src/comm.c:394` (lexical_call_candidate).
- parse_note: `src/note.c:620` (lexical_call_candidate).
- parse_note: `src/note.c:695` (lexical_call_candidate).
- parse_note: `src/note.c:720` (lexical_call_candidate).
- do_spells: `src/skills.c:275` (lexical_call_candidate).
- do_spells: `src/skills.c:292` (lexical_call_candidate).
- do_skills: `src/skills.c:395` (lexical_call_candidate).
- do_skills: `src/skills.c:412` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2273` (declaration_or_dispatch_reference).

Dependencies: `isdigit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.is_number.if.001` | 643 | `if ( *arg == '\0' )` |  | pending |
| `interp.is_number.return.001` | 644 | `return FALSE;` |  | pending |
| `interp.is_number.if.002` | 646 | `if ( *arg == '+' \|\| *arg == '-' )` |  | pending |
| `interp.is_number.or.001` | 646 | `\|\| *arg == '-' )` |  | pending |
| `interp.is_number.for.001` | 649 | `for ( ; *arg != '\0'; arg++ )` |  | pending |
| `interp.is_number.if.003` | 651 | `if ( !isdigit( *arg ) )` |  | pending |
| `interp.is_number.return.002` | 652 | `return FALSE;` |  | pending |
| `interp.is_number.return.003` | 655 | `return TRUE;` |  | pending |

## number_argument

[Source line 663](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:663); ends at line 682. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_look: `src/act_info.c:1022` (lexical_call_candidate).
- get_obj_keeper: `src/act_obj.c:2428` (lexical_call_candidate).
- get_char_room: `src/handler.c:2021` (lexical_call_candidate).
- get_char_world: `src/handler.c:2052` (lexical_call_candidate).
- get_obj_list: `src/handler.c:2096` (lexical_call_candidate).
- get_obj_carry: `src/handler.c:2122` (lexical_call_candidate).
- get_obj_wear: `src/handler.c:2150` (lexical_call_candidate).
- get_obj_world: `src/handler.c:2203` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2274` (declaration_or_dispatch_reference).

Dependencies: `atoi`, `strcpy`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.number_argument.for.001` | 668 | `for ( pdot = argument; *pdot != '\0'; pdot++ )` |  | pending |
| `interp.number_argument.if.001` | 670 | `if ( *pdot == '.' )` |  | pending |
| `interp.number_argument.return.001` | 676 | `return number;` |  | pending |
| `interp.number_argument.return.002` | 681 | `return 1;` |  | pending |

## mult_argument

[Source line 687](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:687); ends at line 706. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_buy: `src/act_obj.c:2622` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2275` (declaration_or_dispatch_reference).

Dependencies: `atoi`, `strcpy`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.mult_argument.for.001` | 692 | `for ( pdot = argument; *pdot != '\0'; pdot++ )` |  | pending |
| `interp.mult_argument.if.001` | 694 | `if ( *pdot == '*' )` |  | pending |
| `interp.mult_argument.return.001` | 700 | `return number;` |  | pending |
| `interp.mult_argument.return.002` | 705 | `return 1;` |  | pending |

## one_argument

[Source line 714](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:714); ends at line 742. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_tell: `src/act_comm.c:835` (lexical_call_candidate).
- do_follow: `src/act_comm.c:1469` (lexical_call_candidate).
- do_order: `src/act_comm.c:1620` (lexical_call_candidate).
- do_order: `src/act_comm.c:1621` (lexical_call_candidate).
- do_group: `src/act_comm.c:1703` (lexical_call_candidate).
- do_split: `src/act_comm.c:1798` (lexical_call_candidate).
- do_split: `src/act_comm.c:1799` (lexical_call_candidate).
- do_scroll: `src/act_info.c:544` (lexical_call_candidate).
- do_look: `src/act_info.c:1020` (lexical_call_candidate).
- do_look: `src/act_info.c:1021` (lexical_call_candidate).
- do_examine: `src/act_info.c:1253` (lexical_call_candidate).
- do_help: `src/act_info.c:1762` (lexical_call_candidate).
- do_whois: `src/act_info.c:1819` (lexical_call_candidate).
- do_who: `src/act_info.c:1934` (lexical_call_candidate).
- do_compare: `src/act_info.c:2159` (lexical_call_candidate).
- do_compare: `src/act_info.c:2160` (lexical_call_candidate).
- do_where: `src/act_info.c:2265` (lexical_call_candidate).
- do_consider: `src/act_info.c:2328` (lexical_call_candidate).
- do_wimpy: `src/act_info.c:2635` (lexical_call_candidate).
- do_open: `src/act_move.c:335` (lexical_call_candidate).
- do_close: `src/act_move.c:429` (lexical_call_candidate).
- do_lock: `src/act_move.c:530` (lexical_call_candidate).
- do_unlock: `src/act_move.c:638` (lexical_call_candidate).
- do_pick: `src/act_move.c:747` (lexical_call_candidate).
- do_wake: `src/act_move.c:1312` (lexical_call_candidate).
- do_get: `src/act_obj.c:201` (lexical_call_candidate).
- do_get: `src/act_obj.c:202` (lexical_call_candidate).
- do_get: `src/act_obj.c:205` (lexical_call_candidate).
- do_put: `src/act_obj.c:352` (lexical_call_candidate).
- do_put: `src/act_obj.c:353` (lexical_call_candidate).
- do_put: `src/act_obj.c:356` (lexical_call_candidate).
- do_drop: `src/act_obj.c:497` (lexical_call_candidate).
- do_drop: `src/act_obj.c:511` (lexical_call_candidate).
- do_give: `src/act_obj.c:662` (lexical_call_candidate).
- do_give: `src/act_obj.c:663` (lexical_call_candidate).
- do_give: `src/act_obj.c:688` (lexical_call_candidate).
- do_fill: `src/act_obj.c:949` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1016` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1143` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1264` (lexical_call_candidate).
- do_wear: `src/act_obj.c:1678` (lexical_call_candidate).
- do_remove: `src/act_obj.c:1719` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1752` (lexical_call_candidate).
- do_quaff: `src/act_obj.c:1845` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1892` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1893` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2048` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2143` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2144` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2528` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2591` (lexical_call_candidate).
- do_list: `src/act_obj.c:2798` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2853` (lexical_call_candidate).
- do_value: `src/act_obj.c:2945` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:184` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:185` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:300` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:503` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:548` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:606` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:607` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:736` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:788` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:789` (lexical_call_candidate).
- do_at: `src/act_wiz.c:871` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1046` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1110` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1165` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1174` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1211` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1531` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1731` (lexical_call_candidate).
- do_mfind: `src/act_wiz.c:1776` (lexical_call_candidate).
- do_ofind: `src/act_wiz.c:1827` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2103` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2183` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2319` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2435` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2468` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2500` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2501` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2553` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2632` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2633` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2722` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2723` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2763` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2848` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2903` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2962` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3010` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3063` (lexical_call_candidate).
- do_slookup: `src/act_wiz.c:3168` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3208` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3258` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3259` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3260` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3334` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3335` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3710` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3711` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3712` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3837` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3873` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3874` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:3985` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:3986` (lexical_call_candidate).
- do_sockets: `src/act_wiz.c:4056` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4096` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4104` (lexical_call_candidate).
- do_invis: `src/act_wiz.c:4237` (lexical_call_candidate).
- do_incognito: `src/act_wiz.c:4282` (lexical_call_candidate).
- substitute_alias: `src/alias.c:77` (lexical_call_candidate).
- do_alias: `src/alias.c:120` (lexical_call_candidate).
- do_unalias: `src/alias.c:223` (lexical_call_candidate).
- ban_site: `src/ban.c:146` (lexical_call_candidate).
- ban_site: `src/ban.c:147` (lexical_call_candidate).
- do_allow: `src/ban.c:273` (lexical_call_candidate).
- nanny: `src/comm.c:1810` (lexical_call_candidate).
- nanny: `src/comm.c:1814` (lexical_call_candidate).
- show_string: `src/comm.c:2378` (lexical_call_candidate).
- act_new: `src/comm.c:2540` (lexical_call_candidate).
- load_old_mob: `src/db.c:544` (lexical_call_candidate).
- do_bash: `src/fight.c:2214` (lexical_call_candidate).
- do_dirt: `src/fight.c:2345` (lexical_call_candidate).
- do_trip: `src/fight.c:2478` (lexical_call_candidate).
- do_kill: `src/fight.c:2593` (lexical_call_candidate).
- do_murder: `src/fight.c:2668` (lexical_call_candidate).
- do_backstab: `src/fight.c:2733` (lexical_call_candidate).
- do_rescue: `src/fight.c:2869` (lexical_call_candidate).
- do_slay: `src/fight.c:3065` (lexical_call_candidate).
- do_flag: `src/flags.c:52` (lexical_call_candidate).
- do_flag: `src/flags.c:53` (lexical_call_candidate).
- do_flag: `src/flags.c:54` (lexical_call_candidate).
- do_flag: `src/flags.c:59` (lexical_call_candidate).
- do_flag: `src/flags.c:200` (lexical_call_candidate).
- is_name: `src/handler.c:826` (lexical_call_candidate).
- is_name: `src/handler.c:835` (lexical_call_candidate).
- is_exact_name: `src/handler.c:857` (lexical_call_candidate).
- do_heal: `src/healer.c:62` (lexical_call_candidate).
- interpret: `src/interp.c:413` (lexical_call_candidate).
- check_social: `src/interp.c:582` (lexical_call_candidate).
- do_cast: `src/magic.c:314` (lexical_call_candidate).
- do_cast: `src/magic.c:315` (lexical_call_candidate).
- spell_ventriloquate: `src/magic.c:4390` (lexical_call_candidate).
- do_play: `src/music.c:225` (lexical_call_candidate).
- do_play: `src/music.c:252` (lexical_call_candidate).
- note_remove: `src/note.c:402` (lexical_call_candidate).
- parse_note: `src/note.c:580` (lexical_call_candidate).
- do_scan: `src/scan.c:56` (lexical_call_candidate).
- do_gain: `src/skills.c:67` (lexical_call_candidate).
- do_spells: `src/skills.c:274` (lexical_call_candidate).
- do_spells: `src/skills.c:291` (lexical_call_candidate).
- do_skills: `src/skills.c:394` (lexical_call_candidate).
- do_skills: `src/skills.c:411` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:669` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2276` (declaration_or_dispatch_reference).

Dependencies: `isspace`, `LOWER`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.one_argument.while.001` | 718 | `while ( isspace(*argument) )` | interp.one_argument.empty, interp.one_argument.leading-spaces, interp.one_argument.single-quotes, interp.one_argument.double-quotes, interp.one_argument.unclosed-quote, interp.one_argument.empty-quoted-token, interp.one_argument.embedded-tab, interp.one_argument.trailing-whitespace, interp.one_argument.whitespace-only, interp.one_argument.tab-leading, interp.one_argument.quote-followed-without-space, interp.one_argument.embedded-quote-unquoted, interp.one_argument.quoted-tab-preserved, interp.one_argument.one-character-token, interp.one_argument.max-fitting-token | specified |
| `interp.one_argument.if.001` | 722 | `if ( *argument == '\'' \|\| *argument == '"' )` | interp.one_argument.empty, interp.one_argument.leading-spaces, interp.one_argument.single-quotes, interp.one_argument.double-quotes, interp.one_argument.unclosed-quote, interp.one_argument.empty-quoted-token, interp.one_argument.embedded-tab, interp.one_argument.trailing-whitespace, interp.one_argument.whitespace-only, interp.one_argument.tab-leading, interp.one_argument.quote-followed-without-space, interp.one_argument.embedded-quote-unquoted, interp.one_argument.quoted-tab-preserved, interp.one_argument.one-character-token, interp.one_argument.max-fitting-token | specified |
| `interp.one_argument.or.001` | 722 | `\|\| *argument == '"' )` | interp.one_argument.empty, interp.one_argument.leading-spaces, interp.one_argument.single-quotes, interp.one_argument.double-quotes, interp.one_argument.unclosed-quote, interp.one_argument.empty-quoted-token, interp.one_argument.embedded-tab, interp.one_argument.trailing-whitespace, interp.one_argument.whitespace-only, interp.one_argument.tab-leading, interp.one_argument.quote-followed-without-space, interp.one_argument.embedded-quote-unquoted, interp.one_argument.quoted-tab-preserved, interp.one_argument.one-character-token, interp.one_argument.max-fitting-token | specified |
| `interp.one_argument.while.002` | 725 | `while ( *argument != '\0' )` | interp.one_argument.empty, interp.one_argument.leading-spaces, interp.one_argument.single-quotes, interp.one_argument.double-quotes, interp.one_argument.unclosed-quote, interp.one_argument.empty-quoted-token, interp.one_argument.embedded-tab, interp.one_argument.trailing-whitespace, interp.one_argument.whitespace-only, interp.one_argument.tab-leading, interp.one_argument.quote-followed-without-space, interp.one_argument.embedded-quote-unquoted, interp.one_argument.quoted-tab-preserved, interp.one_argument.one-character-token, interp.one_argument.max-fitting-token | specified |
| `interp.one_argument.if.002` | 727 | `if ( *argument == cEnd )` | interp.one_argument.leading-spaces, interp.one_argument.single-quotes, interp.one_argument.double-quotes, interp.one_argument.unclosed-quote, interp.one_argument.empty-quoted-token, interp.one_argument.embedded-tab, interp.one_argument.trailing-whitespace, interp.one_argument.tab-leading, interp.one_argument.quote-followed-without-space, interp.one_argument.embedded-quote-unquoted, interp.one_argument.quoted-tab-preserved, interp.one_argument.one-character-token, interp.one_argument.max-fitting-token | specified |
| `interp.one_argument.break.001` | 730 | `break;` | interp.one_argument.leading-spaces, interp.one_argument.single-quotes, interp.one_argument.double-quotes, interp.one_argument.empty-quoted-token, interp.one_argument.embedded-tab, interp.one_argument.trailing-whitespace, interp.one_argument.tab-leading, interp.one_argument.quote-followed-without-space, interp.one_argument.embedded-quote-unquoted, interp.one_argument.quoted-tab-preserved | specified |
| `interp.one_argument.while.003` | 738 | `while ( isspace(*argument) )` | interp.one_argument.empty, interp.one_argument.leading-spaces, interp.one_argument.single-quotes, interp.one_argument.double-quotes, interp.one_argument.unclosed-quote, interp.one_argument.empty-quoted-token, interp.one_argument.embedded-tab, interp.one_argument.trailing-whitespace, interp.one_argument.whitespace-only, interp.one_argument.tab-leading, interp.one_argument.quote-followed-without-space, interp.one_argument.embedded-quote-unquoted, interp.one_argument.quoted-tab-preserved, interp.one_argument.one-character-token, interp.one_argument.max-fitting-token | specified |
| `interp.one_argument.return.001` | 741 | `return argument;` | interp.one_argument.empty, interp.one_argument.leading-spaces, interp.one_argument.single-quotes, interp.one_argument.double-quotes, interp.one_argument.unclosed-quote, interp.one_argument.empty-quoted-token, interp.one_argument.embedded-tab, interp.one_argument.trailing-whitespace, interp.one_argument.whitespace-only, interp.one_argument.tab-leading, interp.one_argument.quote-followed-without-space, interp.one_argument.embedded-quote-unquoted, interp.one_argument.quoted-tab-preserved, interp.one_argument.one-character-token, interp.one_argument.max-fitting-token | specified |
| `interp.one_argument.empty.path` | 721 | `empty` | interp.one_argument.empty | specified |
| `interp.one_argument.leading-spaces.path` | 721 | `leading spaces` | interp.one_argument.leading-spaces | specified |
| `interp.one_argument.single-quotes.path` | 721 | `single quotes` | interp.one_argument.single-quotes | specified |
| `interp.one_argument.double-quotes.path` | 721 | `double quotes` | interp.one_argument.double-quotes | specified |
| `interp.one_argument.unclosed-quote.path` | 721 | `unclosed quote` | interp.one_argument.unclosed-quote | specified |
| `interp.one_argument.empty-quoted-token.path` | 721 | `empty quoted token` | interp.one_argument.empty-quoted-token | specified |
| `interp.one_argument.embedded-tab.path` | 721 | `embedded tab` | interp.one_argument.embedded-tab | specified |
| `interp.one_argument.trailing-whitespace.path` | 721 | `trailing whitespace` | interp.one_argument.trailing-whitespace | specified |
| `interp.one_argument.whitespace-only.path` | 721 | `whitespace only` | interp.one_argument.whitespace-only | specified |
| `interp.one_argument.tab-leading.path` | 721 | `tab leading` | interp.one_argument.tab-leading | specified |
| `interp.one_argument.quote-followed-without-space.path` | 721 | `quote followed without space` | interp.one_argument.quote-followed-without-space | specified |
| `interp.one_argument.embedded-quote-unquoted.path` | 721 | `embedded quote unquoted` | interp.one_argument.embedded-quote-unquoted | specified |
| `interp.one_argument.quoted-tab-preserved.path` | 721 | `quoted tab preserved` | interp.one_argument.quoted-tab-preserved | specified |
| `interp.one_argument.one-character-token.path` | 721 | `one character token` | interp.one_argument.one-character-token | specified |
| `interp.one_argument.max-fitting-token.path` | 721 | `max fitting token` | interp.one_argument.max-fitting-token | specified |
| `interp.one_argument.output-buffer-overflow.path` | 736 | `output buffer overflow` | interp.one_argument.output-buffer-overflow | blocked |

## do_commands

[Source line 747](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:747); ends at line 770. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:114` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:101` (declaration_or_dispatch_reference).

Dependencies: `get_trust`, `sprintf`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.do_commands.for.001` | 754 | `for ( cmd = 0; cmd_table[cmd].name[0] != '\0'; cmd++ )` |  | pending |
| `interp.do_commands.if.001` | 756 | `if ( cmd_table[cmd].level <  LEVEL_HERO         &&   cmd_table[cmd].level <= get_trust( ch )  	&&   cmd_table[cmd].show)` |  | pending |
| `interp.do_commands.and.001` | 757 | `&&   cmd_table[cmd].level <= get_trust( ch )` |  | pending |
| `interp.do_commands.and.002` | 758 | `&&   cmd_table[cmd].show)` |  | pending |
| `interp.do_commands.if.002` | 762 | `if ( ++col % 6 == 0 )` |  | pending |
| `interp.do_commands.if.003` | 767 | `if ( col % 6 != 0 )` |  | pending |
| `interp.do_commands.return.001` | 769 | `return;` |  | pending |

## do_wizhelp

[Source line 772](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:772); ends at line 795. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:105` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:291` (declaration_or_dispatch_reference).

Dependencies: `get_trust`, `sprintf`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `interp.do_wizhelp.for.001` | 779 | `for ( cmd = 0; cmd_table[cmd].name[0] != '\0'; cmd++ )` |  | pending |
| `interp.do_wizhelp.if.001` | 781 | `if ( cmd_table[cmd].level >= LEVEL_HERO         &&   cmd_table[cmd].level <= get_trust( ch )          &&   cmd_table[cmd].show)` |  | pending |
| `interp.do_wizhelp.and.001` | 782 | `&&   cmd_table[cmd].level <= get_trust( ch )` |  | pending |
| `interp.do_wizhelp.and.002` | 783 | `&&   cmd_table[cmd].show)` |  | pending |
| `interp.do_wizhelp.if.002` | 787 | `if ( ++col % 6 == 0 )` |  | pending |
| `interp.do_wizhelp.if.003` | 792 | `if ( col % 6 != 0 )` |  | pending |
| `interp.do_wizhelp.return.001` | 794 | `return;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#endif` — pending configuration/reachability review.
- Line 33: `#include <ctype.h>` — pending configuration/reachability review.
- Line 34: `#include <stdio.h>` — pending configuration/reachability review.
- Line 35: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 36: `#include <string.h>` — pending configuration/reachability review.
- Line 37: `#include <time.h>` — pending configuration/reachability review.
- Line 38: `#include "merc.h"` — pending configuration/reachability review.
- Line 39: `#include "interp.h"` — pending configuration/reachability review.
- Line 48: `#define LOG_NORMAL	0` — pending configuration/reachability review.
- Line 49: `#define LOG_ALWAYS	1` — pending configuration/reachability review.
- Line 50: `#define LOG_NEVER	2` — pending configuration/reachability review.

## Static tables

- `cmd_table` at line 64 — pending entry/termination review.

## Commented code candidates


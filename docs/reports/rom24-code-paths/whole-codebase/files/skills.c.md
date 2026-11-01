# src/skills.c

Role: translation_unit. Disposition: **pending**. SHA-256: `aa4959028cb9db55947e224eea32d6488b38675904d8b67ccea3bf3e4fa95963`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## do_gain

[Source line 44](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:44); ends at line 248. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:256` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:135` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `can_see`, `send_to_char`, `one_argument`, `do_function`, `str_prefix`, `sprintf`, `act`, `exp_per_level`, `group_lookup`, `gn_add`, `skill_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.do_gain.if.001` | 51 | `if (IS_NPC(ch))` |  | pending |
| `skills.do_gain.return.001` | 52 | `return;` |  | pending |
| `skills.do_gain.for.001` | 55 | `for ( trainer = ch->in_room->people;  	  trainer != NULL;  	  trainer = trainer->next_in_room)` |  | pending |
| `skills.do_gain.if.002` | 58 | `if (IS_NPC(trainer) && IS_SET(trainer->act,ACT_GAIN))` |  | pending |
| `skills.do_gain.and.001` | 58 | `&& IS_SET(trainer->act,ACT_GAIN))` |  | pending |
| `skills.do_gain.break.001` | 59 | `break;` |  | pending |
| `skills.do_gain.if.003` | 61 | `if (trainer == NULL \|\| !can_see(ch,trainer))` |  | pending |
| `skills.do_gain.or.001` | 61 | `\|\| !can_see(ch,trainer))` |  | pending |
| `skills.do_gain.return.002` | 64 | `return;` |  | pending |
| `skills.do_gain.if.004` | 69 | `if (arg[0] == '\0')` |  | pending |
| `skills.do_gain.return.003` | 72 | `return;` |  | pending |
| `skills.do_gain.if.005` | 75 | `if (!str_prefix(arg,"list"))` |  | pending |
| `skills.do_gain.for.002` | 85 | `for (gn = 0; gn < MAX_GROUP; gn++)` |  | pending |
| `skills.do_gain.if.006` | 87 | `if (group_table[gn].name == NULL)` |  | pending |
| `skills.do_gain.break.002` | 88 | `break;` |  | pending |
| `skills.do_gain.if.007` | 90 | `if (!ch->pcdata->group_known[gn] 	    &&  group_table[gn].rating[ch->class] > 0)` |  | pending |
| `skills.do_gain.and.002` | 91 | `&&  group_table[gn].rating[ch->class] > 0)` |  | pending |
| `skills.do_gain.if.008` | 96 | `if (++col % 3 == 0)` |  | pending |
| `skills.do_gain.if.009` | 100 | `if (col % 3 != 0)` |  | pending |
| `skills.do_gain.for.003` | 111 | `for (sn = 0; sn < MAX_SKILL; sn++)` |  | pending |
| `skills.do_gain.if.010` | 113 | `if (skill_table[sn].name == NULL)` |  | pending |
| `skills.do_gain.break.003` | 114 | `break;` |  | pending |
| `skills.do_gain.if.011` | 116 | `if (!ch->pcdata->learned[sn]             &&  skill_table[sn].rating[ch->class] > 0 	    &&  skill_table[sn].spell_fun == spell_null)` |  | pending |
| `skills.do_gain.and.003` | 117 | `&&  skill_table[sn].rating[ch->class] > 0` |  | pending |
| `skills.do_gain.and.004` | 118 | `&&  skill_table[sn].spell_fun == spell_null)` |  | pending |
| `skills.do_gain.if.012` | 123 | `if (++col % 3 == 0)` |  | pending |
| `skills.do_gain.if.013` | 127 | `if (col % 3 != 0)` |  | pending |
| `skills.do_gain.return.004` | 129 | `return;` |  | pending |
| `skills.do_gain.if.014` | 132 | `if (!str_prefix(arg,"convert"))` |  | pending |
| `skills.do_gain.if.015` | 134 | `if (ch->practice < 10)` |  | pending |
| `skills.do_gain.return.005` | 138 | `return;` |  | pending |
| `skills.do_gain.return.006` | 145 | `return;` |  | pending |
| `skills.do_gain.if.016` | 148 | `if (!str_prefix(arg,"points"))` |  | pending |
| `skills.do_gain.if.017` | 150 | `if (ch->train < 2)` |  | pending |
| `skills.do_gain.return.007` | 154 | `return;` |  | pending |
| `skills.do_gain.if.018` | 157 | `if (ch->pcdata->points <= 40)` |  | pending |
| `skills.do_gain.return.008` | 161 | `return;` |  | pending |
| `skills.do_gain.return.009` | 170 | `return;` |  | pending |
| `skills.do_gain.if.019` | 176 | `if (gn > 0)` |  | pending |
| `skills.do_gain.if.020` | 178 | `if (ch->pcdata->group_known[gn])` |  | pending |
| `skills.do_gain.return.010` | 182 | `return;` |  | pending |
| `skills.do_gain.if.021` | 185 | `if (group_table[gn].rating[ch->class] <= 0)` |  | pending |
| `skills.do_gain.return.011` | 189 | `return;` |  | pending |
| `skills.do_gain.if.022` | 192 | `if (ch->train < group_table[gn].rating[ch->class])` |  | pending |
| `skills.do_gain.return.012` | 196 | `return;` |  | pending |
| `skills.do_gain.return.013` | 204 | `return;` |  | pending |
| `skills.do_gain.if.023` | 208 | `if (sn > -1)` |  | pending |
| `skills.do_gain.if.024` | 210 | `if (skill_table[sn].spell_fun != spell_null)` |  | pending |
| `skills.do_gain.return.014` | 214 | `return;` |  | pending |
| `skills.do_gain.if.025` | 218 | `if (ch->pcdata->learned[sn])` |  | pending |
| `skills.do_gain.return.015` | 222 | `return;` |  | pending |
| `skills.do_gain.if.026` | 225 | `if (skill_table[sn].rating[ch->class] <= 0)` |  | pending |
| `skills.do_gain.return.016` | 229 | `return;` |  | pending |
| `skills.do_gain.if.027` | 232 | `if (ch->train < skill_table[sn].rating[ch->class])` |  | pending |
| `skills.do_gain.return.017` | 236 | `return;` |  | pending |
| `skills.do_gain.return.018` | 244 | `return;` |  | pending |

## do_spells

[Source line 255](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:255); ends at line 373. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:134` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:258` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `str_prefix`, `one_argument`, `is_number`, `send_to_char`, `atoi`, `sprintf`, `UMAX`, `strcat`, `new_buf`, `add_buf`, `page_to_char`, `buf_string`, `free_buf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.do_spells.if.001` | 265 | `if (IS_NPC(ch))` |  | pending |
| `skills.do_spells.return.001` | 266 | `return;` |  | pending |
| `skills.do_spells.if.002` | 268 | `if (argument[0] != '\0')` |  | pending |
| `skills.do_spells.if.003` | 272 | `if (str_prefix(argument,"all"))` |  | pending |
| `skills.do_spells.if.004` | 275 | `if (!is_number(arg))` |  | pending |
| `skills.do_spells.return.002` | 278 | `return;` |  | pending |
| `skills.do_spells.if.005` | 282 | `if (max_lev < 1 \|\| max_lev > LEVEL_HERO)` |  | pending |
| `skills.do_spells.or.001` | 282 | `\|\| max_lev > LEVEL_HERO)` |  | pending |
| `skills.do_spells.return.003` | 286 | `return;` |  | pending |
| `skills.do_spells.if.006` | 289 | `if (argument[0] != '\0')` |  | pending |
| `skills.do_spells.if.007` | 292 | `if (!is_number(arg))` |  | pending |
| `skills.do_spells.return.004` | 295 | `return;` |  | pending |
| `skills.do_spells.if.008` | 300 | `if (max_lev < 1 \|\| max_lev > LEVEL_HERO)` |  | pending |
| `skills.do_spells.or.002` | 300 | `\|\| max_lev > LEVEL_HERO)` |  | pending |
| `skills.do_spells.return.005` | 305 | `return;` |  | pending |
| `skills.do_spells.if.009` | 308 | `if (min_lev > max_lev)` |  | pending |
| `skills.do_spells.return.006` | 311 | `return;` |  | pending |
| `skills.do_spells.for.001` | 319 | `for (level = 0; level < LEVEL_HERO + 1; level++)` |  | pending |
| `skills.do_spells.for.002` | 325 | `for (sn = 0; sn < MAX_SKILL; sn++)` |  | pending |
| `skills.do_spells.if.010` | 327 | `if (skill_table[sn].name == NULL )` |  | pending |
| `skills.do_spells.break.001` | 328 | `break;` |  | pending |
| `skills.do_spells.if.011` | 330 | `if ((level = skill_table[sn].skill_level[ch->class]) < LEVEL_HERO + 1 	&&  (fAll \|\| level <= ch->level) 	&&  level >= min_lev && level <= max_lev 	&&  skill_table[sn].spell_fun != spell_null 	&&  ch->pcdata->learned[sn] > 0)` |  | pending |
| `skills.do_spells.and.001` | 331 | `&&  (fAll \|\| level <= ch->level)` |  | pending |
| `skills.do_spells.or.003` | 331 | `\|\| level <= ch->level)` |  | pending |
| `skills.do_spells.and.002` | 332 | `&&  level >= min_lev && level <= max_lev` |  | pending |
| `skills.do_spells.and.003` | 332 | `&& level <= max_lev` |  | pending |
| `skills.do_spells.and.004` | 333 | `&&  skill_table[sn].spell_fun != spell_null` |  | pending |
| `skills.do_spells.and.005` | 334 | `&&  ch->pcdata->learned[sn] > 0)` |  | pending |
| `skills.do_spells.if.012` | 338 | `if (ch->level < level)` |  | pending |
| `skills.do_spells.if.013` | 347 | `if (spell_list[level][0] == '\0')` |  | pending |
| `skills.do_spells.if.014` | 351 | `if ( ++spell_columns[level] % 2 == 0)` |  | pending |
| `skills.do_spells.if.015` | 360 | `if (!found)` |  | pending |
| `skills.do_spells.return.007` | 363 | `return;` |  | pending |
| `skills.do_spells.for.003` | 367 | `for (level = 0; level < LEVEL_HERO + 1; level++)` |  | pending |
| `skills.do_spells.if.016` | 368 | `if (spell_list[level][0] != '\0')` |  | pending |

## do_skills

[Source line 375](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:375); ends at line 490. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1952` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:131` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:247` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `str_prefix`, `one_argument`, `is_number`, `send_to_char`, `atoi`, `sprintf`, `strcat`, `new_buf`, `add_buf`, `page_to_char`, `buf_string`, `free_buf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.do_skills.if.001` | 385 | `if (IS_NPC(ch))` |  | pending |
| `skills.do_skills.return.001` | 386 | `return;` |  | pending |
| `skills.do_skills.if.002` | 388 | `if (argument[0] != '\0')` |  | pending |
| `skills.do_skills.if.003` | 392 | `if (str_prefix(argument,"all"))` |  | pending |
| `skills.do_skills.if.004` | 395 | `if (!is_number(arg))` |  | pending |
| `skills.do_skills.return.002` | 398 | `return;` |  | pending |
| `skills.do_skills.if.005` | 402 | `if (max_lev < 1 \|\| max_lev > LEVEL_HERO)` |  | pending |
| `skills.do_skills.or.001` | 402 | `\|\| max_lev > LEVEL_HERO)` |  | pending |
| `skills.do_skills.return.003` | 406 | `return;` |  | pending |
| `skills.do_skills.if.006` | 409 | `if (argument[0] != '\0')` |  | pending |
| `skills.do_skills.if.007` | 412 | `if (!is_number(arg))` |  | pending |
| `skills.do_skills.return.004` | 415 | `return;` |  | pending |
| `skills.do_skills.if.008` | 420 | `if (max_lev < 1 \|\| max_lev > LEVEL_HERO)` |  | pending |
| `skills.do_skills.or.002` | 420 | `\|\| max_lev > LEVEL_HERO)` |  | pending |
| `skills.do_skills.return.005` | 425 | `return;` |  | pending |
| `skills.do_skills.if.009` | 428 | `if (min_lev > max_lev)` |  | pending |
| `skills.do_skills.return.006` | 431 | `return;` |  | pending |
| `skills.do_skills.for.001` | 439 | `for (level = 0; level < LEVEL_HERO + 1; level++)` |  | pending |
| `skills.do_skills.for.002` | 445 | `for (sn = 0; sn < MAX_SKILL; sn++)` |  | pending |
| `skills.do_skills.if.010` | 447 | `if (skill_table[sn].name == NULL )` |  | pending |
| `skills.do_skills.break.001` | 448 | `break;` |  | pending |
| `skills.do_skills.if.011` | 450 | `if ((level = skill_table[sn].skill_level[ch->class]) < LEVEL_HERO + 1 	&&  (fAll \|\| level <= ch->level) 	&&  level >= min_lev && level <= max_lev 	&&  skill_table[sn].spell_fun == spell_null 	&&  ch->pcdata->learned[sn] > 0)` |  | pending |
| `skills.do_skills.and.001` | 451 | `&&  (fAll \|\| level <= ch->level)` |  | pending |
| `skills.do_skills.or.003` | 451 | `\|\| level <= ch->level)` |  | pending |
| `skills.do_skills.and.002` | 452 | `&&  level >= min_lev && level <= max_lev` |  | pending |
| `skills.do_skills.and.003` | 452 | `&& level <= max_lev` |  | pending |
| `skills.do_skills.and.004` | 453 | `&&  skill_table[sn].spell_fun == spell_null` |  | pending |
| `skills.do_skills.and.005` | 454 | `&&  ch->pcdata->learned[sn] > 0)` |  | pending |
| `skills.do_skills.if.012` | 458 | `if (ch->level < level)` |  | pending |
| `skills.do_skills.if.013` | 464 | `if (skill_list[level][0] == '\0')` |  | pending |
| `skills.do_skills.if.014` | 468 | `if ( ++skill_columns[level] % 2 == 0)` |  | pending |
| `skills.do_skills.if.015` | 477 | `if (!found)` |  | pending |
| `skills.do_skills.return.007` | 480 | `return;` |  | pending |
| `skills.do_skills.for.003` | 484 | `for (level = 0; level < LEVEL_HERO + 1; level++)` |  | pending |
| `skills.do_skills.if.016` | 485 | `if (skill_list[level][0] != '\0')` |  | pending |

## list_group_costs

[Source line 493](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:493); ends at line 558. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1950` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:810` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2292` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `sprintf`, `send_to_char`, `exp_per_level`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.list_group_costs.if.001` | 498 | `if (IS_NPC(ch))` |  | pending |
| `skills.list_group_costs.return.001` | 499 | `return;` |  | pending |
| `skills.list_group_costs.for.001` | 506 | `for (gn = 0; gn < MAX_GROUP; gn++)` |  | pending |
| `skills.list_group_costs.if.002` | 508 | `if (group_table[gn].name == NULL)` |  | pending |
| `skills.list_group_costs.break.001` | 509 | `break;` |  | pending |
| `skills.list_group_costs.if.003` | 511 | `if (!ch->gen_data->group_chosen[gn]  	&&  !ch->pcdata->group_known[gn] 	&&  group_table[gn].rating[ch->class] > 0)` |  | pending |
| `skills.list_group_costs.and.001` | 512 | `&&  !ch->pcdata->group_known[gn]` |  | pending |
| `skills.list_group_costs.and.002` | 513 | `&&  group_table[gn].rating[ch->class] > 0)` |  | pending |
| `skills.list_group_costs.if.004` | 518 | `if (++col % 3 == 0)` |  | pending |
| `skills.list_group_costs.if.005` | 522 | `if ( col % 3 != 0 )` |  | pending |
| `skills.list_group_costs.for.002` | 531 | `for (sn = 0; sn < MAX_SKILL; sn++)` |  | pending |
| `skills.list_group_costs.if.006` | 533 | `if (skill_table[sn].name == NULL)` |  | pending |
| `skills.list_group_costs.break.002` | 534 | `break;` |  | pending |
| `skills.list_group_costs.if.007` | 536 | `if (!ch->gen_data->skill_chosen[sn]  	&&  ch->pcdata->learned[sn] == 0 	&&  skill_table[sn].spell_fun == spell_null 	&&  skill_table[sn].rating[ch->class] > 0)` |  | pending |
| `skills.list_group_costs.and.003` | 537 | `&&  ch->pcdata->learned[sn] == 0` |  | pending |
| `skills.list_group_costs.and.004` | 538 | `&&  skill_table[sn].spell_fun == spell_null` |  | pending |
| `skills.list_group_costs.and.005` | 539 | `&&  skill_table[sn].rating[ch->class] > 0)` |  | pending |
| `skills.list_group_costs.if.008` | 544 | `if (++col % 3 == 0)` |  | pending |
| `skills.list_group_costs.if.009` | 548 | `if ( col % 3 != 0 )` |  | pending |
| `skills.list_group_costs.return.002` | 557 | `return;` |  | pending |

## list_group_chosen

[Source line 561](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:561); ends at line 623. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- parse_gen_groups: `src/skills.c:816` (lexical_call_candidate).

Dependencies: `IS_NPC`, `sprintf`, `send_to_char`, `exp_per_level`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.list_group_chosen.if.001` | 566 | `if (IS_NPC(ch))` |  | pending |
| `skills.list_group_chosen.return.001` | 567 | `return;` |  | pending |
| `skills.list_group_chosen.for.001` | 574 | `for (gn = 0; gn < MAX_GROUP; gn++)` |  | pending |
| `skills.list_group_chosen.if.002` | 576 | `if (group_table[gn].name == NULL)` |  | pending |
| `skills.list_group_chosen.break.001` | 577 | `break;` |  | pending |
| `skills.list_group_chosen.if.003` | 579 | `if (ch->gen_data->group_chosen[gn]  	&&  group_table[gn].rating[ch->class] > 0)` |  | pending |
| `skills.list_group_chosen.and.001` | 580 | `&&  group_table[gn].rating[ch->class] > 0)` |  | pending |
| `skills.list_group_chosen.if.004` | 585 | `if (++col % 3 == 0)` |  | pending |
| `skills.list_group_chosen.if.005` | 589 | `if ( col % 3 != 0 )` |  | pending |
| `skills.list_group_chosen.for.002` | 598 | `for (sn = 0; sn < MAX_SKILL; sn++)` |  | pending |
| `skills.list_group_chosen.if.006` | 600 | `if (skill_table[sn].name == NULL)` |  | pending |
| `skills.list_group_chosen.break.002` | 601 | `break;` |  | pending |
| `skills.list_group_chosen.if.007` | 603 | `if (ch->gen_data->skill_chosen[sn]  	&&  skill_table[sn].rating[ch->class] > 0)` |  | pending |
| `skills.list_group_chosen.and.002` | 604 | `&&  skill_table[sn].rating[ch->class] > 0)` |  | pending |
| `skills.list_group_chosen.if.008` | 609 | `if (++col % 3 == 0)` |  | pending |
| `skills.list_group_chosen.if.009` | 613 | `if ( col % 3 != 0 )` |  | pending |
| `skills.list_group_chosen.return.002` | 622 | `return;` |  | pending |

## exp_per_level

[Source line 625](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:625); ends at line 657. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_worth: `src/act_info.c:1394` (lexical_call_candidate).
- do_score: `src/act_info.c:1471` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2681` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2705` (lexical_call_candidate).
- bust_a_prompt: `src/comm.c:1404` (lexical_call_candidate).
- nanny: `src/comm.c:2026` (lexical_call_candidate).
- nanny: `src/comm.c:2085` (lexical_call_candidate).
- damage: `src/fight.c:880` (lexical_call_candidate).
- damage: `src/fight.c:882` (lexical_call_candidate).
- do_gain: `src/skills.c:169` (lexical_call_candidate).
- list_group_costs: `src/skills.c:555` (lexical_call_candidate).
- list_group_chosen: `src/skills.c:620` (lexical_call_candidate).
- gain_exp: `src/update.c:125` (lexical_call_candidate).
- gain_exp: `src/update.c:127` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2294` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.exp_per_level.if.001` | 629 | `if (IS_NPC(ch))` |  | pending |
| `skills.exp_per_level.return.001` | 630 | `return 1000;` |  | pending |
| `skills.exp_per_level.if.002` | 635 | `if (points < 40)` |  | pending |
| `skills.exp_per_level.return.002` | 636 | `return 1000 * (pc_race_table[ch->race].class_mult[ch->class] ?` |  | pending |
| `skills.exp_per_level.ternary.001` | 636 | `?` |  | pending |
| `skills.exp_per_level.while.001` | 642 | `while (points > 9)` |  | pending |
| `skills.exp_per_level.if.003` | 646 | `if (points > 9)` |  | pending |
| `skills.exp_per_level.return.003` | 656 | `return expl * pc_race_table[ch->race].class_mult[ch->class]/100;` |  | pending |

## parse_gen_groups

[Source line 660](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:660); ends at line 827. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:2048` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2291` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `str_prefix`, `do_function`, `send_to_char`, `group_lookup`, `sprintf`, `gn_add`, `skill_lookup`, `strcmp`, `gn_remove`, `list_group_costs`, `list_group_chosen`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.parse_gen_groups.if.001` | 666 | `if (argument[0] == '\0')` |  | pending |
| `skills.parse_gen_groups.return.001` | 667 | `return FALSE;` |  | pending |
| `skills.parse_gen_groups.if.002` | 671 | `if (!str_prefix(arg,"help"))` |  | pending |
| `skills.parse_gen_groups.if.003` | 673 | `if (argument[0] == '\0')` |  | pending |
| `skills.parse_gen_groups.return.002` | 676 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.return.003` | 680 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.004` | 683 | `if (!str_prefix(arg,"add"))` |  | pending |
| `skills.parse_gen_groups.if.005` | 685 | `if (argument[0] == '\0')` |  | pending |
| `skills.parse_gen_groups.return.004` | 688 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.006` | 692 | `if (gn != -1)` |  | pending |
| `skills.parse_gen_groups.if.007` | 694 | `if (ch->gen_data->group_chosen[gn] 	    \|\|  ch->pcdata->group_known[gn])` |  | pending |
| `skills.parse_gen_groups.or.001` | 695 | `\|\|  ch->pcdata->group_known[gn])` |  | pending |
| `skills.parse_gen_groups.return.005` | 698 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.008` | 701 | `if (group_table[gn].rating[ch->class] < 1)` |  | pending |
| `skills.parse_gen_groups.return.006` | 704 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.009` | 708 | `if (ch->gen_data->points_chosen + group_table[gn].rating[ch->class] 		> 300)` |  | pending |
| `skills.parse_gen_groups.return.007` | 713 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.return.008` | 722 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.010` | 726 | `if (sn != -1)` |  | pending |
| `skills.parse_gen_groups.if.011` | 728 | `if (ch->gen_data->skill_chosen[sn] 	    \|\|  ch->pcdata->learned[sn] > 0)` |  | pending |
| `skills.parse_gen_groups.or.002` | 729 | `\|\|  ch->pcdata->learned[sn] > 0)` |  | pending |
| `skills.parse_gen_groups.return.009` | 732 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.012` | 735 | `if (skill_table[sn].rating[ch->class] < 1 	    \|\|  skill_table[sn].spell_fun != spell_null)` |  | pending |
| `skills.parse_gen_groups.or.003` | 736 | `\|\|  skill_table[sn].spell_fun != spell_null)` |  | pending |
| `skills.parse_gen_groups.return.010` | 739 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.013` | 743 | `if (ch->gen_data->points_chosen + skill_table[sn].rating[ch->class] 		> 300)` |  | pending |
| `skills.parse_gen_groups.return.011` | 748 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.return.012` | 756 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.return.013` | 760 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.014` | 763 | `if (!strcmp(arg,"drop"))` |  | pending |
| `skills.parse_gen_groups.if.015` | 765 | `if (argument[0] == '\0')` |  | pending |
| `skills.parse_gen_groups.return.014` | 768 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.016` | 772 | `if (gn != -1 && ch->gen_data->group_chosen[gn])` |  | pending |
| `skills.parse_gen_groups.and.001` | 772 | `&& ch->gen_data->group_chosen[gn])` |  | pending |
| `skills.parse_gen_groups.for.001` | 778 | `for (i = 0; i < MAX_GROUP; i++)` |  | pending |
| `skills.parse_gen_groups.if.017` | 780 | `if (ch->gen_data->group_chosen[gn])` |  | pending |
| `skills.parse_gen_groups.return.015` | 784 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.018` | 788 | `if (sn != -1 && ch->gen_data->skill_chosen[sn])` |  | pending |
| `skills.parse_gen_groups.and.002` | 788 | `&& ch->gen_data->skill_chosen[sn])` |  | pending |
| `skills.parse_gen_groups.return.016` | 795 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.return.017` | 799 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.019` | 802 | `if (!str_prefix(arg,"premise"))` |  | pending |
| `skills.parse_gen_groups.return.018` | 805 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.020` | 808 | `if (!str_prefix(arg,"list"))` |  | pending |
| `skills.parse_gen_groups.return.019` | 811 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.021` | 814 | `if (!str_prefix(arg,"learned"))` |  | pending |
| `skills.parse_gen_groups.return.020` | 817 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.if.022` | 820 | `if (!str_prefix(arg,"info"))` |  | pending |
| `skills.parse_gen_groups.return.021` | 823 | `return TRUE;` |  | pending |
| `skills.parse_gen_groups.return.022` | 826 | `return FALSE;` |  | pending |

## do_groups

[Source line 835](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:835); ends at line 905. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- parse_gen_groups: `src/skills.c:822` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:124` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:259` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:142` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `sprintf`, `send_to_char`, `str_cmp`, `group_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.do_groups.if.001` | 840 | `if (IS_NPC(ch))` |  | pending |
| `skills.do_groups.return.001` | 841 | `return;` |  | pending |
| `skills.do_groups.if.002` | 845 | `if (argument[0] == '\0')` |  | pending |
| `skills.do_groups.for.001` | 848 | `for (gn = 0; gn < MAX_GROUP; gn++)` |  | pending |
| `skills.do_groups.if.003` | 850 | `if (group_table[gn].name == NULL)` |  | pending |
| `skills.do_groups.break.001` | 851 | `break;` |  | pending |
| `skills.do_groups.if.004` | 852 | `if (ch->pcdata->group_known[gn])` |  | pending |
| `skills.do_groups.if.005` | 856 | `if (++col % 3 == 0)` |  | pending |
| `skills.do_groups.if.006` | 860 | `if ( col % 3 != 0 )` |  | pending |
| `skills.do_groups.return.002` | 864 | `return;` |  | pending |
| `skills.do_groups.if.007` | 867 | `if (!str_cmp(argument,"all"))` |  | pending |
| `skills.do_groups.for.002` | 869 | `for (gn = 0; gn < MAX_GROUP; gn++)` |  | pending |
| `skills.do_groups.if.008` | 871 | `if (group_table[gn].name == NULL)` |  | pending |
| `skills.do_groups.break.002` | 872 | `break;` |  | pending |
| `skills.do_groups.if.009` | 875 | `if (++col % 3 == 0)` |  | pending |
| `skills.do_groups.if.010` | 878 | `if ( col % 3 != 0 )` |  | pending |
| `skills.do_groups.return.003` | 880 | `return;` |  | pending |
| `skills.do_groups.if.011` | 886 | `if (gn == -1)` |  | pending |
| `skills.do_groups.return.004` | 891 | `return;` |  | pending |
| `skills.do_groups.for.003` | 894 | `for (sn = 0; sn < MAX_IN_GROUP; sn++)` |  | pending |
| `skills.do_groups.if.012` | 896 | `if (group_table[gn].spells[sn] == NULL)` |  | pending |
| `skills.do_groups.break.003` | 897 | `break;` |  | pending |
| `skills.do_groups.if.013` | 900 | `if (++col % 3 == 0)` |  | pending |
| `skills.do_groups.if.014` | 903 | `if ( col % 3 != 0 )` |  | pending |

## check_improve

[Source line 908](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:908); ends at line 961. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_char_to_char_1: `src/act_info.c:485` (lexical_call_candidate).
- do_pick: `src/act_move.c:771` (lexical_call_candidate).
- do_pick: `src/act_move.c:807` (lexical_call_candidate).
- do_pick: `src/act_move.c:830` (lexical_call_candidate).
- do_pick: `src/act_move.c:854` (lexical_call_candidate).
- do_sneak: `src/act_move.c:1347` (lexical_call_candidate).
- do_sneak: `src/act_move.c:1358` (lexical_call_candidate).
- do_hide: `src/act_move.c:1375` (lexical_call_candidate).
- do_hide: `src/act_move.c:1378` (lexical_call_candidate).
- do_recall: `src/act_move.c:1440` (lexical_call_candidate).
- do_recall: `src/act_move.c:1449` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:869` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:877` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:924` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:931` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1935` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1943` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:1990` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:2025` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2113` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2118` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2223` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2270` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2303` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2581` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2701` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2905` (lexical_call_candidate).
- multi_hit: `src/fight.c:228` (lexical_call_candidate).
- multi_hit: `src/fight.c:241` (lexical_call_candidate).
- one_hit: `src/fight.c:528` (lexical_call_candidate).
- one_hit: `src/fight.c:561` (lexical_call_candidate).
- check_parry: `src/fight.c:1288` (lexical_call_candidate).
- check_shield_block: `src/fight.c:1316` (lexical_call_candidate).
- check_dodge: `src/fight.c:1341` (lexical_call_candidate).
- do_berserk: `src/fight.c:2177` (lexical_call_candidate).
- do_berserk: `src/fight.c:2204` (lexical_call_candidate).
- do_bash: `src/fight.c:2314` (lexical_call_candidate).
- do_bash: `src/fight.c:2332` (lexical_call_candidate).
- do_dirt: `src/fight.c:2450` (lexical_call_candidate).
- do_dirt: `src/fight.c:2466` (lexical_call_candidate).
- do_trip: `src/fight.c:2569` (lexical_call_candidate).
- do_trip: `src/fight.c:2581` (lexical_call_candidate).
- do_backstab: `src/fight.c:2788` (lexical_call_candidate).
- do_backstab: `src/fight.c:2793` (lexical_call_candidate).
- do_rescue: `src/fight.c:2916` (lexical_call_candidate).
- do_rescue: `src/fight.c:2923` (lexical_call_candidate).
- do_kick: `src/fight.c:2961` (lexical_call_candidate).
- do_kick: `src/fight.c:2966` (lexical_call_candidate).
- do_disarm: `src/fight.c:3036` (lexical_call_candidate).
- do_disarm: `src/fight.c:3044` (lexical_call_candidate).
- do_cast: `src/magic.c:542` (lexical_call_candidate).
- do_cast: `src/magic.c:553` (lexical_call_candidate).
- hit_gain: `src/update.c:180` (lexical_call_candidate).
- mana_gain: `src/update.c:246` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2295` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `get_curr_stat`, `number_range`, `URANGE`, `number_percent`, `sprintf`, `send_to_char`, `gain_exp`, `UMIN`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.check_improve.if.001` | 913 | `if (IS_NPC(ch))` |  | pending |
| `skills.check_improve.return.001` | 914 | `return;` |  | pending |
| `skills.check_improve.if.002` | 916 | `if (ch->level < skill_table[sn].skill_level[ch->class]     \|\|  skill_table[sn].rating[ch->class] == 0     \|\|  ch->pcdata->learned[sn] == 0     \|\|  ch->pcdata->learned[sn] == 100)` |  | pending |
| `skills.check_improve.or.001` | 917 | `\|\|  skill_table[sn].rating[ch->class] == 0` |  | pending |
| `skills.check_improve.or.002` | 918 | `\|\|  ch->pcdata->learned[sn] == 0` |  | pending |
| `skills.check_improve.or.003` | 919 | `\|\|  ch->pcdata->learned[sn] == 100)` |  | pending |
| `skills.check_improve.return.002` | 920 | `return;` |  | pending |
| `skills.check_improve.if.003` | 929 | `if (number_range(1,1000) > chance)` |  | pending |
| `skills.check_improve.return.003` | 930 | `return;` |  | pending |
| `skills.check_improve.if.004` | 934 | `if (success)` |  | pending |
| `skills.check_improve.if.005` | 937 | `if (number_percent() < chance)` |  | pending |
| `skills.check_improve.if.006` | 950 | `if (number_percent() < chance)` |  | pending |

## group_lookup

[Source line 964](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:964); ends at line 978. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- fread_char: `src/save.c:945` (lexical_call_candidate).
- do_gain: `src/skills.c:175` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:691` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:771` (lexical_call_candidate).
- do_groups: `src/skills.c:885` (lexical_call_candidate).
- group_add: `src/skills.c:1032` (lexical_call_candidate).
- group_remove: `src/skills.c:1062` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2297` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.group_lookup.for.001` | 968 | `for ( gn = 0; gn < MAX_GROUP; gn++ )` |  | pending |
| `skills.group_lookup.if.001` | 970 | `if ( group_table[gn].name == NULL )` |  | pending |
| `skills.group_lookup.break.001` | 971 | `break;` |  | pending |
| `skills.group_lookup.if.002` | 972 | `if ( LOWER(name[0]) == LOWER(group_table[gn].name[0])         &&   !str_prefix( name, group_table[gn].name ) )` |  | pending |
| `skills.group_lookup.and.001` | 973 | `&&   !str_prefix( name, group_table[gn].name ) )` |  | pending |
| `skills.group_lookup.return.001` | 974 | `return gn;` |  | pending |
| `skills.group_lookup.return.002` | 977 | `return -1;` |  | pending |

## gn_add

[Source line 981](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:981); ends at line 992. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- fread_char: `src/save.c:953` (lexical_call_candidate).
- do_gain: `src/skills.c:200` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:720` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:781` (lexical_call_candidate).
- group_add: `src/skills.c:1042` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2298` (declaration_or_dispatch_reference).

Dependencies: `group_add`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.gn_add.for.001` | 986 | `for ( i = 0; i < MAX_IN_GROUP; i++)` |  | pending |
| `skills.gn_add.if.001` | 988 | `if (group_table[gn].spells[i] == NULL)` |  | pending |
| `skills.gn_add.break.001` | 989 | `break;` |  | pending |

## gn_remove

[Source line 995](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:995); ends at line 1007. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- parse_gen_groups: `src/skills.c:777` (lexical_call_candidate).
- group_remove: `src/skills.c:1067` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2299` (declaration_or_dispatch_reference).

Dependencies: `group_remove`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.gn_remove.for.001` | 1001 | `for ( i = 0; i < MAX_IN_GROUP; i ++)` |  | pending |
| `skills.gn_remove.if.001` | 1003 | `if (group_table[gn].spells[i] == NULL)` |  | pending |
| `skills.gn_remove.break.001` | 1004 | `break;` |  | pending |

## group_add

[Source line 1010](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:1010); ends at line 1044. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1859` (lexical_call_candidate).
- nanny: `src/comm.c:1933` (lexical_call_candidate).
- nanny: `src/comm.c:1934` (lexical_call_candidate).
- nanny: `src/comm.c:1957` (lexical_call_candidate).
- load_char_obj: `src/save.c:646` (lexical_call_candidate).
- load_char_obj: `src/save.c:661` (lexical_call_candidate).
- load_char_obj: `src/save.c:662` (lexical_call_candidate).
- load_char_obj: `src/save.c:663` (lexical_call_candidate).
- gn_add: `src/skills.c:990` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2300` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `skill_lookup`, `group_lookup`, `gn_add`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.group_add.if.001` | 1014 | `if (IS_NPC(ch))` |  | pending |
| `skills.group_add.return.001` | 1015 | `return;` |  | pending |
| `skills.group_add.if.002` | 1019 | `if (sn != -1)` |  | pending |
| `skills.group_add.if.003` | 1021 | `if (ch->pcdata->learned[sn] == 0)` |  | pending |
| `skills.group_add.if.004` | 1024 | `if (deduct)` |  | pending |
| `skills.group_add.return.002` | 1027 | `return;` |  | pending |
| `skills.group_add.if.005` | 1034 | `if (gn != -1)` |  | pending |
| `skills.group_add.if.006` | 1036 | `if (ch->pcdata->group_known[gn] == FALSE)` |  | pending |
| `skills.group_add.if.007` | 1039 | `if (deduct)` |  | pending |

## group_remove

[Source line 1048](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:1048); ends at line 1069. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- gn_remove: `src/skills.c:1005` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2301` (declaration_or_dispatch_reference).

Dependencies: `skill_lookup`, `group_lookup`, `gn_remove`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `skills.group_remove.if.001` | 1054 | `if (sn != -1)` |  | pending |
| `skills.group_remove.return.001` | 1057 | `return;` |  | pending |
| `skills.group_remove.if.002` | 1064 | `if (gn != -1 && ch->pcdata->group_known[gn] == TRUE)` |  | pending |
| `skills.group_remove.and.001` | 1064 | `&& ch->pcdata->group_known[gn] == TRUE)` |  | pending |

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
- Line 40: `#include "magic.h"` — pending configuration/reachability review.
- Line 41: `#include "recycle.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


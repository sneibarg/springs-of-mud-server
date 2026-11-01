# src/update.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `73ffb3825b074e5bc077966c788ea2c7812effa03b974b81001b6477cd0e9376`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## advance_level

[Source line 61](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:61); ends at line 114. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_advance: `src/act_wiz.c:2689` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2701` (lexical_call_candidate).
- gain_exp: `src/update.c:135` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2311` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `set_title`, `get_curr_stat`, `number_range`, `UMAX`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.advance_level.ternary.001` | 73 | `? 1 : 0] );` |  | pending |
| `update.advance_level.if.001` | 81 | `if (!class_table[ch->class].fMana)` |  | pending |
| `update.advance_level.if.002` | 105 | `if (!hide)` |  | pending |
| `update.advance_level.ternary.002` | 109 | `? "" : "s", add_mana, add_move,` |  | pending |
| `update.advance_level.ternary.003` | 110 | `? "" : "s");` |  | pending |
| `update.advance_level.return.001` | 113 | `return;` |  | pending |

## gain_exp

[Source line 118](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:118); ends at line 140. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_recall: `src/act_move.c:1448` (lexical_call_candidate).
- damage: `src/fight.c:882` (lexical_call_candidate).
- group_gain: `src/fight.c:1754` (lexical_call_candidate).
- do_flee: `src/fight.c:2849` (lexical_call_candidate).
- spell_energy_drain: `src/magic.c:2644` (lexical_call_candidate).
- check_improve: `src/skills.c:943` (lexical_call_candidate).
- check_improve: `src/skills.c:958` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2312` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `UMAX`, `exp_per_level`, `send_to_char`, `sprintf`, `log_string`, `wiznet`, `advance_level`, `save_char_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.gain_exp.if.001` | 122 | `if ( IS_NPC(ch) \|\| ch->level >= LEVEL_HERO )` |  | pending |
| `update.gain_exp.or.001` | 122 | `\|\| ch->level >= LEVEL_HERO )` |  | pending |
| `update.gain_exp.return.001` | 123 | `return;` |  | pending |
| `update.gain_exp.while.001` | 126 | `while ( ch->level < LEVEL_HERO && ch->exp >=  	exp_per_level(ch,ch->pcdata->points) * (ch->level+1) )` |  | pending |
| `update.gain_exp.and.001` | 126 | `&& ch->exp >=` |  | pending |
| `update.gain_exp.return.002` | 139 | `return;` |  | pending |

## hit_gain

[Source line 147](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:147); ends at line 214. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- char_update: `src/update.c:644` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/update.c:43` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_AFFECTED`, `UMAX`, `get_curr_stat`, `number_percent`, `get_skill`, `check_improve`, `UMIN`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.hit_gain.if.001` | 152 | `if (ch->in_room == NULL)` |  | pending |
| `update.hit_gain.return.001` | 153 | `return 0;` |  | pending |
| `update.hit_gain.if.002` | 155 | `if ( IS_NPC(ch) )` |  | pending |
| `update.hit_gain.if.003` | 158 | `if (IS_AFFECTED(ch,AFF_REGENERATION))` |  | pending |
| `update.hit_gain.switch.001` | 161 | `switch(ch->position)` |  | pending |
| `update.hit_gain.default.001` | 163 | `default : 		gain /= 2;` |  | pending |
| `update.hit_gain.break.001` | 163 | `break;` |  | pending |
| `update.hit_gain.case.001` | 164 | `case POS_SLEEPING: 	gain = 3 * gain/2;` |  | pending |
| `update.hit_gain.break.002` | 164 | `break;` |  | pending |
| `update.hit_gain.case.002` | 165 | `case POS_RESTING:  					break;` |  | pending |
| `update.hit_gain.break.003` | 165 | `break;` |  | pending |
| `update.hit_gain.case.003` | 166 | `case POS_FIGHTING:	gain /= 3;` |  | pending |
| `update.hit_gain.break.004` | 166 | `break;` |  | pending |
| `update.hit_gain.if.004` | 176 | `if (number < get_skill(ch,gsn_fast_healing))` |  | pending |
| `update.hit_gain.if.005` | 179 | `if (ch->hit < ch->max_hit)` |  | pending |
| `update.hit_gain.switch.002` | 183 | `switch ( ch->position )` |  | pending |
| `update.hit_gain.default.002` | 185 | `default:	   	gain /= 4;` |  | pending |
| `update.hit_gain.break.005` | 185 | `break;` |  | pending |
| `update.hit_gain.case.004` | 186 | `case POS_SLEEPING: 					break;` |  | pending |
| `update.hit_gain.break.006` | 186 | `break;` |  | pending |
| `update.hit_gain.case.005` | 187 | `case POS_RESTING:  	gain /= 2;` |  | pending |
| `update.hit_gain.break.007` | 187 | `break;` |  | pending |
| `update.hit_gain.case.006` | 188 | `case POS_FIGHTING: 	gain /= 6;` |  | pending |
| `update.hit_gain.break.008` | 188 | `break;` |  | pending |
| `update.hit_gain.if.006` | 191 | `if ( ch->pcdata->condition[COND_HUNGER]   == 0 )` |  | pending |
| `update.hit_gain.if.007` | 194 | `if ( ch->pcdata->condition[COND_THIRST] == 0 )` |  | pending |
| `update.hit_gain.if.008` | 201 | `if (ch->on != NULL && ch->on->item_type == ITEM_FURNITURE)` |  | pending |
| `update.hit_gain.and.001` | 201 | `&& ch->on->item_type == ITEM_FURNITURE)` |  | pending |
| `update.hit_gain.if.009` | 204 | `if ( IS_AFFECTED(ch, AFF_POISON) )` |  | pending |
| `update.hit_gain.if.010` | 207 | `if (IS_AFFECTED(ch, AFF_PLAGUE))` |  | pending |
| `update.hit_gain.if.011` | 210 | `if (IS_AFFECTED(ch,AFF_HASTE) \|\| IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `update.hit_gain.or.001` | 210 | `\|\| IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `update.hit_gain.return.002` | 213 | `return UMIN(gain, ch->max_hit - ch->hit);` |  | pending |

## mana_gain

[Source line 218](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:218); ends at line 282. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- char_update: `src/update.c:649` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/update.c:44` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `get_curr_stat`, `number_percent`, `get_skill`, `check_improve`, `IS_AFFECTED`, `UMIN`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.mana_gain.if.001` | 223 | `if (ch->in_room == NULL)` |  | pending |
| `update.mana_gain.return.001` | 224 | `return 0;` |  | pending |
| `update.mana_gain.if.002` | 226 | `if ( IS_NPC(ch) )` |  | pending |
| `update.mana_gain.switch.001` | 229 | `switch (ch->position)` |  | pending |
| `update.mana_gain.default.001` | 231 | `default:		gain /= 2;` |  | pending |
| `update.mana_gain.break.001` | 231 | `break;` |  | pending |
| `update.mana_gain.case.001` | 232 | `case POS_SLEEPING:	gain = 3 * gain/2;` |  | pending |
| `update.mana_gain.break.002` | 232 | `break;` |  | pending |
| `update.mana_gain.case.002` | 233 | `case POS_RESTING:				break;` |  | pending |
| `update.mana_gain.break.003` | 233 | `break;` |  | pending |
| `update.mana_gain.case.003` | 234 | `case POS_FIGHTING:	gain /= 3;` |  | pending |
| `update.mana_gain.break.004` | 234 | `break;` |  | pending |
| `update.mana_gain.if.003` | 242 | `if (number < get_skill(ch,gsn_meditation))` |  | pending |
| `update.mana_gain.if.004` | 245 | `if (ch->mana < ch->max_mana)` |  | pending |
| `update.mana_gain.if.005` | 248 | `if (!class_table[ch->class].fMana)` |  | pending |
| `update.mana_gain.switch.002` | 251 | `switch ( ch->position )` |  | pending |
| `update.mana_gain.default.002` | 253 | `default:		gain /= 4;` |  | pending |
| `update.mana_gain.break.005` | 253 | `break;` |  | pending |
| `update.mana_gain.case.004` | 254 | `case POS_SLEEPING: 					break;` |  | pending |
| `update.mana_gain.break.006` | 254 | `break;` |  | pending |
| `update.mana_gain.case.005` | 255 | `case POS_RESTING:	gain /= 2;` |  | pending |
| `update.mana_gain.break.007` | 255 | `break;` |  | pending |
| `update.mana_gain.case.006` | 256 | `case POS_FIGHTING:	gain /= 6;` |  | pending |
| `update.mana_gain.break.008` | 256 | `break;` |  | pending |
| `update.mana_gain.if.006` | 259 | `if ( ch->pcdata->condition[COND_HUNGER]   == 0 )` |  | pending |
| `update.mana_gain.if.007` | 262 | `if ( ch->pcdata->condition[COND_THIRST] == 0 )` |  | pending |
| `update.mana_gain.if.008` | 269 | `if (ch->on != NULL && ch->on->item_type == ITEM_FURNITURE)` |  | pending |
| `update.mana_gain.and.001` | 269 | `&& ch->on->item_type == ITEM_FURNITURE)` |  | pending |
| `update.mana_gain.if.009` | 272 | `if ( IS_AFFECTED( ch, AFF_POISON ) )` |  | pending |
| `update.mana_gain.if.010` | 275 | `if (IS_AFFECTED(ch, AFF_PLAGUE))` |  | pending |
| `update.mana_gain.if.011` | 278 | `if (IS_AFFECTED(ch,AFF_HASTE) \|\| IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `update.mana_gain.or.001` | 278 | `\|\| IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `update.mana_gain.return.002` | 281 | `return UMIN(gain, ch->max_mana - ch->mana);` |  | pending |

## move_gain

[Source line 286](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:286); ends at line 329. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- char_update: `src/update.c:654` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/update.c:45` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `UMAX`, `get_curr_stat`, `IS_AFFECTED`, `UMIN`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.move_gain.if.001` | 290 | `if (ch->in_room == NULL)` |  | pending |
| `update.move_gain.return.001` | 291 | `return 0;` |  | pending |
| `update.move_gain.if.002` | 293 | `if ( IS_NPC(ch) )` |  | pending |
| `update.move_gain.switch.001` | 301 | `switch ( ch->position )` |  | pending |
| `update.move_gain.case.001` | 303 | `case POS_SLEEPING: gain += get_curr_stat(ch,STAT_DEX);` |  | pending |
| `update.move_gain.break.001` | 303 | `break;` |  | pending |
| `update.move_gain.case.002` | 304 | `case POS_RESTING:  gain += get_curr_stat(ch,STAT_DEX) / 2;` |  | pending |
| `update.move_gain.break.002` | 304 | `break;` |  | pending |
| `update.move_gain.if.003` | 307 | `if ( ch->pcdata->condition[COND_HUNGER]   == 0 )` |  | pending |
| `update.move_gain.if.004` | 310 | `if ( ch->pcdata->condition[COND_THIRST] == 0 )` |  | pending |
| `update.move_gain.if.005` | 316 | `if (ch->on != NULL && ch->on->item_type == ITEM_FURNITURE)` |  | pending |
| `update.move_gain.and.001` | 316 | `&& ch->on->item_type == ITEM_FURNITURE)` |  | pending |
| `update.move_gain.if.006` | 319 | `if ( IS_AFFECTED(ch, AFF_POISON) )` |  | pending |
| `update.move_gain.if.007` | 322 | `if (IS_AFFECTED(ch, AFF_PLAGUE))` |  | pending |
| `update.move_gain.if.008` | 325 | `if (IS_AFFECTED(ch,AFF_HASTE) \|\| IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `update.move_gain.or.001` | 325 | `\|\| IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `update.move_gain.return.002` | 328 | `return UMIN(gain, ch->max_move - ch->move);` |  | pending |

## gain_condition

[Source line 333](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:333); ends at line 365. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_drink: `src/act_obj.c:1218` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1220` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1222` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1224` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1304` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1305` (lexical_call_candidate).
- cold_effect: `src/effects.c:236` (lexical_call_candidate).
- fire_effect: `src/effects.c:343` (lexical_call_candidate).
- char_update: `src/update.c:701` (lexical_call_candidate).
- char_update: `src/update.c:702` (lexical_call_candidate).
- char_update: `src/update.c:703` (lexical_call_candidate).
- char_update: `src/update.c:704` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2313` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `URANGE`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.gain_condition.if.001` | 337 | `if ( value == 0 \|\| IS_NPC(ch) \|\| ch->level >= LEVEL_IMMORTAL)` |  | pending |
| `update.gain_condition.or.001` | 337 | `\|\| IS_NPC(ch) \|\| ch->level >= LEVEL_IMMORTAL)` |  | pending |
| `update.gain_condition.or.002` | 337 | `\|\| ch->level >= LEVEL_IMMORTAL)` |  | pending |
| `update.gain_condition.return.001` | 338 | `return;` |  | pending |
| `update.gain_condition.if.002` | 341 | `if (condition == -1)` |  | pending |
| `update.gain_condition.return.002` | 342 | `return;` |  | pending |
| `update.gain_condition.if.003` | 345 | `if ( ch->pcdata->condition[iCond] == 0 )` |  | pending |
| `update.gain_condition.switch.001` | 347 | `switch ( iCond )` |  | pending |
| `update.gain_condition.case.001` | 349 | `case COND_HUNGER:` |  | pending |
| `update.gain_condition.break.001` | 351 | `break;` |  | pending |
| `update.gain_condition.case.002` | 353 | `case COND_THIRST:` |  | pending |
| `update.gain_condition.break.002` | 355 | `break;` |  | pending |
| `update.gain_condition.case.003` | 357 | `case COND_DRUNK:` |  | pending |
| `update.gain_condition.if.004` | 358 | `if ( condition != 0 )` |  | pending |
| `update.gain_condition.break.003` | 360 | `break;` |  | pending |
| `update.gain_condition.return.003` | 364 | `return;` |  | pending |

## mobile_update

[Source line 374](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:374); ends at line 460. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- update_handler: `src/update.c:1105` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/update.c:46` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_AFFECTED`, `IS_SET`, `number_range`, `number_bits`, `CAN_WEAR`, `can_loot`, `obj_from_room`, `obj_to_char`, `act`, `move_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.mobile_update.for.001` | 382 | `for ( ch = char_list; ch != NULL; ch = ch_next )` |  | pending |
| `update.mobile_update.if.001` | 386 | `if ( !IS_NPC(ch) \|\| ch->in_room == NULL \|\| IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `update.mobile_update.or.001` | 386 | `\|\| ch->in_room == NULL \|\| IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `update.mobile_update.or.002` | 386 | `\|\| IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `update.mobile_update.continue.001` | 387 | `continue;` |  | pending |
| `update.mobile_update.if.002` | 389 | `if (ch->in_room->area->empty && !IS_SET(ch->act,ACT_UPDATE_ALWAYS))` |  | pending |
| `update.mobile_update.and.001` | 389 | `&& !IS_SET(ch->act,ACT_UPDATE_ALWAYS))` |  | pending |
| `update.mobile_update.continue.002` | 390 | `continue;` |  | pending |
| `update.mobile_update.if.003` | 393 | `if ( ch->spec_fun != 0 )` |  | pending |
| `update.mobile_update.if.004` | 395 | `if ( (*ch->spec_fun) ( ch ) )` |  | pending |
| `update.mobile_update.continue.003` | 396 | `continue;` |  | pending |
| `update.mobile_update.if.005` | 399 | `if (ch->pIndexData->pShop != NULL)` |  | pending |
| `update.mobile_update.if.006` | 400 | `if ((ch->gold * 100 + ch->silver) < ch->pIndexData->wealth)` |  | pending |
| `update.mobile_update.if.007` | 408 | `if ( ch->position != POS_STANDING )` |  | pending |
| `update.mobile_update.continue.004` | 409 | `continue;` |  | pending |
| `update.mobile_update.if.008` | 412 | `if ( IS_SET(ch->act, ACT_SCAVENGER) 	&&   ch->in_room->contents != NULL 	&&   number_bits( 6 ) == 0 )` |  | pending |
| `update.mobile_update.and.002` | 413 | `&&   ch->in_room->contents != NULL` |  | pending |
| `update.mobile_update.and.003` | 414 | `&&   number_bits( 6 ) == 0 )` |  | pending |
| `update.mobile_update.for.002` | 422 | `for ( obj = ch->in_room->contents; obj; obj = obj->next_content )` |  | pending |
| `update.mobile_update.if.009` | 424 | `if ( CAN_WEAR(obj, ITEM_TAKE) && can_loot(ch, obj) 		     && obj->cost > max  && obj->cost > 0)` |  | pending |
| `update.mobile_update.and.004` | 424 | `&& can_loot(ch, obj)` |  | pending |
| `update.mobile_update.and.005` | 425 | `&& obj->cost > max  && obj->cost > 0)` |  | pending |
| `update.mobile_update.and.006` | 425 | `&& obj->cost > 0)` |  | pending |
| `update.mobile_update.if.010` | 432 | `if ( obj_best )` |  | pending |
| `update.mobile_update.if.011` | 441 | `if ( !IS_SET(ch->act, ACT_SENTINEL)  	&& number_bits(3) == 0 	&& ( door = number_bits( 5 ) ) <= 5 	&& ( pexit = ch->in_room->exit[door] ) != NULL 	&&   pexit->u1.to_room != NULL 	&&   !IS_SET(pexit->exit_info, EX_CLOSED) 	&&   !IS_SET(pexit->u1.to_room->room_flags, ROOM_NO_MOB) 	&& ( !IS_SET(ch->act, ACT_STAY_AREA) 	\|\|   pexit->u1.to_room->area == ch->in_room->area )  	&& ( !IS_SET(ch->act, ACT_OUTDOORS) 	\|\|   !IS_SET(pexit->u1.to_room->room_flags,ROOM_INDOORS))  	&& ( !IS_SET(ch->act, ACT_INDOORS) 	\|\|   IS_SET(pexit->u1.to_room->room_flags,ROOM_INDOORS)))` |  | pending |
| `update.mobile_update.and.007` | 442 | `&& number_bits(3) == 0` |  | pending |
| `update.mobile_update.and.008` | 443 | `&& ( door = number_bits( 5 ) ) <= 5` |  | pending |
| `update.mobile_update.and.009` | 444 | `&& ( pexit = ch->in_room->exit[door] ) != NULL` |  | pending |
| `update.mobile_update.and.010` | 445 | `&&   pexit->u1.to_room != NULL` |  | pending |
| `update.mobile_update.and.011` | 446 | `&&   !IS_SET(pexit->exit_info, EX_CLOSED)` |  | pending |
| `update.mobile_update.and.012` | 447 | `&&   !IS_SET(pexit->u1.to_room->room_flags, ROOM_NO_MOB)` |  | pending |
| `update.mobile_update.and.013` | 448 | `&& ( !IS_SET(ch->act, ACT_STAY_AREA)` |  | pending |
| `update.mobile_update.or.003` | 449 | `\|\|   pexit->u1.to_room->area == ch->in_room->area )` |  | pending |
| `update.mobile_update.and.014` | 450 | `&& ( !IS_SET(ch->act, ACT_OUTDOORS)` |  | pending |
| `update.mobile_update.or.004` | 451 | `\|\|   !IS_SET(pexit->u1.to_room->room_flags,ROOM_INDOORS))` |  | pending |
| `update.mobile_update.and.015` | 452 | `&& ( !IS_SET(ch->act, ACT_INDOORS)` |  | pending |
| `update.mobile_update.or.005` | 453 | `\|\|   IS_SET(pexit->u1.to_room->room_flags,ROOM_INDOORS)))` |  | pending |
| `update.mobile_update.return.001` | 459 | `return;` |  | pending |

## weather_update

[Source line 467](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:467); ends at line 600. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- update_handler: `src/update.c:1119` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/update.c:47` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `dice`, `UMAX`, `UMIN`, `bug`, `number_bits`, `IS_OUTSIDE`, `IS_AWAKE`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.weather_update.switch.001` | 475 | `switch ( ++time_info.hour )` |  | pending |
| `update.weather_update.case.001` | 477 | `case  5:` |  | pending |
| `update.weather_update.break.001` | 480 | `break;` |  | pending |
| `update.weather_update.case.002` | 482 | `case  6:` |  | pending |
| `update.weather_update.break.002` | 485 | `break;` |  | pending |
| `update.weather_update.case.003` | 487 | `case 19:` |  | pending |
| `update.weather_update.break.003` | 490 | `break;` |  | pending |
| `update.weather_update.case.004` | 492 | `case 20:` |  | pending |
| `update.weather_update.break.004` | 495 | `break;` |  | pending |
| `update.weather_update.case.005` | 497 | `case 24:` |  | pending |
| `update.weather_update.break.005` | 500 | `break;` |  | pending |
| `update.weather_update.if.001` | 503 | `if ( time_info.day   >= 35 )` |  | pending |
| `update.weather_update.if.002` | 509 | `if ( time_info.month >= 17 )` |  | pending |
| `update.weather_update.if.003` | 518 | `if ( time_info.month >= 9 && time_info.month <= 16 )` |  | pending |
| `update.weather_update.and.001` | 518 | `&& time_info.month <= 16 )` |  | pending |
| `update.weather_update.ternary.001` | 519 | `? -2 : 2;` |  | pending |
| `update.weather_update.ternary.002` | 521 | `? -2 : 2;` |  | pending |
| `update.weather_update.switch.002` | 531 | `switch ( weather_info.sky )` |  | pending |
| `update.weather_update.default.001` | 533 | `default:` |  | pending |
| `update.weather_update.break.006` | 536 | `break;` |  | pending |
| `update.weather_update.case.006` | 538 | `case SKY_CLOUDLESS:` |  | pending |
| `update.weather_update.if.004` | 539 | `if ( weather_info.mmhg <  990 	\|\| ( weather_info.mmhg < 1010 && number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.or.001` | 540 | `\|\| ( weather_info.mmhg < 1010 && number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.and.002` | 540 | `&& number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.break.007` | 545 | `break;` |  | pending |
| `update.weather_update.case.007` | 547 | `case SKY_CLOUDY:` |  | pending |
| `update.weather_update.if.005` | 548 | `if ( weather_info.mmhg <  970 	\|\| ( weather_info.mmhg <  990 && number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.or.002` | 549 | `\|\| ( weather_info.mmhg <  990 && number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.and.003` | 549 | `&& number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.if.006` | 555 | `if ( weather_info.mmhg > 1030 && number_bits( 2 ) == 0 )` |  | pending |
| `update.weather_update.and.004` | 555 | `&& number_bits( 2 ) == 0 )` |  | pending |
| `update.weather_update.break.008` | 560 | `break;` |  | pending |
| `update.weather_update.case.008` | 562 | `case SKY_RAINING:` |  | pending |
| `update.weather_update.if.007` | 563 | `if ( weather_info.mmhg <  970 && number_bits( 2 ) == 0 )` |  | pending |
| `update.weather_update.and.005` | 563 | `&& number_bits( 2 ) == 0 )` |  | pending |
| `update.weather_update.if.008` | 569 | `if ( weather_info.mmhg > 1030 	\|\| ( weather_info.mmhg > 1010 && number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.or.003` | 570 | `\|\| ( weather_info.mmhg > 1010 && number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.and.006` | 570 | `&& number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.break.009` | 575 | `break;` |  | pending |
| `update.weather_update.case.009` | 577 | `case SKY_LIGHTNING:` |  | pending |
| `update.weather_update.if.009` | 578 | `if ( weather_info.mmhg > 1010 	\|\| ( weather_info.mmhg >  990 && number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.or.004` | 579 | `\|\| ( weather_info.mmhg >  990 && number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.and.007` | 579 | `&& number_bits( 2 ) == 0 ) )` |  | pending |
| `update.weather_update.break.010` | 583 | `break;` |  | pending |
| `update.weather_update.break.011` | 585 | `break;` |  | pending |
| `update.weather_update.if.010` | 588 | `if ( buf[0] != '\0' )` |  | pending |
| `update.weather_update.for.001` | 590 | `for ( d = descriptor_list; d != NULL; d = d->next )` |  | pending |
| `update.weather_update.if.011` | 592 | `if ( d->connected == CON_PLAYING 	    &&   IS_OUTSIDE(d->character) 	    &&   IS_AWAKE(d->character) )` |  | pending |
| `update.weather_update.and.008` | 593 | `&&   IS_OUTSIDE(d->character)` |  | pending |
| `update.weather_update.and.009` | 594 | `&&   IS_AWAKE(d->character) )` |  | pending |
| `update.weather_update.return.001` | 599 | `return;` |  | pending |

## char_update

[Source line 607](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:607); ends at line 840. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- update_handler: `src/update.c:1120` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/update.c:48` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_AFFECTED`, `number_percent`, `act`, `extract_char`, `hit_gain`, `mana_gain`, `move_gain`, `update_pos`, `get_eq_char`, `extract_obj`, `IS_IMMORTAL`, `stop_fighting`, `send_to_char`, `save_char_obj`, `char_from_room`, `char_to_room`, `get_room_index`, `gain_condition`, `number_range`, `affect_remove`, `is_affected`, `REMOVE_BIT`, `saves_spell`, `number_bits`, `affect_join`, `UMIN`, `damage`, `affect_find`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.char_update.if.001` | 618 | `if (save_number > 29)` |  | pending |
| `update.char_update.for.001` | 621 | `for ( ch = char_list; ch != NULL; ch = ch_next )` |  | pending |
| `update.char_update.if.002` | 628 | `if ( ch->timer > 30 )` |  | pending |
| `update.char_update.if.003` | 631 | `if ( ch->position >= POS_STUNNED )` |  | pending |
| `update.char_update.if.004` | 634 | `if (IS_NPC(ch) && ch->zone != NULL && ch->zone != ch->in_room->area             && ch->desc == NULL &&  ch->fighting == NULL  	    && !IS_AFFECTED(ch,AFF_CHARM) && number_percent() < 5)` |  | pending |
| `update.char_update.and.001` | 634 | `&& ch->zone != NULL && ch->zone != ch->in_room->area` |  | pending |
| `update.char_update.and.002` | 634 | `&& ch->zone != ch->in_room->area` |  | pending |
| `update.char_update.and.003` | 635 | `&& ch->desc == NULL &&  ch->fighting == NULL` |  | pending |
| `update.char_update.and.004` | 635 | `&&  ch->fighting == NULL` |  | pending |
| `update.char_update.and.005` | 636 | `&& !IS_AFFECTED(ch,AFF_CHARM) && number_percent() < 5)` |  | pending |
| `update.char_update.and.006` | 636 | `&& number_percent() < 5)` |  | pending |
| `update.char_update.continue.001` | 640 | `continue;` |  | pending |
| `update.char_update.if.005` | 643 | `if ( ch->hit  < ch->max_hit )` |  | pending |
| `update.char_update.if.006` | 648 | `if ( ch->mana < ch->max_mana )` |  | pending |
| `update.char_update.if.007` | 653 | `if ( ch->move < ch->max_move )` |  | pending |
| `update.char_update.if.008` | 659 | `if ( ch->position == POS_STUNNED )` |  | pending |
| `update.char_update.if.009` | 662 | `if ( !IS_NPC(ch) && ch->level < LEVEL_IMMORTAL )` |  | pending |
| `update.char_update.and.007` | 662 | `&& ch->level < LEVEL_IMMORTAL )` |  | pending |
| `update.char_update.if.010` | 666 | `if ( ( obj = get_eq_char( ch, WEAR_LIGHT ) ) != NULL 	    &&   obj->item_type == ITEM_LIGHT 	    &&   obj->value[2] > 0 )` |  | pending |
| `update.char_update.and.008` | 667 | `&&   obj->item_type == ITEM_LIGHT` |  | pending |
| `update.char_update.and.009` | 668 | `&&   obj->value[2] > 0 )` |  | pending |
| `update.char_update.if.011` | 670 | `if ( --obj->value[2] == 0 && ch->in_room != NULL )` |  | pending |
| `update.char_update.and.010` | 670 | `&& ch->in_room != NULL )` |  | pending |
| `update.char_update.if.012` | 677 | `if ( obj->value[2] <= 5 && ch->in_room != NULL)` |  | pending |
| `update.char_update.and.011` | 677 | `&& ch->in_room != NULL)` |  | pending |
| `update.char_update.if.013` | 681 | `if (IS_IMMORTAL(ch))` |  | pending |
| `update.char_update.if.014` | 684 | `if ( ++ch->timer >= 12 )` |  | pending |
| `update.char_update.if.015` | 686 | `if ( ch->was_in_room == NULL && ch->in_room != NULL )` |  | pending |
| `update.char_update.and.012` | 686 | `&& ch->in_room != NULL )` |  | pending |
| `update.char_update.if.016` | 689 | `if ( ch->fighting != NULL )` |  | pending |
| `update.char_update.if.017` | 694 | `if (ch->level > 1)` |  | pending |
| `update.char_update.ternary.001` | 702 | `? -4 : -2 );` |  | pending |
| `update.char_update.ternary.002` | 704 | `? -2 : -1);` |  | pending |
| `update.char_update.for.002` | 707 | `for ( paf = ch->affected; paf != NULL; paf = paf_next )` |  | pending |
| `update.char_update.if.018` | 710 | `if ( paf->duration > 0 )` |  | pending |
| `update.char_update.if.019` | 713 | `if (number_range(0,4) == 0 && paf->level > 0)` |  | pending |
| `update.char_update.and.013` | 713 | `&& paf->level > 0)` |  | pending |
| `update.char_update.if.020` | 716 | `if ( paf->duration < 0 )` |  | pending |
| `update.char_update.if.021` | 720 | `if ( paf_next == NULL 		\|\|   paf_next->type != paf->type 		\|\|   paf_next->duration > 0 )` |  | pending |
| `update.char_update.or.001` | 721 | `\|\|   paf_next->type != paf->type` |  | pending |
| `update.char_update.or.002` | 722 | `\|\|   paf_next->duration > 0 )` |  | pending |
| `update.char_update.if.022` | 724 | `if ( paf->type > 0 && skill_table[paf->type].msg_off )` |  | pending |
| `update.char_update.and.014` | 724 | `&& skill_table[paf->type].msg_off )` |  | pending |
| `update.char_update.if.023` | 741 | `if (is_affected(ch, gsn_plague) && ch != NULL)` |  | pending |
| `update.char_update.and.015` | 741 | `&& ch != NULL)` |  | pending |
| `update.char_update.if.024` | 747 | `if (ch->in_room == NULL)` |  | pending |
| `update.char_update.continue.002` | 748 | `continue;` |  | pending |
| `update.char_update.for.003` | 753 | `for ( af = ch->affected; af != NULL; af = af->next )` |  | pending |
| `update.char_update.if.025` | 755 | `if (af->type == gsn_plague)` |  | pending |
| `update.char_update.break.001` | 756 | `break;` |  | pending |
| `update.char_update.if.026` | 759 | `if (af == NULL)` |  | pending |
| `update.char_update.continue.003` | 762 | `continue;` |  | pending |
| `update.char_update.if.027` | 765 | `if (af->level == 1)` |  | pending |
| `update.char_update.continue.004` | 766 | `continue;` |  | pending |
| `update.char_update.for.004` | 776 | `for ( vch = ch->in_room->people; vch != NULL; vch = vch->next_in_room)` |  | pending |
| `update.char_update.if.028` | 778 | `if (!saves_spell(plague.level - 2,vch,DAM_DISEASE)  		&&  !IS_IMMORTAL(vch)             	&&  !IS_AFFECTED(vch,AFF_PLAGUE) && number_bits(4) == 0)` |  | pending |
| `update.char_update.and.016` | 779 | `&&  !IS_IMMORTAL(vch)` |  | pending |
| `update.char_update.and.017` | 780 | `&&  !IS_AFFECTED(vch,AFF_PLAGUE) && number_bits(4) == 0)` |  | pending |
| `update.char_update.and.018` | 780 | `&& number_bits(4) == 0)` |  | pending |
| `update.char_update.if.029` | 793 | `if ( IS_AFFECTED(ch, AFF_POISON) && ch != NULL 	     &&   !IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `update.char_update.and.019` | 793 | `&& ch != NULL` |  | pending |
| `update.char_update.and.020` | 794 | `&&   !IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `update.char_update.if.030` | 801 | `if (poison != NULL)` |  | pending |
| `update.char_update.if.031` | 810 | `if ( ch->position == POS_INCAP && number_range(0,1) == 0)` |  | pending |
| `update.char_update.and.021` | 810 | `&& number_range(0,1) == 0)` |  | pending |
| `update.char_update.if.032` | 814 | `if ( ch->position == POS_MORTAL )` |  | pending |
| `update.char_update.for.005` | 824 | `for ( ch = char_list; ch != NULL; ch = ch_next )` |  | pending |
| `update.char_update.if.033` | 828 | `if (ch->desc != NULL && ch->desc->descriptor % 30 == save_number)` |  | pending |
| `update.char_update.and.022` | 828 | `&& ch->desc->descriptor % 30 == save_number)` |  | pending |
| `update.char_update.if.034` | 833 | `if (ch == ch_quit)` |  | pending |
| `update.char_update.return.001` | 839 | `return;` |  | pending |

## obj_update

[Source line 849](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:849); ends at line 985. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- update_handler: `src/update.c:1121` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/update.c:49` (declaration_or_dispatch_reference).

Dependencies: `number_range`, `act`, `affect_remove_obj`, `CAN_WEAR`, `IS_NPC`, `obj_from_obj`, `obj_to_obj`, `extract_obj`, `obj_to_room`, `obj_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.obj_update.for.001` | 855 | `for ( obj = object_list; obj != NULL; obj = obj_next )` |  | pending |
| `update.obj_update.for.002` | 863 | `for ( paf = obj->affected; paf != NULL; paf = paf_next )` |  | pending |
| `update.obj_update.if.001` | 866 | `if ( paf->duration > 0 )` |  | pending |
| `update.obj_update.if.002` | 869 | `if (number_range(0,4) == 0 && paf->level > 0)` |  | pending |
| `update.obj_update.and.001` | 869 | `&& paf->level > 0)` |  | pending |
| `update.obj_update.if.003` | 872 | `if ( paf->duration < 0 )` |  | pending |
| `update.obj_update.if.004` | 876 | `if ( paf_next == NULL                 \|\|   paf_next->type != paf->type                 \|\|   paf_next->duration > 0 )` |  | pending |
| `update.obj_update.or.001` | 877 | `\|\|   paf_next->type != paf->type` |  | pending |
| `update.obj_update.or.002` | 878 | `\|\|   paf_next->duration > 0 )` |  | pending |
| `update.obj_update.if.005` | 880 | `if ( paf->type > 0 && skill_table[paf->type].msg_obj )` |  | pending |
| `update.obj_update.and.002` | 880 | `&& skill_table[paf->type].msg_obj )` |  | pending |
| `update.obj_update.if.006` | 882 | `if (obj->carried_by != NULL)` |  | pending |
| `update.obj_update.if.007` | 888 | `if (obj->in_room != NULL  			&& obj->in_room->people != NULL)` |  | pending |
| `update.obj_update.and.003` | 889 | `&& obj->in_room->people != NULL)` |  | pending |
| `update.obj_update.if.008` | 903 | `if ( obj->timer <= 0 \|\| --obj->timer > 0 )` |  | pending |
| `update.obj_update.or.003` | 903 | `\|\| --obj->timer > 0 )` |  | pending |
| `update.obj_update.continue.001` | 904 | `continue;` |  | pending |
| `update.obj_update.switch.001` | 906 | `switch ( obj->item_type )` |  | pending |
| `update.obj_update.default.001` | 908 | `default:              message = "$p crumbles into dust.";` |  | pending |
| `update.obj_update.break.001` | 908 | `break;` |  | pending |
| `update.obj_update.case.001` | 909 | `case ITEM_FOUNTAIN:   message = "$p dries up.";` |  | pending |
| `update.obj_update.break.002` | 909 | `break;` |  | pending |
| `update.obj_update.case.002` | 910 | `case ITEM_CORPSE_NPC: message = "$p decays into dust.";` |  | pending |
| `update.obj_update.break.003` | 910 | `break;` |  | pending |
| `update.obj_update.case.003` | 911 | `case ITEM_CORPSE_PC:  message = "$p decays into dust.";` |  | pending |
| `update.obj_update.break.004` | 911 | `break;` |  | pending |
| `update.obj_update.case.004` | 912 | `case ITEM_FOOD:       message = "$p decomposes.";` |  | pending |
| `update.obj_update.break.005` | 912 | `break;` |  | pending |
| `update.obj_update.case.005` | 913 | `case ITEM_POTION:     message = "$p has evaporated from disuse.";` |  | pending |
| `update.obj_update.break.006` | 914 | `break;` |  | pending |
| `update.obj_update.case.006` | 915 | `case ITEM_PORTAL:     message = "$p fades out of existence.";` |  | pending |
| `update.obj_update.break.007` | 915 | `break;` |  | pending |
| `update.obj_update.case.007` | 916 | `case ITEM_CONTAINER:` |  | pending |
| `update.obj_update.if.009` | 917 | `if (CAN_WEAR(obj,ITEM_WEAR_FLOAT))` |  | pending |
| `update.obj_update.if.010` | 918 | `if (obj->contains)` |  | pending |
| `update.obj_update.break.008` | 925 | `break;` |  | pending |
| `update.obj_update.if.011` | 928 | `if ( obj->carried_by != NULL )` |  | pending |
| `update.obj_update.if.012` | 930 | `if (IS_NPC(obj->carried_by)  	    &&  obj->carried_by->pIndexData->pShop != NULL)` |  | pending |
| `update.obj_update.and.004` | 931 | `&&  obj->carried_by->pIndexData->pShop != NULL)` |  | pending |
| `update.obj_update.if.013` | 936 | `if ( obj->wear_loc == WEAR_FLOAT)` |  | pending |
| `update.obj_update.if.014` | 940 | `if ( obj->in_room != NULL 	&&      ( rch = obj->in_room->people ) != NULL )` |  | pending |
| `update.obj_update.and.005` | 941 | `&&      ( rch = obj->in_room->people ) != NULL )` |  | pending |
| `update.obj_update.if.015` | 943 | `if (! (obj->in_obj && obj->in_obj->pIndexData->vnum == OBJ_VNUM_PIT 	           && !CAN_WEAR(obj->in_obj,ITEM_TAKE)))` |  | pending |
| `update.obj_update.and.006` | 943 | `&& obj->in_obj->pIndexData->vnum == OBJ_VNUM_PIT` |  | pending |
| `update.obj_update.and.007` | 944 | `&& !CAN_WEAR(obj->in_obj,ITEM_TAKE)))` |  | pending |
| `update.obj_update.if.016` | 951 | `if ((obj->item_type == ITEM_CORPSE_PC \|\| obj->wear_loc == WEAR_FLOAT) 	&&  obj->contains)` |  | pending |
| `update.obj_update.or.004` | 951 | `\|\| obj->wear_loc == WEAR_FLOAT)` |  | pending |
| `update.obj_update.and.008` | 952 | `&&  obj->contains)` |  | pending |
| `update.obj_update.for.003` | 956 | `for (t_obj = obj->contains; t_obj != NULL; t_obj = next_obj)` |  | pending |
| `update.obj_update.if.017` | 961 | `if (obj->in_obj)` |  | pending |
| `update.obj_update.if.018` | 964 | `if (obj->carried_by)` |  | pending |
| `update.obj_update.if.019` | 965 | `if (obj->wear_loc == WEAR_FLOAT)` |  | pending |
| `update.obj_update.if.020` | 966 | `if (obj->carried_by->in_room == NULL)` |  | pending |
| `update.obj_update.if.021` | 973 | `if (obj->in_room == NULL)` |  | pending |
| `update.obj_update.return.001` | 984 | `return;` |  | pending |

## aggr_update

[Source line 1003](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:1003); ends at line 1071. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- update_handler: `src/update.c:1124` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/update.c:50` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `IS_AFFECTED`, `IS_AWAKE`, `can_see`, `number_bits`, `number_range`, `multi_hit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.aggr_update.for.001` | 1013 | `for ( wch = char_list; wch != NULL; wch = wch_next )` |  | pending |
| `update.aggr_update.if.001` | 1016 | `if ( IS_NPC(wch) 	\|\|   wch->level >= LEVEL_IMMORTAL 	\|\|   wch->in_room == NULL  	\|\|   wch->in_room->area->empty)` |  | pending |
| `update.aggr_update.or.001` | 1017 | `\|\|   wch->level >= LEVEL_IMMORTAL` |  | pending |
| `update.aggr_update.or.002` | 1018 | `\|\|   wch->in_room == NULL` |  | pending |
| `update.aggr_update.or.003` | 1019 | `\|\|   wch->in_room->area->empty)` |  | pending |
| `update.aggr_update.continue.001` | 1020 | `continue;` |  | pending |
| `update.aggr_update.for.002` | 1022 | `for ( ch = wch->in_room->people; ch != NULL; ch = ch_next )` |  | pending |
| `update.aggr_update.if.002` | 1028 | `if ( !IS_NPC(ch) 	    \|\|   !IS_SET(ch->act, ACT_AGGRESSIVE) 	    \|\|   IS_SET(ch->in_room->room_flags,ROOM_SAFE) 	    \|\|   IS_AFFECTED(ch,AFF_CALM) 	    \|\|   ch->fighting != NULL 	    \|\|   IS_AFFECTED(ch, AFF_CHARM) 	    \|\|   !IS_AWAKE(ch) 	    \|\|   ( IS_SET(ch->act, ACT_WIMPY) && IS_AWAKE(wch) ) 	    \|\|   !can_see( ch, wch )  	    \|\|   number_bits(1) == 0)` |  | pending |
| `update.aggr_update.or.004` | 1029 | `\|\|   !IS_SET(ch->act, ACT_AGGRESSIVE)` |  | pending |
| `update.aggr_update.or.005` | 1030 | `\|\|   IS_SET(ch->in_room->room_flags,ROOM_SAFE)` |  | pending |
| `update.aggr_update.or.006` | 1031 | `\|\|   IS_AFFECTED(ch,AFF_CALM)` |  | pending |
| `update.aggr_update.or.007` | 1032 | `\|\|   ch->fighting != NULL` |  | pending |
| `update.aggr_update.or.008` | 1033 | `\|\|   IS_AFFECTED(ch, AFF_CHARM)` |  | pending |
| `update.aggr_update.or.009` | 1034 | `\|\|   !IS_AWAKE(ch)` |  | pending |
| `update.aggr_update.or.010` | 1035 | `\|\|   ( IS_SET(ch->act, ACT_WIMPY) && IS_AWAKE(wch) )` |  | pending |
| `update.aggr_update.and.001` | 1035 | `&& IS_AWAKE(wch) )` |  | pending |
| `update.aggr_update.or.011` | 1036 | `\|\|   !can_see( ch, wch )` |  | pending |
| `update.aggr_update.or.012` | 1037 | `\|\|   number_bits(1) == 0)` |  | pending |
| `update.aggr_update.continue.002` | 1038 | `continue;` |  | pending |
| `update.aggr_update.for.003` | 1047 | `for ( vch = wch->in_room->people; vch != NULL; vch = vch_next )` |  | pending |
| `update.aggr_update.if.003` | 1051 | `if ( !IS_NPC(vch) 		&&   vch->level < LEVEL_IMMORTAL 		&&   ch->level >= vch->level - 5  		&&   ( !IS_SET(ch->act, ACT_WIMPY) \|\| !IS_AWAKE(vch) ) 		&&   can_see( ch, vch ) )` |  | pending |
| `update.aggr_update.and.002` | 1052 | `&&   vch->level < LEVEL_IMMORTAL` |  | pending |
| `update.aggr_update.and.003` | 1053 | `&&   ch->level >= vch->level - 5` |  | pending |
| `update.aggr_update.and.004` | 1054 | `&&   ( !IS_SET(ch->act, ACT_WIMPY) \|\| !IS_AWAKE(vch) )` |  | pending |
| `update.aggr_update.or.013` | 1054 | `\|\| !IS_AWAKE(vch) )` |  | pending |
| `update.aggr_update.and.005` | 1055 | `&&   can_see( ch, vch ) )` |  | pending |
| `update.aggr_update.if.004` | 1057 | `if ( number_range( 0, count ) == 0 )` |  | pending |
| `update.aggr_update.if.005` | 1063 | `if ( victim == NULL )` |  | pending |
| `update.aggr_update.continue.003` | 1064 | `continue;` |  | pending |
| `update.aggr_update.return.001` | 1070 | `return;` |  | pending |

## update_handler

[Source line 1081](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:1081); ends at line 1127. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_mac_msdos: `src/comm.c:590` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:781` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2314` (declaration_or_dispatch_reference).

Dependencies: `area_update`, `song_update`, `mobile_update`, `violence_update`, `wiznet`, `weather_update`, `char_update`, `obj_update`, `aggr_update`, `tail_chain`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `update.update_handler.if.001` | 1089 | `if ( --pulse_area     <= 0 )` |  | pending |
| `update.update_handler.if.002` | 1096 | `if ( --pulse_music	  <= 0 )` |  | pending |
| `update.update_handler.if.003` | 1102 | `if ( --pulse_mobile   <= 0 )` |  | pending |
| `update.update_handler.if.004` | 1108 | `if ( --pulse_violence <= 0 )` |  | pending |
| `update.update_handler.if.005` | 1114 | `if ( --pulse_point    <= 0 )` |  | pending |
| `update.update_handler.return.001` | 1126 | `return;` |  | pending |
| `update.update_handler.fresh-process-through-call-1.path` | 1083 | `fresh process through call 1` | update.update_handler.fresh-process-through-call-1 | specified |
| `update.update_handler.fresh-process-through-call-2.path` | 1083 | `fresh process through call 2` | update.update_handler.fresh-process-through-call-2 | specified |
| `update.update_handler.fresh-process-through-call-12.path` | 1083 | `fresh process through call 12` | update.update_handler.fresh-process-through-call-12 | specified |
| `update.update_handler.fresh-process-through-call-13.path` | 1083 | `fresh process through call 13` | update.update_handler.fresh-process-through-call-13 | specified |
| `update.update_handler.fresh-process-through-call-16.path` | 1083 | `fresh process through call 16` | update.update_handler.fresh-process-through-call-16 | specified |
| `update.update_handler.fresh-process-through-call-17.path` | 1083 | `fresh process through call 17` | update.update_handler.fresh-process-through-call-17 | specified |
| `update.update_handler.fresh-process-through-call-24.path` | 1083 | `fresh process through call 24` | update.update_handler.fresh-process-through-call-24 | specified |
| `update.update_handler.fresh-process-through-call-25.path` | 1083 | `fresh process through call 25` | update.update_handler.fresh-process-through-call-25 | specified |
| `update.update_handler.fresh-process-through-call-240.path` | 1083 | `fresh process through call 240` | update.update_handler.fresh-process-through-call-240 | specified |
| `update.update_handler.fresh-process-through-call-241.path` | 1083 | `fresh process through call 241` | update.update_handler.fresh-process-through-call-241 | specified |
| `update.update_handler.fresh-process-through-call-480.path` | 1083 | `fresh process through call 480` | update.update_handler.fresh-process-through-call-480 | specified |
| `update.update_handler.fresh-process-through-call-481.path` | 1083 | `fresh process through call 481` | update.update_handler.fresh-process-through-call-481 | specified |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#endif` — pending configuration/reachability review.
- Line 33: `#include <stdio.h>` — pending configuration/reachability review.
- Line 34: `#include <string.h>` — pending configuration/reachability review.
- Line 35: `#include <time.h>` — pending configuration/reachability review.
- Line 36: `#include "merc.h"` — pending configuration/reachability review.
- Line 37: `#include "interp.h"` — pending configuration/reachability review.
- Line 38: `#include "music.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


# src/fight.c

Role: translation_unit. Disposition: **pending**. SHA-256: `05a0de029900c1678e4de17139267dc464aab7c9312b11dc5de14be5f624eeeb`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## violence_update

[Source line 67](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:67); ends at line 95. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- update_handler: `src/update.c:1111` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2171` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `multi_hit`, `stop_fighting`, `check_assist`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.violence_update.for.001` | 73 | `for ( ch = char_list; ch != NULL; ch = ch->next )` |  | pending |
| `fight.violence_update.if.001` | 77 | `if ( ( victim = ch->fighting ) == NULL \|\| ch->in_room == NULL )` |  | pending |
| `fight.violence_update.or.001` | 77 | `\|\| ch->in_room == NULL )` |  | pending |
| `fight.violence_update.continue.001` | 78 | `continue;` |  | pending |
| `fight.violence_update.if.002` | 80 | `if ( IS_AWAKE(ch) && ch->in_room == victim->in_room )` |  | pending |
| `fight.violence_update.and.001` | 80 | `&& ch->in_room == victim->in_room )` |  | pending |
| `fight.violence_update.if.003` | 85 | `if ( ( victim = ch->fighting ) == NULL )` |  | pending |
| `fight.violence_update.continue.002` | 86 | `continue;` |  | pending |
| `fight.violence_update.return.001` | 94 | `return;` |  | pending |

## check_assist

[Source line 98](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:98); ends at line 181. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- violence_update: `src/fight.c:91` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:42` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `IS_NPC`, `IS_SET`, `do_function`, `multi_hit`, `IS_AFFECTED`, `is_same_group`, `is_safe`, `IS_GOOD`, `IS_EVIL`, `IS_NEUTRAL`, `number_bits`, `can_see`, `number_range`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.check_assist.for.001` | 102 | `for (rch = ch->in_room->people; rch != NULL; rch = rch_next)` |  | pending |
| `fight.check_assist.if.001` | 106 | `if (IS_AWAKE(rch) && rch->fighting == NULL)` |  | pending |
| `fight.check_assist.and.001` | 106 | `&& rch->fighting == NULL)` |  | pending |
| `fight.check_assist.if.002` | 110 | `if (!IS_NPC(ch) && IS_NPC(rch)  	    && IS_SET(rch->off_flags,ASSIST_PLAYERS) 	    &&  rch->level + 6 > victim->level)` |  | pending |
| `fight.check_assist.and.002` | 110 | `&& IS_NPC(rch)` |  | pending |
| `fight.check_assist.and.003` | 111 | `&& IS_SET(rch->off_flags,ASSIST_PLAYERS)` |  | pending |
| `fight.check_assist.and.004` | 112 | `&&  rch->level + 6 > victim->level)` |  | pending |
| `fight.check_assist.continue.001` | 116 | `continue;` |  | pending |
| `fight.check_assist.if.003` | 120 | `if (!IS_NPC(ch) \|\| IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `fight.check_assist.or.001` | 120 | `\|\| IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `fight.check_assist.if.004` | 122 | `if ( ( (!IS_NPC(rch) && IS_SET(rch->act,PLR_AUTOASSIST)) 		\|\|     IS_AFFECTED(rch,AFF_CHARM))  		&&   is_same_group(ch,rch)  		&&   !is_safe(rch, victim))` |  | pending |
| `fight.check_assist.and.005` | 122 | `&& IS_SET(rch->act,PLR_AUTOASSIST))` |  | pending |
| `fight.check_assist.or.002` | 123 | `\|\|     IS_AFFECTED(rch,AFF_CHARM))` |  | pending |
| `fight.check_assist.and.006` | 124 | `&&   is_same_group(ch,rch)` |  | pending |
| `fight.check_assist.and.007` | 125 | `&&   !is_safe(rch, victim))` |  | pending |
| `fight.check_assist.continue.002` | 128 | `continue;` |  | pending |
| `fight.check_assist.if.005` | 133 | `if (IS_NPC(ch) && !IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `fight.check_assist.and.008` | 133 | `&& !IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `fight.check_assist.if.006` | 136 | `if ( (IS_NPC(rch) && IS_SET(rch->off_flags,ASSIST_ALL))  		\|\|   (IS_NPC(rch) && rch->group && rch->group == ch->group)  		\|\|   (IS_NPC(rch) && rch->race == ch->race  		   && IS_SET(rch->off_flags,ASSIST_RACE))  		\|\|   (IS_NPC(rch) && IS_SET(rch->off_flags,ASSIST_ALIGN) 		   &&   ((IS_GOOD(rch)    && IS_GOOD(ch)) 		     \|\|  (IS_EVIL(rch)    && IS_EVIL(ch)) 		     \|\|  (IS_NEUTRAL(rch) && IS_NEUTRAL(ch))))   		\|\|   (rch->pIndexData == ch->pIndexData  		   && IS_SET(rch->off_flags,ASSIST_VNUM)))` |  | pending |
| `fight.check_assist.and.009` | 136 | `&& IS_SET(rch->off_flags,ASSIST_ALL))` |  | pending |
| `fight.check_assist.or.003` | 138 | `\|\|   (IS_NPC(rch) && rch->group && rch->group == ch->group)` |  | pending |
| `fight.check_assist.and.010` | 138 | `&& rch->group && rch->group == ch->group)` |  | pending |
| `fight.check_assist.and.011` | 138 | `&& rch->group == ch->group)` |  | pending |
| `fight.check_assist.or.004` | 140 | `\|\|   (IS_NPC(rch) && rch->race == ch->race` |  | pending |
| `fight.check_assist.and.012` | 140 | `&& rch->race == ch->race` |  | pending |
| `fight.check_assist.and.013` | 141 | `&& IS_SET(rch->off_flags,ASSIST_RACE))` |  | pending |
| `fight.check_assist.or.005` | 143 | `\|\|   (IS_NPC(rch) && IS_SET(rch->off_flags,ASSIST_ALIGN)` |  | pending |
| `fight.check_assist.and.014` | 143 | `&& IS_SET(rch->off_flags,ASSIST_ALIGN)` |  | pending |
| `fight.check_assist.and.015` | 144 | `&&   ((IS_GOOD(rch)    && IS_GOOD(ch))` |  | pending |
| `fight.check_assist.and.016` | 144 | `&& IS_GOOD(ch))` |  | pending |
| `fight.check_assist.or.006` | 145 | `\|\|  (IS_EVIL(rch)    && IS_EVIL(ch))` |  | pending |
| `fight.check_assist.and.017` | 145 | `&& IS_EVIL(ch))` |  | pending |
| `fight.check_assist.or.007` | 146 | `\|\|  (IS_NEUTRAL(rch) && IS_NEUTRAL(ch))))` |  | pending |
| `fight.check_assist.and.018` | 146 | `&& IS_NEUTRAL(ch))))` |  | pending |
| `fight.check_assist.or.008` | 148 | `\|\|   (rch->pIndexData == ch->pIndexData` |  | pending |
| `fight.check_assist.and.019` | 149 | `&& IS_SET(rch->off_flags,ASSIST_VNUM)))` |  | pending |
| `fight.check_assist.if.007` | 156 | `if (number_bits(1) == 0)` |  | pending |
| `fight.check_assist.continue.003` | 157 | `continue;` |  | pending |
| `fight.check_assist.for.002` | 161 | `for (vch = ch->in_room->people; vch; vch = vch->next)` |  | pending |
| `fight.check_assist.if.008` | 163 | `if (can_see(rch,vch) 			&&  is_same_group(vch,victim) 			&&  number_range(0,number) == 0)` |  | pending |
| `fight.check_assist.and.020` | 164 | `&&  is_same_group(vch,victim)` |  | pending |
| `fight.check_assist.and.021` | 165 | `&&  number_range(0,number) == 0)` |  | pending |
| `fight.check_assist.if.009` | 172 | `if (target != NULL)` |  | pending |

## multi_hit

[Source line 187](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:187); ends at line 247. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_steal: `src/act_obj.c:2224` (lexical_call_candidate).
- violence_update: `src/fight.c:81` (lexical_call_candidate).
- check_assist: `src/fight.c:115` (lexical_call_candidate).
- check_assist: `src/fight.c:126` (lexical_call_candidate).
- check_assist: `src/fight.c:175` (lexical_call_candidate).
- do_kill: `src/fight.c:2620` (lexical_call_candidate).
- do_kill: `src/fight.c:2648` (lexical_call_candidate).
- do_murder: `src/fight.c:2721` (lexical_call_candidate).
- do_backstab: `src/fight.c:2789` (lexical_call_candidate).
- do_cast: `src/magic.c:569` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:710` (lexical_call_candidate).
- spec_troll_member: `src/special.c:181` (lexical_call_candidate).
- spec_ogre_member: `src/special.c:240` (lexical_call_candidate).
- spec_patrolman: `src/special.c:317` (lexical_call_candidate).
- spec_executioner: `src/special.c:752` (lexical_call_candidate).
- spec_guard: `src/special.c:833` (lexical_call_candidate).
- spec_guard: `src/special.c:841` (lexical_call_candidate).
- aggr_update: `src/update.c:1066` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2172` (declaration_or_dispatch_reference).

Dependencies: `UMAX`, `IS_NPC`, `mob_hit`, `one_hit`, `IS_AFFECTED`, `get_skill`, `number_percent`, `check_improve`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.multi_hit.if.001` | 192 | `if (ch->desc == NULL)` |  | pending |
| `fight.multi_hit.if.002` | 195 | `if (ch->desc == NULL)` |  | pending |
| `fight.multi_hit.if.003` | 200 | `if (ch->position < POS_RESTING)` |  | pending |
| `fight.multi_hit.return.001` | 201 | `return;` |  | pending |
| `fight.multi_hit.if.004` | 203 | `if (IS_NPC(ch))` |  | pending |
| `fight.multi_hit.return.002` | 206 | `return;` |  | pending |
| `fight.multi_hit.if.005` | 211 | `if (ch->fighting != victim)` |  | pending |
| `fight.multi_hit.return.003` | 212 | `return;` |  | pending |
| `fight.multi_hit.if.006` | 214 | `if (IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `fight.multi_hit.if.007` | 217 | `if ( ch->fighting != victim \|\| dt == gsn_backstab )` |  | pending |
| `fight.multi_hit.or.001` | 217 | `\|\| dt == gsn_backstab )` |  | pending |
| `fight.multi_hit.return.004` | 218 | `return;` |  | pending |
| `fight.multi_hit.if.008` | 222 | `if (IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `fight.multi_hit.if.009` | 225 | `if ( number_percent( ) < chance )` |  | pending |
| `fight.multi_hit.if.010` | 229 | `if ( ch->fighting != victim )` |  | pending |
| `fight.multi_hit.return.005` | 230 | `return;` |  | pending |
| `fight.multi_hit.if.011` | 235 | `if (IS_AFFECTED(ch,AFF_SLOW))` |  | pending |
| `fight.multi_hit.if.012` | 238 | `if ( number_percent( ) < chance )` |  | pending |
| `fight.multi_hit.if.013` | 242 | `if ( ch->fighting != victim )` |  | pending |
| `fight.multi_hit.return.006` | 243 | `return;` |  | pending |
| `fight.multi_hit.return.007` | 246 | `return;` |  | pending |

## mob_hit

[Source line 250](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:250); ends at line 379. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- multi_hit: `src/fight.c:205` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:56` (declaration_or_dispatch_reference).

Dependencies: `one_hit`, `IS_SET`, `IS_AFFECTED`, `get_skill`, `number_percent`, `number_range`, `case`, `do_function`, `get_weapon_sn`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.mob_hit.if.001` | 257 | `if (ch->fighting != victim)` |  | pending |
| `fight.mob_hit.return.001` | 258 | `return;` |  | pending |
| `fight.mob_hit.if.002` | 262 | `if (IS_SET(ch->off_flags,OFF_AREA_ATTACK))` |  | pending |
| `fight.mob_hit.for.001` | 264 | `for (vch = ch->in_room->people; vch != NULL; vch = vch_next)` |  | pending |
| `fight.mob_hit.if.003` | 267 | `if ((vch != victim && vch->fighting == ch))` |  | pending |
| `fight.mob_hit.and.001` | 267 | `&& vch->fighting == ch))` |  | pending |
| `fight.mob_hit.if.004` | 272 | `if (IS_AFFECTED(ch,AFF_HASTE)      \|\|  (IS_SET(ch->off_flags,OFF_FAST) && !IS_AFFECTED(ch,AFF_SLOW)))` |  | pending |
| `fight.mob_hit.or.001` | 273 | `\|\|  (IS_SET(ch->off_flags,OFF_FAST) && !IS_AFFECTED(ch,AFF_SLOW)))` |  | pending |
| `fight.mob_hit.and.002` | 273 | `&& !IS_AFFECTED(ch,AFF_SLOW)))` |  | pending |
| `fight.mob_hit.if.005` | 276 | `if (ch->fighting != victim \|\| dt == gsn_backstab)` |  | pending |
| `fight.mob_hit.or.002` | 276 | `\|\| dt == gsn_backstab)` |  | pending |
| `fight.mob_hit.return.002` | 277 | `return;` |  | pending |
| `fight.mob_hit.if.006` | 281 | `if (IS_AFFECTED(ch,AFF_SLOW) && !IS_SET(ch->off_flags,OFF_FAST))` |  | pending |
| `fight.mob_hit.and.003` | 281 | `&& !IS_SET(ch->off_flags,OFF_FAST))` |  | pending |
| `fight.mob_hit.if.007` | 284 | `if (number_percent() < chance)` |  | pending |
| `fight.mob_hit.if.008` | 287 | `if (ch->fighting != victim)` |  | pending |
| `fight.mob_hit.return.003` | 288 | `return;` |  | pending |
| `fight.mob_hit.if.009` | 293 | `if (IS_AFFECTED(ch,AFF_SLOW) && !IS_SET(ch->off_flags,OFF_FAST))` |  | pending |
| `fight.mob_hit.and.004` | 293 | `&& !IS_SET(ch->off_flags,OFF_FAST))` |  | pending |
| `fight.mob_hit.if.010` | 296 | `if (number_percent() < chance)` |  | pending |
| `fight.mob_hit.if.011` | 299 | `if (ch->fighting != victim)` |  | pending |
| `fight.mob_hit.return.004` | 300 | `return;` |  | pending |
| `fight.mob_hit.if.012` | 305 | `if (ch->wait > 0)` |  | pending |
| `fight.mob_hit.return.005` | 306 | `return;` |  | pending |
| `fight.mob_hit.if.013` | 310 | `if (number == 1 && IS_SET(ch->act,ACT_MAGE))` |  | pending |
| `fight.mob_hit.and.005` | 310 | `&& IS_SET(ch->act,ACT_MAGE))` |  | pending |
| `fight.mob_hit.if.014` | 315 | `if (number == 2 && IS_SET(ch->act,ACT_CLERIC))` |  | pending |
| `fight.mob_hit.and.006` | 315 | `&& IS_SET(ch->act,ACT_CLERIC))` |  | pending |
| `fight.mob_hit.switch.001` | 324 | `switch(number)` |  | pending |
| `fight.mob_hit.case.001` | 326 | `case (0) :` |  | pending |
| `fight.mob_hit.if.015` | 327 | `if (IS_SET(ch->off_flags,OFF_BASH))` |  | pending |
| `fight.mob_hit.break.001` | 329 | `break;` |  | pending |
| `fight.mob_hit.case.002` | 331 | `case (1) :` |  | pending |
| `fight.mob_hit.if.016` | 332 | `if (IS_SET(ch->off_flags,OFF_BERSERK) && !IS_AFFECTED(ch,AFF_BERSERK))` |  | pending |
| `fight.mob_hit.and.007` | 332 | `&& !IS_AFFECTED(ch,AFF_BERSERK))` |  | pending |
| `fight.mob_hit.break.002` | 334 | `break;` |  | pending |
| `fight.mob_hit.case.003` | 337 | `case (2) :` |  | pending |
| `fight.mob_hit.if.017` | 338 | `if (IS_SET(ch->off_flags,OFF_DISARM)  	\|\| (get_weapon_sn(ch) != gsn_hand_to_hand  	&& (IS_SET(ch->act,ACT_WARRIOR)    	\|\|  IS_SET(ch->act,ACT_THIEF))))` |  | pending |
| `fight.mob_hit.or.003` | 339 | `\|\| (get_weapon_sn(ch) != gsn_hand_to_hand` |  | pending |
| `fight.mob_hit.and.008` | 340 | `&& (IS_SET(ch->act,ACT_WARRIOR)` |  | pending |
| `fight.mob_hit.or.004` | 341 | `\|\|  IS_SET(ch->act,ACT_THIEF))))` |  | pending |
| `fight.mob_hit.break.003` | 343 | `break;` |  | pending |
| `fight.mob_hit.case.004` | 345 | `case (3) :` |  | pending |
| `fight.mob_hit.if.018` | 346 | `if (IS_SET(ch->off_flags,OFF_KICK))` |  | pending |
| `fight.mob_hit.break.004` | 348 | `break;` |  | pending |
| `fight.mob_hit.case.005` | 350 | `case (4) :` |  | pending |
| `fight.mob_hit.if.019` | 351 | `if (IS_SET(ch->off_flags,OFF_KICK_DIRT))` |  | pending |
| `fight.mob_hit.break.005` | 353 | `break;` |  | pending |
| `fight.mob_hit.case.006` | 355 | `case (5) :` |  | pending |
| `fight.mob_hit.if.020` | 356 | `if (IS_SET(ch->off_flags,OFF_TAIL))` |  | pending |
| `fight.mob_hit.break.006` | 360 | `break;` |  | pending |
| `fight.mob_hit.case.007` | 362 | `case (6) :` |  | pending |
| `fight.mob_hit.if.021` | 363 | `if (IS_SET(ch->off_flags,OFF_TRIP))` |  | pending |
| `fight.mob_hit.break.007` | 365 | `break;` |  | pending |
| `fight.mob_hit.case.008` | 367 | `case (7) :` |  | pending |
| `fight.mob_hit.if.022` | 368 | `if (IS_SET(ch->off_flags,OFF_CRUSH))` |  | pending |
| `fight.mob_hit.break.008` | 372 | `break;` |  | pending |
| `fight.mob_hit.case.009` | 373 | `case (8) :` |  | pending |
| `fight.mob_hit.if.023` | 374 | `if (IS_SET(ch->off_flags,OFF_BACKSTAB))` |  | pending |

## one_hit

[Source line 385](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:385); ends at line 669. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- multi_hit: `src/fight.c:209` (lexical_call_candidate).
- multi_hit: `src/fight.c:215` (lexical_call_candidate).
- multi_hit: `src/fight.c:227` (lexical_call_candidate).
- multi_hit: `src/fight.c:240` (lexical_call_candidate).
- mob_hit: `src/fight.c:255` (lexical_call_candidate).
- mob_hit: `src/fight.c:268` (lexical_call_candidate).
- mob_hit: `src/fight.c:274` (lexical_call_candidate).
- mob_hit: `src/fight.c:286` (lexical_call_candidate).
- mob_hit: `src/fight.c:298` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:55` (declaration_or_dispatch_reference).

Dependencies: `get_eq_char`, `get_weapon_sn`, `get_weapon_skill`, `IS_NPC`, `IS_SET`, `interpolate`, `GET_HITROLL`, `get_skill`, `case`, `GET_AC`, `can_see`, `number_bits`, `damage`, `tail_chain`, `number_range`, `dice`, `check_improve`, `IS_WEAPON_STAT`, `number_percent`, `IS_AWAKE`, `GET_DAMROLL`, `UMIN`, `affect_find`, `saves_spell`, `send_to_char`, `act`, `affect_join`, `UMAX`, `fire_effect`, `cold_effect`, `shock_effect`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.one_hit.if.001` | 402 | `if (victim == ch \|\| ch == NULL \|\| victim == NULL)` |  | pending |
| `fight.one_hit.or.001` | 402 | `\|\| ch == NULL \|\| victim == NULL)` |  | pending |
| `fight.one_hit.or.002` | 402 | `\|\| victim == NULL)` |  | pending |
| `fight.one_hit.return.001` | 403 | `return;` |  | pending |
| `fight.one_hit.if.002` | 409 | `if ( victim->position == POS_DEAD \|\| ch->in_room != victim->in_room )` |  | pending |
| `fight.one_hit.or.003` | 409 | `\|\| ch->in_room != victim->in_room )` |  | pending |
| `fight.one_hit.return.002` | 410 | `return;` |  | pending |
| `fight.one_hit.if.003` | 417 | `if ( dt == TYPE_UNDEFINED )` |  | pending |
| `fight.one_hit.if.004` | 420 | `if ( wield != NULL && wield->item_type == ITEM_WEAPON )` |  | pending |
| `fight.one_hit.and.001` | 420 | `&& wield->item_type == ITEM_WEAPON )` |  | pending |
| `fight.one_hit.if.005` | 426 | `if (dt < TYPE_HIT)` |  | pending |
| `fight.one_hit.if.006` | 427 | `if (wield != NULL)` |  | pending |
| `fight.one_hit.if.007` | 434 | `if (dam_type == -1)` |  | pending |
| `fight.one_hit.if.008` | 444 | `if ( IS_NPC(ch) )` |  | pending |
| `fight.one_hit.if.009` | 448 | `if (IS_SET(ch->act,ACT_WARRIOR))` |  | pending |
| `fight.one_hit.if.010` | 450 | `if (IS_SET(ch->act,ACT_THIEF))` |  | pending |
| `fight.one_hit.if.011` | 452 | `if (IS_SET(ch->act,ACT_CLERIC))` |  | pending |
| `fight.one_hit.if.012` | 454 | `if (IS_SET(ch->act,ACT_MAGE))` |  | pending |
| `fight.one_hit.if.013` | 464 | `if (thac0 < 0)` |  | pending |
| `fight.one_hit.if.014` | 467 | `if (thac0 < -5)` |  | pending |
| `fight.one_hit.if.015` | 473 | `if (dt == gsn_backstab)` |  | pending |
| `fight.one_hit.switch.001` | 476 | `switch(dam_type)` |  | pending |
| `fight.one_hit.case.001` | 478 | `case(DAM_PIERCE):victim_ac = GET_AC(victim,AC_PIERCE)/10;` |  | pending |
| `fight.one_hit.break.001` | 478 | `break;` |  | pending |
| `fight.one_hit.case.002` | 479 | `case(DAM_BASH):	 victim_ac = GET_AC(victim,AC_BASH)/10;` |  | pending |
| `fight.one_hit.break.002` | 479 | `break;` |  | pending |
| `fight.one_hit.case.003` | 480 | `case(DAM_SLASH): victim_ac = GET_AC(victim,AC_SLASH)/10;` |  | pending |
| `fight.one_hit.break.003` | 480 | `break;` |  | pending |
| `fight.one_hit.default.001` | 481 | `default:	 victim_ac = GET_AC(victim,AC_EXOTIC)/10;` |  | pending |
| `fight.one_hit.break.004` | 481 | `break;` |  | pending |
| `fight.one_hit.if.016` | 484 | `if (victim_ac < -15)` |  | pending |
| `fight.one_hit.if.017` | 487 | `if ( !can_see( ch, victim ) )` |  | pending |
| `fight.one_hit.if.018` | 490 | `if ( victim->position < POS_FIGHTING)` |  | pending |
| `fight.one_hit.if.019` | 493 | `if (victim->position < POS_RESTING)` |  | pending |
| `fight.one_hit.while.001` | 499 | `while ( ( diceroll = number_bits( 5 ) ) >= 20 )` |  | pending |
| `fight.one_hit.if.020` | 502 | `if ( diceroll == 0     \|\| ( diceroll != 19 && diceroll < thac0 - victim_ac ) )` |  | pending |
| `fight.one_hit.or.004` | 503 | `\|\| ( diceroll != 19 && diceroll < thac0 - victim_ac ) )` |  | pending |
| `fight.one_hit.and.002` | 503 | `&& diceroll < thac0 - victim_ac ) )` |  | pending |
| `fight.one_hit.return.003` | 508 | `return;` |  | pending |
| `fight.one_hit.if.021` | 515 | `if ( IS_NPC(ch) && (!ch->pIndexData->new_format \|\| wield == NULL))` |  | pending |
| `fight.one_hit.and.003` | 515 | `&& (!ch->pIndexData->new_format \|\| wield == NULL))` |  | pending |
| `fight.one_hit.or.005` | 515 | `\|\| wield == NULL))` |  | pending |
| `fight.one_hit.if.022` | 516 | `if (!ch->pIndexData->new_format)` |  | pending |
| `fight.one_hit.if.023` | 519 | `if ( wield != NULL )` |  | pending |
| `fight.one_hit.if.024` | 527 | `if (sn != -1)` |  | pending |
| `fight.one_hit.if.025` | 529 | `if ( wield != NULL )` |  | pending |
| `fight.one_hit.if.026` | 531 | `if (wield->pIndexData->new_format)` |  | pending |
| `fight.one_hit.if.027` | 537 | `if (get_eq_char(ch,WEAR_SHIELD) == NULL)` |  | pending |
| `fight.one_hit.if.028` | 541 | `if (IS_WEAPON_STAT(wield,WEAPON_SHARP))` |  | pending |
| `fight.one_hit.if.029` | 545 | `if ((percent = number_percent()) <= (skill / 8))` |  | pending |
| `fight.one_hit.if.030` | 556 | `if ( get_skill(ch,gsn_enhanced_damage) > 0 )` |  | pending |
| `fight.one_hit.if.031` | 559 | `if (diceroll <= get_skill(ch,gsn_enhanced_damage))` |  | pending |
| `fight.one_hit.if.032` | 566 | `if ( !IS_AWAKE(victim) )` |  | pending |
| `fight.one_hit.if.033` | 568 | `if (victim->position < POS_FIGHTING)` |  | pending |
| `fight.one_hit.if.034` | 571 | `if ( dt == gsn_backstab && wield != NULL)` |  | pending |
| `fight.one_hit.and.004` | 571 | `&& wield != NULL)` |  | pending |
| `fight.one_hit.if.035` | 572 | `if ( wield->value[0] != 2 )` |  | pending |
| `fight.one_hit.if.036` | 579 | `if ( dam <= 0 )` |  | pending |
| `fight.one_hit.if.037` | 585 | `if (result && wield != NULL)` |  | pending |
| `fight.one_hit.and.005` | 585 | `&& wield != NULL)` |  | pending |
| `fight.one_hit.if.038` | 589 | `if (ch->fighting == victim && IS_WEAPON_STAT(wield,WEAPON_POISON))` |  | pending |
| `fight.one_hit.and.006` | 589 | `&& IS_WEAPON_STAT(wield,WEAPON_POISON))` |  | pending |
| `fight.one_hit.if.039` | 594 | `if ((poison = affect_find(wield->affected,gsn_poison)) == NULL)` |  | pending |
| `fight.one_hit.if.040` | 599 | `if (!saves_spell(level / 2,victim,DAM_POISON))` |  | pending |
| `fight.one_hit.if.041` | 617 | `if (poison != NULL)` |  | pending |
| `fight.one_hit.if.042` | 622 | `if (poison->level == 0 \|\| poison->duration == 0)` |  | pending |
| `fight.one_hit.or.006` | 622 | `\|\| poison->duration == 0)` |  | pending |
| `fight.one_hit.if.043` | 628 | `if (ch->fighting == victim && IS_WEAPON_STAT(wield,WEAPON_VAMPIRIC))` |  | pending |
| `fight.one_hit.and.007` | 628 | `&& IS_WEAPON_STAT(wield,WEAPON_VAMPIRIC))` |  | pending |
| `fight.one_hit.if.044` | 639 | `if (ch->fighting == victim && IS_WEAPON_STAT(wield,WEAPON_FLAMING))` |  | pending |
| `fight.one_hit.and.008` | 639 | `&& IS_WEAPON_STAT(wield,WEAPON_FLAMING))` |  | pending |
| `fight.one_hit.if.045` | 648 | `if (ch->fighting == victim && IS_WEAPON_STAT(wield,WEAPON_FROST))` |  | pending |
| `fight.one_hit.and.009` | 648 | `&& IS_WEAPON_STAT(wield,WEAPON_FROST))` |  | pending |
| `fight.one_hit.if.046` | 658 | `if (ch->fighting == victim && IS_WEAPON_STAT(wield,WEAPON_SHOCKING))` |  | pending |
| `fight.one_hit.and.010` | 658 | `&& IS_WEAPON_STAT(wield,WEAPON_SHOCKING))` |  | pending |
| `fight.one_hit.return.004` | 668 | `return;` |  | pending |

## damage

[Source line 675](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:675); ends at line 988. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_envenom: `src/act_obj.c:897` (function_symbol_reference_candidate).
- do_mstat: `src/act_wiz.c:1610` (function_symbol_reference_candidate).
- do_mstat: `src/act_wiz.c:1610` (function_symbol_reference_candidate).
- create_mobile: `src/db.c:1567` (function_symbol_reference_candidate).
- create_mobile: `src/db.c:1576` (function_symbol_reference_candidate).
- create_mobile: `src/db.c:1576` (function_symbol_reference_candidate).
- create_mobile: `src/db.c:1577` (function_symbol_reference_candidate).
- create_mobile: `src/db.c:1577` (function_symbol_reference_candidate).
- clone_mobile: `src/db.c:1810` (function_symbol_reference_candidate).
- clone_mobile: `src/db.c:1810` (function_symbol_reference_candidate).
- load_mobiles: `src/db2.c:207` (function_symbol_reference_candidate).
- load_mobiles: `src/db2.c:209` (function_symbol_reference_candidate).
- load_mobiles: `src/db2.c:211` (function_symbol_reference_candidate).
- one_hit: `src/fight.c:506` (lexical_call_candidate).
- one_hit: `src/fight.c:582` (lexical_call_candidate).
- one_hit: `src/fight.c:634` (lexical_call_candidate).
- one_hit: `src/fight.c:645` (lexical_call_candidate).
- one_hit: `src/fight.c:655` (lexical_call_candidate).
- one_hit: `src/fight.c:664` (lexical_call_candidate).
- one_hit: `src/fight.c:428` (function_symbol_reference_candidate).
- one_hit: `src/fight.c:430` (function_symbol_reference_candidate).
- one_hit: `src/fight.c:432` (function_symbol_reference_candidate).
- one_hit: `src/fight.c:523` (function_symbol_reference_candidate).
- one_hit: `src/fight.c:523` (function_symbol_reference_candidate).
- do_bash: `src/fight.c:2319` (lexical_call_candidate).
- do_bash: `src/fight.c:2325` (lexical_call_candidate).
- do_dirt: `src/fight.c:2448` (lexical_call_candidate).
- do_dirt: `src/fight.c:2465` (lexical_call_candidate).
- do_trip: `src/fight.c:2574` (lexical_call_candidate).
- do_trip: `src/fight.c:2579` (lexical_call_candidate).
- do_backstab: `src/fight.c:2794` (lexical_call_candidate).
- do_kick: `src/fight.c:2960` (lexical_call_candidate).
- do_kick: `src/fight.c:2965` (lexical_call_candidate).
- spell_acid_blast: `src/magic.c:732` (lexical_call_candidate).
- spell_burning_hands: `src/magic.c:896` (lexical_call_candidate).
- spell_call_lightning: `src/magic.c:934` (lexical_call_candidate).
- spell_cause_light: `src/magic.c:1184` (lexical_call_candidate).
- spell_cause_critical: `src/magic.c:1192` (lexical_call_candidate).
- spell_cause_serious: `src/magic.c:1200` (lexical_call_candidate).
- spell_chain_lightning: `src/magic.c:1223` (lexical_call_candidate).
- spell_chain_lightning: `src/magic.c:1245` (lexical_call_candidate).
- spell_chain_lightning: `src/magic.c:1269` (lexical_call_candidate).
- spell_chill_touch: `src/magic.c:1396` (lexical_call_candidate).
- spell_colour_spray: `src/magic.c:1425` (lexical_call_candidate).
- spell_demonfire: `src/magic.c:1779` (lexical_call_candidate).
- spell_dispel_evil: `src/magic.c:1976` (lexical_call_candidate).
- spell_dispel_good: `src/magic.c:2007` (lexical_call_candidate).
- spell_earthquake: `src/magic.c:2205` (lexical_call_candidate).
- spell_earthquake: `src/magic.c:2207` (lexical_call_candidate).
- spell_energy_drain: `src/magic.c:2653` (lexical_call_candidate).
- spell_fireball: `src/magic.c:2679` (lexical_call_candidate).
- spell_flamestrike: `src/magic.c:2719` (lexical_call_candidate).
- spell_harm: `src/magic.c:2970` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3168` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3208` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3219` (lexical_call_candidate).
- spell_lightning_bolt: `src/magic.c:3579` (lexical_call_candidate).
- spell_magic_missile: `src/magic.c:3667` (lexical_call_candidate).
- spell_ray_of_truth: `src/magic.c:3968` (lexical_call_candidate).
- spell_shocking_grasp: `src/magic.c:4196` (lexical_call_candidate).
- spell_acid_breath: `src/magic.c:4485` (lexical_call_candidate).
- spell_acid_breath: `src/magic.c:4490` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4528` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4533` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4541` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4546` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4584` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4589` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4597` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4602` (lexical_call_candidate).
- spell_gas_breath: `src/magic.c:4637` (lexical_call_candidate).
- spell_gas_breath: `src/magic.c:4642` (lexical_call_candidate).
- spell_lightning_breath: `src/magic.c:4665` (lexical_call_candidate).
- spell_lightning_breath: `src/magic.c:4670` (lexical_call_candidate).
- spell_general_purpose: `src/magic.c:4685` (lexical_call_candidate).
- spell_high_explosive: `src/magic.c:4697` (lexical_call_candidate).
- fwrite_pet: `src/save.c:375` (function_symbol_reference_candidate).
- char_update: `src/update.c:791` (lexical_call_candidate).
- char_update: `src/update.c:805` (lexical_call_candidate).
- char_update: `src/update.c:812` (lexical_call_candidate).
- char_update: `src/update.c:816` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:399` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:1314` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:1437` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2173` (declaration_or_dispatch_reference).

Dependencies: `bug`, `IS_IMMORTAL`, `get_eq_char`, `send_to_char`, `extract_obj`, `is_safe`, `check_killer`, `set_fighting`, `stop_follower`, `IS_AFFECTED`, `affect_strip`, `REMOVE_BIT`, `act`, `IS_NPC`, `IS_EVIL`, `IS_GOOD`, `check_parry`, `check_dodge`, `check_shield_block`, `check_immune`, `case`, `dam_message`, `update_pos`, `IS_AWAKE`, `stop_fighting`, `group_gain`, `sprintf`, `log_string`, `exp_per_level`, `gain_exp`, `wiznet`, `raw_kill`, `is_same_clan`, `IS_SET`, `get_obj_list`, `can_see_obj`, `do_function`, `number_range`, `number_bits`, `tail_chain`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.damage.if.001` | 681 | `if ( victim->position == POS_DEAD )` |  | pending |
| `fight.damage.return.001` | 682 | `return FALSE;` |  | pending |
| `fight.damage.if.002` | 687 | `if ( dam > 1200 && dt >= TYPE_HIT)` |  | pending |
| `fight.damage.and.001` | 687 | `&& dt >= TYPE_HIT)` |  | pending |
| `fight.damage.if.003` | 691 | `if (!IS_IMMORTAL(ch))` |  | pending |
| `fight.damage.if.004` | 696 | `if (obj != NULL)` |  | pending |
| `fight.damage.if.005` | 704 | `if ( dam > 35)` |  | pending |
| `fight.damage.if.006` | 706 | `if ( dam > 80)` |  | pending |
| `fight.damage.if.007` | 712 | `if ( victim != ch )` |  | pending |
| `fight.damage.if.008` | 718 | `if ( is_safe( ch, victim ) )` |  | pending |
| `fight.damage.return.002` | 719 | `return FALSE;` |  | pending |
| `fight.damage.if.009` | 722 | `if ( victim->position > POS_STUNNED )` |  | pending |
| `fight.damage.if.010` | 724 | `if ( victim->fighting == NULL )` |  | pending |
| `fight.damage.if.011` | 726 | `if (victim->timer <= 4)` |  | pending |
| `fight.damage.if.012` | 730 | `if ( victim->position > POS_STUNNED )` |  | pending |
| `fight.damage.if.013` | 732 | `if ( ch->fighting == NULL )` |  | pending |
| `fight.damage.if.014` | 739 | `if ( victim->master == ch )` |  | pending |
| `fight.damage.if.015` | 746 | `if ( IS_AFFECTED(ch, AFF_INVISIBLE) )` |  | pending |
| `fight.damage.if.016` | 758 | `if ( dam > 1 && !IS_NPC(victim)      &&   victim->pcdata->condition[COND_DRUNK]  > 10 )` |  | pending |
| `fight.damage.and.002` | 758 | `&& !IS_NPC(victim)` |  | pending |
| `fight.damage.and.003` | 759 | `&&   victim->pcdata->condition[COND_DRUNK]  > 10 )` |  | pending |
| `fight.damage.if.017` | 762 | `if ( dam > 1 && IS_AFFECTED(victim, AFF_SANCTUARY) )` |  | pending |
| `fight.damage.and.004` | 762 | `&& IS_AFFECTED(victim, AFF_SANCTUARY) )` |  | pending |
| `fight.damage.if.018` | 765 | `if ( dam > 1 && ((IS_AFFECTED(victim, AFF_PROTECT_EVIL) && IS_EVIL(ch) )     \|\|		     (IS_AFFECTED(victim, AFF_PROTECT_GOOD) && IS_GOOD(ch) )))` |  | pending |
| `fight.damage.and.005` | 765 | `&& ((IS_AFFECTED(victim, AFF_PROTECT_EVIL) && IS_EVIL(ch) )` |  | pending |
| `fight.damage.and.006` | 765 | `&& IS_EVIL(ch) )` |  | pending |
| `fight.damage.or.001` | 766 | `\|\|		     (IS_AFFECTED(victim, AFF_PROTECT_GOOD) && IS_GOOD(ch) )))` |  | pending |
| `fight.damage.and.007` | 766 | `&& IS_GOOD(ch) )))` |  | pending |
| `fight.damage.if.019` | 775 | `if ( dt >= TYPE_HIT && ch != victim)` |  | pending |
| `fight.damage.and.008` | 775 | `&& ch != victim)` |  | pending |
| `fight.damage.if.020` | 777 | `if ( check_parry( ch, victim ) )` |  | pending |
| `fight.damage.return.003` | 778 | `return FALSE;` |  | pending |
| `fight.damage.if.021` | 779 | `if ( check_dodge( ch, victim ) )` |  | pending |
| `fight.damage.return.004` | 780 | `return FALSE;` |  | pending |
| `fight.damage.if.022` | 781 | `if ( check_shield_block(ch,victim))` |  | pending |
| `fight.damage.return.005` | 782 | `return FALSE;` |  | pending |
| `fight.damage.switch.001` | 786 | `switch(check_immune(victim,dam_type))` |  | pending |
| `fight.damage.case.001` | 788 | `case(IS_IMMUNE):` |  | pending |
| `fight.damage.break.001` | 791 | `break;` |  | pending |
| `fight.damage.case.002` | 792 | `case(IS_RESISTANT):` |  | pending |
| `fight.damage.break.002` | 794 | `break;` |  | pending |
| `fight.damage.case.003` | 795 | `case(IS_VULNERABLE):` |  | pending |
| `fight.damage.break.003` | 797 | `break;` |  | pending |
| `fight.damage.if.023` | 800 | `if (show)` |  | pending |
| `fight.damage.if.024` | 803 | `if (dam == 0)` |  | pending |
| `fight.damage.return.006` | 804 | `return FALSE;` |  | pending |
| `fight.damage.if.025` | 811 | `if ( !IS_NPC(victim)     &&   victim->level >= LEVEL_IMMORTAL     &&   victim->hit < 1 )` |  | pending |
| `fight.damage.and.009` | 812 | `&&   victim->level >= LEVEL_IMMORTAL` |  | pending |
| `fight.damage.and.010` | 813 | `&&   victim->hit < 1 )` |  | pending |
| `fight.damage.switch.002` | 817 | `switch( victim->position )` |  | pending |
| `fight.damage.case.004` | 819 | `case POS_MORTAL:` |  | pending |
| `fight.damage.break.004` | 825 | `break;` |  | pending |
| `fight.damage.case.005` | 827 | `case POS_INCAP:` |  | pending |
| `fight.damage.break.005` | 833 | `break;` |  | pending |
| `fight.damage.case.006` | 835 | `case POS_STUNNED:` |  | pending |
| `fight.damage.break.006` | 840 | `break;` |  | pending |
| `fight.damage.case.007` | 842 | `case POS_DEAD:` |  | pending |
| `fight.damage.break.007` | 845 | `break;` |  | pending |
| `fight.damage.default.001` | 847 | `default:` |  | pending |
| `fight.damage.if.026` | 848 | `if ( dam > victim->max_hit / 4 )` |  | pending |
| `fight.damage.if.027` | 850 | `if ( victim->hit < victim->max_hit / 4 )` |  | pending |
| `fight.damage.break.008` | 852 | `break;` |  | pending |
| `fight.damage.if.028` | 858 | `if ( !IS_AWAKE(victim) )` |  | pending |
| `fight.damage.if.029` | 864 | `if ( victim->position == POS_DEAD )` |  | pending |
| `fight.damage.if.030` | 868 | `if ( !IS_NPC(victim) )` |  | pending |
| `fight.damage.ternary.001` | 872 | `? ch->short_descr : ch->name),` |  | pending |
| `fight.damage.if.031` | 880 | `if ( victim->exp > exp_per_level(victim,victim->pcdata->points)  			       * victim->level )` |  | pending |
| `fight.damage.ternary.002` | 887 | `? victim->short_descr : victim->name),` |  | pending |
| `fight.damage.ternary.003` | 888 | `? ch->short_descr : ch->name),` |  | pending |
| `fight.damage.if.032` | 891 | `if (IS_NPC(victim))` |  | pending |
| `fight.damage.if.033` | 898 | `if (ch != victim && !IS_NPC(ch) && !is_same_clan(ch,victim))` |  | pending |
| `fight.damage.and.011` | 898 | `&& !IS_NPC(ch) && !is_same_clan(ch,victim))` |  | pending |
| `fight.damage.and.012` | 898 | `&& !is_same_clan(ch,victim))` |  | pending |
| `fight.damage.if.034` | 900 | `if (IS_SET(victim->act,PLR_KILLER))` |  | pending |
| `fight.damage.if.035` | 908 | `if (!IS_NPC(ch) 	&&  (corpse = get_obj_list(ch,"corpse",ch->in_room->contents)) != NULL 	&&  corpse->item_type == ITEM_CORPSE_NPC && can_see_obj(ch,corpse))` |  | pending |
| `fight.damage.and.013` | 909 | `&&  (corpse = get_obj_list(ch,"corpse",ch->in_room->contents)) != NULL` |  | pending |
| `fight.damage.and.014` | 910 | `&&  corpse->item_type == ITEM_CORPSE_NPC && can_see_obj(ch,corpse))` |  | pending |
| `fight.damage.and.015` | 910 | `&& can_see_obj(ch,corpse))` |  | pending |
| `fight.damage.if.036` | 916 | `if ( IS_SET(ch->act, PLR_AUTOLOOT) && 		 corpse && corpse->contains)` |  | pending |
| `fight.damage.and.016` | 916 | `&&` |  | pending |
| `fight.damage.and.017` | 917 | `&& corpse->contains) /* exists and not empty */` |  | pending |
| `fight.damage.if.037` | 922 | `if (IS_SET(ch->act,PLR_AUTOGOLD) && 	        corpse && corpse->contains  && /* exists and not empty */ 		!IS_SET(ch->act,PLR_AUTOLOOT))` |  | pending |
| `fight.damage.and.018` | 922 | `&&` |  | pending |
| `fight.damage.and.019` | 923 | `&& corpse->contains  && /* exists and not empty */` |  | pending |
| `fight.damage.and.020` | 923 | `&& /* exists and not empty */` |  | pending |
| `fight.damage.if.038` | 926 | `if ((coins = get_obj_list(ch,"gcash",corpse->contains)) 		     != NULL)` |  | pending |
| `fight.damage.if.039` | 933 | `if (IS_SET(ch->act, PLR_AUTOSAC))` |  | pending |
| `fight.damage.if.040` | 935 | `if (IS_SET(ch->act,PLR_AUTOLOOT) && corpse && corpse->contains)` |  | pending |
| `fight.damage.and.021` | 935 | `&& corpse && corpse->contains)` |  | pending |
| `fight.damage.and.022` | 935 | `&& corpse->contains)` |  | pending |
| `fight.damage.return.007` | 937 | `return TRUE;` |  | pending |
| `fight.damage.return.008` | 946 | `return TRUE;` |  | pending |
| `fight.damage.if.041` | 949 | `if ( victim == ch )` |  | pending |
| `fight.damage.return.009` | 950 | `return TRUE;` |  | pending |
| `fight.damage.if.042` | 955 | `if ( !IS_NPC(victim) && victim->desc == NULL )` |  | pending |
| `fight.damage.and.023` | 955 | `&& victim->desc == NULL )` |  | pending |
| `fight.damage.if.043` | 957 | `if ( number_range( 0, victim->wait ) == 0 )` |  | pending |
| `fight.damage.return.010` | 960 | `return TRUE;` |  | pending |
| `fight.damage.if.044` | 967 | `if ( IS_NPC(victim) && dam > 0 && victim->wait < PULSE_VIOLENCE / 2)` |  | pending |
| `fight.damage.and.024` | 967 | `&& dam > 0 && victim->wait < PULSE_VIOLENCE / 2)` |  | pending |
| `fight.damage.and.025` | 967 | `&& victim->wait < PULSE_VIOLENCE / 2)` |  | pending |
| `fight.damage.if.045` | 969 | `if ( ( IS_SET(victim->act, ACT_WIMPY) && number_bits( 2 ) == 0 	&&   victim->hit < victim->max_hit / 5)  	\|\|   ( IS_AFFECTED(victim, AFF_CHARM) && victim->master != NULL 	&&     victim->master->in_room != victim->in_room ) )` |  | pending |
| `fight.damage.and.026` | 969 | `&& number_bits( 2 ) == 0` |  | pending |
| `fight.damage.and.027` | 970 | `&&   victim->hit < victim->max_hit / 5)` |  | pending |
| `fight.damage.or.002` | 971 | `\|\|   ( IS_AFFECTED(victim, AFF_CHARM) && victim->master != NULL` |  | pending |
| `fight.damage.and.028` | 971 | `&& victim->master != NULL` |  | pending |
| `fight.damage.and.029` | 972 | `&&     victim->master->in_room != victim->in_room ) )` |  | pending |
| `fight.damage.if.046` | 978 | `if ( !IS_NPC(victim)     &&   victim->hit > 0     &&   victim->hit <= victim->wimpy     &&   victim->wait < PULSE_VIOLENCE / 2 )` |  | pending |
| `fight.damage.and.030` | 979 | `&&   victim->hit > 0` |  | pending |
| `fight.damage.and.031` | 980 | `&&   victim->hit <= victim->wimpy` |  | pending |
| `fight.damage.and.032` | 981 | `&&   victim->wait < PULSE_VIOLENCE / 2 )` |  | pending |
| `fight.damage.return.011` | 987 | `return TRUE;` |  | pending |

## is_safe

[Source line 990](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:990); ends at line 1093. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_consider: `src/act_info.c:2342` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2164` (lexical_call_candidate).
- check_assist: `src/fight.c:125` (lexical_call_candidate).
- damage: `src/fight.c:718` (lexical_call_candidate).
- do_bash: `src/fight.c:2253` (lexical_call_candidate).
- do_dirt: `src/fight.c:2384` (lexical_call_candidate).
- do_trip: `src/fight.c:2506` (lexical_call_candidate).
- do_kill: `src/fight.c:2624` (lexical_call_candidate).
- do_murder: `src/fight.c:2691` (lexical_call_candidate).
- do_backstab: `src/fight.c:2759` (lexical_call_candidate).
- do_cast: `src/magic.c:391` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:615` (lexical_call_candidate).
- spell_charm_person: `src/magic.c:1318` (lexical_call_candidate).
- spec_troll_member: `src/special.c:146` (lexical_call_candidate).
- spec_ogre_member: `src/special.c:205` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:53` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2169` (declaration_or_dispatch_reference).

Dependencies: `IS_IMMORTAL`, `IS_NPC`, `IS_SET`, `send_to_char`, `act`, `IS_AFFECTED`, `is_clan`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.is_safe.if.001` | 992 | `if (victim->in_room == NULL \|\| ch->in_room == NULL)` |  | pending |
| `fight.is_safe.or.001` | 992 | `\|\| ch->in_room == NULL)` |  | pending |
| `fight.is_safe.return.001` | 993 | `return TRUE;` |  | pending |
| `fight.is_safe.if.002` | 995 | `if (victim->fighting == ch \|\| victim == ch)` |  | pending |
| `fight.is_safe.or.002` | 995 | `\|\| victim == ch)` |  | pending |
| `fight.is_safe.return.002` | 996 | `return FALSE;` |  | pending |
| `fight.is_safe.if.003` | 998 | `if (IS_IMMORTAL(ch) && ch->level > LEVEL_IMMORTAL)` |  | pending |
| `fight.is_safe.and.001` | 998 | `&& ch->level > LEVEL_IMMORTAL)` |  | pending |
| `fight.is_safe.return.003` | 999 | `return FALSE;` |  | pending |
| `fight.is_safe.if.004` | 1002 | `if (IS_NPC(victim))` |  | pending |
| `fight.is_safe.if.005` | 1006 | `if (IS_SET(victim->in_room->room_flags,ROOM_SAFE))` |  | pending |
| `fight.is_safe.return.004` | 1009 | `return TRUE;` |  | pending |
| `fight.is_safe.if.006` | 1012 | `if (victim->pIndexData->pShop != NULL)` |  | pending |
| `fight.is_safe.return.005` | 1015 | `return TRUE;` |  | pending |
| `fight.is_safe.if.007` | 1019 | `if (IS_SET(victim->act,ACT_TRAIN) 	\|\|  IS_SET(victim->act,ACT_PRACTICE) 	\|\|  IS_SET(victim->act,ACT_IS_HEALER) 	\|\|  IS_SET(victim->act,ACT_IS_CHANGER))` |  | pending |
| `fight.is_safe.or.003` | 1020 | `\|\|  IS_SET(victim->act,ACT_PRACTICE)` |  | pending |
| `fight.is_safe.or.004` | 1021 | `\|\|  IS_SET(victim->act,ACT_IS_HEALER)` |  | pending |
| `fight.is_safe.or.005` | 1022 | `\|\|  IS_SET(victim->act,ACT_IS_CHANGER))` |  | pending |
| `fight.is_safe.return.006` | 1025 | `return TRUE;` |  | pending |
| `fight.is_safe.if.008` | 1028 | `if (!IS_NPC(ch))` |  | pending |
| `fight.is_safe.if.009` | 1031 | `if (IS_SET(victim->act,ACT_PET))` |  | pending |
| `fight.is_safe.return.007` | 1035 | `return TRUE;` |  | pending |
| `fight.is_safe.if.010` | 1039 | `if (IS_AFFECTED(victim,AFF_CHARM) && ch != victim->master)` |  | pending |
| `fight.is_safe.and.002` | 1039 | `&& ch != victim->master)` |  | pending |
| `fight.is_safe.return.008` | 1042 | `return TRUE;` |  | pending |
| `fight.is_safe.if.011` | 1050 | `if (IS_NPC(ch))` |  | pending |
| `fight.is_safe.if.012` | 1053 | `if (IS_SET(victim->in_room->room_flags,ROOM_SAFE))` |  | pending |
| `fight.is_safe.return.009` | 1056 | `return TRUE;` |  | pending |
| `fight.is_safe.if.013` | 1060 | `if (IS_AFFECTED(ch,AFF_CHARM) && ch->master != NULL 	    &&  ch->master->fighting != victim)` |  | pending |
| `fight.is_safe.and.003` | 1060 | `&& ch->master != NULL` |  | pending |
| `fight.is_safe.and.004` | 1061 | `&&  ch->master->fighting != victim)` |  | pending |
| `fight.is_safe.return.010` | 1064 | `return TRUE;` |  | pending |
| `fight.is_safe.if.014` | 1070 | `if (!is_clan(ch))` |  | pending |
| `fight.is_safe.return.011` | 1073 | `return TRUE;` |  | pending |
| `fight.is_safe.if.015` | 1076 | `if (IS_SET(victim->act,PLR_KILLER) \|\| IS_SET(victim->act,PLR_THIEF))` |  | pending |
| `fight.is_safe.or.006` | 1076 | `\|\| IS_SET(victim->act,PLR_THIEF))` |  | pending |
| `fight.is_safe.return.012` | 1077 | `return FALSE;` |  | pending |
| `fight.is_safe.if.016` | 1079 | `if (!is_clan(victim))` |  | pending |
| `fight.is_safe.return.013` | 1082 | `return TRUE;` |  | pending |
| `fight.is_safe.if.017` | 1085 | `if (ch->level > victim->level + 8)` |  | pending |
| `fight.is_safe.return.014` | 1088 | `return TRUE;` |  | pending |
| `fight.is_safe.return.015` | 1092 | `return FALSE;` |  | pending |

## is_safe_spell

[Source line 1095](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1095); ends at line 1188. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_cast: `src/magic.c:474` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:654` (lexical_call_candidate).
- spell_chain_lightning: `src/magic.c:1236` (lexical_call_candidate).
- spell_earthquake: `src/magic.c:2203` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3203` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3214` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4518` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4574` (lexical_call_candidate).
- spell_gas_breath: `src/magic.c:4629` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2170` (declaration_or_dispatch_reference).

Dependencies: `IS_IMMORTAL`, `IS_NPC`, `IS_SET`, `IS_AFFECTED`, `is_same_group`, `is_clan`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.is_safe_spell.if.001` | 1097 | `if (victim->in_room == NULL \|\| ch->in_room == NULL)` |  | pending |
| `fight.is_safe_spell.or.001` | 1097 | `\|\| ch->in_room == NULL)` |  | pending |
| `fight.is_safe_spell.return.001` | 1098 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.002` | 1100 | `if (victim == ch && area)` |  | pending |
| `fight.is_safe_spell.and.001` | 1100 | `&& area)` |  | pending |
| `fight.is_safe_spell.return.002` | 1101 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.003` | 1103 | `if (victim->fighting == ch \|\| victim == ch)` |  | pending |
| `fight.is_safe_spell.or.002` | 1103 | `\|\| victim == ch)` |  | pending |
| `fight.is_safe_spell.return.003` | 1104 | `return FALSE;` |  | pending |
| `fight.is_safe_spell.if.004` | 1106 | `if (IS_IMMORTAL(ch) && ch->level > LEVEL_IMMORTAL && !area)` |  | pending |
| `fight.is_safe_spell.and.002` | 1106 | `&& ch->level > LEVEL_IMMORTAL && !area)` |  | pending |
| `fight.is_safe_spell.and.003` | 1106 | `&& !area)` |  | pending |
| `fight.is_safe_spell.return.004` | 1107 | `return FALSE;` |  | pending |
| `fight.is_safe_spell.if.005` | 1110 | `if (IS_NPC(victim))` |  | pending |
| `fight.is_safe_spell.if.006` | 1113 | `if (IS_SET(victim->in_room->room_flags,ROOM_SAFE))` |  | pending |
| `fight.is_safe_spell.return.005` | 1114 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.007` | 1116 | `if (victim->pIndexData->pShop != NULL)` |  | pending |
| `fight.is_safe_spell.return.006` | 1117 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.008` | 1120 | `if (IS_SET(victim->act,ACT_TRAIN) 	\|\|  IS_SET(victim->act,ACT_PRACTICE) 	\|\|  IS_SET(victim->act,ACT_IS_HEALER) 	\|\|  IS_SET(victim->act,ACT_IS_CHANGER))` |  | pending |
| `fight.is_safe_spell.or.003` | 1121 | `\|\|  IS_SET(victim->act,ACT_PRACTICE)` |  | pending |
| `fight.is_safe_spell.or.004` | 1122 | `\|\|  IS_SET(victim->act,ACT_IS_HEALER)` |  | pending |
| `fight.is_safe_spell.or.005` | 1123 | `\|\|  IS_SET(victim->act,ACT_IS_CHANGER))` |  | pending |
| `fight.is_safe_spell.return.007` | 1124 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.009` | 1126 | `if (!IS_NPC(ch))` |  | pending |
| `fight.is_safe_spell.if.010` | 1129 | `if (IS_SET(victim->act,ACT_PET))` |  | pending |
| `fight.is_safe_spell.return.008` | 1130 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.011` | 1133 | `if (IS_AFFECTED(victim,AFF_CHARM) && (area \|\| ch != victim->master))` |  | pending |
| `fight.is_safe_spell.and.004` | 1133 | `&& (area \|\| ch != victim->master))` |  | pending |
| `fight.is_safe_spell.or.006` | 1133 | `\|\| ch != victim->master))` |  | pending |
| `fight.is_safe_spell.return.009` | 1134 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.012` | 1137 | `if (victim->fighting != NULL && !is_same_group(ch,victim->fighting))` |  | pending |
| `fight.is_safe_spell.and.005` | 1137 | `&& !is_same_group(ch,victim->fighting))` |  | pending |
| `fight.is_safe_spell.return.010` | 1138 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.013` | 1143 | `if (area && !is_same_group(victim,ch->fighting))` |  | pending |
| `fight.is_safe_spell.and.006` | 1143 | `&& !is_same_group(victim,ch->fighting))` |  | pending |
| `fight.is_safe_spell.return.011` | 1144 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.014` | 1150 | `if (area && IS_IMMORTAL(victim) && victim->level > LEVEL_IMMORTAL)` |  | pending |
| `fight.is_safe_spell.and.007` | 1150 | `&& IS_IMMORTAL(victim) && victim->level > LEVEL_IMMORTAL)` |  | pending |
| `fight.is_safe_spell.and.008` | 1150 | `&& victim->level > LEVEL_IMMORTAL)` |  | pending |
| `fight.is_safe_spell.return.012` | 1151 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.015` | 1154 | `if (IS_NPC(ch))` |  | pending |
| `fight.is_safe_spell.if.016` | 1157 | `if (IS_AFFECTED(ch,AFF_CHARM) && ch->master != NULL 	    &&  ch->master->fighting != victim)` |  | pending |
| `fight.is_safe_spell.and.009` | 1157 | `&& ch->master != NULL` |  | pending |
| `fight.is_safe_spell.and.010` | 1158 | `&&  ch->master->fighting != victim)` |  | pending |
| `fight.is_safe_spell.return.013` | 1159 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.017` | 1162 | `if (IS_SET(victim->in_room->room_flags,ROOM_SAFE))` |  | pending |
| `fight.is_safe_spell.return.014` | 1163 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.018` | 1166 | `if (ch->fighting != NULL && !is_same_group(ch->fighting,victim))` |  | pending |
| `fight.is_safe_spell.and.011` | 1166 | `&& !is_same_group(ch->fighting,victim))` |  | pending |
| `fight.is_safe_spell.return.015` | 1167 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.019` | 1173 | `if (!is_clan(ch))` |  | pending |
| `fight.is_safe_spell.return.016` | 1174 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.020` | 1176 | `if (IS_SET(victim->act,PLR_KILLER) \|\| IS_SET(victim->act,PLR_THIEF))` |  | pending |
| `fight.is_safe_spell.or.007` | 1176 | `\|\| IS_SET(victim->act,PLR_THIEF))` |  | pending |
| `fight.is_safe_spell.return.017` | 1177 | `return FALSE;` |  | pending |
| `fight.is_safe_spell.if.021` | 1179 | `if (!is_clan(victim))` |  | pending |
| `fight.is_safe_spell.return.018` | 1180 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.if.022` | 1182 | `if (ch->level > victim->level + 8)` |  | pending |
| `fight.is_safe_spell.return.019` | 1183 | `return TRUE;` |  | pending |
| `fight.is_safe_spell.return.020` | 1187 | `return FALSE;` |  | pending |

## check_killer

[Source line 1192](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1192); ends at line 1256. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:720` (lexical_call_candidate).
- do_bash: `src/fight.c:2336` (lexical_call_candidate).
- do_dirt: `src/fight.c:2469` (lexical_call_candidate).
- do_trip: `src/fight.c:2583` (lexical_call_candidate).
- do_kill: `src/fight.c:2647` (lexical_call_candidate).
- do_murder: `src/fight.c:2720` (lexical_call_candidate).
- do_backstab: `src/fight.c:2783` (lexical_call_candidate).
- do_rescue: `src/fight.c:2928` (lexical_call_candidate).
- do_kick: `src/fight.c:2968` (lexical_call_candidate).
- do_disarm: `src/fight.c:3046` (lexical_call_candidate).
- do_cast: `src/magic.c:396` (lexical_call_candidate).
- do_cast: `src/magic.c:488` (lexical_call_candidate).
- do_cast: `src/magic.c:568` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:709` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:44` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2179` (declaration_or_dispatch_reference).

Dependencies: `IS_AFFECTED`, `IS_NPC`, `IS_SET`, `sprintf`, `bug`, `affect_strip`, `REMOVE_BIT`, `stop_follower`, `is_clan`, `send_to_char`, `SET_BIT`, `wiznet`, `save_char_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.check_killer.while.001` | 1199 | `while ( IS_AFFECTED(victim, AFF_CHARM) && victim->master != NULL )` |  | pending |
| `fight.check_killer.and.001` | 1199 | `&& victim->master != NULL )` |  | pending |
| `fight.check_killer.if.001` | 1206 | `if ( IS_NPC(victim)     \|\|   IS_SET(victim->act, PLR_KILLER)     \|\|   IS_SET(victim->act, PLR_THIEF))` |  | pending |
| `fight.check_killer.or.001` | 1207 | `\|\|   IS_SET(victim->act, PLR_KILLER)` |  | pending |
| `fight.check_killer.or.002` | 1208 | `\|\|   IS_SET(victim->act, PLR_THIEF))` |  | pending |
| `fight.check_killer.return.001` | 1209 | `return;` |  | pending |
| `fight.check_killer.if.002` | 1214 | `if ( IS_SET(ch->affected_by, AFF_CHARM) )` |  | pending |
| `fight.check_killer.if.003` | 1216 | `if ( ch->master == NULL )` |  | pending |
| `fight.check_killer.ternary.001` | 1221 | `? ch->short_descr : ch->name );` |  | pending |
| `fight.check_killer.return.002` | 1225 | `return;` |  | pending |
| `fight.check_killer.return.003` | 1233 | `return;` |  | pending |
| `fight.check_killer.if.004` | 1242 | `if ( IS_NPC(ch)     \|\|   ch == victim     \|\|   ch->level >= LEVEL_IMMORTAL     \|\|   !is_clan(ch)     \|\|   IS_SET(ch->act, PLR_KILLER)      \|\|	 ch->fighting  == victim)` |  | pending |
| `fight.check_killer.or.003` | 1243 | `\|\|   ch == victim` |  | pending |
| `fight.check_killer.or.004` | 1244 | `\|\|   ch->level >= LEVEL_IMMORTAL` |  | pending |
| `fight.check_killer.or.005` | 1245 | `\|\|   !is_clan(ch)` |  | pending |
| `fight.check_killer.or.006` | 1246 | `\|\|   IS_SET(ch->act, PLR_KILLER)` |  | pending |
| `fight.check_killer.or.007` | 1247 | `\|\|	 ch->fighting  == victim)` |  | pending |
| `fight.check_killer.return.004` | 1248 | `return;` |  | pending |
| `fight.check_killer.return.005` | 1255 | `return;` |  | pending |

## check_parry

[Source line 1263](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1263); ends at line 1290. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:777` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:45` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `get_skill`, `get_eq_char`, `IS_NPC`, `can_see`, `number_percent`, `act`, `check_improve`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.check_parry.if.001` | 1267 | `if ( !IS_AWAKE(victim) )` |  | pending |
| `fight.check_parry.return.001` | 1268 | `return FALSE;` |  | pending |
| `fight.check_parry.if.002` | 1272 | `if ( get_eq_char( victim, WEAR_WIELD ) == NULL )` |  | pending |
| `fight.check_parry.if.003` | 1274 | `if (IS_NPC(victim))` |  | pending |
| `fight.check_parry.return.002` | 1277 | `return FALSE;` |  | pending |
| `fight.check_parry.if.004` | 1280 | `if (!can_see(ch,victim))` |  | pending |
| `fight.check_parry.if.005` | 1283 | `if ( number_percent( ) >= chance + victim->level - ch->level )` |  | pending |
| `fight.check_parry.return.003` | 1284 | `return FALSE;` |  | pending |
| `fight.check_parry.return.004` | 1289 | `return TRUE;` |  | pending |

## check_shield_block

[Source line 1295](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1295); ends at line 1318. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:781` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:46` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `get_skill`, `get_eq_char`, `number_percent`, `act`, `check_improve`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.check_shield_block.if.001` | 1299 | `if ( !IS_AWAKE(victim) )` |  | pending |
| `fight.check_shield_block.return.001` | 1300 | `return FALSE;` |  | pending |
| `fight.check_shield_block.if.002` | 1306 | `if ( get_eq_char( victim, WEAR_SHIELD ) == NULL )` |  | pending |
| `fight.check_shield_block.return.002` | 1307 | `return FALSE;` |  | pending |
| `fight.check_shield_block.if.003` | 1309 | `if ( number_percent( ) >= chance + victim->level - ch->level )` |  | pending |
| `fight.check_shield_block.return.003` | 1310 | `return FALSE;` |  | pending |
| `fight.check_shield_block.return.004` | 1317 | `return TRUE;` |  | pending |

## check_dodge

[Source line 1324](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1324); ends at line 1343. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:779` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:43` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `get_skill`, `can_see`, `number_percent`, `act`, `check_improve`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.check_dodge.if.001` | 1328 | `if ( !IS_AWAKE(victim) )` |  | pending |
| `fight.check_dodge.return.001` | 1329 | `return FALSE;` |  | pending |
| `fight.check_dodge.if.002` | 1333 | `if (!can_see(victim,ch))` |  | pending |
| `fight.check_dodge.if.003` | 1336 | `if ( number_percent( ) >= chance + victim->level - ch->level )` |  | pending |
| `fight.check_dodge.return.002` | 1337 | `return FALSE;` |  | pending |
| `fight.check_dodge.return.003` | 1342 | `return TRUE;` |  | pending |

## update_pos

[Source line 1350](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1350); ends at line 1376. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_restore: `src/act_wiz.c:2779` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2811` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2833` (lexical_call_candidate).
- damage: `src/fight.c:815` (lexical_call_candidate).
- stop_fighting: `src/fight.c:1415` (lexical_call_candidate).
- spell_cure_critical: `src/magic.c:1590` (lexical_call_candidate).
- spell_cure_light: `src/magic.c:1629` (lexical_call_candidate).
- spell_cure_serious: `src/magic.c:1667` (lexical_call_candidate).
- spell_heal: `src/magic.c:3029` (lexical_call_candidate).
- char_update: `src/update.c:660` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2177` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.update_pos.if.001` | 1352 | `if ( victim->hit > 0 )` |  | pending |
| `fight.update_pos.if.002` | 1354 | `if ( victim->position <= POS_STUNNED )` |  | pending |
| `fight.update_pos.return.001` | 1356 | `return;` |  | pending |
| `fight.update_pos.if.003` | 1359 | `if ( IS_NPC(victim) && victim->hit < 1 )` |  | pending |
| `fight.update_pos.and.001` | 1359 | `&& victim->hit < 1 )` |  | pending |
| `fight.update_pos.return.002` | 1362 | `return;` |  | pending |
| `fight.update_pos.if.004` | 1365 | `if ( victim->hit <= -11 )` |  | pending |
| `fight.update_pos.return.003` | 1368 | `return;` |  | pending |
| `fight.update_pos.if.005` | 1371 | `if ( victim->hit <= -6 )` |  | pending |
| `fight.update_pos.if.006` | 1372 | `if ( victim->hit <= -3 )` |  | pending |
| `fight.update_pos.return.004` | 1375 | `return;` |  | pending |

## set_fighting

[Source line 1383](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1383); ends at line 1398. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:725` (lexical_call_candidate).
- damage: `src/fight.c:733` (lexical_call_candidate).
- do_rescue: `src/fight.c:2929` (lexical_call_candidate).
- do_rescue: `src/fight.c:2930` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:58` (declaration_or_dispatch_reference).

Dependencies: `bug`, `IS_AFFECTED`, `affect_strip`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.set_fighting.if.001` | 1385 | `if ( ch->fighting != NULL )` |  | pending |
| `fight.set_fighting.return.001` | 1388 | `return;` |  | pending |
| `fight.set_fighting.if.002` | 1391 | `if ( IS_AFFECTED(ch, AFF_SLEEP) )` |  | pending |
| `fight.set_fighting.return.002` | 1397 | `return;` |  | pending |

## stop_fighting

[Source line 1405](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1405); ends at line 1420. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_delete: `src/act_comm.c:70` (lexical_call_candidate).
- do_recall: `src/act_move.c:1452` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:534` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:850` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:948` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:1004` (lexical_call_candidate).
- do_peace: `src/act_wiz.c:3112` (lexical_call_candidate).
- violence_update: `src/fight.c:83` (lexical_call_candidate).
- damage: `src/fight.c:859` (lexical_call_candidate).
- raw_kill: `src/fight.c:1664` (lexical_call_candidate).
- do_flee: `src/fight.c:2853` (lexical_call_candidate).
- do_rescue: `src/fight.c:2925` (lexical_call_candidate).
- do_rescue: `src/fight.c:2926` (lexical_call_candidate).
- extract_char: `src/handler.c:1946` (lexical_call_candidate).
- spell_calm: `src/magic.c:994` (lexical_call_candidate).
- spell_word_of_recall: `src/magic.c:4454` (lexical_call_candidate).
- char_update: `src/update.c:690` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2178` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `update_pos`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.stop_fighting.for.001` | 1409 | `for ( fch = char_list; fch != NULL; fch = fch->next )` |  | pending |
| `fight.stop_fighting.if.001` | 1411 | `if ( fch == ch \|\| ( fBoth && fch->fighting == ch ) )` |  | pending |
| `fight.stop_fighting.or.001` | 1411 | `\|\| ( fBoth && fch->fighting == ch ) )` |  | pending |
| `fight.stop_fighting.and.001` | 1411 | `&& fch->fighting == ch ) )` |  | pending |
| `fight.stop_fighting.ternary.001` | 1414 | `? fch->default_pos : POS_STANDING;` |  | pending |
| `fight.stop_fighting.return.001` | 1419 | `return;` |  | pending |

## make_corpse

[Source line 1427](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1427); ends at line 1535. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- raw_kill: `src/fight.c:1666` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:54` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `create_object`, `get_obj_index`, `number_range`, `obj_to_obj`, `create_money`, `REMOVE_BIT`, `is_clan`, `str_dup`, `sprintf`, `free_string`, `obj_from_char`, `IS_SET`, `extract_obj`, `IS_OBJ_STAT`, `act`, `obj_from_obj`, `obj_to_room`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.make_corpse.if.001` | 1435 | `if ( IS_NPC(ch) )` |  | pending |
| `fight.make_corpse.if.002` | 1440 | `if ( ch->gold > 0 )` |  | pending |
| `fight.make_corpse.if.003` | 1454 | `if (!is_clan(ch))` |  | pending |
| `fight.make_corpse.if.004` | 1459 | `if (ch->gold > 1 \|\| ch->silver > 1)` |  | pending |
| `fight.make_corpse.or.001` | 1459 | `\|\| ch->silver > 1)` |  | pending |
| `fight.make_corpse.for.001` | 1480 | `for ( obj = ch->carrying; obj != NULL; obj = obj_next )` |  | pending |
| `fight.make_corpse.if.005` | 1485 | `if (obj->wear_loc == WEAR_FLOAT)` |  | pending |
| `fight.make_corpse.if.006` | 1488 | `if (obj->item_type == ITEM_POTION)` |  | pending |
| `fight.make_corpse.if.007` | 1490 | `if (obj->item_type == ITEM_SCROLL)` |  | pending |
| `fight.make_corpse.if.008` | 1492 | `if (IS_SET(obj->extra_flags,ITEM_ROT_DEATH) && !floating)` |  | pending |
| `fight.make_corpse.and.001` | 1492 | `&& !floating)` |  | pending |
| `fight.make_corpse.if.009` | 1499 | `if ( IS_SET( obj->extra_flags, ITEM_INVENTORY ) )` |  | pending |
| `fight.make_corpse.if.010` | 1501 | `if (floating)` |  | pending |
| `fight.make_corpse.if.011` | 1503 | `if (IS_OBJ_STAT(obj,ITEM_ROT_DEATH))` |  | pending |
| `fight.make_corpse.if.012` | 1505 | `if (obj->contains != NULL)` |  | pending |
| `fight.make_corpse.for.002` | 1511 | `for (in = obj->contains; in != NULL; in = in_next)` |  | pending |
| `fight.make_corpse.return.001` | 1534 | `return;` |  | pending |

## death_cry

[Source line 1542](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1542); ends at line 1656. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- raw_kill: `src/fight.c:1665` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:49` (declaration_or_dispatch_reference).

Dependencies: `number_bits`, `IS_SET`, `act`, `IS_NPC`, `create_object`, `get_obj_index`, `number_range`, `sprintf`, `free_string`, `str_dup`, `obj_to_room`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.death_cry.switch.001` | 1552 | `switch ( number_bits(4))` |  | pending |
| `fight.death_cry.case.001` | 1554 | `case  0: msg  = "$n hits the ground ... DEAD.";` |  | pending |
| `fight.death_cry.break.001` | 1554 | `break;` |  | pending |
| `fight.death_cry.case.002` | 1555 | `case  1:` |  | pending |
| `fight.death_cry.if.001` | 1556 | `if (ch->material == 0)` |  | pending |
| `fight.death_cry.break.002` | 1559 | `break;` |  | pending |
| `fight.death_cry.case.003` | 1561 | `case  2:` |  | pending |
| `fight.death_cry.if.002` | 1562 | `if (IS_SET(ch->parts,PART_GUTS))` |  | pending |
| `fight.death_cry.break.003` | 1567 | `break;` |  | pending |
| `fight.death_cry.case.004` | 1568 | `case  3:` |  | pending |
| `fight.death_cry.if.003` | 1569 | `if (IS_SET(ch->parts,PART_HEAD))` |  | pending |
| `fight.death_cry.break.004` | 1574 | `break;` |  | pending |
| `fight.death_cry.case.005` | 1575 | `case  4:` |  | pending |
| `fight.death_cry.if.004` | 1576 | `if (IS_SET(ch->parts,PART_HEART))` |  | pending |
| `fight.death_cry.break.005` | 1581 | `break;` |  | pending |
| `fight.death_cry.case.006` | 1582 | `case  5:` |  | pending |
| `fight.death_cry.if.005` | 1583 | `if (IS_SET(ch->parts,PART_ARMS))` |  | pending |
| `fight.death_cry.break.006` | 1588 | `break;` |  | pending |
| `fight.death_cry.case.007` | 1589 | `case  6:` |  | pending |
| `fight.death_cry.if.006` | 1590 | `if (IS_SET(ch->parts,PART_LEGS))` |  | pending |
| `fight.death_cry.break.007` | 1595 | `break;` |  | pending |
| `fight.death_cry.case.008` | 1596 | `case 7:` |  | pending |
| `fight.death_cry.if.007` | 1597 | `if (IS_SET(ch->parts,PART_BRAINS))` |  | pending |
| `fight.death_cry.if.008` | 1606 | `if ( vnum != 0 )` |  | pending |
| `fight.death_cry.ternary.001` | 1612 | `? ch->short_descr : ch->name;` |  | pending |
| `fight.death_cry.if.009` | 1624 | `if (obj->item_type == ITEM_FOOD)` |  | pending |
| `fight.death_cry.if.010` | 1626 | `if (IS_SET(ch->form,FORM_POISON))` |  | pending |
| `fight.death_cry.if.011` | 1628 | `if (!IS_SET(ch->form,FORM_EDIBLE))` |  | pending |
| `fight.death_cry.if.012` | 1635 | `if ( IS_NPC(ch) )` |  | pending |
| `fight.death_cry.for.001` | 1641 | `for ( door = 0; door <= 5; door++ )` |  | pending |
| `fight.death_cry.if.013` | 1645 | `if ( ( pexit = was_in_room->exit[door] ) != NULL 	&&   pexit->u1.to_room != NULL 	&&   pexit->u1.to_room != was_in_room )` |  | pending |
| `fight.death_cry.and.001` | 1646 | `&&   pexit->u1.to_room != NULL` |  | pending |
| `fight.death_cry.and.002` | 1647 | `&&   pexit->u1.to_room != was_in_room )` |  | pending |
| `fight.death_cry.return.001` | 1655 | `return;` |  | pending |

## raw_kill

[Source line 1660](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1660); ends at line 1688. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:896` (lexical_call_candidate).
- do_slay: `src/fight.c:3093` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:57` (declaration_or_dispatch_reference).

Dependencies: `stop_fighting`, `death_cry`, `make_corpse`, `IS_NPC`, `URANGE`, `extract_char`, `affect_remove`, `UMAX`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.raw_kill.if.001` | 1668 | `if ( IS_NPC(victim) )` |  | pending |
| `fight.raw_kill.return.001` | 1673 | `return;` |  | pending |
| `fight.raw_kill.while.001` | 1677 | `while ( victim->affected )` |  | pending |
| `fight.raw_kill.for.001` | 1680 | `for (i = 0; i < 4; i++)` |  | pending |
| `fight.raw_kill.return.002` | 1687 | `return;` |  | pending |

## group_gain

[Source line 1692](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1692); ends at line 1775. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:866` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:50` (declaration_or_dispatch_reference).

Dependencies: `is_same_group`, `IS_NPC`, `bug`, `xp_compute`, `sprintf`, `send_to_char`, `gain_exp`, `IS_OBJ_STAT`, `IS_EVIL`, `IS_GOOD`, `IS_NEUTRAL`, `act`, `obj_from_char`, `obj_to_room`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.group_gain.if.001` | 1706 | `if ( victim == ch )` |  | pending |
| `fight.group_gain.return.001` | 1707 | `return;` |  | pending |
| `fight.group_gain.for.001` | 1711 | `for ( gch = ch->in_room->people; gch != NULL; gch = gch->next_in_room )` |  | pending |
| `fight.group_gain.if.002` | 1713 | `if ( is_same_group( gch, ch ) )` |  | pending |
| `fight.group_gain.ternary.001` | 1716 | `? gch->level / 2 : gch->level;` |  | pending |
| `fight.group_gain.if.003` | 1720 | `if ( members == 0 )` |  | pending |
| `fight.group_gain.ternary.002` | 1727 | `? ch->leader : ch;` |  | pending |
| `fight.group_gain.for.002` | 1729 | `for ( gch = ch->in_room->people; gch != NULL; gch = gch->next_in_room )` |  | pending |
| `fight.group_gain.if.004` | 1734 | `if ( !is_same_group( gch, ch ) \|\| IS_NPC(gch))` |  | pending |
| `fight.group_gain.or.001` | 1734 | `\|\| IS_NPC(gch))` |  | pending |
| `fight.group_gain.continue.001` | 1735 | `continue;` |  | pending |
| `fight.group_gain.for.003` | 1756 | `for ( obj = ch->carrying; obj != NULL; obj = obj_next )` |  | pending |
| `fight.group_gain.if.005` | 1759 | `if ( obj->wear_loc == WEAR_NONE )` |  | pending |
| `fight.group_gain.continue.002` | 1760 | `continue;` |  | pending |
| `fight.group_gain.if.006` | 1762 | `if ( ( IS_OBJ_STAT(obj, ITEM_ANTI_EVIL)    && IS_EVIL(ch)    ) 	    \|\|   ( IS_OBJ_STAT(obj, ITEM_ANTI_GOOD)    && IS_GOOD(ch)    ) 	    \|\|   ( IS_OBJ_STAT(obj, ITEM_ANTI_NEUTRAL) && IS_NEUTRAL(ch) ) )` |  | pending |
| `fight.group_gain.and.001` | 1762 | `&& IS_EVIL(ch)    )` |  | pending |
| `fight.group_gain.or.002` | 1763 | `\|\|   ( IS_OBJ_STAT(obj, ITEM_ANTI_GOOD)    && IS_GOOD(ch)    )` |  | pending |
| `fight.group_gain.and.002` | 1763 | `&& IS_GOOD(ch)    )` |  | pending |
| `fight.group_gain.or.003` | 1764 | `\|\|   ( IS_OBJ_STAT(obj, ITEM_ANTI_NEUTRAL) && IS_NEUTRAL(ch) ) )` |  | pending |
| `fight.group_gain.and.003` | 1764 | `&& IS_NEUTRAL(ch) ) )` |  | pending |
| `fight.group_gain.return.002` | 1774 | `return;` |  | pending |

## xp_compute

[Source line 1784](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1784); ends at line 1964. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- group_gain: `src/fight.c:1751` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:51` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `UMAX`, `UMIN`, `URANGE`, `number_range`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.xp_compute.switch.001` | 1794 | `switch (level_range)` |  | pending |
| `fight.xp_compute.default.001` | 1796 | `default : 	base_exp =   0;` |  | pending |
| `fight.xp_compute.break.001` | 1796 | `break;` |  | pending |
| `fight.xp_compute.case.001` | 1797 | `case -9 :	base_exp =   1;` |  | pending |
| `fight.xp_compute.break.002` | 1797 | `break;` |  | pending |
| `fight.xp_compute.case.002` | 1798 | `case -8 :	base_exp =   2;` |  | pending |
| `fight.xp_compute.break.003` | 1798 | `break;` |  | pending |
| `fight.xp_compute.case.003` | 1799 | `case -7 :	base_exp =   5;` |  | pending |
| `fight.xp_compute.break.004` | 1799 | `break;` |  | pending |
| `fight.xp_compute.case.004` | 1800 | `case -6 : 	base_exp =   9;` |  | pending |
| `fight.xp_compute.break.005` | 1800 | `break;` |  | pending |
| `fight.xp_compute.case.005` | 1801 | `case -5 :	base_exp =  11;` |  | pending |
| `fight.xp_compute.break.006` | 1801 | `break;` |  | pending |
| `fight.xp_compute.case.006` | 1802 | `case -4 :	base_exp =  22;` |  | pending |
| `fight.xp_compute.break.007` | 1802 | `break;` |  | pending |
| `fight.xp_compute.case.007` | 1803 | `case -3 :	base_exp =  33;` |  | pending |
| `fight.xp_compute.break.008` | 1803 | `break;` |  | pending |
| `fight.xp_compute.case.008` | 1804 | `case -2 :	base_exp =  50;` |  | pending |
| `fight.xp_compute.break.009` | 1804 | `break;` |  | pending |
| `fight.xp_compute.case.009` | 1805 | `case -1 :	base_exp =  66;` |  | pending |
| `fight.xp_compute.break.010` | 1805 | `break;` |  | pending |
| `fight.xp_compute.case.010` | 1806 | `case  0 :	base_exp =  83;` |  | pending |
| `fight.xp_compute.break.011` | 1806 | `break;` |  | pending |
| `fight.xp_compute.case.011` | 1807 | `case  1 :	base_exp =  99;` |  | pending |
| `fight.xp_compute.break.012` | 1807 | `break;` |  | pending |
| `fight.xp_compute.case.012` | 1808 | `case  2 :	base_exp = 121;` |  | pending |
| `fight.xp_compute.break.013` | 1808 | `break;` |  | pending |
| `fight.xp_compute.case.013` | 1809 | `case  3 :	base_exp = 143;` |  | pending |
| `fight.xp_compute.break.014` | 1809 | `break;` |  | pending |
| `fight.xp_compute.case.014` | 1810 | `case  4 :	base_exp = 165;` |  | pending |
| `fight.xp_compute.break.015` | 1810 | `break;` |  | pending |
| `fight.xp_compute.if.001` | 1813 | `if (level_range > 4)` |  | pending |
| `fight.xp_compute.if.002` | 1820 | `if (IS_SET(victim->act,ACT_NOALIGN))` |  | pending |
| `fight.xp_compute.if.003` | 1825 | `if (align > 500)` |  | pending |
| `fight.xp_compute.if.004` | 1832 | `if (align < -500)` |  | pending |
| `fight.xp_compute.if.005` | 1846 | `if (IS_SET(victim->act,ACT_NOALIGN))` |  | pending |
| `fight.xp_compute.if.006` | 1849 | `if (gch->alignment > 500)` |  | pending |
| `fight.xp_compute.if.007` | 1851 | `if (victim->alignment < -750)` |  | pending |
| `fight.xp_compute.if.008` | 1854 | `if (victim->alignment < -500)` |  | pending |
| `fight.xp_compute.if.009` | 1857 | `if (victim->alignment > 750)` |  | pending |
| `fight.xp_compute.if.010` | 1860 | `if (victim->alignment > 500)` |  | pending |
| `fight.xp_compute.if.011` | 1863 | `if (victim->alignment > 250)` |  | pending |
| `fight.xp_compute.if.012` | 1870 | `if (gch->alignment < -500)` |  | pending |
| `fight.xp_compute.if.013` | 1872 | `if (victim->alignment > 750)` |  | pending |
| `fight.xp_compute.if.014` | 1875 | `if (victim->alignment > 500)` |  | pending |
| `fight.xp_compute.if.015` | 1878 | `if (victim->alignment < -750)` |  | pending |
| `fight.xp_compute.if.016` | 1881 | `if (victim->alignment < -500)` |  | pending |
| `fight.xp_compute.if.017` | 1884 | `if (victim->alignment < -250)` |  | pending |
| `fight.xp_compute.if.018` | 1891 | `if (gch->alignment > 200)` |  | pending |
| `fight.xp_compute.if.019` | 1894 | `if (victim->alignment < -500)` |  | pending |
| `fight.xp_compute.if.020` | 1897 | `if (victim->alignment > 750)` |  | pending |
| `fight.xp_compute.if.021` | 1900 | `if (victim->alignment > 0)` |  | pending |
| `fight.xp_compute.if.022` | 1907 | `if (gch->alignment < -200)` |  | pending |
| `fight.xp_compute.if.023` | 1909 | `if (victim->alignment > 500)` |  | pending |
| `fight.xp_compute.if.024` | 1912 | `if (victim->alignment < -750)` |  | pending |
| `fight.xp_compute.if.025` | 1915 | `if (victim->alignment < 0)` |  | pending |
| `fight.xp_compute.if.026` | 1925 | `if (victim->alignment > 500 \|\| victim->alignment < -500)` |  | pending |
| `fight.xp_compute.or.001` | 1925 | `\|\| victim->alignment < -500)` |  | pending |
| `fight.xp_compute.if.027` | 1928 | `if (victim->alignment < 200 && victim->alignment > -200)` |  | pending |
| `fight.xp_compute.and.001` | 1928 | `&& victim->alignment > -200)` |  | pending |
| `fight.xp_compute.if.028` | 1936 | `if (gch->level < 6)` |  | pending |
| `fight.xp_compute.if.029` | 1940 | `if (gch->level > 35 )` |  | pending |
| `fight.xp_compute.if.030` | 1952 | `if (gch->level < 15)` |  | pending |
| `fight.xp_compute.return.001` | 1963 | `return xp;` |  | pending |

## dam_message

[Source line 1967](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1967); ends at line 2079. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:801` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:47` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `bug`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.dam_message.if.001` | 1975 | `if (ch == NULL \|\| victim == NULL)` |  | pending |
| `fight.dam_message.or.001` | 1975 | `\|\| victim == NULL)` |  | pending |
| `fight.dam_message.return.001` | 1976 | `return;` |  | pending |
| `fight.dam_message.if.002` | 1978 | `if ( dam ==   0 )` |  | pending |
| `fight.dam_message.if.003` | 1979 | `if ( dam <=   4 )` |  | pending |
| `fight.dam_message.if.004` | 1980 | `if ( dam <=   8 )` |  | pending |
| `fight.dam_message.if.005` | 1981 | `if ( dam <=  12 )` |  | pending |
| `fight.dam_message.if.006` | 1982 | `if ( dam <=  16 )` |  | pending |
| `fight.dam_message.if.007` | 1983 | `if ( dam <=  20 )` |  | pending |
| `fight.dam_message.if.008` | 1984 | `if ( dam <=  24 )` |  | pending |
| `fight.dam_message.if.009` | 1985 | `if ( dam <=  28 )` |  | pending |
| `fight.dam_message.if.010` | 1986 | `if ( dam <=  32 )` |  | pending |
| `fight.dam_message.if.011` | 1987 | `if ( dam <=  36 )` |  | pending |
| `fight.dam_message.if.012` | 1988 | `if ( dam <=  40 )` |  | pending |
| `fight.dam_message.if.013` | 1989 | `if ( dam <=  44 )` |  | pending |
| `fight.dam_message.if.014` | 1990 | `if ( dam <=  48 )` |  | pending |
| `fight.dam_message.if.015` | 1991 | `if ( dam <=  52 )` |  | pending |
| `fight.dam_message.if.016` | 1992 | `if ( dam <=  56 )` |  | pending |
| `fight.dam_message.if.017` | 1993 | `if ( dam <=  60 )` |  | pending |
| `fight.dam_message.if.018` | 1995 | `if ( dam <=  75 )` |  | pending |
| `fight.dam_message.if.019` | 1997 | `if ( dam <= 100)` |  | pending |
| `fight.dam_message.if.020` | 1999 | `if ( dam <= 125)` |  | pending |
| `fight.dam_message.if.021` | 2001 | `if ( dam <= 150)` |  | pending |
| `fight.dam_message.ternary.001` | 2006 | `? '.' : '!';` |  | pending |
| `fight.dam_message.if.022` | 2008 | `if ( dt == TYPE_HIT )` |  | pending |
| `fight.dam_message.if.023` | 2010 | `if (ch  == victim)` |  | pending |
| `fight.dam_message.if.024` | 2024 | `if ( dt >= 0 && dt < MAX_SKILL )` |  | pending |
| `fight.dam_message.and.001` | 2024 | `&& dt < MAX_SKILL )` |  | pending |
| `fight.dam_message.if.025` | 2026 | `if ( dt >= TYPE_HIT 	&& dt < TYPE_HIT + MAX_DAMAGE_MESSAGE)` |  | pending |
| `fight.dam_message.and.002` | 2027 | `&& dt < TYPE_HIT + MAX_DAMAGE_MESSAGE)` |  | pending |
| `fight.dam_message.if.026` | 2036 | `if (immune)` |  | pending |
| `fight.dam_message.if.027` | 2038 | `if (ch == victim)` |  | pending |
| `fight.dam_message.if.028` | 2052 | `if (ch == victim)` |  | pending |
| `fight.dam_message.if.029` | 2066 | `if (ch == victim)` |  | pending |
| `fight.dam_message.return.002` | 2078 | `return;` |  | pending |

## disarm

[Source line 2087](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2087); ends at line 2119. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_disarm: `src/fight.c:3035` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/fight.c:59` (declaration_or_dispatch_reference).

Dependencies: `get_eq_char`, `IS_OBJ_STAT`, `act`, `obj_from_char`, `obj_to_char`, `obj_to_room`, `IS_NPC`, `can_see_obj`, `get_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.disarm.if.001` | 2091 | `if ( ( obj = get_eq_char( victim, WEAR_WIELD ) ) == NULL )` |  | pending |
| `fight.disarm.return.001` | 2092 | `return;` |  | pending |
| `fight.disarm.if.002` | 2094 | `if ( IS_OBJ_STAT(obj,ITEM_NOREMOVE))` |  | pending |
| `fight.disarm.return.002` | 2100 | `return;` |  | pending |
| `fight.disarm.if.003` | 2109 | `if ( IS_OBJ_STAT(obj,ITEM_NODROP) \|\| IS_OBJ_STAT(obj,ITEM_INVENTORY) )` |  | pending |
| `fight.disarm.or.001` | 2109 | `\|\| IS_OBJ_STAT(obj,ITEM_INVENTORY) )` |  | pending |
| `fight.disarm.if.004` | 2114 | `if (IS_NPC(victim) && victim->wait == 0 && can_see_obj(victim,obj))` |  | pending |
| `fight.disarm.and.001` | 2114 | `&& victim->wait == 0 && can_see_obj(victim,obj))` |  | pending |
| `fight.disarm.and.002` | 2114 | `&& can_see_obj(victim,obj))` |  | pending |
| `fight.disarm.return.003` | 2118 | `return;` |  | pending |

## do_berserk

[Source line 2121](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2121); ends at line 2206. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- mob_hit: `src/fight.c:333` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:241` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:91` (declaration_or_dispatch_reference).

Dependencies: `get_skill`, `IS_NPC`, `IS_SET`, `send_to_char`, `IS_AFFECTED`, `is_affected`, `skill_lookup`, `number_percent`, `WAIT_STATE`, `UMIN`, `act`, `check_improve`, `number_fuzzy`, `UMAX`, `affect_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_berserk.if.001` | 2125 | `if ((chance = get_skill(ch,gsn_berserk)) == 0     \|\|  (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_BERSERK))     \|\|  (!IS_NPC(ch)     &&   ch->level < skill_table[gsn_berserk].skill_level[ch->class]))` |  | pending |
| `fight.do_berserk.or.001` | 2126 | `\|\|  (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_BERSERK))` |  | pending |
| `fight.do_berserk.and.001` | 2126 | `&& !IS_SET(ch->off_flags,OFF_BERSERK))` |  | pending |
| `fight.do_berserk.or.002` | 2127 | `\|\|  (!IS_NPC(ch)` |  | pending |
| `fight.do_berserk.and.002` | 2128 | `&&   ch->level < skill_table[gsn_berserk].skill_level[ch->class]))` |  | pending |
| `fight.do_berserk.return.001` | 2131 | `return;` |  | pending |
| `fight.do_berserk.if.002` | 2134 | `if (IS_AFFECTED(ch,AFF_BERSERK) \|\| is_affected(ch,gsn_berserk)     \|\|  is_affected(ch,skill_lookup("frenzy")))` |  | pending |
| `fight.do_berserk.or.003` | 2134 | `\|\| is_affected(ch,gsn_berserk)` |  | pending |
| `fight.do_berserk.or.004` | 2135 | `\|\|  is_affected(ch,skill_lookup("frenzy")))` |  | pending |
| `fight.do_berserk.return.002` | 2138 | `return;` |  | pending |
| `fight.do_berserk.if.003` | 2141 | `if (IS_AFFECTED(ch,AFF_CALM))` |  | pending |
| `fight.do_berserk.return.003` | 2144 | `return;` |  | pending |
| `fight.do_berserk.if.004` | 2147 | `if (ch->mana < 50)` |  | pending |
| `fight.do_berserk.return.004` | 2150 | `return;` |  | pending |
| `fight.do_berserk.if.005` | 2156 | `if (ch->position == POS_FIGHTING)` |  | pending |
| `fight.do_berserk.if.006` | 2163 | `if (number_percent() < chance)` |  | pending |

## do_bash

[Source line 2208](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2208); ends at line 2337. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- mob_hit: `src/fight.c:328` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:239` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:90` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `get_skill`, `IS_NPC`, `IS_SET`, `send_to_char`, `get_char_room`, `act`, `is_safe`, `is_same_group`, `IS_AFFECTED`, `get_curr_stat`, `GET_AC`, `number_percent`, `check_improve`, `DAZE_STATE`, `WAIT_STATE`, `damage`, `number_range`, `check_killer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_bash.if.001` | 2216 | `if ( (chance = get_skill(ch,gsn_bash)) == 0     \|\|	 (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_BASH))     \|\|	 (!IS_NPC(ch)     &&	  ch->level < skill_table[gsn_bash].skill_level[ch->class]))` |  | pending |
| `fight.do_bash.or.001` | 2217 | `\|\|	 (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_BASH))` |  | pending |
| `fight.do_bash.and.001` | 2217 | `&& !IS_SET(ch->off_flags,OFF_BASH))` |  | pending |
| `fight.do_bash.or.002` | 2218 | `\|\|	 (!IS_NPC(ch)` |  | pending |
| `fight.do_bash.and.002` | 2219 | `&&	  ch->level < skill_table[gsn_bash].skill_level[ch->class]))` |  | pending |
| `fight.do_bash.return.001` | 2222 | `return;` |  | pending |
| `fight.do_bash.if.002` | 2225 | `if (arg[0] == '\0')` |  | pending |
| `fight.do_bash.if.003` | 2228 | `if (victim == NULL)` |  | pending |
| `fight.do_bash.return.002` | 2231 | `return;` |  | pending |
| `fight.do_bash.if.004` | 2235 | `if ((victim = get_char_room(ch,arg)) == NULL)` |  | pending |
| `fight.do_bash.return.003` | 2238 | `return;` |  | pending |
| `fight.do_bash.if.005` | 2241 | `if (victim->position < POS_FIGHTING)` |  | pending |
| `fight.do_bash.return.004` | 2244 | `return;` |  | pending |
| `fight.do_bash.if.006` | 2247 | `if (victim == ch)` |  | pending |
| `fight.do_bash.return.005` | 2250 | `return;` |  | pending |
| `fight.do_bash.if.007` | 2253 | `if (is_safe(ch,victim))` |  | pending |
| `fight.do_bash.return.006` | 2254 | `return;` |  | pending |
| `fight.do_bash.if.008` | 2256 | `if ( IS_NPC(victim) &&  	victim->fighting != NULL &&  	!is_same_group(ch,victim->fighting))` |  | pending |
| `fight.do_bash.and.003` | 2256 | `&&` |  | pending |
| `fight.do_bash.and.004` | 2257 | `&&` |  | pending |
| `fight.do_bash.return.007` | 2261 | `return;` |  | pending |
| `fight.do_bash.if.009` | 2264 | `if (IS_AFFECTED(ch,AFF_CHARM) && ch->master == victim)` |  | pending |
| `fight.do_bash.and.005` | 2264 | `&& ch->master == victim)` |  | pending |
| `fight.do_bash.return.008` | 2267 | `return;` |  | pending |
| `fight.do_bash.if.010` | 2276 | `if (ch->size < victim->size)` |  | pending |
| `fight.do_bash.if.011` | 2287 | `if (IS_SET(ch->off_flags,OFF_FAST) \|\| IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `fight.do_bash.or.003` | 2287 | `\|\| IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `fight.do_bash.if.012` | 2289 | `if (IS_SET(victim->off_flags,OFF_FAST) \|\| IS_AFFECTED(victim,AFF_HASTE))` |  | pending |
| `fight.do_bash.or.004` | 2289 | `\|\| IS_AFFECTED(victim,AFF_HASTE))` |  | pending |
| `fight.do_bash.if.013` | 2295 | `if (!IS_NPC(victim)  	&& chance < get_skill(victim,gsn_dodge) )` |  | pending |
| `fight.do_bash.and.006` | 2296 | `&& chance < get_skill(victim,gsn_dodge) )` |  | pending |
| `fight.do_bash.if.014` | 2306 | `if (number_percent() < chance )` |  | pending |

## do_dirt

[Source line 2339](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2339); ends at line 2470. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- mob_hit: `src/fight.c:352` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:242` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:113` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `get_skill`, `IS_NPC`, `IS_SET`, `send_to_char`, `get_char_room`, `IS_AFFECTED`, `act`, `is_safe`, `is_same_group`, `get_curr_stat`, `case`, `number_percent`, `damage`, `number_range`, `check_improve`, `WAIT_STATE`, `affect_to_char`, `check_killer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_dirt.if.001` | 2347 | `if ( (chance = get_skill(ch,gsn_dirt)) == 0     \|\|   (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_KICK_DIRT))     \|\|   (!IS_NPC(ch)     &&    ch->level < skill_table[gsn_dirt].skill_level[ch->class]))` |  | pending |
| `fight.do_dirt.or.001` | 2348 | `\|\|   (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_KICK_DIRT))` |  | pending |
| `fight.do_dirt.and.001` | 2348 | `&& !IS_SET(ch->off_flags,OFF_KICK_DIRT))` |  | pending |
| `fight.do_dirt.or.002` | 2349 | `\|\|   (!IS_NPC(ch)` |  | pending |
| `fight.do_dirt.and.002` | 2350 | `&&    ch->level < skill_table[gsn_dirt].skill_level[ch->class]))` |  | pending |
| `fight.do_dirt.return.001` | 2353 | `return;` |  | pending |
| `fight.do_dirt.if.002` | 2356 | `if (arg[0] == '\0')` |  | pending |
| `fight.do_dirt.if.003` | 2359 | `if (victim == NULL)` |  | pending |
| `fight.do_dirt.return.002` | 2362 | `return;` |  | pending |
| `fight.do_dirt.if.004` | 2366 | `if ((victim = get_char_room(ch,arg)) == NULL)` |  | pending |
| `fight.do_dirt.return.003` | 2369 | `return;` |  | pending |
| `fight.do_dirt.if.005` | 2372 | `if (IS_AFFECTED(victim,AFF_BLIND))` |  | pending |
| `fight.do_dirt.return.004` | 2375 | `return;` |  | pending |
| `fight.do_dirt.if.006` | 2378 | `if (victim == ch)` |  | pending |
| `fight.do_dirt.return.005` | 2381 | `return;` |  | pending |
| `fight.do_dirt.if.007` | 2384 | `if (is_safe(ch,victim))` |  | pending |
| `fight.do_dirt.return.006` | 2385 | `return;` |  | pending |
| `fight.do_dirt.if.008` | 2387 | `if (IS_NPC(victim) && 	 victim->fighting != NULL &&  	!is_same_group(ch,victim->fighting))` |  | pending |
| `fight.do_dirt.and.003` | 2387 | `&&` |  | pending |
| `fight.do_dirt.and.004` | 2388 | `&&` |  | pending |
| `fight.do_dirt.return.007` | 2392 | `return;` |  | pending |
| `fight.do_dirt.if.009` | 2395 | `if (IS_AFFECTED(ch,AFF_CHARM) && ch->master == victim)` |  | pending |
| `fight.do_dirt.and.005` | 2395 | `&& ch->master == victim)` |  | pending |
| `fight.do_dirt.return.008` | 2398 | `return;` |  | pending |
| `fight.do_dirt.if.010` | 2408 | `if (IS_SET(ch->off_flags,OFF_FAST) \|\| IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `fight.do_dirt.or.003` | 2408 | `\|\| IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `fight.do_dirt.if.011` | 2410 | `if (IS_SET(victim->off_flags,OFF_FAST) \|\| IS_AFFECTED(victim,AFF_HASTE))` |  | pending |
| `fight.do_dirt.or.004` | 2410 | `\|\| IS_AFFECTED(victim,AFF_HASTE))` |  | pending |
| `fight.do_dirt.if.012` | 2417 | `if (chance % 5 == 0)` |  | pending |
| `fight.do_dirt.switch.001` | 2422 | `switch(ch->in_room->sector_type)` |  | pending |
| `fight.do_dirt.case.001` | 2424 | `case(SECT_INSIDE):		chance -= 20;` |  | pending |
| `fight.do_dirt.break.001` | 2424 | `break;` |  | pending |
| `fight.do_dirt.case.002` | 2425 | `case(SECT_CITY):		chance -= 10;` |  | pending |
| `fight.do_dirt.break.002` | 2425 | `break;` |  | pending |
| `fight.do_dirt.case.003` | 2426 | `case(SECT_FIELD):		chance +=  5;` |  | pending |
| `fight.do_dirt.break.003` | 2426 | `break;` |  | pending |
| `fight.do_dirt.case.004` | 2427 | `case(SECT_FOREST):				break;` |  | pending |
| `fight.do_dirt.break.004` | 2427 | `break;` |  | pending |
| `fight.do_dirt.case.005` | 2428 | `case(SECT_HILLS):				break;` |  | pending |
| `fight.do_dirt.break.005` | 2428 | `break;` |  | pending |
| `fight.do_dirt.case.006` | 2429 | `case(SECT_MOUNTAIN):		chance -= 10;` |  | pending |
| `fight.do_dirt.break.006` | 2429 | `break;` |  | pending |
| `fight.do_dirt.case.007` | 2430 | `case(SECT_WATER_SWIM):		chance  =  0;` |  | pending |
| `fight.do_dirt.break.007` | 2430 | `break;` |  | pending |
| `fight.do_dirt.case.008` | 2431 | `case(SECT_WATER_NOSWIM):	chance  =  0;` |  | pending |
| `fight.do_dirt.break.008` | 2431 | `break;` |  | pending |
| `fight.do_dirt.case.009` | 2432 | `case(SECT_AIR):			chance  =  0;` |  | pending |
| `fight.do_dirt.break.009` | 2432 | `break;` |  | pending |
| `fight.do_dirt.case.010` | 2433 | `case(SECT_DESERT):		chance += 10;` |  | pending |
| `fight.do_dirt.break.010` | 2433 | `break;` |  | pending |
| `fight.do_dirt.if.013` | 2436 | `if (chance == 0)` |  | pending |
| `fight.do_dirt.return.009` | 2439 | `return;` |  | pending |
| `fight.do_dirt.if.014` | 2443 | `if (number_percent() < chance)` |  | pending |

## do_trip

[Source line 2472](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2472); ends at line 2584. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- mob_hit: `src/fight.c:364` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:249` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:272` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `get_skill`, `IS_NPC`, `IS_SET`, `send_to_char`, `get_char_room`, `is_safe`, `is_same_group`, `IS_AFFECTED`, `act`, `WAIT_STATE`, `get_curr_stat`, `number_percent`, `check_improve`, `DAZE_STATE`, `damage`, `number_range`, `check_killer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_trip.if.001` | 2480 | `if ( (chance = get_skill(ch,gsn_trip)) == 0     \|\|   (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_TRIP))     \|\|   (!IS_NPC(ch)  	  && ch->level < skill_table[gsn_trip].skill_level[ch->class]))` |  | pending |
| `fight.do_trip.or.001` | 2481 | `\|\|   (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_TRIP))` |  | pending |
| `fight.do_trip.and.001` | 2481 | `&& !IS_SET(ch->off_flags,OFF_TRIP))` |  | pending |
| `fight.do_trip.or.002` | 2482 | `\|\|   (!IS_NPC(ch)` |  | pending |
| `fight.do_trip.and.002` | 2483 | `&& ch->level < skill_table[gsn_trip].skill_level[ch->class]))` |  | pending |
| `fight.do_trip.return.001` | 2486 | `return;` |  | pending |
| `fight.do_trip.if.002` | 2490 | `if (arg[0] == '\0')` |  | pending |
| `fight.do_trip.if.003` | 2493 | `if (victim == NULL)` |  | pending |
| `fight.do_trip.return.002` | 2496 | `return;` |  | pending |
| `fight.do_trip.if.004` | 2500 | `if ((victim = get_char_room(ch,arg)) == NULL)` |  | pending |
| `fight.do_trip.return.003` | 2503 | `return;` |  | pending |
| `fight.do_trip.if.005` | 2506 | `if (is_safe(ch,victim))` |  | pending |
| `fight.do_trip.return.004` | 2507 | `return;` |  | pending |
| `fight.do_trip.if.006` | 2509 | `if (IS_NPC(victim) && 	 victim->fighting != NULL &&  	!is_same_group(ch,victim->fighting))` |  | pending |
| `fight.do_trip.and.003` | 2509 | `&&` |  | pending |
| `fight.do_trip.and.004` | 2510 | `&&` |  | pending |
| `fight.do_trip.return.005` | 2514 | `return;` |  | pending |
| `fight.do_trip.if.007` | 2517 | `if (IS_AFFECTED(victim,AFF_FLYING))` |  | pending |
| `fight.do_trip.return.006` | 2520 | `return;` |  | pending |
| `fight.do_trip.if.008` | 2523 | `if (victim->position < POS_FIGHTING)` |  | pending |
| `fight.do_trip.return.007` | 2526 | `return;` |  | pending |
| `fight.do_trip.if.009` | 2529 | `if (victim == ch)` |  | pending |
| `fight.do_trip.return.008` | 2534 | `return;` |  | pending |
| `fight.do_trip.if.010` | 2537 | `if (IS_AFFECTED(ch,AFF_CHARM) && ch->master == victim)` |  | pending |
| `fight.do_trip.and.005` | 2537 | `&& ch->master == victim)` |  | pending |
| `fight.do_trip.return.009` | 2540 | `return;` |  | pending |
| `fight.do_trip.if.011` | 2546 | `if (ch->size < victim->size)` |  | pending |
| `fight.do_trip.if.012` | 2554 | `if (IS_SET(ch->off_flags,OFF_FAST) \|\| IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `fight.do_trip.or.003` | 2554 | `\|\| IS_AFFECTED(ch,AFF_HASTE))` |  | pending |
| `fight.do_trip.if.013` | 2556 | `if (IS_SET(victim->off_flags,OFF_FAST) \|\| IS_AFFECTED(victim,AFF_HASTE))` |  | pending |
| `fight.do_trip.or.004` | 2556 | `\|\| IS_AFFECTED(victim,AFF_HASTE))` |  | pending |
| `fight.do_trip.if.014` | 2564 | `if (number_percent() < chance)` |  | pending |

## do_kill

[Source line 2588](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2588); ends at line 2650. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:90` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:92` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:157` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_room`, `multi_hit`, `is_safe`, `is_same_group`, `IS_AFFECTED`, `act`, `WAIT_STATE`, `check_killer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_kill.if.001` | 2595 | `if ( arg[0] == '\0' )` |  | pending |
| `fight.do_kill.return.001` | 2598 | `return;` |  | pending |
| `fight.do_kill.if.002` | 2601 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `fight.do_kill.return.002` | 2604 | `return;` |  | pending |
| `fight.do_kill.if.003` | 2617 | `if ( victim == ch )` |  | pending |
| `fight.do_kill.return.003` | 2621 | `return;` |  | pending |
| `fight.do_kill.if.004` | 2624 | `if ( is_safe( ch, victim ) )` |  | pending |
| `fight.do_kill.return.004` | 2625 | `return;` |  | pending |
| `fight.do_kill.if.005` | 2627 | `if ( victim->fighting != NULL &&  	!is_same_group(ch,victim->fighting))` |  | pending |
| `fight.do_kill.and.001` | 2627 | `&&` |  | pending |
| `fight.do_kill.return.005` | 2631 | `return;` |  | pending |
| `fight.do_kill.if.006` | 2634 | `if ( IS_AFFECTED(ch, AFF_CHARM) && ch->master == victim )` |  | pending |
| `fight.do_kill.and.002` | 2634 | `&& ch->master == victim )` |  | pending |
| `fight.do_kill.return.006` | 2637 | `return;` |  | pending |
| `fight.do_kill.if.007` | 2640 | `if ( ch->position == POS_FIGHTING )` |  | pending |
| `fight.do_kill.return.007` | 2643 | `return;` |  | pending |
| `fight.do_kill.return.008` | 2649 | `return;` |  | pending |

## do_murde

[Source line 2654](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2654); ends at line 2658. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:246` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:170` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_murde.return.001` | 2657 | `return;` |  | pending |

## do_murder

[Source line 2662](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2662); ends at line 2723. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_nasty: `src/special.c:343` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:247` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:171` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `IS_AFFECTED`, `IS_NPC`, `IS_SET`, `get_char_room`, `is_safe`, `is_same_group`, `act`, `WAIT_STATE`, `sprintf`, `do_function`, `check_killer`, `multi_hit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_murder.if.001` | 2670 | `if ( arg[0] == '\0' )` |  | pending |
| `fight.do_murder.return.001` | 2673 | `return;` |  | pending |
| `fight.do_murder.if.002` | 2676 | `if (IS_AFFECTED(ch,AFF_CHARM) \|\| (IS_NPC(ch) && IS_SET(ch->act,ACT_PET)))` |  | pending |
| `fight.do_murder.or.001` | 2676 | `\|\| (IS_NPC(ch) && IS_SET(ch->act,ACT_PET)))` |  | pending |
| `fight.do_murder.and.001` | 2676 | `&& IS_SET(ch->act,ACT_PET)))` |  | pending |
| `fight.do_murder.return.002` | 2677 | `return;` |  | pending |
| `fight.do_murder.if.003` | 2679 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `fight.do_murder.return.003` | 2682 | `return;` |  | pending |
| `fight.do_murder.if.004` | 2685 | `if ( victim == ch )` |  | pending |
| `fight.do_murder.return.004` | 2688 | `return;` |  | pending |
| `fight.do_murder.if.005` | 2691 | `if ( is_safe( ch, victim ) )` |  | pending |
| `fight.do_murder.return.005` | 2692 | `return;` |  | pending |
| `fight.do_murder.if.006` | 2694 | `if (IS_NPC(victim) && 	 victim->fighting != NULL &&  	!is_same_group(ch,victim->fighting))` |  | pending |
| `fight.do_murder.and.002` | 2694 | `&&` |  | pending |
| `fight.do_murder.and.003` | 2695 | `&&` |  | pending |
| `fight.do_murder.return.006` | 2699 | `return;` |  | pending |
| `fight.do_murder.if.007` | 2702 | `if ( IS_AFFECTED(ch, AFF_CHARM) && ch->master == victim )` |  | pending |
| `fight.do_murder.and.004` | 2702 | `&& ch->master == victim )` |  | pending |
| `fight.do_murder.return.007` | 2705 | `return;` |  | pending |
| `fight.do_murder.if.008` | 2708 | `if ( ch->position == POS_FIGHTING )` |  | pending |
| `fight.do_murder.return.008` | 2711 | `return;` |  | pending |
| `fight.do_murder.if.009` | 2715 | `if (IS_NPC(ch))` |  | pending |
| `fight.do_murder.return.009` | 2722 | `return;` |  | pending |

## do_backstab

[Source line 2727](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2727); ends at line 2798. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- mob_hit: `src/fight.c:376` (function_symbol_reference_candidate).
- spec_nasty: `src/special.c:340` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:238` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:240` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:86` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_room`, `is_safe`, `IS_NPC`, `is_same_group`, `get_eq_char`, `act`, `check_killer`, `WAIT_STATE`, `number_percent`, `get_skill`, `IS_AWAKE`, `check_improve`, `multi_hit`, `damage`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_backstab.if.001` | 2735 | `if (arg[0] == '\0')` |  | pending |
| `fight.do_backstab.return.001` | 2738 | `return;` |  | pending |
| `fight.do_backstab.if.002` | 2741 | `if (ch->fighting != NULL)` |  | pending |
| `fight.do_backstab.return.002` | 2744 | `return;` |  | pending |
| `fight.do_backstab.if.003` | 2747 | `if ((victim = get_char_room(ch,arg)) == NULL)` |  | pending |
| `fight.do_backstab.return.003` | 2750 | `return;` |  | pending |
| `fight.do_backstab.if.004` | 2753 | `if ( victim == ch )` |  | pending |
| `fight.do_backstab.return.004` | 2756 | `return;` |  | pending |
| `fight.do_backstab.if.005` | 2759 | `if ( is_safe( ch, victim ) )` |  | pending |
| `fight.do_backstab.return.005` | 2760 | `return;` |  | pending |
| `fight.do_backstab.if.006` | 2762 | `if (IS_NPC(victim) && 	 victim->fighting != NULL &&  	!is_same_group(ch,victim->fighting))` |  | pending |
| `fight.do_backstab.and.001` | 2762 | `&&` |  | pending |
| `fight.do_backstab.and.002` | 2763 | `&&` |  | pending |
| `fight.do_backstab.return.006` | 2767 | `return;` |  | pending |
| `fight.do_backstab.if.007` | 2770 | `if ( ( obj = get_eq_char( ch, WEAR_WIELD ) ) == NULL)` |  | pending |
| `fight.do_backstab.return.007` | 2773 | `return;` |  | pending |
| `fight.do_backstab.if.008` | 2776 | `if ( victim->hit < victim->max_hit / 3)` |  | pending |
| `fight.do_backstab.return.008` | 2780 | `return;` |  | pending |
| `fight.do_backstab.if.009` | 2785 | `if ( number_percent( ) < get_skill(ch,gsn_backstab)     \|\| ( get_skill(ch,gsn_backstab) >= 2 && !IS_AWAKE(victim) ) )` |  | pending |
| `fight.do_backstab.or.001` | 2786 | `\|\| ( get_skill(ch,gsn_backstab) >= 2 && !IS_AWAKE(victim) ) )` |  | pending |
| `fight.do_backstab.and.003` | 2786 | `&& !IS_AWAKE(victim) ) )` |  | pending |
| `fight.do_backstab.return.009` | 2797 | `return;` |  | pending |

## do_flee

[Source line 2802](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2802); ends at line 2859. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:974` (function_symbol_reference_candidate).
- damage: `src/fight.c:983` (function_symbol_reference_candidate).
- spec_nasty: `src/special.c:370` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:244` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:131` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `number_door`, `IS_SET`, `number_range`, `IS_NPC`, `move_char`, `act`, `number_percent`, `gain_exp`, `stop_fighting`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_flee.if.001` | 2809 | `if ( ( victim = ch->fighting ) == NULL )` |  | pending |
| `fight.do_flee.if.002` | 2811 | `if ( ch->position == POS_FIGHTING )` |  | pending |
| `fight.do_flee.return.001` | 2814 | `return;` |  | pending |
| `fight.do_flee.for.001` | 2818 | `for ( attempt = 0; attempt < 6; attempt++ )` |  | pending |
| `fight.do_flee.if.003` | 2824 | `if ( ( pexit = was_in->exit[door] ) == 0 	\|\|   pexit->u1.to_room == NULL 	\|\|   IS_SET(pexit->exit_info, EX_CLOSED) 	\|\|   number_range(0,ch->daze) != 0 	\|\| ( IS_NPC(ch) 	&&   IS_SET(pexit->u1.to_room->room_flags, ROOM_NO_MOB) ) )` |  | pending |
| `fight.do_flee.or.001` | 2825 | `\|\|   pexit->u1.to_room == NULL` |  | pending |
| `fight.do_flee.or.002` | 2826 | `\|\|   IS_SET(pexit->exit_info, EX_CLOSED)` |  | pending |
| `fight.do_flee.or.003` | 2827 | `\|\|   number_range(0,ch->daze) != 0` |  | pending |
| `fight.do_flee.or.004` | 2828 | `\|\| ( IS_NPC(ch)` |  | pending |
| `fight.do_flee.and.001` | 2829 | `&&   IS_SET(pexit->u1.to_room->room_flags, ROOM_NO_MOB) ) )` |  | pending |
| `fight.do_flee.continue.001` | 2830 | `continue;` |  | pending |
| `fight.do_flee.if.004` | 2833 | `if ( ( now_in = ch->in_room ) == was_in )` |  | pending |
| `fight.do_flee.continue.002` | 2834 | `continue;` |  | pending |
| `fight.do_flee.if.005` | 2840 | `if ( !IS_NPC(ch) )` |  | pending |
| `fight.do_flee.if.006` | 2843 | `if( (ch->class == 2)  	    && (number_percent() < 3*(ch->level/2) ) )` |  | pending |
| `fight.do_flee.and.002` | 2844 | `&& (number_percent() < 3*(ch->level/2) ) )` |  | pending |
| `fight.do_flee.return.002` | 2854 | `return;` |  | pending |
| `fight.do_flee.return.003` | 2858 | `return;` |  | pending |

## do_rescue

[Source line 2863](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2863); ends at line 2932. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:248` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:227` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_room`, `IS_NPC`, `is_same_group`, `WAIT_STATE`, `number_percent`, `get_skill`, `check_improve`, `act`, `stop_fighting`, `check_killer`, `set_fighting`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_rescue.if.001` | 2870 | `if ( arg[0] == '\0' )` |  | pending |
| `fight.do_rescue.return.001` | 2873 | `return;` |  | pending |
| `fight.do_rescue.if.002` | 2876 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `fight.do_rescue.return.002` | 2879 | `return;` |  | pending |
| `fight.do_rescue.if.003` | 2882 | `if ( victim == ch )` |  | pending |
| `fight.do_rescue.return.003` | 2885 | `return;` |  | pending |
| `fight.do_rescue.if.004` | 2888 | `if ( !IS_NPC(ch) && IS_NPC(victim) )` |  | pending |
| `fight.do_rescue.and.001` | 2888 | `&& IS_NPC(victim) )` |  | pending |
| `fight.do_rescue.return.004` | 2891 | `return;` |  | pending |
| `fight.do_rescue.if.005` | 2894 | `if ( ch->fighting == victim )` |  | pending |
| `fight.do_rescue.return.005` | 2897 | `return;` |  | pending |
| `fight.do_rescue.if.006` | 2900 | `if ( ( fch = victim->fighting ) == NULL )` |  | pending |
| `fight.do_rescue.return.006` | 2903 | `return;` |  | pending |
| `fight.do_rescue.if.007` | 2906 | `if ( IS_NPC(fch) && !is_same_group(ch,victim))` |  | pending |
| `fight.do_rescue.and.002` | 2906 | `&& !is_same_group(ch,victim))` |  | pending |
| `fight.do_rescue.return.007` | 2909 | `return;` |  | pending |
| `fight.do_rescue.if.008` | 2913 | `if ( number_percent( ) > get_skill(ch,gsn_rescue))` |  | pending |
| `fight.do_rescue.return.008` | 2917 | `return;` |  | pending |
| `fight.do_rescue.return.009` | 2931 | `return;` |  | pending |

## do_kick

[Source line 2936](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2936); ends at line 2970. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- mob_hit: `src/fight.c:347` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:245` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:156` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `send_to_char`, `IS_SET`, `WAIT_STATE`, `get_skill`, `number_percent`, `damage`, `number_range`, `check_improve`, `check_killer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_kick.if.001` | 2940 | `if ( !IS_NPC(ch)     &&   ch->level < skill_table[gsn_kick].skill_level[ch->class] )` |  | pending |
| `fight.do_kick.and.001` | 2941 | `&&   ch->level < skill_table[gsn_kick].skill_level[ch->class] )` |  | pending |
| `fight.do_kick.return.001` | 2945 | `return;` |  | pending |
| `fight.do_kick.if.002` | 2948 | `if (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_KICK))` |  | pending |
| `fight.do_kick.and.002` | 2948 | `&& !IS_SET(ch->off_flags,OFF_KICK))` |  | pending |
| `fight.do_kick.return.002` | 2949 | `return;` |  | pending |
| `fight.do_kick.if.003` | 2951 | `if ( ( victim = ch->fighting ) == NULL )` |  | pending |
| `fight.do_kick.return.003` | 2954 | `return;` |  | pending |
| `fight.do_kick.if.004` | 2958 | `if ( get_skill(ch,gsn_kick) > number_percent())` |  | pending |
| `fight.do_kick.return.004` | 2969 | `return;` |  | pending |

## do_disarm

[Source line 2975](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2975); ends at line 3048. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- mob_hit: `src/fight.c:342` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:243` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:114` (declaration_or_dispatch_reference).

Dependencies: `get_skill`, `send_to_char`, `get_eq_char`, `IS_NPC`, `IS_SET`, `get_weapon_skill`, `get_weapon_sn`, `get_curr_stat`, `number_percent`, `WAIT_STATE`, `disarm`, `check_improve`, `act`, `check_killer`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_disarm.if.001` | 2983 | `if ((chance = get_skill(ch,gsn_disarm)) == 0)` |  | pending |
| `fight.do_disarm.return.001` | 2986 | `return;` |  | pending |
| `fight.do_disarm.if.002` | 2989 | `if ( get_eq_char( ch, WEAR_WIELD ) == NULL      &&   ((hth = get_skill(ch,gsn_hand_to_hand)) == 0     \|\|    (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_DISARM))))` |  | pending |
| `fight.do_disarm.and.001` | 2990 | `&&   ((hth = get_skill(ch,gsn_hand_to_hand)) == 0` |  | pending |
| `fight.do_disarm.or.001` | 2991 | `\|\|    (IS_NPC(ch) && !IS_SET(ch->off_flags,OFF_DISARM))))` |  | pending |
| `fight.do_disarm.and.002` | 2991 | `&& !IS_SET(ch->off_flags,OFF_DISARM))))` |  | pending |
| `fight.do_disarm.return.002` | 2994 | `return;` |  | pending |
| `fight.do_disarm.if.003` | 2997 | `if ( ( victim = ch->fighting ) == NULL )` |  | pending |
| `fight.do_disarm.return.003` | 3000 | `return;` |  | pending |
| `fight.do_disarm.if.004` | 3003 | `if ( ( obj = get_eq_char( victim, WEAR_WIELD ) ) == NULL )` |  | pending |
| `fight.do_disarm.return.004` | 3006 | `return;` |  | pending |
| `fight.do_disarm.if.005` | 3017 | `if ( get_eq_char(ch,WEAR_WIELD) == NULL)` |  | pending |
| `fight.do_disarm.if.006` | 3032 | `if (number_percent() < chance)` |  | pending |
| `fight.do_disarm.return.005` | 3047 | `return;` |  | pending |

## do_sla

[Source line 3052](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:3052); ends at line 3056. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:315` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:248` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_sla.return.001` | 3055 | `return;` |  | pending |

## do_slay

[Source line 3060](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:3060); ends at line 3095. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:316` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:249` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_room`, `IS_NPC`, `get_trust`, `act`, `raw_kill`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `fight.do_slay.if.001` | 3066 | `if ( arg[0] == '\0' )` |  | pending |
| `fight.do_slay.return.001` | 3069 | `return;` |  | pending |
| `fight.do_slay.if.002` | 3072 | `if ( ( victim = get_char_room( ch, arg ) ) == NULL )` |  | pending |
| `fight.do_slay.return.002` | 3075 | `return;` |  | pending |
| `fight.do_slay.if.003` | 3078 | `if ( ch == victim )` |  | pending |
| `fight.do_slay.return.003` | 3081 | `return;` |  | pending |
| `fight.do_slay.if.004` | 3084 | `if ( !IS_NPC(victim) && victim->level >= get_trust(ch) )` |  | pending |
| `fight.do_slay.and.001` | 3084 | `&& victim->level >= get_trust(ch) )` |  | pending |
| `fight.do_slay.return.004` | 3087 | `return;` |  | pending |
| `fight.do_slay.return.005` | 3094 | `return;` |  | pending |

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

## Static tables


## Commented code candidates

- Lines 1737–1749: disabled inside block comment; content hash `5568d3521000ab18451f7808bdfacfd368d07358b7784e108e454699d4dd0c52`.
- Lines 2606–2616: disabled inside block comment; content hash `0a9f7dc67ef62743ee9923287b8385f0ac2d90fd0a375fe6f5d94139981c4b08`.

# src/special.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `78e00c637522c18be0626547577cfa6ddcee0ac68206772d3c0409f361cdd2b6`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## spec_lookup

[Source line 99](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:99); ends at line 111. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_string: `src/act_wiz.c:3792` (lexical_call_candidate).
- load_specials: `src/db.c:1081` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2304` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_lookup.for.001` | 103 | `for ( i = 0; spec_table[i].name != NULL; i++)` |  | pending |
| `special.spec_lookup.if.001` | 105 | `if (LOWER(name[0]) == LOWER(spec_table[i].name[0])         &&  !str_prefix( name,spec_table[i].name))` |  | pending |
| `special.spec_lookup.and.001` | 106 | `&&  !str_prefix( name,spec_table[i].name))` |  | pending |
| `special.spec_lookup.return.001` | 107 | `return spec_table[i].function;` |  | pending |
| `special.spec_lookup.return.002` | 110 | `return 0;` |  | pending |
| `special.spec_lookup.first-full.path` | 105 | `first full` | special.spec_lookup.first-full | specified |
| `special.spec_lookup.ambiguous-prefix-first.path` | 105 | `ambiguous prefix first` | special.spec_lookup.ambiguous-prefix-first | specified |
| `special.spec_lookup.last-full.path` | 105 | `last full` | special.spec_lookup.last-full | specified |
| `special.spec_lookup.unknown.path` | 105 | `unknown` | special.spec_lookup.unknown | specified |
| `special.spec_lookup.empty.path` | 105 | `empty` | special.spec_lookup.empty | specified |

## spec_name

[Source line 113](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:113); ends at line 124. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_mstat: `src/act_wiz.c:1703` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2305` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_name.for.001` | 117 | `for (i = 0; spec_table[i].function != NULL; i++)` |  | pending |
| `special.spec_name.if.001` | 119 | `if (function == spec_table[i].function)` |  | pending |
| `special.spec_name.return.001` | 120 | `return spec_table[i].name;` |  | pending |
| `special.spec_name.return.002` | 123 | `return NULL;` |  | pending |
| `special.spec_name.first-function.path` | 119 | `first function` | special.spec_name.first-function | specified |
| `special.spec_name.last-function.path` | 119 | `last function` | special.spec_name.last-function | specified |
| `special.spec_name.null-function.path` | 119 | `null function` | special.spec_name.null-function | specified |
| `special.spec_name.unregistered-function.path` | 119 | `unregistered function` | special.spec_name.unregistered-function | specified |

## spec_troll_member

[Source line 126](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:126); ends at line 183. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:64` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:90` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `IS_AFFECTED`, `IS_NPC`, `is_safe`, `number_range`, `act`, `multi_hit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_troll_member.if.001` | 132 | `if (!IS_AWAKE(ch) \|\| IS_AFFECTED(ch,AFF_CALM) \|\| ch->in_room == NULL      \|\|  IS_AFFECTED(ch,AFF_CHARM) \|\| ch->fighting != NULL)` |  | pending |
| `special.spec_troll_member.or.001` | 132 | `\|\| IS_AFFECTED(ch,AFF_CALM) \|\| ch->in_room == NULL` |  | pending |
| `special.spec_troll_member.or.002` | 132 | `\|\| ch->in_room == NULL` |  | pending |
| `special.spec_troll_member.or.003` | 133 | `\|\|  IS_AFFECTED(ch,AFF_CHARM) \|\| ch->fighting != NULL)` |  | pending |
| `special.spec_troll_member.or.004` | 133 | `\|\| ch->fighting != NULL)` |  | pending |
| `special.spec_troll_member.return.001` | 134 | `return FALSE;` |  | pending |
| `special.spec_troll_member.for.001` | 137 | `for (vch = ch->in_room->people;  vch != NULL;  vch = vch->next_in_room)` |  | pending |
| `special.spec_troll_member.if.002` | 139 | `if (!IS_NPC(vch) \|\| ch == vch)` |  | pending |
| `special.spec_troll_member.or.005` | 139 | `\|\| ch == vch)` |  | pending |
| `special.spec_troll_member.continue.001` | 140 | `continue;` |  | pending |
| `special.spec_troll_member.if.003` | 142 | `if (vch->pIndexData->vnum == MOB_VNUM_PATROLMAN)` |  | pending |
| `special.spec_troll_member.return.002` | 143 | `return FALSE;` |  | pending |
| `special.spec_troll_member.if.004` | 145 | `if (vch->pIndexData->group == GROUP_VNUM_OGRES 	&&  ch->level > vch->level - 2 && !is_safe(ch,vch))` |  | pending |
| `special.spec_troll_member.and.001` | 146 | `&&  ch->level > vch->level - 2 && !is_safe(ch,vch))` |  | pending |
| `special.spec_troll_member.and.002` | 146 | `&& !is_safe(ch,vch))` |  | pending |
| `special.spec_troll_member.if.005` | 148 | `if (number_range(0,count) == 0)` |  | pending |
| `special.spec_troll_member.if.006` | 155 | `if (victim == NULL)` |  | pending |
| `special.spec_troll_member.return.003` | 156 | `return FALSE;` |  | pending |
| `special.spec_troll_member.switch.001` | 159 | `switch (number_range(0,6))` |  | pending |
| `special.spec_troll_member.default.001` | 161 | `default:  message = NULL;` |  | pending |
| `special.spec_troll_member.break.001` | 161 | `break;` |  | pending |
| `special.spec_troll_member.case.001` | 162 | `case 0:	message = "$n yells 'I've been looking for you, punk!'";` |  | pending |
| `special.spec_troll_member.break.002` | 163 | `break;` |  | pending |
| `special.spec_troll_member.case.002` | 164 | `case 1: message = "With a scream of rage, $n attacks $N.";` |  | pending |
| `special.spec_troll_member.break.003` | 165 | `break;` |  | pending |
| `special.spec_troll_member.case.003` | 166 | `case 2: message =` |  | pending |
| `special.spec_troll_member.break.004` | 168 | `break;` |  | pending |
| `special.spec_troll_member.case.004` | 169 | `case 3: message = "$n cracks his knuckles and says 'Do ya feel lucky?'";` |  | pending |
| `special.spec_troll_member.break.005` | 170 | `break;` |  | pending |
| `special.spec_troll_member.case.005` | 171 | `case 4: message = "$n says 'There's no cops to save you this time!'";` |  | pending |
| `special.spec_troll_member.break.006` | 172 | `break;` |  | pending |
| `special.spec_troll_member.case.006` | 173 | `case 5: message = "$n says 'Time to join your brother, spud.'";` |  | pending |
| `special.spec_troll_member.break.007` | 174 | `break;` |  | pending |
| `special.spec_troll_member.case.007` | 175 | `case 6: message = "$n says 'Let's rock.'";` |  | pending |
| `special.spec_troll_member.break.008` | 176 | `break;` |  | pending |
| `special.spec_troll_member.if.007` | 179 | `if (message != NULL)` |  | pending |
| `special.spec_troll_member.return.004` | 182 | `return TRUE;` |  | pending |

## spec_ogre_member

[Source line 185](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:185); ends at line 242. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:65` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:91` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `IS_AFFECTED`, `IS_NPC`, `is_safe`, `number_range`, `act`, `multi_hit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_ogre_member.if.001` | 191 | `if (!IS_AWAKE(ch) \|\| IS_AFFECTED(ch,AFF_CALM) \|\| ch->in_room == NULL     \|\|  IS_AFFECTED(ch,AFF_CHARM) \|\| ch->fighting != NULL)` |  | pending |
| `special.spec_ogre_member.or.001` | 191 | `\|\| IS_AFFECTED(ch,AFF_CALM) \|\| ch->in_room == NULL` |  | pending |
| `special.spec_ogre_member.or.002` | 191 | `\|\| ch->in_room == NULL` |  | pending |
| `special.spec_ogre_member.or.003` | 192 | `\|\|  IS_AFFECTED(ch,AFF_CHARM) \|\| ch->fighting != NULL)` |  | pending |
| `special.spec_ogre_member.or.004` | 192 | `\|\| ch->fighting != NULL)` |  | pending |
| `special.spec_ogre_member.return.001` | 193 | `return FALSE;` |  | pending |
| `special.spec_ogre_member.for.001` | 196 | `for (vch = ch->in_room->people;  vch != NULL;  vch = vch->next_in_room)` |  | pending |
| `special.spec_ogre_member.if.002` | 198 | `if (!IS_NPC(vch) \|\| ch == vch)` |  | pending |
| `special.spec_ogre_member.or.005` | 198 | `\|\| ch == vch)` |  | pending |
| `special.spec_ogre_member.continue.001` | 199 | `continue;` |  | pending |
| `special.spec_ogre_member.if.003` | 201 | `if (vch->pIndexData->vnum == MOB_VNUM_PATROLMAN)` |  | pending |
| `special.spec_ogre_member.return.002` | 202 | `return FALSE;` |  | pending |
| `special.spec_ogre_member.if.004` | 204 | `if (vch->pIndexData->group == GROUP_VNUM_TROLLS         &&  ch->level > vch->level - 2 && !is_safe(ch,vch))` |  | pending |
| `special.spec_ogre_member.and.001` | 205 | `&&  ch->level > vch->level - 2 && !is_safe(ch,vch))` |  | pending |
| `special.spec_ogre_member.and.002` | 205 | `&& !is_safe(ch,vch))` |  | pending |
| `special.spec_ogre_member.if.005` | 207 | `if (number_range(0,count) == 0)` |  | pending |
| `special.spec_ogre_member.if.006` | 214 | `if (victim == NULL)` |  | pending |
| `special.spec_ogre_member.return.003` | 215 | `return FALSE;` |  | pending |
| `special.spec_ogre_member.switch.001` | 218 | `switch (number_range(0,6))` |  | pending |
| `special.spec_ogre_member.default.001` | 220 | `default: message = NULL;` |  | pending |
| `special.spec_ogre_member.break.001` | 220 | `break;` |  | pending |
| `special.spec_ogre_member.case.001` | 221 | `case 0: message = "$n yells 'I've been looking for you, punk!'";` |  | pending |
| `special.spec_ogre_member.break.002` | 222 | `break;` |  | pending |
| `special.spec_ogre_member.case.002` | 223 | `case 1: message = "With a scream of rage, $n attacks $N.'";` |  | pending |
| `special.spec_ogre_member.break.003` | 224 | `break;` |  | pending |
| `special.spec_ogre_member.case.003` | 225 | `case 2: message =` |  | pending |
| `special.spec_ogre_member.break.004` | 227 | `break;` |  | pending |
| `special.spec_ogre_member.case.004` | 228 | `case 3: message = "$n cracks his knuckles and says 'Do ya feel lucky?'";` |  | pending |
| `special.spec_ogre_member.break.005` | 229 | `break;` |  | pending |
| `special.spec_ogre_member.case.005` | 230 | `case 4: message = "$n says 'There's no cops to save you this time!'";` |  | pending |
| `special.spec_ogre_member.break.006` | 231 | `break;` |  | pending |
| `special.spec_ogre_member.case.006` | 232 | `case 5: message = "$n says 'Time to join your brother, spud.'";` |  | pending |
| `special.spec_ogre_member.break.007` | 233 | `break;` |  | pending |
| `special.spec_ogre_member.case.007` | 234 | `case 6: message = "$n says 'Let's rock.'";` |  | pending |
| `special.spec_ogre_member.break.008` | 235 | `break;` |  | pending |
| `special.spec_ogre_member.if.007` | 238 | `if (message != NULL)` |  | pending |
| `special.spec_ogre_member.return.004` | 241 | `return TRUE;` |  | pending |

## spec_patrolman

[Source line 244](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:244); ends at line 320. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:66` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:92` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `IS_AFFECTED`, `number_range`, `IS_NPC`, `get_eq_char`, `act`, `send_to_char`, `multi_hit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_patrolman.if.001` | 251 | `if (!IS_AWAKE(ch) \|\| IS_AFFECTED(ch,AFF_CALM) \|\| ch->in_room == NULL     \|\|  IS_AFFECTED(ch,AFF_CHARM) \|\| ch->fighting != NULL)` |  | pending |
| `special.spec_patrolman.or.001` | 251 | `\|\| IS_AFFECTED(ch,AFF_CALM) \|\| ch->in_room == NULL` |  | pending |
| `special.spec_patrolman.or.002` | 251 | `\|\| ch->in_room == NULL` |  | pending |
| `special.spec_patrolman.or.003` | 252 | `\|\|  IS_AFFECTED(ch,AFF_CHARM) \|\| ch->fighting != NULL)` |  | pending |
| `special.spec_patrolman.or.004` | 252 | `\|\| ch->fighting != NULL)` |  | pending |
| `special.spec_patrolman.return.001` | 253 | `return FALSE;` |  | pending |
| `special.spec_patrolman.for.001` | 256 | `for (vch = ch->in_room->people; vch != NULL; vch = vch->next_in_room)` |  | pending |
| `special.spec_patrolman.if.002` | 258 | `if (vch == ch)` |  | pending |
| `special.spec_patrolman.continue.001` | 259 | `continue;` |  | pending |
| `special.spec_patrolman.if.003` | 261 | `if (vch->fighting != NULL)` |  | pending |
| `special.spec_patrolman.if.004` | 263 | `if (number_range(0,count) == 0)` |  | pending |
| `special.spec_patrolman.ternary.001` | 265 | `? vch : vch->fighting;` |  | pending |
| `special.spec_patrolman.if.005` | 270 | `if (victim == NULL \|\| (IS_NPC(victim) && victim->spec_fun == ch->spec_fun))` |  | pending |
| `special.spec_patrolman.or.005` | 270 | `\|\| (IS_NPC(victim) && victim->spec_fun == ch->spec_fun))` |  | pending |
| `special.spec_patrolman.and.001` | 270 | `&& victim->spec_fun == ch->spec_fun))` |  | pending |
| `special.spec_patrolman.return.002` | 271 | `return FALSE;` |  | pending |
| `special.spec_patrolman.if.006` | 273 | `if (((obj = get_eq_char(ch,WEAR_NECK_1)) != NULL      &&   obj->pIndexData->vnum == OBJ_VNUM_WHISTLE)     \|\|  ((obj = get_eq_char(ch,WEAR_NECK_2)) != NULL     &&   obj->pIndexData->vnum == OBJ_VNUM_WHISTLE))` |  | pending |
| `special.spec_patrolman.and.002` | 274 | `&&   obj->pIndexData->vnum == OBJ_VNUM_WHISTLE)` |  | pending |
| `special.spec_patrolman.or.006` | 275 | `\|\|  ((obj = get_eq_char(ch,WEAR_NECK_2)) != NULL` |  | pending |
| `special.spec_patrolman.and.003` | 276 | `&&   obj->pIndexData->vnum == OBJ_VNUM_WHISTLE))` |  | pending |
| `special.spec_patrolman.for.002` | 281 | `for ( vch = char_list; vch != NULL; vch = vch->next )` |  | pending |
| `special.spec_patrolman.if.007` | 283 | `if ( vch->in_room == NULL )` |  | pending |
| `special.spec_patrolman.continue.002` | 284 | `continue;` |  | pending |
| `special.spec_patrolman.if.008` | 286 | `if (vch->in_room != ch->in_room  	    &&  vch->in_room->area == ch->in_room->area)` |  | pending |
| `special.spec_patrolman.and.004` | 287 | `&&  vch->in_room->area == ch->in_room->area)` |  | pending |
| `special.spec_patrolman.switch.001` | 292 | `switch (number_range(0,6))` |  | pending |
| `special.spec_patrolman.default.001` | 294 | `default:	message = NULL;` |  | pending |
| `special.spec_patrolman.break.001` | 294 | `break;` |  | pending |
| `special.spec_patrolman.case.001` | 295 | `case 0:	message = "$n yells 'All roit! All roit! break it up!'";` |  | pending |
| `special.spec_patrolman.break.002` | 296 | `break;` |  | pending |
| `special.spec_patrolman.case.002` | 297 | `case 1: message =` |  | pending |
| `special.spec_patrolman.break.003` | 299 | `break;` |  | pending |
| `special.spec_patrolman.case.003` | 300 | `case 2: message =` |  | pending |
| `special.spec_patrolman.break.004` | 302 | `break;` |  | pending |
| `special.spec_patrolman.case.004` | 303 | `case 3: message = "$n shouts 'Stop that! Stop that!' and attacks.";` |  | pending |
| `special.spec_patrolman.break.005` | 304 | `break;` |  | pending |
| `special.spec_patrolman.case.005` | 305 | `case 4: message = "$n pulls out his billy and goes to work.";` |  | pending |
| `special.spec_patrolman.break.006` | 306 | `break;` |  | pending |
| `special.spec_patrolman.case.006` | 307 | `case 5: message =` |  | pending |
| `special.spec_patrolman.break.007` | 309 | `break;` |  | pending |
| `special.spec_patrolman.case.007` | 310 | `case 6: message = "$n says 'Settle down, you hooligans!'";` |  | pending |
| `special.spec_patrolman.break.008` | 311 | `break;` |  | pending |
| `special.spec_patrolman.if.009` | 314 | `if (message != NULL)` |  | pending |
| `special.spec_patrolman.return.003` | 319 | `return TRUE;` |  | pending |

## spec_nasty

[Source line 323](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:323); ends at line 375. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:63` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:89` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `IS_NPC`, `do_function`, `number_bits`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_nasty.if.001` | 328 | `if (!IS_AWAKE(ch))` |  | pending |
| `special.spec_nasty.return.001` | 329 | `return FALSE;` |  | pending |
| `special.spec_nasty.if.002` | 332 | `if (ch->position != POS_FIGHTING)` |  | pending |
| `special.spec_nasty.for.001` | 333 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next)` |  | pending |
| `special.spec_nasty.if.003` | 336 | `if (!IS_NPC(victim)              && (victim->level > ch->level)              && (victim->level < ch->level + 10))` |  | pending |
| `special.spec_nasty.and.001` | 337 | `&& (victim->level > ch->level)` |  | pending |
| `special.spec_nasty.and.002` | 338 | `&& (victim->level < ch->level + 10))` |  | pending |
| `special.spec_nasty.if.004` | 341 | `if (ch->position != POS_FIGHTING)` |  | pending |
| `special.spec_nasty.return.002` | 347 | `return TRUE;` |  | pending |
| `special.spec_nasty.return.003` | 350 | `return FALSE;` |  | pending |
| `special.spec_nasty.if.005` | 354 | `if ( (victim = ch->fighting) == NULL)` |  | pending |
| `special.spec_nasty.return.004` | 355 | `return FALSE;` |  | pending |
| `special.spec_nasty.switch.001` | 357 | `switch ( number_bits(2) )` |  | pending |
| `special.spec_nasty.case.001` | 359 | `case 0:  act( "$n rips apart your coin purse, spilling your gold!",` |  | pending |
| `special.spec_nasty.return.005` | 368 | `return TRUE;` |  | pending |
| `special.spec_nasty.case.002` | 370 | `case 1:  do_function(ch, &do_flee, "");` |  | pending |
| `special.spec_nasty.return.006` | 371 | `return TRUE;` |  | pending |
| `special.spec_nasty.default.001` | 373 | `default: return FALSE;` |  | pending |
| `special.spec_nasty.return.007` | 373 | `return FALSE;` |  | pending |

## dragon

[Source line 380](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:380); ends at line 403. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_breath_acid: `src/special.c:434` (lexical_call_candidate).
- spec_breath_fire: `src/special.c:441` (lexical_call_candidate).
- spec_breath_frost: `src/special.c:448` (lexical_call_candidate).
- spec_breath_lightning: `src/special.c:470` (lexical_call_candidate).

Dependencies: `number_bits`, `skill_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.dragon.if.001` | 386 | `if ( ch->position != POS_FIGHTING )` |  | pending |
| `special.dragon.return.001` | 387 | `return FALSE;` |  | pending |
| `special.dragon.for.001` | 389 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.dragon.if.002` | 392 | `if ( victim->fighting == ch && number_bits( 3 ) == 0 )` |  | pending |
| `special.dragon.and.001` | 392 | `&& number_bits( 3 ) == 0 )` |  | pending |
| `special.dragon.break.001` | 393 | `break;` |  | pending |
| `special.dragon.if.003` | 396 | `if ( victim == NULL )` |  | pending |
| `special.dragon.return.002` | 397 | `return FALSE;` |  | pending |
| `special.dragon.if.004` | 399 | `if ( ( sn = skill_lookup( spell_name ) ) < 0 )` |  | pending |
| `special.dragon.return.003` | 400 | `return FALSE;` |  | pending |
| `special.dragon.return.004` | 402 | `return TRUE;` |  | pending |

## spec_breath_any

[Source line 410](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:410); ends at line 428. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:45` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:71` (declaration_or_dispatch_reference).

Dependencies: `number_bits`, `spec_breath_fire`, `spec_breath_lightning`, `spec_breath_gas`, `spec_breath_acid`, `spec_breath_frost`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_breath_any.if.001` | 412 | `if ( ch->position != POS_FIGHTING )` |  | pending |
| `special.spec_breath_any.return.001` | 413 | `return FALSE;` |  | pending |
| `special.spec_breath_any.switch.001` | 415 | `switch ( number_bits( 3 ) )` |  | pending |
| `special.spec_breath_any.case.001` | 417 | `case 0: return spec_breath_fire		( ch );` |  | pending |
| `special.spec_breath_any.return.002` | 417 | `return spec_breath_fire		( ch );` |  | pending |
| `special.spec_breath_any.case.002` | 418 | `case 1:` |  | pending |
| `special.spec_breath_any.case.003` | 419 | `case 2: return spec_breath_lightning	( ch );` |  | pending |
| `special.spec_breath_any.return.003` | 419 | `return spec_breath_lightning	( ch );` |  | pending |
| `special.spec_breath_any.case.004` | 420 | `case 3: return spec_breath_gas		( ch );` |  | pending |
| `special.spec_breath_any.return.004` | 420 | `return spec_breath_gas		( ch );` |  | pending |
| `special.spec_breath_any.case.005` | 421 | `case 4: return spec_breath_acid		( ch );` |  | pending |
| `special.spec_breath_any.return.005` | 421 | `return spec_breath_acid		( ch );` |  | pending |
| `special.spec_breath_any.case.006` | 422 | `case 5:` |  | pending |
| `special.spec_breath_any.case.007` | 423 | `case 6:` |  | pending |
| `special.spec_breath_any.case.008` | 424 | `case 7: return spec_breath_frost		( ch );` |  | pending |
| `special.spec_breath_any.return.006` | 424 | `return spec_breath_frost		( ch );` |  | pending |
| `special.spec_breath_any.return.007` | 427 | `return FALSE;` |  | pending |

## spec_breath_acid

[Source line 432](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:432); ends at line 435. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_breath_any: `src/special.c:421` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/special.c:46` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:72` (declaration_or_dispatch_reference).

Dependencies: `dragon`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_breath_acid.return.001` | 434 | `return dragon( ch, "acid breath" );` |  | pending |

## spec_breath_fire

[Source line 439](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:439); ends at line 442. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_breath_any: `src/special.c:417` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/special.c:47` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:73` (declaration_or_dispatch_reference).

Dependencies: `dragon`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_breath_fire.return.001` | 441 | `return dragon( ch, "fire breath" );` |  | pending |

## spec_breath_frost

[Source line 446](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:446); ends at line 449. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_breath_any: `src/special.c:424` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/special.c:48` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:74` (declaration_or_dispatch_reference).

Dependencies: `dragon`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_breath_frost.return.001` | 448 | `return dragon( ch, "frost breath" );` |  | pending |

## spec_breath_gas

[Source line 453](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:453); ends at line 464. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_breath_any: `src/special.c:420` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/special.c:49` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:75` (declaration_or_dispatch_reference).

Dependencies: `skill_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_breath_gas.if.001` | 457 | `if ( ch->position != POS_FIGHTING )` |  | pending |
| `special.spec_breath_gas.return.001` | 458 | `return FALSE;` |  | pending |
| `special.spec_breath_gas.if.002` | 460 | `if ( ( sn = skill_lookup( "gas breath" ) ) < 0 )` |  | pending |
| `special.spec_breath_gas.return.002` | 461 | `return FALSE;` |  | pending |
| `special.spec_breath_gas.return.003` | 463 | `return TRUE;` |  | pending |

## spec_breath_lightning

[Source line 468](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:468); ends at line 471. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_breath_any: `src/special.c:419` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/special.c:50` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:76` (declaration_or_dispatch_reference).

Dependencies: `dragon`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_breath_lightning.return.001` | 470 | `return dragon( ch, "lightning breath" );` |  | pending |

## spec_cast_adept

[Source line 475](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:475); ends at line 536. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:51` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:77` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `can_see`, `number_bits`, `IS_NPC`, `act`, `spell_armor`, `skill_lookup`, `spell_bless`, `spell_cure_blindness`, `spell_cure_light`, `spell_cure_poison`, `spell_refresh`, `spell_cure_disease`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_cast_adept.if.001` | 480 | `if ( !IS_AWAKE(ch) )` |  | pending |
| `special.spec_cast_adept.return.001` | 481 | `return FALSE;` |  | pending |
| `special.spec_cast_adept.for.001` | 483 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.spec_cast_adept.if.002` | 486 | `if ( victim != ch && can_see( ch, victim ) && number_bits( 1 ) == 0  	     && !IS_NPC(victim) && victim->level < 11)` |  | pending |
| `special.spec_cast_adept.and.001` | 486 | `&& can_see( ch, victim ) && number_bits( 1 ) == 0` |  | pending |
| `special.spec_cast_adept.and.002` | 486 | `&& number_bits( 1 ) == 0` |  | pending |
| `special.spec_cast_adept.and.003` | 487 | `&& !IS_NPC(victim) && victim->level < 11)` |  | pending |
| `special.spec_cast_adept.and.004` | 487 | `&& victim->level < 11)` |  | pending |
| `special.spec_cast_adept.break.001` | 488 | `break;` |  | pending |
| `special.spec_cast_adept.if.003` | 491 | `if ( victim == NULL )` |  | pending |
| `special.spec_cast_adept.return.002` | 492 | `return FALSE;` |  | pending |
| `special.spec_cast_adept.switch.001` | 494 | `switch ( number_bits( 4 ) )` |  | pending |
| `special.spec_cast_adept.case.001` | 496 | `case 0:` |  | pending |
| `special.spec_cast_adept.return.003` | 499 | `return TRUE;` |  | pending |
| `special.spec_cast_adept.case.002` | 501 | `case 1:` |  | pending |
| `special.spec_cast_adept.return.004` | 504 | `return TRUE;` |  | pending |
| `special.spec_cast_adept.case.003` | 506 | `case 2:` |  | pending |
| `special.spec_cast_adept.return.005` | 510 | `return TRUE;` |  | pending |
| `special.spec_cast_adept.case.004` | 512 | `case 3:` |  | pending |
| `special.spec_cast_adept.return.006` | 516 | `return TRUE;` |  | pending |
| `special.spec_cast_adept.case.005` | 518 | `case 4:` |  | pending |
| `special.spec_cast_adept.return.007` | 522 | `return TRUE;` |  | pending |
| `special.spec_cast_adept.case.006` | 524 | `case 5:` |  | pending |
| `special.spec_cast_adept.return.008` | 527 | `return TRUE;` |  | pending |
| `special.spec_cast_adept.case.007` | 529 | `case 6:` |  | pending |
| `special.spec_cast_adept.return.009` | 535 | `return FALSE;` |  | pending |

## spec_cast_cleric

[Source line 540](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:540); ends at line 589. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:52` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:78` (declaration_or_dispatch_reference).

Dependencies: `number_bits`, `skill_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_cast_cleric.if.001` | 547 | `if ( ch->position != POS_FIGHTING )` |  | pending |
| `special.spec_cast_cleric.return.001` | 548 | `return FALSE;` |  | pending |
| `special.spec_cast_cleric.for.001` | 550 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.spec_cast_cleric.if.002` | 553 | `if ( victim->fighting == ch && number_bits( 2 ) == 0 )` |  | pending |
| `special.spec_cast_cleric.and.001` | 553 | `&& number_bits( 2 ) == 0 )` |  | pending |
| `special.spec_cast_cleric.break.001` | 554 | `break;` |  | pending |
| `special.spec_cast_cleric.if.003` | 557 | `if ( victim == NULL )` |  | pending |
| `special.spec_cast_cleric.return.002` | 558 | `return FALSE;` |  | pending |
| `special.spec_cast_cleric.for.002` | 560 | `for ( ;; )` |  | pending |
| `special.spec_cast_cleric.switch.001` | 564 | `switch ( number_bits( 4 ) )` |  | pending |
| `special.spec_cast_cleric.case.001` | 566 | `case  0: min_level =  0;` |  | pending |
| `special.spec_cast_cleric.break.002` | 566 | `break;` |  | pending |
| `special.spec_cast_cleric.case.002` | 567 | `case  1: min_level =  3;` |  | pending |
| `special.spec_cast_cleric.break.003` | 567 | `break;` |  | pending |
| `special.spec_cast_cleric.case.003` | 568 | `case  2: min_level =  7;` |  | pending |
| `special.spec_cast_cleric.break.004` | 568 | `break;` |  | pending |
| `special.spec_cast_cleric.case.004` | 569 | `case  3: min_level =  9;` |  | pending |
| `special.spec_cast_cleric.break.005` | 569 | `break;` |  | pending |
| `special.spec_cast_cleric.case.005` | 570 | `case  4: min_level = 10;` |  | pending |
| `special.spec_cast_cleric.break.006` | 570 | `break;` |  | pending |
| `special.spec_cast_cleric.case.006` | 571 | `case  5: min_level = 12;` |  | pending |
| `special.spec_cast_cleric.break.007` | 571 | `break;` |  | pending |
| `special.spec_cast_cleric.case.007` | 572 | `case  6: min_level = 12;` |  | pending |
| `special.spec_cast_cleric.break.008` | 572 | `break;` |  | pending |
| `special.spec_cast_cleric.case.008` | 573 | `case  7: min_level = 13;` |  | pending |
| `special.spec_cast_cleric.break.009` | 573 | `break;` |  | pending |
| `special.spec_cast_cleric.case.009` | 574 | `case  8:` |  | pending |
| `special.spec_cast_cleric.case.010` | 575 | `case  9:` |  | pending |
| `special.spec_cast_cleric.case.011` | 576 | `case 10: min_level = 15;` |  | pending |
| `special.spec_cast_cleric.break.010` | 576 | `break;` |  | pending |
| `special.spec_cast_cleric.case.012` | 577 | `case 11: min_level = 15;` |  | pending |
| `special.spec_cast_cleric.break.011` | 577 | `break;` |  | pending |
| `special.spec_cast_cleric.default.001` | 578 | `default: min_level = 16;` |  | pending |
| `special.spec_cast_cleric.break.012` | 578 | `break;` |  | pending |
| `special.spec_cast_cleric.if.004` | 581 | `if ( ch->level >= min_level )` |  | pending |
| `special.spec_cast_cleric.break.013` | 582 | `break;` |  | pending |
| `special.spec_cast_cleric.if.005` | 585 | `if ( ( sn = skill_lookup( spell ) ) < 0 )` |  | pending |
| `special.spec_cast_cleric.return.003` | 586 | `return FALSE;` |  | pending |
| `special.spec_cast_cleric.return.004` | 588 | `return TRUE;` |  | pending |

## spec_cast_judge

[Source line 591](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:591); ends at line 616. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:53` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:79` (declaration_or_dispatch_reference).

Dependencies: `number_bits`, `skill_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_cast_judge.if.001` | 598 | `if ( ch->position != POS_FIGHTING )` |  | pending |
| `special.spec_cast_judge.return.001` | 599 | `return FALSE;` |  | pending |
| `special.spec_cast_judge.for.001` | 601 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.spec_cast_judge.if.002` | 604 | `if ( victim->fighting == ch && number_bits( 2 ) == 0 )` |  | pending |
| `special.spec_cast_judge.and.001` | 604 | `&& number_bits( 2 ) == 0 )` |  | pending |
| `special.spec_cast_judge.break.001` | 605 | `break;` |  | pending |
| `special.spec_cast_judge.if.003` | 608 | `if ( victim == NULL )` |  | pending |
| `special.spec_cast_judge.return.002` | 609 | `return FALSE;` |  | pending |
| `special.spec_cast_judge.if.004` | 612 | `if ( ( sn = skill_lookup( spell ) ) < 0 )` |  | pending |
| `special.spec_cast_judge.return.003` | 613 | `return FALSE;` |  | pending |
| `special.spec_cast_judge.return.004` | 615 | `return TRUE;` |  | pending |

## spec_cast_mage

[Source line 620](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:620); ends at line 668. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spec_mayor: `src/special.c:909` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/special.c:54` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:80` (declaration_or_dispatch_reference).

Dependencies: `number_bits`, `skill_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_cast_mage.if.001` | 627 | `if ( ch->position != POS_FIGHTING )` |  | pending |
| `special.spec_cast_mage.return.001` | 628 | `return FALSE;` |  | pending |
| `special.spec_cast_mage.for.001` | 630 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.spec_cast_mage.if.002` | 633 | `if ( victim->fighting == ch && number_bits( 2 ) == 0 )` |  | pending |
| `special.spec_cast_mage.and.001` | 633 | `&& number_bits( 2 ) == 0 )` |  | pending |
| `special.spec_cast_mage.break.001` | 634 | `break;` |  | pending |
| `special.spec_cast_mage.if.003` | 637 | `if ( victim == NULL )` |  | pending |
| `special.spec_cast_mage.return.002` | 638 | `return FALSE;` |  | pending |
| `special.spec_cast_mage.for.002` | 640 | `for ( ;; )` |  | pending |
| `special.spec_cast_mage.switch.001` | 644 | `switch ( number_bits( 4 ) )` |  | pending |
| `special.spec_cast_mage.case.001` | 646 | `case  0: min_level =  0;` |  | pending |
| `special.spec_cast_mage.break.002` | 646 | `break;` |  | pending |
| `special.spec_cast_mage.case.002` | 647 | `case  1: min_level =  3;` |  | pending |
| `special.spec_cast_mage.break.003` | 647 | `break;` |  | pending |
| `special.spec_cast_mage.case.003` | 648 | `case  2: min_level =  7;` |  | pending |
| `special.spec_cast_mage.break.004` | 648 | `break;` |  | pending |
| `special.spec_cast_mage.case.004` | 649 | `case  3: min_level =  8;` |  | pending |
| `special.spec_cast_mage.break.005` | 649 | `break;` |  | pending |
| `special.spec_cast_mage.case.005` | 650 | `case  4: min_level = 11;` |  | pending |
| `special.spec_cast_mage.break.006` | 650 | `break;` |  | pending |
| `special.spec_cast_mage.case.006` | 651 | `case  5: min_level = 12;` |  | pending |
| `special.spec_cast_mage.break.007` | 651 | `break;` |  | pending |
| `special.spec_cast_mage.case.007` | 652 | `case  6: min_level = 13;` |  | pending |
| `special.spec_cast_mage.break.008` | 652 | `break;` |  | pending |
| `special.spec_cast_mage.case.008` | 653 | `case  7:` |  | pending |
| `special.spec_cast_mage.case.009` | 654 | `case  8:` |  | pending |
| `special.spec_cast_mage.case.010` | 655 | `case  9: min_level = 15;` |  | pending |
| `special.spec_cast_mage.break.009` | 655 | `break;` |  | pending |
| `special.spec_cast_mage.case.011` | 656 | `case 10: min_level = 20;` |  | pending |
| `special.spec_cast_mage.break.010` | 656 | `break;` |  | pending |
| `special.spec_cast_mage.default.001` | 657 | `default: min_level = 20;` |  | pending |
| `special.spec_cast_mage.break.011` | 657 | `break;` |  | pending |
| `special.spec_cast_mage.if.004` | 660 | `if ( ch->level >= min_level )` |  | pending |
| `special.spec_cast_mage.break.012` | 661 | `break;` |  | pending |
| `special.spec_cast_mage.if.005` | 664 | `if ( ( sn = skill_lookup( spell ) ) < 0 )` |  | pending |
| `special.spec_cast_mage.return.003` | 665 | `return FALSE;` |  | pending |
| `special.spec_cast_mage.return.004` | 667 | `return TRUE;` |  | pending |

## spec_cast_undead

[Source line 672](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:672); ends at line 718. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:55` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:81` (declaration_or_dispatch_reference).

Dependencies: `number_bits`, `skill_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_cast_undead.if.001` | 679 | `if ( ch->position != POS_FIGHTING )` |  | pending |
| `special.spec_cast_undead.return.001` | 680 | `return FALSE;` |  | pending |
| `special.spec_cast_undead.for.001` | 682 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.spec_cast_undead.if.002` | 685 | `if ( victim->fighting == ch && number_bits( 2 ) == 0 )` |  | pending |
| `special.spec_cast_undead.and.001` | 685 | `&& number_bits( 2 ) == 0 )` |  | pending |
| `special.spec_cast_undead.break.001` | 686 | `break;` |  | pending |
| `special.spec_cast_undead.if.003` | 689 | `if ( victim == NULL )` |  | pending |
| `special.spec_cast_undead.return.002` | 690 | `return FALSE;` |  | pending |
| `special.spec_cast_undead.for.002` | 692 | `for ( ;; )` |  | pending |
| `special.spec_cast_undead.switch.001` | 696 | `switch ( number_bits( 4 ) )` |  | pending |
| `special.spec_cast_undead.case.001` | 698 | `case  0: min_level =  0;` |  | pending |
| `special.spec_cast_undead.break.002` | 698 | `break;` |  | pending |
| `special.spec_cast_undead.case.002` | 699 | `case  1: min_level =  3;` |  | pending |
| `special.spec_cast_undead.break.003` | 699 | `break;` |  | pending |
| `special.spec_cast_undead.case.003` | 700 | `case  2: min_level =  6;` |  | pending |
| `special.spec_cast_undead.break.004` | 700 | `break;` |  | pending |
| `special.spec_cast_undead.case.004` | 701 | `case  3: min_level =  9;` |  | pending |
| `special.spec_cast_undead.break.005` | 701 | `break;` |  | pending |
| `special.spec_cast_undead.case.005` | 702 | `case  4: min_level = 12;` |  | pending |
| `special.spec_cast_undead.break.006` | 702 | `break;` |  | pending |
| `special.spec_cast_undead.case.006` | 703 | `case  5: min_level = 15;` |  | pending |
| `special.spec_cast_undead.break.007` | 703 | `break;` |  | pending |
| `special.spec_cast_undead.case.007` | 704 | `case  6: min_level = 18;` |  | pending |
| `special.spec_cast_undead.break.008` | 704 | `break;` |  | pending |
| `special.spec_cast_undead.case.008` | 705 | `case  7: min_level = 21;` |  | pending |
| `special.spec_cast_undead.break.009` | 705 | `break;` |  | pending |
| `special.spec_cast_undead.case.009` | 706 | `case  8: min_level = 20;` |  | pending |
| `special.spec_cast_undead.break.010` | 706 | `break;` |  | pending |
| `special.spec_cast_undead.default.001` | 707 | `default: min_level = 18;` |  | pending |
| `special.spec_cast_undead.break.011` | 707 | `break;` |  | pending |
| `special.spec_cast_undead.if.004` | 710 | `if ( ch->level >= min_level )` |  | pending |
| `special.spec_cast_undead.break.012` | 711 | `break;` |  | pending |
| `special.spec_cast_undead.if.005` | 714 | `if ( ( sn = skill_lookup( spell ) ) < 0 )` |  | pending |
| `special.spec_cast_undead.return.003` | 715 | `return FALSE;` |  | pending |
| `special.spec_cast_undead.return.004` | 717 | `return TRUE;` |  | pending |

## spec_executioner

[Source line 721](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:721); ends at line 754. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:56` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:82` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `IS_NPC`, `IS_SET`, `can_see`, `sprintf`, `REMOVE_BIT`, `do_function`, `multi_hit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_executioner.if.001` | 728 | `if ( !IS_AWAKE(ch) \|\| ch->fighting != NULL )` |  | pending |
| `special.spec_executioner.or.001` | 728 | `\|\| ch->fighting != NULL )` |  | pending |
| `special.spec_executioner.return.001` | 729 | `return FALSE;` |  | pending |
| `special.spec_executioner.for.001` | 732 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.spec_executioner.if.002` | 736 | `if ( !IS_NPC(victim) && IS_SET(victim->act, PLR_KILLER)  	&&   can_see(ch,victim))` |  | pending |
| `special.spec_executioner.and.001` | 736 | `&& IS_SET(victim->act, PLR_KILLER)` |  | pending |
| `special.spec_executioner.and.002` | 737 | `&&   can_see(ch,victim))` |  | pending |
| `special.spec_executioner.break.001` | 738 | `break;` |  | pending |
| `special.spec_executioner.if.003` | 740 | `if ( !IS_NPC(victim) && IS_SET(victim->act, PLR_THIEF)  	&&   can_see(ch,victim))` |  | pending |
| `special.spec_executioner.and.003` | 740 | `&& IS_SET(victim->act, PLR_THIEF)` |  | pending |
| `special.spec_executioner.and.004` | 741 | `&&   can_see(ch,victim))` |  | pending |
| `special.spec_executioner.break.002` | 742 | `break;` |  | pending |
| `special.spec_executioner.if.004` | 745 | `if ( victim == NULL )` |  | pending |
| `special.spec_executioner.return.002` | 746 | `return FALSE;` |  | pending |
| `special.spec_executioner.return.003` | 753 | `return TRUE;` |  | pending |

## spec_fido

[Source line 758](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:758); ends at line 786. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:57` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:83` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `act`, `obj_from_obj`, `obj_to_room`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_fido.if.001` | 765 | `if ( !IS_AWAKE(ch) )` |  | pending |
| `special.spec_fido.return.001` | 766 | `return FALSE;` |  | pending |
| `special.spec_fido.for.001` | 768 | `for ( corpse = ch->in_room->contents; corpse != NULL; corpse = c_next )` |  | pending |
| `special.spec_fido.if.002` | 771 | `if ( corpse->item_type != ITEM_CORPSE_NPC )` |  | pending |
| `special.spec_fido.continue.001` | 772 | `continue;` |  | pending |
| `special.spec_fido.for.002` | 775 | `for ( obj = corpse->contains; obj; obj = obj_next )` |  | pending |
| `special.spec_fido.return.002` | 782 | `return TRUE;` |  | pending |
| `special.spec_fido.return.003` | 785 | `return FALSE;` |  | pending |

## spec_guard

[Source line 790](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:790); ends at line 846. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:58` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:84` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `IS_NPC`, `IS_SET`, `can_see`, `sprintf`, `REMOVE_BIT`, `do_function`, `multi_hit`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_guard.if.001` | 799 | `if ( !IS_AWAKE(ch) \|\| ch->fighting != NULL )` |  | pending |
| `special.spec_guard.or.001` | 799 | `\|\| ch->fighting != NULL )` |  | pending |
| `special.spec_guard.return.001` | 800 | `return FALSE;` |  | pending |
| `special.spec_guard.for.001` | 806 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.spec_guard.if.002` | 810 | `if ( !IS_NPC(victim) && IS_SET(victim->act, PLR_KILLER)  	&&   can_see(ch,victim))` |  | pending |
| `special.spec_guard.and.001` | 810 | `&& IS_SET(victim->act, PLR_KILLER)` |  | pending |
| `special.spec_guard.and.002` | 811 | `&&   can_see(ch,victim))` |  | pending |
| `special.spec_guard.break.001` | 812 | `break;` |  | pending |
| `special.spec_guard.if.003` | 814 | `if ( !IS_NPC(victim) && IS_SET(victim->act, PLR_THIEF)  	&&   can_see(ch,victim))` |  | pending |
| `special.spec_guard.and.003` | 814 | `&& IS_SET(victim->act, PLR_THIEF)` |  | pending |
| `special.spec_guard.and.004` | 815 | `&&   can_see(ch,victim))` |  | pending |
| `special.spec_guard.break.002` | 816 | `break;` |  | pending |
| `special.spec_guard.if.004` | 818 | `if ( victim->fighting != NULL 	&&   victim->fighting != ch 	&&   victim->alignment < max_evil )` |  | pending |
| `special.spec_guard.and.005` | 819 | `&&   victim->fighting != ch` |  | pending |
| `special.spec_guard.and.006` | 820 | `&&   victim->alignment < max_evil )` |  | pending |
| `special.spec_guard.if.005` | 827 | `if ( victim != NULL )` |  | pending |
| `special.spec_guard.return.002` | 834 | `return TRUE;` |  | pending |
| `special.spec_guard.if.006` | 837 | `if ( ech != NULL )` |  | pending |
| `special.spec_guard.return.003` | 842 | `return TRUE;` |  | pending |
| `special.spec_guard.return.004` | 845 | `return FALSE;` |  | pending |

## spec_janitor

[Source line 850](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:850); ends at line 875. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:59` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:85` (declaration_or_dispatch_reference).

Dependencies: `IS_AWAKE`, `IS_SET`, `can_loot`, `act`, `obj_from_room`, `obj_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_janitor.if.001` | 855 | `if ( !IS_AWAKE(ch) )` |  | pending |
| `special.spec_janitor.return.001` | 856 | `return FALSE;` |  | pending |
| `special.spec_janitor.for.001` | 858 | `for ( trash = ch->in_room->contents; trash != NULL; trash = trash_next )` |  | pending |
| `special.spec_janitor.if.002` | 861 | `if ( !IS_SET( trash->wear_flags, ITEM_TAKE ) \|\| !can_loot(ch,trash))` |  | pending |
| `special.spec_janitor.or.001` | 861 | `\|\| !can_loot(ch,trash))` |  | pending |
| `special.spec_janitor.continue.001` | 862 | `continue;` |  | pending |
| `special.spec_janitor.if.003` | 863 | `if ( trash->item_type == ITEM_DRINK_CON 	\|\|   trash->item_type == ITEM_TRASH 	\|\|   trash->cost < 10 )` |  | pending |
| `special.spec_janitor.or.002` | 864 | `\|\|   trash->item_type == ITEM_TRASH` |  | pending |
| `special.spec_janitor.or.003` | 865 | `\|\|   trash->cost < 10 )` |  | pending |
| `special.spec_janitor.return.002` | 870 | `return TRUE;` |  | pending |
| `special.spec_janitor.return.003` | 874 | `return FALSE;` |  | pending |

## spec_mayor

[Source line 879](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:879); ends at line 977. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:60` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:86` (declaration_or_dispatch_reference).

Dependencies: `spec_cast_mage`, `move_char`, `act`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_mayor.if.001` | 891 | `if ( !move )` |  | pending |
| `special.spec_mayor.if.002` | 893 | `if ( time_info.hour ==  6 )` |  | pending |
| `special.spec_mayor.if.003` | 900 | `if ( time_info.hour == 20 )` |  | pending |
| `special.spec_mayor.if.004` | 908 | `if ( ch->fighting != NULL )` |  | pending |
| `special.spec_mayor.return.001` | 909 | `return spec_cast_mage( ch );` |  | pending |
| `special.spec_mayor.if.005` | 910 | `if ( !move \|\| ch->position < POS_SLEEPING )` |  | pending |
| `special.spec_mayor.or.001` | 910 | `\|\| ch->position < POS_SLEEPING )` |  | pending |
| `special.spec_mayor.return.002` | 911 | `return FALSE;` |  | pending |
| `special.spec_mayor.switch.001` | 913 | `switch ( path[pos] )` |  | pending |
| `special.spec_mayor.case.001` | 915 | `case '0':` |  | pending |
| `special.spec_mayor.case.002` | 916 | `case '1':` |  | pending |
| `special.spec_mayor.case.003` | 917 | `case '2':` |  | pending |
| `special.spec_mayor.case.004` | 918 | `case '3':` |  | pending |
| `special.spec_mayor.break.001` | 920 | `break;` |  | pending |
| `special.spec_mayor.case.005` | 922 | `case 'W':` |  | pending |
| `special.spec_mayor.break.002` | 925 | `break;` |  | pending |
| `special.spec_mayor.case.006` | 927 | `case 'S':` |  | pending |
| `special.spec_mayor.break.003` | 930 | `break;` |  | pending |
| `special.spec_mayor.case.007` | 932 | `case 'a':` |  | pending |
| `special.spec_mayor.break.004` | 934 | `break;` |  | pending |
| `special.spec_mayor.case.008` | 936 | `case 'b':` |  | pending |
| `special.spec_mayor.break.005` | 939 | `break;` |  | pending |
| `special.spec_mayor.case.009` | 941 | `case 'c':` |  | pending |
| `special.spec_mayor.break.006` | 944 | `break;` |  | pending |
| `special.spec_mayor.case.010` | 946 | `case 'd':` |  | pending |
| `special.spec_mayor.break.007` | 948 | `break;` |  | pending |
| `special.spec_mayor.case.011` | 950 | `case 'e':` |  | pending |
| `special.spec_mayor.break.008` | 953 | `break;` |  | pending |
| `special.spec_mayor.case.012` | 955 | `case 'E':` |  | pending |
| `special.spec_mayor.break.009` | 958 | `break;` |  | pending |
| `special.spec_mayor.case.013` | 960 | `case 'O':` |  | pending |
| `special.spec_mayor.break.010` | 963 | `break;` |  | pending |
| `special.spec_mayor.case.014` | 965 | `case 'C':` |  | pending |
| `special.spec_mayor.break.011` | 968 | `break;` |  | pending |
| `special.spec_mayor.case.015` | 970 | `case '.' :` |  | pending |
| `special.spec_mayor.break.012` | 972 | `break;` |  | pending |
| `special.spec_mayor.return.003` | 976 | `return FALSE;` |  | pending |

## spec_poison

[Source line 981](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:981); ends at line 995. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:61` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:87` (declaration_or_dispatch_reference).

Dependencies: `number_percent`, `act`, `spell_poison`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_poison.if.001` | 985 | `if ( ch->position != POS_FIGHTING     \|\| ( victim = ch->fighting ) == NULL     \|\|   number_percent( ) > 2 * ch->level )` |  | pending |
| `special.spec_poison.or.001` | 986 | `\|\| ( victim = ch->fighting ) == NULL` |  | pending |
| `special.spec_poison.or.002` | 987 | `\|\|   number_percent( ) > 2 * ch->level )` |  | pending |
| `special.spec_poison.return.001` | 988 | `return FALSE;` |  | pending |
| `special.spec_poison.return.002` | 994 | `return TRUE;` |  | pending |

## spec_thief

[Source line 999](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:999); ends at line 1041. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/special.c:62` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/special.c:88` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `number_bits`, `can_see`, `IS_AWAKE`, `number_range`, `act`, `UMIN`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `special.spec_thief.if.001` | 1005 | `if ( ch->position != POS_STANDING )` |  | pending |
| `special.spec_thief.return.001` | 1006 | `return FALSE;` |  | pending |
| `special.spec_thief.for.001` | 1008 | `for ( victim = ch->in_room->people; victim != NULL; victim = v_next )` |  | pending |
| `special.spec_thief.if.002` | 1012 | `if ( IS_NPC(victim) 	\|\|   victim->level >= LEVEL_IMMORTAL 	\|\|   number_bits( 5 ) != 0  	\|\|   !can_see(ch,victim))` |  | pending |
| `special.spec_thief.or.001` | 1013 | `\|\|   victim->level >= LEVEL_IMMORTAL` |  | pending |
| `special.spec_thief.or.002` | 1014 | `\|\|   number_bits( 5 ) != 0` |  | pending |
| `special.spec_thief.or.003` | 1015 | `\|\|   !can_see(ch,victim))` |  | pending |
| `special.spec_thief.continue.001` | 1016 | `continue;` |  | pending |
| `special.spec_thief.if.003` | 1018 | `if ( IS_AWAKE(victim) && number_range( 0, ch->level ) == 0 )` |  | pending |
| `special.spec_thief.and.001` | 1018 | `&& number_range( 0, ch->level ) == 0 )` |  | pending |
| `special.spec_thief.return.002` | 1024 | `return TRUE;` |  | pending |
| `special.spec_thief.return.003` | 1036 | `return TRUE;` |  | pending |
| `special.spec_thief.return.004` | 1040 | `return FALSE;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#include <time.h>` — pending configuration/reachability review.
- Line 31: `#else` — pending configuration/reachability review.
- Line 32: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 33: `#endif` — pending configuration/reachability review.
- Line 34: `#include <stdio.h>` — pending configuration/reachability review.
- Line 35: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 36: `#include <string.h>` — pending configuration/reachability review.
- Line 37: `#include <time.h>` — pending configuration/reachability review.
- Line 38: `#include "merc.h"` — pending configuration/reachability review.
- Line 39: `#include "interp.h"` — pending configuration/reachability review.
- Line 40: `#include "magic.h"` — pending configuration/reachability review.

## Static tables

- `spec_table` at line 69 — pending entry/termination review.

## Commented code candidates


# src/effects.c

Role: translation_unit. Disposition: **pending**. SHA-256: `db376c5680960f280967cc0cb192f531f330532c898d260645b5eff1950797df`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## acid_effect

[Source line 40](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/effects.c:40); ends at line 194. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- acid_effect: `src/effects.c:50` (lexical_call_candidate).
- acid_effect: `src/effects.c:64` (lexical_call_candidate).
- acid_effect: `src/effects.c:187` (lexical_call_candidate).
- spell_acid_breath: `src/magic.c:4484` (lexical_call_candidate).
- spell_acid_breath: `src/magic.c:4489` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2161` (declaration_or_dispatch_reference).

Dependencies: `acid_effect`, `IS_OBJ_STAT`, `number_range`, `URANGE`, `number_percent`, `act`, `affect_enchant`, `UMAX`, `new_affect`, `obj_from_obj`, `obj_to_room`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `effects.acid_effect.if.001` | 42 | `if (target == TARGET_ROOM)` |  | pending |
| `effects.acid_effect.for.001` | 47 | `for (obj = room->contents; obj != NULL; obj = obj_next)` |  | pending |
| `effects.acid_effect.return.001` | 52 | `return;` |  | pending |
| `effects.acid_effect.if.002` | 55 | `if (target == TARGET_CHAR)` |  | pending |
| `effects.acid_effect.for.002` | 61 | `for (obj = victim->carrying; obj != NULL; obj = obj_next)` |  | pending |
| `effects.acid_effect.return.002` | 66 | `return;` |  | pending |
| `effects.acid_effect.if.003` | 69 | `if (target == TARGET_OBJ)` |  | pending |
| `effects.acid_effect.if.004` | 76 | `if (IS_OBJ_STAT(obj,ITEM_BURN_PROOF) 	\|\|  IS_OBJ_STAT(obj,ITEM_NOPURGE) 	\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.acid_effect.or.001` | 77 | `\|\|  IS_OBJ_STAT(obj,ITEM_NOPURGE)` |  | pending |
| `effects.acid_effect.or.002` | 78 | `\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.acid_effect.return.003` | 79 | `return;` |  | pending |
| `effects.acid_effect.if.005` | 83 | `if (chance > 25)` |  | pending |
| `effects.acid_effect.if.006` | 85 | `if (chance > 50)` |  | pending |
| `effects.acid_effect.if.007` | 88 | `if (IS_OBJ_STAT(obj,ITEM_BLESS))` |  | pending |
| `effects.acid_effect.switch.001` | 93 | `switch (obj->item_type)` |  | pending |
| `effects.acid_effect.default.001` | 95 | `default:` |  | pending |
| `effects.acid_effect.return.004` | 96 | `return;` |  | pending |
| `effects.acid_effect.case.001` | 97 | `case ITEM_CONTAINER:` |  | pending |
| `effects.acid_effect.case.002` | 98 | `case ITEM_CORPSE_PC:` |  | pending |
| `effects.acid_effect.case.003` | 99 | `case ITEM_CORPSE_NPC:` |  | pending |
| `effects.acid_effect.break.001` | 101 | `break;` |  | pending |
| `effects.acid_effect.case.004` | 102 | `case ITEM_ARMOR:` |  | pending |
| `effects.acid_effect.break.002` | 104 | `break;` |  | pending |
| `effects.acid_effect.case.005` | 105 | `case ITEM_CLOTHING:` |  | pending |
| `effects.acid_effect.break.003` | 107 | `break;` |  | pending |
| `effects.acid_effect.case.006` | 108 | `case ITEM_STAFF:` |  | pending |
| `effects.acid_effect.case.007` | 109 | `case ITEM_WAND:` |  | pending |
| `effects.acid_effect.break.004` | 112 | `break;` |  | pending |
| `effects.acid_effect.case.008` | 113 | `case ITEM_SCROLL:` |  | pending |
| `effects.acid_effect.break.005` | 116 | `break;` |  | pending |
| `effects.acid_effect.if.008` | 121 | `if (number_percent() > chance)` |  | pending |
| `effects.acid_effect.return.005` | 122 | `return;` |  | pending |
| `effects.acid_effect.if.009` | 124 | `if (obj->carried_by != NULL)` |  | pending |
| `effects.acid_effect.if.010` | 126 | `if (obj->in_room != NULL && obj->in_room->people != NULL)` |  | pending |
| `effects.acid_effect.and.001` | 126 | `&& obj->in_room->people != NULL)` |  | pending |
| `effects.acid_effect.if.011` | 129 | `if (obj->item_type == ITEM_ARMOR)` |  | pending |
| `effects.acid_effect.for.003` | 137 | `for ( paf = obj->affected; paf != NULL; paf = paf->next)` |  | pending |
| `effects.acid_effect.if.012` | 139 | `if ( paf->location == APPLY_AC)` |  | pending |
| `effects.acid_effect.break.006` | 145 | `break;` |  | pending |
| `effects.acid_effect.if.013` | 149 | `if (!af_found)` |  | pending |
| `effects.acid_effect.if.014` | 164 | `if (obj->carried_by != NULL && obj->wear_loc != WEAR_NONE)` |  | pending |
| `effects.acid_effect.and.002` | 164 | `&& obj->wear_loc != WEAR_NONE)` |  | pending |
| `effects.acid_effect.for.004` | 165 | `for (i = 0; i < 4; i++)` |  | pending |
| `effects.acid_effect.return.006` | 167 | `return;` |  | pending |
| `effects.acid_effect.if.015` | 171 | `if (obj->contains)` |  | pending |
| `effects.acid_effect.for.005` | 173 | `for (t_obj = obj->contains; t_obj != NULL; t_obj = n_obj)` |  | pending |
| `effects.acid_effect.if.016` | 177 | `if (obj->in_room != NULL)` |  | pending |
| `effects.acid_effect.if.017` | 179 | `if (obj->carried_by != NULL)` |  | pending |
| `effects.acid_effect.continue.001` | 184 | `continue;` |  | pending |
| `effects.acid_effect.return.007` | 192 | `return;` |  | pending |

## cold_effect

[Source line 197](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/effects.c:197); ends at line 297. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- cold_effect: `src/effects.c:207` (lexical_call_candidate).
- cold_effect: `src/effects.c:242` (lexical_call_candidate).
- one_hit: `src/fight.c:654` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4568` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4583` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4588` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4596` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4601` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2162` (declaration_or_dispatch_reference).

Dependencies: `cold_effect`, `saves_spell`, `act`, `skill_lookup`, `affect_join`, `IS_NPC`, `gain_condition`, `IS_OBJ_STAT`, `number_range`, `URANGE`, `number_percent`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `effects.cold_effect.if.001` | 199 | `if (target == TARGET_ROOM)` |  | pending |
| `effects.cold_effect.for.001` | 204 | `for (obj = room->contents; obj != NULL; obj = obj_next)` |  | pending |
| `effects.cold_effect.return.001` | 209 | `return;` |  | pending |
| `effects.cold_effect.if.002` | 212 | `if (target == TARGET_CHAR)` |  | pending |
| `effects.cold_effect.if.003` | 218 | `if (!saves_spell(level/4 + dam / 20, victim, DAM_COLD))` |  | pending |
| `effects.cold_effect.if.004` | 235 | `if (!IS_NPC(victim))` |  | pending |
| `effects.cold_effect.for.002` | 239 | `for (obj = victim->carrying; obj != NULL; obj = obj_next)` |  | pending |
| `effects.cold_effect.return.002` | 244 | `return;` |  | pending |
| `effects.cold_effect.if.005` | 247 | `if (target == TARGET_OBJ)` |  | pending |
| `effects.cold_effect.if.006` | 253 | `if (IS_OBJ_STAT(obj,ITEM_BURN_PROOF) 	\|\|  IS_OBJ_STAT(obj,ITEM_NOPURGE) 	\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.cold_effect.or.001` | 254 | `\|\|  IS_OBJ_STAT(obj,ITEM_NOPURGE)` |  | pending |
| `effects.cold_effect.or.002` | 255 | `\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.cold_effect.return.003` | 256 | `return;` |  | pending |
| `effects.cold_effect.if.007` | 260 | `if (chance > 25)` |  | pending |
| `effects.cold_effect.if.008` | 262 | `if (chance > 50)` |  | pending |
| `effects.cold_effect.if.009` | 265 | `if (IS_OBJ_STAT(obj,ITEM_BLESS))` |  | pending |
| `effects.cold_effect.switch.001` | 270 | `switch(obj->item_type)` |  | pending |
| `effects.cold_effect.default.001` | 272 | `default:` |  | pending |
| `effects.cold_effect.return.004` | 273 | `return;` |  | pending |
| `effects.cold_effect.case.001` | 274 | `case ITEM_POTION:` |  | pending |
| `effects.cold_effect.break.001` | 277 | `break;` |  | pending |
| `effects.cold_effect.case.002` | 278 | `case ITEM_DRINK_CON:` |  | pending |
| `effects.cold_effect.break.002` | 281 | `break;` |  | pending |
| `effects.cold_effect.if.010` | 286 | `if (number_percent() > chance)` |  | pending |
| `effects.cold_effect.return.005` | 287 | `return;` |  | pending |
| `effects.cold_effect.if.011` | 289 | `if (obj->carried_by != NULL)` |  | pending |
| `effects.cold_effect.if.012` | 291 | `if (obj->in_room != NULL && obj->in_room->people != NULL)` |  | pending |
| `effects.cold_effect.and.001` | 291 | `&& obj->in_room->people != NULL)` |  | pending |
| `effects.cold_effect.return.006` | 295 | `return;` |  | pending |

## fire_effect

[Source line 301](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/effects.c:301); ends at line 442. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- fire_effect: `src/effects.c:311` (lexical_call_candidate).
- fire_effect: `src/effects.c:350` (lexical_call_candidate).
- fire_effect: `src/effects.c:435` (lexical_call_candidate).
- one_hit: `src/fight.c:644` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4512` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4527` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4532` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4540` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4545` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2163` (declaration_or_dispatch_reference).

Dependencies: `fire_effect`, `IS_AFFECTED`, `saves_spell`, `act`, `skill_lookup`, `number_range`, `affect_to_char`, `IS_NPC`, `gain_condition`, `IS_OBJ_STAT`, `URANGE`, `number_percent`, `obj_from_obj`, `obj_to_room`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `effects.fire_effect.if.001` | 303 | `if (target == TARGET_ROOM)` |  | pending |
| `effects.fire_effect.for.001` | 308 | `for (obj = room->contents; obj != NULL; obj = obj_next)` |  | pending |
| `effects.fire_effect.return.001` | 313 | `return;` |  | pending |
| `effects.fire_effect.if.002` | 316 | `if (target == TARGET_CHAR)` |  | pending |
| `effects.fire_effect.if.003` | 322 | `if (!IS_AFFECTED(victim,AFF_BLIND) 	&&  !saves_spell(level / 4 + dam / 20, victim,DAM_FIRE))` |  | pending |
| `effects.fire_effect.and.001` | 323 | `&&  !saves_spell(level / 4 + dam / 20, victim,DAM_FIRE))` |  | pending |
| `effects.fire_effect.if.004` | 342 | `if (!IS_NPC(victim))` |  | pending |
| `effects.fire_effect.for.002` | 346 | `for (obj = victim->carrying; obj != NULL; obj = obj_next)` |  | pending |
| `effects.fire_effect.return.002` | 352 | `return;` |  | pending |
| `effects.fire_effect.if.005` | 355 | `if (target == TARGET_OBJ)` |  | pending |
| `effects.fire_effect.if.006` | 362 | `if (IS_OBJ_STAT(obj,ITEM_BURN_PROOF)         \|\|  IS_OBJ_STAT(obj,ITEM_NOPURGE) 	\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.fire_effect.or.001` | 363 | `\|\|  IS_OBJ_STAT(obj,ITEM_NOPURGE)` |  | pending |
| `effects.fire_effect.or.002` | 364 | `\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.fire_effect.return.003` | 365 | `return;` |  | pending |
| `effects.fire_effect.if.007` | 369 | `if (chance > 25)` |  | pending |
| `effects.fire_effect.if.008` | 371 | `if (chance > 50)` |  | pending |
| `effects.fire_effect.if.009` | 374 | `if (IS_OBJ_STAT(obj,ITEM_BLESS))` |  | pending |
| `effects.fire_effect.switch.001` | 378 | `switch ( obj->item_type )` |  | pending |
| `effects.fire_effect.default.001` | 380 | `default:` |  | pending |
| `effects.fire_effect.return.004` | 381 | `return;` |  | pending |
| `effects.fire_effect.case.001` | 382 | `case ITEM_CONTAINER:` |  | pending |
| `effects.fire_effect.break.001` | 384 | `break;` |  | pending |
| `effects.fire_effect.case.002` | 385 | `case ITEM_POTION:` |  | pending |
| `effects.fire_effect.break.002` | 388 | `break;` |  | pending |
| `effects.fire_effect.case.003` | 389 | `case ITEM_SCROLL:` |  | pending |
| `effects.fire_effect.break.003` | 392 | `break;` |  | pending |
| `effects.fire_effect.case.004` | 393 | `case ITEM_STAFF:` |  | pending |
| `effects.fire_effect.break.004` | 396 | `break;` |  | pending |
| `effects.fire_effect.case.005` | 397 | `case ITEM_WAND:` |  | pending |
| `effects.fire_effect.break.005` | 399 | `break;` |  | pending |
| `effects.fire_effect.case.006` | 400 | `case ITEM_FOOD:` |  | pending |
| `effects.fire_effect.break.006` | 402 | `break;` |  | pending |
| `effects.fire_effect.case.007` | 403 | `case ITEM_PILL:` |  | pending |
| `effects.fire_effect.break.007` | 405 | `break;` |  | pending |
| `effects.fire_effect.if.010` | 410 | `if (number_percent() > chance)` |  | pending |
| `effects.fire_effect.return.005` | 411 | `return;` |  | pending |
| `effects.fire_effect.if.011` | 413 | `if (obj->carried_by != NULL)` |  | pending |
| `effects.fire_effect.if.012` | 415 | `if (obj->in_room != NULL && obj->in_room->people != NULL)` |  | pending |
| `effects.fire_effect.and.002` | 415 | `&& obj->in_room->people != NULL)` |  | pending |
| `effects.fire_effect.if.013` | 418 | `if (obj->contains)` |  | pending |
| `effects.fire_effect.for.003` | 422 | `for (t_obj = obj->contains; t_obj != NULL; t_obj = n_obj)` |  | pending |
| `effects.fire_effect.if.014` | 426 | `if (obj->in_room != NULL)` |  | pending |
| `effects.fire_effect.if.015` | 428 | `if (obj->carried_by != NULL)` |  | pending |
| `effects.fire_effect.continue.001` | 433 | `continue;` |  | pending |
| `effects.fire_effect.return.006` | 440 | `return;` |  | pending |

## poison_effect

[Source line 444](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/effects.c:444); ends at line 531. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- poison_effect: `src/effects.c:454` (lexical_call_candidate).
- poison_effect: `src/effects.c:487` (lexical_call_candidate).
- spell_gas_breath: `src/magic.c:4623` (lexical_call_candidate).
- spell_gas_breath: `src/magic.c:4636` (lexical_call_candidate).
- spell_gas_breath: `src/magic.c:4641` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2164` (declaration_or_dispatch_reference).

Dependencies: `poison_effect`, `saves_spell`, `send_to_char`, `act`, `affect_join`, `IS_OBJ_STAT`, `number_range`, `URANGE`, `number_percent`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `effects.poison_effect.if.001` | 446 | `if (target == TARGET_ROOM)` |  | pending |
| `effects.poison_effect.for.001` | 451 | `for (obj = room->contents; obj != NULL; obj = obj_next)` |  | pending |
| `effects.poison_effect.return.001` | 456 | `return;` |  | pending |
| `effects.poison_effect.if.002` | 459 | `if (target == TARGET_CHAR)` |  | pending |
| `effects.poison_effect.if.003` | 465 | `if (!saves_spell(level / 4 + dam / 20,victim,DAM_POISON))` |  | pending |
| `effects.poison_effect.for.002` | 484 | `for (obj = victim->carrying; obj != NULL; obj = obj_next)` |  | pending |
| `effects.poison_effect.return.002` | 489 | `return;` |  | pending |
| `effects.poison_effect.if.004` | 492 | `if (target == TARGET_OBJ)` |  | pending |
| `effects.poison_effect.if.005` | 498 | `if (IS_OBJ_STAT(obj,ITEM_BURN_PROOF)   	\|\|  IS_OBJ_STAT(obj,ITEM_BLESS) 	\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.poison_effect.or.001` | 499 | `\|\|  IS_OBJ_STAT(obj,ITEM_BLESS)` |  | pending |
| `effects.poison_effect.or.002` | 500 | `\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.poison_effect.return.003` | 501 | `return;` |  | pending |
| `effects.poison_effect.if.006` | 504 | `if (chance > 25)` |  | pending |
| `effects.poison_effect.if.007` | 506 | `if (chance > 50)` |  | pending |
| `effects.poison_effect.switch.001` | 511 | `switch (obj->item_type)` |  | pending |
| `effects.poison_effect.default.001` | 513 | `default:` |  | pending |
| `effects.poison_effect.return.004` | 514 | `return;` |  | pending |
| `effects.poison_effect.case.001` | 515 | `case ITEM_FOOD:` |  | pending |
| `effects.poison_effect.break.001` | 516 | `break;` |  | pending |
| `effects.poison_effect.case.002` | 517 | `case ITEM_DRINK_CON:` |  | pending |
| `effects.poison_effect.if.008` | 518 | `if (obj->value[0] == obj->value[1])` |  | pending |
| `effects.poison_effect.return.005` | 519 | `return;` |  | pending |
| `effects.poison_effect.break.002` | 520 | `break;` |  | pending |
| `effects.poison_effect.if.009` | 525 | `if (number_percent() > chance)` |  | pending |
| `effects.poison_effect.return.006` | 526 | `return;` |  | pending |
| `effects.poison_effect.return.007` | 529 | `return;` |  | pending |

## shock_effect

[Source line 534](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/effects.c:534); ends at line 620. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- shock_effect: `src/effects.c:544` (lexical_call_candidate).
- shock_effect: `src/effects.c:565` (lexical_call_candidate).
- one_hit: `src/fight.c:663` (lexical_call_candidate).
- spell_lightning_breath: `src/magic.c:4664` (lexical_call_candidate).
- spell_lightning_breath: `src/magic.c:4669` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2165` (declaration_or_dispatch_reference).

Dependencies: `shock_effect`, `saves_spell`, `send_to_char`, `DAZE_STATE`, `UMAX`, `IS_OBJ_STAT`, `number_range`, `URANGE`, `number_percent`, `act`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `effects.shock_effect.if.001` | 536 | `if (target == TARGET_ROOM)` |  | pending |
| `effects.shock_effect.for.001` | 541 | `for (obj = room->contents; obj != NULL; obj = obj_next)` |  | pending |
| `effects.shock_effect.return.001` | 546 | `return;` |  | pending |
| `effects.shock_effect.if.002` | 549 | `if (target == TARGET_CHAR)` |  | pending |
| `effects.shock_effect.if.003` | 555 | `if (!saves_spell(level/4 + dam/20,victim,DAM_LIGHTNING))` |  | pending |
| `effects.shock_effect.for.002` | 562 | `for (obj = victim->carrying; obj != NULL; obj = obj_next)` |  | pending |
| `effects.shock_effect.return.002` | 567 | `return;` |  | pending |
| `effects.shock_effect.if.004` | 570 | `if (target == TARGET_OBJ)` |  | pending |
| `effects.shock_effect.if.005` | 576 | `if (IS_OBJ_STAT(obj,ITEM_BURN_PROOF) 	\|\|  IS_OBJ_STAT(obj,ITEM_NOPURGE) 	\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.shock_effect.or.001` | 577 | `\|\|  IS_OBJ_STAT(obj,ITEM_NOPURGE)` |  | pending |
| `effects.shock_effect.or.002` | 578 | `\|\|  number_range(0,4) == 0)` |  | pending |
| `effects.shock_effect.return.003` | 579 | `return;` |  | pending |
| `effects.shock_effect.if.006` | 583 | `if (chance > 25)` |  | pending |
| `effects.shock_effect.if.007` | 585 | `if (chance > 50)` |  | pending |
| `effects.shock_effect.if.008` | 588 | `if (IS_OBJ_STAT(obj,ITEM_BLESS))` |  | pending |
| `effects.shock_effect.switch.001` | 593 | `switch(obj->item_type)` |  | pending |
| `effects.shock_effect.default.001` | 595 | `default:` |  | pending |
| `effects.shock_effect.return.004` | 596 | `return;` |  | pending |
| `effects.shock_effect.case.001` | 597 | `case ITEM_WAND:` |  | pending |
| `effects.shock_effect.case.002` | 598 | `case ITEM_STAFF:` |  | pending |
| `effects.shock_effect.break.001` | 601 | `break;` |  | pending |
| `effects.shock_effect.case.003` | 602 | `case ITEM_JEWELRY:` |  | pending |
| `effects.shock_effect.if.009` | 609 | `if (number_percent() > chance)` |  | pending |
| `effects.shock_effect.return.005` | 610 | `return;` |  | pending |
| `effects.shock_effect.if.010` | 612 | `if (obj->carried_by != NULL)` |  | pending |
| `effects.shock_effect.if.011` | 614 | `if (obj->in_room != NULL && obj->in_room->people != NULL)` |  | pending |
| `effects.shock_effect.and.001` | 614 | `&& obj->in_room->people != NULL)` |  | pending |
| `effects.shock_effect.return.006` | 618 | `return;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#endif` — pending configuration/reachability review.
- Line 33: `#include <stdio.h>` — pending configuration/reachability review.
- Line 34: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 35: `#include <string.h>` — pending configuration/reachability review.
- Line 36: `#include <time.h>` — pending configuration/reachability review.
- Line 37: `#include "merc.h"` — pending configuration/reachability review.
- Line 38: `#include "recycle.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


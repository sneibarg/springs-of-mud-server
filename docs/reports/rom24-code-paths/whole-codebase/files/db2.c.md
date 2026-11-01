# src/db2.c

Role: translation_unit. Disposition: **pending**. SHA-256: `c593c857ecce36a1d5fd9af2acc49135530413c38982b1059249a3bc4ee194df`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## load_socials

[Source line 50](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db2.c:50); ends at line 129. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:357` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:221` (declaration_or_dispatch_reference).

Dependencies: `fread_word`, `strcmp`, `strcpy`, `fread_to_eol`, `fread_string_eol`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db2.load_socials.for.001` | 52 | `for ( ; ; )` |  | pending |
| `db2.load_socials.if.001` | 67 | `if (!strcmp(temp,"#0"))` |  | pending |
| `db2.load_socials.return.001` | 68 | `return;` |  | pending |
| `db2.load_socials.if.002` | 73 | `if (!strcmp(temp,"$"))` |  | pending |
| `db2.load_socials.if.003` | 75 | `if (!strcmp(temp,"#"))` |  | pending |
| `db2.load_socials.continue.001` | 79 | `continue;` |  | pending |
| `db2.load_socials.if.004` | 85 | `if (!strcmp(temp,"$"))` |  | pending |
| `db2.load_socials.if.005` | 102 | `if (!strcmp(temp,"$"))` |  | pending |
| `db2.load_socials.if.006` | 104 | `if (!strcmp(temp,"#"))` |  | pending |
| `db2.load_socials.continue.002` | 108 | `continue;` |  | pending |
| `db2.load_socials.if.007` | 114 | `if (!strcmp(temp,"$"))` |  | pending |
| `db2.load_socials.if.008` | 116 | `if (!strcmp(temp,"#"))` |  | pending |
| `db2.load_socials.continue.003` | 120 | `continue;` |  | pending |
| `db2.load_socials.return.002` | 128 | `return;` |  | pending |

## load_mobiles

[Source line 139](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db2.c:139); ends at line 294. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:351` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:215` (declaration_or_dispatch_reference).

Dependencies: `fread_letter`, `bug`, `exit`, `fread_number`, `get_mob_index`, `alloc_perm`, `fread_string`, `race_lookup`, `UPPER`, `fread_flag`, `attack_lookup`, `fread_word`, `position_lookup`, `sex_lookup`, `size_lookup`, `str_dup`, `str_prefix`, `REMOVE_BIT`, `ungetc`, `URANGE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db2.load_mobiles.for.001` | 143 | `for ( ; ; )` |  | pending |
| `db2.load_mobiles.if.001` | 150 | `if ( letter != '#' )` |  | pending |
| `db2.load_mobiles.if.002` | 157 | `if ( vnum == 0 )` |  | pending |
| `db2.load_mobiles.break.001` | 158 | `break;` |  | pending |
| `db2.load_mobiles.if.003` | 161 | `if ( get_mob_index( vnum ) != NULL )` |  | pending |
| `db2.load_mobiles.for.002` | 245 | `for ( ; ; )` |  | pending |
| `db2.load_mobiles.if.004` | 249 | `if (letter == 'F')` |  | pending |
| `db2.load_mobiles.if.005` | 257 | `if (!str_prefix(word,"act"))` |  | pending |
| `db2.load_mobiles.if.006` | 259 | `if (!str_prefix(word,"aff"))` |  | pending |
| `db2.load_mobiles.if.007` | 261 | `if (!str_prefix(word,"off"))` |  | pending |
| `db2.load_mobiles.if.008` | 263 | `if (!str_prefix(word,"imm"))` |  | pending |
| `db2.load_mobiles.if.009` | 265 | `if (!str_prefix(word,"res"))` |  | pending |
| `db2.load_mobiles.if.010` | 267 | `if (!str_prefix(word,"vul"))` |  | pending |
| `db2.load_mobiles.if.011` | 269 | `if (!str_prefix(word,"for"))` |  | pending |
| `db2.load_mobiles.if.012` | 271 | `if (!str_prefix(word,"par"))` |  | pending |
| `db2.load_mobiles.break.002` | 282 | `break;` |  | pending |
| `db2.load_mobiles.return.001` | 293 | `return;` |  | pending |

## load_objects

[Source line 299](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db2.c:299); ends at line 492. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:353` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:217` (declaration_or_dispatch_reference).

Dependencies: `fread_letter`, `bug`, `exit`, `fread_number`, `get_obj_index`, `alloc_perm`, `fread_string`, `item_lookup`, `fread_word`, `fread_flag`, `weapon_type`, `attack_lookup`, `liq_lookup`, `skill_lookup`, `case`, `ungetc`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db2.load_objects.for.001` | 303 | `for ( ; ; )` |  | pending |
| `db2.load_objects.if.001` | 310 | `if ( letter != '#' )` |  | pending |
| `db2.load_objects.if.002` | 317 | `if ( vnum == 0 )` |  | pending |
| `db2.load_objects.break.001` | 318 | `break;` |  | pending |
| `db2.load_objects.if.003` | 321 | `if ( get_obj_index( vnum ) != NULL )` |  | pending |
| `db2.load_objects.switch.001` | 341 | `switch(pObjIndex->item_type)` |  | pending |
| `db2.load_objects.case.001` | 343 | `case ITEM_WEAPON:` |  | pending |
| `db2.load_objects.break.002` | 349 | `break;` |  | pending |
| `db2.load_objects.case.002` | 350 | `case ITEM_CONTAINER:` |  | pending |
| `db2.load_objects.break.003` | 356 | `break;` |  | pending |
| `db2.load_objects.case.003` | 357 | `case ITEM_DRINK_CON:` |  | pending |
| `db2.load_objects.case.004` | 358 | `case ITEM_FOUNTAIN:` |  | pending |
| `db2.load_objects.break.004` | 364 | `break;` |  | pending |
| `db2.load_objects.case.005` | 365 | `case ITEM_WAND:` |  | pending |
| `db2.load_objects.case.006` | 366 | `case ITEM_STAFF:` |  | pending |
| `db2.load_objects.break.005` | 372 | `break;` |  | pending |
| `db2.load_objects.case.007` | 373 | `case ITEM_POTION:` |  | pending |
| `db2.load_objects.case.008` | 374 | `case ITEM_PILL:` |  | pending |
| `db2.load_objects.case.009` | 375 | `case ITEM_SCROLL:` |  | pending |
| `db2.load_objects.break.006` | 381 | `break;` |  | pending |
| `db2.load_objects.default.001` | 382 | `default:` |  | pending |
| `db2.load_objects.break.007` | 388 | `break;` |  | pending |
| `db2.load_objects.switch.002` | 396 | `switch (letter)` |  | pending |
| `db2.load_objects.case.010` | 398 | `case ('P') :		pObjIndex->condition = 100;` |  | pending |
| `db2.load_objects.break.008` | 398 | `break;` |  | pending |
| `db2.load_objects.case.011` | 399 | `case ('G') :		pObjIndex->condition =  90;` |  | pending |
| `db2.load_objects.break.009` | 399 | `break;` |  | pending |
| `db2.load_objects.case.012` | 400 | `case ('A') :		pObjIndex->condition =  75;` |  | pending |
| `db2.load_objects.break.010` | 400 | `break;` |  | pending |
| `db2.load_objects.case.013` | 401 | `case ('W') :		pObjIndex->condition =  50;` |  | pending |
| `db2.load_objects.break.011` | 401 | `break;` |  | pending |
| `db2.load_objects.case.014` | 402 | `case ('D') :		pObjIndex->condition =  25;` |  | pending |
| `db2.load_objects.break.012` | 402 | `break;` |  | pending |
| `db2.load_objects.case.015` | 403 | `case ('B') :		pObjIndex->condition =  10;` |  | pending |
| `db2.load_objects.break.013` | 403 | `break;` |  | pending |
| `db2.load_objects.case.016` | 404 | `case ('R') :		pObjIndex->condition =   0;` |  | pending |
| `db2.load_objects.break.014` | 404 | `break;` |  | pending |
| `db2.load_objects.default.002` | 405 | `default:			pObjIndex->condition = 100;` |  | pending |
| `db2.load_objects.break.015` | 405 | `break;` |  | pending |
| `db2.load_objects.for.002` | 408 | `for ( ; ; )` |  | pending |
| `db2.load_objects.if.004` | 414 | `if ( letter == 'A' )` |  | pending |
| `db2.load_objects.if.005` | 431 | `if (letter == 'F')` |  | pending |
| `db2.load_objects.switch.003` | 437 | `switch (letter)` |  | pending |
| `db2.load_objects.case.017` | 439 | `case 'A':` |  | pending |
| `db2.load_objects.break.016` | 441 | `break;` |  | pending |
| `db2.load_objects.case.018` | 442 | `case 'I':` |  | pending |
| `db2.load_objects.break.017` | 444 | `break;` |  | pending |
| `db2.load_objects.case.019` | 445 | `case 'R':` |  | pending |
| `db2.load_objects.break.018` | 447 | `break;` |  | pending |
| `db2.load_objects.case.020` | 448 | `case 'V':` |  | pending |
| `db2.load_objects.break.019` | 450 | `break;` |  | pending |
| `db2.load_objects.default.003` | 451 | `default:` |  | pending |
| `db2.load_objects.if.006` | 466 | `if ( letter == 'E' )` |  | pending |
| `db2.load_objects.break.020` | 481 | `break;` |  | pending |
| `db2.load_objects.return.001` | 491 | `return;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#include <stdio.h>` — pending configuration/reachability review.
- Line 29: `#include <string.h>` — pending configuration/reachability review.
- Line 30: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 31: `#include <ctype.h>` — pending configuration/reachability review.
- Line 32: `#include <time.h>` — pending configuration/reachability review.
- Line 33: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 34: `#include <types.h>` — pending configuration/reachability review.
- Line 35: `#else` — pending configuration/reachability review.
- Line 36: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 37: `#include <sys/time.h>` — pending configuration/reachability review.
- Line 38: `#endif` — pending configuration/reachability review.
- Line 40: `#include "merc.h"` — pending configuration/reachability review.
- Line 41: `#include "db.h"` — pending configuration/reachability review.
- Line 42: `#include "lookup.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


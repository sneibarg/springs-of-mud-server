# src/healer.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `742b9baad4a772d0fe918a26af1f85111e17720cab493eeee5a06c440cb5eb21`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## do_heal

[Source line 41](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/healer.c:41); ends at line 196. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:214` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:145` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `send_to_char`, `one_argument`, `act`, `str_prefix`, `skill_lookup`, `WAIT_STATE`, `deduct_cost`, `dice`, `UMIN`, `spell`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `healer.do_heal.for.001` | 50 | `for ( mob = ch->in_room->people; mob; mob = mob->next_in_room )` |  | pending |
| `healer.do_heal.if.001` | 52 | `if ( IS_NPC(mob) && IS_SET(mob->act, ACT_IS_HEALER) )` |  | pending |
| `healer.do_heal.and.001` | 52 | `&& IS_SET(mob->act, ACT_IS_HEALER) )` |  | pending |
| `healer.do_heal.break.001` | 53 | `break;` |  | pending |
| `healer.do_heal.if.002` | 56 | `if ( mob == NULL )` |  | pending |
| `healer.do_heal.return.001` | 59 | `return;` |  | pending |
| `healer.do_heal.if.003` | 64 | `if (arg[0] == '\0')` |  | pending |
| `healer.do_heal.return.002` | 79 | `return;` |  | pending |
| `healer.do_heal.if.004` | 82 | `if (!str_prefix(arg,"light"))` |  | pending |
| `healer.do_heal.if.005` | 90 | `if (!str_prefix(arg,"serious"))` |  | pending |
| `healer.do_heal.if.006` | 98 | `if (!str_prefix(arg,"critical"))` |  | pending |
| `healer.do_heal.if.007` | 106 | `if (!str_prefix(arg,"heal"))` |  | pending |
| `healer.do_heal.if.008` | 114 | `if (!str_prefix(arg,"blindness"))` |  | pending |
| `healer.do_heal.if.009` | 122 | `if (!str_prefix(arg,"disease"))` |  | pending |
| `healer.do_heal.if.010` | 130 | `if (!str_prefix(arg,"poison"))` |  | pending |
| `healer.do_heal.if.011` | 138 | `if (!str_prefix(arg,"uncurse") \|\| !str_prefix(arg,"curse"))` |  | pending |
| `healer.do_heal.or.001` | 138 | `\|\| !str_prefix(arg,"curse"))` |  | pending |
| `healer.do_heal.if.012` | 146 | `if (!str_prefix(arg,"mana") \|\| !str_prefix(arg,"energize"))` |  | pending |
| `healer.do_heal.or.002` | 146 | `\|\| !str_prefix(arg,"energize"))` |  | pending |
| `healer.do_heal.if.013` | 155 | `if (!str_prefix(arg,"refresh") \|\| !str_prefix(arg,"moves"))` |  | pending |
| `healer.do_heal.or.003` | 155 | `\|\| !str_prefix(arg,"moves"))` |  | pending |
| `healer.do_heal.return.003` | 167 | `return;` |  | pending |
| `healer.do_heal.if.014` | 170 | `if (cost > (ch->gold * 100 + ch->silver))` |  | pending |
| `healer.do_heal.return.004` | 174 | `return;` |  | pending |
| `healer.do_heal.if.015` | 184 | `if (spell == NULL)` |  | pending |
| `healer.do_heal.return.005` | 189 | `return;` |  | pending |
| `healer.do_heal.if.016` | 192 | `if (sn == -1)` |  | pending |
| `healer.do_heal.return.006` | 193 | `return;` |  | pending |
| `healer.do_heal.no-healer-before-argument-parsing.path` | 56 | `no healer before argument parsing` | healer.do_heal.no-healer-before-argument-parsing | specified |
| `healer.do_heal.price-menu.path` | 64 | `price menu` | healer.do_heal.price-menu | specified |
| `healer.do_heal.unknown-service.path` | 165 | `unknown service` | healer.do_heal.unknown-service | specified |
| `healer.do_heal.light-one-silver-short.path` | 170 | `light one silver short` | healer.do_heal.light-one-silver-short | specified |
| `healer.do_heal.light-exact-price.path` | 170 | `light exact price` | healer.do_heal.light-exact-price | specified |
| `healer.do_heal.serious-one-silver-short.path` | 170 | `serious one silver short` | healer.do_heal.serious-one-silver-short | specified |
| `healer.do_heal.serious-exact-price.path` | 170 | `serious exact price` | healer.do_heal.serious-exact-price | specified |
| `healer.do_heal.critical-one-silver-short.path` | 170 | `critical one silver short` | healer.do_heal.critical-one-silver-short | specified |
| `healer.do_heal.critical-exact-price.path` | 170 | `critical exact price` | healer.do_heal.critical-exact-price | specified |
| `healer.do_heal.heal-one-silver-short.path` | 170 | `heal one silver short` | healer.do_heal.heal-one-silver-short | specified |
| `healer.do_heal.heal-exact-price.path` | 170 | `heal exact price` | healer.do_heal.heal-exact-price | specified |
| `healer.do_heal.blindness-one-silver-short.path` | 170 | `blindness one silver short` | healer.do_heal.blindness-one-silver-short | specified |
| `healer.do_heal.blindness-exact-price.path` | 170 | `blindness exact price` | healer.do_heal.blindness-exact-price | specified |
| `healer.do_heal.disease-one-silver-short.path` | 170 | `disease one silver short` | healer.do_heal.disease-one-silver-short | specified |
| `healer.do_heal.disease-exact-price.path` | 170 | `disease exact price` | healer.do_heal.disease-exact-price | specified |
| `healer.do_heal.poison-one-silver-short.path` | 170 | `poison one silver short` | healer.do_heal.poison-one-silver-short | specified |
| `healer.do_heal.poison-exact-price.path` | 170 | `poison exact price` | healer.do_heal.poison-exact-price | specified |
| `healer.do_heal.uncurse-one-silver-short.path` | 170 | `uncurse one silver short` | healer.do_heal.uncurse-one-silver-short | specified |
| `healer.do_heal.uncurse-exact-price.path` | 170 | `uncurse exact price` | healer.do_heal.uncurse-exact-price | specified |
| `healer.do_heal.curse-one-silver-short.path` | 170 | `curse one silver short` | healer.do_heal.curse-one-silver-short | specified |
| `healer.do_heal.curse-exact-price.path` | 170 | `curse exact price` | healer.do_heal.curse-exact-price | specified |
| `healer.do_heal.refresh-one-silver-short.path` | 170 | `refresh one silver short` | healer.do_heal.refresh-one-silver-short | specified |
| `healer.do_heal.refresh-exact-price.path` | 170 | `refresh exact price` | healer.do_heal.refresh-exact-price | specified |
| `healer.do_heal.moves-one-silver-short.path` | 170 | `moves one silver short` | healer.do_heal.moves-one-silver-short | specified |
| `healer.do_heal.moves-exact-price.path` | 170 | `moves exact price` | healer.do_heal.moves-exact-price | specified |
| `healer.do_heal.mana-uncapped.path` | 184 | `mana uncapped` | healer.do_heal.mana-uncapped | specified |
| `healer.do_heal.mana-capped.path` | 184 | `mana capped` | healer.do_heal.mana-capped | specified |
| `healer.do_heal.mana-existing-wait-preserved.path` | 184 | `mana existing wait preserved` | healer.do_heal.mana-existing-wait-preserved | specified |
| `healer.do_heal.missing-skill-index-still-charges.path` | 192 | `missing skill index still charges` | healer.do_heal.missing-skill-index-still-charges | specified |

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
- Line 39: `#include "magic.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


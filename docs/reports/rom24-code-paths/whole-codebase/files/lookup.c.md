# src/lookup.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `80dcc2ee12622678d6efab9bff930aa5666085b496b81a3aac4aa6d364363ade`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## flag_lookup

[Source line 38](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/lookup.c:38); ends at line 50. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_flag: `src/flags.c:205` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/flags.c:41` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `lookup.flag_lookup.for.001` | 42 | `for (flag = 0; flag_table[flag].name != NULL; flag++)` |  | pending |
| `lookup.flag_lookup.if.001` | 44 | `if (LOWER(name[0]) == LOWER(flag_table[flag].name[0]) 	&&  !str_prefix(name,flag_table[flag].name))` |  | pending |
| `lookup.flag_lookup.and.001` | 45 | `&&  !str_prefix(name,flag_table[flag].name))` |  | pending |
| `lookup.flag_lookup.return.001` | 46 | `return flag_table[flag].bit;` |  | pending |
| `lookup.flag_lookup.return.002` | 49 | `return 0;` |  | pending |
| `lookup.flag_lookup.empty-table.path` | 44 | `empty table` | lookup.flag_lookup.empty-table | specified |
| `lookup.flag_lookup.first-of-multiple-prefixes.path` | 44 | `first of multiple prefixes` | lookup.flag_lookup.first-of-multiple-prefixes | specified |
| `lookup.flag_lookup.case-insensitive.path` | 44 | `case insensitive` | lookup.flag_lookup.case-insensitive | specified |
| `lookup.flag_lookup.nonsettable-still-found.path` | 44 | `nonsettable still found` | lookup.flag_lookup.nonsettable-still-found | specified |
| `lookup.flag_lookup.skip-nonmatch.path` | 44 | `skip nonmatch` | lookup.flag_lookup.skip-nonmatch | specified |
| `lookup.flag_lookup.unknown.path` | 44 | `unknown` | lookup.flag_lookup.unknown | specified |
| `lookup.flag_lookup.empty-name-does-not-match-nonempty.path` | 44 | `empty name does not match nonempty` | lookup.flag_lookup.empty-name-does-not-match-nonempty | specified |

## clan_lookup

[Source line 52](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/lookup.c:52); ends at line 64. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_who: `src/act_info.c:1972` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:206` (lexical_call_candidate).
- load_rooms: `src/db.c:939` (lexical_call_candidate).
- fread_char: `src/save.c:887` (lexical_call_candidate).
- fread_pet: `src/save.c:1257` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/lookup.h:29` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `lookup.clan_lookup.for.001` | 56 | `for (clan = 0; clan < MAX_CLAN; clan++)` |  | pending |
| `lookup.clan_lookup.if.001` | 58 | `if (LOWER(name[0]) == LOWER(clan_table[clan].name[0]) 	&&  !str_prefix(name,clan_table[clan].name))` |  | pending |
| `lookup.clan_lookup.and.001` | 59 | `&&  !str_prefix(name,clan_table[clan].name))` |  | pending |
| `lookup.clan_lookup.return.001` | 60 | `return clan;` |  | pending |
| `lookup.clan_lookup.return.002` | 63 | `return 0;` |  | pending |
| `lookup.clan_lookup.loner.path` | 58 | `loner` | lookup.clan_lookup.loner | specified |
| `lookup.clan_lookup.rom.path` | 58 | `rom` | lookup.clan_lookup.rom | specified |
| `lookup.clan_lookup.empty-matches-entry-zero.path` | 58 | `empty matches entry zero` | lookup.clan_lookup.empty-matches-entry-zero | specified |
| `lookup.clan_lookup.unknown-indistinguishable-from-zero.path` | 58 | `unknown indistinguishable from zero` | lookup.clan_lookup.unknown-indistinguishable-from-zero | specified |

## position_lookup

[Source line 66](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/lookup.c:66); ends at line 78. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- load_mobiles: `src/db2.c:231` (lexical_call_candidate).
- load_mobiles: `src/db2.c:232` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/lookup.h:30` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `lookup.position_lookup.for.001` | 70 | `for (pos = 0; position_table[pos].name != NULL; pos++)` |  | pending |
| `lookup.position_lookup.if.001` | 72 | `if (LOWER(name[0]) == LOWER(position_table[pos].name[0]) 	&&  !str_prefix(name,position_table[pos].name))` |  | pending |
| `lookup.position_lookup.and.001` | 73 | `&&  !str_prefix(name,position_table[pos].name))` |  | pending |
| `lookup.position_lookup.return.001` | 74 | `return pos;` |  | pending |
| `lookup.position_lookup.return.002` | 77 | `return -1;` |  | pending |
| `lookup.position_lookup.standing-full.path` | 72 | `standing full` | lookup.position_lookup.standing-full | specified |
| `lookup.position_lookup.ambiguous-s-first-stunned.path` | 72 | `ambiguous s first stunned` | lookup.position_lookup.ambiguous-s-first-stunned | specified |
| `lookup.position_lookup.case-insensitive.path` | 72 | `case insensitive` | lookup.position_lookup.case-insensitive | specified |
| `lookup.position_lookup.empty.path` | 72 | `empty` | lookup.position_lookup.empty | specified |
| `lookup.position_lookup.missing.path` | 72 | `missing` | lookup.position_lookup.missing | specified |
| `lookup.position_lookup.longer.path` | 72 | `longer` | lookup.position_lookup.longer | specified |

## sex_lookup

[Source line 80](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/lookup.c:80); ends at line 92. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- load_mobiles: `src/db2.c:233` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/lookup.h:31` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `lookup.sex_lookup.for.001` | 84 | `for (sex = 0; sex_table[sex].name != NULL; sex++)` |  | pending |
| `lookup.sex_lookup.if.001` | 86 | `if (LOWER(name[0]) == LOWER(sex_table[sex].name[0]) 	&&  !str_prefix(name,sex_table[sex].name))` |  | pending |
| `lookup.sex_lookup.and.001` | 87 | `&&  !str_prefix(name,sex_table[sex].name))` |  | pending |
| `lookup.sex_lookup.return.001` | 88 | `return sex;` |  | pending |
| `lookup.sex_lookup.return.002` | 91 | `return -1;` |  | pending |
| `lookup.sex_lookup.none.path` | 86 | `none` | lookup.sex_lookup.none | specified |
| `lookup.sex_lookup.male.path` | 86 | `male` | lookup.sex_lookup.male | specified |
| `lookup.sex_lookup.female.path` | 86 | `female` | lookup.sex_lookup.female | specified |
| `lookup.sex_lookup.last-entry.path` | 86 | `last entry` | lookup.sex_lookup.last-entry | specified |
| `lookup.sex_lookup.empty.path` | 86 | `empty` | lookup.sex_lookup.empty | specified |
| `lookup.sex_lookup.missing.path` | 86 | `missing` | lookup.sex_lookup.missing | specified |

## size_lookup

[Source line 94](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/lookup.c:94); ends at line 106. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- load_mobiles: `src/db2.c:242` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/lookup.h:32` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `lookup.size_lookup.for.001` | 98 | `for ( size = 0; size_table[size].name != NULL; size++)` |  | pending |
| `lookup.size_lookup.if.001` | 100 | `if (LOWER(name[0]) == LOWER(size_table[size].name[0])         &&  !str_prefix( name,size_table[size].name))` |  | pending |
| `lookup.size_lookup.and.001` | 101 | `&&  !str_prefix( name,size_table[size].name))` |  | pending |
| `lookup.size_lookup.return.001` | 102 | `return size;` |  | pending |
| `lookup.size_lookup.return.002` | 105 | `return -1;` |  | pending |
| `lookup.size_lookup.tiny.path` | 100 | `tiny` | lookup.size_lookup.tiny | specified |
| `lookup.size_lookup.small.path` | 100 | `small` | lookup.size_lookup.small | specified |
| `lookup.size_lookup.medium.path` | 100 | `medium` | lookup.size_lookup.medium | specified |
| `lookup.size_lookup.large.path` | 100 | `large` | lookup.size_lookup.large | specified |
| `lookup.size_lookup.huge.path` | 100 | `huge` | lookup.size_lookup.huge | specified |
| `lookup.size_lookup.last-entry.path` | 100 | `last entry` | lookup.size_lookup.last-entry | specified |
| `lookup.size_lookup.empty.path` | 100 | `empty` | lookup.size_lookup.empty | specified |
| `lookup.size_lookup.missing.path` | 100 | `missing` | lookup.size_lookup.missing | specified |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#endif` — pending configuration/reachability review.
- Line 33: `#include <stdio.h>` — pending configuration/reachability review.
- Line 34: `#include <time.h>` — pending configuration/reachability review.
- Line 35: `#include "merc.h"` — pending configuration/reachability review.
- Line 36: `#include "tables.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


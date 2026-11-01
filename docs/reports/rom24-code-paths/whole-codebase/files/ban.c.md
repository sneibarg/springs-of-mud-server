# src/ban.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `7a9610d96ea75d1415f1042871671ce392fd9dd4438d9cd82de7d271986429a4`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## save_bans

[Source line 44](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:44); ends at line 70. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- ban_site: `src/ban.c:250` (lexical_call_candidate).
- do_allow: `src/ban.c:300` (lexical_call_candidate).

Dependencies: `fclose`, `fopen`, `perror`, `IS_SET`, `fprintf`, `print_flags`, `unlink`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.save_bans.if.001` | 51 | `if ( ( fp = fopen( BAN_FILE, "w" ) ) == NULL )` |  | pending |
| `ban.save_bans.for.001` | 56 | `for (pban = ban_list; pban != NULL; pban = pban->next)` |  | pending |
| `ban.save_bans.if.002` | 58 | `if (IS_SET(pban->ban_flags,BAN_PERMANENT))` |  | pending |
| `ban.save_bans.if.003` | 68 | `if (!found)` |  | pending |

## load_bans

[Source line 72](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:72); ends at line 103. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:384` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:224` (declaration_or_dispatch_reference).

Dependencies: `fopen`, `feof`, `fclose`, `new_ban`, `str_dup`, `fread_word`, `fread_number`, `fread_flag`, `fread_to_eol`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.load_bans.if.001` | 77 | `if ( ( fp = fopen( BAN_FILE, "r" ) ) == NULL )` |  | pending |
| `ban.load_bans.return.001` | 78 | `return;` |  | pending |
| `ban.load_bans.for.001` | 81 | `for ( ; ; )` |  | pending |
| `ban.load_bans.if.002` | 84 | `if ( feof(fp) )` |  | pending |
| `ban.load_bans.return.002` | 87 | `return;` |  | pending |
| `ban.load_bans.if.003` | 97 | `if (ban_list == NULL)` |  | pending |

## check_ban

[Source line 105](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:105); ends at line 133. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- init_descriptor: `src/comm.c:931` (lexical_call_candidate).
- nanny: `src/comm.c:1593` (lexical_call_candidate).
- nanny: `src/comm.c:1632` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2099` (declaration_or_dispatch_reference).

Dependencies: `strcpy`, `capitalize`, `LOWER`, `IS_SET`, `strstr`, `str_suffix`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.check_ban.for.001` | 113 | `for ( pban = ban_list; pban != NULL; pban = pban->next )` |  | pending |
| `ban.check_ban.if.001` | 115 | `if(!IS_SET(pban->ban_flags,type))` |  | pending |
| `ban.check_ban.continue.001` | 116 | `continue;` |  | pending |
| `ban.check_ban.if.002` | 118 | `if (IS_SET(pban->ban_flags,BAN_PREFIX)  	&&  IS_SET(pban->ban_flags,BAN_SUFFIX)   	&&  strstr(pban->name,host) != NULL)` |  | pending |
| `ban.check_ban.and.001` | 119 | `&&  IS_SET(pban->ban_flags,BAN_SUFFIX)` |  | pending |
| `ban.check_ban.and.002` | 120 | `&&  strstr(pban->name,host) != NULL)` |  | pending |
| `ban.check_ban.return.001` | 121 | `return TRUE;` |  | pending |
| `ban.check_ban.if.003` | 123 | `if (IS_SET(pban->ban_flags,BAN_PREFIX) 	&&  !str_suffix(pban->name,host))` |  | pending |
| `ban.check_ban.and.003` | 124 | `&&  !str_suffix(pban->name,host))` |  | pending |
| `ban.check_ban.return.002` | 125 | `return TRUE;` |  | pending |
| `ban.check_ban.if.004` | 127 | `if (IS_SET(pban->ban_flags,BAN_SUFFIX) 	&&  !str_prefix(pban->name,host))` |  | pending |
| `ban.check_ban.and.004` | 128 | `&&  !str_prefix(pban->name,host))` |  | pending |
| `ban.check_ban.return.003` | 129 | `return TRUE;` |  | pending |
| `ban.check_ban.return.004` | 132 | `return FALSE;` |  | pending |
| `ban.check_ban.empty-list.path` | 110 | `empty list` | ban.check_ban.empty-list | specified |
| `ban.check_ban.type-not-set.path` | 110 | `type not set` | ban.check_ban.type-not-set | specified |
| `ban.check_ban.exact-without-prefix-suffix-does-not-match.path` | 110 | `exact without prefix suffix does not match` | ban.check_ban.exact-without-prefix-suffix-does-not-match | specified |
| `ban.check_ban.prefix-flag-tests-host-suffix.path` | 110 | `prefix flag tests host suffix` | ban.check_ban.prefix-flag-tests-host-suffix | specified |
| `ban.check_ban.suffix-flag-tests-host-prefix.path` | 110 | `suffix flag tests host prefix` | ban.check_ban.suffix-flag-tests-host-prefix | specified |
| `ban.check_ban.both-flags-host-contained-in-pattern.path` | 110 | `both flags host contained in pattern` | ban.check_ban.both-flags-host-contained-in-pattern | specified |
| `ban.check_ban.both-flags-do-not-match-interior-pattern-in-host.path` | 110 | `both flags do not match interior pattern in host` | ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.later-entry-matches.path` | 110 | `later entry matches` | ban.check_ban.later-entry-matches | specified |

## ban_site

[Source line 136](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:136); ends at line 254. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_ban: `src/ban.c:258` (lexical_call_candidate).
- do_permban: `src/ban.c:263` (lexical_call_candidate).

Dependencies: `one_argument`, `send_to_char`, `new_buf`, `add_buf`, `sprintf`, `IS_SET`, `page_to_char`, `buf_string`, `free_buf`, `str_prefix`, `strlen`, `str_cmp`, `get_trust`, `free_ban`, `new_ban`, `str_dup`, `SET_BIT`, `save_bans`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.ban_site.if.001` | 149 | `if ( arg1[0] == '\0' )` |  | pending |
| `ban.ban_site.if.002` | 151 | `if (ban_list == NULL)` |  | pending |
| `ban.ban_site.return.001` | 154 | `return;` |  | pending |
| `ban.ban_site.for.001` | 159 | `for (pban = ban_list;pban != NULL;pban = pban->next)` |  | pending |
| `ban.ban_site.ternary.001` | 162 | `? "*" : "",` |  | pending |
| `ban.ban_site.ternary.002` | 164 | `? "*" : "");` |  | pending |
| `ban.ban_site.ternary.003` | 167 | `? "newbies" :` |  | pending |
| `ban.ban_site.ternary.004` | 168 | `? "permit"  :` |  | pending |
| `ban.ban_site.ternary.005` | 169 | `? "all"	: "",` |  | pending |
| `ban.ban_site.ternary.006` | 170 | `? "perm" : "temp");` |  | pending |
| `ban.ban_site.return.002` | 176 | `return;` |  | pending |
| `ban.ban_site.if.003` | 180 | `if (arg2[0] == '\0' \|\| !str_prefix(arg2,"all"))` |  | pending |
| `ban.ban_site.or.001` | 180 | `\|\| !str_prefix(arg2,"all"))` |  | pending |
| `ban.ban_site.if.004` | 182 | `if (!str_prefix(arg2,"newbies"))` |  | pending |
| `ban.ban_site.if.005` | 184 | `if (!str_prefix(arg2,"permit"))` |  | pending |
| `ban.ban_site.return.003` | 190 | `return;` |  | pending |
| `ban.ban_site.if.006` | 195 | `if (name[0] == '*')` |  | pending |
| `ban.ban_site.if.007` | 201 | `if (name[strlen(name) - 1] == '*')` |  | pending |
| `ban.ban_site.if.008` | 207 | `if (strlen(name) == 0)` |  | pending |
| `ban.ban_site.return.004` | 210 | `return;` |  | pending |
| `ban.ban_site.for.002` | 214 | `for ( pban = ban_list; pban != NULL; prev = pban, pban = pban->next )` |  | pending |
| `ban.ban_site.if.009` | 216 | `if (!str_cmp(name,pban->name))` |  | pending |
| `ban.ban_site.if.010` | 218 | `if (pban->level > get_trust(ch))` |  | pending |
| `ban.ban_site.return.005` | 221 | `return;` |  | pending |
| `ban.ban_site.if.011` | 225 | `if (prev == NULL)` |  | pending |
| `ban.ban_site.if.012` | 241 | `if (prefix)` |  | pending |
| `ban.ban_site.if.013` | 243 | `if (suffix)` |  | pending |
| `ban.ban_site.if.014` | 245 | `if (fPerm)` |  | pending |
| `ban.ban_site.return.006` | 253 | `return;` |  | pending |

## do_ban

[Source line 256](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:256); ends at line 259. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:289` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:89` (declaration_or_dispatch_reference).

Dependencies: `ban_site`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.do_ban.entry` | 256 | `Straight-line entry` |  | pending |

## do_permban

[Source line 261](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:261); ends at line 264. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:294` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:197` (declaration_or_dispatch_reference).

Dependencies: `ban_site`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.do_permban.entry` | 261 | `Straight-line entry` |  | pending |

## do_allow

[Source line 266](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:266); ends at line 307. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:288` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:74` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `get_trust`, `free_ban`, `sprintf`, `save_bans`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.do_allow.if.001` | 275 | `if ( arg[0] == '\0' )` |  | pending |
| `ban.do_allow.return.001` | 278 | `return;` |  | pending |
| `ban.do_allow.for.001` | 282 | `for ( curr = ban_list; curr != NULL; prev = curr, curr = curr->next )` |  | pending |
| `ban.do_allow.if.002` | 284 | `if ( !str_cmp( arg, curr->name ) )` |  | pending |
| `ban.do_allow.if.003` | 286 | `if (curr->level > get_trust(ch))` |  | pending |
| `ban.do_allow.return.002` | 290 | `return;` |  | pending |
| `ban.do_allow.if.004` | 292 | `if ( prev == NULL )` |  | pending |
| `ban.do_allow.return.003` | 301 | `return;` |  | pending |
| `ban.do_allow.return.004` | 306 | `return;` |  | pending |

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
- Line 38: `#include <unistd.h>` — pending configuration/reachability review.
- Line 39: `#include "merc.h"` — pending configuration/reachability review.
- Line 40: `#include "recycle.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


# src/ban.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `7a9610d96ea75d1415f1042871671ce392fd9dd4438d9cd82de7d271986429a4`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## save_bans

[Source line 44](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:44); ends at line 70. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- ban_site: `src/ban.c:250` (lexical_call_candidate).
- do_allow: `src/ban.c:300` (lexical_call_candidate).

Dependencies: `fclose`, `fopen`, `perror`, `IS_SET`, `fprintf`, `print_flags`, `unlink`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.save_bans.if.001` | 51 | `if ( ( fp = fopen( BAN_FILE, "w" ) ) == NULL )` | ban.save_bans.empty, ban.save_bans.permanent-in-list-order, ban.save_bans.open-failure-permanent-row-undefined | specified |
| `ban.save_bans.for.001` | 56 | `for (pban = ban_list; pban != NULL; pban = pban->next)` | ban.save_bans.empty, ban.save_bans.temporary-only, ban.save_bans.permanent-in-list-order, ban.save_bans.open-failure-permanent-row-undefined | specified |
| `ban.save_bans.if.002` | 58 | `if (IS_SET(pban->ban_flags,BAN_PERMANENT))` | ban.save_bans.temporary-only, ban.save_bans.permanent-in-list-order, ban.save_bans.open-failure-permanent-row-undefined | specified |
| `ban.save_bans.if.003` | 68 | `if (!found)` | ban.save_bans.empty, ban.save_bans.temporary-only, ban.save_bans.permanent-in-list-order | specified |
| `ban.save_bans.empty.path` | 68 | `empty` | ban.save_bans.empty | specified |
| `ban.save_bans.temporary-only.path` | 68 | `temporary only` | ban.save_bans.temporary-only | specified |
| `ban.save_bans.permanent-in-list-order.path` | 68 | `permanent in list order` | ban.save_bans.permanent-in-list-order | specified |
| `ban.save_bans.open-failure-permanent-row-undefined.path` | 53 | `open failure permanent row undefined` | ban.save_bans.open-failure-permanent-row-undefined | blocked |
| `ban.save_bans.open-failure-without-permanent-row-undefined.path` | 53 | `open failure without permanent row undefined` | ban.save_bans.open-failure-without-permanent-row-undefined | blocked |

## load_bans

[Source line 72](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:72); ends at line 103. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:384` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:224` (declaration_or_dispatch_reference).

Dependencies: `fopen`, `feof`, `fclose`, `new_ban`, `str_dup`, `fread_word`, `fread_number`, `fread_flag`, `fread_to_eol`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.load_bans.if.001` | 77 | `if ( ( fp = fopen( BAN_FILE, "r" ) ) == NULL )` | ban.load_bans.missing-file, ban.load_bans.loads-two-rows-in-file-order | specified |
| `ban.load_bans.return.001` | 78 | `return;` | ban.load_bans.missing-file | specified |
| `ban.load_bans.for.001` | 81 | `for ( ; ; )` | ban.load_bans.loads-two-rows-in-file-order | specified |
| `ban.load_bans.if.002` | 84 | `if ( feof(fp) )` | ban.load_bans.loads-two-rows-in-file-order | specified |
| `ban.load_bans.return.002` | 87 | `return;` | ban.load_bans.loads-two-rows-in-file-order | specified |
| `ban.load_bans.if.003` | 97 | `if (ban_list == NULL)` | ban.load_bans.loads-two-rows-in-file-order, ban.load_bans.nonempty-list-first-append-undefined | specified |
| `ban.load_bans.missing-file.path` | 77 | `missing file` | ban.load_bans.missing-file | specified |
| `ban.load_bans.loads-two-rows-in-file-order.path` | 97 | `loads two rows in file order` | ban.load_bans.loads-two-rows-in-file-order | specified |
| `ban.load_bans.nonempty-list-first-append-undefined.path` | 100 | `nonempty list first append undefined` | ban.load_bans.nonempty-list-first-append-undefined | blocked |
| `ban.load_bans.empty-file-parser-exits.path` | 92 | `empty file parser exits` | ban.load_bans.empty-file-parser-exits | specified |
| `ban.load_bans.whitespace-only-parser-exits.path` | 92 | `whitespace only parser exits` | ban.load_bans.whitespace-only-parser-exits | specified |
| `ban.load_bans.bad-level-parser-exits.path` | 92 | `bad level parser exits` | ban.load_bans.bad-level-parser-exits | specified |
| `ban.load_bans.no-final-newline-does-not-terminate.path` | 92 | `no final newline does not terminate` | ban.load_bans.no-final-newline-does-not-terminate | specified |
| `ban.load_bans.trailing-spaces-create-phantom-record.path` | 92 | `trailing spaces create phantom record` | ban.load_bans.trailing-spaces-create-phantom-record | specified |
| `ban.load_bans.invalid-flag-character-is-zero.path` | 92 | `invalid flag character is zero` | ban.load_bans.invalid-flag-character-is-zero | specified |
| `ban.load_bans.duplicate-letter-flags-add.path` | 92 | `duplicate letter flags add` | ban.load_bans.duplicate-letter-flags-add | specified |

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
| `ban.check_ban.for.001` | 113 | `for ( pban = ban_list; pban != NULL; pban = pban->next )` | ban.check_ban.empty-list | specified |
| `ban.check_ban.if.001` | 115 | `if(!IS_SET(pban->ban_flags,type))` | ban.check_ban.type-not-set | specified |
| `ban.check_ban.continue.001` | 116 | `continue;` | ban.check_ban.type-not-set | specified |
| `ban.check_ban.if.002` | 118 | `if (IS_SET(pban->ban_flags,BAN_PREFIX)  	&&  IS_SET(pban->ban_flags,BAN_SUFFIX)   	&&  strstr(pban->name,host) != NULL)` | ban.check_ban.exact-without-prefix-suffix-does-not-match, ban.check_ban.prefix-flag-tests-host-suffix, ban.check_ban.both-flags-host-contained-in-pattern, ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.and.001` | 119 | `&&  IS_SET(pban->ban_flags,BAN_SUFFIX)` | ban.check_ban.exact-without-prefix-suffix-does-not-match, ban.check_ban.both-flags-host-contained-in-pattern | specified |
| `ban.check_ban.and.002` | 120 | `&&  strstr(pban->name,host) != NULL)` | ban.check_ban.prefix-flag-tests-host-suffix, ban.check_ban.both-flags-host-contained-in-pattern, ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.return.001` | 121 | `return TRUE;` | ban.check_ban.both-flags-host-contained-in-pattern | specified |
| `ban.check_ban.if.003` | 123 | `if (IS_SET(pban->ban_flags,BAN_PREFIX) 	&&  !str_suffix(pban->name,host))` | ban.check_ban.exact-without-prefix-suffix-does-not-match, ban.check_ban.prefix-flag-tests-host-suffix, ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.and.003` | 124 | `&&  !str_suffix(pban->name,host))` | ban.check_ban.exact-without-prefix-suffix-does-not-match, ban.check_ban.prefix-flag-tests-host-suffix, ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.return.002` | 125 | `return TRUE;` | ban.check_ban.prefix-flag-tests-host-suffix | specified |
| `ban.check_ban.if.004` | 127 | `if (IS_SET(pban->ban_flags,BAN_SUFFIX) 	&&  !str_prefix(pban->name,host))` | ban.check_ban.exact-without-prefix-suffix-does-not-match, ban.check_ban.suffix-flag-tests-host-prefix, ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.and.004` | 128 | `&&  !str_prefix(pban->name,host))` | ban.check_ban.exact-without-prefix-suffix-does-not-match, ban.check_ban.suffix-flag-tests-host-prefix, ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.return.003` | 129 | `return TRUE;` | ban.check_ban.suffix-flag-tests-host-prefix | specified |
| `ban.check_ban.return.004` | 132 | `return FALSE;` | ban.check_ban.empty-list, ban.check_ban.exact-without-prefix-suffix-does-not-match, ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.empty-list.path` | 110 | `empty list` | ban.check_ban.empty-list | specified |
| `ban.check_ban.type-not-set.path` | 110 | `type not set` | ban.check_ban.type-not-set | specified |
| `ban.check_ban.exact-without-prefix-suffix-does-not-match.path` | 110 | `exact without prefix suffix does not match` | ban.check_ban.exact-without-prefix-suffix-does-not-match | specified |
| `ban.check_ban.prefix-flag-tests-host-suffix.path` | 110 | `prefix flag tests host suffix` | ban.check_ban.prefix-flag-tests-host-suffix | specified |
| `ban.check_ban.suffix-flag-tests-host-prefix.path` | 110 | `suffix flag tests host prefix` | ban.check_ban.suffix-flag-tests-host-prefix | specified |
| `ban.check_ban.both-flags-host-contained-in-pattern.path` | 110 | `both flags host contained in pattern` | ban.check_ban.both-flags-host-contained-in-pattern | specified |
| `ban.check_ban.both-flags-do-not-match-interior-pattern-in-host.path` | 110 | `both flags do not match interior pattern in host` | ban.check_ban.both-flags-do-not-match-interior-pattern-in-host | specified |
| `ban.check_ban.later-entry-matches.path` | 110 | `later entry matches` | ban.check_ban.later-entry-matches | specified |

## ban_site

[Source line 136](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:136); ends at line 254. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_ban: `src/ban.c:258` (lexical_call_candidate).
- do_permban: `src/ban.c:263` (lexical_call_candidate).

Dependencies: `one_argument`, `send_to_char`, `new_buf`, `add_buf`, `sprintf`, `IS_SET`, `page_to_char`, `buf_string`, `free_buf`, `str_prefix`, `strlen`, `str_cmp`, `get_trust`, `free_ban`, `new_ban`, `str_dup`, `SET_BIT`, `save_bans`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.ban_site.if.001` | 149 | `if ( arg1[0] == '\0' )` | ban.ban_site.no-sites, ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.if.002` | 151 | `if (ban_list == NULL)` | ban.ban_site.no-sites, ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.return.001` | 154 | `return;` | ban.ban_site.no-sites | specified |
| `ban.ban_site.for.001` | 159 | `for (pban = ban_list;pban != NULL;pban = pban->next)` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.ternary.001` | 162 | `? "*" : "",` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.ternary.002` | 164 | `? "*" : "");` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.ternary.003` | 167 | `? "newbies" :` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.ternary.004` | 168 | `? "permit"  :` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.ternary.005` | 169 | `? "all"	: "",` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.ternary.006` | 170 | `? "perm" : "temp");` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.return.002` | 176 | `return;` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.if.003` | 180 | `if (arg2[0] == '\0' \|\| !str_prefix(arg2,"all"))` | ban.ban_site.invalid-type-before-pattern, ban.ban_site.plain-default-type | specified |
| `ban.ban_site.or.001` | 180 | `\|\| !str_prefix(arg2,"all"))` | ban.ban_site.invalid-type-before-pattern, ban.ban_site.plain-default-type | specified |
| `ban.ban_site.if.004` | 182 | `if (!str_prefix(arg2,"newbies"))` | ban.ban_site.invalid-type-before-pattern, ban.ban_site.both-wildcards-permanent-newbies | specified |
| `ban.ban_site.if.005` | 184 | `if (!str_prefix(arg2,"permit"))` | ban.ban_site.invalid-type-before-pattern, ban.ban_site.suffix-permit | specified |
| `ban.ban_site.return.003` | 190 | `return;` | ban.ban_site.invalid-type-before-pattern | specified |
| `ban.ban_site.if.006` | 195 | `if (name[0] == '*')` | ban.ban_site.double-star-empty-name, ban.ban_site.plain-default-type, ban.ban_site.both-wildcards-permanent-newbies, ban.ban_site.suffix-permit | specified |
| `ban.ban_site.if.007` | 201 | `if (name[strlen(name) - 1] == '*')` | ban.ban_site.double-star-empty-name, ban.ban_site.plain-default-type, ban.ban_site.both-wildcards-permanent-newbies, ban.ban_site.suffix-permit | specified |
| `ban.ban_site.if.008` | 207 | `if (strlen(name) == 0)` | ban.ban_site.double-star-empty-name, ban.ban_site.plain-default-type | specified |
| `ban.ban_site.return.004` | 210 | `return;` | ban.ban_site.double-star-empty-name | specified |
| `ban.ban_site.for.002` | 214 | `for ( pban = ban_list; pban != NULL; prev = pban, pban = pban->next )` | ban.ban_site.higher-trust, ban.ban_site.plain-default-type | specified |
| `ban.ban_site.if.009` | 216 | `if (!str_cmp(name,pban->name))` | ban.ban_site.higher-trust, ban.ban_site.plain-default-type | specified |
| `ban.ban_site.if.010` | 218 | `if (pban->level > get_trust(ch))` | ban.ban_site.higher-trust, ban.ban_site.replace-head-with-empty-free-list, ban.ban_site.replace-interior-with-empty-free-list | specified |
| `ban.ban_site.return.005` | 221 | `return;` | ban.ban_site.higher-trust | specified |
| `ban.ban_site.if.011` | 225 | `if (prev == NULL)` | ban.ban_site.replace-head-with-empty-free-list, ban.ban_site.replace-interior-with-empty-free-list | specified |
| `ban.ban_site.if.012` | 241 | `if (prefix)` | ban.ban_site.plain-default-type, ban.ban_site.both-wildcards-permanent-newbies, ban.ban_site.suffix-permit | specified |
| `ban.ban_site.if.013` | 243 | `if (suffix)` | ban.ban_site.plain-default-type, ban.ban_site.both-wildcards-permanent-newbies, ban.ban_site.suffix-permit | specified |
| `ban.ban_site.if.014` | 245 | `if (fPerm)` | ban.ban_site.plain-default-type, ban.ban_site.both-wildcards-permanent-newbies, ban.ban_site.suffix-permit | specified |
| `ban.ban_site.return.006` | 253 | `return;` | ban.ban_site.plain-default-type, ban.ban_site.both-wildcards-permanent-newbies, ban.ban_site.suffix-permit | specified |
| `ban.ban_site.no-sites.path` | 146 | `no sites` | ban.ban_site.no-sites | specified |
| `ban.ban_site.invalid-type-before-pattern.path` | 146 | `invalid type before pattern` | ban.ban_site.invalid-type-before-pattern | specified |
| `ban.ban_site.double-star-empty-name.path` | 146 | `double star empty name` | ban.ban_site.double-star-empty-name | specified |
| `ban.ban_site.higher-trust.path` | 146 | `higher trust` | ban.ban_site.higher-trust | specified |
| `ban.ban_site.plain-default-type.path` | 146 | `plain default type` | ban.ban_site.plain-default-type | specified |
| `ban.ban_site.both-wildcards-permanent-newbies.path` | 146 | `both wildcards permanent newbies` | ban.ban_site.both-wildcards-permanent-newbies | specified |
| `ban.ban_site.suffix-permit.path` | 146 | `suffix permit` | ban.ban_site.suffix-permit | specified |
| `ban.ban_site.list-formats-wildcards-and-type-precedence.path` | 149 | `list formats wildcards and type precedence` | ban.ban_site.list-formats-wildcards-and-type-precedence | specified |
| `ban.ban_site.replace-head-with-empty-free-list.path` | 225 | `replace head with empty free list` | ban.ban_site.replace-head-with-empty-free-list | specified |
| `ban.ban_site.replace-interior-with-empty-free-list.path` | 225 | `replace interior with empty free list` | ban.ban_site.replace-interior-with-empty-free-list | specified |
| `ban.ban_site.single-star-empty-name-index-undefined.path` | 201 | `single star empty name index undefined` | ban.ban_site.single-star-empty-name-index-undefined | blocked |
| `ban.ban_site.replacement-walks-recycle-list.path` | 229 | `replacement walks recycle list` | ban.ban_site.replacement-walks-recycle-list | specified |

## do_ban

[Source line 256](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:256); ends at line 259. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:289` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:89` (declaration_or_dispatch_reference).

Dependencies: `ban_site`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.do_ban.entry` | 256 | `Straight-line entry` | ban.do_ban.dispatch-unchanged-argument | specified |
| `ban.do_ban.dispatch-unchanged-argument.path` | 258 | `dispatch unchanged argument` | ban.do_ban.dispatch-unchanged-argument | specified |

## do_permban

[Source line 261](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:261); ends at line 264. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:294` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:197` (declaration_or_dispatch_reference).

Dependencies: `ban_site`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.do_permban.entry` | 261 | `Straight-line entry` | ban.do_permban.dispatch-unchanged-argument | specified |
| `ban.do_permban.dispatch-unchanged-argument.path` | 263 | `dispatch unchanged argument` | ban.do_permban.dispatch-unchanged-argument | specified |

## do_allow

[Source line 266](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/ban.c:266); ends at line 307. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:288` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:74` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `get_trust`, `free_ban`, `sprintf`, `save_bans`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `ban.do_allow.if.001` | 275 | `if ( arg[0] == '\0' )` | ban.do_allow.missing-name | specified |
| `ban.do_allow.return.001` | 278 | `return;` | ban.do_allow.missing-name | specified |
| `ban.do_allow.for.001` | 282 | `for ( curr = ban_list; curr != NULL; prev = curr, curr = curr->next )` | ban.do_allow.missing-entry | specified |
| `ban.do_allow.if.002` | 284 | `if ( !str_cmp( arg, curr->name ) )` | ban.do_allow.missing-entry, ban.do_allow.higher-trust | specified |
| `ban.do_allow.if.003` | 286 | `if (curr->level > get_trust(ch))` | ban.do_allow.higher-trust, ban.do_allow.remove-head-at-equal-trust | specified |
| `ban.do_allow.return.002` | 290 | `return;` | ban.do_allow.higher-trust | specified |
| `ban.do_allow.if.004` | 292 | `if ( prev == NULL )` | ban.do_allow.remove-head-at-equal-trust, ban.do_allow.remove-interior | specified |
| `ban.do_allow.return.003` | 301 | `return;` | ban.do_allow.remove-head-at-equal-trust, ban.do_allow.remove-interior | specified |
| `ban.do_allow.return.004` | 306 | `return;` | ban.do_allow.missing-entry | specified |
| `ban.do_allow.missing-name.path` | 275 | `missing name` | ban.do_allow.missing-name | specified |
| `ban.do_allow.missing-entry.path` | 275 | `missing entry` | ban.do_allow.missing-entry | specified |
| `ban.do_allow.higher-trust.path` | 275 | `higher trust` | ban.do_allow.higher-trust | specified |
| `ban.do_allow.remove-head-at-equal-trust.path` | 275 | `remove head at equal trust` | ban.do_allow.remove-head-at-equal-trust | specified |
| `ban.do_allow.remove-interior.path` | 275 | `remove interior` | ban.do_allow.remove-interior | specified |

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


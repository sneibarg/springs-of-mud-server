# src/alias.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `24fe637762d4041792a187f5b28d9e77fcc04d48f77bbcbc40e0ea8aa47b4e8d`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## substitute_alias

[Source line 39](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:39); ends at line 96. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- game_loop_mac_msdos: `src/comm.c:577` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:768` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2096` (declaration_or_dispatch_reference).

Dependencies: `str_prefix`, `strlen`, `send_to_char`, `sprintf`, `IS_NPC`, `interpret`, `strcpy`, `one_argument`, `strcmp`, `strcat`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `alias.substitute_alias.ternary.001` | 46 | `? d->original : d->character;` |  | pending |
| `alias.substitute_alias.if.001` | 49 | `if (ch->prefix[0] != '\0' && str_prefix("prefix",argument))` |  | pending |
| `alias.substitute_alias.and.001` | 49 | `&& str_prefix("prefix",argument))` |  | pending |
| `alias.substitute_alias.if.002` | 51 | `if (strlen(ch->prefix) + strlen(argument) > MAX_INPUT_LENGTH)` |  | pending |
| `alias.substitute_alias.if.003` | 60 | `if (IS_NPC(ch) \|\| ch->pcdata->alias[0] == NULL     \|\|	!str_prefix("alias",argument) \|\| !str_prefix("una",argument)      \|\|  !str_prefix("prefix",argument))` |  | pending |
| `alias.substitute_alias.or.001` | 60 | `\|\| ch->pcdata->alias[0] == NULL` |  | pending |
| `alias.substitute_alias.or.002` | 61 | `\|\|	!str_prefix("alias",argument) \|\| !str_prefix("una",argument)` |  | pending |
| `alias.substitute_alias.or.003` | 61 | `\|\| !str_prefix("una",argument)` |  | pending |
| `alias.substitute_alias.or.004` | 62 | `\|\|  !str_prefix("prefix",argument))` |  | pending |
| `alias.substitute_alias.return.001` | 65 | `return;` |  | pending |
| `alias.substitute_alias.for.001` | 70 | `for (alias = 0; alias < MAX_ALIAS; alias++)` |  | pending |
| `alias.substitute_alias.if.004` | 72 | `if (ch->pcdata->alias[alias] == NULL)` |  | pending |
| `alias.substitute_alias.break.001` | 73 | `break;` |  | pending |
| `alias.substitute_alias.if.005` | 75 | `if (!str_prefix(ch->pcdata->alias[alias],argument))` |  | pending |
| `alias.substitute_alias.if.006` | 78 | `if (!strcmp(ch->pcdata->alias[alias],name))` |  | pending |
| `alias.substitute_alias.if.007` | 85 | `if (strlen(buf) > MAX_INPUT_LENGTH - 1)` |  | pending |
| `alias.substitute_alias.break.002` | 91 | `break;` |  | pending |
| `alias.substitute_alias.exact-first-word.path` | 46 | `exact first word` | alias.substitute_alias.exact-first-word | specified |
| `alias.substitute_alias.no-recursive-expansion.path` | 46 | `no recursive expansion` | alias.substitute_alias.no-recursive-expansion | specified |
| `alias.substitute_alias.prefix-not-exact-alias.path` | 46 | `prefix not exact alias` | alias.substitute_alias.prefix-not-exact-alias | specified |
| `alias.substitute_alias.input-lowercases-first-word-only.path` | 46 | `input lowercases first word only` | alias.substitute_alias.input-lowercases-first-word-only | specified |
| `alias.substitute_alias.protected-alias-command.path` | 46 | `protected alias command` | alias.substitute_alias.protected-alias-command | specified |
| `alias.substitute_alias.protected-una-prefix.path` | 46 | `protected una prefix` | alias.substitute_alias.protected-una-prefix | specified |
| `alias.substitute_alias.prefix-precedes-alias.path` | 46 | `prefix precedes alias` | alias.substitute_alias.prefix-precedes-alias | specified |
| `alias.substitute_alias.prefix-command-bypasses-prefix.path` | 46 | `prefix command bypasses prefix` | alias.substitute_alias.prefix-command-bypasses-prefix | specified |
| `alias.substitute_alias.no-aliases.path` | 46 | `no aliases` | alias.substitute_alias.no-aliases | specified |
| `alias.substitute_alias.original-npc-bypasses-alias.path` | 46 | `original npc bypasses alias` | alias.substitute_alias.original-npc-bypasses-alias | specified |
| `alias.substitute_alias.replacement-truncates-at-255.path` | 85 | `replacement truncates at 255` | alias.substitute_alias.replacement-truncates-at-255 | specified |
| `alias.substitute_alias.prefix-overflow-boundary-undefined.path` | 51 | `prefix overflow boundary undefined` | alias.substitute_alias.prefix-overflow-boundary-undefined | blocked |

## do_alia

[Source line 98](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:98); ends at line 102. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:147` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:72` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `alias.do_alia.return.001` | 101 | `return;` |  | pending |
| `alias.do_alia.requires-full-name.path` | 100 | `requires full name` | alias.do_alia.requires-full-name | specified |

## do_alias

[Source line 104](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:104); ends at line 205. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:148` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:73` (declaration_or_dispatch_reference).

Dependencies: `smash_tilde`, `IS_NPC`, `one_argument`, `send_to_char`, `sprintf`, `str_prefix`, `str_cmp`, `free_string`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `alias.do_alias.if.001` | 112 | `if (ch->desc == NULL)` |  | pending |
| `alias.do_alias.ternary.001` | 115 | `? ch->desc->original : ch;` |  | pending |
| `alias.do_alias.if.002` | 117 | `if (IS_NPC(rch))` |  | pending |
| `alias.do_alias.return.001` | 118 | `return;` |  | pending |
| `alias.do_alias.if.003` | 123 | `if (arg[0] == '\0')` |  | pending |
| `alias.do_alias.if.004` | 126 | `if (rch->pcdata->alias[0] == NULL)` |  | pending |
| `alias.do_alias.return.002` | 129 | `return;` |  | pending |
| `alias.do_alias.for.001` | 133 | `for (pos = 0; pos < MAX_ALIAS; pos++)` |  | pending |
| `alias.do_alias.if.005` | 135 | `if (rch->pcdata->alias[pos] == NULL 	    \|\|	rch->pcdata->alias_sub[pos] == NULL)` |  | pending |
| `alias.do_alias.or.001` | 136 | `\|\|	rch->pcdata->alias_sub[pos] == NULL)` |  | pending |
| `alias.do_alias.break.001` | 137 | `break;` |  | pending |
| `alias.do_alias.return.003` | 143 | `return;` |  | pending |
| `alias.do_alias.if.006` | 146 | `if (!str_prefix("una",arg) \|\| !str_cmp("alias",arg))` |  | pending |
| `alias.do_alias.or.002` | 146 | `\|\| !str_cmp("alias",arg))` |  | pending |
| `alias.do_alias.return.004` | 149 | `return;` |  | pending |
| `alias.do_alias.if.007` | 152 | `if (argument[0] == '\0')` |  | pending |
| `alias.do_alias.for.002` | 154 | `for (pos = 0; pos < MAX_ALIAS; pos++)` |  | pending |
| `alias.do_alias.if.008` | 156 | `if (rch->pcdata->alias[pos] == NULL 	    \|\|	rch->pcdata->alias_sub[pos] == NULL)` |  | pending |
| `alias.do_alias.or.003` | 157 | `\|\|	rch->pcdata->alias_sub[pos] == NULL)` |  | pending |
| `alias.do_alias.break.002` | 158 | `break;` |  | pending |
| `alias.do_alias.if.009` | 160 | `if (!str_cmp(arg,rch->pcdata->alias[pos]))` |  | pending |
| `alias.do_alias.return.005` | 165 | `return;` |  | pending |
| `alias.do_alias.return.006` | 170 | `return;` |  | pending |
| `alias.do_alias.if.010` | 173 | `if (!str_prefix(argument,"delete") \|\| !str_prefix(argument,"prefix"))` |  | pending |
| `alias.do_alias.or.004` | 173 | `\|\| !str_prefix(argument,"prefix"))` |  | pending |
| `alias.do_alias.return.007` | 176 | `return;` |  | pending |
| `alias.do_alias.for.003` | 179 | `for (pos = 0; pos < MAX_ALIAS; pos++)` |  | pending |
| `alias.do_alias.if.011` | 181 | `if (rch->pcdata->alias[pos] == NULL)` |  | pending |
| `alias.do_alias.break.003` | 182 | `break;` |  | pending |
| `alias.do_alias.if.012` | 184 | `if (!str_cmp(arg,rch->pcdata->alias[pos]))` |  | pending |
| `alias.do_alias.return.008` | 190 | `return;` |  | pending |
| `alias.do_alias.if.013` | 194 | `if (pos >= MAX_ALIAS)` |  | pending |
| `alias.do_alias.return.009` | 197 | `return;` |  | pending |
| `alias.do_alias.no-aliases.path` | 110 | `no aliases` | alias.do_alias.no-aliases | specified |
| `alias.do_alias.reserved-alias.path` | 110 | `reserved alias` | alias.do_alias.reserved-alias | specified |
| `alias.do_alias.reserved-una-prefix.path` | 110 | `reserved una prefix` | alias.do_alias.reserved-una-prefix | specified |
| `alias.do_alias.undefined-query.path` | 110 | `undefined query` | alias.do_alias.undefined-query | specified |
| `alias.do_alias.defined-query.path` | 110 | `defined query` | alias.do_alias.defined-query | specified |
| `alias.do_alias.add.path` | 110 | `add` | alias.do_alias.add | specified |
| `alias.do_alias.redefine.path` | 110 | `redefine` | alias.do_alias.redefine | specified |
| `alias.do_alias.delete-abbreviation-rejected.path` | 110 | `delete abbreviation rejected` | alias.do_alias.delete-abbreviation-rejected | specified |
| `alias.do_alias.prefix-abbreviation-rejected.path` | 110 | `prefix abbreviation rejected` | alias.do_alias.prefix-abbreviation-rejected | specified |
| `alias.do_alias.full-delete-plus-argument-allowed-quirk.path` | 110 | `full delete plus argument allowed quirk` | alias.do_alias.full-delete-plus-argument-allowed-quirk | specified |
| `alias.do_alias.tilde-sanitized.path` | 110 | `tilde sanitized` | alias.do_alias.tilde-sanitized | specified |
| `alias.do_alias.at-five-alias-limit.path` | 194 | `at five alias limit` | alias.do_alias.at-five-alias-limit | specified |

## do_unalias

[Source line 208](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:208); ends at line 258. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:171` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:275` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `one_argument`, `send_to_char`, `strcmp`, `free_string`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `alias.do_unalias.if.001` | 215 | `if (ch->desc == NULL)` |  | pending |
| `alias.do_unalias.ternary.001` | 218 | `? ch->desc->original : ch;` |  | pending |
| `alias.do_unalias.if.002` | 220 | `if (IS_NPC(rch))` |  | pending |
| `alias.do_unalias.return.001` | 221 | `return;` |  | pending |
| `alias.do_unalias.if.003` | 225 | `if (arg[0] == '\0')` |  | pending |
| `alias.do_unalias.return.002` | 228 | `return;` |  | pending |
| `alias.do_unalias.for.001` | 231 | `for (pos = 0; pos < MAX_ALIAS; pos++)` |  | pending |
| `alias.do_unalias.if.004` | 233 | `if (rch->pcdata->alias[pos] == NULL)` |  | pending |
| `alias.do_unalias.break.001` | 234 | `break;` |  | pending |
| `alias.do_unalias.if.005` | 236 | `if (found)` |  | pending |
| `alias.do_unalias.continue.001` | 242 | `continue;` |  | pending |
| `alias.do_unalias.if.006` | 245 | `if(!strcmp(arg,rch->pcdata->alias[pos]))` |  | pending |
| `alias.do_unalias.if.007` | 256 | `if (!found)` |  | pending |
| `alias.do_unalias.missing-name.path` | 223 | `missing name` | alias.do_unalias.missing-name | specified |
| `alias.do_unalias.not-found.path` | 223 | `not found` | alias.do_unalias.not-found | specified |
| `alias.do_unalias.remove-only.path` | 223 | `remove only` | alias.do_unalias.remove-only | specified |
| `alias.do_unalias.remove-first-shifts-all.path` | 223 | `remove first shifts all` | alias.do_unalias.remove-first-shifts-all | specified |
| `alias.do_unalias.remove-middle-shifts-tail.path` | 223 | `remove middle shifts tail` | alias.do_unalias.remove-middle-shifts-tail | specified |
| `alias.do_unalias.remove-last.path` | 223 | `remove last` | alias.do_unalias.remove-last | specified |

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

## Static tables


## Commented code candidates


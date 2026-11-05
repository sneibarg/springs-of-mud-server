# src/flags.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `a41ec36ceedb69477efbeb98fa029729735e66ce6f3c6e4f334726c41e0fafaa`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## do_flag

[Source line 43](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/flags.c:43); ends at line 245. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:292` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:130` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_prefix`, `get_char_world`, `IS_NPC`, `flag_lookup`, `SET_BIT`, `IS_SET`, `REMOVE_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `flags.do_flag.if.001` | 58 | `if (type == '=' \|\| type == '-' \|\| type == '+')` |  | pending |
| `flags.do_flag.or.001` | 58 | `\|\| type == '-' \|\| type == '+')` |  | pending |
| `flags.do_flag.or.002` | 58 | `\|\| type == '+')` |  | pending |
| `flags.do_flag.if.002` | 61 | `if (arg1[0] == '\0')` |  | pending |
| `flags.do_flag.return.001` | 70 | `return;` |  | pending |
| `flags.do_flag.if.003` | 73 | `if (arg2[0] == '\0')` |  | pending |
| `flags.do_flag.return.002` | 76 | `return;` |  | pending |
| `flags.do_flag.if.004` | 79 | `if (arg3[0] == '\0')` |  | pending |
| `flags.do_flag.return.003` | 82 | `return;` |  | pending |
| `flags.do_flag.if.005` | 85 | `if (argument[0] == '\0')` |  | pending |
| `flags.do_flag.return.004` | 88 | `return;` |  | pending |
| `flags.do_flag.if.006` | 91 | `if (!str_prefix(arg1,"mob") \|\| !str_prefix(arg1,"char"))` |  | pending |
| `flags.do_flag.or.003` | 91 | `\|\| !str_prefix(arg1,"char"))` |  | pending |
| `flags.do_flag.if.007` | 94 | `if (victim == NULL)` |  | pending |
| `flags.do_flag.return.005` | 97 | `return;` |  | pending |
| `flags.do_flag.if.008` | 101 | `if (!str_prefix(arg3,"act"))` |  | pending |
| `flags.do_flag.if.009` | 103 | `if (!IS_NPC(victim))` |  | pending |
| `flags.do_flag.return.006` | 106 | `return;` |  | pending |
| `flags.do_flag.if.010` | 113 | `if (!str_prefix(arg3,"plr"))` |  | pending |
| `flags.do_flag.if.011` | 115 | `if (IS_NPC(victim))` |  | pending |
| `flags.do_flag.return.007` | 118 | `return;` |  | pending |
| `flags.do_flag.if.012` | 125 | `if (!str_prefix(arg3,"aff"))` |  | pending |
| `flags.do_flag.if.013` | 131 | `if (!str_prefix(arg3,"immunity"))` |  | pending |
| `flags.do_flag.if.014` | 137 | `if (!str_prefix(arg3,"resist"))` |  | pending |
| `flags.do_flag.if.015` | 143 | `if (!str_prefix(arg3,"vuln"))` |  | pending |
| `flags.do_flag.if.016` | 149 | `if (!str_prefix(arg3,"form"))` |  | pending |
| `flags.do_flag.if.017` | 151 | `if (!IS_NPC(victim))` |  | pending |
| `flags.do_flag.return.008` | 154 | `return;` |  | pending |
| `flags.do_flag.if.018` | 161 | `if (!str_prefix(arg3,"parts"))` |  | pending |
| `flags.do_flag.if.019` | 163 | `if (!IS_NPC(victim))` |  | pending |
| `flags.do_flag.return.009` | 166 | `return;` |  | pending |
| `flags.do_flag.if.020` | 173 | `if (!str_prefix(arg3,"comm"))` |  | pending |
| `flags.do_flag.if.021` | 175 | `if (IS_NPC(victim))` |  | pending |
| `flags.do_flag.return.010` | 178 | `return;` |  | pending |
| `flags.do_flag.return.011` | 188 | `return;` |  | pending |
| `flags.do_flag.if.022` | 194 | `if (type != '=')` |  | pending |
| `flags.do_flag.for.001` | 198 | `for (; ;)` |  | pending |
| `flags.do_flag.if.023` | 202 | `if (word[0] == '\0')` |  | pending |
| `flags.do_flag.break.001` | 203 | `break;` |  | pending |
| `flags.do_flag.if.024` | 206 | `if (pos == 0)` |  | pending |
| `flags.do_flag.return.012` | 209 | `return;` |  | pending |
| `flags.do_flag.for.002` | 215 | `for (pos = 0; flag_table[pos].name != NULL; pos++)` |  | pending |
| `flags.do_flag.if.025` | 217 | `if (!flag_table[pos].settable && IS_SET(old,flag_table[pos].bit))` |  | pending |
| `flags.do_flag.and.001` | 217 | `&& IS_SET(old,flag_table[pos].bit))` |  | pending |
| `flags.do_flag.continue.001` | 220 | `continue;` |  | pending |
| `flags.do_flag.if.026` | 223 | `if (IS_SET(marked,flag_table[pos].bit))` |  | pending |
| `flags.do_flag.switch.001` | 225 | `switch(type)` |  | pending |
| `flags.do_flag.case.001` | 227 | `case '=':` |  | pending |
| `flags.do_flag.case.002` | 228 | `case '+':` |  | pending |
| `flags.do_flag.break.002` | 230 | `break;` |  | pending |
| `flags.do_flag.case.003` | 231 | `case '-':` |  | pending |
| `flags.do_flag.break.003` | 233 | `break;` |  | pending |
| `flags.do_flag.default.001` | 234 | `default:` |  | pending |
| `flags.do_flag.if.027` | 235 | `if (IS_SET(new,flag_table[pos].bit))` |  | pending |
| `flags.do_flag.return.013` | 243 | `return;` |  | pending |
| `flags.do_flag.no-arguments.path` | 61 | `no arguments` | flags.do_flag.no-arguments | specified |
| `flags.do_flag.missing-target.path` | 61 | `missing target` | flags.do_flag.missing-target | specified |
| `flags.do_flag.missing-field.path` | 61 | `missing field` | flags.do_flag.missing-field | specified |
| `flags.do_flag.missing-flags.path` | 61 | `missing flags` | flags.do_flag.missing-flags | specified |
| `flags.do_flag.missing-world-target.path` | 93 | `missing world target` | flags.do_flag.missing-world-target | specified |
| `flags.do_flag.act-on-pc.path` | 93 | `act on pc` | flags.do_flag.act-on-pc | specified |
| `flags.do_flag.plr-on-npc.path` | 93 | `plr on npc` | flags.do_flag.plr-on-npc | specified |
| `flags.do_flag.form-on-pc.path` | 93 | `form on pc` | flags.do_flag.form-on-pc | specified |
| `flags.do_flag.parts-on-pc.path` | 93 | `parts on pc` | flags.do_flag.parts-on-pc | specified |
| `flags.do_flag.comm-on-npc.path` | 93 | `comm on npc` | flags.do_flag.comm-on-npc | specified |
| `flags.do_flag.unsupported-off-field.path` | 93 | `unsupported off field` | flags.do_flag.unsupported-off-field | specified |
| `flags.do_flag.unknown-type-silent.path` | 56 | `unknown type silent` | flags.do_flag.unknown-type-silent | specified |
| `flags.do_flag.invalid-word-clears-zone.path` | 56 | `invalid word clears zone` | flags.do_flag.invalid-word-clears-zone | specified |
| `flags.do_flag.valid-then-invalid-atomic-flags.path` | 56 | `valid then invalid atomic flags` | flags.do_flag.valid-then-invalid-atomic-flags | specified |
| `flags.do_flag.add.path` | 56 | `add` | flags.do_flag.add | specified |
| `flags.do_flag.remove.path` | 56 | `remove` | flags.do_flag.remove | specified |
| `flags.do_flag.toggle-present.path` | 56 | `toggle present` | flags.do_flag.toggle-present | specified |
| `flags.do_flag.toggle-absent.path` | 56 | `toggle absent` | flags.do_flag.toggle-absent | specified |
| `flags.do_flag.equal-preserves-npc.path` | 56 | `equal preserves npc` | flags.do_flag.equal-preserves-npc | specified |
| `flags.do_flag.nonsettable-present-preserved.path` | 56 | `nonsettable present preserved` | flags.do_flag.nonsettable-present-preserved | specified |
| `flags.do_flag.duplicate-toggle-only-once.path` | 56 | `duplicate toggle only once` | flags.do_flag.duplicate-toggle-only-once | specified |
| `flags.do_flag.type-label-does-not-restrict-kind.path` | 56 | `type label does not restrict kind` | flags.do_flag.type-label-does-not-restrict-kind | specified |
| `flags.do_flag.operator-alone.path` | 56 | `operator alone` | flags.do_flag.operator-alone | specified |
| `flags.do_flag.nonsettable-absent-can-be-added-reference-quirk.path` | 217 | `nonsettable absent can be added reference quirk` | flags.do_flag.nonsettable-absent-can-be-added-reference-quirk | specified |
| `flags.do_flag.aff-field.path` | 191 | `aff field` | flags.do_flag.aff-field | specified |
| `flags.do_flag.immunity-field.path` | 191 | `immunity field` | flags.do_flag.immunity-field | specified |
| `flags.do_flag.resist-field.path` | 191 | `resist field` | flags.do_flag.resist-field | specified |
| `flags.do_flag.vuln-field.path` | 191 | `vuln field` | flags.do_flag.vuln-field | specified |
| `flags.do_flag.form-field.path` | 191 | `form field` | flags.do_flag.form-field | specified |
| `flags.do_flag.parts-field.path` | 191 | `parts field` | flags.do_flag.parts-field | specified |
| `flags.do_flag.comm-field.path` | 191 | `comm field` | flags.do_flag.comm-field | specified |
| `flags.do_flag.plr-field.path` | 191 | `plr field` | flags.do_flag.plr-field | specified |
| `flags.do_flag.ambiguous-a-selects-act.path` | 191 | `ambiguous a selects act` | flags.do_flag.ambiguous-a-selects-act | specified |
| `flags.do_flag.operator-attached-consumes-word.path` | 58 | `operator attached consumes word` | flags.do_flag.operator-attached-consumes-word | specified |

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
- Line 39: `#include "tables.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


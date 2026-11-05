# src/scan.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `8f12b282411f2b31d747cb860248ec070d3cfc0529111afab399e14b1e0d622f`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## do_scan

[Source line 48](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/scan.c:48); ends at line 94. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- spell_farsight: `src/magic2.c:52` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.h:237` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `act`, `send_to_char`, `scan_list`, `str_cmp`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `scan.do_scan.if.001` | 58 | `if (arg1[0] == '\0')` | scan.do_scan.invalid-direction, scan.do_scan.around-includes-current-and-each-exit, scan.do_scan.north-short, scan.do_scan.north-long, scan.do_scan.east-short, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.north-long-with-0-hops, scan.do_scan.north-long-with-1-hops, scan.do_scan.north-long-with-2-hops, scan.do_scan.east-long-with-0-hops, scan.do_scan.east-long-with-1-hops, scan.do_scan.east-long-with-2-hops, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops, scan.do_scan.around-null-destination-is-safe | specified |
| `scan.do_scan.for.001` | 64 | `for (door=0;door<6;door++)` | scan.do_scan.around-includes-current-and-each-exit, scan.do_scan.around-null-destination-is-safe | specified |
| `scan.do_scan.if.002` | 66 | `if ((pExit = ch ->in_room->exit[door]) != NULL)` | scan.do_scan.around-includes-current-and-each-exit, scan.do_scan.around-null-destination-is-safe | specified |
| `scan.do_scan.return.001` | 69 | `return;` | scan.do_scan.around-includes-current-and-each-exit, scan.do_scan.around-null-destination-is-safe | specified |
| `scan.do_scan.if.003` | 71 | `if (!str_cmp(arg1, "n") \|\| !str_cmp(arg1, "north"))` | scan.do_scan.invalid-direction, scan.do_scan.north-short, scan.do_scan.north-long, scan.do_scan.east-short, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.north-long-with-0-hops, scan.do_scan.north-long-with-1-hops, scan.do_scan.north-long-with-2-hops, scan.do_scan.east-long-with-0-hops, scan.do_scan.east-long-with-1-hops, scan.do_scan.east-long-with-2-hops, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.or.001` | 71 | `\|\| !str_cmp(arg1, "north")) door = 0;` | scan.do_scan.invalid-direction, scan.do_scan.north-short, scan.do_scan.north-long, scan.do_scan.east-short, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.north-long-with-0-hops, scan.do_scan.north-long-with-1-hops, scan.do_scan.north-long-with-2-hops, scan.do_scan.east-long-with-0-hops, scan.do_scan.east-long-with-1-hops, scan.do_scan.east-long-with-2-hops, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.if.004` | 72 | `if (!str_cmp(arg1, "e") \|\| !str_cmp(arg1, "east"))` | scan.do_scan.invalid-direction, scan.do_scan.east-short, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.east-long-with-0-hops, scan.do_scan.east-long-with-1-hops, scan.do_scan.east-long-with-2-hops, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.or.002` | 72 | `\|\| !str_cmp(arg1, "east"))  door = 1;` | scan.do_scan.invalid-direction, scan.do_scan.east-short, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.east-long-with-0-hops, scan.do_scan.east-long-with-1-hops, scan.do_scan.east-long-with-2-hops, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.if.005` | 73 | `if (!str_cmp(arg1, "s") \|\| !str_cmp(arg1, "south"))` | scan.do_scan.invalid-direction, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.or.003` | 73 | `\|\| !str_cmp(arg1, "south")) door = 2;` | scan.do_scan.invalid-direction, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.if.006` | 74 | `if (!str_cmp(arg1, "w") \|\| !str_cmp(arg1, "west"))` | scan.do_scan.invalid-direction, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.or.004` | 74 | `\|\| !str_cmp(arg1, "west"))  door = 3;` | scan.do_scan.invalid-direction, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.if.007` | 75 | `if (!str_cmp(arg1, "u") \|\| !str_cmp(arg1, "up" ))` | scan.do_scan.invalid-direction, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.or.005` | 75 | `\|\| !str_cmp(arg1, "up" ))   door = 4;` | scan.do_scan.invalid-direction, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.if.008` | 76 | `if (!str_cmp(arg1, "d") \|\| !str_cmp(arg1, "down"))` | scan.do_scan.invalid-direction, scan.do_scan.down-short, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.or.006` | 76 | `\|\| !str_cmp(arg1, "down"))  door = 5;` | scan.do_scan.invalid-direction, scan.do_scan.down-short, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.return.002` | 77 | `return;` | scan.do_scan.invalid-direction | specified |
| `scan.do_scan.for.002` | 85 | `for (depth = 1; depth < 4; depth++)` | scan.do_scan.north-short, scan.do_scan.north-long, scan.do_scan.east-short, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.north-long-with-0-hops, scan.do_scan.north-long-with-1-hops, scan.do_scan.north-long-with-2-hops, scan.do_scan.east-long-with-0-hops, scan.do_scan.east-long-with-1-hops, scan.do_scan.east-long-with-2-hops, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.if.009` | 87 | `if ((pExit = scan_room->exit[door]) != NULL)` | scan.do_scan.north-short, scan.do_scan.north-long, scan.do_scan.east-short, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.north-long-with-0-hops, scan.do_scan.north-long-with-1-hops, scan.do_scan.north-long-with-2-hops, scan.do_scan.east-long-with-0-hops, scan.do_scan.east-long-with-1-hops, scan.do_scan.east-long-with-2-hops, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.return.003` | 93 | `return;` | scan.do_scan.north-short, scan.do_scan.north-long, scan.do_scan.east-short, scan.do_scan.south-short, scan.do_scan.west-short, scan.do_scan.up-short, scan.do_scan.down-short, scan.do_scan.north-long-with-0-hops, scan.do_scan.north-long-with-1-hops, scan.do_scan.north-long-with-2-hops, scan.do_scan.east-long-with-0-hops, scan.do_scan.east-long-with-1-hops, scan.do_scan.east-long-with-2-hops, scan.do_scan.south-long-with-0-hops, scan.do_scan.south-long-with-1-hops, scan.do_scan.south-long-with-2-hops, scan.do_scan.west-long-with-0-hops, scan.do_scan.west-long-with-1-hops, scan.do_scan.west-long-with-2-hops, scan.do_scan.up-long-with-0-hops, scan.do_scan.up-long-with-1-hops, scan.do_scan.up-long-with-2-hops, scan.do_scan.down-long-with-0-hops, scan.do_scan.down-long-with-1-hops, scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.invalid-direction.path` | 77 | `invalid direction` | scan.do_scan.invalid-direction | specified |
| `scan.do_scan.around-includes-current-and-each-exit.path` | 58 | `around includes current and each exit` | scan.do_scan.around-includes-current-and-each-exit | specified |
| `scan.do_scan.north-short.path` | 85 | `north short` | scan.do_scan.north-short | specified |
| `scan.do_scan.north-long.path` | 85 | `north long` | scan.do_scan.north-long | specified |
| `scan.do_scan.east-short.path` | 85 | `east short` | scan.do_scan.east-short | specified |
| `scan.do_scan.south-short.path` | 85 | `south short` | scan.do_scan.south-short | specified |
| `scan.do_scan.west-short.path` | 85 | `west short` | scan.do_scan.west-short | specified |
| `scan.do_scan.up-short.path` | 85 | `up short` | scan.do_scan.up-short | specified |
| `scan.do_scan.down-short.path` | 85 | `down short` | scan.do_scan.down-short | specified |
| `scan.do_scan.north-long-with-0-hops.path` | 85 | `north long with 0 hops` | scan.do_scan.north-long-with-0-hops | specified |
| `scan.do_scan.north-long-with-1-hops.path` | 85 | `north long with 1 hops` | scan.do_scan.north-long-with-1-hops | specified |
| `scan.do_scan.north-long-with-2-hops.path` | 85 | `north long with 2 hops` | scan.do_scan.north-long-with-2-hops | specified |
| `scan.do_scan.east-long-with-0-hops.path` | 85 | `east long with 0 hops` | scan.do_scan.east-long-with-0-hops | specified |
| `scan.do_scan.east-long-with-1-hops.path` | 85 | `east long with 1 hops` | scan.do_scan.east-long-with-1-hops | specified |
| `scan.do_scan.east-long-with-2-hops.path` | 85 | `east long with 2 hops` | scan.do_scan.east-long-with-2-hops | specified |
| `scan.do_scan.south-long-with-0-hops.path` | 85 | `south long with 0 hops` | scan.do_scan.south-long-with-0-hops | specified |
| `scan.do_scan.south-long-with-1-hops.path` | 85 | `south long with 1 hops` | scan.do_scan.south-long-with-1-hops | specified |
| `scan.do_scan.south-long-with-2-hops.path` | 85 | `south long with 2 hops` | scan.do_scan.south-long-with-2-hops | specified |
| `scan.do_scan.west-long-with-0-hops.path` | 85 | `west long with 0 hops` | scan.do_scan.west-long-with-0-hops | specified |
| `scan.do_scan.west-long-with-1-hops.path` | 85 | `west long with 1 hops` | scan.do_scan.west-long-with-1-hops | specified |
| `scan.do_scan.west-long-with-2-hops.path` | 85 | `west long with 2 hops` | scan.do_scan.west-long-with-2-hops | specified |
| `scan.do_scan.up-long-with-0-hops.path` | 85 | `up long with 0 hops` | scan.do_scan.up-long-with-0-hops | specified |
| `scan.do_scan.up-long-with-1-hops.path` | 85 | `up long with 1 hops` | scan.do_scan.up-long-with-1-hops | specified |
| `scan.do_scan.up-long-with-2-hops.path` | 85 | `up long with 2 hops` | scan.do_scan.up-long-with-2-hops | specified |
| `scan.do_scan.down-long-with-0-hops.path` | 85 | `down long with 0 hops` | scan.do_scan.down-long-with-0-hops | specified |
| `scan.do_scan.down-long-with-1-hops.path` | 85 | `down long with 1 hops` | scan.do_scan.down-long-with-1-hops | specified |
| `scan.do_scan.down-long-with-2-hops.path` | 85 | `down long with 2 hops` | scan.do_scan.down-long-with-2-hops | specified |
| `scan.do_scan.null-exit-destination-fails-next-iteration.path` | 87 | `null exit destination fails next iteration` | scan.do_scan.null-exit-destination-fails-next-iteration | blocked |
| `scan.do_scan.around-null-destination-is-safe.path` | 67 | `around null destination is safe` | scan.do_scan.around-null-destination-is-safe | specified |

## scan_list

[Source line 96](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/scan.c:96); ends at line 109. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_scan: `src/scan.c:62` (lexical_call_candidate).
- do_scan: `src/scan.c:67` (lexical_call_candidate).
- do_scan: `src/scan.c:90` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/scan.c:44` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `get_trust`, `can_see`, `scan_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `scan.scan_list.if.001` | 101 | `if (scan_room == NULL)` | scan.scan_list.null-room, scan.scan_list.empty, scan.scan_list.self-skipped, scan.scan_list.pc-invis-too-high, scan.scan_list.pc-invis-equality-visible, scan.scan_list.npc-bypasses-pre-filter, scan.scan_list.can-see-false, scan.scan_list.multiple-in-list-order | specified |
| `scan.scan_list.return.001` | 101 | `return;` | scan.scan_list.null-room | specified |
| `scan.scan_list.for.001` | 102 | `for (rch=scan_room->people; rch != NULL; rch=rch->next_in_room)` | scan.scan_list.empty, scan.scan_list.self-skipped, scan.scan_list.pc-invis-too-high, scan.scan_list.pc-invis-equality-visible, scan.scan_list.npc-bypasses-pre-filter, scan.scan_list.can-see-false, scan.scan_list.multiple-in-list-order | specified |
| `scan.scan_list.if.002` | 104 | `if (rch == ch)` | scan.scan_list.self-skipped, scan.scan_list.pc-invis-too-high, scan.scan_list.pc-invis-equality-visible, scan.scan_list.npc-bypasses-pre-filter, scan.scan_list.can-see-false, scan.scan_list.multiple-in-list-order | specified |
| `scan.scan_list.continue.001` | 104 | `continue;` | scan.scan_list.self-skipped | specified |
| `scan.scan_list.if.003` | 105 | `if (!IS_NPC(rch) && rch->invis_level > get_trust(ch))` | scan.scan_list.pc-invis-too-high, scan.scan_list.pc-invis-equality-visible, scan.scan_list.npc-bypasses-pre-filter, scan.scan_list.can-see-false, scan.scan_list.multiple-in-list-order | specified |
| `scan.scan_list.and.001` | 105 | `&& rch->invis_level > get_trust(ch)) continue;` | scan.scan_list.pc-invis-too-high, scan.scan_list.pc-invis-equality-visible, scan.scan_list.npc-bypasses-pre-filter, scan.scan_list.can-see-false, scan.scan_list.multiple-in-list-order | specified |
| `scan.scan_list.continue.002` | 105 | `continue;` | scan.scan_list.pc-invis-too-high | specified |
| `scan.scan_list.if.004` | 106 | `if (can_see(ch, rch))` | scan.scan_list.pc-invis-equality-visible, scan.scan_list.npc-bypasses-pre-filter, scan.scan_list.can-see-false, scan.scan_list.multiple-in-list-order | specified |
| `scan.scan_list.return.002` | 108 | `return;` | scan.scan_list.empty, scan.scan_list.self-skipped, scan.scan_list.pc-invis-too-high, scan.scan_list.pc-invis-equality-visible, scan.scan_list.npc-bypasses-pre-filter, scan.scan_list.can-see-false, scan.scan_list.multiple-in-list-order | specified |
| `scan.scan_list.null-room.path` | 101 | `null room` | scan.scan_list.null-room | specified |
| `scan.scan_list.empty.path` | 104 | `empty` | scan.scan_list.empty | specified |
| `scan.scan_list.self-skipped.path` | 104 | `self skipped` | scan.scan_list.self-skipped | specified |
| `scan.scan_list.pc-invis-too-high.path` | 104 | `pc invis too high` | scan.scan_list.pc-invis-too-high | specified |
| `scan.scan_list.pc-invis-equality-visible.path` | 104 | `pc invis equality visible` | scan.scan_list.pc-invis-equality-visible | specified |
| `scan.scan_list.npc-bypasses-pre-filter.path` | 104 | `npc bypasses pre filter` | scan.scan_list.npc-bypasses-pre-filter | specified |
| `scan.scan_list.can-see-false.path` | 104 | `can see false` | scan.scan_list.can-see-false | specified |
| `scan.scan_list.multiple-in-list-order.path` | 104 | `multiple in list order` | scan.scan_list.multiple-in-list-order | specified |

## scan_char

[Source line 111](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/scan.c:111); ends at line 127. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- scan_list: `src/scan.c:106` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/scan.c:46` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `PERS`, `sprintf`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `scan.scan_char.return.001` | 126 | `return;` | scan.scan_char.depth-1, scan.scan_char.depth-2, scan.scan_char.depth-3, scan.scan_char.pers-rechecks-visibility, scan.scan_char.pers-visible-npc, scan.scan_char.pers-visible-pc | specified |
| `scan.scan_char.depth-1.path` | 121 | `depth 1` | scan.scan_char.depth-1 | specified |
| `scan.scan_char.depth-2.path` | 121 | `depth 2` | scan.scan_char.depth-2 | specified |
| `scan.scan_char.depth-3.path` | 121 | `depth 3` | scan.scan_char.depth-3 | specified |
| `scan.scan_char.around-depth-zero-negative-door-undefined.path` | 121 | `around depth zero negative door undefined` | scan.scan_char.around-depth-zero-negative-door-undefined | blocked |
| `scan.scan_char.pers-rechecks-visibility.path` | 119 | `pers rechecks visibility` | scan.scan_char.pers-rechecks-visibility | specified |
| `scan.scan_char.pers-visible-npc.path` | 119 | `pers visible npc` | scan.scan_char.pers-visible-npc | specified |
| `scan.scan_char.pers-visible-pc.path` | 119 | `pers visible pc` | scan.scan_char.pers-visible-pc | specified |

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

## Static tables

- `distance` at line 39 — pending entry/termination review.

## Commented code candidates


# ROM2.4 whole-codebase code-path report

**Status: partial behavioral specification; whole-source lexical inventory. The requested complete semantic trace is unfinished.**

Source: `C:\Users\scott\PycharmProjects\PyRom\Rom24`. HEAD reference: `d3a29007355e7298e0033fcb666e9a6895c2146f`. Per-file hashes identify the inspected snapshot. Normal Git status is unavailable; the manifest records an independent comparison against HEAD content. Generated 2026-10-31.

## Coverage and evidence

| Measure | Count |
|---|---:|
| source files | 43 |
| translation units | 30 |
| source lines | 46516 |
| functions inventoried | 677 |
| functions with cases | 49 |
| functions completely traced | 0 |
| cases specified | 430 |
| cases blocked | 2 |
| cases dynamically verified | 0 |
| lexical sites pending | 10796 |
| ancillary files inventoried | 485 |

No executable branch coverage, whole-server parity, successful C build, or passing gameplay tests is claimed. Every file/function/site has an explicit pending or specified disposition in the manifest; pending sites are work remaining, not exclusions.

## Artifacts

- [Pseudo suite](pseudo-suite.md): readable Arrange/Act/Assert contracts.
- [Case catalog](cases.json): portable structured expectations.
- [Coverage manifest](manifest.json): hashes, function inventory, call candidates, macros, preprocessor alternatives, tables, data inventory, and pending work.
- [Tracing notes](tracing-notes.md): helper contracts, source quirks, configuration risks and Python adaptation.

- [Validation results](verification.json): snapshot, link and structural checks; no gameplay execution.

## File inventory

| File | Lines | Definitions | Disposition |
|---|---:|---:|---|
| [src/act_comm.c](files/act_comm.c.md) | 1999 | 42 | pending |
| [src/act_enter.c](files/act_enter.c.md) | 214 | 2 | partially_specified |
| [src/act_info.c](files/act_info.c.md) | 2755 | 54 | pending |
| [src/act_move.c](files/act_move.c.md) | 1640 | 24 | pending |
| [src/act_obj.c](files/act_obj.c.md) | 2989 | 29 | pending |
| [src/act_wiz.c](files/act_wiz.c.md) | 4378 | 69 | pending |
| [src/alias.c](files/alias.c.md) | 273 | 4 | partially_specified |
| [src/ban.c](files/ban.c.md) | 309 | 7 | partially_specified |
| [src/comm.c](files/comm.c.md) | 2572 | 23 | pending |
| [src/const.c](files/const.c.md) | 2125 | 0 | pending |
| [src/db.c](files/db.c.md) | 3372 | 56 | partially_specified |
| [src/db.h](files/db.h.md) | 52 | 0 | pending |
| [src/db2.c](files/db2.c.md) | 493 | 3 | pending |
| [src/effects.c](files/effects.c.md) | 621 | 5 | pending |
| [src/fight.c](files/fight.c.md) | 3095 | 36 | pending |
| [src/flags.c](files/flags.c.md) | 249 | 1 | partially_specified |
| [src/handler.c](files/handler.c.md) | 2912 | 87 | partially_specified |
| [src/healer.c](files/healer.c.md) | 196 | 1 | partially_specified |
| [src/interp.c](files/interp.c.md) | 796 | 9 | partially_specified |
| [src/interp.h](files/interp.h.md) | 298 | 0 | pending |
| [src/lookup.c](files/lookup.c.md) | 106 | 5 | partially_specified |
| [src/lookup.h](files/lookup.h.md) | 32 | 0 | pending |
| [src/magic.c](files/magic.c.md) | 4699 | 105 | partially_specified |
| [src/magic.h](files/magic.h.md) | 130 | 0 | pending |
| [src/magic2.c](files/magic2.c.md) | 174 | 3 | partially_specified |
| [src/Makefile](files/Makefile.md) | 22 | 0 | pending |
| [src/Makefile.linux](files/Makefile.linux.md) | 19 | 0 | pending |
| [src/Makefile.normal](files/Makefile.normal.md) | 18 | 0 | pending |
| [src/Makefile.solaris](files/Makefile.solaris.md) | 19 | 0 | pending |
| [src/merc.h](files/merc.h.md) | 2322 | 0 | pending |
| [src/music.c](files/music.c.md) | 350 | 3 | pending |
| [src/music.h](files/music.h.md) | 43 | 0 | pending |
| [src/note.c](files/note.c.md) | 960 | 17 | pending |
| [src/recycle.c](files/recycle.c.md) | 652 | 29 | pending |
| [src/recycle.h](files/recycle.h.md) | 112 | 0 | pending |
| [src/save.c](files/save.c.md) | 1665 | 9 | pending |
| [src/scan.c](files/scan.c.md) | 127 | 3 | partially_specified |
| [src/skills.c](files/skills.c.md) | 1069 | 14 | pending |
| [src/special.c](files/special.c.md) | 1042 | 25 | partially_specified |
| [src/tables.c](files/tables.c.md) | 322 | 0 | pending |
| [src/tables.h](files/tables.h.md) | 81 | 0 | pending |
| [src/telnet.h](files/telnet.h.md) | 87 | 0 | pending |
| [src/update.c](files/update.c.md) | 1127 | 12 | partially_specified |

## Coverage criterion and continuation

Case selection distinguishes observable guard outcomes, ordered failures, string and arithmetic boundaries, loop cardinalities, mutation order and caller-versus-helper contracts. It does not enumerate a Cartesian product of all game states. The lexical index includes explicit control transfers and short-circuit operators but cannot establish feasibility or find every implicit branch.

Continue from `manifest.json`, keeping current case IDs. First resolve syntax sites in functions already carrying cases; then process command dispatch/session handling, movement/objects/combat, magic/effects, update/persistence, content loaders and specials. Load-dependent area/data contracts and platform branches remain in scope. Do not mark a function complete solely because it has one case.

Reproduction: `python docs/reports/rom24-code-paths/whole-codebase/build_report.py`. The renderer checks structure and source line bounds; manual source review is still required for behavioral correctness. It reads the C checkout and writes only this report directory.

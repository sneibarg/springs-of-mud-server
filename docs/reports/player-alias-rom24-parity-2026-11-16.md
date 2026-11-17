# ROM24 parity review of player command aliases

This review covers the bundled `alia`, `alias`, and `unalias` commands and single-pass player alias expansion. It follows aliases through listing, lookup, creation, redefinition, removal, the five-entry limit, switched control, and the 255-character expansion boundary. The archived interpreter reviews sampled alias dispatch and examined command prefixes. This review focuses on alias management and leaves the separate `prefix` command policy outside scope. [Prior interpreter review](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/archive/repository-rom24-parity-2026-10-31-third-review.md:75)

## Confirmed defect

### Alias management edits the switched mobile while expansion reads the player

Start with `alias x say original`, then switch into a mobile and run `alias`, `alias x`, and `alias x say switched`. ROM24 lists and queries the original player's aliases and updates that player's `x`. The switched mobile executes `say switched` when the player types `x`. In Springs, the first two commands report an empty list and an undefined alias. The third confirms that it set `x`, but it writes `{'x': 'say switched'}` to the mobile's context. Typing `x` still executes `say original`. A subsequent `unalias x` confirms removal of the mobile's entry while the original player's alias remains active. This also makes guard results such as the capacity check depend on the mobile's entries. [ROM24 ownership for alias](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:110) · [ROM24 ownership for unalias](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:208) · [Springs alias and unalias handlers](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:99) · [Springs guard lookup and storage](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:73) · [Springs expansion owner](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:124)

## Verified differences with unresolved design intent

### Replacement validation reverses the prefix comparison

ROM24 tests whether the **entire replacement** is a case-insensitive prefix of the literals `delete` or `prefix`. Springs extracts the first token and tests whether that token **begins with** either literal. The denial happens before modifying the alias in both implementations. The table compares entering each replacement as `alias q <replacement>` with an available slot. The Springs column was reproduced through the public interpreter. [ROM24 predicate](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:173) · [ROM24 prefix helper](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3164) · [Springs predicate](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:83) · [Springs guard registration](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:3275)

| Replacement | ROM24 | Springs |
| --- | --- | --- |
| `delete` or `prefix` | Rejects | Rejects |
| `del` or `pre` | Rejects | Stores |
| `delete now` or `prefix say` | Stores | Rejects |
| `deletefile` | Stores | Rejects |

### The raw-input gate changes which alias names can expand

ROM24 runs a case-insensitive raw-prefix check before parsing the first word. With `alias aliasfoo say hit`, both implementations store the alias. ROM24 skips expansion when the player types `aliasfoo` because the line starts with `alias`. Springs checks the parsed token for exact equality with `alias`, so it executes `say hit`. With `alias x say hit`, ROM24 skips that alias on either `  x again` or `"x" again` because neither raw line starts with `x`. Springs expands both to `say hit again`. ROM24 preserves printable leading spaces at descriptor input. The Springs Telnet text decoder strips outer whitespace before interpretation, and the alias parser also trims it when called directly. [ROM24 raw gate and exact match](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:60) · [ROM24 descriptor input](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1127) · [Springs substitution](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:151) · [Springs argument parser](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/InterpUtil.py:44) · [Springs text decoder](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/protocol/MessageCodec.py:45)

### Tildes are rewritten before ROM24 parses an alias definition

`alias w~ say hi~` creates the key `w-` and replacement `say hi-` in ROM24. The same input creates `w~` and `say hi~` in Springs, and invoking `w~` retains the tilde in speech. The C rewrite occurs before parsing, so it affects lookup input as well as stored values. ROM24 saves the replacement with a tilde terminator. Springs serializes the alias map with its character data, so it can represent literal tildes. [ROM24 definition entry](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:104) · [ROM24 rewrite](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3116) · [ROM24 save format](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:282) · [Springs parser](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:27) · [Springs serialization](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:128)

### A switched player sees the truncation warning in Springs

For a 244-character ASCII replacement plus a space and an 11-character argument, both implementations truncate the 256-character expansion to 255 and dispatch it. At exactly 255 characters there is no truncation warning. In ROM24's switched case, the warning is sent to the original player object, whose descriptor was cleared by `switch`, so it produces no output. Springs routes the warning to the switched mobile's bound connection before dispatch. The probe used the same ASCII input both in the original body and while switched. [ROM24 limit and recipient](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:80) · [ROM24 descriptor transfer](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2234) · [ROM24 send behavior](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2337) · [Springs truncation](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:159) · [Springs warning delivery](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/InterpHandler.py:61)

## Matching paths

- For an unswitched player, empty listing, lookup, and removal prompts use the corresponding authored responses. The explicit `alia` entry instructs the player to use the full command. Removal consumes the first argument and preserves the order of surviving entries. Both implementations reject exact `alias` and names beginning with `una` during definition or lookup. [ROM24 alias management](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:98) · [ROM24 removal](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:223) · [Springs handlers](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:95) · [Springs reserved-name rule](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:73)
- A player with five entries can redefine an existing alias in place. The sixth new definition is rejected until a slot is freed. Alias expansion preserves interior spacing in the remainder and runs once before dispatch. A replacement that names a second alias receives ordinary command lookup. [ROM24 capacity and redefinition](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:179) · [ROM24 expansion and dispatch](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:70) · [Springs capacity and mutation](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:89) · [Springs dispatch](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/InterpHandler.py:73)

## Validation

Ruff ran in read-only mode against three entry-point files with concise output and against three supporting files with rule counts. Its diagnostic at the replacement guard directed the first targeted read. The ROM24 comparison established the reversed prefix semantics. Collection queries checked only the relevant command documents. Public-interpreter probes exercised the bundled guards and payloads with a real message bus and test connections. All 86 focused tests passed across six isolated invocations, including alias save/reload, input spacing, switched expansion, and command authorization. The initial combined invocation encountered an injector stub shared across suites, so each suite was rerun in its own process.

ROM24 expectations came from the local C source. The probes ran the Springs interpreter with test connections. Live socket gameplay, unusual alias names across ROM24 save/reload, and command-prefix policy were outside this review.

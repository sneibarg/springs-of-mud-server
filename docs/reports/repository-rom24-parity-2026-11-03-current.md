# ROM24 parity review of the current working tree

November 3, 2026. Python HEAD is `40949b8`, with the five visibility and inspection fixes present as working-tree changes. The comparison uses the local ROM24 C checkout. This review adds only its report and the isolated test results.

## Gameplay findings

### P2 — Automatic exits disclose directions from a pitch-black room

A mortal with AUTOEXIT and no holy light looks around a pitch-black room or receives an automatic room view after entering it. ROM24 displays the darkness notice and eligible occupants, then returns before rendering exits. Python's room renderer reports a blocked view by returning false, but the two callers continue to automatic exits. That helper gates blindness and destination visibility, so open routes can still be listed even though the current room is pitch black. Standalone `exits` has a separate C path and should retain that distinction.

[ROM24 act_info.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1011) · [RoomHandler.py](../../src/area/RoomHandler.py#L92) · [Info.py](../../src/interp/commands/Info.py#L175) · [PlayerHandler.py](../../src/player/PlayerHandler.py#L1031)

### P2 — Base damage messages reach sleeping bystanders

An unrelated sleeping player shares a room with a fight. ROM24 dispatches the ordinary room damage line through `act`, whose default minimum position is resting. Python's round payload excludes the two combatants from its room target list but applies no posture gate. A production renderer and round-builder probe put a sleeping character in the payload's target list. Recipient-aware substitution can hide a name, but the sleeping character still receives the combat line.

[ROM24 fight.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2071) · [ROM24 merc.h](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1841) · [ROM24 comm.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475) · [CombatHandler.py](../../src/combat/CombatHandler.py#L1270)

### P3 — Self-damage creates two direct combat messages

When an actor damages themself, ROM24 uses a self-directed actor line and a room line, with no separate victim delivery. Springs renders the actor as a separate opponent in all three channels and puts the same player into both direct channels. With ten points of ordinary self-damage, the production builder returned `You hit Alice.` and `Alice hits you.` for Alice, and `Alice hits Alice.` for the room. ROM24 also handles self-targeted skill nouns and immunity explicitly.

[ROM24 fight.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2010) · [CombatHandler.py](../../src/combat/CombatHandler.py#L527) · [CombatHandler.py](../../src/combat/CombatHandler.py#L1280)

### P3 — Explicit look obeys brief mode

A sighted player with BRIEF enabled types a bare `look`. ROM24 always includes the description for a bare look and applies the BRIEF check to automatic room views. Both Python paths call the same room renderer without passing the view mode, so both suppress the description. The distinction lets a player keep movement output short while asking for a description on demand.

[ROM24 act_info.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1038) · [Info.py](../../src/interp/commands/Info.py#L175) · [RoomHandler.py](../../src/area/RoomHandler.py#L99)

### P3 — Explicit exits suppress vnums for immortals without holy light

ROM24 includes destination vnums in explicit exits for immortals, independently of holy light. Springs uses the general room-heading vnum predicate for explicit exits as well. A sighted immortal with holy light off therefore loses vnums from the exit list. The stricter predicate is appropriate for ROM24's ordinary room heading.

[ROM24 act_info.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1359) · [RoomHandler.py](../../src/area/RoomHandler.py#L74) · [Room.py](../../src/area/Room.py#L344)

## Validation

The isolated run covered 136 top-level unittest modules and reported 1,655 tests. Of those modules, 122 passed and 14 failed, with no timeouts. The public-path regression for the previous five findings passed. Compared with the October 31 snapshot, two more modules fail. Three errors in those modules arise from fixture interfaces exercised by the recent fixes.

- Room extra inspection supplies a SimpleNamespace where the chain walker expects its canonical model or serialized data.
- Two poison/plague tests supply room stubs with `players_in_room` but without the `player_targets` interface used for recipient filtering. The public-path poison regression uses a production Room and passed.

These are observed test compatibility failures. The normal room loader supplies the canonical extra-description model, and production rooms implement the listener interface. Existing failures, including the energy-drain assertions and command authorization assertion, remain visible in the [complete test output](repository-rom24-parity-2026-11-03-current-tests.json). Their presence alone does not establish additional gameplay discrepancies.

## Review coverage

This review paired a repository-wide regression sweep with source comparison of the affected gameplay paths. It used the prior [family-by-family coverage matrix](repository-rom24-parity-2026-10-31-third-review.md#repository-coverage) for historical coverage of all 30 C translation units. In this pass, combat rendering, room views, periodic effects, room extras and switched channel preferences received targeted source or runtime verification. Automatic escape and outdoor darkness were checked against the reference ordering and predicates. Object and shop behavior, skills and spell targeting, mobile specials, progression, resets, communication, notes, administrator commands, weather, and session lifecycle received current suite coverage, with the module-level exceptions in the test results.

This is repository-wide at the regression-suite level. It is not a fresh branch-by-branch audit of every subsystem or every authored record. The review did not compare complete area snapshots, run a compiled C server, or exercise live content services. Earlier unresolved differences in command-prefix policy, idle/limbo behavior, pose eligibility, and offline recovery still need policy or service-contract evidence.

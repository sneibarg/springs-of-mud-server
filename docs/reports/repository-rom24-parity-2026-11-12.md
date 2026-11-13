# Repository-wide ROM24 parity review

November 12, 2026. Reviewed the Springs of MUD working tree at `612b0d8cb3553ff22f3a81b485874f1d14582ea2`, including edits already present in that checkout, against the local `PyRom/Rom24/src` reference. The review surveyed the repository and traced selected gameplay paths in depth.

| Priority | Finding | Player impact |
| --- | --- | --- |
| P1 | F01 · An empty or unknown `cast` ends the gameplay session | Ordinary input reaches the connection loop's fatal error path. |
| P1 | F02 · Killing a possessed NPC leaves its controller attached to the removed body | The session continues taking input for a body that has left the world. |
| P1 | F03 · Death leaves stale pet and follower relationships | A dead pet can block replacement, and a player's live pet survives their death. |
| P2 | F04 · A purchased pet disappears after a saved quit and fresh login | The runtime save/load path loses a paid-for companion that ROM restores. |
| P2 | F05 · Ending combat can stop a separate fight in the same room | An unrelated combatant loses its target and turn in a three-way fight. |
| P2 | F06 · A master can hit a charmed follower without breaking charm | The follower enters combat while still eligible for the master's orders. |
| P2 | F07 · Player death ignores the configured clan hall | All three shipped clans respawn at room 3001 instead of their configured room 3054. |

P1 covers loss of a gameplay session or invalid live character ownership. P2 covers material changes to progression, combat, or travel under a narrower trigger.

## F01 · Empty or unknown casts end the gameplay session

**Trigger and result.** Enter `cast` or `cast unrecognized-spell`. ROM24 returns the missing-argument or unknown-spell response before charging mana or wait. The shipped Springs command already defines `noArgument` and `spellNotLearned`, but the handler reads `spell.target` before evaluating them. The lookup produces `None` for both inputs. The production interpreter probe raised `AttributeError` for each. The executor classifies it as a runtime-helper exception, and the connection loop catches it and breaks. Socket closure was traced through the enclosing connection handler.

**Fix boundary.** Let the existing early guards handle missing spell definitions before target-dependent checks. Test both inputs through the normal command route, then issue a valid command in the same session. Keep spell-specific guard ordering for resolved spells.

[ROM24 cast validation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:316) · [Cast handler](../../src/interp/commands/Fight.py#L104) · [Player dispatch](../../src/player/PlayerHandler.py#L754) · [Executor exception handling](../../src/interp/CommandExecutor.py#L83) · [Connection loop](../../src/server/handlers/ConnectionHandler.py#L373)

## F02 · Death of a possessed NPC leaves its controller in the removed body

**Trigger and result.** An immortal switches into an NPC that then dies. ROM24's lethal path calls full extraction, which invokes `do_return` for a switched body and restores the original descriptor binding. Springs removes the mobile from its room and registry without calling `WizHandler.return_character`. A probe using the real switch operation, session registry, room models and `raw_kill` left `session.character` pointing to the removed mobile. The game loop uses that reference for later commands.

**Fix boundary.** Reuse possession cleanup at the NPC death extraction boundary, after corpse creation and with existing kill accounting preserved. Cover death through ordinary damage and `slay`, including connection rebinding and the next command running as the original character.

[ROM24 lethal NPC extraction](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1660) · [ROM24 extraction calls return](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1967) · [ROM24 descriptor rebinding](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2273) · [NPC death](../../src/combat/CombatHandler.py#L571) · [Existing extraction cleanup](../../src/util/EntityExtractor.py#L17) · [Session rebinding](../../src/game/WizHandler.py#L106)

## F03 · Death leaves stale pet and follower relationships

**Trigger and result.** In ROM24, extraction removes the victim's owned pet before branching between player respawn and full NPC extraction. Full extraction also clears follower relationships, including the owner's pet pointer if the victim is the pet. Springs' death handler takes separate room/registry removal and player-respawn paths that skip both steps. The probes observed three outcomes.

- When the owner died, the player respawned and their live pet stayed in the old room with ownership intact.
- When that pet died, its owner still pointed to the removed pet. The shipped pet-buy guard rejects a player with a nonempty pet slot.
- When an NPC master died, a surviving follower retained both its master and leader links to the removed mobile.

**Fix boundary.** Share the relevant extraction operations with the death path. Preserve ROM24's distinction between full NPC extraction and player respawn, where ordinary follower cleanup is conditional and the owned pet is always removed. Cover corpse creation, pet replacement, and follower/group cleanup after each type of death.

[ROM24 common pet cleanup and conditional follower cleanup](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1939) · [ROM24 pet removal](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1566) · [ROM24 follower cleanup](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1584) · [Death path](../../src/combat/CombatHandler.py#L571) · [Existing relationship cleanup](../../src/util/EntityExtractor.py#L25) · [Pet purchase preparation](../../src/interp/commands/Object.py#L1061)

## F04 · Purchased pets disappear after a saved quit and fresh login

**Trigger and result.** Quit successfully with a purchased pet in the same room and log in again. ROM24 saves the co-located pet, reconstructs its master and leader links on load, and places it with the owner on login. Springs' purchase creates a live mobile and sets the ownership links. The character snapshot omits the pet, then successful quit extracts the live pet. A direct production serializer/deserializer round trip produced no pet record and no restored pet.

**Fix boundary.** Establish the character service contract for an optional pet snapshot and restore it on fresh world entry. Verify a paid purchase through successful quit, fresh authentication and pet restoration. Cover an absent or distant pet and a link-dead reconnect to the existing live character. The runtime omission was reproduced locally. The service schema and deployed save/load behavior remain unverified.

[ROM24 co-location save condition](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:149) · [ROM24 restores ownership](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:1267) · [ROM24 login placement](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2123) · [Purchase](../../src/area/Shop.py#L251) · [Character serializer](../../src/player/CharacterService.py#L88) · [Successful quit extraction](../../src/player/PlayerHandler.py#L119)

## F05 · Ending combat can stop a separate fight

**Trigger and result.** A targets B while B and C target each other. A successfully flees, recalls, or otherwise triggers `stop_fighting(A, both=True)`. ROM24 clears A and anyone targeting A, so B and C keep fighting. Springs unconditionally adds A's outgoing opponent, B, to the set of participants to clear. The production stop helper left A and B idle while C still targeted B. This can cancel B's next turn and change the outcome of combat between B and C.

**Fix boundary.** Select A and incoming combat links for the shared stop operation. Retain mutual-duel cleanup and verify three-way cases for flee and recall. Keep combat-event and posture updates consistent with the links that were actually cleared.

[ROM24 stop selection](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1405) · [ROM24 flee caller](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2853) · [Python stop selection](../../src/combat/CombatHandler.py#L410) · [Flee caller](../../src/interp/commands/Fight.py#L337) · [Recall caller](../../src/interp/commands/Movement.py#L376)

## F06 · Hitting one's own charmed follower leaves charm active

**Trigger and result.** A player hits their own charmed non-pet NPC in a room where combat is allowed. ROM24 starts combat and calls `stop_follower` before damage modifiers and the zero-damage exit. That helper strips the charm affect and clears the master and leader links. Springs starts combat and proceeds directly to invisibility and damage handling. A production `damage` boundary probe with a zero-damage hit retained the charm effect and both ownership links while setting the follower's combat target to the master. The order selector still treats an in-room charmed follower with that master as eligible.

**Fix boundary.** Apply the follower break in the shared damage transition after safety checks. Cover a missed attack, a damaging hit, safety rejection, and a charmed target owned by someone else.

[ROM24 damage follower break](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:736) · [ROM24 charm and ownership cleanup](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1538) · [Python damage entry](../../src/combat/CombatHandler.py#L867) · [Order target selection](../../src/api/CommunicationsApi.py#L236)

## F07 · Player death ignores the configured clan hall

**Trigger and result.** A clanless player or a member of `loner` or `rom` dies while both temple rooms are loaded. ROM24 relocates the player to their clan's hall, room 3054 for all three shipped records. The Springs GameData snapshot has those same hall values and the room snapshot includes both destinations. The Python death path hard-codes 3001, the ordinary recall temple. A probe with both rooms loaded sent all three players to 3001.

**Fix boundary.** Resolve the death destination from the authored clan catalog. Cover clanless, independent and regular clans, a custom hall, and a missing hall. The C relocation helper falls back to the temple if the requested room cannot be resolved. Recall uses its separate temple destination.

[ROM24 death relocation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1958) · [ROM24 hall table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/tables.c:40) · [ROM24 fallback](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1382) · [Python respawn](../../src/combat/CombatHandler.py#L1919) · [GameData clan catalog loader](../../src/game/GameData.py#L58)

## Coverage and validation

The inventory covered 215 Python source files, 30 ROM24 C translation units and 17 collection snapshots. Fresh comparisons concentrated on the state transitions below. Test coverage is broader than the fresh source tracing.

| Area | Evidence reviewed |
| --- | --- |
| Commands and spells | Cast entry, authored guards, spell lookup, direct command dispatch and the socket error path. Also sampled offensive retaliation, item-cast targeting and gate/teleport relocation. |
| Combat, effects and advancement | Damage setup, combat teardown, death, corpse order, pet/follower ownership, group reward dispatch, periodic damage and combat escape checks. Existing learning, reward, condition and defense suites exercised the wider subsystem. |
| Travel, rooms and world updates | Recall/flee call sites, room membership, area/reset and pulse ordering, light extinction, mayor gate actions and mobile-special notices. |
| Items, shops and persistence | Buy guards, pet creation, character serialization and quit/entry, plus sampling of shop stock, item resets and corpse ownership. |
| Communication, notes and administration | Follower orders, group/money helpers, clan-note routing, possession, ordinary extraction and slay. Broader communication and administrator branches received existing regression coverage. |
| Reference infrastructure | Inventoried legacy area conversion, C storage helpers and jukebox/music. The review made no parity determination for those paths. |

- **1,711 tests passed across all 137 top-level unittest modules.** Each module ran in its own Python process using the repository virtual environment. An initial sandboxed run hit Windows asyncio loopback timeouts. The subsequent loopback-enabled run passed 130 modules with 1,517 tests. Seven modules needed `src` on `PYTHONPATH` and passed on rerun with 194 more tests. The legacy tests in `tests/old-tests` were outside the sweep.
- Read-only probes used real character, mobile, room, combat, session, interpreter and serialization code with controlled fixtures. Death probes called `raw_kill` directly with corpse creation and death notices stubbed. The combat-stop probe exercised the helper, with caller paths verified by reading source. The charm probe exercised damage setup with safety and downstream damage controlled. The cast probe executed the shipped command lambda through the public interpreter, with disconnect behavior verified by reading the socket path.
- The five November 6 findings have passing coverage in the current checkout for reciprocal mayor gates, described-door status, clanless criminal flag cleanup, lamp extinction and NPC-special visibility. [Previous report](repository-rom24-parity-2026-11-06.md) · [Current regression tests](../../tests/test_rom24_report_fixes.py)
- The collection CLI verified the shipped cast and buy guards, the clan catalog and both room records. Remote service responses, every authored command/spell/reset branch, live gameplay and executable C differential tests were outside this review. Command-prefix policy, idle limbo and offline recovery remain unresolved design or service questions.

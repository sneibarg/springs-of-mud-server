# ROM24 gameplay review — 2026-10-29

**N01–N07 are resolved; none of this review's seven findings remains open.** Gameplay must match the local ROM24 source; Python architecture and designer-managed content are not themselves findings. Earlier G01–G28 and R01–R15 remediation is historical and is not reopened here. The initial review changed no runtime, collection, or test implementation. The subsequently authorized remediation below changes runtime code and tests; original descriptions and line anchors retain the pre-remediation evidence.

## Remediation — N01–N07 resolved

- **N01:** Permanent effects receive the reference's 25-point resistance adjustment (five spell levels), with the original clamping and strict roll boundary preserved.
- **N02:** NPC thief backstab accuracy uses the same level-based proficiency, daze adjustment and clamp as activation; non-thief proficiency remains zero.
- **N03–N04:** The thief special executes configured backstab/murder commands and the existing physical flee command. Opening attacks finish the special so a combat turn is not also taken during the same pulse. Murder now resolves its existing melee action definition instead of looking for a nonexistent murder skill. The command payloads use the existing mobile-to-standard-emitter integration. Fight commands are injected through the existing Bootstrapper binding.
- **N05:** Spell world targeting reuses the existing visible live-world lookup, preserving local priority, world ordinal counting and exclusion of retired/offline entities. Summon/gate relocate entities and portal/nexus create their exits through their existing spell operations.
- **N06:** Specific immunity, resistance and vulnerability resolve in the reference's exclusive priority order; generic defense fallbacks remain intact.
- **N07:** Condition gains/decay and lamp consumption use actual immortal level. Trust-based privileges elsewhere retain their existing behavior.

Changes are focused runtime corrections using existing capabilities, with no new attribute-existence guards or collection rewrites. **23 regressions** in `tests/test_remaining_gameplay_parity.py` cover roll endpoints/clamps, permanent effect removal and raw flags, NPC proficiency, all eight defense-flag combinations and spell saves, local/world visibility and ordinal lookup, actual spell documents and real movement/portal creation, trust/level boundaries, thief backstab/fallback/miss behavior, successful/failed flee, purse and idle behavior. Two existing test fixtures were updated to represent actual immortal levels rather than the old trust-based exemption.

**Final validation:** 115 modules ran in isolated processes with `src` on `PYTHONPATH`. **105 modules / 1,179 tests pass**, with 1,464 cases reported overall. Every previously passing module remains green; the same 10 baseline modules retain exactly their previous failure/error counts. [Remediation results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/remaining-gameplay-remediation-2026-10-29-tests.json). `git diff --check` passes. The historical discrepancy probes are retired in favor of these regressions. No live server or content-service deployment was performed.

## Spells and defense resolution

### N05 (resolved) — P1: Named world-target spells always fizzle

Python: [SpellApi.py:1577](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:1577), [PlayerUtil.py:180](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/PlayerUtil.py:180), exception handling [SpellApi.py:82](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:82).
C: [magic.c:2888](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:2888), [magic.c:4319](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4319), [magic2.c:61](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic2.c:61), [magic2.c:113](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic2.c:113).

The shared world lookup passes four arguments to `PlayerUtil.get_target`, which accepts three. A nonempty target and populated room registry therefore raise `TypeError`; spell execution catches it and fizzles instead of resolving the target. The probe reproduced this using all four actual spell documents: **summon, gate, portal, nexus**. C resolves a visible world character before evaluating each spell's restrictions. Normal casting has already charged mana and wait before this failure.

### N01 (resolved) — P2: Permanent effects are too easy to dispel

Python: [EffectUtil.py:175](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/EffectUtil.py:175).
C: [magic.c:239](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:239).

For duration `-1`, C adds five to the **spell level**, giving 25 additional resistance points before clamping. Python adds only five resistance points. With equal level-20 caster/effect and roll 60, Python removes permanent sanctuary; C resists at threshold 75 and weakens the effect to level 19. The production effect-handler probe confirms removal. Dispel magic, cancellation, and permanent sanctuary's raw-flag fallback use the affected calculation.

### N06 (resolved) — P2: Vulnerability incorrectly reduces explicit immunity or resistance

Python: [CombatHandler.py:1836](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:1836).
C: [handler.c:308](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:308).

When a damage type has overlapping defense flags, C's `if/else if` gives immunity precedence over resistance and vulnerability. Python processes vulnerability afterward: fire immunity plus fire vulnerability becomes **resistant**, and fire resistance plus fire vulnerability becomes **normal**. Both combinations were reproduced with real status flags. This changes damage and spell saves. Valid overlapping runtime flags are sufficient to trigger it; no claim is made that a particular bundled mobile starts with this combination.

## NPC combat and the thief special

### N02 (resolved) — P2: NPC backstab uses zero proficiency for THAC0

Python: [CombatHandler.py:1533](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:1533), consumer [CombatHandler.py:1801](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:1801).
C: [handler.c:420](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:420), [fight.c:472](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:472).

The combat-local NPC skill reader implements second/third attack only, returning zero for backstab. C gives an ACT_THIEF mobile `20 + 2 * level`, subject to condition penalties and clamping. A level-20 thief correctly receives 60 proficiency from Python's activation API, but the hit calculation subtracts **1,000 THAC0 instead of C's 400**. This inflates accuracy against sufficiently armored targets. R13's corrected multiplier remains correct; this is a different input-path defect.

### N03 (resolved) — P2: The thief special opens with ordinary attacks instead of backstab

Python: [MobileApi.py:541](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/MobileApi.py:541), [MobileApi.py:266](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/MobileApi.py:266).
C: [special.c:333](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:333).

For a victim one to nine levels above a nonfighting `spec_nasty` mobile, C invokes backstab, then murder only if the mobile still is not fighting. Python ignores the configured `skills=['backstab', 'murder']` argument and directly invokes ordinary `multi_hit(TYPE_UNDEFINED)`. The probe recorded that actual call. This bypasses backstab's prerequisites, proficiency roll, accuracy and damage multiplier. The bundled assignment is mobile **3163**.

### N04 (resolved) — P2: The thief special's flee action never moves

Python: [MobileApi.py:554](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/MobileApi.py:554), especially line 568.
C: [special.c:374](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:374), [fight.c:2802](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2802).

When `spec_nasty` chooses flee, C runs `do_flee`, attempting exits and stopping both combat links on success. Python only stops the mobile's combat link and marks the action performed. The probe leaves the thief in its original room without attempting travel. It therefore neither escapes nor retains combat when all exits fail, as C would. The ordinary flee command's previous fixes do not reach this caller.

## Character ticks

### N07 (resolved) — P2: Trusted mortals stop consuming conditions and lamp fuel

Python: [Character.py:397](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/Character.py:397), [Character.py:407](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/Character.py:407), [Character.py:428](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/Character.py:428); trust predicate [CharacterApi.py:130](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/CharacterApi.py:130).
C: [update.c:337](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:337), [update.c:662](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:662).

C exempts characters by actual level in these paths. Python calls `is_immortal`, which uses trust. A level-20 character trusted to level 52 retains hunger/thirst/drunkenness/fuel **10/10/12/3** after a tick; C produces **9/9/11/2**. The probe confirms the Python result. Other trust-based immortal privileges are not implicated by this finding.

## Scope and validation

The repository inventory contains **214 Python source files and 17 collection snapshots**, including 221 commands, 38 skills, 97 spells, 986 mobiles, 1,266 items, 3,127 rooms and 5,196 resets. Collection inspection used collection-query before focused extraction.

Fresh traces sampled gameplay across command dispatch/authorization, learning and advancement, current stats/carrying, equipment/effects/visibility, movement/followers/escape/portals, area reset ownership, mobile construction/scheduling/specials, combat accuracy/defenses/damage/death, spell primitives and authored spell lambdas, consumables/transfers/shops, elemental exposure, regeneration/conditions/light, weather and persistence boundaries. The earlier medium/small NPC stat fix and separate NPC THAC0 class priority were retained. Presentation, architecture, networking and tooling differences were excluded unless they alter gameplay.

**At review time, all seven deterministic production-method probes reproduced**, including actual world-target spell document execution. Run [the probe script](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-gameplay-review-2026-10-29-probes.py) from the checkout with `.venv/Scripts/python.exe`. Their historical bodies describe the original discrepancies; all seven are now skipped, with current behavior validated by the regression module above. C expectations were traced from source; no C executable differential harness was run.

The suite ran in **114 isolated module processes**, with `src` on `PYTHONPATH`: **104 modules / 1,156 tests pass**, with 1,441 cases reported overall, including an import-failure placeholder. The same 10 baseline failing modules retain their exact failure/error counts; comparison against the preceding entry/following artifact found no status/count changes for existing modules. Full results: [test artifact](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-gameplay-review-2026-10-29-tests.json). No live server or content service was exercised. This is a repository-wide review with focused behavioral traces, not proof of exhaustive equivalence for every state or authored content combination.

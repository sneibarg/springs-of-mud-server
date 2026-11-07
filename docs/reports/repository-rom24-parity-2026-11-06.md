# Repository ROM24 behavioral parity review

November 6, 2026. Reviewed Python HEAD `2c15d2e14d2acff08825bcb3d484195c4300eb17` against `C:/Users/scott/PycharmProjects/PyRom/Rom24/src`.

**Five verified behavioral mismatches need resolution: four P2 issues and one P3 issue.** This review changes documentation and evidence scripts only. It leaves runtime code, collections, the C reference, and the pre-existing working-tree changes under `rom24-code-paths/whole-codebase` untouched.

The scope is repository-wide inventory and regression validation, with fresh source comparison and executable probes of selected paths. It is **not an exhaustive branch-by-branch certification** of the entire server. The coverage matrix below distinguishes fresh tracing, test coverage, and unexamined behavior. Historical findings are not automatically counted as current defects.

## Resolution queue

| ID | Priority | Issue | Suggested implementation boundary |
| --- | --- | --- | --- |
| F01 | P2 | Mayor gate actions bypass door rules and leave the reverse exit unchanged | Reuse runtime door transitions from authored special steps |
| F02 | P3 | Looking at a described door omits its open/closed state | Directional look pipeline and authored messages |
| F03 | P2 | Clanless player kills do not clear the victim's criminal flag | Shared clan semantics in death cleanup |
| F04 | P2 | Burning-out lights reveal invisible items and notify sleeping observers | Light tick notification rendering and recipients |
| F05 | P2 | NPC-special room notices reveal invisible actors and notify sleeping observers | Shared special-message rendering and recipients |

All five have C source evidence and reproductions in the [probe script](rom24-parity-2026-11-06-probes.py), with [captured observations](rom24-parity-2026-11-06-probes.json). These are probes asserting the current discrepancy, not regression tests asserting the corrected behavior. They use production domain models and handlers, collection-backed fixtures, and captured socket delivery. No compiled C process or live content service was used.

### F01 — Mayor gate actions bypass door rules and leave the reverse exit unchanged

**Trigger:** The mayor reaches an `O` or `C` step in the bundled `spec_mayor` route at a gate with a reciprocal exit. A locked gate additionally exposes the missing open guard.

**Expected:** [special.c:962](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:962) invokes ordinary `do_open("gate")`; the close step invokes `do_close`. [act_move.c:398](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:398) refuses a locked gate, and [act_move.c:405](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:405) updates the reciprocal exit when it points back to the origin. Closing has the equivalent reciprocal update at [act_move.c:491](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:491). The command also produces the door notices.

**Actual:** The authored mayor route reaches [MobileApi.py:470](../../src/api/MobileApi.py#L470), then [MobileApi.py:751](../../src/api/MobileApi.py#L751). `_toggle_gate` directly changes CLOSED on each local exit whose entire keyword equals `gate`. It neither checks LOCKED nor updates the reciprocal exit or emits the ordinary door notices.

**Reproduction:** Executed the actual mayor route lambda with a one-step `O.` route state and real paired exits. Starting with flags `3/3` (door + closed), Python produces `1/3`: open on the mayor's side and closed on the other. Starting with local flags `7` (door + closed + locked), it produces `5`: open but still locked. Closing's asymmetry is established by the shared helper; the executable probe exercises opening.

**Consequence:** Scheduled gate changes permit travel from only one side and can bypass a lock. Players on the far side cannot rely on the mayor's opening announcement.

**Resolution:** Keep route/time content editable; make the special invoke the existing reusable door transition with its guards, reciprocal update, keyword lookup, and notices. Cover open/close from both sides, locked gates, multiword gate keywords, missing reverse exits, reverse exits leading elsewhere, and already-open/closed cases. Do not change the C reference or hard-code the mayor route in Python.

### F02 — Looking at a described door omits its open/closed state

**Trigger:** A sighted player enters `look north` where the exit has both a description and a door keyword.

**Expected:** [act_info.c:1219](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1219) prints the description (or the default notice), then independently prints the named door's open/closed state at [act_info.c:1224](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1224).

**Actual:** [RoomHandler.py:125](../../src/area/RoomHandler.py#L125) returns immediately after a nonempty description, so its door-state branch is unreachable. The current `look` collection command's guards and pipeline permit this case; they do not supply the missing state afterward. The dispatch is [Info.py:194](../../src/interp/commands/Info.py#L194).

**Reproduction:** The public interpreter, current `look` document, production room handler, and message bus output only `An iron gate blocks the road.` for a closed gate. There is no closed-state line.

**Consequence:** Adding designer-authored descriptive text removes useful door-state feedback.

**Resolution:** Render description/default and door status as separate steps before finishing. Use the existing authored message keys. Cover described open and closed doors, a description-free door, an ordinary described exit, and an absent exit. Also check ROM's first-keyword `$d` rendering when a door has multiple keywords. The described closed-door case is reproduced; the other cases are proposed regression coverage.

### F03 — Clanless player kills do not clear the victim's criminal flag

**Trigger:** A clanless player kills another clanless player carrying PLR_KILLER or PLR_THIEF; both have the canonical empty `guild` value.

**Expected:** [fight.c:898](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:898) clears KILLER, or otherwise THIEF, when a different player kills someone outside their same clan. [handler.c:333](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:333) explicitly returns false for independent clans. [tables.c:46](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/tables.c:46) marks both the empty clan and `loner` independent. Two clanless players therefore do not qualify for the same-clan exemption.

**Actual:** [CombatDeathHandler.py:149](../../src/combat/CombatDeathHandler.py#L149) exempts matching guild strings unless the attacker's string is exactly `independent` or `loner`. Empty strings match and return early. The live lethal-damage path calls this helper after `raw_kill` at [CombatHandler.py:1036](../../src/combat/CombatHandler.py#L1036).

**Reproduction:** With real Character models and loaded player flags, invoking production cleanup separately for KILLER and THIEF leaves each flag set. This probe targets the cleanup boundary; it does not simulate the preceding lethal attack.

**Consequence:** Clanless criminals retain the flag after a death that should clear it, affecting later criminal targeting and restrictions.

**Resolution:** Apply catalog-backed independent/same-clan semantics, including the empty clan, rather than equality plus two reserved names. Cover empty clan, loner, matching real clan, different clans, self-death, NPC attacker, and both criminal flags together (KILLER clears first). Keep guild names and independence data designer/service owned.

### F04 — Burning-out lights reveal invisible items and notify sleeping observers

**Trigger:** A mortal's equipped light has one unit remaining and expires during a character tick. A bystander is asleep, or cannot detect the now-extinguished invisible light.

**Expected:** [update.c:673](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:673) sends the light notice through `act` after reducing its fuel to zero. The default minimum position is RESTING ([merc.h:1842](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1842)); [comm.c:2475](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475) filters recipients, and [comm.c:2522](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2522) resolves `$p` per observer. The lit-light visibility exception at [handler.c:2508](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2508) no longer applies once fuel is zero.

**Actual:** [Character.py:444](../../src/player/Character.py#L444) constructs literal item-name strings. [EntityUpdateHandler.py:112](../../src/game/EntityUpdateHandler.py#L112) sends that same string to all other room players, without a posture or object-visibility check. This is distinct from ordinary item-timer decay, whose recipient rendering was already repaired.

**Reproduction:** A real invisible light expires from fuel 1 to 0. Production object visibility confirms that the awake witness cannot see it. Both that witness and a sleeping player nevertheless receive `the secret lamp goes out.` through the real message bus.

**Consequence:** Light exhaustion discloses an unseen object's identity and produces notices for sleeping characters.

**Resolution:** Preserve the light/ownership transition, but snapshot recipient-aware messages using the common room-listener and visible-object helpers. Preserve the C timing of the visibility check after fuel exhaustion. Cover detection versus no detection, sleeping owner/bystander, switched recipients, ordinary lamps, flicker warnings, and permanent lights.

### F05 — NPC-special room notices reveal invisible actors and notify sleeping observers

**Trigger:** An awake invisible NPC running `spec_fido` devours an NPC corpse while an awake player without detection and a sleeping player are present.

**Expected:** [special.c:774](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:774) uses `act` for the devouring notice. Its recipient posture filter and per-observer `$n` expansion are [comm.c:2475](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475) and [comm.c:2512](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2512). The awake witness sees a generic identity; the sleeper receives nothing.

**Actual:** The current `spec_fido` collection lambda calls [MobileApi.py:394](../../src/api/MobileApi.py#L394). It expands `$n` once through [MobileApi.py:863](../../src/api/MobileApi.py#L863), then [MobileApi.py:770](../../src/api/MobileApi.py#L770) selects room players without a posture filter. `MobileHandler._handle_payload` forwards that literal room message to the selected targets.

**Reproduction:** Executed the current authored special with a real invisible Mobile and NPC corpse. The corpse is removed, and its queued notice is `the invisible fido savagely devours a corpse.` with both awake and sleeping witnesses included. The probe checks the produced payload and audience; socket delivery for this special was traced rather than executed.

**Consequence:** This special reveals an unseen NPC's identity and bypasses ordinary sleep filtering. Other callers of the shared special-message helper warrant follow-up, but this finding does not assert that every special has the same defect.

**Resolution:** Keep authored special text; carry actor/object references until per-recipient rendering and use the shared eligible-listener helper. Audit other callers such as the mayor's scripted room notices. Cover hidden/visible actors, detect-invisibility, sleepers, possession, and unchanged corpse-content transfer.

## Validation and test-maintenance work

The complete isolated sweep ran **136 top-level modules, 1,673 reported tests, 123 passing modules, 13 non-passing modules, zero timeouts, five failure entries, and 30 error entries**. The reported count includes unittest loader-error placeholders; it is not a count of successful test methods. Full per-module output is in [test results](rom24-parity-2026-11-06-tests.json), and the [runner](rom24-parity-2026-11-06-tests.py) makes the isolation and 45-second timeout reproducible.

The initial system `python` was an ActiveState launcher that failed before tests started. The repository `.venv/Scripts/python.exe` is Python 3.14.0. Sandbox asyncio runs stalled; they were stopped, and the completed sweep ran with local Windows asyncio loopback access. Modules ran in separate processes because several test files install global import stubs. A successful combined-process discovery run is not claimed. No implementation fixes or desired-behavior regression tests were added.

Treat these as a separate test-maintenance backlog, not 13 additional gameplay findings:

| Module | Observed failure / next resolution step |
| --- | --- |
| `test_combat_group_rewards` | 11 errors: fixture attributes lack `points`, required by the current advancement path. Repair the fixture and rerun reward assertions. |
| `test_combat_handler_aggression` | Stubbed InterpApi is `object` and lacks `command_payload`. |
| `test_combat_survival` | Fixture bus lacks `connection_manager` used by payload emission. |
| `test_command_authorization` | One symbolic `IM` threshold assertion fails. Reconcile the test's expected 55 with the configured LEVEL_IMMORTAL mapping before classifying it as a runtime defect. |
| `test_final_combat_parity` | Stubbed MovementUtil lacks `DIR_NAME`. |
| `test_import_rom_helps` | Imports absent `src.devtools.import_rom_helps`; decide whether to restore the utility or retire/update its test. |
| `test_mobile_pulse` | Scavenger fixture lacks Mobile's `add_item` method. |
| `test_object_fountain_commands` | Six errors: InterpUtil stub lacks `parse_object_arguments`. |
| `test_object_lookup_parity` | Two errors: observer fixtures lack `status_flags` now used by recipient object visibility. |
| `test_player_handler_cast_prompt` | Its `server.messaging` stub is not a package, so MessageBus cannot import. |
| `test_remaining_gameplay_parity` | Five errors: constructed MobileHandler fixture lacks `handler_service`. |
| `test_spell_affect_payload_messages` | Three energy-drain assertions fail. The earlier source investigation identified missing `points` in the victim fixture; current assertions alone do not establish a production defect. Restore a valid advancement fixture and rerun. |
| `test_weather_update` | Calendar rollover assertion assumes year 1 without setting the starting year. Construction uses current time, so the test receives 1335 after rollover instead of 2. Freeze time or explicitly initialize the year. |

## Repository coverage

Inventory: **214 Python source files, 30 reference C translation units, 17 collection snapshots, and all 136 current top-level test modules**. Queried content counts include 221 commands, 38 skills, 97 spells, 244 socials, 412 special records, 986 mobiles, 1,266 items, 3,127 rooms, 5,196 resets, 62 shops, 49 areas, and 251 help documents. Counts describe the surface, not per-record verification. [Manifest](rom24-parity-2026-11-06-manifest.json) records the Python revision and SHA-256 of every reference `.c` file.

| Reference family | Evidence and depth in this review |
| --- | --- |
| `act_move.c`, `act_enter.c` | Fresh directional/follower, recall, door and portal runtime inspection; mayor-to-door C trace; movement/entry/furniture regression modules. F01; not every topology or posture branch re-traced. |
| `act_info.c`, `scan.c` | Fresh public directional-look probe and room/exit rendering inspection; information, inspection, visibility, where and spell tests. F02; scan receives regression/historical coverage, not a fresh complete C trace. |
| `fight.c`, `handler.c`, `tables.c` | Fresh lethal-damage cleanup, clan definitions, recipient and item-visibility traces; combat, defense, rewards, death, carry and flag tests. F03/F04; reward fixture failures limit validation. |
| `update.c`, `db.c`, `db2.c` | Fresh world-tick scheduling, light expiry, weather, regeneration, area reset and population runtime inspection, with selected C update comparisons; update/reset/factory suites. F04; legacy area conversion and every reset record unexamined. |
| `special.c` | Fresh mayor and fido authored paths, mobile dispatch, money update and shared helpers; direct collection-backed probes and mobile/special suites. F01/F05; not all 412 records executed. |
| `act_obj.c`, `healer.c` | Object ownership, timer decay and transfer-message runtime sampling; broad object/shop/consumption/theft/healer tests. No new verified finding; selected fixture failures remain. No fresh complete C object-command traversal. |
| `magic.c`, `magic2.c`, `effects.c` | Casting and periodic effect runtime sampling; spell targeting, payload, breath, weapon-effect and elemental-exposure suites. Existing energy-drain fixture failures retained. Not every authored spell or probability branch re-traced. |
| `skills.c`, `const.c` | Learning and advancement formula runtime inspection and learning/training/XP tests; historical C comparisons consulted. No new full class/skill/table equivalence proof. |
| `interp.c`, `alias.c` | Input/alias/command-access runtime inspection, C prefix lookup check and parser/authorization tests. Explicit-shortcut policy remains unresolved. |
| `act_comm.c`, `note.c` | Clan preference, pose and note recipient runtime sampling; C clan-sender check; communication/social/note suites. Repaired clan-note membership and travel-related rendering present. External note-service transactions untested. |
| `act_wiz.c`, `ban.c`, `flags.c`, `lookup.c` | Administrator, ban, lookup, possession, flag and identity tests plus shared-helper inspection and historical reports. Regression-level coverage; no fresh exhaustive C administrator-command review. |
| `comm.c`, `save.c` | Fresh `act` recipient/substitution trace; session, authentication, input, persistence and connection runtime sampling; wire/reconnect/persistence tests. Offline recovery remains a service-contract question. No live login/server exercise. |
| `music.c`, `recycle.c` | Inventoried only. Music scheduler placeholder noted; jukebox/song delivery not freshly audited. C memory allocation/free-list equivalence is not a requirement for managed Python. |

Prior room/visibility, travel, note membership, and item-transfer remediation is present in the inspected paths and covered by the current tests. This review does not revive the archived findings merely because their titles resemble F04/F05: those two use separate notification producers.

## Unresolved discrepancies and remaining limits

These remain decisions or follow-up investigations, not verified defects in the queue:

- **Command abbreviations:** [interp.c:424](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:424) accepts table-order prefixes, while [InterpUtil.py:136](../../src/util/InterpUtil.py#L136) resolves names and authored shortcuts. Confirm whether that explicit shortcut policy is deliberate, including socials, before changing lookup semantics.
- **Idle/limbo/autoquit:** ROM [update.c:684](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:684) advances idle ticks and moves characters to limbo. Python's [SessionHandler.py:55](../../src/server/session/SessionHandler.py#L55) and connection loop use elapsed session activity. Product intent for limbo and automatic quit still needs confirmation; do not infer a defect from different scheduler architecture alone.
- **Pose selection:** [act_comm.c:1347](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1347) uses C pose eligibility/tables. [Communications.py:311](../../src/interp/commands/Communications.py#L311) selects authored pose keys. Class/level eligibility policy remains unconfirmed.
- **QUIET clan sender:** [act_comm.c:680](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:680) checks NOCHANNELS before sending; Python [Communications.py:199](../../src/interp/commands/Communications.py#L199) also rejects a QUIET sender. Establish intended channel policy before altering it.
- **Offline recovery:** [save.c:921](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:921) applies elapsed-offline resource recovery. Python persistence/authentication is service-backed. This review did not inspect the upstream character service, so responsibility and actual end-to-end behavior remain unresolved.

Accepted differences include asynchronous transport, service-backed persistence/authentication, dynamic enums and registries, designer-authored guards/payloads, and managed memory. They are not defects merely because ROM uses synchronous C code and static tables.

Not performed: exhaustive branch pairing of every function, full area/content record comparison, legacy `tests/old-tests`, executable-C differential testing, live sockets/content services, or all cross-command timing/interleaving scenarios. A subsystem with passing tests or no new finding is not certified behaviorally equivalent. Resolve F01–F05 with focused regressions, repair the listed test fixtures, and use the coverage matrix to select the next deeper audit rather than treating this report as complete parity proof.

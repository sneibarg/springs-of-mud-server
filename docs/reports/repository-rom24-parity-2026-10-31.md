# Repository-wide ROM24 parity review — October 31, 2026

**The five confirmed findings are now resolved (October 31, 2026).** Spell announcements render caster identity per observer, retaining class translation and excluding sleeping recipients. Fallback NPC attacks select uniformly among slash, pound, and pierce. Area resets establish a separate runtime origin; eligible displaced NPCs are extracted before regeneration/effects with the strict `< 5` roll and controlled/charmed/fighting/position exclusions. Input parsing recognizes leading punctuation and preserves interior argument whitespace through aliases, prefixes, speech delivery, and description storage. Existing visibility/extraction/payload mechanisms are reused; no collection or C-reference changes were needed. The abbreviation and idle-policy questions remain unresolved and unchanged.

**Remediation validation:** [15 focused regression tests](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_repository_parity_remediation.py) pass. The full isolated run, performed with the first 13 new cases, exercised **134 modules / 1,637 tests**, with **122 passing modules / 1,328 tests**. The same 12 modules retain exactly the baseline's failure/error identifiers: **no new failures**. Two additional spawn/movement cases were then added and the focused 15-test module passed. [Full run output](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-remediation-2026-10-31-tests.json). `git diff --check` passes. No live deployment was performed.

The original review follows as a historical record of the pre-remediation behavior; its source line anchors may have shifted after the fixes.

The current working tree has **five confirmed behavioral mismatches** in the traced paths: invisible-caster disclosure, fallback NPC attack selection, missing foreign-area NPC cleanup, punctuation-command parsing, and mutation of command-body whitespace. Command abbreviation and idle handling are additional verified differences whose intended product policy remains unresolved. These findings do not establish exhaustive equivalence elsewhere.

This is a review only. Runtime, content, existing tests, and the C reference were not changed. Added artifacts are this report, reproducible review probes/results, and an isolated test runner/results. Existing staged deletions and unrelated working-tree changes were retained. The Python HEAD was `e4659bd4c9c573f1361fb3a60468ed939df4dd05`; findings refer to working-tree contents, not just HEAD. The reference is the local `C:/Users/scott/PycharmProjects/PyRom/Rom24/src` checkout. Its Git command failed with a worktree-path error, so no reference commit identity is asserted.

## Confirmed findings

### F01 — P2: Spell announcements disclose an invisible caster's identity

**Trigger:** An invisible caster uses an ordinary spell other than ventriloquate while a player who cannot see the caster is in the room.

**Expected:** ROM constructs `$n utters the words…` in [magic.c:197](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:197) and calls `act(..., TO_VICT)` separately for each observer. [comm.c:2512](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2512) expands `$n` through `PERS(ch, to)`, preserving the observer's visibility restrictions.

**Actual:** [SpellApi.py:115](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:115) calculates a literal actor name once. Lines 118–142 create translated/plain announcements with that name and distribute them by class, without rendering names for each recipient. The direct victim announcement has the same problem. Neither translation nor ordinary payload emission restores visibility once the name is literal text.

**Evidence:** The production announcement probe first verifies `CharacterApi.can_see(Bob, Alice, room) == False`, then obtains `Alice utters the words, 'abrazak'.` addressed to Bob and Cara. This is identity disclosure even when the spell does not remove invisibility, such as self-cast armor.

**Recommendation:** Render both class variants per observer using the existing visibility-aware text mechanisms. Cover direct victims, same/different classes, invisibility/wizinvis, and sleeping recipients. Preserve authored spell ownership and existing translation rules.

### F02 — P2: NPCs without an authored attack type always receive slash

**Trigger:** Spawn a mobile whose `dam_type` is empty or `none`.

**Expected:** [db.c:1579](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1579) selects uniformly with `number_range(1,3)`, assigning attack indices 3, 7, or 11: slash, pound, or pierce.

**Actual:** [MobileFactory.py:44](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/mobile/MobileFactory.py:44) indexes the same three alternatives with `rng.dice(0, 2)`. [RandomNumberGenerator.py:55](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/RandomNumberGenerator.py:55) returns zero for zero dice, so only index 3 can occur. [MobileFactory.py:165](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/mobile/MobileFactory.py:165) invokes this fallback during normal creation. [CombatHandler.py:1645](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:1645) resolves numeric attack indices, so the discrepancy affects attack verbs and physical damage type, including defenses against slash/bash/pierce.

**Evidence:** All 100 production-helper calls returned 3; more decisively, the zero-dice implementation makes alternatives unreachable. Collection-query found actual `none` prototypes, including vnums 1000, 1001, 8600, 8301, and 9401. This is not limited to hypothetical designer content.

**Recommendation:** Use the shared uniform range operation for the three alternatives and verify each branch deterministically. Retain explicitly authored attack types.

### F03 — P2: Displaced NPCs never receive ROM's tick-time cleanup

**Trigger:** A mobile spawned in area A remains in area B, at least stunned, uncontrolled, not fighting, and uncharmed; the cleanup roll is below 5.

**Expected:** The reset path records the mobile's origin area in [db.c:1288](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1288). [update.c:635](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:635) checks origin versus current room area before regeneration. An eligible 1–4 roll out of 100 emits the wandering-home notice, extracts the mobile, and skips the remainder of that entity's tick. Despite the message, C extracts the mobile; it does not walk or teleport it home.

**Actual:** [EntityUpdateHandler.py:63](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/EntityUpdateHandler.py:63) proceeds directly to regeneration, effect expiration, and status damage. [AreaHandler.py:125](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/AreaHandler.py:125) and `MobileFactory.create` do not establish a separate reset-origin lifecycle contract. Generic wandering and mobile specials do not implement this character-tick extraction rule. Movement also updates the actor's current `area_id`, so that field cannot safely serve both current and origin area.

**Evidence:** A production entity-tick probe supplies a standing, uncharmed mobile with an explicit foreign `zone` and a random provider returning 1. The mobile remains in the room and no cleanup roll is requested. Static tracing of both update coordinators confirms the missing branch.

**Consequence/recommendation:** Escaped or transferred NPCs persist in foreign areas instead of eventually being removed, potentially retaining inventory and affecting population limits. Preserve reset origin independently and add the reusable lifecycle rule at the entity-tick boundary. Test the strict roll boundary and all eligibility exclusions, and use extraction rather than death/reward logic.

### F04 — P2: Punctuation commands require an extra space

**Trigger:** Enter `'hello` or `.hello` through normal descriptor command handling.

**Expected:** [interp.c:399](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:399) treats a leading non-alphanumeric character as a one-character command and passes the remaining text as its body. These inputs execute say and gossip respectively.

**Actual:** [InterpUtil.py:122](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/InterpUtil.py:122) splits only on whitespace, treating the entire `'hello` or `.hello` string as a command name. [InterpHandler.py:75](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/InterpHandler.py:75) reaches that parser after alias expansion. The bundled say record already has the `'` shortcut and the `.` record exists; this is a parser defect, not missing authored text.

**Evidence:** Both full-interpreter probes emitted only `Huh?` to the actor and nothing to Bob. The ordinary `say hello` control delivered correctly.

**Recommendation:** Split the leading punctuation token before command lookup while preserving the rest of the input. Verify each supported punctuation route through the public interpreter, including alias/prefix substitution.

### F05 — P3: The interpreter collapses authored command-body whitespace

**Trigger:** Enter `say hello   brave world` through normal command handling.

**Expected:** ROM's [interp.c:413](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:413) consumes the command word with `one_argument` and preserves spacing inside the remaining message body.

**Actual:** [InterpUtil.py:118](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/InterpUtil.py:118) applies `" ".join(input.split())` to the entire input. The resulting normalized parameters become `Context.result`, used by speech and other text-bearing commands. Keeping the original string as `raw_command` for auditing does not restore the body passed to handlers.

**Evidence:** The full-interpreter probe delivered `Alice says 'hello brave world'`, losing the two extra spaces. [test_speech_text_parity.py:46](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_speech_text_parity.py:46) calls `_handle_lambdas` directly with an already separated body, bypassing the destructive parser; its repeated-space case therefore passes without covering this path.

**Recommendation:** Normalize the command token independently and preserve interior body text. Add an end-to-end interpreter case for speech and a stored-text command such as description or note composition.

## Unresolved policy differences

These are verified differences, not established intentional exemptions or automatically approved fixes.

- **U01 — Prefix abbreviations:** [interp.c:424](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:424) searches command prefixes in table order while skipping commands above actor trust. [InterpUtil.py:136](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/InterpUtil.py:136) accepts exact names and explicit shortcuts only. `recal` returns `Huh?` with the current collection; ROM selects recall. Explicit designer-managed shortcuts may be the desired product policy, but no instruction found establishes that as a deliberate removal of ROM prefix semantics. If parity is desired, precedence and trust filtering must be preserved, rather than simply calling `startswith` over the current collection order.
- **U02 — Idle lifecycle:** [update.c:684](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:684) moves mortal players into limbo after 12 idle ticks, stops combat, and preserves their prior room. The later `timer > 30` path attempts autoquit. [ConnectionHandler.py:391](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:391) instead ends the connection wait on its configured wall-clock timeout after sending a void notice, leaving the live character in the world through disconnect cleanup. [SessionHandler.py:7](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/session/SessionHandler.py:7) defaults to 30 seconds. Prior repository reviews explicitly left login/idle policy unresolved; this review does not promote it to a newly confirmed defect or prescribe changing it.

No architecture finding is made for dynamic enums, service-backed persistence/authentication, asynchronous transport, data-defined spells/skills/commands, or designer-owned messages. Music playback and account creation/deletion/password workflows need a product-scope decision before treating their absence or replacement as gameplay defects.

## Repository coverage and evidence depth

The inventory includes all 30 reference C translation units, the Python runtime domains, 17 collection snapshots, and every current top-level `tests/test_*.py` module. The collection inventory has 221 commands, 38 skills, 97 spells, 244 socials, 986 mobiles, 1,266 items, 3,127 rooms, and 5,196 resets. Inventory counts do not mean every document was behaviorally compared.

| Reference files / domain | Python paths and evidence used | Coverage limit |
| --- | --- | --- |
| `interp.c`, `alias.c` | `InterpHandler`, `InterpUtil`, `CommandAccess`, `AliasApi`; public-interpreter probes; authorization, aliases, input tests | New parsing findings; not every abbreviation/trust collision |
| `act_comm.c`, social paths in `interp.c` | Communications handlers/APIs, `SocialHandler`, `DisplayUtil`, real message-bus probe; speech, tell, social, group/broadcast tests | Sampled restrictions, rendering and delivery; not all 244 social templates |
| `act_info.c` | `Info`, lookup/display helpers, character inspection and score; information/where/compare/container tests | Representative inspection/output paths; not every format and filter combination |
| `act_move.c`, `act_enter.c`, `scan.c` | `Movement`, `MovementUtil`, room/follower/portal contracts; movement/entry/recall/wake tests | Test-backed mechanics and sampled traces; scan content not re-audited branch by branch |
| `act_obj.c`, `healer.c` | `Object`, equipment, ownership, decay, shop and consumption paths; broad object/healer suites | Numerous existing regressions; fixture failures listed below leave specific gaps |
| `fight.c` | `CombatHandler`, `FightUtil`, guards/plans; attacks, defenses, assistance, damage, death, XP suites | Sampled attack/assist traces; reward/emission fixtures prevent a clean full validation |
| `magic.c`, `magic2.c`, `effects.c`, `magic.h` | `SpellApi`, effect handler/utilities, elemental exposure; actual spell documents, 130-test payload suite plus breath/exposure tests | Visibility finding; energy-drain assertions remain unresolved; not all 97 spells exhaustively compared |
| `skills.c`, advancement in `update.c`, tables in `const.c` | `CharacterAdvancement`, abilities/learning, stat/resource models; advancement, training, learning and spell-list suites | Sampled arithmetic and contracts; not full character-generation equivalence |
| `update.c`, population/reset paths in `db.c` | `UpdateHandler`, `EntityUpdateHandler`, mobile/item/weather updates, `AreaHandler`, `MobileFactory`; tick/spawn probes and reset/weather tests | NPC findings; not every one of 5,196 resets or all traversal-order interactions |
| `special.c` | `MobileHandler`, `MobileApi`, special registry/content; specials, pulse, room-access tests | Current scheduler/scavenge paths inspected; every special's lambda was not independently re-traced |
| `act_wiz.c`, `flags.c`, `ban.c` | `Wiz`, `WizHandler`, command access, `SiteBans`; immortal movement/state/identity/force/recovery suites | Existing domain tests plus sampled contracts; not every admin field/flag mutation |
| `note.c` | `NoteHandler`, character read tracking; list/read/remove/delete and note suites | Selected current paths and tests; no live content-service transaction validation |
| `comm.c`, `save.c` | connection/session handling, messaging, timers, autosave, persistence workers; reconnect/wire/runtime-ownership tests | Local behavior only; authentication and storage formats are accepted replacements; idle policy unresolved |
| `handler.c`, `lookup.c`, `tables.c` | shared visibility/lookup, carry calculations, flags/enums/effects; related focused tests | Selected helper behavior; no exhaustive table-value comparison |
| `db2.c`, remaining `db.c` content loaders | service/factory architecture and collection inventory | Inventory/historical-report context only for legacy conversion; no full area import differential |
| `music.c`, `recycle.c` | scheduler inventory; managed Python runtime and product substitutions | Inventory only; music policy and C allocation/free-list internals are not asserted equivalent |

Historical reports were used to locate prior remediations and avoid reporting already-fixed behavior. They are not treated as proof that current unexamined branches match. The new findings come from current source traces and review probes.

## Validation and outstanding test failures

Used `.venv/Scripts/python.exe` (Python 3.14.0). The shell's plain `python` points to an ActiveState wrapper that could not write its external log directory; the repository virtual environment worked. Windows asyncio initially stalled creating a local socketpair under restricted execution. The completed test/probe runs used approved local loopback access.

The final runner sets `PYTHONPATH` to this repository's `src`, runs each top-level module in a fresh process, allows up to four independent processes, and applies a 60-second per-module timeout. This avoids contamination between different modules' global stubs, but cannot correct stubs installed inside a module. No timeouts occurred in the completed run.

**133 modules / 1,624 unittest-reported tests; 121 modules pass, containing 1,315 tests.** The other 12 modules report **4 failures and 29 errors**, including subtest failures and failed-import placeholders. Those counts must not be read as 1,624 independent C-derived parity cases. There is no same-runner clean baseline from which to claim that these failures are new regressions.

| Non-passing module | Observed reason / disposition |
| --- | --- |
| `test_combat_group_rewards` | 11 errors: fixture attributes lack `points`; reward cases not validated by this run |
| `test_combat_handler_aggression` | 1 error: stubbed `InterpApi` is `object`, lacking `command_payload` |
| `test_combat_survival` | 1 error: fixture message bus lacks `connection_manager` |
| `test_command_authorization` | 1 assertion failure for symbolic `IM`; expected denial conflicts with actual result; retain for fixture/threshold investigation |
| `test_final_combat_parity` | 1 error: stubbed movement utility lacks `DIR_NAME` |
| `test_import_rom_helps` | 1 failed-import error; `src.devtools.import_rom_helps` is deleted in the existing working tree |
| `test_mobile_pulse` | 1 error: fixture actor lacks `add_item` |
| `test_object_fountain_commands` | 6 errors: stubbed parser lacks `parse_object_arguments` |
| `test_object_theft_parity` | 1 error: `server.messaging` replaced by a non-package stub |
| `test_player_handler_cast_prompt` | 1 failed-import error involving the same messaging-package stub pattern |
| `test_remaining_gameplay_parity` | 5 errors: fixture `MobileHandler` lacks `handler_service` |
| `test_spell_affect_payload_messages` | 3 energy-drain assertion failures (`execute_lambdas` returns false); not independently established as runtime parity defects |

Artifacts:

- [Reproducible production probes](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-probes.py) and [observed probe outputs](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-probes.json).
- [Isolated test runner](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-run-tests.py) and [complete per-module output](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-tests.json).

No executable-C differential harness, live game/content-service integration, exhaustive state-space review, complete area-data comparison, or legacy `tests/old-tests` execution was performed. The repository-wide scope is an assessment across domains with explicit evidence depth, not certification of every ROM branch. Priority follow-up is to fix the five demonstrated mismatches with narrow regressions, resolve the two policy differences, and restore the failing test fixtures before using the full suite as a parity gate.

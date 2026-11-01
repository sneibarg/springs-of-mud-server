# Repository-wide ROM24 parity review — October 31, 2026, second pass

**All five additional findings are resolved (October 31, 2026).** Punctuation routes now use their matching handlers; semicolon has authored group-tell messages and guards, and both group-tell routes enforce the sender's NOTELL restriction. Pose uses the existing five variants moved into designer-editable command payloads, with correct first-person grammar, visibility-aware room rendering, and resting-or-higher listeners; the separate unresolved class/level pose-table policy is unchanged. Teleport snapshots each observer's names independently in the source and destination rooms. Attack concatenation and condition-line construction preserve `RecipientText` through actual delivery. Fresh world entry establishes an idempotent playtime baseline, snapshots accumulate session time without changing live counters, and quit/extraction stop the clock; link-dead reconnection retains the existing baseline.

**Validation:** [15 new focused tests](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_additional_repository_parity_fixes.py) pass, covering actual delivery, visibility changes before emission, XP/score, repeated saves, restart, cached re-login, zero logon, successful/failed quit, extraction, and real link-loss/reattachment. The final isolated run exercised **135 modules / 1,654 tests**: **123 modules / 1,345 tests pass**. The same 12 baseline modules retain the same failure/error identifiers; no new regressions detected. Updated one renderer stub in the spell suite for the visibility-aware interface; its three pre-existing energy-drain failures remain. [Final per-module results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-second-remediation-2026-10-31-tests.json). `git diff --check` passes.

Collection-query and collection-modify were used for the three changed command records. Windows denied atomic file replacement; the exact devtools-validated serialization was written in place, then queried again. Publish/reload the updated `pose`, `;`, and `gtell` command documents through the content service for live use. No live deployment or C-reference changes were made.

The original review below records the pre-remediation behavior; source line anchors may have shifted after the fixes.

**Five additional behavioral mismatches were reproduced in the current working tree.** Punctuation commands dispatch to incorrect communication handlers, `pose` raises an exception, teleport notices disclose invisible characters, login/save timing miscounts playtime and changes XP, and combat merging destroys visibility-aware weapon-proc text. The 15 regressions for the previous five fixes still pass; these are additional paths, not evidence that those fixes were reverted.

This review changed only review artifacts. Runtime, collections, existing tests, and the C checkout were not edited. Unrelated staged deletions and working-tree changes were preserved. Python HEAD remains `e4659bd4c9c573f1361fb3a60468ed939df4dd05`, with the accepted fixes present as working-tree changes. The reference is the local `C:/Users/scott/PycharmProjects/PyRom/Rom24/src` tree. No executable-C comparison or live service deployment was performed.

## Findings

### F01 — P2: Punctuation commands dispatch to the wrong communication handlers

**Trigger:** Use `.hello`, `,waves`, or `;private group message` through the public interpreter with the bundled command records.

**Reference:** [interp.c:183](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:183) routes `.` to gossip, `,` to emote, and `;` to group tell. Gossip applies `COMM_NOGOSSIP` for sender auto-enable and recipient opt-outs in [act_comm.c:325](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:325); group tell uses group membership and its own sender restriction in [act_comm.c:1908](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1908).

**Python:** The dispatch entries in [Communications.py:64](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:64) instead select gossip for comma, quote for semicolon, and grats for dot. Their collection payloads still describe the correct ROM commands. Consequently, text and behavior disagree: [the channel helper](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:592) chooses flags and targets using the wrong handler's channel while reading text from the original command's payload.

**Reproduced:** With Bob's gossip disabled and Cara's grats disabled, `.hello` delivers `Alice gossips 'hello'` to Bob and excludes Cara. `gossip hello` correctly excludes Bob and reaches Cara. `,waves` acknowledges `Alice waves` only to Alice; the corresponding `emote waves` reaches both room listeners. `;private group message` emits nothing, while `gtell private group message` reaches the grouped Bob.

**Consequence/remedy:** Players receive opted-out channel messages or lose messages on ordinary shortcuts. Route punctuation to the same runtime handlers as their full command names, preserving each authored payload. Test sender toggles, recipient opt-outs, no-argument behavior, group membership, and actual message delivery. Parser-only assertions cannot establish dispatch parity.

### F02 — P2: `pose` raises an exception and exits ordinary connection handling

**Trigger:** A standing player executes the enabled bundled `pose` command.

**Reference:** [act_comm.c:1347](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1347) chooses a pose bounded by level and renders the class-specific actor/room messages through `act`, then returns normally.

**Python:** [Communications.py:319](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:319) calls `self._room_targets(character, room)`. `Communications` neither defines nor initializes that helper and has no base class providing it. The production constructor and public-interpreter probe raise `AttributeError: 'Communications' object has no attribute '_room_targets'` before returning a payload. This is not a fixture missing a runtime dependency.

**Consequence/remedy:** No pose is delivered. The exception propagates through command execution into [ConnectionHandler.py:378](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:378), whose game-loop exception branch logs and breaks; normal outer cleanup then closes the connection. The probe reproduced propagation, not a real socket disconnect. Reuse the existing room-listener/rendering mechanisms and add a public-command regression. Also verify class/level selection and recipient visibility when replacing the broken path; the current five generic Python strings do not establish parity with the C pose table, and that content decision was not counted as a separate finding.

### F03 — P2: Teleport room notices reveal invisible characters

**Trigger:** An invisible character self-teleports while an observer unable to see that character is in the departure or arrival room.

**Reference:** [magic.c:4373](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4373) emits `$n vanishes!` and `$n slowly fades into existence.` through `act` on either side of movement. [comm.c:2512](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2512) renders `$n` through the individual recipient's `PERS` visibility rules. Teleport does not remove invisibility.

**Python:** [SpellApi.move_to](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:1378) renders both room notices with [_ability_message](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:373), which fills victim/target tokens with a literal entity name. [_queue_room_text](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:1596) distributes that same string without observer-specific expansion. The bundled teleport payload has correct authored templates; the shared runtime rendering loses visibility information.

**Reproduced:** Executed all lambdas from the actual teleport document, fixing only the random destination. The source-room Cara cannot see Alice but is targeted with `Alice vanishes!`; arrival-room Bob cannot see Alice but is targeted with `Alice slowly fades into existence.` Both visibility checks use the real `CharacterApi` before/after relocation. These are separate from the ordinary cast announcements fixed in the previous pass.

**Consequence/remedy:** Teleport exposes a concealed player's identity. Snapshot recipient-specific departure text before movement and arrival text in the destination, preserving authored message keys, exclusions, and room context. Exercise the public spell path, not only announcement generation. Other consumers of the shared movement/message helpers should be checked when fixing this; this review does not claim every spell notice has been traced.

### F04 — P2: Fresh login retains stale logon time, counting offline time toward age and XP

**Trigger:** A persisted player record has one hour of accumulated playtime and a logon timestamp 20 hours before the current time; that record enters a new login after being offline.

**Reference:** A new ROM character starts with `logon = current_time` in [recycle.c:321](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:321). Saving writes accumulated playtime plus current-session elapsed time in [save.c:192](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:192). Age and score use played-plus-session time, and [fight.c:1947](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1947) uses it for the quarter-hours-per-level XP factor. A new login must not count the offline interval as active playtime.

**Python:** `Character.from_json` restores stored status timing fields, and [ConnectionHandler._nanny](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:443) promotes the player without establishing a new session timing baseline. [CharacterService.py:123](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:123) serializes those fields unchanged. No runtime path updates `played` or establishes a fresh `logon`. [Info.py:264](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:264) and [CombatHandler.py:832](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:832) then count the entire time since that stale timestamp.

**Reproduced:** A fresh session entering production `_nanny` retains `played=3600` and `logon=now-72000`. Production score prints `18 years old (21 hours)`, and serialization still writes the original timing values. With the same level-20 player, no-alignment target, and minimum random reward roll, production `xp_compute` returns **21 XP** with the stale baseline versus **9 XP** when logon is correctly set to now. The probe uses supplied persisted values and mocks transport/account lookup; it does not rely on an external service's behavior.

**Consequence/remedy:** Offline time can inflate XP rewards and displayed age, while records with zero logon can fail to accumulate session time. Establish timing at actual world entry and accumulate it in persistence snapshots. Distinguish a fresh login from reconnection to an existing live/link-dead body, and keep live-state reads on the socket loop. Verify quit/relogin, autosave, server restart, and switched originals without double-counting sessions. No change to idle-disconnect policy is needed to demonstrate this timing discrepancy.

### F05 — P2: Attack merging removes visibility protection from weapon-proc notices

**Trigger:** An attack produces a weapon-proc room notice for an invisible weapon that a bystander cannot see.

**Reference:** [fight.c:642](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:642) emits the flaming-weapon notice using `$p`; [comm.c:2521](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2521) substitutes the object according to recipient visibility. An unseen weapon is described generically rather than by its hidden description.

**Python:** The elemental renderer correctly creates a `RecipientText` with individual variants. However, the ordinary [one-hit path](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:1089) merges the proc result into the attack through [_merge_attack_payloads](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:1453), which explicitly applies `str()` to both message operands. That discards all variants and retains the base string containing the real object description.

**Reproduced:** With the actual flaming-weapon payload and an invisible blade, production rendering for Cara yields `Bob is burned by something.` After production attack merging with a nonempty base hit, the result is plain `str`. Real standard-handler/message-bus delivery to Cara contains `Base hit.` followed by `Bob is burned by an invisible blade.` The helper was correct before integration; the downstream merger causes the disclosure.

**Consequence/remedy:** Combat exposes hidden object descriptions despite focused visibility tests passing. Preserve recipient-aware text through attack concatenation and any later condition/round construction. Add a regression that carries the result from weapon-proc rendering through combat merging to actual delivery. The existing elemental concatenation test uses `WeaponHitHandler._merge`, which preserves variants, and therefore does not cover `FightHandler._merge_attack_payloads`.

## Scope and coverage

This pass inventories **214 Python source files, all 30 reference C translation units, 17 collection snapshots, and all 134 current top-level unittest modules**. Collection-query preceded authored-data inspection, including the three punctuation records, pose, teleport, plague, and the GameData identity. Inventory remains 221 commands, 38 skills, 97 spells, 244 socials, 412 special records, 986 mobiles, 1,266 items, 3,127 rooms, and 5,196 resets. These counts describe scope, not a claim that every document or branch is equivalent.

| C source families | Current Python evidence | Depth / material gaps |
| --- | --- | --- |
| `interp.c`, `alias.c` | Public interpreter, alias/prefix and command-access paths; prior parser regressions and new shortcut probes | End-to-end sampled input paths; arbitrary prefix semantics remain unresolved |
| `act_comm.c`, `act_info.c` | Communications dispatch/channel helpers, score, shared display; delivery probes and broad speech/tell/social/information tests | New F01/F02/F04; not every output template or social audited |
| `act_move.c`, `act_enter.c`, `scan.c` | Movement/random-room/portal helpers, followers, origin retention; movement/entry/wake suites | Current helper traces plus regression evidence; scan branches not freshly re-traced individually |
| `act_obj.c`, `healer.c` | Shop pricing/stock/pets, factories, object ownership; object/healer suites | Representative source inspection and extensive existing tests; fountain/theft fixture gaps remain |
| `fight.c`, `effects.c` | Attack/proc composition, XP, escape/death helpers, acid/elemental exposure; combat/exposure suites and delivery probe | F04/F05; not exhaustive roll combinations; reward fixture errors remain |
| `magic.c`, `magic2.c` | Actual teleport lambdas, relocation/rendering, random-room/resource helpers; spell/targeting/breath suites | F03; all 97 spells not independently traced this pass; energy-drain assertions unresolved |
| `skills.c`, `const.c` | Learning/class/proficiency/advancement helpers; learning, stat and advancement suites | Sampled current Python rules and suite evidence; full table equality/character creation unverified |
| `update.c` | Entity/home cleanup, weather/tick scheduling, item/effect updates; prior-fix and tick/weather suites | Previous cleanup fix retained; no exhaustive cross-entity traversal timing proof |
| `db.c`, `db2.c` | Resets, factories and population tests; origin tracking retained | Runtime spawn/reset sampling; full legacy-area conversion not re-audited |
| `special.c` | Mobile/special/pulse tests and current scheduler interfaces | Suite-backed domain coverage; every data lambda not freshly traced |
| `handler.c`, `lookup.c`, `tables.c`, `flags.c` | Shared lookup/visibility, flags/enums, effect helpers; focused boundary tests | Selected contracts; no complete table-value comparison |
| `act_wiz.c`, `ban.c` | Existing administration/recovery/targeting/force/movement/site-ban suites | Regression sweep; not every administrator mutation independently re-reviewed |
| `note.c` | Current read/remove/delete/recipient/draft paths and note tests | Selected Python traces and suite evidence; live service behavior unverified |
| `comm.c`, `save.c` | Fresh login, status snapshots, score/XP timing, wire/persistence/reconnect suites | F04; offline resource regeneration/service ownership requires further contract tracing |
| `music.c`, `recycle.c` | Reference timing initialization; allocation/music inventory | Timing initialization traced; C free lists and product music delivery not asserted equivalent |

The previous five findings are not carried forward as open: all **15 `test_repository_parity_remediation` tests pass**. In particular, observer-specific casting announcements, fallback attack alternatives, displaced-NPC eligibility/removal, punctuation tokenization, and preserved argument spacing remain covered. F01 concerns dispatch after tokenization; F03 concerns relocation notices after casting announcements; F05 concerns combat merging after elemental rendering.

## Validation

Ran every `tests/test_*.py` module in an isolated process using the repository Python 3.14 environment, with `PYTHONPATH=src` and local loopback access required by Windows asyncio. **134 modules / 1,639 reported tests; 122 modules pass, containing 1,330 tests.** No module timed out. The same 12 modules as the prior review/remediation snapshot remain non-passing, with identical failure/error identifiers: **4 failures and 29 errors**. Two additional focused remediation cases explain the test-count increase from the earlier full-run snapshot.

| Remaining non-passing module | Observed limitation |
| --- | --- |
| `test_combat_group_rewards` | 11 fixture errors: missing `points` |
| `test_combat_handler_aggression` | Stubbed `InterpApi` lacks `command_payload` |
| `test_combat_survival` | Fixture bus lacks `connection_manager` |
| `test_command_authorization` | Symbolic `IM` expectation fails |
| `test_final_combat_parity` | Stubbed movement utility lacks `DIR_NAME` |
| `test_import_rom_helps` | Imports a module deleted in the pre-existing working tree |
| `test_mobile_pulse` | Fixture actor lacks `add_item` |
| `test_object_fountain_commands` | Six parser-stub errors |
| `test_object_theft_parity` | Messaging module stub is not a package |
| `test_player_handler_cast_prompt` | Messaging package import failure |
| `test_remaining_gameplay_parity` | Five fixture errors: missing `handler_service` |
| `test_spell_affect_payload_messages` | Three energy-drain assertions fail; not newly demonstrated gameplay defects |

Read-only production probes independently reproduce the five findings; they are discrepancy assertions, not desired-behavior regression tests. C expectations are source-derived, not observed from an executable C server. Passing tests, especially stub-heavy modules, do not prove domain-wide parity.

- [Production probe source](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-second-probes.py)
- [Observed outputs](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-second-probes.json)
- [Complete isolated test results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-second-tests.json)
- [Previous review and remediation record](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31.md)

## Unresolved differences and exclusions

The previous prefix-abbreviation and idle/limbo/autoquit policy differences remain unresolved. No new authorization to change them is inferred. Whether the generic pose content intentionally replaces the class/level table also remains unconfirmed; the exception in F02 is independently actionable. Offline load-time regeneration is present in C `save.c`, but responsibility across the Python runtime and external character service was not established sufficiently to count it as a further confirmed defect.

Designer-owned data, service-backed storage/authentication, asynchronous messaging, dynamic enums, and managed Python memory are accepted architecture choices. Their structural differences are not findings. This review does not certify complete parity over every source function, content document, input, probability outcome, save/reconnect sequence, or live service transformation. Legacy `tests/old-tests`, exhaustive area-data comparison, real sockets, and executable-C differential validation remain outside the completed evidence.

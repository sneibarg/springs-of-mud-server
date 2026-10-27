# Repository-wide Python review and regression verification

Reviewed October 25, 2026 using the repository `python-code-review` skill and applicable `AGENTS.md`. Target: commit `e93105c8f2dbd9a2b512e075e9b992c3b8282c1c` plus the current working tree, including all recent application fixes and both fixes documented in `python-code-review-regression-2026-10-25.md`.

## Result

**No additional actionable application findings or newly verified regressions were found in this review.** The two issues from the immediately preceding review remain addressed under the checks below. There is no new correctness finding to implement from this report.

This does not mean the entire repository is defect-free: seven previously observed test modules still fail, external persistence contracts remain unverified, and the previously deferred authentication issue remains unchanged. Those limits are recorded separately below rather than presented as new regressions.

## Regression assessment

| Area | Evidence and result |
| --- | --- |
| Pending quit save and world progress | The strengthened selected-player test completes the entity update and advances an unrelated player while the quitting player's save remains pending. Retirement is checked before lock acquisition and again inside the lock. A tick already running still finishes before quit snapshots the character. No recurrence of the previous world-update stall was observed. |
| Item ownership and final-save consistency | Item mutations and effect-aware expiration complete synchronously on the socket event loop before notices are delivered. Tests cover pickup and transfer during paused output, direct and nested items, once-per-pulse ticking, completed timers in final saves, and unrelated item updates during a retired owner's pending save. No recurrence of the previously reproduced ownership race was observed. |
| Expiration and deferred notices | Existing update tests cover room/player/NPC inventory expiration, shop credit, nested-message suppression, corpse contents, and effect notices. An additional runtime probe applied a real worn +2 strength effect with duration zero to an item with timer one. Actual effect expiration and item decay restored strength and cleared the equipment slot before either notice was delivered. Character serialization observed that completed state at both sends. |
| Earlier application fixes | Both application regression suites pass. Coverage includes denial-message uniqueness and terminal rejection, freeze authorization, group tells, room rates, stable equipment-effect provenance across hydration, combat counters, clone independence, nested socials, equal-timestamp note cursors, world-item lookup, and quit save/failure behavior. No additional defect was verified in the traced paths. |

The latest item-update implementation has no await between its world-item selection and state mutations. Async delivery follows that phase, so gameplay input cannot invalidate ownership during the mutations. Expiration uses the existing effect-aware detachment operations. The removed expiration wrapper has no remaining callers in source or tests. No performance improvement is claimed or benchmarked.

## Architecture, object ownership, and DRY

The reviewed changes retain the repository's intended boundaries: designer content owns payloads, character state owns persisted counters/cursors, handlers coordinate async output and lifecycle operations, and existing item-ownership traversal supports live-world lookup and detachment. Hydration restores transient wearer relationships without serializing those runtime references.

The entity tick wrapper adds synchronization and lifecycle validation, so it is justified rather than a redundant forwarding layer. Shared social parsing and live item traversal address demonstrated duplication without adding another dispatch or ownership framework. No new nonblocking design recommendation or additional design pattern is warranted by the evidence from this pass.

## Verification

- Parsed all **336 Python files** under `src` and `tests` successfully.
- Ran all **86 top-level unittest modules in separate interpreters** with `.venv/Scripts/python.exe` and `PYTHONPATH=src`: **79 passed, 7 failed, 1,060 test executions**. Counts include imported test classes and loader placeholders rather than deduplicated test identities. Async tests used the local socket access required by Windows asyncio.
- The application suites pass **25 tests** in `test_review_application_fixes` and **22 tests** in `test_fresh_review_fixes`. The update suite passes **33 tests** in `test_update_handler_active_players`. These executions are included in the repository totals.
- The same seven modules fail as in the immediately preceding verification: `test_area_pet_shop_resets`, `test_combat_api_dynamic_checks`, `test_combat_death_rules`, `test_combat_group_rewards`, `test_object_fountain_commands`, `test_player_handler_cast_prompt`, and `test_spell_affect_payload_messages`. Known failures include fixture/stub contract problems and three unresolved energy-drain assertions. Their persistence limits confidence; matching failing module names alone does not prove identical root causes.
- Ran the additional worn-effect/decay/serialization probe described above using real models and runtime methods with mocked output and message lookup. No source or permanent test edits were needed.
- `git diff --check` passes. This review adds only this Markdown report and preserves all existing application changes, fixtures, collection snapshots, and earlier reports.

## Scope and limitations

Repository-wide inventory, parsing, and test execution were combined with manual tracing of current diffs and representative startup/injection, admission and cleanup, interpreter authorization and nested execution, scheduling and autosave, final-save lifecycle, world/item ownership, effect application/removal, combat modifier readers, hydration/serialization, clone behavior, notes, and message delivery. This was a risk-based review, not a line-by-line execution audit of every function.

Legacy `tests/old-tests` files were parsed but not executed in the top-level pass. Aggregate test discovery's known global-module-stub contamination was not repaired or remeasured. No untouched checkout baseline was run during this pass; regression comparison uses the preceding recorded verification and the inspected changes.

The external content service must retain `hitRoll`, `damRoll`, `savingThrow`, `noteReadStamps`, and `noteReadIds`. Local wire round trips are covered; a live external persistence round trip remains unverified. No live listener, external account/content writes, deployment, restart, or ROM24 parity audit was performed. The previously user-deferred identifiers-only authentication finding remains outside the new-findings result and was not changed.

# Repository-wide Python regression review

Reviewed October 25, 2026 using the repository `python-code-review` skill and `AGENTS.md`. Target: commit `e93105c8f2dbd9a2b512e075e9b992c3b8282c1c` plus the current working tree, including both rounds of application fixes and the login-rejection follow-up.

**Two actionable findings were verified.** R1 is a regression in the newly added synchronization. R2 is an existing ownership race left uncovered by that synchronization; it means the previous report's R3 lifecycle issue is not completely resolved. This review changes only this report. Source, tests, collections, and live services were not changed.

## Implementation follow-up — October 25, 2026

**Both findings are resolved in the working tree.** Original review evidence is retained below.

- **R1:** Entity ticks check retirement before waiting on the character lock and recheck after acquisition. An already-running entity tick still finishes before quit takes its final snapshot. Item updates no longer wait on a retiring player's persistence lock.
- **R2:** Item updates finish effect changes, timer changes, and effect-aware expiration synchronously on the socket event loop, then deliver queued notices. No gameplay coroutine can pick up, transfer, or retire an owner between selection and mutation. Expiration also removes items before yielding for its notice. This uses the existing world traversal and adds no full-world lookup per ordinary item. Message routing and nested-content expiration rules remain covered by the existing update suite.
- Strengthened the selected-player test to require another player to tick while the quit save is still pending. Updated the owned-item test to require a complete final timer snapshot during paused output. Added coverage for pickup and player transfer during output, including nested contents and once-per-pulse ticking; expiration before output; and unrelated item progression during a retired owner's pending save. The latest regression suite now passes **22 tests**; the earlier application suite passes **25**, and the update suite passes **33**.
- Ran all **86 top-level unittest modules in separate interpreters**: **79 passed, the same seven modules failed, and 1,060 test executions ran**. All **336 Python files** under source/tests parse. After removing an unused expiration wrapper and updating the affected fixture seam, reran the latest regression and update suites successfully. `git diff --check` passes.
- No collections, external contracts, or live services were changed. No deployment or live server restart was performed. The seven previously observed failing modules remain unresolved.

## Original correctness findings (resolved)

### R1 — [P2] A retired player's pending save blocks updates for the rest of the world

Primary location: [EntityUpdateHandler.py:55](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/EntityUpdateHandler.py:55). The same pattern occurs at [ItemUpdateHandler.py:35](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/ItemUpdateHandler.py:35). Related lock lifetime: [PlayerHandler.py:75](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:75), including the save awaited at line 109.

Both tick paths acquire the character's async lock **before** checking `world_retired`. Quit holds that lock throughout its final HTTP save and departure output. If an update selected the character before quit retired it, the update waits for the entire save before discovering that it should skip the character. Entity and item updates process their lists sequentially. `GameService` also waits for the complete world pulse before scheduling another one, so this wait delays unrelated regeneration, item updates, combat pulses, and input wait/daze countdowns. The content worker is shared and ordered, so queued I/O can extend the wait beyond one request's timeout. Socket input still runs; this is a stall in world progression, not a blocked Python event loop.

**Reproduction:** used the actual `EntityUpdateHandler.update` and `PlayerHandler.do_quit` with three real Character models. Paused the first character's tick at an awaited message, started the second character's quit with a suspended save, then released the first tick. The second character was already retired, but the update remained pending and the third character's thirst remained 48. Only after releasing the save did the update finish and reduce the third character's thirst to 47. The existing overlapping-quit regression tests verify the retired character stays unchanged, but do not assert progress for other characters while persistence remains pending.

**Focused remedy:** let already-retired players be skipped before waiting on their update lock, and recheck eligibility after acquiring the lock. Preserve the lock for a tick already in progress so quit still snapshots its completed state. Apply the rule to both entity and owned-item updates. Add a regression that leaves the save pending while asserting that an unrelated player and the world pulse can advance.

### R2 — [P2] Item-update selection uses stale ownership and can mutate a player after its final save

Location: [ItemUpdateHandler.py:31](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/ItemUpdateHandler.py:31), especially the captured `location['parent']` used at lines 33–39.

The update snapshots item references **and their ownership locations** before any item is ticked. Earlier item messages can yield to ordinary gameplay. If a player picks up a later room item during that yield, the later item still carries its old Room parent in the update snapshot. It therefore bypasses the player's lock and retirement check. Giving an item to another player can similarly make the update consult the former owner's lifecycle. Fixing only R1's early retirement check would not fix this race.

**Reproduction:** selected two room items, paused the first item's effect-message phase, moved the second item into a real player's inventory, and completed that player's actual quit with a captured final save. Releasing the update changed the carried item's timer from the saved value 3 to 2 despite its owner being retired. A second probe used timer 1 and the real `expire_item` path: the saved timer was 1, the live timer became 0, and the item remained in the retired player's inventory because world lookup could no longer locate that player. After re-adding the player to the room and running another item update, the item was still carried with timer 0. `Item.tick_timer` only expires a timer when a positive value reaches zero, so the missed removal is not retried.

**Attribution:** item references could already outlive ownership changes before the last fix. The new locking did not introduce that underlying race, but its reliance on the selected location leaves the claimed final-save invariant incomplete. Existing tests cover items that were already carried when selected, not items acquired or transferred after selection.

**Focused remedy:** validate current ownership and world presence when selecting the mutation boundary, coordinate with the current player owner, and revalidate after any wait that could change ownership. Skip objects no longer in the live world. Preserve once-per-pulse traversal, nested-content handling, and effect-aware expiration. Cover room-to-player pickup, player-to-player transfer, retirement before a queued item tick, and a timer reaching zero across those interleavings. Avoid adding a whole-world search per item without assessing its cost; use the existing ownership operations or a narrowly maintained ownership contract.

## Architecture and maintainability

The fixes otherwise follow the repository's domain and data boundaries: stable effect provenance, character-owned combat counters and note cursors, independent cloned effects, shared social argument parsing, and reuse of live item traversal. No additional design-pattern framework is warranted. The remaining issue is the scope and timing of lifecycle/ownership validation, rather than a need for another scheduler or persistence abstraction.

No additional actionable regression was verified in the reviewed denial/freeze paths, group tells, room-rate preservation, equipment hydration/removal, combat-counter serialization, cloned effects, social dispatch, note boundaries, or wizard item lookup. This is a statement about the checks below, not a guarantee that those paths have no other defects.

## Verification and limitations

- Parsed all **336 Python files** under `src` and `tests` successfully.
- Ran all **86 top-level unittest modules in separate interpreters**, using `.venv/Scripts/python.exe` and `PYTHONPATH=src`: **79 passed, 7 failed, 1,057 test executions**. Counts include imported test classes and loader placeholders, not deduplicated test identities. Windows asyncio tests used the local socket access they require.
- Both application regression suites pass: **25 earlier application/login tests and 19 latest-fix tests**. Relevant equipment, persistence, note, wizard, dynamic command, combat, and update suites were also included in the repository pass.
- The same seven modules failed as in the immediately preceding review/fix verification: `test_area_pet_shop_resets`, `test_combat_api_dynamic_checks`, `test_combat_death_rules`, `test_combat_group_rewards`, `test_object_fountain_commands`, `test_player_handler_cast_prompt`, and `test_spell_affect_payload_messages`. The known fixture/stub failures and three energy-drain assertion failures remain unresolved; matching module names do not establish that every failure has the same underlying cause.
- Reproduced both findings using real runtime methods/models, deterministic asyncio gates, and mocked transport/persistence. The expiration variant used the real item expiration method. No permanent test or source modifications were made to run these probes.
- Manual tracing covered current diffs and representative startup/injection, authentication/admission/cleanup, interpreter authorization and nested dispatch, messaging, room/world/item ownership, character hydration and wire serialization, effects and combat modifier readers, cloning, note cursors, update scheduling, and final-save boundaries. Repository-wide parsing and tests complement this risk-based tracing; this was not a line-by-line execution audit of every function.
- Legacy `tests/old-tests` files were parsed but not executed in the top-level module pass. Aggregate discovery's known global-module-stub contamination was not repaired or remeasured. The seven failing modules limit confidence in their covered behaviors.
- External persistence must retain `hitRoll`, `damRoll`, `savingThrow`, `noteReadStamps`, and `noteReadIds`; this remains an unverified live-service contract. No external content/account calls, live listener, deployment, restart, or ROM24 parity audit was performed. The previously user-deferred identifiers-only authentication issue remains outside these findings and was not changed.
- `git diff --check` passes. Prior working changes and prior reports were preserved.

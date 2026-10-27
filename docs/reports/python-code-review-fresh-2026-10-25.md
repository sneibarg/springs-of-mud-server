# Fresh repository-wide Python review

Reviewed October 25, 2026 using the repository `python-code-review` skill and `AGENTS.md`. Target: commit `e93105c8f2dbd9a2b512e075e9b992c3b8282c1c` plus the current working tree, including the recent application fixes and login-rejection follow-ups. Earlier reports remain unchanged.

**Seven actionable application findings were verified.** R3 concerns the recent uncommitted quit implementation; the other findings are existing paths. Authentication remains the previously documented, user-deferred issue and is not counted as a new finding. This review changed only this report, not source, fixtures, snapshots, or live service data.

## Implementation follow-up — October 25, 2026

**All seven findings below are resolved in the working tree.** The original review evidence is retained below for reference.

| Finding | Resolution |
| --- | --- |
| R1 | Item contributions use stable persisted item IDs. Hydration recognizes legacy process-ID sources and restores equipped-item wearer associations without reapplying saved bonuses. Applying equipment effects replaces that item's prior contribution. |
| R2 | Characters own and persist hit-roll, damage-roll, and saving-throw counters. Legacy records without counters reconstruct them from existing effects once. Score displays use the same effective modifier reader as combat. |
| R3 | Entity ticks and quitting share a per-character async lock. Quit waits for an active entity tick before snapshotting; already-selected work skips a retired player. The subsequent regression follow-up moves item mutations before async notice delivery and skips retired players before waiting on locks; see `python-code-review-regression-2026-10-25.md`. Failed saves, including exceptions, restore update eligibility. Plague spread rechecks a recipient's retirement after awaited output. |
| R4 | Cloned item effects are deeply copied, including effects on nested contents. |
| R5 | Both interpreter boundaries parse social names with the existing argument utility while preserving the complete invocation for the social handler. |
| R6 | Note cursors persist read IDs at their boundary timestamp. Explicit reads and catchup preserve equal-timestamp unread notes, with deterministic list ordering. Legacy timestamp-only cursors retain their prior read semantics. |
| R7 | Wizard item searches reuse live room/item ownership traversal, including player and NPC inventories, equipment, and nested contents, without consulting offline character records. |

### Implementation verification

- Added `tests/test_fresh_review_fixes.py`: **19 regression tests pass**, covering legacy/current save-load behavior, equipment removal and refresh, authored combat effects, cloning independence, mixed world ownership, nested socials, note cursor collisions, overlapping quit/tick schedules, and save-exception rollback.
- Ran **86 top-level unittest modules in separate interpreters**: **79 passed and the same seven modules failed as in the review baseline**, with 1,056 test executions in that pass. After adding the final rollback test and adjustment, reran the new suite (19 passing) and the prior application regression suite (25 passing). No additional failing module was observed.
- `git diff --check` passes. Existing unrelated working changes were preserved; this implementation made no collection edits or live service writes.
- Persistence now emits `hitRoll`, `damRoll`, `savingThrow`, and `noteReadIds` alongside `noteReadStamps`. Local JSON round trips are covered; an external content service must retain these fields. No live listener, external persistence round trip, deployment, or production restart was exercised. Previously corrupted saved stats are not automatically repaired beyond recognizing legacy equipped-item sources and reconstructing omitted combat counters.

## Original findings (resolved)

### R1 — [P1] Equipped-item effects cannot be removed correctly after save/load

Locations: [EffectHandler.py:278](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/EffectHandler.py:278), [EffectHandler.py:284](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/EffectHandler.py:284), [Character.py:91](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/Character.py:91).

Item-effect ownership uses `item:<item.id>:<id(item)>`. Character persistence saves those source strings, the already-modified character attributes, and equipped items. Loading creates new Python item objects while retaining the old effect source strings. Removing the restored item constructs a source with the new memory identity, finds no matching character effects, and leaves the bonus applied. Loading also does not restore `_effect_wearer`, so subsequent changes to a restored worn item's affects cannot refresh its wearer through that reference.

**Verified:** a real Character started at strength 13, reached 15 when wearing a +2 ring, and remained at 15 after JSON save/load and ring removal. One item-derived character effect remained. The persisted source and newly computed source differed only in their process-specific object identity. Re-equipping can consequently add another contribution without removing the orphaned one, enabling permanent stat stacking across reloads.

**Focused remedy:** use stable ownership identifiers across persistence and explicitly reconstruct wearer associations during hydration. Define how existing saved memory-identity sources are migrated or reconciled without double-applying bonuses. Cover save/load/remove/re-equip, two distinct items with similar definitions, nested equipment serialization, item expiration, and live changes to a restored worn item. Preserve the designer-owned effect definitions.

### R2 — [P2] Player hit-roll, damage-roll, and saving-throw affects silently do nothing

Locations: [EffectHandler.py:83](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/EffectHandler.py:83), [EffectHandler.py:99](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/EffectHandler.py:99), [FightUtil.py:132](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/FightUtil.py:132), [Character.py:26](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/Character.py:26).

The effect handler changes these modifiers only if the target already exposes `hit_roll`/`hitroll`, `dam_roll`/`damroll`, or `saving_throw`. Real player Characters declare none of those fields. Combat reads the dynamic fields with a zero fallback, and spell saves likewise default the absent saving throw to zero. The affect records can therefore appear on the player without affecting the corresponding calculation.

**Verified:** direct application of +5 hit roll, +7 damage roll, and -4 saving throw to a real Character left all three effective modifiers at zero. Applying the checked-in bless affect definitions at level 24 created the expected +3 hit-roll and -3 saving-throw records, but both effective values remained zero. The spell fixture supplied the constructor's required class maps while retaining the authored affect data unchanged. Existing effect tests use stand-ins that explicitly provide these fields, concealing the real-model mismatch.

**Focused remedy:** establish a canonical owner for these effective modifiers, including initialization, application/removal, persistence, and the combat/save readers. Avoid adding independent counters that will drift from saved effects. Add real-Character regressions for bless, curse, frenzy, equipment, expiration/dispel, and save/load; retain the existing content-driven magnitudes and durations.

### R3 — [P2] An in-flight world update can mutate a character after its final quit snapshot

Locations: [EntityUpdateHandler.py:36](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/EntityUpdateHandler.py:36), [PlayerHandler.py:100](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:100), [UpdateHandler.py:90](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/UpdateHandler.py:90).

The recent quit implementation removes the character from room/playing membership and marks its session disconnecting before saving. This excludes future selections, but `EntityUpdateHandler.update` may already hold the Character in its `active_characters` list or a room snapshot. After awaiting another entity's messages, it proceeds with that old reference without checking current ownership or retirement. Changes made after the final save snapshot are lost when quit completes, because the character has left subsequent autosave selection.

**Verified:** paused an actual entity update while it delivered a hunger message for the first player, then started a second player's quit with a held save. The quit snapshot contained thirst 48. Resuming the original update ticked the retired second player, changing live thirst to 47. Quit then completed with the persisted snapshot still at 48. This used real Character condition ticks and mocked message delivery/persistence, not a live service.

**Focused remedy:** make retirement visible to already-selected update work and revalidate ownership after relevant awaits. Cover both the active-character list and room snapshots, as well as an entity tick already in progress. Define the save boundary explicitly; a second event loop or a thread lock held across awaits would not solve this safely. Add a deterministic regression that interleaves a held message, retirement, snapshot capture, and resumed ticking.

### R4 — [P2] Cloning an item shares mutable affects with the original

Location: [ItemUtil.py:394](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/ItemUtil.py:394); caller: [Wiz.py:901](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:901).

`clone_object_instance` first constructs an independent item, then overwrites its effects with `list(original.effects)`. That copies the list while retaining each original Effect object. Enchantment and timed effect updates mutate those records in place, so changing a cloned item can also change its source. Shared duration records may also be decremented once per owning item during a world tick.

**Verified:** the cloned item's first Effect was the identical Python object as the original's. Setting the clone's modifier to 99 also changed the original's modifier to 99. Existing cloning coverage verifies nested container independence but does not check effect identity.

**Focused remedy:** preserve independent effect records during instance cloning, including nested children. Reuse the existing safe effect-copying mechanism or retain the independent effects produced during construction. Test mutation, enchantment, expiration, and clone removal without altering the source item or its wearer's contributions.

### R5 — [P2] Targeted socials still fail through nested command execution

Location: [PlayerHandler.py:565](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:565); corrected neighboring path: [InterpHandler.py:83](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/InterpHandler.py:83).

Normal interpreter fallback now looks up the social verb separately from its argument. The nested interpreter still uses `raw_command.lower()` as the social name. Commands such as `at ... smile Tester`, or targeted socials executed through force/order, look for a social named `smile tester` and emit `Huh?` instead of invoking the social handler.

**Verified:** `_interpret_nested_command(..., 'smile Tester')` queried `name='smile tester'`, made zero social-handler calls, and returned `Huh?` despite a valid `smile` social being available.

**Focused remedy:** use the same verb/argument resolution at both interpreter boundaries while preserving actor authorization and freeze policy. Prefer the existing parsing utility over a new dispatch framework. Exercise targeted, untargeted, mixed-case, and whitespace-separated socials through at/force/order as well as ordinary input.

### R6 — [P2] Reading one note marks other notes posted in the same second as read

Locations: [NoteHandler.py:102](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:102), [NoteHandler.py:216](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:216).

Posting uses `int(time.time())`, while unread selection requires `note.date_stamp > last_read`. Reading the first of two notes with the same timestamp advances the cursor past both, even though the second note has not been displayed. The newly persistent cursor preserves this skipped-unread state across save/load. The note remains accessible by explicit number, but normal next-unread traversal misses it.

**Verified:** supplied two visible notes with distinct IDs/subjects and timestamp 123. The first `note` invocation displayed FIRST; the next said `You have no unread notes.` without displaying SECOND.

**Focused remedy:** use an unambiguous cursor, such as a stable timestamp/ID ordering with matching comparison semantics, or track read identities at the boundary timestamp. Changing only client clock precision is insufficient if content-service timestamps can collide. Cover equal timestamps, pagination/list numbering, explicit reads, catchup, out-of-order service responses, and legacy cursor migration.

### R7 — [P2] Wizard world-item lookup crashes on registered NPCs

Location: [WizUtil.py:109](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/WizUtil.py:109); callers include [Wiz.py:578](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:578) and [WizSetApi.py:324](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/WizSetApi.py:324).

`AreaHandler` registers live NPCs in CharacterRegistry, but `find_world_item` assumes every entry has a player's `loot` attribute. Mobile uses `inventory` and has no `loot`. A search that reaches an NPC before finding its target raises rather than continuing into room objects. World object inspection/set/string paths can consequently abort; an uncaught command exception ends the invoking connection's game loop. Registry set iteration makes the failing order variable when both players and NPCs are present.

**Verified:** the real helper with a Mobile entry raised `AttributeError: 'Mobile' object has no attribute 'loot'` before searching rooms. Confirmed that normal area resets register these NPCs into the same registry. Existing world-lookup tests cover mixed entity-name lookup, but not this item traversal.

**Focused remedy:** reuse authoritative live item traversal through the existing Room/ItemOwnership operations, or explicitly use each entity's owned-item contract. Avoid replacing the exception with a silent skip that loses NPC inventory, equipment, or nested contents. Test a mixed player/NPC registry, room items, worn items, nested containers, and offline character records.

## Object design and DRY recommendations

The findings demonstrate ownership mismatches rather than a need for more frameworks. Item-derived effects need stable persisted provenance and an explicit hydration contract. Effective character modifiers need one authoritative representation shared by application, removal, serialization, and combat. Retirement needs a lifecycle invariant observed by update work that has already yielded.

R5 shows concrete drift between two implementations of command/social resolution. R7 bypasses existing item-ownership abstractions and assumes one concrete inventory layout. Consolidating those demonstrated shared rules would simplify callers, at the cost of updating their fixtures and preserving authorization/visibility/ownership behavior. Do not unify differently owned content merely because its strings look alike, or serialize transient world references to compensate for missing lifecycle reconstruction.

No additional Strategy, State, Factory, event-bus, or repository framework is warranted by these findings. Small changes at the existing domain and interpreter boundaries are sufficient; regression coverage should precede broader refactoring.

## Verification and limitations

- Parsed all **335 Python files** under `src` and `tests`. An AST scan found no mutable literal function defaults or same-class calls with excessive positional arguments after accounting for static methods. These checks do not establish behavioral correctness.
- Ran all **85 top-level unittest modules in separate interpreters** using `.venv/Scripts/python.exe` and `PYTHONPATH=src`: **78 passed, 7 failed, 1,038 test executions**. Counts include imported test classes and loader placeholders and are not deduplicated. Windows async tests used the local socket access required by asyncio.
- The same seven failing modules were observed in the earlier review runs: `test_area_pet_shop_resets`, `test_combat_api_dynamic_checks`, `test_combat_death_rules`, `test_combat_group_rewards`, `test_object_fountain_commands`, `test_player_handler_cast_prompt`, and `test_spell_affect_payload_messages`. Failures involve stub-package contracts, incomplete fixtures, and three energy-drain assertions whose underlying cause remains unestablished. They were not converted into production findings solely from failing assertions.
- The recent application/login regression suite passes all 25 tests. Its current quit test covers selection after retirement, but not a world update that selected the character before yielding; R3 exercises that missing interleaving.
- Reproduced all seven findings with actual relevant runtime methods/models and mocked I/O. The bless probe retained the checked-in affect definitions and supplied required class-map fixture fields. Collection inspection used the prescribed collection-query CLI/loader; no collections were edited.
- Fresh manual tracing covered representative startup/injection and service contracts, registry/world ownership, admission/command boundaries, message delivery, save/load/reloads, spells and effects, combat modifier readers, item cloning/traversal, update scheduling, and note cursors. Repository-wide inventory and tests were combined with deeper investigation of these higher-risk paths; this was not a line-by-line execution audit of every function.
- Legacy `tests/old-tests` files were included in parsing but not in the top-level module execution pass. Aggregate discovery's previously documented global-stub contamination was not repaired or remeasured here. No live game listener, external content/account service, deployment, production restart, or ROM24 parity audit was exercised. The external service's support for `noteReadStamps` remains an unverified contract dependency from the earlier implementation follow-up.
- The previously deferred identifiers-only authentication issue remains outside these new findings and was not changed. No untouched-revision baseline was checked out; only R3 is specifically attributed here to the recent uncommitted implementation by tracing its added retirement/save boundary.

`git diff --check` passes for the existing working changes. This review leaves those changes intact and adds only this Markdown report.

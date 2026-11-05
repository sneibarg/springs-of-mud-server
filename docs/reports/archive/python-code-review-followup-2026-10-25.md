# Repository Python code review — follow-up

Reviewed October 25, 2026 at commit `e93105c8f2dbd9a2b512e075e9b992c3b8282c1c`, using the repository `python-code-review` skill and `AGENTS.md`. The working tree was clean at the beginning of this pass. This report preserves the earlier review and its implementation history in `python-code-review-2026-10-25.md`.

The review identified six additional runtime findings, one previously documented authentication issue, and an existing test-isolation problem. The original findings below describe the reviewed snapshot; they are not attributed to a particular introducing commit. No production source, tests, or collection data were modified during the review itself.

## Implementation follow-up — October 25, 2026

Application findings **1, 2, and 4–7 are addressed** in the working tree. Finding **3 remains unchanged at the user's request**. T1 concerns test infrastructure and was outside the requested application fixes.

| Finding | Implemented behavior |
| --- | --- |
| 1 — Quit persistence | A valid quit temporarily retires the player from room/playing membership and marks its session disconnecting before capturing the ordered final save. Successful persistence completes departure; failure or cancellation restores membership and session status. Reconnects cannot attach while that save is pending. No farewell is emitted after a failed save; its response is authored in the quit command's `payload.toChar.unsaved`. |
| 2 — Character denial | Admission checks canonical `PLR_DENY`, including authoritative live characters and a recheck after a takeover confirmation. Rejection precedes session binding or replacement of the existing connection. Account bans and allowed sibling characters retain their separate behavior. |
| 4 — Freeze | Shared command authorization enforces `PLR_FREEZE` on the controlling player. Normal and nested social fallback enforce the same restriction. Forced/ordered/nested commands cannot bypass it; NPC act bits are not interpreted as player flags. Command payloads may override `command_frozen`. |
| 5 — Group tells | Existing world group membership selects recipients, excluding the sender and NPCs while including remote player members. Authored text and missing-input guards remain in content. |
| 6 — Note cursors | Character owns a persistent, monotonic `note_read_stamps` mapping; NoteHandler uses that model operation. Serialization emits `noteReadStamps`; loading legacy or null fields supplies independent empty mappings. Runtime context remains excluded. |
| 7 — Room rates | Model defaults are 100; construction preserves explicitly supplied rates, including zero. RoomService and real regeneration paths are covered. |

**Verification:** 21 new real-model regressions passed in `tests/test_review_application_fixes.py`. All 85 top-level modules were then run in separate interpreters: **78 passed and the same seven modules failed** as in the review baseline, across **1,034 test executions**. The new suite accounts for the additional 21 executions. Existing note/persistence fixture assertions were updated to reference the persistent field. All Python sources/tests parse, and `git diff --check` passes. Semantic comparison confirms the Commands snapshot changes only the quit failure message. Authentication source is untouched.

**Content-service contract:** character PUT/GET documents now include `noteReadStamps`, an object mapping numeric note-type strings to nonnegative integer timestamps, for example `{"0": 123, "1": 456}`. The separate content service must retain and return this field for persistence across a live server restart. This repository implements and tests the wire round trip with mocked HTTP; the external service schema and deployment were not changed or verified. The authored quit message also requires loading the updated command content into the live service; the runtime has a fallback for older content.

The collection tool's validated atomic replace failed because Windows denied replacement of the open Commands file. Its generated output was compared semantically against the original, verified to contain exactly the intended field addition, and applied in place. No other collection document changed.

**Login rejection follow-up:** rejected sessions now transition to `DISCONNECTING` and record a terminal rejection before awaiting output. Re-entering admission cannot emit another denial or promote the session to playing, even if the flag changes during output. Transport closes in a `finally` block. A full Telnet-path regression verifies one denial on the wire, closed transport, no room entry, no playing binding, no game-loop dispatch, and session cleanup. Re-entry and snapshot checks are also covered. The current Characters snapshot has Janky's `act=8192`, which excludes `PLR_DENY`; it was preserved rather than removing unrelated bits. The 25 application regressions and 14 reconnect tests pass in separate processes. The reported production symptom was not reproduced against a running server in this follow-up.

## Correctness findings

### 1. [P1] Quitting removes a character from autosave without saving its final state

Location: [PlayerHandler.py:68](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:68).

`do_quit` emits farewell messages, removes the character from its room and the playing registry, and disconnects. Neither the authored `quit` lambda nor this path requests a character save. Disconnect cleanup also does not save. Autosave subsequently excludes the character because it is no longer a live room occupant or playing-session character.

After inventory, currency, practice, or other changes since the last save, a normal quit therefore leaves persisted state stale indefinitely while the character stays offline. A later server restart loses those changes. Remaining in the process's character registry can conceal the problem during an immediate reconnect.

**Evidence:** inspected the collection-backed quit command and its complete cleanup/save-selection path. A real-character probe removed the character from its room and observed zero calls to both queued and asynchronous persistence methods.

**Remedy:** capture and complete an ordered final save before removing the character from live ownership; handle persistence failure explicitly. Reuse the existing asynchronous persistence capability. Test successful quit after a state change, save failure, cancellation, and exclusion from subsequent autosaves. A mocked persistence round trip should demonstrate that the final state is recoverable after restart.

### 2. [P1] Character denial does not prevent the next login

Location: [ConnectionHandler.py:368](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:368); producer: [Wiz.py:967](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:967).

`deny` sets `PLR_DENY`, requests persistence, and disconnects its target. Login admission checks the account's `banned` property but never checks the character's denial flag. Authentication still resolves the denied character through account membership, so the same account can reconnect that character immediately. This is distinct from the account-wide `ban` command and from identity verification in finding 3.

**Evidence:** a real Character carrying `PLR_DENY` was accepted by `_nanny` and assigned `SessionStatus.PLAYING` with an unbanned account. Inspection of authentication and attachment found no preceding character-denial check.

**Remedy:** enforce character denial before binding a session or adding the character to playing state, using the canonical status bitfield. Test denial through the full login/reconnect path, persistence round trips, and an allowed sibling character on the same account.

### 3. [P1] Authentication still accepts identifiers without proof of identity

Location: [AuthenticationService.py:28](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/session/AuthenticationService.py:28).

**Previously reported, still present.** An AUTH payload succeeds when its account ID exists and its character ID belongs to that account. It requires no password, verifiable ticket, or authenticated upstream assertion. An untrusted caller who obtains these identifiers can impersonate the player, including a privileged character. Severity assumes an untrusted caller can reach the game listener; deployment gateway/firewall guarantees were not established by this review.

**Evidence:** the actual authentication service returned success for a payload containing only fictitious `accountId` and `characterId`, using mocked registries and message delivery. No real credentials or external service were used.

**Remedy:** verify an expiring account-service assertion bound to the selected account and character, or enforce and authenticate the trusted-gateway boundary. Cover absent, invalid, expired, and mismatched assertions. The earlier report records this issue as deferred; this review makes no authentication changes.

### 4. [P2] Freeze sets a flag that command execution never enforces

Location: [CommandAccess.py:70](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/CommandAccess.py:70); producer: [Wiz.py:358](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:358).

The freeze command sets `PLR_FREEZE` and tells the victim, “You can't do ANYthing!” Normal input dispatch and `CommandAccess.check` do not consult that flag. The collection-backed `say` command only guards against missing input, and the command collection contains no `PLR_FREEZE` guard. A frozen player can continue executing otherwise authorized commands.

**Evidence:** `CommandAccess.check` returned `None` (allowed) for the actual `say` command and a real Character carrying `PLR_FREEZE`. Traced normal dispatch through that authorization boundary and inspected the authored guards.

**Remedy:** enforce frozen-player input restrictions at the shared interpreter admission boundary, with an explicit policy for nested/forced commands and controlled bodies. Keep response text in the existing content/message mechanism. Test ordinary commands, socials, thawing, and the selected nested-command policy.

### 5. [P2] Group tells expose messages to unrelated room occupants

Location: [Communications.py:362](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:362).

`do_gtell` assigns `room.player_targets(character)` as the recipient list. That operation selects every other player in the room, regardless of group membership, and excludes group members elsewhere. The standard payload emitter sends the resulting list directly. Private group discussion is therefore delivered to bystanders while remote members miss it.

**Evidence:** with an unrelated local bystander and a remote character whose leader was the sender, the payload targeted only `bystander`. The runtime group predicate independently confirmed that the remote character belonged to the group and the bystander did not. The authored `gtell` payload/guard does not correct the target list.

**Remedy:** select live group recipients using the existing group-members operation and appropriate delivery filters. Preserve authored payload text. Test unrelated local occupants, local and remote group members, sender echo, and unavailable recipients.

### 6. [P2] Note read/catchup progress is lost across persistence

Locations: [NoteHandler.py:313](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:313), [CharacterService.py:87](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:87).

Read and catchup actions store their cursor exclusively in `character.context['note_read_stamps']`. Character persistence deliberately omits runtime context and has no separate field for these cursors. After a persisted character is restored, its first read treats previously consumed notes as unread. Manual save and autosave cannot preserve that progress.

**Evidence:** marking a real Character's note cursor as `123`, JSON-serializing it through `CharacterService`, and restoring it through `Character.from_json` changed the cursor from `123` to `0`.

**Remedy:** give note-read progress an explicit persistent field and wire contract, defaulting legacy records to an empty mapping. Do not serialize the entire runtime context, which also holds transient state and references. Test read/catchup save-load behavior independently for each note type and legacy documents.

### 7. [P2] Room construction discards explicitly supplied regeneration rates

Location: [Room.py:58](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/Room.py:58).

The Room dataclass accepts `heal_rate` and `mana_rate`, but `__post_init__` unconditionally replaces both with `100`. `RoomService` passes normalized room fields into this constructor, so a content-service document supplying these rates loses them before regeneration reads the room. This defeats data-driven tuning of an existing runtime capability.

**Evidence:** `Room(id='r', heal_rate=250, mana_rate=175)` produced rates `(100, 100)`. The checked-in room snapshot currently contains neither rate field, so the impact is conditional on supplying explicit values through the supported model/service path; this is not a claim that existing snapshot rooms currently regenerate incorrectly.

**Remedy:** put the normal rate in the dataclass defaults and preserve explicit values during initialization. Test both omitted values and nondefault values through RoomService, followed by real entity regeneration. No new design pattern is needed.

## Test infrastructure finding

### T1. [P2] Global import stubs prevent the prescribed aggregate suite from being a useful gate

Examples: [test_note_commands.py:25](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_note_commands.py:25), [test_command_authorization.py:18](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_command_authorization.py:18).

Several modules install stubs into `sys.modules` during import, sometimes without restoration. Later tests inherit fake API classes or packages instead of their intended runtime dependencies. Aggregate discovery reports thousands of failing subtests even though most modules pass in fresh interpreters. This issue was also identified by the earlier review and remains actionable.

Restore import state around fixture loading, or run the incompatible suites in isolated subprocesses through a supported test runner. Fix incomplete fixture contracts separately. Preserve the isolation purpose of narrow unit tests; replacing every test double with an entire server bootstrap would add unnecessary dependencies.

## Object design and DRY assessment

The existing command authorization, group selection, ordered persistence, and content-owned payload abstractions are suitable owners for the fixes above. Reuse them rather than repeating denial/freeze checks in individual commands, implementing another group traversal, or adding an independent save worker.

Note read cursors are persistent domain state currently mixed into a transient context bag; an explicit model field is the smallest useful ownership correction. Room defaults belong in the model's declared defaults rather than destructive initialization. No additional Strategy, State, Factory, event-bus, or repository framework is warranted by these findings. These recommendations are scoped to demonstrated behavior, not a request for broad refactoring.

## Verification and limits

All **334 Python files parsed successfully**: 211 source files / 34,274 lines and 123 test files / 34,182 lines. Static scanning also checked same-class calls for excessive positional arguments while accounting for static methods; it found none. Manual review traced representative startup/injection, authentication/session ownership, command authorization and dispatch, messaging, persistence/reloads, notes, spells, combat/update, item/effect ownership, movement/resets, weather/regeneration, and collection-tool paths. Review depth varied; this is not an exhaustive execution of every function or gameplay combination.

The default `python` launcher failed inside ActiveState before running tests. The repository `.venv/Scripts/python.exe` worked. Initial restricted async runs stalled in Windows' internal loopback socket-pair setup; a bounded faulthandler probe confirmed this. The completed runs used the access required by Windows asyncio.

| Verification | Result |
| --- | --- |
| Prescribed `unittest discover tests` | 757 executions; 2,022 failures and 394 errors, including subtests and import failures |
| Each top-level test module in a fresh interpreter, with `PYTHONPATH=src` | 77 of 84 modules passed; 7 failed; 1,013 executions, 4 failures and 20 errors |
| Focused real-model probes with mocked I/O | Reproduced quit without save, denial admission, freeze authorization, wrong gtell targets, lost note cursor, discarded room rates, and identifiers-only authentication |
| Collection inspection | Used collection-query CLI for inventory, room schema, and quit/gtell/freeze/say contracts; no collection edits |

Counts are executions, not unique tests: some modules import test classes from other modules, and subtest failure counts can exceed execution counts.

The seven independently failing modules were:

| Module | Observed failure |
| --- | --- |
| `test_area_pet_shop_resets` | Stubbed `server.messaging` is not a package providing `MessageBus` |
| `test_combat_api_dynamic_checks` | Guard context fixture lacks `room` |
| `test_combat_death_rules` | XP fixture lacks `character_attributes.points` |
| `test_combat_group_rewards` | Eleven errors involving incomplete XP fixtures, including missing `points` |
| `test_object_fountain_commands` | Six errors involving missing `owned_items` or stubbed `InterpUtil.number_argument` |
| `test_player_handler_cast_prompt` | Import failure from stubbed `server.messaging` package contract |
| `test_spell_affect_payload_messages` | Three energy-drain assertions where execution returned false; underlying cause not established here |

Test failures alone were not promoted to production findings. No untouched-revision baseline was run, so this report does not label them introduced or pre-existing. Legacy files under `tests/old-tests` were syntax-checked but were not part of the top-level isolated execution pass. No live game listener, external persistence/account service, production restart, or designer deployment was exercised. Security impact depends in part on deployment access controls. No ROM24 parity audit was performed.

# Repository Python code review

Date: October 25, 2026. Reviewed checkout: `2935c2c11afd45f743a6c914881c581759eea527`, including the working tree. Review guidance: the repository's `python-code-review` skill, including its DRY guidance, and `AGENTS.md`. This is a review of current behavior, not a claim that these defects were introduced by the uncommitted skill edits. No runtime code, tests, or collection documents were changed.

## Findings

Thirteen runtime findings follow: five P1 issues and eight P2 issues. P1 means a high-impact failure warranting prompt attention; P2 means a concrete functional or persistence defect. Authentication severity assumes the game socket is reachable by an untrusted client; its deployment boundary needs confirmation.

### F1 — [P1] Player spell lookup still calls an instance method using its old calling convention

**Follow-up status — addressed October 25, 2026:** corrected both Python callers and the collection guard to use the bound instance method. Updated existing mock contracts and added [four real-character casting regressions](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_cast_learned_contract.py). All 58 focused tests passed in separate suite processes: the four new regressions, 16 combat command tests, 18 spell casting/payload tests, and 20 command authorization tests. Verified the collection snapshot changes only the cast learned-spell predicate. No live content service was updated; the original review evidence below describes the state before this fix.

Sources: [FightUtil.py:77](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/FightUtil.py:77), [SpellApi.py:55](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:55), [Character.py:286](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/Character.py:286). The `cast` command's `guards[3].predicate` in the Commands collection repeats this call.

`get_learned` is now an instance method, but these callers use `actor.get_learned(actor, spell.name, ...)`. For a player who meets a matching spell's class-level requirement, `FightUtil.find_spell` raises `TypeError` before casting can proceed. Fixing lookup alone leaves the same failure in the collection guard and proficiency calculation. The exception propagates through command execution to connection handling, which ends the client loop.

**Verified:** an actual `Character` with a learned `armor` spell raised `Character.get_learned() takes 2 positional arguments but 3 ... were given` in both spell lookup and proficiency calculation. The collection predicate was verified through the query CLI.

**Remedy and coverage:** call the bound method with only the spell name in all three places. Keep the guard declarative. Add an end-to-end cast regression using the real `Character` and representative command/spell documents; the current proficiency test uses a `Mock` that explicitly accepts the obsolete argument list.

### F2 — [P1] Runtime callers bypass guarded bitfield writes and raise after partial mutations

**Follow-up status — addressed October 25, 2026:** revelation now uses `StatusFlags.unset_flag`; body switching and peace use the existing character API flag helpers. Migrated all eight flag-removal domains in `MobileUtil.apply_flag_removes` to guarded writes. Added [four runtime regressions](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_guarded_flag_runtime_paths.py) covering attack progression/reveal routing, switch/return bindings, peace across multiple combatants, and the removal-domain aliases. They verify unrelated flags survive and direct writes remain prohibited. Updated the existing reveal fixture to use real `StatusFlags`. All 52 focused tests passed in separate suite processes: 4 new regressions, 7 combat-state tests, 14 reconnect tests, 9 design-contract tests, 11 wizard-command metadata tests, 3 mobile armor tests, and the 4 F1 casting regressions. No collection data changed for F2; the evidence below describes the original failure.

Sources: [CombatHandler.py:878](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:878), [WizHandler.py:103](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/WizHandler.py:103), [Wiz.py:519](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:519), [StatusFlags.py:65](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/StatusFlags.py:65).

`StatusFlags` rejects direct assignments to initialized bitfields. Invisible attack revelation nevertheless uses `affected_by &= ~bit`; switching bodies assigns `comm` directly; `peace` assigns NPC `act` directly. Each raises `AttributeError` on real runtime models. Revelation strips effects before raising. Switching rebinds the connection and changes the controlled body before raising. An invisible attack executed by the world update can propagate out of `violence_update`; [MudServer.py:33](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/MudServer.py:33) logs the exception and closes the world event loop.

**Verified:** revelation raised `affected_by must be modified through StatusFlags bitfield helpers`. Body switching raised the corresponding `comm` error after `session.character` had already changed.

**Remedy and coverage:** use `unset_flag`, `assign_bitfield`, or the existing API wrappers. Audit `MobileUtil.apply_flag_removes` for the same obsolete writes, although no current caller was identified for that helper. Exercise revelation, switching/returning, and peace with real `StatusFlags`, including state consistency after an operation fails.

### F3 — [P1] Authentication accepts account and character identifiers without proof of identity

**Follow-up status — deferred at the user's request.** Authentication behavior is unchanged.

Sources: [AuthenticationService.py:26](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/session/AuthenticationService.py:26), [ConnectionHandler.py:60](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:60), [MessageCodec.py:64](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/protocol/MessageCodec.py:64).

An AUTH message, including the supported `logon` JSON form, is accepted when the supplied account exists and its character list contains the supplied character ID. No password, signed ticket, or authenticated upstream identity is checked. Character membership establishes authorization only after the caller's identity has been established; knowing the identifiers currently suffices to establish it.

**Verified:** a mocked account/character registry authenticated a payload containing only `accountId` and `characterId`. No service or live account was contacted.

**Remedy and coverage:** validate a short-lived, server-verifiable login ticket from the account service, bound to the account and character. If a trusted gateway is the intended authenticator, enforce that boundary at the game listener and authenticate the gateway's assertion. Deployment firewall/gateway guarantees were not available in this review. Test missing, forged, expired, and mismatched credentials as well as reconnects.

### F4 — [P1] Player command execution does not enforce action wait time

**Follow-up status — addressed October 25, 2026:** the socket input loop now retains typed commands in order and waits for the controlled character's `pulse_wait` to clear before dispatch. Recovery advances once per world pulse, including outside combat, for connected players, link-dead room occupants, and possession bodies/originals, deduplicated by object identity. Combat no longer subtracts a second recovery interval from those entities. Forced/ordered/nested execution deliberately bypasses the socket gate; a player's typed `order` command still uses it. Authored beats remain in content. Disconnect/session replacement abandons a waiting command. The autonomous NPC timer inconsistency was subsequently addressed in F6.

Sources: [ConnectionHandler.py:288](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:288), [InterpHandler.py:68](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/InterpHandler.py:68), [CommandExecutor.py:26](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/CommandExecutor.py:26), [Fight.py:400](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Fight.py:400).

Skills set `status_flags.pulse_wait`, but the socket loop immediately dispatches the next input and the normal command authorization/execution path does not consult this value. The representative `kick` skill guards check access, room, and victim, not wait time. Consequently a client can repeatedly invoke an available combat skill between world pulses, bypassing its authored beats. This remains a problem independently of F1's spell failure.

**Verified:** two commands were dispatched through `InterpHandler.handle_command` with the character's wait value fixed at `24`. The command and skill guard paths were inspected and the kick guards queried.

**Remedy and coverage:** enforce input waiting at the player input scheduling boundary, with explicit policy for forced/ordered commands. Decrement waits on a consistent pulse clock, including outside combat; currently the decrement is tied to `multi_hit`. Keep ability beats in content. Test queued rapid input, a noncombat action's recovery, and nested command behavior.

### F5 — [P1] Normal player commands perform blocking HTTP on an event-loop thread

**Follow-up status — addressed October 25, 2026:** added an ordered background I/O worker shared by both event loops. Character and account saves capture detached payloads under their existing model locks before submission; deny-list saves copy their values before submission. Automatic saves, advancement, combat/theft flags, and wizard persistence enqueue writes without holding up the world loop. Manual saves await the actual result, preserving the content-owned failure message; cancellation of that wait does not cancel an already queued save. Note command dispatch is async: only the blocking note service calls run on the worker, while draft/read-state changes and payload handling remain on the command loop. Queued HTTP writes do not mutate the character/account registries from a worker; the existing synchronous compatibility save methods still register successful saves on their caller. Unexpected worker exceptions are logged. No live content service was contacted or deployed.

**Follow-up verification for F4/F5:** [11 concurrency regressions](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_input_wait_and_persistence.py) cover ordered typed input, disconnect during recovery, noncombat/link-dead/possession recovery, prevention of double combat decrement, snapshot isolation and write ordering, event-loop progress during held HTTP, actual manual-save failures, cancellation-safe queued saves, account/deny-list snapshots, nonblocking autosave/level gain, and slow note reads. All **293 focused test executions** passed across 12 isolated suites. Across the broader isolated-module checks and affected-suite reruns, **72 of 79 modules passed**, with **967 test executions**; the same seven failures documented in the original verification table remained. Syntax compilation and whitespace checks passed. The single I/O worker prioritizes ordering and can accumulate a backlog during service outages; production load/latency and a live restart were not tested. Model locks protect snapshot capture where writers honor them; this does not resolve the broader cross-thread world-ownership concerns in D3.

Sources: [Communications.py:383](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:383), [CharacterService.py:49](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:49), [PlayerHandler.py:509](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:509), [NoteService.py:32](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteService.py:32), [AdvancementHandler.py:19](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/AdvancementHandler.py:19).

The async player command path calls synchronous `save_character` and note operations, which execute `requests` directly. A slow content service therefore blocks the socket loop, delaying all clients' input/output until that request completes or fails. Level-gain persistence can similarly block whichever loop awards XP, including the world loop. The request timeout is not a strict total-operation deadline. Autosave already uses `asyncio.to_thread`, but manual saves, notes, and advancement do not.

**Evidence:** traced collection command lambdas through the async player handlers to the synchronous HTTP calls. No service-latency benchmark was performed.

**Remedy and coverage:** introduce an awaited I/O boundary or persistence queue. Snapshot mutable character state under the appropriate ownership policy before performing I/O; offloading a mutable model wholesale is insufficient to guarantee a consistent save. Verify another client's command and a scheduled pulse can progress while a mocked save/note request is held pending, and preserve save failure messages and ordering.

### F6 — [P2] NPC wait timers are decremented on a different object from the one skills use

Sources: [CombatHandler.py:1515](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:1515), [CombatSkillHandler.py:29](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatSkillHandler.py:29), [Fight.py:684](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Fight.py:684).

For NPCs, `_decrement_combat_timers` only decrements top-level `entity.pulse_wait` and `entity.pulse_daze`, then returns. Skills write the values on `entity.status_flags`, and NPC skill selection reads `actor.status_flags.pulse_wait`. After the first skill sets a wait, subsequent NPC rounds can permanently skip skill selection. Daze can also remain indefinitely.

**Verified:** a real `Mobile` instance carrying status timers `(24, 12)` retained `(24, 12)` after the NPC decrement branch.

**Remedy and coverage:** use one timer owner for players and NPCs. Test successive actual NPC skill rounds, including a wait longer than one round and eventual recovery.

**Follow-up status � addressed October 25, 2026:** autonomous NPC combat recovery now subtracts 12 from `status_flags.pulse_wait` and `status_flags.pulse_daze`, clamping both at zero. Players and controlled bodies retain their world-pulse recovery without a second combat decrement. Regression coverage uses a real spawned Mobile and successive NPC skill selections with a wait lasting more than two rounds; selection resumes when the wait clears.

### F7 — [P2] Spawned NPC alignment disagrees with the alignment read by gameplay

Sources: [MobileUtil.py:284](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/MobileUtil.py:284), [MobileUtil.py:300](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/MobileUtil.py:300), [CharacterApi.py:137](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/CharacterApi.py:137).

Spawning copies content alignment to `mob.alignment` but creates `character_attributes` with alignment `0` and never copies the authored alignment there. `CharacterApi.is_good/is_evil` and spell alignment helpers prefer the attributes object. NPCs consequently behave as neutral for these checks despite their authored alignment, affecting alignment-dependent spells, rewards, and assistance.

**Verified with repository content:** mob vnum `3001` has authored alignment `900`; the normal build/spawn path produced top-level `900`, attribute alignment `0`, and `CharacterApi.is_good(mob) == False`.

**Remedy and coverage:** establish one authoritative entity alignment operation and initialize it during spawn/clone. Preserve the mobile service's wire format. Test positive, negative, and neutral content through spawning, classification, spell checks, and cloning.

**Follow-up status � addressed October 25, 2026:** `AnimateEntity.get_alignment` reads runtime attributes, falling back to the prototype's service field before attributes exist. Spawn initializes runtime alignment through `set_alignment`; cloning preserves current runtime alignment even after it diverges from the original content value. Character classification and spell alignment checks share that accessor. Mobile service fields remain strings. Regression coverage exercises positive, negative, neutral, and classification-boundary values, spawn/clone independence, spell reads, and runtime mutations.

**F6/F7 validation:** 96 test executions passed across 11 focused modules, run separately to avoid fixture module contamination: mobile armor/alignment, combat round skills, combat rounding/XP, assistance, mobile pulses, special binding/access, cast learned contracts, guarded flag paths, active-player updates, and input wait/persistence. Windows asyncio suites required local socket access outside the restricted sandbox; the sandboxed assistance run timed out, then passed with that access. No live content service or server session was exercised. The earlier repository-wide failures listed below were not rerun as part of this focused validation.

### F8 — [P2] Targeted socials fail at both dispatch and target resolution

Sources: [InterpHandler.py:79](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/InterpHandler.py:79), [SocialHandler.py:36](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/SocialHandler.py:36), [Room.py:165](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/Room.py:165).

For `smile Tester`, interpreter fallback looks up the social named `smile tester` instead of `smile`, so it normally emits `Huh?`. Calling the social handler directly still fails: it looks up `room.characters[target_name]`, while that dictionary is keyed by character IDs. NPC targets are also absent from that lookup.

**Verified:** the interpreter queried `name='smile tester'` and did not call the social handler. Supplying a social directly with `Tester` present under its actual ID yielded the missing-target message.

**Remedy and coverage:** split the social verb from its argument before lookup and reuse visible room-entity name resolution. Exclude actor/victim from appropriate bystander payloads. Test untargeted, player-targeted, NPC-targeted, self-targeted, missing, and invisible-target cases through the interpreter.

**Follow-up status � addressed October 25, 2026:** interpreter fallback now looks up only the social verb. Social targeting uses the shared room-entity lookup and `CharacterApi.can_see`, covering players, NPC keywords, self, and whitespace-separated arguments. Bystander lists exclude the actor and direct target. Interpreter-level regressions cover untargeted, player/NPC/self targets, missing targets, and a real player hidden by invisibility level.

### F9 — [P2] `pmote` passes an extra argument to `do_emote`

Source: [Communications.py:269](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:269).

`do_pmote` calls `self.do_emote(character, context)`, but the bound method accepts only `context`. An available `pmote` command therefore raises before producing output and propagates into connection-loop error handling.

**Verified:** the real method raised `Communications.do_emote() takes 2 positional arguments but 3 were given`.

**Remedy and coverage:** correct the delegation argument list. Test the collection-backed command through the communications dispatcher. Whether per-recipient pmote rewriting should be implemented is a separate behavior question; fixing this exception does not require deciding it.

**Follow-up status � addressed October 25, 2026:** `pmote` delegates with the correct context argument. Its emote path now uses the existing room player-target operation rather than a nonexistent helper. The shared payload renderer recognizes the already-authored `%e` token. Collection-backed dispatcher regressions verify rendered text, recipients, and the missing-argument guard; per-recipient pmote rewriting remains outside this fix.

### F10 — [P2] Saving aliases rewrites user-defined keys

Sources: [CharacterService.py:110](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:110), [CharacterService.py:160](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:160), [AliasApi.py:40](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:40).

The recursive serializer camelizes every dictionary key, including alias names. An allowed alias `go_home` is saved as `goHome`; alias normalization on reload lowercases it to `gohome`. The original command stops expanding after a save/reload. Distinct names such as `go_home` and `goHome` can also collide during serialization.

**Verified:** creating `go_home -> recall`, serializing, and restoring an actual `Character` produced payload `{'goHome': 'recall'}` and left `go_home` unexpanded.

**Remedy and coverage:** distinguish schema field names from arbitrary mapping keys. Preserve alias keys verbatim when saving. Add JSON round-trip tests with underscores and collision-prone names; do not solve this by forbidding otherwise valid alias names.

**Follow-up status � addressed October 25, 2026:** character serialization copies the alias mapping without camelizing its user-defined keys. JSON save/reload regression coverage verifies underscore names, repeated underscores, collision-prone `go_home`/`gohome` names, and subsequent argument-preserving expansion. Schema serialization remains unchanged.

### F11 — [P2] Alignment prompts read an attribute that player characters do not expose

Sources: [PromptFormat.py:32](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/PromptFormat.py:32), [Info.py:1045](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:1045).

The prompt command enables `%a`, whose renderer reads `character.alignment`. Player alignment lives on `character.character_attributes.alignment`; `Character` has no `alignment` property. Once enabled, rendering raises, and `MessageBus.send_prompt` catches the error and returns false instead of displaying the prompt. The broken setting survives a prompt-format save.

**Verified:** `PromptFormat(alignment=True).render_prompt(...)` with an actual `Character` raised `AttributeError: 'Character' object has no attribute 'alignment'`.

**Remedy and coverage:** render through the authoritative entity alignment accessor, consistent with F7. Test each supported prompt token against real player models and verify enabled options survive serialization.

**Follow-up status � addressed October 25, 2026:** alignment prompts now call the authoritative entity alignment accessor. Regression coverage renders every supported prompt token against a real Character and saves/reloads each enabled prompt option, including alignment.

**F8�F11 validation:** 115 test executions passed across nine isolated focused modules: social/alias/prompt regressions, communications dynamic commands, input wait/persistence, active-player updates, cast learned contracts, combat dynamic commands, mobile armor/alignment, interpreter argument text, and immortal checks. `git diff --check` passed. Async checks used local socket access required by Windows asyncio. No live server or external persistence service was exercised; earlier repository-wide failures were not rerun.

### F12 — [P2] Failed collection reloads discard the last usable registry

Sources: [SkillService.py:24](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/skill/SkillService.py:24), [SpellService.py:19](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/skill/SpellService.py:19), [RoomService.py:27](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/RoomService.py:27), [FetchAndRegisterMixin.py:10](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/FetchAndRegisterMixin.py:10).

Reload methods reset their registries before fetching replacements. The shared loader catches request/build errors and returns `None`, also used for a successful list load. A temporary service failure therefore leaves an empty registry while the caller logs reload completion. A malformed document partway through a list can leave a partially rebuilt registry. Reloading rooms also needs an explicit policy for preserving live occupants and area bindings.

**Verified:** preloading a real `SkillRegistry`, mocking a connection failure, and invoking `reload_skills` left zero definitions.

**Remedy and coverage:** fetch and validate a candidate snapshot before committing it, return an explicit success/result contract, and retain the old snapshot on failure. Treat room/world reload migration separately from definition replacement. Test request failure, invalid documents, successful replacement, and live-object preservation.

**Follow-up status � addressed October 25, 2026:** collection reload entrypoints now build an isolated registry, validate every document and lookup conflict, and publish its indexes/items only after the entire candidate succeeds. They return `True` for a committed snapshot (including a valid empty collection) and `False` on fetch, HTTP, JSON, document, registration, or policy failure; only successful publication logs completion. The injected registry object remains the same. This shared path covers skills, spells, commands, mobiles, items, resets, shops, specials, helps, socials, characters, accounts, rooms, and areas; local group reloads also stage before publishing without mutating their source dictionaries. Generated summary commands are part of the staged command snapshot. Initial/single-document fetch compatibility remains separate.

**World reload policy:** room and area replacement is definition loading, not live-world migration. Room reloads are rejected if existing rooms have area bindings, occupants, contents, or tracked runtime activity, or if replacements would bind into a loaded area. Area reloads are rejected while rooms exist. Rejected reloads retain original room/area identity, occupants, items, locks, bindings, and population counters. Replacing an initialized world requires a restart. Empty unbound room snapshots may be replaced. Malformed exits reject a room reload instead of silently publishing truncated exit lists. The registries dependency lacks a public snapshot replacement API, so its storage adapter is confined to the shared loader; no cross-registry transaction or live-world migration is introduced.

### F13 — [P2] Link-dead and switched-out players are omitted from periodic saves

Sources: [ConnectionHandler.py:227](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:227), [UpdateHandler.py:97](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/UpdateHandler.py:97), [UpdateHandler.py:115](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/UpdateHandler.py:115), [EntityUpdateHandler.py:37](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/EntityUpdateHandler.py:37).

Disconnect cleanup removes a session while intentionally retaining its live player in the room. Entity updates continue ticking that player, but autosave enumerates only playing sessions. A disconnected character can therefore change through regeneration, effects, combat, or inventory interactions for an arbitrary period without being saved. After a process restart, changes since the last connected save are lost. Possession also makes `session.character` a `Mobile`, which the save selector skips while the original player remains in the world.

**Evidence:** traced cleanup, world entity enumeration, and the autosave selector. No crash/restart against an external persistence service was performed.

**Remedy and coverage:** enumerate authoritative live player characters for persistence, including link-dead players and possession originals, deduplicated by ID. Preserve session-only selection for features that truly require a connection. Test save-bucket eligibility after disconnect and during possession without duplicating saves.

**Follow-up status � addressed October 25, 2026:** autosave now enumerates real player Characters from authoritative room occupants and playing sessions, including possession originals from session metadata/body context. It deduplicates by character ID and prefers the live room instance, retains existing save buckets and queued persistence, excludes NPC bodies and offline account records, and saves after entity ticks. The existing active-session selector remains in use for session-dependent behavior.

**F12/F13 validation:** 146 test executions passed across 12 isolated focused modules: reload/live autosave (15 tests, including parameterized service cases), active-player updates, input wait/persistence, social/alias/prompt, communications, mobile special binding, mobile pulses, cast learned contracts, combat dynamic commands, area occupancy, mobile room access, and area utilities. Regression cases cover request/HTTP/JSON failures, malformed later documents, missing IDs, duplicate lookup keys, builders returning no item, successful replacement and empty snapshots, generated command failure, source-preserving group reloads, live room/area preservation, disconnect and possession save eligibility, deduplication, save timing, and exclusion after leaving the world. `git diff --check` passed. Windows async tests required local socket access. No external content/persistence service or live server was exercised; earlier repository-wide failures were not rerun.

## Nonblocking DRY and object-design recommendations

### D1 — Share guard normalization across commands and abilities

[Command.py:56](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/Command.py:56) and [Ability.py:58](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/skill/Ability.py:58) repeat the same predicate, message-key, channel, fallback, and token-factory normalization. This is shared schema knowledge: a future guard field or compatibility fix must change both implementations.

Extract one small pure normalization function at a shared content-contract boundary. Preserve string shorthand, camelCase keys, omitted fields, and rejection of malformed entries. Parameterized loader-contract tests should cover both consumers. A base-class hierarchy or a new schema framework would add unnecessary cost.

**Follow-up status - addressed October 25, 2026:** Command and Ability now delegate guard normalization to the pure `normalize_guards` function in `src/game/action/GuardNormalization.py`, alongside the shared action contracts. Existing model entrypoints remain available. Predicate shorthand, the `lambda` alias, camelCase/snake_case fields and message keys, optional defaults, malformed-entry skipping, entry order, and independent output mappings retain their existing behavior. Skill's existing second normalization pass is retained to preserve its shorthand output shape. No new inheritance hierarchy or schema framework was added.

**D1 review:** reviewed the extraction, its imports and ownership boundary, Command/Ability/Skill/Spell loader paths, and InterpApi/FightApi consumers using the repository python-code-review skill. No additional actionable correctness findings were identified in this change. The remaining second normalization pass in Skill predates D1 and is deliberately covered as compatibility behavior.

**D1 validation:** eight loader-contract tests passed before and after extraction, parameterized across real Command, Skill, and Spell loaders using mapping and JSON-string documents. Coverage includes omitted fields, shorthand, key conversion, predicate precedence, invalid entries, defaults, and input/output isolation. The final focused run passed 116 test executions across seven isolated modules: guard normalization, combat commands, communications commands, movement commands, cast contracts, reload/live autosave, and command execution. `git diff --check` passed. Async suites used local socket access required by Windows asyncio. Collection documents were unchanged; earlier repository-wide failures were not rerun.

### D2 — Separate wire-field conversion from arbitrary dictionary serialization

[CharacterService.py:145](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:145) and [PlayerService.py:83](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerService.py:83) duplicate recursive serialization and camelization. Their exclusion rules differ legitimately, but the shared conversion mechanism requires coordinated maintenance. F10 demonstrates a concrete consequence of applying the mechanism too broadly.

Use a small shared codec for value conversion with explicit wire fields and caller-owned exclusions. Preserve user mapping keys. Keep the account and character payload schemas separate, including the prompt adapter's special field names. Round-trip tests should cover nested items/effects, enums, aliases, and omission of runtime-only state. Avoid an ORM or blanket `asdict` replacement.

**Follow-up status - addressed October 25, 2026:** CharacterService and PlayerService now delegate recursive conversion and field-name camelization to `server.WireCodec`. The codec treats dataclass fields as schema names and preserves dictionary keys verbatim, including nested user mappings and collision-prone underscore/camelCase names. Raw dictionary records retain their supplied wire keys rather than having their schema inferred. Enum values and supported sequences become JSON values; conversion builds independent containers. Services retain their explicit, separate top-level payload schemas and caller-owned dataclass exclusions. The character race/prompt adapters remain explicit, including the prompt contract's underscore field names. Aliases use the same shared conversion path rather than a special-case key-preservation workaround. No ORM or blanket `asdict` conversion was added.

**D2 validation:** 105 test executions passed across eight isolated focused modules: the shared codec (7), item persistence (9), social/alias/prompt regressions (4), input wait/persistence (11), fullness/hunger (14), reload/live autosave (15), communications commands (38), and runtime ownership (7). Coverage includes real account/character JSON round trips, nested inventory/equipment and effects, ordinary/IntEnum values, tuples/sets, collision-prone mapping keys, alias persistence, prompt special fields, caller-specific recursive exclusions, class-variable omission, top-level runtime-state omission, and output isolation. `git diff --check` passed. Async suites used Windows asyncio local socket access. No live persistence endpoint was exercised; earlier repository-wide failures were not rerun.

**D2 cleanup:** removed the unused `_camelize` wrappers and the delegating `_serialize_value` wrappers. Service payload builders call `serialize_wire_value` explicitly with their own exclusion policies; tests call the codec directly or exercise complete payload round trips. All 45 focused serializer, item, fullness, alias/prompt, and persistence test executions passed after this cleanup. No wrapper references remain under `src` or `tests`; `git diff --check` passed.

### D3 — Make state ownership consistent before adding abstractions

F2, F6, and F7 show the cost of maintaining competing representations of flags, timers, and alignment. Continue the existing `AnimateEntity`/`StatusFlags` direction: expose small invariant-preserving operations, use them from callers, and keep wire-format adaptation at loading/saving boundaries. Do not introduce separate player/NPC algorithms for state that already has a shared runtime contract.

There is also a threading boundary to resolve: [MudServer.py:25](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/MudServer.py:25) starts world updates on another thread, while [SessionHandler.py:44](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/session/SessionHandler.py:44) iterates the same mutable session map that socket handlers modify. Entity/world mutations and worker-thread serialization have similar ownership concerns. Prefer explicit loop ownership or short synchronized snapshots; avoid locks held across awaits. This is a design/race-risk recommendation, not a claim that a concurrent failure was reproduced.

**Reassessment and follow-up status - addressed October 25, 2026:** F2/F6/F7 already resolved the competing runtime flag, timer, and alignment representations. F5 already moved character/account serialization to prepared snapshots before HTTP work. The remaining D3 issue was still present: GameService executed world mutations on its scheduler thread while socket commands changed the same live state.

`MudServer.start` now records the socket event loop as the runtime owner before starting the background scheduler. GameService dispatches each complete update to that loop using `run_coroutine_threadsafe` and waits for its result before scheduling another pulse. Timing/stalling remains on the scheduler thread. Commands, session changes, world mutations, and live persistence snapshot capture therefore execute on the same thread; async operations can still interleave at awaits, so this is not a transaction across arbitrary awaited operations. Runtime shutdown stops the scheduler and cancels an outstanding dispatched update. No thread lock is held across gameplay awaits.

The note content cache remains shared with its I/O worker, so NoteRegistry readers now use its existing writer lock for short lookups/snapshots and filter outside that lock. A deterministic regression publishes a new note while an existing snapshot is filtered, covering the previous mutable-dictionary iteration hazard. Repository architecture guidance now documents the owner-loop boundary.

**D3 validation:** 171 test executions passed across 11 isolated focused modules: runtime ownership/note snapshots (7), input wait/persistence (11), reload/live autosave (15), active-player updates (33), social/alias/prompt (4), communications (38), combat dynamic commands (16), notes (8), command executor (14), reconnect (14), and wizard commands/possession (11). Real background event-loop tests verify update thread/loop identity, progress by socket work while a pulse awaits, sequential pulses, error propagation, pending-update cancellation, and server shutdown. `git diff --check` passed. Async tests required local socket access. No live content service or production server was exercised, and this is not a general guarantee for arbitrary external threads mutating models; future runtime integrations must follow the documented owner-loop contract.

### D4 — Preserve the established content-driven architecture

The existing action definitions, guards, payloads, ability resolver, item ownership coordinator, and exposure collaborators are useful abstractions. Reuse them. In particular, fix F1's guard through collection tooling and fix F8 using existing visible lookup behavior rather than introducing another matching algorithm. Do not centralize differently owned content merely because its strings or lambdas look similar.

No additional Strategy, State, Factory, event-bus, or repository framework is justified by these findings. The useful changes are small shared functions, consistent domain operations, an explicit reload commit contract, and an asynchronous persistence boundary. Keep designer-owned rules and text in content as those boundaries evolve.

## Verification

### Scope and approach

All 323 Python files under `src` and `tests` parsed successfully with the repository virtual environment (Python 3.14 on Windows). The inventory contains 208 runtime files / 34,266 lines and 115 test files / 32,758 lines. Static checks included syntax, mutable function defaults, direct bitfield writes, repeated normalization/serialization logic, and same-class calls with excessive positional arguments. These checks support review coverage, not a proof of correctness.

Manual tracing covered startup/injection, service loading and registries, authentication/reconnect/session ownership, message routing, commands/guards/action plans, spells and learning, combat and aftermath, area resets/movement, item/effect ownership and updates, character/account persistence, notes, weather/regeneration, and collection tooling. Representative callers and tests were inspected around reported paths. Depth varied by subsystem; every function and gameplay combination was not independently exercised.

Collection inspection used `python -m src.devtools` as prescribed: collection inventory and field shapes; save/note command lambdas; cast and kick guards; and mobile alignment. The mobile-spawn probe then used the repository collection loader to instantiate selected data without printing entire collections. No collection was edited. No live socket server, account service, or content service was exercised. This was not a ROM24 parity audit.

### Test results

The prescribed `.venv/Scripts/python.exe -m unittest discover tests` completed **713 test executions**, reporting **2,023 failures and 357 errors**. The failure count includes subtest failures and can exceed the number of tests. This is not evidence of that many independent runtime defects.

Several test modules replace production entries in `sys.modules` at import time without restoring them. Examples: [test_combat_dynamic_commands.py:32](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_combat_dynamic_commands.py:32) and [test_note_commands.py:61](C:/Users/scott/PycharmProjects/springs-of-mud-server/tests/test_note_commands.py:61). Discovery can leave unrelated tests using fake API classes or older fixture contracts. This makes the normal aggregate suite unsuitable as a reliable regression gate until import isolation is repaired.

Each of the 76 top-level test modules was subsequently run in a fresh interpreter. With `PYTHONPATH` set to the absolute `src` directory, **69 modules passed and 7 failed**, across **948 test executions** including loader-failure placeholders and overlapping imported test classes. These runs reported **4 failures and 20 errors**. They are not a deduplicated count of unique tests.

| Independently failing module | Observed failure |
| --- | --- |
| `tests.test_area_pet_shop_resets` | One failure: fixture replaces `server.messaging` without providing the imported `server.messaging.MessageBus` module. |
| `tests.test_combat_api_dynamic_checks` | One error: manually constructed guard view lacks `context.room`. |
| `tests.test_combat_death_rules` | One error: XP fixture lacks `character_attributes.points`. |
| `tests.test_combat_group_rewards` | Eleven errors, including incomplete XP fixtures lacking `points`. |
| `tests.test_object_fountain_commands` | Six errors: character stand-ins lack `owned_items()`. |
| `tests.test_player_handler_cast_prompt` | One import error from the `server.messaging` fixture contract. |
| `tests.test_spell_affect_payload_messages` | Three failing energy-drain cases where spell execution returned false. |

The energy-drain cases require separate diagnosis; they were not attributed to a production XP defect merely from these assertions. No untouched-revision baseline was run in this review, so none of the failures is classified here as pre-existing. The 38 files in `tests/old-tests` were included in syntax inventory and legacy-context consideration but were not executed by the top-level module pass or the normal discovery result above.

The first sandboxed aggregate attempt stalled creating Windows asyncio's internal loopback socket pair. A bounded diagnostic confirmed the location; executable async checks and subsequent test runs succeeded outside that restriction. An earlier isolated pass without `PYTHONPATH=src` passed 64 modules; its extra import-path failures were excluded from the final seven-module result.

To reproduce isolated module checks in PowerShell, set `PYTHONPATH` for a fresh process to the repository's `src` directory and run each module separately:

```powershell
$env:PYTHONPATH = (Resolve-Path src).Path
Get-ChildItem tests/test_*.py | ForEach-Object {
    & ./.venv/Scripts/python.exe -m unittest "tests.$($_.BaseName)"
}
```

### Targeted review probes

Probes used actual models and selected content, with mocked registries, HTTP failures, or message delivery as needed. They did not mutate persisted game state.

| Probe | Observed result |
| --- | --- |
| Learned player spell lookup and proficiency | Both raised the bound-method `TypeError` described in F1. |
| Invisible attacker revelation | Guarded `affected_by` write raised. |
| Body switching | Guarded `comm` write raised after the session changed body. |
| Authentication with identifiers only | Returned success. |
| Dispatch twice with wait `24` | Both commands reached dispatch. |
| NPC combat timer decrement | Status timers stayed `(24, 12)`. |
| Spawn content mob `3001` | Authored alignment `900`, attribute alignment `0`, classified as not good. |
| Targeted social via interpreter/direct handler | Whole-input lookup / target-not-found result. |
| `pmote` delegation | Raised an argument-count `TypeError`. |
| Alias JSON round trip | `go_home` saved as `goHome`; original alias stopped expanding. |
| Actual player alignment prompt | Raised missing `Character.alignment`. |
| Skill reload with a mocked request failure | Previously populated registry became empty. |
| Prompt option save/load control | `max_health` and `room_name` remained enabled; no finding raised for those fields. |

## Suggested implementation order

1. Restore real-model contracts: F1/F2, then cover complete cast, reveal, and switch paths with real models.
2. Establish the authentication trust boundary (F3) and input/persistence scheduling boundaries (F4/F5).
3. Correct NPC timer/alignment ownership (F6/F7), then the localized social, pmote, alias, and prompt failures (F8–F11).
4. Make reload/persistence enumeration resilient (F12/F13), and repair test import isolation and stale fixtures so the prescribed aggregate check becomes useful.
5. Consolidate the demonstrated duplicated knowledge in D1/D2 only after behavior is protected by those regression tests.

## Wrapper cleanup follow-up

The subsequent repository-wide wrapper pass removed 32 unnecessary forwarding methods, normalized the inventory item-list type, and updated callers/tests to use their implementation owners directly. See [Python wrapper review](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/python-wrapper-review-2026-10-25.md) for the removal inventory, retained contracts, verification, and the seven previously recorded failing test modules.

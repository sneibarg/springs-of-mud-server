# Server exception-handling review

Reviewed commit `612b0d8` on `agentic-game-polishing`. The trace begins at `src/main.py` and follows startup, client input, scheduled updates, persistence, and shutdown. Command, guard, spell, and mobile-special documents can supply Python callables at runtime. The graph follows their dispatch boundaries and representative handlers. It does not enumerate every callable or content-dependent branch.

## Findings

### 1. [P1] Mobile special output can stop the whole server

**Reproduced at the mobile-special boundary.** `MobileHandler._execute_lambda_sequence` catches errors raised while evaluating or calling a special, then flushes its payload outside that handler. A special can successfully queue `{"to_room": "hello", "targets": None}`. Delivery raises `TypeError` on `len(targets)` and escapes the mobile pulse. The generic special path also flushes outside its evaluation handler. The current scheduler correctly treats the escaped error as fatal and disconnects all clients. A malformed output payload therefore has the same reach as a failed world-state invariant.

Validate payload shape before enqueuing or dispatching it, with the special name and mobile ID in diagnostics. Treat invalid presentation data as a special failure. Preserve fatal propagation for exceptions that leave world mutations in an unknown state. [MobileHandler.py](../../src/mobile/MobileHandler.py#L258) · [GameService.py](../../src/game/GameService.py#L78) · [MudServer.py](../../src/server/MudServer.py#L44)

### 2. [P1] One stalled client can hold up world pulses and server shutdown

**Traced through the transport, with the shutdown wait reproduced using a stalled close.** The scheduler waits for the complete owner-loop pulse. Pulse handlers send messages inline, and `TelnetConnection` awaits `writer.drain()` with no deadline. Once a non-reading client fills the write buffer, the pulse can stall without producing an exception for the scheduler to report. A saved shutdown can then wait on that active pulse or stall while sending its announcement. Once teardown commits, clients close serially and each `writer.wait_closed()` also has no deadline. The probe held `close_all()` open and confirmed that teardown had committed but never reached the listener's `wait_closed()` before the probe timed out.

Bound sends and graceful transport closure at the connection boundary. Abort a transport that exceeds its deadline and continue closing other clients. Verify with a non-reading client or a transport double that holds both drain and close open. [GameService.py](../../src/game/GameService.py#L56) · [GameService.py](../../src/game/GameService.py#L87) · [TelnetConnection.py](../../src/server/connection/TelnetConnection.py#L31) · [TelnetConnection.py](../../src/server/connection/TelnetConnection.py#L76) · [ConnectionManager.py](../../src/server/connection/ConnectionManager.py#L56) · [RuntimeControl.py](../../src/server/RuntimeControl.py#L53)

### 3. [P2] A room-entry exception leaves membership and location inconsistent

**Reproduced through the north command.** Movement spends movement points, removes the actor from the source room, and adds the actor to the destination. The destination add calls its entry hook after inserting the actor and updating occupancy. Movement updates `room_id` and `area_id` only after that hook returns. An entry hook failure therefore leaves the player in the destination's occupant map with the original room ID. The probe injected an entry-hook error and observed exactly that state. The live hook processes plague effects. The command loop then disconnects the client, and reconnect can find the live actor by scanning room membership while prompts and later commands resolve the stale room ID.

Give the room transfer one owner. Commit membership, location IDs, light, and occupancy together before dispatching entry effects, with a defined failure policy for those effects. Exercise the transfer with a failing entry hook and verify both room maps and character IDs. [Movement.py](../../src/interp/commands/Movement.py#L96) · [Room.py](../../src/area/Room.py#L149) · [EffectUpdateHandler.py](../../src/item/EffectUpdateHandler.py#L141) · [ConnectionHandler.py](../../src/server/handlers/ConnectionHandler.py#L155)

### 4. [P2] A failed snoop notification interrupts disconnect cleanup

**Reproduced.** `_detach_session` marks cleanup complete and removes connection and session bindings before awaiting a direct send to the snooper. A broken pipe skips the remaining account and character cleanup. A second call returns immediately because the cleanup flag is already set. The probe confirmed that the session was gone while the account still retained the character in `current_characters`. The same helper runs during a takeover, so a failed send can also interrupt the replacement login after removing the old session.

Finish ownership, account, and switched-body cleanup before awaiting notices. Deliver the notices through a best-effort path so notification failure cannot interrupt detachment or takeover. [ConnectionHandler.py](../../src/server/handlers/ConnectionHandler.py#L226) · [ConnectionHandler.py](../../src/server/handlers/ConnectionHandler.py#L257)

### 5. [P2] A failed note fetch can mark unseen notes as read

**Reproduced.** `get_notes_by_type` turns a timeout into cached results. `note catchup` treats the fallback as authoritative and, with an empty cache, uses the current time as the read watermark. The probe returned the success payload and confirmed that an unseen note with an earlier timestamp would subsequently count as read. Autosave can persist that watermark. The cache also accumulates successful fetch results without pruning records omitted by the backend, so fallback reads can include stale entries.

Carry fetch status with the result. Allow a stale-cache read where appropriate and require an authoritative result for catchup or selecting a note to mutate. Preserve the cursor on service failure and return a content-defined error message. [NoteService.py](../../src/notes/NoteService.py#L28) · [NoteHandler.py](../../src/notes/NoteHandler.py#L163) · [Character.py](../../src/player/Character.py#L156) · [CharacterService.py](../../src/player/CharacterService.py#L122)

### 6. [P2] A command script error disconnects the player without a command-level error

**Traced.** A syntax error, missing helper, or exception in an awaited command lambda is logged and re-raised by `CommandExecutor`. The session loop clears command bookkeeping, then breaks at its outer exception handler. A malformed authored step can drop an otherwise healthy connection. Forced and ordered commands share the executor, so the connection that issued the outer command can be the one that drops. An earlier step may already have changed state.

Validate authored expressions before publishing definitions where possible. Report recoverable command-content errors to the issuing player and keep the session usable. Treat failures after an unsafe partial mutation according to the owning operation's recovery policy. [CommandExecutor.py](../../src/interp/CommandExecutor.py#L48) · [PlayerHandler.py](../../src/player/PlayerHandler.py#L650) · [ConnectionHandler.py](../../src/server/handlers/ConnectionHandler.py#L368)

### 7. [P2] Persistent moderation actions acknowledge a failed write as success

**Traced.** Permanent site-ban updates mutate the live rules and queue persistence. The command returns the success payload before the HTTP result arrives. On a timeout or HTTP failure, `_persist_deny_list` logs the failure and returns `False`. The command ignores that future, and the worker's exception callback sees a successful future with a false result. A permanent ban can appear successful and disappear after restart. A failed removal can reappear after restart.

Handle the persistence result for permanent changes on the socket loop. Tell the administrator when the live change has failed to persist and preserve an explicit retry or reconciliation path. Apply the same contract to legacy site denies. [Wiz.py](../../src/interp/commands/Wiz.py#L964) · [Wiz.py](../../src/interp/commands/Wiz.py#L1015) · [GameService.py](../../src/game/GameService.py#L113) · [BackgroundIO.py](../../src/server/BackgroundIO.py#L18)

### 8. [P2] A failed spell script still enters the successful cast path

**Reproduced through `Fight.do_cast`.** `execute_lambdas` catches a script exception, marks the spell context failed, and queues a fizzle. `cast` ignores that outcome and calls `Ability.check_improve` with success. The command also invokes the offensive retaliation hook. The probe observed the fizzle, a success argument to learning, and invocation of the retaliation hook. Prior script effects and spent mana remain in place.

Propagate an explicit script failure outcome through the cast path. Separate it from an ordinary failed proficiency roll so learning, mana, and retaliation follow the intended rule for each. Define how multi-step spells handle effects already applied before failure. [SpellApi.py](../../src/api/SpellApi.py#L65) · [SpellContext.py](../../src/skill/SpellContext.py#L72) · [Fight.py](../../src/interp/commands/Fight.py#L149)

### 9. [P2] A snapshot-building exception can turn one player's autosave into a server exit

**Traced.** The periodic save iterates due players and calls `queue_save_character`. Snapshot construction and submission run synchronously on the world owner loop. A serializer error escapes before the persistence worker can turn failure into a result. That skips later due players and triggers fatal scheduler shutdown. HTTP write failures take a different path, returning `False` inside the worker with no retry tracked by the autosave caller.

Handle snapshot and persistence failures per character at the autosave boundary. Record the failed character, continue saving other due players, and schedule a bounded retry with a fresh snapshot. Preserve explicit failure reporting for manual saves and saved shutdown. [UpdateHandler.py](../../src/game/UpdateHandler.py#L96) · [CharacterService.py](../../src/player/CharacterService.py#L40) · [CharacterService.py](../../src/player/CharacterService.py#L61)

### 10. [P3] A failed quit restores occupancy but loses furniture state

**Reproduced.** The quit path temporarily removes the player before saving. `remove_player_from_room` clears `character.on`. A failed save restores room membership, the playing registry, and session status but leaves `on` cleared. Re-adding the actor also invokes the room-entry hook, so recovery can run entry effects for a move that never occurred.

Restore the previous furniture reference when it still exists in the room. Use a rollback operation that restores occupancy and light without emitting a fresh entry event. [PlayerHandler.py](../../src/player/PlayerHandler.py#L105) · [Room.py](../../src/area/Room.py#L149)

### 11. [P3] Valid JSON with the wrong login shape closes the socket without an authentication reply

**Reproduced at the decoder and authentication boundary.** `logon []` decodes into an AUTH message with a list payload. Authentication calls `.get` on it and raises `AttributeError` before sending an error. The outer connection handler logs the exception and closes the socket. A structured GAME message can also supply non-mapping `data`, which reaches the same assumption in `Message.get`.

Validate the envelope and message-specific fields before dispatch. Return a protocol error for malformed input and reject malformed authentication before changing session state. [MessageCodec.py](../../src/server/protocol/MessageCodec.py#L45) · [Message.py](../../src/server/protocol/Message.py#L31) · [AuthenticationService.py](../../src/server/session/AuthenticationService.py#L26) · [ConnectionHandler.py](../../src/server/handlers/ConnectionHandler.py#L141)

## Call graph from `main.py`

```text
main.py
├─ module initialization → LoggerFactory → read and parse server.yml
└─ asyncio.run(main)
   ├─ MudServer(...) → _configure_server
   │  ├─ _start_services → Bootstrapper.bootstrap
   │  │  ├─ create_injector → GameService → fetch GameData → build enums
   │  │  └─ lazy_load → collection services → fetch, build, register
   │  │              → wire handlers → AreaHandler.initialize_world → area resets
   │  └─ _load_player_one → PlayerRegistry
   └─ await MudServer.start
      ├─ asyncio.start_server(handle_client) on the socket loop
      │  └─ ConnectionHandler.handle_new_connection
      │     ├─ TelnetConnection → TelnetProtocol → MessageCodec
      │     ├─ AuthenticationService → registries → attach → room entry
      │     ├─ _game_loop → InterpHandler
      │     │  ├─ social fallback → CommandAccess.check_actor → SocialHandler
      │     │  └─ CommandExecutor → CommandAccess → authored command steps
      │     │     ├─ PlayerHandler → command family → runtime APIs
      │     │     │  ├─ Movement → Room → EffectUpdateHandler.room_entered
      │     │     │  ├─ Fight / Object → SpellApi → effects and combat
      │     │     │  └─ NoteHandler → BackgroundIO → NoteService → HTTP
      │     │     ├─ quit / save → CharacterService → BackgroundIO → HTTP
      │     │     └─ shutdown / reboot → RuntimeControl → saves → client close
      │     └─ _cleanup_session → _detach_session → connection close
      ├─ GameLoop thread → GameService.start → _run_updates
      │  └─ submit UpdateHandler.handle_updates to the socket loop
      │     ├─ AreaHandler → resets and spawned entities
      │     ├─ MobileHandler → specials, movement, and payload delivery
      │     ├─ FightHandler → combat, aggression, death, and rewards
      │     ├─ WeatherHandler / EntityUpdateHandler / ItemUpdateHandler
      │     └─ autosave / advancement → CharacterService → BackgroundIO → HTTP
      └─ wait for RuntimeControl or scheduler failure
         └─ close listener admission → stop scheduler → close clients
            → wait for listener closure → return or propagate failure
```

Session and pulse output both converge on `MessageBus` and the socket transports. Bootstrap failures propagate before listener creation, saved shutdown can roll back before it commits, and a fatal pulse exception reaches `main.py` with its original cause. The findings above concern failure paths inside or alongside those boundaries. [main.py](../../src/main.py#L17) · [Bootstrapper.py](../../src/server/Bootstrapper.py#L215) · [UpdateHandler.py](../../src/game/UpdateHandler.py#L54) · [RuntimeControl.py](../../src/server/RuntimeControl.py#L35)

## Verification

On Python 3.14, 168 tests passed across 12 focused modules run in separate processes. The modules cover bootstrap, runtime ownership, reconnect, saved shutdown, notes, command execution, movement, casting, persistence, mobile pulses, and messaging. Failure-injection probes used local fixtures and mocked backend calls. The stalled-client finding uses source tracing for TCP backpressure and a controlled pending close for the shutdown consequence. No live content service or deployment was exercised.

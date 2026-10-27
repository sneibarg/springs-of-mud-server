# Immortal command ROM24 parity review

Reviewed October 27, 2026, against the current working tree, including the fixes already made in this conversation. This is a behavioral review, not an implementation change. The reference is the local `C:/Users/scott/PycharmProjects/PyRom/Rom24/src` checkout.

## Remediation update — first priority group

F01–F05 have subsequently been addressed in the working tree. The findings below retain the original audit observations; their line references describe the pre-remediation version.

- F01: punishment commands execute their collection guards, freeze's inverted predicate is corrected, and freeze/unfreeze queue a character save.
- F02: RuntimeControl drains active commands and world updates, snapshots and awaits saves for connected original characters, then closes the listener/connections and stops the scheduler. MudServer returns from its main wait. Failed saves resume gameplay/admission without disconnecting clients. Reboot follows ROM's process-exit behavior; any process restart belongs to the existing external launcher/supervisor.
- F03: wizlock rejects fresh mortal logins and preserves ROM's exception for reconnection to a character already present in the world. Newlock/account creation remains U01; the immortality threshold remains U05.
- F04: purge uses shared extraction cleanup for combat, followers, pets, replies, and switched bodies. Player saves complete before extraction/disconnection, with rollback on save failure/cancellation. CharacterRegistry also owns the offline service cache, so retired players retain cached inventory and the saved room hint for later authentication, while room and playing membership are removed. NPCs are unregistered and their possessions detached. This follows the Python cache/persistence architecture rather than freeing the cached player definition.
- F05: note removal preserves other recipients; permanent delete requires creator trust. Failed recipient updates leave the live record unchanged.

Behavioral tests cover the real collection guards, listener/scheduler termination, save ordering and failures, shutdown/purge cancellation, reconnection, extraction relationships, and recipient preservation. Later findings F06–F22 and unresolved design decisions remain outside this remediation group.

Remediation validation: **163 focused tests passed** across three isolated test processes (70 runtime/admission/persistence, 9 note tests, 84 existing runtime/immortal/factory regressions). Compilation and diff whitespace checks also passed. Async suites ran outside the sandbox because its Windows socketpair restriction prevented event-loop startup.

## Remediation update — second priority group

F06–F07 have subsequently been addressed in the working tree:

- Controller trust now resolves through both player and mobile bodies. Command access, internal guards, visibility checks, cloning thresholds, and other trust consumers see the same authority. Malformed controller cycles fail closed. Standard replies and victim prompts reach connected mobile bodies while unconnected NPC output remains suppressed.
- Shared world targeting uses live room membership, retirement state, and consistent room identity instead of treating the offline character-service cache as the world. It applies observer visibility, local-first searches, keyword/ordinal matching, `self`, and player/mobile filters. All immortal guard, execution, setter, and location adapters pass their observer to the same lookup primitives.
- Object targeting checks room items, carried items, worn items, and then the live world, including nested contents. Offline inventories and invisible items are excluded. Immortal location adapters resolve visible character/floor-object targets while preserving the existing numeric and room-name selectors.
- Bulk force groups now enumerate live PCs only. Their existing trust/hero filters remain, and they intentionally do not filter by visibility, matching C's bulk-force branch rather than its individual-target lookup.
- Loaded mobiles now receive their actual room and area IDs before registration so live-target validation does not mistake a freshly loaded mobile for a stale prototype.

Sixteen new behavioral tests cover these changes using actual model, collection-guard, session-binding, and payload paths. Final focused validation: **247 tests passed** in isolated test processes, including the earlier runtime/persistence paths, object lookup, flag paths, aliases, and elemental visibility. Two older fixtures were completed with the combat-handler/context fields already required by their production paths; no combat behavior was changed for those fixtures. Compilation and diff checks passed. This was focused testing rather than a full-suite/live-service certification.

World fallback iteration follows Python's live room/container order; the implementation does not introduce a C-style global allocation-order list. Local priority and ordinal counting within the selected traversal are covered by tests. The existing shared visibility APIs are reused; their entire stealth/detection implementation was not re-audited here. Findings F08–F22 and the unresolved product decisions remain outside this group.

## Scope and evidence

All **62 enabled commands whose collection role is `immortal`** were inventoried through collection-query. Their lambdas, guards, access metadata, dispatch, and relevant helpers were traced. `:` is an `immtalk` shortcut; `pref` and `prefi` resolve to `prefix`. `teleport` shares transfer behavior. `penalty` actually routes to `NoteHandler`, and `imotd` routes to help: dormant methods in `Wiz.py` were not mistaken for their execution paths.

Validation:

- 59 focused tests passed: immortal metadata, recovery, movement, force/clone, runtime factories, mobile armor isolation, and item persistence.
- Isolated execution of source methods reproduced skipped punishment guards, lost switched-body trust, inert command prefixes, rejection of quoted multiword skills, ignored remote room-stat targets, and failed typed vnum searches.
- Other findings are supported by static branch and caller tracing, as identified below. They are not claims of live multiplayer or service integration testing.
- An additional run including site-ban tests stalled and was stopped; it is not counted as passing. Earlier runs in this environment identified Windows asyncio/socketpair startup stalls.
- No gameplay source, collection, or test files were changed during this review. This report is the only new artifact.

## Findings

### F01 — [P1] Punishment commands bypass their collection guards

`freeze`, `nochannels`, `noemote`, `noshout`, and `notell` call `_toggle_penalty_flag` without evaluating guards. The command executor checks access metadata but does not automatically evaluate those content guards. An actor able to execute the command can therefore punish an equal/higher-trust target; empty or missing targets raise an exception, and NPC exclusions are skipped. Isolated execution changed a senior target's communication flags with **zero guard-evaluator calls**.

There is also a latent collection error: freeze's `noArgument` predicate is `lambda v: InterpUtil.argument_text(v)`, so simply wiring its guards would reject valid nonempty arguments. Freeze also lacks the immediate save performed by C.

Evidence: [Python helper](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:415), [executor](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/CommandExecutor.py:25), [freeze predicate](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:7914); [C nochannels](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:295), [C freeze](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2843).

### F02 — [P1] Reboot/shutdown disconnect clients without shutting down or saving first

Both commands build a broadcast/close-connections payload. `shutdown_kind` has no consumer. The socket listener continues serving and the scheduler continues running; there is no command-driven save/flush of connected original characters before closing them. Disconnect cleanup keeps live entities for linkdead recovery rather than performing ROM's shutdown save. Consequently clients can reconnect to the same running process after a purported shutdown.

Evidence: [payload](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:1246), [consumer](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:906), [listener lifecycle](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/MudServer.py:25), [disconnect cleanup](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:251); [C reboot/shutdown](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2005).

### F03 — [P1] Wizlock is not enforced at login

`wizlock` flips `WizHandler.wizlocked`, but no login/authentication path reads it. Ordinary mortals can still authenticate and enter while the command reports that the game is locked. ROM rejects non-immortal logins while wizlocked. `newlocked` is also an orphaned flag, but the appropriate integration with externally managed account/character creation needs a contract decision; see U01.

Evidence: [flags/toggles](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/WizHandler.py:51), [login checks](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:409); [C login checks](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1606).

### F04 — [P1] Purge does not perform character extraction cleanup

NPC purge removes the room entry and registry item but does not stop combat, detach followers/pets, or return a controller switched into that body. A purged fighting mobile leaves opponents pointing at it; a purged switched body can leave the session attached to a removed entity. Player purge removes room membership and closes the connection but does not save first or unregister the player from the character registry. C saves players above level 1 and runs `extract_char(..., TRUE)`, including combat, follower, pet, switched-body, and reply cleanup.

Evidence: [Python purge](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:494), [unregister helper](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:1302); [C purge](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2545), [C extraction](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1925).

### F05 — [P1] Penalty-note removal can delete other recipients' records

The active `penalty` route is `NoteHandler`. Its `remove` and `delete` actions share a permanent delete path, and any immortal passes `_can_delete`. For a penalty addressed to Alice and Bob by someone else, Alice's `remove` deletes the whole stored note rather than removing Alice from the recipients. Immortals below trust 59 can also use `delete`. C distinguishes recipient removal from global deletion and restricts `delete` to `MAX_LEVEL - 1`.

Evidence: [Python deletion](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:122), [authorization](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:261); [C remove semantics](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:386), [C delete threshold](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:716).

### F06 — [P2] Switched bodies lose controller trust inside command logic and lose replies

CommandAccess follows `controller_original` on any body, but `CharacterApi.get_trust` follows it only when the body is exactly a player `Character`. Switched bodies are `Mobile` objects. Thus command access can succeed under the controller's trust while internal guards and helpers use the mobile's level, capped below hero. An isolated trust-60 controller in a level-10 body was reported as trust 10. This affects force, visibility levels, cloning, privacy checks, wiznet eligibility, and related operations.

Separately, standard payload delivery suppresses `to_char` for every NPC, including a switched body with an active connection. Switch acknowledgment, command denials emitted through that path, and diagnostic output can disappear. C uses the original descriptor for trust and sends output to the controlled body.

Evidence: [trust](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/CharacterApi.py:50), [principal access](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/CommandAccess.py:57), [output suppression](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:866), [switch binding](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/WizHandler.py:81); [C trust](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:706), [C switch](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2178).

### F07 — [P2] World targeting ignores visibility, local priority, ordinal syntax, and live presence

`WizUtil.find_world_entity` returns the first name match in the global registry, without an observer, room-membership check, visibility check, local-first search, or `2.guard` selection. CharacterService loads persisted characters into that registry, so registry presence is not proof that a character exists in the live world. Individual transfer/restore/punishment/switch/snoop/set commands can therefore find hidden or offline targets or select a different duplicate than ROM. `find_world_item` similarly has no observer/visibility or ordinal/local-priority policy.

The newly corrected force groups exclude NPCs and filter trust/hero level, but still iterate that same all-characters registry without restricting it to live world occupants; they can include offline persisted characters. This is a remaining targeting issue, not a reversal of the corrected group rules.

Evidence: [character lookup](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/WizUtil.py:82), [item lookup](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/WizUtil.py:103), [registry population](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:33), [force targets](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/WizApi.py:722); [C room/world lookup](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2003).

### F08 — [P2] Log settings are not connected to command execution

`log all` toggles a boolean and `log <player>` toggles `PLR_LOG`, but neither is read by the command executor/interpreter. Command `log` metadata is also not used for ROM-style command audit logging or secure wiznet events. The existing generic debug line is unconditional and does not implement `LOG_NEVER`, `LOG_ALWAYS`, or per-player/global selection. `do_log` also skips its collection guards, causing invalid-target exceptions and permitting NPC flag changes.

Evidence: [log command](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:754), [interpreter](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/InterpHandler.py:71), [executor](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/CommandExecutor.py:25); [C logging](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:439), [C log command](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2898).

### F09 — [P2] Prefix is stored but never applied; its abbreviation guard is unreachable

After `prefix say`, typing `hello` still interprets `hello` rather than `say hello`. Alias substitution never reads the stored prefix, as reproduced in isolation. In addition, the collection shortcuts `pref, prefi` resolve directly to `prefix`, so the dedicated `do_prefi` refusal cannot run for those inputs. C applies the prefix before alias handling and intercepts `prefi` to prevent accidental prefix changes.

Evidence: [prefix setter](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:736), [substitution](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:120), [shortcuts](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:9535); [C substitution](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/alias.c:48), [C prefi/prefix](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4343).

### F10 — [P2] Mobile cloning rerolls resources and drops current effects/state

`MobileFactory.copy_instance` first creates a fresh spawn, rolling hit points and mana and setting its starting position, then copies selected descriptive/flag fields and possessions. It does not restore the parent's current/max resources, current position, full runtime attributes, or active effects. Cloning a wounded poisoned mobile therefore creates a freshly rolled body with copied poison flags but no corresponding timed effect. C `clone_mobile` copies current/max resources, position, stats, and affects. The earlier recursive possession-eligibility fix remains present; this is a separate gap.

Evidence: [Python mobile copy](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/mobile/MobileFactory.py:185), [spawn initialization](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/mobile/MobileFactory.py:103); [C clone state](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1744).

### F11 — [P2] Set/string parsing loses quoted names; set field abbreviations run backward

`set skill bob 'cure light' 100` is split with Python whitespace splitting, making the value `light' 100`; it returns `value_must_be_numeric`. This was reproduced against the actual method. C's `one_argument` preserves quoted multiword ability names. Similar whitespace splitting exists in string and other set subcommands. In addition, checks such as `field.startswith('level')` reject C-supported `lev` while accepting unintended extensions such as `leveljunk`; room/object/mobile field branches share this reversal.

Evidence: [skill parser](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/WizSetApi.py:133), [mobile fields](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/WizSetApi.py:178), [string parser](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:822); [C sset](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3248), [C mset](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3324), [C string](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3700).

### F12 — [P2] Setting stats while affected changes the effective value instead of the permanent value

Set writes directly to attributes also modified by EffectHandler. For a permanent strength of 15 with a +5 affect, `set char bob str 20` stores effective strength 20; expiration subtracts 5 and leaves 15. C sets permanent strength 20, retaining the modifier while active and leaving 20 after expiration. The same distinction matters for other primary stats and sex modifiers. A fix needs to preserve the engine's effect accounting rather than simply assigning a new effective value.

Evidence: [set stat](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/WizSetApi.py:391), [effect arithmetic](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/EffectHandler.py:56); [C permanent stats](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3365), [C true sex](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3439).

### F13 — [P2] Core diagnostic commands omit functional search paths and data

- **stat:** `stat room 9999` reports the current room, ignoring the requested location (reproduced). Bare numeric room lookup is absent, and generic lookup prefers characters over objects, unlike C. Room/object/mobile output omits most flags, attributes, affects, exits, ownership, and other diagnostic state.
- **vnum:** `vnum mob guard` searches for the whole string `mob guard` and finds nothing (reproduced). The `obj`, `mob`/`char`, and `skill`/`spell` dispatch paths are missing; there is no skill/spell result path.
- **mwhere:** no argument lists all room mobiles instead of connected visible characters and switched originals. Named searches ignore PCs entirely.
- **owhere:** only top-level room objects are searched, missing carried, equipped, and nested objects. C also applies visibility and level rules and reports the outer carrier/location.

Evidence: [Python diagnostics](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:559); [C stat/rstat](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1038), [C vnum](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1726), [C owhere](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1866), [C mwhere](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1927).

### F14 — [P2] Numeric disconnect cannot close an unauthenticated connection

The numeric path locates the socket but then returns `session.character`. A pre-authentication descriptor has no character, so it is treated as a missing target and never closed. C closes the matching descriptor directly, independently of whether it has a character. The name-based Python path additionally excludes mobile bodies, preventing name-based disconnection of a switched session.

Evidence: [resolution](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/WizApi.py:603), [command](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:1115); [C disconnect](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:542).

### F15 — [P2] Wizinvis bypasses the range guard; visibility setters retain reply state

`invis` and `wizinvis` share a handler, but only `invis` has the range guard. Thus `wizinvis 100` or `wizinvis -1` can set a level that the equivalent `invis` rejects. C aliases both names to the same range-checked function. Explicit `invis <level>` and `incognito <level>` also clear the actor's reply pointer in C; Python leaves `context['reply_to']` intact.

Evidence: [shared visibility helper](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:386), [wizinvis document](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:9305); [C invis/incognito](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:4231).

### F16 — [P2] Advance does not persist its result immediately

The Python advance path adjusts level, resources, experience, and trust and returns messages without requesting a save. C ends with `save_char_obj`. A service restart before a later autosave can discard an administrator's level change. This is a persistence timing gap, not a request to copy C's file format.

Evidence: [Python advance](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/WizSetApi.py:60); [C save](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2708).

### F17 — [P2] Echo provenance and immortal-channel visibility differ

Room/global/zone echoes send identical unmarked text to all recipients. C prepends `local>`, `global>`, or `zone>` for recipients with trust at least the sender's. Pecho similarly lacks C's personal-echo provenance rule. This removes the indication that apparently authoritative text was generated by an echo command. `immtalk` uses the literal actor name for all recipients instead of C's visibility-aware `$n`, revealing an invisible sender's identity to recipients who cannot see them. These paths were traced through their collection payloads as well as their handlers.

Evidence: [echo handlers](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:220), [immtalk](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:712); [C echo variants](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:655), [C immtalk](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:708).

### F18 — [P2] String extended descriptions replace previous descriptions

`string obj chest ed lid ...` overwrites `extra_descr` and `extra_description`. Adding a second keyword loses the earlier description. C allocates a new extra-description entry and prepends it, preserving previous keywords. The current single-description representation limits a faithful fix; any expansion should remain compatible with designer/service data rather than hiding a second description store in Python.

Evidence: [Python string](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:822), [description model](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/ExtraDescriptionData.py:9); [C append behavior](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3831).

### F19 — [P2] Slay discards death notifications returned by raw_kill

`raw_kill` returns death-cry/corpse notices for callers to emit, but `do_slay` ignores that list and emits only the slay payload. State changes and corpse creation still occur; death notifications do not. C emits the slay messages and then executes raw_kill's death-cry behavior.

Evidence: [slay caller](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:793), [returned notices](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:556); [C slay](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:3060), [C raw_kill](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1660).

### F20 — [P2] Immortal movement leaves furniture and carried-light bookkeeping behind

`WizUtil.move_entity` changes membership and IDs but does not clear `entity.on` or transfer carried-light contribution between rooms. Room add/remove methods do not perform those operations either. A transferred/teleporting character can remain associated with furniture in the old room and leave illumination in the wrong room. C `char_from_room` clears furniture and decrements light, and `char_to_room` increments destination light. For `at`, furniture must be saved before moving and restored after returning, while the nested command must execute detached from the old furniture.

Evidence: [shared move](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/WizUtil.py:50), [room membership](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/Room.py:142), [at](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:258); [C leave](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1327), [C enter](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1378).

### F21 — [P3] Wiznet rejects its canonical newbies option and abbreviations

The handler constructs `WIZ_<argument>`, so `wiznet newbies` looks for nonexistent `WIZ_NEWBIES`; the actual bit is `WIZ_NEWBIE`. C's table maps the canonical plural name to that bit. Python also requires exact option/control names where C accepts prefixes. Python's singular `newbie` works, but that does not preserve the documented/table spelling.

Evidence: [Python options](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:154), [option enumeration](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/WizHandler.py:210); [C option handling](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:49), [C option table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/const.c:93). Collection-query confirmed the service table also names this option `newbies`.

### F22 — [P3] Wizhelp lists commands unavailable to its caller

Python lists every command whose role is immortal, without checking trust, enabled state, or display visibility. A lower immortal sees implementor-only commands; a disabled definition is still listed. C filters by required level and the command's show flag. This does not grant execution rights, but gives an inaccurate command list.

Evidence: [Python listing](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:146); [C listing](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:772).

## Unresolved differences and exclusions

- **U01 — Newlock and newbie bans:** neither is connected to a Python character-creation path. The runtime authenticates already registered characters, while creation belongs to another service/workflow. The flags have no runtime effect here, but matching ROM's creation restriction needs an agreed cross-service contract. Existing-player login denial should not be substituted for creation gating.
- **U02 — Guild validation:** Python accepts arbitrary guild strings; C looks them up in its clan table and rejects unknown names. There is no corresponding clan catalog in the inspected GameData contract. Determine whether free-form guild creation is intended before enforcing a fixed catalog. NPC targets are also excluded by the Python lookup whereas C allows them.
- **U03 — Ban reference quirks:** this C checkout's `check_ban` has no exact-host branch for an unstarred pattern, and its double-star substring test is reversed. Python implements conventional exact/contains matching. These observable differences were recorded rather than recommended as regressions to reproduce. Prefix/suffix matching, ban kinds, trust protection, and permanent serialization were traced.
- **U04 — Diagnostic representation:** Python `memory`/`dump` report runtime counts rather than C allocation pools/byte totals and dump files. C allocation details are architecture-specific and are not parity defects. Whether `dump` should export a comparable operational artifact remains a product decision.
- **U05 — Immortality threshold differs from ROM:** the collection sets `LEVEL_IMMORTAL` to **55**, equal to the named `IMMORTAL` rank; C sets `LEVEL_IMMORTAL` to **52**, the `AVATAR` rank, while its named `IMMORTAL` rank is 55. Consequently Python's `IM` commands and general immortal-role checks exclude levels 52–54 that ROM permits. This is a confirmed data discrepancy with broad effects, but whether the higher threshold is an intentional game-design choice is not documented in the inspected sources. Resolve that intent before changing it. Evidence: [Python parameter](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.GameData.json:115), [C constants](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:134), [Python level resolution](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/CommandAccess.py:40).
- Exact-command/shortcut dispatch is used throughout Python instead of ROM's generic command-prefix matching. Only concrete command-specific problems (such as `prefi`, set fields, and wiznet options) are reported above; no broad interpreter rewrite is prescribed.
- The C command table comments out some entries (`at`, `goto`, `sockets`) while their function implementations remain. Their Python exposure was not treated as a defect. The active shared commands' symbolic access levels were checked; U05 records the important difference in what `IM` resolves to.
- C undefined behavior and C memory-management details were excluded.

## Coverage matrix

Every named command below had its active collection route inspected. “No new core mismatch” means no additional discrepancy was established in the inspected main path; it does not certify every input or erase shared findings.

| Family | Commands | Result / remaining scope |
| --- | --- | --- |
| Server lifecycle / admission | reboot, shutdown, wizlock, newlock | F02, F03; U01. Listener, sessions, cleanup, and admission traced. |
| Site / access moderation | allow, ban, permban, deny | Ban core policy and deny save/disconnect traced; U01/U03 and shared targeting F07. |
| Command auditing / execution | log, force | F08; force group/trust fixes remain present, with F06/F07 affecting switched/offline targets. |
| Immortal movement | at, goto, violate, transfer, teleport | Combat-stop, bulk-transfer, and goto privacy fixes remain present; F07/F20 remain. |
| Session control | switch, return, snoop, protect, disconnect, sockets | F06/F07/F14. Sockets lacks C's visibility filtering and considers playing sessions only; treat that as an additional diagnostic limitation under F13. Snoop bindings/loop guards/output mirroring and return cleanup inspected. Protect excludes NPC targets although C accepts them. |
| Punishments | freeze, nochannels, noemote, noshout, notell, pardon | F01/F07. Pardon clears both runtime representations and saves; no new core mismatch established for its flag clearing. |
| Combat / recovery / removal | restore, peace, slay, purge | Recovery/peace fixes remain present; F04/F07/F19 and switched response limitation F06. |
| Creation | load, clone | New-format load levels and recursive clone eligibility remain corrected; F10/F07. Old-format object initialization formulas were not re-audited across every item type. |
| Content / character administration | set, flag, string, advance, trust, guild | F07/F11/F12/F16/F18, U02. Flag guards, bit operations, protected-bit preservation and enum resolution traced. Trust excludes NPCs even though C accepts them; shared trust behavior for NPC bodies needs correction before claiming complete trust parity. |
| Visibility / appearance | holylight, invis, wizinvis, incognito, poofin, poofout | F06/F15. Poof storage/name requirement traced. Holylight lacks C's NPC early return and can modify mobile act bits when switched. |
| Communication / command prefix | echo, gecho, zecho, pecho, immtalk, smote, wiznet, prefix | F09/F17/F21. Smote personalizes only the first case-insensitive occurrence of a viewer name, whereas C walks subsequent occurrences case-sensitively; this smaller textual discrepancy was identified but not assigned a separate finding. |
| Diagnostics | wizhelp, mwhere, owhere, stat, vnum, memory, dump | F13/F22; U04. Core count sources inspected; allocation-byte equivalence excluded. |
| Help / records | imotd, penalty | Actual help/note routes confirmed; F05. Note visibility, drafts, read tracking, service CRUD, and delete authorization inspected. Other general note differences (such as numbering conventions) were not expanded into a whole-note-system audit. |

## Suggested remediation order

1. Guard enforcement, purge extraction, lifecycle/admission, and penalty-record deletion: F01–F05.
2. Shared switched-body identity/output and live/visible targeting: F06–F07. These influence many apparently independent commands.
3. Logging, prefixes, clone state, setter semantics, and diagnostics: F08–F13.
4. Remaining per-command persistence, visibility, messaging, content, and movement gaps: F14–F22.

Keep denial text and ordinary content behavior in collections. Prefer reusable identity, targeting, extraction, movement, and persistence primitives for fixes that span commands. Add behavioral tests that execute the real collection guards and payload consumers; passing metadata-only tests did not detect the guard bypass.

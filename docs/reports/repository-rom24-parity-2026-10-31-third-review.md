# Repository-wide ROM24 parity review — October 31, 2026, third pass

**Five further behavioral mismatches were reproduced:** ordinary damage messages reveal invisible targets; `exits` exposes closed/restricted/dark destinations and works while blind; periodic poison notices reveal invisible sufferers and reach sleeping observers; secondary room extra descriptions cannot be inspected; and switched recipients use the NPC body's channel preferences instead of the original player's. No documented intentional exemption was found for these behaviors. They are separate from the ten remediated findings, whose 30 regression tests still pass.

This is a review only. Added artifacts are this report, read-only discrepancy probes, their outputs, and a fresh isolated-suite result file. Runtime, collections, existing tests, the local C reference, and unrelated working-tree/staged changes were not edited. Findings refer to the current working tree containing both accepted remediation sets, with Python HEAD `e4659bd4c9c573f1361fb3a60468ed939df4dd05`. The reference is `C:/Users/scott/PycharmProjects/PyRom/Rom24/src`; no executable-C or live-service validation is claimed.

## Findings

### F01 — P2: Ordinary damage messages identify invisible targets

**Trigger:** An attacker and a bystander cannot see an invisible target when a normal damage message is rendered, such as an ongoing fight with a target that has become invisible.

**Reference:** [fight.c:2016](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2016) constructs damage messages using `$n` and `$N`, then sends actor, victim, and room variants through `act`. [comm.c:2512](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2512) expands those names with each recipient's `PERS` visibility rules. The attacker and bystander should see a generic identity for a target they cannot see.

**Python:** [CombatHandler.dam_message](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:497) calculates literal attacker/victim names at [lines 527–528](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatHandler.py:527), then embeds them in every channel. Ordinary damage invokes this renderer, and round construction/delivery does not restore recipient visibility. Revealing the attacker during `damage` does not make the invisible victim visible.

**Reproduced:** Real visibility checks reject Alice seeing invisible Bob. Production `dam_message`, round construction, and standard-handler/message-bus delivery emit `You hit Bob.` to Alice and `Alice hits Bob.` to Cara, who also lacks detection. Both should identify Bob generically. This probe exercises the production message path; it does not simulate a full attack roll or HP transition.

**Consequence/remedy:** Combat discloses an opponent's identity. Render damage names separately for actor, victim, and each room observer, preserving recipient-aware text through the now-fixed merger. Include miss/immune/skill-noun/self-damage branches and visible-versus-unseen recipients in regression coverage. This finding concerns the base damage renderer, not the weapon-proc merge fixed in the previous pass.

### F02 — P2: `exits` bypasses blindness, closed-door, room-access, and darkness rules

**Trigger:** A mortal uses `exits` with a closed exit, an exit to `ROOM_IMP_ONLY`, an open exit into a dark room, or while affected by blindness.

**Reference:** [act_info.c:1328](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1328) checks blindness first. [Line 1343](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1343) requires destination room visibility and excludes `EX_CLOSED`. For listed destinations, [line 1356](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1356) substitutes `Too dark to tell` when the destination is dark. An inaccessible room or closed exit is omitted entirely.

**Python:** The actual command document calls [RoomHandler.print_exits](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/RoomHandler.py:50). Its authored guard has an empty predicate, and the handler performs none of those checks. It iterates every destination and renders its real name. `can_see_room_vnum` governs only numeric room identifiers and cannot replace destination-access or darkness checks. The ordinary look/autoexit path also calls this handler.

**Reproduced:** Four public-interpreter `exits` probes each print `North - Hidden Vault`: closed door, destination restricted to implementors, dark destination, and blind actor. The restricted-room probe first confirms `CharacterApi.can_see_room(actor, destination) == False`; the darkness probe confirms the real room's dark predicate. Each case violates a distinct reference gate within the same handler.

**Consequence/remedy:** Players discover routes or destination identities ROM hides, including while unable to see. Reuse shared blindness, room-access, exit-flag, and darkness rules. Cover explicit and automatic exits, empty results, immortal exceptions, and missing destinations while preserving designer-editable messages.

### F03 — P2: Periodic poison messages reveal unseen sufferers and reach sleeping observers

**Trigger:** An invisible poisoned character receives a status tick while an observer lacks detection or is sleeping.

**Reference:** [update.c:803](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:803) calls `act("$n shivers and suffers.", ...)` before periodic damage. [comm.c:2475](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475) excludes recipients below the default minimum position, and its name expansion is visibility-aware. Later self-damage revealing a sufferer does not retroactively change the already-rendered notice.

**Python:** [EffectUpdateHandler.py:163](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/EffectUpdateHandler.py:163) fills the skill/spell-owned message's victim token with `entity.display_name()`. [Line 184](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/EffectUpdateHandler.py:184) sends that one string to every room player except the sufferer, without a posture filter. The same shared notice path also serves plague tick/spread messages, although the executed probe is poison-specific.

**Reproduced:** With the actual poison spell document and effect record, production `tick_status_effects` delivers `Bob shivers and suffers.` to Alice, who cannot see Bob, and also to sleeping Cara. Only the subsequent periodic-damage collaborator is mocked; effect lookup, spell ownership, rendering, room enumeration, and bus delivery are real.

**Consequence/remedy:** Status ticks disclose identities and send room action messages to ineligible observers. Keep the messages in their owning ability documents; render room tokens per eligible observer before damage or spread changes state. Preserve the direct sufferer notice and tick ordering. This is not the fixed cast-announcement or teleport-notice path.

### F04 — P2: Room inspection ignores extra descriptions after the first entry

**Trigger:** A room has a valid linked extra-description chain: `banner` followed by `mural`; the player enters `look mural`.

**Reference:** [act_info.c:1179](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1179) searches room extras with `get_extra_descr`. [db.c:2052](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2052) walks the complete chain and returns the matching description. The second entry is as inspectable as the first.

**Python:** The room service and `ExtraDescriptionData` already load and retain `next` chains. Object-extra lookup uses the chain walker. However, [PlayerHandler.py:222](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:222) classifies room extras using only the root keyword, and [ItemHandler.py:85](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/item/ItemHandler.py:85) likewise renders only the root. Updating just one boundary leaves the other incomplete.

**Reproduced:** Loaded an equivalent minimal room extra-description document through the production room-service loader and confirmed that the canonical walker exposes both entries. Through the actual public look command and handlers, `look banner` prints `A bright banner.`, while `look mural` prints `You do not see that here.` This is a supported-contract fixture, not a claim that a particular bundled room currently contains that exact chain.

**Consequence/remedy:** Designer-authored secondary descriptions, including clues, are inaccessible despite surviving loading. Use the existing chain walker for room classification and rendering, preserving ROM's object/room ordering and ordinal-match behavior. Cover root/secondary entries, absent keywords, and overlapping item/room names.

### F05 — P2: Switched recipients use the body's channel preferences

**Trigger:** An immortal controls an NPC whose gossip setting differs from the original player's setting.

**Reference:** In [act_comm.c:366](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:366), gossip selects `d->original` when present for preference checks, including `COMM_NOGOSSIP` and `COMM_QUIET`, but delivers to the controlled body. Other global-channel implementations use the same descriptor/original distinction.

**Python:** [Communications._channel](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Communications.py:616) uses `session.character` for both filtering and delivery. The runtime already stores the original in session metadata and the body's `controller_original` context, but this recipient filter does not consult either.

**Reproduced:** A real mobile body with an explicitly immortal original is bound to that original's recipient connection. When the original has gossip disabled but the body does not, public `gossip hello` reaches the controlled connection. When the original has gossip enabled but the body has it disabled, nothing arrives. The command, channel helper, controller relationship, and real bus delivery are exercised; session enumeration is supplied by a minimal descriptor fixture.

**Consequence/remedy:** Switching bodies defeats the player's communication preferences or suppresses wanted channels. Separate the preference owner from the delivery body, using existing controller/session relationships. Test channel-specific opt-outs and QUIET in both directions, normal recipients, and return from possession. This is independent of the corrected punctuation dispatch entries.

## Repository coverage

The assessment inventories **214 Python source files, all 30 C translation units, 17 collection snapshots, and every current top-level unittest module**. Collection-query preceded authored-data inspection. Content counts remain 221 commands, 38 skills, 97 spells, 244 socials, 412 special records, 986 mobiles, 1,266 items, 3,127 rooms, and 5,196 resets. Counts identify the review surface; they do not certify each document's equivalence.

| Reference family | Evidence in this pass | Coverage qualification |
| --- | --- | --- |
| `interp.c`, `alias.c` | Public interpretation, prior parser/dispatch regressions, command definitions and pipeline boundaries | Representative input and authorization paths; not every abbreviation collision |
| `act_comm.c`, `act_info.c` | Damage-adjacent messages, channels/possession, exits, room/item inspection and public-command probes | F02/F04/F05; broad existing information/speech/social tests; not all prose/templates |
| `fight.c`, `effects.c` | Base damage renderer and actual delivery; defense/message and aftermath traces; combat and exposure suites | F01; full attack rolls/HP transition not part of the message probe; fixture gaps remain |
| `update.c` | Real poison status tick/ability payload path, current regeneration/cleanup/tick helpers and suites | F03; poison executed, shared plague path statically traced; not all traversal-order combinations |
| `magic.c`, `magic2.c`, `scan.c` | Spell/targeting/payload/breath suites and prior casting/teleport regressions | Suite-backed verification; not every spell's C branches independently re-traced this pass |
| `act_move.c`, `act_enter.c` | Movement/entry/recall/follower/portal tests and current recall trace | Sampled runtime branches and existing regressions; not every world topology |
| `act_obj.c`, `healer.c` | Factories, ownership/decay, shop stock/pricing/pets, object/healer suites | Selected current source paths; fountain/theft test limitations remain |
| `skills.c`, `const.c` | Creation-point XP formula checked against this exact C checkout; learning/training/advancement suites | The unusual sub-40-point integer division matches C and is not reported as a defect |
| `db.c`, `db2.c`, `handler.c`, `lookup.c` | Room extra loader/chain lookup, visibility/carry helpers, reset/factory/population suites | F04; full legacy-area conversion and all room/item records not compared |
| `special.c` | Current mobile pulse, special dispatch and shop-money traces, special/pulse suites | Selected scheduler/helper paths; not all 412 special records independently executed |
| `act_wiz.c`, `ban.c`, `flags.c`, `tables.c` | Possession representation, site-ban policy, current extra-description editing, administrator/flag suites | Focused current interfaces plus regression sweep; not every admin mutation/table value |
| `note.c` | Current recipient/read/remove/draft boundaries and note suites | Sampled contracts; no live note-service transactions |
| `comm.c`, `save.c` | Recipient visibility/posture reference, delivery, fresh time-snapshot/source checks and persistence/reconnect tests | Prior timing fixes retained; external service transformations and offline recovery remain unverified |
| `music.c`, `recycle.c` | Inventory and existing runtime/persistence context | No claim of music-delivery or C allocation/free-list parity |

All **30 regressions for the previous ten fixes pass**: cast announcements, NPC attack fallback and origin cleanup, punctuation parsing/dispatch, whitespace preservation, pose, teleport, playtime/XP, and combat-proc merging. The newly found paths occur before or outside those corrected boundaries. Passing those regressions did not establish visibility or behavioral equivalence across all message producers and handlers.

## Validation and artifacts

Ran all top-level `tests/test_*.py` modules separately using the repository Python 3.14 environment, `PYTHONPATH=src`, up to four independent processes, and a 60-second per-module limit. Local loopback access was used for Windows asyncio. **135 modules / 1,654 reported tests; 123 modules pass, containing 1,345 tests.** No module timed out. The 12 non-passing modules retain exactly the failure/error identifiers in the final second-remediation snapshot: **4 failures and 29 errors**. The source was not modified during this run.

| Non-passing module | Existing limitation |
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
| `test_player_handler_cast_prompt` | Messaging-package import failure |
| `test_remaining_gameplay_parity` | Five fixture errors: missing `handler_service` |
| `test_spell_affect_payload_messages` | Three pre-existing energy-drain assertion failures |

The new read-only probes independently assert observed discrepancies. They are evidence scripts rather than desired-behavior regression tests. Reference expectations were traced in source, not obtained by running a compiled C server.

- [Probe source](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-third-probes.py)
- [Observed probe outputs](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-third-probes.json)
- [Complete isolated test results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-third-tests.json)
- [Second review and remediation record](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-31-second-review.md)

## Unresolved differences and limits

The earlier command-prefix, idle/limbo/autoquit, and pose class/level-table policy questions remain unresolved. No authorization to change those policies is inferred. Offline resource recovery and upstream character-service responsibilities still require contract tracing. Dynamic enums, designer-authored content/payloads, service-backed storage/authentication, async transport, and managed memory remain accepted architectural differences rather than findings.

This is a repository-wide assessment with explicit evidence depth, not proof of every function, content document, random outcome, input, or persistence sequence. Complete area-data comparison, legacy `tests/old-tests`, live server/content-service integration, actual socket sessions, and executable-C differential validation were not performed. A domain without a new finding is not certified equivalent.

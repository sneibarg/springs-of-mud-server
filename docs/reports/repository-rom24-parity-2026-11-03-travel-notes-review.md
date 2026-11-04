# ROM24 parity review after communication and item-decay fixes

November 3, 2026. Reviewed the working tree based on Python HEAD `40949b8` against the local ROM24 C source. Both prior room and combat remediation sets and the latest communication and item-decay fixes are present.

## Findings

### P2 — Directional travel defeats stealth and discloses invisible identities

ROM24 suppresses both notices for a traveler with AFF_SNEAK or an invisibility level at least LEVEL_HERO. In other cases, the C `act` call resolves the actor separately for each eligible observer and excludes observers below resting. Springs emits the authored departure and arrival keys with a literal actor name and an unfiltered room player list. The older MovementApi helpers implement part of the suppression policy, but the active directional command path constructs separate payloads. Using the actual north command document, movement handler and standard payload resolver, I observed `actor leaves north.` for a witness in all three cases tested: AFF_SNEAK, invisibility level 60, and ordinary magical invisibility. Flee and wander use the same physical travel path.

[ROM24 act_move.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:191) · [ROM24 act posture and visibility](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475) · [Movement.py](../../src/interp/commands/Movement.py#L113) · [MovementApi.py](../../src/api/MovementApi.py#L451)

### P2 — Recall notices reveal an invisible traveler

ROM24 renders the prayer and departure in the origin, and arrival in the destination, with each observer's visibility and the resting threshold. Springs captures both audiences but inserts the same literal name into each notice. The production recall and payload resolver produced `actor prays for transportation!` and `actor disappears.` for a witness lacking detection. The prayer runs before recall's failure conditions, so a failed recall can disclose the same identity without movement. This path is separate from the previously repaired teleport spell notices.

[ROM24 act_move.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1415) · [ROM24 arrival and departure](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1456) · [Movement.py](../../src/interp/commands/Movement.py#L335) · [Recall movement notices](../../src/interp/commands/Movement.py#L378)

### P2 — Portal entry announces the literal traveler and portal to observers

ROM24's entry and arrival notices render actor and object placeholders independently. Springs supplies both literal descriptions to every observer. An invisible traveler produced `actor steps into portal.` for a witness lacking detection in the real enter payload path. Separately, a traveler who can detect an invisible portal can name it to bystanders who cannot see it. That object branch and the arrival branch were confirmed by tracing the template and token inputs. Like recall, this path also uses a room player list without the C posture gate.

[ROM24 act_enter.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_enter.c:129) · [ROM24 actor and object placeholders](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2512) · [Movement.py](../../src/interp/commands/Movement.py#L454)

### P3 — Law-room follower rejection gives no explanation during ordinary travel

A leader enters a LAW room with a standing aggressive NPC follower. Both implementations leave the follower behind. ROM24 tells the leader that the follower cannot enter the city and sends the follower its own refusal. Springs silently skips that follower in ordinary travel. The portal path has a separate rejection branch with authored messages. This is a source-confirmed feedback discrepancy.

[ROM24 act_move.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:218) · [Movement.py](../../src/interp/commands/Movement.py#L139) · [Portal follower handling](../../src/interp/commands/Movement.py#L487)

### P2 — Notes addressed to a clan are hidden from its members

ROM24 treats the reader's exact clan name as a recipient token. Springs recognizes personal names, sender, all, and immortal aliases, but never tests the reader's clan. A note sent to a canonical clan name can be visible to its author while absent from the members' lists and unread selection. The previous notes review identified this difference but left the mapping open. The current guild command assigns the canonical catalog name directly to the persisted `guild` field, so the runtime representation is now established. This is a source-confirmed runtime discrepancy. Delivery through a live note service was not exercised.

[ROM24 note.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:343) · [NoteHandler.py](../../src/notes/NoteHandler.py#L271) · [Wiz.py](../../src/interp/commands/Wiz.py#L1056) · [Previous notes review](repository-rom24-parity-2026-10-30-notes-review.md)

## Validation and coverage

- Re-ran 56 focused tests for movement, visibility, and communication. All passed. Executed five additional travel/recall/portal scenarios through the production command handlers and payload resolver. These probes validated selected recipients and rendered messages before socket delivery.
- Used the immediately preceding full isolated run on the same runtime as repository-wide regression evidence. It reported 1,659 tests across 136 modules. 124 modules passed and 12 previously failing modules remained.
- Consulted the [historical translation-unit coverage matrix](repository-rom24-parity-2026-10-31-third-review.md#repository-coverage). Fresh traces in this pass concentrated on directional travel, follower rules, recall, portal entry, notes, and the current authored payloads. The full suite covers the broader domains, including combat, magic, objects, shops, NPCs, world updates, advancement, administration, sessions, and persistence, subject to its existing failures.
- This pass did not independently repeat a branch-by-branch source comparison across all subsystems, compare every world-data record, or execute a compiled C server or live note/content services. The earlier command-prefix, idle/limbo, pose eligibility, offline recovery, and clan QUIET policy questions remain open.

Only this report was added during the review.

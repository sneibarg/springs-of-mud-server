# ROM24 parity review — November 3, 2026

Reviewed Python revision `40949b8` against the local `PyRom/Rom24/src` checkout. This pass uses the October 31 repository-wide audit as its baseline and rechecks its five outstanding findings against current source. The previous pass contains the full family-by-family coverage matrix and executable evidence. Coverage outside the five paths below is historical and was not independently repeated for this revision.

## Findings

| Priority | Trigger | ROM24 behavior | Current Springs behavior |
| --- | --- | --- | --- |
| P2 | An opponent becomes invisible during combat | Damage messages resolve each actor's identity for the recipient in [fight.c](../../../PyRom/Rom24/src/fight.c#L2016) and [comm.c](../../../PyRom/Rom24/src/comm.c#L2512). | The renderer inserts literal names into actor, victim, and room messages, exposing the invisible opponent. [CombatHandler.py](../../src/combat/CombatHandler.py#L527) |
| P2 | A blind mortal uses `exits`, or an exit is closed or leads to a restricted or dark room | The command checks blindness, omits closed and inaccessible exits, and obscures dark destination names. [act_info.c](../../../PyRom/Rom24/src/act_info.c#L1328) | The handler lists destinations with their real names, leaking route or destination information. The room display also uses this handler for automatic exits. [RoomHandler.py](../../src/area/RoomHandler.py#L50) |
| P2 | Poison ticks while the sufferer is invisible or an observer is asleep | The periodic notice uses recipient-aware identity and excludes sleeping observers. [update.c](../../../PyRom/Rom24/src/update.c#L803) and [comm.c](../../../PyRom/Rom24/src/comm.c#L2475) | The shared status notice inserts the sufferer's literal display name and sends it to other room players without a posture gate. [EffectUpdateHandler.py](../../src/item/EffectUpdateHandler.py#L163) |
| P2 | A player looks at a keyword in the second or later entry of a room's extra-description chain | Room lookup walks the entire chain. [act_info.c](../../../PyRom/Rom24/src/act_info.c#L1179) and [db.c](../../../PyRom/Rom24/src/db.c#L2052) | Both classification and rendering check only the first room entry, making subsequent descriptions inaccessible. [PlayerHandler.py](../../src/player/PlayerHandler.py#L222) and [ItemHandler.py](../../src/item/ItemHandler.py#L85) |
| P2 | A switched immortal's gossip or quiet preference differs from the possessed body's | Gossip filters on the original player's preferences and delivers to the controlled body. [act_comm.c](../../../PyRom/Rom24/src/act_comm.c#L366) | Global channel routing uses the controlled body for both steps. A player can receive a channel they disabled or miss one they enabled. [Communications.py](../../src/interp/commands/Communications.py#L616) |

## Coverage and evidence

- The [October 31 coverage matrix](repository-rom24-parity-2026-10-31-third-review.md#repository-coverage) maps all 30 C translation units to reviewed behavior or explicit coverage gaps. It covers combat, spells, movement, objects and shops, NPCs and world updates, progression, communication and inspection, notes, administration, and session and persistence boundaries.
- The five findings above are current static confirmations of [previously reproduced discrepancies](repository-rom24-parity-2026-10-31-third-probes.json). The collection-query CLI enumerated 17 collections and found the authored exits command. This was a targeted snapshot check.
- The [historical isolated suite results](repository-rom24-parity-2026-10-31-third-tests.json) reported 123 passing modules out of 135. Those counts apply to the October 31 run. This pass did not complete a new isolated suite or a fresh executable comparison.
- Command prefix resolution, idle and limbo policy, pose eligibility, and offline resource recovery remain unresolved policy or service-contract questions. Full spell-branch and world-content comparison, live service behavior, and executable C differential testing remain open.

Only this report was added.

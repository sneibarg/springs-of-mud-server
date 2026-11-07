# Completed item: is_same_clan

**Complete static specification of `src/handler.c:is_same_clan`, with 19 specified cases and no remaining function-level gaps.** All original case IDs are preserved. The full caller implementations and the rest of handler.c remain separate partial/pending report items. No executable gameplay tests were generated or run.

Source: [helper](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:333), lines 333–339, and [clan table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/tables.c:42). HEAD reference: `d3a29007355e7298e0033fcb666e9a6895c2146f`. SHA-256: handler.c `0e95a3bd6480448855bba8d7cae6b6f8b5aad3d2be2738a21cd58571f7bf2261`; tables.c `ee69d8e2e1a7f78420f3f48c652fccd6db32d5c761eca17dad2ff56c720b6e33`. Generation verifies both reviewed hashes. Normal Git status is unavailable; the [manifest](manifest.json) records the independent HEAD comparison and source hashes.

## Complete contract

The actor must be readable and its clan must index the three-row table (`MAX_CLAN=3`). Indices 0 (unaffiliated) and 1 (loner) have `independent=TRUE`; either causes an immediate FALSE return without dereferencing the victim. For index 2 (rom), the helper compares actor and victim clan integers and returns that equality. Here the victim must be readable, but its clan need not be a valid table index because the helper never indexes it. No relative operand evaluation order is imposed on the final equality expression.

| Actor clan / victim clan | 0: unaffiliated | 1: loner | 2: rom |
|---|---|---|---|
| 0: unaffiliated | FALSE | FALSE | FALSE |
| 1: loner | FALSE | FALSE | FALSE |
| 2: rom | FALSE | FALSE | TRUE |

Every cell has a concrete `handler.is_same_clan.clans-A-B` case in the [catalog](cases.json) and [pseudo suite](pseudo-suite.md). Three self-identity cases establish that comparing a character with itself still returns false for independent memberships. Three NPC/PC combinations complement the base matrix: kind, level, trust, position, room, connection and effects are not consulted. Two NULL-victim cases prove the independent-actor early return. Two cases with actor clan 2 and victim clan -1 or 3 return false without indexing the victim value.

The only dependency is the immutable table; there are no callees, macros, loops, recursion, allocations, random draws, callbacks, messages or mutations. There are no conditional compilation alternatives within the helper/table. Readable valid input gives a fully determined Boolean. NULL actor, out-of-bounds actor index, or NULL victim with actor clan 2 violates the read preconditions; no portable failure outcome is asserted. The predicate is directionally implemented even though its valid three-by-three result matrix is symmetric.

| Ledger item | Outcomes and evidence | Disposition |
|---|---|---|
| `handler.is_same_clan.if.001` | independent TRUE for 0/1; FALSE for 2 | Specified |
| `handler.is_same_clan.return.001` | FALSE before any victim access, including NULL victim | Specified |
| `handler.is_same_clan.return.002` | Equality TRUE for 2/2; FALSE for 2/0, 2/1 and non-table victim values | Specified |
| Implicit identity/kind alternatives | Three aliasing cases, all four kind combinations with matrix baseline | Specified |

```text
CASE handler.is_same_clan.independent-1-null-victim
GIVEN readable actor with clan=1 and victim=C NULL
WHEN is_same_clan(actor, victim) is called
THEN inspect clan_table[1].independent and return FALSE
AND NEVER dereference victim, emit output or mutate either entity

CASE handler.is_same_clan.victim-clan-outside-table-3
GIVEN actor.clan=2 and readable victim.clan=3
WHEN is_same_clan(actor, victim) is called
THEN clan_table[2].independent is FALSE, compare 2 with 3, return FALSE
AND NEVER access clan_table[3]
```

## All five caller sites

A source-wide symbol search found five direct calls and a [header declaration](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:2200). No table takes this helper's address; it is not itself a command, special callback or scheduled update. Caller gates do not become helper preconditions.

- [do_clantalk](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:657) rejects nonmembers and independent senders. Empty input toggles the channel and returns. Nonempty input requires channel privileges, clears sender NOCLAN, and sends the sender's echo before recipient iteration. Only playing descriptors with a character different from the sender reach the helper. A true result is followed by recipient NOCLAN and QUIET checks before `act_new` targets that recipient at POS_DEAD. It uses the active `d->character`, not an original controller. The [clan command entry](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:94) requires POS_SLEEPING and level 0; direct calls do not inherit interpreter gates.
- [damage](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:898) calls after `raw_kill`, only for a distinct attacker who is not an NPC. If the result is false, it removes victim PLR_KILLER when present; otherwise it removes PLR_THIEF. A true result skips that removal. This checks fields at the actual post-kill call, not a pre-death snapshot. [raw_kill](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1660) relocates PCs and extracts NPCs; [free_char](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:342) recycles an NPC structure without clearing its clan integer. The helper has no validity or liveness check. Complete death/recycle behavior is not claimed by this helper specification.
- [spell_gate](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:2898) evaluates `is_clan(victim) && !is_same_clan(ch,victim)` after earlier lookup/room/level failures but before the hero/NPC save checks. Victim clan 0 skips the helper; nonzero includes loner. False from the helper makes this guard fail the spell with `You failed.\n\r` before movement. Matching real clans only pass this guard, not all other guards.
- [spell_portal](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic2.c:74) uses the same expression as its final travel guard, after hero/NPC immunity/save checks. Failure occurs before held-component lookup, consumption or portal creation.
- [spell_nexus](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic2.c:127) likewise uses it as the final guard after destination/origin visibility, room flags, level and NPC save checks. Failure precedes components and creation. The skill table dispatches gate at POS_FIGHTING and portal/nexus at POS_STANDING; all three are TAR_IGNORE ([gate](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/const.c:1378), [nexus](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/const.c:1491), [portal](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/const.c:1520)). Those spell-entry conditions are not tested inside this helper.

`is_clan` itself simply returns the actor clan value ([source](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:328)); membership and same-clan eligibility are distinct. In particular, two loners fail the travel clan check, while an unaffiliated destination skips it. Loaded character data selects among the compiled rows; it cannot alter the independence flags. The complete matrix therefore covers all valid table-dependent helper outcomes without inspecting collection data.

## Adaptation and verification

Python [CharacterApi.is_clan](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/CharacterApi.py:102) reads the content-service `guild` representation and includes independent loner membership. No same-clan helper was found in the inspected Python source. Future neutral fixtures should model both membership identity and independence; do not equate nonempty guild equality with this C predicate. No Python parity, approved override or implementation change is claimed.

Manual tracing establishes the source expectations. Regeneration/validation checks the source hashes, all nine matrix cells, 19 case outcomes, early-return read constraints, caller references and bidirectional ledger links. [Validation results](verification.json) distinguish these artifact checks from execution: no C probe or gameplay test ran. The completion record has no remaining helper gaps; unrelated callers retain their own partial/pending dispositions.

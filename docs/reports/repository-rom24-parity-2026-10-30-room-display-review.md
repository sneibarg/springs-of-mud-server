# Repository ROM24 parity review — room display and consider, 2026-10-30

**All three findings resolved.** Room-character rendering reads criminal markers from act flags and renders secondary fighting opponents through the observer-aware entity helper, including NPC short descriptions. The YOU, missing-opponent and departed-opponent branches remain intact. Consider now calls the existing runtime melee safety policy after its argument/target guards, returning the policy's reason followed by its existing authored refusal for protected targets.

**Validation:** six new regressions cover act/comm separation, NPC marker exclusion, invisible opponents, NPC names, fighting display branches, safe rooms, shopkeepers, trainers/practicers/healers/changers, existing-combat and immortal safety exceptions, and missing-input guard ordering. All **212 tests across 21 isolated suites pass**, including the recent note and weapon/prompt fixes. `git diff --check` passes. [Remediation results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/room-display-consider-remediation-2026-10-30-tests.json). No collection edits or live deployment were performed. Original review follows for history.

Review of the current working tree, including the recent note, weapon-drop and prompt fixes. No runtime, collection or test changes were made during this review. Three behavioral mismatches were reproduced.

## P2 — Room display reads killer/thief markers from communication flags

[PlayerUtil.py:59](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/PlayerUtil.py:59) reads `status_flags.comm` inside `_has_player_act_bit`, then tests that value against PLR_KILLER and PLR_THIEF. [Room.py:323](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/Room.py:323) uses this helper for visible players during room display. ROM [act_info.c:261](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:261) tests these flags against the target's `act` field.

Production-model probe: a visible player with both act flags set and comm=0 rendered simply `Hidden target is here.` Clearing act and putting those same bit values in comm instead rendered `(KILLER) (THIEF) hidden target is here.` The PLR_THIEF bit overlaps COMM_AFK in the reference definitions ([merc.h:1234](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1234), [merc.h:1265](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1265)); an ordinary AFK player can therefore be falsely labeled a thief.

Consequence: room inspection misidentifies player criminal status. Read the canonical act bitfield for these markers, retaining the player-only restriction. This is not a change to intentional cloak concealment.

## P2 — Fighting descriptions expose unseen opponents

[PlayerUtil.py:138](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/PlayerUtil.py:138) uses `fighting.name` directly when the target and its opponent share a room. Visibility filtering in Room protects the character whose line is being shown, but does not check this secondary opponent reference. ROM [act_info.c:391](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:391) uses `PERS(victim->fighting, ch)`, which applies the observer's visibility and an NPC's short description.

Probe: a visible player's opponent was named SecretImmortal, with invis_level=60 and the same room ID. `CharacterApi.can_see(observer, opponent, room)` returned false, yet `room.get_players_in_room(observer)` returned `Hidden target is here, fighting SecretImmortal.` ROM would render the unseen opponent as someone. A visible NPC opponent also gets its keyword name rather than its short description through the same direct-name path.

Consequence: ordinary room inspection leaks identities that other commands conceal. Render the secondary opponent using the existing observer-aware entity helpers, preserving the YOU, absent-opponent and departed-opponent branches.

## P3 — Consider omits the melee safety check

[Info.py:455](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:455) resolves a visible target, runs its data guards and immediately compares levels. The bundled consider document has only missing-argument and missing-target guards; its existing `isSafe` message is unused. [PlayerHandler.py:257](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:257) delegates to this method without an additional safety boundary.

ROM [act_info.c:2343](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2343) calls `is_safe` before computing the level difference and refuses protected targets. That shared function rejects NPC attacks in ROOM_SAFE ([fight.c:1006](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1006)) and covers shopkeepers, trainers and other protection rules, with its normal exceptions.

Probe: a level-20 player considers a level-1 city guard in ROOM_SAFE. The production method returned `You can kill guard city sentinel naked and weaponless.` ROM instead emits its safety refusal followed by the consider refusal. This is misleading advice, not an attack-authorization bypass: actual attack commands have their own checks. Reuse the shared safety policy and authored consider refusal rather than copying its rules into this command. No documented intentional exemption for consider was found; product intent remains unconfirmed.

## Scope and validation

This was a repository-wide sampling pass, not an exhaustive function-by-function review. Source inspection covered information/room presentation and its callers; movement, doors and posture; automatic combat escape and melee/spell safety; death consequences; item expiration and ownership; living-entity tick phases and conditions; spell effect application; learning; area/mobile reset limits. The recent note, weapon-drop and prompt fixes were exercised through their regression suites rather than reported again. Local C traces covered act_info.c room/consider rendering and fight.c safety, with flag definitions in merc.h. Prior review evidence supplied context, not a substitute for tracing the new findings.

Collection-query inventoried snapshots and inspected the complete consider command definition. Deterministic probes used initialized MovementFixture game tables and production Room, Character, PlayerUtil and Info methods. They changed only in-memory fixtures and made no external writes. Expected behavior came from the local C source, not an executable C server.

**All 206 tests across 20 isolated modules passed.** Suites covered note remediation, affect-driven weapon drops and prompts, information commands and inspection, information utility boundaries, alias/prompt serialization, movement, combat defenses/death, weapon effects, object lookup/carrying/shops/equipment, population/resets, weather, hunger, learning, wizard recovery, spell object targeting and periodic damage. Tests ran in separate processes with PYTHONPATH=src; local Windows asyncio socket creation required execution outside the filesystem sandbox. [Machine-readable results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-30-room-display-tests.json).

No full discovery run, live-server/content-service validation, executable-C differential testing or exhaustive state/content coverage was performed. These passing suites do not cover the reproduced discrepancies. Other room-presentation differences such as title/furniture/AFK text were observed but were not fully traced or classified in this report.

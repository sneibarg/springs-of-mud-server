# Repository ROM24 parity review — wake and furniture, 2026-10-30

**Both findings resolved.** Wake now delegates to the existing visible room-character lookup, including NPC keywords, numbered selectors, self and player prefixes. Invisible targets are rejected without mutation; NPC messages use short descriptions. Existing target-waking behavior is preserved; the separately documented C actor-standing quirk was not adopted.

Room-character descriptions now render occupied furniture for sleeping, resting, sitting and standing, using the corresponding dynamic furniture flags with AT then ON then IN precedence. The no-furniture descriptions and NPC start-position long-description path remain intact.

**Validation:** seven new regression tests cover invisible and undetected targets, NPCs, keyword/ordinal/self/prefix lookup, magical sleep and already-awake branches, both entity types across all four postures and three relations, relation precedence and NPC long-description behavior. All **241 tests across 21 isolated suites pass**. `git diff --check` passes. [Remediation results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/wake-furniture-remediation-2026-10-30-tests.json). No collection changes or live deployment were performed. Original review follows for history.

Review only, against the current working tree including recent remediations. No gameplay code, collection documents or tests were changed. Two behavioral discrepancies were reproduced; a separate reference quirk requires an explicit behavior decision.

## P2 — Wake bypasses visible, unified room-character lookup

[Movement.py:289](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Movement.py:289) searches only `room.characters`, using raw exact-name/name-prefix matching. It does not inspect NPCs, enforce actor visibility, support keyword/ordinal selectors, or use the shared room-character lookup. The bundled wake command has no guards supplying these checks; [PlayerHandler.py:522](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:522) delegates directly and emits the returned action.

ROM [act_move.c:1319](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1319) uses `get_char_room`. That helper ([handler.c:2014](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2014)) searches all room people, applies can_see, keyword matching and numeric selection, and supports self.

Production-method probes using initialized game tables:

- A sleeping NPC with keywords `guard city sentinel` in the actor's room produced `target_missing` for `wake guard`. ROM finds the NPC and proceeds to its position/effect checks.
- A sleeping player named SecretImmortal with invis_level=60 was invisible to the actor (`CharacterApi.can_see` returned false), yet `wake SecretImmortal` returned the wake action and changed that player's position to standing. ROM rejects that lookup before performing any wake action.

Consequence: players can locate and interfere with unseen players, while visible NPC targets are unavailable. Reuse the shared visible room-character selector instead of maintaining a separate player-only search. This finding concerns target eligibility, independent of the successful-wake reference quirk below. Tests should exercise invisible targets, NPCs, numbered duplicate keywords, self and player prefix matching.

## P3 — Room descriptions omit occupied furniture

[PlayerUtil.py:124](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/PlayerUtil.py:124) renders sleeping, resting and sitting as generic `here` descriptions and standing falls through to the same generic location. It never examines target.on or furniture relation flags. Both player and NPC room listings use this renderer.

ROM's [act_info.c:282](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:282) checks the occupant's furniture and SLEEP_AT/SLEEP_ON flags, with the remaining case rendered as in. Equivalent REST, SIT and STAND branches follow ([act_info.c:307](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:307), [act_info.c:332](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:332), [act_info.c:358](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:358)). Preserve the earlier long-description fast path for NPCs at their start position.

Probe: a visible sleeping player whose on reference pointed to a room bed with SLEEP_ON rendered `SecretImmortal is sleeping here.` ROM reports that the character is sleeping on the bed. Python already stores furniture occupancy in its posture path ([Movement.py:259](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Movement.py:259)) and uses it for regeneration ([AnimateEntity.py:279](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/AnimateEntity.py:279)); the missing piece is display, not missing furniture support.

Consequence: observers cannot identify who occupies capacity-limited or regeneration furniture. Render the relation and furniture short description from the existing state. No documented intentional removal of occupancy descriptions was found; this is a verified compatibility discrepancy with unconfirmed product intent.

## Unresolved: successful targeted wake stands the actor in this C checkout

After notifying the victim, [act_move.c:1329](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1329) invokes `do_stand(ch, "")`, where ch is the actor, not the victim. Python instead sets the victim to standing ([Movement.py:304](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Movement.py:304)). This is defined reference behavior, though it appears to be a C logic error. The current Python behavior is also reflected in its authored wake messages. Do not silently change which character stands merely while fixing lookup. Decide explicitly whether this game wants literal parity with that quirk or conventional targeted waking; neither intent was established during this review.

## Scope and validation

Repository-wide sampling covered posture, wake and room presentation; visible lookup and command delegation; the recent consider/marker fixes; effects, weight-driven weapon drops and prompts; combat skill selection; NPC pulses; area/container resets; following and ordering. Additional tests exercised learning, movement, combat maneuvers, spells, elemental breath, item consumption/equipment, weather and administration. Local C inspection included act_move.c posture/wake, handler.c character lookup, act_info.c furniture rendering and db.c random-exit resets. This is not a line-by-line comparison of every gameplay function or document.

Collection-query inventoried all snapshots and inspected the complete wake command, including metadata, lambdas and payloads. Probes used the production Movement, Room and Character methods with existing initialized MovementFixture data, modifying only local in-memory entities. No external writes or C-server execution occurred.

**All 234 tests across 20 isolated suites passed**, including the latest room-display/consider regressions and earlier note, effect-drop and prompt fixes. [Machine-readable results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-30-wake-furniture-tests.json). Processes used PYTHONPATH=src; Windows asyncio suites required local socket access outside the filesystem sandbox. These existing suites do not cover the two reproduced discrepancies.

No full discovery run, live-server/content-service validation, exhaustive content/state exploration or executable-C differential tests were performed. Passing sampled tests does not certify whole-repository parity.

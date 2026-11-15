# Repository-wide ROM24 parity follow-up

November 14, 2026. Reviewed the Springs of MUD working tree at HEAD `3e2fdc570139d3aa69b7d1e031a4e4fa4eaca8ed`, including the completed November 14 fixes, against the local PyRom ROM24 source. P1 covers session or character access failures and economy defects affecting a shared runtime path. P2 covers material gameplay differences with narrower triggers.

| Priority | Finding | Player impact |
| --- | --- | --- |
| P1 | F01 · Ordering a follower to use `wear all` or `score` ends the player's session | A normal player can disconnect while issuing a valid order. |
| P1 | F02 · A saved pet with any carried or equipped item blocks login | The character fails to enter the world when the server restores the companion. |
| P1 | F03 · Spawned shopkeepers lack their cash replenishment budget | Shops below their authored cash target receive no periodic top-up and can stop buying from players. |
| P2 | F04 · Offensive spell damage omits the switched victim's direct message | A switched player can lose HP without the spell's hit message. |
| P2 | F05 · `hide` survives player death | A human character can respawn in the temple already concealed from other players. |

## F01 · Ordered mobile commands end the issuer's session

**Trigger and result.** With an awake, charmed, unswitched follower, enter `order follower wear all` or `order follower score`. ROM interprets the order as the follower. Its bulk wear walks the common carrying list, even when empty. Its score path formats NPC title and class separately. Springs also dispatches as the follower, but bulk wear reads the player-only `loot` attribute and score reads the player-only `title` attribute.

**Reproduction.** Ran the shipped `order`, `wear`, and `score` command lambdas through the real interpreter and game loop with a level-20 owner and a real mobile follower. Each order raised an `AttributeError` in its handler and ended the game loop after the first socket read. The outer connection handler closes the connection when the loop exits.

**Fix boundary.** Use the shared carrying API for bulk wear and provide NPC-safe score fields and armor calculation. Verify both through nested `order` and through an actual switched body. Include a subsequent input to establish that the issuer stays connected.

[ROM order dispatch](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1679) · [ROM bulk wear](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1673) · [ROM NPC score](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1402) · [Python bulk wear](../../../src/game/Equipped.py#L309) · [Python score](../../../src/interp/commands/Info.py#L280) · [Python nested order](../../../src/player/PlayerHandler.py#L730) · [Game-loop error boundary](../../../src/server/handlers/ConnectionHandler.py#L403)

**Resolution.** Bulk wear uses shared item ownership and skips worn items. Score formats NPC identity and stats and uses the same armor adapter as player score. The game-loop regression executes both ordered commands and then a player command. It also verifies that a switched body displays NPC score and armor. [Ordered command regression](../../../tests/test_wiz_identity_targeting_parity.py#L280)

## F02 · Item-bearing pet snapshots block login

**Trigger and result.** Save a character with a purchased pet that has one item carried or equipped, then authenticate and enter the world. A switched immortal can put a takeable object into a mobile's inventory with `load obj`. The previous review encountered the equipped case while checking hit roll. This review followed both forms through quit and fresh authentication. ROM reconstructs the owned companion from its prototype and saved pet state. Springs extends that persistence contract with item trees.

**Reproduction.** Ran the existing paid-pet quit/authentication fixture twice, with one carried item and with one equipped item. Using a mock API that faithfully stored the outgoing payload, quit succeeded and authentication identified the character. In both tests `_enter_world` raised before adding the player to the room. The recursive pet serializer drops `areaId` and `extraFlags` from nested item records along with the pet's own fields. The item constructor requires both. The error reaches the outer login cleanup, and the saved snapshot remains available to trigger the same failure on another attempt.

**Fix boundary.** Keep entity-only exclusions at the pet level and preserve the item schema for nested inventory and equipment. Exercise a new populated save and a previously written snapshot with omitted fields. Legacy records need a recovery path for login, with explicit handling of item metadata that cannot be reconstructed.

[ROM pet save](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:331) · [ROM pet reconstruction](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:1130) · [Python administrator object load](../../../src/interp/commands/Wiz.py#L642) · [Pet serializer](../../../src/mobile/PetSnapshot.py#L22) · [Item restoration](../../../src/mobile/PetSnapshot.py#L66) · [World admission](../../../src/server/handlers/ConnectionHandler.py#L153)

**Resolution.** New pet saves retain item areas and flags through carried, nested, and equipped item records. Legacy snapshots recover omitted fields from the item prototype when available and otherwise use the owner's area and zero flags. Exact runtime flag changes omitted by old saves cannot be recovered. The quit and fresh-authentication regression exercises the cache, the mock API response, and a legacy response. [Pet login regression](../../../tests/test_review_application_fixes.py#L228)

## F03 · Shopkeeper cash replenishment is unreachable after spawn

**Trigger and result.** Reduce a shopkeeper's cash below its authored wealth by selling items to it. ROM's mobile pulse checks the prototype's wealth before topping up the till. Springs loads wealth onto the prototype, then creates a live mobile without carrying the value over. The pulse reads wealth from the live instance, defaults to zero, and exits before rolling. A shop with depleted funds can continue rejecting sales across otherwise eligible replenishment pulses.

**Reproduction.** Loaded the shipped Midgaard potion brewer at vnum 3070 and its shop binding. The local C area and Python prototype both supplied wealth 5,000. After spawning, the mobile had no wealth attribute. With both coin balances at zero and both random draws forced to 20, the production top-up helper left the till at zero. Supplying the prototype wealth to the same live mobile and replaying the pulse added two silver, matching ROM's integer formula.

**Fix boundary.** Give the pulse access to the keeper's authored budget through the prototype or a declared runtime field. Check a keeper made by the normal spawn path at zero and at or above its target. Preserve special-procedure ordering and the existing per-pulse rolls.

[ROM potion brewer](C:/Users/scott/PycharmProjects/PyRom/Rom24/area/midgaard.are:566) · [ROM till top-up](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:399) · [ROM sale funds check](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2889) · [Python prototype wealth](../../../src/mobile/MobileFactory.py#L364) · [Python spawn](../../../src/mobile/MobileFactory.py#L109) · [Python till top-up](../../../src/mobile/MobileHandler.py#L179)

**Resolution.** Mobile creation copies the authored wealth budget into the live keeper. The pulse regression spawns a brewer whose budget is 5,000 silver, verifies the two-silver replenishment at zero cash with fixed rolls, and verifies that both rolls are skipped when the keeper reaches the target. [Shopkeeper pulse regression](../../../tests/test_wiz_identity_targeting_parity.py#L339)

After resolving F01–F03, all **1,743 tests across 137 active Python modules** passed in isolated processes.

## F04 · Offensive spells omit direct output for switched victims

**Trigger and result.** Hit a switched mobile with an offensive spell. In ROM, `magic missile` calls shared damage with messages enabled, and direct victim delivery uses the body's descriptor. The recent Springs fix covers the combat round builder and scheduler. Spell damage routes through `SpellApi.send`, which drops the direct victim line based on NPC type before the player emitter sees it.

**Reproduction.** Executed the shipped `magic missile` lambda against a real switched body with its connection still bound. With the save and damage roll controlled, HP fell from 50 to 47. The real damage formatter produced the victim line, and the spell queued zero direct messages for the controlled body.

**Fix boundary.** Apply shared connection-aware delivery to direct spell damage. Exercise a switched victim and an ordinary NPC through an authored offensive spell. Keep the separate scheduled-combat regression.

**Resolution.** Spell payloads use the same open-connection check as scheduled combat for direct NPC recipients. The mobile emitter routes direct victim lines through the message bus. The shipped magic missile regression verifies damage and direct delivery through both emitters while the body is controlled, then verifies that the same NPC takes damage without a direct line after the controller returns. [Spell delivery regression](../../../tests/test_wiz_identity_targeting_parity.py#L420)

[ROM magic missile](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:3648) · [ROM damage routing](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2072) · [ROM descriptor check](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475) · [Python spell damage queue](../../../src/api/SpellApi.py#L1558) · [Spell recipient filter](../../../src/api/SpellApi.py#L170)

## F05 · Death preserves recordless concealment

**Trigger and result.** Successfully `hide` as a human and die while the concealment flag remains set. The shipped hide skill sets `AFF_HIDE` directly. ROM removes temporary effects and restores the race's base affect flags on death. Springs removes effect records, but the hide flag has no record to remove. Room visibility continues treating the respawned character as hidden.

**Reproduction.** Used the shipped hide skill on a real level-30 human warrior with rating 90 and a forced successful roll, then invoked the production death handler. The temple received the player with `AFF_HIDE` still set, and the normal visibility check concealed the player from a mortal temple witness. There were zero active effect records before and after death.

**Fix boundary.** Restore the base innate affect flags at player death, clearing temporary flags set outside the effect list. Verify an ordinary human hide death and a character with legitimate innate affects.

**Resolution.** Death restores the race's authored affect bitfield after removing effect records and before the player enters the respawn room. The regression uses the shipped hide skill and verifies visibility after respawn for a human and an elf. It also verifies that the elf regains innate infrared vision. [Death affect regression](../../../tests/test_wiz_identity_targeting_parity.py#L860)

[ROM hide flag](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_move.c:1374) · [ROM death reset](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1679) · [ROM human and elf flags](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/const.c:178) · [Python skill activation](../../../src/api/SkillApi.py#L91) · [Python death cleanup](../../../src/combat/CombatHandler.py#L1920) · [Python concealment check](../../../src/api/CharacterApi.py#L464)

## Prior findings and validation

- The configured command API returned HTTP 200 and 221 records with `lambdas` and zero records with `function`. The real startup loader built a 222-entry local registry from that response, including the generated summary command.
- The configured character API returned HTTP 200 and two records with the `pet` field. The six character-progress fields from the November 13 report were absent from both. The companion API rollout for groups, combat counters, and note cursors remains pending. The item-bearing pet failure above reproduced with a faithful mock save response. The API check measured field presence on read. [November 13 resolution](repository-rom24-parity-2026-11-13.md#resolution) · [Companion API patch](f01-character-progress-som-server-modulith.patch)
- All **1,741 tests across 137 active Python modules** passed in isolated processes. The review covered the Python runtime and 17 collection snapshots, with fresh traces through interpreter and connection boundaries, persistence, combat, spells, effects, visibility, world updates, movement, shops, object ownership, and area resets. Branch coverage varied by subsystem.
- Verification used local runtime probes, shipped fixtures and content, read-only API GETs, and C source traces. The probes ran without a compiled ROM session or live gameplay. Idle and limbo policy, offline recovery, command prefixes, and movement-triggered aggression remain open policy questions.

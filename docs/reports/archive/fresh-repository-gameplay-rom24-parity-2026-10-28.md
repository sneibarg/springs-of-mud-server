# Fresh repository-wide gameplay parity review — 2026-10-28

Reference: `C:/Users/scott/PycharmProjects/PyRom/Rom24/src`. Reviewed Python: the current working tree of `C:/Users/scott/PycharmProjects/springs-of-mud-server`, including the completed G01–G28 remediation. This is a new review, with new identifiers R01–R15; the earlier report remains historical. **R01–R15 are resolved; no findings remain open from this review.** The review initially made no runtime, collection or test edits; the authorized equipment/reset remediation below subsequently changed those paths. Original finding line anchors and descriptions retain the pre-remediation evidence.

Only observable mechanics are findings. Service architecture, synchronization model, data-driven implementation, prose, administrative diagnostics and UI differences are excluded. No explicit design exemption was located for these discrepancies. Verified behavior does not establish designer intent; the report describes differences from this local C checkout rather than claiming every C rule is desirable.

## Equipment and reset ownership

### Remediation status — R01–R05 resolved

**Implemented 2026-10-28:** Equipment armor protection is derived from equipped armor values and ROM slot multipliers in combat AC, score AC and bash calculations. The stored armor scalar remains the baseline plus explicit affects; save/load, removal, cloning and filtered cloning therefore do not double-apply the newly supported base armor contribution.

Normal wear/wield/hold and reset equipment share runtime alignment checks and effect application. Incompatible items drop into the current room after the existing replacement/level/two-hand/weight checks, preserving C's removal-before-zap ordering and cursed-slot behavior. The three command documents own the zap messages. Raw equipment restoration stays available for persistence/clone paths that already copy effective affect state.

Room entry/exit now owns the transfer of lit equipped light contributions, while equip/unequip adjusts the current room. The equipped-light check accepts any nonzero fuel, including permanent lights. Duplicate entry/exit and occupied-slot equipment calls do not duplicate counts or discard items. Ordinary walking, spell/portal relocation, administrator movement, NPC movement, login, extraction and decay use this ownership lifecycle; administrator movement's old manual light adjustment was removed to avoid double counting. Light expiration removes its contribution once before detachment, preserving other carriers' light.

G resets always add inventory. E resets add inventory first, then attempt the requested equipment slot through the shared runtime primitive. Occupied/invalid slots preserve the item in inventory; incompatible E items fall into the room; successful E items apply their affects, including shopkeeper equipment. Mobile now has a zero-default damage-roll modifier so equipment APPLY_DAMROLL contributions can be applied and reversed through the existing effect handler without changing its separate prototype damage-dice calculation. AreaHandler receives the existing shared EffectHandler through injection.

**Content delivery:** Runtime and wear/wield/hold command payload updates must deploy together. The three payload changes were dry-run through collection-modify and verified through collection-query. Because this Windows Commands snapshot has the previously established atomic-replacement restriction, the validated writer output was applied in place with parsed-equality assertions and unchanged-document preservation. No item, mobile or reset content definitions were rewritten.

**Regression coverage:** `tests/test_equipment_reset_ownership_parity.py` adds 26 tests spanning every supported armor slot/category, explicit AC affects, save/load cycles, cloning/filtering, alignment/replacement/cursed-slot rules, actual command payloads, finite/empty/permanent lights, duplicate membership, multiple carriers, login, walking, administrator/NPC moves, extraction, burnout, consecutive G resets, E affects, shop stock, occupied/invalid slots, and NPC resource/combat modifiers. No existing behavioral assertion was removed. Isolated fixtures were supplied their new effect-handler/alignment dependencies.

**Final validation:** 111 modules were run in isolated processes, reporting 1,394 cases. All 100 previously passing modules remain green, and the new 26-test module passes: **101 passing modules / 1,109 passing tests**. The same 10 baseline modules retain exactly their previous failure/error counts, with no newly failing module or added failure count. Results are recorded in [the remediation test artifact](equipment-reset-remediation-2026-10-28-tests.json). `git diff --check` passes. The 10 remaining discrepancy probes R06–R15 still reproduce, confirming that the later report groups remain open. No live-server deployment is claimed. Previously spawned NPC equipment will receive the reset fixes on respawn; a restart/re-entry establishes light counts for already-loaded characters. Existing base armor becomes effective through the derived calculation.

**Remaining in this group:** No further verified issue is open among R01–R05. R06–R09 and the related R15 were subsequently resolved in the stat/carrying pass below; R10–R12 were subsequently resolved in the entry/following pass below; R13–R14 were subsequently resolved in the accuracy/mobile pass below. The five descriptions below are the original evidence, not current behavior.

| Finding | Priority | Closely related change area |
| --- | --- | --- |
| R01 (resolved) | P1 | Armor contributions on equipment transitions |
| R02 (resolved) | P1 | Alignment eligibility on equipment transitions |
| R03 (resolved) | P1 | Light ownership on equipment and room transitions |
| R04 (resolved) | P1 | G-reset inventory ownership |
| R05 (resolved) | P1 | E-reset equipment affect application |

### R01 — Wearing armor does not apply its base armor values

Python: `src/game/Equipped.py:119–138,173–234`, `src/item/EffectHandler.py:305–316`, `src/combat/CombatHandler.py:1802–1812`. C: `handler.c:1525–1554,1602–1604,1642–1644`.

An armor item with positive value0–value3 is equipped, but neither the equip path nor the damage consumer applies those values. Python applies explicit affect records; ordinary base armor is a separate mechanism in C. The combat consumer reads the stored armor_class plus dexterity defense, without deriving equipped armor contributions. C subtracts apply_ac for all four damage categories, with body ×3, head/legs/about ×2 and the other supported slots ×1, reversing that on removal.

A production-method probe wore body armor with value0=10: piercing combat AC stayed 10 before and after. C reduces raw piercing AC by 30. The snapshot contains 327 armor prototypes. This affects ordinary armor protection, independently of the now-working APPLY_AC effects.

### R02 — Alignment-incompatible equipment can be worn

Python: `src/game/Equipped.py:173–234`; compensating kill-time path `src/combat/CombatHandler.py:685–705`. C: `handler.c:1588–1600`.

A good actor can wear ITEM_ANTI_GOOD equipment and retain its effects; the same omission applies to anti-evil and anti-neutral items. Neither the wear command guards nor the shared wear/equip path checks those flags. C zaps the actor and drops the incompatible item into the room before setting wear_loc or applying bonuses. The probe successfully equipped an anti-good ring on an alignment +800 actor. Python's later equipment check during group rewards only runs after a kill; it does not enforce the wear-time restriction.

### R03 — Equipped lights never illuminate or travel between rooms

Python: `src/game/Equipped.py:119–138,173–234`, `src/area/Room.py:142–179,275–291`, `src/player/Character.py:428–440`. C: `handler.c:1340–1344,1408–1411,1616–1620,1692–1696`.

Equipping an ITEM_LIGHT with nonzero fuel does not increment room.light. Adding/removing a character from a room also does not move that contribution. Room darkness actually reads room.light, so this is a visibility mechanic rather than a display issue. The light-expiry path can decrement the room counter, but no corresponding ordinary equip/entry increment exists.

The probe equipped a fueled lamp and walked north: both source and destination light counters stayed zero; C leaves one unit in the destination. A normally lit room therefore stays dark, affecting room/object/character visibility. Removal, movement, login and NPC equipment should be checked together when repairing the ownership lifecycle.

### R04 — Non-shop G resets equip inventory into the light slot and discard previous stock

Python: `src/area/AreaHandler.py:260–279`, `src/game/Equipped.py:119–125`. C: `db.c:1422–1451`.

The ordinary mobile-item reset branch interprets arg3 as a wear location for both G and E commands. Bundled G resets have arg3=0, so items intended for carried inventory are equipped in the light slot. Subsequent G resets overwrite that slot, removing the earlier item from all live ownership. C always puts the item in inventory and only calls equip_char when command == E. The shopkeeper branch already distinguishes E correctly.

Two G resets in the probe produced zero inventory entries, one surviving owned item and a potion in the light slot; C retains both carried objects. There are 534 G resets in the snapshot. This changes loot, NPC inventory and prototype population counts.

### R05 — E-reset equipment bypasses affect application

Python: `src/area/AreaHandler.py:249–257,273–279`, `src/game/Equipped.py:119–125`; normal wear comparison `src/game/Equipped.py:225–229`. C: `db.c:1448–1451`, `handler.c:1606–1617`.

Reset equipment invokes mob.equip_item, which only changes ownership and wear metadata. It never calls EffectHandler.apply_item_effects as ordinary player wear does. An E-reset HP ring with APPLY_HIT +25 occupied the intended slot but left a 100-HP mobile at max_hit=100 with no applied affects. C applies the modifier through equip_char. This includes shopkeeper E resets. It is distinct from R01: adding base armor alone will not apply resource, stat, hitroll or defense affects. The snapshot contains 1,519 E resets.

## Training, current stats and carrying

### Remediation status — R06–R09 resolved; related R15 resolved

**Implemented 2026-10-28:** CharacterApi now supplies a shared bounded current-stat calculation, race maximum lookup, permanent-stat calculation and corrected training maximum. Human/nonhuman prime-stat training bonuses are distinct from current-stat headroom, and the exact level > LEVEL_IMMORTAL exception is retained. Training compares permanent stats and increments the existing effective field by one, preserving every active modifier. Permanent stats are derived by subtracting applied effect modifiers from the saved effective total; no new persisted stat representation or migration was introduced.

Regeneration, advancement, melee/sneak calculations, dexterity armor defense, weapon-weight checks, learning and spell stat operations use the shared current-stat helper. This replaces duplicated code, including SpellApi's separate stat-cap formula and Fight's repeated attribute-existence fallbacks. The helper relies on actual model fields and uses the NPC/PC distinction for their different contracts, without adding chains of defensive instance-attribute checks.

The existing carry count/weight methods now live on AnimateEntity, shared by Character and Mobile. Limits derive from current stats, level, the existing wear-slot mapping and strength bonus table. Player immortal and NPC pet exceptions follow C; zero pet capacity is enforced rather than treated as unlimited. Get/give/steal and score use these methods. The two buy guards also call the shared limits, preserving their existing quantity/coin-weight policies. This directly resolves R15's missing Mobile capacity methods. Saved max_items/max_weight fields remain wire-compatible but no longer override the runtime calculation.

**Content delivery:** The updated buy command's two carrying predicates must deploy with the runtime. Collection-query verified the original fields and final predicates; collection-modify validated the guards-array dry run and write. The existing Windows atomic-replacement restriction again required the validated focused writer, with parsed-equality assertions and unrelated documents preserved. No other collection content was changed in this pass.

**Regression coverage:** `tests/test_training_stats_carry_parity.py` adds 19 tests: prime/race/level boundaries, positive/negative and overlapping spell/item modifiers, training through save/load/removal, numeric affect locations, bounded current stats without mutating stored totals, NPC/PC rules, spell/regen/combat/learning inputs, dynamic capacities and legacy cached fields, immortal/pet limits, buy/get checks, and real item transfers to ordinary mobiles versus pets. Existing isolated fixtures supply the new current-stat rule and enum dependencies; no behavioral assertions were removed.

**Final validation:** 112 modules were run in isolated processes, reporting 1,413 cases. All 101 previously passing modules remain green, plus the new 19-test module: **102 passing modules / 1,128 passing tests**. The same 10 baseline modules retain their previous failure/error counts; there is no newly failing module or added failure count. Results are recorded in [the stat/carrying test artifact](training-stat-carry-remediation-2026-10-28-tests.json). `git diff --check` passes, and the five remaining discrepancy probes R10–R14 still reproduce. Existing historically overtrained permanent stats are not reduced automatically; current-stat caps govern their runtime use. No live-server deployment is claimed.

**Remaining in this group:** None of R06–R09 remains open. R15 is also resolved by the shared carrying contract. R10–R12 were subsequently resolved below; R13–R14 were subsequently resolved in the accuracy/mobile pass below. The original descriptions below retain pre-remediation evidence.

| Finding | Priority | Closely related change area |
| --- | --- | --- |
| R06 (resolved) | P2 | Permanent training limits |
| R07 (resolved) | P1 | Permanent versus modified training state |
| R08 (resolved) | P1 | Effective current-stat consumers |
| R09 (resolved) | P2 | Current-stat and level-derived carrying limits |

### R06 — Prime-attribute training bonuses are omitted

Python: `src/api/CharacterApi.py:473–495`, `src/interp/commands/Movement.py:580–585`. C: `handler.c:754–769`, `act_move.c:1622–1626`.

get_max_train returns the race maximum without C's +3 human prime-stat bonus or +2 nonhuman prime-stat bonus, and without its final ceiling of 25. For a human whose class prime attribute is strength and racial maximum is 18, Python rejects training at 18; C allows training through 21. The production train-handler probe returned already_at_maximum and consumed no train at strength 18. SpellApi.current_stat separately adds current-stat headroom; that is not a substitute for the permanent training limit.

### R07 — Temporary stat affects let players train beyond their permanent limit

Python: `src/item/EffectHandler.py:57–86`, `src/interp/commands/Movement.py:580–591`. C: `handler.c:943–953`, `act_move.c:1622–1636`.

Python stores both permanent stats and temporary affect contributions in character_attributes. Train compares this modified total against the cap and increments it directly. C checks and increments perm_stat, keeping mod_stat separate. With permanent strength already at a non-prime racial cap of 18, the probe applied weaken -5, successfully trained strength, then removed weaken: the permanent result became 19. C rejects that training at permanent strength 18. Conversely, positive buffs can incorrectly prevent otherwise valid training. The model can stay data-driven, but training must distinguish permanent values from active modifiers.

### R08 — Gameplay consumers use uncapped modified stats instead of ROM current stats

Python: `src/player/Character.py:506–590`, `src/player/CharacterAdvancement.py:187–200`, `src/api/CharacterApi.py:168–179,413–454`, `src/combat/ArmorDefense.py:1–5`. C: `handler.c:730–750`; representative consumers `update.c:178–180,246–247,299–305`.

Affects directly change the stored attributes, and regeneration, advancement, sneak perception and combat bonuses read those totals. C get_curr_stat clamps to a minimum of 3 and a race/class/human-dependent maximum no higher than 25. Python's bonus-table lookup only clamps to 0–25, and formulas outside those tables read the raw total. SpellApi.current_stat implements the current-stat rule for some spell operations, but these consumers do not call it.

With raw dexterity 30, a sleeping level-20 PC received base movement regeneration 50 in the probe; C can give at most 45 from that formula. Lower-than-three stats and race-specific caps also differ. This is independent of R06: permanent training ceilings and effective current-stat ceilings are different C rules.

### R09 — Carry limits remain stored constants when stats or level change

Python: `src/player/Character.py:213–217`; enforcement `src/interp/commands/Object.py:554–570,1417–1424,1672–1679`. C: `handler.c:778–800`.

max_items/max_weight return the saved character_attributes fields. No stat/level/effect update recomputes them. C computes item capacity from MAX_WEAR + 2×current dexterity + level and weight capacity from the strength table plus 25×level, with immortal and pet exceptions. Raising dexterity by four, strength by four and level by one left Python's limits at the fixture's 10 items/100 weight; C's item cap alone rises by nine for the same within-cap changes. Get/give/steal enforce these stale values, and zero stored limits bypass checks entirely. This is a mechanics discrepancy; whether designers want configurable base allowances instead of C's exact formulas remains a product decision.

## Room entry and movement integration

### Remediation status — R10–R12 resolved

**Implemented 2026-10-29:** Room membership invokes an entry-effect callback after adding a new player/mobile and releasing its lock. Bootstrap wires the shared EffectUpdateHandler and registers callback cleanup with the existing runtime reset mechanism. Duplicate membership does not reroll infection. A plague-bearing entrant immediately exposes eligible occupants using the actual plague record, level minus one, APPLY_STR -5, randomized positive duration, disease saving throws and C's six-bit (1/64) spread roll. Orphan AFF_PLAGUE flags are cleared, and level-one plague does not spread. Periodic plague retains its separate four-bit (1/16) roll and resource drain/damage. Both paths share the spread primitive. State changes finish synchronously; only existing spell-owned notification delivery is scheduled on the live event loop. Empty-world initialization needs no player notification task.

The Movement command family now exposes physical travel that uses the existing eligibility/state helpers and follower recursion without interpreted posture guards. Generic mobile walking preserves its closed/no-mob/stay-area/indoor/outdoor prefilters, then calls physical travel instead of transferring membership directly. This enforces room visibility and owner-aware privacy and processes eligible followers. Mobile movement payloads are sent through the existing standard PlayerHandler emitter, retaining direction context, room views and entry reactions.

Flee preserves its six-attempt/daze/closed/no-mob prefilters and existing XP/combat consequences, but successful movement now uses the same engine. Leader and follower costs/waits apply once, nested direction payloads retain their context, and standing followers or eligible charmed sleepers move with their leader. Magical sleep, fighting/incapacitated postures, insufficient movement and aggressive-NPC law restrictions keep followers behind as appropriate. Shared visited tracking prevents cyclic follow chains. No collection content needed changing; plague notifications use the existing spell payload.

**Validation:** 113 existing/new modules were exercised in isolated processes, followed by focused rechecks after tightening charmed-follower standing to the postures supported by C. **103 modules / 1,152 tests pass**; 1,437 cases are reported overall. Every previously passing module remains green, and the same 10 baseline failing modules retain exactly their previous failure/error counts. [The validation artifact](entry-following-remediation-2026-10-29-tests.json) records the final module results. `tests/test_entry_and_following_parity.py` adds **24 regressions**, covering immediate/periodic plague rolls, saves, record identity, duration/modifier/resource effects, duplicate membership, existing infections, immortals, orphan flags, callback reset, PC/NPC/portal/admin entry, visibility/privacy, preserved wander prefilters, follower chains, waits/costs, charm/sleep/incapacity, law restrictions and mobile payload-emitter routing. The existing flee fixture was supplied its new movement collaborator without removing assertions. `git diff --check` passes. No live-server deployment or exhaustive state-space equivalence is claimed.

**Remaining in this group:** None of R10–R12 remains open. R13 and R14 were subsequently resolved below. Original descriptions and line anchors below retain historical evidence.

| Finding | Priority | Closely related change area |
| --- | --- | --- |
| R10 (resolved) | P2 | Entry-time plague propagation |
| R11 (resolved) | P2 | Generic mobile travel integration |
| R12 (resolved) | P2 | Flee follower integration |

### R10 — Movement does not perform entry-time plague spread

Python: `src/area/Room.py:142–179`, `src/interp/commands/Movement.py:61–149`; remaining periodic behavior `src/item/EffectUpdateHandler.py:64–118`. C: `handler.c:1412–1456`.

C char_to_room immediately checks a plague-bearing entrant and rolls saves plus a 1/64 infection chance for eligible occupants, using an affect one level below the entrant's plague, with APPLY_STR -5 and a randomized positive duration. Python room addition only updates membership, and no entry caller invokes that spread. The periodic tick implementation is present, but uses the separate tick schedule and 1/16 chance corresponding to update.c. It does not replace immediate entry exposure.

The probe moved a level-20 plagued actor into an occupied room with failed saves forced: no save was attempted and the occupant stayed unaffected. Walking, portals and spell relocation inherit the missing entry behavior. C also clears an orphan AFF_PLAGUE bit on entry; Python waits until its status tick to do that.

### R11 — Wandering mobiles bypass shared room visibility and privacy gates

Python: `src/api/MobileApi.py:695–740,828–835`, caller `src/mobile/MobileHandler.py:126–133`. C: `update.c:441–458` invoking `act_move.c:78–108`.

The mobile wander helper applies C's wandering prefilters (closed exit, NO_MOB, stay-area and indoor/outdoor restrictions), then directly transfers dictionary membership. C runs those prefilters and calls move_char, which additionally checks can_see_room and owner-aware privacy. The probe moved an ordinary NPC into an owned ROOM_IMP_ONLY destination; Python accepted it, while C rejects it at room visibility even before privacy. This path also skips normal follower processing. Applying the ordinary player command posture restrictions is not necessary; the missing checks belong to shared travel eligibility.

### R12 — Flee still leaves eligible standing followers behind

Python: `src/interp/commands/Fight.py:306–367`; ordinary follower path `src/interp/commands/Movement.py:122–145`. C: `fight.c:2832` invoking `act_move.c:203–232`.

The G28 fix correctly shares eligibility, cost and wait with movement, but successful flee still transfers only the fleeing actor. C calls move_char and therefore processes eligible standing followers, including pet/charm follower standing behavior and its existing restrictions. In the probe, the leader fled to the destination while its ordinary standing follower stayed in the original room. This is additional integration behavior beyond the gates/cost/wait scope of the original G28 finding, not a re-listing of the corrected formula.

## Combat accuracy and mobile stat construction

### Remediation status — R13–R15 resolved

R13 now applies the reference backstab THAC0 reduction, `10 * (100 - proficiency)`, without dividing it by 100. R14 now accumulates each applicable warrior/thief/cleric/mage stat modifier independently. The separate THAC0 class-priority branches remain unchanged. These fixes change four production lines and add no attribute-existence guards.

R15 was already resolved with R06–R09 through shared animate-entity carrying methods. Its real-mobile gift transfer and pet-capacity rejection regression was rerun successfully; no additional production change was needed.

**Validation:** **143 tests pass across 15 isolated focused modules**, including three new regressions covering both backstab attack identifiers at proficiency boundaries, all 16 class-flag combinations, and preserved THAC0 class priority. Existing combat, mobile construction, armor isolation, carrying, item-give and entry/following tests also pass. [Validation results](accuracy-mobile-remediation-2026-10-29-tests.json). `git diff --check` passes. This was a focused rerun; the preceding full-suite baseline failures were not rechecked in this pass.

**Remaining:** None of R01–R15 remains open. The descriptions below retain the original pre-remediation evidence.

### R13 — Backstab's THAC0 adjustment divides the C bonus by 100 (resolved)

Priority: **P2**. Python: `src/combat/CombatHandler.py:1796–1798`. C: `fight.c:472–474`.

For a backstab hit, Python subtracts 10×(100−backstab proficiency)//100 from THAC0. This local C checkout subtracts 10×(100−proficiency), without the division. The production-method probe at proficiency 50 reduced Python THAC0 by 5, compared with C's 500. After a successful backstab activation, Python consequently has a much lower chance of landing the hit against many armor classes. The C rule is unusually generous at low proficiency; no claim is made that it is good balance, but it is the actual reference behavior and no intentional exemption was found. Changing it requires choosing the desired rule, not assuming a remembered standard-ROM formula.

### R14 — Multi-class mobile act flags apply only the first stat bonus (resolved)

Priority: **P2**. Python: `src/mobile/MobileFactory.py:49–75`. C: `db.c:1607–1633`.

The C mobile-construction stat bonuses for ACT_WARRIOR/THIEF/CLERIC/MAGE are independent if branches. Python uses if/elif, dropping all later class bonuses when more than one flag is present. A level-10 medium warrior+cleric in the probe received strength/wisdom/dexterity 16/13/13; C produces 17/16/12. This is not merely hypothetical: 36 bundled mobile prototypes have multiple class bits, including vnums 9202, 3504, 9003, 9004 and 9006. Their stats affect combat and spell behavior. THAC0's separate class selection intentionally uses else-if in C; that branch should not be changed as part of this finding.

## Object transfers

### R15 — Giving an object to an NPC raises before capacity checks finish (resolved with R06–R09)

Priority: **P1**. Python: `src/interp/commands/Object.py:1397–1424`, `src/player/Character.py:207–217`, `src/mobile/Mobile.py:12–61`, `src/game/AnimateEntity.py:17–49,150–203`. C: `act_obj.c:799–805,817–821`; NPC capacity rules `handler.c:778–800`.

The item-give preparation path unconditionally calls victim.max_items(), then carry_count(), max_weight() and carry_weight(). These methods exist on Character but not Mobile or its AnimateEntity base. Giving an otherwise valid carried object to a visible ordinary mobile therefore raises AttributeError before guards or transfer complete. The production preparation probe raises `'Mobile' object has no attribute 'max_items'`. C handles NPC capacity normally and gives permitted objects, while rejecting pet capacity according to its own rule. This is separate from R09's stale player limits: adding dynamic formulas only to Character would leave NPC transfers broken. Money giving uses a different branch and is not included in this finding.

## Validation and review coverage

The inventory covers 214 Python files and 17 collection snapshots: 221 commands, 38 skills, 97 spells, 986 mobiles, 1,266 item prototypes, 3,127 rooms and 5,196 resets. Command execution routes were inventoried from the actual collection lambdas. Collections were inspected through collection-query before focused programmatic extraction; whole JSON snapshots were not dumped into context.

Fresh detailed traces covered equipment/affect ownership and combat AC, item visibility/darkness/light, stats/regen/advancement/training/carrying, ordinary movement/flee/followers/portals, spell relocation/targeting/saving/dispels and representative spell effects, mobile construction/special invocation/wandering, area reset branches, periodic living/item/effect updates, damage/accuracy/escape/death/reward consumers, interpreter/alias/social/nested dispatch, and persistence boundaries. Existing tests additionally exercised combat skills, object transactions/consumption/magic items, elemental exposure, spells, communication/group behavior, and gameplay-affecting administrator operations. Existing reports served as history, not evidence for copying findings; the paths above were checked against current code and local C.

At review time all **15 production-method discrepancy probes** completed successfully in [the reproducible probe script](fresh-gameplay-parity-2026-10-28-probes.py). They use real models, actual runtime enums and representative command documents, with narrow collaborators and deterministic rolls; their assertions describe the current mismatches, not fixed behavior. The script uses the repository test fixtures and must be run from this checkout. After remediation it skips all R01–R15 probes, whose corrected outcomes are exercised by the regression suites; the original probe bodies remain as historical evidence. No C executable differential harness or live content-service/server session was run.

The existing suite was run in **110 isolated module processes** to avoid cross-test module-stub contamination, using `.venv/Scripts/python.exe` and an approved unrestricted environment for Windows async tests. **100 modules pass, containing 1,083 tests.** Across all processes unittest reports 1,368 test cases, including an import-failure placeholder. Ten modules fail; full summaries are in [the test-result artifact](fresh-gameplay-parity-2026-10-28-tests.json):

- combat_group_rewards: missing points in advancement fixtures (11 errors).
- combat_handler_aggression: stub InterpApi lacks command_payload (one error).
- combat_survival: emitter fixture lacks connection_manager (one error).
- command_authorization: symbolic IM-level assertion (one failure).
- final_combat_parity: flee fixture's stub MovementUtil lacks DIR_NAME (one error). This is an additional fixture incompatibility exposed by the recent shared-movement change; it was not listed among the earlier nine failing modules.
- mobile_pulse: fixture mobile lacks add_item (one error).
- object_fountain_commands: stub parser lacks parse_object_arguments (six errors).
- object_theft_parity and player_handler_cast_prompt: stub messaging package import failures (one each).
- spell_affect_payload_messages: three existing energy-drain assertions, with advancement fixtures missing required attributes.

These failures were retained and reported, not repaired during the review or promoted automatically into gameplay findings. Passing tests do not establish C parity; the new probes demonstrate discrepancies outside existing coverage.

This is a repository-wide survey, not an exhaustive proof for every command, spell, social, mobile special, content document or state combination. Detailed equivalence of every data-authored lambda, legacy area conversion, every admin mutation, reconnect/possession sequence and live service transformation remains unverified. Intentional networking/storage/designer architecture, prose and music delivery were not assessed as gameplay bugs. The 15 findings are concrete verified mechanics differences within the traced scope; additional unexamined discrepancies may remain.

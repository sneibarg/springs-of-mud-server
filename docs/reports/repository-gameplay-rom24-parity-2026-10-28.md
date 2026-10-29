# Repository gameplay parity review — 2026-10-28

Reference: `C:/Users/scott/PycharmProjects/PyRom/Rom24/src`. Python: current working tree of `C:/Users/scott/PycharmProjects/springs-of-mud-server`.

The initial review identified **26 gameplay discrepancies**. The three remediation passes resolve **all original findings G01–G26**. Two further related discrepancies, G27–G28, were traced during remediation and are also resolved by the fourth pass. No recorded finding remains open. Existing collection-modify changes are unrelated and were left intact. Prior parity reports were used as navigation, then relevant current paths were checked; previously resolved findings were not copied into the initial review.

Only mechanics are findings: eligibility, success probability, visibility, movement, resources, effects, spawning and world state. Architecture, designer-authored rules, networking protocols, storage format, administrative monitoring, prose and message formatting are excluded. No explicit design exemption was located for the findings below. A verified difference is not proof that the designers want it changed; product intent remains unconfirmed where no decision is documented.

Paths below are relative to the respective checkout. Finding line anchors describe the original reviewed working tree, before the remediation edits. P1 denotes broad or exploitable gameplay impact; P2 denotes narrower mechanics.

## Shared skills, effects and perception

### Remediation groups and current status

| Group | Original findings | Status | Related work still open |
| --- | --- | --- | --- |
| Effect application | G01–G02 | Resolved | G26 resolved in the third pass: permanent innate mobile buffs are applied |
| Skill proficiency | G03–G04 | Resolved | No further issue established in this subgroup |
| Stealth and perception | G05–G08 | Resolved | G27 resolved in the fourth pass; G22 was resolved in the second pass |

**Implemented 2026-10-28:** Resource affects now add/subtract HP, mana and movement maxima, including worn items and save/load/removal. Defense affects update the correct immunity/resistance/vulnerability field and restore overlapping effects when one source is removed. Missing/zero/ineligible skills return zero; PC and NPC command proficiency uses the shared daze/drunkenness adjustment and final clamp.

Sneak/hide use a reusable self-skill activation primitive. The skill documents own preparation, improvement multiplier, flags and sneak's level-scaled affect; Python supplies the reusable operation. Sneak strips its prior affect before checking residual innate flags, rolls with C's strict endpoint, creates a timed affect on success and uses the existing expiration/message ownership path. Hide clears its prior flag before the roll. Character visibility implements sneak's proficiency/stat/level calculation and hide rejection, retaining detection, fighting and trust exceptions. Outdoor darkness follows the existing weather state. Room views filter people and items and apply the same position/blindness/darkness gates for explicit look and automatic arrival views; dark looks retain eligible character perception and holy light bypasses blindness/darkness. The explicit autoexit call was corrected to the room handler's one-character contract.

**Validation:** 25 new regressions in `tests/test_shared_gameplay_parity.py` pass, including a real bundled ring (6601), effect persistence/overlap, the real damage immunity resolver, skill access, roll endpoints, NPC proficiency, timed sneak expiration, character/object vision, wizinvis, night sectors/light, explicit look and automatic room views. The final focused run passes **214 tests across 16 modules**. A broader isolated run exercised 106 modules; with the subsequent successful devtools retry, **97 modules pass**. The nine previously documented failing modules remain baseline limitations. A new test-import dependency in the theft fixture was adjusted; its 18 tests again reach the same one pre-existing emitter import error instead of failing at module import. No live server/content-service deployment was performed.

**Content delivery:** The runtime and updated `sneak`/`hide` skill documents and `look` command guards must be delivered together. Collection changes were dry-run through collection-modify and verified through collection-query. Windows denied atomic replacement of the Commands snapshot; its tool-validated output was applied in place only after asserting parsed equality with the requested documents, preserving all other content and formatting. Existing active player resource totals are not retroactively recalculated; new applications/removals follow the corrected rule.

The descriptions G01–G08 below retain the original evidence for reference; their status is resolved as described above.

### G01 — P1: Equipment/resource affects do not change maximum resources

Python `src/item/EffectHandler.py:51–103,135–168,268–280`; C `handler.c:960–962` and equipment affect application at `handler.c:614–616`.

`_apply_stat_modifier` handles stats, combat bonuses, AC and saves, but never APPLY_HIT, APPLY_MANA or APPLY_MOVE. Equipping an item with those affects records the effects without changing the corresponding maxima. These are stored scalar fields, with no getter supplying the omitted contribution. Current content includes item 6601 with `A,13,4` (APPLY_HIT +4). A direct production-code probe applying APPLY_HIT +25 left max HP at 30; C would make it 55. Item-based survivability and resource capacity are therefore wrong.

### G02 — P2: Immunity/resistance/vulnerability affects are inert

Python `src/item/EffectHandler.py:135–168,268–280`; damage consumer `src/combat/CombatHandler.py:1837–1854`; C `handler.c:904–938,1034–1041`.

For an affect whose destination is TO_IMMUNE, TO_RESIST or TO_VULN, Python stores the record but never updates status_flags.imm/res/vuln. Damage and saving throws read those flags, rather than derive them from records. A direct TO_IMMUNE bit-16 application left immunity at zero. Innate/template flags still work; the discrepancy concerns affect-driven additions/removals. No matching immunity item was established in the bundled snapshot, so this is a verified runtime capability discrepancy rather than a claim about a particular shipped item.

### G03 — P1: Unlearned skills are treated as 1% learned

Python `src/player/Character.py:196–200`, `src/api/SkillApi.py:26–28`, `src/api/FightApi.py:309–316`; C `handler.c:369–374`.

`skill_level` returns `learned or 1`, including for missing and explicitly zero learned entries. FightApi's class-level access check then accepts the positive rating. An otherwise level-eligible player can attempt an unlearned combat skill; modifiers may raise its success chance above 1%. C returns zero and rejects skill-dependent commands. Directly querying the real SkillApi for an absent bash entry returned 1.

### G04 — P1: Player command-skill rolls ignore daze and drunkenness

Python `src/api/SkillApi.py:26–28,73–87`; callers `src/api/FightApi.py:72`, `src/interp/commands/Fight.py:203,280`; C `handler.c:443–454`.

The penalty/clamp block is indented inside the NPC branch. PCs return raw learned proficiency, so command mechanics using SkillApi ignore both penalties. With 90% learned, positive daze and drunk=20, the production API returned 90; C produces 54 after 2/3 and 9/10 scaling. Other paths that use SkillUtil.adjusted_percent already apply penalties; this finding is specific to SkillApi callers.

### G05 — P1: Sneak and hide always succeed; sneak has no expiry

Python `src/interp/commands/Movement.py:355–363`; commands `sneak` and `hide` in SOMDB.Commands; C `act_move.c:1335–1384`.

Both handlers unconditionally set their raw flags, without proficiency rolls or improvement. Sneak creates no affect/duration. Their command documents only delegate to these handlers and add no such checks. A character with no sneak entry acquired AFF_SNEAK in a direct check. C rolls against get_skill; successful sneak creates a level-duration affect and can expire. This changes access, reliability and duration independently of the perception defects below.

### G06 — P1: Shared character visibility ignores hide and sneak concealment

Python `src/api/CharacterApi.py:413–450`; C `handler.c:2468–2489`.

The sneak branch is a `pass`, the subsequent chance is always zero, and there is no AFF_HIDE rejection. A nonfighting hidden target is returned as visible to an ordinary observer without detect hidden; this was reproduced with production objects. C rejects hidden targets and applies its proficiency/stat/level roll to sneaking targets. Visible-target lookup, targeting and aggression that rely on this helper inherit the discrepancy.

### G07 — P1: Room views reveal occupants and objects without visibility checks

Python `src/area/Room.py:287–301,311–321`, `src/area/RoomHandler.py:72–91`, `src/player/PlayerHandler.py:1032–1044`; C `act_info.c:127–176,494–516,1004–1052`.

Room listings enumerate people and item descriptions without calling can_see/can_see_obj; the character-line formatter adds labels but does not filter. A non-cloaked invisible/wizinvis occupant or invisible object is listed to an observer unable to see it. Automatic views on movement also print the room directly, bypassing do_look's guard path. This is disclosure of otherwise concealed world state, not a cosmetic formatting difference. Fixing G06 alone does not fix these independent callers.

### G08 — P1: Ordinary outdoor rooms never become dark at night

Python `src/area/Room.py:270–284`; C `handler.c:2356–2374`.

After light, ROOM_DARK and indoor/city checks, Python always returns false. C also tests SUN_SET/SUN_DARK. An unlit field without ROOM_DARK remains visible through the ordinary darkness-dependent object/character checks throughout the night. Direct inspection/probing confirms the helper has no weather dependency; correcting the weather scheduler does not correct this rule.

## Movement, escape and locks

### Remediation groups and current status

| Group | Original findings | Status | Related work still open |
| --- | --- | --- | --- |
| Directional travel access and cost | G09, G11–G15 | Resolved | G28: flee duplicates movement validation and cost/wait handling |
| Recall | G10 | Resolved | No further recall discrepancy established in this pass |
| Locks and picking | G16–G17 | Resolved | No further discrepancy established in the reviewed lock state transitions |
| Portals and followers | G18–G20 | Resolved | No further discrepancy established in the reviewed portal branches |
| Posture and concealment cleanup | G21–G22 | Resolved | G27: interpreter input still does not break hiding |

**Implemented 2026-10-28:** Ordinary movement now reads AFF_FLYING, honors ANGEL closed-door and immortal boat exemptions, permits room owners through the privacy gate, and enforces destination visibility, charm/master and class-guild restrictions. Guild rooms come from GameData's existing class definitions. Successful PC movement applies a one-pulse minimum wait and preserves zero movement cost after haste/flight division. Following respects room visibility and aggressive-NPC law restrictions; magical sleep prevents forced follower standing.

Recall now uses the configured temple vnum, rejects curse and non-pet NPCs, preserves the local C combat roll's unusual strict failure condition, charges 25/50 XP for connected/link-dead combat success, applies failure recovery and skill improvement, halves movement on success and dispatches pet recall. Pet recursion is guarded against malformed cycles. Portal travel checks visible object targeting and destination access, uses ANGEL/IMPLEMENTOR trust at the separate boundaries, filters random rooms with the local C privacy/safe/law rules and preserves the strict 4% buggy-gate endpoint. Followers consume shared portal charges in order; exhausted portals are removed once, and GOWITH moves the portal before follower attempts, matching C's lookup order.

Lock actions share a normalized exit/container/portal state and content-owned guards/messages. They use the correct container value2 versus portal value4 key reference, enforce door/closeable/no-close/no-lock/pickproof state, mirror reverse exits and permit appropriate immortal door-pick exemptions. Pick recovery and nearby awake NPC checks precede the PC proficiency roll, which uses C's inclusive success boundary; skill improvement occurs only on the corresponding roll failure or completed success. Furniture posture commands resolve visible room furniture, honor allowed posture bits/capacity/current users, maintain `on` for regeneration, prevent waking magical sleep and clear furniture relationships on departure or object removal. `visible` strips invisibility, mass invisibility and sneak records before clearing raw concealment flags.

**Validation:** All **35 new regressions** in `tests/test_movement_rules_parity.py` pass. They exercise the updated collection guards and production movement/lock/posture paths, including reverse exits, follower charge exhaustion, privacy trust boundaries, shared furniture state and real recall XP changes. The final focused check passes **208 tests across 16 fully passing modules**. Another 163 tests were exercised in the existing theft, combat-survival and spell suites; their five previously recorded failures/errors remain (one theft emitter import, one combat emitter fixture, three energy-drain assertions). New dependency requirements were supplied to isolated test fixtures without removing behavioral assertions. The broader run exercised 108 test modules, including a concurrently present mobile-resource suite; its extra movement-fixture failures were corrected and rechecked. No clean full-suite or live-server validation is claimed.

**Content delivery:** Updated direction/lock/posture command documents and runtime must be delivered together. All 26 collection operations were dry-run through collection-modify and verified through collection-query. As in the first pass, the validated CLI output was written in place with parsed-equality assertions because this Windows Commands file could not be atomically replaced; unrelated documents were preserved. The separate concurrent `Mobile` resource-field change was left intact and is not part of this remediation.

**Remaining in these groups:** G27 (hide-breaking input) and G28 (flee's independent movement rules) were subsequently resolved in the fourth pass below. World-population/mobile-construction G23–G26 were subsequently resolved in the third pass below. The descriptions G09–G22 below retain the original evidence; their original findings are resolved by this pass, without asserting exhaustive equivalence of every movement-related command.

### G09 — P1: Magical/innate flight is not recognized by ordinary movement

Python `src/api/CharacterApi.py:402–403`, `src/api/MovementApi.py:93–114`; spell `fly` affectData; C `act_move.c:155–199,222–224`.

is_flying tests a POS_FLYING posture rather than AFF_FLYING. The fly spell and flight equipment grant the affect bit without changing posture. A standing actor with AFF_FLYING returned false in the production helper. Such actors are denied air/water movement and miss the flight movement discount; C permits them. The flee path already reads AFF_FLYING, so ordinary travel and fleeing also disagree with each other.

### G10 — P1: Recall bypasses curse and combat escape costs/failure

Python `src/interp/commands/Movement.py:372–422`; `recall` command document; automatic caller `src/combat/CombatEscapeHandler.py:43–75`; C `act_move.c:1402–1484`.

After checking ROOM_NO_RECALL, Python moves to the temple, stops combat and halves movement. It omits AFF_CURSE, the combat recall roll, failure wait and success XP charge; the command document has no compensating guards. A cursed fighting character moved to the temple with zero XP change in a direct production-handler check. C rejects curse; in combat it can fail with wait=4, or succeeds with a 25/50 XP cost depending on connection. The automatic link-dead recall path inherits this mismatch. The handler also omits C's non-pet NPC rejection and recalling a co-located pet.

### G11 — P1: Directional movement omits room-visibility, charm and class-guild gates

Python `src/interp/commands/Movement.py:55–128`, `src/api/MovementApi.py:64–126`; all six direction command guards; C `act_move.c:101–150`.

Neither the state builder nor directional guards check CharacterApi.can_see_room, a charmed follower leaving its co-located master, or entry to another class's guild. The reusable room-visibility helper exists but is not called here; `_can_see_room` used for followers just checks non-null. Consequently PCs can traverse exits into otherwise restricted clan/newbie/god/class rooms and charmed actors can leave their master. Following also omits C's aggressive-NPC/ROOM_LAW rejection at `act_move.c:270–280`, allowing a master to bring those followers into law rooms.

### G12 — P2: Room owners cannot enter their own private rooms

Python `src/api/MovementApi.py:120,185–187`, `src/area/Room.py:245–260`; C `act_move.c:126–130`, `handler.c:2378–2384`.

Room.is_private correctly returns true for an owned room, but the movement guard rejects it unconditionally. C exempts is_room_owner from this directional-entry privacy check. A named owner arriving from an adjacent room is therefore blocked by Python.

### G13 — P2: Trusted closed-door and immortal boat exemptions are missing

Python `src/api/MovementApi.py:85–90,105–110`; C `act_move.c:111–115,175–178`.

A trusted ANGEL without pass door is denied movement through a closed exit, where C allows it. Separately, a non-flying immortal without a boat is denied a water-noswim exit, where C sets found=true. These differences are independent of G09 and remain after flight is corrected.

### G14 — P2: Successful directional movement imposes no wait

Python `src/interp/commands/Movement.py:75–76,128–131`, `src/player/PlayerHandler.py:1046–1047`; C `act_move.c:237–238`.

Python deducts movement but never raises pulse_wait; the player wrapper only emits the payload and no direction document supplies a wait. C applies WAIT_STATE(ch,1) before movement. Buffered directional commands can therefore execute without the one-pulse pacing/cooldown that controls ROM travel speed.

### G15 — P2: Zero-cost hasted/flying movement is forced to cost one

Python `src/api/MovementApi.py:337–343`; C `act_move.c:213–238`.

For two inside sectors, average cost is 1, halved to 0 by haste/flight. C retains zero, whereas Python returns max(1,move). A hasted actor at zero movement is incorrectly blocked; one who can move loses a point. The direct helper returned 1 for the flight-discount case. This is separate from recognizing flight itself.

### G16 — P1: Door picking bypasses proficiency, guarding NPCs and recovery

Python `src/interp/commands/Movement.py:212–213`, `pick` command guards; C `act_move.c:740–775,836–863`.

Once the door exists, is closed/locked and is not pickproof, the handler simply unlocks it. No roll, skill-access check, nearby high-level awake NPC check, wait or skill improvement exists in its complete guard/call path. A novice can therefore pick an ordinary locked door reliably next to a guard who would prevent the attempt in C. C also rejects doors without a key definition for mortals; Python's pick guards omit that check.

### G17 — P1: Container/portal opening and unlocking are routed only to exits

Python `src/interp/commands/Movement.py:151–152,201–213`, `src/api/MovementApi.py:129–150`; command documents `open`, `unlock`, `pick`; C `act_move.c:355–407,608–697,776–833`.

These commands resolve door_state and operate on exits, so a valid closed chest or locked portal is reported as no door. close/lock have a container path, but portals are not containers there. A player can close/lock a chest and then cannot reopen/unlock it using the corresponding commands. C explicitly implements object/container/portal branches. This is functional access to stored items and travel, not missing messages.

### G18 — P1: Random portals use unfiltered destinations

Python `src/interp/commands/Movement.py:883–904,1006–1007`; C `act_enter.c:41–60,103–117`.

`_random_room` chooses any room other than the origin; it does not apply ROM's PRIVATE/SOLITARY/SAFE/LAW or room-visibility filters. Final portal checks only reject occupied/owned privacy and the local `_can_see_room` returns true for any room. A random gate can enter a restricted clan/newbie/gods room or a SAFE/empty PRIVATE room which ROM's random-room helper excludes. For currently occupied private rooms the unfiltered selection can instead fail, whereas C rerolls eligible destinations. Fixed-destination portals also miss can_see_room. The buggy-portal probability is separately 5% (`<=5`) versus C's 4% (`<5`).

### G19 — P2: Followers do not traverse portals with their master

Python `src/interp/commands/Movement.py:424–490`; C `act_enter.c:165–201`.

do_enter moves only the actor, optionally moves the portal and decrements/expires it. It never processes the master's followers. With a usable multi-charge or unlimited portal, standing/charmed followers remain behind. C processes followers after charging the master's transit and before final portal extraction, respecting exhaustion and law checks.

### G20 — P2: Any immortal bypasses portal-room privacy

Python `src/interp/commands/Movement.py:915–919`; C `act_enter.c:113–117`.

`_room_private_for` returns false for every immortal. C permits a private destination only for IMPLEMENTOR trust. An ordinary immortal can therefore enter an occupied private/solitary or owned room through a portal despite C's rejection. This is distinct from G12's directional owner rule.

### G21 — P2: Posture commands ignore furniture and its regeneration state

Python `src/interp/commands/Movement.py:242–320`; regeneration consumer `src/game/AnimateEntity.py:277–285`; C `act_move.c:871–1330` and `update.c:202,270,317`.

stand/rest/sit/sleep do not resolve their furniture argument, check capacity/allowed posture bits, or set/clear `character.on`. Resting or sleeping on a valid bed cannot establish the furniture regeneration multiplier; standing from an existing furniture relationship does not implement C's detach/reposition rules. The regeneration primitive exists, but ordinary posture commands do not maintain the state it consumes.

### G22 — P2: Visible clears concealment bits but leaves spell effects active

Python `src/interp/commands/Movement.py:365–370`; spell duplicate checks `src/api/SpellApi.py:504–512`; C `act_move.c:1388–1397`.

The handler clears AFF_HIDE/INVISIBLE/SNEAK without stripping invisibility, mass invisibility or sneak affect records. A direct check left an active `spell.invis` record after visible. C removes those records too. The retained records continue to block ID-based recasting or participate in affect restoration/expiry despite the player's visible action.

## World population and mobile construction

### Remediation groups and current status

| Group | Original findings | Status | Related work still open |
| --- | --- | --- | --- |
| Reset population and floor items | G23–G25 | Resolved | No further issue established in this subgroup |
| Innate mobile affects | G26 | Resolved | No further issue established in this subgroup |

**Implemented 2026-10-28:** M resets compare their arg2 cap with matching live mobiles across all registered rooms, retaining the independent arg4 destination-room cap. O resets reject an existing floor item of the same prototype, allow unrelated objects and other distinct O resets, and set each newly created floor object's cost to zero without changing its prototype. Occupied-area suppression remains in effect; nested items do not count as floor duplicates, matching C's direct object-list check.

Mobile creation now applies permanent sanctuary, haste and protection effects through the shared EffectHandler. The records have the existing spell handler identities, mobile level, duration -1, affect bits and C's modifiers, including haste's level thresholds at 18/25/32. Mobile now has a zero-default saving_throw field so protection modifiers affect saving throws and reverse correctly on removal. Spawned instances and clones retain independent effects without applying modifiers twice. The previously present movement-resource fields were preserved.

**Validation:** **77 tests across 10 isolated modules pass**, including seven new regressions in `tests/test_world_population_parity.py`. Coverage includes cross-area global caps, independent room caps, successful spawning, multiple floor prototypes and duplicate suppression, zero cost without prototype mutation, nested items, all haste threshold boundaries, permanent spell identities, effect removal and sibling/clone isolation. Existing occupancy, armor, special binding, runtime factory, mobile resource, shared gameplay, effect ownership, exit reset and API boundary tests pass. The protection/sanctuary/haste identities were verified through collection-query; no collection changes were needed. No live server or full-suite validation is claimed.

**Remaining:** No additional discrepancy was established within these two groups. All original findings G01–G26 are resolved; separately recorded G27 and G28 were subsequently resolved in the fourth pass below. Existing live mobiles are not retroactively rebuilt; the corrected innate effects apply to newly constructed mobiles.

The descriptions G23–G26 below retain the original evidence; their status is resolved as described above.

### G23 — P2: Mobile reset population caps count only the destination area

Python `src/area/AreaHandler.py:123–139,299–314`; C `db.c:1253–1257`.

The M reset arg2 is compared with an area-filtered live count. C compares the prototype's global count. If the only capped NPC wanders to another area, Python spawns another on reset even when the global limit is already reached. The per-room arg4 limit is a separate check and does not compensate for this case.

### G24 — P1: Any floor item suppresses unrelated object resets

Python `src/area/AreaHandler.py:103–119`; C `db.c:1310–1315`.

O resets reject `len(room.contents)>0` rather than counting the reset object's prototype in the room. Leave a different item in an empty area's target room and the intended object never respawns. Multiple different O resets into one room also suppress each other after the first successful spawn. C permits each distinct object prototype while rejecting duplicates of that prototype.

### G25 — P2: Floor-reset items retain their prototype sale value

Python `src/area/AreaHandler.py:117–119`, `src/item/ItemFactory.py:35–61`; C `db.c:1319–1322`.

C explicitly sets an O-reset object's cost to zero after creation. Python clones the prototype, including cost, without this assignment. A floor-spawned item with a nonzero prototype cost therefore has a different sell/value/reward input from the C-spawned object. This also changes scavenger ranking and cost-dependent actions; it is not a JSON-format difference.

### G26 — P1: Innately affected mobiles never receive their permanent buff affects

Python `src/mobile/MobileFactory.py:86–98,177–178`; C `db.c:1643–1690`.

`_apply_affected_by` creates sanctuary/haste/protection Effect values into local variables but never attaches/applies them. Innate haste lacks its +1..4 dexterity modifier; protection lacks -1 saves. Sanctuary/haste/protection also lack their spell identity, level and permanent affect records used for dispelling. The raw flags remain, so some visible/flag-based benefits still work; this is not a claim that sanctuary's damage reduction vanishes. C calls affect_to_char for each constructed affect.

## Additional related work found during remediation

### Fourth remediation pass — G27–G28 resolved

**Implemented 2026-10-28:** Normal and nested interpretation share a nonempty-input preparation step that removes only AFF_HIDE before alias substitution, command/social lookup and freeze/authorization checks. Empty input leaves hide intact, other concealment bits are preserved, and executing hide can set the bit again after preparation. This also covers force/order-style nested interpreted input through PlayerHandler.

Flee now uses MovementApi's existing movement state, visibility/charm/guild predicates, room-owner exemption, flight/boat rules and movement-cost calculation. The duplicate minimum-one cost formula and separate subset of travel checks were removed. Ordinary directional movement and flee share the same resource-charge/one-pulse-wait operation, preserving longer waits; successful flee clears furniture state. Flee retains its own six-attempt direction loop, daze rolls, closed-exit rejection even for trusted/pass-door actors, NPC ROOM_NO_MOB check, experience handling and combat stop. Command posture guards remain separate from travel eligibility so fighting actors can flee.

**Validation:** **145 tests across eight fully passing modules**, including all **18 new regressions** in `tests/test_input_and_flee_parity.py`. Another 35 tests in combat-survival and command-authorization were exercised; 33 pass and their two previously documented baseline problems remain (message-bus connection-manager fixture error and symbolic IM-level assertion). Fixtures for executor/social interpretation now supply affect enums; the combat-survival fixture supplies the shared movement collaborator rather than the removed flee-only cost helper. No behavioral assertions were removed. Direction/flee collection guards were inspected through collection-query; no content changes were needed. `git diff --check` passes. No full-suite or live-server validation is claimed.

**Remaining:** All recorded findings G01–G28 are resolved. This closes the report's findings, not an exhaustive parity proof for all interpreter or escape behavior. The original G27–G28 descriptions below retain historical evidence.

### G27 — P2: Command input does not break hiding

Python `src/interp/InterpHandler.py:72–96`, `src/interp/CommandExecutor.py:30–39`; C `interp.c:378–386`.

C clears AFF_HIDE for every nonempty interpreted input, before freeze, command lookup and dispatch. Python's interpreter/executor never performs that transition. After a successful hide, a player can issue ordinary commands, move or attempt unknown commands while retaining the hide bit. This is independent of the now-correct activation roll and visibility helper. It was established while tracing the first section but is outside the original G01–G08 fixes; it was resolved in the fourth pass after G22 was resolved in the second pass. No claim that the whole stealth command lifecycle is now equivalent to C is made.

### G28 — P2: Flee bypasses the shared movement gates, zero-cost travel and wait

Python `src/interp/commands/Fight.py:329–346,746–781`; C `fight.c:2818–2831`, which invokes `move_char`, and `act_move.c:101–150,213–238`.

Flee's `_flee_destination` checks its own subset of movement eligibility and directly changes room membership rather than invoking the ordinary movement path. Unlike C's `move_char` call, it does not enforce room visibility, charm/master or other-class guild access. It rejects all private rooms without the owner exemption, forces hasted/flying inside-sector cost to one and does not impose movement's one-pulse wait. For example, a hasted PC with zero movement can now walk between inside rooms but still cannot flee through the same route; a charmed actor may flee away from a co-located master where the C movement call rejects departure. This was verified while tracing the second group and was resolved in the fourth pass described above. The independent C prefilter that rejects closed exits during flee should be retained, even for actors who could ordinarily pass a closed door.

## Original review coverage and validation

The original repository-wide inventory covered runtime modules, 221 command documents, the collection inventory, prior review resolutions and the test inventory. Detailed traces covered interpreter authorization/dispatch, skill access/proficiency, character/object visibility, equipment/effects, movement/portals/escape/posture, area resets, mobile construction/updates, spell execution primitives and representative spell documents, damage/safety/rewards/death/automatic escape, progression/regeneration, weather/tick ordering and persistence boundaries. Command documents were inspected through collection-query, not inferred absent from Python names.

Existing combat, spell, object, learning, weather and administrator regression suites were also exercised. The broad run invoked **105 test modules in separate Python processes**, to avoid test-global module stubs contaminating unrelated modules. Initially **91 modules passed**; 1,092 test cases were reported, including import-error placeholders. Seven import-failing modules were retried with `src` explicitly on sys.path: five more modules passed (57 real tests), while fountain fixtures and the spell suite still failed. Thus **96 modules passed; nine modules still had failures/errors**. These counts are baseline checks, not a proof of ROM equivalence.

Remaining failing modules: combat_group_rewards (fixture attributes), combat_handler_aggression (stub API), combat_survival (stub message bus), command_authorization (assertion), mobile_pulse (fixture mobile), object_fountain_commands (stub parser), object_theft_parity and player_handler_cast_prompt (stub import paths), spell_affect_payload_messages (three energy-drain assertions). Energy-drain fixtures replace attributes with SimpleNamespace values lacking fields now required by real advancement; do not count these failed assertions as demonstrated runtime parity bugs. No test/source changes were made to repair baseline fixtures during this review.

Synchronous checks using production methods and existing runtime fixtures reproduced G01, G02, G03, G04, G05, G06, G08, G09, G10, G15, G22, G24, G25 and G26. Reset checks isolated registry/factory collaborators; mobile/character effect and perception checks used the real methods and loaded runtime enums. All six direction documents were checked for compensating access predicates. Other findings are verified by tracing the full relevant current branch/guard/caller path against C. No live gameplay server or C executable differential run was performed. The sandbox initially stalled asynchronous tests; the completed broad run used an approved unrestricted environment. The ordinary Python launcher was avoided in favor of `.venv/Scripts/python.exe`.

This is a repository-wide survey with detailed findings, not an exhaustive proof over every command, every spell, all 5,196 resets, all 3,127 rooms, every administrator operation or all persistence/reconnect sequences. Old-format area conversion, content equivalence to every C area file, exhaustive social/NPC reactions and all state combinations remain coverage limits. Music delivery, login/idle product policy and legacy anti-cheat punishment were not promoted to gameplay findings without resolving their intended scope. No claim of complete parity follows from a passing existing test or from a domain without a new finding here.

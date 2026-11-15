# Bundled mobile specials compared with ROM24

November 15, 2026

Reviewed the Springs working tree at base revision `3e2fdc570139d3aa69b7d1e031a4e4fa4eaca8ed`, including local runtime and collection changes, against the local `PyRom/Rom24` sources and area files. The reviewed bundle contains **413 records and 24 special names**. Its **411 mobile assignments match ROM24 exactly by mobile vnum and special name**. The other two records define generic scavenging and wandering. All 411 assignments resolve to their bundled mobile in the correct area, with unique assignment keys and document IDs. Four assigned prototypes have no bundled `M` reset, a separate question from binding integrity.

The highest-impact defects are the empty scripts on **53 bound mobiles**, the combat-handler selection that breaks combat spells across **288 bound mobiles**, and the mayor's route getting stuck at the park entrance and missing both evening gate closures. The table below covers every bundled family. Counts describe distinct prototype assignments, regardless of how many copies are spawned.

## Verified findings

### F01 · Eight assigned families have no executable script

The records load and bind by area and vnum, and spawning copies the binding. Every record in the following families has an empty `specialFunction` array. A real dispatch of one record per family returned false with zero actions. Generic mobile processing can still run on those mobiles.

| Family | Bound mobiles | ROM24 behavior missing from the bundle |
| --- | ---: | --- |
| `spec_breath_any` | 19 | A fighting mobile draws three bits and delegates to fire, lightning, gas, acid or frost with weights 1/2/1/1/3. The selected special applies its own target rules. The prism dragon `2016` and dragon hatchling `2200` have the empty script. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:410) · [Bundle](../../resources/collections/SOMDB.Specials.json#L479) |
| `spec_breath_acid` | 11 | A fighting mobile checks characters fighting it with a one-in-eight roll per eligible candidate and breathes acid at the first success. The Great Black Dragon `2222` has the empty script. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:380) · [Bundle](../../resources/collections/SOMDB.Specials.json#L887) |
| `spec_cast_adept` | 6 | An awake adept can select a visible PC below level 11 and cast a support spell. Seven of the 16 spell outcomes cast. Cure disease still returns false to the mobile update after casting. Apollo, Athena, the Midgaard healer, and both school adepts are affected. Trainer recognition by special name still works independently. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:475) · [Bundle](../../resources/collections/SOMDB.Specials.json#L2218) · [Trainer lookup](../../src/api/MobileApi.py#L911) |
| `spec_cast_judge` | 7 | A fighting judge selects an opponent with a one-in-four roll per character fighting it, then casts high explosive. Affected bindings include Judge Beddows `8011` and the Guardian of Hell `10401`. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:591) · [Bundle](../../resources/collections/SOMDB.Specials.json#L439) |
| `spec_executioner` | 1 | An awake, unfighting Hassan `3011` finds the first visible killer or thief, yells the accusation, and attacks. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:721) · [Bundle](../../resources/collections/SOMDB.Specials.json#L4930) |
| `spec_ogre_member` | 4 | An awake, idle, uncalmed and uncharmed ogre chooses a safe-to-attack rival troll using the level check and reservoir sampling. A patrolman prevents the attack. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:185) · [Bundle](../../resources/collections/SOMDB.Specials.json#L1138) |
| `spec_troll_member` | 4 | The corresponding troll-to-ogre rivalry. The level, safety and patrolman checks also apply. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:126) · [Bundle](../../resources/collections/SOMDB.Specials.json#L1101) |
| `spec_patrolman` | 1 | The idle patrolman `2106` samples ongoing fights, chooses the higher-level participant from the selected fight (the opponent wins ties), rejects a fellow patrolman target, uses an equipped whistle if present, and attacks. The bundled whistle and neck equip resets exist. No intervention or whistle action runs from the empty record. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:244) · [Bundled binding](../../resources/collections/SOMDB.Specials.json#L1244) |

Restore the scripts through content. Preserve each procedure's eligibility, probability and pulse return separately from its messages. Fix F02 and F03 before relying on the restored breath or judge scripts. Existing primitives cover parts of the adept, gang and patrolman paths. Their availability alone does not exercise those paths. [Service binding](../../src/mobile/MobileService.py#L39) · [Spawn copy](../../src/mobile/MobileFactory.py#L140) · [Empty-script branch](../../src/mobile/MobileHandler.py#L197)

### F02 · Production mobile spell dispatch selects the wrong combat collaborator

`MobileHandler` has both `fight_handler`, which implements combat, and `fight_commands`, the `Fight` command interpreter. When a special creates a `SpellContext` with the mobile handler, `SpellApi._fight_handler` picks `fight_commands` first. The interpreter has no `_check_immunity`, `damage`, or `is_safe_spell`. As a result, bound spells fail when they reach those calls. NPC spell errors are logged during lambda execution, and players can see a bite or a cast announcement even when the underlying spell never resolves.

**Reproduction.** Used the bundled scripts, real spell executor and both production collaborator types, with deterministic target and spell selection. Forced every distinct choice in the mage, cleric and undead tables (30 family/spell pairs). The eligible paths each failed on a missing combat method. The four active breath families also failed with stocked HP and an eligible opponent. The poison bite announced the bite but failed its poison save lookup. The mayor's mage delegation hit the same failure. Energy drain lowered caster alignment from +500 to +450 before failing the save and still reported the special as performed. Gas reaches floor poison exposure before the missing room-safety call and can therefore get partway through its effect.

The wiring affects 99 mage, 73 cleric, 39 undead, 49 active breath and 27 poison bindings, plus the mayor's combat branch. The existing unswitched-mobile test casts armor with a reduced handler fixture, so it can pass without reaching this failure. Resolve the real combat handler first. Test a damaging spell, a saved debuff and an area breath with both collaborators present. Verify script failure cannot be mistaken for a completed cast.

[ROM24 mage dispatch](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:620) · [ROM24 poison bite](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:981) · [Mobile collaborators](../../src/mobile/MobileHandler.py#L55) · [Context creation](../../src/api/MobileApi.py#L153) · [Resolver ordering](../../src/api/SpellApi.py#L1732) · [Save lookup](../../src/api/SpellApi.py#L227) · [Existing armor test](../../tests/test_cast_learned_contract.py#L150)

### F03 · Targeted dragon breaths skip the target roll and can aim at the wrong opponent

ROM24 fire, frost, lightning and acid use `dragon()`. Only candidates whose `fighting` points to the dragon are eligible, and each gets a three-bit roll from which only zero succeeds. No successful roll means no breath. The bundled fire, frost and lightning scripts call `cast_dragon_breath`, which goes directly to `actor.fighting`. This makes a single eligible opponent a guaranteed target whenever the helper runs, compared with 1/8 in ROM24. Fire and frost may also use a different target for the full-damage branch of their cones.

**Reproduction.** A lightning dragon targeted its non-reciprocating current opponent with zero target rolls, despite a different character fighting the dragon and a forced nonzero roll. The probe instrumented the spell invocation boundary to bypass F02. Gas correctly skips the dragon target roll because ROM24 runs its separate room-wide procedure. Use shared opponent selection with three-bit rolls for the targeted breaths, including acid when restored.

[ROM24 dragon helper and dispatch](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:380) · [Bundled lightning](../../resources/collections/SOMDB.Specials.json#L1469) · [Python target helper](../../src/api/MobileApi.py#L145) · [Fire/frost primary versus collateral](../../src/api/SpellApi.py#L918)

### F04 · The mayor's scripted route uses wander restrictions and misses both evening gates

ROM24 gives the mayor ordinary `move_char` for digits in his route. The generic wander path separately checks `ROOM_NO_MOB`, stay-area and indoor/outdoor constraints. Springs' mayor uses the same helper as wandering, so he refuses to enter the Park Entrance, vnum `3105`, despite an open south exit from `3102`. The room has `ROOM_NO_MOB` in both source and bundled data. The script still advances, interpreting later directions from the wrong room.

**Reproduction.** Replayed both bundled paths starting in the Mayor's Office `3138`, with the bundled Midgaard exits and door resets. The first divergent move was `3102` south to `3105`. The opening instructions ran at `3041` and `3040`, the closing instructions both ran at `3150`, and the mayor ended at `3119`. A control using ordinary shared travel for route digits reached `3041` and `3040` for both opening and closing, then returned to `3138`. Restore ordinary travel for timed routes and keep the wander filters on generic wandering.

[ROM24 scripted movement](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:908) · [ROM24 Park Entrance flags](C:/Users/scott/PycharmProjects/PyRom/Rom24/area/midgaard.are:4347) · [ROM24 wander restrictions](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:440) · [Bundle route](../../resources/collections/SOMDB.Specials.json#L5396) · [Route dispatch](../../src/api/MobileApi.py#L443) · [Wander prefilters](../../src/api/MobileApi.py#L696)

### F05 · Mayor wake, sleep and combat decisions diverge from ROM24

**Resolved in the runtime and bundled content.** The mayor's timed script initializes a due route before delegating to the mage special. While fighting, it returns that special's result and preserves the route instruction, including when the mage skips its cast. The route resumes at the saved instruction on the first eligible pulse after combat. Wake and sleep now set live posture through the shared character API. Ordinary route steps still deliver movement, door and speech output and leave the generic phase available. After a scripted move, generic processing uses the destination room.

The updated mayor record needs to be loaded and bound by the running server. F02 still tracks the mage spell's combat collaborator, and F04 tracks the route's movement restrictions.

The focused tests cover both schedule hours, successful and skipped combat delegation, route resumption, live wake and sleep posture, gate notices and generic processing after movement. All 33 focused tests passed. The async fixtures ran in memory to avoid the Windows sandbox event-loop initialization hang. [Timed script](../../src/api/MobileApi.py#L417) · [Updated bundled record](../../resources/collections/SOMDB.Specials.json#L5399) · [Mobile pulse](../../src/mobile/MobileHandler.py#L153) · [Regression tests](../../tests/test_rom24_report_fixes.py#L98)

**Original findings**

- `W` and `S` write the top-level position. The active posture accessor reads `character_attributes.position` first. Starting from live sleeping posture, a reproduced `W` advanced the route and announced waking while the mayor stayed effectively asleep. The same stale state occurs in reverse on `S`.
- In ROM24 a due route is initialized before combat handling. If the mayor has an opponent, the special then returns the mage result immediately. The authored sequence delegates and can continue to a route step. With a failed target roll, the reproduced mayor advanced the route while fighting. A mage guard that finishes the shared context can instead skip due-route initialization. Route progression should depend on combat state independently of cast success.
- The ordinary ROM24 route branch returns false even after moving, speaking or using a gate. The Python route marks successful steps performed and skips the generic phase. A reproduced wake returned true. The bundled mayor is a sentinel, so this last difference is lower impact for him than the posture and route mistakes.

The previously reported scheduler-order mismatch is resolved in the reviewed working tree. Both runtimes run mobile and violence pulses before the time tick, and both try a bound special before shop replenishment. [ROM24 mayor](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:897) · [ROM24 pulse order](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:1081) · [Python route state](../../src/api/MobileApi.py#L417) · [Combat delegation](../../src/api/MobileApi.py#L110) · [Live posture accessor](../../src/game/AnimateEntity.py#L88) · [Python pulse order](../../src/game/UpdateHandler.py#L61)

### F06 · A guard can attack twice and starts combat before the first swing

Once ROM24 finds a visible criminal, the guard yells, calls `multi_hit` once and returns. Only a pulse without a criminal considers the lowest-alignment fighter below 300. The bundled guard runs both branches. In a room with a visible thief and an unrelated eligible fighter, the bundled dispatch called `multi_hit` for the thief and then for the fighter on the same pulse.

The Python helper also sets both combat links before `multi_hit`. ROM24 resolves the first swing with the target's existing posture, then damage establishes combat links for a target above stunned. With a zero-HP stunned thief, the production Python combat transition set the target's position to fighting and linked it to the guard before the first swing. This can remove the first-swing posture modifiers, strip sleep early, and introduce a combat link for an incapacitated target. Finish the criminal branch after its single attempt and let damage own combat initiation.

[ROM24 guard return](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:826) · [ROM24 hit posture](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:488) · [ROM24 combat linkage](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:722) · [Bundled guard](../../resources/collections/SOMDB.Specials.json#L2254) · [Python attack helper](../../src/api/MobileApi.py#L267) · [Combat posture mutation](../../src/combat/CombatHandler.py#L1032)

### F07 · Guard accusations ignore yell recipient rules

ROM24 clears the guard's own `COMM_NOSHOUT`, then uses the area yell command. It reaches playing listeners in the area who have quiet off and meet the `act` posture threshold, and it resolves the guard's name for each listener. The script's `yell` helper queues raw area text. The mobile handler iterates player room occupants without checking quiet mode or posture. Connected switched bodies also bypass this room-character list. A quiet listener and a sleeping listener both received the accusation in a real message-bus probe. Sender attribution was absent. Reuse existing yell recipient and visibility rules while honoring the special's sender override.

[ROM24 guard yell](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:826) · [ROM24 yell recipients](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:974) · [ROM24 act posture](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2473) · [Python special yell](../../src/api/MobileApi.py#L257) · [Python delivery](../../src/mobile/MobileHandler.py#L397) · [Existing command rules](../../src/interp/commands/Communications.py#L375)

### F08 · Janitors take protected items and leave eligible drink containers and trash

ROM24 takes the first takeable and lootable floor object that is a drink container, trash, or costs less than 10. The Python selector supplies `can_loot=True` for every object. It also exposes the raw type, so the script's `ITEM_DRINK_CON` and `ITEM_TRASH` checks miss the bundled `drink` and `trash` values. These kinds then qualify only by price. In a probe the janitor left a takeable drink worth 100, then took cheap trash owned by a present unrelated player with looting disabled. Bundled item `3601`, a takeable brandy bottle worth 100, has the same type and price. Use the existing ownership and canonical item-kind helpers, as generic scavenging already does for ownership.

[ROM24 janitor](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:850) · [Bundled predicate](../../resources/collections/SOMDB.Specials.json#L2714) · [Python selectors](../../src/api/MobileApi.py#L361) · [Ownership policy](../../src/api/ItemApi.py#L46) · [Type normalization](../../src/item/Item.py#L270)

### F09 · Saved spells can lose their notices and yield the rest of the pulse

ROM24 mage, cleric, undead and breath wrappers return true once they invoke the selected spell, even if the spell saves or has no effect. The mobile spell adapter drops every queued spell payload and returns false when `SpellContext.performed` is false. This conflates a normal resisted invocation, a missing spell, and failures before any effects. The poison bite has its own true return, but still loses the discarded spell output. With the save forced true and the combat collaborator supplied directly to isolate F02, the bundled poison special sent its bite notice and discarded the poison spell's resisted messages. A normal resisted weighted cast can also fall through into shop and generic processing where ROM24 has claimed the pulse. Separate spell resolution status, notices, and consumption of the NPC's pulse. Treat the adept cure-disease return in F01 as its own case.

[ROM24 caster return](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:659) · [ROM24 poison save notice](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:3850) · [Python performed gates](../../src/api/MobileApi.py#L153) · [Python poison bite](../../src/api/MobileApi.py#L479) · [Pulse fallback](../../src/mobile/MobileHandler.py#L148)

### F10 · NPC teleport skips the destination room display

ROM24 teleport moves the player and invokes automatic look. The Python spell creates a destination-view payload. The mobile payload dispatcher recognizes a command context and a handful of direct message channels, but has no route for a standalone destination view. After bypassing F02 in the fixture, the live player moved to the destination under the bundled mage spell, received the cast and teleport notices, and got no room display or destination prompt from that payload. Route special-origin spell payloads through the existing room-view handling.

[ROM24 teleport](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4352) · [Python view producer](../../src/api/SpellApi.py#L1378) · [Mobile payload dispatcher](../../src/mobile/MobileHandler.py#L367) · [Standard view handler](../../src/player/PlayerHandler.py#L973)

### F11 · Level-one pickpockets can take money

ROM24 caps the random percentage at integer `level / 2`, yielding zero at level one. Python floors the cap at one. With a level-one thief, a dispatch that passed the eligibility roll and missed discovery took one gold and one silver from a player holding 100 of each. Bundled level-one thieves include the spoiled brat `6608` and smurfs `101` and `102`. The percentage, separate rolls, and level-squared caps otherwise match for positive deployed levels above one when given the same target and draws.

[ROM24 coin formula](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:1029) · [Python coin formula](../../src/api/MobileApi.py#L515) · [Bundled thief script](../../resources/collections/SOMDB.Specials.json#L22)

### F12 · A resting nasty thief can rip a coin purse

ROM24 uses the ambush branch whenever current posture differs from `POS_FIGHTING`. With no eligible ambush victim it returns false, even if a fighting pointer persists. The authored ambush step returns false in that state, then Python's second step checks the pointer alone. With live resting posture, an existing opponent outside the ambush level window and a forced purse outcome, the bundled script took 10 of 100 gold. Gate the in-combat action on fighting posture before choosing the purse, flee or idle outcome.

[ROM24 posture split](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:323) · [Bundled nasty script](../../resources/collections/SOMDB.Specials.json#L5421) · [Python combat branch](../../src/api/MobileApi.py#L556)

### F13 · First match can select a different corpse, item or opponent

ROM24 prepends occupants and contents to the room lists. The Python room stores occupants and contents in insertion order, and `people()` visits PCs before mobiles. With two NPC corpses added in order, the bundled fido devoured the older corpse and left the newer one. ROM24 would visit the newer corpse first and spill its contents. The same ordering difference can change who gets the first combat-caster, guard, or pickpocket check, which item a janitor takes, and which equally valuable item a generic scavenger chooses. This is a traversal difference, independent of the otherwise matching single-corpse spill behavior.

[ROM24 character insertion](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1378) · [ROM24 object insertion](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1775) · [ROM24 fido](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:758) · [Python room order](../../src/area/Room.py#L224) · [Python fido](../../src/api/MobileApi.py#L390)

### F14 · Reloading specials leaves cached and copied scripts stale

This is a Python content-delivery defect relevant to deploying the bundle fixes. After successful registry reload, the mobile handler's warmed name library still uses its old lambda lists. Bound mobiles also hold copies taken at prototype load and spawn. With the wander entry cached, a mocked service response passed through the real reload path and replaced its script in the registry, while dispatch still returned the old script from the cache. A fresh mobile prototype load sees the current assignment. Decide whether reload applies to active mobiles and make that contract explicit in the runtime. A fresh world load binds the replacement records.

[Special reload](../../src/area/SpecialService.py#L20) · [Registry publication](../../src/server/FetchAndRegisterMixin.py#L62) · [Cached library](../../src/mobile/MobileHandler.py#L421) · [Prototype assignment](../../src/mobile/MobileService.py#L39) · [Spawn copy](../../src/mobile/MobileFactory.py#L140)

### F15 · Undead casters roll harm too often

ROM24 gives harm one explicit outcome (6) and seven default outcomes (9–15). The bundle assigns weights of two and seven to the two harm entries. At level 21 and above the result is 9/17 harm instead of 8/16, and each other spell becomes less likely. At levels 18–19 harm is 9/15 instead of 8/14, and at level 20 it is 9/16 instead of 8/15. Enumerating all 17 draws in the bundled level-21 script produced nine harms and one of each of the other eight spells. Change the explicit harm weight from two to one in the 39 matching records and verify the distributions at levels 18, 20 and 21.

[ROM24 undead table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:672) · [Bundled undead table](../../resources/collections/SOMDB.Specials.json#L135) · [Weighted selector](../../src/api/MobileApi.py#L222)

## Coverage of the nonempty scripts

| Family | Records | Compared behavior |
| --- | ---: | --- |
| `spec_cast_mage` | 99 | Fighting posture and per-opponent two-bit draw match. Eligible spell weights match ROM24's rejection sampling after filtering by level. F02, F09, F10 and F13. |
| `spec_cast_cleric` | 73 | Same target selection and effective table weights, including four dispel-magic outcomes and three harm outcomes at the relevant levels. F02, F09 and F13. |
| `spec_cast_undead` | 39 | Fighting gate and per-opponent two-bit draw match. Harm is overweight. F02, F09, F10, F13 and F15. |
| `spec_breath_fire` | 21 | Live fighting gate matches. Primary and collateral saves, exposure and HP damage use the ROM24 fire branch structure after target selection. F02 and F03. |
| `spec_breath_frost` | 10 | Live fighting gate matches. Frost uses the same primary/collateral structure with cold exposure. F02 and F03. |
| `spec_breath_lightning` | 7 | Live fighting gate matches. Single-target save and shock exposure are present. F02 and F03. |
| `spec_breath_gas` | 11 | No individual target roll. Shared base damage, room exposure first, area safety and the ROM24 NPC exception are present. Gas excludes an NPC if either combat pointer connects it to the NPC caster, which differs from the fire/frost reciprocal-target condition. F02. |
| `spec_guard` | 24 | Awake and idle gates, visible criminal scan and the fallback alignment cutoff of 300 are present. F06, F07 and F13. |
| `spec_poison` | 27 | Current fighting posture, opponent and inclusive percent threshold `2 × level` match. C invokes the poison spell even if saved. F02 and F09. |
| `spec_thief` | 36 | Standing gate, mortal level limit, five-bit roll, visibility, awake discovery, independent money rolls and caps compared. F11 and F13. |
| `spec_fido` | 6 | Awake gate, NPC corpse recognition, removal and item spill verified. F13 changes which corpse is used. |
| `spec_janitor` | 3 | Awake and takeable checks work. F08 and F13 affect the selected item. |
| `spec_mayor` | 1 | Hours 6 and 20 and both route strings match. Door actions operate through real movement commands. F05 is resolved in the runtime and bundled record. F02 and F04 still affect combat casting and route movement. |
| `spec_nasty` | 1 | Level window of +1 through +9, backstab-to-murder fallback, and the quarter purse, quarter flee and half idle weights match for the appropriate posture. F12 and F13. |
| `spec_scavenge` | 1 generic | Standing gate, scavenger flag, six-bit chance, loot eligibility and best cost above one match. F13 affects ties. |
| `spec_wander` | 1 generic | Present in the current bundle. Standing gate, sentinel exclusion, 3-bit attempt, 5-bit direction and exit/room restrictions tested. The previous missing-definition and stale-standing findings are resolved on the bundled path. |

[ROM24 caster tables](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:540) · [ROM24 breath effects](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4496) · [Runtime weights](../../src/api/MobileApi.py#L222) · [Generic ROM24 pulse](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:374) · [Bundled wander regression](../../tests/test_entry_and_following_parity.py#L314)

The C caster tables redraw when the roll selects a spell above the mobile's level. The Python selector filters by level and then draws once. For equivalent valid weights this gives the same conditional spell distribution and uses fewer random draws on pulses where C rejects a roll.

## Validation and limits

- Parsed the ROM area `#SPECIALS` sections and compared the assignment multiset with the bundled snapshot. Parsed all 413 records through the Python special model, built all 986 mobile prototypes through `MobileService`, and checked that 411 bound and 358 received nonempty scripts. All 1,002 shipped lambda entries compiled and their direct context helper signatures bound. All 23 distinct spell names referenced by the active specials resolved from bundled content.
- Used the production dispatchers with fixed rolls and in-memory rooms, combat and message boundaries. Probes isolated downstream behavior from F02 by supplying a working collaborator directly where needed. For the mayor route, loaded the bundled Midgaard rooms and applied bundled door resets. The control changed only which travel path handled the scripted directions.
- **206 focused existing tests passed** across isolated runs. The total includes 144 spell and elemental tests, 34 movement and gameplay parity tests, and 28 mobile, binding, emission, independent-cast, fido and mayor checks. The last group used an in-memory coroutine runner to avoid the Windows sandbox event-loop socket initialization hang. A combined harness produced three visibility-fixture failures that cleared when the mayor/fido module ran in isolation.
- The review compared all 24 families at the assignment, script and primary gameplay decision levels. Live service contents, executable-C differential sessions, and every branch of the downstream spells and combat engine remain unverified. Generic cast announcements and some direct notices also differ in presentation and recipient rendering. The findings above cover reproducible gameplay and delivery failures without requiring changes to the game's wording.

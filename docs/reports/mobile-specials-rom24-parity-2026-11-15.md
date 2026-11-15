# Bundled mobile specials compared with ROM24

November 15, 2026

Reviewed the Springs working tree at base revision `3e2fdc570139d3aa69b7d1e031a4e4fa4eaca8ed`, including local runtime and collection changes, against the local `PyRom/Rom24` sources and area files. The reviewed bundle contains **413 records and 24 special names**. Its **411 mobile assignments match ROM24 exactly by mobile vnum and special name**. The other two records define generic scavenging and wandering. All 411 assignments resolve to their bundled mobile in the correct area, with unique assignment keys and document IDs. Four assigned prototypes have no bundled `M` reset, a separate question from binding integrity.

The original review found empty scripts on **53 bound mobiles**, a combat-handler selection that broke combat spells across **288 bound mobiles**, and a route error that caused the mayor to miss both evening gate closures. All three are resolved in the working tree. Counts describe distinct prototype assignments, regardless of how many copies are spawned.

## Verified findings

### F01 · Eight assigned families have no executable script

**Resolved in the runtime and bundled content.** All 53 assignments now have executable `specialFunction` scripts. The Special records hold the spell tables, level limits, group and whistle identifiers, and dialogue. Shared runtime operations select targets, cast, deliver notices, and execute combat. Targeted breaths use the reciprocal-opponent roll, and the adept's cure disease branch casts while leaving the mobile pulse available. Hassan uses the shared yell command and attacks the first visible criminal. Gang members honor the patrolman veto, and the patrolman can intervene with or without his equipped whistle.

Verified the new scripts through the mobile dispatcher and bundled spells. Seven new tests cover all eight families, including all eight mixed-breath outcomes, missed target rolls, adept pulse returns, executioner yell recipients, both rival gangs, and the patrolman's response with and without a whistle. Another 234 focused tests passed across mobile, spell, combat, and collection modules. Async tests ran on a socketless event loop in the Windows sandbox. Once the server is running the matching runtime, import the updated Special records into its content service and reload them through the path described in F14. [Restored scripts](../../resources/collections/SOMDB.Specials.json) · [Dispatch regressions](../../tests/test_restored_mobile_specials.py)

**Original finding.** These records loaded and bound by area and vnum, and spawning copied an empty `specialFunction` array. A dispatch of one record per family returned false with zero actions. Generic mobile processing could still run on those mobiles.

| Family | Bound mobiles | ROM24 behavior missing from the bundle |
| --- | ---: | --- |
| `spec_breath_any` | 19 | A fighting mobile draws three bits and delegates to fire, lightning, gas, acid or frost with weights 1/2/1/1/3. The selected special applies its own target rules. The prism dragon `2016` and dragon hatchling `2200` have the empty script. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:410) · [Bundle](../../resources/collections/SOMDB.Specials.json#L483) |
| `spec_breath_acid` | 11 | A fighting mobile checks characters fighting it with a one-in-eight roll per eligible candidate and breathes acid at the first success. The Great Black Dragon `2222` has the empty script. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:380) · [Bundle](../../resources/collections/SOMDB.Specials.json#L921) |
| `spec_cast_adept` | 6 | An awake adept can select a visible PC below level 11 and cast a support spell. Seven of the 16 spell outcomes cast. Cure disease still returns false to the mobile update after casting. Apollo, Athena, the Midgaard healer, and both school adepts are affected. Trainer recognition by special name still works independently. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:475) · [Bundle](../../resources/collections/SOMDB.Specials.json#L2364) · [Trainer lookup](../../src/api/MobileApi.py#L917) |
| `spec_cast_judge` | 7 | A fighting judge selects an opponent with a one-in-four roll per character fighting it, then casts high explosive. Affected bindings include Judge Beddows `8011` and the Guardian of Hell `10401`. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:591) · [Bundle](../../resources/collections/SOMDB.Specials.json#L439) |
| `spec_executioner` | 1 | An awake, unfighting Hassan `3011` finds the first visible killer or thief, yells the accusation, and attacks. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:721) · [Bundle](../../resources/collections/SOMDB.Specials.json#L5143) |
| `spec_ogre_member` | 4 | An awake, idle, uncalmed and uncharmed ogre chooses a safe-to-attack rival troll using the level check and reservoir sampling. A patrolman prevents the attack. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:185) · [Bundle](../../resources/collections/SOMDB.Specials.json#L1187) |
| `spec_troll_member` | 4 | The corresponding troll-to-ogre rivalry. The level, safety and patrolman checks also apply. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:126) · [Bundle](../../resources/collections/SOMDB.Specials.json#L1138) |
| `spec_patrolman` | 1 | The idle patrolman `2106` samples ongoing fights, chooses the higher-level participant from the selected fight (the opponent wins ties), rejects a fellow patrolman target, uses an equipped whistle if present, and attacks. The bundled whistle and neck equip resets exist. No intervention or whistle action runs from the empty record. [ROM24](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:244) · [Bundled binding](../../resources/collections/SOMDB.Specials.json#L1320) |

### F02 · Production mobile spell dispatch selects the wrong combat collaborator

**Resolved as a dependency of F01.** `SpellApi` now resolves the combat handler before the command interpreter. With both collaborators present, the restored high explosive and breath scripts reach spell saves, damage, and room safety as applicable. [Resolver](../../src/api/SpellApi.py#L1732) · [Spell regressions](../../tests/test_restored_mobile_specials.py)

**Original finding.** `MobileHandler` has both `fight_handler`, which implements combat, and `fight_commands`, the `Fight` command interpreter. When a special created a `SpellContext` with the mobile handler, `SpellApi._fight_handler` picked `fight_commands` first. The interpreter has no `_check_immunity`, `damage`, or `is_safe_spell`. Bound spells failed when they reached those calls. NPC spell errors appeared in the log, and players could see a bite or cast announcement with no spell effect.

**Reproduction.** Used the bundled scripts, real spell executor and both production collaborator types, with deterministic target and spell selection. Forced every distinct choice in the mage, cleric and undead tables (30 family/spell pairs). The eligible paths each failed on a missing combat method. The four active breath families also failed with stocked HP and an eligible opponent. The poison bite announced the bite but failed its poison save lookup. The mayor's mage delegation hit the same failure. Energy drain lowered caster alignment from +500 to +450 before failing the save and still reported the special as performed. Gas reaches floor poison exposure before the missing room-safety call and can therefore get partway through its effect.

The original wiring affected 99 mage, 73 cleric, 39 undead, 49 active breath and 27 poison bindings, plus the mayor's combat branch. The existing unswitched-mobile test casts armor with a reduced handler fixture, so it could pass without reaching this failure.

[ROM24 mage dispatch](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:620) · [ROM24 poison bite](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:981) · [Mobile collaborators](../../src/mobile/MobileHandler.py#L56) · [Context creation](../../src/api/MobileApi.py#L153) · [Resolver ordering](../../src/api/SpellApi.py#L1732) · [Save lookup](../../src/api/SpellApi.py#L227) · [Existing armor test](../../tests/test_cast_learned_contract.py#L150)

### F03 · Targeted dragon breaths skip the target roll and can aim at the wrong opponent

**Resolved as a dependency of F01.** The shared targeted breath primitive now rolls three bits per character fighting the caster and skips the cast when no roll succeeds. The mixed-breath script delegates to this primitive through the bound fire, frost, lightning and acid specials. Gas keeps its separate room-wide path. [Targeted breath](../../src/api/MobileApi.py#L154) · [Breath regressions](../../tests/test_restored_mobile_specials.py)

**Original finding.** ROM24 fire, frost, lightning and acid use `dragon()`. Only candidates whose `fighting` points to the dragon are eligible, and each gets a three-bit roll from which only zero succeeds. No successful roll means no breath. The bundled fire, frost and lightning scripts called `cast_dragon_breath`, which went directly to `actor.fighting`. This made a single eligible opponent a guaranteed target whenever the helper ran, compared with 1/8 in ROM24. Fire and frost could also use a different target for the full-damage branch of their cones.

**Reproduction.** A lightning dragon targeted its non-reciprocating current opponent with zero target rolls, despite a different character fighting the dragon and a forced nonzero roll. The probe instrumented the spell invocation boundary to bypass F02. Gas skipped the dragon target roll because it runs a separate room-wide procedure in ROM24.

[ROM24 dragon helper and dispatch](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:380) · [Bundled lightning](../../resources/collections/SOMDB.Specials.json#L1597) · [Python target helper](../../src/api/MobileApi.py#L154) · [Fire/frost primary versus collateral](../../src/api/SpellApi.py#L918)

### F04 · The mayor's scripted route uses wander restrictions and misses both evening gates

**Resolved in the runtime.** Timed route steps now call ordinary shared travel. Random wandering applies its closed-door, `ROOM_NO_MOB`, stay-area, and indoor/outdoor checks before calling that same travel path. Scripted steps still follow the ordinary travel rules for doors and access, and a blocked step advances the route cursor as in ROM24.

Replayed both schedules against the bundled Midgaard rooms and door resets. The mayor passed through Park Entrance `3105`, opened and closed both sides of the gates at `3041` and `3040`, and returned to sleep in his office `3138` after each route. The replay failed for both schedules when route digits used the old wandering path. All 79 focused tests passed, including checks for wandering restrictions and a scripted step blocked by a closed door. [Route replay and closed-door regression](../../tests/test_rom24_report_fixes.py#L156)

**Original finding.** The wander filter rejected the open south exit from `3102` to the Park Entrance, which has `ROOM_NO_MOB` in both ROM24 and the bundle. The route advanced in the wrong room. Both evening gate instructions ran at `3150`, and the mayor ended at `3119`.

[ROM24 scripted movement](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:908) · [ROM24 Park Entrance flags](C:/Users/scott/PycharmProjects/PyRom/Rom24/area/midgaard.are:4347) · [ROM24 wander restrictions](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:440) · [Bundle route](../../resources/collections/SOMDB.Specials.json#L5622) · [Route dispatch](../../src/api/MobileApi.py#L449) · [Wander prefilters](../../src/api/MobileApi.py#L704)

### F05 · Mayor wake, sleep and combat decisions diverge from ROM24

**Resolved in the runtime and bundled content.** The mayor's timed script initializes a due route before delegating to the mage special. While fighting, it returns that special's result and preserves the route instruction, including when the mage skips its cast. The route resumes at the saved instruction on the first eligible pulse after combat. Wake and sleep now set live posture through the shared character API. Ordinary route steps still deliver movement, door and speech output and leave the generic phase available. After a scripted move, generic processing uses the destination room.

The updated mayor record needs to be loaded and bound by the running server.

The focused tests cover both schedule hours, successful and skipped combat delegation, route resumption, live wake and sleep posture, gate notices and generic processing after movement. All 33 focused tests passed. The async fixtures ran in memory to avoid the Windows sandbox event-loop initialization hang. [Timed script](../../src/api/MobileApi.py#L417) · [Updated bundled record](../../resources/collections/SOMDB.Specials.json#L5625) · [Mobile pulse](../../src/mobile/MobileHandler.py#L166) · [Regression tests](../../tests/test_rom24_report_fixes.py#L98)

**Original findings**

- `W` and `S` write the top-level position. The active posture accessor reads `character_attributes.position` first. Starting from live sleeping posture, a reproduced `W` advanced the route and announced waking while the mayor stayed effectively asleep. The same stale state occurs in reverse on `S`.
- In ROM24 a due route is initialized before combat handling. If the mayor has an opponent, the special then returns the mage result immediately. The authored sequence delegates and can continue to a route step. With a failed target roll, the reproduced mayor advanced the route while fighting. A mage guard that finishes the shared context can instead skip due-route initialization. Route progression should depend on combat state independently of cast success.
- The ordinary ROM24 route branch returns false even after moving, speaking or using a gate. The Python route marks successful steps performed and skips the generic phase. A reproduced wake returned true. The bundled mayor is a sentinel, so this last difference is lower impact for him than the posture and route mistakes.

The previously reported scheduler-order mismatch is resolved in the reviewed working tree. Both runtimes run mobile and violence pulses before the time tick, and both try a bound special before shop replenishment. [ROM24 mayor](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:897) · [ROM24 pulse order](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:1081) · [Python route state](../../src/api/MobileApi.py#L417) · [Combat delegation](../../src/api/MobileApi.py#L117) · [Live posture accessor](../../src/game/AnimateEntity.py#L88) · [Python pulse order](../../src/game/UpdateHandler.py#L61)

### F06 · A guard can attack twice and starts combat before the first swing

**Resolved in the runtime and bundled content.** All 24 `spec_guard` records now finish the pulse after the accusation and a single `multi_hit` call, including when damage rejects the attack. Only a pulse without a visible criminal considers the lowest-alignment fighter below 300. Both branches use the normal first swing and leave safety and combat linkage to damage, as in ROM24.

Three new regressions cover the criminal branch after rejected damage, the fallback cutoff and target selection, and an opening swing against a stunned thief. The last test uses the runtime's hit roll and combat-link logic to verify the stunned posture modifier affects the swing and neither combat link is created. All 27 focused tests passed on a socketless event loop in the Windows sandbox. Import the updated guard records into the server's content service and reload them on the matching runtime. [Guard regressions](../../tests/test_restored_mobile_specials.py)

**Original finding.** With both a visible thief and an unrelated eligible fighter in the room, the old scripts called `multi_hit` for both on the same pulse. The old attack helper also linked both participants before the first swing. That could remove first-swing posture modifiers, strip sleep early, and create a combat link to an incapacitated target. The shared helper's early linkage was removed during F01.

[ROM24 guard return](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:826) · [ROM24 hit posture](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:488) · [ROM24 combat linkage](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:722) · [Bundled guard](../../resources/collections/SOMDB.Specials.json#L2408) · [Python attack helper](../../src/api/MobileApi.py#L274) · [Combat posture mutation](../../src/combat/CombatHandler.py#L1032)

### F07 · Guard accusations ignore yell recipient rules

**Shared yell path updated during F01.** The sender-override path used by both Hassan and the guard now clears `COMM_NOSHOUT` and invokes the standard yell command. The executioner regression verifies sender attribution and the quiet and sleeping recipient exclusions. [Shared yell dispatch](../../src/mobile/MobileHandler.py#L100) · [Executioner regression](../../tests/test_restored_mobile_specials.py)

ROM24 clears the guard's own `COMM_NOSHOUT`, then uses the area yell command. It reaches playing listeners in the area who have quiet off and meet the `act` posture threshold, and it resolves the guard's name for each listener. The script's `yell` helper queues raw area text. The mobile handler iterates player room occupants without checking quiet mode or posture. Connected switched bodies also bypass this room-character list. A quiet listener and a sleeping listener both received the accusation in a real message-bus probe. Sender attribution was absent. Reuse existing yell recipient and visibility rules while honoring the special's sender override.

[ROM24 guard yell](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:826) · [ROM24 yell recipients](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:974) · [ROM24 act posture](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2473) · [Python special yell](../../src/api/MobileApi.py#L262) · [Python delivery](../../src/mobile/MobileHandler.py#L407) · [Existing command rules](../../src/interp/commands/Communications.py#L375)

### F08 · Janitors take protected items and leave eligible drink containers and trash

**Resolved in the runtime.** The room-item selector now gives all three bundled janitor scripts the shared loot decision and the canonical item type. The authored predicate accepts takeable, lootable drink containers, trash, and objects costing less than 10. The loot check uses the same live owners as generic scavenging, so an owner elsewhere in the world can still protect an item. F13 tracks which eligible item is visited first.

Two regressions exercise the bundled `spec_janitor` through the mobile dispatcher. They cover the 100-silver brandy bottle `3601`, high-value trash, the strict cost cutoff, takeability, pickup notices, and a live owner granting `PLR_CANLOOT`. Both regressions reproduced the original failures when given the old selector values. All 47 focused tests passed. [Janitor regressions](../../tests/test_restored_mobile_specials.py#L82)

**Original finding.** The selector supplied `can_loot=True` and exposed raw `drink` and `trash` values. The janitor skipped a takeable drink worth 100 and took cheap trash owned by a live unrelated player with looting disabled.

[ROM24 janitor](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:850) · [Bundled predicate](../../resources/collections/SOMDB.Specials.json#L2874) · [Room-item selector](../../src/api/MobileApi.py#L363) · [Ownership policy](../../src/api/ItemApi.py#L46) · [Type normalization](../../src/item/Item.py#L270)

### F09 · Saved spells can lose their notices and yield the rest of the pulse

**Resolved in the runtime.** A completed mobile spell invocation now forwards its authored notices and claims the pulse even if a save or a normal early exit leaves the target unaffected. Missing spells, unresolved targets and script errors leave the pulse available to the caller. The adept's cure-disease branch forwards its output and explicitly leaves the pulse available. A poison bite still claims the pulse for the bite itself and now delivers the spell's resisted notices to the victim and room. Room-wide casts such as gas breath pass a room target kind and a null victim to the spell executor.

The bundled poison and mage regressions reproduce the dropped notices and pulse fallthrough when run with the old cast gate. Additional coverage verifies missing spells, unresolved targets, and script errors after an earlier step marks the spell performed. All 188 focused tests passed across mobile, spell, and breath suites. [Cast regressions](../../tests/test_restored_mobile_specials.py#L188)

**Original finding.** The adapter discarded queued spell output whenever `SpellContext.performed` was false. A saved poison bite sent its bite notice and lost the resisted notices. A saved weighted cast could yield the pulse to shop replenishment and generic processing.

[ROM24 caster return](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:659) · [ROM24 poison save notice](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:3850) · [Mobile spell adapter](../../src/api/MobileApi.py#L160) · [Python poison bite](../../src/api/MobileApi.py#L487) · [Pulse fallback](../../src/mobile/MobileHandler.py#L161)

### F10 · NPC teleport skips the destination room display

**Resolved in the runtime.** The mobile dispatcher now sends a standalone destination view through the standard player payload handler. After a successful NPC teleport, the target receives the automatic look and then a prompt for the destination. A saved teleport leaves the player in place. The dispatcher skips a stale view if the player has moved again and rejects malformed view payloads through its existing validation path.

The regression runs the bundled mage special and teleport spell through the mobile dispatcher, room display, and prompt renderer. With the old dispatcher, the player moved and received only the cast and teleport notices. All 226 focused tests passed across mobile payload, spell, and travel suites. [Teleport and payload regressions](../../tests/test_rom24_report_fixes.py#L115)

[ROM24 teleport](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4352) · [Python view producer](../../src/api/SpellApi.py#L1418) · [Mobile payload dispatcher](../../src/mobile/MobileHandler.py#L398) · [Standard view handler](../../src/player/PlayerHandler.py#L973)

### F11 · Level-one pickpockets can take money

**Resolved in the runtime.** The pickpocket percentage is capped at integer `level / 2` for both coin rolls. A level-one thief can still complete the attempt and claim the pulse, but the percentage cap is zero. The regression uses the bundled spoiled brat `6608`, checks the roll order and both balances at levels one and two, and reproduces the theft at level one when the old minimum is restored.

[ROM24 coin formula](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:1028) · [Python coin formula](../../src/api/MobileApi.py#L511) · [Bundled thief script](../../resources/collections/SOMDB.Specials.json#L22) · [Regression](../../tests/test_restored_mobile_specials.py#L84)

### F12 · A resting nasty thief can rip a coin purse

**Resolved in the runtime.** The combat helper requires live `POS_FIGHTING` and an opponent before it draws a purse, flee, or idle outcome. The bundled `spec_nasty` regression starts with a resting thief whose opponent is outside the ambush window and verifies that the special returns false before drawing an action. With fighting posture restored, the same opponent loses 10 of 100 gold on the forced purse outcome. The resting case reproduces the theft when the old opponent-only check is restored. All 91 focused tests passed for F11 and F12.

[ROM24 posture split](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:332) · [Bundled nasty script](../../resources/collections/SOMDB.Specials.json#L5650) · [Python combat branch](../../src/api/MobileApi.py#L566) · [Regression](../../tests/test_restored_mobile_specials.py#L103)

### F13 · First match can select a different corpse, item or opponent

**Resolved in the runtime.** Mobile special scans visit the newest room occupant or floor object first, matching ROM24's prepended lists. The room tracks entry order across players and mobiles, including reentry. The regressions verify that a caster chooses the newest eligible opponent across both types, fido devours the newest corpse and spills its contents, and generic scavenging chooses the newest item when eligible values tie.

[ROM24 character insertion](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1395) · [ROM24 object insertion](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1777) · [Room traversal](../../src/area/Room.py#L253) · [Mixed occupant regression](../../tests/test_mobile_special_room_access.py#L104) · [Fido regression](../../tests/test_rom24_report_fixes.py#L415)

### F14 · Reloading specials leaves cached and copied scripts stale

**Resolved in the runtime.** A successful `reload_specials()` on the world event loop refreshes prototype and active mobile bindings for the next dispatch. Mobiles that move across areas keep the assignment scope of their prototype. Wizard overrides resolve by Special ID, so the override follows edits to its selected record. Removed definitions clear their bindings. Named delegates resolve against the published registry, including when lookup was already warmed. Failed reloads retain the previous definitions and bindings.

Named lookup prefers an executable library record when several records share a name, with record ID as the tie-breaker. The regression uses the real reload path with simulated content-service responses. It covers updated, added and removed assignments, a mobile that left its prototype area, a wizard override, a future spawn, a warmed delegate, and a failed reload. [Special reload and binding publication](../../src/area/SpecialService.py#L27) · [Named lookup](../../src/area/SpecialRegistry.py#L23) · [Reload regression](../../tests/test_mobile_special_binding.py#L94)

### F15 · Undead casters roll harm too often

**Resolved in bundled content.** All 39 `spec_cast_undead` records now give harm one explicit outcome and seven default outcomes. The regression enumerates the eligible draws at levels 18, 20, and 21, obtaining harm probabilities of 8/14, 8/15, and 8/16 respectively. All 200 focused tests passed for F13 through F15.

[ROM24 undead table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:672) · [Bundled undead table](../../resources/collections/SOMDB.Specials.json#L135) · [Weighted selector](../../src/api/MobileApi.py#L230) · [Distribution regression](../../tests/test_restored_mobile_specials.py#L86)

## Coverage of the nonempty scripts

| Family | Records | Compared behavior |
| --- | ---: | --- |
| `spec_cast_mage` | 99 | Fighting posture and per-opponent two-bit draw match. Eligible spell weights match ROM24's rejection sampling after filtering by level. NPC teleport displays the destination. |
| `spec_cast_cleric` | 73 | Same target selection and effective table weights, including four dispel-magic outcomes and three harm outcomes at the relevant levels. |
| `spec_cast_undead` | 39 | Fighting gate and per-opponent two-bit draw match. NPC teleport displays the destination. The table gives harm eight eligible outcomes. |
| `spec_breath_fire` | 21 | Live fighting gate and target roll match. Primary and collateral saves, exposure and HP damage use the ROM24 fire branch structure after target selection. |
| `spec_breath_frost` | 10 | Live fighting gate and target roll match. Frost uses the same primary/collateral structure with cold exposure. |
| `spec_breath_lightning` | 7 | Live fighting gate and target roll match. Single-target save and shock exposure are present. |
| `spec_breath_gas` | 11 | No individual target roll. Shared base damage, room exposure first, area safety and the ROM24 NPC exception are present. Gas excludes an NPC when either combat pointer connects it to the NPC caster. |
| `spec_guard` | 24 | Awake and idle gates, newest-first criminal scan and the fallback alignment cutoff of 300 are present. The accusation uses the standard area yell. |
| `spec_poison` | 27 | Fighting posture, opponent and inclusive percent threshold `2 × level` match. The bite claims the pulse and forwards a saved spell's resisted notices. |
| `spec_thief` | 36 | Standing gate, mortal level limit, five-bit roll, visibility, awake discovery, and separate coin rolls match. The percentage cap is zero at level one. |
| `spec_fido` | 6 | Awake gate, newest-first NPC corpse selection, removal and item spill verified. |
| `spec_janitor` | 3 | Picks the newest item that passes the takeable, ownership, item type, and price checks while awake. |
| `spec_mayor` | 1 | Hours 6 and 20 and both route strings match. Both routes reach the east and west gates and return to the office. Wake, sleep, and combat decisions match the behavior covered by F05. |
| `spec_nasty` | 1 | The ambush uses the +1 through +9 level window and backstab-to-murder fallback. Live fighting posture gates the quarter purse, quarter flee and half idle combat outcomes. |
| `spec_scavenge` | 1 generic | Standing gate, scavenger flag, six-bit chance, loot eligibility and best cost above one match. The newest eligible item wins a tie. |
| `spec_wander` | 1 generic | Present in the current bundle. Standing gate, sentinel exclusion, 3-bit attempt, 5-bit direction and exit/room restrictions tested. The previous missing-definition and stale-standing findings are resolved on the bundled path. |

[ROM24 caster tables](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:540) · [ROM24 breath effects](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4496) · [Runtime weights](../../src/api/MobileApi.py#L227) · [Generic ROM24 pulse](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:374) · [Bundled wander regression](../../tests/test_entry_and_following_parity.py#L314)

The C caster tables redraw when the roll selects a spell above the mobile's level. The Python selector filters by level and then draws once. For equivalent valid weights this gives the same conditional spell distribution and uses fewer random draws on pulses where C rejects a roll.

## Validation and limits

- In the original review, parsed the ROM area `#SPECIALS` sections and compared the assignment multiset with the bundled snapshot. Parsed all 413 records through the Python special model, built all 986 mobile prototypes through `MobileService`, and checked that 411 bound and 358 received nonempty scripts. All 1,002 shipped lambda entries compiled and their direct context helper signatures bound. All 23 distinct spell names referenced by the active specials resolved from bundled content. The F01 update changes only `specialFunction` on the 53 previously empty assignments.
- Used the production dispatchers with fixed rolls and in-memory rooms, combat and message boundaries. Probes isolated downstream behavior from F02 by supplying a working collaborator directly where needed. For the mayor route, loaded the bundled Midgaard rooms and applied bundled door resets. The control changed only which travel path handled the scripted directions.
- **206 focused existing tests passed** across isolated runs. The total includes 144 spell and elemental tests, 34 movement and gameplay parity tests, and 28 mobile, binding, emission, independent-cast, fido and mayor checks. The last group used an in-memory coroutine runner to avoid the Windows sandbox event-loop socket initialization hang. A combined harness produced three visibility-fixture failures that cleared when the mayor/fido module ran in isolation.
- The review compared all 24 families at the assignment, script and primary gameplay decision levels. Live service contents, executable-C differential sessions, and every branch of the downstream spells and combat engine remain unverified. Generic cast announcements and some direct notices also differ in presentation and recipient rendering. The findings above cover reproducible gameplay and delivery failures without requiring changes to the game's wording.

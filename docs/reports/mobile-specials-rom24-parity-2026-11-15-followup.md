# Bundled mobile specials compared with ROM 2.4

November 15, 2026 · Follow-up to the [previous review](archive/mobile-specials-rom24-parity-2026-11-15.md)

Reviewed Springs at `2a1899221f0f139db3950541b22d603bb127fceb` with the current working tree, against the local PyRom ROM 2.4 C source and area files. The bundle contains **413 executable records across 24 families**. All **411 bound assignments** match ROM by mobile vnum and special name. The other two records implement generic scavenging and wandering. All 986 mobile prototypes built successfully, and every expected assignment bound to its prototype. The remaining discrepancies occur after binding, in spell execution, combat initiation, update order, and delivery.

## Verified findings

### F16 · P2 · Change sex fails on saved player values

**Resolved in the runtime and bundled spell.** Change Sex and `APPLY_SEX` now use the same conversion for named and numeric values. Both caster specials apply the 40-tick effect at level 20 after a failed save. Expiry restores the original sex using its numeric string representation. The regression exercises `male` and `female` through both bundled special scripts and advances the effect timer through removal. [Value conversion](../../src/game/AnimateEntity.py#L71) · [Spell helper](../../src/api/SpellApi.py#L473) · [Spell record](../../resources/collections/SOMDB.Spells.json#L4193) · [Regression](../../tests/test_restored_mobile_specials.py#L109)

**Original behavior**

Both the cleric and mage tables can select Change Sex from level 12. ROM applies a different sex value for twice the caster's level on a failed save and returns true from the special. The bundled spell evaluates `int(victim.sex)` twice. Both bundled player records use `"male"`, and the live character model recognizes named sex values. With a failed save, this conversion raises `ValueError` before applying the effect. The mobile dispatcher treats the script failure as a skipped special.

Forced the cast through the bundled mage and cleric scripts at level 20. Both families failed against `"male"` and `"female"`, leaving the stat and effect list alone. Both changed `"1"` to `"2"` and applied a 40-tick effect under the same rolls. The affected paths include 99 mage and 73 cleric assignments and the mayor's mage delegate. The shared `APPLY_SEX` mutator also uses integer conversion with a zero fallback, so a correction needs to cover effect application and removal as well as the spell expression. [ROM spell](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:1279) · [Cleric table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:565) · [Mage table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:645) · [Saved characters](../../resources/collections/SOMDB.Characters.json#L8) · [Spell expression](../../resources/collections/SOMDB.Spells.json#L4193) · [Effect mutator](../../src/item/EffectHandler.py#L89) · [Mobile return handling](../../src/api/MobileApi.py#L187)

### F17 · P2 · The Midgaard thief's murder fallback changes the opening attack

**Resolved in the shared murder command and bundled command payload.** On an allowed murder attempt, the attacker takes one violence pulse of wait and the victim attempts the standard area yell using the authored line. The first swing uses the victim's current posture, with combat linkage handled by damage. The regression sends an unarmed thief through the backstab fallback and verifies wait, posture, combat links, and delivery from the victim to a same-area witness with quiet mode off. [Opening action](../../src/interp/commands/Fight.py#L101) · [Attack execution](../../src/api/FightApi.py#L108) · [Command payload](../../resources/collections/SOMDB.Commands.json#L6950) · [Regression](../../tests/test_remaining_gameplay_parity.py#L279)

**Original behavior**

The level-30 thief `3163` spawns in room `3048` without a wielded weapon. A visible level-31 player triggers the ambush. Backstab requires a weapon, so the ordinary spawn reaches the murder fallback. ROM sets one violence pulse of wait, makes the victim attempt a help yell, then calls `multi_hit`. The first swing sees the victim's original posture, with combat linkage occurring in damage. Springs routes murder to the generic kill plan. That plan sets combat on both participants before the swing and emits no help yell or murder wait.

Ran the bundled ambush through `MobileHandler`, `Fight` and `FightApi`, recording state at the first swing. A resting victim was already in fighting posture and linked to the thief, the thief's wait was zero, and the emitted payloads contained no help yell. The early posture change can alter the first swing. The surrounding area loses the warning it would receive when the victim can yell. [ROM reset](C:/Users/scott/PycharmProjects/PyRom/Rom24/area/midgaard.are:6205) · [ROM ambush](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:332) · [ROM murder](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2711) · [ROM hit posture](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:488) · [Bundled ambush](../../resources/collections/SOMDB.Specials.json#L5649) · [Python murder](../../src/interp/commands/Fight.py#L89) · [First-swing plan](../../src/api/FightApi.py#L108)

### F18 · P2 · Mobile pulse order reverses which rival strikes first

**Resolved in the runtime.** The mobile pulse visits its snapshot in descending creation order across all rooms. Movement preserves creation order, and newly spawned or cloned mobiles get a new sequence value. Before dispatch the handler checks whether the same instance is still present. Regressions cover which rival opens combat before and after reentry, ordering across rooms, removal during the pulse, and deferral of new spawns to a subsequent pulse. [Creation order](../../src/game/AnimateEntity.py#L61) · [Pulse snapshot](../../src/mobile/MobileHandler.py#L136)

**Original behavior**

ROM traverses the global character list, with newly created mobiles prepended. Springs takes its pulse snapshot by room and visits each room's mobiles in insertion order. The newest-first target scan inside a special does not affect which mobile gets to act first.

In a room with no patrolman, spawned the bundled troll `2101` before the bundled ogre `2102`. Both were idle, level-eligible, and safe to attack. With combat linkage at the first attack, Springs ran the troll's attack and the ogre's now-fighting guard skipped its turn. ROM's creation order gives the ogre the first attack under that setup. Across rooms, room enumeration additionally replaces the global creation order. The difference can change which mobile opens a fight or gets a special off before another mobile acts. [ROM creation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1737) · [ROM mobile update](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:374) · [Gang guards](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:126) · [Python pulse snapshot](../../src/mobile/MobileHandler.py#L135)

### F19 · P2 · Area damage still visits targets in a different order

**Resolved in the runtime and bundled Earthquake spell.** Fire, frost, and gas breath traverse the mixed room list newest arrival first. Earthquake visits eligible room targets in newest global entry order, based on mobile creation and fresh player entry. Returning to a room or reattaching an existing session preserves that global order. Pet snapshots omit the runtime sequence. Restoring a pet gives it a new sequence and accepts older snapshots that include the field. The regression reenters an older player into a mixed room and verifies that breath and Earthquake visit targets in their respective orders. [Fire and frost](../../src/api/SpellApi.py#L924) · [Gas](../../src/api/SpellApi.py#L994) · [Earthquake](../../src/api/SpellApi.py#L631) · [Pet restore](../../src/mobile/PetSnapshot.py#L34) · [Regression](../../tests/test_restored_mobile_specials.py#L271)

**Original behavior**

ROM fire, frost, and gas breath walk the room's mixed newest-first list. The cleric's Earthquake traverses ROM's global character list and applies damage to occupants it encounters in the caster's room. Springs uses a helper that concatenates players and mobiles, each in insertion order. Exposure, saves, and damage run inside that loop. The wave can assign rolls and apply damage side effects in a different sequence even when its primary target is correct.

Forced the fire outcome of the bundled mixed-breath special against two eligible players. The newer arrival was correctly selected as primary. Springs called damage on the older collateral target first, then on the newer primary. ROM visits the newer player first in that room state. [ROM breath loops](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4496) · [ROM Earthquake](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:2188) · [ROM room insertion](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1395) · [Python elemental breath](../../src/api/SpellApi.py#L893) · [Gas damage](../../src/api/SpellApi.py#L965) · [Earthquake iteration](../../src/api/SpellApi.py#L627) · [Shared target order](../../src/api/SpellApi.py#L1609)

### F20 · P3 · Teleport skips the destination view for a switched player

**Resolved in the runtime.** An NPC teleport can now hand off the destination view to a switched body through the standard room renderer. The dispatch checks that the body remains controlled and in the destination before showing the room and sending its prompt. The regression drives the bundled mage special through the message bus and verifies teleport confirmation, destination description, and prompt on the switched body's connection. [View producer](../../src/api/SpellApi.py#L1433) · [Delivery](../../src/mobile/MobileHandler.py#L400) · [Regression](../../tests/test_rom24_report_fixes.py#L164)

**Original behavior**

ROM calls automatic look on the victim after teleport. A switched body carries the wizard's descriptor, so it can receive that look. Springs restores the view for a player character, but the spell skips view creation for a switched mobile. The mobile payload validator would also reject a standalone view with a `Mobile` as the viewer.

Forced the bundled mage's teleport against a connected, awake switched body. The body moved and received the private teleport notice. The dispatcher received no destination-view payload, so the standard output path supplied neither a look nor its follow-up prompt. [ROM teleport](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4352) · [ROM descriptor transfer](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:2236) · [ROM look guard](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:980) · [Python switch state](../../src/game/WizHandler.py#L97) · [View producer](../../src/api/SpellApi.py#L1418) · [Payload validation](../../src/mobile/MobileHandler.py#L330) · [Look and prompt delivery](../../src/mobile/MobileHandler.py#L398)

### F21 · P3 · Special combat notices bypass visibility and posture rules

**Resolved in the runtime and bundled nasty special.** Bite, purse, and pickpocket discovery use shared, recipient-specific act rendering. Actor, victim, and room notices honor the resting posture threshold and include switched bodies where applicable. A successful bite invokes Poison directly, so it emits the spell's result without an extra summary that could identify an unseen attacker. The nasty record supplies the attacker, victim, and room lines for the purse attack. [Act routing](../../src/util/DisplayUtil.py#L88) · [Bite](../../src/api/MobileApi.py#L487) · [Purse record](../../resources/collections/SOMDB.Specials.json#L5654) · [Regression](../../tests/test_restored_mobile_specials.py#L390)

**Original behavior**

ROM's bite `act` renders the attacker for the victim and requires at least resting posture. The poison bite sends a raw attacker name directly to a PC and excludes NPC victims even when controlled. A forced bite from an invisible attacker identified the attacker to a player who could not see it. A sleeping player also received the bite line. The subsequent resisted-poison notice is a separate spell result and can still be delivered.

The nasty thief's purse attack has the inverse attribution problem. Its victim message always names the attacker as “Someone,” even when visible. The handler also drops the attacker-facing bite tuple entry and has no attacker-facing purse entry. Those channels matter when a wizard controls the acting mobile. The discovered-pickpocket line follows the same raw-name pattern, although normal thief eligibility first checks whether the thief can see the victim. [ROM bite](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:981) · [ROM purse](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:358) · [ROM pickpocket](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:1010) · [ROM act routing](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2431) · [Python bite](../../src/api/MobileApi.py#L487) · [Pickpocket](../../src/api/MobileApi.py#L518) · [Purse](../../src/api/MobileApi.py#L566)

### F22 · P3 · Breath warnings arrive as generic cast summaries

**Resolved in the runtime and all five bundled breath spells.** Each spell queues its authored warning before rolling damage or applying exposure. Targeted breaths have separate victim and room lines, and gas sends its room warning to eligible listeners other than the caster. The mobile adapter suppresses the generic cast summary when the script supplies a warning. Regressions cover all five spells through mixed breath and verify pre-damage queueing, visibility, sleeping recipients, and switched casters and victims. [Spell warning operation](../../src/api/SpellApi.py#L822) · [Bundled fire warning](../../resources/collections/SOMDB.Spells.json#L4340) · [Mobile dispatch](../../src/api/MobileApi.py#L187) · [Regression](../../tests/test_restored_mobile_specials.py#L303)

**Original behavior**

ROM's five breath spells send their action notices before rolling damage and applying exposure. The victim and room get distinct notices, rendered with the normal visibility and posture rules. The bundled spells implement exposure and damage, and the mobile adapter adds a generic cast summary only after the script runs. That summary is prepended to the spell's outgoing notices for a successful cast, so the recipient normally sees it before the damage lines. It still uses raw names and includes sleeping room occupants. For targeted breaths it excludes the primary target from room delivery and sends a generic direct line to that player.

Forced fire breath with a sleeping primary target. The probe delivered a direct generic cast line to the sleeper and named that player to the room. ROM's direct warning goes through the posture threshold, and the room warning announces the cone without naming the primary target. The discrepancy is in the warning and its audience. The observed fire cast still ran the damage path. [ROM breath notices](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:4467) · [Bundled fire breath](../../resources/collections/SOMDB.Spells.json#L4313) · [Mobile cast payload order](../../src/api/MobileApi.py#L187) · [Generic cast summary recipients](../../src/api/MobileApi.py#L792)

## Coverage

| Bundled families | Records | Compared behavior |
| --- | ---: | --- |
| `spec_cast_mage`, `spec_cast_cleric`, `spec_cast_undead`, `spec_cast_judge` | 218 | Fighting gates, reciprocal opponents, per-candidate roll, level bands, weighted tables, and pulse returns. Undead Harm retains eight eligible outcomes. F16, F19, and F20 cover downstream defects. |
| `spec_cast_adept` | 6 | Awake and visibility gates, roll before PC and level filters, seven spell outcomes, and the cure-disease fallthrough. |
| `spec_breath_any`, `spec_breath_acid`, `spec_breath_fire`, `spec_breath_frost`, `spec_breath_gas`, `spec_breath_lightning` | 79 | Mixed breath's eight outcomes, targeted reciprocal selection, gas's room-wide dispatch, HP-based damage, save scaling, exposure order, and NPC eligibility. See F19 and F22. |
| `spec_guard`, `spec_executioner` | 25 | Awake and idle gates, first visible criminal, killer-before-thief on the same target, shared yell route, one attack, and the guard's alignment fallback below 300. |
| `spec_troll_member`, `spec_ogre_member`, `spec_patrolman` | 9 | Rival level and safety checks, reservoir sampling, patrolman veto, higher-level intervention with opponent winning ties, neck slots, and local and distant whistle notices. See F18 for turn order. |
| `spec_fido`, `spec_janitor` | 9 | Awake gate, newest corpse and contained-item spill, takeability, live ownership, and drink, trash, and low-cost selection. |
| `spec_thief`, `spec_nasty`, `spec_poison` | 64 | Thief roll order and integer caps, nasty ambush level window and combat action weights, poison's inclusive chance and save output. See F17 and F21. |
| `spec_mayor` | 1 | Both scheduled routes, live wake and sleep, pause and resume during combat, gate operations, and continuation into the generic phase. Its combat delegate shares the mage findings. |
| `spec_scavenge`, `spec_wander` | 2 | Generic order after the bound special and shop top-up, charm and empty-area gates, standing posture, loot selection, separate wander rolls, and travel restrictions. |

## Validation and limits

- After the F19–F22 fixes, **414 focused tests passed** in 19 isolated module runs, including login, reconnect, and pet persistence. The collection query tool verified the Earthquake ordering rule, all five breath warnings, and the nasty thief's purse lines. Deploy the matching runtime and publish the revised Spell and Special records together.
- After the F16–F18 fixes, **301 focused tests passed** in 12 isolated module runs. The collection query tool confirmed the updated Change Sex expression and murder help yell. Deploy the matching runtime and publish the updated Spell and Command records together.
- Compared the ROM area `#SPECIALS` assignment multiset against the checked-in collection. Verified 413 unique record IDs, 411 unique area/vnum bindings, zero empty scripts, and identical scripts within each family. All **1,177 lambda entries** compiled. Four assigned prototypes have no bundled `M` reset, matching the previous inventory. Their vnums are `1132`, `1365`, `8319`, and `9237`. [Specials bundle](../../resources/collections/SOMDB.Specials.json) · [Binding code](../../src/mobile/MobileService.py#L39)
- Probed **44 family/spell pairs covering 32 distinct spells** through the mobile spell adapter and bundled spell lambdas with controlled saves and in-memory collaborators. Only the two Change Sex pairs aborted in that sweep. This checks dispatch under the tested conditions. The pair count lists spells directly referenced by their respective families and counts delegates through their respective spell families. Separate probes ran the full bundled special scripts for combat fallback, rival initiative, breath order, teleport, and bite delivery.
- **232 focused tests passed** in eight isolated module runs covering bindings, pulse behavior, room access, spells, movement, and combat. A combined run produced fixture failures when modules with global stubs shared a process. Those failures cleared in isolated runs. Async tests used a socketless event loop in the Windows sandbox.
- Compared the local sources and ran in-memory Python probes. Live content-service records, a compiled ROM differential session, and exhaustive downstream spell and combat permutations remain unverified. The tested `reload_specials()` method refreshes bound instances when called. A search of the checked-in runtime found only its definition, so the report does not establish an operator-facing live reload entry point. [Reload method](../../src/area/SpecialService.py#L27) · [Reload regression](../../tests/test_mobile_special_binding.py#L94)

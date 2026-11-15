# Repository-wide ROM24 parity review

November 15, 2026

Reviewed the Springs of MUD working tree at base revision `3e2fdc570139d3aa69b7d1e031a4e4fa4eaca8ed`, including local runtime and test changes, against the local `PyRom/Rom24/src` checkout. Four high-priority differences reproduced. Fix `charm person` first. Correct the mobile posture check before restoring generic wandering, because both scavenging and wandering use that check.

## F01 · Charm person always stops at its safety guard

On a successful cast against a visible, uncharmed, lower-level ordinary NPC in a room that permits combat and charm, ROM24 proceeds past `is_safe`, checks the victim's save, then assigns the caster as master and leader and applies `AFF_CHARM` if the save fails. In Springs, the shipped spell stops at its first step. `SpellApi.is_safe` passes through the combat handler's two-element result. Even the allowed result `(False, "")` is truthy, so the spell stops before the save or any follower or effect changes. A normal successful casting roll still spends mana and applies the casting wait before executing the spell.

**Reproduction.** Ran the shipped spell with a level-35 caster, a level-1 mobile and the production melee safety check. Safety returned `(False, "")`. A forced successful casting roll with a five-mana cost moved mana from 100 to 95 and wait from 0 to 12 pulses. The spell stopped with zero saving throws, no master, and no effects. The collection query found one spell using this helper. The existing guard tests mock the safety result as a Boolean, which explains why the spell test module passed all 131 tests despite the production mismatch.

**Fix.** Unpack the safety result at the spell API boundary and expose the Boolean to authored conditions. Preserve ROM's safety notice on blocked targets. Verify an eligible target becomes a charmed follower after a failed save, and a protected target remains unchanged.

[ROM24 charm](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:1313) · [Shipped guard](../../../resources/collections/SOMDB.Spells.json#L469) · [Spell safety adapter](../../../src/api/SpellApi.py#L514) · [Guard evaluation](../../../src/api/SpellApi.py#L815) · [Combat safety return](../../../src/combat/CombatHandler.py#L151) · [Cast charges and wait](../../../src/api/SpellApi.py#L67) · [Existing charm guard fixture](../../../tests/test_spell_affect_payload_messages.py#L830)

## F02 · The bundled specials omit generic NPC wandering

After its special, shop and standing checks, ROM24 gives an eligible non-sentinel NPC a wander roll. On a valid direction it checks exit and room restrictions and invokes ordinary travel. Springs dispatches a named `spec_wander` from the same part of the mobile pulse. The bundled specials have the generic `spec_scavenge` entry and omit `spec_wander`. The runtime returns before invoking the available wander primitive whenever the specials registry lacks that entry. A world seeded from the bundled snapshot therefore loses generic NPC wandering across its areas, changing where players encounter ordinary roaming mobs.

**Reproduction.** Loaded all 412 bundled records through the runtime special model and ran the mobile update with a standing non-sentinel and an open north exit. The mobile stayed put and the RNG received zero calls. With only the missing `lambda ctx: ctx.wander()` definition supplied in memory, the same mobile and pulse used both forced-zero rolls and arrived through the exit. Commit `27f4de5` removed the original record during a bulk snapshot refresh. The configured service may carry different data. This finding is verified for the bundled snapshot and any service seeded from it.

**Fix.** Restore the generic special through designer-owned content, check that the served record reaches the runtime registry, and verify wandering through the full mobile pulse with open and blocked exits. Include the fighting-mobile case in F03 before restoring the definition.

[ROM24 wander](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:440) · [Bundled specials](../../../resources/collections/SOMDB.Specials.json) · [Special service loader](../../../src/area/SpecialService.py#L23) · [Pulse dispatch](../../../src/mobile/MobileHandler.py#L169) · [Missing-name branch](../../../src/mobile/MobileHandler.py#L218) · [Wander primitive](../../../src/api/MobileApi.py#L677)

## F03 · Fighting NPCs can scavenge during the mobile pulse

ROM24 skips generic scavenging and wandering unless the NPC is currently standing. Springs initializes the mobile's top-level `position` at spawn, then combat changes `character_attributes.position` to fighting. The mobile pulse reads the top-level value and runs the generic routines as if the NPC were standing. During combat a scavenger can remove a takeable floor item from the room, including an item players dropped during the encounter. The same check would allow a non-sentinel fighter to attempt generic wandering once F02 is corrected.

**Reproduction.** Spawned bundled mobile `6600` (dwarven youth), engaged it using the production combat transition, and ran the mobile pulse with a takeable item worth 100 and a successful scavenging roll. The combat posture was `POS_FIGHTING` (7) and the top-level value was `POS_STANDING` (8). The pulse transferred the floor item to the mobile's inventory.

**Fix.** Read the live posture through the shared character position accessor. Test a standing scavenger, a scavenger that just entered combat, and one that has returned to standing. Cover wandering with the authored definition present.

[ROM24 standing check and scavenging](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:408) · [Mobile spawn posture](../../../src/mobile/MobileFactory.py#L175) · [Combat posture transition](../../../src/util/FightUtil.py#L108) · [Mobile standing check](../../../src/api/MobileApi.py#L897) · [Generic pulse gate](../../../src/mobile/MobileHandler.py#L158) · [Scavenge transfer](../../../src/api/MobileApi.py#L630)

## F04 · Bless applies to characters already fighting

ROM24 rejects a character target in `POS_FIGHTING` before granting either the hit-roll or saving-throw effect. Springs' shipped `bless` has that guard, but the spell API returns false if the target lacks a top-level `position` attribute. A recently loaded player can enter combat with only `character_attributes.position` set. The guard then lets a caster grant combat bonuses during the fight. The shared bless path also matters when `holy word` invokes the buff.

**Reproduction.** Started combat for a freshly built real player through the production combat handler and ran the shipped `bless` lambdas at caster level 32. The target had live position `POS_FIGHTING` and no top-level `position`. The engine applied both effects, yielding +4 hit roll and −4 saving throw. The existing `holy word` test for this restriction supplies an explicit top-level `position`, bypassing the faulty guard condition.

**Fix.** Evaluate the character target's current posture through the shared accessor. Verify the shipped spell rejects an unblessed fighter and applies both effects to an eligible standing target. Exercise the same condition through `holy word`.

[ROM24 bless](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:820) · [ROM24 holy word](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:3196) · [Shipped bless guard](../../../resources/collections/SOMDB.Spells.json#L202) · [Spell posture check](../../../src/api/SpellApi.py#L619) · [Shared position accessor](../../../src/api/CharacterApi.py#L366) · [Existing holy word fixture](../../../tests/test_spell_affect_payload_messages.py#L2675)

## Coverage and verification

| Runtime area | Reviewed paths |
| --- | --- |
| Combat, spells and skills | Combat startup and safety, damage and defenses, assists, death and automatic looting, fleeing, cast and item target routing, effects, charm and bless, and skill improvement. Compared selected paths in `fight.c`, `magic.c`, `handler.c`, `act_obj.c` and `skills.c`. |
| Movement, mobile AI and world updates | Directional travel, follow and portal restrictions, regeneration and periodic effects, mobile specials and pulse conditions, object decay, reset placement, and shop cash replenishment. Compared selected paths in `act_move.c`, `act_enter.c`, `update.c`, `handler.c`, `special.c` and `db.c`. |
| Objects, economy and progression | Corpse ownership and extraction, inventory and equipment state, shop and item-activation entry points, learning, and saved progress. Sampled the corresponding C paths and surveyed the Python regression modules. |
| Commands, communications and persistence | Command dispatch and action waits, reconnect, possession and extraction, quit and pet persistence, and group and note state. Compared selected paths in `comm.c`, `act_comm.c`, `save.c` and `note.c`. Information commands, socials, and the wider immortal command set received regression or earlier-report coverage. |

- A bounded isolated run attempted all 137 top-level Python test modules with `src` on the import path. 961 tests passed across 85 modules. Fifty modules timed out, and two collection-tool modules hit sandbox permissions when writing test fixtures to the default temporary directory. A standalone `asyncio.run` reproduced a hang at Windows event-loop socket-pair initialization. All four findings were reproduced through local runtime probes. The mobile probes executed the update coroutine with in-memory message handling.
- The [November 14 follow-up](repository-rom24-parity-2026-11-14-followup.md) recorded a pending character-service rollout for group ownership, combat counters and note cursors. That rollout was outside this review. Idle and limbo behavior, offline recovery, command abbreviations, and movement-triggered aggression remain open policy or service questions.
- Validation covered sampled gameplay branches and the bundled snapshots. Live service responses, a compiled ROM24 gameplay session, the full authored branch inventory, music, and legacy area conversion remain unverified.

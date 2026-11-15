# Repository-wide ROM24 parity review

November 13, 2026. Reviewed the Python working tree at HEAD `3e2fdc570139d3aa69b7d1e031a4e4fa4eaca8ed`, including the pending changes from the previous parity review, against the local `PyRom/Rom24/src` reference. The review combined a repository-wide regression sweep with fresh source traces and targeted runtime probes.

| Priority | Finding | Gameplay impact |
| --- | --- | --- |
| P1 | F01 · The character API omits purchased group ownership | A fresh runtime load loses the player's explicit group ownership and can let them spend trains on the same group again. |
| P1 | F02 · Mobile damage bonuses are lost when armed and multiplied with posture when unarmed | Equipped NPCs can lose a large authored damage bonus, and unarmed attacks against downed opponents can gain damage ROM would add only once. |
| P2 | F03 · NPC area attacks merge different victims into one result | The primary victim can receive the secondary victim's hit text. A secondary death marks the primary-target round as lethal. |
| P2 | F04 · A charmed NPC can cast when ordered by its owner | A player can use an unswitched follower to apply spells with the follower's resources. |
| P2 | F05 · A follow-up hit leaves an engaged victim in their downed posture | A resting combatant stays vulnerable to the lower-posture hit and damage modifiers across subsequent attacks. |

P1 denotes material loss of saved advancement or a broad combat balance error. P2 denotes a material gameplay error with a more specific trigger.

## Resolution

- **F01.** The [companion API patch](f01-character-progress-som-server-modulith.patch) preserves purchased groups, the three combat counters, and both note cursors through the character write and read paths. It was tested against `som-server-modulith` revision `1fd0c5775d9f3cb8bd6070411e6693a2a0b54df1`. All 13 targeted Java tests passed, including an HTTP PUT and fresh GET with Spring's BSON mapping and a test for legacy records with absent combat counters. The Python gain regression rejects repurchasing a group after reloading the character. The companion service still needs the patch deployed. Records that already lost group ownership require a historical source to recover it.
- **F02.** NPCs add the authored damage dice bonus through their base damage roll for both armed and unarmed attacks. The calculation applies posture to the base hit and scales damage roll with proficiency. Pet snapshots created before the change receive the missing base bonus on load.
- **F03.** An NPC's area swings deliver each target's messages and death aftermath in attack order. A lethal primary hit ends the round before the sweep. The combat scheduler and mobile specials use the same round payload for delivery.
- **F04.** The cast command checks for an active switched session controlling the acting NPC. An order to an unswitched follower consumes no follower mana or wait and applies no spell. Mobile specials retain their spell execution path.
- **F05.** Damage to an already engaged, active victim above stunned restores fighting posture for later swings while retaining their current opponent. The current swing uses the victim's posture at the time of the attack roll. ROM's exact idle-timer behavior remains outside this fix.

After the fixes, all 1,735 tests across 137 top-level Python test modules passed in isolated processes.

## F01 · The character API omits purchased group ownership

**Trigger and result.** Acquire a group with `gain`, save, then load the character into a fresh runtime from the configured character API. ROM24 writes explicit known group names and restores them through `gn_add`. Springs' gain path records ownership in `character.groups`, and its PUT snapshot includes `groups`. The configured `GET /api/v1/characters` response returned two documents with `skills` and `characterAttributes` and omitted `groups` from both. The deserializer initializes an omitted group list to empty. A local probe granted the `combat` group and verified that ownership survives the full Python snapshot and disappears when the response omits `groups`. Learned members and their group's purchase record are separate state, so even retained skills cannot restore the purchase.

**Fix boundary.** Extend the character API's request, persisted document, and response together. Verify a nonempty group list through save and a fresh read, and check that the gain guard recognizes the restored purchase. The GET was read-only. It establishes the missing response field, while the write-side and stored-record behavior require a separate round trip.

The same response omitted `hitRoll`, `damRoll`, `savingThrow`, `noteReadStamps`, and `noteReadIds`, all emitted by the Python writer. ROM24 persists combat counters and note read timestamps. Python can reconstruct omitted combat counters from saved effects, so the omissions specifically threaten independent base values and read progress. These adjacent fields warrant the same contract check with nondefault fixtures.

[ROM24 saved group ownership](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:301) · [ROM24 group load](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:937) · [ROM24 combat counters](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:232) · [Python group grant](../../../src/interp/commands/Movement.py#L796) · [Character save fields](../../../src/player/CharacterService.py#L120) · [Missing-group default](../../../src/player/Character.py#L89)

## F02 · Mobile damage bonuses use the wrong stage of the attack

**Trigger and result.** Spawn a modern-format NPC with a nonzero bonus in its authored damage dice. The school acolyte at vnum 3700 has `2d4+30` in both the reference area and the shipped snapshot. ROM24 stores 30 in the NPC's damage roll when creating it. For unarmed attacks it rolls only the dice before applying victim posture, and it adds scaled damage roll afterward whether the mobile is armed or unarmed. Python spawns the acolyte with `dam_roll = 0`, adds 30 directly to the unarmed base, and skips the dice bonus entirely with a weapon.

**Reproduction.** Created the acolyte with the production mobile factory and fixed the base dice result at 8, total proficiency at 100, and the shared strength contribution at 6. Against a resting opponent the unarmed calculation returned 63, compared with ROM's `8 × 3 / 2 + 30 + 6 = 48`. Against a standing opponent with a modern `2d4` weapon and no shield the same mobile returned 14, compared with ROM's `8 × 11 / 10 + 30 + 6 = 44` before common damage reduction. This comparison isolates the bonus stage using equivalent formula inputs.

**Fix boundary.** Initialize the mobile's base damage roll from the authored bonus, roll only dice in the modern unarmed branch, and preserve later effect and strength contributions. Verify armed and unarmed attacks, proficiency scaling, and standing and downed victims. Legacy-format conversion needs its own comparison.

[ROM24 acolyte prototype](C:/Users/scott/PycharmProjects/PyRom/Rom24/area/school.are:8) · [ROM24 mobile initialization](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1567) · [ROM24 damage calculation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:514) · [ROM24 damage-roll stage](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:577) · [Python mobile initialization](../../../src/mobile/MobileFactory.py#L154) · [Python attack calculation](../../../src/combat/CombatHandler.py#L1682)

## F03 · NPC area attacks merge different victims into one result

**Trigger and result.** An NPC with `OFF_AREA_ATTACK` fights a primary target while another player attacks it. ROM24 calls `one_hit` for each target, and damage messages and death state belong to that target. Springs applies damage to each separately, then folds their results into a single dictionary. The merge concatenates direct victim text and ORs the killed flag. Round construction attaches the merged victim text to the primary target alone. Vnum 3700 is one shipped mobile with the flag.

**Reproduction.** Drove the production NPC round and damage/death handlers with two real player models and controlled hit amounts. The primary took one damage and remained at 24 HP. The secondary died and respawned at 1 HP. The round result reported `killed=True` and attached both direct hit strings to the primary player's payload. Hit selection and text generation were controlled to make attribution observable. Corpse creation and round construction ran locally.

**Fix boundary.** Keep the target and aftermath on each hit until delivery, preserving the attack order and leaving shared round-level logic with the primary target. Test a living primary and lethal secondary, a primary death before the sweep, and distinct direct recipients.

[ROM24 area attack loop](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:262) · [ROM24 victim delivery](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2098) · [Python area hit merge](../../../src/combat/CombatHandler.py#L1106) · [Python round recipient](../../../src/combat/CombatHandler.py#L1275) · [Python payload merge](../../../src/combat/CombatHandler.py#L1446)

## F04 · An unswitched follower can cast when ordered

**Trigger and result.** Give an awake, charmed and unswitched NPC the order `cast armor`. ROM24's `do_order` interprets the command as the follower, then `do_cast` exits for an NPC without a descriptor before any spell costs or effects. Springs dispatches through the same nested interpreter as other orders. The cast handler and authored guards accept the mobile using NPC proficiency and do not require a controlling session. A probe through the shipped `order` and `cast` command lambdas, with a successful proficiency roll, took the follower from 100 to 95 mana, added 12 pulses of wait, and applied `spell.armor`.

**Fix boundary.** Enforce controlled-body eligibility at ordinary cast entry using the effective actor's session or controller. Nested execution can inherit the issuer's connection, so a nonempty command connection alone is insufficient. Cover the unswitched order, a genuinely switched NPC, and independent mobile-special spell execution.

[ROM24 order dispatch](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:1679) · [ROM24 cast eligibility](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c:307) · [Python nested order](../../../src/player/PlayerHandler.py#L730) · [Inherited connection](../../../src/player/PlayerHandler.py#L640) · [Python cast entry](../../../src/interp/commands/Fight.py#L104) · [NPC casting proficiency](../../../src/api/SpellApi.py#L51)

## F05 · A follow-up hit leaves an engaged victim downed

**Trigger and result.** A victim already has a combat target, is resting after a knockdown, has positive HP, and has a ROM idle timer of at most four ticks. ROM24 promotes the victim to fighting during damage setup even when their combat pointer is already set. The attack roll and damage formula for the current swing were already computed, so the posture change affects later swings. Springs changes position only when establishing a previously absent combat link. A probe with an existing combat link and a nonlethal one-point hit left the victim at `POS_RESTING` (5) instead of `POS_FIGHTING` (7). While that posture persists, later melee attacks retain the below-fighting AC and 1.5× base damage adjustments.

**Fix boundary.** Apply the active-victim posture transition at the shared damage boundary, while retaining the current opponent and respecting the idle-policy distinction. Verify the first follow-up swing's knockdown benefit, the subsequent swing's restored fighting posture, and the stunned or incapacitated exclusions. This finding uses the ordinary active-combat case. Exact idle timing remains a separate policy question.

[ROM24 damage setup](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:722) · [ROM24 posture modifiers](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:489) · [Python combat setup](../../../src/combat/CombatHandler.py#L1037) · [Python hit modifier](../../../src/combat/CombatHandler.py#L1075) · [Python damage modifier](../../../src/combat/CombatHandler.py#L1724)

## Coverage and verification

- All **1,728 tests across 137 top-level modules** passed in isolated Python processes with `src` on `PYTHONPATH`. The inventory covered 216 Python source files, 30 C translation units, and 17 collection snapshots. The legacy tests in `../../../tests/old-tests` were outside the sweep.
- Fresh combat tracing covered hit resolution, posture, NPC multi-attacks, combat escape, aggression, and defense gates. Spell and command tracing covered cast targeting, authored guards, orders, and nested dispatch. The query CLI checked the acolyte, offense flags, and the shipped cast and order documents.
- World and object sampling covered reset levels and ownership, item decay, movement and portals, shop stock, theft, and healer paths. Advancement, notes, visibility, equipment, specials, administrative commands, authentication, and sessions received regression coverage with selected source checks. The report does not claim per-branch parity or exhaustive comparison of content records.
- The previous review's F01–F03 and F05–F07 fixes are in the working tree and covered by the passing suite. The read-only character response now includes `pet`. A populated pet's live PUT/GET round trip and fresh-login restoration against the deployed service remain unverified. [Previous report](repository-rom24-parity-2026-11-12.md)
- No compiled C gameplay session or live persistence write was used. Explicit command abbreviations, idle limbo, and offline recovery remain open policy or contract questions. The timing of movement-triggered aggression was observed during the survey and remains outside the verified queue pending a decision on that gameplay behavior.

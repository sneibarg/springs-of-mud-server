# ROM24 magic parity review

Date: 2026-10-22. Python checkout: `17416e143977cc329cdf27e389ce780b6f3caeec` plus the working-tree files inspected during this review.

Reference: `C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic.c`, `magic2.c`, and `magic.h`. Python implementation: `src/api/SpellApi.py`, `src/skill/SpellContext.py`, `src/interp/commands/Fight.py`, item casting in `src/interp/commands/Object.py`, effect handling/utilities, and the current spell and cast-command collection snapshots.

## Scope and interpretation

This is a static behavioral review, with existing focused tests and two isolated effect-composition probes as supporting validation. Findings describe differences established from the inspected execution paths, not end-to-end reproductions in a running MUD. All 97 non-null spell declarations in `magic.h` have corresponding collection definitions; absence of a same-named Python function was not used as evidence of missing behavior. `spell_null` is a C sentinel, not a missing player spell. The inventory at the end records the declaration-to-data mapping.

The service/registry architecture, lambdas, dynamic enums, payload rendering, and designer ownership of spell content are accepted design choices. None is a defect. No documentation encountered established the gameplay changes below as intentional. Treat the listed behavior as a correction backlog, subject to confirming any desired balance changes with the designers. Priorities indicate gameplay impact: P1 broad correctness, progression, targeting or resource problems; P2 narrower mechanics; P3 feedback/detail differences.

References below are repository-relative `file:line` anchors. C anchors are relative to the reference checkout; Python/data anchors are relative to this repository. Collection anchors identify the document, with the relevant `lambdas`, `affectData`, or guards nearby. The findings intentionally group related discrepancies instead of counting every missing message or branch as a separate defect.

## Shared casting and effect machinery

### M01 — P1: Cast accepts spells without learned/class access checks

**Addressed 2026-10-23:** Added cast-command collection guards for class level and nonzero learned spell proficiency, before mana/target-error guards. They reuse `FightUtil.level_for_class`, `Character.get_learned` and `Character.learned_entry_level`; NPCs retain the C exemption. No runtime Python changes were needed. `tests.test_combat_dynamic_commands.TestFightDynamicCommands` passes all 6 tests, including 8 cast-access scenarios covering absent/zero proficiency, class-level boundaries, a different class requirement, rejection before mana charging/execution, and the NPC exemption. This status applies only to M01; the remaining casting findings are separate.

**Evidence:** C `magic.c:80`, `magic.c:324`; Python `src/interp/commands/Fight.py:101`, `src/util/FightUtil.py:49` (`find_spell`), `resources/collections/SOMDB.Commands.json:990` (cast document).

**Trigger/expected/actual:** A player names a spell present in the registry but has not learned it, or is below its class level. C rejects it. Python checks whether a registry entry exists and whether mana/target checks pass; neither `do_cast` nor its collection guards checks learned proficiency or class access. The nearby `_has_skill_access` helper is not called by `do_cast`. A player can therefore use spells outside normal progression. Add a regression for an unlearned spell and an under-level caster before execution or resource changes.

### M02 — P1: Spell position, proficiency failure, recovery and improvement are omitted

**Addressed 2026-10-23:** The cast collection now guards the spell's minimum position before target-error and mana guards. A reusable `SpellApi.cast` attempt operation announces, sets recovery without shortening an existing wait, rolls spell proficiency (including NPC, daze and drunkenness rules), charges half mana and checks failed improvement on concentration failure, or charges full mana before execution and checks successful improvement afterward. Non-mana classes cast at three-quarters level; explicit cast levels are preserved, and direct/room effect operations receive the effective level. Existing item/script lambda execution remains separate. The focused cast-command, spell-payload and object-spell tests pass (35 tests total). Retaliation remains the separate M08 finding.

**Evidence:** C `magic.c:335`, `magic.c:530`; Python `src/interp/commands/Fight.py:101`, `resources/collections/SOMDB.Commands.json:990`, `src/skill/SpellContext.py:56`.

**Trigger/expected/actual:** Cast a standing-only spell while fighting, or repeatedly cast with low proficiency. C checks the spell's minimum position, applies its `beats`, rolls skill success, charges half mana on concentration failure, and calls `check_improve`. Python uses the cast command's general fighting position, executes the lambda directly, and has no corresponding spell-level wait, concentration roll, or improvement call. Non-mana classes also receive full actor level rather than C's `3 * level / 4`. Verify position rejection, one failed roll, recovery beats, improvement, and effective cast level independently.

### M03 — P1: Mana is minimum-only and spell rejection is free

**Addressed 2026-10-23:** `FightUtil.cast_mana_cost` implements the actual `do_cast` class-level formula, its 50-mana zero-divisor special case, and C-style integer division. Target validation precedes insufficient mana; the mana guard preserves the NPC exemption. The shared normal-cast attempt announces before concentration and charges before spell execution, independent of `performed`, so saved, duplicate and component-rejected spells no longer receive free retries after successful concentration. Regression coverage includes unlock-level costs, odd half-cost truncation, equality on the proficiency roll, rejected spell effects, and pre-attempt guard rejection without charging. The separate C `mana_cost()` helper's 1000 special case is not used for normal casting.

**Evidence:** C `magic.c:341`, `magic.c:520`; Python `src/interp/commands/Fight.py:104`, `src/interp/commands/Fight.py:135`, `src/util/FightUtil.py:45` (`min_mana`), `src/api/SpellApi.py:180`, `src/api/SpellApi.py:208`.

**Trigger/expected/actual:** Cast near the class unlock level, into a successful save, or on an already affected target. C uses `max(min_mana, 100 / (2 + caster_level - class_spell_level))` for ordinary eligible casts and pays before entering the spell function. Python always uses `min_mana` and deducts only when `performed` is true. Save/duplicate/invalid-component returns commonly leave it false, allowing free retries. Utterances are also conditional on `performed`, whereas C announces before concentration and spell execution. Test a saved blindness and rejected portal as well as the near-unlock mana formula. C's separate `mana_cost()` helper has a different special case from `do_cast`; use the actual caller's formula.

### M04 — P1: Ordinary spell saves bypass immunity and caster-class adjustment

**Addressed 2026-10-23:** The shared save utility applies the PC mana-class adjustment independently of the optional immunity callback. Reusable `SpellApi.saves_spell` supplies the existing combat immunity resolver, effective level and selected target. Ordinary damage/area spells now pass their damage type; existing blindness/weaken collection save gates use DAM_OTHER, and existing poison/charm/sleep, movement, energy-drain and chill-touch save sites use their reference types and level adjustments. The remaining plague-spread caller now supplies DAM_DISEASE and the same resolver. Already-typed elemental/poison exposure paths retain their behavior. No collection changes or new files were needed for M04. Missing save branches and other spell-specific mechanics remain in their separate findings (for example M25/M31).

Validation: 104 targeted tests passed across effect utilities, spell payloads/save gates, acid/elemental/poison exposure, cast commands, object spells, weapon effects, visibility, and one plague-spread regression. New coverage checks strict probability endpoints, bounds, resistance/vulnerability, berserk/class adjustment ordering, the NPC exception, unconditional class adjustment, immunity without a random roll, typed target/level forwarding, and the actual blindness collection sequence stopping before effect application. The plague test initially stalled in the sandbox while Python created its Windows asyncio socket pair; it passed outside the sandbox. No full-suite pass is claimed.

**Evidence:** C `magic.c:213`; Python `src/util/EffectUtil.py:215`, `src/api/SpellApi.py:208`, `src/api/SpellApi.py:334`, `src/api/SpellApi.py:487`.

**Trigger/expected/actual:** A resistant, vulnerable, immune, or mana-class victim is targeted by an ordinary spell. C always runs `check_immune` for the actual damage type and applies the mana-class 90% save adjustment. Python only runs those branches when an optional `immunity` callback is supplied; ordinary `damage_expr` and `stop_if_saved` supply neither the callback nor the actual damage type (they pass `0`). Thus HP immunity downstream does not restore correct spell-save probabilities or prevent save-gated debuffs. The newer elemental-breath and poison-cloud paths do supply the callback and should not be changed indiscriminately. Test save thresholds and immune debuffs through the real helper call sites.

### M05 — P1: Multi-part effects collapse, and object entries leak into character effects

**Addressed 2026-10-23:** Shared spell-effect application now adds independent character records by default and filters object/weapon templates away from characters (and character templates away from objects). Filtering accepts the existing `item`/`object` aliases and named or numeric `where` values. A reusable `join=True` option is exposed through `SpellApi.apply_affect_data`; plague's collection lambda explicitly opts in, preserving its accumulating effect behavior. The underlying ROM-style type-based `affect_join` operation remains unchanged. Flag restoration after partial character-effect removal now normalizes named/numeric bits and restores only the shared flag, without reapplying a surviving record's stat modifier.

Validation: 57 focused tests passed across effect utilities/application, spell payloads, consumption and object-spell paths. Regressions load current bless/curse/frenzy/calm/invisibility/plague documents and verify separate stat records and durations, target filtering, reversal on removal and expiration, shared-flag ownership, effective-level/join forwarding, and explicit plague accumulation. No new files were needed. Spell-specific guard omissions, frenzy division and calm's PC magnitude remain the separate M25/M28, M07 and M35 findings.

**Evidence:** C `magic.c:767`, `magic.c:1676`, `magic.c:2827`, `magic.c:950`; Python `src/item/EffectHandler.py:224`, `src/item/EffectHandler.py:247`, `src/api/SpellApi.py:218`; data `SOMDB.Spells.json:117` (bless), `:535` (curse), `:2721` (frenzy), `:2880` (calm).

**Trigger/expected/actual:** Apply bless, curse, frenzy or calm to a fresh character. C adds separate effects for each stat. Python calls `affect_join` for every entry; it matches only spell type, removes the previous entry, adds its duration/modifier to the next entry, and leaves only the last location. At level 24, frenzy's intended three effects (+4 hit, +4 damage, +20 AC, each duration 8) become one +28 AC effect with duration 24. In addition, the `elif not hasattr(victim, 'item_type')` branch accepts object-only entries on characters. Bless/curse/invisibility therefore process object metadata too. Fix target filtering and distinguish add-versus-join semantics before adjusting individual spell values. Test actual stat changes, effect count, flags, duration, and reversal on expiration.

### M06 — P2: Dispel removes individual records rather than the whole spell

**Addressed 2026-10-23:** A failed dispel save now strips every matching spell record and stops further rolls, returning the removed records for payload rendering. Saved records lose one level without a zero clamp. Removal feedback is deduplicated by spell type, so multi-part effects produce one wear-off message. Regressions cover a saved record followed by a failed save, complete stat restoration, unrelated effects, all-saved records weakening below zero, no-match calls without rolls, and duplicate wear-off suppression.

**Evidence:** C `magic.c:254`; Python `src/item/EffectHandler.py:275`.

**Trigger/expected/actual:** A spell has several affect records, or several matching records from different sources. C attempts records until a failed save permits stripping all records with that spell ID, then returns; saved records lose one level. Python rolls each record independently and removes only that record, permitting partial spell removal. It also clamps weakening at zero where C decrements. Test a two-record spell with a save followed by a failed save, including the remaining effect list and number of rolls. This becomes more visible after M05 is fixed.

### M07 — P2: `number_fuzzy` probabilities and intermediate integer division differ

**Addressed 2026-10-23:** Both effect expressions and spell expressions delegate fuzzy rolls through a reusable `EffectUtil.number_fuzzy` wrapper to the existing ROM-compatible `RandomNumberGenerator.number_fuzzy`. Four controlled rolls verify offsets -1/0/0/+1 and the minimum of one. Frenzy's designer-authored AC expression now uses `10 * (level // 12)`; level-boundary regressions verify the intermediate integer division at 11/12/23/24/25. This is a targeted positive-level formula correction, preserving the expression evaluator's existing division semantics for other designer content.

**Evidence:** C `db.c:2938`, `magic.c:2827`; Python `src/util/EffectUtil.py:12`, `src/util/EffectUtil.py:125`, `src/api/SpellApi.py:1053`; data `SOMDB.Spells.json:2721`.

**Trigger/expected/actual:** Generate fuzzy durations for charm/pass door/fireproof, or evaluate frenzy AC at levels not divisible by 12. C fuzzy offsets are -1/0/+1 with probabilities 1/4, 1/2, 1/4; Python chooses all three equally. Python expression `/` retains fractions until final `int`: frenzy's `10 * (level / 12)` at level 23 yields 10 in C and 19 in Python. This changes buff magnitude. Use intermediate C integer semantics where required, rather than globally replacing division without examining negative operands. Test level 23 and the fuzzy distribution mapping with controlled random inputs.

### M08 — P1: Player offensive-cast retaliation differs from C

**Addressed 2026-10-23:** The cast collection contains the charmed-master restriction. A reusable guard filter permits evaluation in phases: eligibility/position/target safety first, then caster killer checks, then remaining follower/mana checks in the C target-type-specific order. Notices survive a later guard rejection. Mixed object/character offense uses spell safety for both explicit and implicit character targets, and ordinary offensive NPC targeting retains C's safety exemption. Approved normal casts mark the caster before announcement/concentration and check retaliation after every attempt, independent of `performed`. The target retaliates via `check_killer(victim, caster)` and `multi_hit`, with nested payloads attributed to that target; followers, self, busy or departed targets do not retaliate. Current room membership is checked, and no fighting state is forced. Regressions include failed concentration, resisted/no-effect spells, sleeping victims using the real combat path, and existing item-spell retaliation. Charm relationship completion is documented in M23.

**Evidence:** C `magic.c:395`, `magic.c:567`; Python `src/interp/commands/Fight.py:135`, `src/interp/commands/Fight.py:444`, `src/api/SpellApi.py:138`.

**Trigger/expected/actual:** Cast a saved offensive debuff at an idle victim, cast sleep/charm successfully, or cast while charmed against the master. C performs target sanity/master checks, and after a completed cast attempt an eligible victim still present in the room immediately `multi_hit`s the caster, except the caster's follower. Python has no master check here and only calls `start_offensive_combat` after `performed`; that helper simply sets both fighting states without the follower exception, immediate retaliation, or checking the victim is still in the caster's room. Saved effects can avoid retaliation; sleep/charm successes can be put straight into combat. Item casting has a separate `_item_spell_retaliation` path and is not evidence that player casting is correct. Test saved debuffs, followers, and targets moved by spell execution.

### M09 — P2: Prefix spell lookup is lost

**Addressed 2026-10-23:** `FightUtil.find_spell` accepts an optional caster for deterministic ROM-style prefix resolution. It sorts by canonical spell handler name, selects the first learned and class-accessible match for PCs, and returns the first match when none is accessible so existing guards reject it. NPCs take the first matching spell. Player casting supplies the caster; exact content-reference lookup remains available to item/script callers without a caster. Tests use reversed registry input, ambiguous cure prefixes, under-level/unlearned matches, NPCs, exact names, normalized handler names, and missing input.

Validation for M06–M09: 192 targeted tests passed: effect utilities/application (16), spell payloads (20), complete combat aggression (69), complete dynamic command/payload tests (16), object casting/retaliation/consumption (36), and acid/elemental/poison exposure (35). Payload coverage also confirms that announcements preserve earlier killer notices. The two complete combat modules ran outside the sandbox to allow Windows asyncio's internal socket pair. Collection changes were dry-run reviewed and queried afterward. The command collection's atomic replacement was denied by Windows, so the reviewed guard insertion was applied in place and verified. No new files were created, and no full-suite pass is claimed.

**Evidence:** C `magic.c:58`, `magic.c:80`; Python `src/util/FightUtil.py:49` (`find_spell`).

**Trigger/expected/actual:** A player uses a spell-name prefix accepted by ROM, or two spells share that prefix. C prefix-matches and prefers an accessible learned spell. Python accepts only the exact name or normalized exact handler ID. Restore intended lookup behavior with tests for ambiguous prefixes and accessible-versus-unlearned candidates; do not assume changing collection names alone restores this.

## Damage and combat spells

### M10 — P1: Seven classic damage-table spells use unrelated level dice

**Addressed 2026-10-23:** Restored all seven C `dam_each` arrays in designer-editable `tables.damage` fields. Reusable `SpellApi.damage_table` clamps the effective level for the uniform inclusive roll, typed save and failed-save follow-up without changing the caller's cast level. `damage_expr` supports a failed-save callback before damage. Chill touch's collection applies its strength effect with joining through the same cold save; the effect and its room message are data-owned. Colour spray invokes the existing blindness content at half the bounded level through reusable `invoke_spell`, preserving blindness's own duplicate check, save, effects and payload handling. Child spell termination does not stop the parent damage. The obsolete specialized chill-touch implementation was removed.

Validation: 196 targeted tests passed: spell payload/table behavior and effect application (40), complete combat/dynamic command modules (85), object casting/retaliation/consumption and elemental exposure (71). Regressions exercise negative/zero levels, first nonzero entries, levels 49/50/100, both uniform roll endpoints, save halving and bounded typed saves for every table; chill-touch effect ordering, stacking and removal; and colour-spray blindness success, save and already-blind branches. All table entries were extracted from and checked against the local C source. Collection changes were dry-run reviewed, written through devtools and queried afterward. No full-suite pass is claimed.

**Evidence:** C `magic.c:877` (burning hands), `:1361` (chill touch), `:1402` (colour spray), `:2660` (fireball), `:3560` (lightning bolt), `:3648` (magic missile), `:4177` (shocking grasp). Python/data `SOMDB.Spells.json:228`, `:315`, `:340`, `:872`, `:1016`, `:1066`, `:1517`; `src/api/SpellApi.py:1009`.

**Trigger/expected/actual:** Cast these at a fixed level. C clamps the effective level to its `dam_each` table, then rolls uniformly from half to twice its entry. Python uses `dice(level, sides)` with sides 7/5/6/10/7/4/5 respectively. Damage distribution, scaling, and save level beyond the table bounds differ substantially. For example level-50 burning hands uses C entry 48 (24–96 before save), versus Python 50d7 (50–350). Colour spray also omits its failed-save blindness at half level. Chill touch rolls damage save and strength-effect save separately after damage; C uses one save and applies the strength effect before damage. Keep tables/formulas in designer-editable data and test boundary levels plus the shared-save outcome.

### M11 — P2: Cause spells gain a saving throw absent in C

**Addressed 2026-10-23:** Cause light, cause serious and cause critical now explicitly pass `save_half=False` to the existing reusable `damage_expr` operation in their collection lambdas. Their damage formulas and `DAM_HARM` routing are preserved. No runtime Python changes or new files were needed. A collection-backed regression executes all three spells with a save mock that would succeed, verifies that no save is rolled, and checks the full C-formula damage and d8 roll count. All 24 spell payload/behavior tests passed. Collection changes were dry-run reviewed, written through devtools and queried afterward.

**Evidence:** C `magic.c:1182`, `:1190`, `:1198`; data `SOMDB.Spells.json:1695`, `:1720`, `:1745`; Python `src/api/SpellApi.py:334`.

**Trigger/expected/actual:** Cause light/serious/critical hits a victim whose save succeeds. The damage expressions match C, but the default `save_half=True` halves their damage; C directly calls `damage` without a spell save. Specify the appropriate save policy in the collection and test that no save roll occurs.

### M12 — P1: Harm has no C damage bounds

**Addressed 2026-10-23:** Harm's collection expression now starts at `max(20, victim.hit - d4)`, halves on its typed harm save, caps saved damage at 50 and final damage at 100. A reusable `post_save_expression` option on `damage_expr` keeps those bounds in content. The obsolete specialized harm method was removed. Regression cases cover low HP, odd save halving, the 100-point boundary and large HP pools.

**Evidence:** C `magic.c:2961`; Python `src/api/SpellApi.py:1035`.

**Trigger/expected/actual:** Harm targets a high-HP victim or one near death. C starts at `max(20, hit - d4)`, caps saved damage at 50 and final damage at 100. Python starts at `max(0, hit - d4)` and only applies generic save-halving. It can remove nearly all of a large HP pool, and deals less than C's minimum at low HP. Test both extremes and the saved cap.

### M13 — P1: Energy drain removes levels instead of experience and drains different resources

**Addressed 2026-10-23:** Energy drain's content pipeline shifts alignment before the negative save (except self-casts), returns with the victim's chill message on a save, and uses the C low-level branch of caster HP plus one damage. Other victims lose a level-based random amount of experience through the existing `CharacterAdvancement.gain_experience` service, halve mana and movement, take one dlevel damage roll, and heal the caster by that roll without a max-HP cap. Levels are never decremented and victim HP changes only through combat damage. Reusable resource-expression, content-message and conditional-stop operations support the data pipeline; the specialized energy-drain method was removed. Tests cover save ordering, alignment floor/self exemption, levels 1/2, odd resources, roll ranges, uncapped healing, player/NPC/hero experience handling and the existing experience floor. Experience uses this server's current/accumulated progression model and its existing zero floor rather than importing C's cumulative-experience storage representation.

**Evidence:** C `magic.c:2623`; Python `src/api/SpellApi.py:885`; data `SOMDB.Spells.json:847`.

**Trigger/expected/actual:** Drain an ordinary victim above level 2. C lowers caster alignment, subtracts random experience, halves victim mana/move, rolls 1dlevel damage and adds that damage to caster HP. Python directly decrements victim level, subtracts level from mana and HP, heals caster by level with a cap, then inflicts another level damage; it does not drain movement or experience. A successful save still takes 1 damage rather than returning, and the C low-level lethal branch is absent. This can corrupt progression rather than perform the intended drain. Test saves, level <=2, experience, alignment, mana, movement, HP, and actual damage separately.

### M14 — P1: Ray of truth reverses protected alignment and omits backlash/blindness

**Addressed 2026-10-23:** Ray of truth's data pipeline redirects evil casters (including the -350 boundary) onto themselves, protects good victims at +350, rolls level d10 with a holy save, then applies the C nonlinear alignment multiplier with truncation toward zero. It invokes existing blindness content at three-quarters level after damage, independently of the damage save, and restores the original cast target for normal retaliation. Messages live in the spell payload, including backlash and protection recipients. The specialized ray method was removed; generic post-save expressions and existing spell invocation handle the behavior. Regression coverage includes both alignment poles, neutral and boundary targets, the -651 compression boundary, save-before-multiplier rounding, backlash, blindness success/save and target restoration.

**Evidence:** C `magic.c:3929`; Python `src/api/SpellApi.py:770`.

**Trigger/expected/actual:** Target a good or evil creature, or cast as an evil character. C protects good victims, redirects an evil caster's ray onto the caster, computes saved level-dice damage with a nonlinear alignment multiplier, and invokes blindness at 3/4 level. Python declares evil victims unaffected, damages good victims, uses `level * 10 - alignment // 10` without a save, and has no backlash or blindness. Test both alignment poles, neutral targets, evil caster, and blindness save independently.


Validation for M12–M14: 206 targeted tests passed: spell payload/behavior and effect application (50), full dynamic-command/combat modules (85), and object casting/retaliation/consumption plus acid/elemental/poison exposure (71). Collections were dry-run reviewed, written with devtools and queried afterward. No new files were retained and no full-suite pass is claimed.

### M15 — P1: Dispel evil/good and demonfire omit alignment targeting

**Addressed 2026-10-23:** Dispel evil/good now use collection conditions for player-only caster backlash, protected alignments and neutral immunity. Their damage expression uses the C low-HP branch (including its actor-level threshold), with the appropriate holy/negative save. Demonfire redirects non-evil players before shifting alignment by -50, rolls level d10 with a negative save, and invokes curse at three-quarters level after damage. Original cast targets are restored for retaliation. Formulas, conditions and messages remain content-owned; the only additional alignment helper is a reusable NPC predicate. Curse's existing content now checks the character's curse flag and negative save before applying effects, so the chained curse behaves correctly; object application still bypasses those character checks. This addresses the curse-character subset of M25, not its other spells or the separate object-curse finding.

**Evidence:** C `magic.c:1950`, `:1981`, `:1755`; data `SOMDB.Spells.json:772`, `:2978`, `:2780`.

**Trigger/expected/actual:** Use dispel evil/good on a protected or neutral alignment, or as a player of the forbidden caster alignment. C can redirect to caster, return without damage on protected/neutral victims, and uses a special low-HP damage branch. Python always damages the chosen target with level d4. Demonfire in C redirects non-evil player casters, shifts alignment -50, deals level d10 and casts curse at 3/4 level; Python deals level d4 +20 to the chosen target and does none of those side effects. Add alignment-matrix regressions and chained-effect checks.

### M16 — P1: Chain lightning omits safety, saves, repeated arcs and caster rebound

**Addressed 2026-10-23:** Replaced the specialized one-pass chain-lightning method with reusable `chain_damage`. Spell data supplies level d6 damage, decrement 4, save divisor 3 and first/arc/rebound/fizzle message keys. The initial target is hit directly; later room sweeps invoke `is_safe_spell(..., area=True)`, exclude only the last victim, repeat sweeps, and rebound onto the caster when no eligible target exists. Consecutive caster rebounds ground out. The C inner-sweep ordering is retained even if level reaches zero or below mid-sweep (nonpositive dice counts produce zero damage); subsequent saves use each arc's effective level. Scoped contexts preserve the caller's cast level and target. Removed room occupants are skipped on later traversal; caster removal ends subsequent sweeps. Traversal uses the server's existing ordered player/mobile room collections rather than introducing a new room roster representation.

**Evidence:** C `magic.c:1204`; Python `src/api/SpellApi.py:839`.

**Trigger/expected/actual:** Cast in a room with protected bystanders or no eligible second target. C rolls level d6 (one-third on save), reduces level by four per arc, searches safe eligible targets repeatedly, and can rebound onto caster. Python builds a one-pass list of all other occupants, starts at `4 * level`, halves each subsequent amount, and performs no spell safety/save check in that loop. The damage handler's own safety does not reproduce area targeting eligibility, repeated arcs or rebound. Test a safe/grouped bystander, one target only, multiple rounds of arcs, and saved damage.


Validation for M15–M16: 215 targeted tests passed: spell payload/behavior (42), effect application and object casting/retaliation/consumption plus elemental exposure (88), and complete dynamic-command/combat modules (85). New collection-backed regressions cover player/NPC and alignment matrices, dispel HP/actor-level boundaries, demonfire save/curse ordering, curse save and duplicate rejection, object-curse guard exemption, chain safety filtering, repeated targets, one-third saves, decrement ordering, rebound, target extraction and grounding. Existing combat safety tests cover actual group/protection rules; chain tests verify that the runtime delegates area eligibility to that helper. Collection edits were dry-run reviewed, written through devtools and queried afterward. No new files were retained; no full-suite pass is claimed.

### M17 — P1: Holy word is a different spell and has no caster exhaustion

**Addressed 2026-10-23:** Holy word is now a content pipeline using reusable room iteration, alignment-group predicates and spell invocation. Matching alignments (including neutral) receive frenzy then bless, with the caster included. Opposite good/evil alignments receive curse and unsaved level d6 energy damage when area safety permits; neutral casters curse non-neutral victims at half level and inflict unsaved level d4 energy damage. Non-neutral casters leave neutral bystanders alone. Caster movement becomes zero and HP halves after the room effects. Supporting collection prerequisites prevent duplicate/fighting-character bless and duplicate/berserk/calmed/mismatched-alignment frenzy, including when invoked by holy word. Existing child-spell message payloads are reused; child prerequisite rejection feedback was subsequently added in the guard-focused follow-up. The obsolete specialized holy-word implementation was removed.

**Evidence:** C `magic.c:3173`; Python `src/api/SpellApi.py:851`.

**Trigger/expected/actual:** Cast with same/opposite/neutral-alignment room occupants. C grants same-alignment frenzy+bless, curses and damages opposing alignments (energy damage), supports neutral casters, then zeros caster movement and halves HP. Python rejects neutral casters, heals allies and caster, applies different damage formulas/types, omits bless/frenzy/curse, and never exhausts the caster. Test the full alignment matrix and final caster state.

### M18 — P2: Call lightning ignores outdoor/weather prerequisites and target-side rule

**Addressed 2026-10-23:** Call lightning's collection now rejects indoor and non-raining casts before rolling damage. It rolls `dice(level // 2, 8)` once, stores that amount for the whole cast and attacks only the opposite NPC/player side in the room, with independent typed saves. It intentionally does not add an area-safety prefilter absent from this C spell. Reusable weather/outdoor predicates and area-message routing send the distant lightning notice only to awake outdoor occupants in other rooms of the same area. The specialized call-lightning method was removed; rules, formulas and messages remain content-owned.

**Evidence:** C `magic.c:902`; Python `src/api/SpellApi.py:1029`, `:487`.

**Trigger/expected/actual:** Cast indoors or in clear weather, or in a mixed room. C requires outdoors and rain, rolls `dice(level/2, 8)` once, and attacks only the opposite NPC/player side. Python only requires a weather object and calls generic area damage using `dice(level, 4) + level // 2`, rolled per victim, without the opposite-side filter. It omits the outdoor/awake same-area lightning notice. Test prerequisites, side selection, and one shared base roll.

### M19 — P2: Earthquake damages flyers and introduces a save

**Addressed 2026-10-23:** Earthquake now uses reusable filtered room iteration with area safety. Its collection expression calls zero bash damage for flying victims and unsaved `level + dice(2, 8)` for grounded victims. Flyers still go through the damage operation, and no saving throw occurs. Cast and same-area distant tremor notices are defined in the spell payload; distant notices are not restricted by indoors or sleep state.

**Evidence:** C `magic.c:2188`; data `SOMDB.Spells.json:797`; Python `src/api/SpellApi.py:487`.

**Trigger/expected/actual:** An eligible flying victim is present. C calls zero damage for flyers and unsaved `level + 2d8` for grounded targets, plus area tremor notices. Python gives all eligible victims generic save-halved damage regardless of flight and omits the wider notice. Test grounded/flying targets with a forced successful save.

### M20 — P2: Breath damage omits caster HP; gas also misses the C NPC exclusion

**Addressed 2026-10-23:** All five breath documents now supply their HP minimum, range divisors and die sides to reusable `breath_damage`, retaining the C `max(hp_damage + dice_damage // 10, dice_damage + hp_damage // 10)` formula. Gas preserves this checkout's fixed upper endpoint 8; a reversed range returns its lower endpoint as C's number_range does. Its content-defined room target filter excludes NPC-on-NPC victims if either is fighting the other. The existing acid/elemental/poison exposure operations and their pre-damage/save/collateral scaling remain in place. Damage depends on current caster HP and is shared across area-breath victims as before.

**Evidence:** C `magic.c:4467`, `:4496`, `:4552`, `:4609`, `:4647`; data `SOMDB.Spells.json:2314`, `:2367`, `:2405`, `:2436`, `:2475`; Python `src/api/SpellApi.py:334`, `:415`, `:487`.

**Trigger/expected/actual:** A wounded versus healthy breather uses the same spell level. Every C breath combines a random HP-derived component with level dice via `max(hp_dam + dice_dam/10, dice_dam + hp_dam/10)`. Python uses level dice only. Existing elemental exposure scaling is present and is not missing wholesale. Gas additionally omits C's explicit exclusion for NPC-on-NPC targets when either is fighting the other (the unusual condition in this checkout is the reference). Test HP-sensitive damage and that exact NPC condition. Preserve the already implemented exposure-before-damage ordering.

### M21 — P2: Heat metal never removes/drops equipment and can damage without heatable items

**Addressed 2026-10-23:** Heat metal now invokes reusable equipment heating over all owned items. It performs the initial level+2 fire save and raw fire-immunity check, per-item eligibility and save rolls, nonmetal/burn-proof exclusions, worn flaming-weapon exemption, no-drop/immortal rules, armor weight-versus-current-dexterity check and existing equipment removal. Successful drops remove item effects through the existing equipment machinery and transfer the item to the room; failed removals leave it owned. Content-owned item rules choose damage contributions for worn/carried armor/weapons and dropped/stuck outcomes. Empty/fully protected inventories produce no damage; successful outcomes (including zero summed damage) receive the final two-thirds fire save and one damage operation. No-effect, removal, drop and searing messages live in the spell payload. A defaulted optional Spell.rules field carries designer-authored outcome rules; the specialized heat-metal method was removed.

**Evidence:** C `magic.c:3036`; Python `src/api/SpellApi.py:873`.

**Trigger/expected/actual:** Target someone with no metal equipment, or with droppable/worn metal armor and weapons. C gates on saves/fire immunity, evaluates carried items, `ITEM_NONMETAL`/burn-proof flags, weight/dexterity/removal/drop checks, and accumulates damage from those outcomes. Python always deals `dice(level, 2)` plus a small material-name bonus, scans only equipped attributes, and never removes/drops anything. Test no eligible item, burn-proof and nonmetal items, and both successful/failed item removal.


Validation for M17–M21: 226 targeted tests passed: spell payload/behavior (53), effect application and object casting/retaliation/consumption plus acid/elemental/poison exposure (88), and complete dynamic-command/combat modules (85). New collection-backed cases cover all holy-word alignment branches, safety and exhaustion; invoked buff restrictions; call-lightning prerequisite rejection, shared roll, player/NPC side selection and distant-recipient filters; earthquake grounded/flying/protected targets with a forced successful save; HP-sensitive damage for every breath, reversed gas ranges and both NPC fighting directions; and heat-metal worn/carried armor/weapon outcomes, flags/immunity, final saves, strict weight bounds, failed removal, effect removal, room transfers and zero-damage drops. Collection changes were dry-run reviewed, written through devtools and queried afterward. No new files were retained. This is focused validation, not a full-suite or live-server parity claim.

## Buffs, ailments and dispelling

### M22 — P1: Sleep has no persistent sleep affect

**Addressed 2026-10-23:** Sleep retains its collection prerequisites (raw AFF_SLEEP, NPC undead, level+2 limit and level-4 charm save) and persistent joined AFF_SLEEP effect lasting 4+level. Its success messages are now owned by the spell payload and emitted only for awake victims: the victim receives the sleepy notice, and everyone else in the room, including a player caster, receives the sleep notice. The runtime now uses the existing CharacterApi.set_position operation to update both canonical character_attributes.position and the direct position field; the prior direct-field assignment could leave the position API reading an awake state. Naturally sleeping and unconscious victims still receive the affect but keep their position and receive no extra success notices.

Validation: 259 targeted tests passed: spell content/payload/guards (73), effect application, movement commands, object casting/retaliation/consumption and elemental exposure (101), and complete dynamic-command/combat modules (85). New tests execute real sleep collection content with the actual effect handler and position API, checking standing/resting/fighting/asleep/stunned/dead targets, self and NPC casts, exact messages/recipients and both position fields. A cast-to-wake regression runs the real stand and targeted-wake methods with real position/affected-bit checks: both refuse while AFF_SLEEP remains, the flag survives the tick decrementing duration to zero, and expiration or a successful dispel removes it and permits waking. Ending the effect does not automatically stand the victim. Existing guard cases cover invalid targets and save ordering. The message edit was dry-run reviewed, written with devtools and queried afterward. No new files were retained and no full-suite/live-server claim is made.


**Evidence:** C `magic.c:4202`; Python `src/api/SpellApi.py:983`; data `SOMDB.Spells.json:1263` (`affectData: []`).

**Trigger/expected/actual:** Sleep passes its save. C rejects undead/over-level victims and adds AFF_SLEEP for `4 + level`, then sleeps awake victims. Python marks an empty affect application performed and changes position, with no AFF_SLEEP or expiration state; it also lacks undead/level guards. Player cast combat-start handling compounds this (M08). Add tests for the actual effect record, duration, natural wake restrictions and invalid victims.

### M23 — P1: Charm lacks follower relationships and most eligibility rules

**Addressed 2026-10-23:** Existing content guards preserve C ordering for safety, self, charm on either participant, victim level, IMM_CHARM, the typed save and the victim-room law flag. A reusable follow operation now detaches the old master, clears its pet pointer when applicable, establishes the caster as master and group leader, and sends visibility-gated follow notices before the charm affect. Follow and charm-success messages live in content. Tests exercise visible/invisible old/new-master notices, transfers, NPC followers, group membership, affect ordering and the existing M08 retaliation exclusion for the newly established master.

**Evidence:** C `magic.c:1313`; Python `src/api/SpellApi.py:973`; data `SOMDB.Spells.json:278`.

**Trigger/expected/actual:** Charm a higher-level, already charmed, charm-immune, or city-law victim; alternatively charm an eligible follower of another master. C checks all those conditions and charmed caster status, detaches old following, adds the new follower and sets leader. Python only rejects self and a generic save before applying AFF_CHARM. A flag alone does not establish control/following. Test relationship mutations, law, level, immunity and both charmed parties, then integrate with M08.

### M24 — P2: Change sex is permanent direct mutation with no save or duplicate guard

**Addressed 2026-10-23:** Change sex checks its spell record before DAM_OTHER, applies a temporary APPLY_SEX delta for 2*level, and preserves repeated random rolls until sex differs. Modifier expressions leave templates unchanged, and normal removal/expiration restores sex. Success now sends content-owned victim/room messages after the sex changes, with a reusable object-pronoun token reflecting the new sex. Tests cover saved targets, self/other recipients, rerolls, recast guards, removal and expiration restoration. The direct-mutation method was removed.

**Evidence:** C `magic.c:1279`; Python `src/api/SpellApi.py:901`; data `SOMDB.Spells.json:2245`.

**Trigger/expected/actual:** Cast successfully or recast on the same target. C saves/checks existing effect, stores an APPLY_SEX delta for `2 * level`, and reverses it through normal effect removal. Python directly assigns a random different sex and stores no effect, so cancellation/expiration cannot undo it. The unused collection modifier `'= 0 )'` is malformed and must not be activated as a substitute fix. Test save, recast, dispel and expiration restoration.

### M25 — P2: Plague/curse/frenzy/faerie fire/weaken omit spell-specific guards

**Addressed guard behavior 2026-10-23:** Plague now rolls its disease save before checking NPC undead and preserves join behavior for eligible repeated infections. Faerie fire rejects its raw flag; weaken rejects its spell record before its other-damage save. Existing curse guards are preserved, and frenzy's duplicate/berserk/calm/alignment rejections now render self/other-specific payload messages. Tests cover rejection without effect application, save ordering and eligible paths.


**Evidence:** C `magic.c:3756`, `:1676`, `:2827`, `:2725`, `:4407`; data `SOMDB.Spells.json:2671`, `:535`, `:2721`, `:2027`, `:1914`.

**Trigger/expected/actual:** Plague an undead/saving target; curse an already cursed/saving character; frenzy a calmed/berserk/different-alignment character; recast faerie fire/weaken. C rejects those cases (plague uses a disease save; weaken allows its save but rejects an existing spell). Python plague/curse/frenzy/faerie fire go directly to generic affect application; weaken checks only a save. Recasts therefore join/accumulate and prerequisites disappear. Add narrow collection guards/API predicates for each rule and test them separately from M05.

### M26 — P2: Haste/slow interaction and protection exclusivity differ

**Addressed 2026-10-23:** Existing guards/opposition preserve haste/slow save order, innate flags, OFF_FAST, IMM_MAGIC and protection exclusivity. Haste now selects level/2 for self and level/4 for others through a content duration expression. Reusable apply_affect_data duration overrides evaluate at the effective cast level without changing templates. Actual-effect tests cover odd-level rounding, both identities and stat restoration; existing tests cover saved/failed counters and rejection feedback.

**Evidence:** C `magic.c:2976`, `:4231`, `:3870`, `:3899`; Python `src/api/SpellApi.py:995`; data `SOMDB.Spells.json:2616`, `:1147`, `:3067`.

**Trigger/expected/actual:** Haste someone slowed or naturally fast, slow an immune/saving hasted target, or apply the opposite protection. C haste rejects AFF_HASTE/OFF_FAST, first attempts to dispel slow, and self duration is level/2 versus level/4 on others. Python checks only its spell ID, never dispels slow, and always uses level/4. Python slow attempts haste dispel before its save, lacks the explicit IMM_MAGIC check, and marks performed even if dispel fails. Protection checks only the same spell ID, allowing both opposing protections and ignoring raw flags. Test these interactions and self/other duration.

### M27 — P2: Several flag-based duplicate checks use only spell identity

**Addressed 2026-10-23:** The nine relevant detect/fly/infravision/pass-door/sanctuary documents now guard AFF_* rather than spell IDs. Regression cases exercise every raw flag with no effect record for self and other targets. Armor, shield and stone skin retain their C spell-identity checks.

**Evidence:** C `magic.c:1783`, `:1811`, `:1840`, `:1869`, `:1899`, `:2799`, `:3457`, `:3727`, `:4119`; Python `src/api/SpellApi.py:180`, `:1076`; corresponding detect/fly/infravision/pass door/sanctuary collection lambdas.

**Trigger/expected/actual:** A victim has the ability bit from race, innate state or another spell, with no record under the expected spell ID. C's relevant spells check AFF_* directly. The Python lambdas ask `stop_if_affected('spell.…')`, whose ID lookup does not imply the raw bit is active. They can apply unnecessary extra effects and change their lifetime. Test innate flight, detection and sanctuary. Armor/shield/stone skin intentionally use spell-ID checks in C and should not be indiscriminately converted.

### M28 — P2: Bless/curse object opposition and repeat rules are missing

**Addressed 2026-10-23:** Object duplicate/opposition guards and character bless prerequisites remain content-owned. Successful opposition removes the first matching object affect and clears its flag without applying the opposite spell. EffectHandler now tracks the wearer when applying equipment effects and refreshes that item's stat contribution when live object affects are added/removed, including expiration and opposition. Actual-effect tests verify immediate saving-throw changes of -1/+1, resistant counters preserving state, successful counters restoring saves, expiration, and unequip/re-equip without duplicate stat changes.


**Evidence:** C `magic.c:767`, `:1676`; Python `src/api/SpellApi.py:218`, `src/item/EffectHandler.py:247`; data `SOMDB.Spells.json:117`, `:535`.

**Trigger/expected/actual:** Bless an evil/already blessed object, curse a blessed/already evil object, or bless a fighting character. C rejects duplicates/fighting bless targets and tries a dispel to remove the opposite object enchantment before returning. Python applies the requested entry unconditionally, permitting opposing flags and repeated effects. Equipped-item saving-throw adjustments also need verification when restoring C behavior. Test both opposed flags, failed dispel, successful removal without adding the opposite effect, and duplicate rejection.

### M29 — P2: Poison object handling and character duration differ

**Addressed 2026-10-23:** Existing object guards and food/drink value3 handling remain. Character poison now uses a separate collection affect template with duration level and modifier -2, and explicitly joins repeated infections. The collection also owns DAM_POISON rejection and victim/room success feedback, plus the weapon-coating message. Tests verify actual character duration/effective level, additive joined duration/strength penalties, saved targets and full stat restoration. Shared target filtering prevents the weapon template from affecting characters and the character template from affecting objects. The specialized poison method was removed.

**Evidence:** C `magic.c:3786`; Python `src/api/SpellApi.py:954`; data `SOMDB.Spells.json:1097`.

**Trigger/expected/actual:** Poison food/drink, a blessed/burn-proof weapon, an incompatible magical weapon, or an already poisoned weapon. C sets food/drink `value[3]`, checks protections/weapon flags, and rejects unsupported objects. Python applies the TO_WEAPON template to any object without those checks; food poison state is not set. Character poison lasts level/2 instead of C's level. Test food/drink state, all weapon exclusions, unsupported items and duration.

### M30 — P2: Cure blindness/disease/poison bypass dispel resistance

**Addressed 2026-10-23:** Each cure now uses collection guards to require its spell record (an innate ailment flag alone is insufficient), attempts the existing resisted dispel at the effective cast level, and sends cure-specific victim/room success or caster-only failure feedback. Saved effects retain their duration and weaken by one level through the shared dispel engine. Optional notify=False suppresses generic expiration text so it does not duplicate cure feedback. Absent-record messages distinguish self from other targets. A reusable victim possessive token supports the disease room message.

**Evidence:** C `magic.c:1559`, `:1598`, `:1638`; data `SOMDB.Spells.json:440`, `:2575`, `:1416`; Python `src/api/SpellApi.py:257`.

**Trigger/expected/actual:** Cure a high-level resistant ailment. C calls `check_dispel`, can fail, and weakens saved effects; Python `remove_effects` strips the matching spell unconditionally. Test a forced successful dispel save, a failed save, and an absent ailment including the corresponding recipient feedback.

### M31 — P2: Cancellation and dispel magic share an incorrect policy

**Addressed 2026-10-23:** Cancellation and dispel magic now define their ordered 30-effect removal lists in content, including chill touch and excluding plague/poison. Cancellation uses effective level+2 with its existing eligibility guard and no initial save; dispel magic retains DAM_OTHER and uses the unmodified level. Only dispel magic attempts raw sanctuary, immediately after the sanctuary-record attempt, preserving the C flag/save/record-check order even when a resistant record remains. Reusable dispel_sequence/dispel_flag operations execute policy, while per-effect room notices and final Ok./failure feedback live in the spell payloads. Actual-effect tests verify whole-spell removal, victim expiration text, room recipients, excluded ailments, resistance weakening, the permanent-duration raw-flag roll and completion feedback. Specialized shared-policy methods and the hard-coded list were removed.

**Evidence:** C `magic.c:1015`, `:2014`, `:2155`; Python `src/api/SpellApi.py:33`, `:922`, `:935`.

**Trigger/expected/actual:** A victim saves against dispel magic; a PC cancels an unrelated NPC; an NPC cancels a PC; or dispelling a raw sanctuary bit. C dispel magic first grants a DAM_OTHER save and has a raw-sanctuary fallback. Cancellation has no initial save, uses level+2 and restricts PC/NPC combinations with the charmed-master exception. Python aliases cancellation to dispel magic, gives neither the initial dispel save nor cancellation's bonus/restriction, and cannot remove raw sanctuary without an effect record. Its list also attempts plague/poison, absent from these C dispel lists. Test the two spells independently, their eligibility matrix, removable set, raw sanctuary and M06's whole-spell removal.

### M32 — P2: Remove curse clears every carried curse at an inflated level

**Addressed 2026-10-23:** Remove curse now uses a collection pipeline with a separate direct-object branch. Character curse removal uses resisted dispel at the cast level, emits its own victim/room feedback only on success, and still proceeds to carried items after a failed character dispel. Reusable uncurse_owned_items traverses the existing ordered inventory, skips clean/NOUNCURSE objects without rolling, uses the cast level without the object bonus, continues after resistance and stops after the first successful item removal. Item owner/room messages are content-owned and independent of character-effect feedback. Direct objects retain level+2, clean/permanent/resisted notices and blue-glow success feedback.

Validation for M30/M32: 270 targeted tests passed: spell content/payload/guards, effect handling, movement, object casting/retaliation/consumption and elemental exposure (185), plus complete dynamic-command/combat modules (85). New cases cover all three cures with actual effect removal and saved-effect weakening, self/other absent-record feedback including innate flags, unrelated-effect preservation, character/item success independence, resistant inventories, first-success ordering, owner/room recipients and direct-object bonus boundaries. Collection changes were dry-run reviewed, written through devtools and queried afterward; git diff --check passed. No full-suite or live-server parity claim is made.

**Evidence:** C `magic.c:4064`; Python `src/api/SpellApi.py:938`, `:1289`.

**Trigger/expected/actual:** Cast on a character carrying several cursed items. C attempts until the first successful item uncurse, uses level for carried items, and notifies owner/room. Python loops every owned item and uses the object-target helper's level+2 for every attempt, with quiet item messages. Direct object targeting correctly has the +2 rule; preserve that branch. Test two cursed items and distinguish direct-object from character-target roll levels and recipients.

### M33 — P2: Faerie fog skips saves but fails to clear the full concealment state

**Addressed 2026-10-23:** Faerie fog now uses guarded room steps in content: skip positive invisibility levels/caster, roll DAM_OTHER, strip invisibility, mass-invisibility and sneak records (including legacy sneak identity), then clear raw HIDE/INVISIBLE/SNEAK bits. It applies no fog affect. Conjure and revealed messages are content-owned with C recipients. Actual-effect tests preserve saved/immortal/caster records and bits, remove every relevant record on an eligible target, retain unrelated effects/flags, and verify room/victim messages. The specialized fog method was removed.

**Evidence:** C `magic.c:2747`; Python `src/api/SpellApi.py:910`; `src/item/EffectHandler.py` (`affect_strip`).

**Trigger/expected/actual:** Fog a saved/invis-level victim, a mass-invisible or sneaking target, or one with raw HIDE. C respects invis level and saves, strips invis/mass invis/sneak records, and clears HIDE/INVISIBLE/SNEAK bits. Python processes every non-caster without a save/invis-level check, strips only `spell.invis` plus an effect literally named `AFF_HIDE` (not the raw bit), and applies the fog document. Test records and flags separately, including a saved victim.

### M34 — P2: Mass invis targets everyone on the same NPC/player side instead of the group

**Addressed 2026-10-23:** Mass invis now uses a collection pipeline selecting same-group occupants without raw AFF_INVISIBLE, including fighting PCs and NPC pets. It sends the victim/room fade messages before applying the effect (level/2, duration 24, APPLY_NONE, modifier 0), then always sends the caster Ok., even when no new effects are applied. Tests execute the real collection and effect handler, verify recipients and message ordering, exclude strangers and innate invisibility, and verify repeated casts do not stack effects. The specialized runtime method was removed.

**Evidence:** C `magic.c:3691`; Python `src/api/SpellApi.py:786`, `:1258`; data `SOMDB.Spells.json:1952`.

**Trigger/expected/actual:** Unrelated PCs share the room, or a group contains a pet/NPC, or a member is fighting. C selects same-group members without an extra fighting exclusion. Python uses same NPC/player status and skips fighters, so it affects strangers and misses grouped companions. Mass healing's same-side selection matches its C selection and is not this defect. Test mixed groups and unrelated PCs.

### M35 — P2: Calm only affects fighters and uses the wrong PC modifiers

**Addressed 2026-10-23:** Calm now uses collection-owned formulas and ordered target guards. Its chance counts only POS_FIGHTING occupants, weights PC levels by integer division by two, preserves the inclusive success boundary and unclamped range, and uses the caster’s immortal status to override the resistance total. On success it visits every occupant, including idle characters and the caster. NPC magic immunity/undead status and calm/berserk/frenzy stop the entire traversal at that occupant, preserving earlier effects. Eligible victims receive the calm message, stop fighting with both=False when needed, and receive separate HITROLL and DAMROLL effects: PCs -5 each, NPCs -2 each, duration level/4. Reusable SpellApi operations provide room combat statistics, range rolls, immortal checks, stopping combat and guarded nested room steps; spell policy stays in content. The specialized calm method was removed.

Validation for M34/M35: 265 targeted tests passed: spell content/payload/guards and effects, movement, object casting/retaliation/consumption and elemental exposure (180), plus complete dynamic-command/combat modules (85). New cases cover exact effects/messages, removal restoring stats, idle rooms, chance failure/equality, negative ranges, immortal override, pointer-versus-position distinctions, and first/middle traversal blockers. Collection changes were dry-run reviewed, written through devtools and queried afterward. No full-suite or live-server parity claim is made.

**Evidence:** C `magic.c:950`; Python `src/api/SpellApi.py:811`; data `SOMDB.Spells.json:2880`.

**Trigger/expected/actual:** Calm a room containing fighters and idle occupants, or an immortal casts into a large fight. C computes chance from fighters, then traverses all room occupants in order; even its early returns may occur after earlier occupants were affected. Python prevalidates only fighters and applies only to them, returns immediately with no fighters, and omits the immortal success override. Its data uses -2 for PCs instead of -5 (and M05 merges the two stat effects). Test idle occupants, PC/NPC magnitudes, immortals and traversal/early-return side effects.


Guard-focused follow-up, 2026-10-23: 243 targeted tests passed: spell content/payload/guards (70), effect application plus object casting/retaliation/consumption and elemental exposure (88), and complete dynamic-command/combat modules (85). Coverage loads current collection documents and tests raw innate flags, predicate ordering, valid boundaries, PC/NPC exceptions, immunity and save rejection, opposed effects, object flags/types, group selection, rejection recipients, and persistent state supporting recast guards. New reusable support lives in SpellApi; guard policy and feedback live in spell collections. The shared spell-message renderer also normalizes camelCase keys, fixing rejection lookups discovered by these tests. Collection changes were dry-run reviewed, written through devtools and queried afterward. No new files were retained; no full-suite or live-server parity claim is made. During that earlier guard-focused pass, M30, M32 and M35 were not changed: they concern cure resistance, removal iteration and calm traversal/formulas rather than these missing prerequisite guards.

Partial-finding completion, 2026-10-23 (M23, M24, M26, M28, M29, M31, M33): 331 targeted tests passed: spell content/payload/guards, effects, movement, object casting/retaliation/consumption and exposure (195), equipment/shop (15), communications (36), and dynamic-command/combat (85). New regression cases execute actual collection pipelines and the real effect handler for relationships, odd-level duration arithmetic, reversible stat changes, message ordering/recipients, ordered dispel policy and raw-versus-record concealment cleanup. Python compilation and git diff --check passed. An additional standalone update-handler run passed 23 of 24 tests; test_character_condition_rules_and_disabled_conditions errors because its unbootstrapped CharacterApi fixture lacks GameParameters. The failing path is Character.gain_condition -> CharacterApi.is_immortal, outside these fixes. Loading unrelated stub-heavy test modules together also fails during import, so equipment, communications and combat were run in separate processes. All spell collection changes were dry-run reviewed, written through devtools and queried afterward. No new files were retained. No full-suite or live-server parity claim is made.

## Movement and magic2.c

### M36 — P1: Portal/nexus omit destination restrictions and warp-stone consumption

**Addressed 2026-10-23:** Portal/nexus now use content guards for world-target/self/room presence, room visibility and destination flags, source NO_RECALL, level/hero limits, NPC summon immunity and typed DAM_NONE save, and clan membership. Nexus independently checks source visibility and SAFE. Component validation follows all destination guards; mortal casters require a held warp stone, and a valid held stone is consumed even for immortals. Reusable held-item consumption removes equipment effects and ownership; generic portal creation uses content-owned prototype/timer rules, correct destination vnums, source/remote notices and one portal for same-room nexus. Portal timer is 2+level/25 and nexus timer is 1+level/10, with C integer truncation. Specialized portal/nexus policy methods were removed.

**Evidence:** C `magic2.c:60`, `:119`; Python `src/api/SpellApi.py:1160`; data `SOMDB.Spells.json:3217`, `:3242`.

**Trigger/expected/actual:** Cast without a held warp stone, onto self, a protected/private/no-recall/unseen destination, or a high-level/immune/saving/clan-restricted target. C rejects the relevant conditions and consumes a valid held component even for immortals holding one. Python only requires a found character, rooms, and prototype 25, then creates portals without any component handling. C portal timer is `2 + level/25`; nexus is `1 + level/10`. Python uses `max(2, 1 + level/10)` for both. Test guards before creation, component extraction, one/two-way destinations, same-room nexus and distinct timers. These are engine predicates/operations plus designer-authored policy, not a reason to hard-code every spell.

### M37 — P2: Farsight implements world-character location instead of directional scan

**Addressed 2026-10-23:** Farsight now checks raw blindness and invokes a reusable local-exit scan driven by content directions, distance labels and messages. Empty arguments show current/adjacent occupants; directional scans cover three depths, use character visibility and never locate a named character in the world. This checkout's scan.c intentionally does not test exit closure, and that behavior is preserved. The unused directional heading in C is not emitted. Tests cover all-around/directional output, depth limits, closed exits, hidden targets, blindness and invalid character-name arguments. The former world-location method was removed.

**Evidence:** C `magic2.c:47`; Python `src/api/SpellApi.py:725`; data `SOMDB.Spells.json:3267`.

**Trigger/expected/actual:** Cast farsight north, or while blind. C rejects blindness and calls `do_scan(target_name)`. Python searches a world character and reports its room, ignoring scan direction, range, exits and blindness. Test a directional scan, no argument, blind caster and a name which should not become a world locator.

### M38 — P1: Summon/gate omit protected-character rules; gate leaves pets behind

**Addressed 2026-10-23:** Summon/gate now use content prerequisites in C order. Summon checks level+3, immortal PC level, fighting, NPC aggression/immunity/shopkeeper status, PC NOSUMMON and the typed NPC save. Gate adds destination visibility, PC hero-level and clan restrictions, and snapshots a co-located pet before moving the caster. Only that initially co-located pet follows through a successful gate. Shared move_to preserves departure, traveler/arrival, summoned-target and automatic-look ordering, including valid same-room moves; room lookup uses the spell handler registry. New CharacterApi.can_see_room implements trust/immortal/newbie/clan visibility, and Room retains its authored clan instead of overwriting it during initialization. Specialized summon/gate policy methods were removed.

**Evidence:** C `magic.c:4315`, `:2883`; Python `src/api/SpellApi.py:638`, `:691`.

**Trigger/expected/actual:** Summon a target >= level+3, an immortal PC, or shopkeeper; gate to a hero/clan-restricted/unviewable room with a co-located pet. C rejects those summon/gate cases and transports the pet on valid gates. Python summon lacks level/immortal/shopkeeper checks. Gate lacks room visibility, hero and clan checks and never transports pets. Existing room flags and some immunity/save checks are present. Test each missing rule independently, including pet movement only when initially co-located.

### M39 — P1: Teleport destination filtering and combat eligibility differ

**Addressed 2026-10-23:** Teleport now uses content guards: source NO_RECALL, non-self raw IMM_SUMMON (including PCs), fighting victims whenever the caster is a PC (including self), then non-self DAM_OTHER at effective level-5. Destination selection occurs only after guards/save pass. Reusable random_room filters by victim room visibility, owner/occupancy privacy, PRIVATE/SOLITARY/SAFE and the local C NPC/raw-aggression/LAW rule; destination NO_RECALL is permitted. Room.is_private now includes owners, NPC occupants and IMP_ONLY. Tests cover the caster/self/combat matrix, ordering before randomness, clan/level visibility and destination filtering, and same-room disappearance/arrival/look behavior. The specialized teleport policy method was removed.

**Evidence:** C `magic.c:4352`, `act_enter.c:42`; Python `src/api/SpellApi.py:617`, `:1115`.

**Trigger/expected/actual:** A PC self-teleports while fighting, or a teleport can choose safe/private/solitary/invisible/law rooms. C blocks a fighting victim when the caster is a PC, including self, and delegates destination filtering to `get_random_room(victim)`. Python checks combat only for non-self victims (including NPC caster cases where C permits it), and random-room selection only excludes NO_RECALL. It can enter protected/unviewable rooms and excludes NO_RECALL destinations which C's helper does not exclude. Test the exact caster/victim matrix and destination flags/visibility/private occupancy.

### M40 — P2: Word of recall charges the victim's movement instead of the caster's

**Addressed 2026-10-23:** Word of recall now uses collection guards and a content-owned temple destination. NPC targets stop silently. Missing-temple and blocked/curse failures address the victim, before combat or resource changes. Successful recall stops the victim's combat with both=True and halves the caster's movement, matching the local reference, then relocates/shows the victim even if already in the temple. Tests distinguish caster/victim movement, failure recipients, NPC silence, combat-stop arguments, and same-room effects. The specialized recall method was removed.

**Evidence:** C `magic.c:4432`; Python `src/api/SpellApi.py:666`.

**Trigger/expected/actual:** Recall another PC. The local C explicitly halves `ch->move`; Python halves the victim's movement. C failures address the victim; Python `ctx.fail` addresses the caster. Python also returns early if already in the temple, bypassing the C combat-stop/movement effects. Test a distinct caster/victim, same-room recall, blocked recall, and recipient routing. Whether to retain C's caster-cost choice is a design decision, but it is the actual reference behavior.

Validation for M36–M40, 2026-10-23: 364 targeted tests passed: spell content/payload/guards, effects, movement commands, object casting/retaliation/consumption and elemental exposure (210); dynamic-command/combat (85); equipment/shop (15); communications (36); character immortal/clan helpers, room occupancy, area helpers and mobile room access (18). New tests execute the actual spell collection pipelines with real room membership operations, room visibility/privacy rules and equipment detachment. Coverage includes destination rejection before component consumption, mortal/immortal components, timer arithmetic/endpoints, pet movement, save types and ordering, protected targets, random-room rules, failure recipients, caster costs and scan behavior. Async-dependent modules ran outside the sandbox for Windows socket initialization and separately where their test stubs conflict. Collection changes were dry-run reviewed, written through devtools and queried afterward. No new files were retained; no full-suite or live-server parity claim is made.

## Objects, information and feedback

### M41 — P1: Enchant armor/weapon are unconditional scalable upgrades

**Addressed 2026-10-23:** Enchant armor/weapon now guard type and worn state in content, then invoke a reusable EffectHandler enchantment operation configured by spell rules. Risk counts canonical item affects once, including hydrated prototype bonuses, applies the separate armor/weapon costs, flag reductions, bounds, integer divisions and strict result thresholds. Outcomes can destroy/extract, disenchant/clear instance affects and extra flags, fail unchanged, or add the bounded ordinary/exceptional bonuses. Successful records preserve existing durations, raise affect levels without lowering them, update spell identity, set MAGIC/GLOW/HUM as appropriate and increment object level only up to HERO-1. Prototype affects become instance-owned on success; raw prototype metadata is not reapplied after disenchantment. Neutral prototype defaults in ItemUtil now use bitvector 0 rather than -1, preventing unintended flags. Outcome messages live in spell payloads. Tests cover all result bands, endpoints, clamps, flag reductions, repeated attempts, prototype conversion, duration preservation, worn rejection and extraction.

**Evidence:** C `magic.c:2219`, `:2397`; Python `src/api/SpellApi.py:1178`.

**Trigger/expected/actual:** Enchant an already enhanced or equipped item repeatedly. C requires carried/unworn items, computes risk from current bonuses/flags/level, and can destroy, disenchant, fail or succeed with bounded additions and flag/level/prototype-affect transitions. Python checks only item type, always appends level-scaled permanent bonuses, raises item level to caster level and sets enchanted. There is no risk, diminishing success or worn-item check. Test the full C outcome bands, existing prototype effects and repeated enchantment. Restoring only the random failure roll would not restore success semantics.

### M42 — P1: Recharge can be repeated safely forever

**Addressed 2026-10-23:** Recharge now uses collection type guards and configured C reference ordinals, skill-limit and chance formulas. The ordinal map is restricted to the actual 134 initialized skill-table entries, excluding the later group table, and accepts numeric, named and resolved-ability references without confusing ROM slot numbers with indices. It rejects advanced spells and zero capacity before randomness, preserves full/partial recovery thresholds, consumes recharge eligibility on success, reduces capacity on a recoverable failure and extracts exploding objects. The local C partial-success branch deliberately sends the caster notice twice, without a room notice; tests preserve that behavior. Payloads own all outcomes, and tests cover exact band boundaries, repeated attempts, maximum/current charges, named references and rejection before RNG.

**Evidence:** C `magic.c:3974`; Python `src/api/SpellApi.py:758`.

**Trigger/expected/actual:** Recharge an eligible wand/staff repeatedly, or one whose spell is too advanced. C checks spell slot value against level, prevents further recharge once `value[1] == 0`, computes chance from missing charges and supports full/partial recovery, reduced capacity or explosion. Python always adds `max(1, level/8)` up to capacity, never consumes recharge eligibility and cannot explode. Test all C result bands and repeat attempts.

### M43 — P2: Creation spells omit per-cast object setup and destinations

**Addressed 2026-10-23:** Creation now uses reusable configuration, carried-object lookup, flags and equipment operations with content-authored expressions and messages. Food values scale by effective cast level, roses enter inventory, springs receive a cast-level timer, and discs use the caster's level for capacities and timer base but the effective spell level for the random subtraction, matching this checkout. Disc NOREMOVE checks happen before creation/randomness; eligible old float-slot items return to inventory before the new disc is equipped. Continual light with an argument searches visible, unworn carried items and sets GLOW, rejects missing/already glowing targets and creates no light ball in that branch. Caster/bystander creation and wear notices are covered without duplicate caster delivery.

**Evidence:** C `magic.c:1431`, `:1480`, `:1493`, `:1503`, `:2775`; Python `src/api/SpellApi.py:551`; data `SOMDB.Spells.json:1595`, `:390`, `:2953`, `:2195`, `:3292`.

**Trigger/expected/actual:** Create food/rose/spring/disc, or name a carried object for continual light. Python only clones the matching prototype into the room. C scales food values to level; puts rose in inventory; gives spring a level timer; configures disc capacity, per-item maximum and randomized timer, places it in inventory and equips it after the no-remove floating-slot check. Continual light with an argument should add GLOW to that carried item, not spawn another light ball. Prototype values cannot supply per-cast scaling/placement logic. Test created object values, ownership/equipment/timer and the existing-object glow branch.

### M44 — P2: Create water overwrites other liquids and ignores rain scaling

**Addressed 2026-10-23:** Create water now guards for drink containers only and rejects nonempty other liquids without mutation. A reusable fill_liquid operation caps added volume at the actual remaining capacity, does nothing for a full/zero-capacity vessel, sets the canonical named water reference, refreshes derived liquid color/condition metadata from GameData, and adds the water keyword only when filling succeeds. This prevents an emptied beer vessel from retaining beer effects after being filled with water. Content chooses level*4 in rain or level*2 otherwise and owns filled/rejection feedback. Tests cover fountains, non-water contents, empty other-liquid vessels, rain, exact capacity, zero capacity, names and unchanged failures.

**Evidence:** C `magic.c:1517`; Python `src/api/SpellApi.py:566`.

**Trigger/expected/actual:** Cast on a nonempty beer/wine container, an empty zero-capacity container, or during rain. C only accepts drink containers, rejects non-water contents, fills at level*4 in rain versus level*2 otherwise up to remaining capacity, and adds the water keyword when filling. Python accepts fountains too, overwrites liquid type, always uses level*2, can manufacture capacity when zero, and does not add the keyword. Test rejection without mutation, rain/dry amounts, capacity and lookup keywords.

### M45 — P2: Locate object omits carried/nested objects and ignores concealment rules

**Addressed 2026-10-23:** Locate object now traverses room contents, PC/NPC inventory, equipment and nested containers through a reusable world-object iterator with cycle/duplicate protection. It applies object visibility, ROM keyword-prefix matching, NOLOCATE, chance and caster-level filtering in C order. Parent traversal reports the outer owner/location, hides the room when the carrier cannot be seen, includes room vnums for immortals, and caps matches at 2*effective level or 200. Templates own result/absence text. Tests cover nested floor/carried objects, equipment, visibility and flag rejection before rolls, chance/level order, concealed carriers and both limits. Iteration uses the Python world traversal rather than C's global object-list layout.

**Evidence:** C `magic.c:3585`; Python `src/api/SpellApi.py:602`.

**Trigger/expected/actual:** Locate a carried/nested item, a NOLOCATE/invisible/over-level item, or many matches. C scans world objects, filters visibility/name/NOLOCATE/chance/level, follows containers to owner/location, and caps at 2*level (200 for immortals). Python scans only direct room contents, uses substring matching without those filters and caps at `max(2, level/2)`. It misses carried objects while exposing protected floor-object locations. Test ownership chains, filters and limits.

### M46 — P2: Identify loses gameplay-relevant object details

**Addressed 2026-10-23:** Identify now renders content-owned templates for object flags, scaled weight/cost/level, consumable spell references, wand/staff charges, liquid color/name, container capacity/weight limits/flags/multipliers, weapon classes and old/new damage formats, weapon flags, armor values, prototype/runtime stat affects, timed durations and affect/object/weapon/immunity/resistance/vulnerability bits. Unknown affect destinations are reported explicitly. Numeric references use configured C ordinals while named/resolved references remain compatible with the service contract. Item accepts an optional new_format field, defaulting to modern dice format, and GameApi exposes the existing liquid table instead of duplicating it in spell data. Tests cover representative types, prototype versus timed records, spell references, old-format damage and unknown bits. Wording/formatting is template-driven.

**Evidence:** C `magic.c:3229`; Python `src/api/SpellApi.py:588`; data `SOMDB.Spells.json:1492`.

**Trigger/expected/actual:** Identify a weapon, armor, consumable, wand/staff, container or affected object. C reports the relevant flags, enchantments/affects, spell/charge values and item-type details. Python returns only a generic description/type/level/weight/cost block. Players cannot inspect the combat/consumable properties C exposes. Compare representative items by type and render their existing runtime data through payloads.

### M47 — P2: Healing does not update position; several information/feedback paths differ

**Addressed 2026-10-23:** Healing now invokes the existing combat update_pos operation immediately after HP restoration, and heal/cure/refresh success/completion messages live in collection pipelines. Refresh distinguishes full from partial recovery. Detect poison distinguishes food/drink from other objects, including fountains; the report's original description of the C non-food text as broken was inaccurate: the local source says It doesn't look poisoned. Alignment uses all seven strict C bands. Ventriloquate uses the existing argument parser and independently rolls DAM_OTHER for every awake, non-named-speaker listener, including the caster; saved listeners receive the deception notice. Related control-weather behavior now adds/subtracts level/3 d4 to tendency only, leaves pressure unchanged, and emits the invalid-request/Ok. notices. Tests execute actual combat position recovery for incapacitated healed targets, distinguish self/other recipients, cover band endpoints, per-listener saves/exclusions and weather dice/feedback.

**Evidence:** C `magic.c:1583`, `:1622`, `:1660`, `:3025`, `:4051`, `:1929`, `:3538`, `:4383`; Python `src/api/SpellApi.py:527`, `:537`, `:579`, `:741`, `:1042`.

**Trigger/expected/actual:** Heal someone stunned/incapacitated, refresh a tired character, detect poison on a non-food object, inspect alignment near category boundaries, or ventriloquate near awake/sleeping listeners. Healing amounts match but Python never calls the C-equivalent `update_pos`, so restored HP need not immediately restore posture. Heal/cure/refresh lack C success feedback in the queried documents/helpers. Detect poison says non-food objects look delicious rather than broken. Know alignment collapses C's seven bands into five. Ventriloquate sends one room line without per-listener saves, the awake check, exclusion of the named speaker or the saved-listener deception notice. Test healing state and recipient-sensitive branches; keep user-facing text in collections when correcting these paths.

### M48 — P2/P3: Successful effect-removal and spell-action feedback is incomplete

**Addressed 2026-10-23:** The concrete feedback paths enumerated by this finding are now covered: creation/enchant/recharge actions in this pass, portal/nexus in M36, mass invisibility in M34, resisted cures in M30, and spell-specific dispel room transitions in M31. Mass healing now invokes the real heal and refresh collection pipelines for each same-NPC/player-side room occupant, preserving posture updates, victim notices and per-other-target caster acknowledgments. Object action room routes exclude a caster who already receives the character channel; victim/room spell routes retain their distinct recipients. New tests record caster, victim and bystander output as well as state. This closes the named missing-feedback cases; it does not assert that every unrelated spell message or visibility-dependent presentation has been exhaustively audited.

**Evidence:** C spell bodies throughout `magic.c` and `magic2.c`; Python `src/api/SpellApi.py:229`, `:280`, `:551`, `:1160`; current spell payload documents.

**Trigger/expected/actual:** Observe a portal opening, a conjured object, mass invis/healing or a removed defensive effect. Python has real collection-based affect-application/removal rendering, so these messages are not universally absent. However, generic object creation/portal helpers never enqueue the C creation lines, mass helpers bypass ordinary application payload rendering, and dispel helpers mostly use owned effect `msgOff` instead of the C spell-specific room transitions. Cure success/failure/absence feedback differs as well (M30). Record sender, victim and bystander output in regression fixtures rather than fixing only text strings. Pure wording differences should remain lower priority than missing actionable state feedback.

Validation for M41–M48, 2026-10-23: 382 targeted tests passed: spell content/payload/guards, real effects, movement, object casting/retaliation/consumption and elemental exposure (231); dynamic-command/combat (85); equipment/shop (15); communications (36); item normalization (5); object lookup (10). New tests use actual collection pipelines, item/room models, effect handling and isolated real combat position recovery. Test helpers isolate heavy dependencies; they do not simulate a live server or separately deployed content service. An additional fountain-command module cannot import because its fixture environment lacks the mobile package (Object -> CombatHandler -> MobileApi); that module is not counted as passed. Async-dependent modules ran outside the sandbox for Windows socket initialization. Compilation and git diff --check passed. Collection changes were dry-run reviewed, written through devtools and queried afterward. No new files were retained for these fixes, and no full-suite pass is claimed.

## Correction order and regression approach

1. Correct shared cast eligibility, charging, recovery, save plumbing, affect target filtering and add-versus-join behavior (M01–M08). These invalidate otherwise reasonable spell templates.
2. Restore progression/resource integrity and targeting protections: energy drain, alignment attacks, holy word, chain lightning, portal/nexus/gate/summon/teleport, enchant/recharge.
3. Restore spell-specific guards/interactions/formulas in collection data, backed by reusable API predicates and operations. Do not replace designer-editable content with a monolithic hard-coded Python spell switch.
4. Add focused `unittest` cases loading representative documents. Use controlled random values, real effect records and minimal room/item/character fixtures; check side effects, roll count/order, recipients and resource timing, not just returned booleans.

## Validation and limits

At the original review stage, the collection-query skill was used before collection inspection: `list`, `summary spells`, and targeted `find`, `get --json` and `path` queries. No collection or runtime source was changed during that initial review. Subsequent corrections and their validation are documented under the findings above. The C checkout remains read-only reference material. Initial review checks follow below.

The review traces the named files and related helpers, not all combat, movement, updates, item-use commands, world content or content-service deployment behavior. It does not claim every message or rare branch is enumerated. Snapshot data may differ from a separately deployed content service. Clan/room visibility, equipment removal and follower primitives must be integrated with existing domain APIs when implementing corrections; their omission here is a behavioral finding, not an architectural prescription. C undefined behavior is not a requested compatibility target.

### Checks performed

Each test module/class ran separately because repository fixtures install module stubs. Commands used `.venv/Scripts/python.exe`:

| unittest target | Result |
| --- | --- |
| `tests.test_spell_affect_payload_messages` | 7 passed |
| `tests.test_object_container_shop_spell_parity` | 16 passed |
| `tests.test_effect_util_affects` | 4 passed |
| `tests.test_combat_dynamic_commands.TestFightDynamicCommands` | 5 passed |

The combined multi-module run failed at import because a fixture's `SimpleNamespace` stub was used as another module's `Ability` base class. The full combat-dynamic module, run separately, completed five synchronous tests then stalled in its async tests without further output and was interrupted. No full-suite pass is claimed. These passes establish existing behavior, not C parity for the findings.

Two isolated probes executed the actual AST-extracted `EffectHandler.affect_join` / `apply_spell_effects` methods with minimal dependencies. They confirmed M05: level-24 frenzy becomes a single APPLY_AC +28/duration-24 record; applying current bless data to a character accepts all three entries, including TO_OBJECT. These probes isolate composition/dispatch and do not simulate stat mutation, messaging or a live server. Suggested regression scenarios above are follow-up work, not newly added tests.

The default `python` resolves to an ActiveState wrapper that failed on external log/config permissions. Commands succeeded using the repository virtual-environment executable with Python 3.14, despite its virtual-environment-location warning.


### Reference file fingerprints

SHA-256 fingerprints identify the C files inspected (a Git revision was not obtained for that checkout):

- `magic.c`: `c519ce5a018cffc063ab509d353f137d37f8986ac84fbcf0c3efa51acac327b3`
- `magic2.c`: `f3f11b1edf2391671685e0d710e9d15d9a0706bae104afd92cda23d3b1d05169`
- `magic.h`: `93b2e628cb795cc175ccab542d1ab640508302f52c3fa5defb6099187bf397c0`

## Declaration and implementation inventory

All 98 declarations were accounted for: 97 spell documents plus the null sentinel. The data column uses the `functionName` anchor in `resources/collections/SOMDB.Spells.json`. The entry column is current lambda dispatch, not a claim that every branch matches C. All ordinary player casts remain subject to M01–M09; matching basic formulas can still be affected by shared machinery and other findings above.

| C declaration | Definition | Spell document / line | Python/data entry |
| --- | --- | --- | --- |
| `spell_null` | `magic.c:3719` | Sentinel; no player document required | Not a missing implementation |
| `spell_acid_blast` | `magic.c:724` | acid blast / 1989 | `lambda ctx: ctx.damage_expr('dice(level, 12)', 'DAM_ACID')` |
| `spell_armor` | `magic.c:738` | armor / 34 | `lambda ctx: ctx.stop_if_affected('spell.armor', 'alreadyAffected', 'alreadyAffectedOther')`<br>`lambda ctx: ctx.apply_affect_data()` |
| `spell_bless` | `magic.c:767` | bless / 123 | content prerequisites and execution pipeline (see document lambdas) |
| `spell_blindness` | `magic.c:853` | blindness / 189 | `lambda ctx: ctx.stop_if_affected('AFF_BLIND')`<br>`lambda ctx: ctx.stop_if_saved()`<br>`lambda ctx: ctx.apply_affect_data()` |
| `spell_burning_hands` | `magic.c:877` | burning hands / 228 | `lambda ctx: ctx.damage_table('DAM_FIRE')` |
| `spell_call_lightning` | `magic.c:902` | call lightning / 319 | content guards, shared damage, opposite-side room filter and distant notices |
| `spell_calm` | `magic.c:950` | calm / 3469 | content chance formula and ordered guarded room traversal; separate per-stat effects |
| `spell_cancellation` | `magic.c:1015` | cancellation / 3671 | content eligibility, ordered dispel list at level+2 and per-effect/completion feedback |
| `spell_cause_critical` | `magic.c:1190` | cause critical / 2127 | `lambda ctx: ctx.damage_expr('dice(3, 8) + level - 6', 'DAM_HARM', save_half=False)` |
| `spell_cause_light` | `magic.c:1182` | cause light / 2102 | `lambda ctx: ctx.damage_expr('dice(1, 8) + level // 3', 'DAM_HARM', save_half=False)` |
| `spell_cause_serious` | `magic.c:1198` | cause serious / 2152 | `lambda ctx: ctx.damage_expr('dice(2, 8) + level // 2', 'DAM_HARM', save_half=False)` |
| `spell_change_sex` | `magic.c:1279` | change sex / 2994 | guarded reversible sex delta and post-change victim/room feedback |
| `spell_chain_lightning` | `magic.c:1204` | chain lightning / 2994 | chain_damage with content-owned dice, decrement, save divisor and messages |
| `spell_charm_person` | `magic.c:1313` | charm person / 366 | content guards, follower transfer/grouping, affect and success messages |
| `spell_chill_touch` | `magic.c:1361` | chill touch / 373 | `lambda ctx: ctx.damage_table('DAM_COLD', on_failed_save=lambda hit: hit.apply_affect_data(join=True))` |
| `spell_colour_spray` | `magic.c:1402` | colour spray / 472 | `lambda ctx: ctx.damage_table('DAM_LIGHT', on_failed_save=lambda hit: hit.invoke_spell('blindness', hit.level // 2))` |
| `spell_continual_light` | `magic.c:1431` | continual light / 2510 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_control_weather` | `magic.c:1465` | control weather / 610 | content tendency dice/sign and completion/invalid feedback |
| `spell_create_food` | `magic.c:1480` | create food / 640 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_create_rose` | `magic.c:1493` | create rose / 4394 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_create_spring` | `magic.c:1503` | create spring / 3341 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_create_water` | `magic.c:1517` | create water / 670 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_cure_blindness` | `magic.c:1559` | cure blindness / 666 | guarded resisted dispel with cure-owned feedback |
| `spell_cure_critical` | `magic.c:1583` | cure critical / 737 | resource expression, position recovery for healing, and self/other success feedback |
| `spell_cure_disease` | `magic.c:1598` | cure disease / 3157 | guarded resisted dispel with cure-owned feedback |
| `spell_cure_light` | `magic.c:1622` | cure light / 768 | resource expression, position recovery for healing, and self/other success feedback |
| `spell_cure_poison` | `magic.c:1638` | cure poison / 1900 | guarded resisted dispel with cure-owned feedback |
| `spell_cure_serious` | `magic.c:1660` | cure serious / 2782 | resource expression, position recovery for healing, and self/other success feedback |
| `spell_curse` | `magic.c:1676` | curse / 756 | content prerequisites and execution pipeline (see document lambdas) |
| `spell_demonfire` | `magic.c:1755` | demonfire / 3232 | content pipeline: backlash, alignment shift, level d10 damage, curse invocation and target restoration |
| `spell_detect_evil` | `magic.c:1783` | detect evil / 832 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_DETECT_EVIL', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_detect_good` | `magic.c:1811` | detect good / 3597 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_DETECT_GOOD', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_detect_hidden` | `magic.c:1840` | detect hidden / 1902 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_DETECT_HIDDEN', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_detect_invis` | `magic.c:1869` | detect invis / 883 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_DETECT_INVIS', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_detect_magic` | `magic.c:1899` | detect magic / 934 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_DETECT_MAGIC', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_detect_poison` | `magic.c:1929` | detect poison / 1038 | content branches distinguish poisoned/clean food or drink and other objects |
| `spell_dispel_evil` | `magic.c:1950` | dispel evil / 965 | content conditions: caster backlash, alignment immunity, low-HP damage and holy save |
| `spell_dispel_good` | `magic.c:1981` | dispel good / 3440 | content conditions: caster backlash, alignment immunity, low-HP damage and negative save |
| `spell_dispel_magic` | `magic.c:2014` | dispel magic / 2240 | initial save, ordered content dispels with raw-sanctuary fallback and feedback |
| `spell_earthquake` | `magic.c:2188` | earthquake / 1018 | content room filter: flying zero damage, grounded unsaved damage, area notices |
| `spell_enchant_armor` | `magic.c:2219` | enchant armor / 4344 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_enchant_weapon` | `magic.c:2397` | enchant weapon / 1144 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_energy_drain` | `magic.c:2623` | energy drain / 1039 | content pipeline: alignment, save guard, experience/resources, roll/heal, messages, damage |
| `spell_faerie_fire` | `magic.c:2725` | faerie fire / 2536 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_FAERIE_FIRE'); lambda ctx: ctx.apply_affect_data() |
| `spell_faerie_fog` | `magic.c:2747` | faerie fog / 2795 | guarded room steps, complete concealment cleanup and content messages |
| `spell_farsight` | `magic2.c:44` | farsight / 4465 | blindness guard and content-driven directional local scan |
| `spell_fireball` | `magic.c:2660` | fireball / 1059 | `lambda ctx: ctx.damage_table('DAM_FIRE')` |
| `spell_fireproof` | `magic.c:2684` | fireproof / 3328 | `lambda ctx: ctx.apply_affect_data()` |
| `spell_flamestrike` | `magic.c:2711` | flamestrike / 1770 | `lambda ctx: ctx.damage_expr('dice(6, 8) + level', 'DAM_FIRE')` |
| `spell_floating_disc` | `magic.c:2775` | floating disc / 5068 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_fly` | `magic.c:2799` | fly / 2060 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_FLYING', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_frenzy` | `magic.c:2827` | frenzy / 3261 | content prerequisites and execution pipeline (see document lambdas) |
| `spell_gate` | `magic.c:2883` | gate / 3095 | content guards and ordered caster/co-located-pet relocation |
| `spell_giant_strength` | `magic.c:2932` | giant strength / 1303 | `lambda ctx: ctx.stop_if_affected('spell.giant_strength', 'alreadyAffected', 'alreadyAffectedOther')`<br>`lambda ctx: ctx.apply_affect_data()` |
| `spell_harm` | `magic.c:2961` | harm / 1152 | damage_expr with content-owned minimum and post-save caps |
| `spell_haste` | `magic.c:2976` | haste / 3396 | content guards/opposition and self/other duration override |
| `spell_heal` | `magic.c:3025` | heal / 1339 | resource expression, position recovery for healing, and self/other success feedback |
| `spell_heat_metal` | `magic.c:3036` | heat metal / 3670 | heat_equipment with content-owned outcome rules and messages |
| `spell_holy_word` | `magic.c:3173` | holy word / 3301 | content pipeline: alignment rules, child spells, energy damage and exhaustion |
| `spell_identify` | `magic.c:3229` | identify / 2164 | typed object facts and affect details rendered through content templates |
| `spell_infravision` | `magic.c:3457` | infravision / 2667 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_INFRARED', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_invis` | `magic.c:3486` | invisibility / 968 | `lambda ctx: ctx.apply_affect_data()` |
| `spell_know_alignment` | `magic.c:3538` | know alignment / 2553 | seven strict content-owned alignment bands |
| `spell_lightning_bolt` | `magic.c:3560` | lightning bolt / 1258 | `lambda ctx: ctx.damage_table('DAM_LIGHTNING')` |
| `spell_locate_object` | `magic.c:3585` | locate object / 1520 | filtered world/nested ownership search with content limits and feedback |
| `spell_magic_missile` | `magic.c:3648` | magic missile / 1363 | `lambda ctx: ctx.damage_table('DAM_ENERGY')` |
| `spell_mass_healing` | `magic.c:3671` | mass healing / 4242 | same-side room pipeline invoking heal and refresh content |
| `spell_mass_invis` | `magic.c:3691` | mass invis / 2474 | grouped room pipeline, pre-effect fade messages and unconditional completion feedback |
| `spell_nexus` | `magic2.c:105` | nexus / 4417 | content destination/source/component guards; paired portals with same-room exception |
| `spell_pass_door` | `magic.c:3727` | pass door / 2614 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_PASS_DOOR', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_plague` | `magic.c:3756` | plague / 3205 | guarded content pipeline: lambda ctx: ctx.stop_when(ctx.saves_spell('DAM_DISEASE') or (ctx.is_npc(ctx.victim) and ctx.character_flag('act', 'ACT_UNDEAD')), 'resisted' if ctx.victim is ctx.actor else 'resistedOther'); lambda ctx: ctx.apply_affect_data(join=True) |
| `spell_poison` | `magic.c:3786` | poison / 1551 | guarded object/character pipelines, target-specific affects, explicit joins and feedback |
| `spell_portal` | `magic2.c:56` | portal / 4370 | content destination/component guards; reusable one-way portal creation |
| `spell_protection_evil` | `magic.c:3870` | protection evil / 1579 | guarded content pipeline: lambda ctx: ctx.stop_when(ctx.is_affected('AFF_PROTECT_EVIL') or ctx.is_affected('AFF_PROTECT_GOOD'), 'alreadyAffected' if ctx.victim is ctx.actor else 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_protection_good` | `magic.c:3899` | protection good / 3648 | guarded content pipeline: lambda ctx: ctx.stop_when(ctx.is_affected('AFF_PROTECT_EVIL') or ctx.is_affected('AFF_PROTECT_GOOD'), 'alreadyAffected' if ctx.victim is ctx.actor else 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_ray_of_truth` | `magic.c:3929` | ray of truth / 3621 | content pipeline: backlash, good-target guard, alignment multiplier, holy damage, blindness, target restoration |
| `spell_recharge` | `magic.c:3974` | recharge / 4707 | content guards/configuration and reusable object operations; payload-owned feedback |
| `spell_refresh` | `magic.c:4051` | refresh / 3373 | resource expression, position recovery for healing, and self/other success feedback |
| `spell_remove_curse` | `magic.c:4064` | remove curse / 1636 | object/character content branches and ordered first-success carried-item removal |
| `spell_sanctuary` | `magic.c:4119` | sanctuary / 1657 | guarded content pipeline: lambda ctx: ctx.stop_if_affected('AFF_SANCTUARY', 'alreadyAffected', 'alreadyAffectedOther'); lambda ctx: ctx.apply_affect_data() |
| `spell_shocking_grasp` | `magic.c:4177` | shocking grasp / 1869 | `lambda ctx: ctx.damage_table('DAM_LIGHTNING')` |
| `spell_shield` | `magic.c:4148` | shield / 1863 | `lambda ctx: ctx.stop_if_affected('spell.shield', 'alreadyAffected', 'alreadyAffectedOther')`<br>`lambda ctx: ctx.apply_affect_data()` |
| `spell_sleep` | `magic.c:4202` | sleep / 1701 | guarded persistent sleep effect, canonical position update and content-owned awake-only feedback |
| `spell_slow` | `magic.c:4231` | slow / 3699 | content prerequisites and execution pipeline (see document lambdas) |
| `spell_stone_skin` | `magic.c:4286` | stone skin / 1810 | `lambda ctx: ctx.stop_if_affected('spell.stone_skin', 'alreadyAffected', 'alreadyAffectedOther')`<br>`lambda ctx: ctx.apply_affect_data()` |
| `spell_summon` | `magic.c:4315` | summon / 1869 | content protected-target guards and summoned-target relocation |
| `spell_teleport` | `magic.c:4352` | teleport / 80 | content eligibility/save guards and filtered random-room relocation |
| `spell_ventriloquate` | `magic.c:4383` | ventriloquate / 1989 | per-awake-listener typed saves and content-owned speech/deception notices |
| `spell_weaken` | `magic.c:4407` | weaken / 2422 | content prerequisites and execution pipeline (see document lambdas) |
| `spell_word_of_recall` | `magic.c:4432` | word of recall / 1938 | victim-directed failure guards, caster movement cost and relocation |
| `spell_acid_breath` | `magic.c:4467` | acid breath / 2770 | HP-sensitive breath_damage expression; existing exposure operation and save scaling |
| `spell_fire_breath` | `magic.c:4496` | fire breath / 2823 | HP-sensitive breath_damage expression; existing exposure operation and save scaling |
| `spell_frost_breath` | `magic.c:4552` | frost breath / 2861 | HP-sensitive breath_damage expression; existing exposure operation and save scaling |
| `spell_gas_breath` | `magic.c:4609` | gas breath / 2892 | HP-sensitive breath_damage expression; existing exposure operation and save scaling |
| `spell_lightning_breath` | `magic.c:4647` | lightning breath / 2931 | HP-sensitive breath_damage expression; existing exposure operation and save scaling |
| `spell_general_purpose` | `magic.c:4677` | general purpose / 2500 | `lambda ctx: ctx.damage_expr('number_range(25, 100)', 'DAM_PIERCE')` |
| `spell_high_explosive` | `magic.c:4689` | high explosive / 2525 | `lambda ctx: ctx.damage_expr('number_range(30, 120)', 'DAM_PIERCE')` |

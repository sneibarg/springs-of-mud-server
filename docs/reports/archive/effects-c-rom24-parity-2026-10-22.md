# ROM24 effects.c parity review

Date: 2026-10-22. Reference: local `C:/Users/scott/PycharmProjects/PyRom/Rom24/src` checkout. Python baseline: `fb3f9dcbdae820dbf2561855998c8042327d707f`.

## Result and scope

**Current status (2026-10-22):** All four scoped findings have been addressed; see the resolution notes under each finding. Latest focused validation: 68 tests passed. The original review below describes the baseline, not the current implementation. Remaining limits include the base breath-damage formulas and paths outside this effects review.

Partial parity: the weapon-hit path implements much of `fire_effect`, `cold_effect`, and `shock_effect`, but the breath-spell paths do not invoke their secondary effects. Acid corrosion and environmental poison behavior are absent from the traced runtime paths. Four actionable discrepancies are detailed below.

Reviewed all five functions in `effects.c`, their callers in `fight.c` and `magic.c`, and relevant saving throws, condition updates, affect joining, and message substitution. Python coverage includes `WeaponHitHandler`, its combat integration, `SpellApi`, `EffectUtil`, `EffectHandler`, ownership/equipment helpers, message delivery, the five breath-spell documents, and `combat.weaponHitEffects` in GameData.

This is a behavioral review, not a request to reproduce the C architecture. Designer-authored payloads and collection rules are appropriate. No documented intentional exception was found for the discrepancies below. The initial review made no runtime or collection changes; subsequent fixes are recorded in the resolution notes.

References below use repository-relative paths and one-based line numbers. C references are relative to the reference checkout's `src` directory; Python/data references are relative to this repository.

## Findings

### 1. [P2] Acid breath never corrodes or destroys equipment

**Resolution (2026-10-22):** Addressed by `src/util/AcidExposure.py` and the `SpellApi.damage_expr` acid-exposure option, enabled in the acid-breath collection document. Exposure runs before HP damage, with half effect level and quarter effect damage when the existing breath save succeeds. Armor etching persists on the item and refreshes worn modifiers; susceptible objects are destroyed and contents spill with recursive half-strength exposure. Notices remain in the spell payload. The existing breath damage formula, generic saving-throw implementation, and observer-visibility issue remain outside this fix. Focused validation: 34 tests passed across `tests.test_acid_exposure`, `tests.test_weapon_hit_effects`, and `tests.test_spell_affect_payload_messages` (including 13 new acid tests). A broader collection-query test run encountered temporary-directory permission errors.

**Evidence:** C `effects.c:40–193`, especially `:73–120` (eligibility/chance), `:132–164` (armor etching), and `:168–191` (spilling and destruction); C `magic.c:4482–4490` (calls before HP damage). Python `resources/collections/SOMDB.Spells.json:2294–2310` (`spell.acid_breath`), `src/api/SpellApi.py:334–358`, and `src/combat/WeaponHitHandler.py:114–187`.

**Trigger:** Acid breath hits a character carrying eligible armor, containers, corpses, clothing, staffs, wands, or scrolls; the C item checks and random rolls succeed.

**Expected:** C traverses carried items even after a successful breath save, using reduced effect level/damage in that case. It honors burn-proof/no-purge protection and the one-in-five bypass, computes the softened destruction chance, and applies type adjustments. Armor survives but gains a permanent +1 APPLY_AC penalty, updates an existing AC affect where present, and immediately worsens all four armor values when worn. Other eligible items are destroyed, with contents spilled and recursively exposed at half level/damage when a room is available.

**Actual:** The acid-breath document runs only `ctx.damage_expr('dice(level, 16)', 'DAM_ACID')`. The helper saves, applies HP damage, and queues damage output. It never traverses inventory or applies corrosion. The weapon elemental helper has no acid branch or armor-etch operation to supply this behavior elsewhere.

**Consequence:** Acid breath leaves equipment intact and never accumulates ROM's permanent armor degradation. Its corrosion messages and recursive container consequences are also absent.

**Correction direction:** Add reusable elemental/object-effect support, including armor enchant/AC bookkeeping, then call it from designer-authored acid-breath behavior before HP damage with the appropriate save-dependent strength.

### 2. [P2] Gas breath omits character poisoning and food/drink contamination

**Resolution (2026-10-22):** Addressed by `src/util/PoisonExposure.py`, the `SpellApi.poison_effect` primitive, and the gas-breath collection lambda. Floor items are exposed before character safety checks; a single damage roll supplies the cloud, and saved victims receive half-level/quarter-damage exposure before half HP damage. Secondary saves include poison immunity, resistance/vulnerability, berserk, and mana-class adjustment. Failed secondary saves join `spell.poison`; carried food/drink is checked even on successful saves. Contamination preserves the local C bless/burn-proof protections, no-purge exception, and drink capacity-equality guard. Messages remain in the gas-breath payload. Validation covers 10 new poison tests alongside the existing acid, weapon, spell-payload, and affect tests. The existing breath damage formula, NPC target-selection differences, and observer-specific rendering remain outside this fix.

**Evidence:** C `effects.c:444–531`; C `magic.c:4623–4642`; Python `resources/collections/SOMDB.Spells.json:2369–2386`, `src/api/SpellApi.py:360–383`, and `src/combat/WeaponHitHandler.py:85–99`.

**Trigger:** Gas breath exposes a room or character containing susceptible food or drink, or a character fails the secondary poison save.

**Expected:** C first applies poison to room objects, then applies character effects before each victim's HP damage, with reduced effect strength on a successful breath save. The secondary save uses `level/4 + dam/20` and DAM_POISON. Failure joins a poison affect with level `level`, duration `level/2`, strength -1, and AFF_POISON, and sends victim/room notices. Carried objects are checked regardless of the secondary save result. Eligible food/drink gets `value[3] = 1` after the item chance succeeds.

The exact local C rules matter: poison objects reject ITEM_BURN_PROOF and ITEM_BLESS, **not** ITEM_NOPURGE; drink containers are rejected when capacity equals current amount (`value[0] == value[1]`). Those rules should not be replaced by the destructive elements' shared immunity gate or an assumed empty-container check.

**Actual:** Gas breath runs only `damage_room_expr('dice(level, 12)', 'DAM_POISON')`. That helper never joins poison affects or visits room/inventory objects. The weapon-poison branch implements a different coating proc with different effect-level/save inputs and no object traversal; it does not provide environmental poison behavior.

**Consequence:** Gas breath causes immediate damage without the poison debuff, subsequent poison consequences, or contaminated consumables that ROM produces.

**Correction direction:** Provide a reusable poison exposure primitive separate from weapon coating application, keeping poison's distinct object protections and drink guard.

### 3. [P2] Fire, frost, and lightning breath bypass the existing elemental side effects

**Resolution (2026-10-22):** Addressed by the shared `WeaponHitHandler.expose` primitive and `SpellApi.elemental_effect`/`elemental_breath`, enabled in all three spell documents. Fire/frost expose floor objects first at full level and half base damage, then process eligible characters. Primary and collateral victims receive the local C save levels, effect scaling, and HP-damage fractions; NPC area targets must satisfy ROM's mutual-combat rule. Lightning exposes only its primary victim. Exposure reuses the tested weapon implementation for blindness, chill joining, daze, conditions, object protections/chances, equipment removal, and fire-container spilling. Each spell owns its secondary/destruction payload. Validation: 12 new breath tests and 48 existing focused tests passed (60 total). The original dice-only base damage expressions remain unchanged; matching ROM's HP-dependent base breath formulas and observer-specific rendering are separate work.

**Evidence:** C `effects.c:197–298`, `:301–441`, `:534–624`; C `magic.c:4512–4547`, `:4568–4603`, `:4662–4670`. Python `resources/collections/SOMDB.Spells.json:2319–2361` and `:2394–2410`; `src/api/SpellApi.py:334–383`; `src/combat/WeaponHitHandler.py:103–187`; `src/combat/CombatHandler.py:1097–1100`.

**Trigger:** A breath spell exposes a character who fails its secondary save, carries susceptible equipment, or shares a fire/frost room containing susceptible floor objects.

**Expected:** Fire can blind (-4 hitroll, random duration 0 through effect-level/10), adjust player thirst, and destroy eligible objects. Frost can join a six-hour strength -1 chill-touch affect, adjust player hunger, and shatter potions/drink containers. Lightning can raise daze to at least `max(12, level/4 + dam/20)` and destroy eligible wands, staffs, and jewelry. Carried equipment is exposed even if the secondary character save succeeds. Fire/frost also process floor objects before their character loops. The breath callers scale character-effect level/damage according to the breath save and, for fire/frost, primary versus collateral targets.

**Actual:** The documents call generic `damage_expr` or `damage_room_expr`. Neither invokes `WeaponHitHandler._element` or `_object_effect`. Those helpers are reached by the damaging melee weapon path only. Breath damage does not implicitly invoke weapon procs.

**Consequence:** The same damage family has different secondary behavior depending on its source: flaming/frost/shocking weapons expose gear and apply debuffs, but their breath counterparts do not. Floor objects are untouched by fire/frost breath.

**Correction direction:** Extract reusable exposure primitives usable by both weapon procs and spell content. Preserve ROM's room-before-character ordering, save-dependent effect inputs, and collateral scaling rather than simply applying the weapon helper at full strength to every target.

### 4. [P2] Elemental notices reveal names and objects without observer visibility checks

**Resolution (2026-10-22):** Addressed through `DisplayUtil.visible_tokens` and `RecipientText`. Weapon/elemental messages resolve direct-recipient descriptions and capture room-observer variants at the event using the existing character/object visibility checks, with `someone`/`something` substitutions. Acid and poison spell notices use the same mechanism. Recipient variants survive combat text concatenation and spell queuing; MessageBus resolves the destination's text before paging, delivery, and snoop mirroring without mutating the shared message or its metadata. Unknown recipients receive the anonymous fallback. Payload templates remain designer-owned. Validation: eight new visibility/delivery tests plus the existing 60 focused tests passed. The delivery regression uses immediate mocked IO because Windows event-loop socket initialization stalls in this sandbox; live socket delivery was not exercised.

**Evidence:** C `effects.c:221–222`, `:285–288`, `:329–331`, `:410–413`, `:615–618`; C `comm.c:2512–2525` and `merc.h:1858` (PERS/can_see_obj). Python `src/combat/WeaponHitHandler.py:45–59`, `:124–133`, `:165`, `src/util/DisplayUtil.py:3–8`, `src/combat/CombatHandler.py:115–127`, and `src/server/messaging/MessageBus.py:67–69`. Payloads are in GameData `combat.weaponHitEffects` (`resources/collections/SOMDB.GameData.json:2638–2787`).

**Trigger:** An observer cannot see the victim or an affected object, while an elemental weapon proc generates a chill/blindness or object-destruction notice. For example, a blind observer receives a destroyed scroll's description, or an observer unable to see an invisible victim receives that victim's name in a chill notice.

**Expected:** ROM renders `$n` via PERS for each recipient and `$p` via `can_see_obj`, substituting an anonymous person/object description when visibility fails.

**Actual:** `_messages` resolves the victim's name and object's short description once without an observer, producing plain strings for each channel. Room delivery sends the same already-rendered text to every recipient; MessageBus does not re-evaluate visibility.

**Consequence:** Elemental secondary/destruction notices disclose identities and item descriptions that ROM hides. Data-driven wording itself is not the defect; the missing recipient-specific substitution is.

**Correction direction:** Retain collection-owned messages but render entity/object references against each recipient's visibility through a shared message-rendering primitive.

## Behavior aligned in the weapon path

Static comparison and the focused tests support the following within the current fire/frost/shock weapon path:

- Character save level is effect-level/4 plus damage/20. Saving throws include immunity, resistance/vulnerability, berserk, mana-class adjustment, 5–95 clamping, and the strict percent `< save` endpoint.
- Existing blindness suppresses the fire secondary save. Fire uses `affect_to_char`; frost uses `affect_join`. Joining averages level and adds duration/modifier, matching C for the nonnegative levels examined.
- Shock daze preserves a longer existing daze. Fire/frost condition adjustments are **positive** damage/20 in this C checkout, despite their comments suggesting thirst/hunger loss. Python preserves that sign, excludes NPCs/immortals, and respects disabled conditions.
- Object checks preserve burn-proof/no-purge immunity, the one-in-five bypass, sequential softcaps above 25 and 50, bless -5, item-level penalty, type bonuses, 5–95 bounds, and inclusive destruction at `roll == chance`.
- The configured fire/frost/shock susceptible types and chance bonuses match C. Fire spills contents before recursively exposing them at half level/damage. Destroyed equipped items have their applied effects removed and leave ownership.

These are scoped observations, not proof of complete integration parity. In particular, they do not cover the absent acid/poison branches or breath entry points.

## Validation and limitations

Collection inspection used the collection-query CLI: collection listing, targeted retrieval of all five breath documents, and the GameData `combat.weaponHitEffects` path. No large collection was loaded wholesale for this review.

Executed with `.venv/Scripts/python.exe`:

| Command | Result |
| --- | --- |
| `-m unittest tests.test_weapon_hit_effects` | 14 tests passed |
| `-m unittest tests.test_effect_util_affects` | 4 tests passed |
| `-m unittest tests.test_combat_state_effects` | Did not complete; interrupted after two progress dots |
| Combined invocation of those three modules | Did not complete; interrupted after 20 progress dots |

The combat-state test stall was not diagnosed and is not classified as an effects parity defect. The standalone weapon tests use isolated dependencies and mocked effect/immunity/damage services; they do not exercise a live server or prove end-to-end message visibility. No C executable was built or differential simulation run. Findings are established by tracing source and active collection definitions, not by live gameplay reproduction.

Breath HP-damage formulas, primary/collateral damage selection, generic spell saving throws, and NPC target-selection differences were encountered at the integration boundary but are not audited comprehensively here. They need a separate `magic.c` review; wiring secondary effects alone should not be interpreted as establishing full breath-spell parity. Tick scheduling, persistence, and garbage-collection equivalence were not exhaustively tested.

Recommended regression coverage for future fixes: saved/unsaved breath exposure; floor versus carried versus nested items; acid armor degradation while worn and unworn; acid/fire content spilling; poison's bless/no-purge distinctions and capacity-equality guard; repeated chill/poison joins; and observer-specific character/object notices.

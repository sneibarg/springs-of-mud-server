# Object-oriented design review

Date: 2026-10-23

Review baseline: `cac412d` (`magic updates.`)

Scope: current Python runtime design following the ROM24 parity work; recommendations only.

Implementation follow-up: the suggested sequence has been implemented in the working tree. See [implementation and validation notes](object-oriented-design-implementation-2026-10-23.md) for the changes, compatibility boundaries, and reproduced baseline test failures. The assessment below records the original review baseline.

## Assessment

The most valuable improvement is to give shared state transitions one owner. Item removal, equipment effects, ability lookup, and entity state normalization currently have several implementations. These create more practical risk than the number of static methods by itself.

The existing `AnimateEntity`, `Ability`, `FetchAndRegisterMixin`, action models, and registry abstractions already provide useful reuse. Extend those contracts selectively. Preserve the content-facing APIs and designer-authored payloads, guards, rules, and lambdas while changing their implementation behind the facade.

This is a targeted architectural review across entities, combat, effects, spells, item ownership, loading, and bootstrap paths. It is not an exhaustive review of every method or another comparison against C. Findings describe the current design; they are not claims that a particular parity commit introduced each issue.

## Priority overview

| ID | Priority | Recommendation | Main technique |
| --- | --- | --- | --- |
| 1 | High: behavioral defect | Route equipped-item expiration through effect-aware removal | Encapsulate a state transition |
| 2 | High: design | Share item location, detachment, and traversal operations | Composition; reuse existing room/item helpers |
| 3 | Medium | Put player/NPC regeneration variation behind entity overrides | Extend existing inheritance; Template Method |
| 4 | Medium | Make learned-ability operations instance-owned | Instance methods; optional small component |
| 5 | Medium | Separate ability definitions from learning orchestration | Injected service |
| 6 | Medium | Centralize ability resolution for effect messages | Shared resolver |
| 7 | Medium | Extract reusable elemental exposure mechanics | Composition before additional inheritance |
| 8 | Medium | Give armor a common runtime value contract | Shared value object and boundary adapters |
| 9 | Medium | Consolidate position and affected-flag operations | Delegate to existing state owners |
| 10 | Medium | Make API dependencies and reset ownership explicit | Composition and lifecycle ownership |
| 11 | Low | Share corpse/body-part naming and formatting helpers | Small pure helper |

Except for finding 1, these are maintainability recommendations, not demonstrated gameplay defects. Priorities reflect expected change risk and benefit, not incident severity.

## 1. Equipped-item expiration bypasses the removal invariant

**Evidence:** [ItemUpdateHandler.py:55](../../src/item/ItemUpdateHandler.py#L55), [ItemUpdateHandler.py:112](../../src/item/ItemUpdateHandler.py#L112), [Equipped.py:128](../../src/game/Equipped.py#L128), [EffectHandler.py:274](../../src/item/EffectHandler.py#L274), [EffectHandler.py:284](../../src/item/EffectHandler.py#L284).

`expire_item()` eventually calls `_remove_item_at_location()`. For `char_equipped` and `mob_equipped`, that helper simply sets the matching equipment slot to `None`. It does not remove the item's sourced effects from the wearer, clear `_effect_wearer`, or reset `wear_location`/`wear_loc`.

**Trigger and consequence:** a timer expires on a worn item that contributes stat modifiers. The item disappears from its slot while its wearer can retain the applied effects. Stale wear metadata and the wearer reference remain on the removed object. An isolated execution of the actual helper confirmed slot removal with all three kinds of state retained. This reproduces the helper contract failure; it is not a full server integration test.

Other removal paths already coordinate this transition: [SpellApi.py:1144](../../src/api/SpellApi.py#L1144), [WeaponHitHandler.py:198](../../src/combat/WeaponHitHandler.py#L198), and [AcidExposure.py:88](../../src/util/AcidExposure.py#L88) remove item effects and unequip before removing the carried item.

**Recommendation:** introduce one effect-aware detachment operation used by expiration and destruction. Keep low-level slot state on `Equipped`, inventory membership on the entity, and effect removal on `EffectHandler`; coordinate them in an item/equipment service. Normal unequipping returns an item to inventory, so permanent removal must also detach that returned item. Expiration should bypass voluntary-removal restrictions while preserving this cleanup invariant.

**Validation:** expire worn items with strength/AC modifiers on both a character and mobile; verify effect reversal, slot clearing, wear metadata, wearer reference, and absence from inventory. Include floating containers and existing child-spill behavior. Apply cleanup once even when an item is referenced more than once.

## 2. Item ownership is interpreted independently by several consumers

**Evidence:** [Room.py:83](../../src/area/Room.py#L83), [Room.py:96](../../src/area/Room.py#L96), [Room.py:104](../../src/area/Room.py#L104), [ItemUpdateHandler.py:47](../../src/item/ItemUpdateHandler.py#L47), [ItemUpdateHandler.py:89](../../src/item/ItemUpdateHandler.py#L89), [SpellApi.py:1130](../../src/api/SpellApi.py#L1130), [SpellApi.py:1144](../../src/api/SpellApi.py#L1144).

The room model already supplies item locations, recursive traversal, and containment lookup. Spell operations add a separate recursive walker and decode location kinds to remove objects; item expiration has another set of location-kind branches and direct collection mutations. Acid and weapon exposure implement further removal sequences. Adding a new ownership location therefore requires coordinated edits in multiple subsystems.

**Recommendation:** build a small shared item-location collaborator around `Room.item_locations()`, `Room.locate_item()`, and existing `Item` traversal helpers. Start with `find_location`, `walk_world_items`, and the detachment transition in finding 1. A typed location record can replace dictionary keys when it materially simplifies callers. Keep expiration-specific spill policy and spell-specific payload routing with their respective callers.

Prefer an ordinary service and record over a class hierarchy for every location kind. Preserve identity-based traversal, cycle protection, snapshots during mutation, actor inventory differences, and the existing wire representation. This also gives lock ownership a concrete home; callers currently mutate `loot`, `inventory`, `contents`, and equipment outside the entity's locking methods.

**Validation:** use `test_world_objects_and_shields`, `test_item_persistence`, `test_update_handler_active_players`, and elemental exposure suites, adding nested-container and equipped-item detachment cases before migrating consumers.

## 3. Use the existing entity inheritance for regeneration variation

**Evidence:** [AnimateEntity.py:202](../../src/game/AnimateEntity.py#L202), [AnimateEntity.py:218](../../src/game/AnimateEntity.py#L218), [AnimateEntity.py:274](../../src/game/AnimateEntity.py#L274), [AnimateEntity.py:331](../../src/game/AnimateEntity.py#L331), [AnimateEntity.py:382](../../src/game/AnimateEntity.py#L382), [EntityUpdateHandler.py:52](../../src/game/EntityUpdateHandler.py#L52).

`Character` and `Mobile` already inherit `AnimateEntity`, and the update handler calls `entity.regenerate()`. Nevertheless, each gain method branches on `CharacterApi.is_npc(self)`. The base class imports `Character` and `Ability` to support player learning. This makes the shared model depend on its more specialized player behavior.

**Recommendation:** retain `regenerate()` as the common algorithm and move the player and NPC portions of gain calculation into protected overrides on `Character` and `Mobile`. Share the existing furniture and affect-penalty helpers. Introduce only hooks needed to preserve the current calculation stages; player and NPC position/condition handling differ, so avoid an overly generic formula with flags.

This is a justified Template Method application: a common update caller and two existing variations are already present. A composition-based regeneration policy is a reasonable alternative if policies later vary independently of entity type; current evidence does not require that extra layer.

**Cost and validation:** preserve integer-division order, RNG calls, learning side effects, resource caps, missing-room behavior, and tick ordering. Existing player/NPC regeneration cases in `test_update_handler_active_players` are the starting contract. Some tests invoke model methods on minimal stand-ins; migrate fixtures deliberately so they exercise actual overrides.

## 4. Learned-ability state is handled as static utility code on Character

**Evidence:** [Character.py:258](../../src/player/Character.py#L258), [Character.py:272](../../src/player/Character.py#L272), [Character.py:286](../../src/player/Character.py#L286), [Character.py:307](../../src/player/Character.py#L307), [Ability.py:211](../../src/skill/Ability.py#L211).

`learned_entries(character)`, `get_learned(character, ...)`, and `set_learned(character, ...)` receive the state owner explicitly. They read and mutate its `skills`/`spells`. Internal callers also explicitly name `Character`, which bypasses normal instance dispatch. In contrast, entry-name and entry-level normalization operate only on the supplied record and are appropriately pure helpers.

**Recommendation:** make collection lookup and mutation instance methods on `Character`. Keep stateless entry normalization static or module-level. If the skill/spell collection rules warrant a separate `LearnedAbilities` component, have the character own it; do not force that extra class merely to change the syntax.

Retain dict/object record compatibility, exact-before-prefix selection, visibility callbacks, level clamping, creation behavior, and serialization. Existing unbound calls such as `Character.get_learned(character, ...)` can remain valid during migration to instance methods, provided signatures remain compatible.

**Benefit:** the owner becomes the supported mutation boundary, and learning services no longer need to manipulate collection shapes themselves. This is an instance-method correction, not an opportunity for another entity subclass.

## 5. Ability definitions also orchestrate player progression

**Evidence:** [Ability.py:116](../../src/skill/Ability.py#L116), [Ability.py:149](../../src/skill/Ability.py#L149), [Ability.py:177](../../src/skill/Ability.py#L177), [Ability.py:198](../../src/skill/Ability.py#L198), [Ability.py:243](../../src/skill/Ability.py#L243), [PlayerHandler.py:811](../../src/player/PlayerHandler.py#L811), [EntityUpdateHandler.py:59](../../src/game/EntityUpdateHandler.py#L59).

`Ability` is a content definition and common superclass for `Skill`/`Spell`. Its static learning methods also locate registries through `CharacterApi`, draw from module-level random sources, update character learning, award experience, and attach a pending message queue to the character. These are independent runtime responsibilities with hidden collaborators.

**Recommendation:** move improvement orchestration into an injected learning/progression service with explicit registry, bonus-table, RNG, and advancement dependencies. Put definition-local queries such as level/rating lookup on an ability instance when they use that instance's maps; retain character collection mutation on the owner from finding 4. Give pending improvement messages explicit ownership rather than dynamically attaching them from `Ability`.

Preserve static entry points as forwarding adapters while migrating combat, regeneration, and command callers. Preserve the existing designer API and payload behavior; moving message text into content is a separate content change, not a prerequisite for this extraction.

**Validation:** practice visibility, class fallbacks, success/failure improvement, XP award, deterministic random inputs, and exactly-once message draining. This extraction has meaningful wiring cost in `Bootstrapper`; make it a focused change with characterization tests.

## 6. Effect-message lookup duplicates ability identity rules

**Evidence:** [SpellApi.py:349](../../src/api/SpellApi.py#L349), [SpellApi.py:369](../../src/api/SpellApi.py#L369), [EffectUpdateHandler.py:125](../../src/item/EffectUpdateHandler.py#L125), [Ability.py:116](../../src/skill/Ability.py#L116).

Spell removal and periodic effect handling each scan definitions and normalize identity independently. They already differ: the spell helper searches spells by handler/name/id, while the update helper searches both skills and spells and considers stripped `spell.`/`skill.` prefixes. Practice lookup performs another name scan with skills-first precedence.

**Recommendation:** share an ability resolver backed by the existing registries. Make lookup intent explicit: resolving an effect owner and resolving a player-entered practice name need not use identical namespaces or precedence. Start with explicit resolver methods and a documented collision policy; add indexes only if needed, with reload invalidation.

Keep rendering and routing in their current contexts. The shared responsibility is identity resolution, not a universal messaging framework. Continue to obtain user-facing messages from the owning skill/spell payload.

**Validation:** handler IDs, document IDs, display names, prefixed names, collisions, skill-owned effects, missing definitions, reloads, and the existing `test_spell_affect_payload_messages` cases. The observed lookup differences are verified; whether every difference is intentional requires contract decisions before changing results.

## 7. Elemental exposure is a reusable engine operation inside a weapon handler

**Evidence:** [WeaponHitHandler.py:123](../../src/combat/WeaponHitHandler.py#L123), [WeaponHitHandler.py:169](../../src/combat/WeaponHitHandler.py#L169), [AcidExposure.py:25](../../src/util/AcidExposure.py#L25), [PoisonExposure.py:27](../../src/util/PoisonExposure.py#L27), [SpellApi.py:862](../../src/api/SpellApi.py#L862), [SpellApi.py:896](../../src/api/SpellApi.py#L896).

Environmental fire/cold/shock exposure shares the weapon-hit handler with weapon procs. Acid, poison, and elemental object handling duplicate the diminishing-return chance calculation, type normalization, inventory/room iteration, and some destruction cleanup. Spell APIs now use these engine operations too, so their responsibility extends beyond weapon hits.

**Recommendation:** extract common pure chance/type helpers first, then place exposure operations in a reusable collaborator used by both `WeaponHitHandler` and `SpellApi`. Reuse the item-detachment operation from findings 1–2. Preserve each element's content-provided rules and messages.

Do not immediately force acid, poison, fire, cold, and shock into one base class. Poison treats blessing as immunity; acid/fire use blessing as a chance adjustment. Acid damages armor while other paths destroy objects, and notification contracts differ. If a common base is later introduced, its public exposure contract must first be aligned; otherwise composition is simpler and safer.

**Validation:** preserve early-return and RNG draw order, save behavior, item immunity, half-strength recursive exposure, armor updates, equipped effects, and spell-versus-weapon payload ownership. Existing acid, poison, weapon-hit, and breath tests provide focused coverage.

## 8. Armor needs a common runtime contract and separate input adapters

**Evidence:** [player/ArmorClass.py:10](../../src/player/ArmorClass.py#L10), [player/ArmorClass.py:20](../../src/player/ArmorClass.py#L20), [mobile/ArmorClass.py:9](../../src/mobile/ArmorClass.py#L9), [MobileUtil.py:130](../../src/util/MobileUtil.py#L130), [CombatHandler.py:1842](../../src/combat/CombatHandler.py#L1842), [EffectHandler.py:93](../../src/item/EffectHandler.py#L93).

Two armor dataclasses represent the same four runtime categories using different names and input formats. Combat has to probe both naming schemes; effects enumerate eight possible attribute names. Player armor also has `get_ac(char, ac)`, which reaches into `CharacterApi` for the character's dexterity bonus. Combat independently computes that bonus and applies its own division into combat units.

**Recommendation:** use one shared armor value object with category lookup and bulk adjustment. Keep player/mobile JSON adapters at the loading boundary and preserve their service formats. Calculate dexterity-adjusted combat defense in combat policy, or accept an already-resolved defensive bonus; armor storage should not query global character rules.

A common value object is preferable to making mobile armor inherit player armor or vice versa. If separate public classes must remain, use a small shared base with compatible adapters. Do not merge the raw and combat-scaled AC return contracts accidentally.

**Validation:** all four damage categories, negative values and truncation, AC effects and reversal, JSON round trips, and cloned mobile armor isolation (`test_mobile_armor_isolation`).

## 9. Position and affected flags have competing normalization paths

**Evidence:** [AnimateEntity.py:85](../../src/game/AnimateEntity.py#L85), [AnimateEntity.py:99](../../src/game/AnimateEntity.py#L99), [AnimateEntity.py:106](../../src/game/AnimateEntity.py#L106), [CharacterApi.py:342](../../src/api/CharacterApi.py#L342), [CharacterApi.py:365](../../src/api/CharacterApi.py#L365), [CharacterApi.py:381](../../src/api/CharacterApi.py#L381).

The model and API each interpret positions and affected flags. Their position fallbacks differ: the entity also considers `start_pos`; the API uses character attributes or a direct position and defaults to standing. Setters can maintain both a direct field and an attributes field. Flag mutation similarly has separate normalization and assignment paths.

**Recommendation:** define the supported state contract on `AnimateEntity` and `StatusFlags`, then make API helpers delegate with the appropriate injected enum values. Preserve the deliberately different NPC fallback through an override or explicit argument. Avoid moving registry or messaging work into these state methods.

This reduces the chance that combat, movement, and updates interpret the same entity differently. Do not silently unify the existing fallbacks: characterize missing attributes, named positions, numeric values, mobile start positions, and letter/integer flags first.

## 10. API inheritance hides runtime dependency and reset ownership

**Evidence:** [GameApi.py:12](../../src/api/GameApi.py#L12), [GameApi.py:33](../../src/api/GameApi.py#L33), [GameApi.py:47](../../src/api/GameApi.py#L47), [CharacterApi.py:24](../../src/api/CharacterApi.py#L24), [CharacterApi.py:34](../../src/api/CharacterApi.py#L34), [MobileApi.py:25](../../src/api/MobileApi.py#L25), [MobileApi.py:43](../../src/api/MobileApi.py#L43), [EffectUtil.py:99](../../src/util/EffectUtil.py#L99), [Bootstrapper.py:107](../../src/server/Bootstrapper.py#L107).

`GameApi` owns global configured data, but subclasses acquire additional registry/weather state through lazy loading. `CharacterApi.lazy_load` and `MobileApi.lazy_load` are exact duplicated bodies. Their reset hooks differ: the mobile hook clears only its logger despite lazy loading assigning registry/weather attributes. `EffectUtil` separately stores a process-wide handler.

**Recommendation:** give bootstrap explicit ownership of runtime dependencies and reset lifecycle. Introduce a small shared dependency object or explicit collaborator arguments incrementally, retaining facade methods for content compatibility. New runtime services should receive dependencies rather than copying this global configuration approach.

A shared lazy-load helper can remove the immediate duplicate, but avoid deriving `MobileApi` from `CharacterApi` merely for that reuse: it would inherit unrelated player APIs. If class-based facade state remains, add reset coverage for every configured subclass and make the intended reset entry point explicit.

**Impact and limits:** this is demonstrated lifecycle asymmetry and test-isolation risk, not proof that the running single-world server has crossed configurations. Do not undertake a repository-wide DI rewrite. Migrate the services identified above first and update `Bootstrapper` bindings in the same change.

## 11. Share the small death-loot formatting helpers

**Evidence:** [CombatHandler.py:618](../../src/combat/CombatHandler.py#L618), [CombatHandler.py:1347](../../src/combat/CombatHandler.py#L1347), [CombatHandler.py:1353](../../src/combat/CombatHandler.py#L1353), [BodyParts.py:113](../../src/item/BodyParts.py#L113), [BodyParts.py:127](../../src/item/BodyParts.py#L127), [BodyParts.py:135](../../src/item/BodyParts.py#L135).

Corpse and body-part construction duplicate victim-name selection and the same `%s` formatting/fallback implementation. These operations depend only on their arguments.

**Recommendation:** extract small pure functions into a shared item/death-loot helper, called by both construction paths. Keep the legacy template semantics and NPC short-description preference. Neither an injected service nor a common handler superclass earns its cost here.

## Inheritance decisions

| Candidate | Decision | Reason |
| --- | --- | --- |
| Character/Mobile regeneration | Extend `AnimateEntity` with overrides | Existing common caller and demonstrated subtype variation |
| Skill/Spell common behavior | Continue using `Ability` | Existing shared content contract; definition-local behavior can live here |
| Armor variants | Prefer one value type; optional small common base | Different serialization shapes are not different combat responsibilities |
| Exposure variants | Share helpers/composed collaborators first | Different immunity, mutation, and callback contracts |
| Loading services | Retain `FetchAndRegisterMixin` | Fetch/build/register already uses a useful template; no second generic service hierarchy is justified here |
| MobileApi/CharacterApi | Do not derive one from the other | Shared bootstrap code does not make one a substitute for the other |
| Command/combat action definitions | Retain shared `game.action` models | Compatibility modules already alias the common definitions; this is not duplicated implementation |
| Corpse/body-part formatting | Pure helper | Shared code without polymorphic variation |

## Suggested implementation sequence

1. Fix and test equipped expiration using a shared cleanup transition. Keep the patch narrow.
2. Consolidate item location/detachment and effect-owner lookup, migrating one consumer at a time.
3. Convert learned-state operations to instance methods and extract learning orchestration behind compatibility wrappers.
4. Add regeneration overrides with deterministic tests guarding arithmetic and random-call order.
5. Consolidate armor and entity normalization after input/output contracts are documented.
6. Extract exposure mechanics and address facade lifecycle incrementally. Fold in the small formatting cleanup when touching the relevant subsystem.

Do not combine these into a broad rewrite. Keep collection documents unchanged for implementation-only refactors. A class extraction should preserve the named operations invoked by content lambdas; new bindings and lazy-load setup belong in `Bootstrapper`. Keep async delivery in handlers and payload routing, outside pure model transitions.

## Review method and validation

Read the repository-local object-oriented-design-review skill and `AGENTS.md`; inspected representative entity, item, spell, combat, service, registry, context, bootstrap, and test paths. Used an AST comparison of class-method bodies to find exact duplicates, then checked their callers. The duplicate scan excludes short methods and cannot detect all semantic duplication. No collection snapshots were inspected or edited, and no application source was changed.

Executed separately with `.venv/Scripts/python.exe`:

| Suite | Result |
| --- | --- |
| `tests.test_acid_exposure` | 13 passed |
| `tests.test_poison_exposure` | 10 passed |
| `tests.test_weapon_hit_effects` | 14 passed |
| `tests.test_spell_affect_payload_messages` | 130 passed |
| `tests.test_update_handler_active_players` | Interrupted after remaining pending without a result; no pass/fail conclusion |

Also executed the actual `_remove_item_at_location` method in isolation using an AST-extracted function and minimal objects: the equipment slot was cleared, while `wear_loc`, `wear_location`, `_effect_wearer`, and the owner's effect list were retained. This directly supports finding 1; it does not establish every downstream server consequence.

The default `python` launcher failed before running the inspection script because its ActiveState wrapper could not access its log/configuration and IPC service in the sandbox. Inspection and completed tests used the repository virtual environment instead. No full test-suite or live-server claim is made.

The working tree was clean at the initial check. A separate modification to `tests/test_combat_api_dynamic_checks.py` appeared during the review; this review did not edit that file. The report is the only file authored for this task.

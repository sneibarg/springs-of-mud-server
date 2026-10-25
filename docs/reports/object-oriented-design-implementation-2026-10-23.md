# Object-oriented design implementation

Implemented the six steps from the [design review](object-oriented-design-review-2026-10-23.md) in its suggested order. Application changes remain in the working tree; no collection documents were changed.

## Changes

1. **Equipment expiration:** added `ItemOwnership` to coordinate effect removal, unequipping, wear metadata, and permanent inventory detachment. Expiration, spell extraction, acid destruction, and weapon collateral damage now share that transition. Detachment uses identity and removes duplicate references without reversing effects twice.
2. **Ownership and ability resolution:** spell world-item traversal and item updates share live-item traversal and location lookup. `AbilityResolver` owns definition lookup without stale caches. Practice retains skills-first precedence; periodic effect lookup retains spells-first precedence and prefix aliases; spell dispel retains its spell-only namespace.
3. **Learning:** learned collections expose instance methods on `Character`. Transient improvement notices have an explicit character field and a shared queue helper. `LearningService` coordinates registry resolution, rules, random inputs, and XP through explicit collaborators. `Ability` retains compatibility entry points and gains definition-local class-level/rating queries. Bootstrap binds and configures the service.
4. **Regeneration:** `AnimateEntity` keeps resource caps, room/furniture multipliers, and affect penalties. `Character` and `Mobile` override the base gain calculations. The shared model no longer branches on NPC identity or imports player learning to calculate regeneration.
5. **Armor and entity state:** player/mobile armor adapters share `ArmorValues`, preserving their existing serialized field names and formats. Combat owns dexterity adjustment and scaling. Position interpretation delegates to the entity contract with explicit legacy fallbacks; affected-bit operations share the `StatusFlags` guarded-write path.
6. **Exposure, lifecycle, and formatting:** extracted `ElementalExposure`, shared by injected spell and weapon handlers. Acid/poison/elemental exposure share chance and item-type helpers while retaining their distinct immunity and mutation rules. Facades share bootstrap dependency snapshots and actor initialization; reset clears all configured facade dependencies/enum aliases and registered learning/effect-service adapters. Corpse/body-part construction shares pure naming and template helpers.

The spell/weapon facade methods remain available. Armor's legacy raw `get_ac` adapter remains separate from combat-scaled AC. Async delivery, effect-owned content payloads, expiration spill rules, and the existing action-model/loader inheritance remain in place.

Package exports for `skill` and `server` now load lazily so importing resolver or logging helpers does not eagerly load the server/model graph. Internal skill imports use explicit model modules. This avoids import cycles exposed by separating the collaborators.

## Validation

- Compiled `src` successfully with `.venv/Scripts/python.exe -m compileall -q src`.
- Ran all **71 top-level unittest modules in separate processes**. **67 modules passed, containing 890 tests**.
- Added 12 regression/contract tests for effect-aware detachment, duplicate references, definition precedence/reload behavior, learned collections, learning RNG/XP/messages, armor formats/reversal, position fallbacks, flag writes, regeneration random order/caps, bootstrap injection, and reset lifecycle.
- Updated existing fixtures to exercise actual regeneration subclasses, the extracted exposure saving-throw collaborator, and explicit module dependencies.
- Verified bootstrap/service imports and real injector resolution of the shared exposure and learning services without starting the network server.
- `git diff --check` reports no whitespace errors.

Four modules still fail. Each failure was reproduced separately from a temporary archive of untouched `HEAD` (`cac412d`):

| Module | Reproduced baseline issue |
| --- | --- |
| `tests.test_area_pet_shop_resets` | Fixture stubs `server.messaging` without the imported `MessageBus` submodule |
| `tests.test_combat_api_dynamic_checks` | Guard-view fixture lacks `context.room` |
| `tests.test_object_fountain_commands` | Six cases use character stand-ins without `owned_items()` |
| `tests.test_player_handler_cast_prompt` | Fixture stubs `server.messaging` without the imported `MessageBus` submodule |

These unrelated failures were left unchanged, including the separate existing edit to `tests/test_combat_api_dynamic_checks.py`.

The isolated runs use the repository virtual environment and `PYTHONPATH=src`. Several existing test modules install process-global import stubs, so loading arbitrary suites together can produce additional fixture collisions; the 890-test result describes isolated modules, not a green single-process discovery run. Async tests ran outside the filesystem sandbox because Windows event-loop initialization otherwise blocked inside local socket-pair creation. No live-world or external content-service integration run was performed.

## Compatibility boundaries

The remaining static `Ability` and weapon exposure entry points are forwarding adapters. New implementations receive collaborators directly; this does not replace every historical facade or service locator in the repository. Separate armor adapter classes remain because their service contracts differ. Exposure variants use composition rather than an artificial shared inheritance tree. These are the incremental boundaries recommended by the review.

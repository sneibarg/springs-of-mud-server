# Repository Guidelines

## Project Direction

This repository is the Python runtime server for Springs of MUD. Keep the long-term product direction in mind: game designers should define and tune game content through data and the separate `springs-of-mud-designer` repository, not by requiring backend source edits for ordinary content changes.

Prefer low-code/data-driven changes when the behavior can reasonably live in `resources/collections` or in the content service contracts. Add Python only for reusable runtime capabilities, engine behavior, or new primitives that designer-authored content can call.

## Architecture Map

- `src/main.py` loads `resources/server.yml` and starts `server.MudServer`.
- `src/server` owns sockets, telnet protocol, sessions, connection handling, service endpoint config, logging, and `Bootstrapper`.
- `Bootstrapper` wires the `injector` container, configures `GameApi`, dynamic enums, registries, handlers, services, and API facades.
- `src/game` owns global runtime state, `GameService`, enum loading, registries/handlers aggregators, the update loop, weather, combat pulses, regen, autosave, and item/effect ticking.
- `src/interp`, `src/skill`, and `src/combat` contain the dynamic command, skill, spell, guard, payload, and action-plan machinery.
- `src/area`, `src/item`, `src/mobile`, `src/player`, and `src/notes` contain domain models, registries, services, and handlers.
- `src/api` contains gameplay facades shared by handlers and dynamic lambdas.
- `src/util` contains normalization, lookup, rendering, movement, combat, item, effect, area, and player helper logic.
- `src/devtools` contains repository-local tools for inspecting collection snapshots.

## Collection Data

Use `$collection-query` before inspecting or editing `resources/collections/*.json`. That skill explains how to query collection snapshots through `python -m src.devtools` without dumping large JSON files into context.

Read a whole collection only when `$collection-query` cannot answer the question or when exact edit context is required. After editing a collection, use the skill again to verify the changed document.

## Low-Code Runtime Patterns

- Commands come from `SOMDB.Commands.json` and become `interp.Command` objects. They may define `lambdas`, `guards`, `payload`, `pipeline`, and metadata such as role, position, usage, and level.
- Skills and spells share `skill.Ability`. They normalize collection JSON into payloads, guards, class level/rating maps, handler IDs, targets, beats, mana, and effect data.
- Guard definitions are data-driven lambda strings compiled by `InterpApi` or `FightApi`. Prefer adding safe helper functions to API/util classes over embedding complex logic in collection lambdas.
- Payloads should flow through `GamePayload`, `PayloadUtil`, `InterpApi.render_message_key`, and `MessageBus`. Use `to_char`, `to_victim`, `to_room`, `to_area`, `to_world`, and `to_wiznet` payload channels instead of writing directly to connections.
- Fight actions use `game.action.ActionDefinition`, `ActionGuard`, `ActionPlan`, and `MessageRef`. Skill documents can provide `fightExecutor`, `fightPlan`, and guards; Python should provide reusable executors or helpers.
- Spell lambdas execute through `SpellApi` and `SpellContext`. Add reusable spell operations to `SpellApi` when designer-authored spell data needs a new primitive.
- Effects are runtime state, but their user-facing payloads belong to the skill or spell document that created or owns the effect. Periodic effect ticks such as plague, poison, or object affect expiration should render message keys from the appropriate `SOMDB.Skills.json` or `SOMDB.Spells.json` payload instead of hard-coding text in `UpdateHandler` or effect utilities.

## Coding Conventions

- The codebase uses dataclasses heavily. Most models expose `from_json` and normalize camelCase service data to snake_case with `GenericUtil.camel_to_snake_case`.
- Registries generally subclass `registries.Registry` and define `lookup_attrs`. Use `get_or_none` for optional lookups and `get` when absence is exceptional.
- Services usually subclass `FetchAndRegisterMixin`, fetch REST data from `ServiceConfig`, build domain objects in `_build_fetch_item`, and register them in `_register_fetch_item`.
- Runtime enums are loaded from `GameData.enums` into `IntEnum` types. Access them through `EnumProvider` or `GameApi`/`CharacterApi` helpers rather than hard-coded numbers.
- ROM-style flags may be stored as letters or integers. Use `GameApi.flags_to_int`, `letters_to_flags`, `flags_to_letters`, `is_set`, `set_bit`, and `unset_bit`.
- Preserve async boundaries. Network/session/message paths are async. The game scheduler runs in a background thread with its own event loop, but dispatches each world update onto the socket event loop, which owns live gameplay and session mutations. Persistence workers receive prepared snapshots; avoid reading or mutating live entities in workers.
- When adding new services, registries, handlers, or API facades, update `Bootstrapper` bindings and lazy-load setup.

## Testing

Use `unittest`; there is no project packaging file at present. Tests usually add `src` to `sys.path` directly and often stub heavy modules to isolate behavior.

Run focused tests for the area you changed:

```powershell
python -m unittest tests.test_devtools_collection_query
python -m unittest tests.test_combat_dynamic_commands
python -m unittest discover tests
```

When changing dynamic command, skill, spell, or collection behavior, add or update tests that load representative documents from `resources/collections` or construct equivalent minimal fixtures. Prefer narrow regression tests around payloads, guards, registry lookups, and runtime side effects.

## Change Discipline

- Do not replace designer-editable data with hard-coded Python behavior unless the task is explicitly to add engine support.
- Keep backend source changes compatible with the designer workflow and content service contracts.
- Do not rewrite unrelated collection documents. Use focused JSON edits and verify with `python -m src.devtools`.
- Avoid broad refactors in shared APIs, handlers, and utilities unless tests cover the affected command families and runtime paths.

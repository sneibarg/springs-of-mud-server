# Repository Guidelines

## Project Direction

This repository is the Python runtime server for Springs of MUD. Keep the long-term product direction in mind: game designers should define and tune game content through data and the separate `springs-of-mud-designer` repository, not by requiring backend source edits for ordinary content changes.

Prefer low-code/data-driven changes when the behavior can reasonably live in `resources/collections` or in the content service contracts. Add Python only for reusable runtime capabilities, engine behavior, or new primitives that designer-authored content can call.

## Reference

Open a reference when the work touches that area.

- Package ownership, startup, sockets, and runtime services ([Architecture Map](docs/references/Architecture.md)).
- Repository alignment, ROM24 reports, and shared AI skill instructions ([Shared AI Skills](docs/references/Skills.md)).
- Querying, editing, and verifying collection snapshots ([Collection Data](docs/references/Collections.md)).
- Data-driven commands, skills, spells, guards, payloads, and effects ([Low-Code Runtime Patterns](docs/references/RuntimePatterns.md)).
- Which tests to run and how to cover dynamic content behavior ([Testing](docs/references/Testing.md)).

## Coding Conventions

- The codebase uses dataclasses heavily. Most models expose `from_json` and normalize camelCase service data to snake_case with `GenericUtil.camel_to_snake_case`.
- Registries generally subclass `registries.Registry` and define `lookup_attrs`. Use `get_or_none` for optional lookups and `get` when absence is exceptional.
- Services usually subclass `FetchAndRegisterMixin`, fetch REST data from `ServiceConfig`, build domain objects in `_build_fetch_item`, and register them in `_register_fetch_item`.
- Runtime enums are loaded from `GameData.enums` into `IntEnum` types. Access them through `EnumProvider` or `GameApi`/`CharacterApi` helpers rather than hard-coded numbers.
- ROM-style flags may be stored as letters or integers. Use `GameApi.flags_to_int`, `letters_to_flags`, `flags_to_letters`, `is_set`, `set_bit`, and `unset_bit`.
- Preserve async boundaries. Network/session/message paths are async. The game scheduler runs in a background thread with its own event loop, but dispatches each world update onto the socket event loop, which owns live gameplay and session mutations. Persistence workers receive prepared snapshots; avoid reading or mutating live entities in workers.
- When adding new services, registries, handlers, or API facades, update `Bootstrapper` bindings and lazy-load setup.

## Change Discipline

- Do not replace designer-editable data with hard-coded Python behavior unless the task is explicitly to add engine support.
- Keep backend source changes compatible with the designer workflow and content service contracts.
- Do not rewrite unrelated collection documents. Use focused JSON edits and verify with `python -m src.devtools`.
- Avoid broad refactors in shared APIs, handlers, and utilities unless tests cover the affected command families and runtime paths.

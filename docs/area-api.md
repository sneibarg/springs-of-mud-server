# Area operations

`AreaUtil` has been removed. Its responsibilities now belong to:

- `AreaApi.find_location(argument, room_registry, character_registry, matcher)`:
  world-location resolution for wizard commands and guard adapters. Search order
  remains room vnum, registered character, room mobile, then room name.
- `Exit.format_destination(...)` and `Exit.direction_label(...)`: exit display.
- `Exit.apply_door_reset(state, exit_flags_enum)`: open/closed/locked reset state,
  preserving unrelated flags and accepting both enum naming conventions.
- `Room.get_formatted_exits()`, `Room.get_exit(...)`, and
  `Room.destination_id_for_direction(...)`: room-owned exit queries.
- `Room.randomize_exits(max_exits, rng)`: sparse exit-slot randomization.

Direction display and room aliases share `Exit.DIRECTION_NAMES`. The redundant
lookup wrappers and the separate `DirectionEnum` have been removed.

`AreaApi` is stateless and bound by `Bootstrapper`; it needs no lazy-load or reset
hook. `InterpApi` exposes it to collection lambdas in place of `AreaUtil`.
Existing `WizApi` guard methods retain their context-adaptation contracts and use
the same location resolver as wizard execution and room-setting commands.
Authorization, privacy checks, and relocation remain with their existing owners.

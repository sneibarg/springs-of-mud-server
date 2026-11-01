# Architecture Map

- `src/main.py` loads `resources/server.yml` and starts `server.MudServer`.
- `src/server` owns sockets, telnet protocol, sessions, connection handling, service endpoint config, logging, and `Bootstrapper`.
- `Bootstrapper` wires the `injector` container, configures `GameApi`, dynamic enums, registries, handlers, services, and API facades.
- `src/game` owns global runtime state, `GameService`, enum loading, registries/handlers aggregators, the update loop, weather, combat pulses, regen, autosave, and item/effect ticking.
- `src/interp`, `src/skill`, and `src/combat` contain the dynamic command, skill, spell, guard, payload, and action-plan machinery.
- `src/area`, `src/item`, `src/mobile`, `src/player`, and `src/notes` contain domain models, registries, services, and handlers.
- `src/api` contains gameplay facades shared by handlers and dynamic lambdas.
- `src/util` contains normalization, lookup, rendering, movement, combat, item, effect, area, and player helper logic.
- `src/devtools` contains repository-local tools for inspecting collection snapshots.

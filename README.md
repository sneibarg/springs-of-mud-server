# springs-of-mud-server

`springs-of-mud-server` is the real-time Python server for *Springs of MUD*, a modernized MUD platform designed by Springy Pythonic Solutions to be a re-imagining of the classic Rivers of MUD (ROM) experience.

In the 90s, when ROM MUDs became popular, they were a place for players to enjoy a fantasy Dungeons and Dragons-like experience, join clans, and meet new friends. Some MUDs were strictly for role-playing, while others were more focused on combat, exploration, and player-versus-player. Coders were often sought by game owners and implementers for their expertise earned through rite of passage.

The project is intentionally being shaped as a low-code/no-code foundation. The long-term product direction is not "developers edit source files to change the game." It is "game designers use tools to define commands, content, rules, and world data without needing to be software engineers." This server exists to execute that content reliably at runtime.

## What This Server Does

- Accepts player connections over telnet-style sockets.
- Authenticates a session and binds it to an in-memory player/character model.
- Loads world data, commands, skills, spells, socials, helps, notes, and other game content from REST endpoints.
- Maintains live registries for rooms, areas, mobiles, items, players, characters, and combat events.
- Runs the continuous game update loop for weather, combat, NPC behavior, item decay, regeneration, and autosave.
- Routes messages, prompts, room output, and broadcasts back to connected players.

## Architecture

This codebase is organized around a few deliberate boundaries:

### 1. Real-time server runtime in Python

The Python process owns the parts of the game that need low-latency state transitions:

- socket handling in `src/server`
- session and connection management in `src/server/session` and `src/server/connection`
- the main game pulse in `src/game/GameService.py`
- world updates in `src/game/UpdateHandler.py`

`src/main.py` starts the server, loads `resources/server.yml`, and boots `MudServer`. `MudServer` starts two concurrent flows:

- an asyncio network server for player connections
- a background game loop thread for simulation pulses

That split keeps connection I/O and world updates decoupled while still running as one application.

### 2. Service / registry / handler layering

The project consistently separates responsibilities:

- **services** fetch and persist data through APIs
- **registries** hold the in-memory runtime state
- **handlers** apply gameplay behavior and side effects
- **APIs** expose reusable gameplay logic for commands and rules

Dependency injection is assembled in `src/util/ServerUtil.py` using `injector`, which keeps startup explicit and makes the runtime graph easier to reason about.

### 3. Data-driven content instead of hard-coded game behavior

One of the central design choices here is that a large amount of gameplay definition is loaded from data rather than baked into Python code. `InterpService`, `SkillService`, `SpellService`, `AreaService`, `RoomService`, `ItemService`, `MobileService`, and related services pull content from external endpoints and register it into the live runtime.

The tests in `tests/` make that direction especially clear: many of them validate **dynamic commands**, **dynamic guards**, and payload-driven behavior rather than only hard-coded command implementations.

### 4. Python runtime paired with external content services

This repository is not trying to be the whole platform by itself. The broader architecture assumes a companion backend that owns persisted content and administrative CRUD workflows. In practice, this server reads endpoint locations from `resources/server.yml` and consumes REST APIs for:

- game data and enums
- players and characters
- commands and helps
- rooms, areas, items, mobiles, shops, resets, and specials
- skills, spells, socials, and notes

That boundary is important: the Python server is optimized for simulation and player interaction, while content storage and editorial workflows can evolve independently.

### 5. Message-oriented runtime behavior

`MessageBus` provides a central path for sending output to one character, a room, an area, or the whole active player set. That keeps prompt rendering, paging, room output, and combat/event text on a common delivery path instead of scattering socket writes across the codebase.

## Why It Is Being Built This Way

The design goal is to let the game become more editable by designers and operators over time.

Instead of requiring a programmer to modify combat text, command metadata, help entries, rooms, resets, or skill definitions in source code, the platform is moving toward a model where those concerns are stored as content and managed through external tools. The intended end state is a game designer user interface that can enhance and customize the world for non-engineers.

That low-code/no-code direction drives several architecture decisions in this repo:

- content is loaded from APIs rather than embedded locally
- commands and checks can be described as data
- runtime state is maintained in registries that can be refreshed from service data
- the server is focused on execution, orchestration, and simulation rather than authoring workflows

In short: this server is the gameplay engine, not the authoring tool. The authoring experience is expected to live on top of the APIs and data model that feed it.

## Repository Layout

- `src/server` - network, protocol, sessions, messaging, and server bootstrap
- `src/game` - global runtime state, update loop, world handlers
- `src/interp` - command interpretation, command metadata, helps, socials
- `src/fight` - combat rules and combat event handling
- `src/area`, `src/item`, `src/mobile`, `src/player`, `src/skill` - domain models, registries, services, handlers
- `src/api` - reusable gameplay APIs shared by command and handler layers
- `resources` - server config plus JSON content snapshots and data fixtures
- `tests` - focused regression and dynamic behavior coverage

## Running the Server

This repository does not currently include a pinned dependency manifest, so environment setup is still manual.

1. Create a Python environment.
2. Install the runtime dependencies used by the codebase, including `PyYAML`, `requests`, and `injector`.
3. Update `resources/server.yml` so the host, port, and service endpoints point at your backend environment.
4. Start the server with:

```bash
python src/main.py
```

## Running Tests

The current test suite is organized under `tests/` and can be run with:

```bash
python -m unittest discover tests
```

## Current Status

The project already reflects the core platform direction:

- the runtime server is in place
- the game loop and update handlers are in place
- content domains are split into registries and services
- command behavior is moving toward dynamic, payload-driven execution

The next major value comes from continuing the low-code/no-code path: building stronger content tooling, tighter API contracts, and a designer-facing interface that can safely modify the game without requiring direct source edits.

# springs-of-mud-server

`springs-of-mud-server` is the Python runtime server for *Springs of MUD*, a modernized MUD platform inspired by classic Rivers of MUD / ROM gameplay.

This repository is one part of a larger platform. It runs the live game process; content authoring and persistence are handled by companion applications and services.

## Related Repositories

- `springs-of-mud-designer` - designer/admin UI for managing game content.
- `som-server-modulith` - backend service for content persistence and administrative APIs.

## Developer Guidance

See `AGENTS.md` for architecture, repository conventions, collection tooling, testing guidance, and change rules.

## Running the Server

This repository does not currently include a pinned dependency manifest, so environment setup is manual.

1. Create and activate a Python environment.
2. Install the runtime dependencies used by the codebase, including `PyYAML`, `requests`, and `injector`.
3. Update `resources/server.yml` so host, port, and service endpoints point at the correct backend environment.
4. Start the server:

```bash
python src/main.py
```

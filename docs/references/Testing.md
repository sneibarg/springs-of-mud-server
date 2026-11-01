# Testing

Use `unittest`; there is no project packaging file at present. Tests usually add `src` to `sys.path` directly and often stub heavy modules to isolate behavior.

Run focused tests for the area you changed:

```powershell
python -m unittest tests.test_devtools_collection_query
python -m unittest tests.test_combat_dynamic_commands
python -m unittest discover tests
```

When changing dynamic command, skill, spell, or collection behavior, add or update tests that load representative documents from `resources/collections` or construct equivalent minimal fixtures. Prefer narrow regression tests around payloads, guards, registry lookups, and runtime side effects.

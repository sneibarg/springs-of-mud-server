---
name: collection-query
description: Use the repository's devtools collection query CLI to inspect resources/collections/SOMDB.*.json without dumping large JSON files into context. Use when Claude Code needs to understand, search, compare, summarize, or modify collection data such as skills, spells, commands, items, mobiles, rooms, resets, socials, specials, helps, areas, classes, races, shops, characters, notes, or game data.
---

# Collection Query

Use `python -m src.devtools` from the repository root to inspect `resources/collections` before reading or editing collection JSON files directly. Prefer concise CLI output over `Get-Content`, PowerShell JSON parsing, or loading full collection files into context.

## Core Workflow

1. Start with `python -m src.devtools list` to see available collection names and document counts.
2. Use `summary` or `fields` to understand shape before querying unfamiliar collections.
3. Use `find`, `get`, `values`, and `path` to answer targeted questions.
4. Use the `collection-modify` skill for safe collection rewrites when an edit is needed.
5. Read a full JSON file only when the CLI cannot answer the question or when an exact edit location is required.
6. After modifying a collection, query the changed document again to verify the relevant fields.

## Commands

List collections:

```powershell
python -m src.devtools list
```

Summarize one or more collections:

```powershell
python -m src.devtools summary skills
python -m src.devtools fields skills
```

Find matching documents without printing full JSON:

```powershell
python -m src.devtools find bash skills --search-field name --field name --field handlerId --field target
python -m src.devtools find healer mobiles --field vnum --field name --field shortDescription --limit 10
```

Fetch one document by exact `name`, `vnum`, `_id`, `id`, `handlerId`, or `command`:

```powershell
python -m src.devtools get skills axe
python -m src.devtools get items 6600 --field vnum --field name --field itemType --field level
```

Inspect one nested field path:

```powershell
python -m src.devtools path skills axe payload.toChar.msgOff
python -m src.devtools path skills axe levelByClass
```

Count distinct values:

```powershell
python -m src.devtools values skills target
python -m src.devtools values skills levelByClass.warrior
```

Print full JSON only for a single matched document when needed:

```powershell
python -m src.devtools get skills axe --json
```

## Editing Guidance

Use CLI queries to identify the document and field values first. Then use the `collection-modify` skill for validated dry-run edits and safe rewrites. Do not paste or inspect entire large collection files unless the task requires exact surrounding JSON context.

If running outside the repository root, pass the collection directory explicitly:

```powershell
python -m src.devtools --collections-dir C:\Users\scott\PycharmProjects\springs-of-mud-server\resources\collections list
```

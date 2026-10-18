---
name: collection-modify
description: Use the repository's devtools collection modify CLI to safely rewrite resources/collections/SOMDB.*.json with validation and dry-run output. Use when Codex needs to edit collection documents, set existing fields, explicitly add new nested object sections or keys, rename existing subsections, or verify collection changes without hand-editing large JSON files.
---

# Collection Modify

Use `python -m src.devtools modify ...` from the repository root for collection JSON edits. The modify CLI is dry-run by default, validates type and key conventions, and only rewrites files when `--write` is explicitly passed.

Before editing, use `$collection-query` to identify the target collection, document key, field path, and current value.

## Workflow

1. Query the target document with `$collection-query`.
2. Run the modify command without `--write` and inspect the printed change.
3. Re-run the same command with `--write` only when the dry-run output is correct.
4. Query the document again with `$collection-query` to verify the changed value.

## Commands

Set an existing field:

```powershell
python -m src.devtools modify set skills axe target IGNORE
python -m src.devtools modify set skills axe target IGNORE --expect-current IGNORE
```

Set a non-string value by parsing JSON:

```powershell
python -m src.devtools modify set skills axe slot 0 --json-value
python -m src.devtools modify set commands bash enabled true --json-value
```

Create a missing key or missing object path only with explicit section creation:

```powershell
python -m src.devtools modify set skills axe payload.toChar.success "Done." --add-section
python -m src.devtools modify add-section skills axe payload.toRoom
python -m src.devtools modify add-section skills axe payload.toRoom --value '{"success":"Done."}'
```

Rename an existing subsection only with explicit rename:

```powershell
python -m src.devtools modify rename-section skills axe payload toChar toRoom
```

Pass `--lookup-field` when the document key should match a field other than the default lookup fields:

```powershell
python -m src.devtools modify set commands doSomething enabled false --lookup-field name --json-value
```

Pass `--collections-dir` when running outside the repository root:

```powershell
python -m src.devtools modify --collections-dir C:\Users\scott\PycharmProjects\springs-of-mud-server\resources\collections set skills axe target IGNORE
```

## Safety Rules

- Treat dry-run output as mandatory review. Do not add `--write` until the document id, path, old value, and new value are correct.
- Use `--expect-current` for changes where overwriting an unexpected value would be risky.
- Use `--json-value` for booleans, integers, arrays, objects, and `null`.
- Use `set --add-section` or `add-section` when adding a new nested key or object section.
- Use `rename-section` when renaming an existing subsection. Do not simulate a rename by adding one key and deleting another manually.
- Read or hand-edit a full collection file only when the modify CLI cannot express the required change.

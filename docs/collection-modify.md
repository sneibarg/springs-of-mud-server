# Collection modification

Run the CLI from the repository root. All operations print a dry run unless
`--write` is passed.

## Add a document

Append a complete document from a UTF-8 JSON file to an existing collection:

```powershell
python -m src.devtools modify add-document skills --value-file new-skill.json
python -m src.devtools modify add-document skills --value-file new-skill.json --write
```

Alternatively, pass inline JSON with `--value`:

```powershell
python -m src.devtools modify add-document skills --value '{"name":"new skill"}' --lookup-field name
```

The input must be a non-empty JSON object. Supply at least one identifier:
`_id` (a string or MongoDB `$oid` object), `id`, `vnum`, or a field specified
with `--lookup-field`. Identifiers must be non-empty strings or integers.
Existing `_id`, `id`, and `vnum` values are checked for duplicates automatically.
Repeat `--lookup-field` to check additional unique fields or dotted paths.
Names and handler IDs are not assumed unique unless explicitly selected.

The command appends the supplied object without generating IDs, filling defaults,
or enforcing a gameplay schema. Existing documents retain their values and order;
writing uses the CLI's standard atomic JSON rewrite. No new collection is created.
Review the full proposed document in the dry run before writing, then verify with
`python -m src.devtools get skills <identifier> --json`.

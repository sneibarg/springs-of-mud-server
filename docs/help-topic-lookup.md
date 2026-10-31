# Help topic lookup

`help <topic>` returns one document selected by an exact topic or a configured command shortcut. Case, surrounding quotes, and repeated whitespace are normalized. Arbitrary prefixes and words occurring in help prose are not searched. No argument selects `summary`; an unknown topic returns the existing no-help response.

Help documents in `SOMDB.Helps.json` now provide an explicit `topics` array:

```json
{
  "keyword": "HOLD REMOVE WEAR WIELD",
  "topics": ["hold", "remove", "wear", "wield"],
  "level": 0,
  "text": "Syntax: hold <object>..."
}
```

`keyword` remains the display title. `topics` is the complete lookup allowlist, including aliases and multiword phrases; it takes precedence over the title. An explicit empty list makes the document unavailable by topic. Keep aliases unique across documents. A shared document can describe several commands, but a query returns that document once. The command association built by InterpService and live help lookup use the same HelpRegistry resolver.

Command/spell name collisions are explicit: `sleep`, `teleport`, and `invis` select command help, while `sleep spell`, `teleport spell`, and `invisibility` select spell help. `mass invis` and `invis spell` also select the invisibility spell document.

For older service records without `topics`, a valid keyword header supplies exact aliases, respecting quoted phrases. Multiline prose and tilde-delimited imports are not treated as legacy alias headers. Duplicate aliases in remote/legacy records still select only one document, preferring an exact title and then stable document ID. No concatenation occurs. Service IDs are retained, including MongoDB `$oid` values; transport metadata is ignored.

The repair preserved all 168 existing document IDs, corrected 55 malformed records whose keyword fields contained body text, and separated three merged documents: invisibility spell help, IMOTD, and CLAN. Source-matched repairs restored titles, bodies, and levels from the local ROM area help files; custom records and custom merged text were preserved. The collection now contains 171 documents and 300 unique topic aliases.

Deploy the corrected help collection through the content service and preserve the new `topics` field in its response. Existing running servers need the runtime change and a help reload or restart. Help queries read the live registry rather than stale command attachments. Automated tests cover every collection topic, command associations, aliases, collisions, reloads, shared-registry injection, and single-message emission. External service persistence was not exercised.

## Missing ROM help import — October 31, 2026

The collection now contains **251 pages and 421 unique topics**. The missing content was primarily in ROM24's `area/group.are`, which contains skill, race, group and newer spell help, including KICK. Added 79 records from that file and one record from `area/help.are` for uncovered note-board aliases. All 171 preexisting documents, IDs, text and explicit topic mappings remain unchanged. Existing aliases take precedence over imported ones; for example, `pick` keeps its command page while `pick lock` receives the skill page. `mass healing` resolves as a spell phrase separately from the `healing` skill group.

All `.are` files in the reference `area.lst` were inspected for `#HELPS` sections; only help.are, rom.are and group.are contain nonempty ones. The importer reads signed levels and tilde-terminated headers/bodies, respects quoted aliases, stops at the `$` sentinel and preserves body paragraphs. Reimporting the updated collection produces no additions.

Reproduce the dry-run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m src.devtools.import_rom_helps --area-dir C:/Users/scott/PycharmProjects/PyRom/Rom24/area
```

Use `--write` after reviewing the plan. This dedicated importer is needed because collection-modify supports editing existing documents rather than appending new documents. It uses the shared validated collection loader/writer. On this Windows checkout atomic replacement was denied; `--write --in-place` provided a verified append while retaining existing formatting. The import plan is saved in `docs/reports/rom24-help-import-2026-10-31.json`.

Validation: four importer tests and 17 help lookup tests pass, including lookup of every configured topic, command associations, aliases and existing disambiguation. Source coverage and preservation checks found no missing import candidates or source aliases and confirmed all original documents remain identical. No runtime or reference-C behavior was changed. Publish the updated Helps snapshot through the content service and reload helps or restart the server to make the new pages live; no live service deployment was performed here.

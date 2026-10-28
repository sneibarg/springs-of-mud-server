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

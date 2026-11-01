---
name: align-repository
description: Review Springs of MUD cross-repository API, content schema, and runtime compatibility with som-server-modulith and springs-of-mud-designer. File an alignment report with proposed changes without applying updates.
---

# Align Repository

Compare this runtime with the target repositories and report alignment gaps and
proposed changes, preserving designer-authored content and runtime responsibilities.
Do not modify source, tests, configuration, or collection data in any compared
repository. The only output written by this skill is the alignment report.

## Target repositories

- `som-server-modulith`: content service APIs and contracts.
- `springs-of-mud-designer`: designer models, validation, and authored content.

Use the target repository name above for each report. When comparing both targets,
file a separate report for each.

## Establish the comparison

- Read this repository's `AGENTS.md` and relevant companion-repository instructions.
- Locate companion checkouts from workspace context and nearby project directories;
  do not assume fixed absolute paths. If a required repository is unavailable,
  request its location or relevant diff and continue independent work here.
- Inspect branches, HEAD revisions, and working-tree changes. Honor user-supplied
  commit ranges, branches, diffs, or feature scope. Otherwise establish the relevant
  changes from history and documentation, stating the baseline and uncertainty.
  Do not assume the latest commit captures every change or that branches share a baseline.
- Treat all compared repositories as reference inputs.
  Do not pull, switch branches, or discard local changes merely for comparison.

## Trace compatibility

Follow each relevant change from its definition through its producer and consumer.
Use source evidence and representative documents to establish actual contracts.
Check the affected subset of:

- Service routes, methods, request/response envelopes, pagination, errors, and
  configuration against this runtime's services and `ServiceConfig`.
- Designer models, editors, defaults, validation, and saved/exported documents
  against runtime `from_json` normalization and content service contracts.
- Field names/types, optional/null/missing values, identifiers, references, enums,
  flags, and defaults across the affected repositories.
- Commands, skills, spells, guards, lambdas, payload/message keys, action plans,
  effects, and the runtime helpers that execute designer-authored data.
- Loading, registration, caching/reload, and persistence for changed contracts.

Use `$collection-query` before inspecting collection snapshots. Establish whether
the service, designer, or a snapshot defines the intended contract; local snapshots
may lag the other repositories. Do not migrate or rewrite documents.

Distinguish confirmed incompatibilities from intentional differences, unrelated
changes, and product decisions. If producer and consumer disagree, report the
source evidence rather than silently selecting one as authoritative.

## Assess proposed alignment

Prefer content/configuration for ordinary game design and reusable Python
primitives for engine capabilities. Follow `AGENTS.md` for normalization, dynamic
enums/flags, payload rendering, event-loop ownership, and Bootstrapper wiring.
Do not propose copying another repository's architecture merely to align contracts.

Describe required defaults, migration behavior, and compatibility with older
documents when the intended contract requires them. Avoid speculative fallbacks
that hide malformed content and unrelated document rewrites. Identify focused
validation needed for a proposal without adding or updating tests.

## Report

File the report in `docs/alignment` in this repository. Create the folder when it
is missing. Name the file with the target repository from Target repositories and
the local time it is filed, in 24-hour form:
`<repository>_<YYYY-MM-DDTHHMMSS>.md`.

Record the compared revisions, local changes considered, comparison scope, and
source evidence. State the local filing time and timezone.

For each recorded gap, name the file, the standard it addresses, and the proposed
change, including any move, importer, and cycle notes. Cite the source locations
that establish the standard and the gap. State when move, importer, or cycle
notes do not apply.

If the comparison finds no gap, say there is nothing to propose. If a gap cannot
be stated precisely, name the file and what is still unknown.

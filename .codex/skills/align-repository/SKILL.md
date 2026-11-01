---
name: align-repository
description: Align the Springs of MUD Python runtime with changes in som-server-modulith and springs-of-mud-designer. Use for cross-repository API, content schema, and runtime compatibility updates or alignment reviews.
---

# Align Repository

Keep this runtime compatible with changes in `som-server-modulith` and
`springs-of-mud-designer`, preserving designer-authored content and the Python
runtime's responsibilities.

## Establish the comparison

- Read this repository's `AGENTS.md` and relevant companion-repository instructions.
- Locate companion checkouts from workspace context and nearby project directories;
  do not assume fixed absolute paths. If a required repository is unavailable,
  request its location or relevant diff and continue independent work here.
- Inspect branches, HEAD revisions, and working-tree changes. Honor user-supplied
  commit ranges, branches, diffs, or feature scope. Otherwise establish the relevant
  changes from history and documentation, stating the baseline and uncertainty.
  Do not assume the latest commit captures every change or that branches share a baseline.
- Treat companion repositories as reference inputs unless edits there are requested.
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

Use `$collection-query` before inspecting collection snapshots and
`$collection-modify` for rewrites; both skills live alongside this skill.
Query edited documents again to verify them. Establish whether the service,
designer, or a snapshot defines the intended contract before migrating data;
local snapshots may lag the other repositories.

Distinguish confirmed incompatibilities from intentional differences, unrelated
changes, and product decisions. If producer and consumer disagree, report the
source evidence rather than silently selecting one as authoritative.

## Apply scoped alignment

For implementation requests, carry confirmed changes through the affected runtime
paths. For review-only requests, report findings without changing files.

Prefer content/configuration for ordinary game design and reusable Python
primitives for engine capabilities. Follow `AGENTS.md` for normalization, dynamic
enums/flags, payload rendering, event-loop ownership, and Bootstrapper wiring.
Do not copy another repository's architecture merely to align contracts.

Choose defaults and migration behavior deliberately. Preserve older documents
when the intended contract requires them; avoid speculative fallbacks that hide
malformed content and unrelated document rewrites.

## Verify and report

Add or update focused `unittest` coverage for changed contracts using representative
producer/designer documents or equivalent minimal fixtures. Exercise affected
service deserialization and runtime side effects, including relevant defaults,
omitted fields, and invalid values. Run focused tests and broader checks justified
by the affected paths.

Report compared revisions and local changes considered, confirmed contract changes,
files updated, validation results, and remaining incompatibilities or unavailable
integration checks. Cite source locations for unresolved issues and identify any
companion-repository work still needed.

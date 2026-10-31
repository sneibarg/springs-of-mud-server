# Report and pseudo-suite format

Use this format by default; adapt the representation if the user requests another format. The semantic fields matter more than exact headings. Reports are specifications, not assertions that the target implementation already passes.

## Artifacts

- `report.md`: scope and snapshot, behavioral contracts, path ledger, fixture profiles, notable quirks/decisions, migration notes and unresolved work. Include readable case summaries and language-neutral pseudocode, factoring repeated setup through explicit fixture profiles.
- `cases.json`: portable case catalog with source-derived expectations.
- `manifest.json`: file/function inventory, coverage dispositions and links to cases. This is also the continuation checkpoint for a large review.

Use paths relative to each identified repository in structured references. Include local clickable absolute links in Markdown when available. Record branch IDs in the ledger; line numbers support navigation but are not the identity of a branch.

## Manifest fields

Include:

- `schema_version`: `1`.
- `scope`: requested paths/functions, exclusions explicitly requested, resolved source root and target root if used.
- `snapshot`: revision or unknown, dirty status, build assumptions and a per-file SHA-256 map. Note unavailable build configuration rather than assuming one silently.
- `inventory`: each file's path, role and status; each defined function's name, entry routes, status, relevant helper/data dependencies and branch ledger.
- `branch ledger`: stable ID, source reference, ordered predicate/outcome, disposition and case IDs. Dispositions distinguish `specified`, `blocked`, `unreachable`, `disabled`, `out_of_scope` and `pending`. Explain exclusions and reachability claims.
- `verification`: structural checks performed and any actual compile/probe/test commands and results. List missing dependencies and pending decisions.

Counts must distinguish functions inventoried from functions traced, and cases specified from cases dynamically verified. No coverage percentage should imply executable branch coverage unless it was actually measured.

## Case fields

Use stable IDs such as `fight.damage.safe-room-rejects-npc` or `update.char_update.poison.tick-damage`; add a semantic suffix or parameter IDs for boundaries. Retain IDs when line numbers move.

A case object has:

- `id`, `title`, `status` (`specified` or `blocked`) and `branch_ids`.
- `source_refs`: objects with `file`, `function`, `line` and optional `repository`; point at the decisive C predicates and side effects, not just the function start.
- `entry`: function/dispatch route, arguments, caller prerequisites and return domain. Distinguish a direct-helper call from interpreted input.
- `fixture`: an explicit named profile plus overrides, or a complete initial state. Include actor/target kind, relevant flags/stats/resources, room/world membership, carried/worn/container ownership, active effects and connection/controller state when used by the path. Values irrelevant to the outcome can be omitted with an explicit dependency contract.
- `controls`: deterministic random draws keyed by ordered call, clock/tick values, helper return values or failure injection. Identify whether a controlled helper is a stubbed boundary or was traced into additional cases. Never stub away the predicate being tested.
- `action`: one input, function invocation or scheduled event. Use separate cases for distinct actions unless a sequence is essential to the stateful path.
- `expected`: return/control outcome, ordered events, resulting state, relevant unchanged state and forbidden events. Describe exact arithmetic, message channels/recipients and ordering. If wording is intentionally target-specific, identify the message semantic/key and distinguish that override from the literal C text.
- `evidence`: `static_trace` by default, with actual probe/test references only when executed.
- `open_questions`: unresolved oracle/configuration decisions; a blocked case must name why no portable expected outcome is available.
- `adaptation`: optional Python or other-language fixture/API mappings and approved behavior overrides. Keep these separate from the source expectation.

Use JSON values or strings that clearly denote expressions/symbols. Distinguish C NULL, absent state, zero and an empty string; annotate pointer relationships using entity IDs rather than relying on language-specific object identity syntax. Express flag masks by symbolic enum names with the resolved definition referenced. Define units for waits, pulses, game ticks, weight and currency.

## Pseudocode pattern

```text
CASE <stable case ID>
SOURCE <verified C file:function:line references>
GIVEN <fixture profile and concrete overrides>
AND <scripted random draws and traced dependency contracts>
WHEN <entry route receives input/event>
THEN <ordered observable events>
AND <specific final state and relevant unchanged fields>
AND NEVER <forbidden side effects or recipients>
```

This pattern is a specification template, not a license to leave placeholders in delivered cases. For formulas, include a worked input/output boundary rather than only repeating the expression. For randomness, cover equality and adjacent values at strict/inclusive cutoffs and distinguish individual roll outcomes from their resulting probabilities. For time-dependent behavior, state the number and order of scheduler invocations.

## Coverage ledger and cross-checks

A useful ledger row is:

```text
branch ID | C predicate/return | reachable caller routes | case IDs | disposition/gap
```

Check that:

1. Case and branch IDs are unique; every linked ID resolves in both directions.
2. Every requested file/function is present and every discovered branch has a disposition.
3. Scripted random calls match source order, including short-circuited calls that must not occur.
4. Earlier failures dominate later guards as in C, including any costs or waits before a return.
5. Ownership/state assertions account for extracted objects, effect reversal and all relevant recipients.
6. Suspected C bugs, approved target differences and unresolved/undefined behavior remain visibly separate.
7. The manifest names files/functions still pending. Partial work never inherits a complete status from an older report.

For a Python adapter, map neutral actor/world/message fixtures to the repository's actual models and payload pathways, then use unittest assertions at those boundaries. An expected event list can drive another language's test harness without retaining the Python class names. Do not report generated pseudocode or JSON cases as passing tests.

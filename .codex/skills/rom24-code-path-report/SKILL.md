---
name: rom24-code-path-report
description: Trace execution paths through one, several, or all ROM24 C files and generate a source-grounded, language-neutral pseudo test suite for Python regression tests or migration to another language. Use for requested code-path reports, branch inventories, and behavioral test specifications; use rom24-parity instead for comparing implementations or fixing parity defects.
---

# ROM24 code path report

Produce a behavioral specification from the local ROM24 C source. The primary deliverable is a pseudo test suite, not an implementation review or runnable test code. Cases should be specific enough to implement with Python unittest or a different language's test framework without rereading the entire C function.

## Scope and source authority

- Resolve the reference tree from a user-specified ROM24 checkout, otherwise use the sibling `../PyRom/Rom24/src` relative to this repository when present. The current Springs of MUD repository is the default Python consumer. If the reference checkout cannot be found, ask for its location; do not silently substitute an online ROM version. Read applicable repository instructions. Do not modify the C source, game content, runtime, or existing tests merely to generate this report.
- Accept a single file, a list of files/functions, or the whole C codebase. Resolve explicit targets first. If scope is absent, ask which files or functions to trace rather than silently selecting a whole-repository audit.
- For whole-codebase requests, inventory the source files and function definitions first. Include headers, macros, dispatch tables, function pointers, disabled code and non-gameplay files in the inventory with an explicit disposition. Follow relevant area files and other loaded data when they change execution. Do not claim all files or paths reviewed after a sampling pass.
- Identify the exact source snapshot: repository revision, working-tree status, and content hashes for reviewed files. Cite repository-relative file paths, function names and verified line numbers; dirty files require hashes rather than a commit ID alone. Record build/configuration assumptions. Never treat recollections of standard ROM as evidence for this checkout.
- Existing Python code or tests can guide integration notes, but the C path supplies the expected behavior. Do not derive expected results from Python's current implementation. Repository architecture and intentional game differences are adaptation constraints, not reasons to rewrite the C specification.

## Trace paths and contracts

For each in-scope function, distinguish its entry contract from the caller's contract. Inventory direct callers, command dispatch entries, scheduled ticks, specials, and other indirect invocation routes that materially affect reachability. Check whether a caller's guard is absent when the function is invoked internally.

Read callees, macros, enum/flag definitions and tables far enough to determine observable behavior. Record an explicit unresolved dependency if tracing stops. A helper name alone is not evidence that a check or side effect occurs.

Build a path ledger linking code branches and meaningful implicit branches to cases:

- Each guard and early return; ordered guards where more than one can fail; success and failure branches; fallthrough and default cases.
- Short-circuit AND/OR conditions, NULL checks, flag combinations, NPC/player and trust/level exceptions, visibility, lookup location/keyword/ordinal semantics and ownership.
- Formula boundaries, caps, strict versus inclusive comparisons, integer truncation, negative operands, probability endpoints and random-call order. Do not translate C integer arithmetic using Python `/` or `//` without checking its semantics for the actual domain.
- Loop scenarios: zero, one and multiple elements; early exit, mutation/removal during iteration, matching order and relevant limits. Use bounded behavior classes rather than claiming to enumerate infinite loop or recursion paths. Include recursion termination and reentry protections when applicable.
- Effects, damage, currency/resources, waits/daze, combat starts/stops, movement, object extraction, equipment, persistence and messages. Track when side effects happen relative to failure, calls and returns, not just the final state.
- Other people/objects in scope: actor, target, observers, groups, followers, owners, rooms and world registries. Record who must remain unchanged and who must not receive messages when those are behavioral assertions.

Avoid multiplying every condition into an exhaustive Cartesian product. Select feasible paths that distinguish observable outcomes; give individual predicates boundary cases and use combinations when they expose ordering, interaction or short-circuit behavior. State the chosen coverage criterion and remaining gaps. Label unreachable or disabled paths with source evidence instead of deleting them from the ledger.

## Generate the pseudo suite

Read [references/report-format.md](references/report-format.md) when producing artifacts. By default create a Markdown report plus a JSON case catalog and coverage manifest under `docs/reports/rom24-code-paths/<scope-slug>/` in the current writable workspace. Respect the user's destination and output-format preferences. Keep the source checkout read-only and never overwrite unrelated reports.

Each runnable-specification case needs concrete initial state, input/entry point, controlled collaborators/randomness, ordered expected behavior and source references. Derive exact values and ranges from the C path. If no expected result can be established, mark the case blocked and explain what evidence is missing; do not invent an assertion or use a passing placeholder.

Keep case IDs stable across report revisions. Trace each case to the path ledger, and each ledger item to a case or a documented exclusion/gap. Factor common setup into named fixture profiles only when all relevant values remain explicit. Record helper contracts separately where many cases share them.

Preserve source quirks as described behavior. Flag suspicious-but-defined behavior as a reference quirk with a proposed decision, not an automatically corrected expectation. For undefined, implementation-defined or platform-dependent behavior, record the limitation and platform assumptions; do not specify one accidental result as portable truth. Separate the C oracle from intentional target-game overrides and document the authorization for any override.

## Python and migration use

- Include a concise mapping from neutral entities/events to likely Python fixtures, APIs, payload channels and unittest assertions when Python integration is requested or the default consumer is present. Read actual Python paths before naming a mapping. Keep unmapped paths explicit.
- Do not require the target to reproduce C structs, allocation, globals, function layout or synchronous networking. Assert the behavioral contract at the target's appropriate execution boundary, preserving meaningful timing and ordering.
- Use deterministic random sequences or scripted collaborators; state which calls consume which values. Assert emitted messages/recipients and state transitions rather than only a Boolean return. Test doubles should model dependency contracts, not duplicate the algorithm under test.
- Executable tests are a separate deliverable only when requested. Default output uses language-neutral Arrange/Act/Assert pseudocode and structured data; it must not import the Python runtime or depend on a live server to be understood.
- If inspecting designer-authored Python collection data for adaptation, use the repository's collection-query workflow when available. Content edits and unrelated parity fixes are outside the reporting task.

## Validate and finish

Parse generated JSON, check unique IDs and reference integrity, and ensure every in-scope inventory item and ledger item has a disposition. Recheck branch predicates, expected arithmetic, random boundaries and citations against the source; structural validation alone does not prove behavioral completeness. Only label a path dynamically verified when an actual probe or test exercised it; report exactly what ran.

For large scopes, process coherent subsystems and checkpoint the same manifest as work progresses. Reuse fixture/helper contracts across batches. If the work remains partial, name completed and pending files/functions and continue from that checkpoint; do not silently narrow the original scope or call a partial catalog complete.

The final reply should link the artifacts, state source scope and snapshot, summarize cases and coverage gaps, and distinguish source inspection, pseudo tests, generated executable tests and tests actually run. Do not claim whole-server parity or test coverage from this specification alone.

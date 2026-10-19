---
name: rom24-parity
description: Compare Springs of MUD Python gameplay behavior with the local PyRom ROM24 C source in detail. Use for ROM24 parity reviews or parity fixes; exclude architectural preferences and intentional game design differences.
---

# ROM24 behavioral parity

Use `C:/Users/scott/PycharmProjects/PyRom/Rom24/src` as the reference implementation and `C:/Users/scott/PycharmProjects/springs-of-mud-server` as the Python implementation. Read applicable repository instructions. Treat the C checkout as reference material; do not modify it unless explicitly requested.

## Scope and intentional differences

Compare observable gameplay behavior and implementation details that affect it. Do not require matching C structure, memory management, naming, object layout, synchronous execution, or static tables when Python uses services, async messaging, registries, dynamic enums, or designer-authored data.

Respect intentional product and game design choices established by the user, repository guidance, or explicit documentation. Exclude those choices from parity findings; compare the remaining behavior within the chosen design. A difference alone does not establish a deliberate decision. If intent is unknown, identify the discrepancy as unresolved rather than assuming either a bug or an exemption. Ask only when that uncertainty materially blocks the requested work.

Review requests authorize investigation and findings, not implementation edits. When fixes are requested, preserve the Python architecture and designer workflow. Prefer content changes for content behavior and reusable Python primitives for engine support. Do not expand a focused request into a whole-server audit.

## Trace and compare

- Locate the relevant C functions with `rg` in the reference `src` directory. Follow called helpers, macros, headers, flags, tables, and update-loop callers far enough to establish actual behavior. Use this checkout rather than recollections of standard ROM behavior.
- Locate the Python execution path, including handlers, API/util helpers, guards, action plans, payloads, and collection definitions. Use `$collection-query` before inspecting collections and `$collection-modify` when editing them, following repository instructions. A missing Python function name is not proof of missing behavior.
- Compare equivalent initial states and inputs. Track branch ordering, prerequisites, target lookup, NPC/player exceptions, success/failure paths, state changes, and side effects. Include early returns and the timing of resource charges, waits, combat starts, effects, movement, and object removal where relevant.
- Check formulas, bounds, rounding, integer division, probability endpoints, random roll frequency, flag semantics, stacking, duration units, and tick/pulse timing. Python division, negative rounding, truthiness, and random APIs can differ from C; establish the values and helper semantics before claiming a mismatch. Do not prescribe C undefined behavior as a parity requirement.
- Compare messages and recipients, substitutions, visibility rules, and ordering when those are within scope. Follow Python payload/message rendering instead of treating data-driven text as absent. Respect established wording or presentation changes.
- Inspect existing focused tests. For requested fixes, add meaningful `unittest` regressions for demonstrated mismatches, including representative collection data or minimal equivalent fixtures where appropriate, and run the affected tests. Derive expectations from the C path under the accepted design constraints.

## Findings and evidence

Report actionable behavioral mismatches with both C and Python file/line references, the triggering state/input, expected versus actual behavior, and the gameplay consequence. Distinguish verified defects from uncertain discrepancies and unexamined paths. Mention intentional differences only when needed to explain an exclusion; do not present design critiques as defects.

State the reviewed scope and validation performed. If no mismatches are found, say so within that scope and disclose material gaps; do not claim comprehensive parity from static inspection or a few tests. When implementing fixes, summarize the behavior corrected and the test results.

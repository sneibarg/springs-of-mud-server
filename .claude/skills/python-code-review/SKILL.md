---
name: python-code-review
description: Review Python code or changes for correctness, repository architecture alignment, object-oriented responsibility placement, and maintainability. Recommend design patterns when they simplify a demonstrated problem. Use for requested Python code reviews and design reviews; reviewing alone does not authorize implementation changes.
---

# Python Code Review

Produce an evidence-based review that explains concrete defects and design improvements in the requested scope. Preserve the project's architecture and product direction rather than imposing a preferred style.

## Establish the architectural context

- Read the applicable AGENTS.md and AGENTS.override.md instructions, including instructions scoped to the files under review. Use them as the source of truth for architecture, ownership boundaries, data-driven behavior, conventions, and verification. Do not copy a particular repository's architecture into this skill.
- Identify the review target from the request: working changes, a commit or branch comparison, a pull request, or named files/classes. Inspect the relevant diff and existing working changes without altering them. If the target is ambiguous, inspect what is available and clarify only the ambiguity that affects the review.
- Follow relevant repository skills when handling specialized resources, such as collection data. If architecture instructions are absent or incomplete, infer conventions from neighboring implementations and label assumptions explicitly.
- Read callers, model definitions, service boundaries, and representative tests far enough to understand behavior and dependencies. For a migration or compatibility review, compare the referenced implementation when available and distinguish intentional redesigns from behavioral regressions.

## Review behavior and object ownership

Prioritize observable correctness: state transitions, edge cases, contracts, side effects, error handling, resource lifetime, async boundaries, and concurrency. Trace a plausible failing path before reporting a defect.

For each substantial function or class, assess who owns the data, invariant, and operation:

- Put behavior that maintains an object's own state or invariants on that domain object when it has the information needed to act. Prefer meaningful operations over external code that repeatedly inspects and mutates another object's internals.
- Keep scheduling, transport, persistence, presentation, and orchestration separate from domain rules according to AGENTS.md. A scheduler should decide when to invoke behavior; a domain model should decide the rules governing its state. Operations requiring several aggregates, registries, or external services may belong in a domain service or handler rather than a single entity.
- Check encapsulation, cohesion, coupling, and dependency direction. Look for classes with unrelated reasons to change, duplicated business rules, long parameter lists, mutable shared state, and dependencies that make behavior difficult to test.
- Apply SOLID principles through concrete consequences: focused responsibilities; extension points supported by actual variation; substitutable subclasses; narrow client-facing interfaces; and explicit dependencies on capabilities rather than unnecessary concrete infrastructure. A SOLID label alone is not a finding.
- Prefer composition when behavior varies independently. Preserve inheritance that represents a real substitutable relationship. Python dataclasses, functions, protocols, and simple modules are valid designs; do not require every function to become a method or every interface to become an abstract base class.
- Check that moving a method would reduce knowledge and coupling, not merely relocate the same oversized logic. Models should not acquire the injector, network clients, or broad registry access just to absorb an orchestration function.
- Preserve designer-editable or declarative behavior when the repository requires it. Do not recommend replacing content with hard-coded branches as an architectural cleanup.

## Review DRY and duplicated knowledge

Apply DRY (Don't Repeat Yourself) to repeated knowledge: business rules, validation, conversions, defaults, and workflows that must change together. Check nearby implementations and existing shared capabilities before recommending new abstractions.

- Identify the duplicated locations and explain the concrete risk: inconsistent behavior, a fix that must be repeated, or drift between implementations. Similar syntax alone is not sufficient evidence; code serving independent concepts may reasonably remain separate.
- Prefer one authoritative owner for a shared rule, placed at the appropriate domain or architectural boundary. Reuse an existing method, function, or declarative definition when it fits. Preserve designer-editable data and avoid introducing cross-layer dependencies merely to remove repetition.
- Recommend extraction only when the shared concept is clear and the result simplifies its callers. Weigh reduced duplication against indirection, parameter flags, conditionals, and coupling; avoid premature generalization or combining behavior that changes for different reasons.
- Avoid pass-through wrappers that only delegate to another callable without adding meaningful behavior or a required contract. Prefer explicit calls to the underlying function. Renaming the callee or prebinding a fixed option alone does not justify another layer when the direct call is equally clear; do not introduce these wrappers during extraction or retain unused wrappers as speculative compatibility shims.
- Before recommending wrapper removal, inspect callers and contracts. Preserve wrappers that enforce validation, invariants, authorization, resource lifetime, synchronization, error translation, or a demonstrated API/protocol compatibility boundary. Cite the actual value added; naming, an extra stack frame, or a possible future extension is insufficient. Treat unnecessary indirection as a maintainability recommendation unless a concrete behavioral defect is demonstrated, and do not claim a measured performance gain without evidence.
- Report duplication as a correctness defect only when a concrete failing path is demonstrated. Otherwise present it as a nonblocking maintainability recommendation, citing the affected locations, the smallest useful consolidation, and behavior and regression coverage to preserve.

## Evaluate design patterns selectively

Recommend a pattern only when the reviewed code demonstrates the problem it solves. Prefer an existing abstraction or a small function over a new framework when either is sufficient.

Useful candidates include Strategy for independently varying algorithms, State for complex state-dependent transitions, Adapter for an external contract mismatch, Factory for genuinely complex construction, and Command for operations that need a common execution contract. These are examples, not a checklist to satisfy.

For each recommendation:

1. Identify the concrete source of complexity, duplication, or coupling and cite the code.
2. Explain why the current structure is difficult to change or understand.
3. Name the proposed pattern or simpler alternative, identify the participating existing classes, and describe the responsibility or dependency change.
4. State the benefit and the added cost, including new indirection, configuration, or migration work. Prefer the smallest change justified by present requirements.
5. Identify the behavior that must stay compatible and the regression coverage needed before refactoring.

Do not recommend speculative extension points, new inheritance trees, repositories, event buses, or singletons merely to use a named pattern. Say that no additional pattern is warranted when the existing structure is clearer.

## Verify and report

- Run focused existing checks when feasible and appropriate to the review. Use repository-prescribed tools. Do not edit code, fixtures, snapshots, or configuration during a review unless implementation changes are also requested.
- Distinguish observed test failures from suspected causes. Do not call a failure pre-existing without baseline evidence, and do not claim a performance improvement without measurement. Identify missing coverage without inventing successful validation.
- Lead with actionable correctness findings, ordered by severity. Include the precise file and line, triggering conditions, impact, and a focused remedy. For change reviews, distinguish introduced regressions from existing issues and keep existing issues clearly labeled.
- Present nonblocking object-design and pattern recommendations separately from correctness defects. Explain tradeoffs and scope; avoid assigning high severity solely because a design differs from an idealized pattern.
- Finish with verification performed and material limitations or open assumptions. If no actionable defects are found, state that plainly; do not manufacture findings or pattern recommendations.

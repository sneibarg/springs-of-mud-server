---
name: object-oriented-design-review
description: Review object-oriented design across languages, including responsibility placement, encapsulation, contracts, dependency direction, and justified use of design patterns. Use for requested object-design reviews or design-focused refactoring; distinguish behavioral defects from maintainability recommendations.
---

# Object-Oriented Design Review

Produce an evidence-based assessment of the requested code and recommend the smallest changes that improve its design. Interpret best practices through the project's constraints and language idioms, rather than imposing a class hierarchy or pattern catalog.

## Establish scope and design intent

Read applicable repository instructions and identify the target: named classes, a subsystem, working changes, or a revision comparison. Trace representative callers, collaborators, construction paths, and tests before deciding where responsibilities belong. Distinguish changes introduced by the review target from existing design issues.

Identify the important state, invariants, ownership boundaries, supported variations, and external contracts. Respect intentional architectural choices, including declarative content and procedural or functional components. If the available evidence does not establish a design requirement, label the assumption instead of inventing a future requirement.

A review request authorizes findings and recommendations. Implement only when the user also requests changes; keep authorized changes within the requested scope.

## Assess responsibilities and boundaries

Use these lenses where relevant, following the consequences through real call paths:

- **Ownership and invariants:** Prefer operations on the object that owns the state and can enforce its rules. Look for repeated external mutation, invalid intermediate states, ambiguous ownership, and getters that expose mutable internals. Do not move orchestration into an entity if that would require broad registry, transport, or persistence access.
- **Cohesion and coupling:** Identify unrelated reasons to change, duplicated domain rules, knowledge of collaborator internals, dependency cycles, and excessive coordination. Class length or method count alone does not prove a design problem. Prefer extracting a coherent responsibility over redistributing the same dependencies across more classes.
- **Contracts and substitutability:** Check whether implementations preserve caller expectations about valid inputs, results, exceptions, side effects, mutability, and lifecycle. A subclass that rejects ordinary base-class operations or weakens guarantees needs a concrete failing caller example. Distinguish inheritance used for shared implementation from a genuine substitutable relationship.
- **Dependencies and interfaces:** Keep infrastructure concerns outside domain policy according to the repository architecture. Favor explicit dependencies and interfaces shaped by actual clients. Flag global mutable dependencies or service locators when they obscure ownership, lifetime, or testing; do not require an interface or dependency-injection framework for every class.
- **Construction and lifecycle:** Check that construction establishes a valid object, resource ownership is clear, and cleanup is reliable. Consider identity versus value equality, mutable hash keys, aliasing, shared defaults, and asynchronous or concurrent access when those affect the reviewed behavior.
- **Extension and reuse:** Prefer composition for independently varying behavior, and preserve inheritance when its contract is useful. Introduce extension points for demonstrated variation. Shared code should express a stable responsibility, not merely combine similar-looking operations with many flags or callbacks.

Apply SOLID, information hiding, and other principles as reasoning tools. Explain the observed dependency, invariant, or change cost; a principle's name alone is not a finding. Simple functions, modules, data records, and existing frameworks may already be the right abstraction.

## Recommend proportionate changes

For each material recommendation, identify the current owner, the proposed owner or collaborator, and the responsibility or dependency that changes. Explain why this reduces coupling or protects an invariant instead of simply moving code.

Recommend a design pattern only when an observed problem warrants its indirection. Describe its participating existing types, the simpler alternative considered, and the added configuration, migration, or testing cost. Reuse established project abstractions before proposing a new framework. Avoid speculative generalization and broad rewrites justified only by stylistic preference.

When implementation is authorized, preserve observable behavior and public contracts unless the user requests a behavior change. Make the affected state transitions and contracts testable with focused regression checks, using the repository's normal tools. Do not replace designer-editable policy with hard-coded source behavior as an architectural cleanup.

## Report evidence and practical impact

Lead with actionable behavioral or contract defects, ordered by impact. Cite precise files and lines, a triggering scenario or caller, the consequence, and a focused remedy. Present nonblocking design improvements separately, with their tradeoffs and an incremental implementation path.

State which principles or local conventions support a recommendation without treating optional conventions as universal requirements. Distinguish verified behavior, architectural inference, and uncertainty. Report checks actually run and their limitations; call a failure pre-existing only with baseline evidence. Say when no actionable issues or additional patterns are warranted.

# Shared AI Skills

Use [`align-repository`](../../.codex/skills/align-repository/SKILL.md) to align this
Python runtime with changes in `som-server-modulith` and
`springs-of-mud-designer`. It reviews API and content contract changes and files proposed alignment
changes in `docs/alignment` without updating runtime code or data, preserving
the designer-driven workflow.

For ROM24 execution-path reports and language-neutral pseudo test suites, use
[`rom24-code-path-report`](../../.codex/skills/rom24-code-path-report/SKILL.md) and its
linked report-format reference. It supports selected C files/functions or the
whole reference tree. This is distinct from `rom24-parity`, which compares
implementations and investigates parity fixes.

Matching skill instructions are available in `.codex/skills`, `.claude/skills`
and `.grok/skills`. AI tools without native skill discovery can read the linked
Markdown files directly and follow the same workflow. Keep these copies in sync.

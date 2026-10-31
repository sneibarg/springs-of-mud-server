# Repository ROM24 parity review — 2026-10-30, current working tree

**All three findings resolved.** News editing now requires MAX_LEVEL minus 7 trust and changes editing requires MAX_LEVEL minus 1. Reading, listing, catchup and existing removal rules remain available before that editing boundary. Composition actions attach a draft automatically and preserve a draft belonging to another board. Explicit `read next` (including ROM prefix selectors) and `read all` use visibility-filtered notes and existing read-state tracking; `all` reads the first visible note, matching this C checkout.

Five regression tests cover editing actions below the trust threshold, posting at the threshold, mortal read access, automatic attachment, cross-board protection and read selection. All 14 note tests pass. Across four isolated suites, **59 of 60 tests pass**; the sole command-authorization `IM` subtest failure exactly matches the earlier social-remediation baseline. Command execution and input/persistence suites pass. `git diff --check` passes. [Remediation results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/notes-remediation-2026-10-30-tests.json). No content changes or deployment were needed. Original review follows for history.

Review only: no runtime, collection, test, or reference-C changes. Existing working-tree changes were treated as the implementation under review. Earlier resolved reports were not reused as current defects.

## Findings

### P2 — Ordinary players can publish news and changes

Python [NoteHandler.py:44](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:44) routes every board through the same editing actions, and [NoteHandler.py:223](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:223) persists posts without a board-specific trust check. The bundled `news` and `changes` commands both have level 0, player role, and no guards. Their command lambdas call PlayerHandler.do_note_command, which delegates directly to this handler. General CommandAccess checks therefore do not supply the missing restriction.

ROM [note.c:767](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:767) permits reading before enforcing ANGEL trust for editing news and CREATOR trust for editing changes; these are MAX_LEVEL minus 7 and minus 1 respectively ([merc.h:146](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:146)).

Reproduction: a trust-1 mortal executes `news write`, `news to all`, `news subject Forged bulletin`, `news + Body`, `news post`. The production handler calls the in-memory service's create method once. The equivalent `changes` sequence also creates a post. ROM rejects the editing actions at that trust. This lets ordinary players author the administrative bulletin boards. Add the board-specific editing boundary while preserving public reading.

### P2 — Standard ROM note composition cannot start a draft

Python [NoteHandler.py:249](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:249) rejects a missing draft. `to`, `subject`, and `+` all reach that check; only the added `write` action creates one.

ROM calls `note_attach` automatically for `+` ([note.c:777](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:777)), `subject` ([note.c:849](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:849)), and `to` ([note.c:865](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:865)). Thus a player with no draft can begin with `note to Bob`, `note subject Greetings`, or `note + First line`.

Production-handler probe: a fresh player's `note to Bob` returns `You have no note in progress.` with `blocked=true`, leaving no draft. Existing tests cover only the added write-first flow. Restore automatic attachment for these composition actions, retaining the different-board draft check. No documented intentional change to this workflow was found; this is a verified compatibility discrepancy whose product intent remains unconfirmed.

### P3 — Explicit next-unread note selectors are rejected

Python [NoteHandler.py:107](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/notes/NoteHandler.py:107) accepts an empty selector or digits, rejecting `next` and `all` before lookup. ROM [note.c:583](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/note.c:583) explicitly accepts both. In this specific C checkout, `read all` returns the first visible note because the matching loop returns after one result; parity does not mean inventing a bulk-read behavior.

Probe with a visible unread note: `note read next` and `note read all` each return `Read which number?`. ROM reads the next unread note for `next`, and the first visible note for `all`, updating the read watermark. Support these selectors through the existing visibility and read-state paths. No documented intentional removal was found; product intent remains unconfirmed.

## Other discrepancies requiring intent or service-contract confirmation

- Python numbers notes from 1; this ROM checkout numbers them from 0. Current Python tests explicitly assert the one-based presentation, so this review does not classify it as an accidental defect.
- `_can_read` treats an empty recipient list as public, whereas ROM's `is_note_to` does not. The normal posting path rejects empty recipients; exposure depends on imported or service-authored records, which were not examined live.
- The note handler does not implement ROM clan-name recipients. Python's guild/clan mapping and intended service contract need establishing before recommending a fix.

## Scope and evidence

Repository inventory plus sampled source comparisons covered command execution/access and note delegation; movement and automatic escape; combat death, defenses and rewards; spell effect application/retaliation and periodic effects; item expiration/ownership and container use; NPC pulses and area resets; weather, regeneration, learning and advancement. Reference reads included note.c, update.c and merc.h. This was a repository-wide sampling pass, not a line-by-line review of every C function, every Python command, or every content document. Findings concentrated in the less-covered note subsystem; absence of other findings is not a parity certification.

Collection-query was used to inventory snapshots and inspect note/news/changes command metadata and lambdas. Probes used production NoteHandler methods, bundled command documents and existing test doubles; they performed no network writes. Expected behavior was derived by tracing the local C source, not by executing a C server.

Validation: **20 suites, 322 tests, 308 passes, 3 failures and 11 errors**. Eighteen suites pass completely. `test_combat_group_rewards` has 11 fixture errors for missing `character_attributes.points`; `test_spell_affect_payload_messages` has the same three energy-drain failures recorded in social-remediation-2026-10-30-tests.json. They are disclosed as existing validation gaps, not new gameplay findings. Tests ran in separate processes because their module stubs interfere when combined. The spell suite required PYTHONPATH=src. Local asyncio socket creation required execution outside the filesystem sandbox; initial sandbox hangs were not counted as gameplay failures.

Machine-readable results: [notes-validation.json](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-30-notes-validation.json).

No live server/content-service validation, exhaustive random-state coverage, or executable-C differential testing was performed. Full repository discovery was not rerun.

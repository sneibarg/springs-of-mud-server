# healer.c ROM24 parity review

Reviewed October 25, 2026 using the repository `rom24-parity` skill and `AGENTS.md`. Reference: local `C:/Users/scott/PycharmProjects/PyRom/Rom24/src/healer.c`. Python scope: the `heal` command, healer selection, service resolution/payment, spell invocation, associated collection definitions, and outgoing payload routing.

**Four behavioral discrepancies were verified.** No documented intentional healer-specific exemption was found. Treat the currency representation difference in particular as requiring a product/parity decision before changing shared money helpers. This review changes only this report, not source, content, tests, or the C reference checkout.

## Implementation follow-up — October 25, 2026

**H1–H4 and the smaller presentation differences are addressed in the working tree.** The original findings below are retained as review evidence.

| Finding | Implemented behavior |
| --- | --- |
| H1 | Successful purchases assign the configured `PULSE_VIOLENCE` to real status flags, retaining any longer existing wait. No shared wait-helper behavior was changed. |
| H2 | Selection uses one-way abbreviations in ROM branch order, so `m` means mana and suffixes such as `manafoo` are rejected before payment or lag. |
| H3 | The incantation includes the buyer, excludes the healer and observers below resting position, and uses existing recipient-specific text rendering for visible versus unseen healer names. Listings and refusals use the selected healer's visible identity. |
| H4 | Healer purchases spend silver first and break only the gold needed for a shortfall; healer credits preserve existing silver. Shared shop money helpers remain unchanged. |

The service list, refusal messages, mana response, and incantation now render from the `heal` command payload. The list preserves ROM's tab alignment, message capitalization, hint wording, and its existing 15-gold serious listing/16-gold charge. Standard server CRLF message framing is retained. Missing spell content no longer invents a restoration message after charging; the configured-service path still delegates to authored spell operations.

**Verification:** added `tests/test_healer_parity.py`, with **9 passing real-model tests** covering all service prefixes and prices, malformed input, pending-input lag, configurable lag and longer waits, rejection side effects, denomination preservation, recipient visibility/position, listings, missing content, real restoration formulas/caps, and real authored condition dispels. Updated the existing object suite's healer expectations and enum fixture: **55 tests pass**. The repository pass ran **87 top-level modules independently: 80 passed and the same seven modules failed** as in the preceding verification (1,068 executions in that pass). The final ninth healer test was added afterward and the full healer suite reran successfully. All **337 Python source/test files** parsed in that pass; `git diff --check` passes.

Collection changes were dry-run and validated through the collection-modify tool. Windows denied atomic replacement of the open Commands snapshot, so the same tool-generated output was applied in place after asserting that the sole additional document change was the `heal` payload. Collection-query verified the resulting fields. Earlier unrelated working changes, including the quit payload, were preserved.

**Deployment dependency:** load the updated `heal` command payload from `SOMDB.Commands.json` into the content service alongside this runtime change. The new list/response fields and observer tokens require that content update. No live service data, deployment, C source, or server process was changed. The seven known failing modules remain unresolved; exhaustive downstream spell parity and switched-client edge cases remain outside these fixes.

**Utterance compatibility follow-up:** the healer renderer also expands legacy ROM `$n`/`$N` identity and `$T` utterance tokens, supporting older live incantation payloads alongside the new brace tokens. Identity substitution remains recipient-specific. A regression uses the original `$n utters the words '$T'.` payload and verifies exact visible/unseen recipient output with no literal markers. All **10 healer tests and 55 object-command tests pass**; `git diff --check` passes. No live server process was restarted.

**Missing-list compatibility follow-up:** older live command data lacks the newly added `services` and `warmGlow` messages. Returning an empty string for those missing keys caused bare `heal` to produce no list. Missing healer message keys now fall back to the bundled `heal` payload in `resources/collections/SOMDB.Commands.json`, loaded once on demand and cached. Live keys always take precedence, including designer customizations. No text is duplicated into Python. Older live content therefore no longer needs a content update merely to restore the list or mana response; loading the updated content remains appropriate for the other new message templates. Two regressions cover an older payload with both keys removed and a live custom list that must override the bundled default. All **12 healer tests and 55 object-command tests pass**. The server process must load the updated Python code; no live restart was performed.

## Original findings (resolved)

### H1 — [P2] Healer purchases apply no command lag

**C:** [healer.c:177](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/healer.c:177), [merc.h:1836](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1836), [merc.h:138](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:138).

**Python:** [Object.py:180](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Object.py:180), [CharacterApi.py:187](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/CharacterApi.py:187).

ROM assigns `wait = max(wait, PULSE_VIOLENCE)` after the funds check and before payment. This checkout defines four pulses per second and twelve pulses per violence round: normally three seconds of purchase lag. Python calls `CharacterApi.wait_state(character, 24)` but discards its result. That helper returns the maximum without assigning `status_flags.pulse_wait`. The healer invokes spell lambdas directly, bypassing ordinary cast preparation, so that path does not supply the missing buyer lag.

**Verified:** purchases of light, serious, critical, heal, refresh, and mana on a real Character all left `pulse_wait=0`. Existing healer coverage passes because its CharacterApi double mutates a synthetic `character.wait` and expects 24; it does not exercise the real helper's contract. Merely assigning the current hard-coded result would still produce twice ROM's configured lag.

**Consequence/remedy:** customers can immediately issue another action after buying treatment. Assign the wait through the runtime's state contract using the configured `PULSE_VIOLENCE`, preserving any longer existing wait. Test real status flags, pending input, and rejected purchases without modifying unrelated callers of the shared helper by assumption.

### H2 — [P2] Service resolution changes `heal m` and accepts invalid suffixes

**C:** [healer.c:82](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/healer.c:82), [healer.c:146](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/healer.c:146), [db.c:3164](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3164).

**Python:** [Object.py:2618](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Object.py:2618), [Object.py:2623](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Object.py:2623).

ROM checks the mana/energize branch before refresh/moves and accepts only an input that is a prefix of a supported service name. Python puts refresh/moves first and permits either direction of prefix matching.

**Verified:** Python resolves `m` to refresh (500 silver, movement restoration), while ROM resolves it to mana (1,000 silver, mana restoration). Python also resolves `manafoo` to mana, `lightning` to cure light, and `criticalextra` to cure critical; ROM rejects those strings with the service-list hint and no payment or lag. Full aliases such as `moves`, and ordinary abbreviations such as `ma`, otherwise work.

**Consequence/remedy:** abbreviated input can buy a different resource, while malformed input can charge for an unintended purchase. Preserve the C branch precedence and one-way abbreviation matching. Designer-authored service metadata is compatible with this behavior; matching C does not require retaining a hard-coded Python table.

### H3 — [P2] The customer misses the healer's incantation; room rendering lacks ROM's observer rules

**C:** [healer.c:182](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/healer.c:182), [comm.c:2475](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475), [comm.c:2482](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2482), [comm.c:2512](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2512).

**Python:** [Object.py:182](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Object.py:182), [Room.py:200](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/Room.py:200), [PlayerHandler.py:641](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:641).

ROM calls `act` with the healer as actor and `TO_ROOM`, excluding the healer and including the customer. Python builds its target list with `room.player_targets(character)`, where `character` is the customer, so it excludes that customer. With no bystanders, nobody receives the incantation at all. Spell restoration text still reaches the customer through the separate victim payload.

**Verified:** with a customer and one observer, the returned incantation target list contained only the observer. The payload emitter uses that list without adding the customer.

The same raw string exposes the healer's `short_description` identically to every observer, and the target helper does not filter sleeping characters. ROM's `act` uses its resting-position threshold and `PERS` visibility substitution. These are additional observable differences in this announcement path, established by tracing the two routing implementations; they were not tested against live clients.

**Focused remedy:** render the authored incantation from the healer's perspective with observer-aware identity, include the customer, and honor the relevant recipient-position rules. Keep messages in the command payload rather than adding more literal strings. Cover a lone buyer, a bystander, a sleeping observer, and an unseen healer.

### H4 — [P2] Buying treatment also exchanges existing silver into gold

**C:** [healer.c:179](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/healer.c:179), [handler.c:2219](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2219).

**Python:** [Object.py:2674](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Object.py:2674), [Object.py:2681](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Object.py:2681).

ROM spends the customer's silver first, breaking only enough gold to cover any shortfall. It credits the healer with `cost / 100` gold and `cost % 100` silver without exchanging the healer's existing balance. Python subtracts/adds a total silver-equivalent value and normalizes the entire remainder into gold and fewer than 100 silver.

**Verified example:** a buyer with 0 gold/2,100 silver purchases mana for 1,000 silver from a healer holding 0 gold/150 silver. ROM leaves the buyer at **0 gold/1,100 silver** and the healer at **10 gold/150 silver**. Python leaves them at **11 gold/0 silver** and **11 gold/50 silver**, respectively. Total value is conserved, but coin counts differ. Denominations are gameplay-visible and have different weight contributions under ROM's carry-weight macro and the Python currency-weight calculation.

**Decision/remedy:** this is a confirmed parity discrepancy, with intent unconfirmed. If free automatic currency exchange is an intentional economy rule, document that exemption. Otherwise preserve ROM's silver-first deduction and direct denomination credit at this boundary, assessing the other users of the shared helpers before changing them globally. Include existing-silver and gold-shortfall cases in coverage.

## Behavior that matched, and smaller presentation differences

- Both command tables require at least resting position and level zero. Both implementations find a flagged healer before resolving a service and treat the first argument as the service selector. Neither healer dispatcher requires visibility of the healer or a learned spell, spends healer mana, or runs the ordinary player casting checks.
- The service prices match: light 1,000; serious 1,600; critical 2,500; heal 5,000; blindness 2,000; disease 1,500; poison 2,500; uncurse 5,000; mana 1,000; refresh 500, all in silver-equivalent units. The **15-gold serious listing versus 16-gold actual charge exists in both implementations** and is not a Python parity defect.
- The service incantation words match. `critic` and `blind` already qualify as abbreviations in C, so Python's explicit aliases do not establish extra behavior by themselves. The curse, energize, and moves aliases are present in both.
- The inspected restoration definitions match ROM's formulas for ordinary positive healer levels: light `1d8 + level/3`; serious `2d8 + level/2`; critical `3d8 + level - 6`; heal +100 hit points; refresh +level movement; mana `2d8 + level/3`. Resource caps and use of the healer's level match in the examined paths. For level 30 and every die returning 4, actual Python purchases changed initial hit 10 to 24/33/46/110, movement 10 to 40, and mana 0 to 18, as expected.
- The blindness, disease, poison, and uncurse services delegate to the corresponding authored spell operations. Static tracing checked their dispel/owned-item entry paths and payloads, but this review does not certify exhaustive parity of those shared spells, every resistance roll, or all cursed-item ordering.
- Python's refusal payloads use the fixed label `The healer`, while C formats the selected NPC through `act`. The list and announcement strings also differ in capitalization/alignment and newline representation. These smaller presentation differences are recorded without inventing additional high-priority findings.
- If spell content is absent, Python emits `You feel momentarily better.` after charging; C has direct compiled function pointers and returns after payment if skill lookup yields -1. Content-removal/configuration failure behavior has no exact equivalent in this reference and is not counted as a normal configured-service defect.

## Regression attribution, validation, and limits

The healer dispatcher and service/money helpers have no working-tree changes relative to the current Python HEAD. The relevant wait helper also was not changed by the recent hit-roll/flag additions in CharacterApi. These findings concern existing healer behavior; no finding here is attributed to the recent quit, item-tick, note, or login fixes.

Ran `tests.test_object_get_dynamic_commands` in an isolated interpreter: **55 tests pass**, including four existing healer tests. Their synthetic CharacterApi/SpellApi collaborators limit parity coverage, as illustrated by H1. Additional read-only runtime probes used real Character state, command guards, room targets, the real wait helper, authored restoration spell lambdas, and SpellApi, with controlled random rolls and a position-update collaborator. No C executable or live client/server session was run.

Collection inspection used the prescribed `collection-query` CLI and loader. The review traced local C helpers/macros and Python dispatch, payment, spell context, payload emission, and existing tests. Multiple-healer selection order, switched/NPC client edge cases, abnormal negative levels/resources, and exhaustive downstream spell parity were not dynamically compared. No collection edits, source/test changes, live service calls, deployment, or broad repository test rerun were performed. The separate repository-wide review's known failing modules remain outside this focused verification.

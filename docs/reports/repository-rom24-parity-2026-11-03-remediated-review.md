# ROM24 parity review of the remediated working tree

November 3, 2026. Reviewed the working tree based on `40949b8`, including both sets of visibility, inspection and combat message fixes, against the local ROM24 C checkout.

## Findings

| Priority | Trigger and consequence | Reference and runtime evidence |
| --- | --- | --- |
| P2 | An item with an expiration timer is invisible to a room observer, or the observer is asleep. ROM24 renders the object placeholder using each recipient's object visibility and skips recipients below resting. Springs substitutes the actual item description once and sends it to all room players. An invisible item can disclose its identity when it decays. A sleeping player can also receive the notice. | [ROM24 update.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:930), [ROM24 comm.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475), [ROM24 object placeholder](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2522), [ItemUpdateHandler.py](../../src/item/ItemUpdateHandler.py#L114), [Item.py](../../src/item/Item.py#L138) |
| P2 | An invisible clan member sends a clan message and another member lacks detection. ROM24 expands the sender placeholder per recipient, including for clan messages, and displays a generic identity when visibility fails. Springs uses a single literal sender name for every clan recipient. | [ROM24 act_comm.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:687), [ROM24 comm.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2512), [Communications.py](../../src/interp/commands/Communications.py#L208) |
| P2 | A switched immortal receives a shout in an eligible area and the original player and controlled NPC differ on QUIET or SHOUTSOFF. ROM24 checks the original player's flags and delivers to the body. Springs checks the body for both flags. The recent global-channel fix covers a different helper. The prior review explicitly retained the authored shout scope, so this finding concerns eligible recipients within that scope. | [ROM24 act_comm.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:794), [Communications.py](../../src/interp/commands/Communications.py#L357), [Prior audience review](repository-rom24-parity-2026-10-30-audience-review.md) |
| P3 | A player enters bare `shout`. ROM24 toggles their incoming-shout preference before checking whether they may send a shout. The bundled command instead returns an argument prompt and never toggles the flag. The public-interpreter fixture reproduced `Shout what?` with the current command document. | [ROM24 act_comm.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_comm.c:762), [Communications.py](../../src/interp/commands/Communications.py#L357), [Commands collection](../../resources/collections/SOMDB.Commands.json) |

The first three findings are source-confirmed. Their live delivery paths were not executed in this pass.

## Unresolved behavior

Springs blocks a QUIET sender from using clan chat. The C clan path checks NOCHANNELS on the sender and QUIET on recipients. This could be an authored policy choice. Its intent remains unverified. Likewise, the existing command-prefix, idle/limbo, pose eligibility, and offline recovery questions remain open.

## Validation and coverage

- Re-ran 65 focused tests for the previous findings, room inspection fixtures, and periodic status fixtures. All passed.
- Used the immediately preceding isolated run on this implementation as the full regression snapshot. It ran 136 modules and 1,656 tests, with 124 passing modules and the same 12 failing module names reported before the most recent fixes. The earlier November 3 report describes the intermediate revision and has different totals.
- Traced the energy-drain failures into the authored experience step. The targeted probe logged an exception because the test victim's SimpleNamespace lacks `points`. The production CharacterAttributes model declares that field. This explains why the fixture stops before damage, and the three failing assertions alone do not establish a production spell defect.
- Used the [repository coverage matrix](repository-rom24-parity-2026-10-31-third-review.md#repository-coverage) as historical source coverage across the C translation units. Fresh source tracing sampled communications, item expiration, combat round construction, flee and travel eligibility, and energy drain and advancement. The recent full suite provides broader evidence across movement, objects and shops, spells and skills, NPCs and resets, notes, administration, weather, sessions and persistence, subject to its reported failures.
- No complete fresh branch-by-branch comparison, record-level world audit, executable C differential run, or live service run was completed.

Only the review report was added in this pass.

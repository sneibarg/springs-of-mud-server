# ROM24 parity review after travel and clan-note fixes

November 3, 2026. Reviewed the current Springs working tree based on `40949b8` against the local ROM24 C checkout.

## Findings

| Priority | Trigger and result | Evidence |
| --- | --- | --- |
| P2 | **Wound and death notices reveal victims to ineligible observers.** A combatant is invisible when they become stunned, incapacitated, mortally wounded, or dead. ROM24 resolves the victim separately for each room observer and skips recipients below resting. Springs uses one literal name and the room's unfiltered player list. The same helper builds local and adjacent death-cry notices. A probe with a real invisible actor and sleeping witness confirmed the literal name and selected audience at the payload boundary. Ordinary attack lines use a separate, already repaired path. | [ROM24 fight.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:815), [death cry](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:1596), [ROM24 comm.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475), [CombatDeathHandler.py](../../src/combat/CombatDeathHandler.py#L31) |
| P3 | **Consider consumes trailing words as part of its target.** For `consider guard trailing` with one visible target named `guard`, ROM24 selects `guard` with `one_argument`. Springs hands the entire argument to the visible-target matcher, which requires each supplied word to match. The lookup probe found the target with the first word and returned no match with the entire selector. Keep ROM's quoted-selector behavior when changing this command's argument handling. | [ROM24 act_info.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2328), [Info.py](../../src/interp/commands/Info.py#L456), [LookupUtil.py](../../src/util/LookupUtil.py#L16) |
| P3 | **Consider prints NPC keywords in difficulty messages.** When the selected visible NPC has a keyword list such as `guard watchman` and a short description such as `a city guard`, ROM24 renders the short description via the victim placeholder. Springs uses the raw name field in every branch that names the target. The level thresholds themselves agree. | [ROM24 act_info.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2350), [ROM24 comm.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2512), [Info.py](../../src/interp/commands/Info.py#L472) |
| P3 | **Deleting the last description line also deletes earlier blank lines.** A three-line description containing a blank middle line should retain that blank line after `description -`. ROM24 truncates at the prior line delimiter. Springs filters every blank line before removing the last line. The actual Python handler changed `First line.\r\n\r\nLast line.\r\n` into `First line.\r\n`. | [ROM24 act_info.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2422), [Info.py](../../src/interp/commands/Info.py#L510) |

The death notice probe used a minimal text renderer to isolate recipient selection and token substitution. It did not execute a lethal attack or a socket delivery. The NPC display-name finding is source-confirmed.

## Unresolved differences

- **Clock and weather at boot.** ROM24 derives calendar time and initial sunlight from the wall clock and chooses season-dependent pressure before play begins. Springs starts at midnight on a fixed date with daylight and cloudless skies. Restart timing therefore affects outdoor visibility differently. The desired calendar persistence and boot policy are unverified. [ROM24 db.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:256) · [WeatherHandler.py](../../src/game/WeatherHandler.py#L33)
- **Profile tilde handling.** ROM24 replaces tildes with hyphens and truncates titles before applying that substitution. Springs removes tildes and truncates the title afterward. The text difference is established. Whether the service-backed profile contract intentionally sanitizes these characters differently remains unverified. [ROM24 act_info.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2401) · [ROM24 db.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3116) · [Info.py](../../src/interp/commands/Info.py#L502)
- Earlier policy and contract questions remain open for command prefixes, idle and limbo, pose eligibility, offline recovery, and QUIET senders on clan chat.

## Validation and coverage

Ran all 136 top-level unittest modules in isolated processes. The run reported 1,662 tests, with 124 modules passing, 12 previously failing modules, and no timeouts. The recent travel visibility, LAW follower, clan-note, decay, and communication regression modules passed. The historical failure set includes test-double and import problems as well as assertions that warrant separate diagnosis.

This pass freshly traced combat aftermath, target lookup and consider, profile editing, boot weather and calendar, and the previous travel and note fixes. The full isolated suite exercises the broader runtime, including spell and skill execution, objects and shops, mobiles and resets, advancement, command dispatch, administration, sessions, and persistence, subject to the failures above. Broader source coverage is documented in the [historical translation-unit matrix](repository-rom24-parity-2026-10-31-third-review.md#repository-coverage).

The review is repository-wide at the regression-suite level. It did not repeat a complete fresh source audit across every subsystem or compare every content record. No compiled C server or live service was exercised. Only this report was added in this pass.

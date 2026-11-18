# ROM24 parity review of the wimpy setting

This review follows `wimpy` from command input through threshold storage, confirmation, and the decision to attempt automatic flee after damage. Earlier combat reviews traced escape selection and movement. This review focuses on the setting that feeds the player escape branch. The success or failure of the ensuing flee command is outside scope. [Earlier combat review](archive/fight-c-rom24-parity-2026-10-18.md)

## Confirmed defect

### Setting zero produces a confirmation with no number

`wimpy 0` disables automatic flee in both implementations. ROM24 confirms “Wimpy set to 0 hit points.” Springs stores zero and sends “Wimpy set to  hit points.” The bundled template uses `%d`, and the legacy token renderer substitutes an empty string for a falsey value. The public-command probe reproduced the message and verified that the stored zero prevented a flee attempt. The `score` command reads the stored integer directly and avoids that token path. [ROM24 assignment and confirmation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2654) · [Bundled template](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:3820) · [Springs assignment and score](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:250) · [Legacy token rendering](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/GamePayload.py:46)

## Verified differences with unresolved intent

### Argument parsing changes the resulting flee threshold

ROM24 extracts the first token with `one_argument`, including quoted tokens, then uses `atoi`. Springs checks the whole argument with `lstrip("-").isdigit()` and separately converts it with a zero fallback. The table uses a maximum of 103 HP and an already configured threshold. [ROM24 parser](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2635) · [ROM24 token parser](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:714) · [Springs parser](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:236) · [Bundled guards](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:3820)

| Input | Starting threshold | ROM24 | Springs |
| --- | ---: | --- | --- |
| `wimpy +20`, `wimpy 20 trailing`, `wimpy "20"`, or `wimpy 20hp` | 10 | Sets 20 | Rejects and retains 10 |
| `wimpy abc` | 20 | Sets 0 | Rejects and retains 20 |
| `wimpy --20` | 20 | Sets 0 | Sets 0 |

At 18 HP after a qualifying hit, ROM24 attempts flee in the first row and Springs does not. In the second row, the result reverses. The probe passed the threshold set by the actual Springs interpreter into the production post-damage selector, with a connected player, no wait, and a stub for executing the selected action. In the third row, Springs accepts the repeated minus because the digit check removes both signs before conversion. The conversion falls back to zero, so reaching the same result as ROM24 depends on two separate parsing steps. [Numeric conversion fallback](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/GenericUtil.py:39) · [ROM24 decision](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:978) · [Springs decision](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/combat/CombatEscapeHandler.py:45)

### A switched player cannot set the mobile's numeric threshold in Springs

With a mobile at 103 maximum HP, `wimpy 12` stores 12 on that body and confirms the setting in ROM24. Springs returns silently before parsing and leaves both bodies' thresholds unchanged. The probe used a switched mobile with a starting threshold of three and an original player with a threshold of 20. Both values survived the Springs command. ROM24's automatic NPC flee branch uses `ACT_WIMPY`, a random roll and an HP ratio, or the separated-charmed-NPC rule. Its numeric setter does not change those NPC escape criteria. [ROM24 command](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2629) · [ROM24 NPC escape](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:967) · [Springs NPC return](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:226)

## Matching paths and validation

Both commands default to one fifth of maximum HP. At 103 maximum HP, the default is 20, the upper bound is 51, and 52 and negative thresholds are rejected without altering the stored value. Both preserve the threshold across their local character serialization paths. For a connected player with a threshold of 20, positive damage from another character triggers an attempt at 20 remaining HP and a wait of five pulses. The probe found no attempt at 21 HP, at the six-pulse boundary, at zero HP, or after zero damage. [ROM24 bounds](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2635) · [ROM24 save](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:241) · [ROM24 load](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:1115) · [ROM24 zero-damage return](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:803) · [Springs serializer](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:132)

Ruff ran read-only against four Python files. Rule counts and concise diagnostics directed source reads to the command, selector and serialization branches. The probes used the bundled command, production interpreter, test connections, and a local serialization round trip. All 47 focused tests passed across four isolated invocations. Two combat suites needed production modules preloaded before their test stubs. ROM24 expectations came from the local C source. Live sockets and external character-service storage were outside the probes.

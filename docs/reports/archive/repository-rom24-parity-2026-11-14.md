# Repository-wide ROM24 parity review

November 14, 2026. Reviewed the Springs of MUD working tree at HEAD `3e2fdc570139d3aa69b7d1e031a4e4fa4eaca8ed`, including pending edits, against the local PyRom ROM24 C source. P1 covers a startup blocker or a broad combat balance error. P2 covers a material gameplay error with a specific trigger.

| Priority | Finding | Consequence |
| --- | --- | --- |
| P1 | F01 · The configured API still sends a command field the runtime rejects | A cold start fails while loading commands. |
| P1 | F02 · Spawned NPCs lose their authored hit roll | 105 bundled prototypes have nonzero hit roll values that the spawn path drops. |
| P2 | F03 · Sleeping and stunned targets retain their dexterity armor adjustment | Ordinary melee attacks can miss targets that ROM would hit in the same posture. |
| P2 | F04 · The combat scheduler drops output for a switched NPC | A controller can take or deal damage without receiving the direct round messages. |
| P2 | F05 · Container resets can restock an older copy elsewhere | A newly reset container can stay empty while a copy moved to another room receives the contents. |

## F01 · Command loading fails against the configured API

**Trigger and evidence.** Start the current Python revision against the configured content service. The command API returned HTTP 200 and 221 records. All 221 contained `function` alongside `lambdas`. The working tree removed the dataclass field, and `Command.from_json` forwards normalized keys to the constructor. All 221 records failed to build with the same unexpected-keyword error. The actual `InterpService.load_commands()` call raised its startup error. With only `function` removed from copies of the same response, the loader published 222 commands, including the generated summary.

**Fix boundary.** Accept the deployed response shape at deserialization while the command service and runtime transition. Test both response shapes through startup and reload. The bundled command snapshot already omits `function`, so the deployed response is needed to reproduce the integration failure reliably. This is a Springs startup regression. ROM dispatches from a built-in command table.

[Python command constructor](../../../src/interp/Command.py#L42) · [Command startup loader](../../../src/interp/InterpService.py#L31) · [Startup failure handling](../../../src/server/FetchAndRegisterMixin.py#L81) · [ROM command table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:64)

**Resolution.** The API was updated to remove `function`, and command fixtures now omit the obsolete field. After the fixture and combat changes, all 1,739 tests across 137 active Python modules passed in isolated processes.

## F02 · Mobile creation loses authored hit roll

**Trigger and evidence.** Spawn a mobile whose document supplies a nonzero `hitroll`, such as the school acolyte at vnum 3700. The fixture read 10 from both the shipped snapshot and the C area. The Python builder stored it as `prototype.hitroll` while `prototype.hit_roll` was zero. Creation copies `hit_roll` only. ROM assigns the prototype value to the mobile's live hit roll. The factory and combat probe held effective skill at 100 and the other accuracy inputs constant. Carrying the authored value into the spawned mobile changed THAC0 from −1 to −11. The collection query found 105 nonzero values among 986 mobile prototypes, including negative values and positives up to 30.

**Fix boundary.** Normalize the authored value into the counter copied at spawn and read by combat. Cover both signs and check that equipment and effects adjust it exactly once. Check the same counter through NPC cloning and paid-pet restoration.

[ROM acolyte prototype](C:/Users/scott/PycharmProjects/PyRom/Rom24/area/school.are:17) · [ROM mobile creation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1566) · [Python prototype fields](../../../src/mobile/MobileFactory.py#L329) · [Spawned hit roll](../../../src/mobile/MobileFactory.py#L154) · [THAC0 calculation](../../../src/combat/CombatHandler.py#L1814)

**Resolution.** Mobile loading now maps the authored `hitroll` to `hit_roll`. An explicit `hitRoll` takes precedence when both keys are provided. The fix applies at spawn. A fresh pet snapshot preserves the effective hit roll and supports removing a restored timed effect exactly once. Older snapshots retain their saved totals. The attempted round trip with equipped gear also exposed a separate snapshot defect. The serializer omits required item fields `areaId` and `extraFlags`, and item restoration raises. [Mobile normalization](../../../src/mobile/MobileFactory.py#L359) · [Hit-roll regression](../../../tests/test_wiz_identity_targeting_parity.py#L467) · [Pet snapshot fields](../../../src/mobile/PetSnapshot.py#L15)

## F03 · Unconscious defenders retain dexterity armor

**Trigger and evidence.** Attack a sleeping or stunned character with a substantial dexterity armor adjustment. ROM's `GET_AC` includes that adjustment only above sleeping, then `one_hit` applies its separate posture modifiers. Python includes the adjustment unconditionally before the posture modifiers. A real character with effective dexterity 23 and raw bash armor 100 yielded scaled armor 1 while standing, sleeping, and stunned. ROM gives scaled armor 10 for the last two cases before posture adjustment. With fixed THAC0 20 and roll 5, the production `one_hit` passed zero damage downstream. The same probe with ROM's zero sleeping dexterity adjustment passed the fixed hit damage of 10.

**Fix boundary.** Apply the awake gate before adding dexterity armor while keeping equipment armor and the later posture modifiers. Exercise an awake target and an asleep or stunned target through the same melee entry point.

[ROM armor macro](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1824) · [ROM attack and posture calculation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:476) · [Python armor calculation](../../../src/combat/CombatHandler.py#L1822) · [Python posture calculation](../../../src/combat/CombatHandler.py#L1078)

**Resolution.** The shared dexterity armor helper applies the adjustment only while the defender is awake, matching ROM's `GET_AC` in both melee and `score`. The regression keeps torso armor equipped and checks standing, resting, sleeping, and stunned defenders through the armor and melee paths. [Shared armor helper](../../../src/combat/ArmorDefense.py#L1) · [Posture regression](../../../tests/test_wiz_identity_targeting_parity.py#L508)

## F04 · Switched NPCs lose direct combat output

**Trigger and evidence.** Switch into a mobile and let a nonlethal round resolve through the world combat emitter. ROM targets the combat participants and sends to eligible recipients with descriptors, which include controlled NPCs. Springs binds the connection to the NPC correctly and generates both direct damage strings. Round building drops an NPC victim, and the scheduled emitter skips an NPC attacker. A real switched session and nonlethal damage-message probe exercised both roles. The player on the other side got the direct line each time. The switched body, with its connection still bound, got neither line.

**Fix boundary.** Use active connection or session ownership for direct delivery and prompt eligibility. Retain ordinary NPC suppression and test both participant roles on the scheduled path. The same round builder also serves standard fight-command payloads, where it can discard an NPC victim before the standard emitter sees it.

[ROM combat messages](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/fight.c:2072) · [ROM descriptor gate](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2475) · [Switched connection binding](../../../src/game/WizHandler.py#L81) · [Python round builder](../../../src/combat/CombatHandler.py#L1287) · [Python round emitter](../../../src/combat/CombatHandler.py#L105)

**Resolution.** Combat rounds use the body's open connection to qualify NPC participants for direct messages and prompts. The scheduler regression covers both roles and returns control to the original player to verify ordinary NPC suppression. A separate regression covers a switched victim in a standard fight-command payload. [Recipient check](../../../src/combat/CombatHandler.py#L145) · [Scheduler regression](../../../tests/test_wiz_identity_targeting_parity.py#L281)

## F05 · Put resets can refill a relocated older container

**Trigger and evidence.** Keep an older copy of a reset container in another room, then let the reset create a replacement at the original location and run its `P` row. ROM prepends each created object to its global list, and `get_obj_type` returns the first matching prototype, so the newly created container wins. Springs selects the first matching instance in room traversal order. A local probe created two copies of the shipped takeable Grove spice jar, vnum 8902, with the older copy in the first scanned room. The production put-reset path returned success and put black powder 8903 into that older jar. The new jar stayed empty. The Grove area and the shipped reset snapshot both contain these jar and powder rows.

**Fix boundary.** Preserve the reference's newest matching instance selection for the put-reset path, including copies that have moved or are carried. Verify which concrete object gets contents and has its lock state restored. Keep the existing occupancy and reset-limit checks.

[ROM Grove reset rows](C:/Users/scott/PycharmProjects/PyRom/Rom24/area/grove.are:920) · [ROM put reset](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1343) · [ROM insertion order](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1961) · [ROM object lookup](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2072) · [Python reset](../../../src/area/AreaHandler.py#L188) · [Python world item search](../../../src/item/ItemOwnership.py#L90)

**Resolution.** Put resets select the newest live matching container by runtime creation order, then apply the location and preceding-reset checks to that instance. Moving an item keeps its order. A saved item receives its order when the runtime loads it. The regressions cover a replacement jar with older copies in another room, and a newer carried jar that receives contents and has its lock state restored only when the preceding reset allows it. All 1,741 tests across 137 active Python modules passed. [Runtime item order](../../../src/item/Item.py#L78) · [Reset regressions](../../../tests/test_world_objects_and_shields.py#L68)

## Prior finding still pending in the configured service

The read-only character API check returned two documents. Both included `pet`. Neither included `groups`, `hitRoll`, `damRoll`, `savingThrow`, `noteReadStamps`, or `noteReadIds`. The previous companion patch remains the remediation for this deployment gap. A populated pet round trip or recovery of missing historical data still requires separate verification. [November 13 resolution](repository-rom24-parity-2026-11-13.md#resolution) · [Companion patch](f01-character-progress-som-server-modulith.patch)

## Coverage and verification

- Inventoried 216 Python source files, 30 C translation units, and 17 collection snapshots. The isolated test sweep ran all 137 top-level Python test modules and reported 1,735 cases. The 92 green modules accounted for 1,047 tests. Each of the 45 red modules encountered the removed `function` field in a fixture. One of those modules also reported an assertion failure. The red suites limit regression coverage for their gameplay paths.
- Fresh source tracing covered bootstrap and command ingestion, combat and damage, advancement and group rewards, movement and portals, direct and area spell paths, equipment and item ownership, shop and theft handling, death and periodic effects, resets, sessions and output routing. Collection queries verified representative authored records. Branch coverage varied by subsystem.
- Verification used read-only GETs, local Python fixtures, and C source traces. Prior questions around idle and limbo, offline recovery, command prefixes, and movement-triggered aggression remain open.

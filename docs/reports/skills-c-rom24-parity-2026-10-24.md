# skills.c ROM24 parity review

Compared the local `C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c` with the current Python working tree, including its uncommitted changes. Review only: no runtime, test, or collection edits.

## Findings

### 1. P1: Gain trainers are invisible to the gain command's eligibility check

Resolved 2026-10-25: `Movement._mobile_act` now reads the runtime `status_flags.act` field. Gain conversion and purchase regressions use this model shape; an additional regression verifies that an obsolete trainer flag cannot override a cleared current flag.

Python: `src/interp/commands/Movement.py:745–754,850–853`; model construction: `src/util/MobileUtil.py:33–37,297`.
C: `skills.c:57–72`.

ROM checks the NPC's current act flags for `ACT_GAIN`. Python `_mobile_act` reads `mobile_flags` or `act`, but current mobile instances hold these flags in `status_flags.act`, with no compatibility property for the obsolete field. Therefore a normally constructed trainer with ACT_GAIN returns zero from this helper and `gain` rejects the location. Reproduced the helper returning zero for a mobile-shaped object whose `status_flags.act` was nonzero. Existing gain tests populate the obsolete `mobile_flags` field and miss the regression.

Use the shared status-flag access path. This blocks normal use of all gain subcommands; findings below describe the independently broken paths after trainer eligibility is satisfied.

### 2. P1: Improvement uses the practice ceiling and can reduce existing proficiency

Resolved 2026-10-25: `LearningService.check_improve` uses 100 for the success probability and both improvement caps. The class adept value remains the practice ceiling. Regressions cover skills and spells at 75, 90, and 99 proficiency, success and failure increments, messages/XP, and the success-probability formula above adept.

Python: `src/skill/LearningService.py:94,105–115`.
C: `skills.c:936–957`.

C allows improvement to 100%, independent of the class practice adept value. Python uses `skill_adept` both in the success probability and as the final cap. For a class with adept 75, a forced successful learning roll leaves learned 75 unchanged; starting at 90 reduces it to 75 without an improvement message or XP. Both success and failure branches can reduce above-adept proficiency. Reproduced 75 -> 75 and 90 -> 75 with the production LearningService and Character model. Use 100 for improvement, preserving adept as the practice-only ceiling.

### 3. P1: Improvement omits eligibility guards, including the zero-rating guard

Resolved 2026-10-25: improvement returns for below-required-level, zero-rating, unlearned/missing, and mastered abilities before attribute-bonus lookup or random rolls. Regressions verify unchanged proficiency, no messages or XP, no random consumption, and eligibility exactly at the required level. Validation: `tests.test_learning_parity` and `tests.test_object_design_contracts` passed together (13 tests); `tests.test_skill_util_melee_resolution` passed separately (6 tests).

Python: `src/skill/LearningService.py:83–100`.
C: `skills.c:913–921`.

C returns for below-required-level, zero-rating, unlearned, and mastered abilities before rolling. Python checks only NPC/definition existence, then divides by rating. Reproduced a rating-zero `ZeroDivisionError`, an unlearned entry improving 0 -> 1, and a level-1 character improving an ability requiring level 40. Learned 100 is also not skipped and can be reduced by finding 2. Restore the guards before probability calculation and random-number consumption. Ability's public improvement facades delegate directly to this service; no equivalent guard exists there.

### 4. P1: Buying a group destroys prior training in its members

Resolved 2026-10-25: group acquisition initializes only missing or zero-proficiency abilities. Existing skill and spell proficiency survives direct, nested, repeated, and overlapping membership. Command regressions verify preserved sword 80 / magic missile 60, initialization of dagger 0 to 1, new spell acquisition, and a single train charge for the purchased root group.

Python: `src/interp/commands/Movement.py:811–815,830–847`.
C: `skills.c:200,981–992,1017–1028`.

C recursively adds members but initializes a skill only when learned is zero. Python `_add_group` unconditionally sets each direct member to 1. Buying a group containing one trained and one missing member therefore spends trains and resets the trained member. Reproduced sword 80 -> 1 through `_add_group`. Group acquisition should preserve every already-learned proficiency.

### 5. P1: Nested groups become fictitious spell entries

Resolved 2026-10-25: `Movement._add_group` resolves registered skills/spells before nested groups and recursively expands members from either content list. A per-acquisition visited set prevents cycles and duplicate traversal. Unknown member names are ignored, as in ROM, rather than becoming learned records. Each expanded group is recorded as owned. Regressions cover nested names in both member lists, a cycle, shared members, unknown names, and repeat acquisition.

Python: `src/interp/commands/Movement.py:811–815`.
C: `skills.c:981–992,1010–1043`.
Content: GameData `groups.mage default` and `groups.combat`.

The real `mage default` definition contains names such as `combat`, `detection`, and `weather` in its spells list. These are nested groups: C resolves members as skills or groups recursively. Python appends each name directly to character.spells, without resolving the referenced group. Reproduced learned spell records named `combat` and `detection`, rather than their constituent spells. A purchase with this shape charges for abilities it never grants. Introduce reusable group expansion with cycle handling while retaining designer-authored membership.

### 6. P2: Gain points charges trains without changing experience requirements

Resolved 2026-10-25: `CharacterAdvancement.experience_per_level` implements the ROM creation-point formula using the character race's class multiplier. After a successful gain-points purchase, `reset_experience_for_points` refreshes the cached leveling cost, clears within-level progress, and resets accumulated XP to the current-level floor. Regression coverage checks formula tier boundaries, multiplier rounding, NPC costs, the 50-to-49 purchase, subsequent leveling at the reduced cost, and unchanged XP/trains/points for rejected purchases. Validation: movement (19), learning/object-design contracts (13), and combat death rules (13), all 45 tests passed.

Python: `src/interp/commands/Movement.py:630–642`; XP consumer: `src/player/CharacterAdvancement.py:62–80`.
C: `skills.c:148–170,625–657`.

C deducts two trains and one creation point, recalculates experience per level, and resets total experience to the current level floor. Python changes trains and points only. The advancement code continues using the unchanged cached `character_attributes.experience_per_level`, so purchasing lower points does not lower leveling cost. For example, at 50 points with a 100% class multiplier, C changes the requirement from 1500 to 1450 after purchase; Python leaves a cached 1500 unchanged. No runtime point-to-XP formula or recalculation was found elsewhere under src.

Python stores both progress-within-level and accumulated XP; preserve that representation when implementing the equivalent current-level-floor reset instead of copying C's storage layout. The separate character creation/content service may calculate initial costs, but this runtime command makes no service call to update them.

### 7. P2: Gain rejects valid ROM abbreviations

Resolved 2026-10-25: gain parses the first token with `InterpUtil.one_argument` for prefix subcommands, while retaining the full argument for multiword content names. Group, skill, and spell lookup accepts case-insensitive prefixes in registry iteration order, including ambiguous prefixes. Regressions cover abbreviated purchases, list/convert/points, suffix rejection, multiword groups, spell lookup, and empty input. Validation at resolution: `tests.test_movement_dynamic_commands`, 17 tests passed. The separate gain-points XP defect was subsequently resolved in item 6.

Python: `src/interp/commands/Movement.py:616,620,630,760–768`.
C: `skills.c:75,132,148,172,207,964–977`; skill lookup: `magic.c` `skill_lookup`.

C accepts prefix subcommands such as `gain con` and `gain po`, and resolves abbreviated skill/group names. Python tests whether the input starts with the *full* subcommand and uses exact-only name lookup backed by exact registry lookup. Thus `con`, `po`, and a uniquely identifying skill prefix such as `swo` fail where C succeeds. Reproduced `_find_gain_entry('swo', [sword], ...)` returning None. Conversely, strings such as `convertjunk` are accepted as conversion in Python but are not prefixes of `convert` in C. Parse the first token and apply prefix matching in the correct direction; resolve content names with stable ordering.

### 8. P2: Known groups are inferred from abilities rather than durably tracked

Resolved in the runtime contract 2026-10-25: `Character.groups` is an independent list of group names, loaded by `Character.from_json` and emitted by `CharacterService._serialize_character`. `GroupOwnership` supplies shared explicit ownership checks for gain and group display; neither infers ownership from proficiency. Characters may purchase ownership even if all members were learned individually. Missing/null legacy fields load as independent empty lists, with no inferred historical purchases. Save/load regressions preserve both parent and nested ownership independently from learned members.

Content-service contract: character reads and writes must retain `"groups": ["mage default", "combat"]` as an array of group-name strings. New and legacy characters may omit it (runtime default `[]`). Character creation should explicitly include any starting groups it grants. Existing historical ownership cannot be reconstructed reliably from learned abilities; migrate only from authoritative purchase/creation records. The external character service and designer repository were not modified or integration-tested here; durable storage there requires retaining this field.

Validation for items 4, 5, and 8: movement (21), info (18), item/character persistence (9), and learning/object-design contracts (13), 61 tests passed in isolated suite processes. No live content-service save/load was run.

Python: `src/interp/commands/Movement.py:800–822`; `src/interp/commands/Info.py:1300–1332`; `src/player/CharacterService.py:81–117`; `src/player/Character.py:23–43`.
C: `skills.c:175–181,835–870,981–992,1033–1043`; persistence: `save.c` group save/load branches.

C tracks group ownership independently from learned member skills and saves known groups. Python treats knowing all members as owning the group, stores purchases in a dynamically added `character.groups` attribute, and omits that attribute from serialization and the Character model. The group commands then reconstruct ownership from member abilities after reload. Consequently, a player who individually acquires a group's members is incorrectly told they already own the group and cannot purchase its ownership; explicit purchase identity cannot survive save/load. Reproduced serialization omitting an assigned groups list. Add durable content-contract support for group ownership rather than deriving it from proficiency.

## Function coverage and limits

| C functions | Python path / result |
| --- | --- |
| do_gain | Movement.do_gain and gain collection payload; findings 1, 4–8. Conversion's 10 practices -> 1 train arithmetic matches. |
| do_skills / do_spells | Info._do_learned_list and command payloads. Compared learned filtering, level ranges, future n/a entries, two-column grouping, and mana arithmetic. No substantive mismatch found for valid registered abilities with full command arguments; Python sorts names rather than retaining C table order. Python also requires the full `all`, where C accepts its prefixes; minor parser discrepancy. |
| do_groups / group_lookup | Info group listing plus gain lookup. Content names are resolved through registries; see findings 7–8. |
| check_improve | Ability facade -> LearningService -> Character learned records / advancement; findings 2–3. |
| gn_add / group_add | Movement._add_group / _set_learned; findings 4–5 and missing durable ownership. |
| exp_per_level | No equivalent runtime formula found; initial XP requirement is supplied in character data. The gain-points defect is independently verified above. |
| list_group_costs / list_group_chosen / parse_gen_groups / gn_remove / group_remove | No equivalent in-server character-generation purchase/drop flow found by tracing src. Character/account creation may belong to the separate service/designer workflow; this is an unresolved scope difference, not a claim that externally owned behavior is missing. Recursive removal and the 300-point creation limit were not validated against that service. |

Read command documents through collection-query and inspected representative GameData group definitions. Retaining designer-owned metadata/payloads is compatible with parity; no static C tables or hard-coded content are recommended. No established intentional rule overriding these findings was found in the inspected repository guidance/reports.

## Validation

Existing tests, each run in a separate process to avoid global fixture collisions:

- tests.test_object_design_contracts: 9 passed.
- tests.test_movement_dynamic_commands: 13 passed.
- tests.test_info_dynamic_commands: 17 passed.

Total: 39 passed. Additional isolated checks reproduced learning cap/regression, unlearned and under-level improvement, zero-rating division, obsolete trainer-flag lookup, group proficiency reset, nested-name insertion, exact-only lookup, and omitted group serialization. These are focused reproductions, not newly committed regression tests. No live server, external content-service integration, or C executable comparison was run. Probability and state expectations were derived from the local C source.

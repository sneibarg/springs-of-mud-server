# Repository ROM24 parity review — compare, 2026-10-30

**Both findings resolved.** Comparison values now use ROM's new-format dice expression or old-format sum for weapons and the three physical armor values. Named operands use the shared visible unworn-inventory lookup. Implicit equipped candidates require the same normalized type, overlapping wear flags excluding ITEM_TAKE and observer visibility in the current room. Existing keyword and numbered lookup behavior is retained.

Six new regressions cover the reversed weapon/armor rankings, mixed/new/old weapon formats, rounding ties, invisible/incompatible equipment, explicit worn-item rejection and numbered lookup. The information-command fixture now implements the shared inventory lookup contract; the two sleep/wake fixture errors were repaired by supplying consistent room IDs. No runtime visibility bypass was added for test doubles.

**Validation:** across 13 isolated suites, **278 of 281 tests pass**. The sole failing module retains its three existing energy-drain failures, with no errors; both previously exposed sleep/wake subtest errors are gone. `git diff --check` passes. [Remediation results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/compare-remediation-2026-10-30-tests.json). No collection changes or live deployment were performed. The earlier full-repository results below describe the pre-remediation review and were not rerun in full for this focused fix. Original review follows for history.

Current-working-tree review, including all recent fixes. No runtime, collection or test changes were made. Two new behavioral mismatches were reproduced in compare.

## P2 — Compare ranks weapons and armor with incorrect formulas

[ItemApi.py:153](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/ItemApi.py:153) computes weapon value as `(value1 + value2) // 2`, ignoring new_format, and armor value as value0 alone. [Info.py:1062](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:1062) uses these values for player advice.

ROM [act_info.c:2218](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2218) sums armor value0, value1 and value2. Its weapon branch ([act_info.c:2222](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2222)) uses `(1 + value2) * value1` for new-format dice and `value1 + value2` for old-format weapons. The doubled expected-damage representation preserves ordering and avoids rounding ties; the Python fields are already represented as dice for new-format weapons.

Production-method probes with carried items:

- New-format alpha weapon: 2d6; beta: 1d9. Python returned `alpha looks worse than beta.` ROM comparison values are 14 versus 10, so alpha is better.
- Alpha armor: values (1,10,10); beta: (5,1,1). Python again returned worse. ROM values are 21 versus 7, so alpha is better.

Consequence: compare can recommend the weaker weapon or armor and create false ties. Use the reference formulas with the existing new_format discriminator; keep the values as integers rather than dividing to rounded averages. No documented intentional alternative ranking policy was found.

## P2 — Compare selects ineligible and invisible equipment

[ItemApi.py:141](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/ItemApi.py:141) returns the first equipped item of the same type. It does not require overlapping wear flags or observer visibility. ROM [act_info.c:2174](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2174) requires visibility, identical type and shared wear flags excluding ITEM_TAKE when choosing the implicit equipped comparison.

Probe: a carried finger-wearable alpha armor and equipped body-wearable beta armor produced a comparison, despite having no compatible wear location. Setting beta to compatible wear flags but making it invisible still produced `alpha looks worse than (Invis) beta.`, while ItemApi.can_see_object returned false. ROM reports no comparable worn item in both cases when no other eligible candidate exists.

Explicit selectors also differ: [Info.py:1058](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:1058) calls find_owned_item, which includes equipped items. ROM uses get_obj_carry for both explicit operands ([act_info.c:2167](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2167)); that helper requires WEAR_NONE as well as visibility. The explicit Python lookup already checks visibility through AnimateEntity.find_owned_item, so it is specifically the implicit comparison that leaks invisible equipment. Do not remove the existing explicit visibility checks while correcting selection.

Consequence: advice concerns unrelated wear slots, can reveal invisible equipped objects, and permits explicit operands ROM rejects as worn. Use visible unworn inventory for named operands and filter implicit equipment by shared wear flags, type and visibility. Preserve keyword/ordinal behavior through the existing lookup utilities.

## Validation gaps discovered by the broader run

Every top-level `tests/test_*.py` module was executed in a separate process: **131 modules / 1,613 reported tests**. **121 modules / 1,328 tests pass completely**. Ten modules fail, with four failures and 25 errors reported by unittest; subtest error counts are not independent test-method counts. No module timed out.

Nine failing modules have exactly the same failure/error identifiers as social-remediation-2026-10-30-tests.json: combat_group_rewards, combat_handler_aggression, combat_survival, command_authorization, final_combat_parity, mobile_pulse, object_fountain_commands, object_theft_parity and player_handler_cast_prompt.

The tenth, spell_affect_payload_messages, retains the same three energy-drain failures and additionally reports two subtest errors in `test_sleep_blocks_stand_and_targeted_wake_until_expiry_or_dispel` (expiry/dispel). The recent wake lookup now reaches PlayerUtil._get_character_target, where that suite's SimpleNamespace target lacks room_id. This is a newly exposed fixture-contract gap; live Character objects have room_id. The missing fixture data prevents those two integration cases from validating the new path, so they must not be called passing or counted as unchanged baseline errors. No test repair was performed during this review.

[Complete isolated-module results](C:/Users/scott/PycharmProjects/springs-of-mud-server/docs/reports/repository-rom24-parity-2026-10-30-compare-tests.json).

## Scope and limits

Source sampling covered information commands and item selection; movement, portals, training and gain; visible character lookup and recent wake/furniture fixes; melee defenses, position recovery, death consequences and combat stopping; spell saves/effect application; NPC creation and shop-money updates; reset scheduling; tick dispatch, random helpers, learning, command access, notes, tell/reply and persistence serialization. C traces included act_info.c compare, handler.c object-carry selection, act_move.c pick/train and magic.c spell saves. Collection-query inventoried snapshots and inspected the complete compare command: its guards check missing inputs and type/value availability, but supply neither the missing equipment-selection filters nor alternate value formulas.

The deterministic comparison probes used production Item, Info and ItemApi methods with initialized MovementFixture enums and bundled command data. They changed only in-memory entities and made no service writes. Expected results were derived from the local C source, not by executing a C server.

The suite run covers all top-level test modules, excluding tests/old-tests, rather than a combined discovery process whose stubs interfere. Processes used PYTHONPATH=src and local asyncio socket access outside the filesystem sandbox. Source review remains sampled, not a line-by-line comparison of every runtime function and content document. No live-server/content-service or executable-C differential validation was performed. No comprehensive parity certification is implied.

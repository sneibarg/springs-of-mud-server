# Python wrapper review - October 25, 2026

Applied the repository python-code-review skill to Python source under `src`, focusing on unnecessary delegation and type-only adapters. This was a maintainability cleanup; no performance improvement was measured or claimed.

## Changes

Removed 32 forwarding methods and changed their callers to use the implementation directly:

| Area | Removed forwarding methods | Count |
| --- | --- | --- |
| Inventory serialization | CharacterService._inventory_items | 1 |
| Guard normalization | Command._normalize_checks; Ability._normalize_checks | 2 |
| Payload construction and rendering | Fight/Movement/Wiz._command_payload; Communications/Info._render_message_key | 5 |
| Registry and item lookup | Wiz._register_live_character; Object._shop_carried_item | 2 |
| Enum lookup | Movement/Object._enum_bit | 2 |
| Combat helpers | FightHandler._corpse_name, _format_template, _adjust_combat_skill, _combat_target_name, _weapon_skill_name, _check_improve; Fight._target_name; FightApi._active_melee_skill_name | 8 |
| Body-part message formatting | BodyParts._victim_name; BodyParts._format_template | 2 |
| Weapon exposure | WeaponHitHandler._flag, _saves, _element, _object_effect | 4 |
| Spell display | SpellApi._entity_name, _display_effect_message; SpellContext._entity_name | 3 |
| Shop stock comparison | Shop.same_stock_item forwarding layer; the comparison implementation now owns that public name directly | 1 |
| Communications internals | CommunicationsApi._player_handler; no-op __init_subclass__ | 2 |

`Character.get_items()` and its `loot` field now use `list[Item]`. Character serialization passes that list directly to the codec instead of wrapping it in a new `list[Any]` adapter. Snapshot isolation still belongs to the codec and queued save boundary. The existing second guard-normalization pass in Skill remains to preserve its output shape for shorthand entries.

Tests that exercised or mocked removed wrappers now exercise the shared implementation or its output. This includes payload routing, sleep/wake messages, weapon object exposure, learned weapon proficiency, and guard input/output isolation. No wrapper was retained solely to keep an internal test mock working.

## Boundaries retained

A short method is not automatically unnecessary. The scan also found service loader overrides required by FetchAndRegisterMixin, command dispatch entrypoints, designer-facing API methods used by content lambdas, domain operations preserving state rules, asynchronous persistence boundaries, and accessors providing snapshots or synchronization. Those have concrete contracts and were retained. Collection-query checks found no command/skill/spell content references to the removed private payload, normalization, display, player-handler, and active-melee helper names. Collection documents were unchanged.

## Verification

- Broad isolated sweep: 84 top-level unittest modules; 77 passed and 7 failed. The run reported 1013 test executions, including overlapping imported tests and loader failure placeholders; this is not a unique test count.
- The final four forwarding-method removals were verified afterward with the affected combat damage, round skills, dynamic commands, aggression, communications, and guard suites: all six modules passed (149 executions).
- All Python source parsed successfully; `git diff --check` passed.
- Windows asyncio tests ran with local socket access. Modules were isolated in separate processes because fixtures modify `sys.modules`.

The seven failed modules match the failures recorded in the earlier repository review:

- `tests.test_area_pet_shop_resets`: fixture stubs server.messaging as a non-package.
- `tests.test_combat_api_dynamic_checks`: guard fixture lacks context.room.
- `tests.test_combat_death_rules`: XP fixture lacks character_attributes.points.
- `tests.test_combat_group_rewards`: XP fixtures lack character_attributes.points.
- `tests.test_object_fountain_commands`: fixture characters lack owned_items.
- `tests.test_player_handler_cast_prompt`: fixture stubs server.messaging as a non-package.
- `tests.test_spell_affect_payload_messages`: three energy-drain assertions fail during execute_lambdas.

These failures remain outside this cleanup. No live server or external content/persistence service was exercised. F3 remains deferred as requested.

# Repository-wide getattr review

Reviewed the working checkout on 2026-11-08. This is a review and cleanup specification; no runtime source, tests, or collection documents were changed.

## Findings

The excess is primarily defensive access to known model fields, followed by adapters retained around old field layouts and sparse test doubles. There is no demonstrated new gameplay defect in this review. The findings below are nonblocking maintainability recommendations (P3), not performance claims.

### 1. Replace fallback access to fields already guaranteed by the receiver

`src/player/CharacterService.py:114` through `:124` reads six guaranteed Character fields with getattr: hit_roll, dam_roll, saving_throw, aliases, note_read_stamps, and note_read_ids. `_serialize_character` requires a Character and already reads many other Character fields directly. Character declares these members at `src/player/Character.py:41` through `:53`; Character.from_json also initializes the note dictionaries. Attribute absence is not part of this serialization contract.

Use direct access. Preserve `or {}` where it deliberately handles a null value, and preserve wire serialization. Do not change the serializer's payload shape as part of removing getattr.

The same issue occurs in:

- `src/notes/NoteHandler.py:274`, `:280`, `:281`, `:318` through `:328`, and `src/interp/commands/Wiz.py:1243` through `:1258`: notes come from NoteService as InGameNote objects. InGameNote declares all of the queried note fields in `src/notes/InGameNote.py:17` through `:27`.
- `src/api/MoneyApi.py:42`, `:85`, `:86`, `:118`, `:119`, and `:125`: the split actor and group members are live animated entities; gold, silver, and id are base fields. Use direct access after preserving the group/target contract, plus GenericUtil.to_int where still required.
- `src/interp/CommandExecutor.py:41`: command is a required Command, declares lambdas, and is already dereferenced directly before this lookup. Use `command.lambdas or []`.
- `src/item/ItemFactory.py:50`, `:51`, `:66`, `:70`, `:73`, and Item's own field access at `src/item/Item.py:97`, `:104`, `:106`, `:114`, `:120`, `:133`, `:139`, `:150`, and `:160`: fixed fields exist on the actual Item. Keep optional timer/effects behavior and conversions. Treat extra_descr/description separately because those are additional or legacy fields, not equivalent declared Item fields.

The inventory distinguishes explicit typed/self contracts from inferred domain receiver roles. The latter are cleanup candidates, not permission to rewrite every matching spelling mechanically.

### 2. Optional dependency values do not require optional attribute lookup

`src/combat/CombatHandler.py:86` through `:88` initializes escape_handler, npc_skill_handler, and death_handler to None. Subsequent repeated getattr checks at `:606`, `:645`, `:989`, `:1020`, `:1153`, `:1299` through `:1317`, and `:1512` should read those attributes directly and keep their `is not None` conditions.

Similarly, InterpHandler initializes command_audit at `src/interp/InterpHandler.py:33`, and PlayerHandler initializes it at `src/player/PlayerHandler.py:78`. Their getattr calls at InterpHandler `:46`, `:88` and PlayerHandler `:623`, `:668` can use `self.command_audit`. SpellApi initializes elemental_exposure at `src/api/SpellApi.py:47`; `:870` can use `self.elemental_exposure` while retaining the optional dependency fallback.

These dependencies really can be None. Their attributes do not disappear from constructed instances. Update tests using __new__ to establish the required instance state; do not remove the production None branches to make tests pass.

### 3. Use the result and context contracts where they already exist

AliasApi.substitute_command always returns AliasSubstitution, which declares message, message_key, and message_command. `src/interp/InterpHandler.py:62`, `:63`, and `:65` can access those directly.

`src/interp/commands/Object.py:1910` through `:1917` reads WearResult fields through getattr. The callers obtain the structured equipment result, and `src/game/Equipped.py:50` through `:55` declares the fields. Make the result parameter explicitly WearResult and use direct access, preserving message ordering, blocked results, and token normalization.

Context declares result, parameters, character, command, room, raw_command, and handler_service in `src/interp/Context.py`. Fixed-field access in `src/util/InterpUtil.py:139`, `:143`, `src/api/MovementApi.py:564`, `:566`, `:596`, `:603`, and the analogous command argument helpers should use this contract once their accepted input types are narrowed. Existing tests such as `tests/test_interp_util_argument_text.py` explicitly supply a context without those fields; that sparse-fixture contract must be deliberately changed alongside such cleanup.

This does **not** apply to target_item, interp_tokens, tell_disconnected, look_mode, or command-specific get/buy/pour fields. Context does not declare them. Their existence depends on preparation and guard phase. For those fields, verify every preparation path, initialize state at the owning boundary, or introduce a focused command-state type before removing defaults. Avoid turning Context into a collection of every command's unrelated state.

### 4. Remove duplicated shape compatibility at authoritative domain boundaries

`src/interp/commands/Communications.py:683` through `:696` probes guild, clan, clan_name, and clan_id on both a character and CharacterAttributes. The current contract explicitly uses guild (`src/api/CharacterApi.py:105`), and CharacterAttributes declares none of those clan fields. Prefer that authoritative clan/guild operation; remove the old spelling/owner fallbacks as one focused change after checking external callers.

Likewise:

- `src/interp/commands/Info.py:297` through `:299` and `src/combat/CombatHandler.py:846`, `:847` repeat alternate status-field ownership. StatusFlags owns these fields.
- `src/api/SpellApi.py:1009`, `:1010`, `:1093`, and `:1094` retain move/max_move fallbacks around the current movement/max_movement names.
- `src/interp/commands/Movement.py:776` probes ratingByClass even though Ability uses rating_by_class after boundary normalization.
- `src/interp/commands/Communications.py:577` probes who_name, which is not declared by CharacterClass; the class-name fallback is the actual current model path.
- `src/interp/commands/Fight.py:592` probes both bashing and bash. Both layouts currently exist: player ArmorClass uses bashing, mobile ArmorClass uses bash. This is real polymorphism. Reuse the existing ArmorValues.base_value operation rather than choosing one spelling globally.

The goal is one explicit normalization/ownership decision, not another generic safe-getattr wrapper. Preserve the designer/content-service boundary; do not substitute hard-coded content behavior.

### 5. Stop probing required domain methods solely to accommodate incomplete doubles

`src/server/connection/Connection.py:38` defines get_peer_info, inherited by TelnetConnection. The fallbacks in ConnectionHandler at `src/server/handlers/ConnectionHandler.py:191` and `:447` add no normal connection behavior; nearby paths already call this method directly. Require the connection contract and make doubles implement it.

Room methods such as people, find_visible_target, add/remove item, and add/remove player/mobile are similarly probed with fallback dictionary mutation in CommunicationsApi, Movement commands, MobileApi, LookupUtil, and ItemOwnership. Use the real Room/Item/AnimateEntity capabilities for runtime domain objects. If an additional shape is intentionally supported, keep that adaptation at one documented boundary instead of duplicating it in every command.

Concrete examples include `src/api/CommunicationsApi.py:137`, `:302`, `:328`, `src/interp/commands/Movement.py:925`, `:933`, `:1019` through `:1030`, and `src/item/ItemOwnership.py:21`, `:35`, `:44`, `:59`.

Within EffectHandler, the getters at `src/item/EffectHandler.py:91`, `:94`, `:96`, `:99`, `:101`, `:109`, `:173`, and `:179` are already inside matching hasattr branches. Use direct access **inside those branches** even if the outer compatibility checks remain.

### 6. Preserve genuine reflection and deliberate conversion boundaries

The following should not be blanket-replaced:

- Runtime-selected enum names, equipment slots, stat names, resource/currency fields, dataclass serialization fields, dynamic command dispatch, and lazy module exports. Examples: `src/game/Equipped.py:121`, `src/api/CharacterApi.py:486`, `:503`, `src/server/WireCodec.py:30`, `src/combat/CombatSkillHandler.py:59`.
- Enum member/raw integer normalization (`getattr(member, 'value', member)`) and optional named enum members. Prefer existing EnumProvider/EffectUtil operations where they fit, but keep the actual accepted scalar/member behavior.
- `src/item/EffectHandler.py:111` through `:132`: as_effect explicitly accepts legacy effect-like objects in addition to Effect/dict/string. Attribute absence is part of that adapter's input contract.
- `src/server/messaging/MessageBus.py:37`: plain text and recipient-specific rich text are intentionally different shapes.
- `src/skill/SpellContext.py:40`, `:43` and `src/mobile/MobileContext.py:29`: dynamic API dispatch.
- `src/interp/Context.py:36`, `:41`: view/context unwrapping and character-state creation accept different shapes. Mobile does not declare every player field. These helpers need explicit contracts before simplification.
- Character-only fields such as trust, role, character_class, aliases and world_retired, versus mobile-only fields such as short_description, vnum, group and special_name. Narrow the entity kind before direct access. Do not copy player fields into every object merely to remove getattr.
- Lazy/ad hoc fields such as on, pet, _effect_wearer, _special_state and _world_update_lock. Promote them to the appropriate model if the engine intends them to exist universally; otherwise their absence is real.

### 7. Distinguish prototypes, live entities, and optional nested values

AnimateEntity declares equipped, status_flags, character_attributes, and armor_class as optional. A direct base-field read is safe; immediately dereferencing its result without checking is not. MobileFactory.create installs runtime hit/max_hit/mana/max_mana/position fields, while raw mobile prototypes need not have that complete runtime state (`src/mobile/MobileFactory.py:155` onward).

The documented alignment adapter at `src/game/AnimateEntity.py:57` through `:62` is a useful counterexample: runtime attributes own alignment, while mobile prototypes retain the service field. Preserve that distinction.

SessionState always declares character, but character may be None (`src/server/session/SessionState.py:29`). Use `session.character`, then retain the guard. A missing playing-session character is not equivalent to a missing attribute.

Item.timer and Item.effects can be None (`src/item/Item.py:59`, `:64`); equipment slots can be None even when Equipped exists. These are valid model states, not low-probability accidents.

## Scope and evidence

- Enumerated 399 Python files with AST parsing: 1,857 direct builtin getattr calls, comprising 1,525 runtime calls in 90 files and 332 test calls in 55 files.
- Inspected one additional getattr inside the executable subprocess-test string in `tests/test_area_pet_shop_resets.py:175`. The embedded code selects a flag field by name; retain reflection.
- Queried all collections through devtools for getattr expressions. The 29 matching documents contain 296 calls: 25 commands, three skills, and one spell. The collection inventory records each document, nested expression path, and call separately.
- Total occurrence coverage: **2,154 calls**, including the embedded test script. Nested getters are separate occurrences, not merged into one line.
- Reviewed domain declarations, factory/service construction, relevant callers, runtime extension assignments, command preparation, and representative tests. The CSV records declaration evidence and the strength of each conclusion.

`python-calls.csv` is the exhaustive direct-Python inventory. `embedded-python-calls.csv` covers the subprocess string. `collection-calls.csv` covers executable content expressions. `summary.json` contains counts. `file-summary.md` indexes all files containing direct calls.

## Meaning of the classifications

The direct-cleanup group comprises DIRECT_CONTRACT, DIRECT_INITIALIZED, DIRECT_GUARDED, and DIRECT_CLASS. These establish member presence through a declared/typed receiver, constructor assignment, preceding matching hasattr, or imported class definition. Existing optional-value checks and conversions remain necessary.

MODEL_CANDIDATE records members backed by domain models but used through untyped or broadly typed parameters. Its receiver type is an explicit inference, and removing getattr is conditional on preserving/narrowing the receiver and None contract. These are not counted as proven-safe substitutions.

The other classifications specify what must change or remain: runtime-only fields, union/prototype differences, old layouts, optional capabilities, command extensions, content-loaded enum contracts, and intentional adapters. TEST_FIXTURE records intentionally sparse test doubles. KEEP_DYNAMIC records actual runtime field selection.

An exhaustive occurrence inventory is not whole-program nullability proof. Python permits mutation and dynamically evaluated content; production source uses Any and accepted alternate shapes. Where None cannot be ruled out, the inventory says so. No probability or claim that a value can never be None is inferred from a field name or type hint alone.

`getattr(obj, 'field', fallback)` returns the fallback for an absent attribute, including access on None; it does **not** replace an existing field whose value is None. Therefore two independent questions govern each cleanup: whether the receiver can be None, and whether the attribute is guaranteed to exist. A third question is whether its value may be None. Keep these decisions separate.

## Implementation order and verification

1. Replace the direct-cleanup group in small domain batches. Preserve serializers, payload keys, message order, `or` fallbacks and numeric conversions.
2. Tighten model-backed candidates at their receiver boundary and update sparse test fixtures in the same batch. Do not add a common fallback wrapper.
3. Consolidate legacy ownership/name adapters using existing domain operations. Keep actual player/mobile and player/mobile-armor differences explicit.
4. For content expressions, prove preparation-before-evaluation for each command family before removing command-state defaults. Of the 296 collection calls, 249 touch prepared context extensions; they need this path analysis rather than a bulk string replacement. Use collection-query and collection-modify for any resulting data edits.
5. Preserve reflective dispatch, serialization, dynamic names, and documented adapters.

Regression coverage should exercise serialization/save-reload, absent equipment and slots, prototype versus spawned mobiles, optional handler dependencies, disconnected/switched sessions, command guard ordering, invalid targets, and normal/failed command preparation. Test actual dataclasses as well as sparse fixtures; fixture convenience must not define an accidental production interface.

Verification results and final classification totals are recorded below after inventory reconciliation. No gameplay source changes were made during this review.

## Final totals

| Runtime decision | Calls |
|---|---:|
| CAPABILITY_CONTRACT | 6 |
| DIRECT_CLASS | 3 |
| DIRECT_CONTRACT | 202 |
| DIRECT_GUARDED | 12 |
| DIRECT_INITIALIZED | 18 |
| ENUM_CONTRACT | 8 |
| GUARD_THEN_VARS | 7 |
| KEEP_ADAPTER | 53 |
| KEEP_DYNAMIC | 102 |
| KEEP_EXTENSION | 53 |
| LEGACY_SHAPE | 24 |
| MODEL_CANDIDATE | 893 |
| RUNTIME_CONTRACT | 27 |
| SHAPE_CONTRACT | 97 |
| UNION_CONTRACT | 15 |
| WEATHER_CONTRACT | 5 |

235 runtime calls are in the direct-cleanup group. Another 893 are model-backed candidates with conditional receiver contracts. The remaining 397 runtime calls involve dynamic names, adapters, optional shapes, legacy layouts, capabilities, or initialization changes. These counts describe review recommendations, not implemented replacements.

Tests contain 86 direct-AST dynamic-name calls and 246 literal-name fixture calls; the embedded subprocess adds one dynamic-name call. Collections contain two declared-context calls, 249 prepared-context calls, 31 entity-model candidates, and 14 other contract-dependent calls.

## Validation performed

- Reparsed all 399 Python files and reconciled every direct occurrence by file, line, and column against the inventory; no missing or duplicate occurrences. Nested calls and the embedded subprocess call are separately accounted for.
- Parsed all 296 matching collection calls from documents retrieved through the devtools CLI; preserved document names and expression paths in the separate inventory.
- 27 existing tests passed: all 21 movement dynamic-command tests, three money-splitting regressions, and three item-ownership tests. These provide baseline coverage, not proof that hypothetical rewrites are correct.
- The note-command test run produced no result and was interrupted; no passing note-test result is claimed.
- git diff --check passed. Git status showed only this untracked review directory; no runtime, test, or collection edits.
- Source revision: 88e09931ea0849c42282048548c2b5bf384432f5. source-hashes.json records the reviewed Python files so line-based findings can be checked against later changes.

No new abstraction or design pattern is warranted for the direct replacements. Prefer explicit domain contracts and existing operations; introduce a small boundary adapter only where additional input shapes are demonstrated.

# getattr cleanup progress

The original report and inventories describe the reviewed source revision. Keep them as the audit baseline; this file records subsequent implementation batches.

## Completed: notes model fields

Replaced 22 fixed-field getattr calls with direct InGameNote access:

- 14 in src/notes/NoteHandler.py: unread timestamps, deletion IDs, sorting, recipients and note formatting.
- Eight in the note display helpers in src/interp/commands/Wiz.py: sorting and individual/list rendering.

NoteService constructs InGameNote from service responses, and NoteRegistry stores and returns InGameNote. Helper annotations now make that existing contract explicit. Numeric conversions, null-value normalization, note lookup guards, sorting and display numbering are preserved.

These sites were model-backed candidates in the original inventory. Inspection of the service and registry established their concrete receiver contract before replacement. No broad receiver/type normalization was introduced.

At the end of this batch, eight getattr calls in NoteHandler concerned character/context access rather than note fields. The player batch below subsequently removed the three character-name/guild lookups and processed Character's note-read tracking and serialized read state. Five context-related lookups remain for the interpreter/context contract pass.

Validation: all 15 tests in tests.test_note_commands passed. The restricted Windows sandbox stalled while asyncio created a local event-loop socket pair; the normal test command passed outside that restriction. Twelve additional comparisons against HEAD confirmed identical wizard note formatting and sorting for populated, default and None-valued note fields. git diff --check passed.

## Completed: players and persistence

Removed another 48 getattr calls: 18 in Character, six in CharacterService, 21 in PlayerHandler and three character-field reads in NoteHandler.

- Character now reads its declared note-read dictionaries, equipment, status, race, resource and class fields directly. Explicit checks preserve absent equipment, missing status/attributes/class/race, optional slot values and null note-read dictionaries.
- CharacterService uses the six declared persistence fields directly, preserving wire names, serializer behavior and null dictionary normalization.
- PlayerHandler uses validated entity, room, item, context and command fields directly, including prompt targets, visibility/extra-description lookup, nested commands and standard payload rendering. The optional command_audit value remains checked where needed; its attribute is always initialized by the constructor.
- NoteHandler uses the player's declared name/guild fields directly. Test-only character fixtures now initialize note-read dictionaries and guild, and affected __new__ handler fixtures initialize command_audit.

Six getattr calls remain in src/player for intentional contracts: the lazy world-update lock, runtime-selected condition fields, the legacy size extension when no CharacterRace is available, dynamic advancement fields, optional payload getter adaptation, and dynamic payload channels. These are outside the fixed-field replacement pass.

Validation covered 379 distinct test methods across 24 isolated modules: 369 passed and ten failed. The same ten failures, including matching exception signatures, were reproduced with the original HEAD versions of the three player files loaded in memory. They concern outdated InterpHandler.handle_command calls and an input-wait timeout. Nineteen complete modules passed (307 tests); the other suites' successful methods account for another 62 passes. The six persistence-boundary tests and all 15 note tests also passed in the final targeted rerun. git diff --check passed.

The source comparison did not alter working files. Detailed module results and baseline failure evidence are in players-validation.json, players-additional-validation.json, players-final-targeted-validation.json and players-baseline-validation.json. No interpreter signature or unrelated timing behavior was changed.

## Completed: items and effects

Removed 85 getattr calls across 11 files in src/item:

- Item: 22; EffectHandler: 34; EffectUpdateHandler: nine.
- ItemFactory: five; BodyParts: four; DeathLoot and ItemUpdateHandler: three each.
- ItemHandler: two; BodyForm, Effect and ItemOwnership: one each.

Item fields, normalized Effect fields, known stat/flag fields and body-part item fields now use direct access. EffectHandler retains its target-kind checks and legacy conversion boundary; within existing hasattr branches, the subsequent fixed-field reads are direct. The wielded-slot lookup now checks explicitly for absent equipment. Item type predicates retain an explicit None branch, and flag checks retain the former false result for a missing item. Optional timers/effect lists, numeric conversions and recursive container accounting remain intact.

Sparse test fixtures now supply the item contents/type/weight fields, equipment wielded slot and clone enchanted state that real models guarantee. Test execution sets src on PYTHONPATH for standalone modules that do not initialize their own import path.

The 57 remaining calls in src/item cover dynamic enum/stat/serialization names, enum-versus-scalar conversion, legacy extra descriptions, lazy wearer/wear-location state, heterogeneous effect targets, optional ability rendering and ownership capability adaptation. They are retained for the later contract pass rather than replaced mechanically.

Validation covered 588 distinct test methods across 35 isolated modules: 583 passed and five failed. Thirty-four complete modules passed (573 tests); ten more methods passed in the broader repository-parity suite. Its five failing methods use the outdated InterpHandler.handle_command signature, and their failure signatures were reproduced with the original HEAD item source loaded in memory. No remaining item/effect regression was observed in these checks. Coverage includes 131 spell-effect tests, recursive item accounting, equipment modifier reversal, decay/update handling, loot, body parts, cloning, poison/acid exposure, item activation and persistence. git diff --check passed.

Results and the original-source comparison are retained in the items-*-validation.json files. The initial items-validation.json records the first run; later fixture/final/clone result files supersede the corresponding initial failures.

## Completed: combat

Removed 156 getattr calls across five combat files: 137 in CombatHandler, 14 in CombatDeathHandler, three in CombatSkillHandler and one each in CombatEscapeHandler and CombatView.

The cleanup uses declared live-entity, room, item, exit and dice fields directly, plus the three optional handlers initialized by FightHandler.__init__. Optional fighting targets, masters, equipment, status flags and armor retain their value checks. Room/entity lookup helpers explicitly retain their None return/false behavior. Weapon-name logging, death-room descriptions and immunity checks keep explicit absent-value handling. NPC-only fields are read only in the existing NPC branches; player/mobile attack-type differences remain adapted.

The 33 remaining calls cover actual runtime selection, lazy pet/controller/wear fields, skill/payload and pronoun capability adapters, old XP time ownership, legacy form/parts storage and player/mobile damage-type differences. These belong to the later contract pass.

Shared combat fixtures now supply the fields required by their real entity/room/item/exit models. __new__ handler fixtures initialize the optional handlers, and the nested-input fixture initializes PlayerHandler.command_audit. No assertions were weakened, and no combat rules, message keys or collection documents were changed.

Validation covered 582 tests across 36 existing modules: 577 passed and five failed. Thirty-four complete modules passed (563 tests), with another 14 successful tests in the input/flee suite. The five remaining failures are four input tests and one repository-visibility test calling the outdated InterpHandler.handle_command signature; the same failures and exception signatures were reproduced with the original HEAD combat source loaded in memory. Coverage includes aggression/assistance, attack damage and rounding, defenses, NPC skills, immunity, status effects, experience/group rewards, death/corpse transfer, autoloot/autosacrifice, fleeing, weapon/spell effects and mobile callers. The final immunity simplification was rechecked with all 30 guarded-flag/shared-gameplay tests. git diff --check passed.

The combat-*-validation.json files retain the initial, fixture, additional, final, follow-up, immunity and baseline results. An attempted module name that did not exist is marked excluded in the raw final-run log and is not counted as a repository test or failure.

## Completed: shared game state and equipment

Removed 57 getattr calls across five game files: 19 in AnimateEntity, five in Equipped, seven in UpdateHandler, 25 in WizHandler and one in EntityUpdateHandler.

AnimateEntity now reads declared state directly while preserving optional character attributes, status flags and equipment. Owned equipment uses vars after the existing None check. Regeneration still distinguishes prototypes/base entities from spawned resource state, and room regeneration rates use the declared Room fields after the existing missing-room guard. Equipment contribution and removal helpers retain explicit handling for missing characters, equipment and slots. Session enumeration uses SessionState's declared character/metadata fields and keeps the existing None, switched-original and live-player filtering. Switching, socket displays and wizard diagnostics use their established entity/room/command fields directly.

The 63 remaining calls in src/game cover runtime enum/slot/stat/channel selection, legacy storage ownership and optional extensions, scalar-versus-enum conversion, prototype/resource differences, controller context and slot initialization. No dynamic content, startup binding or scheduler/persistence ownership changes were introduced.

Audit correction: the original inventory marked the two fixed-name getters in StatusFlags.__setattr__ as DIRECT_CONTRACT. StatusFlags is a slotted dataclass, and those slots are not yet initialized when construction first invokes __setattr__. Field declarations alone do not prove presence at that phase. Both checks are intentionally retained, and StatusFlags is unchanged. This is an exception to the original first-pass classification, not an outstanding replacement task.

Fixtures now provide declared session metadata and optional entity attributes. Equipment-effect fixtures use the real Equipped model where all slots are expected, and the school-light prototype fixture supplies value2. No assertions were weakened.

Validation covered 670 tests across 32 isolated modules: 667 passed and three failed. Thirty complete modules passed (634 tests), with 33 additional successful tests in the two broader suites. The remaining failures are the known input-wait timeout and two outdated InterpHandler.handle_command calls; identical failure signatures were reproduced with the original HEAD game source loaded in memory. Coverage includes updates/regeneration/conditions, equipment light and armor effects, save/reload/autosave, switched bodies and wizard controls, combat, item handling, mobile callers, bitfield guard behavior and 131 spell-effect tests. git diff --check passed.

The game-state-*-validation.json files retain initial, fixture, additional, final-fixture and original-source comparison results. The initial failures superseded by completed fixtures remain in the raw logs for traceability.

## Completed: interpreter and commands

Removed 380 getattr calls: 377 in src/interp across 11 files, plus three deferred context reads in NoteHandler. Object commands account for 144 removals; Fight 62, Movement 61, Info 50, Wiz 28 and Communications 23. CommandAudit, CommandExecutor, InterpHandler, InterpService and SocialHandler account for the other nine.

Command metadata, declared Context fields, alias substitution results, WearResult fields and established live entity/item/room fields now use direct access. Optional command audit entries, equipment, targets, status flags, weather information and skill metadata retain explicit None handling. Corpse pickup still accepts an absent container, and pet purchase haggle messages still accept an absent shopkeeper. Social pronouns retain their neutral result for an absent target. No command rules, content expressions or collection documents changed.

The 145 remaining calls in src/interp cover dynamic names, deliberately fail-closed command metadata validation, prepared context extensions, player/mobile shape differences, legacy ownership and capability adapters. These remain for the separate contract pass. In particular, Mobile prototypes do not initialize live resource values until spawning; the group-display fixture now supplies the resource state of a spawned group member.

Updated 25 stale test calls to the existing two-argument InterpHandler.handle_command API and corrected the input queue fixture callback signature. Fixtures that bypass handler construction now initialize optional command_audit state. Shared command fixtures supply declared model fields and context services, without weakening assertions.

Validation passed all 1163 tests across 83 isolated modules. Coverage includes command authorization/execution, queued and nested input, alias/social handling, note commands, communications, movement/following/portals, learning/training, inspection, object pickup/containers/currency/shops/consumption/equipment/theft/item spells, combat commands and wizard controls. The input-wait and outdated interpreter-call failures recorded in earlier batches are resolved by these fixture signature updates. git diff --check passed. Final module output is retained in interpreter-validation.json; interpreter-removals.json records the source-package counts.

## Completed: gameplay APIs

Removed 191 getattr calls across 12 files in src/api: SpellApi 68, MobileApi 32, WizSetApi 23, CommunicationsApi 22, MovementApi 11, ItemApi nine, CharacterApi eight, MoneyApi seven, AreaApi four, FightApi and WizApi three each, and GameApi one.

Declared live entity, room, item, effect, ability, Context and SpellContext fields now use direct access. Money splitting reads established currency/id fields, location lookup reads room/mobile names, and wizard operations read initialized dependencies and model state. Equipment dictionaries use vars after explicit optional-equipment checks. Optional targets, receivers, status flags, weather and ability references retain their previous missing-value handling. Item flag and portal-key selection use conditional field access. Runtime behavior and collection documents are unchanged.

The 100 remaining calls in src/api cover dynamic enum/stat/payload/slot names, prepared command state, lazy controller/pet/special state, player/mobile differences, legacy movement/position ownership, pronoun/message capabilities and heterogeneous context/handler adapters. These remain for the separate contract pass. AliasApi's alias-state lookup also remains because Mobile does not declare the Character aliases field.

Fixtures now supply the declared currency/ownership/status, actor/target identity, spell noun/cast-level, context parameters and room membership fields exercised by the changed paths. No assertions were weakened.

Validation covered all 136 top-level test modules in isolated subprocesses: 1,669 of 1,685 test methods passed, with 131 complete modules passing. The 16 remaining failures across five modules were reproduced with the original HEAD API source loaded in memory; failed method sets and exception signatures match. They are fixture gaps from prior domain batches: area_occupancy and mobile_special_room_access omit equipped, combat_death_rules omits container.owner, combat_round_skills uses object() for a Room, and corpse_currency omits the NPC short description. No remaining API regression was observed. The corrected spell suite passed all 131 tests, and movement passed all 21. git diff --check passed.

apis-validation.json retains the initial run, apis-final-validation.json the broad follow-up, apis-followup-validation.json the final spell/movement fixture checks, apis-combined-validation.json their combined result, and apis-baseline-validation.json the original-source comparison. apis-removals.json records per-file counts.

## Completed: areas and rooms

Removed 27 getattr calls across three files: AreaHandler 17, Room six, and Shop four. Reset population counting, nested world-item traversal, room light/ownership, exit directions and pet placement now read declared model fields directly. Equipment traversal uses vars after existing None checks; the fixed player/mobile inventory selection in Room.item_locations uses a conditional rather than dynamic attribute lookup.

Missing pet-shop stock rooms still return False, optional equipment is skipped, recursive item traversal retains its cycle detection and None filtering, and exit randomization explicitly skips absent exit entries. Shop.complete_pet_purchase already requires a Room for add_mobile_to_room, so its subsequent room and area assignment reads that Room directly. No reset limits, shop rules, ownership precedence or collection documents changed.

The three remaining getattr calls are intentional: person.on is attached lazily by furniture actions, ROOM_IMP_ONLY is an optional enum member, and Item.wear_loc is lazy wear state rather than a declared Item field.

Room-occupancy fixtures now provide the optional equipment field declared on live player/mobile models, resolving all six occupancy failures recorded in the preceding API batch. Spell location/travel observers now provide the Character loot list used by Room.item_locations. No assertions were weakened.

Validation covered 452 tests across 26 isolated modules: 445 passed, with 25 complete modules passing. Coverage includes occupancy, area services, live reset limits, pet shops, door resets, reset equipment, nested ownership, location lookup, movement/following, shops, world population, wizard movement and all 131 spell tests. The seven remaining failures in test_mobile_special_room_access omit equipped in their shared fixture; their method set and AttributeError signature match a run with the original area source loaded in memory. This existing mobile fixture issue is retained for the next domain. git diff --check passed.

areas-validation.json retains the initial result, areas-followup-validation.json the final occupancy/spell checks, areas-combined-validation.json their combined result, and areas-baseline-validation.json the original-source comparison. areas-removals.json records per-file counts.

## Completed: mobiles

Removed 30 getattr calls across four files: MobileHandler 25, Mobile and MobileContext two each, and MobileFactory one. Kill-table levels, mobile identity/currency/special fields, area state, special definitions, room diagnostics, recipient IDs and clone effects now use declared fields directly. Expired-stock credit retains its zero-cost behavior for an absent item, and special execution/diagnostics retain their absent-mobile handling. No special lambdas, update ordering, stock-replenishment rules, clone ownership, bindings or collection documents changed.

The six remaining calls are intentional: MobileContext dispatches API names dynamically; same_special can compare a player or other entity without special_name; cloning selects optional live/prototype fields by name; wear_loc is lazy item state; MobileHandler dispatches named fight commands; and wealth is an extended factory field absent from directly constructed Mobile models.

Completed the mobile-special room fixtures with declared equipment/fighting fields, resolving all seven failures recorded in the area batch. Mobile pulse fixtures now supply the declared optional special fields. The isolated clone factory fixture supplies the empty effects list created by the real factory. No assertions were weakened.

Validation covered 348 tests across 28 isolated modules: 346 passed, with 26 complete modules passing. Coverage includes runtime factories, special binding and room targeting, pulse ordering, shop replenishment, scavenging, resource/armor isolation, resets, clone contents/equipment, world population, following, combat and expired stock. The two remaining failures in test_combat_death_rules and test_corpse_currency omit container.owner and the NPC short description respectively. Both failed method sets and AttributeError signatures match runs with the original mobile source loaded in memory; they are existing fixture gaps outside this batch. git diff --check passed.

mobiles-validation.json retains the first run, mobiles-final-validation.json the final broader run, mobiles-baseline-validation.json the original-source comparison, and mobiles-removals.json the per-file counts.

## Completed: skills and spells

Removed six getattr calls across four files: SpellContext three, and Ability, AbilityResolver and GroupOwnership one each. The learning-service fallback calls CharacterApi's declared get_registry method directly while retaining its unconfigured-runtime handling. Effect-owner lookup reads Ability's handler_id/name/id fields directly. Group ownership reads Character.groups on the existing player-only command paths and preserves an empty list for a missing character. SpellContext reads actor level and Item short_description/name directly, retaining absent-actor level zero, cast-level precedence and absent-target handling.

The seven remaining calls are intentional: LearningService supports metadata with class-specific methods as well as older metadata exposing only maps; improvement messages use lazy transient state; SpellContext adapts handlers that may not expose spell_api and dispatches API names dynamically; the package initializer resolves lazy imports by name. No learning probabilities, class fallback rules, resolver ordering, message keys, content expressions or collection documents changed.

Completed the item spell fixture with Item.short_description. No assertions were weakened.

Validation covered 876 tests across 53 isolated modules: 875 passed, with 52 complete modules passing. Coverage includes learning/proficiency, practice/training/groups, ability lookup, casting, spell effects and messages, object spells, inspection, advancement, guards, movement and relevant combat/repository paths. All 131 spell tests passed after the fixture correction. The sole remaining failure is test_combat_round_skills.test_selected_kick_uses_real_command_wait_rating_damage_and_payload, whose fixture uses object() for a Room; the failed method and AttributeError match the original skill source loaded in memory. git diff --check passed.

skills-validation.json retains the initial result, skills-followup-validation.json the final spell checks, skills-combined-validation.json their combined result, skills-baseline-validation.json the original-source comparison, and skills-removals.json the per-file counts.

## Completed: shared utilities

Removed 57 getattr calls across 12 files in src/util: WizDiagnostics 12, EffectUtil and FightUtil ten each, DisplayUtil seven, LookupUtil and SkillUtil four each, EntityExtractor three, ElementalExposure and PlayerUtil two each, and InfoUtil, InterpUtil and WizUtil one each.

Rendering, lookup, saving throws, effect display, melee adjustments, combat links, diagnostics and world membership now read declared entity/item/effect/room/ability fields directly. Optional receivers, missing rooms, missing equipment and None skill metadata retain explicit handling. The 33 remaining calls cover runtime enum/stat/slot selection, lazy furniture/wear/controller/pet state, player/mobile and legacy position/proficiency adapters, heterogeneous diagnostic fields and non-command argument contexts. In particular, InterpUtil.argument_text intentionally continues accepting contexts without result or parameters, as covered by its existing regression test.

## Completed: connections, sessions and messaging

Removed six getattr calls across two server files: three in ConnectionHandler and three in MessageBus. Login paths call Connection.get_peer_info directly; the input gate reads declared status flags while preserving an absent character; snoop mirroring reads SessionState.character/metadata and the Character name directly. Async boundaries, input ordering, session transitions, persistence and message-routing behavior are unchanged.

The five remaining server calls are intentional: reload validation rejects documents whose required ID is missing, switched-body context can be absent, recipient-specific text is a capability protocol, WireCodec serializes dataclass fields by name, and the package initializer resolves lazy imports dynamically.

## Final validation and fixture completion

The final run passed all 1685 tests across all 136 top-level test modules, each in an isolated subprocess. This covers gameplay, spell/content pipelines, sockets/session behavior, messaging/snooping, input gating, persistence, reloads and developer tooling. git diff --check passed.

Shared fixtures now supply the fields their real models declare: NPC/item descriptions, entity names and room IDs, room collections, effect bitvectors and levels, status counters, session character names and ability IDs. Assertions were preserved. The three outstanding fixture failures from previous batches are resolved: the combat-round fixture now supplies a Room-shaped object and ability ID; money pickup supplies container ownership and item flags; the common NPC fixture supplies its short description. An overlapping fixture edit was corrected before the final successful run.

final-domains-validation.json contains the successful full-suite results; final-domains-removals.json records per-file counts. Earlier batch reports remain historical snapshots and their failures are superseded by this final run.

## Domain pass complete

All planned source domains have completed their applicable first-pass cleanup. The retained lookups above are not blanket replacement targets. The original report's separate contract/legacy cleanup and prepared-content-expression analysis remain distinct follow-up work; these passes did not modify designer-authored expressions or collection documents. Original inventory files remain unchanged for traceability.

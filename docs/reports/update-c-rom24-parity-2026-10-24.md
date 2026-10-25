# update.c ROM24 parity review

Reference: `C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c`. Python: current Springs of MUD working tree, including existing uncommitted changes. Review only; no gameplay or collection edits.

Each update type has its own subsection below. Functions defined in update.c but serving as helpers are covered separately. Area, music, and violence are covered at their scheduler boundary because update.c calls them but defines them elsewhere. Findings distinguish verified defects from differences whose product intent remains unresolved.

## Update types

### update_handler: pulse scheduling

**P2 — Tick work executes before mobile and violence pulses instead of afterward.** C `update.c:1081–1134`; Python `src/game/UpdateHandler.py:47–72`. At coincident deadlines, C executes area, music, mobile, violence, weather, character, object, then aggression. Python executes area, weather, character, object, music placeholder, mobile, violence, then aggression. Therefore specials see the new hour one mobile pulse earlier; regeneration, poison, expiring effects and object decay happen before combat instead of after combat. This can alter who survives a combat pulse and which effects apply to it. This is the scheduler mismatch also identified in the mobile-specials report.

The configured periods match C merc.h: four pulses/second; area 480 pulses, music 24, mobile 16, violence 12, tick 240. Both initialize counters to zero and decrement before testing. The local C's purported random pulse intervals are commented out; Python's fixed periods are not a mismatch.

**P3 — Missing tick monitoring notice.** C `update.c:1116` emits `TICK!` through WIZ_TICKS. Python's tick branch has no equivalent notice. This removes an administrator's tick-observation facility, though it does not itself stop updates.

### area_update: area aging/reset pulse

C call: `update.c:1093`; implementation: `db.c:1172–1210`. Python: `src/area/AreaHandler.py:54–69`.

Compared the age increment, initial three-update gate, empty/occupied reset thresholds, random age reset to 0–3, school age override to 13, and empty-area transition. These decisions match the inspected C path. Python's registry ownership is compatible with the chosen architecture.

**P3 — Reset monitoring notice omitted.** C `db.c:1194–1196` announces resets to WIZ_RESETS; the Python age/reset path does not. Individual reset command semantics were not audited here.

### song_update: music pulse

C `update.c:1096–1100`, `music.c:45` advances queued songs and delivers song text. Python `src/game/UpdateHandler.py:41,62–63` resets the counter but performs no song update. This is a verified missing behavior, with **unresolved intent**: the comment says music may be skipped, but no confirmed product decision was found. Treat this as a scope decision, not an automatic requirement to implement ROM's music system.

### mobile_update: autonomous NPC pulse

C `update.c:374–461`; Python `src/mobile/MobileHandler.py:85–157`, `src/api/MobileApi.py:628–727`.

Charmed/empty-area eligibility, assigned-special dispatch before the standing check, scavenging's 1-in-64 roll, wandering's 1-in-8 roll followed by a 0–31 direction roll, and the inspected exit/area/indoor gates substantially match C.

**P2 — Shopkeeper replenishment occurs before the special can claim the pulse.** C `update.c:393–405` calls the special first and skips replenishment on true. Python `MobileHandler.py:111–119` replenishes first. A shopkeeper with a successful special receives money and consumes two extra random rolls when C would skip both.

**P2 — Scavengers ignore loot ownership and take items silently.** C `update.c:423–437` requires `can_loot` and announces `$n gets $p.`. Python `MobileApi.py:644–659,824–829` tests takeability/cost only and moves the object without queuing a pickup message. Thus an owned, takeable item that fails C's `act_obj.c:58` ownership checks can be stolen by a scavenger, and observers do not see the pickup. Keep the ownership check and content-owned room notice in the generic primitive.

The previously verified mayor-specific position/combat/return-value defects remain applicable; see [mobile-specials report](mobile-specials-rom24-parity-2026-10-24.md). They are special behavior defects, not evidence that the four-second scheduler fails to invoke specials. This review does not re-audit all special documents or every move_char side effect.

### weather_update: clock, sunlight, pressure and sky

C `update.c:467–599`; Python `src/game/WeatherHandler.py:43–148`.

Hour transitions 5/6/19/20, day/month rollover at 35/17, seasonal pressure threshold 985 versus 1015, change clamp -12..12 and pressure clamp 960..1040 match the inspected normal paths.

**P2 — Three transitions compare the sky enum to pressure thresholds.** Python `WeatherHandler.py:127,131,134`; C `update.c:555–579` compares mmhg throughout. In Python, cloudy skies never clear at high pressure because sky > 1030 is impossible; rain can become lightning at ordinary/high pressure because sky < 970 is always true; and guaranteed clearing above 1030 is lost. Python also uses elif after its erroneous lightning check, suppressing the rain-clearing branch whenever that check succeeds. Reproduced with a zero chance roll: cloudy/1040 remains cloudy; raining/1000 and raining/1040 both become lightning. C would clear the first and third and leave the second raining.

**P2 — Sleeping players receive outdoor weather messages.** C `update.c:588–596` sends only to playing, awake, outside characters. Python `WeatherHandler.py:49–69` broadcasts to everyone except IDs returned by `_indoors`; that helper excludes only characters who are both indoors and awake. Sleeping players indoors and outdoors are therefore included. MessageBus.broadcast (`src/server/messaging/MessageBus.py`) treats its second argument as an exclusion list, confirming this is not merely an unfortunate helper name. Build recipients using both positive eligibility requirements.

Minor differences: Python splits time/sky notices into separate sends, omits punctuation from some time notices, and broadcasts an invalid-sky diagnostic rather than only logging the C bug message. These are secondary to the recipient/transition defects.

### char_update: character and NPC hourly tick

C `update.c:607–840`; Python `src/game/UpdateHandler.py:74–102`, `src/game/EntityUpdateHandler.py:35–80`, Character/AnimateEntity model methods and EffectUpdateHandler.

The inspected flow regenerates before condition decay, ticks live link-dead room characters as well as session characters, includes NPCs, and does not tick offline registry-only characters. These behaviors match C's live character list concept. Active players are deduplicated by ID. C's chosen descriptor save bucket becomes a character-ID bucket in Python; both distribute connected-character saves over 30 ticks. The changed bucket key is an implementation difference rather than a gameplay defect.

**P2 — Resources above maximum are never clamped.** C `update.c:643–658` sets hit/mana/move to their maxima in each else branch. Python `src/game/AnimateEntity.py:204–218` only touches resources below maximum. Reproduced HP 40 remaining 40 with max HP 30. Temporary over-max resources can persist indefinitely instead of being corrected on the next eligible tick.

**P2 — Timed effect message suppression has the opposite duration condition.** C `update.c:720–733`; Python `src/item/EffectHandler.py:386–395`. C suppresses the message when the next effect has the same type and duration <= 0, so a contiguous group expiring together yields one notice. Python suppresses when the next duration is > 0. Reproduced same-type durations (0,0) producing two message candidates and (0,5) producing none; C produces one in each case. This defect also affects obj_update through the shared effect ticker. Positive duration decrement, negative permanence, and one-in-five positive-level fading otherwise follow the inspected rules.

**P1 — Periodic damage bypasses combat's typed damage pipeline.** C `update.c:792–819` calls damage with DAM_DISEASE/DAM_POISON/DAM_NONE. Python `src/item/EffectUpdateHandler.py:38–116` calls `CombatHandler.apply_periodic_damage`; that method (`src/combat/CombatHandler.py:2058–2070`) subtracts HP directly and raw-kills. C damage (`fight.c:758–817`) applies drunkenness, sanctuary/protection, immunity/resistance/vulnerability, and the immortal 1-HP floor before position/death handling. For example, a poison-immune victim still loses HP in Python, and a low-HP immortal can die from poison/plague. The helper also discards raw_kill notices instead of passing consequences through the normal emission path. Reuse a quiet typed-damage path; retain skill/spell-owned tick messages.

Plague/poison core formulas and precedence substantially match the inspected nonlethal path: plague level 1 stops before spread/drain, new plague is one level weaker with -5 strength, damage is min(character level, plague level/5+1), mana/movement drain before damage, poison is level/10+1 and is suppressed by slow, incapacitated damage has a 50% roll, and mortally wounded entities take one point. Python checks spread eligibility/chance before saves whereas C rolls saves first, changing random-number consumption; the final spread probability for otherwise equivalent eligible targets is not itself shown incorrect. Death damage remains subject to the pipeline defect above.

**Unresolved behavioral gap — NPC return-home extraction.** C `update.c:634–641` gives uncharmed, unfighting, uncontrolled NPCs outside their origin zone a <5 percent roll (1–4 on a 1–100 roll) to announce wandering home and be extracted. No equivalent origin-zone check/extraction was found in EntityUpdateHandler or other src paths. This can leave wandering NPCs outside their source area indefinitely. Confirm whether this ROM behavior is desired before treating it as an implementation requirement.

**Unresolved behavioral gap — Idle void/autoquit timing.** C `update.c:628–629,681–701,823–836` moves idle players to limbo after 12 ticks and selects an overdue timer >30 for autoquit. Python's separate `ConnectionHandler.py:288–339` uses a socket timeout, sends a void notice, returns and closes the connection; it does not perform the same limbo-room relocation. `SessionHandler.is_session_idle` also compares elapsed seconds with max_idle_time*1000, while receive timeout uses max_idle_time directly. This is a verified unit inconsistency and lifecycle difference, but the intended session-based timeout policy needs confirmation rather than assuming C's descriptor lifecycle is mandatory.

Light fuel countdown/low-fuel messages, mortal/immortal gating, and room light decrement follow the normal inspected path. Python clears the equipped-light slot at burnout (`Character.py:337–357`) instead of using full item extraction; ownership/effect aliases outside that slot are not cleaned up there. Full extraction equivalence remains a focused follow-up, particularly for lights with effects or inventory aliases.

### obj_update: object effects, timers and decay

C `update.c:849–987`; Python `src/item/ItemUpdateHandler.py:27–105` and shared Item/EffectHandler methods. Both tick affects first; timers <=0 do not expire; a positive timer expires when decremented to zero. Shopkeeper credit uses cost/5; fixed-pit suppression, equipped-item detachment and content spill paths exist. Shared affect-message suppression differs as described under char_update.

**P1 — Real player-corpse types fail the preservation branch.** Python `ItemUpdateHandler.py:47–48,79–84` recognizes only the enum name ITEM_CORPSE_PC. The checked collection document for vnum 11 stores `pc_corpse`, preserved by ItemUtil normalization. Consequently is_pc_corpse is false and contents are not moved before the corpse is detached. Reproduced an expiring pc_corpse containing treasure: the room ended empty rather than containing the treasure. C `update.c:951–981` explicitly preserves player-corpse contents. This is item loss, not just wording. Normalize type checks using existing item predicates/aliases.

**P2 — Decay text dispatch rejects ordinary collection item types.** `src/item/Item.py:123–140` maps ITEM_FOOD, ITEM_PORTAL, ITEM_CORPSE_PC, etc., but live documents use names such as food, portal, pc_corpse and npc_corpse. Reproduced all four selecting the generic crumbles-into-dust message. C `update.c:912–935` selects each type's intended decay text. Floating-container text is likewise gated by an unmatched ITEM_CONTAINER string for ordinary container data.

**P2 — Nested object expiration messages leak to the room.** C `update.c:881–899,939–949` emits affect/decay messages only when an object itself has carried_by or in_room; an item in another item has neither. Python `ItemUpdateHandler.py:106–151` uses the enclosing room returned by ownership traversal even for item_contains, so concealed items inside a bag can announce their expiration to room observers. The fixed-pit suppression is not a general nested-container visibility rule. Preserve C's direct ownership distinction unless broader room notices are an intentional product change.

Global C object-list membership is represented by Python's live room/character ownership traversal. That architecture is acceptable. This review did not prove coverage for live objects temporarily outside any room-owned graph; do not infer such objects are safely ticked from prototype registry membership.

### aggr_update: per-pulse aggression

C `update.c:1003–1069`; Python `src/combat/CombatHandler.py:477–497,1608–1667,2042–2056`.

Empty-area, aggressive/safe/calm/charm/awake checks, five-level victim tolerance, wimpy/asleep restriction, reservoir selection, and immediate multi_hit are represented.

**P2 — Aggression retries are reduced to one per room rather than per player witness.** C loops mortal PCs, then room NPCs, with a new number_bits(1) gate per eligible witness until the NPC starts fighting. Python evaluates each aggressor once, using one chosen victim as the witness. With two fully eligible visible PCs and no other blockers, C can attempt twice: 75% chance to start combat that pulse; Python has one 50% chance. Larger parties therefore suppress aggression relative to C. This is an observable probability change, not merely iteration-order variation.

**P2 — Players already fighting another opponent are excluded as victims.** Python `_select_aggressive_victim` at `CombatHandler.py:1650–1652` skips those candidates. C `update.c:1045–1060` has no equivalent exclusion. A free aggressive NPC will decline to join combat against an otherwise eligible player already fighting something else. No established intentional exemption was found for this target-filter change.

### violence_update: scheduled combat boundary

C scheduler `update.c:1108–1112`; implementation `fight.c` violence_update. Python `UpdateHandler.py:67–71`, `CombatHandler.py:1992–2040`. The three-second period and ongoing-combat update call are present; Python refreshes its combat-event registry before dispatch. The relative ordering defect is listed under update_handler. Round execution, combat assistance, and every weapon/offensive action were not re-audited here; no whole-combat parity claim is made.

## Other functions defined in update.c

### hit_gain / mana_gain / move_gain

C `update.c:147–330`; Python `AnimateEntity.py:220–300`, `Character.py:423–514`, `Mobile.py:60–91`. Inspected base player/NPC formulas, integer divisions on normal nonnegative gains, position multipliers, hunger/thirst penalties, room/furniture rates, regeneration flag, poison/plague penalties and haste/slow halving. These match the covered normal inputs, apart from the caller's over-max clamp omission. Furniture rates use value3 for HP/movement and value4 for mana, as C does.

Fast-healing/meditation improvement invokes the LearningService defects already documented in [skills.c report](skills-c-rom24-parity-2026-10-24.md). Python uses raw learned percentages in these regeneration helpers, whereas C uses get_skill. In C, get_skill also enforces class level availability and daze/drunk scaling (`handler.c`); those adjustments are not present in `Character._skill_percent`. Thus identical learned records can grant regeneration bonuses in Python when C would reduce/disallow them. Treat this as a P2 integration mismatch rather than a base formula discrepancy.

### gain_condition

C `update.c:333–370`; Python `Character.py:327–335,359–387`. Covered zero-change/NPC/immortal/disabled gates, clamp 0–48, sober notice only when transitioning from nonzero, hunger/thirst warnings at zero, and separate fullness/hunger decay with large-race scaling. No mismatch found in those inspected branches. Conditions remain designer-compatible runtime state; no content rewrite is required for parity.

### advance_level / gain_exp

C `update.c:61–140`; Python `src/player/CharacterAdvancement.py:46–181`. Inspected growth draws, 90% scaling, HP/mana minimum 2, movement minimum 6, class mana halving, practice award, train +1, hero gating and title update. Normal covered growth arithmetic matches. Python represents within-level and accumulated XP separately, which is not itself a defect.

Differences: C recalculates XP cost from points each award; Python uses a cached requirement (see gain-points defect in skills.c report). C's minimum total XP floor is one exp_per_level, while Python clamps accumulated XP to zero. C saves immediately and announces level gains to WIZ_LEVELS; Python's helper returns a result without either side effect, relying on callers and later autosave. No equivalent level-up save/wiznet emission was found in the inspected advancement path. C's last_level and permanent HP/mana/movement bookkeeping are absent from the inspected Python model; their downstream product requirements were not established here. Full character persistence/service integration was not executed.

## Validation and scope limits

Used collection-query for pulse configuration, corpse types and plague payloads; content-owned periodic messages are present and were not mistaken for missing hard-coded text. Existing local repository instructions and rom24-parity skill were followed. The C checkout was not modified.

Focused suites ran separately to avoid process-global fixture collisions:

| Suite | Passed |
| --- | ---: |
| tests.test_update_handler_active_players | 24 |
| tests.test_fullness_hunger_parity | 14 |
| tests.test_combat_handler_aggression | 69 |
| tests.test_object_design_contracts | 9 |
| tests.test_mobile_special_binding | 4 |
| Total | 120 |

Additional isolated production-code checks reproduced the three weather transition errors, over-max HP remaining unchanged, shared effect-message inversion, ordinary item-type decay fallback, and player-corpse content loss. Async checks ran outside the sandbox because Windows asyncio socketpair initialization is blocked inside it. One initial over-max reproduction used an incomplete RNG mock and failed in unrelated mana regeneration; the corrected check filled the other resources and reproduced the HP defect.

Existing tests are not evidence of full parity: some construct enum-name item types instead of actual collection aliases, and they do not assert all order/recipient/probability rules above. No new regression tests or fixes were committed as part of this review. No live server run, C executable differential run, exhaustive area reset audit, full music migration review or full violence_update audit was performed. Intent remains unresolved for music, idle policy, and NPC home extraction; these should not be silently implemented as product decisions.

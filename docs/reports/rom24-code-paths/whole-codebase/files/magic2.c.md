# src/magic2.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `f3f11b1edf2391671685e0d710e9d15d9a0706bae104afd92cda23d3b1d05169`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## spell_farsight

[Source line 44](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic2.c:44); ends at line 53. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/const.c:1329` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/magic.h:79` (declaration_or_dispatch_reference).

Dependencies: `IS_AFFECTED`, `send_to_char`, `do_function`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `magic2.spell_farsight.if.001` | 46 | `if (IS_AFFECTED(ch,AFF_BLIND))` | magic2.spell_farsight.blind-rejects-before-scan, magic2.spell_farsight.delegates-raw-target-name | specified |
| `magic2.spell_farsight.return.001` | 49 | `return;` | magic2.spell_farsight.blind-rejects-before-scan | specified |
| `magic2.spell_farsight.blind-rejects-before-scan.path` | 46 | `blind rejects before scan` | magic2.spell_farsight.blind-rejects-before-scan | specified |
| `magic2.spell_farsight.delegates-raw-target-name.path` | 52 | `delegates raw target name` | magic2.spell_farsight.delegates-raw-target-name | specified |

## spell_portal

[Source line 56](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic2.c:56); ends at line 103. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/const.c:1520` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/magic.h:106` (declaration_or_dispatch_reference).

Dependencies: `get_char_world`, `can_see_room`, `IS_SET`, `IS_NPC`, `saves_spell`, `is_clan`, `is_same_clan`, `send_to_char`, `get_eq_char`, `IS_IMMORTAL`, `act`, `extract_obj`, `create_object`, `get_obj_index`, `obj_to_room`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `magic2.spell_portal.if.001` | 61 | `if ( ( victim = get_char_world( ch, target_name ) ) == NULL     \|\|   victim == ch     \|\|   victim->in_room == NULL     \|\|   !can_see_room(ch,victim->in_room)     \|\|   IS_SET(victim->in_room->room_flags, ROOM_SAFE)     \|\|   IS_SET(victim->in_room->room_flags, ROOM_PRIVATE)     \|\|   IS_SET(victim->in_room->room_flags, ROOM_SOLITARY)     \|\|   IS_SET(victim->in_room->room_flags, ROOM_NO_RECALL)     \|\|   IS_SET(ch->in_room->room_flags, ROOM_NO_RECALL)     \|\|   victim->level >= level + 3     \|\|   (!IS_NPC(victim) && victim->level >= LEVEL_HERO)  /* NOT trust */     \|\|   (IS_NPC(victim) && IS_SET(victim->imm_flags,IMM_SUMMON))     \|\|   (IS_NPC(victim) && saves_spell( level, victim,DAM_NONE) )      \|\|	(is_clan(victim) && !is_same_clan(ch,victim)))` | magic2.spell_portal.no-victim, magic2.spell_portal.self-target, magic2.spell_portal.victim-no-room, magic2.spell_portal.room-not-visible, magic2.spell_portal.destination-safe, magic2.spell_portal.destination-private, magic2.spell_portal.destination-solitary, magic2.spell_portal.destination-no-recall, magic2.spell_portal.origin-no-recall, magic2.spell_portal.victim-level-at-spell-plus-three, magic2.spell_portal.hero-pc-regardless-of-trust, magic2.spell_portal.npc-summon-immune, magic2.spell_portal.npc-saves, magic2.spell_portal.clan-mismatch, magic2.spell_portal.mortal-no-component, magic2.spell_portal.mortal-wrong-component, magic2.spell_portal.immortal-no-component, magic2.spell_portal.immortal-wrong-component, magic2.spell_portal.success-level-24, magic2.spell_portal.success-level-25, magic2.spell_portal.success-level-49, magic2.spell_portal.success-level-50 | specified |
| `magic2.spell_portal.or.001` | 62 | `\|\|   victim == ch` | magic2.spell_portal.self-target | specified |
| `magic2.spell_portal.or.002` | 63 | `\|\|   victim->in_room == NULL` | magic2.spell_portal.victim-no-room | specified |
| `magic2.spell_portal.or.003` | 64 | `\|\|   !can_see_room(ch,victim->in_room)` | magic2.spell_portal.room-not-visible | specified |
| `magic2.spell_portal.or.004` | 65 | `\|\|   IS_SET(victim->in_room->room_flags, ROOM_SAFE)` | magic2.spell_portal.destination-safe | specified |
| `magic2.spell_portal.or.005` | 66 | `\|\|   IS_SET(victim->in_room->room_flags, ROOM_PRIVATE)` | magic2.spell_portal.destination-private | specified |
| `magic2.spell_portal.or.006` | 67 | `\|\|   IS_SET(victim->in_room->room_flags, ROOM_SOLITARY)` | magic2.spell_portal.destination-solitary | specified |
| `magic2.spell_portal.or.007` | 68 | `\|\|   IS_SET(victim->in_room->room_flags, ROOM_NO_RECALL)` | magic2.spell_portal.destination-no-recall | specified |
| `magic2.spell_portal.or.008` | 69 | `\|\|   IS_SET(ch->in_room->room_flags, ROOM_NO_RECALL)` | magic2.spell_portal.origin-no-recall | specified |
| `magic2.spell_portal.or.009` | 70 | `\|\|   victim->level >= level + 3` | magic2.spell_portal.victim-level-at-spell-plus-three | specified |
| `magic2.spell_portal.or.010` | 71 | `\|\|   (!IS_NPC(victim) && victim->level >= LEVEL_HERO)  /* NOT trust */` | magic2.spell_portal.hero-pc-regardless-of-trust | specified |
| `magic2.spell_portal.and.001` | 71 | `&& victim->level >= LEVEL_HERO)  /* NOT trust */` | magic2.spell_portal.hero-pc-regardless-of-trust | specified |
| `magic2.spell_portal.or.011` | 72 | `\|\|   (IS_NPC(victim) && IS_SET(victim->imm_flags,IMM_SUMMON))` | magic2.spell_portal.npc-summon-immune | specified |
| `magic2.spell_portal.and.002` | 72 | `&& IS_SET(victim->imm_flags,IMM_SUMMON))` | magic2.spell_portal.npc-summon-immune | specified |
| `magic2.spell_portal.or.012` | 73 | `\|\|   (IS_NPC(victim) && saves_spell( level, victim,DAM_NONE) )` | magic2.spell_portal.npc-saves | specified |
| `magic2.spell_portal.and.003` | 73 | `&& saves_spell( level, victim,DAM_NONE) )` | magic2.spell_portal.npc-saves | specified |
| `magic2.spell_portal.or.013` | 74 | `\|\|	(is_clan(victim) && !is_same_clan(ch,victim)))` | magic2.spell_portal.clan-mismatch | specified |
| `magic2.spell_portal.and.004` | 74 | `&& !is_same_clan(ch,victim)))` | magic2.spell_portal.clan-mismatch | specified |
| `magic2.spell_portal.return.001` | 77 | `return;` | magic2.spell_portal.no-victim, magic2.spell_portal.self-target, magic2.spell_portal.victim-no-room, magic2.spell_portal.room-not-visible, magic2.spell_portal.destination-safe, magic2.spell_portal.destination-private, magic2.spell_portal.destination-solitary, magic2.spell_portal.destination-no-recall, magic2.spell_portal.origin-no-recall, magic2.spell_portal.victim-level-at-spell-plus-three, magic2.spell_portal.hero-pc-regardless-of-trust, magic2.spell_portal.npc-summon-immune, magic2.spell_portal.npc-saves, magic2.spell_portal.clan-mismatch | specified |
| `magic2.spell_portal.if.002` | 81 | `if (!IS_IMMORTAL(ch)      &&  (stone == NULL \|\| stone->item_type != ITEM_WARP_STONE))` | magic2.spell_portal.mortal-no-component, magic2.spell_portal.mortal-wrong-component, magic2.spell_portal.immortal-no-component, magic2.spell_portal.immortal-wrong-component, magic2.spell_portal.success-level-24, magic2.spell_portal.success-level-25, magic2.spell_portal.success-level-49, magic2.spell_portal.success-level-50 | specified |
| `magic2.spell_portal.and.005` | 82 | `&&  (stone == NULL \|\| stone->item_type != ITEM_WARP_STONE))` | magic2.spell_portal.mortal-no-component, magic2.spell_portal.mortal-wrong-component, magic2.spell_portal.immortal-no-component, magic2.spell_portal.immortal-wrong-component, magic2.spell_portal.success-level-24, magic2.spell_portal.success-level-25, magic2.spell_portal.success-level-49, magic2.spell_portal.success-level-50 | specified |
| `magic2.spell_portal.or.014` | 82 | `\|\| stone->item_type != ITEM_WARP_STONE))` | magic2.spell_portal.mortal-no-component, magic2.spell_portal.mortal-wrong-component | specified |
| `magic2.spell_portal.return.002` | 85 | `return;` | magic2.spell_portal.mortal-no-component, magic2.spell_portal.mortal-wrong-component | specified |
| `magic2.spell_portal.if.003` | 88 | `if (stone != NULL && stone->item_type == ITEM_WARP_STONE)` | magic2.spell_portal.immortal-no-component, magic2.spell_portal.immortal-wrong-component, magic2.spell_portal.success-level-24, magic2.spell_portal.success-level-25, magic2.spell_portal.success-level-49, magic2.spell_portal.success-level-50 | specified |
| `magic2.spell_portal.and.006` | 88 | `&& stone->item_type == ITEM_WARP_STONE)` | magic2.spell_portal.immortal-no-component, magic2.spell_portal.immortal-wrong-component, magic2.spell_portal.success-level-24, magic2.spell_portal.success-level-25, magic2.spell_portal.success-level-49, magic2.spell_portal.success-level-50 | specified |
| `magic2.spell_portal.no-victim.path` | 61 | `no victim` | magic2.spell_portal.no-victim | specified |
| `magic2.spell_portal.self-target.path` | 61 | `self target` | magic2.spell_portal.self-target | specified |
| `magic2.spell_portal.victim-no-room.path` | 61 | `victim no room` | magic2.spell_portal.victim-no-room | specified |
| `magic2.spell_portal.room-not-visible.path` | 61 | `room not visible` | magic2.spell_portal.room-not-visible | specified |
| `magic2.spell_portal.destination-safe.path` | 61 | `destination safe` | magic2.spell_portal.destination-safe | specified |
| `magic2.spell_portal.destination-private.path` | 61 | `destination private` | magic2.spell_portal.destination-private | specified |
| `magic2.spell_portal.destination-solitary.path` | 61 | `destination solitary` | magic2.spell_portal.destination-solitary | specified |
| `magic2.spell_portal.destination-no-recall.path` | 61 | `destination no recall` | magic2.spell_portal.destination-no-recall | specified |
| `magic2.spell_portal.origin-no-recall.path` | 61 | `origin no recall` | magic2.spell_portal.origin-no-recall | specified |
| `magic2.spell_portal.victim-level-at-spell-plus-three.path` | 61 | `victim level at spell plus three` | magic2.spell_portal.victim-level-at-spell-plus-three | specified |
| `magic2.spell_portal.hero-pc-regardless-of-trust.path` | 61 | `hero pc regardless of trust` | magic2.spell_portal.hero-pc-regardless-of-trust | specified |
| `magic2.spell_portal.npc-summon-immune.path` | 61 | `npc summon immune` | magic2.spell_portal.npc-summon-immune | specified |
| `magic2.spell_portal.npc-saves.path` | 61 | `npc saves` | magic2.spell_portal.npc-saves | specified |
| `magic2.spell_portal.clan-mismatch.path` | 61 | `clan mismatch` | magic2.spell_portal.clan-mismatch | specified |
| `magic2.spell_portal.mortal-no-component.path` | 80 | `mortal no component` | magic2.spell_portal.mortal-no-component | specified |
| `magic2.spell_portal.mortal-wrong-component.path` | 80 | `mortal wrong component` | magic2.spell_portal.mortal-wrong-component | specified |
| `magic2.spell_portal.immortal-no-component.path` | 80 | `immortal no component` | magic2.spell_portal.immortal-no-component | specified |
| `magic2.spell_portal.immortal-wrong-component.path` | 80 | `immortal wrong component` | magic2.spell_portal.immortal-wrong-component | specified |
| `magic2.spell_portal.success-level-24.path` | 96 | `success level 24` | magic2.spell_portal.success-level-24 | specified |
| `magic2.spell_portal.success-level-25.path` | 96 | `success level 25` | magic2.spell_portal.success-level-25 | specified |
| `magic2.spell_portal.success-level-49.path` | 96 | `success level 49` | magic2.spell_portal.success-level-49 | specified |
| `magic2.spell_portal.success-level-50.path` | 96 | `success level 50` | magic2.spell_portal.success-level-50 | specified |

## spell_nexus

[Source line 105](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic2.c:105); ends at line 174. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/const.c:1491` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/magic.h:102` (declaration_or_dispatch_reference).

Dependencies: `get_char_world`, `can_see_room`, `IS_SET`, `IS_NPC`, `saves_spell`, `is_clan`, `is_same_clan`, `send_to_char`, `get_eq_char`, `IS_IMMORTAL`, `act`, `extract_obj`, `create_object`, `get_obj_index`, `obj_to_room`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `magic2.spell_nexus.if.001` | 113 | `if ( ( victim = get_char_world( ch, target_name ) ) == NULL     \|\|   victim == ch     \|\|   (to_room = victim->in_room) == NULL     \|\|   !can_see_room(ch,to_room) \|\| !can_see_room(ch,from_room)     \|\|   IS_SET(to_room->room_flags, ROOM_SAFE)     \|\|	 IS_SET(from_room->room_flags,ROOM_SAFE)     \|\|   IS_SET(to_room->room_flags, ROOM_PRIVATE)     \|\|   IS_SET(to_room->room_flags, ROOM_SOLITARY)     \|\|   IS_SET(to_room->room_flags, ROOM_NO_RECALL)     \|\|   IS_SET(from_room->room_flags,ROOM_NO_RECALL)     \|\|   victim->level >= level + 3     \|\|   (!IS_NPC(victim) && victim->level >= LEVEL_HERO)  /* NOT trust */     \|\|   (IS_NPC(victim) && IS_SET(victim->imm_flags,IMM_SUMMON))     \|\|   (IS_NPC(victim) && saves_spell( level, victim,DAM_NONE) )      \|\|	 (is_clan(victim) && !is_same_clan(ch,victim)))` | magic2.spell_nexus.no-victim, magic2.spell_nexus.self-target, magic2.spell_nexus.victim-no-room, magic2.spell_nexus.room-not-visible, magic2.spell_nexus.destination-safe, magic2.spell_nexus.destination-private, magic2.spell_nexus.destination-solitary, magic2.spell_nexus.destination-no-recall, magic2.spell_nexus.origin-no-recall, magic2.spell_nexus.victim-level-at-spell-plus-three, magic2.spell_nexus.hero-pc-regardless-of-trust, magic2.spell_nexus.npc-summon-immune, magic2.spell_nexus.npc-saves, magic2.spell_nexus.clan-mismatch, magic2.spell_nexus.mortal-no-component, magic2.spell_nexus.mortal-wrong-component, magic2.spell_nexus.immortal-no-component, magic2.spell_nexus.immortal-wrong-component, magic2.spell_nexus.success-level-9, magic2.spell_nexus.success-level-10, magic2.spell_nexus.success-level-19, magic2.spell_nexus.success-level-20, magic2.spell_nexus.same-room-one-portal, magic2.spell_nexus.safe-origin-denies, magic2.spell_nexus.origin-invisible-after-visible-destination, magic2.spell_nexus.empty-destination-people-skips-announcements | specified |
| `magic2.spell_nexus.or.001` | 114 | `\|\|   victim == ch` | magic2.spell_nexus.self-target | specified |
| `magic2.spell_nexus.or.002` | 115 | `\|\|   (to_room = victim->in_room) == NULL` | magic2.spell_nexus.victim-no-room | specified |
| `magic2.spell_nexus.or.003` | 116 | `\|\|   !can_see_room(ch,to_room) \|\| !can_see_room(ch,from_room)` | magic2.spell_nexus.room-not-visible | specified |
| `magic2.spell_nexus.or.004` | 116 | `\|\| !can_see_room(ch,from_room)` | magic2.spell_nexus.origin-invisible-after-visible-destination | specified |
| `magic2.spell_nexus.or.005` | 117 | `\|\|   IS_SET(to_room->room_flags, ROOM_SAFE)` | magic2.spell_nexus.destination-safe | specified |
| `magic2.spell_nexus.or.006` | 118 | `\|\|	 IS_SET(from_room->room_flags,ROOM_SAFE)` | magic2.spell_nexus.safe-origin-denies | specified |
| `magic2.spell_nexus.or.007` | 119 | `\|\|   IS_SET(to_room->room_flags, ROOM_PRIVATE)` | magic2.spell_nexus.destination-private | specified |
| `magic2.spell_nexus.or.008` | 120 | `\|\|   IS_SET(to_room->room_flags, ROOM_SOLITARY)` | magic2.spell_nexus.destination-solitary | specified |
| `magic2.spell_nexus.or.009` | 121 | `\|\|   IS_SET(to_room->room_flags, ROOM_NO_RECALL)` | magic2.spell_nexus.destination-no-recall | specified |
| `magic2.spell_nexus.or.010` | 122 | `\|\|   IS_SET(from_room->room_flags,ROOM_NO_RECALL)` | magic2.spell_nexus.origin-no-recall | specified |
| `magic2.spell_nexus.or.011` | 123 | `\|\|   victim->level >= level + 3` | magic2.spell_nexus.victim-level-at-spell-plus-three | specified |
| `magic2.spell_nexus.or.012` | 124 | `\|\|   (!IS_NPC(victim) && victim->level >= LEVEL_HERO)  /* NOT trust */` | magic2.spell_nexus.hero-pc-regardless-of-trust | specified |
| `magic2.spell_nexus.and.001` | 124 | `&& victim->level >= LEVEL_HERO)  /* NOT trust */` | magic2.spell_nexus.hero-pc-regardless-of-trust | specified |
| `magic2.spell_nexus.or.013` | 125 | `\|\|   (IS_NPC(victim) && IS_SET(victim->imm_flags,IMM_SUMMON))` | magic2.spell_nexus.npc-summon-immune | specified |
| `magic2.spell_nexus.and.002` | 125 | `&& IS_SET(victim->imm_flags,IMM_SUMMON))` | magic2.spell_nexus.npc-summon-immune | specified |
| `magic2.spell_nexus.or.014` | 126 | `\|\|   (IS_NPC(victim) && saves_spell( level, victim,DAM_NONE) )` | magic2.spell_nexus.npc-saves | specified |
| `magic2.spell_nexus.and.003` | 126 | `&& saves_spell( level, victim,DAM_NONE) )` | magic2.spell_nexus.npc-saves | specified |
| `magic2.spell_nexus.or.015` | 127 | `\|\|	 (is_clan(victim) && !is_same_clan(ch,victim)))` | magic2.spell_nexus.clan-mismatch | specified |
| `magic2.spell_nexus.and.004` | 127 | `&& !is_same_clan(ch,victim)))` | magic2.spell_nexus.clan-mismatch | specified |
| `magic2.spell_nexus.return.001` | 130 | `return;` | magic2.spell_nexus.no-victim, magic2.spell_nexus.self-target, magic2.spell_nexus.victim-no-room, magic2.spell_nexus.room-not-visible, magic2.spell_nexus.destination-safe, magic2.spell_nexus.destination-private, magic2.spell_nexus.destination-solitary, magic2.spell_nexus.destination-no-recall, magic2.spell_nexus.origin-no-recall, magic2.spell_nexus.victim-level-at-spell-plus-three, magic2.spell_nexus.hero-pc-regardless-of-trust, magic2.spell_nexus.npc-summon-immune, magic2.spell_nexus.npc-saves, magic2.spell_nexus.clan-mismatch, magic2.spell_nexus.safe-origin-denies, magic2.spell_nexus.origin-invisible-after-visible-destination | specified |
| `magic2.spell_nexus.if.002` | 134 | `if (!IS_IMMORTAL(ch)     &&  (stone == NULL \|\| stone->item_type != ITEM_WARP_STONE))` | magic2.spell_nexus.mortal-no-component, magic2.spell_nexus.mortal-wrong-component, magic2.spell_nexus.immortal-no-component, magic2.spell_nexus.immortal-wrong-component, magic2.spell_nexus.success-level-9, magic2.spell_nexus.success-level-10, magic2.spell_nexus.success-level-19, magic2.spell_nexus.success-level-20, magic2.spell_nexus.same-room-one-portal, magic2.spell_nexus.empty-destination-people-skips-announcements | specified |
| `magic2.spell_nexus.and.005` | 135 | `&&  (stone == NULL \|\| stone->item_type != ITEM_WARP_STONE))` | magic2.spell_nexus.mortal-no-component, magic2.spell_nexus.mortal-wrong-component, magic2.spell_nexus.immortal-no-component, magic2.spell_nexus.immortal-wrong-component, magic2.spell_nexus.success-level-9, magic2.spell_nexus.success-level-10, magic2.spell_nexus.success-level-19, magic2.spell_nexus.success-level-20, magic2.spell_nexus.same-room-one-portal, magic2.spell_nexus.empty-destination-people-skips-announcements | specified |
| `magic2.spell_nexus.or.016` | 135 | `\|\| stone->item_type != ITEM_WARP_STONE))` | magic2.spell_nexus.mortal-no-component, magic2.spell_nexus.mortal-wrong-component | specified |
| `magic2.spell_nexus.return.002` | 138 | `return;` | magic2.spell_nexus.mortal-no-component, magic2.spell_nexus.mortal-wrong-component | specified |
| `magic2.spell_nexus.if.003` | 141 | `if (stone != NULL && stone->item_type == ITEM_WARP_STONE)` | magic2.spell_nexus.immortal-no-component, magic2.spell_nexus.immortal-wrong-component, magic2.spell_nexus.success-level-9, magic2.spell_nexus.success-level-10, magic2.spell_nexus.success-level-19, magic2.spell_nexus.success-level-20, magic2.spell_nexus.same-room-one-portal, magic2.spell_nexus.empty-destination-people-skips-announcements | specified |
| `magic2.spell_nexus.and.006` | 141 | `&& stone->item_type == ITEM_WARP_STONE)` | magic2.spell_nexus.immortal-no-component, magic2.spell_nexus.immortal-wrong-component, magic2.spell_nexus.success-level-9, magic2.spell_nexus.success-level-10, magic2.spell_nexus.success-level-19, magic2.spell_nexus.success-level-20, magic2.spell_nexus.same-room-one-portal, magic2.spell_nexus.empty-destination-people-skips-announcements | specified |
| `magic2.spell_nexus.if.004` | 159 | `if (to_room == from_room)` | magic2.spell_nexus.immortal-no-component, magic2.spell_nexus.immortal-wrong-component, magic2.spell_nexus.success-level-9, magic2.spell_nexus.success-level-10, magic2.spell_nexus.success-level-19, magic2.spell_nexus.success-level-20, magic2.spell_nexus.same-room-one-portal, magic2.spell_nexus.empty-destination-people-skips-announcements | specified |
| `magic2.spell_nexus.return.003` | 160 | `return;` | magic2.spell_nexus.same-room-one-portal | specified |
| `magic2.spell_nexus.if.005` | 169 | `if (to_room->people != NULL)` | magic2.spell_nexus.immortal-no-component, magic2.spell_nexus.immortal-wrong-component, magic2.spell_nexus.success-level-9, magic2.spell_nexus.success-level-10, magic2.spell_nexus.success-level-19, magic2.spell_nexus.success-level-20, magic2.spell_nexus.empty-destination-people-skips-announcements | specified |
| `magic2.spell_nexus.no-victim.path` | 113 | `no victim` | magic2.spell_nexus.no-victim | specified |
| `magic2.spell_nexus.self-target.path` | 113 | `self target` | magic2.spell_nexus.self-target | specified |
| `magic2.spell_nexus.victim-no-room.path` | 113 | `victim no room` | magic2.spell_nexus.victim-no-room | specified |
| `magic2.spell_nexus.room-not-visible.path` | 113 | `room not visible` | magic2.spell_nexus.room-not-visible | specified |
| `magic2.spell_nexus.destination-safe.path` | 113 | `destination safe` | magic2.spell_nexus.destination-safe | specified |
| `magic2.spell_nexus.destination-private.path` | 113 | `destination private` | magic2.spell_nexus.destination-private | specified |
| `magic2.spell_nexus.destination-solitary.path` | 113 | `destination solitary` | magic2.spell_nexus.destination-solitary | specified |
| `magic2.spell_nexus.destination-no-recall.path` | 113 | `destination no recall` | magic2.spell_nexus.destination-no-recall | specified |
| `magic2.spell_nexus.origin-no-recall.path` | 113 | `origin no recall` | magic2.spell_nexus.origin-no-recall | specified |
| `magic2.spell_nexus.victim-level-at-spell-plus-three.path` | 113 | `victim level at spell plus three` | magic2.spell_nexus.victim-level-at-spell-plus-three | specified |
| `magic2.spell_nexus.hero-pc-regardless-of-trust.path` | 113 | `hero pc regardless of trust` | magic2.spell_nexus.hero-pc-regardless-of-trust | specified |
| `magic2.spell_nexus.npc-summon-immune.path` | 113 | `npc summon immune` | magic2.spell_nexus.npc-summon-immune | specified |
| `magic2.spell_nexus.npc-saves.path` | 113 | `npc saves` | magic2.spell_nexus.npc-saves | specified |
| `magic2.spell_nexus.clan-mismatch.path` | 113 | `clan mismatch` | magic2.spell_nexus.clan-mismatch | specified |
| `magic2.spell_nexus.mortal-no-component.path` | 133 | `mortal no component` | magic2.spell_nexus.mortal-no-component | specified |
| `magic2.spell_nexus.mortal-wrong-component.path` | 133 | `mortal wrong component` | magic2.spell_nexus.mortal-wrong-component | specified |
| `magic2.spell_nexus.immortal-no-component.path` | 133 | `immortal no component` | magic2.spell_nexus.immortal-no-component | specified |
| `magic2.spell_nexus.immortal-wrong-component.path` | 133 | `immortal wrong component` | magic2.spell_nexus.immortal-wrong-component | specified |
| `magic2.spell_nexus.success-level-9.path` | 150 | `success level 9` | magic2.spell_nexus.success-level-9 | specified |
| `magic2.spell_nexus.success-level-10.path` | 150 | `success level 10` | magic2.spell_nexus.success-level-10 | specified |
| `magic2.spell_nexus.success-level-19.path` | 150 | `success level 19` | magic2.spell_nexus.success-level-19 | specified |
| `magic2.spell_nexus.success-level-20.path` | 150 | `success level 20` | magic2.spell_nexus.success-level-20 | specified |
| `magic2.spell_nexus.same-room-one-portal.path` | 159 | `same room one portal` | magic2.spell_nexus.same-room-one-portal | specified |
| `magic2.spell_nexus.safe-origin-denies.path` | 118 | `safe origin denies` | magic2.spell_nexus.safe-origin-denies | specified |
| `magic2.spell_nexus.origin-invisible-after-visible-destination.path` | 116 | `origin invisible after visible destination` | magic2.spell_nexus.origin-invisible-after-visible-destination | specified |
| `magic2.spell_nexus.empty-destination-people-skips-announcements.path` | 169 | `empty destination people skips announcements` | magic2.spell_nexus.empty-destination-people-skips-announcements | specified |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#endif` — pending configuration/reachability review.
- Line 33: `#include <stdio.h>` — pending configuration/reachability review.
- Line 34: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 35: `#include <string.h>` — pending configuration/reachability review.
- Line 36: `#include <time.h>` — pending configuration/reachability review.
- Line 37: `#include "merc.h"` — pending configuration/reachability review.
- Line 38: `#include "interp.h"` — pending configuration/reachability review.
- Line 39: `#include "magic.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


# src/act_enter.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `3eb4a58d9ab2cf52f14f0e5f6ab11b860a321df08888b34f7ab26cfa95693054`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## get_random_room

[Source line 42](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_enter.c:42); ends at line 61. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:105` (lexical_call_candidate).
- do_enter: `src/act_enter.c:109` (lexical_call_candidate).
- spell_teleport: `src/magic.c:4368` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2079` (declaration_or_dispatch_reference).

Dependencies: `get_room_index`, `number_range`, `can_see_room`, `room_is_private`, `IS_SET`, `IS_NPC`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_enter.get_random_room.for.001` | 46 | `for ( ; ; )` |  | pending |
| `act_enter.get_random_room.if.001` | 49 | `if ( room != NULL )` |  | pending |
| `act_enter.get_random_room.if.002` | 50 | `if ( can_see_room(ch,room) 	&&   !room_is_private(room)         &&   !IS_SET(room->room_flags, ROOM_PRIVATE)         &&   !IS_SET(room->room_flags, ROOM_SOLITARY)  	&&   !IS_SET(room->room_flags, ROOM_SAFE)  	&&   (IS_NPC(ch) \|\| IS_SET(ch->act,ACT_AGGRESSIVE)  	\|\|   !IS_SET(room->room_flags,ROOM_LAW)))` |  | pending |
| `act_enter.get_random_room.and.001` | 51 | `&&   !room_is_private(room)` |  | pending |
| `act_enter.get_random_room.and.002` | 52 | `&&   !IS_SET(room->room_flags, ROOM_PRIVATE)` |  | pending |
| `act_enter.get_random_room.and.003` | 53 | `&&   !IS_SET(room->room_flags, ROOM_SOLITARY)` |  | pending |
| `act_enter.get_random_room.and.004` | 54 | `&&   !IS_SET(room->room_flags, ROOM_SAFE)` |  | pending |
| `act_enter.get_random_room.and.005` | 55 | `&&   (IS_NPC(ch) \|\| IS_SET(ch->act,ACT_AGGRESSIVE)` |  | pending |
| `act_enter.get_random_room.or.001` | 55 | `\|\| IS_SET(ch->act,ACT_AGGRESSIVE)` |  | pending |
| `act_enter.get_random_room.or.002` | 56 | `\|\|   !IS_SET(room->room_flags,ROOM_LAW)))` |  | pending |
| `act_enter.get_random_room.break.001` | 57 | `break;` |  | pending |
| `act_enter.get_random_room.return.001` | 60 | `return room;` |  | pending |
| `act_enter.get_random_room.reject-missing-index.path` | 48 | `reject missing index` | act_enter.get_random_room.reject-missing-index | specified |
| `act_enter.get_random_room.reject-invisible.path` | 48 | `reject invisible` | act_enter.get_random_room.reject-invisible | specified |
| `act_enter.get_random_room.reject-private-helper.path` | 48 | `reject private helper` | act_enter.get_random_room.reject-private-helper | specified |
| `act_enter.get_random_room.reject-private-flag.path` | 48 | `reject private flag` | act_enter.get_random_room.reject-private-flag | specified |
| `act_enter.get_random_room.reject-solitary-flag.path` | 48 | `reject solitary flag` | act_enter.get_random_room.reject-solitary-flag | specified |
| `act_enter.get_random_room.reject-safe-flag.path` | 48 | `reject safe flag` | act_enter.get_random_room.reject-safe-flag | specified |
| `act_enter.get_random_room.reject-law-denies-ordinary-pc.path` | 48 | `reject law denies ordinary pc` | act_enter.get_random_room.reject-law-denies-ordinary-pc | specified |
| `act_enter.get_random_room.npc-law-allowed-even-aggressive.path` | 55 | `npc law allowed even aggressive` | act_enter.get_random_room.npc-law-allowed-even-aggressive | specified |
| `act_enter.get_random_room.pc-aggressive-bit-law-allowed.path` | 55 | `pc aggressive bit law allowed` | act_enter.get_random_room.pc-aggressive-bit-law-allowed | specified |
| `act_enter.get_random_room.ordinary-room-first-draw.path` | 55 | `ordinary room first draw` | act_enter.get_random_room.ordinary-room-first-draw | specified |

## do_enter

[Source line 64](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_enter.c:64); ends at line 214. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:191` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:254` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:257` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:124` (declaration_or_dispatch_reference).

Dependencies: `get_obj_list`, `send_to_char`, `IS_SET`, `IS_TRUSTED`, `IS_AFFECTED`, `get_random_room`, `number_percent`, `get_room_index`, `can_see_room`, `room_is_private`, `act`, `IS_NPC`, `char_from_room`, `char_to_room`, `obj_from_room`, `obj_to_room`, `do_function`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_enter.do_enter.if.001` | 68 | `if ( ch->fighting != NULL )` |  | pending |
| `act_enter.do_enter.return.001` | 69 | `return;` |  | pending |
| `act_enter.do_enter.if.002` | 72 | `if (argument[0] != '\0')` |  | pending |
| `act_enter.do_enter.if.003` | 82 | `if (portal == NULL)` |  | pending |
| `act_enter.do_enter.return.002` | 85 | `return;` |  | pending |
| `act_enter.do_enter.if.004` | 88 | `if (portal->item_type != ITEM_PORTAL          \|\|  (IS_SET(portal->value[1],EX_CLOSED) && !IS_TRUSTED(ch,ANGEL)))` |  | pending |
| `act_enter.do_enter.or.001` | 89 | `\|\|  (IS_SET(portal->value[1],EX_CLOSED) && !IS_TRUSTED(ch,ANGEL)))` |  | pending |
| `act_enter.do_enter.and.001` | 89 | `&& !IS_TRUSTED(ch,ANGEL)))` |  | pending |
| `act_enter.do_enter.return.003` | 92 | `return;` |  | pending |
| `act_enter.do_enter.if.005` | 95 | `if (!IS_TRUSTED(ch,ANGEL) && !IS_SET(portal->value[2],GATE_NOCURSE) 	&&  (IS_AFFECTED(ch,AFF_CURSE)  	\|\|   IS_SET(old_room->room_flags,ROOM_NO_RECALL)))` |  | pending |
| `act_enter.do_enter.and.002` | 95 | `&& !IS_SET(portal->value[2],GATE_NOCURSE)` |  | pending |
| `act_enter.do_enter.and.003` | 96 | `&&  (IS_AFFECTED(ch,AFF_CURSE)` |  | pending |
| `act_enter.do_enter.or.002` | 97 | `\|\|   IS_SET(old_room->room_flags,ROOM_NO_RECALL)))` |  | pending |
| `act_enter.do_enter.return.004` | 100 | `return;` |  | pending |
| `act_enter.do_enter.if.006` | 103 | `if (IS_SET(portal->value[2],GATE_RANDOM) \|\| portal->value[3] == -1)` |  | pending |
| `act_enter.do_enter.or.003` | 103 | `\|\| portal->value[3] == -1)` |  | pending |
| `act_enter.do_enter.if.007` | 108 | `if (IS_SET(portal->value[2],GATE_BUGGY) && (number_percent() < 5))` |  | pending |
| `act_enter.do_enter.and.004` | 108 | `&& (number_percent() < 5))` |  | pending |
| `act_enter.do_enter.if.008` | 113 | `if (location == NULL 	\|\|  location == old_room 	\|\|  !can_see_room(ch,location)  	\|\|  (room_is_private(location) && !IS_TRUSTED(ch,IMPLEMENTOR)))` |  | pending |
| `act_enter.do_enter.or.004` | 114 | `\|\|  location == old_room` |  | pending |
| `act_enter.do_enter.or.005` | 115 | `\|\|  !can_see_room(ch,location)` |  | pending |
| `act_enter.do_enter.or.006` | 116 | `\|\|  (room_is_private(location) && !IS_TRUSTED(ch,IMPLEMENTOR)))` |  | pending |
| `act_enter.do_enter.and.005` | 116 | `&& !IS_TRUSTED(ch,IMPLEMENTOR)))` |  | pending |
| `act_enter.do_enter.return.005` | 119 | `return;` |  | pending |
| `act_enter.do_enter.if.009` | 122 | `if (IS_NPC(ch) && IS_SET(ch->act,ACT_AGGRESSIVE)         &&  IS_SET(location->room_flags,ROOM_LAW))` |  | pending |
| `act_enter.do_enter.and.006` | 122 | `&& IS_SET(ch->act,ACT_AGGRESSIVE)` |  | pending |
| `act_enter.do_enter.and.007` | 123 | `&&  IS_SET(location->room_flags,ROOM_LAW))` |  | pending |
| `act_enter.do_enter.return.006` | 126 | `return;` |  | pending |
| `act_enter.do_enter.if.010` | 131 | `if (IS_SET(portal->value[2],GATE_NORMAL_EXIT))` |  | pending |
| `act_enter.do_enter.if.011` | 140 | `if (IS_SET(portal->value[2],GATE_GOWITH))` |  | pending |
| `act_enter.do_enter.if.012` | 146 | `if (IS_SET(portal->value[2],GATE_NORMAL_EXIT))` |  | pending |
| `act_enter.do_enter.if.013` | 154 | `if (portal->value[0] > 0)` |  | pending |
| `act_enter.do_enter.if.014` | 157 | `if (portal->value[0] == 0)` |  | pending |
| `act_enter.do_enter.if.015` | 162 | `if (old_room == location)` |  | pending |
| `act_enter.do_enter.return.007` | 163 | `return;` |  | pending |
| `act_enter.do_enter.for.001` | 165 | `for ( fch = old_room->people; fch != NULL; fch = fch_next )` |  | pending |
| `act_enter.do_enter.if.016` | 169 | `if (portal == NULL \|\| portal->value[0] == -1)` |  | pending |
| `act_enter.do_enter.or.007` | 169 | `\|\| portal->value[0] == -1)` |  | pending |
| `act_enter.do_enter.continue.001` | 171 | `continue;` |  | pending |
| `act_enter.do_enter.if.017` | 173 | `if ( fch->master == ch && IS_AFFECTED(fch,AFF_CHARM)             &&   fch->position < POS_STANDING)` |  | pending |
| `act_enter.do_enter.and.008` | 173 | `&& IS_AFFECTED(fch,AFF_CHARM)` |  | pending |
| `act_enter.do_enter.and.009` | 174 | `&&   fch->position < POS_STANDING)` |  | pending |
| `act_enter.do_enter.if.018` | 177 | `if ( fch->master == ch && fch->position == POS_STANDING)` |  | pending |
| `act_enter.do_enter.and.010` | 177 | `&& fch->position == POS_STANDING)` |  | pending |
| `act_enter.do_enter.if.019` | 180 | `if (IS_SET(ch->in_room->room_flags,ROOM_LAW)                 &&  (IS_NPC(fch) && IS_SET(fch->act,ACT_AGGRESSIVE)))` |  | pending |
| `act_enter.do_enter.and.011` | 181 | `&&  (IS_NPC(fch) && IS_SET(fch->act,ACT_AGGRESSIVE)))` |  | pending |
| `act_enter.do_enter.and.012` | 181 | `&& IS_SET(fch->act,ACT_AGGRESSIVE)))` |  | pending |
| `act_enter.do_enter.continue.002` | 187 | `continue;` |  | pending |
| `act_enter.do_enter.if.020` | 195 | `if (portal != NULL && portal->value[0] == -1)` |  | pending |
| `act_enter.do_enter.and.013` | 195 | `&& portal->value[0] == -1)` |  | pending |
| `act_enter.do_enter.if.021` | 198 | `if (ch->in_room == old_room)` |  | pending |
| `act_enter.do_enter.if.022` | 200 | `if (old_room->people != NULL)` |  | pending |
| `act_enter.do_enter.return.008` | 209 | `return;` |  | pending |
| `act_enter.do_enter.return.009` | 213 | `return;` |  | pending |
| `act_enter.do_enter.fighting-silent.path` | 68 | `fighting silent` | act_enter.do_enter.fighting-silent | specified |
| `act_enter.do_enter.empty-argument.path` | 68 | `empty argument` | act_enter.do_enter.empty-argument | specified |
| `act_enter.do_enter.no-object.path` | 68 | `no object` | act_enter.do_enter.no-object | specified |
| `act_enter.do_enter.not-a-portal.path` | 68 | `not a portal` | act_enter.do_enter.not-a-portal | specified |
| `act_enter.do_enter.closed-mortal.path` | 68 | `closed mortal` | act_enter.do_enter.closed-mortal | specified |
| `act_enter.do_enter.cursed-mortal.path` | 68 | `cursed mortal` | act_enter.do_enter.cursed-mortal | specified |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#include <time.h>` — pending configuration/reachability review.
- Line 31: `#else` — pending configuration/reachability review.
- Line 32: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 33: `#include <sys/time.h>` — pending configuration/reachability review.
- Line 34: `#endif` — pending configuration/reachability review.
- Line 35: `#include <stdio.h>` — pending configuration/reachability review.
- Line 36: `#include <string.h>` — pending configuration/reachability review.
- Line 37: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 38: `#include "merc.h"` — pending configuration/reachability review.
- Line 39: `#include "interp.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


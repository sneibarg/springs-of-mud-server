# src/music.c

Role: translation_unit. Disposition: **pending**. SHA-256: `e629865f348b4fb3a085912192d29be425a169f068a9be3cdc53fb1a2e0c3129`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## song_update

[Source line 45](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/music.c:45); ends at line 154. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- update_handler: `src/update.c:1099` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/music.h:42` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `IS_SET`, `act_new`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `music.song_update.if.001` | 56 | `if (channel_songs[1] >= MAX_SONGS)` |  | pending |
| `music.song_update.if.002` | 59 | `if (channel_songs[1] > -1)` |  | pending |
| `music.song_update.if.003` | 61 | `if (channel_songs[0] >= MAX_LINES         \|\|  channel_songs[0] >= song_table[channel_songs[1]].lines)` |  | pending |
| `music.song_update.or.001` | 62 | `\|\|  channel_songs[0] >= song_table[channel_songs[1]].lines)` |  | pending |
| `music.song_update.for.001` | 67 | `for (i = 1; i < MAX_GLOBAL; i++)` |  | pending |
| `music.song_update.if.004` | 73 | `if (channel_songs[0] < 0)` |  | pending |
| `music.song_update.for.002` | 87 | `for (d = descriptor_list; d != NULL; d = d->next)` |  | pending |
| `music.song_update.ternary.001` | 89 | `? d->original : d->character;` |  | pending |
| `music.song_update.if.005` | 91 | `if ( d->connected == CON_PLAYING &&              	     !IS_SET(victim->comm,COMM_NOMUSIC) &&              	     !IS_SET(victim->comm,COMM_QUIET) )` |  | pending |
| `music.song_update.and.001` | 91 | `&&` |  | pending |
| `music.song_update.and.002` | 92 | `&&` |  | pending |
| `music.song_update.for.003` | 99 | `for (obj = object_list; obj != NULL; obj = obj->next)` |  | pending |
| `music.song_update.if.006` | 101 | `if (obj->item_type != ITEM_JUKEBOX \|\| obj->value[1] < 0)` |  | pending |
| `music.song_update.or.002` | 101 | `\|\| obj->value[1] < 0)` |  | pending |
| `music.song_update.continue.001` | 102 | `continue;` |  | pending |
| `music.song_update.if.007` | 104 | `if (obj->value[1] >= MAX_SONGS)` |  | pending |
| `music.song_update.continue.002` | 107 | `continue;` |  | pending |
| `music.song_update.if.008` | 112 | `if ((room = obj->in_room) == NULL)` |  | pending |
| `music.song_update.if.009` | 114 | `if (obj->carried_by == NULL)` |  | pending |
| `music.song_update.continue.003` | 115 | `continue;` |  | pending |
| `music.song_update.if.010` | 117 | `if ((room = obj->carried_by->in_room) == NULL)` |  | pending |
| `music.song_update.continue.004` | 118 | `continue;` |  | pending |
| `music.song_update.if.011` | 121 | `if (obj->value[0] < 0)` |  | pending |
| `music.song_update.if.012` | 125 | `if (room->people != NULL)` |  | pending |
| `music.song_update.continue.005` | 128 | `continue;` |  | pending |
| `music.song_update.if.013` | 132 | `if (obj->value[0] >= MAX_LINES  	    \|\| obj->value[0] >= song_table[obj->value[1]].lines)` |  | pending |
| `music.song_update.or.003` | 133 | `\|\| obj->value[0] >= song_table[obj->value[1]].lines)` |  | pending |
| `music.song_update.continue.006` | 143 | `continue;` |  | pending |
| `music.song_update.if.014` | 151 | `if (room->people != NULL)` |  | pending |

## load_songs

[Source line 158](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/music.c:158); ends at line 216. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:385` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/music.h:43` (declaration_or_dispatch_reference).

Dependencies: `fopen`, `bug`, `fclose`, `fread_letter`, `ungetc`, `fread_string`, `fread_string_eol`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `music.load_songs.for.001` | 165 | `for (i = 0; i <= MAX_GLOBAL; i++)` |  | pending |
| `music.load_songs.if.001` | 168 | `if ((fp = fopen(MUSIC_FILE,"r")) == NULL)` |  | pending |
| `music.load_songs.return.001` | 172 | `return;` |  | pending |
| `music.load_songs.for.002` | 175 | `for (count = 0; count < MAX_SONGS; count++)` |  | pending |
| `music.load_songs.if.002` | 178 | `if (letter == '#')` |  | pending |
| `music.load_songs.if.003` | 180 | `if (count < MAX_SONGS)` |  | pending |
| `music.load_songs.return.002` | 183 | `return;` |  | pending |
| `music.load_songs.for.003` | 194 | `for ( ; ;)` |  | pending |
| `music.load_songs.if.004` | 198 | `if (letter == '~')` |  | pending |
| `music.load_songs.break.001` | 201 | `break;` |  | pending |
| `music.load_songs.if.005` | 206 | `if (lines >= MAX_LINES)` |  | pending |
| `music.load_songs.break.002` | 209 | `break;` |  | pending |

## do_play

[Source line 218](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/music.c:218); ends at line 350. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_examine: `src/act_info.c:1271` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:261` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:199` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `can_see_obj`, `send_to_char`, `str_cmp`, `new_buf`, `sprintf`, `add_buf`, `capitalize`, `str_prefix`, `page_to_char`, `buf_string`, `free_buf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `music.do_play.for.001` | 227 | `for (juke = ch->in_room->contents; juke != NULL; juke = juke->next_content)` |  | pending |
| `music.do_play.if.001` | 228 | `if (juke->item_type == ITEM_JUKEBOX && can_see_obj(ch,juke))` |  | pending |
| `music.do_play.and.001` | 228 | `&& can_see_obj(ch,juke))` |  | pending |
| `music.do_play.break.001` | 229 | `break;` |  | pending |
| `music.do_play.if.002` | 231 | `if (argument[0] == '\0')` |  | pending |
| `music.do_play.return.001` | 234 | `return;` |  | pending |
| `music.do_play.if.003` | 237 | `if (juke == NULL)` |  | pending |
| `music.do_play.return.002` | 240 | `return;` |  | pending |
| `music.do_play.if.004` | 243 | `if (!str_cmp(arg,"list"))` |  | pending |
| `music.do_play.if.005` | 254 | `if (!str_cmp(arg,"artist"))` |  | pending |
| `music.do_play.if.006` | 257 | `if (argument[0] != '\0')` |  | pending |
| `music.do_play.for.002` | 264 | `for (i = 0; i < MAX_SONGS; i++)` |  | pending |
| `music.do_play.if.007` | 266 | `if (song_table[i].name == NULL)` |  | pending |
| `music.do_play.break.002` | 267 | `break;` |  | pending |
| `music.do_play.if.008` | 269 | `if (artist && (!match  	    \|\| 		   !str_prefix(argument,song_table[i].group)))` |  | pending |
| `music.do_play.and.002` | 269 | `&& (!match` |  | pending |
| `music.do_play.or.001` | 270 | `\|\| 		   !str_prefix(argument,song_table[i].group)))` |  | pending |
| `music.do_play.if.009` | 273 | `if (!artist && (!match  	    \|\| 	 		 !str_prefix(argument,song_table[i].name)))` |  | pending |
| `music.do_play.and.003` | 273 | `&& (!match` |  | pending |
| `music.do_play.or.002` | 274 | `\|\| 	 		 !str_prefix(argument,song_table[i].name)))` |  | pending |
| `music.do_play.continue.001` | 277 | `continue;` |  | pending |
| `music.do_play.if.010` | 279 | `if (!artist && ++col % 2 == 0)` |  | pending |
| `music.do_play.and.004` | 279 | `&& ++col % 2 == 0)` |  | pending |
| `music.do_play.if.011` | 282 | `if (!artist && col % 2 != 0)` |  | pending |
| `music.do_play.and.005` | 282 | `&& col % 2 != 0)` |  | pending |
| `music.do_play.return.003` | 287 | `return;` |  | pending |
| `music.do_play.if.012` | 290 | `if (!str_cmp(arg,"loud"))` |  | pending |
| `music.do_play.if.013` | 296 | `if (argument[0] == '\0')` |  | pending |
| `music.do_play.return.004` | 299 | `return;` |  | pending |
| `music.do_play.if.014` | 302 | `if ((global && channel_songs[MAX_GLOBAL] > -1)      \|\|  (!global && juke->value[4] > -1))` |  | pending |
| `music.do_play.and.006` | 302 | `&& channel_songs[MAX_GLOBAL] > -1)` |  | pending |
| `music.do_play.or.003` | 303 | `\|\|  (!global && juke->value[4] > -1))` |  | pending |
| `music.do_play.and.007` | 303 | `&& juke->value[4] > -1))` |  | pending |
| `music.do_play.return.005` | 306 | `return;` |  | pending |
| `music.do_play.for.003` | 309 | `for (song = 0; song < MAX_SONGS; song++)` |  | pending |
| `music.do_play.if.015` | 311 | `if (song_table[song].name == NULL)` |  | pending |
| `music.do_play.return.006` | 314 | `return;` |  | pending |
| `music.do_play.if.016` | 316 | `if (!str_prefix(argument,song_table[song].name))` |  | pending |
| `music.do_play.break.003` | 317 | `break;` |  | pending |
| `music.do_play.if.017` | 320 | `if (song >= MAX_SONGS)` |  | pending |
| `music.do_play.return.007` | 323 | `return;` |  | pending |
| `music.do_play.if.018` | 328 | `if (global)` |  | pending |
| `music.do_play.for.004` | 330 | `for (i = 1; i <= MAX_GLOBAL; i++)` |  | pending |
| `music.do_play.if.019` | 331 | `if (channel_songs[i] < 0)` |  | pending |
| `music.do_play.if.020` | 333 | `if (i == 1)` |  | pending |
| `music.do_play.return.008` | 336 | `return;` |  | pending |
| `music.do_play.for.005` | 341 | `for (i = 1; i < 5; i++)` |  | pending |
| `music.do_play.if.021` | 342 | `if (juke->value[i] < 0)` |  | pending |
| `music.do_play.if.022` | 344 | `if (i == 1)` |  | pending |
| `music.do_play.return.009` | 347 | `return;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#include <sys/time.h>` — pending configuration/reachability review.
- Line 33: `#endif` — pending configuration/reachability review.
- Line 34: `#include <stdio.h>` — pending configuration/reachability review.
- Line 35: `#include <string.h>` — pending configuration/reachability review.
- Line 36: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 37: `#include <time.h>` — pending configuration/reachability review.
- Line 38: `#include "merc.h"` — pending configuration/reachability review.
- Line 39: `#include "music.h"` — pending configuration/reachability review.
- Line 40: `#include "recycle.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates


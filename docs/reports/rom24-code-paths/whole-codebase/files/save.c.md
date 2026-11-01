# src/save.c

Role: translation_unit. Disposition: **pending**. SHA-256: `2792431c4237a7971cf57c216f7c29ccdc4bf4b5bd50788858d646de451b38c9`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## print_flags

[Source line 51](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:51); ends at line 78. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- save_bans: `src/ban.c:62` (lexical_call_candidate).
- fwrite_char: `src/save.c:216` (lexical_call_candidate).
- fwrite_char: `src/save.c:218` (lexical_call_candidate).
- fwrite_char: `src/save.c:219` (lexical_call_candidate).
- fwrite_char: `src/save.c:221` (lexical_call_candidate).
- fwrite_pet: `src/save.c:363` (lexical_call_candidate).
- fwrite_pet: `src/save.c:365` (lexical_call_candidate).
- fwrite_pet: `src/save.c:367` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2116` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.print_flags.for.001` | 57 | `for (count = 0; count < 32;  count++)` |  | pending |
| `save.print_flags.if.001` | 59 | `if (IS_SET(flag,1<<count))` |  | pending |
| `save.print_flags.if.002` | 61 | `if (count < 26)` |  | pending |
| `save.print_flags.if.003` | 69 | `if (pos == 0)` |  | pending |
| `save.print_flags.return.001` | 77 | `return buf;` |  | pending |

## save_char_obj

[Source line 107](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:107); ends at line 158. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_quit: `src/act_comm.c:1424` (lexical_call_candidate).
- do_save: `src/act_comm.c:1455` (lexical_call_candidate).
- do_password: `src/act_info.c:2752` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2234` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:533` (lexical_call_candidate).
- do_reboot: `src/act_wiz.c:2024` (lexical_call_candidate).
- do_shutdown: `src/act_wiz.c:2058` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2607` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2708` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2891` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:554` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:606` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:633` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:721` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:743` (lexical_call_candidate).
- game_loop_unix: `src/comm.c:798` (lexical_call_candidate).
- check_killer: `src/fight.c:1254` (lexical_call_candidate).
- gain_exp: `src/update.c:136` (lexical_call_candidate).
- char_update: `src/update.c:695` (lexical_call_candidate).
- char_update: `src/update.c:830` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2287` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `defined`, `IS_IMMORTAL`, `fclose`, `sprintf`, `capitalize`, `fopen`, `bug`, `perror`, `fprintf`, `get_trust`, `fwrite_char`, `fwrite_obj`, `fwrite_pet`, `rename`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.save_char_obj.if.001` | 112 | `if ( IS_NPC(ch) )` |  | pending |
| `save.save_char_obj.return.001` | 113 | `return;` |  | pending |
| `save.save_char_obj.if.002` | 115 | `if ( ch->desc != NULL && ch->desc->original != NULL )` |  | pending |
| `save.save_char_obj.and.001` | 115 | `&& ch->desc->original != NULL )` |  | pending |
| `save.save_char_obj.if.003` | 118 | `if defined(unix)` |  | pending |
| `save.save_char_obj.if.004` | 120 | `if (IS_IMMORTAL(ch) \|\| ch->level >= LEVEL_IMMORTAL)` |  | pending |
| `save.save_char_obj.or.001` | 120 | `\|\| ch->level >= LEVEL_IMMORTAL)` |  | pending |
| `save.save_char_obj.if.005` | 124 | `if ((fp = fopen(strsave,"w")) == NULL)` |  | pending |
| `save.save_char_obj.if.006` | 139 | `if ( ( fp = fopen( TEMP_FILE, "w" ) ) == NULL )` |  | pending |
| `save.save_char_obj.if.007` | 147 | `if ( ch->carrying != NULL )` |  | pending |
| `save.save_char_obj.if.008` | 150 | `if (ch->pet != NULL && ch->pet->in_room == ch->in_room)` |  | pending |
| `save.save_char_obj.and.002` | 150 | `&& ch->pet->in_room == ch->in_room)` |  | pending |
| `save.save_char_obj.return.002` | 157 | `return;` |  | pending |

## fwrite_char

[Source line 165](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:165); ends at line 328. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- save_char_obj: `src/save.c:146` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/save.c:92` (declaration_or_dispatch_reference).

Dependencies: `fprintf`, `IS_NPC`, `str_cmp`, `get_room_index`, `print_flags`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.fwrite_char.ternary.001` | 170 | `? "MOB" : "PLAYER"	);` |  | pending |
| `save.fwrite_char.if.001` | 176 | `if (ch->short_descr[0] != '\0')` |  | pending |
| `save.fwrite_char.if.002` | 178 | `if( ch->long_descr[0] != '\0')` |  | pending |
| `save.fwrite_char.if.003` | 180 | `if (ch->description[0] != '\0')` |  | pending |
| `save.fwrite_char.if.004` | 182 | `if (ch->prompt != NULL \|\| !str_cmp(ch->prompt,"<%hhp %mm %vmv> "))` |  | pending |
| `save.fwrite_char.or.001` | 182 | `\|\| !str_cmp(ch->prompt,"<%hhp %mm %vmv> "))` |  | pending |
| `save.fwrite_char.if.005` | 185 | `if (ch->clan)` |  | pending |
| `save.fwrite_char.if.006` | 190 | `if (ch->trust != 0)` |  | pending |
| `save.fwrite_char.and.001` | 200 | `&& ch->was_in_room != NULL )` |  | pending |
| `save.fwrite_char.ternary.002` | 201 | `? ch->was_in_room->vnum` |  | pending |
| `save.fwrite_char.ternary.003` | 202 | `? 3001 : ch->in_room->vnum );` |  | pending |
| `save.fwrite_char.if.007` | 206 | `if (ch->gold > 0)` |  | pending |
| `save.fwrite_char.if.008` | 210 | `if (ch->silver > 0)` |  | pending |
| `save.fwrite_char.if.009` | 215 | `if (ch->act != 0)` |  | pending |
| `save.fwrite_char.if.010` | 217 | `if (ch->affected_by != 0)` |  | pending |
| `save.fwrite_char.if.011` | 220 | `if (ch->wiznet)` |  | pending |
| `save.fwrite_char.if.012` | 222 | `if (ch->invis_level)` |  | pending |
| `save.fwrite_char.if.013` | 224 | `if (ch->incog_level)` |  | pending |
| `save.fwrite_char.ternary.004` | 227 | `? POS_STANDING : ch->position );` |  | pending |
| `save.fwrite_char.if.014` | 228 | `if (ch->practice != 0)` |  | pending |
| `save.fwrite_char.if.015` | 230 | `if (ch->train != 0)` |  | pending |
| `save.fwrite_char.if.016` | 232 | `if (ch->saving_throw != 0)` |  | pending |
| `save.fwrite_char.if.017` | 235 | `if (ch->hitroll != 0)` |  | pending |
| `save.fwrite_char.if.018` | 237 | `if (ch->damroll != 0)` |  | pending |
| `save.fwrite_char.if.019` | 241 | `if (ch->wimpy !=0 )` |  | pending |
| `save.fwrite_char.if.020` | 257 | `if ( IS_NPC(ch) )` |  | pending |
| `save.fwrite_char.if.021` | 264 | `if (ch->pcdata->bamfin[0] != '\0')` |  | pending |
| `save.fwrite_char.if.022` | 266 | `if (ch->pcdata->bamfout[0] != '\0')` |  | pending |
| `save.fwrite_char.for.001` | 282 | `for (pos = 0; pos < MAX_ALIAS; pos++)` |  | pending |
| `save.fwrite_char.if.023` | 284 | `if (ch->pcdata->alias[pos] == NULL 	    \|\|  ch->pcdata->alias_sub[pos] == NULL)` |  | pending |
| `save.fwrite_char.or.002` | 285 | `\|\|  ch->pcdata->alias_sub[pos] == NULL)` |  | pending |
| `save.fwrite_char.break.001` | 286 | `break;` |  | pending |
| `save.fwrite_char.for.002` | 292 | `for ( sn = 0; sn < MAX_SKILL; sn++ )` |  | pending |
| `save.fwrite_char.if.024` | 294 | `if ( skill_table[sn].name != NULL && ch->pcdata->learned[sn] > 0 )` |  | pending |
| `save.fwrite_char.and.002` | 294 | `&& ch->pcdata->learned[sn] > 0 )` |  | pending |
| `save.fwrite_char.for.003` | 301 | `for ( gn = 0; gn < MAX_GROUP; gn++ )` |  | pending |
| `save.fwrite_char.if.025` | 303 | `if ( group_table[gn].name != NULL && ch->pcdata->group_known[gn])` |  | pending |
| `save.fwrite_char.and.003` | 303 | `&& ch->pcdata->group_known[gn])` |  | pending |
| `save.fwrite_char.for.004` | 310 | `for ( paf = ch->affected; paf != NULL; paf = paf->next )` |  | pending |
| `save.fwrite_char.if.026` | 312 | `if (paf->type < 0 \|\| paf->type>= MAX_SKILL)` |  | pending |
| `save.fwrite_char.or.003` | 312 | `\|\| paf->type>= MAX_SKILL)` |  | pending |
| `save.fwrite_char.continue.001` | 313 | `continue;` |  | pending |
| `save.fwrite_char.return.001` | 327 | `return;` |  | pending |

## fwrite_pet

[Source line 331](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:331); ends at line 401. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- save_char_obj: `src/save.c:151` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/save.c:95` (declaration_or_dispatch_reference).

Dependencies: `fprintf`, `print_flags`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.fwrite_pet.if.001` | 341 | `if (pet->short_descr != pet->pIndexData->short_descr)` |  | pending |
| `save.fwrite_pet.if.002` | 343 | `if (pet->long_descr != pet->pIndexData->long_descr)` |  | pending |
| `save.fwrite_pet.if.003` | 345 | `if (pet->description != pet->pIndexData->description)` |  | pending |
| `save.fwrite_pet.if.004` | 347 | `if (pet->race != pet->pIndexData->race)` |  | pending |
| `save.fwrite_pet.if.005` | 349 | `if (pet->clan)` |  | pending |
| `save.fwrite_pet.if.006` | 352 | `if (pet->level != pet->pIndexData->level)` |  | pending |
| `save.fwrite_pet.if.007` | 356 | `if (pet->gold > 0)` |  | pending |
| `save.fwrite_pet.if.008` | 358 | `if (pet->silver > 0)` |  | pending |
| `save.fwrite_pet.if.009` | 360 | `if (pet->exp > 0)` |  | pending |
| `save.fwrite_pet.if.010` | 362 | `if (pet->act != pet->pIndexData->act)` |  | pending |
| `save.fwrite_pet.if.011` | 364 | `if (pet->affected_by != pet->pIndexData->affected_by)` |  | pending |
| `save.fwrite_pet.if.012` | 366 | `if (pet->comm != 0)` |  | pending |
| `save.fwrite_pet.ternary.001` | 368 | `? POS_STANDING : pet->position);` |  | pending |
| `save.fwrite_pet.if.013` | 369 | `if (pet->saving_throw != 0)` |  | pending |
| `save.fwrite_pet.if.014` | 371 | `if (pet->alignment != pet->pIndexData->alignment)` |  | pending |
| `save.fwrite_pet.if.015` | 373 | `if (pet->hitroll != pet->pIndexData->hitroll)` |  | pending |
| `save.fwrite_pet.if.016` | 375 | `if (pet->damroll != pet->pIndexData->damage[DICE_BONUS])` |  | pending |
| `save.fwrite_pet.for.001` | 388 | `for ( paf = pet->affected; paf != NULL; paf = paf->next )` |  | pending |
| `save.fwrite_pet.if.017` | 390 | `if (paf->type < 0 \|\| paf->type >= MAX_SKILL)` |  | pending |
| `save.fwrite_pet.or.001` | 390 | `\|\| paf->type >= MAX_SKILL)` |  | pending |
| `save.fwrite_pet.continue.001` | 391 | `continue;` |  | pending |
| `save.fwrite_pet.return.001` | 400 | `return;` |  | pending |

## fwrite_obj

[Source line 406](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:406); ends at line 533. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- save_char_obj: `src/save.c:148` (lexical_call_candidate).
- fwrite_obj: `src/save.c:416` (lexical_call_candidate).
- fwrite_obj: `src/save.c:530` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/save.c:93` (declaration_or_dispatch_reference).

Dependencies: `fwrite_obj`, `fprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.fwrite_obj.if.001` | 415 | `if ( obj->next_content != NULL )` |  | pending |
| `save.fwrite_obj.if.002` | 421 | `if ( (ch->level < obj->level - 2 && obj->item_type != ITEM_CONTAINER)     \|\|   obj->item_type == ITEM_KEY     \|\|   (obj->item_type == ITEM_MAP && !obj->value[0]))` |  | pending |
| `save.fwrite_obj.and.001` | 421 | `&& obj->item_type != ITEM_CONTAINER)` |  | pending |
| `save.fwrite_obj.or.001` | 422 | `\|\|   obj->item_type == ITEM_KEY` |  | pending |
| `save.fwrite_obj.or.002` | 423 | `\|\|   (obj->item_type == ITEM_MAP && !obj->value[0]))` |  | pending |
| `save.fwrite_obj.and.002` | 423 | `&& !obj->value[0]))` |  | pending |
| `save.fwrite_obj.return.001` | 424 | `return;` |  | pending |
| `save.fwrite_obj.if.003` | 428 | `if (!obj->pIndexData->new_format)` |  | pending |
| `save.fwrite_obj.if.004` | 430 | `if (obj->enchanted)` |  | pending |
| `save.fwrite_obj.if.005` | 436 | `if ( obj->name != obj->pIndexData->name)` |  | pending |
| `save.fwrite_obj.if.006` | 438 | `if ( obj->short_descr != obj->pIndexData->short_descr)` |  | pending |
| `save.fwrite_obj.if.007` | 440 | `if ( obj->description != obj->pIndexData->description)` |  | pending |
| `save.fwrite_obj.if.008` | 442 | `if ( obj->extra_flags != obj->pIndexData->extra_flags)` |  | pending |
| `save.fwrite_obj.if.009` | 444 | `if ( obj->wear_flags != obj->pIndexData->wear_flags)` |  | pending |
| `save.fwrite_obj.if.010` | 446 | `if ( obj->item_type != obj->pIndexData->item_type)` |  | pending |
| `save.fwrite_obj.if.011` | 448 | `if ( obj->weight != obj->pIndexData->weight)` |  | pending |
| `save.fwrite_obj.if.012` | 450 | `if ( obj->condition != obj->pIndexData->condition)` |  | pending |
| `save.fwrite_obj.if.013` | 456 | `if (obj->level != obj->pIndexData->level)` |  | pending |
| `save.fwrite_obj.if.014` | 458 | `if (obj->timer != 0)` |  | pending |
| `save.fwrite_obj.if.015` | 461 | `if (obj->value[0] != obj->pIndexData->value[0]     \|\|  obj->value[1] != obj->pIndexData->value[1]     \|\|  obj->value[2] != obj->pIndexData->value[2]     \|\|  obj->value[3] != obj->pIndexData->value[3]     \|\|  obj->value[4] != obj->pIndexData->value[4])` |  | pending |
| `save.fwrite_obj.or.003` | 462 | `\|\|  obj->value[1] != obj->pIndexData->value[1]` |  | pending |
| `save.fwrite_obj.or.004` | 463 | `\|\|  obj->value[2] != obj->pIndexData->value[2]` |  | pending |
| `save.fwrite_obj.or.005` | 464 | `\|\|  obj->value[3] != obj->pIndexData->value[3]` |  | pending |
| `save.fwrite_obj.or.006` | 465 | `\|\|  obj->value[4] != obj->pIndexData->value[4])` |  | pending |
| `save.fwrite_obj.switch.001` | 470 | `switch ( obj->item_type )` |  | pending |
| `save.fwrite_obj.case.001` | 472 | `case ITEM_POTION:` |  | pending |
| `save.fwrite_obj.case.002` | 473 | `case ITEM_SCROLL:` |  | pending |
| `save.fwrite_obj.case.003` | 474 | `case ITEM_PILL:` |  | pending |
| `save.fwrite_obj.if.016` | 475 | `if ( obj->value[1] > 0 )` |  | pending |
| `save.fwrite_obj.if.017` | 481 | `if ( obj->value[2] > 0 )` |  | pending |
| `save.fwrite_obj.if.018` | 487 | `if ( obj->value[3] > 0 )` |  | pending |
| `save.fwrite_obj.break.001` | 493 | `break;` |  | pending |
| `save.fwrite_obj.case.004` | 495 | `case ITEM_STAFF:` |  | pending |
| `save.fwrite_obj.case.005` | 496 | `case ITEM_WAND:` |  | pending |
| `save.fwrite_obj.if.019` | 497 | `if ( obj->value[3] > 0 )` |  | pending |
| `save.fwrite_obj.break.002` | 503 | `break;` |  | pending |
| `save.fwrite_obj.for.001` | 506 | `for ( paf = obj->affected; paf != NULL; paf = paf->next )` |  | pending |
| `save.fwrite_obj.if.020` | 508 | `if (paf->type < 0 \|\| paf->type >= MAX_SKILL)` |  | pending |
| `save.fwrite_obj.or.007` | 508 | `\|\| paf->type >= MAX_SKILL)` |  | pending |
| `save.fwrite_obj.continue.001` | 509 | `continue;` |  | pending |
| `save.fwrite_obj.for.002` | 521 | `for ( ed = obj->extra_descr; ed != NULL; ed = ed->next )` |  | pending |
| `save.fwrite_obj.if.021` | 529 | `if ( obj->contains != NULL )` |  | pending |
| `save.fwrite_obj.return.002` | 532 | `return;` |  | pending |

## load_char_obj

[Source line 540](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:540); ends at line 694. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1581` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2288` (declaration_or_dispatch_reference).

Dependencies: `new_char`, `new_pcdata`, `str_dup`, `get_pc_id`, `race_lookup`, `fclose`, `defined`, `sprintf`, `capitalize`, `fopen`, `system`, `fread_letter`, `fread_to_eol`, `bug`, `fread_word`, `str_cmp`, `fread_char`, `fread_obj`, `fread_pet`, `group_add`, `case`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.load_char_obj.for.001` | 566 | `for (stat =0; stat < MAX_STATS; stat++)` |  | pending |
| `save.load_char_obj.if.001` | 575 | `if defined(unix)` |  | pending |
| `save.load_char_obj.if.002` | 578 | `if ( ( fp = fopen( strsave, "r" ) ) != NULL )` |  | pending |
| `save.load_char_obj.if.003` | 587 | `if ( ( fp = fopen( strsave, "r" ) ) != NULL )` |  | pending |
| `save.load_char_obj.for.002` | 591 | `for ( iNest = 0; iNest < MAX_NEST; iNest++ )` |  | pending |
| `save.load_char_obj.for.003` | 595 | `for ( ; ; )` |  | pending |
| `save.load_char_obj.if.004` | 601 | `if ( letter == '*' )` |  | pending |
| `save.load_char_obj.continue.001` | 604 | `continue;` |  | pending |
| `save.load_char_obj.if.005` | 607 | `if ( letter != '#' )` |  | pending |
| `save.load_char_obj.break.001` | 610 | `break;` |  | pending |
| `save.load_char_obj.if.006` | 614 | `if      ( !str_cmp( word, "PLAYER" ) )` |  | pending |
| `save.load_char_obj.if.007` | 615 | `if ( !str_cmp( word, "OBJECT" ) )` |  | pending |
| `save.load_char_obj.if.008` | 616 | `if ( !str_cmp( word, "O"      ) )` |  | pending |
| `save.load_char_obj.if.009` | 617 | `if ( !str_cmp( word, "PET"    ) )` |  | pending |
| `save.load_char_obj.if.010` | 618 | `if ( !str_cmp( word, "END"    ) )` |  | pending |
| `save.load_char_obj.break.002` | 618 | `break;` |  | pending |
| `save.load_char_obj.break.003` | 622 | `break;` |  | pending |
| `save.load_char_obj.if.011` | 632 | `if (found)` |  | pending |
| `save.load_char_obj.if.012` | 636 | `if (ch->race == 0)` |  | pending |
| `save.load_char_obj.for.004` | 642 | `for (i = 0; i < 5; i++)` |  | pending |
| `save.load_char_obj.if.013` | 644 | `if (pc_race_table[ch->race].skills[i] == NULL)` |  | pending |
| `save.load_char_obj.break.004` | 645 | `break;` |  | pending |
| `save.load_char_obj.if.014` | 659 | `if (found && ch->version < 2)` |  | pending |
| `save.load_char_obj.and.001` | 659 | `&& ch->version < 2)  /* need to add the new skills */` |  | pending |
| `save.load_char_obj.if.015` | 668 | `if (found && ch->version < 3 && (ch->level > 35 \|\| ch->trust > 35))` |  | pending |
| `save.load_char_obj.and.002` | 668 | `&& ch->version < 3 && (ch->level > 35 \|\| ch->trust > 35))` |  | pending |
| `save.load_char_obj.and.003` | 668 | `&& (ch->level > 35 \|\| ch->trust > 35))` |  | pending |
| `save.load_char_obj.or.001` | 668 | `\|\| ch->trust > 35))` |  | pending |
| `save.load_char_obj.switch.001` | 670 | `switch (ch->level)` |  | pending |
| `save.load_char_obj.case.001` | 672 | `case(40) : ch->level = 60;` |  | pending |
| `save.load_char_obj.break.005` | 672 | `break;` |  | pending |
| `save.load_char_obj.case.002` | 673 | `case(39) : ch->level = 58;` |  | pending |
| `save.load_char_obj.break.006` | 673 | `break;` |  | pending |
| `save.load_char_obj.case.003` | 674 | `case(38) : ch->level = 56;` |  | pending |
| `save.load_char_obj.break.007` | 674 | `break;` |  | pending |
| `save.load_char_obj.case.004` | 675 | `case(37) : ch->level = 53;` |  | pending |
| `save.load_char_obj.break.008` | 675 | `break;` |  | pending |
| `save.load_char_obj.switch.002` | 678 | `switch (ch->trust)` |  | pending |
| `save.load_char_obj.case.005` | 680 | `case(40) : ch->trust = 60;` |  | pending |
| `save.load_char_obj.break.009` | 680 | `break;` |  | pending |
| `save.load_char_obj.case.006` | 681 | `case(39) : ch->trust = 58;` |  | pending |
| `save.load_char_obj.break.010` | 681 | `break;` |  | pending |
| `save.load_char_obj.case.007` | 682 | `case(38) : ch->trust = 56;` |  | pending |
| `save.load_char_obj.break.011` | 682 | `break;` |  | pending |
| `save.load_char_obj.case.008` | 683 | `case(37) : ch->trust = 53;` |  | pending |
| `save.load_char_obj.break.012` | 683 | `break;` |  | pending |
| `save.load_char_obj.case.009` | 684 | `case(36) : ch->trust = 51;` |  | pending |
| `save.load_char_obj.break.013` | 684 | `break;` |  | pending |
| `save.load_char_obj.if.016` | 689 | `if (found && ch->version < 4)` |  | pending |
| `save.load_char_obj.and.004` | 689 | `&& ch->version < 4)` |  | pending |
| `save.load_char_obj.return.001` | 693 | `return found;` |  | pending |

## fread_char

[Source line 728](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:728); ends at line 1127. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_char_obj: `src/save.c:614` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/save.c:96` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `log_string`, `feof`, `fread_word`, `UPPER`, `fread_to_eol`, `KEY`, `fread_flag`, `fread_number`, `str_cmp`, `str_dup`, `fread_string`, `new_affect`, `skill_lookup`, `bug`, `clan_lookup`, `UMIN`, `IS_AFFECTED`, `group_lookup`, `fprintf`, `gn_add`, `KEYS`, `race_lookup`, `get_room_index`, `free_string`, `get_mob_index`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.fread_char.for.001` | 740 | `for ( ; ; )` |  | pending |
| `save.fread_char.ternary.001` | 742 | `? "End" : fread_word( fp );` |  | pending |
| `save.fread_char.switch.001` | 745 | `switch ( UPPER(word[0]) )` |  | pending |
| `save.fread_char.case.001` | 747 | `case '*':` |  | pending |
| `save.fread_char.break.001` | 750 | `break;` |  | pending |
| `save.fread_char.case.002` | 752 | `case 'A':` |  | pending |
| `save.fread_char.if.001` | 759 | `if (!str_cmp( word, "Alia"))` |  | pending |
| `save.fread_char.if.002` | 761 | `if (count >= MAX_ALIAS)` |  | pending |
| `save.fread_char.break.002` | 765 | `break;` |  | pending |
| `save.fread_char.break.003` | 772 | `break;` |  | pending |
| `save.fread_char.if.003` | 775 | `if (!str_cmp( word, "Alias"))` |  | pending |
| `save.fread_char.if.004` | 777 | `if (count >= MAX_ALIAS)` |  | pending |
| `save.fread_char.break.004` | 781 | `break;` |  | pending |
| `save.fread_char.break.005` | 788 | `break;` |  | pending |
| `save.fread_char.if.005` | 791 | `if (!str_cmp( word, "AC") \|\| !str_cmp(word,"Armor"))` |  | pending |
| `save.fread_char.or.001` | 791 | `\|\| !str_cmp(word,"Armor"))` |  | pending |
| `save.fread_char.break.006` | 795 | `break;` |  | pending |
| `save.fread_char.if.006` | 798 | `if (!str_cmp(word,"ACs"))` |  | pending |
| `save.fread_char.for.002` | 802 | `for (i = 0; i < 4; i++)` |  | pending |
| `save.fread_char.break.007` | 805 | `break;` |  | pending |
| `save.fread_char.if.007` | 808 | `if (!str_cmp(word, "AffD"))` |  | pending |
| `save.fread_char.if.008` | 816 | `if (sn < 0)` |  | pending |
| `save.fread_char.break.008` | 829 | `break;` |  | pending |
| `save.fread_char.if.009` | 832 | `if (!str_cmp(word, "Affc"))` |  | pending |
| `save.fread_char.if.010` | 840 | `if (sn < 0)` |  | pending |
| `save.fread_char.break.009` | 854 | `break;` |  | pending |
| `save.fread_char.if.011` | 857 | `if ( !str_cmp( word, "AttrMod"  ) \|\| !str_cmp(word,"AMod"))` |  | pending |
| `save.fread_char.or.002` | 857 | `\|\| !str_cmp(word,"AMod"))` |  | pending |
| `save.fread_char.for.003` | 860 | `for (stat = 0; stat < MAX_STATS; stat ++)` |  | pending |
| `save.fread_char.break.010` | 863 | `break;` |  | pending |
| `save.fread_char.if.012` | 866 | `if ( !str_cmp( word, "AttrPerm" ) \|\| !str_cmp(word,"Attr"))` |  | pending |
| `save.fread_char.or.003` | 866 | `\|\| !str_cmp(word,"Attr"))` |  | pending |
| `save.fread_char.for.004` | 870 | `for (stat = 0; stat < MAX_STATS; stat++)` |  | pending |
| `save.fread_char.break.011` | 873 | `break;` |  | pending |
| `save.fread_char.break.012` | 875 | `break;` |  | pending |
| `save.fread_char.case.003` | 877 | `case 'B':` |  | pending |
| `save.fread_char.break.013` | 882 | `break;` |  | pending |
| `save.fread_char.case.004` | 884 | `case 'C':` |  | pending |
| `save.fread_char.if.013` | 889 | `if ( !str_cmp( word, "Condition" ) \|\| !str_cmp(word,"Cond"))` |  | pending |
| `save.fread_char.or.004` | 889 | `\|\| !str_cmp(word,"Cond"))` |  | pending |
| `save.fread_char.break.014` | 895 | `break;` |  | pending |
| `save.fread_char.if.014` | 897 | `if (!str_cmp(word,"Cnd"))` |  | pending |
| `save.fread_char.break.015` | 904 | `break;` |  | pending |
| `save.fread_char.break.016` | 908 | `break;` |  | pending |
| `save.fread_char.case.005` | 910 | `case 'D':` |  | pending |
| `save.fread_char.break.017` | 915 | `break;` |  | pending |
| `save.fread_char.case.006` | 917 | `case 'E':` |  | pending |
| `save.fread_char.if.015` | 918 | `if ( !str_cmp( word, "End" ) )` |  | pending |
| `save.fread_char.if.016` | 925 | `if (percent > 0 && !IS_AFFECTED(ch,AFF_POISON)     		&&  !IS_AFFECTED(ch,AFF_PLAGUE))` |  | pending |
| `save.fread_char.and.001` | 925 | `&& !IS_AFFECTED(ch,AFF_POISON)` |  | pending |
| `save.fread_char.and.002` | 926 | `&&  !IS_AFFECTED(ch,AFF_PLAGUE))` |  | pending |
| `save.fread_char.return.001` | 932 | `return;` |  | pending |
| `save.fread_char.break.018` | 935 | `break;` |  | pending |
| `save.fread_char.case.007` | 937 | `case 'G':` |  | pending |
| `save.fread_char.if.017` | 939 | `if ( !str_cmp( word, "Group" )  \|\| !str_cmp(word,"Gr"))` |  | pending |
| `save.fread_char.or.005` | 939 | `\|\| !str_cmp(word,"Gr"))` |  | pending |
| `save.fread_char.if.018` | 947 | `if ( gn < 0 )` |  | pending |
| `save.fread_char.break.019` | 956 | `break;` |  | pending |
| `save.fread_char.case.008` | 958 | `case 'H':` |  | pending |
| `save.fread_char.if.019` | 962 | `if ( !str_cmp( word, "HpManaMove" ) \|\| !str_cmp(word,"HMV"))` |  | pending |
| `save.fread_char.or.006` | 962 | `\|\| !str_cmp(word,"HMV"))` |  | pending |
| `save.fread_char.break.020` | 971 | `break;` |  | pending |
| `save.fread_char.if.020` | 974 | `if ( !str_cmp( word, "HpManaMovePerm" ) \|\| !str_cmp(word,"HMVP"))` |  | pending |
| `save.fread_char.or.007` | 974 | `\|\| !str_cmp(word,"HMVP"))` |  | pending |
| `save.fread_char.break.021` | 980 | `break;` |  | pending |
| `save.fread_char.break.022` | 983 | `break;` |  | pending |
| `save.fread_char.case.009` | 985 | `case 'I':` |  | pending |
| `save.fread_char.break.023` | 990 | `break;` |  | pending |
| `save.fread_char.case.010` | 992 | `case 'L':` |  | pending |
| `save.fread_char.break.024` | 1001 | `break;` |  | pending |
| `save.fread_char.case.011` | 1003 | `case 'N':` |  | pending |
| `save.fread_char.if.021` | 1006 | `if (!str_cmp(word,"Not"))` |  | pending |
| `save.fread_char.break.025` | 1014 | `break;` |  | pending |
| `save.fread_char.break.026` | 1016 | `break;` |  | pending |
| `save.fread_char.case.012` | 1018 | `case 'P':` |  | pending |
| `save.fread_char.break.027` | 1031 | `break;` |  | pending |
| `save.fread_char.case.013` | 1033 | `case 'R':` |  | pending |
| `save.fread_char.if.022` | 1037 | `if ( !str_cmp( word, "Room" ) )` |  | pending |
| `save.fread_char.if.023` | 1040 | `if ( ch->in_room == NULL )` |  | pending |
| `save.fread_char.break.028` | 1043 | `break;` |  | pending |
| `save.fread_char.break.029` | 1046 | `break;` |  | pending |
| `save.fread_char.case.014` | 1048 | `case 'S':` |  | pending |
| `save.fread_char.if.024` | 1058 | `if ( !str_cmp( word, "Skill" ) \|\| !str_cmp(word,"Sk"))` |  | pending |
| `save.fread_char.or.008` | 1058 | `\|\| !str_cmp(word,"Sk"))` |  | pending |
| `save.fread_char.if.025` | 1068 | `if ( sn < 0 )` |  | pending |
| `save.fread_char.break.030` | 1078 | `break;` |  | pending |
| `save.fread_char.case.015` | 1080 | `case 'T':` |  | pending |
| `save.fread_char.if.026` | 1087 | `if ( !str_cmp( word, "Title" )  \|\| !str_cmp( word, "Titl"))` |  | pending |
| `save.fread_char.or.009` | 1087 | `\|\| !str_cmp( word, "Titl"))` |  | pending |
| `save.fread_char.if.027` | 1090 | `if (ch->pcdata->title[0] != '.' && ch->pcdata->title[0] != ','  		&&  ch->pcdata->title[0] != '!' && ch->pcdata->title[0] != '?')` |  | pending |
| `save.fread_char.and.003` | 1090 | `&& ch->pcdata->title[0] != ','` |  | pending |
| `save.fread_char.and.004` | 1091 | `&&  ch->pcdata->title[0] != '!' && ch->pcdata->title[0] != '?')` |  | pending |
| `save.fread_char.and.005` | 1091 | `&& ch->pcdata->title[0] != '?')` |  | pending |
| `save.fread_char.break.031` | 1098 | `break;` |  | pending |
| `save.fread_char.break.032` | 1101 | `break;` |  | pending |
| `save.fread_char.case.016` | 1103 | `case 'V':` |  | pending |
| `save.fread_char.if.028` | 1106 | `if ( !str_cmp( word, "Vnum" ) )` |  | pending |
| `save.fread_char.break.033` | 1110 | `break;` |  | pending |
| `save.fread_char.break.034` | 1112 | `break;` |  | pending |
| `save.fread_char.case.017` | 1114 | `case 'W':` |  | pending |
| `save.fread_char.break.035` | 1118 | `break;` |  | pending |
| `save.fread_char.if.029` | 1121 | `if ( !fMatch )` |  | pending |

## fread_pet

[Source line 1130](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:1130); ends at line 1341. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_char_obj: `src/save.c:617` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/save.c:97` (declaration_or_dispatch_reference).

Dependencies: `feof`, `fread_word`, `str_cmp`, `fread_number`, `get_mob_index`, `bug`, `create_mobile`, `UPPER`, `fread_to_eol`, `KEY`, `fread_flag`, `new_affect`, `skill_lookup`, `clan_lookup`, `fread_string`, `IS_AFFECTED`, `UMIN`, `race_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.fread_pet.ternary.001` | 1139 | `? "END" : fread_word(fp);` |  | pending |
| `save.fread_pet.if.001` | 1140 | `if (!str_cmp(word,"Vnum"))` |  | pending |
| `save.fread_pet.if.002` | 1145 | `if (get_mob_index(vnum) == NULL)` |  | pending |
| `save.fread_pet.for.001` | 1159 | `for ( ; ; )` |  | pending |
| `save.fread_pet.ternary.002` | 1161 | `? "END" : fread_word(fp);` |  | pending |
| `save.fread_pet.switch.001` | 1164 | `switch (UPPER(word[0]))` |  | pending |
| `save.fread_pet.case.001` | 1166 | `case '*':` |  | pending |
| `save.fread_pet.break.001` | 1169 | `break;` |  | pending |
| `save.fread_pet.case.002` | 1171 | `case 'A':` |  | pending |
| `save.fread_pet.if.003` | 1176 | `if (!str_cmp(word,"ACs"))` |  | pending |
| `save.fread_pet.for.002` | 1180 | `for (i = 0; i < 4; i++)` |  | pending |
| `save.fread_pet.break.002` | 1183 | `break;` |  | pending |
| `save.fread_pet.if.004` | 1186 | `if (!str_cmp(word,"AffD"))` |  | pending |
| `save.fread_pet.if.005` | 1194 | `if (sn < 0)` |  | pending |
| `save.fread_pet.break.003` | 1207 | `break;` |  | pending |
| `save.fread_pet.if.006` | 1210 | `if (!str_cmp(word,"Affc"))` |  | pending |
| `save.fread_pet.if.007` | 1218 | `if (sn < 0)` |  | pending |
| `save.fread_pet.break.004` | 1232 | `break;` |  | pending |
| `save.fread_pet.if.008` | 1235 | `if (!str_cmp(word,"AMod"))` |  | pending |
| `save.fread_pet.for.003` | 1239 | `for (stat = 0; stat < MAX_STATS; stat++)` |  | pending |
| `save.fread_pet.break.005` | 1242 | `break;` |  | pending |
| `save.fread_pet.if.009` | 1245 | `if (!str_cmp(word,"Attr"))` |  | pending |
| `save.fread_pet.for.004` | 1249 | `for (stat = 0; stat < MAX_STATS; stat++)` |  | pending |
| `save.fread_pet.break.006` | 1252 | `break;` |  | pending |
| `save.fread_pet.break.007` | 1254 | `break;` |  | pending |
| `save.fread_pet.case.003` | 1256 | `case 'C':` |  | pending |
| `save.fread_pet.break.008` | 1259 | `break;` |  | pending |
| `save.fread_pet.case.004` | 1261 | `case 'D':` |  | pending |
| `save.fread_pet.break.009` | 1264 | `break;` |  | pending |
| `save.fread_pet.case.005` | 1266 | `case 'E':` |  | pending |
| `save.fread_pet.if.010` | 1267 | `if (!str_cmp(word,"End"))` |  | pending |
| `save.fread_pet.if.011` | 1275 | `if (percent > 0 && !IS_AFFECTED(ch,AFF_POISON)     		&&  !IS_AFFECTED(ch,AFF_PLAGUE))` |  | pending |
| `save.fread_pet.and.001` | 1275 | `&& !IS_AFFECTED(ch,AFF_POISON)` |  | pending |
| `save.fread_pet.and.002` | 1276 | `&&  !IS_AFFECTED(ch,AFF_PLAGUE))` |  | pending |
| `save.fread_pet.return.001` | 1283 | `return;` |  | pending |
| `save.fread_pet.break.010` | 1286 | `break;` |  | pending |
| `save.fread_pet.case.006` | 1288 | `case 'G':` |  | pending |
| `save.fread_pet.break.011` | 1290 | `break;` |  | pending |
| `save.fread_pet.case.007` | 1292 | `case 'H':` |  | pending |
| `save.fread_pet.if.012` | 1295 | `if (!str_cmp(word,"HMV"))` |  | pending |
| `save.fread_pet.break.012` | 1304 | `break;` |  | pending |
| `save.fread_pet.break.013` | 1306 | `break;` |  | pending |
| `save.fread_pet.case.008` | 1308 | `case 'L':` |  | pending |
| `save.fread_pet.break.014` | 1312 | `break;` |  | pending |
| `save.fread_pet.case.009` | 1314 | `case 'N':` |  | pending |
| `save.fread_pet.break.015` | 1316 | `break;` |  | pending |
| `save.fread_pet.case.010` | 1318 | `case 'P':` |  | pending |
| `save.fread_pet.break.016` | 1320 | `break;` |  | pending |
| `save.fread_pet.case.011` | 1322 | `case 'R':` |  | pending |
| `save.fread_pet.break.017` | 1324 | `break;` |  | pending |
| `save.fread_pet.case.012` | 1326 | `case 'S' :` |  | pending |
| `save.fread_pet.break.018` | 1331 | `break;` |  | pending |
| `save.fread_pet.if.013` | 1333 | `if ( !fMatch )` |  | pending |

## fread_obj

[Source line 1345](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:1345); ends at line 1665. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_char_obj: `src/save.c:615` (lexical_call_candidate).
- load_char_obj: `src/save.c:616` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/save.c:98` (declaration_or_dispatch_reference).

Dependencies: `feof`, `fread_word`, `str_cmp`, `fread_number`, `get_obj_index`, `bug`, `create_object`, `new_obj`, `str_dup`, `UPPER`, `fread_to_eol`, `new_affect`, `skill_lookup`, `KEY`, `fread_string`, `new_extra_descr`, `free_obj`, `extract_obj`, `obj_to_char`, `obj_to_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `save.fread_obj.ternary.001` | 1363 | `? "End" : fread_word( fp );` |  | pending |
| `save.fread_obj.if.001` | 1364 | `if (!str_cmp(word,"Vnum" ))` |  | pending |
| `save.fread_obj.if.002` | 1370 | `if (  get_obj_index( vnum )  == NULL )` |  | pending |
| `save.fread_obj.if.003` | 1382 | `if (obj == NULL)` |  | pending |
| `save.fread_obj.for.001` | 1394 | `for ( ; ; )` |  | pending |
| `save.fread_obj.if.004` | 1396 | `if (first)` |  | pending |
| `save.fread_obj.ternary.002` | 1399 | `? "End" : fread_word( fp );` |  | pending |
| `save.fread_obj.switch.001` | 1402 | `switch ( UPPER(word[0]) )` |  | pending |
| `save.fread_obj.case.001` | 1404 | `case '*':` |  | pending |
| `save.fread_obj.break.001` | 1407 | `break;` |  | pending |
| `save.fread_obj.case.002` | 1409 | `case 'A':` |  | pending |
| `save.fread_obj.if.005` | 1410 | `if (!str_cmp(word,"AffD"))` |  | pending |
| `save.fread_obj.if.006` | 1418 | `if (sn < 0)` |  | pending |
| `save.fread_obj.break.002` | 1431 | `break;` |  | pending |
| `save.fread_obj.if.007` | 1433 | `if (!str_cmp(word,"Affc"))` |  | pending |
| `save.fread_obj.if.008` | 1441 | `if (sn < 0)` |  | pending |
| `save.fread_obj.break.003` | 1455 | `break;` |  | pending |
| `save.fread_obj.break.004` | 1457 | `break;` |  | pending |
| `save.fread_obj.case.003` | 1459 | `case 'C':` |  | pending |
| `save.fread_obj.break.005` | 1462 | `break;` |  | pending |
| `save.fread_obj.case.004` | 1464 | `case 'D':` |  | pending |
| `save.fread_obj.break.006` | 1467 | `break;` |  | pending |
| `save.fread_obj.case.005` | 1469 | `case 'E':` |  | pending |
| `save.fread_obj.if.009` | 1471 | `if ( !str_cmp( word, "Enchanted"))` |  | pending |
| `save.fread_obj.break.007` | 1475 | `break;` |  | pending |
| `save.fread_obj.if.010` | 1481 | `if ( !str_cmp( word, "ExtraDescr" ) \|\| !str_cmp(word,"ExDe"))` |  | pending |
| `save.fread_obj.or.001` | 1481 | `\|\| !str_cmp(word,"ExDe"))` |  | pending |
| `save.fread_obj.if.011` | 1494 | `if ( !str_cmp( word, "End" ) )` |  | pending |
| `save.fread_obj.if.012` | 1496 | `if ( !fNest \|\| !fVnum \|\| obj->pIndexData == NULL)` |  | pending |
| `save.fread_obj.or.002` | 1496 | `\|\| !fVnum \|\| obj->pIndexData == NULL)` |  | pending |
| `save.fread_obj.or.003` | 1496 | `\|\| obj->pIndexData == NULL)` |  | pending |
| `save.fread_obj.return.001` | 1500 | `return;` |  | pending |
| `save.fread_obj.if.013` | 1504 | `if (!new_format)` |  | pending |
| `save.fread_obj.if.014` | 1511 | `if (!obj->pIndexData->new_format  		    && obj->item_type == ITEM_ARMOR 		    &&  obj->value[1] == 0)` |  | pending |
| `save.fread_obj.and.001` | 1512 | `&& obj->item_type == ITEM_ARMOR` |  | pending |
| `save.fread_obj.and.002` | 1513 | `&&  obj->value[1] == 0)` |  | pending |
| `save.fread_obj.if.015` | 1518 | `if (make_new)` |  | pending |
| `save.fread_obj.if.016` | 1528 | `if ( iNest == 0 \|\| rgObjNest[iNest] == NULL )` |  | pending |
| `save.fread_obj.or.004` | 1528 | `\|\| rgObjNest[iNest] == NULL )` |  | pending |
| `save.fread_obj.return.002` | 1532 | `return;` |  | pending |
| `save.fread_obj.break.008` | 1535 | `break;` |  | pending |
| `save.fread_obj.case.006` | 1537 | `case 'I':` |  | pending |
| `save.fread_obj.break.009` | 1540 | `break;` |  | pending |
| `save.fread_obj.case.007` | 1542 | `case 'L':` |  | pending |
| `save.fread_obj.break.010` | 1545 | `break;` |  | pending |
| `save.fread_obj.case.008` | 1547 | `case 'N':` |  | pending |
| `save.fread_obj.if.017` | 1550 | `if ( !str_cmp( word, "Nest" ) )` |  | pending |
| `save.fread_obj.if.018` | 1553 | `if ( iNest < 0 \|\| iNest >= MAX_NEST )` |  | pending |
| `save.fread_obj.or.005` | 1553 | `\|\| iNest >= MAX_NEST )` |  | pending |
| `save.fread_obj.break.011` | 1564 | `break;` |  | pending |
| `save.fread_obj.case.009` | 1566 | `case 'O':` |  | pending |
| `save.fread_obj.if.019` | 1567 | `if ( !str_cmp( word,"Oldstyle" ) )` |  | pending |
| `save.fread_obj.if.020` | 1569 | `if (obj->pIndexData != NULL && obj->pIndexData->new_format)` |  | pending |
| `save.fread_obj.and.003` | 1569 | `&& obj->pIndexData->new_format)` |  | pending |
| `save.fread_obj.break.012` | 1573 | `break;` |  | pending |
| `save.fread_obj.case.010` | 1576 | `case 'S':` |  | pending |
| `save.fread_obj.if.021` | 1580 | `if ( !str_cmp( word, "Spell" ) )` |  | pending |
| `save.fread_obj.if.022` | 1587 | `if ( iValue < 0 \|\| iValue > 3 )` |  | pending |
| `save.fread_obj.or.006` | 1587 | `\|\| iValue > 3 )` |  | pending |
| `save.fread_obj.if.023` | 1591 | `if ( sn < 0 )` |  | pending |
| `save.fread_obj.break.013` | 1600 | `break;` |  | pending |
| `save.fread_obj.break.014` | 1603 | `break;` |  | pending |
| `save.fread_obj.case.011` | 1605 | `case 'T':` |  | pending |
| `save.fread_obj.break.015` | 1608 | `break;` |  | pending |
| `save.fread_obj.case.012` | 1610 | `case 'V':` |  | pending |
| `save.fread_obj.if.024` | 1611 | `if ( !str_cmp( word, "Values" ) \|\| !str_cmp(word,"Vals"))` |  | pending |
| `save.fread_obj.or.007` | 1611 | `\|\| !str_cmp(word,"Vals"))` |  | pending |
| `save.fread_obj.if.025` | 1617 | `if (obj->item_type == ITEM_WEAPON && obj->value[0] == 0)` |  | pending |
| `save.fread_obj.and.004` | 1617 | `&& obj->value[0] == 0)` |  | pending |
| `save.fread_obj.break.016` | 1620 | `break;` |  | pending |
| `save.fread_obj.if.026` | 1623 | `if ( !str_cmp( word, "Val" ) )` |  | pending |
| `save.fread_obj.break.017` | 1631 | `break;` |  | pending |
| `save.fread_obj.if.027` | 1634 | `if ( !str_cmp( word, "Vnum" ) )` |  | pending |
| `save.fread_obj.if.028` | 1639 | `if ( ( obj->pIndexData = get_obj_index( vnum ) ) == NULL )` |  | pending |
| `save.fread_obj.break.018` | 1644 | `break;` |  | pending |
| `save.fread_obj.break.019` | 1646 | `break;` |  | pending |
| `save.fread_obj.case.013` | 1648 | `case 'W':` |  | pending |
| `save.fread_obj.break.020` | 1655 | `break;` |  | pending |
| `save.fread_obj.if.029` | 1659 | `if ( !fMatch )` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 29: `#include <types.h>` — pending configuration/reachability review.
- Line 30: `#else` — pending configuration/reachability review.
- Line 31: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 32: `#endif` — pending configuration/reachability review.
- Line 33: `#include <ctype.h>` — pending configuration/reachability review.
- Line 34: `#include <stdio.h>` — pending configuration/reachability review.
- Line 35: `#include <string.h>` — pending configuration/reachability review.
- Line 36: `#include <time.h>` — pending configuration/reachability review.
- Line 37: `#include <malloc.h>` — pending configuration/reachability review.
- Line 38: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 39: `#include "merc.h"` — pending configuration/reachability review.
- Line 40: `#include "recycle.h"` — pending configuration/reachability review.
- Line 41: `#include "lookup.h"` — pending configuration/reachability review.
- Line 42: `#include "tables.h"` — pending configuration/reachability review.
- Line 44: `#if !defined(macintosh)` — pending configuration/reachability review.
- Line 46: `#endif` — pending configuration/reachability review.
- Line 84: `#define MAX_NEST	100` — pending configuration/reachability review.
- Line 118: `#if defined(unix)` — pending configuration/reachability review.
- Line 135: `#endif` — pending configuration/reachability review.
- Line 575: `#if defined(unix)` — pending configuration/reachability review.
- Line 584: `#endif` — pending configuration/reachability review.
- Line 702: `#if defined(KEY)` — pending configuration/reachability review.
- Line 703: `#undef KEY` — pending configuration/reachability review.
- Line 704: `#endif` — pending configuration/reachability review.
- Line 706: `#define KEY( literal, field, value )					\ 				if ( !str_cmp( word, literal ) )	\ 				{					\ 				    field  = value;			\ 				    fMatch = TRUE;			\ 				    break;				\ 				}` — pending configuration/reachability review.
- Line 715: `#if defined(KEYS)` — pending configuration/reachability review.
- Line 716: `#undef KEYS` — pending configuration/reachability review.
- Line 717: `#endif` — pending configuration/reachability review.
- Line 719: `#define KEYS( literal, field, value )					\ 				if ( !str_cmp( word, literal ) )	\ 				{					\ 				    free_string(field);			\ 				    field  = value;			\ 				    fMatch = TRUE;			\ 				    break;				\ 				}` — pending configuration/reachability review.

## Static tables


## Commented code candidates


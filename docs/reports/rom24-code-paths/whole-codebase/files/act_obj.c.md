# src/act_obj.c

Role: translation_unit. Disposition: **pending**. SHA-256: `3b0876d4686643d00579744ab196e60b1b894ac3f1f55256fac600a189cff338`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## can_loot

[Source line 58](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:58); ends at line 86. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- get_obj: `src/act_obj.c:117` (lexical_call_candidate).
- do_get: `src/act_obj.c:280` (lexical_call_candidate).
- spec_janitor: `src/special.c:861` (lexical_call_candidate).
- mobile_update: `src/update.c:424` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2088` (declaration_or_dispatch_reference).

Dependencies: `IS_IMMORTAL`, `str_cmp`, `IS_NPC`, `IS_SET`, `is_same_group`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.can_loot.if.001` | 62 | `if (IS_IMMORTAL(ch))` |  | pending |
| `act_obj.can_loot.return.001` | 63 | `return TRUE;` |  | pending |
| `act_obj.can_loot.if.002` | 65 | `if (!obj->owner \|\| obj->owner == NULL)` |  | pending |
| `act_obj.can_loot.or.001` | 65 | `\|\| obj->owner == NULL)` |  | pending |
| `act_obj.can_loot.return.002` | 66 | `return TRUE;` |  | pending |
| `act_obj.can_loot.for.001` | 69 | `for ( wch = char_list; wch != NULL ; wch = wch->next )` |  | pending |
| `act_obj.can_loot.if.003` | 70 | `if (!str_cmp(wch->name,obj->owner))` |  | pending |
| `act_obj.can_loot.if.004` | 73 | `if (owner == NULL)` |  | pending |
| `act_obj.can_loot.return.003` | 74 | `return TRUE;` |  | pending |
| `act_obj.can_loot.if.005` | 76 | `if (!str_cmp(ch->name,owner->name))` |  | pending |
| `act_obj.can_loot.return.004` | 77 | `return TRUE;` |  | pending |
| `act_obj.can_loot.if.006` | 79 | `if (!IS_NPC(owner) && IS_SET(owner->act,PLR_CANLOOT))` |  | pending |
| `act_obj.can_loot.and.001` | 79 | `&& IS_SET(owner->act,PLR_CANLOOT))` |  | pending |
| `act_obj.can_loot.return.005` | 80 | `return TRUE;` |  | pending |
| `act_obj.can_loot.if.007` | 82 | `if (is_same_group(ch,owner))` |  | pending |
| `act_obj.can_loot.return.006` | 83 | `return TRUE;` |  | pending |
| `act_obj.can_loot.return.007` | 85 | `return FALSE;` |  | pending |

## get_obj

[Source line 89](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:89); ends at line 188. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_get: `src/act_obj.c:226` (lexical_call_candidate).
- do_get: `src/act_obj.c:239` (lexical_call_candidate).
- do_get: `src/act_obj.c:304` (lexical_call_candidate).
- do_get: `src/act_obj.c:323` (lexical_call_candidate).
- disarm: `src/fight.c:2115` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2089` (declaration_or_dispatch_reference).

Dependencies: `CAN_WEAR`, `send_to_char`, `get_obj_number`, `can_carry_n`, `act`, `get_carry_weight`, `get_obj_weight`, `can_carry_w`, `can_loot`, `get_trust`, `IS_OBJ_STAT`, `REMOVE_BIT`, `obj_from_obj`, `obj_from_room`, `IS_SET`, `IS_AFFECTED`, `is_same_group`, `sprintf`, `do_function`, `extract_obj`, `obj_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.get_obj.if.001` | 96 | `if ( !CAN_WEAR(obj, ITEM_TAKE) )` |  | pending |
| `act_obj.get_obj.return.001` | 99 | `return;` |  | pending |
| `act_obj.get_obj.if.002` | 102 | `if ( ch->carry_number + get_obj_number( obj ) > can_carry_n( ch ) )` |  | pending |
| `act_obj.get_obj.return.002` | 106 | `return;` |  | pending |
| `act_obj.get_obj.if.003` | 109 | `if ((!obj->in_obj \|\| obj->in_obj->carried_by != ch)     &&  (get_carry_weight(ch) + get_obj_weight(obj) > can_carry_w(ch)))` |  | pending |
| `act_obj.get_obj.or.001` | 109 | `\|\| obj->in_obj->carried_by != ch)` |  | pending |
| `act_obj.get_obj.and.001` | 110 | `&&  (get_carry_weight(ch) + get_obj_weight(obj) > can_carry_w(ch)))` |  | pending |
| `act_obj.get_obj.return.003` | 114 | `return;` |  | pending |
| `act_obj.get_obj.if.004` | 117 | `if (!can_loot(ch,obj))` |  | pending |
| `act_obj.get_obj.return.004` | 120 | `return;` |  | pending |
| `act_obj.get_obj.if.005` | 123 | `if (obj->in_room != NULL)` |  | pending |
| `act_obj.get_obj.for.001` | 125 | `for (gch = obj->in_room->people; gch != NULL; gch = gch->next_in_room)` |  | pending |
| `act_obj.get_obj.if.006` | 126 | `if (gch->on == obj)` |  | pending |
| `act_obj.get_obj.return.005` | 130 | `return;` |  | pending |
| `act_obj.get_obj.if.007` | 135 | `if ( container != NULL )` |  | pending |
| `act_obj.get_obj.if.008` | 137 | `if (container->pIndexData->vnum == OBJ_VNUM_PIT 	&&  get_trust(ch) < obj->level)` |  | pending |
| `act_obj.get_obj.and.002` | 138 | `&&  get_trust(ch) < obj->level)` |  | pending |
| `act_obj.get_obj.return.006` | 141 | `return;` |  | pending |
| `act_obj.get_obj.if.009` | 144 | `if (container->pIndexData->vnum == OBJ_VNUM_PIT 	&&  !CAN_WEAR(container, ITEM_TAKE) 	&&  !IS_OBJ_STAT(obj,ITEM_HAD_TIMER))` |  | pending |
| `act_obj.get_obj.and.003` | 145 | `&&  !CAN_WEAR(container, ITEM_TAKE)` |  | pending |
| `act_obj.get_obj.and.004` | 146 | `&&  !IS_OBJ_STAT(obj,ITEM_HAD_TIMER))` |  | pending |
| `act_obj.get_obj.if.010` | 160 | `if ( obj->item_type == ITEM_MONEY)` |  | pending |
| `act_obj.get_obj.if.011` | 164 | `if (IS_SET(ch->act,PLR_AUTOSPLIT))` |  | pending |
| `act_obj.get_obj.for.002` | 167 | `for (gch = ch->in_room->people; gch != NULL; gch = gch->next_in_room )` |  | pending |
| `act_obj.get_obj.if.012` | 169 | `if (!IS_AFFECTED(gch,AFF_CHARM) && is_same_group( gch, ch ) )` |  | pending |
| `act_obj.get_obj.and.005` | 169 | `&& is_same_group( gch, ch ) )` |  | pending |
| `act_obj.get_obj.if.013` | 173 | `if ( members > 1 && (obj->value[0] > 1 \|\| obj->value[1]))` |  | pending |
| `act_obj.get_obj.and.006` | 173 | `&& (obj->value[0] > 1 \|\| obj->value[1]))` |  | pending |
| `act_obj.get_obj.or.002` | 173 | `\|\| obj->value[1]))` |  | pending |
| `act_obj.get_obj.return.007` | 187 | `return;` |  | pending |

## do_get

[Source line 192](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:192); ends at line 340. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:919` (function_symbol_reference_candidate).
- damage: `src/fight.c:929` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:86` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:226` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:136` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `str_cmp`, `send_to_char`, `str_prefix`, `get_obj_list`, `act`, `get_obj`, `is_name`, `can_see_obj`, `get_obj_here`, `can_loot`, `IS_SET`, `IS_IMMORTAL`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_get.if.001` | 204 | `if (!str_cmp(arg2,"from"))` |  | pending |
| `act_obj.do_get.if.002` | 208 | `if ( arg1[0] == '\0' )` |  | pending |
| `act_obj.do_get.return.001` | 211 | `return;` |  | pending |
| `act_obj.do_get.if.003` | 214 | `if ( arg2[0] == '\0' )` |  | pending |
| `act_obj.do_get.if.004` | 216 | `if ( str_cmp( arg1, "all" ) && str_prefix( "all.", arg1 ) )` |  | pending |
| `act_obj.do_get.and.001` | 216 | `&& str_prefix( "all.", arg1 ) )` |  | pending |
| `act_obj.do_get.if.005` | 220 | `if ( obj == NULL )` |  | pending |
| `act_obj.do_get.return.002` | 223 | `return;` |  | pending |
| `act_obj.do_get.for.001` | 232 | `for ( obj = ch->in_room->contents; obj != NULL; obj = obj_next )` |  | pending |
| `act_obj.do_get.if.006` | 235 | `if ( ( arg1[3] == '\0' \|\| is_name( &arg1[4], obj->name ) ) 		&&   can_see_obj( ch, obj ) )` |  | pending |
| `act_obj.do_get.or.001` | 235 | `\|\| is_name( &arg1[4], obj->name ) )` |  | pending |
| `act_obj.do_get.and.002` | 236 | `&&   can_see_obj( ch, obj ) )` |  | pending |
| `act_obj.do_get.if.007` | 243 | `if ( !found )` |  | pending |
| `act_obj.do_get.if.008` | 245 | `if ( arg1[3] == '\0' )` |  | pending |
| `act_obj.do_get.if.009` | 255 | `if ( !str_cmp( arg2, "all" ) \|\| !str_prefix( "all.", arg2 ) )` |  | pending |
| `act_obj.do_get.or.002` | 255 | `\|\| !str_prefix( "all.", arg2 ) )` |  | pending |
| `act_obj.do_get.return.003` | 258 | `return;` |  | pending |
| `act_obj.do_get.if.010` | 261 | `if ( ( container = get_obj_here( ch, arg2 ) ) == NULL )` |  | pending |
| `act_obj.do_get.return.004` | 264 | `return;` |  | pending |
| `act_obj.do_get.switch.001` | 267 | `switch ( container->item_type )` |  | pending |
| `act_obj.do_get.default.001` | 269 | `default:` |  | pending |
| `act_obj.do_get.return.005` | 271 | `return;` |  | pending |
| `act_obj.do_get.case.001` | 273 | `case ITEM_CONTAINER:` |  | pending |
| `act_obj.do_get.case.002` | 274 | `case ITEM_CORPSE_NPC:` |  | pending |
| `act_obj.do_get.break.001` | 275 | `break;` |  | pending |
| `act_obj.do_get.case.003` | 277 | `case ITEM_CORPSE_PC:` |  | pending |
| `act_obj.do_get.if.011` | 280 | `if (!can_loot(ch,container))` |  | pending |
| `act_obj.do_get.return.006` | 283 | `return;` |  | pending |
| `act_obj.do_get.if.012` | 288 | `if ( IS_SET(container->value[1], CONT_CLOSED) )` |  | pending |
| `act_obj.do_get.return.007` | 291 | `return;` |  | pending |
| `act_obj.do_get.if.013` | 294 | `if ( str_cmp( arg1, "all" ) && str_prefix( "all.", arg1 ) )` |  | pending |
| `act_obj.do_get.and.003` | 294 | `&& str_prefix( "all.", arg1 ) )` |  | pending |
| `act_obj.do_get.if.014` | 298 | `if ( obj == NULL )` |  | pending |
| `act_obj.do_get.return.008` | 302 | `return;` |  | pending |
| `act_obj.do_get.for.002` | 310 | `for ( obj = container->contains; obj != NULL; obj = obj_next )` |  | pending |
| `act_obj.do_get.if.015` | 313 | `if ( ( arg1[3] == '\0' \|\| is_name( &arg1[4], obj->name ) ) 		&&   can_see_obj( ch, obj ) )` |  | pending |
| `act_obj.do_get.or.003` | 313 | `\|\| is_name( &arg1[4], obj->name ) )` |  | pending |
| `act_obj.do_get.and.004` | 314 | `&&   can_see_obj( ch, obj ) )` |  | pending |
| `act_obj.do_get.if.016` | 317 | `if (container->pIndexData->vnum == OBJ_VNUM_PIT 		    &&  !IS_IMMORTAL(ch))` |  | pending |
| `act_obj.do_get.and.005` | 318 | `&&  !IS_IMMORTAL(ch))` |  | pending |
| `act_obj.do_get.return.009` | 321 | `return;` |  | pending |
| `act_obj.do_get.if.017` | 327 | `if ( !found )` |  | pending |
| `act_obj.do_get.if.018` | 329 | `if ( arg1[3] == '\0' )` |  | pending |
| `act_obj.do_get.return.010` | 339 | `return;` |  | pending |

## do_put

[Source line 344](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:344); ends at line 486. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:221` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:209` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `str_cmp`, `send_to_char`, `str_prefix`, `get_obj_here`, `act`, `IS_SET`, `get_obj_carry`, `can_drop_obj`, `WEIGHT_MULT`, `get_obj_weight`, `get_true_weight`, `CAN_WEAR`, `SET_BIT`, `number_range`, `obj_from_char`, `obj_to_obj`, `is_name`, `can_see_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_put.if.001` | 355 | `if (!str_cmp(arg2,"in") \|\| !str_cmp(arg2,"on"))` |  | pending |
| `act_obj.do_put.or.001` | 355 | `\|\| !str_cmp(arg2,"on"))` |  | pending |
| `act_obj.do_put.if.002` | 358 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' )` |  | pending |
| `act_obj.do_put.or.002` | 358 | `\|\| arg2[0] == '\0' )` |  | pending |
| `act_obj.do_put.return.001` | 361 | `return;` |  | pending |
| `act_obj.do_put.if.003` | 364 | `if ( !str_cmp( arg2, "all" ) \|\| !str_prefix( "all.", arg2 ) )` |  | pending |
| `act_obj.do_put.or.003` | 364 | `\|\| !str_prefix( "all.", arg2 ) )` |  | pending |
| `act_obj.do_put.return.002` | 367 | `return;` |  | pending |
| `act_obj.do_put.if.004` | 370 | `if ( ( container = get_obj_here( ch, arg2 ) ) == NULL )` |  | pending |
| `act_obj.do_put.return.003` | 373 | `return;` |  | pending |
| `act_obj.do_put.if.005` | 376 | `if ( container->item_type != ITEM_CONTAINER )` |  | pending |
| `act_obj.do_put.return.004` | 379 | `return;` |  | pending |
| `act_obj.do_put.if.006` | 382 | `if ( IS_SET(container->value[1], CONT_CLOSED) )` |  | pending |
| `act_obj.do_put.return.005` | 385 | `return;` |  | pending |
| `act_obj.do_put.if.007` | 388 | `if ( str_cmp( arg1, "all" ) && str_prefix( "all.", arg1 ) )` |  | pending |
| `act_obj.do_put.and.001` | 388 | `&& str_prefix( "all.", arg1 ) )` |  | pending |
| `act_obj.do_put.if.008` | 391 | `if ( ( obj = get_obj_carry( ch, arg1, ch ) ) == NULL )` |  | pending |
| `act_obj.do_put.return.006` | 394 | `return;` |  | pending |
| `act_obj.do_put.if.009` | 397 | `if ( obj == container )` |  | pending |
| `act_obj.do_put.return.007` | 400 | `return;` |  | pending |
| `act_obj.do_put.if.010` | 403 | `if ( !can_drop_obj( ch, obj ) )` |  | pending |
| `act_obj.do_put.return.008` | 406 | `return;` |  | pending |
| `act_obj.do_put.if.011` | 409 | `if (WEIGHT_MULT(obj) != 100)` |  | pending |
| `act_obj.do_put.return.009` | 412 | `return;` |  | pending |
| `act_obj.do_put.if.012` | 415 | `if (get_obj_weight( obj ) + get_true_weight( container ) 	     > (container->value[0] * 10)  	\|\|  get_obj_weight(obj) > (container->value[3] * 10))` |  | pending |
| `act_obj.do_put.or.004` | 417 | `\|\|  get_obj_weight(obj) > (container->value[3] * 10))` |  | pending |
| `act_obj.do_put.return.010` | 420 | `return;` |  | pending |
| `act_obj.do_put.if.013` | 423 | `if (container->pIndexData->vnum == OBJ_VNUM_PIT  	&&  !CAN_WEAR(container,ITEM_TAKE))` |  | pending |
| `act_obj.do_put.and.002` | 424 | `&&  !CAN_WEAR(container,ITEM_TAKE))` |  | pending |
| `act_obj.do_put.if.014` | 425 | `if (obj->timer)` |  | pending |
| `act_obj.do_put.if.015` | 433 | `if (IS_SET(container->value[1],CONT_PUT_ON))` |  | pending |
| `act_obj.do_put.for.001` | 447 | `for ( obj = ch->carrying; obj != NULL; obj = obj_next )` |  | pending |
| `act_obj.do_put.if.016` | 451 | `if ( ( arg1[3] == '\0' \|\| is_name( &arg1[4], obj->name ) ) 	    &&   can_see_obj( ch, obj ) 	    &&   WEIGHT_MULT(obj) == 100 	    &&   obj->wear_loc == WEAR_NONE 	    &&   obj != container 	    &&   can_drop_obj( ch, obj ) 	    &&   get_obj_weight( obj ) + get_true_weight( container ) 		 <= (container->value[0] * 10)  	    &&   get_obj_weight(obj) < (container->value[3] * 10))` |  | pending |
| `act_obj.do_put.or.005` | 451 | `\|\| is_name( &arg1[4], obj->name ) )` |  | pending |
| `act_obj.do_put.and.003` | 452 | `&&   can_see_obj( ch, obj )` |  | pending |
| `act_obj.do_put.and.004` | 453 | `&&   WEIGHT_MULT(obj) == 100` |  | pending |
| `act_obj.do_put.and.005` | 454 | `&&   obj->wear_loc == WEAR_NONE` |  | pending |
| `act_obj.do_put.and.006` | 455 | `&&   obj != container` |  | pending |
| `act_obj.do_put.and.007` | 456 | `&&   can_drop_obj( ch, obj )` |  | pending |
| `act_obj.do_put.and.008` | 457 | `&&   get_obj_weight( obj ) + get_true_weight( container )` |  | pending |
| `act_obj.do_put.and.009` | 459 | `&&   get_obj_weight(obj) < (container->value[3] * 10))` |  | pending |
| `act_obj.do_put.if.017` | 461 | `if (container->pIndexData->vnum == OBJ_VNUM_PIT 	    	&&  !CAN_WEAR(obj, ITEM_TAKE) )` |  | pending |
| `act_obj.do_put.and.010` | 462 | `&&  !CAN_WEAR(obj, ITEM_TAKE) )` |  | pending |
| `act_obj.do_put.if.018` | 463 | `if (obj->timer)` |  | pending |
| `act_obj.do_put.if.019` | 471 | `if (IS_SET(container->value[1],CONT_PUT_ON))` |  | pending |
| `act_obj.do_put.return.011` | 485 | `return;` |  | pending |

## do_drop

[Source line 490](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:490); ends at line 650. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:209` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:118` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `is_number`, `atoi`, `str_cmp`, `extract_obj`, `obj_to_room`, `create_money`, `act`, `str_prefix`, `get_obj_carry`, `can_drop_obj`, `obj_from_char`, `IS_OBJ_STAT`, `is_name`, `can_see_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_drop.if.001` | 499 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_drop.return.001` | 502 | `return;` |  | pending |
| `act_obj.do_drop.if.002` | 505 | `if ( is_number( arg ) )` |  | pending |
| `act_obj.do_drop.if.003` | 512 | `if ( amount <= 0 	\|\| ( str_cmp( arg, "coins" ) && str_cmp( arg, "coin" ) &&  	     str_cmp( arg, "gold"  ) && str_cmp( arg, "silver") ) )` |  | pending |
| `act_obj.do_drop.or.001` | 513 | `\|\| ( str_cmp( arg, "coins" ) && str_cmp( arg, "coin" ) &&` |  | pending |
| `act_obj.do_drop.and.001` | 513 | `&& str_cmp( arg, "coin" ) &&` |  | pending |
| `act_obj.do_drop.and.002` | 513 | `&&` |  | pending |
| `act_obj.do_drop.and.003` | 514 | `&& str_cmp( arg, "silver") ) )` |  | pending |
| `act_obj.do_drop.return.002` | 517 | `return;` |  | pending |
| `act_obj.do_drop.if.004` | 520 | `if ( !str_cmp( arg, "coins") \|\| !str_cmp(arg,"coin")  	\|\|   !str_cmp( arg, "silver"))` |  | pending |
| `act_obj.do_drop.or.002` | 520 | `\|\| !str_cmp(arg,"coin")` |  | pending |
| `act_obj.do_drop.or.003` | 521 | `\|\|   !str_cmp( arg, "silver"))` |  | pending |
| `act_obj.do_drop.if.005` | 523 | `if (ch->silver < amount)` |  | pending |
| `act_obj.do_drop.return.003` | 526 | `return;` |  | pending |
| `act_obj.do_drop.if.006` | 535 | `if (ch->gold < amount)` |  | pending |
| `act_obj.do_drop.return.004` | 538 | `return;` |  | pending |
| `act_obj.do_drop.for.001` | 545 | `for ( obj = ch->in_room->contents; obj != NULL; obj = obj_next )` |  | pending |
| `act_obj.do_drop.switch.001` | 549 | `switch ( obj->pIndexData->vnum )` |  | pending |
| `act_obj.do_drop.case.001` | 551 | `case OBJ_VNUM_SILVER_ONE:` |  | pending |
| `act_obj.do_drop.break.001` | 554 | `break;` |  | pending |
| `act_obj.do_drop.case.002` | 556 | `case OBJ_VNUM_GOLD_ONE:` |  | pending |
| `act_obj.do_drop.break.002` | 559 | `break;` |  | pending |
| `act_obj.do_drop.case.003` | 561 | `case OBJ_VNUM_SILVER_SOME:` |  | pending |
| `act_obj.do_drop.break.003` | 564 | `break;` |  | pending |
| `act_obj.do_drop.case.004` | 566 | `case OBJ_VNUM_GOLD_SOME:` |  | pending |
| `act_obj.do_drop.break.004` | 569 | `break;` |  | pending |
| `act_obj.do_drop.case.005` | 571 | `case OBJ_VNUM_COINS:` |  | pending |
| `act_obj.do_drop.break.005` | 575 | `break;` |  | pending |
| `act_obj.do_drop.return.005` | 582 | `return;` |  | pending |
| `act_obj.do_drop.if.007` | 585 | `if ( str_cmp( arg, "all" ) && str_prefix( "all.", arg ) )` |  | pending |
| `act_obj.do_drop.and.004` | 585 | `&& str_prefix( "all.", arg ) )` |  | pending |
| `act_obj.do_drop.if.008` | 588 | `if ( ( obj = get_obj_carry( ch, arg, ch ) ) == NULL )` |  | pending |
| `act_obj.do_drop.return.006` | 591 | `return;` |  | pending |
| `act_obj.do_drop.if.009` | 594 | `if ( !can_drop_obj( ch, obj ) )` |  | pending |
| `act_obj.do_drop.return.007` | 597 | `return;` |  | pending |
| `act_obj.do_drop.if.010` | 604 | `if (IS_OBJ_STAT(obj,ITEM_MELT_DROP))` |  | pending |
| `act_obj.do_drop.for.002` | 615 | `for ( obj = ch->carrying; obj != NULL; obj = obj_next )` |  | pending |
| `act_obj.do_drop.if.011` | 619 | `if ( ( arg[3] == '\0' \|\| is_name( &arg[4], obj->name ) ) 	    &&   can_see_obj( ch, obj ) 	    &&   obj->wear_loc == WEAR_NONE 	    &&   can_drop_obj( ch, obj ) )` |  | pending |
| `act_obj.do_drop.or.004` | 619 | `\|\| is_name( &arg[4], obj->name ) )` |  | pending |
| `act_obj.do_drop.and.005` | 620 | `&&   can_see_obj( ch, obj )` |  | pending |
| `act_obj.do_drop.and.006` | 621 | `&&   obj->wear_loc == WEAR_NONE` |  | pending |
| `act_obj.do_drop.and.007` | 622 | `&&   can_drop_obj( ch, obj ) )` |  | pending |
| `act_obj.do_drop.if.012` | 629 | `if (IS_OBJ_STAT(obj,ITEM_MELT_DROP))` |  | pending |
| `act_obj.do_drop.if.013` | 638 | `if ( !found )` |  | pending |
| `act_obj.do_drop.if.014` | 640 | `if ( arg[3] == '\0' )` |  | pending |
| `act_obj.do_drop.return.008` | 649 | `return;` |  | pending |

## do_give

[Source line 654](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:654); ends at line 823. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_give: `src/act_obj.c:746` (function_symbol_reference_candidate).
- do_give: `src/act_obj.c:752` (function_symbol_reference_candidate).
- do_give: `src/act_obj.c:757` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:213` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:137` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `is_number`, `atoi`, `str_cmp`, `get_char_room`, `sprintf`, `act`, `IS_NPC`, `IS_SET`, `can_see`, `do_function`, `get_obj_carry`, `can_drop_obj`, `get_obj_number`, `can_carry_n`, `get_carry_weight`, `get_obj_weight`, `can_carry_w`, `can_see_obj`, `obj_from_char`, `obj_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_give.if.001` | 665 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' )` |  | pending |
| `act_obj.do_give.or.001` | 665 | `\|\| arg2[0] == '\0' )` |  | pending |
| `act_obj.do_give.return.001` | 668 | `return;` |  | pending |
| `act_obj.do_give.if.002` | 671 | `if ( is_number( arg1 ) )` |  | pending |
| `act_obj.do_give.if.003` | 678 | `if ( amount <= 0 	\|\| ( str_cmp( arg2, "coins" ) && str_cmp( arg2, "coin" ) &&  	     str_cmp( arg2, "gold"  ) && str_cmp( arg2, "silver")) )` |  | pending |
| `act_obj.do_give.or.002` | 679 | `\|\| ( str_cmp( arg2, "coins" ) && str_cmp( arg2, "coin" ) &&` |  | pending |
| `act_obj.do_give.and.001` | 679 | `&& str_cmp( arg2, "coin" ) &&` |  | pending |
| `act_obj.do_give.and.002` | 679 | `&&` |  | pending |
| `act_obj.do_give.and.003` | 680 | `&& str_cmp( arg2, "silver")) )` |  | pending |
| `act_obj.do_give.return.002` | 683 | `return;` |  | pending |
| `act_obj.do_give.if.004` | 689 | `if ( arg2[0] == '\0' )` |  | pending |
| `act_obj.do_give.return.003` | 692 | `return;` |  | pending |
| `act_obj.do_give.if.005` | 695 | `if ( ( victim = get_char_room( ch, arg2 ) ) == NULL )` |  | pending |
| `act_obj.do_give.return.004` | 698 | `return;` |  | pending |
| `act_obj.do_give.if.006` | 701 | `if ( (!silver && ch->gold < amount) \|\| (silver && ch->silver < amount) )` |  | pending |
| `act_obj.do_give.and.004` | 701 | `&& ch->gold < amount) \|\| (silver && ch->silver < amount) )` |  | pending |
| `act_obj.do_give.or.003` | 701 | `\|\| (silver && ch->silver < amount) )` |  | pending |
| `act_obj.do_give.and.005` | 701 | `&& ch->silver < amount) )` |  | pending |
| `act_obj.do_give.return.005` | 704 | `return;` |  | pending |
| `act_obj.do_give.if.007` | 707 | `if (silver)` |  | pending |
| `act_obj.do_give.ternary.001` | 718 | `? "silver" : "gold");` |  | pending |
| `act_obj.do_give.ternary.002` | 721 | `? "silver" : "gold");` |  | pending |
| `act_obj.do_give.if.008` | 724 | `if (IS_NPC(victim) && IS_SET(victim->act,ACT_IS_CHANGER))` |  | pending |
| `act_obj.do_give.and.006` | 724 | `&& IS_SET(victim->act,ACT_IS_CHANGER))` |  | pending |
| `act_obj.do_give.ternary.003` | 728 | `? 95 * amount / 100 / 100` |  | pending |
| `act_obj.do_give.if.009` | 732 | `if (!silver && change > victim->silver)` |  | pending |
| `act_obj.do_give.and.007` | 732 | `&& change > victim->silver)` |  | pending |
| `act_obj.do_give.if.010` | 735 | `if (silver && change > victim->gold)` |  | pending |
| `act_obj.do_give.and.008` | 735 | `&& change > victim->gold)` |  | pending |
| `act_obj.do_give.if.011` | 738 | `if (change < 1 && can_see(victim,ch))` |  | pending |
| `act_obj.do_give.and.009` | 738 | `&& can_see(victim,ch))` |  | pending |
| `act_obj.do_give.ternary.004` | 745 | `? "silver" : "gold",ch->name);` |  | pending |
| `act_obj.do_give.if.012` | 748 | `if (can_see(victim,ch))` |  | pending |
| `act_obj.do_give.ternary.005` | 751 | `? "gold" : "silver",ch->name);` |  | pending |
| `act_obj.do_give.if.013` | 753 | `if (silver)` |  | pending |
| `act_obj.do_give.return.006` | 764 | `return;` |  | pending |
| `act_obj.do_give.if.014` | 767 | `if ( ( obj = get_obj_carry( ch, arg1, ch ) ) == NULL )` |  | pending |
| `act_obj.do_give.return.007` | 770 | `return;` |  | pending |
| `act_obj.do_give.if.015` | 773 | `if ( obj->wear_loc != WEAR_NONE )` |  | pending |
| `act_obj.do_give.return.008` | 776 | `return;` |  | pending |
| `act_obj.do_give.if.016` | 779 | `if ( ( victim = get_char_room( ch, arg2 ) ) == NULL )` |  | pending |
| `act_obj.do_give.return.009` | 782 | `return;` |  | pending |
| `act_obj.do_give.if.017` | 785 | `if (IS_NPC(victim) && victim->pIndexData->pShop != NULL)` |  | pending |
| `act_obj.do_give.and.010` | 785 | `&& victim->pIndexData->pShop != NULL)` |  | pending |
| `act_obj.do_give.return.010` | 790 | `return;` |  | pending |
| `act_obj.do_give.if.018` | 793 | `if ( !can_drop_obj( ch, obj ) )` |  | pending |
| `act_obj.do_give.return.011` | 796 | `return;` |  | pending |
| `act_obj.do_give.if.019` | 799 | `if ( victim->carry_number + get_obj_number( obj ) > can_carry_n( victim ) )` |  | pending |
| `act_obj.do_give.return.012` | 802 | `return;` |  | pending |
| `act_obj.do_give.if.020` | 805 | `if (get_carry_weight(victim) + get_obj_weight(obj) > can_carry_w( victim ) )` |  | pending |
| `act_obj.do_give.return.013` | 808 | `return;` |  | pending |
| `act_obj.do_give.if.021` | 811 | `if ( !can_see_obj( victim, obj ) )` |  | pending |
| `act_obj.do_give.return.014` | 814 | `return;` |  | pending |
| `act_obj.do_give.return.015` | 822 | `return;` |  | pending |

## do_envenom

[Source line 827](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:827); ends at line 939. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:211` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:125` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `get_obj_list`, `get_skill`, `IS_OBJ_STAT`, `act`, `number_percent`, `check_improve`, `WAIT_STATE`, `IS_WEAPON_STAT`, `affect_to_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_envenom.if.001` | 834 | `if (argument[0] == '\0')` |  | pending |
| `act_obj.do_envenom.return.001` | 837 | `return;` |  | pending |
| `act_obj.do_envenom.if.002` | 842 | `if (obj== NULL)` |  | pending |
| `act_obj.do_envenom.return.002` | 845 | `return;` |  | pending |
| `act_obj.do_envenom.if.003` | 848 | `if ((skill = get_skill(ch,gsn_envenom)) < 1)` |  | pending |
| `act_obj.do_envenom.return.003` | 851 | `return;` |  | pending |
| `act_obj.do_envenom.if.004` | 854 | `if (obj->item_type == ITEM_FOOD \|\| obj->item_type == ITEM_DRINK_CON)` |  | pending |
| `act_obj.do_envenom.or.001` | 854 | `\|\| obj->item_type == ITEM_DRINK_CON)` |  | pending |
| `act_obj.do_envenom.if.005` | 856 | `if (IS_OBJ_STAT(obj,ITEM_BLESS) \|\| IS_OBJ_STAT(obj,ITEM_BURN_PROOF))` |  | pending |
| `act_obj.do_envenom.or.002` | 856 | `\|\| IS_OBJ_STAT(obj,ITEM_BURN_PROOF))` |  | pending |
| `act_obj.do_envenom.return.004` | 859 | `return;` |  | pending |
| `act_obj.do_envenom.if.006` | 862 | `if (number_percent() < skill)` |  | pending |
| `act_obj.do_envenom.if.007` | 866 | `if (!obj->value[3])` |  | pending |
| `act_obj.do_envenom.return.005` | 872 | `return;` |  | pending |
| `act_obj.do_envenom.if.008` | 876 | `if (!obj->value[3])` |  | pending |
| `act_obj.do_envenom.return.006` | 879 | `return;` |  | pending |
| `act_obj.do_envenom.if.009` | 882 | `if (obj->item_type == ITEM_WEAPON)` |  | pending |
| `act_obj.do_envenom.if.010` | 884 | `if (IS_WEAPON_STAT(obj,WEAPON_FLAMING)         \|\|  IS_WEAPON_STAT(obj,WEAPON_FROST)         \|\|  IS_WEAPON_STAT(obj,WEAPON_VAMPIRIC)         \|\|  IS_WEAPON_STAT(obj,WEAPON_SHARP)         \|\|  IS_WEAPON_STAT(obj,WEAPON_VORPAL)         \|\|  IS_WEAPON_STAT(obj,WEAPON_SHOCKING)         \|\|  IS_OBJ_STAT(obj,ITEM_BLESS) \|\| IS_OBJ_STAT(obj,ITEM_BURN_PROOF))` |  | pending |
| `act_obj.do_envenom.or.003` | 885 | `\|\|  IS_WEAPON_STAT(obj,WEAPON_FROST)` |  | pending |
| `act_obj.do_envenom.or.004` | 886 | `\|\|  IS_WEAPON_STAT(obj,WEAPON_VAMPIRIC)` |  | pending |
| `act_obj.do_envenom.or.005` | 887 | `\|\|  IS_WEAPON_STAT(obj,WEAPON_SHARP)` |  | pending |
| `act_obj.do_envenom.or.006` | 888 | `\|\|  IS_WEAPON_STAT(obj,WEAPON_VORPAL)` |  | pending |
| `act_obj.do_envenom.or.007` | 889 | `\|\|  IS_WEAPON_STAT(obj,WEAPON_SHOCKING)` |  | pending |
| `act_obj.do_envenom.or.008` | 890 | `\|\|  IS_OBJ_STAT(obj,ITEM_BLESS) \|\| IS_OBJ_STAT(obj,ITEM_BURN_PROOF))` |  | pending |
| `act_obj.do_envenom.or.009` | 890 | `\|\| IS_OBJ_STAT(obj,ITEM_BURN_PROOF))` |  | pending |
| `act_obj.do_envenom.return.007` | 893 | `return;` |  | pending |
| `act_obj.do_envenom.if.011` | 896 | `if (obj->value[3] < 0  	\|\|  attack_table[obj->value[3]].damage == DAM_BASH)` |  | pending |
| `act_obj.do_envenom.or.010` | 897 | `\|\|  attack_table[obj->value[3]].damage == DAM_BASH)` |  | pending |
| `act_obj.do_envenom.return.008` | 900 | `return;` |  | pending |
| `act_obj.do_envenom.if.012` | 903 | `if (IS_WEAPON_STAT(obj,WEAPON_POISON))` |  | pending |
| `act_obj.do_envenom.return.009` | 906 | `return;` |  | pending |
| `act_obj.do_envenom.if.013` | 910 | `if (percent < skill)` |  | pending |
| `act_obj.do_envenom.return.010` | 926 | `return;` |  | pending |
| `act_obj.do_envenom.return.011` | 933 | `return;` |  | pending |
| `act_obj.do_envenom.return.012` | 938 | `return;` |  | pending |

## do_fill

[Source line 941](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:941); ends at line 1007. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:212` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:129` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_carry`, `sprintf`, `act`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_fill.if.001` | 951 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_fill.return.001` | 954 | `return;` |  | pending |
| `act_obj.do_fill.if.002` | 957 | `if ( ( obj = get_obj_carry( ch, arg, ch ) ) == NULL )` |  | pending |
| `act_obj.do_fill.return.002` | 960 | `return;` |  | pending |
| `act_obj.do_fill.for.001` | 964 | `for ( fountain = ch->in_room->contents; fountain != NULL; 	fountain = fountain->next_content )` |  | pending |
| `act_obj.do_fill.if.003` | 967 | `if ( fountain->item_type == ITEM_FOUNTAIN )` |  | pending |
| `act_obj.do_fill.break.001` | 970 | `break;` |  | pending |
| `act_obj.do_fill.if.004` | 974 | `if ( !found )` |  | pending |
| `act_obj.do_fill.return.003` | 977 | `return;` |  | pending |
| `act_obj.do_fill.if.005` | 980 | `if ( obj->item_type != ITEM_DRINK_CON )` |  | pending |
| `act_obj.do_fill.return.004` | 983 | `return;` |  | pending |
| `act_obj.do_fill.if.006` | 986 | `if ( obj->value[1] != 0 && obj->value[2] != fountain->value[2] )` |  | pending |
| `act_obj.do_fill.and.001` | 986 | `&& obj->value[2] != fountain->value[2] )` |  | pending |
| `act_obj.do_fill.return.005` | 989 | `return;` |  | pending |
| `act_obj.do_fill.if.007` | 992 | `if ( obj->value[1] >= obj->value[0] )` |  | pending |
| `act_obj.do_fill.return.006` | 995 | `return;` |  | pending |
| `act_obj.do_fill.return.007` | 1006 | `return;` |  | pending |

## do_pour

[Source line 1009](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1009); ends at line 1134. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:220` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:202` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_carry`, `str_cmp`, `sprintf`, `act`, `get_obj_here`, `get_char_room`, `get_eq_char`, `UMIN`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_pour.if.001` | 1018 | `if (arg[0] == '\0' \|\| argument[0] == '\0')` |  | pending |
| `act_obj.do_pour.or.001` | 1018 | `\|\| argument[0] == '\0')` |  | pending |
| `act_obj.do_pour.return.001` | 1021 | `return;` |  | pending |
| `act_obj.do_pour.if.002` | 1025 | `if ((out = get_obj_carry(ch,arg, ch)) == NULL)` |  | pending |
| `act_obj.do_pour.return.002` | 1028 | `return;` |  | pending |
| `act_obj.do_pour.if.003` | 1031 | `if (out->item_type != ITEM_DRINK_CON)` |  | pending |
| `act_obj.do_pour.return.003` | 1034 | `return;` |  | pending |
| `act_obj.do_pour.if.004` | 1037 | `if (!str_cmp(argument,"out"))` |  | pending |
| `act_obj.do_pour.if.005` | 1039 | `if (out->value[1] == 0)` |  | pending |
| `act_obj.do_pour.return.004` | 1042 | `return;` |  | pending |
| `act_obj.do_pour.return.005` | 1054 | `return;` |  | pending |
| `act_obj.do_pour.if.006` | 1057 | `if ((in = get_obj_here(ch,argument)) == NULL)` |  | pending |
| `act_obj.do_pour.if.007` | 1061 | `if (vch == NULL)` |  | pending |
| `act_obj.do_pour.return.006` | 1064 | `return;` |  | pending |
| `act_obj.do_pour.if.008` | 1069 | `if (in == NULL)` |  | pending |
| `act_obj.do_pour.return.007` | 1072 | `return;` |  | pending |
| `act_obj.do_pour.if.009` | 1076 | `if (in->item_type != ITEM_DRINK_CON)` |  | pending |
| `act_obj.do_pour.return.008` | 1079 | `return;` |  | pending |
| `act_obj.do_pour.if.010` | 1082 | `if (in == out)` |  | pending |
| `act_obj.do_pour.return.009` | 1085 | `return;` |  | pending |
| `act_obj.do_pour.if.011` | 1088 | `if (in->value[1] != 0 && in->value[2] != out->value[2])` |  | pending |
| `act_obj.do_pour.and.001` | 1088 | `&& in->value[2] != out->value[2])` |  | pending |
| `act_obj.do_pour.return.010` | 1091 | `return;` |  | pending |
| `act_obj.do_pour.if.012` | 1094 | `if (out->value[1] == 0)` |  | pending |
| `act_obj.do_pour.return.011` | 1097 | `return;` |  | pending |
| `act_obj.do_pour.if.013` | 1100 | `if (in->value[1] >= in->value[0])` |  | pending |
| `act_obj.do_pour.return.012` | 1103 | `return;` |  | pending |
| `act_obj.do_pour.if.014` | 1112 | `if (vch == NULL)` |  | pending |

## do_drink

[Source line 1136](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1136); ends at line 1255. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:208` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:117` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_here`, `IS_NPC`, `bug`, `UMIN`, `IS_IMMORTAL`, `act`, `gain_condition`, `number_fuzzy`, `affect_join`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_drink.if.001` | 1145 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_drink.for.001` | 1147 | `for ( obj = ch->in_room->contents; obj; obj = obj->next_content )` |  | pending |
| `act_obj.do_drink.if.002` | 1149 | `if ( obj->item_type == ITEM_FOUNTAIN )` |  | pending |
| `act_obj.do_drink.break.001` | 1150 | `break;` |  | pending |
| `act_obj.do_drink.if.003` | 1153 | `if ( obj == NULL )` |  | pending |
| `act_obj.do_drink.return.001` | 1156 | `return;` |  | pending |
| `act_obj.do_drink.if.004` | 1161 | `if ( ( obj = get_obj_here( ch, arg ) ) == NULL )` |  | pending |
| `act_obj.do_drink.return.002` | 1164 | `return;` |  | pending |
| `act_obj.do_drink.if.005` | 1168 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_DRUNK] > 10 )` |  | pending |
| `act_obj.do_drink.and.001` | 1168 | `&& ch->pcdata->condition[COND_DRUNK] > 10 )` |  | pending |
| `act_obj.do_drink.return.003` | 1171 | `return;` |  | pending |
| `act_obj.do_drink.switch.001` | 1174 | `switch ( obj->item_type )` |  | pending |
| `act_obj.do_drink.default.001` | 1176 | `default:` |  | pending |
| `act_obj.do_drink.return.004` | 1178 | `return;` |  | pending |
| `act_obj.do_drink.case.001` | 1180 | `case ITEM_FOUNTAIN:` |  | pending |
| `act_obj.do_drink.if.006` | 1181 | `if ( ( liquid = obj->value[2] )  < 0 )` |  | pending |
| `act_obj.do_drink.break.002` | 1187 | `break;` |  | pending |
| `act_obj.do_drink.case.002` | 1189 | `case ITEM_DRINK_CON:` |  | pending |
| `act_obj.do_drink.if.007` | 1190 | `if ( obj->value[1] <= 0 )` |  | pending |
| `act_obj.do_drink.return.005` | 1193 | `return;` |  | pending |
| `act_obj.do_drink.if.008` | 1196 | `if ( ( liquid = obj->value[2] )  < 0 )` |  | pending |
| `act_obj.do_drink.break.003` | 1204 | `break;` |  | pending |
| `act_obj.do_drink.if.009` | 1206 | `if (!IS_NPC(ch) && !IS_IMMORTAL(ch)      &&  ch->pcdata->condition[COND_FULL] > 45)` |  | pending |
| `act_obj.do_drink.and.002` | 1206 | `&& !IS_IMMORTAL(ch)` |  | pending |
| `act_obj.do_drink.and.003` | 1207 | `&&  ch->pcdata->condition[COND_FULL] > 45)` |  | pending |
| `act_obj.do_drink.return.006` | 1210 | `return;` |  | pending |
| `act_obj.do_drink.if.010` | 1227 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_DRUNK]  > 10 )` |  | pending |
| `act_obj.do_drink.and.004` | 1227 | `&& ch->pcdata->condition[COND_DRUNK]  > 10 )` |  | pending |
| `act_obj.do_drink.if.011` | 1229 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_FULL]   > 40 )` |  | pending |
| `act_obj.do_drink.and.005` | 1229 | `&& ch->pcdata->condition[COND_FULL]   > 40 )` |  | pending |
| `act_obj.do_drink.if.012` | 1231 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_THIRST] > 40 )` |  | pending |
| `act_obj.do_drink.and.006` | 1231 | `&& ch->pcdata->condition[COND_THIRST] > 40 )` |  | pending |
| `act_obj.do_drink.if.013` | 1234 | `if ( obj->value[3] != 0 )` |  | pending |
| `act_obj.do_drink.if.014` | 1251 | `if (obj->value[0] > 0)` |  | pending |
| `act_obj.do_drink.return.007` | 1254 | `return;` |  | pending |

## do_eat

[Source line 1259](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1259); ends at line 1340. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:210` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:121` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_carry`, `IS_IMMORTAL`, `IS_NPC`, `act`, `gain_condition`, `number_fuzzy`, `affect_join`, `obj_cast_spell`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_eat.if.001` | 1265 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_eat.return.001` | 1268 | `return;` |  | pending |
| `act_obj.do_eat.if.002` | 1271 | `if ( ( obj = get_obj_carry( ch, arg, ch ) ) == NULL )` |  | pending |
| `act_obj.do_eat.return.002` | 1274 | `return;` |  | pending |
| `act_obj.do_eat.if.003` | 1277 | `if ( !IS_IMMORTAL(ch) )` |  | pending |
| `act_obj.do_eat.if.004` | 1279 | `if ( obj->item_type != ITEM_FOOD && obj->item_type != ITEM_PILL )` |  | pending |
| `act_obj.do_eat.and.001` | 1279 | `&& obj->item_type != ITEM_PILL )` |  | pending |
| `act_obj.do_eat.return.003` | 1282 | `return;` |  | pending |
| `act_obj.do_eat.if.005` | 1285 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_FULL] > 40 )` |  | pending |
| `act_obj.do_eat.and.002` | 1285 | `&& ch->pcdata->condition[COND_FULL] > 40 )` |  | pending |
| `act_obj.do_eat.return.004` | 1288 | `return;` |  | pending |
| `act_obj.do_eat.switch.001` | 1295 | `switch ( obj->item_type )` |  | pending |
| `act_obj.do_eat.case.001` | 1298 | `case ITEM_FOOD:` |  | pending |
| `act_obj.do_eat.if.006` | 1299 | `if ( !IS_NPC(ch) )` |  | pending |
| `act_obj.do_eat.if.007` | 1306 | `if ( condition == 0 && ch->pcdata->condition[COND_HUNGER] > 0 )` |  | pending |
| `act_obj.do_eat.and.003` | 1306 | `&& ch->pcdata->condition[COND_HUNGER] > 0 )` |  | pending |
| `act_obj.do_eat.if.008` | 1308 | `if ( ch->pcdata->condition[COND_FULL] > 40 )` |  | pending |
| `act_obj.do_eat.if.009` | 1312 | `if ( obj->value[3] != 0 )` |  | pending |
| `act_obj.do_eat.break.001` | 1329 | `break;` |  | pending |
| `act_obj.do_eat.case.002` | 1331 | `case ITEM_PILL:` |  | pending |
| `act_obj.do_eat.break.002` | 1335 | `break;` |  | pending |
| `act_obj.do_eat.return.005` | 1339 | `return;` |  | pending |

## remove_obj

[Source line 1347](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1347); ends at line 1367. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- wear_obj: `src/act_obj.c:1392` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1404` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1405` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1433` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1434` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1460` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1470` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1480` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1490` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1500` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1510` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1520` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1530` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1542` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1543` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1575` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1596` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1647` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1657` (lexical_call_candidate).
- do_remove: `src/act_obj.c:1733` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3064` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3113` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_obj.c:46` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/magic.c:48` (declaration_or_dispatch_reference).

Dependencies: `get_eq_char`, `IS_SET`, `act`, `unequip_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.remove_obj.if.001` | 1351 | `if ( ( obj = get_eq_char( ch, iWear ) ) == NULL )` |  | pending |
| `act_obj.remove_obj.return.001` | 1352 | `return TRUE;` |  | pending |
| `act_obj.remove_obj.if.002` | 1354 | `if ( !fReplace )` |  | pending |
| `act_obj.remove_obj.return.002` | 1355 | `return FALSE;` |  | pending |
| `act_obj.remove_obj.if.003` | 1357 | `if ( IS_SET(obj->extra_flags, ITEM_NOREMOVE) )` |  | pending |
| `act_obj.remove_obj.return.003` | 1360 | `return FALSE;` |  | pending |
| `act_obj.remove_obj.return.004` | 1366 | `return TRUE;` |  | pending |

## wear_obj

[Source line 1376](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1376); ends at line 1669. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_wear: `src/act_obj.c:1694` (lexical_call_candidate).
- do_wear: `src/act_obj.c:1706` (lexical_call_candidate).
- spell_floating_disc: `src/magic.c:2794` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_obj.c:47` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/magic.c:49` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `send_to_char`, `act`, `remove_obj`, `equip_char`, `CAN_WEAR`, `get_eq_char`, `bug`, `IS_WEAPON_STAT`, `IS_NPC`, `get_obj_weight`, `get_curr_stat`, `get_weapon_sn`, `get_weapon_skill`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.wear_obj.if.001` | 1380 | `if ( ch->level < obj->level )` |  | pending |
| `act_obj.wear_obj.return.001` | 1387 | `return;` |  | pending |
| `act_obj.wear_obj.if.002` | 1390 | `if ( obj->item_type == ITEM_LIGHT )` |  | pending |
| `act_obj.wear_obj.if.003` | 1392 | `if ( !remove_obj( ch, WEAR_LIGHT, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.002` | 1393 | `return;` |  | pending |
| `act_obj.wear_obj.return.003` | 1397 | `return;` |  | pending |
| `act_obj.wear_obj.if.004` | 1400 | `if ( CAN_WEAR( obj, ITEM_WEAR_FINGER ) )` |  | pending |
| `act_obj.wear_obj.if.005` | 1402 | `if ( get_eq_char( ch, WEAR_FINGER_L ) != NULL 	&&   get_eq_char( ch, WEAR_FINGER_R ) != NULL 	&&   !remove_obj( ch, WEAR_FINGER_L, fReplace ) 	&&   !remove_obj( ch, WEAR_FINGER_R, fReplace ) )` |  | pending |
| `act_obj.wear_obj.and.001` | 1403 | `&&   get_eq_char( ch, WEAR_FINGER_R ) != NULL` |  | pending |
| `act_obj.wear_obj.and.002` | 1404 | `&&   !remove_obj( ch, WEAR_FINGER_L, fReplace )` |  | pending |
| `act_obj.wear_obj.and.003` | 1405 | `&&   !remove_obj( ch, WEAR_FINGER_R, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.004` | 1406 | `return;` |  | pending |
| `act_obj.wear_obj.if.006` | 1408 | `if ( get_eq_char( ch, WEAR_FINGER_L ) == NULL )` |  | pending |
| `act_obj.wear_obj.return.005` | 1413 | `return;` |  | pending |
| `act_obj.wear_obj.if.007` | 1416 | `if ( get_eq_char( ch, WEAR_FINGER_R ) == NULL )` |  | pending |
| `act_obj.wear_obj.return.006` | 1421 | `return;` |  | pending |
| `act_obj.wear_obj.return.007` | 1426 | `return;` |  | pending |
| `act_obj.wear_obj.if.008` | 1429 | `if ( CAN_WEAR( obj, ITEM_WEAR_NECK ) )` |  | pending |
| `act_obj.wear_obj.if.009` | 1431 | `if ( get_eq_char( ch, WEAR_NECK_1 ) != NULL 	&&   get_eq_char( ch, WEAR_NECK_2 ) != NULL 	&&   !remove_obj( ch, WEAR_NECK_1, fReplace ) 	&&   !remove_obj( ch, WEAR_NECK_2, fReplace ) )` |  | pending |
| `act_obj.wear_obj.and.004` | 1432 | `&&   get_eq_char( ch, WEAR_NECK_2 ) != NULL` |  | pending |
| `act_obj.wear_obj.and.005` | 1433 | `&&   !remove_obj( ch, WEAR_NECK_1, fReplace )` |  | pending |
| `act_obj.wear_obj.and.006` | 1434 | `&&   !remove_obj( ch, WEAR_NECK_2, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.008` | 1435 | `return;` |  | pending |
| `act_obj.wear_obj.if.010` | 1437 | `if ( get_eq_char( ch, WEAR_NECK_1 ) == NULL )` |  | pending |
| `act_obj.wear_obj.return.009` | 1442 | `return;` |  | pending |
| `act_obj.wear_obj.if.011` | 1445 | `if ( get_eq_char( ch, WEAR_NECK_2 ) == NULL )` |  | pending |
| `act_obj.wear_obj.return.010` | 1450 | `return;` |  | pending |
| `act_obj.wear_obj.return.011` | 1455 | `return;` |  | pending |
| `act_obj.wear_obj.if.012` | 1458 | `if ( CAN_WEAR( obj, ITEM_WEAR_BODY ) )` |  | pending |
| `act_obj.wear_obj.if.013` | 1460 | `if ( !remove_obj( ch, WEAR_BODY, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.012` | 1461 | `return;` |  | pending |
| `act_obj.wear_obj.return.013` | 1465 | `return;` |  | pending |
| `act_obj.wear_obj.if.014` | 1468 | `if ( CAN_WEAR( obj, ITEM_WEAR_HEAD ) )` |  | pending |
| `act_obj.wear_obj.if.015` | 1470 | `if ( !remove_obj( ch, WEAR_HEAD, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.014` | 1471 | `return;` |  | pending |
| `act_obj.wear_obj.return.015` | 1475 | `return;` |  | pending |
| `act_obj.wear_obj.if.016` | 1478 | `if ( CAN_WEAR( obj, ITEM_WEAR_LEGS ) )` |  | pending |
| `act_obj.wear_obj.if.017` | 1480 | `if ( !remove_obj( ch, WEAR_LEGS, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.016` | 1481 | `return;` |  | pending |
| `act_obj.wear_obj.return.017` | 1485 | `return;` |  | pending |
| `act_obj.wear_obj.if.018` | 1488 | `if ( CAN_WEAR( obj, ITEM_WEAR_FEET ) )` |  | pending |
| `act_obj.wear_obj.if.019` | 1490 | `if ( !remove_obj( ch, WEAR_FEET, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.018` | 1491 | `return;` |  | pending |
| `act_obj.wear_obj.return.019` | 1495 | `return;` |  | pending |
| `act_obj.wear_obj.if.020` | 1498 | `if ( CAN_WEAR( obj, ITEM_WEAR_HANDS ) )` |  | pending |
| `act_obj.wear_obj.if.021` | 1500 | `if ( !remove_obj( ch, WEAR_HANDS, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.020` | 1501 | `return;` |  | pending |
| `act_obj.wear_obj.return.021` | 1505 | `return;` |  | pending |
| `act_obj.wear_obj.if.022` | 1508 | `if ( CAN_WEAR( obj, ITEM_WEAR_ARMS ) )` |  | pending |
| `act_obj.wear_obj.if.023` | 1510 | `if ( !remove_obj( ch, WEAR_ARMS, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.022` | 1511 | `return;` |  | pending |
| `act_obj.wear_obj.return.023` | 1515 | `return;` |  | pending |
| `act_obj.wear_obj.if.024` | 1518 | `if ( CAN_WEAR( obj, ITEM_WEAR_ABOUT ) )` |  | pending |
| `act_obj.wear_obj.if.025` | 1520 | `if ( !remove_obj( ch, WEAR_ABOUT, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.024` | 1521 | `return;` |  | pending |
| `act_obj.wear_obj.return.025` | 1525 | `return;` |  | pending |
| `act_obj.wear_obj.if.026` | 1528 | `if ( CAN_WEAR( obj, ITEM_WEAR_WAIST ) )` |  | pending |
| `act_obj.wear_obj.if.027` | 1530 | `if ( !remove_obj( ch, WEAR_WAIST, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.026` | 1531 | `return;` |  | pending |
| `act_obj.wear_obj.return.027` | 1535 | `return;` |  | pending |
| `act_obj.wear_obj.if.028` | 1538 | `if ( CAN_WEAR( obj, ITEM_WEAR_WRIST ) )` |  | pending |
| `act_obj.wear_obj.if.029` | 1540 | `if ( get_eq_char( ch, WEAR_WRIST_L ) != NULL 	&&   get_eq_char( ch, WEAR_WRIST_R ) != NULL 	&&   !remove_obj( ch, WEAR_WRIST_L, fReplace ) 	&&   !remove_obj( ch, WEAR_WRIST_R, fReplace ) )` |  | pending |
| `act_obj.wear_obj.and.007` | 1541 | `&&   get_eq_char( ch, WEAR_WRIST_R ) != NULL` |  | pending |
| `act_obj.wear_obj.and.008` | 1542 | `&&   !remove_obj( ch, WEAR_WRIST_L, fReplace )` |  | pending |
| `act_obj.wear_obj.and.009` | 1543 | `&&   !remove_obj( ch, WEAR_WRIST_R, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.028` | 1544 | `return;` |  | pending |
| `act_obj.wear_obj.if.030` | 1546 | `if ( get_eq_char( ch, WEAR_WRIST_L ) == NULL )` |  | pending |
| `act_obj.wear_obj.return.029` | 1553 | `return;` |  | pending |
| `act_obj.wear_obj.if.031` | 1556 | `if ( get_eq_char( ch, WEAR_WRIST_R ) == NULL )` |  | pending |
| `act_obj.wear_obj.return.030` | 1563 | `return;` |  | pending |
| `act_obj.wear_obj.return.031` | 1568 | `return;` |  | pending |
| `act_obj.wear_obj.if.032` | 1571 | `if ( CAN_WEAR( obj, ITEM_WEAR_SHIELD ) )` |  | pending |
| `act_obj.wear_obj.if.033` | 1575 | `if ( !remove_obj( ch, WEAR_SHIELD, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.032` | 1576 | `return;` |  | pending |
| `act_obj.wear_obj.if.034` | 1579 | `if (weapon != NULL && ch->size < SIZE_LARGE  	&&  IS_WEAPON_STAT(weapon,WEAPON_TWO_HANDS))` |  | pending |
| `act_obj.wear_obj.and.010` | 1579 | `&& ch->size < SIZE_LARGE` |  | pending |
| `act_obj.wear_obj.and.011` | 1580 | `&&  IS_WEAPON_STAT(weapon,WEAPON_TWO_HANDS))` |  | pending |
| `act_obj.wear_obj.return.033` | 1583 | `return;` |  | pending |
| `act_obj.wear_obj.return.034` | 1589 | `return;` |  | pending |
| `act_obj.wear_obj.if.035` | 1592 | `if ( CAN_WEAR( obj, ITEM_WIELD ) )` |  | pending |
| `act_obj.wear_obj.if.036` | 1596 | `if ( !remove_obj( ch, WEAR_WIELD, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.035` | 1597 | `return;` |  | pending |
| `act_obj.wear_obj.if.037` | 1599 | `if ( !IS_NPC(ch)  	&& get_obj_weight(obj) > (str_app[get_curr_stat(ch,STAT_STR)].wield   		* 10))` |  | pending |
| `act_obj.wear_obj.and.012` | 1600 | `&& get_obj_weight(obj) > (str_app[get_curr_stat(ch,STAT_STR)].wield` |  | pending |
| `act_obj.wear_obj.return.036` | 1604 | `return;` |  | pending |
| `act_obj.wear_obj.if.038` | 1607 | `if (!IS_NPC(ch) && ch->size < SIZE_LARGE  	&&  IS_WEAPON_STAT(obj,WEAPON_TWO_HANDS)  	&&  get_eq_char(ch,WEAR_SHIELD) != NULL)` |  | pending |
| `act_obj.wear_obj.and.013` | 1607 | `&& ch->size < SIZE_LARGE` |  | pending |
| `act_obj.wear_obj.and.014` | 1608 | `&&  IS_WEAPON_STAT(obj,WEAPON_TWO_HANDS)` |  | pending |
| `act_obj.wear_obj.and.015` | 1609 | `&&  get_eq_char(ch,WEAR_SHIELD) != NULL)` |  | pending |
| `act_obj.wear_obj.return.037` | 1612 | `return;` |  | pending |
| `act_obj.wear_obj.if.039` | 1621 | `if (sn == gsn_hand_to_hand)` |  | pending |
| `act_obj.wear_obj.return.038` | 1622 | `return;` |  | pending |
| `act_obj.wear_obj.if.040` | 1626 | `if (skill >= 100)` |  | pending |
| `act_obj.wear_obj.if.041` | 1628 | `if (skill > 85)` |  | pending |
| `act_obj.wear_obj.if.042` | 1630 | `if (skill > 70)` |  | pending |
| `act_obj.wear_obj.if.043` | 1632 | `if (skill > 50)` |  | pending |
| `act_obj.wear_obj.if.044` | 1634 | `if (skill > 25)` |  | pending |
| `act_obj.wear_obj.if.045` | 1636 | `if (skill > 1)` |  | pending |
| `act_obj.wear_obj.return.039` | 1642 | `return;` |  | pending |
| `act_obj.wear_obj.if.046` | 1645 | `if ( CAN_WEAR( obj, ITEM_HOLD ) )` |  | pending |
| `act_obj.wear_obj.if.047` | 1647 | `if ( !remove_obj( ch, WEAR_HOLD, fReplace ) )` |  | pending |
| `act_obj.wear_obj.return.040` | 1648 | `return;` |  | pending |
| `act_obj.wear_obj.return.041` | 1652 | `return;` |  | pending |
| `act_obj.wear_obj.if.048` | 1655 | `if ( CAN_WEAR(obj,ITEM_WEAR_FLOAT) )` |  | pending |
| `act_obj.wear_obj.if.049` | 1657 | `if (!remove_obj(ch,WEAR_FLOAT, fReplace) )` |  | pending |
| `act_obj.wear_obj.return.042` | 1658 | `return;` |  | pending |
| `act_obj.wear_obj.return.043` | 1662 | `return;` |  | pending |
| `act_obj.wear_obj.if.050` | 1665 | `if ( fReplace )` |  | pending |
| `act_obj.wear_obj.return.044` | 1668 | `return;` |  | pending |

## do_wear

[Source line 1673](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1673); ends at line 1710. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:104` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:215` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:232` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:284` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `str_cmp`, `can_see_obj`, `wear_obj`, `get_obj_carry`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_wear.if.001` | 1680 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_wear.return.001` | 1683 | `return;` |  | pending |
| `act_obj.do_wear.if.002` | 1686 | `if ( !str_cmp( arg, "all" ) )` |  | pending |
| `act_obj.do_wear.for.001` | 1690 | `for ( obj = ch->carrying; obj != NULL; obj = obj_next )` |  | pending |
| `act_obj.do_wear.if.003` | 1693 | `if ( obj->wear_loc == WEAR_NONE && can_see_obj( ch, obj ) )` |  | pending |
| `act_obj.do_wear.and.001` | 1693 | `&& can_see_obj( ch, obj ) )` |  | pending |
| `act_obj.do_wear.return.002` | 1696 | `return;` |  | pending |
| `act_obj.do_wear.if.004` | 1700 | `if ( ( obj = get_obj_carry( ch, arg, ch ) ) == NULL )` |  | pending |
| `act_obj.do_wear.return.003` | 1703 | `return;` |  | pending |
| `act_obj.do_wear.return.004` | 1709 | `return;` |  | pending |

## do_remove

[Source line 1714](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1714); ends at line 1735. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:224` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:222` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_wear`, `remove_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_remove.if.001` | 1721 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_remove.return.001` | 1724 | `return;` |  | pending |
| `act_obj.do_remove.if.002` | 1727 | `if ( ( obj = get_obj_wear( ch, arg ) ) == NULL )` |  | pending |
| `act_obj.do_remove.return.002` | 1730 | `return;` |  | pending |
| `act_obj.do_remove.return.003` | 1734 | `return;` |  | pending |

## do_sacrifice

[Source line 1739](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1739); ends at line 1836. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:941` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/interp.c:227` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:228` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.c:229` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:234` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `str_cmp`, `act`, `send_to_char`, `get_obj_list`, `CAN_WEAR`, `UMAX`, `UMIN`, `sprintf`, `IS_SET`, `is_same_group`, `do_function`, `wiznet`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_sacrifice.if.001` | 1754 | `if ( arg[0] == '\0' \|\| !str_cmp( arg, ch->name ) )` |  | pending |
| `act_obj.do_sacrifice.or.001` | 1754 | `\|\| !str_cmp( arg, ch->name ) )` |  | pending |
| `act_obj.do_sacrifice.return.001` | 1760 | `return;` |  | pending |
| `act_obj.do_sacrifice.if.002` | 1764 | `if ( obj == NULL )` |  | pending |
| `act_obj.do_sacrifice.return.002` | 1767 | `return;` |  | pending |
| `act_obj.do_sacrifice.if.003` | 1770 | `if ( obj->item_type == ITEM_CORPSE_PC )` |  | pending |
| `act_obj.do_sacrifice.if.004` | 1772 | `if (obj->contains)` |  | pending |
| `act_obj.do_sacrifice.return.003` | 1776 | `return;` |  | pending |
| `act_obj.do_sacrifice.if.005` | 1781 | `if ( !CAN_WEAR(obj, ITEM_TAKE) \|\| CAN_WEAR(obj, ITEM_NO_SAC))` |  | pending |
| `act_obj.do_sacrifice.or.002` | 1781 | `\|\| CAN_WEAR(obj, ITEM_NO_SAC))` |  | pending |
| `act_obj.do_sacrifice.return.004` | 1784 | `return;` |  | pending |
| `act_obj.do_sacrifice.if.006` | 1787 | `if (obj->in_room != NULL)` |  | pending |
| `act_obj.do_sacrifice.for.001` | 1789 | `for (gch = obj->in_room->people; gch != NULL; gch = gch->next_in_room)` |  | pending |
| `act_obj.do_sacrifice.if.007` | 1790 | `if (gch->on == obj)` |  | pending |
| `act_obj.do_sacrifice.return.005` | 1794 | `return;` |  | pending |
| `act_obj.do_sacrifice.if.008` | 1800 | `if (obj->item_type != ITEM_CORPSE_NPC && obj->item_type != ITEM_CORPSE_PC)` |  | pending |
| `act_obj.do_sacrifice.and.001` | 1800 | `&& obj->item_type != ITEM_CORPSE_PC)` |  | pending |
| `act_obj.do_sacrifice.if.009` | 1803 | `if (silver == 1)` |  | pending |
| `act_obj.do_sacrifice.if.010` | 1815 | `if (IS_SET(ch->act,PLR_AUTOSPLIT) )` |  | pending |
| `act_obj.do_sacrifice.for.002` | 1818 | `for (gch = ch->in_room->people; gch != NULL; gch = gch->next_in_room )` |  | pending |
| `act_obj.do_sacrifice.if.011` | 1820 | `if ( is_same_group( gch, ch ) )` |  | pending |
| `act_obj.do_sacrifice.if.012` | 1824 | `if ( members > 1 && silver > 1)` |  | pending |
| `act_obj.do_sacrifice.and.002` | 1824 | `&& silver > 1)` |  | pending |
| `act_obj.do_sacrifice.return.006` | 1835 | `return;` |  | pending |

## do_quaff

[Source line 1840](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1840); ends at line 1880. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:222` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:210` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_obj_carry`, `act`, `obj_cast_spell`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_quaff.if.001` | 1847 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_quaff.return.001` | 1850 | `return;` |  | pending |
| `act_obj.do_quaff.if.002` | 1853 | `if ( ( obj = get_obj_carry( ch, arg, ch ) ) == NULL )` |  | pending |
| `act_obj.do_quaff.return.002` | 1856 | `return;` |  | pending |
| `act_obj.do_quaff.if.003` | 1859 | `if ( obj->item_type != ITEM_POTION )` |  | pending |
| `act_obj.do_quaff.return.003` | 1862 | `return;` |  | pending |
| `act_obj.do_quaff.if.004` | 1865 | `if (ch->level < obj->level)` |  | pending |
| `act_obj.do_quaff.return.004` | 1868 | `return;` |  | pending |
| `act_obj.do_quaff.return.005` | 1879 | `return;` |  | pending |

## do_recite

[Source line 1884](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1884); ends at line 1948. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:223` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:221` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `get_obj_carry`, `send_to_char`, `get_char_room`, `get_obj_here`, `act`, `number_percent`, `get_skill`, `check_improve`, `obj_cast_spell`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_recite.if.001` | 1895 | `if ( ( scroll = get_obj_carry( ch, arg1, ch ) ) == NULL )` |  | pending |
| `act_obj.do_recite.return.001` | 1898 | `return;` |  | pending |
| `act_obj.do_recite.if.002` | 1901 | `if ( scroll->item_type != ITEM_SCROLL )` |  | pending |
| `act_obj.do_recite.return.002` | 1904 | `return;` |  | pending |
| `act_obj.do_recite.if.003` | 1907 | `if ( ch->level < scroll->level)` |  | pending |
| `act_obj.do_recite.return.003` | 1911 | `return;` |  | pending |
| `act_obj.do_recite.if.004` | 1915 | `if ( arg2[0] == '\0' )` |  | pending |
| `act_obj.do_recite.if.005` | 1921 | `if ( ( victim = get_char_room ( ch, arg2 ) ) == NULL 	&&   ( obj    = get_obj_here  ( ch, arg2 ) ) == NULL )` |  | pending |
| `act_obj.do_recite.and.001` | 1922 | `&&   ( obj    = get_obj_here  ( ch, arg2 ) ) == NULL )` |  | pending |
| `act_obj.do_recite.return.004` | 1925 | `return;` |  | pending |
| `act_obj.do_recite.if.006` | 1932 | `if (number_percent() >= 20 + get_skill(ch,gsn_scrolls) * 4/5)` |  | pending |
| `act_obj.do_recite.return.005` | 1947 | `return;` |  | pending |

## do_brandish

[Source line 1952](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:1952); ends at line 2037. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:206` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:92` (declaration_or_dispatch_reference).

Dependencies: `get_eq_char`, `send_to_char`, `bug`, `WAIT_STATE`, `act`, `number_percent`, `get_skill`, `check_improve`, `IS_NPC`, `obj_cast_spell`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_brandish.if.001` | 1959 | `if ( ( staff = get_eq_char( ch, WEAR_HOLD ) ) == NULL )` |  | pending |
| `act_obj.do_brandish.return.001` | 1962 | `return;` |  | pending |
| `act_obj.do_brandish.if.002` | 1965 | `if ( staff->item_type != ITEM_STAFF )` |  | pending |
| `act_obj.do_brandish.return.002` | 1968 | `return;` |  | pending |
| `act_obj.do_brandish.if.003` | 1971 | `if ( ( sn = staff->value[3] ) < 0     \|\|   sn >= MAX_SKILL     \|\|   skill_table[sn].spell_fun == 0 )` |  | pending |
| `act_obj.do_brandish.or.001` | 1972 | `\|\|   sn >= MAX_SKILL` |  | pending |
| `act_obj.do_brandish.or.002` | 1973 | `\|\|   skill_table[sn].spell_fun == 0 )` |  | pending |
| `act_obj.do_brandish.return.003` | 1976 | `return;` |  | pending |
| `act_obj.do_brandish.if.004` | 1981 | `if ( staff->value[2] > 0 )` |  | pending |
| `act_obj.do_brandish.if.005` | 1985 | `if ( ch->level < staff->level  	\|\|   number_percent() >= 20 + get_skill(ch,gsn_staves) * 4/5)` |  | pending |
| `act_obj.do_brandish.or.003` | 1986 | `\|\|   number_percent() >= 20 + get_skill(ch,gsn_staves) * 4/5)` |  | pending |
| `act_obj.do_brandish.for.001` | 1993 | `for ( vch = ch->in_room->people; vch; vch = vch_next )` |  | pending |
| `act_obj.do_brandish.switch.001` | 1997 | `switch ( skill_table[sn].target )` |  | pending |
| `act_obj.do_brandish.default.001` | 1999 | `default:` |  | pending |
| `act_obj.do_brandish.return.004` | 2001 | `return;` |  | pending |
| `act_obj.do_brandish.case.001` | 2003 | `case TAR_IGNORE:` |  | pending |
| `act_obj.do_brandish.if.006` | 2004 | `if ( vch != ch )` |  | pending |
| `act_obj.do_brandish.continue.001` | 2005 | `continue;` |  | pending |
| `act_obj.do_brandish.break.001` | 2006 | `break;` |  | pending |
| `act_obj.do_brandish.case.002` | 2008 | `case TAR_CHAR_OFFENSIVE:` |  | pending |
| `act_obj.do_brandish.if.007` | 2009 | `if ( IS_NPC(ch) ? IS_NPC(vch) : !IS_NPC(vch) )` |  | pending |
| `act_obj.do_brandish.ternary.001` | 2009 | `? IS_NPC(vch) : !IS_NPC(vch) )` |  | pending |
| `act_obj.do_brandish.continue.002` | 2010 | `continue;` |  | pending |
| `act_obj.do_brandish.break.002` | 2011 | `break;` |  | pending |
| `act_obj.do_brandish.case.003` | 2013 | `case TAR_CHAR_DEFENSIVE:` |  | pending |
| `act_obj.do_brandish.if.008` | 2014 | `if ( IS_NPC(ch) ? !IS_NPC(vch) : IS_NPC(vch) )` |  | pending |
| `act_obj.do_brandish.ternary.002` | 2014 | `? !IS_NPC(vch) : IS_NPC(vch) )` |  | pending |
| `act_obj.do_brandish.continue.003` | 2015 | `continue;` |  | pending |
| `act_obj.do_brandish.break.003` | 2016 | `break;` |  | pending |
| `act_obj.do_brandish.case.004` | 2018 | `case TAR_CHAR_SELF:` |  | pending |
| `act_obj.do_brandish.if.009` | 2019 | `if ( vch != ch )` |  | pending |
| `act_obj.do_brandish.continue.004` | 2020 | `continue;` |  | pending |
| `act_obj.do_brandish.break.004` | 2021 | `break;` |  | pending |
| `act_obj.do_brandish.if.010` | 2029 | `if ( --staff->value[2] <= 0 )` |  | pending |
| `act_obj.do_brandish.return.005` | 2036 | `return;` |  | pending |

## do_zap

[Source line 2041](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2041); ends at line 2130. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:233` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:297` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_eq_char`, `get_char_room`, `get_obj_here`, `WAIT_STATE`, `act`, `number_percent`, `get_skill`, `check_improve`, `obj_cast_spell`, `extract_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_zap.if.001` | 2049 | `if ( arg[0] == '\0' && ch->fighting == NULL )` |  | pending |
| `act_obj.do_zap.and.001` | 2049 | `&& ch->fighting == NULL )` |  | pending |
| `act_obj.do_zap.return.001` | 2052 | `return;` |  | pending |
| `act_obj.do_zap.if.002` | 2055 | `if ( ( wand = get_eq_char( ch, WEAR_HOLD ) ) == NULL )` |  | pending |
| `act_obj.do_zap.return.002` | 2058 | `return;` |  | pending |
| `act_obj.do_zap.if.003` | 2061 | `if ( wand->item_type != ITEM_WAND )` |  | pending |
| `act_obj.do_zap.return.003` | 2064 | `return;` |  | pending |
| `act_obj.do_zap.if.004` | 2068 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_zap.if.005` | 2070 | `if ( ch->fighting != NULL )` |  | pending |
| `act_obj.do_zap.return.004` | 2077 | `return;` |  | pending |
| `act_obj.do_zap.if.006` | 2082 | `if ( ( victim = get_char_room ( ch, arg ) ) == NULL 	&&   ( obj    = get_obj_here  ( ch, arg ) ) == NULL )` |  | pending |
| `act_obj.do_zap.and.002` | 2083 | `&&   ( obj    = get_obj_here  ( ch, arg ) ) == NULL )` |  | pending |
| `act_obj.do_zap.return.005` | 2086 | `return;` |  | pending |
| `act_obj.do_zap.if.007` | 2092 | `if ( wand->value[2] > 0 )` |  | pending |
| `act_obj.do_zap.if.008` | 2094 | `if ( victim != NULL )` |  | pending |
| `act_obj.do_zap.if.009` | 2106 | `if (ch->level < wand->level  	\|\|  number_percent() >= 20 + get_skill(ch,gsn_wands) * 4/5)` |  | pending |
| `act_obj.do_zap.or.001` | 2107 | `\|\|  number_percent() >= 20 + get_skill(ch,gsn_wands) * 4/5)` |  | pending |
| `act_obj.do_zap.if.010` | 2122 | `if ( --wand->value[2] <= 0 )` |  | pending |
| `act_obj.do_zap.return.006` | 2129 | `return;` |  | pending |

## do_steal

[Source line 2134](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2134); ends at line 2306. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:272` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:263` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `get_char_room`, `is_safe`, `IS_NPC`, `WAIT_STATE`, `number_percent`, `IS_AWAKE`, `can_see`, `get_skill`, `is_clan`, `affect_strip`, `REMOVE_BIT`, `act`, `number_range`, `sprintf`, `do_function`, `check_improve`, `multi_hit`, `wiznet`, `IS_SET`, `SET_BIT`, `save_char_obj`, `str_cmp`, `get_obj_carry`, `can_drop_obj`, `get_obj_number`, `can_carry_n`, `get_obj_weight`, `can_carry_w`, `obj_from_char`, `obj_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_steal.if.001` | 2146 | `if ( arg1[0] == '\0' \|\| arg2[0] == '\0' )` |  | pending |
| `act_obj.do_steal.or.001` | 2146 | `\|\| arg2[0] == '\0' )` |  | pending |
| `act_obj.do_steal.return.001` | 2149 | `return;` |  | pending |
| `act_obj.do_steal.if.002` | 2152 | `if ( ( victim = get_char_room( ch, arg2 ) ) == NULL )` |  | pending |
| `act_obj.do_steal.return.002` | 2155 | `return;` |  | pending |
| `act_obj.do_steal.if.003` | 2158 | `if ( victim == ch )` |  | pending |
| `act_obj.do_steal.return.003` | 2161 | `return;` |  | pending |
| `act_obj.do_steal.if.004` | 2164 | `if (is_safe(ch,victim))` |  | pending |
| `act_obj.do_steal.return.004` | 2165 | `return;` |  | pending |
| `act_obj.do_steal.if.005` | 2167 | `if ( IS_NPC(victim)  	  && victim->position == POS_FIGHTING)` |  | pending |
| `act_obj.do_steal.and.001` | 2168 | `&& victim->position == POS_FIGHTING)` |  | pending |
| `act_obj.do_steal.return.005` | 2172 | `return;` |  | pending |
| `act_obj.do_steal.if.006` | 2178 | `if (!IS_AWAKE(victim))` |  | pending |
| `act_obj.do_steal.if.007` | 2180 | `if (!can_see(victim,ch))` |  | pending |
| `act_obj.do_steal.if.008` | 2185 | `if ( ((ch->level + 7 < victim->level \|\| ch->level -7 > victim->level)      && !IS_NPC(victim) && !IS_NPC(ch) )     \|\| ( !IS_NPC(ch) && percent > get_skill(ch,gsn_steal))     \|\| ( !IS_NPC(ch) && !is_clan(ch)) )` |  | pending |
| `act_obj.do_steal.or.002` | 2185 | `\|\| ch->level -7 > victim->level)` |  | pending |
| `act_obj.do_steal.and.002` | 2186 | `&& !IS_NPC(victim) && !IS_NPC(ch) )` |  | pending |
| `act_obj.do_steal.and.003` | 2186 | `&& !IS_NPC(ch) )` |  | pending |
| `act_obj.do_steal.or.003` | 2187 | `\|\| ( !IS_NPC(ch) && percent > get_skill(ch,gsn_steal))` |  | pending |
| `act_obj.do_steal.and.004` | 2187 | `&& percent > get_skill(ch,gsn_steal))` |  | pending |
| `act_obj.do_steal.or.004` | 2188 | `\|\| ( !IS_NPC(ch) && !is_clan(ch)) )` |  | pending |
| `act_obj.do_steal.and.005` | 2188 | `&& !is_clan(ch)) )` |  | pending |
| `act_obj.do_steal.switch.001` | 2199 | `switch(number_range(0,3))` |  | pending |
| `act_obj.do_steal.case.001` | 2201 | `case 0 :` |  | pending |
| `act_obj.do_steal.break.001` | 2203 | `break;` |  | pending |
| `act_obj.do_steal.case.002` | 2204 | `case 1 :` |  | pending |
| `act_obj.do_steal.ternary.001` | 2206 | `? "her" : "his");` |  | pending |
| `act_obj.do_steal.break.002` | 2207 | `break;` |  | pending |
| `act_obj.do_steal.case.003` | 2208 | `case 2 :` |  | pending |
| `act_obj.do_steal.break.003` | 2210 | `break;` |  | pending |
| `act_obj.do_steal.case.004` | 2211 | `case 3 :` |  | pending |
| `act_obj.do_steal.break.004` | 2213 | `break;` |  | pending |
| `act_obj.do_steal.if.009` | 2215 | `if (!IS_AWAKE(victim))` |  | pending |
| `act_obj.do_steal.if.010` | 2217 | `if (IS_AWAKE(victim))` |  | pending |
| `act_obj.do_steal.if.011` | 2219 | `if ( !IS_NPC(ch) )` |  | pending |
| `act_obj.do_steal.if.012` | 2221 | `if ( IS_NPC(victim) )` |  | pending |
| `act_obj.do_steal.if.013` | 2230 | `if ( !IS_SET(ch->act, PLR_THIEF) )` |  | pending |
| `act_obj.do_steal.return.006` | 2239 | `return;` |  | pending |
| `act_obj.do_steal.if.014` | 2242 | `if ( !str_cmp( arg1, "coin"  )     \|\|   !str_cmp( arg1, "coins" )     \|\|   !str_cmp( arg1, "gold"  )      \|\|	 !str_cmp( arg1, "silver"))` |  | pending |
| `act_obj.do_steal.or.005` | 2243 | `\|\|   !str_cmp( arg1, "coins" )` |  | pending |
| `act_obj.do_steal.or.006` | 2244 | `\|\|   !str_cmp( arg1, "gold"  )` |  | pending |
| `act_obj.do_steal.or.007` | 2245 | `\|\|	 !str_cmp( arg1, "silver"))` |  | pending |
| `act_obj.do_steal.if.015` | 2251 | `if ( gold <= 0 && silver <= 0 )` |  | pending |
| `act_obj.do_steal.and.006` | 2251 | `&& silver <= 0 )` |  | pending |
| `act_obj.do_steal.return.007` | 2254 | `return;` |  | pending |
| `act_obj.do_steal.if.016` | 2261 | `if (silver <= 0)` |  | pending |
| `act_obj.do_steal.if.017` | 2263 | `if (gold <= 0)` |  | pending |
| `act_obj.do_steal.return.008` | 2271 | `return;` |  | pending |
| `act_obj.do_steal.if.018` | 2274 | `if ( ( obj = get_obj_carry( victim, arg1, ch ) ) == NULL )` |  | pending |
| `act_obj.do_steal.return.009` | 2277 | `return;` |  | pending |
| `act_obj.do_steal.if.019` | 2280 | `if ( !can_drop_obj( ch, obj )     \|\|   IS_SET(obj->extra_flags, ITEM_INVENTORY)     \|\|   obj->level > ch->level )` |  | pending |
| `act_obj.do_steal.or.008` | 2281 | `\|\|   IS_SET(obj->extra_flags, ITEM_INVENTORY)` |  | pending |
| `act_obj.do_steal.or.009` | 2282 | `\|\|   obj->level > ch->level )` |  | pending |
| `act_obj.do_steal.return.010` | 2285 | `return;` |  | pending |
| `act_obj.do_steal.if.020` | 2288 | `if ( ch->carry_number + get_obj_number( obj ) > can_carry_n( ch ) )` |  | pending |
| `act_obj.do_steal.return.011` | 2291 | `return;` |  | pending |
| `act_obj.do_steal.if.021` | 2294 | `if ( ch->carry_weight + get_obj_weight( obj ) > can_carry_w( ch ) )` |  | pending |
| `act_obj.do_steal.return.012` | 2297 | `return;` |  | pending |
| `act_obj.do_steal.return.013` | 2305 | `return;` |  | pending |

## find_keeper

[Source line 2313](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2313); ends at line 2376. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_buy: `src/act_obj.c:2619` (lexical_call_candidate).
- do_list: `src/act_obj.c:2796` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2861` (lexical_call_candidate).
- do_value: `src/act_obj.c:2953` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_obj.c:48` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `send_to_char`, `do_function`, `can_see`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.find_keeper.for.001` | 2320 | `for ( keeper = ch->in_room->people; keeper; keeper = keeper->next_in_room )` |  | pending |
| `act_obj.find_keeper.if.001` | 2322 | `if ( IS_NPC(keeper) && (pShop = keeper->pIndexData->pShop) != NULL )` |  | pending |
| `act_obj.find_keeper.and.001` | 2322 | `&& (pShop = keeper->pIndexData->pShop) != NULL )` |  | pending |
| `act_obj.find_keeper.break.001` | 2323 | `break;` |  | pending |
| `act_obj.find_keeper.if.002` | 2326 | `if ( pShop == NULL )` |  | pending |
| `act_obj.find_keeper.return.001` | 2329 | `return NULL;` |  | pending |
| `act_obj.find_keeper.if.003` | 2354 | `if ( time_info.hour < pShop->open_hour )` |  | pending |
| `act_obj.find_keeper.return.002` | 2357 | `return NULL;` |  | pending |
| `act_obj.find_keeper.if.004` | 2360 | `if ( time_info.hour > pShop->close_hour )` |  | pending |
| `act_obj.find_keeper.return.003` | 2363 | `return NULL;` |  | pending |
| `act_obj.find_keeper.if.005` | 2369 | `if ( !can_see( keeper, ch ) )` |  | pending |
| `act_obj.find_keeper.return.004` | 2372 | `return NULL;` |  | pending |
| `act_obj.find_keeper.return.005` | 2375 | `return keeper;` |  | pending |

## obj_to_keeper

[Source line 2379](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2379); ends at line 2418. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_sell: `src/act_obj.c:2929` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_obj.c:50` (declaration_or_dispatch_reference).

Dependencies: `str_cmp`, `IS_OBJ_STAT`, `extract_obj`, `get_obj_number`, `get_obj_weight`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.obj_to_keeper.for.001` | 2384 | `for (t_obj = ch->carrying; t_obj != NULL; t_obj = t_obj_next)` |  | pending |
| `act_obj.obj_to_keeper.if.001` | 2388 | `if (obj->pIndexData == t_obj->pIndexData  	&&  !str_cmp(obj->short_descr,t_obj->short_descr))` |  | pending |
| `act_obj.obj_to_keeper.and.001` | 2389 | `&&  !str_cmp(obj->short_descr,t_obj->short_descr))` |  | pending |
| `act_obj.obj_to_keeper.if.002` | 2392 | `if (IS_OBJ_STAT(t_obj,ITEM_INVENTORY))` |  | pending |
| `act_obj.obj_to_keeper.return.001` | 2395 | `return;` |  | pending |
| `act_obj.obj_to_keeper.break.001` | 2398 | `break;` |  | pending |
| `act_obj.obj_to_keeper.if.003` | 2402 | `if (t_obj == NULL)` |  | pending |

## get_obj_keeper

[Source line 2421](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2421); ends at line 2449. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_buy: `src/act_obj.c:2623` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_obj.c:51` (declaration_or_dispatch_reference).

Dependencies: `number_argument`, `can_see_obj`, `is_name`, `str_cmp`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.get_obj_keeper.for.001` | 2430 | `for ( obj = keeper->carrying; obj != NULL; obj = obj->next_content )` |  | pending |
| `act_obj.get_obj_keeper.if.001` | 2432 | `if (obj->wear_loc == WEAR_NONE         &&  can_see_obj( keeper, obj ) 	&&  can_see_obj(ch,obj)         &&  is_name( arg, obj->name ) )` |  | pending |
| `act_obj.get_obj_keeper.and.001` | 2433 | `&&  can_see_obj( keeper, obj )` |  | pending |
| `act_obj.get_obj_keeper.and.002` | 2434 | `&&  can_see_obj(ch,obj)` |  | pending |
| `act_obj.get_obj_keeper.and.003` | 2435 | `&&  is_name( arg, obj->name ) )` |  | pending |
| `act_obj.get_obj_keeper.if.002` | 2437 | `if ( ++count == number )` |  | pending |
| `act_obj.get_obj_keeper.return.001` | 2438 | `return obj;` |  | pending |
| `act_obj.get_obj_keeper.while.001` | 2441 | `while (obj->next_content != NULL 	    && obj->pIndexData == obj->next_content->pIndexData 	    && !str_cmp(obj->short_descr,obj->next_content->short_descr))` |  | pending |
| `act_obj.get_obj_keeper.and.004` | 2442 | `&& obj->pIndexData == obj->next_content->pIndexData` |  | pending |
| `act_obj.get_obj_keeper.and.005` | 2443 | `&& !str_cmp(obj->short_descr,obj->next_content->short_descr))` |  | pending |
| `act_obj.get_obj_keeper.return.002` | 2448 | `return NULL;` |  | pending |

## get_cost

[Source line 2451](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2451); ends at line 2500. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_buy: `src/act_obj.c:2624` (lexical_call_candidate).
- do_list: `src/act_obj.c:2805` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2884` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2903` (lexical_call_candidate).
- do_value: `src/act_obj.c:2976` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/act_obj.c:49` (declaration_or_dispatch_reference).

Dependencies: `IS_OBJ_STAT`, `str_cmp`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.get_cost.if.001` | 2456 | `if ( obj == NULL \|\| ( pShop = keeper->pIndexData->pShop ) == NULL )` |  | pending |
| `act_obj.get_cost.or.001` | 2456 | `\|\| ( pShop = keeper->pIndexData->pShop ) == NULL )` |  | pending |
| `act_obj.get_cost.return.001` | 2457 | `return 0;` |  | pending |
| `act_obj.get_cost.if.002` | 2459 | `if ( fBuy )` |  | pending |
| `act_obj.get_cost.for.001` | 2469 | `for ( itype = 0; itype < MAX_TRADE; itype++ )` |  | pending |
| `act_obj.get_cost.if.003` | 2471 | `if ( obj->item_type == pShop->buy_type[itype] )` |  | pending |
| `act_obj.get_cost.break.001` | 2474 | `break;` |  | pending |
| `act_obj.get_cost.if.004` | 2478 | `if (!IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT))` |  | pending |
| `act_obj.get_cost.for.002` | 2479 | `for ( obj2 = keeper->carrying; obj2; obj2 = obj2->next_content )` |  | pending |
| `act_obj.get_cost.if.005` | 2481 | `if ( obj->pIndexData == obj2->pIndexData 		&&   !str_cmp(obj->short_descr,obj2->short_descr) )` |  | pending |
| `act_obj.get_cost.and.001` | 2482 | `&&   !str_cmp(obj->short_descr,obj2->short_descr) )` |  | pending |
| `act_obj.get_cost.if.006` | 2483 | `if (IS_OBJ_STAT(obj2,ITEM_INVENTORY))` |  | pending |
| `act_obj.get_cost.if.007` | 2491 | `if ( obj->item_type == ITEM_STAFF \|\| obj->item_type == ITEM_WAND )` |  | pending |
| `act_obj.get_cost.or.002` | 2491 | `\|\| obj->item_type == ITEM_WAND )` |  | pending |
| `act_obj.get_cost.if.008` | 2493 | `if (obj->value[1] == 0)` |  | pending |
| `act_obj.get_cost.return.002` | 2499 | `return cost;` |  | pending |

## do_buy

[Source line 2504](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2504); ends at line 2740. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:83` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:95` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `IS_SET`, `smash_tilde`, `IS_NPC`, `one_argument`, `get_room_index`, `bug`, `get_char_room`, `number_percent`, `get_skill`, `sprintf`, `check_improve`, `deduct_cost`, `create_mobile`, `SET_BIT`, `free_string`, `str_dup`, `char_to_room`, `add_follower`, `act`, `find_keeper`, `mult_argument`, `get_obj_keeper`, `get_cost`, `can_see_obj`, `IS_OBJ_STAT`, `str_cmp`, `get_obj_number`, `can_carry_n`, `get_obj_weight`, `can_carry_w`, `create_object`, `obj_from_char`, `REMOVE_BIT`, `obj_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_buy.if.001` | 2509 | `if ( argument[0] == '\0' )` |  | pending |
| `act_obj.do_buy.return.001` | 2512 | `return;` |  | pending |
| `act_obj.do_buy.if.002` | 2515 | `if ( IS_SET(ch->in_room->room_flags, ROOM_PET_SHOP) )` |  | pending |
| `act_obj.do_buy.if.003` | 2525 | `if ( IS_NPC(ch) )` |  | pending |
| `act_obj.do_buy.return.002` | 2526 | `return;` |  | pending |
| `act_obj.do_buy.if.004` | 2531 | `if (ch->in_room->vnum == 9621)` |  | pending |
| `act_obj.do_buy.if.005` | 2535 | `if ( pRoomIndexNext == NULL )` |  | pending |
| `act_obj.do_buy.return.003` | 2539 | `return;` |  | pending |
| `act_obj.do_buy.if.006` | 2547 | `if ( pet == NULL \|\| !IS_SET(pet->act, ACT_PET) )` |  | pending |
| `act_obj.do_buy.or.001` | 2547 | `\|\| !IS_SET(pet->act, ACT_PET) )` |  | pending |
| `act_obj.do_buy.return.004` | 2550 | `return;` |  | pending |
| `act_obj.do_buy.if.007` | 2553 | `if ( ch->pet != NULL )` |  | pending |
| `act_obj.do_buy.return.005` | 2556 | `return;` |  | pending |
| `act_obj.do_buy.if.008` | 2561 | `if ( (ch->silver + 100 * ch->gold) < cost )` |  | pending |
| `act_obj.do_buy.return.006` | 2564 | `return;` |  | pending |
| `act_obj.do_buy.if.009` | 2567 | `if ( ch->level < pet->level )` |  | pending |
| `act_obj.do_buy.return.007` | 2571 | `return;` |  | pending |
| `act_obj.do_buy.if.010` | 2576 | `if (roll < get_skill(ch,gsn_haggle))` |  | pending |
| `act_obj.do_buy.if.011` | 2592 | `if ( arg[0] != '\0' )` |  | pending |
| `act_obj.do_buy.return.008` | 2610 | `return;` |  | pending |
| `act_obj.do_buy.if.012` | 2619 | `if ( ( keeper = find_keeper( ch ) ) == NULL )` |  | pending |
| `act_obj.do_buy.return.009` | 2620 | `return;` |  | pending |
| `act_obj.do_buy.if.013` | 2626 | `if (number < 1 \|\| number > 99)` |  | pending |
| `act_obj.do_buy.or.002` | 2626 | `\|\| number > 99)` |  | pending |
| `act_obj.do_buy.return.010` | 2629 | `return;` |  | pending |
| `act_obj.do_buy.if.014` | 2632 | `if ( cost <= 0 \|\| !can_see_obj( ch, obj ) )` |  | pending |
| `act_obj.do_buy.or.003` | 2632 | `\|\| !can_see_obj( ch, obj ) )` |  | pending |
| `act_obj.do_buy.return.011` | 2637 | `return;` |  | pending |
| `act_obj.do_buy.if.015` | 2640 | `if (!IS_OBJ_STAT(obj,ITEM_INVENTORY))` |  | pending |
| `act_obj.do_buy.for.001` | 2642 | `for (t_obj = obj->next_content; 	     	 count < number && t_obj != NULL;  	     	 t_obj = t_obj->next_content)` |  | pending |
| `act_obj.do_buy.and.001` | 2643 | `&& t_obj != NULL;` |  | pending |
| `act_obj.do_buy.if.016` | 2646 | `if (t_obj->pIndexData == obj->pIndexData 	    	&&  !str_cmp(t_obj->short_descr,obj->short_descr))` |  | pending |
| `act_obj.do_buy.and.002` | 2647 | `&&  !str_cmp(t_obj->short_descr,obj->short_descr))` |  | pending |
| `act_obj.do_buy.break.001` | 2650 | `break;` |  | pending |
| `act_obj.do_buy.if.017` | 2653 | `if (count < number)` |  | pending |
| `act_obj.do_buy.return.012` | 2658 | `return;` |  | pending |
| `act_obj.do_buy.if.018` | 2662 | `if ( (ch->silver + ch->gold * 100) < cost * number )` |  | pending |
| `act_obj.do_buy.if.019` | 2664 | `if (number > 1)` |  | pending |
| `act_obj.do_buy.return.013` | 2671 | `return;` |  | pending |
| `act_obj.do_buy.if.020` | 2674 | `if ( obj->level > ch->level )` |  | pending |
| `act_obj.do_buy.return.014` | 2679 | `return;` |  | pending |
| `act_obj.do_buy.if.021` | 2682 | `if (ch->carry_number +  number * get_obj_number(obj) > can_carry_n(ch))` |  | pending |
| `act_obj.do_buy.return.015` | 2685 | `return;` |  | pending |
| `act_obj.do_buy.if.022` | 2688 | `if ( ch->carry_weight + number * get_obj_weight(obj) > can_carry_w(ch))` |  | pending |
| `act_obj.do_buy.return.016` | 2691 | `return;` |  | pending |
| `act_obj.do_buy.if.023` | 2696 | `if (!IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT)  	&& roll < get_skill(ch,gsn_haggle))` |  | pending |
| `act_obj.do_buy.and.003` | 2697 | `&& roll < get_skill(ch,gsn_haggle))` |  | pending |
| `act_obj.do_buy.if.024` | 2704 | `if (number > 1)` |  | pending |
| `act_obj.do_buy.for.002` | 2721 | `for (count = 0; count < number; count++)` |  | pending |
| `act_obj.do_buy.if.025` | 2723 | `if ( IS_SET( obj->extra_flags, ITEM_INVENTORY ) )` |  | pending |
| `act_obj.do_buy.if.026` | 2732 | `if (t_obj->timer > 0 && !IS_OBJ_STAT(t_obj,ITEM_HAD_TIMER))` |  | pending |
| `act_obj.do_buy.and.004` | 2732 | `&& !IS_OBJ_STAT(t_obj,ITEM_HAD_TIMER))` |  | pending |
| `act_obj.do_buy.if.027` | 2736 | `if (cost < t_obj->cost)` |  | pending |

## do_list

[Source line 2744](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2744); ends at line 2841. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:216` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:158` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `get_room_index`, `bug`, `send_to_char`, `sprintf`, `find_keeper`, `one_argument`, `can_see_obj`, `get_cost`, `is_name`, `IS_OBJ_STAT`, `str_cmp`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_list.if.001` | 2748 | `if ( IS_SET(ch->in_room->room_flags, ROOM_PET_SHOP) )` |  | pending |
| `act_obj.do_list.if.002` | 2755 | `if (ch->in_room->vnum == 9621)` |  | pending |
| `act_obj.do_list.if.003` | 2760 | `if ( pRoomIndexNext == NULL )` |  | pending |
| `act_obj.do_list.return.001` | 2764 | `return;` |  | pending |
| `act_obj.do_list.for.001` | 2768 | `for ( pet = pRoomIndexNext->people; pet; pet = pet->next_in_room )` |  | pending |
| `act_obj.do_list.if.004` | 2770 | `if ( IS_SET(pet->act, ACT_PET) )` |  | pending |
| `act_obj.do_list.if.005` | 2772 | `if ( !found )` |  | pending |
| `act_obj.do_list.if.006` | 2784 | `if ( !found )` |  | pending |
| `act_obj.do_list.return.002` | 2786 | `return;` |  | pending |
| `act_obj.do_list.if.007` | 2796 | `if ( ( keeper = find_keeper( ch ) ) == NULL )` |  | pending |
| `act_obj.do_list.return.003` | 2797 | `return;` |  | pending |
| `act_obj.do_list.for.002` | 2801 | `for ( obj = keeper->carrying; obj; obj = obj->next_content )` |  | pending |
| `act_obj.do_list.if.008` | 2803 | `if ( obj->wear_loc == WEAR_NONE 	    &&   can_see_obj( ch, obj ) 	    &&   ( cost = get_cost( keeper, obj, TRUE ) ) > 0  	    &&   ( arg[0] == '\0'    	       \|\|  is_name(arg,obj->name) ))` |  | pending |
| `act_obj.do_list.and.001` | 2804 | `&&   can_see_obj( ch, obj )` |  | pending |
| `act_obj.do_list.and.002` | 2805 | `&&   ( cost = get_cost( keeper, obj, TRUE ) ) > 0` |  | pending |
| `act_obj.do_list.and.003` | 2806 | `&&   ( arg[0] == '\0'` |  | pending |
| `act_obj.do_list.or.001` | 2807 | `\|\|  is_name(arg,obj->name) ))` |  | pending |
| `act_obj.do_list.if.009` | 2809 | `if ( !found )` |  | pending |
| `act_obj.do_list.if.010` | 2815 | `if (IS_OBJ_STAT(obj,ITEM_INVENTORY))` |  | pending |
| `act_obj.do_list.while.001` | 2822 | `while (obj->next_content != NULL  		    && obj->pIndexData == obj->next_content->pIndexData 		    && !str_cmp(obj->short_descr, 			        obj->next_content->short_descr))` |  | pending |
| `act_obj.do_list.and.004` | 2823 | `&& obj->pIndexData == obj->next_content->pIndexData` |  | pending |
| `act_obj.do_list.and.005` | 2824 | `&& !str_cmp(obj->short_descr,` |  | pending |
| `act_obj.do_list.if.011` | 2837 | `if ( !found )` |  | pending |
| `act_obj.do_list.return.004` | 2839 | `return;` |  | pending |

## do_sell

[Source line 2845](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2845); ends at line 2933. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:225` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:240` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `find_keeper`, `get_obj_carry`, `act`, `can_drop_obj`, `can_see_obj`, `get_cost`, `number_percent`, `IS_OBJ_STAT`, `get_skill`, `UMIN`, `check_improve`, `sprintf`, `deduct_cost`, `extract_obj`, `obj_from_char`, `SET_BIT`, `number_range`, `obj_to_keeper`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_sell.if.001` | 2855 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_sell.return.001` | 2858 | `return;` |  | pending |
| `act_obj.do_sell.if.002` | 2861 | `if ( ( keeper = find_keeper( ch ) ) == NULL )` |  | pending |
| `act_obj.do_sell.return.002` | 2862 | `return;` |  | pending |
| `act_obj.do_sell.if.003` | 2864 | `if ( ( obj = get_obj_carry( ch, arg, ch ) ) == NULL )` |  | pending |
| `act_obj.do_sell.return.003` | 2869 | `return;` |  | pending |
| `act_obj.do_sell.if.004` | 2872 | `if ( !can_drop_obj( ch, obj ) )` |  | pending |
| `act_obj.do_sell.return.004` | 2875 | `return;` |  | pending |
| `act_obj.do_sell.if.005` | 2878 | `if (!can_see_obj(keeper,obj))` |  | pending |
| `act_obj.do_sell.return.005` | 2881 | `return;` |  | pending |
| `act_obj.do_sell.if.006` | 2884 | `if ( ( cost = get_cost( keeper, obj, FALSE ) ) <= 0 )` |  | pending |
| `act_obj.do_sell.return.006` | 2887 | `return;` |  | pending |
| `act_obj.do_sell.if.007` | 2889 | `if ( cost > (keeper-> silver + 100 * keeper->gold) )` |  | pending |
| `act_obj.do_sell.return.007` | 2893 | `return;` |  | pending |
| `act_obj.do_sell.if.008` | 2899 | `if (!IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT) && roll < get_skill(ch,gsn_haggle))` |  | pending |
| `act_obj.do_sell.and.001` | 2899 | `&& roll < get_skill(ch,gsn_haggle))` |  | pending |
| `act_obj.do_sell.ternary.001` | 2908 | `? "" : "s" );` |  | pending |
| `act_obj.do_sell.if.009` | 2913 | `if ( keeper->gold < 0 )` |  | pending |
| `act_obj.do_sell.if.010` | 2915 | `if ( keeper->silver< 0)` |  | pending |
| `act_obj.do_sell.if.011` | 2918 | `if ( obj->item_type == ITEM_TRASH \|\| IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT))` |  | pending |
| `act_obj.do_sell.or.001` | 2918 | `\|\| IS_OBJ_STAT(obj,ITEM_SELL_EXTRACT))` |  | pending |
| `act_obj.do_sell.if.012` | 2925 | `if (obj->timer)` |  | pending |
| `act_obj.do_sell.return.008` | 2932 | `return;` |  | pending |

## do_value

[Source line 2937](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_obj.c:2937); ends at line 2989. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:231` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:279` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `send_to_char`, `find_keeper`, `get_obj_carry`, `act`, `can_see_obj`, `can_drop_obj`, `get_cost`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `act_obj.do_value.if.001` | 2947 | `if ( arg[0] == '\0' )` |  | pending |
| `act_obj.do_value.return.001` | 2950 | `return;` |  | pending |
| `act_obj.do_value.if.002` | 2953 | `if ( ( keeper = find_keeper( ch ) ) == NULL )` |  | pending |
| `act_obj.do_value.return.002` | 2954 | `return;` |  | pending |
| `act_obj.do_value.if.003` | 2956 | `if ( ( obj = get_obj_carry( ch, arg, ch ) ) == NULL )` |  | pending |
| `act_obj.do_value.return.003` | 2961 | `return;` |  | pending |
| `act_obj.do_value.if.004` | 2964 | `if (!can_see_obj(keeper,obj))` |  | pending |
| `act_obj.do_value.return.004` | 2967 | `return;` |  | pending |
| `act_obj.do_value.if.005` | 2970 | `if ( !can_drop_obj( ch, obj ) )` |  | pending |
| `act_obj.do_value.return.005` | 2973 | `return;` |  | pending |
| `act_obj.do_value.if.006` | 2976 | `if ( ( cost = get_cost( keeper, obj, FALSE ) ) <= 0 )` |  | pending |
| `act_obj.do_value.return.006` | 2979 | `return;` |  | pending |
| `act_obj.do_value.return.007` | 2988 | `return;` |  | pending |

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
- Line 44: `#define CD CHAR_DATA` — pending configuration/reachability review.
- Line 45: `#define OD OBJ_DATA` — pending configuration/reachability review.
- Line 53: `#undef OD` — pending configuration/reachability review.
- Line 54: `#undef	CD` — pending configuration/reachability review.

## Static tables


## Commented code candidates

- Lines 2332–2350: disabled inside block comment; content hash `3d051aab03dec3bee0fe57a52d45174283cfba8bb92771fab8ffef15b9d4e5d1`.

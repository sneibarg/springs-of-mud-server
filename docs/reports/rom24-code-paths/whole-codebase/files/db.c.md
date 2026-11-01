# src/db.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `b30dbee85e6251821f16edb0b1139d1e432ffc66ac555834dfcfb02e94d37312`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## boot_db

[Source line 233](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:233); ends at line 389. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- main: `src/comm.c:410` (lexical_call_candidate).
- main: `src/comm.c:417` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2117` (declaration_or_dispatch_reference).

Dependencies: `calloc`, `bug`, `exit`, `init_mm`, `number_range`, `fopen`, `perror`, `strcpy`, `fread_word`, `fread_letter`, `str_cmp`, `load_area`, `load_helps`, `load_old_mob`, `load_mobiles`, `load_old_obj`, `load_objects`, `load_resets`, `load_rooms`, `load_shops`, `load_socials`, `load_specials`, `fclose`, `fix_exits`, `area_update`, `load_notes`, `load_bans`, `load_songs`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.boot_db.if.001` | 240 | `if ( ( string_space = calloc( 1, MAX_STRING ) ) == NULL )` |  | pending |
| `db.boot_db.if.002` | 271 | `if ( time_info.hour <  5 )` |  | pending |
| `db.boot_db.if.003` | 272 | `if ( time_info.hour <  6 )` |  | pending |
| `db.boot_db.if.004` | 273 | `if ( time_info.hour < 19 )` |  | pending |
| `db.boot_db.if.005` | 274 | `if ( time_info.hour < 20 )` |  | pending |
| `db.boot_db.if.006` | 279 | `if ( time_info.month >= 7 && time_info.month <=12 )` |  | pending |
| `db.boot_db.and.001` | 279 | `&& time_info.month <=12 )` |  | pending |
| `db.boot_db.if.007` | 284 | `if ( weather_info.mmhg <=  980 )` |  | pending |
| `db.boot_db.if.008` | 285 | `if ( weather_info.mmhg <= 1000 )` |  | pending |
| `db.boot_db.if.009` | 286 | `if ( weather_info.mmhg <= 1020 )` |  | pending |
| `db.boot_db.for.001` | 297 | `for ( sn = 0; sn < MAX_SKILL; sn++ )` |  | pending |
| `db.boot_db.if.010` | 299 | `if ( skill_table[sn].pgsn != NULL )` |  | pending |
| `db.boot_db.if.011` | 310 | `if ( ( fpList = fopen( AREA_LIST, "r" ) ) == NULL )` |  | pending |
| `db.boot_db.for.002` | 316 | `for ( ; ; )` |  | pending |
| `db.boot_db.if.012` | 319 | `if ( strArea[0] == '$' )` |  | pending |
| `db.boot_db.break.001` | 320 | `break;` |  | pending |
| `db.boot_db.if.013` | 322 | `if ( strArea[0] == '-' )` |  | pending |
| `db.boot_db.if.014` | 328 | `if ( ( fpArea = fopen( strArea, "r" ) ) == NULL )` |  | pending |
| `db.boot_db.for.003` | 335 | `for ( ; ; )` |  | pending |
| `db.boot_db.if.015` | 339 | `if ( fread_letter( fpArea ) != '#' )` |  | pending |
| `db.boot_db.if.016` | 347 | `if ( word[0] == '$'               )` |  | pending |
| `db.boot_db.break.002` | 347 | `break;` |  | pending |
| `db.boot_db.if.017` | 348 | `if ( !str_cmp( word, "AREA"     ) )` |  | pending |
| `db.boot_db.if.018` | 349 | `if ( !str_cmp( word, "HELPS"    ) )` |  | pending |
| `db.boot_db.if.019` | 350 | `if ( !str_cmp( word, "MOBOLD"   ) )` |  | pending |
| `db.boot_db.if.020` | 351 | `if ( !str_cmp( word, "MOBILES"  ) )` |  | pending |
| `db.boot_db.if.021` | 352 | `if ( !str_cmp( word, "OBJOLD"   ) )` |  | pending |
| `db.boot_db.if.022` | 353 | `if ( !str_cmp( word, "OBJECTS"  ) )` |  | pending |
| `db.boot_db.if.023` | 354 | `if ( !str_cmp( word, "RESETS"   ) )` |  | pending |
| `db.boot_db.if.024` | 355 | `if ( !str_cmp( word, "ROOMS"    ) )` |  | pending |
| `db.boot_db.if.025` | 356 | `if ( !str_cmp( word, "SHOPS"    ) )` |  | pending |
| `db.boot_db.if.026` | 357 | `if ( !str_cmp( word, "SOCIALS"  ) )` |  | pending |
| `db.boot_db.if.027` | 358 | `if ( !str_cmp( word, "SPECIALS" ) )` |  | pending |
| `db.boot_db.if.028` | 366 | `if ( fpArea != stdin )` |  | pending |
| `db.boot_db.return.001` | 388 | `return;` |  | pending |

## load_area

[Source line 396](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:396); ends at line 421. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:348` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:212` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `fread_string`, `fread_number`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.load_area.if.001` | 412 | `if ( area_first == NULL )` |  | pending |
| `db.load_area.if.002` | 414 | `if ( area_last  != NULL )` |  | pending |
| `db.load_area.return.001` | 420 | `return;` |  | pending |

## load_helps

[Source line 428](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:428); ends at line 455. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:349` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:213` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `fread_number`, `fread_string`, `str_cmp`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.load_helps.for.001` | 432 | `for ( ; ; )` |  | pending |
| `db.load_helps.if.001` | 437 | `if ( pHelp->keyword[0] == '$' )` |  | pending |
| `db.load_helps.break.001` | 438 | `break;` |  | pending |
| `db.load_helps.if.002` | 441 | `if ( !str_cmp( pHelp->keyword, "greeting" ) )` |  | pending |
| `db.load_helps.if.003` | 444 | `if ( help_first == NULL )` |  | pending |
| `db.load_helps.if.004` | 446 | `if ( help_last  != NULL )` |  | pending |
| `db.load_helps.return.001` | 454 | `return;` |  | pending |

## load_old_mob

[Source line 462](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:462); ends at line 584. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:350` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:214` (declaration_or_dispatch_reference).

Dependencies: `fread_letter`, `bug`, `exit`, `fread_number`, `get_mob_index`, `alloc_perm`, `fread_string`, `UPPER`, `fread_flag`, `one_argument`, `race_lookup`, `URANGE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.load_old_mob.for.001` | 469 | `for ( ; ; )` |  | pending |
| `db.load_old_mob.if.001` | 476 | `if ( letter != '#' )` |  | pending |
| `db.load_old_mob.if.002` | 483 | `if ( vnum == 0 )` |  | pending |
| `db.load_old_mob.break.001` | 484 | `break;` |  | pending |
| `db.load_old_mob.if.003` | 487 | `if ( get_mob_index( vnum ) != NULL )` |  | pending |
| `db.load_old_mob.if.004` | 533 | `if (pMobIndex->start_pos < POS_SLEEPING)` |  | pending |
| `db.load_old_mob.if.005` | 535 | `if (pMobIndex->default_pos < POS_SLEEPING)` |  | pending |
| `db.load_old_mob.if.006` | 546 | `if (name[0] == '\0' \|\| (race =  race_lookup(name)) == 0)` |  | pending |
| `db.load_old_mob.or.001` | 546 | `\|\| (race =  race_lookup(name)) == 0)` |  | pending |
| `db.load_old_mob.if.007` | 570 | `if ( letter != 'S' )` |  | pending |
| `db.load_old_mob.return.001` | 583 | `return;` |  | pending |

## load_old_obj

[Source line 589](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:589); ends at line 730. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:352` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:216` (declaration_or_dispatch_reference).

Dependencies: `fread_letter`, `bug`, `exit`, `fread_number`, `get_obj_index`, `alloc_perm`, `fread_string`, `LOWER`, `UPPER`, `str_dup`, `fread_flag`, `is_name`, `SET_BIT`, `ungetc`, `slot_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.load_old_obj.for.001` | 593 | `for ( ; ; )` |  | pending |
| `db.load_old_obj.if.001` | 600 | `if ( letter != '#' )` |  | pending |
| `db.load_old_obj.if.002` | 607 | `if ( vnum == 0 )` |  | pending |
| `db.load_old_obj.break.001` | 608 | `break;` |  | pending |
| `db.load_old_obj.if.003` | 611 | `if ( get_obj_index( vnum ) != NULL )` |  | pending |
| `db.load_old_obj.if.004` | 646 | `if (pObjIndex->item_type == ITEM_WEAPON)` |  | pending |
| `db.load_old_obj.if.005` | 648 | `if (is_name("two",pObjIndex->name)  	    \|\|  is_name("two-handed",pObjIndex->name)  	    \|\|  is_name("claymore",pObjIndex->name))` |  | pending |
| `db.load_old_obj.or.001` | 649 | `\|\|  is_name("two-handed",pObjIndex->name)` |  | pending |
| `db.load_old_obj.or.002` | 650 | `\|\|  is_name("claymore",pObjIndex->name))` |  | pending |
| `db.load_old_obj.for.002` | 654 | `for ( ; ; )` |  | pending |
| `db.load_old_obj.if.006` | 660 | `if ( letter == 'A' )` |  | pending |
| `db.load_old_obj.if.007` | 677 | `if ( letter == 'E' )` |  | pending |
| `db.load_old_obj.break.002` | 692 | `break;` |  | pending |
| `db.load_old_obj.if.008` | 697 | `if (pObjIndex->item_type == ITEM_ARMOR)` |  | pending |
| `db.load_old_obj.switch.001` | 706 | `switch ( pObjIndex->item_type )` |  | pending |
| `db.load_old_obj.case.001` | 708 | `case ITEM_PILL:` |  | pending |
| `db.load_old_obj.case.002` | 709 | `case ITEM_POTION:` |  | pending |
| `db.load_old_obj.case.003` | 710 | `case ITEM_SCROLL:` |  | pending |
| `db.load_old_obj.break.003` | 715 | `break;` |  | pending |
| `db.load_old_obj.case.004` | 717 | `case ITEM_STAFF:` |  | pending |
| `db.load_old_obj.case.005` | 718 | `case ITEM_WAND:` |  | pending |
| `db.load_old_obj.break.004` | 720 | `break;` |  | pending |
| `db.load_old_obj.return.001` | 729 | `return;` |  | pending |

## load_resets

[Source line 739](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:739); ends at line 853. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:354` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:218` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`, `fread_letter`, `fread_to_eol`, `alloc_perm`, `fread_number`, `get_mob_index`, `get_room_index`, `get_obj_index`, `IS_SET`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.load_resets.if.001` | 743 | `if ( area_last == NULL )` |  | pending |
| `db.load_resets.for.001` | 749 | `for ( ; ; )` |  | pending |
| `db.load_resets.if.002` | 756 | `if ( ( letter = fread_letter( fp ) ) == 'S' )` |  | pending |
| `db.load_resets.break.001` | 757 | `break;` |  | pending |
| `db.load_resets.if.003` | 759 | `if ( letter == '*' )` |  | pending |
| `db.load_resets.continue.001` | 762 | `continue;` |  | pending |
| `db.load_resets.or.001` | 770 | `\|\| letter == 'R')` |  | pending |
| `db.load_resets.ternary.001` | 771 | `? 0 : fread_number( fp );` |  | pending |
| `db.load_resets.or.002` | 772 | `\|\| letter == 'M')` |  | pending |
| `db.load_resets.ternary.002` | 773 | `? fread_number(fp) : 0;` |  | pending |
| `db.load_resets.switch.001` | 780 | `switch ( letter )` |  | pending |
| `db.load_resets.default.001` | 782 | `default:` |  | pending |
| `db.load_resets.break.002` | 785 | `break;` |  | pending |
| `db.load_resets.case.001` | 787 | `case 'M':` |  | pending |
| `db.load_resets.break.003` | 790 | `break;` |  | pending |
| `db.load_resets.case.002` | 792 | `case 'O':` |  | pending |
| `db.load_resets.break.004` | 796 | `break;` |  | pending |
| `db.load_resets.case.003` | 798 | `case 'P':` |  | pending |
| `db.load_resets.break.005` | 802 | `break;` |  | pending |
| `db.load_resets.case.004` | 804 | `case 'G':` |  | pending |
| `db.load_resets.case.005` | 805 | `case 'E':` |  | pending |
| `db.load_resets.break.006` | 808 | `break;` |  | pending |
| `db.load_resets.case.006` | 810 | `case 'D':` |  | pending |
| `db.load_resets.if.004` | 813 | `if ( pReset->arg2 < 0 	    \|\|   pReset->arg2 > 5 	    \|\| ( pexit = pRoomIndex->exit[pReset->arg2] ) == NULL 	    \|\| !IS_SET( pexit->exit_info, EX_ISDOOR ) )` |  | pending |
| `db.load_resets.or.003` | 814 | `\|\|   pReset->arg2 > 5` |  | pending |
| `db.load_resets.or.004` | 815 | `\|\| ( pexit = pRoomIndex->exit[pReset->arg2] ) == NULL` |  | pending |
| `db.load_resets.or.005` | 816 | `\|\| !IS_SET( pexit->exit_info, EX_ISDOOR ) )` |  | pending |
| `db.load_resets.if.005` | 822 | `if ( pReset->arg3 < 0 \|\| pReset->arg3 > 2 )` |  | pending |
| `db.load_resets.or.006` | 822 | `\|\| pReset->arg3 > 2 )` |  | pending |
| `db.load_resets.break.007` | 828 | `break;` |  | pending |
| `db.load_resets.case.007` | 830 | `case 'R':` |  | pending |
| `db.load_resets.if.006` | 833 | `if ( pReset->arg2 < 0 \|\| pReset->arg2 > 6 )` |  | pending |
| `db.load_resets.or.007` | 833 | `\|\| pReset->arg2 > 6 )` |  | pending |
| `db.load_resets.break.008` | 839 | `break;` |  | pending |
| `db.load_resets.if.007` | 842 | `if ( area_last->reset_first == NULL )` |  | pending |
| `db.load_resets.if.008` | 844 | `if ( area_last->reset_last  != NULL )` |  | pending |
| `db.load_resets.return.001` | 852 | `return;` |  | pending |

## load_rooms

[Source line 860](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:860); ends at line 1013. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:355` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:219` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`, `fread_letter`, `fread_number`, `get_room_index`, `alloc_perm`, `str_dup`, `fread_string`, `fread_flag`, `SET_BIT`, `clan_lookup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.load_rooms.if.001` | 864 | `if ( area_last == NULL )` |  | pending |
| `db.load_rooms.for.001` | 870 | `for ( ; ; )` |  | pending |
| `db.load_rooms.if.002` | 878 | `if ( letter != '#' )` |  | pending |
| `db.load_rooms.if.003` | 885 | `if ( vnum == 0 )` |  | pending |
| `db.load_rooms.break.001` | 886 | `break;` |  | pending |
| `db.load_rooms.if.004` | 889 | `if ( get_room_index( vnum ) != NULL )` |  | pending |
| `db.load_rooms.if.005` | 908 | `if ( 3000 <= vnum && vnum < 3400)` |  | pending |
| `db.load_rooms.and.001` | 908 | `&& vnum < 3400)` |  | pending |
| `db.load_rooms.for.002` | 912 | `for ( door = 0; door <= 5; door++ )` |  | pending |
| `db.load_rooms.for.003` | 919 | `for ( ; ; )` |  | pending |
| `db.load_rooms.if.006` | 923 | `if ( letter == 'S' )` |  | pending |
| `db.load_rooms.break.002` | 924 | `break;` |  | pending |
| `db.load_rooms.if.007` | 926 | `if ( letter == 'H')` |  | pending |
| `db.load_rooms.if.008` | 929 | `if ( letter == 'M')` |  | pending |
| `db.load_rooms.if.009` | 932 | `if ( letter == 'C')` |  | pending |
| `db.load_rooms.if.010` | 934 | `if (pRoomIndex->clan)` |  | pending |
| `db.load_rooms.if.011` | 943 | `if ( letter == 'D' )` |  | pending |
| `db.load_rooms.if.012` | 949 | `if ( door < 0 \|\| door > 5 )` |  | pending |
| `db.load_rooms.or.001` | 949 | `\|\| door > 5 )` |  | pending |
| `db.load_rooms.switch.001` | 963 | `switch ( locks )` |  | pending |
| `db.load_rooms.case.001` | 965 | `case 1: pexit->exit_info = EX_ISDOOR;` |  | pending |
| `db.load_rooms.break.003` | 965 | `break;` |  | pending |
| `db.load_rooms.case.002` | 966 | `case 2: pexit->exit_info = EX_ISDOOR \| EX_PICKPROOF;` |  | pending |
| `db.load_rooms.break.004` | 966 | `break;` |  | pending |
| `db.load_rooms.case.003` | 967 | `case 3: pexit->exit_info = EX_ISDOOR \| EX_NOPASS;` |  | pending |
| `db.load_rooms.break.005` | 967 | `break;` |  | pending |
| `db.load_rooms.case.004` | 968 | `case 4: pexit->exit_info = EX_ISDOOR\|EX_NOPASS\|EX_PICKPROOF;` |  | pending |
| `db.load_rooms.break.006` | 969 | `break;` |  | pending |
| `db.load_rooms.if.013` | 976 | `if ( letter == 'E' )` |  | pending |
| `db.load_rooms.if.014` | 988 | `if (letter == 'O')` |  | pending |
| `db.load_rooms.if.015` | 990 | `if (pRoomIndex->owner[0] != '\0')` |  | pending |
| `db.load_rooms.return.001` | 1012 | `return;` |  | pending |

## load_shops

[Source line 1020](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1020); ends at line 1054. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:356` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:220` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `fread_number`, `fread_to_eol`, `get_mob_index`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.load_shops.for.001` | 1024 | `for ( ; ; )` |  | pending |
| `db.load_shops.if.001` | 1031 | `if ( pShop->keeper == 0 )` |  | pending |
| `db.load_shops.break.001` | 1032 | `break;` |  | pending |
| `db.load_shops.for.002` | 1033 | `for ( iTrade = 0; iTrade < MAX_TRADE; iTrade++ )` |  | pending |
| `db.load_shops.if.002` | 1043 | `if ( shop_first == NULL )` |  | pending |
| `db.load_shops.if.003` | 1045 | `if ( shop_last  != NULL )` |  | pending |
| `db.load_shops.return.001` | 1053 | `return;` |  | pending |

## load_specials

[Source line 1060](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1060); ends at line 1092. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:358` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:222` (declaration_or_dispatch_reference).

Dependencies: `fread_letter`, `bug`, `exit`, `get_mob_index`, `fread_number`, `spec_lookup`, `fread_word`, `fread_to_eol`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.load_specials.for.001` | 1062 | `for ( ; ; )` |  | pending |
| `db.load_specials.switch.001` | 1067 | `switch ( letter = fread_letter( fp ) )` |  | pending |
| `db.load_specials.default.001` | 1069 | `default:` |  | pending |
| `db.load_specials.case.001` | 1073 | `case 'S':` |  | pending |
| `db.load_specials.return.001` | 1074 | `return;` |  | pending |
| `db.load_specials.case.002` | 1076 | `case '*':` |  | pending |
| `db.load_specials.break.001` | 1077 | `break;` |  | pending |
| `db.load_specials.case.003` | 1079 | `case 'M':` |  | pending |
| `db.load_specials.if.001` | 1082 | `if ( pMobIndex->spec_fun == 0 )` |  | pending |
| `db.load_specials.break.002` | 1087 | `break;` |  | pending |

## fix_exits

[Source line 1100](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1100); ends at line 1165. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:380` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:226` (declaration_or_dispatch_reference).

Dependencies: `get_room_index`, `SET_BIT`, `sprintf`, `bug`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.fix_exits.for.001` | 1111 | `for ( iHash = 0; iHash < MAX_KEY_HASH; iHash++ )` |  | pending |
| `db.fix_exits.for.002` | 1113 | `for ( pRoomIndex  = room_index_hash[iHash]; 	      pRoomIndex != NULL; 	      pRoomIndex  = pRoomIndex->next )` |  | pending |
| `db.fix_exits.for.003` | 1120 | `for ( door = 0; door <= 5; door++ )` |  | pending |
| `db.fix_exits.if.001` | 1122 | `if ( ( pexit = pRoomIndex->exit[door] ) != NULL )` |  | pending |
| `db.fix_exits.if.002` | 1124 | `if ( pexit->u1.vnum <= 0  		    \|\| get_room_index(pexit->u1.vnum) == NULL)` |  | pending |
| `db.fix_exits.or.001` | 1125 | `\|\| get_room_index(pexit->u1.vnum) == NULL)` |  | pending |
| `db.fix_exits.if.003` | 1134 | `if (!fexit)` |  | pending |
| `db.fix_exits.for.004` | 1139 | `for ( iHash = 0; iHash < MAX_KEY_HASH; iHash++ )` |  | pending |
| `db.fix_exits.for.005` | 1141 | `for ( pRoomIndex  = room_index_hash[iHash]; 	      pRoomIndex != NULL; 	      pRoomIndex  = pRoomIndex->next )` |  | pending |
| `db.fix_exits.for.006` | 1145 | `for ( door = 0; door <= 5; door++ )` |  | pending |
| `db.fix_exits.if.004` | 1147 | `if ( ( pexit     = pRoomIndex->exit[door]       ) != NULL 		&&   ( to_room   = pexit->u1.to_room            ) != NULL 		&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != NULL 		&&   pexit_rev->u1.to_room != pRoomIndex  		&&   (pRoomIndex->vnum < 1200 \|\| pRoomIndex->vnum > 1299))` |  | pending |
| `db.fix_exits.and.001` | 1148 | `&&   ( to_room   = pexit->u1.to_room            ) != NULL` |  | pending |
| `db.fix_exits.and.002` | 1149 | `&&   ( pexit_rev = to_room->exit[rev_dir[door]] ) != NULL` |  | pending |
| `db.fix_exits.and.003` | 1150 | `&&   pexit_rev->u1.to_room != pRoomIndex` |  | pending |
| `db.fix_exits.and.004` | 1151 | `&&   (pRoomIndex->vnum < 1200 \|\| pRoomIndex->vnum > 1299))` |  | pending |
| `db.fix_exits.or.002` | 1151 | `\|\| pRoomIndex->vnum > 1299))` |  | pending |
| `db.fix_exits.ternary.001` | 1157 | `? 0 : pexit_rev->u1.to_room->vnum );` |  | pending |
| `db.fix_exits.return.001` | 1164 | `return;` |  | pending |

## area_update

[Source line 1172](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1172); ends at line 1206. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:382` (lexical_call_candidate).
- update_handler: `src/update.c:1093` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2118` (declaration_or_dispatch_reference).

Dependencies: `reset_area`, `sprintf`, `wiznet`, `number_range`, `get_room_index`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.area_update.for.001` | 1177 | `for ( pArea = area_first; pArea != NULL; pArea = pArea->next )` |  | pending |
| `db.area_update.if.001` | 1180 | `if ( ++pArea->age < 3 )` |  | pending |
| `db.area_update.continue.001` | 1181 | `continue;` |  | pending |
| `db.area_update.if.002` | 1187 | `if ( (!pArea->empty && (pArea->nplayer == 0 \|\| pArea->age >= 15)) 	\|\|    pArea->age >= 31)` |  | pending |
| `db.area_update.and.001` | 1187 | `&& (pArea->nplayer == 0 \|\| pArea->age >= 15))` |  | pending |
| `db.area_update.or.001` | 1187 | `\|\| pArea->age >= 15))` |  | pending |
| `db.area_update.or.002` | 1188 | `\|\|    pArea->age >= 31)` |  | pending |
| `db.area_update.if.003` | 1198 | `if ( pRoomIndex != NULL && pArea == pRoomIndex->area )` |  | pending |
| `db.area_update.and.002` | 1198 | `&& pArea == pRoomIndex->area )` |  | pending |
| `db.area_update.if.004` | 1200 | `if (pArea->nplayer == 0)` |  | pending |
| `db.area_update.return.001` | 1205 | `return;` |  | pending |

## reset_area

[Source line 1213](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1213); ends at line 1509. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- area_update: `src/db.c:1192` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:228` (declaration_or_dispatch_reference).

Dependencies: `bug`, `get_mob_index`, `get_room_index`, `create_mobile`, `IS_SET`, `SET_BIT`, `char_to_room`, `URANGE`, `get_obj_index`, `count_obj_list`, `create_object`, `UMIN`, `number_fuzzy`, `obj_to_room`, `get_obj_type`, `number_range`, `obj_to_obj`, `UMAX`, `fprintf`, `obj_to_char`, `equip_char`, `REMOVE_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.reset_area.for.001` | 1223 | `for ( pReset = pArea->reset_first; pReset != NULL; pReset = pReset->next )` |  | pending |
| `db.reset_area.switch.001` | 1234 | `switch ( pReset->command )` |  | pending |
| `db.reset_area.default.001` | 1236 | `default:` |  | pending |
| `db.reset_area.break.001` | 1238 | `break;` |  | pending |
| `db.reset_area.case.001` | 1240 | `case 'M':` |  | pending |
| `db.reset_area.if.001` | 1241 | `if ( ( pMobIndex = get_mob_index( pReset->arg1 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.001` | 1244 | `continue;` |  | pending |
| `db.reset_area.if.002` | 1247 | `if ( ( pRoomIndex = get_room_index( pReset->arg3 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.002` | 1250 | `continue;` |  | pending |
| `db.reset_area.if.003` | 1253 | `if ( pMobIndex->count >= pReset->arg2 )` |  | pending |
| `db.reset_area.break.002` | 1256 | `break;` |  | pending |
| `db.reset_area.for.002` | 1260 | `for (mob = pRoomIndex->people; mob != NULL; mob = mob->next_in_room)` |  | pending |
| `db.reset_area.if.004` | 1261 | `if (mob->pIndexData == pMobIndex)` |  | pending |
| `db.reset_area.if.005` | 1264 | `if (count >= pReset->arg4)` |  | pending |
| `db.reset_area.break.003` | 1267 | `break;` |  | pending |
| `db.reset_area.if.006` | 1271 | `if (count >= pReset->arg4)` |  | pending |
| `db.reset_area.break.004` | 1272 | `break;` |  | pending |
| `db.reset_area.if.007` | 1282 | `if ( pRoomIndexPrev != NULL 		&&   IS_SET(pRoomIndexPrev->room_flags, ROOM_PET_SHOP) )` |  | pending |
| `db.reset_area.and.001` | 1283 | `&&   IS_SET(pRoomIndexPrev->room_flags, ROOM_PET_SHOP) )` |  | pending |
| `db.reset_area.break.005` | 1293 | `break;` |  | pending |
| `db.reset_area.case.002` | 1295 | `case 'O':` |  | pending |
| `db.reset_area.if.008` | 1296 | `if ( ( pObjIndex = get_obj_index( pReset->arg1 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.003` | 1299 | `continue;` |  | pending |
| `db.reset_area.if.009` | 1302 | `if ( ( pRoomIndex = get_room_index( pReset->arg3 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.004` | 1305 | `continue;` |  | pending |
| `db.reset_area.if.010` | 1308 | `if ( pArea->nplayer > 0 	    \|\|   count_obj_list( pObjIndex, pRoomIndex->contents ) > 0 )` |  | pending |
| `db.reset_area.or.001` | 1309 | `\|\|   count_obj_list( pObjIndex, pRoomIndex->contents ) > 0 )` |  | pending |
| `db.reset_area.break.006` | 1312 | `break;` |  | pending |
| `db.reset_area.break.007` | 1320 | `break;` |  | pending |
| `db.reset_area.case.003` | 1322 | `case 'P':` |  | pending |
| `db.reset_area.if.011` | 1323 | `if ( ( pObjIndex = get_obj_index( pReset->arg1 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.005` | 1326 | `continue;` |  | pending |
| `db.reset_area.if.012` | 1329 | `if ( ( pObjToIndex = get_obj_index( pReset->arg3 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.006` | 1332 | `continue;` |  | pending |
| `db.reset_area.if.013` | 1335 | `if (pReset->arg2 > 50)` |  | pending |
| `db.reset_area.if.014` | 1337 | `if (pReset->arg2 == -1)` |  | pending |
| `db.reset_area.if.015` | 1342 | `if (pArea->nplayer > 0 	    \|\| (obj_to = get_obj_type( pObjToIndex ) ) == NULL 	    \|\| (obj_to->in_room == NULL && !last) 	    \|\| ( pObjIndex->count >= limit && number_range(0,4) != 0) 	    \|\| (count = count_obj_list(pObjIndex,obj_to->contains))  		> pReset->arg4 )` |  | pending |
| `db.reset_area.or.002` | 1343 | `\|\| (obj_to = get_obj_type( pObjToIndex ) ) == NULL` |  | pending |
| `db.reset_area.or.003` | 1344 | `\|\| (obj_to->in_room == NULL && !last)` |  | pending |
| `db.reset_area.and.002` | 1344 | `&& !last)` |  | pending |
| `db.reset_area.or.004` | 1345 | `\|\| ( pObjIndex->count >= limit && number_range(0,4) != 0)` |  | pending |
| `db.reset_area.and.003` | 1345 | `&& number_range(0,4) != 0)` |  | pending |
| `db.reset_area.or.005` | 1346 | `\|\| (count = count_obj_list(pObjIndex,obj_to->contains))` |  | pending |
| `db.reset_area.break.008` | 1350 | `break;` |  | pending |
| `db.reset_area.while.001` | 1353 | `while (count < pReset->arg4)` |  | pending |
| `db.reset_area.if.016` | 1358 | `if (pObjIndex->count >= limit)` |  | pending |
| `db.reset_area.break.009` | 1359 | `break;` |  | pending |
| `db.reset_area.break.010` | 1364 | `break;` |  | pending |
| `db.reset_area.case.004` | 1366 | `case 'G':` |  | pending |
| `db.reset_area.case.005` | 1367 | `case 'E':` |  | pending |
| `db.reset_area.if.017` | 1368 | `if ( ( pObjIndex = get_obj_index( pReset->arg1 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.007` | 1371 | `continue;` |  | pending |
| `db.reset_area.if.018` | 1374 | `if ( !last )` |  | pending |
| `db.reset_area.break.011` | 1375 | `break;` |  | pending |
| `db.reset_area.if.019` | 1377 | `if ( mob == NULL )` |  | pending |
| `db.reset_area.break.012` | 1382 | `break;` |  | pending |
| `db.reset_area.if.020` | 1385 | `if ( mob->pIndexData->pShop != NULL )` |  | pending |
| `db.reset_area.if.021` | 1389 | `if (!pObjIndex->new_format)` |  | pending |
| `db.reset_area.switch.002` | 1390 | `switch ( pObjIndex->item_type )` |  | pending |
| `db.reset_area.case.006` | 1392 | `case ITEM_PILL:` |  | pending |
| `db.reset_area.case.007` | 1393 | `case ITEM_POTION:` |  | pending |
| `db.reset_area.case.008` | 1394 | `case ITEM_SCROLL:` |  | pending |
| `db.reset_area.for.003` | 1396 | `for (i = 1; i < 5; i++)` |  | pending |
| `db.reset_area.if.022` | 1398 | `if (pObjIndex->value[i] > 0)` |  | pending |
| `db.reset_area.for.004` | 1400 | `for (j = 0; j < MAX_CLASS; j++)` |  | pending |
| `db.reset_area.break.013` | 1410 | `break;` |  | pending |
| `db.reset_area.case.009` | 1411 | `case ITEM_WAND:		olevel = number_range( 10, 20 );` |  | pending |
| `db.reset_area.break.014` | 1411 | `break;` |  | pending |
| `db.reset_area.case.010` | 1412 | `case ITEM_STAFF:	olevel = number_range( 15, 25 );` |  | pending |
| `db.reset_area.break.015` | 1412 | `break;` |  | pending |
| `db.reset_area.case.011` | 1413 | `case ITEM_ARMOR:	olevel = number_range(  5, 15 );` |  | pending |
| `db.reset_area.break.016` | 1413 | `break;` |  | pending |
| `db.reset_area.case.012` | 1414 | `case ITEM_WEAPON:	olevel = number_range(  5, 15 );` |  | pending |
| `db.reset_area.break.017` | 1414 | `break;` |  | pending |
| `db.reset_area.case.013` | 1415 | `case ITEM_TREASURE:	olevel = number_range( 10, 20 );` |  | pending |
| `db.reset_area.break.018` | 1415 | `break;` |  | pending |
| `db.reset_area.if.023` | 1424 | `if (pReset->arg2 > 50)` |  | pending |
| `db.reset_area.if.024` | 1426 | `if (pReset->arg2 == -1)` |  | pending |
| `db.reset_area.if.025` | 1431 | `if (pObjIndex->count < limit \|\| number_range(0,4) == 0)` |  | pending |
| `db.reset_area.or.006` | 1431 | `\|\| number_range(0,4) == 0)` |  | pending |
| `db.reset_area.if.026` | 1436 | `if (obj->level > mob->level + 3 		    \|\|  (obj->item_type == ITEM_WEAPON  		    &&   pReset->command == 'E'  		    &&   obj->level < mob->level -5 && obj->level < 45))` |  | pending |
| `db.reset_area.or.007` | 1437 | `\|\|  (obj->item_type == ITEM_WEAPON` |  | pending |
| `db.reset_area.and.004` | 1438 | `&&   pReset->command == 'E'` |  | pending |
| `db.reset_area.and.005` | 1439 | `&&   obj->level < mob->level -5 && obj->level < 45))` |  | pending |
| `db.reset_area.and.006` | 1439 | `&& obj->level < 45))` |  | pending |
| `db.reset_area.break.019` | 1446 | `break;` |  | pending |
| `db.reset_area.if.027` | 1449 | `if ( pReset->command == 'E' )` |  | pending |
| `db.reset_area.break.020` | 1452 | `break;` |  | pending |
| `db.reset_area.case.014` | 1454 | `case 'D':` |  | pending |
| `db.reset_area.if.028` | 1455 | `if ( ( pRoomIndex = get_room_index( pReset->arg1 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.008` | 1458 | `continue;` |  | pending |
| `db.reset_area.if.029` | 1461 | `if ( ( pexit = pRoomIndex->exit[pReset->arg2] ) == NULL )` |  | pending |
| `db.reset_area.break.021` | 1462 | `break;` |  | pending |
| `db.reset_area.switch.003` | 1464 | `switch ( pReset->arg3 )` |  | pending |
| `db.reset_area.case.015` | 1466 | `case 0:` |  | pending |
| `db.reset_area.break.022` | 1469 | `break;` |  | pending |
| `db.reset_area.case.016` | 1471 | `case 1:` |  | pending |
| `db.reset_area.break.023` | 1474 | `break;` |  | pending |
| `db.reset_area.case.017` | 1476 | `case 2:` |  | pending |
| `db.reset_area.break.024` | 1479 | `break;` |  | pending |
| `db.reset_area.break.025` | 1483 | `break;` |  | pending |
| `db.reset_area.case.018` | 1485 | `case 'R':` |  | pending |
| `db.reset_area.if.030` | 1486 | `if ( ( pRoomIndex = get_room_index( pReset->arg1 ) ) == NULL )` |  | pending |
| `db.reset_area.continue.009` | 1489 | `continue;` |  | pending |
| `db.reset_area.for.005` | 1496 | `for ( d0 = 0; d0 < pReset->arg2 - 1; d0++ )` |  | pending |
| `db.reset_area.break.026` | 1504 | `break;` |  | pending |
| `db.reset_area.return.001` | 1508 | `return;` |  | pending |

## create_mobile

[Source line 1516](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1516); ends at line 1741. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_buy: `src/act_obj.c:2586` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2406` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2482` (lexical_call_candidate).
- reset_area: `src/db.c:1274` (lexical_call_candidate).
- fread_pet: `src/save.c:1148` (lexical_call_candidate).
- fread_pet: `src/save.c:1151` (lexical_call_candidate).
- fread_pet: `src/save.c:1156` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2119` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`, `new_char`, `get_mob_id`, `number_range`, `dice`, `case`, `str_dup`, `UMIN`, `IS_SET`, `IS_AFFECTED`, `skill_lookup`, `affect_to_char`, `interpolate`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.create_mobile.if.001` | 1524 | `if ( pMobIndex == NULL )` |  | pending |
| `db.create_mobile.if.002` | 1542 | `if (pMobIndex->wealth == 0)` |  | pending |
| `db.create_mobile.if.003` | 1556 | `if (pMobIndex->new_format)` |  | pending |
| `db.create_mobile.if.004` | 1579 | `if (mob->dam_type == 0)` |  | pending |
| `db.create_mobile.switch.001` | 1580 | `switch(number_range(1,3))` |  | pending |
| `db.create_mobile.case.001` | 1582 | `case (1): mob->dam_type = 3;` |  | pending |
| `db.create_mobile.break.001` | 1582 | `break;` |  | pending |
| `db.create_mobile.case.002` | 1583 | `case (2): mob->dam_type = 7;` |  | pending |
| `db.create_mobile.break.002` | 1583 | `break;` |  | pending |
| `db.create_mobile.case.003` | 1584 | `case (3): mob->dam_type = 11;` |  | pending |
| `db.create_mobile.break.003` | 1584 | `break;` |  | pending |
| `db.create_mobile.for.001` | 1586 | `for (i = 0; i < 4; i++)` |  | pending |
| `db.create_mobile.if.005` | 1595 | `if (mob->sex == 3)` |  | pending |
| `db.create_mobile.for.002` | 1605 | `for (i = 0; i < MAX_STATS; i ++)` |  | pending |
| `db.create_mobile.if.006` | 1608 | `if (IS_SET(mob->act,ACT_WARRIOR))` |  | pending |
| `db.create_mobile.if.007` | 1615 | `if (IS_SET(mob->act,ACT_THIEF))` |  | pending |
| `db.create_mobile.if.008` | 1622 | `if (IS_SET(mob->act,ACT_CLERIC))` |  | pending |
| `db.create_mobile.if.009` | 1629 | `if (IS_SET(mob->act,ACT_MAGE))` |  | pending |
| `db.create_mobile.if.010` | 1636 | `if (IS_SET(mob->off_flags,OFF_FAST))` |  | pending |
| `db.create_mobile.if.011` | 1643 | `if (IS_AFFECTED(mob,AFF_SANCTUARY))` |  | pending |
| `db.create_mobile.if.012` | 1655 | `if (IS_AFFECTED(mob,AFF_HASTE))` |  | pending |
| `db.create_mobile.if.013` | 1668 | `if (IS_AFFECTED(mob,AFF_PROTECT_EVIL))` |  | pending |
| `db.create_mobile.if.014` | 1680 | `if (IS_AFFECTED(mob,AFF_PROTECT_GOOD))` |  | pending |
| `db.create_mobile.switch.002` | 1707 | `switch(number_range(1,3))` |  | pending |
| `db.create_mobile.case.004` | 1709 | `case (1): mob->dam_type = 3;` |  | pending |
| `db.create_mobile.break.004` | 1709 | `break;` |  | pending |
| `db.create_mobile.case.005` | 1710 | `case (2): mob->dam_type = 7;` |  | pending |
| `db.create_mobile.break.005` | 1710 | `break;` |  | pending |
| `db.create_mobile.case.006` | 1711 | `case (3): mob->dam_type = 11;` |  | pending |
| `db.create_mobile.break.006` | 1711 | `break;` |  | pending |
| `db.create_mobile.for.003` | 1713 | `for (i = 0; i < 3; i++)` |  | pending |
| `db.create_mobile.for.004` | 1729 | `for (i = 0; i < MAX_STATS; i ++)` |  | pending |
| `db.create_mobile.return.001` | 1740 | `return mob;` |  | pending |

## clone_mobile

[Source line 1744](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1744); ends at line 1816. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_clone: `src/act_wiz.c:2407` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2120` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `str_dup`, `affect_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.clone_mobile.if.001` | 1749 | `if ( parent == NULL \|\| clone == NULL \|\| !IS_NPC(parent))` |  | pending |
| `db.clone_mobile.or.001` | 1749 | `\|\| clone == NULL \|\| !IS_NPC(parent))` |  | pending |
| `db.clone_mobile.or.002` | 1749 | `\|\| !IS_NPC(parent))` |  | pending |
| `db.clone_mobile.return.001` | 1750 | `return;` |  | pending |
| `db.clone_mobile.for.001` | 1800 | `for (i = 0; i < 4; i++)` |  | pending |
| `db.clone_mobile.for.002` | 1803 | `for (i = 0; i < MAX_STATS; i++)` |  | pending |
| `db.clone_mobile.for.003` | 1809 | `for (i = 0; i < 3; i++)` |  | pending |
| `db.clone_mobile.for.004` | 1813 | `for (paf = parent->affected; paf != NULL; paf = paf->next)` |  | pending |

## create_object

[Source line 1824](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1824); ends at line 1966. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_buy: `src/act_obj.c:2724` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:245` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:253` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:275` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:284` (lexical_call_candidate).
- recursive_clone: `src/act_wiz.c:2303` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2370` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2413` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2532` (lexical_call_candidate).
- nanny: `src/comm.c:2097` (lexical_call_candidate).
- reset_area: `src/db.c:1315` (lexical_call_candidate).
- reset_area: `src/db.c:1355` (lexical_call_candidate).
- reset_area: `src/db.c:1418` (lexical_call_candidate).
- reset_area: `src/db.c:1433` (lexical_call_candidate).
- make_corpse: `src/fight.c:1438` (lexical_call_candidate).
- make_corpse: `src/fight.c:1451` (lexical_call_candidate).
- death_cry: `src/fight.c:1613` (lexical_call_candidate).
- create_money: `src/handler.c:2262` (lexical_call_candidate).
- create_money: `src/handler.c:2266` (lexical_call_candidate).
- create_money: `src/handler.c:2270` (lexical_call_candidate).
- create_money: `src/handler.c:2280` (lexical_call_candidate).
- create_money: `src/handler.c:2291` (lexical_call_candidate).
- spell_continual_light: `src/magic.c:1456` (lexical_call_candidate).
- spell_create_food: `src/magic.c:1484` (lexical_call_candidate).
- spell_create_rose: `src/magic.c:1496` (lexical_call_candidate).
- spell_create_spring: `src/magic.c:1507` (lexical_call_candidate).
- spell_floating_disc: `src/magic.c:2786` (lexical_call_candidate).
- spell_portal: `src/magic2.c:95` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:149` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:163` (lexical_call_candidate).
- fread_obj: `src/save.c:1376` (lexical_call_candidate).
- fread_obj: `src/save.c:1525` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2121` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`, `new_obj`, `UMAX`, `str_dup`, `number_fuzzy`, `affect_to_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.create_object.if.001` | 1830 | `if ( pObjIndex == NULL )` |  | pending |
| `db.create_object.if.002` | 1842 | `if (pObjIndex->new_format)` |  | pending |
| `db.create_object.if.003` | 1862 | `if (level == -1 \|\| pObjIndex->new_format)` |  | pending |
| `db.create_object.or.001` | 1862 | `\|\| pObjIndex->new_format)` |  | pending |
| `db.create_object.switch.001` | 1871 | `switch ( obj->item_type )` |  | pending |
| `db.create_object.default.001` | 1873 | `default:` |  | pending |
| `db.create_object.break.001` | 1875 | `break;` |  | pending |
| `db.create_object.case.001` | 1877 | `case ITEM_LIGHT:` |  | pending |
| `db.create_object.if.004` | 1878 | `if (obj->value[2] == 999)` |  | pending |
| `db.create_object.break.002` | 1880 | `break;` |  | pending |
| `db.create_object.case.002` | 1882 | `case ITEM_FURNITURE:` |  | pending |
| `db.create_object.case.003` | 1883 | `case ITEM_TRASH:` |  | pending |
| `db.create_object.case.004` | 1884 | `case ITEM_CONTAINER:` |  | pending |
| `db.create_object.case.005` | 1885 | `case ITEM_DRINK_CON:` |  | pending |
| `db.create_object.case.006` | 1886 | `case ITEM_KEY:` |  | pending |
| `db.create_object.case.007` | 1887 | `case ITEM_FOOD:` |  | pending |
| `db.create_object.case.008` | 1888 | `case ITEM_BOAT:` |  | pending |
| `db.create_object.case.009` | 1889 | `case ITEM_CORPSE_NPC:` |  | pending |
| `db.create_object.case.010` | 1890 | `case ITEM_CORPSE_PC:` |  | pending |
| `db.create_object.case.011` | 1891 | `case ITEM_FOUNTAIN:` |  | pending |
| `db.create_object.case.012` | 1892 | `case ITEM_MAP:` |  | pending |
| `db.create_object.case.013` | 1893 | `case ITEM_CLOTHING:` |  | pending |
| `db.create_object.case.014` | 1894 | `case ITEM_PORTAL:` |  | pending |
| `db.create_object.if.005` | 1895 | `if (!pObjIndex->new_format)` |  | pending |
| `db.create_object.break.003` | 1897 | `break;` |  | pending |
| `db.create_object.case.015` | 1899 | `case ITEM_TREASURE:` |  | pending |
| `db.create_object.case.016` | 1900 | `case ITEM_WARP_STONE:` |  | pending |
| `db.create_object.case.017` | 1901 | `case ITEM_ROOM_KEY:` |  | pending |
| `db.create_object.case.018` | 1902 | `case ITEM_GEM:` |  | pending |
| `db.create_object.case.019` | 1903 | `case ITEM_JEWELRY:` |  | pending |
| `db.create_object.break.004` | 1904 | `break;` |  | pending |
| `db.create_object.case.020` | 1906 | `case ITEM_JUKEBOX:` |  | pending |
| `db.create_object.for.001` | 1907 | `for (i = 0; i < 5; i++)` |  | pending |
| `db.create_object.break.005` | 1909 | `break;` |  | pending |
| `db.create_object.case.021` | 1911 | `case ITEM_SCROLL:` |  | pending |
| `db.create_object.if.006` | 1912 | `if (level != -1 && !pObjIndex->new_format)` |  | pending |
| `db.create_object.and.001` | 1912 | `&& !pObjIndex->new_format)` |  | pending |
| `db.create_object.break.006` | 1914 | `break;` |  | pending |
| `db.create_object.case.022` | 1916 | `case ITEM_WAND:` |  | pending |
| `db.create_object.case.023` | 1917 | `case ITEM_STAFF:` |  | pending |
| `db.create_object.if.007` | 1918 | `if (level != -1 && !pObjIndex->new_format)` |  | pending |
| `db.create_object.and.002` | 1918 | `&& !pObjIndex->new_format)` |  | pending |
| `db.create_object.if.008` | 1924 | `if (!pObjIndex->new_format)` |  | pending |
| `db.create_object.break.007` | 1926 | `break;` |  | pending |
| `db.create_object.case.024` | 1928 | `case ITEM_WEAPON:` |  | pending |
| `db.create_object.if.009` | 1929 | `if (level != -1 && !pObjIndex->new_format)` |  | pending |
| `db.create_object.and.003` | 1929 | `&& !pObjIndex->new_format)` |  | pending |
| `db.create_object.break.008` | 1934 | `break;` |  | pending |
| `db.create_object.case.025` | 1936 | `case ITEM_ARMOR:` |  | pending |
| `db.create_object.if.010` | 1937 | `if (level != -1 && !pObjIndex->new_format)` |  | pending |
| `db.create_object.and.004` | 1937 | `&& !pObjIndex->new_format)` |  | pending |
| `db.create_object.break.009` | 1943 | `break;` |  | pending |
| `db.create_object.case.026` | 1945 | `case ITEM_POTION:` |  | pending |
| `db.create_object.case.027` | 1946 | `case ITEM_PILL:` |  | pending |
| `db.create_object.if.011` | 1947 | `if (level != -1 && !pObjIndex->new_format)` |  | pending |
| `db.create_object.and.005` | 1947 | `&& !pObjIndex->new_format)` |  | pending |
| `db.create_object.break.010` | 1949 | `break;` |  | pending |
| `db.create_object.case.028` | 1951 | `case ITEM_MONEY:` |  | pending |
| `db.create_object.if.012` | 1952 | `if (!pObjIndex->new_format)` |  | pending |
| `db.create_object.break.011` | 1954 | `break;` |  | pending |
| `db.create_object.for.002` | 1957 | `for (paf = pObjIndex->affected; paf != NULL; paf = paf->next)` |  | pending |
| `db.create_object.if.013` | 1958 | `if ( paf->location == APPLY_SPELL_AFFECT )` |  | pending |
| `db.create_object.return.001` | 1965 | `return obj;` |  | pending |

## clone_object

[Source line 1969](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1969); ends at line 2011. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- recursive_clone: `src/act_wiz.c:2304` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2371` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2414` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2122` (declaration_or_dispatch_reference).

Dependencies: `str_dup`, `affect_to_obj`, `new_extra_descr`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.clone_object.if.001` | 1975 | `if (parent == NULL \|\| clone == NULL)` |  | pending |
| `db.clone_object.or.001` | 1975 | `\|\| clone == NULL)` |  | pending |
| `db.clone_object.return.001` | 1976 | `return;` |  | pending |
| `db.clone_object.for.001` | 1992 | `for (i = 0;  i < 5; i ++)` |  | pending |
| `db.clone_object.for.002` | 1998 | `for (paf = parent->affected; paf != NULL; paf = paf->next)` |  | pending |
| `db.clone_object.for.003` | 2002 | `for (ed = parent->extra_descr; ed != NULL; ed = ed->next)` |  | pending |

## clear_char

[Source line 2018](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2018); ends at line 2047. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/merc.h:2123` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.clear_char.for.001` | 2031 | `for (i = 0; i < 4; i++)` |  | pending |
| `db.clear_char.for.002` | 2041 | `for (i = 0; i < MAX_STATS; i ++)` |  | pending |
| `db.clear_char.return.001` | 2046 | `return;` |  | pending |

## get_extra_descr

[Source line 2052](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2052); ends at line 2060. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_look: `src/act_info.c:1121` (lexical_call_candidate).
- do_look: `src/act_info.c:1130` (lexical_call_candidate).
- do_look: `src/act_info.c:1153` (lexical_call_candidate).
- do_look: `src/act_info.c:1161` (lexical_call_candidate).
- do_look: `src/act_info.c:1179` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2124` (declaration_or_dispatch_reference).

Dependencies: `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.get_extra_descr.for.001` | 2054 | `for ( ; ed != NULL; ed = ed->next )` |  | pending |
| `db.get_extra_descr.if.001` | 2056 | `if ( is_name( (char *) name, ed->keyword ) )` |  | pending |
| `db.get_extra_descr.return.001` | 2057 | `return ed->description;` |  | pending |
| `db.get_extra_descr.return.002` | 2059 | `return NULL;` |  | pending |

## get_mob_index

[Source line 2068](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2068); ends at line 2087. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_mfind: `src/act_wiz.c:1795` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2476` (lexical_call_candidate).
- load_old_mob: `src/db.c:487` (lexical_call_candidate).
- load_resets: `src/db.c:788` (lexical_call_candidate).
- load_shops: `src/db.c:1040` (lexical_call_candidate).
- load_specials: `src/db.c:1080` (lexical_call_candidate).
- reset_area: `src/db.c:1241` (lexical_call_candidate).
- do_dump: `src/db.c:2904` (lexical_call_candidate).
- load_mobiles: `src/db2.c:161` (lexical_call_candidate).
- fread_char: `src/save.c:1108` (lexical_call_candidate).
- fread_pet: `src/save.c:1145` (lexical_call_candidate).
- fread_pet: `src/save.c:1148` (lexical_call_candidate).
- fread_pet: `src/save.c:1151` (lexical_call_candidate).
- fread_pet: `src/save.c:1156` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2125` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.get_mob_index.for.001` | 2072 | `for ( pMobIndex  = mob_index_hash[vnum % MAX_KEY_HASH]; 	  pMobIndex != NULL; 	  pMobIndex  = pMobIndex->next )` |  | pending |
| `db.get_mob_index.if.001` | 2076 | `if ( pMobIndex->vnum == vnum )` |  | pending |
| `db.get_mob_index.return.001` | 2077 | `return pMobIndex;` |  | pending |
| `db.get_mob_index.if.002` | 2080 | `if ( fBootDb )` |  | pending |
| `db.get_mob_index.return.002` | 2086 | `return NULL;` |  | pending |

## get_obj_index

[Source line 2095](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2095); ends at line 2114. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_outfit: `src/act_wiz.c:245` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:253` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:275` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:284` (lexical_call_candidate).
- do_ofind: `src/act_wiz.c:1846` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2526` (lexical_call_candidate).
- nanny: `src/comm.c:2097` (lexical_call_candidate).
- load_old_obj: `src/db.c:611` (lexical_call_candidate).
- load_resets: `src/db.c:793` (lexical_call_candidate).
- load_resets: `src/db.c:799` (lexical_call_candidate).
- load_resets: `src/db.c:801` (lexical_call_candidate).
- load_resets: `src/db.c:806` (lexical_call_candidate).
- reset_area: `src/db.c:1296` (lexical_call_candidate).
- reset_area: `src/db.c:1323` (lexical_call_candidate).
- reset_area: `src/db.c:1329` (lexical_call_candidate).
- reset_area: `src/db.c:1368` (lexical_call_candidate).
- do_dump: `src/db.c:2854` (lexical_call_candidate).
- do_dump: `src/db.c:2920` (lexical_call_candidate).
- load_objects: `src/db2.c:321` (lexical_call_candidate).
- make_corpse: `src/fight.c:1438` (lexical_call_candidate).
- make_corpse: `src/fight.c:1451` (lexical_call_candidate).
- death_cry: `src/fight.c:1613` (lexical_call_candidate).
- create_money: `src/handler.c:2262` (lexical_call_candidate).
- create_money: `src/handler.c:2266` (lexical_call_candidate).
- create_money: `src/handler.c:2270` (lexical_call_candidate).
- create_money: `src/handler.c:2280` (lexical_call_candidate).
- create_money: `src/handler.c:2291` (lexical_call_candidate).
- spell_continual_light: `src/magic.c:1456` (lexical_call_candidate).
- spell_create_food: `src/magic.c:1484` (lexical_call_candidate).
- spell_create_rose: `src/magic.c:1496` (lexical_call_candidate).
- spell_create_spring: `src/magic.c:1507` (lexical_call_candidate).
- spell_floating_disc: `src/magic.c:2786` (lexical_call_candidate).
- spell_portal: `src/magic2.c:95` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:149` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:163` (lexical_call_candidate).
- fread_obj: `src/save.c:1370` (lexical_call_candidate).
- fread_obj: `src/save.c:1376` (lexical_call_candidate).
- fread_obj: `src/save.c:1639` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2126` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.get_obj_index.for.001` | 2099 | `for ( pObjIndex  = obj_index_hash[vnum % MAX_KEY_HASH]; 	  pObjIndex != NULL; 	  pObjIndex  = pObjIndex->next )` |  | pending |
| `db.get_obj_index.if.001` | 2103 | `if ( pObjIndex->vnum == vnum )` |  | pending |
| `db.get_obj_index.return.001` | 2104 | `return pObjIndex;` |  | pending |
| `db.get_obj_index.if.002` | 2107 | `if ( fBootDb )` |  | pending |
| `db.get_obj_index.return.002` | 2113 | `return NULL;` |  | pending |

## get_room_index

[Source line 2122](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2122); ends at line 2141. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- get_random_room: `src/act_enter.c:48` (lexical_call_candidate).
- do_enter: `src/act_enter.c:111` (lexical_call_candidate).
- do_recall: `src/act_move.c:1416` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2532` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2534` (lexical_call_candidate).
- do_list: `src/act_obj.c:2756` (lexical_call_candidate).
- do_list: `src/act_obj.c:2758` (lexical_call_candidate).
- find_location: `src/act_wiz.c:767` (lexical_call_candidate).
- nanny: `src/comm.c:2099` (lexical_call_candidate).
- nanny: `src/comm.c:2110` (lexical_call_candidate).
- nanny: `src/comm.c:2114` (lexical_call_candidate).
- stop_idling: `src/comm.c:2321` (lexical_call_candidate).
- load_resets: `src/db.c:789` (lexical_call_candidate).
- load_resets: `src/db.c:795` (lexical_call_candidate).
- load_resets: `src/db.c:811` (lexical_call_candidate).
- load_resets: `src/db.c:831` (lexical_call_candidate).
- load_rooms: `src/db.c:889` (lexical_call_candidate).
- fix_exits: `src/db.c:1125` (lexical_call_candidate).
- fix_exits: `src/db.c:1130` (lexical_call_candidate).
- area_update: `src/db.c:1197` (lexical_call_candidate).
- reset_area: `src/db.c:1247` (lexical_call_candidate).
- reset_area: `src/db.c:1281` (lexical_call_candidate).
- reset_area: `src/db.c:1302` (lexical_call_candidate).
- reset_area: `src/db.c:1455` (lexical_call_candidate).
- reset_area: `src/db.c:1486` (lexical_call_candidate).
- char_to_room: `src/handler.c:1388` (lexical_call_candidate).
- extract_char: `src/handler.c:1960` (lexical_call_candidate).
- spell_word_of_recall: `src/magic.c:4440` (lexical_call_candidate).
- fwrite_char: `src/save.c:199` (lexical_call_candidate).
- fread_char: `src/save.c:1039` (lexical_call_candidate).
- fread_char: `src/save.c:1041` (lexical_call_candidate).
- char_update: `src/update.c:697` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2127` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.get_room_index.for.001` | 2126 | `for ( pRoomIndex  = room_index_hash[vnum % MAX_KEY_HASH]; 	  pRoomIndex != NULL; 	  pRoomIndex  = pRoomIndex->next )` |  | pending |
| `db.get_room_index.if.001` | 2130 | `if ( pRoomIndex->vnum == vnum )` |  | pending |
| `db.get_room_index.return.001` | 2131 | `return pRoomIndex;` |  | pending |
| `db.get_room_index.if.002` | 2134 | `if ( fBootDb )` |  | pending |
| `db.get_room_index.return.002` | 2140 | `return NULL;` |  | pending |

## fread_letter

[Source line 2148](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2148); ends at line 2159. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:339` (lexical_call_candidate).
- load_old_mob: `src/db.c:475` (lexical_call_candidate).
- load_old_mob: `src/db.c:509` (lexical_call_candidate).
- load_old_mob: `src/db.c:519` (lexical_call_candidate).
- load_old_mob: `src/db.c:521` (lexical_call_candidate).
- load_old_mob: `src/db.c:524` (lexical_call_candidate).
- load_old_mob: `src/db.c:526` (lexical_call_candidate).
- load_old_obj: `src/db.c:599` (lexical_call_candidate).
- load_old_obj: `src/db.c:658` (lexical_call_candidate).
- load_resets: `src/db.c:756` (lexical_call_candidate).
- load_rooms: `src/db.c:877` (lexical_call_candidate).
- load_rooms: `src/db.c:921` (lexical_call_candidate).
- load_specials: `src/db.c:1067` (lexical_call_candidate).
- load_mobiles: `src/db2.c:149` (lexical_call_candidate).
- load_mobiles: `src/db2.c:194` (lexical_call_candidate).
- load_mobiles: `src/db2.c:196` (lexical_call_candidate).
- load_mobiles: `src/db2.c:201` (lexical_call_candidate).
- load_mobiles: `src/db2.c:203` (lexical_call_candidate).
- load_mobiles: `src/db2.c:208` (lexical_call_candidate).
- load_mobiles: `src/db2.c:210` (lexical_call_candidate).
- load_mobiles: `src/db2.c:247` (lexical_call_candidate).
- load_objects: `src/db2.c:309` (lexical_call_candidate).
- load_objects: `src/db2.c:395` (lexical_call_candidate).
- load_objects: `src/db2.c:412` (lexical_call_candidate).
- load_objects: `src/db2.c:436` (lexical_call_candidate).
- load_songs: `src/music.c:177` (lexical_call_candidate).
- load_songs: `src/music.c:196` (lexical_call_candidate).
- load_char_obj: `src/save.c:600` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2128` (declaration_or_dispatch_reference).

Dependencies: `getc`, `isspace`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.fread_letter.while.001` | 2156 | `while ( isspace(c) )` |  | pending |
| `db.fread_letter.return.001` | 2158 | `return c;` |  | pending |

## fread_number

[Source line 2166](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2166); ends at line 2212. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_bans: `src/ban.c:93` (lexical_call_candidate).
- load_area: `src/db.c:406` (lexical_call_candidate).
- load_area: `src/db.c:407` (lexical_call_candidate).
- load_helps: `src/db.c:435` (lexical_call_candidate).
- load_old_mob: `src/db.c:482` (lexical_call_candidate).
- load_old_mob: `src/db.c:508` (lexical_call_candidate).
- load_old_mob: `src/db.c:510` (lexical_call_candidate).
- load_old_mob: `src/db.c:516` (lexical_call_candidate).
- load_old_mob: `src/db.c:517` (lexical_call_candidate).
- load_old_mob: `src/db.c:518` (lexical_call_candidate).
- load_old_mob: `src/db.c:520` (lexical_call_candidate).
- load_old_mob: `src/db.c:522` (lexical_call_candidate).
- load_old_mob: `src/db.c:523` (lexical_call_candidate).
- load_old_mob: `src/db.c:525` (lexical_call_candidate).
- load_old_mob: `src/db.c:527` (lexical_call_candidate).
- load_old_mob: `src/db.c:528` (lexical_call_candidate).
- load_old_mob: `src/db.c:529` (lexical_call_candidate).
- load_old_mob: `src/db.c:530` (lexical_call_candidate).
- load_old_mob: `src/db.c:531` (lexical_call_candidate).
- load_old_mob: `src/db.c:541` (lexical_call_candidate).
- load_old_obj: `src/db.c:606` (lexical_call_candidate).
- load_old_obj: `src/db.c:631` (lexical_call_candidate).
- load_old_obj: `src/db.c:634` (lexical_call_candidate).
- load_old_obj: `src/db.c:635` (lexical_call_candidate).
- load_old_obj: `src/db.c:636` (lexical_call_candidate).
- load_old_obj: `src/db.c:637` (lexical_call_candidate).
- load_old_obj: `src/db.c:641` (lexical_call_candidate).
- load_old_obj: `src/db.c:642` (lexical_call_candidate).
- load_old_obj: `src/db.c:643` (lexical_call_candidate).
- load_old_obj: `src/db.c:669` (lexical_call_candidate).
- load_old_obj: `src/db.c:670` (lexical_call_candidate).
- load_resets: `src/db.c:767` (lexical_call_candidate).
- load_resets: `src/db.c:768` (lexical_call_candidate).
- load_resets: `src/db.c:769` (lexical_call_candidate).
- load_resets: `src/db.c:771` (lexical_call_candidate).
- load_resets: `src/db.c:773` (lexical_call_candidate).
- load_rooms: `src/db.c:884` (lexical_call_candidate).
- load_rooms: `src/db.c:905` (lexical_call_candidate).
- load_rooms: `src/db.c:910` (lexical_call_candidate).
- load_rooms: `src/db.c:927` (lexical_call_candidate).
- load_rooms: `src/db.c:930` (lexical_call_candidate).
- load_rooms: `src/db.c:948` (lexical_call_candidate).
- load_rooms: `src/db.c:959` (lexical_call_candidate).
- load_rooms: `src/db.c:960` (lexical_call_candidate).
- load_rooms: `src/db.c:961` (lexical_call_candidate).
- load_shops: `src/db.c:1030` (lexical_call_candidate).
- load_shops: `src/db.c:1034` (lexical_call_candidate).
- load_shops: `src/db.c:1035` (lexical_call_candidate).
- load_shops: `src/db.c:1036` (lexical_call_candidate).
- load_shops: `src/db.c:1037` (lexical_call_candidate).
- load_shops: `src/db.c:1038` (lexical_call_candidate).
- load_specials: `src/db.c:1080` (lexical_call_candidate).
- fread_number: `src/db.c:2207` (lexical_call_candidate).
- load_mobiles: `src/db2.c:156` (lexical_call_candidate).
- load_mobiles: `src/db2.c:186` (lexical_call_candidate).
- load_mobiles: `src/db2.c:187` (lexical_call_candidate).
- load_mobiles: `src/db2.c:189` (lexical_call_candidate).
- load_mobiles: `src/db2.c:190` (lexical_call_candidate).
- load_mobiles: `src/db2.c:193` (lexical_call_candidate).
- load_mobiles: `src/db2.c:195` (lexical_call_candidate).
- load_mobiles: `src/db2.c:197` (lexical_call_candidate).
- load_mobiles: `src/db2.c:200` (lexical_call_candidate).
- load_mobiles: `src/db2.c:202` (lexical_call_candidate).
- load_mobiles: `src/db2.c:204` (lexical_call_candidate).
- load_mobiles: `src/db2.c:207` (lexical_call_candidate).
- load_mobiles: `src/db2.c:209` (lexical_call_candidate).
- load_mobiles: `src/db2.c:211` (lexical_call_candidate).
- load_mobiles: `src/db2.c:215` (lexical_call_candidate).
- load_mobiles: `src/db2.c:216` (lexical_call_candidate).
- load_mobiles: `src/db2.c:217` (lexical_call_candidate).
- load_mobiles: `src/db2.c:218` (lexical_call_candidate).
- load_mobiles: `src/db2.c:235` (lexical_call_candidate).
- load_objects: `src/db2.c:316` (lexical_call_candidate).
- load_objects: `src/db2.c:345` (lexical_call_candidate).
- load_objects: `src/db2.c:346` (lexical_call_candidate).
- load_objects: `src/db2.c:351` (lexical_call_candidate).
- load_objects: `src/db2.c:353` (lexical_call_candidate).
- load_objects: `src/db2.c:354` (lexical_call_candidate).
- load_objects: `src/db2.c:355` (lexical_call_candidate).
- load_objects: `src/db2.c:359` (lexical_call_candidate).
- load_objects: `src/db2.c:360` (lexical_call_candidate).
- load_objects: `src/db2.c:362` (lexical_call_candidate).
- load_objects: `src/db2.c:363` (lexical_call_candidate).
- load_objects: `src/db2.c:367` (lexical_call_candidate).
- load_objects: `src/db2.c:368` (lexical_call_candidate).
- load_objects: `src/db2.c:369` (lexical_call_candidate).
- load_objects: `src/db2.c:371` (lexical_call_candidate).
- load_objects: `src/db2.c:376` (lexical_call_candidate).
- load_objects: `src/db2.c:390` (lexical_call_candidate).
- load_objects: `src/db2.c:391` (lexical_call_candidate).
- load_objects: `src/db2.c:392` (lexical_call_candidate).
- load_objects: `src/db2.c:423` (lexical_call_candidate).
- load_objects: `src/db2.c:424` (lexical_call_candidate).
- load_objects: `src/db2.c:458` (lexical_call_candidate).
- load_objects: `src/db2.c:459` (lexical_call_candidate).
- load_thread: `src/note.c:247` (lexical_call_candidate).
- fread_char: `src/save.c:756` (lexical_call_candidate).
- fread_char: `src/save.c:757` (lexical_call_candidate).
- fread_char: `src/save.c:803` (lexical_call_candidate).
- fread_char: `src/save.c:821` (lexical_call_candidate).
- fread_char: `src/save.c:822` (lexical_call_candidate).
- fread_char: `src/save.c:823` (lexical_call_candidate).
- fread_char: `src/save.c:824` (lexical_call_candidate).
- fread_char: `src/save.c:825` (lexical_call_candidate).
- fread_char: `src/save.c:845` (lexical_call_candidate).
- fread_char: `src/save.c:846` (lexical_call_candidate).
- fread_char: `src/save.c:847` (lexical_call_candidate).
- fread_char: `src/save.c:848` (lexical_call_candidate).
- fread_char: `src/save.c:849` (lexical_call_candidate).
- fread_char: `src/save.c:850` (lexical_call_candidate).
- fread_char: `src/save.c:861` (lexical_call_candidate).
- fread_char: `src/save.c:871` (lexical_call_candidate).
- fread_char: `src/save.c:885` (lexical_call_candidate).
- fread_char: `src/save.c:886` (lexical_call_candidate).
- fread_char: `src/save.c:891` (lexical_call_candidate).
- fread_char: `src/save.c:892` (lexical_call_candidate).
- fread_char: `src/save.c:893` (lexical_call_candidate).
- fread_char: `src/save.c:899` (lexical_call_candidate).
- fread_char: `src/save.c:900` (lexical_call_candidate).
- fread_char: `src/save.c:901` (lexical_call_candidate).
- fread_char: `src/save.c:902` (lexical_call_candidate).
- fread_char: `src/save.c:911` (lexical_call_candidate).
- fread_char: `src/save.c:912` (lexical_call_candidate).
- fread_char: `src/save.c:934` (lexical_call_candidate).
- fread_char: `src/save.c:938` (lexical_call_candidate).
- fread_char: `src/save.c:959` (lexical_call_candidate).
- fread_char: `src/save.c:960` (lexical_call_candidate).
- fread_char: `src/save.c:964` (lexical_call_candidate).
- fread_char: `src/save.c:965` (lexical_call_candidate).
- fread_char: `src/save.c:966` (lexical_call_candidate).
- fread_char: `src/save.c:967` (lexical_call_candidate).
- fread_char: `src/save.c:968` (lexical_call_candidate).
- fread_char: `src/save.c:969` (lexical_call_candidate).
- fread_char: `src/save.c:976` (lexical_call_candidate).
- fread_char: `src/save.c:977` (lexical_call_candidate).
- fread_char: `src/save.c:978` (lexical_call_candidate).
- fread_char: `src/save.c:986` (lexical_call_candidate).
- fread_char: `src/save.c:987` (lexical_call_candidate).
- fread_char: `src/save.c:988` (lexical_call_candidate).
- fread_char: `src/save.c:989` (lexical_call_candidate).
- fread_char: `src/save.c:993` (lexical_call_candidate).
- fread_char: `src/save.c:994` (lexical_call_candidate).
- fread_char: `src/save.c:995` (lexical_call_candidate).
- fread_char: `src/save.c:996` (lexical_call_candidate).
- fread_char: `src/save.c:997` (lexical_call_candidate).
- fread_char: `src/save.c:998` (lexical_call_candidate).
- fread_char: `src/save.c:1005` (lexical_call_candidate).
- fread_char: `src/save.c:1008` (lexical_call_candidate).
- fread_char: `src/save.c:1009` (lexical_call_candidate).
- fread_char: `src/save.c:1010` (lexical_call_candidate).
- fread_char: `src/save.c:1011` (lexical_call_candidate).
- fread_char: `src/save.c:1012` (lexical_call_candidate).
- fread_char: `src/save.c:1021` (lexical_call_candidate).
- fread_char: `src/save.c:1022` (lexical_call_candidate).
- fread_char: `src/save.c:1023` (lexical_call_candidate).
- fread_char: `src/save.c:1024` (lexical_call_candidate).
- fread_char: `src/save.c:1025` (lexical_call_candidate).
- fread_char: `src/save.c:1026` (lexical_call_candidate).
- fread_char: `src/save.c:1027` (lexical_call_candidate).
- fread_char: `src/save.c:1028` (lexical_call_candidate).
- fread_char: `src/save.c:1039` (lexical_call_candidate).
- fread_char: `src/save.c:1049` (lexical_call_candidate).
- fread_char: `src/save.c:1050` (lexical_call_candidate).
- fread_char: `src/save.c:1051` (lexical_call_candidate).
- fread_char: `src/save.c:1052` (lexical_call_candidate).
- fread_char: `src/save.c:1055` (lexical_call_candidate).
- fread_char: `src/save.c:1064` (lexical_call_candidate).
- fread_char: `src/save.c:1081` (lexical_call_candidate).
- fread_char: `src/save.c:1082` (lexical_call_candidate).
- fread_char: `src/save.c:1083` (lexical_call_candidate).
- fread_char: `src/save.c:1084` (lexical_call_candidate).
- fread_char: `src/save.c:1085` (lexical_call_candidate).
- fread_char: `src/save.c:1104` (lexical_call_candidate).
- fread_char: `src/save.c:1105` (lexical_call_candidate).
- fread_char: `src/save.c:1108` (lexical_call_candidate).
- fread_char: `src/save.c:1115` (lexical_call_candidate).
- fread_char: `src/save.c:1116` (lexical_call_candidate).
- fread_pet: `src/save.c:1144` (lexical_call_candidate).
- fread_pet: `src/save.c:1174` (lexical_call_candidate).
- fread_pet: `src/save.c:1181` (lexical_call_candidate).
- fread_pet: `src/save.c:1199` (lexical_call_candidate).
- fread_pet: `src/save.c:1200` (lexical_call_candidate).
- fread_pet: `src/save.c:1201` (lexical_call_candidate).
- fread_pet: `src/save.c:1202` (lexical_call_candidate).
- fread_pet: `src/save.c:1203` (lexical_call_candidate).
- fread_pet: `src/save.c:1223` (lexical_call_candidate).
- fread_pet: `src/save.c:1224` (lexical_call_candidate).
- fread_pet: `src/save.c:1225` (lexical_call_candidate).
- fread_pet: `src/save.c:1226` (lexical_call_candidate).
- fread_pet: `src/save.c:1227` (lexical_call_candidate).
- fread_pet: `src/save.c:1228` (lexical_call_candidate).
- fread_pet: `src/save.c:1240` (lexical_call_candidate).
- fread_pet: `src/save.c:1250` (lexical_call_candidate).
- fread_pet: `src/save.c:1262` (lexical_call_candidate).
- fread_pet: `src/save.c:1285` (lexical_call_candidate).
- fread_pet: `src/save.c:1289` (lexical_call_candidate).
- fread_pet: `src/save.c:1293` (lexical_call_candidate).
- fread_pet: `src/save.c:1297` (lexical_call_candidate).
- fread_pet: `src/save.c:1298` (lexical_call_candidate).
- fread_pet: `src/save.c:1299` (lexical_call_candidate).
- fread_pet: `src/save.c:1300` (lexical_call_candidate).
- fread_pet: `src/save.c:1301` (lexical_call_candidate).
- fread_pet: `src/save.c:1302` (lexical_call_candidate).
- fread_pet: `src/save.c:1309` (lexical_call_candidate).
- fread_pet: `src/save.c:1311` (lexical_call_candidate).
- fread_pet: `src/save.c:1319` (lexical_call_candidate).
- fread_pet: `src/save.c:1327` (lexical_call_candidate).
- fread_pet: `src/save.c:1328` (lexical_call_candidate).
- fread_pet: `src/save.c:1330` (lexical_call_candidate).
- fread_obj: `src/save.c:1369` (lexical_call_candidate).
- fread_obj: `src/save.c:1423` (lexical_call_candidate).
- fread_obj: `src/save.c:1424` (lexical_call_candidate).
- fread_obj: `src/save.c:1425` (lexical_call_candidate).
- fread_obj: `src/save.c:1426` (lexical_call_candidate).
- fread_obj: `src/save.c:1427` (lexical_call_candidate).
- fread_obj: `src/save.c:1446` (lexical_call_candidate).
- fread_obj: `src/save.c:1447` (lexical_call_candidate).
- fread_obj: `src/save.c:1448` (lexical_call_candidate).
- fread_obj: `src/save.c:1449` (lexical_call_candidate).
- fread_obj: `src/save.c:1450` (lexical_call_candidate).
- fread_obj: `src/save.c:1451` (lexical_call_candidate).
- fread_obj: `src/save.c:1460` (lexical_call_candidate).
- fread_obj: `src/save.c:1461` (lexical_call_candidate).
- fread_obj: `src/save.c:1478` (lexical_call_candidate).
- fread_obj: `src/save.c:1479` (lexical_call_candidate).
- fread_obj: `src/save.c:1538` (lexical_call_candidate).
- fread_obj: `src/save.c:1539` (lexical_call_candidate).
- fread_obj: `src/save.c:1543` (lexical_call_candidate).
- fread_obj: `src/save.c:1544` (lexical_call_candidate).
- fread_obj: `src/save.c:1552` (lexical_call_candidate).
- fread_obj: `src/save.c:1585` (lexical_call_candidate).
- fread_obj: `src/save.c:1606` (lexical_call_candidate).
- fread_obj: `src/save.c:1607` (lexical_call_candidate).
- fread_obj: `src/save.c:1613` (lexical_call_candidate).
- fread_obj: `src/save.c:1614` (lexical_call_candidate).
- fread_obj: `src/save.c:1615` (lexical_call_candidate).
- fread_obj: `src/save.c:1616` (lexical_call_candidate).
- fread_obj: `src/save.c:1625` (lexical_call_candidate).
- fread_obj: `src/save.c:1626` (lexical_call_candidate).
- fread_obj: `src/save.c:1627` (lexical_call_candidate).
- fread_obj: `src/save.c:1628` (lexical_call_candidate).
- fread_obj: `src/save.c:1629` (lexical_call_candidate).
- fread_obj: `src/save.c:1638` (lexical_call_candidate).
- fread_obj: `src/save.c:1649` (lexical_call_candidate).
- fread_obj: `src/save.c:1650` (lexical_call_candidate).
- fread_obj: `src/save.c:1651` (lexical_call_candidate).
- fread_obj: `src/save.c:1652` (lexical_call_candidate).
- fread_obj: `src/save.c:1653` (lexical_call_candidate).
- fread_obj: `src/save.c:1654` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2129` (declaration_or_dispatch_reference).

Dependencies: `getc`, `isspace`, `isdigit`, `bug`, `exit`, `fread_number`, `ungetc`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.fread_number.while.001` | 2176 | `while ( isspace(c) )` |  | pending |
| `db.fread_number.if.001` | 2181 | `if ( c == '+' )` |  | pending |
| `db.fread_number.if.002` | 2185 | `if ( c == '-' )` |  | pending |
| `db.fread_number.if.003` | 2191 | `if ( !isdigit(c) )` |  | pending |
| `db.fread_number.while.002` | 2197 | `while ( isdigit(c) )` |  | pending |
| `db.fread_number.if.004` | 2203 | `if ( sign )` |  | pending |
| `db.fread_number.if.005` | 2206 | `if ( c == '\|' )` |  | pending |
| `db.fread_number.if.006` | 2208 | `if ( c != ' ' )` |  | pending |
| `db.fread_number.return.001` | 2211 | `return number;` |  | pending |

## fread_flag

[Source line 2214](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2214); ends at line 2259. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_bans: `src/ban.c:94` (lexical_call_candidate).
- load_old_mob: `src/db.c:505` (lexical_call_candidate).
- load_old_mob: `src/db.c:506` (lexical_call_candidate).
- load_old_obj: `src/db.c:632` (lexical_call_candidate).
- load_old_obj: `src/db.c:633` (lexical_call_candidate).
- load_rooms: `src/db.c:906` (lexical_call_candidate).
- fread_flag: `src/db.c:2250` (lexical_call_candidate).
- load_mobiles: `src/db2.c:181` (lexical_call_candidate).
- load_mobiles: `src/db2.c:183` (lexical_call_candidate).
- load_mobiles: `src/db2.c:221` (lexical_call_candidate).
- load_mobiles: `src/db2.c:223` (lexical_call_candidate).
- load_mobiles: `src/db2.c:225` (lexical_call_candidate).
- load_mobiles: `src/db2.c:227` (lexical_call_candidate).
- load_mobiles: `src/db2.c:237` (lexical_call_candidate).
- load_mobiles: `src/db2.c:239` (lexical_call_candidate).
- load_mobiles: `src/db2.c:255` (lexical_call_candidate).
- load_objects: `src/db2.c:339` (lexical_call_candidate).
- load_objects: `src/db2.c:340` (lexical_call_candidate).
- load_objects: `src/db2.c:348` (lexical_call_candidate).
- load_objects: `src/db2.c:352` (lexical_call_candidate).
- load_objects: `src/db2.c:383` (lexical_call_candidate).
- load_objects: `src/db2.c:384` (lexical_call_candidate).
- load_objects: `src/db2.c:385` (lexical_call_candidate).
- load_objects: `src/db2.c:386` (lexical_call_candidate).
- load_objects: `src/db2.c:387` (lexical_call_candidate).
- load_objects: `src/db2.c:460` (lexical_call_candidate).
- fread_char: `src/save.c:753` (lexical_call_candidate).
- fread_char: `src/save.c:754` (lexical_call_candidate).
- fread_char: `src/save.c:755` (lexical_call_candidate).
- fread_char: `src/save.c:906` (lexical_call_candidate).
- fread_char: `src/save.c:1117` (lexical_call_candidate).
- fread_pet: `src/save.c:1172` (lexical_call_candidate).
- fread_pet: `src/save.c:1173` (lexical_call_candidate).
- fread_pet: `src/save.c:1258` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2130` (declaration_or_dispatch_reference).

Dependencies: `getc`, `isspace`, `isdigit`, `flag_convert`, `fread_flag`, `ungetc`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.fread_flag.while.001` | 2224 | `while ( isspace(c))` |  | pending |
| `db.fread_flag.if.001` | 2226 | `if (c == '-')` |  | pending |
| `db.fread_flag.if.002` | 2234 | `if (!isdigit(c))` |  | pending |
| `db.fread_flag.while.002` | 2236 | `while (('A' <= c && c <= 'Z') \|\| ('a' <= c && c <= 'z'))` |  | pending |
| `db.fread_flag.and.001` | 2236 | `&& c <= 'Z') \|\| ('a' <= c && c <= 'z'))` |  | pending |
| `db.fread_flag.or.001` | 2236 | `\|\| ('a' <= c && c <= 'z'))` |  | pending |
| `db.fread_flag.and.002` | 2236 | `&& c <= 'z'))` |  | pending |
| `db.fread_flag.while.003` | 2243 | `while (isdigit(c))` |  | pending |
| `db.fread_flag.if.003` | 2249 | `if (c == '\|')` |  | pending |
| `db.fread_flag.if.004` | 2252 | `if  ( c != ' ')` |  | pending |
| `db.fread_flag.if.005` | 2255 | `if (negative)` |  | pending |
| `db.fread_flag.return.001` | 2256 | `return -1 * number;` |  | pending |
| `db.fread_flag.return.002` | 2258 | `return number;` |  | pending |

## flag_convert

[Source line 2261](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2261); ends at line 2280. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- fread_flag: `src/db.c:2238` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2135` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.flag_convert.if.001` | 2266 | `if ('A' <= letter && letter <= 'Z')` |  | pending |
| `db.flag_convert.and.001` | 2266 | `&& letter <= 'Z')` |  | pending |
| `db.flag_convert.for.001` | 2269 | `for (i = letter; i > 'A'; i--)` |  | pending |
| `db.flag_convert.if.002` | 2272 | `if ('a' <= letter && letter <= 'z')` |  | pending |
| `db.flag_convert.and.002` | 2272 | `&& letter <= 'z')` |  | pending |
| `db.flag_convert.for.002` | 2275 | `for (i = letter; i > 'a'; i --)` |  | pending |
| `db.flag_convert.return.001` | 2279 | `return bitsum;` |  | pending |

## fread_string

[Source line 2293](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2293); ends at line 2395. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_area: `src/db.c:403` (lexical_call_candidate).
- load_area: `src/db.c:404` (lexical_call_candidate).
- load_area: `src/db.c:405` (lexical_call_candidate).
- load_helps: `src/db.c:436` (lexical_call_candidate).
- load_helps: `src/db.c:439` (lexical_call_candidate).
- load_old_mob: `src/db.c:497` (lexical_call_candidate).
- load_old_mob: `src/db.c:498` (lexical_call_candidate).
- load_old_mob: `src/db.c:499` (lexical_call_candidate).
- load_old_mob: `src/db.c:500` (lexical_call_candidate).
- load_old_obj: `src/db.c:622` (lexical_call_candidate).
- load_old_obj: `src/db.c:623` (lexical_call_candidate).
- load_old_obj: `src/db.c:624` (lexical_call_candidate).
- load_old_obj: `src/db.c:625` (lexical_call_candidate).
- load_old_obj: `src/db.c:682` (lexical_call_candidate).
- load_old_obj: `src/db.c:683` (lexical_call_candidate).
- load_rooms: `src/db.c:903` (lexical_call_candidate).
- load_rooms: `src/db.c:904` (lexical_call_candidate).
- load_rooms: `src/db.c:939` (lexical_call_candidate).
- load_rooms: `src/db.c:956` (lexical_call_candidate).
- load_rooms: `src/db.c:957` (lexical_call_candidate).
- load_rooms: `src/db.c:981` (lexical_call_candidate).
- load_rooms: `src/db.c:982` (lexical_call_candidate).
- load_rooms: `src/db.c:996` (lexical_call_candidate).
- load_mobiles: `src/db2.c:172` (lexical_call_candidate).
- load_mobiles: `src/db2.c:173` (lexical_call_candidate).
- load_mobiles: `src/db2.c:174` (lexical_call_candidate).
- load_mobiles: `src/db2.c:175` (lexical_call_candidate).
- load_mobiles: `src/db2.c:176` (lexical_call_candidate).
- load_objects: `src/db2.c:333` (lexical_call_candidate).
- load_objects: `src/db2.c:334` (lexical_call_candidate).
- load_objects: `src/db2.c:335` (lexical_call_candidate).
- load_objects: `src/db2.c:336` (lexical_call_candidate).
- load_objects: `src/db2.c:471` (lexical_call_candidate).
- load_objects: `src/db2.c:472` (lexical_call_candidate).
- load_songs: `src/music.c:188` (lexical_call_candidate).
- load_songs: `src/music.c:189` (lexical_call_candidate).
- load_thread: `src/note.c:239` (lexical_call_candidate).
- load_thread: `src/note.c:243` (lexical_call_candidate).
- load_thread: `src/note.c:251` (lexical_call_candidate).
- load_thread: `src/note.c:255` (lexical_call_candidate).
- load_thread: `src/note.c:259` (lexical_call_candidate).
- fread_char: `src/save.c:785` (lexical_call_candidate).
- fread_char: `src/save.c:878` (lexical_call_candidate).
- fread_char: `src/save.c:879` (lexical_call_candidate).
- fread_char: `src/save.c:880` (lexical_call_candidate).
- fread_char: `src/save.c:881` (lexical_call_candidate).
- fread_char: `src/save.c:887` (lexical_call_candidate).
- fread_char: `src/save.c:913` (lexical_call_candidate).
- fread_char: `src/save.c:914` (lexical_call_candidate).
- fread_char: `src/save.c:999` (lexical_call_candidate).
- fread_char: `src/save.c:1000` (lexical_call_candidate).
- fread_char: `src/save.c:1004` (lexical_call_candidate).
- fread_char: `src/save.c:1019` (lexical_call_candidate).
- fread_char: `src/save.c:1020` (lexical_call_candidate).
- fread_char: `src/save.c:1029` (lexical_call_candidate).
- fread_char: `src/save.c:1030` (lexical_call_candidate).
- fread_char: `src/save.c:1035` (lexical_call_candidate).
- fread_char: `src/save.c:1053` (lexical_call_candidate).
- fread_char: `src/save.c:1054` (lexical_call_candidate).
- fread_char: `src/save.c:1089` (lexical_call_candidate).
- fread_pet: `src/save.c:1257` (lexical_call_candidate).
- fread_pet: `src/save.c:1263` (lexical_call_candidate).
- fread_pet: `src/save.c:1310` (lexical_call_candidate).
- fread_pet: `src/save.c:1315` (lexical_call_candidate).
- fread_pet: `src/save.c:1323` (lexical_call_candidate).
- fread_pet: `src/save.c:1329` (lexical_call_candidate).
- fread_obj: `src/save.c:1465` (lexical_call_candidate).
- fread_obj: `src/save.c:1466` (lexical_call_candidate).
- fread_obj: `src/save.c:1487` (lexical_call_candidate).
- fread_obj: `src/save.c:1488` (lexical_call_candidate).
- fread_obj: `src/save.c:1548` (lexical_call_candidate).
- fread_obj: `src/save.c:1577` (lexical_call_candidate).
- fread_obj: `src/save.c:1578` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2131` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`, `getc`, `isspace`, `UMIN`, `strcmp`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.fread_string.if.001` | 2299 | `if ( plast > &string_space[MAX_STRING - MAX_STRING_LENGTH] )` |  | pending |
| `db.fread_string.while.001` | 2313 | `while ( isspace(c) )` |  | pending |
| `db.fread_string.if.002` | 2315 | `if ( ( *plast++ = c ) == '~' )` |  | pending |
| `db.fread_string.return.001` | 2316 | `return &str_empty[0];` |  | pending |
| `db.fread_string.for.001` | 2318 | `for ( ;; )` |  | pending |
| `db.fread_string.switch.001` | 2326 | `switch ( *plast = getc(fp) )` |  | pending |
| `db.fread_string.default.001` | 2328 | `default:` |  | pending |
| `db.fread_string.break.001` | 2330 | `break;` |  | pending |
| `db.fread_string.case.001` | 2332 | `case EOF:` |  | pending |
| `db.fread_string.return.002` | 2335 | `return NULL;` |  | pending |
| `db.fread_string.break.002` | 2337 | `break;` |  | pending |
| `db.fread_string.case.002` | 2339 | `case '\n':` |  | pending |
| `db.fread_string.break.003` | 2342 | `break;` |  | pending |
| `db.fread_string.case.003` | 2344 | `case '\r':` |  | pending |
| `db.fread_string.break.004` | 2345 | `break;` |  | pending |
| `db.fread_string.case.004` | 2347 | `case '~':` |  | pending |
| `db.fread_string.for.002` | 2363 | `for ( pHash = string_hash[iHash]; pHash; pHash = pHashPrev )` |  | pending |
| `db.fread_string.for.003` | 2365 | `for ( ic = 0; ic < sizeof(char *); ic++ )` |  | pending |
| `db.fread_string.if.003` | 2370 | `if ( top_string[sizeof(char *)] == pHash[0] 		    &&   !strcmp( top_string+sizeof(char *)+1, pHash+1 ) )` |  | pending |
| `db.fread_string.and.001` | 2371 | `&&   !strcmp( top_string+sizeof(char *)+1, pHash+1 ) )` |  | pending |
| `db.fread_string.return.003` | 2372 | `return pHash;` |  | pending |
| `db.fread_string.if.004` | 2375 | `if ( fBootDb )` |  | pending |
| `db.fread_string.for.004` | 2380 | `for ( ic = 0; ic < sizeof(char *); ic++ )` |  | pending |
| `db.fread_string.return.004` | 2386 | `return pString + sizeof(char *);` |  | pending |
| `db.fread_string.return.005` | 2390 | `return str_dup( top_string + sizeof(char *) );` |  | pending |

## fread_string_eol

[Source line 2397](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2397); ends at line 2492. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_socials: `src/db2.c:72` (lexical_call_candidate).
- load_socials: `src/db2.c:84` (lexical_call_candidate).
- load_socials: `src/db2.c:101` (lexical_call_candidate).
- load_socials: `src/db2.c:113` (lexical_call_candidate).
- load_songs: `src/music.c:212` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2132` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`, `getc`, `isspace`, `UMIN`, `strcmp`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.fread_string_eol.if.001` | 2403 | `if ( char_special[EOF-EOF] != TRUE )` |  | pending |
| `db.fread_string_eol.if.002` | 2411 | `if ( plast > &string_space[MAX_STRING - MAX_STRING_LENGTH] )` |  | pending |
| `db.fread_string_eol.while.001` | 2425 | `while ( isspace(c) )` |  | pending |
| `db.fread_string_eol.if.003` | 2427 | `if ( ( *plast++ = c ) == '\n')` |  | pending |
| `db.fread_string_eol.return.001` | 2428 | `return &str_empty[0];` |  | pending |
| `db.fread_string_eol.for.001` | 2430 | `for ( ;; )` |  | pending |
| `db.fread_string_eol.if.004` | 2432 | `if ( !char_special[ ( *plast++ = getc( fp ) ) - EOF ] )` |  | pending |
| `db.fread_string_eol.continue.001` | 2433 | `continue;` |  | pending |
| `db.fread_string_eol.switch.001` | 2435 | `switch ( plast[-1] )` |  | pending |
| `db.fread_string_eol.default.001` | 2437 | `default:` |  | pending |
| `db.fread_string_eol.break.001` | 2438 | `break;` |  | pending |
| `db.fread_string_eol.case.001` | 2440 | `case EOF:` |  | pending |
| `db.fread_string_eol.break.002` | 2443 | `break;` |  | pending |
| `db.fread_string_eol.case.002` | 2445 | `case '\n':  case '\r':` |  | pending |
| `db.fread_string_eol.case.003` | 2445 | `case '\r':` |  | pending |
| `db.fread_string_eol.for.002` | 2460 | `for ( pHash = string_hash[iHash]; pHash; pHash = pHashPrev )` |  | pending |
| `db.fread_string_eol.for.003` | 2462 | `for ( ic = 0; ic < sizeof(char *); ic++ )` |  | pending |
| `db.fread_string_eol.if.005` | 2467 | `if ( top_string[sizeof(char *)] == pHash[0]                     &&   !strcmp( top_string+sizeof(char *)+1, pHash+1 ) )` |  | pending |
| `db.fread_string_eol.and.001` | 2468 | `&&   !strcmp( top_string+sizeof(char *)+1, pHash+1 ) )` |  | pending |
| `db.fread_string_eol.return.002` | 2469 | `return pHash;` |  | pending |
| `db.fread_string_eol.if.006` | 2472 | `if ( fBootDb )` |  | pending |
| `db.fread_string_eol.for.004` | 2477 | `for ( ic = 0; ic < sizeof(char *); ic++ )` |  | pending |
| `db.fread_string_eol.return.003` | 2483 | `return pString + sizeof(char *);` |  | pending |
| `db.fread_string_eol.return.004` | 2487 | `return str_dup( top_string + sizeof(char *) );` |  | pending |

## fread_to_eol

[Source line 2499](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2499); ends at line 2517. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_bans: `src/ban.c:95` (lexical_call_candidate).
- load_resets: `src/db.c:761` (lexical_call_candidate).
- load_resets: `src/db.c:774` (lexical_call_candidate).
- load_shops: `src/db.c:1039` (lexical_call_candidate).
- load_specials: `src/db.c:1090` (lexical_call_candidate).
- load_socials: `src/db2.c:70` (lexical_call_candidate).
- load_char_obj: `src/save.c:603` (lexical_call_candidate).
- fread_char: `src/save.c:749` (lexical_call_candidate).
- fread_char: `src/save.c:763` (lexical_call_candidate).
- fread_char: `src/save.c:779` (lexical_call_candidate).
- fread_char: `src/save.c:793` (lexical_call_candidate).
- fread_char: `src/save.c:1124` (lexical_call_candidate).
- fread_pet: `src/save.c:1168` (lexical_call_candidate).
- fread_pet: `src/save.c:1336` (lexical_call_candidate).
- fread_obj: `src/save.c:1406` (lexical_call_candidate).
- fread_obj: `src/save.c:1662` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2133` (declaration_or_dispatch_reference).

Dependencies: `getc`, `ungetc`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.fread_to_eol.while.001` | 2507 | `while ( c != '\n' && c != '\r' )` |  | pending |
| `db.fread_to_eol.and.001` | 2507 | `&& c != '\r' );` |  | pending |
| `db.fread_to_eol.while.002` | 2513 | `while ( c == '\n' \|\| c == '\r' )` |  | pending |
| `db.fread_to_eol.or.001` | 2513 | `\|\| c == '\r' );` |  | pending |
| `db.fread_to_eol.return.001` | 2516 | `return;` |  | pending |

## fread_word

[Source line 2524](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2524); ends at line 2562. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_bans: `src/ban.c:92` (lexical_call_candidate).
- boot_db: `src/db.c:318` (lexical_call_candidate).
- boot_db: `src/db.c:345` (lexical_call_candidate).
- load_specials: `src/db.c:1081` (lexical_call_candidate).
- load_socials: `src/db2.c:66` (lexical_call_candidate).
- load_mobiles: `src/db2.c:212` (lexical_call_candidate).
- load_mobiles: `src/db2.c:231` (lexical_call_candidate).
- load_mobiles: `src/db2.c:232` (lexical_call_candidate).
- load_mobiles: `src/db2.c:233` (lexical_call_candidate).
- load_mobiles: `src/db2.c:242` (lexical_call_candidate).
- load_mobiles: `src/db2.c:243` (lexical_call_candidate).
- load_mobiles: `src/db2.c:254` (lexical_call_candidate).
- load_objects: `src/db2.c:338` (lexical_call_candidate).
- load_objects: `src/db2.c:344` (lexical_call_candidate).
- load_objects: `src/db2.c:347` (lexical_call_candidate).
- load_objects: `src/db2.c:361` (lexical_call_candidate).
- load_objects: `src/db2.c:370` (lexical_call_candidate).
- load_objects: `src/db2.c:377` (lexical_call_candidate).
- load_objects: `src/db2.c:378` (lexical_call_candidate).
- load_objects: `src/db2.c:379` (lexical_call_candidate).
- load_objects: `src/db2.c:380` (lexical_call_candidate).
- load_thread: `src/note.c:237` (lexical_call_candidate).
- load_thread: `src/note.c:241` (lexical_call_candidate).
- load_thread: `src/note.c:245` (lexical_call_candidate).
- load_thread: `src/note.c:249` (lexical_call_candidate).
- load_thread: `src/note.c:253` (lexical_call_candidate).
- load_thread: `src/note.c:257` (lexical_call_candidate).
- load_char_obj: `src/save.c:613` (lexical_call_candidate).
- fread_char: `src/save.c:742` (lexical_call_candidate).
- fread_char: `src/save.c:768` (lexical_call_candidate).
- fread_char: `src/save.c:769` (lexical_call_candidate).
- fread_char: `src/save.c:784` (lexical_call_candidate).
- fread_char: `src/save.c:815` (lexical_call_candidate).
- fread_char: `src/save.c:839` (lexical_call_candidate).
- fread_char: `src/save.c:944` (lexical_call_candidate).
- fread_char: `src/save.c:1065` (lexical_call_candidate).
- fread_pet: `src/save.c:1139` (lexical_call_candidate).
- fread_pet: `src/save.c:1161` (lexical_call_candidate).
- fread_pet: `src/save.c:1193` (lexical_call_candidate).
- fread_pet: `src/save.c:1217` (lexical_call_candidate).
- fread_obj: `src/save.c:1363` (lexical_call_candidate).
- fread_obj: `src/save.c:1399` (lexical_call_candidate).
- fread_obj: `src/save.c:1417` (lexical_call_candidate).
- fread_obj: `src/save.c:1440` (lexical_call_candidate).
- fread_obj: `src/save.c:1586` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2134` (declaration_or_dispatch_reference).

Dependencies: `getc`, `isspace`, `ungetc`, `bug`, `exit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.fread_word.while.001` | 2534 | `while ( isspace( cEnd ) )` |  | pending |
| `db.fread_word.if.001` | 2536 | `if ( cEnd == '\'' \|\| cEnd == '"' )` |  | pending |
| `db.fread_word.or.001` | 2536 | `\|\| cEnd == '"' )` |  | pending |
| `db.fread_word.for.001` | 2547 | `for ( ; pword < word + MAX_INPUT_LENGTH; pword++ )` |  | pending |
| `db.fread_word.if.002` | 2550 | `if ( cEnd == ' ' ? isspace(*pword) : *pword == cEnd )` |  | pending |
| `db.fread_word.ternary.001` | 2550 | `? isspace(*pword) : *pword == cEnd )` |  | pending |
| `db.fread_word.if.003` | 2552 | `if ( cEnd == ' ' )` |  | pending |
| `db.fread_word.return.001` | 2555 | `return word;` |  | pending |
| `db.fread_word.return.002` | 2561 | `return NULL;` |  | pending |

## alloc_mem

[Source line 2568](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2568); ends at line 2603. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_list_to_char: `src/act_info.c:151` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:152` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:515` (lexical_call_candidate).
- init_descriptor: `src/comm.c:895` (lexical_call_candidate).
- write_to_buffer: `src/comm.c:1491` (lexical_call_candidate).
- page_to_char: `src/comm.c:2361` (lexical_call_candidate).
- str_dup: `src/db.c:2700` (lexical_call_candidate).
- new_mem_data: `src/recycle.c:473` (lexical_call_candidate).
- new_buf: `src/recycle.c:538` (lexical_call_candidate).
- new_buf_size: `src/recycle.c:565` (lexical_call_candidate).
- add_buf: `src/recycle.c:619` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2136` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`, `alloc_perm`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.alloc_mem.for.001` | 2576 | `for ( iList = 0; iList < MAX_MEM_LIST; iList++ )` |  | pending |
| `db.alloc_mem.if.001` | 2578 | `if ( sMem <= rgSizeList[iList] )` |  | pending |
| `db.alloc_mem.break.001` | 2579 | `break;` |  | pending |
| `db.alloc_mem.if.002` | 2582 | `if ( iList == MAX_MEM_LIST )` |  | pending |
| `db.alloc_mem.if.003` | 2588 | `if ( rgFreeList[iList] == NULL )` |  | pending |
| `db.alloc_mem.return.001` | 2602 | `return pMem;` |  | pending |

## free_mem

[Source line 2611](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2611); ends at line 2645. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_list_to_char: `src/act_info.c:235` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:236` (lexical_call_candidate).
- write_to_buffer: `src/comm.c:1493` (lexical_call_candidate).
- show_string: `src/comm.c:2383` (lexical_call_candidate).
- show_string: `src/comm.c:2411` (lexical_call_candidate).
- free_string: `src/db.c:2719` (lexical_call_candidate).
- free_descriptor: `src/recycle.c:137` (lexical_call_candidate).
- free_buf: `src/recycle.c:578` (lexical_call_candidate).
- add_buf: `src/recycle.c:622` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2138` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.free_mem.if.001` | 2619 | `if (*magic != MAGIC_NUM)` |  | pending |
| `db.free_mem.return.001` | 2623 | `return;` |  | pending |
| `db.free_mem.for.001` | 2629 | `for ( iList = 0; iList < MAX_MEM_LIST; iList++ )` |  | pending |
| `db.free_mem.if.002` | 2631 | `if ( sMem <= rgSizeList[iList] )` |  | pending |
| `db.free_mem.break.001` | 2632 | `break;` |  | pending |
| `db.free_mem.if.003` | 2635 | `if ( iList == MAX_MEM_LIST )` |  | pending |
| `db.free_mem.return.002` | 2644 | `return;` |  | pending |

## alloc_perm

[Source line 2653](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2653); ends at line 2682. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_area: `src/db.c:400` (lexical_call_candidate).
- load_helps: `src/db.c:434` (lexical_call_candidate).
- load_old_mob: `src/db.c:494` (lexical_call_candidate).
- load_old_obj: `src/db.c:618` (lexical_call_candidate).
- load_old_obj: `src/db.c:664` (lexical_call_candidate).
- load_old_obj: `src/db.c:681` (lexical_call_candidate).
- load_resets: `src/db.c:765` (lexical_call_candidate).
- load_rooms: `src/db.c:896` (lexical_call_candidate).
- load_rooms: `src/db.c:955` (lexical_call_candidate).
- load_rooms: `src/db.c:980` (lexical_call_candidate).
- load_shops: `src/db.c:1029` (lexical_call_candidate).
- alloc_mem: `src/db.c:2590` (lexical_call_candidate).
- load_mobiles: `src/db2.c:168` (lexical_call_candidate).
- load_objects: `src/db2.c:328` (lexical_call_candidate).
- load_objects: `src/db2.c:418` (lexical_call_candidate).
- load_objects: `src/db2.c:435` (lexical_call_candidate).
- load_objects: `src/db2.c:470` (lexical_call_candidate).
- load_thread: `src/note.c:235` (lexical_call_candidate).
- new_note: `src/recycle.c:49` (lexical_call_candidate).
- new_ban: `src/recycle.c:85` (lexical_call_candidate).
- new_descriptor: `src/recycle.c:119` (lexical_call_candidate).
- new_gen_data: `src/recycle.c:152` (lexical_call_candidate).
- new_extra_descr: `src/recycle.c:182` (lexical_call_candidate).
- new_affect: `src/recycle.c:218` (lexical_call_candidate).
- new_obj: `src/recycle.c:251` (lexical_call_candidate).
- new_char: `src/recycle.c:306` (lexical_call_candidate).
- new_pcdata: `src/recycle.c:393` (lexical_call_candidate).
- new_buf: `src/recycle.c:527` (lexical_call_candidate).
- new_buf_size: `src/recycle.c:550` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2137` (declaration_or_dispatch_reference).

Dependencies: `bug`, `exit`, `calloc`, `perror`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.alloc_perm.while.001` | 2659 | `while ( sMem % sizeof(long) != 0 )` |  | pending |
| `db.alloc_perm.if.001` | 2661 | `if ( sMem > MAX_PERM_BLOCK )` |  | pending |
| `db.alloc_perm.if.002` | 2667 | `if ( pMemPerm == NULL \|\| iMemPerm + sMem > MAX_PERM_BLOCK )` |  | pending |
| `db.alloc_perm.or.001` | 2667 | `\|\| iMemPerm + sMem > MAX_PERM_BLOCK )` |  | pending |
| `db.alloc_perm.if.003` | 2670 | `if ( ( pMemPerm = calloc( 1, MAX_PERM_BLOCK ) ) == NULL )` |  | pending |
| `db.alloc_perm.return.001` | 2681 | `return pMem;` |  | pending |

## str_dup

[Source line 2690](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2690); ends at line 2703. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_list_to_char: `src/act_info.c:188` (lexical_call_candidate).
- do_prompt: `src/act_info.c:895` (lexical_call_candidate).
- set_title: `src/act_info.c:2385` (lexical_call_candidate).
- do_description: `src/act_info.c:2448` (lexical_call_candidate).
- do_description: `src/act_info.c:2458` (lexical_call_candidate).
- do_description: `src/act_info.c:2480` (lexical_call_candidate).
- do_password: `src/act_info.c:2751` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2596` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2602` (lexical_call_candidate).
- do_bamfin: `src/act_wiz.c:458` (lexical_call_candidate).
- do_bamfout: `src/act_wiz.c:488` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2240` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3746` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3753` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3760` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3768` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3815` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3822` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3829` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3849` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3850` (lexical_call_candidate).
- do_prefix: `src/act_wiz.c:4363` (lexical_call_candidate).
- do_prefix: `src/act_wiz.c:4377` (lexical_call_candidate).
- do_alias: `src/alias.c:187` (lexical_call_candidate).
- do_alias: `src/alias.c:201` (lexical_call_candidate).
- do_alias: `src/alias.c:202` (lexical_call_candidate).
- load_bans: `src/ban.c:92` (lexical_call_candidate).
- ban_site: `src/ban.c:235` (lexical_call_candidate).
- game_loop_mac_msdos: `src/comm.c:513` (lexical_call_candidate).
- init_descriptor: `src/comm.c:901` (lexical_call_candidate).
- init_descriptor: `src/comm.c:920` (lexical_call_candidate).
- nanny: `src/comm.c:1777` (lexical_call_candidate).
- check_reconnect: `src/comm.c:2260` (lexical_call_candidate).
- load_old_obj: `src/db.c:629` (lexical_call_candidate).
- load_rooms: `src/db.c:897` (lexical_call_candidate).
- create_mobile: `src/db.c:1601` (lexical_call_candidate).
- clone_mobile: `src/db.c:1753` (lexical_call_candidate).
- clone_mobile: `src/db.c:1755` (lexical_call_candidate).
- clone_mobile: `src/db.c:1756` (lexical_call_candidate).
- clone_mobile: `src/db.c:1757` (lexical_call_candidate).
- clone_mobile: `src/db.c:1793` (lexical_call_candidate).
- create_object: `src/db.c:1851` (lexical_call_candidate).
- clone_object: `src/db.c:1979` (lexical_call_candidate).
- clone_object: `src/db.c:1980` (lexical_call_candidate).
- clone_object: `src/db.c:1981` (lexical_call_candidate).
- clone_object: `src/db.c:1989` (lexical_call_candidate).
- clone_object: `src/db.c:2005` (lexical_call_candidate).
- clone_object: `src/db.c:2006` (lexical_call_candidate).
- fread_string: `src/db.c:2390` (lexical_call_candidate).
- fread_string_eol: `src/db.c:2487` (lexical_call_candidate).
- load_mobiles: `src/db2.c:243` (lexical_call_candidate).
- make_corpse: `src/fight.c:1455` (lexical_call_candidate).
- make_corpse: `src/fight.c:1474` (lexical_call_candidate).
- make_corpse: `src/fight.c:1478` (lexical_call_candidate).
- death_cry: `src/fight.c:1618` (lexical_call_candidate).
- death_cry: `src/fight.c:1622` (lexical_call_candidate).
- create_money: `src/handler.c:2273` (lexical_call_candidate).
- create_money: `src/handler.c:2283` (lexical_call_candidate).
- create_money: `src/handler.c:2294` (lexical_call_candidate).
- do_function: `src/interp.c:519` (lexical_call_candidate).
- spell_create_water: `src/magic.c:1549` (lexical_call_candidate).
- note_attach: `src/note.c:375` (lexical_call_candidate).
- note_attach: `src/note.c:376` (lexical_call_candidate).
- note_attach: `src/note.c:377` (lexical_call_candidate).
- note_attach: `src/note.c:378` (lexical_call_candidate).
- note_attach: `src/note.c:379` (lexical_call_candidate).
- note_remove: `src/note.c:413` (lexical_call_candidate).
- parse_note: `src/note.c:797` (lexical_call_candidate).
- parse_note: `src/note.c:838` (lexical_call_candidate).
- parse_note: `src/note.c:845` (lexical_call_candidate).
- parse_note: `src/note.c:860` (lexical_call_candidate).
- parse_note: `src/note.c:875` (lexical_call_candidate).
- parse_note: `src/note.c:949` (lexical_call_candidate).
- load_char_obj: `src/save.c:554` (lexical_call_candidate).
- load_char_obj: `src/save.c:560` (lexical_call_candidate).
- load_char_obj: `src/save.c:562` (lexical_call_candidate).
- load_char_obj: `src/save.c:563` (lexical_call_candidate).
- load_char_obj: `src/save.c:564` (lexical_call_candidate).
- load_char_obj: `src/save.c:565` (lexical_call_candidate).
- fread_char: `src/save.c:768` (lexical_call_candidate).
- fread_char: `src/save.c:769` (lexical_call_candidate).
- fread_char: `src/save.c:784` (lexical_call_candidate).
- fread_char: `src/save.c:1095` (lexical_call_candidate).
- fread_obj: `src/save.c:1385` (lexical_call_candidate).
- fread_obj: `src/save.c:1386` (lexical_call_candidate).
- fread_obj: `src/save.c:1387` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2139` (declaration_or_dispatch_reference).

Dependencies: `return`, `alloc_mem`, `strlen`, `strcpy`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.str_dup.if.001` | 2694 | `if ( str[0] == '\0' )` |  | pending |
| `db.str_dup.return.001` | 2695 | `return &str_empty[0];` |  | pending |
| `db.str_dup.if.002` | 2697 | `if ( str >= string_space && str < top_string )` |  | pending |
| `db.str_dup.and.001` | 2697 | `&& str < top_string )` |  | pending |
| `db.str_dup.return.002` | 2698 | `return (char *) str;` |  | pending |
| `db.str_dup.return.003` | 2702 | `return str_new;` |  | pending |

## free_string

[Source line 2712](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2712); ends at line 2721. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_list_to_char: `src/act_info.c:202` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:220` (lexical_call_candidate).
- do_prompt: `src/act_info.c:894` (lexical_call_candidate).
- set_title: `src/act_info.c:2384` (lexical_call_candidate).
- do_description: `src/act_info.c:2447` (lexical_call_candidate).
- do_description: `src/act_info.c:2457` (lexical_call_candidate).
- do_description: `src/act_info.c:2479` (lexical_call_candidate).
- do_password: `src/act_info.c:2750` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2595` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2601` (lexical_call_candidate).
- do_bamfin: `src/act_wiz.c:457` (lexical_call_candidate).
- do_bamfout: `src/act_wiz.c:487` (lexical_call_candidate).
- do_return: `src/act_wiz.c:2267` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3745` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3752` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3759` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3766` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3814` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3821` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3828` (lexical_call_candidate).
- do_prefix: `src/act_wiz.c:4362` (lexical_call_candidate).
- do_prefix: `src/act_wiz.c:4370` (lexical_call_candidate).
- do_alias: `src/alias.c:186` (lexical_call_candidate).
- do_unalias: `src/alias.c:248` (lexical_call_candidate).
- do_unalias: `src/alias.c:249` (lexical_call_candidate).
- nanny: `src/comm.c:1776` (lexical_call_candidate).
- check_reconnect: `src/comm.c:2259` (lexical_call_candidate).
- make_corpse: `src/fight.c:1473` (lexical_call_candidate).
- make_corpse: `src/fight.c:1477` (lexical_call_candidate).
- death_cry: `src/fight.c:1617` (lexical_call_candidate).
- death_cry: `src/fight.c:1621` (lexical_call_candidate).
- create_money: `src/handler.c:2272` (lexical_call_candidate).
- create_money: `src/handler.c:2282` (lexical_call_candidate).
- create_money: `src/handler.c:2293` (lexical_call_candidate).
- do_function: `src/interp.c:525` (lexical_call_candidate).
- spell_create_water: `src/magic.c:1548` (lexical_call_candidate).
- note_remove: `src/note.c:412` (lexical_call_candidate).
- parse_note: `src/note.c:796` (lexical_call_candidate).
- parse_note: `src/note.c:837` (lexical_call_candidate).
- parse_note: `src/note.c:844` (lexical_call_candidate).
- parse_note: `src/note.c:859` (lexical_call_candidate).
- parse_note: `src/note.c:874` (lexical_call_candidate).
- free_note: `src/recycle.c:64` (lexical_call_candidate).
- free_note: `src/recycle.c:65` (lexical_call_candidate).
- free_note: `src/recycle.c:66` (lexical_call_candidate).
- free_note: `src/recycle.c:67` (lexical_call_candidate).
- free_note: `src/recycle.c:68` (lexical_call_candidate).
- free_ban: `src/recycle.c:103` (lexical_call_candidate).
- free_descriptor: `src/recycle.c:136` (lexical_call_candidate).
- free_extra_descr: `src/recycle.c:200` (lexical_call_candidate).
- free_extra_descr: `src/recycle.c:201` (lexical_call_candidate).
- free_obj: `src/recycle.c:285` (lexical_call_candidate).
- free_obj: `src/recycle.c:286` (lexical_call_candidate).
- free_obj: `src/recycle.c:287` (lexical_call_candidate).
- free_obj: `src/recycle.c:288` (lexical_call_candidate).
- free_char: `src/recycle.c:367` (lexical_call_candidate).
- free_char: `src/recycle.c:368` (lexical_call_candidate).
- free_char: `src/recycle.c:369` (lexical_call_candidate).
- free_char: `src/recycle.c:370` (lexical_call_candidate).
- free_char: `src/recycle.c:371` (lexical_call_candidate).
- free_char: `src/recycle.c:372` (lexical_call_candidate).
- free_pcdata: `src/recycle.c:422` (lexical_call_candidate).
- free_pcdata: `src/recycle.c:423` (lexical_call_candidate).
- free_pcdata: `src/recycle.c:424` (lexical_call_candidate).
- free_pcdata: `src/recycle.c:425` (lexical_call_candidate).
- free_pcdata: `src/recycle.c:430` (lexical_call_candidate).
- free_pcdata: `src/recycle.c:431` (lexical_call_candidate).
- fread_char: `src/save.c:1094` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2140` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/save.c:722` (declaration_or_dispatch_reference).

Dependencies: `free_mem`, `strlen`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.free_string.if.001` | 2714 | `if ( pstr == NULL     \|\|   pstr == &str_empty[0]     \|\| ( pstr >= string_space && pstr < top_string ) )` |  | pending |
| `db.free_string.or.001` | 2715 | `\|\|   pstr == &str_empty[0]` |  | pending |
| `db.free_string.or.002` | 2716 | `\|\| ( pstr >= string_space && pstr < top_string ) )` |  | pending |
| `db.free_string.and.001` | 2716 | `&& pstr < top_string ) )` |  | pending |
| `db.free_string.return.001` | 2717 | `return;` |  | pending |
| `db.free_string.return.002` | 2720 | `return;` |  | pending |

## do_areas

[Source line 2725](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2725); ends at line 2756. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:111` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:76` (declaration_or_dispatch_reference).

Dependencies: `send_to_char`, `sprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.do_areas.if.001` | 2733 | `if (argument[0] != '\0')` |  | pending |
| `db.do_areas.return.001` | 2736 | `return;` |  | pending |
| `db.do_areas.for.001` | 2742 | `for ( iArea = 0; iArea < iAreaHalf; iArea++ )` |  | pending |
| `db.do_areas.for.002` | 2745 | `for ( iArea = 0; iArea < iAreaHalf; iArea++ )` |  | pending |
| `db.do_areas.ternary.001` | 2748 | `? pArea2->credits : "" );` |  | pending |
| `db.do_areas.if.002` | 2751 | `if ( pArea2 != NULL )` |  | pending |
| `db.do_areas.return.002` | 2755 | `return;` |  | pending |

## do_memory

[Source line 2760](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2760); ends at line 2788. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:329` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:163` (declaration_or_dispatch_reference).

Dependencies: `sprintf`, `send_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.do_memory.return.001` | 2787 | `return;` |  | pending |

## do_dump

[Source line 2790](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2790); ends at line 2931. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/interp.c:284` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/interp.h:119` (declaration_or_dispatch_reference).

Dependencies: `fclose`, `fopen`, `fprintf`, `get_obj_index`, `get_mob_index`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.do_dump.for.001` | 2820 | `for (fch = char_list; fch != NULL; fch = fch->next)` |  | pending |
| `db.do_dump.if.001` | 2823 | `if (fch->pcdata != NULL)` |  | pending |
| `db.do_dump.for.002` | 2825 | `for (af = fch->affected; af != NULL; af = af->next)` |  | pending |
| `db.do_dump.for.003` | 2828 | `for (fch = char_free; fch != NULL; fch = fch->next)` |  | pending |
| `db.do_dump.for.004` | 2836 | `for (pc = pcdata_free; pc != NULL; pc = pc->next)` |  | pending |
| `db.do_dump.for.005` | 2844 | `for (d = descriptor_list; d != NULL; d = d->next)` |  | pending |
| `db.do_dump.for.006` | 2846 | `for (d= descriptor_free; d != NULL; d = d->next)` |  | pending |
| `db.do_dump.for.007` | 2853 | `for ( vnum = 0; nMatch < top_obj_index; vnum++ )` |  | pending |
| `db.do_dump.if.002` | 2854 | `if ( ( pObjIndex = get_obj_index( vnum ) ) != NULL )` |  | pending |
| `db.do_dump.for.008` | 2856 | `for (af = pObjIndex->affected; af != NULL; af = af->next)` |  | pending |
| `db.do_dump.for.009` | 2867 | `for (obj = object_list; obj != NULL; obj = obj->next)` |  | pending |
| `db.do_dump.for.010` | 2870 | `for (af = obj->affected; af != NULL; af = af->next)` |  | pending |
| `db.do_dump.for.011` | 2873 | `for (obj = obj_free; obj != NULL; obj = obj->next)` |  | pending |
| `db.do_dump.for.012` | 2881 | `for (af = affect_free; af != NULL; af = af->next)` |  | pending |
| `db.do_dump.for.013` | 2903 | `for (vnum = 0; nMatch < top_mob_index; vnum++)` |  | pending |
| `db.do_dump.if.003` | 2904 | `if ((pMobIndex = get_mob_index(vnum)) != NULL)` |  | pending |
| `db.do_dump.for.014` | 2919 | `for (vnum = 0; nMatch < top_obj_index; vnum++)` |  | pending |
| `db.do_dump.if.004` | 2920 | `if ((pObjIndex = get_obj_index(vnum)) != NULL)` |  | pending |

## number_fuzzy

[Source line 2938](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2938); ends at line 2947. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_drink: `src/act_obj.c:1243` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1322` (lexical_call_candidate).
- reset_area: `src/db.c:1315` (lexical_call_candidate).
- reset_area: `src/db.c:1355` (lexical_call_candidate).
- reset_area: `src/db.c:1433` (lexical_call_candidate).
- create_object: `src/db.c:1865` (lexical_call_candidate).
- create_object: `src/db.c:1866` (lexical_call_candidate).
- create_object: `src/db.c:1866` (lexical_call_candidate).
- create_object: `src/db.c:1913` (lexical_call_candidate).
- create_object: `src/db.c:1920` (lexical_call_candidate).
- create_object: `src/db.c:1921` (lexical_call_candidate).
- create_object: `src/db.c:1931` (lexical_call_candidate).
- create_object: `src/db.c:1931` (lexical_call_candidate).
- create_object: `src/db.c:1932` (lexical_call_candidate).
- create_object: `src/db.c:1932` (lexical_call_candidate).
- create_object: `src/db.c:1939` (lexical_call_candidate).
- create_object: `src/db.c:1940` (lexical_call_candidate).
- create_object: `src/db.c:1941` (lexical_call_candidate).
- create_object: `src/db.c:1948` (lexical_call_candidate).
- create_object: `src/db.c:1948` (lexical_call_candidate).
- do_berserk: `src/fight.c:2182` (lexical_call_candidate).
- spell_charm_person: `src/magic.c:1348` (lexical_call_candidate).
- spell_fireproof: `src/magic.c:2698` (lexical_call_candidate).
- spell_pass_door: `src/magic.c:3744` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2141` (declaration_or_dispatch_reference).

Dependencies: `number_bits`, `UMAX`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.number_fuzzy.switch.001` | 2940 | `switch ( number_bits( 2 ) )` |  | pending |
| `db.number_fuzzy.case.001` | 2942 | `case 0:  number -= 1;` |  | pending |
| `db.number_fuzzy.break.001` | 2942 | `break;` |  | pending |
| `db.number_fuzzy.case.002` | 2943 | `case 3:  number += 1;` |  | pending |
| `db.number_fuzzy.break.002` | 2943 | `break;` |  | pending |
| `db.number_fuzzy.return.001` | 2946 | `return UMAX( 1, number );` |  | pending |
| `db.number_fuzzy.number-10-bits-0.path` | 2940 | `number 10 bits 0` | db.number_fuzzy.number-10-bits-0 | specified |
| `db.number_fuzzy.number-10-bits-1.path` | 2940 | `number 10 bits 1` | db.number_fuzzy.number-10-bits-1 | specified |
| `db.number_fuzzy.number-10-bits-2.path` | 2940 | `number 10 bits 2` | db.number_fuzzy.number-10-bits-2 | specified |
| `db.number_fuzzy.number-10-bits-3.path` | 2940 | `number 10 bits 3` | db.number_fuzzy.number-10-bits-3 | specified |
| `db.number_fuzzy.number-1-bits-0.path` | 2940 | `number 1 bits 0` | db.number_fuzzy.number-1-bits-0 | specified |
| `db.number_fuzzy.number-0-bits-3.path` | 2940 | `number 0 bits 3` | db.number_fuzzy.number-0-bits-3 | specified |
| `db.number_fuzzy.number--2-bits-1.path` | 2940 | `number  2 bits 1` | db.number_fuzzy.number--2-bits-1 | specified |

## number_range

[Source line 2954](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2954); ends at line 2972. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_pose: `src/act_comm.c:1356` (lexical_call_candidate).
- get_random_room: `src/act_enter.c:48` (lexical_call_candidate).
- do_put: `src/act_obj.c:428` (lexical_call_candidate).
- do_put: `src/act_obj.c:466` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2199` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2249` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2250` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2928` (lexical_call_candidate).
- boot_db: `src/db.c:280` (lexical_call_candidate).
- boot_db: `src/db.c:282` (lexical_call_candidate).
- area_update: `src/db.c:1196` (lexical_call_candidate).
- reset_area: `src/db.c:1345` (lexical_call_candidate).
- reset_area: `src/db.c:1411` (lexical_call_candidate).
- reset_area: `src/db.c:1412` (lexical_call_candidate).
- reset_area: `src/db.c:1413` (lexical_call_candidate).
- reset_area: `src/db.c:1414` (lexical_call_candidate).
- reset_area: `src/db.c:1415` (lexical_call_candidate).
- reset_area: `src/db.c:1431` (lexical_call_candidate).
- reset_area: `src/db.c:1498` (lexical_call_candidate).
- create_mobile: `src/db.c:1551` (lexical_call_candidate).
- create_mobile: `src/db.c:1552` (lexical_call_candidate).
- create_mobile: `src/db.c:1580` (lexical_call_candidate).
- create_mobile: `src/db.c:1596` (lexical_call_candidate).
- create_mobile: `src/db.c:1700` (lexical_call_candidate).
- create_mobile: `src/db.c:1707` (lexical_call_candidate).
- dice: `src/db.c:3095` (lexical_call_candidate).
- acid_effect: `src/effects.c:78` (lexical_call_candidate).
- cold_effect: `src/effects.c:255` (lexical_call_candidate).
- fire_effect: `src/effects.c:333` (lexical_call_candidate).
- fire_effect: `src/effects.c:364` (lexical_call_candidate).
- poison_effect: `src/effects.c:500` (lexical_call_candidate).
- shock_effect: `src/effects.c:578` (lexical_call_candidate).
- check_assist: `src/fight.c:165` (lexical_call_candidate).
- mob_hit: `src/fight.c:308` (lexical_call_candidate).
- mob_hit: `src/fight.c:322` (lexical_call_candidate).
- one_hit: `src/fight.c:518` (lexical_call_candidate).
- one_hit: `src/fight.c:534` (lexical_call_candidate).
- one_hit: `src/fight.c:550` (lexical_call_candidate).
- one_hit: `src/fight.c:630` (lexical_call_candidate).
- one_hit: `src/fight.c:641` (lexical_call_candidate).
- one_hit: `src/fight.c:650` (lexical_call_candidate).
- one_hit: `src/fight.c:660` (lexical_call_candidate).
- damage: `src/fight.c:957` (lexical_call_candidate).
- make_corpse: `src/fight.c:1439` (lexical_call_candidate).
- make_corpse: `src/fight.c:1452` (lexical_call_candidate).
- make_corpse: `src/fight.c:1489` (lexical_call_candidate).
- make_corpse: `src/fight.c:1491` (lexical_call_candidate).
- make_corpse: `src/fight.c:1494` (lexical_call_candidate).
- death_cry: `src/fight.c:1614` (lexical_call_candidate).
- xp_compute: `src/fight.c:1958` (lexical_call_candidate).
- do_bash: `src/fight.c:2319` (lexical_call_candidate).
- do_dirt: `src/fight.c:2448` (lexical_call_candidate).
- do_trip: `src/fight.c:2574` (lexical_call_candidate).
- do_flee: `src/fight.c:2827` (lexical_call_candidate).
- do_kick: `src/fight.c:2960` (lexical_call_candidate).
- char_to_room: `src/handler.c:1436` (lexical_call_candidate).
- spell_burning_hands: `src/magic.c:893` (lexical_call_candidate).
- spell_calm: `src/magic.c:979` (lexical_call_candidate).
- spell_change_sex: `src/magic.c:1301` (lexical_call_candidate).
- spell_chill_touch: `src/magic.c:1378` (lexical_call_candidate).
- spell_colour_spray: `src/magic.c:1418` (lexical_call_candidate).
- spell_energy_drain: `src/magic.c:2644` (lexical_call_candidate).
- spell_fireball: `src/magic.c:2676` (lexical_call_candidate).
- spell_floating_disc: `src/magic.c:2789` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3051` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3063` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3070` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3079` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3092` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3101` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3129` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3141` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3150` (lexical_call_candidate).
- spell_lightning_bolt: `src/magic.c:3576` (lexical_call_candidate).
- spell_magic_missile: `src/magic.c:3664` (lexical_call_candidate).
- spell_shocking_grasp: `src/magic.c:4193` (lexical_call_candidate).
- spell_acid_breath: `src/magic.c:4477` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4508` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4564` (lexical_call_candidate).
- spell_gas_breath: `src/magic.c:4619` (lexical_call_candidate).
- spell_lightning_breath: `src/magic.c:4657` (lexical_call_candidate).
- spell_general_purpose: `src/magic.c:4682` (lexical_call_candidate).
- spell_high_explosive: `src/magic.c:4694` (lexical_call_candidate).
- check_improve: `src/skills.c:929` (lexical_call_candidate).
- check_improve: `src/skills.c:956` (lexical_call_candidate).
- spec_troll_member: `src/special.c:148` (lexical_call_candidate).
- spec_troll_member: `src/special.c:159` (lexical_call_candidate).
- spec_ogre_member: `src/special.c:207` (lexical_call_candidate).
- spec_ogre_member: `src/special.c:218` (lexical_call_candidate).
- spec_patrolman: `src/special.c:263` (lexical_call_candidate).
- spec_patrolman: `src/special.c:292` (lexical_call_candidate).
- spec_thief: `src/special.c:1018` (lexical_call_candidate).
- spec_thief: `src/special.c:1028` (lexical_call_candidate).
- spec_thief: `src/special.c:1032` (lexical_call_candidate).
- advance_level: `src/update.c:76` (lexical_call_candidate).
- advance_level: `src/update.c:79` (lexical_call_candidate).
- advance_level: `src/update.c:83` (lexical_call_candidate).
- mobile_update: `src/update.c:402` (lexical_call_candidate).
- mobile_update: `src/update.c:403` (lexical_call_candidate).
- char_update: `src/update.c:713` (lexical_call_candidate).
- char_update: `src/update.c:771` (lexical_call_candidate).
- char_update: `src/update.c:810` (lexical_call_candidate).
- obj_update: `src/update.c:869` (lexical_call_candidate).
- aggr_update: `src/update.c:1057` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2142` (declaration_or_dispatch_reference).

Dependencies: `number_mm`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.number_range.if.001` | 2959 | `if (from == 0 && to == 0)` |  | pending |
| `db.number_range.and.001` | 2959 | `&& to == 0)` |  | pending |
| `db.number_range.return.001` | 2960 | `return 0;` |  | pending |
| `db.number_range.if.002` | 2962 | `if ( ( to = to - from + 1 ) <= 1 )` |  | pending |
| `db.number_range.return.002` | 2963 | `return from;` |  | pending |
| `db.number_range.for.001` | 2965 | `for ( power = 2; power < to; power <<= 1 )` |  | pending |
| `db.number_range.while.001` | 2968 | `while ( ( number = number_mm() & (power -1 ) ) >= to )` |  | pending |
| `db.number_range.return.003` | 2971 | `return from + number;` |  | pending |
| `db.number_range.both-zero.path` | 2962 | `both zero` | db.number_range.both-zero | specified |
| `db.number_range.equal.path` | 2962 | `equal` | db.number_range.equal | specified |
| `db.number_range.reversed.path` | 2962 | `reversed` | db.number_range.reversed | specified |
| `db.number_range.lower-end.path` | 2962 | `lower end` | db.number_range.lower-end | specified |
| `db.number_range.upper-end.path` | 2962 | `upper end` | db.number_range.upper-end | specified |
| `db.number_range.reject-equality-then-accept.path` | 2962 | `reject equality then accept` | db.number_range.reject-equality-then-accept | specified |
| `db.number_range.multiple-rejections.path` | 2962 | `multiple rejections` | db.number_range.multiple-rejections | specified |
| `db.number_range.negative-domain.path` | 2962 | `negative domain` | db.number_range.negative-domain | specified |

## number_percent

[Source line 2979](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2979); ends at line 2987. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:108` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:482` (lexical_call_candidate).
- do_pick: `src/act_move.c:768` (lexical_call_candidate).
- do_sneak: `src/act_move.c:1345` (lexical_call_candidate).
- do_hide: `src/act_move.c:1372` (lexical_call_candidate).
- do_recall: `src/act_move.c:1438` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:862` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:909` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1932` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:1986` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2107` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2176` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2575` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2695` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2898` (lexical_call_candidate).
- acid_effect: `src/effects.c:121` (lexical_call_candidate).
- cold_effect: `src/effects.c:286` (lexical_call_candidate).
- fire_effect: `src/effects.c:410` (lexical_call_candidate).
- poison_effect: `src/effects.c:525` (lexical_call_candidate).
- shock_effect: `src/effects.c:609` (lexical_call_candidate).
- multi_hit: `src/fight.c:225` (lexical_call_candidate).
- multi_hit: `src/fight.c:238` (lexical_call_candidate).
- mob_hit: `src/fight.c:284` (lexical_call_candidate).
- mob_hit: `src/fight.c:296` (lexical_call_candidate).
- one_hit: `src/fight.c:545` (lexical_call_candidate).
- one_hit: `src/fight.c:558` (lexical_call_candidate).
- check_parry: `src/fight.c:1283` (lexical_call_candidate).
- check_shield_block: `src/fight.c:1309` (lexical_call_candidate).
- check_dodge: `src/fight.c:1336` (lexical_call_candidate).
- do_berserk: `src/fight.c:2163` (lexical_call_candidate).
- do_bash: `src/fight.c:2306` (lexical_call_candidate).
- do_dirt: `src/fight.c:2443` (lexical_call_candidate).
- do_trip: `src/fight.c:2564` (lexical_call_candidate).
- do_backstab: `src/fight.c:2785` (lexical_call_candidate).
- do_flee: `src/fight.c:2844` (lexical_call_candidate).
- do_rescue: `src/fight.c:2913` (lexical_call_candidate).
- do_kick: `src/fight.c:2958` (lexical_call_candidate).
- do_disarm: `src/fight.c:3032` (lexical_call_candidate).
- can_see: `src/handler.c:2480` (lexical_call_candidate).
- saves_spell: `src/magic.c:234` (lexical_call_candidate).
- saves_dispel: `src/magic.c:249` (lexical_call_candidate).
- do_cast: `src/magic.c:539` (lexical_call_candidate).
- spell_enchant_armor: `src/magic.c:2282` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2475` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3603` (lexical_call_candidate).
- spell_recharge: `src/magic.c:4005` (lexical_call_candidate).
- check_improve: `src/skills.c:937` (lexical_call_candidate).
- check_improve: `src/skills.c:950` (lexical_call_candidate).
- spec_poison: `src/special.c:987` (lexical_call_candidate).
- hit_gain: `src/update.c:175` (lexical_call_candidate).
- mana_gain: `src/update.c:241` (lexical_call_candidate).
- char_update: `src/update.c:636` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2143` (declaration_or_dispatch_reference).

Dependencies: `number_mm`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.number_percent.while.001` | 2983 | `while ( (percent = number_mm() & (128-1) ) > 99 )` |  | pending |
| `db.number_percent.return.001` | 2986 | `return 1 + percent;` |  | pending |
| `db.number_percent.lower.path` | 2983 | `lower` | db.number_percent.lower | specified |
| `db.number_percent.upper.path` | 2983 | `upper` | db.number_percent.upper | specified |
| `db.number_percent.reject-100.path` | 2983 | `reject 100` | db.number_percent.reject-100 | specified |
| `db.number_percent.reject-127.path` | 2983 | `reject 127` | db.number_percent.reject-127 | specified |
| `db.number_percent.mask-before-test.path` | 2983 | `mask before test` | db.number_percent.mask-before-test | specified |

## number_door

[Source line 2994](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2994); ends at line 3002. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_flee: `src/fight.c:2823` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2144` (declaration_or_dispatch_reference).

Dependencies: `number_mm`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.number_door.while.001` | 2998 | `while ( ( door = number_mm() & (8-1) ) > 5)` |  | pending |
| `db.number_door.return.001` | 3001 | `return door;` |  | pending |
| `db.number_door.lower.path` | 2998 | `lower` | db.number_door.lower | specified |
| `db.number_door.upper.path` | 2998 | `upper` | db.number_door.upper | specified |
| `db.number_door.reject-six-seven.path` | 2998 | `reject six seven` | db.number_door.reject-six-seven | specified |
| `db.number_door.mask-before-test.path` | 2998 | `mask before test` | db.number_door.mask-before-test | specified |

## number_bits

[Source line 3004](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3004); ends at line 3007. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- number_fuzzy: `src/db.c:2940` (lexical_call_candidate).
- check_assist: `src/fight.c:156` (lexical_call_candidate).
- one_hit: `src/fight.c:499` (lexical_call_candidate).
- damage: `src/fight.c:969` (lexical_call_candidate).
- death_cry: `src/fight.c:1552` (lexical_call_candidate).
- char_to_room: `src/handler.c:1445` (lexical_call_candidate).
- check_social: `src/interp.c:609` (lexical_call_candidate).
- spec_nasty: `src/special.c:357` (lexical_call_candidate).
- dragon: `src/special.c:392` (lexical_call_candidate).
- spec_breath_any: `src/special.c:415` (lexical_call_candidate).
- spec_cast_adept: `src/special.c:486` (lexical_call_candidate).
- spec_cast_adept: `src/special.c:494` (lexical_call_candidate).
- spec_cast_cleric: `src/special.c:553` (lexical_call_candidate).
- spec_cast_cleric: `src/special.c:564` (lexical_call_candidate).
- spec_cast_judge: `src/special.c:604` (lexical_call_candidate).
- spec_cast_mage: `src/special.c:633` (lexical_call_candidate).
- spec_cast_mage: `src/special.c:644` (lexical_call_candidate).
- spec_cast_undead: `src/special.c:685` (lexical_call_candidate).
- spec_cast_undead: `src/special.c:696` (lexical_call_candidate).
- spec_thief: `src/special.c:1014` (lexical_call_candidate).
- mobile_update: `src/update.c:414` (lexical_call_candidate).
- mobile_update: `src/update.c:442` (lexical_call_candidate).
- mobile_update: `src/update.c:443` (lexical_call_candidate).
- weather_update: `src/update.c:540` (lexical_call_candidate).
- weather_update: `src/update.c:549` (lexical_call_candidate).
- weather_update: `src/update.c:555` (lexical_call_candidate).
- weather_update: `src/update.c:563` (lexical_call_candidate).
- weather_update: `src/update.c:570` (lexical_call_candidate).
- weather_update: `src/update.c:579` (lexical_call_candidate).
- char_update: `src/update.c:780` (lexical_call_candidate).
- aggr_update: `src/update.c:1037` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2145` (declaration_or_dispatch_reference).

Dependencies: `number_mm`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.number_bits.return.001` | 3006 | `return number_mm( ) & ( ( 1 << width ) - 1 );` |  | pending |
| `db.number_bits.width-0-raw-255.path` | 3006 | `width 0 raw 255` | db.number_bits.width-0-raw-255 | specified |
| `db.number_bits.width-1-raw-2.path` | 3006 | `width 1 raw 2` | db.number_bits.width-1-raw-2 | specified |
| `db.number_bits.width-2-raw-7.path` | 3006 | `width 2 raw 7` | db.number_bits.width-2-raw-7 | specified |
| `db.number_bits.width-3-raw-5.path` | 3006 | `width 3 raw 5` | db.number_bits.width-3-raw-5 | specified |

## init_mm

[Source line 3027](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3027); ends at line 3049. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- boot_db: `src/db.c:253` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/db.c:211` (declaration_or_dispatch_reference).

Dependencies: `defined`, `srandom`, `time`, `getpid`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.init_mm.if.001` | 3029 | `if defined (OLD_RAND)` |  | pending |
| `db.init_mm.for.001` | 3040 | `for ( iState = 2; iState < 55; iState++ )` |  | pending |
| `db.init_mm.return.001` | 3048 | `return;` |  | pending |

## number_mm

[Source line 3053](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3053); ends at line 3077. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- number_range: `src/db.c:2968` (lexical_call_candidate).
- number_percent: `src/db.c:2983` (lexical_call_candidate).
- number_door: `src/db.c:2998` (lexical_call_candidate).
- number_bits: `src/db.c:3006` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2146` (declaration_or_dispatch_reference).

Dependencies: `defined`, `random`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.number_mm.if.001` | 3055 | `if defined (OLD_RAND)` |  | pending |
| `db.number_mm.if.002` | 3067 | `if ( ++iState1 == 55 )` |  | pending |
| `db.number_mm.if.003` | 3069 | `if ( ++iState2 == 55 )` |  | pending |
| `db.number_mm.return.001` | 3073 | `return iRand >> 6;` |  | pending |
| `db.number_mm.return.002` | 3075 | `return random() >> 6;` |  | pending |

## dice

[Source line 3083](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3083); ends at line 3098. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- create_mobile: `src/db.c:1568` (lexical_call_candidate).
- create_mobile: `src/db.c:1572` (lexical_call_candidate).
- create_mobile: `src/db.c:1705` (lexical_call_candidate).
- one_hit: `src/fight.c:523` (lexical_call_candidate).
- one_hit: `src/fight.c:532` (lexical_call_candidate).
- do_heal: `src/healer.c:186` (lexical_call_candidate).
- spell_acid_blast: `src/magic.c:729` (lexical_call_candidate).
- spell_call_lightning: `src/magic.c:920` (lexical_call_candidate).
- spell_cause_light: `src/magic.c:1184` (lexical_call_candidate).
- spell_cause_critical: `src/magic.c:1192` (lexical_call_candidate).
- spell_cause_serious: `src/magic.c:1200` (lexical_call_candidate).
- spell_chain_lightning: `src/magic.c:1220` (lexical_call_candidate).
- spell_chain_lightning: `src/magic.c:1242` (lexical_call_candidate).
- spell_chain_lightning: `src/magic.c:1266` (lexical_call_candidate).
- spell_control_weather: `src/magic.c:1468` (lexical_call_candidate).
- spell_control_weather: `src/magic.c:1470` (lexical_call_candidate).
- spell_cure_critical: `src/magic.c:1588` (lexical_call_candidate).
- spell_cure_light: `src/magic.c:1627` (lexical_call_candidate).
- spell_cure_serious: `src/magic.c:1665` (lexical_call_candidate).
- spell_demonfire: `src/magic.c:1776` (lexical_call_candidate).
- spell_dispel_evil: `src/magic.c:1971` (lexical_call_candidate).
- spell_dispel_evil: `src/magic.c:1973` (lexical_call_candidate).
- spell_dispel_good: `src/magic.c:2002` (lexical_call_candidate).
- spell_dispel_good: `src/magic.c:2004` (lexical_call_candidate).
- spell_earthquake: `src/magic.c:2207` (lexical_call_candidate).
- spell_energy_drain: `src/magic.c:2647` (lexical_call_candidate).
- spell_flamestrike: `src/magic.c:2716` (lexical_call_candidate).
- spell_harm: `src/magic.c:2966` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3207` (lexical_call_candidate).
- spell_holy_word: `src/magic.c:3218` (lexical_call_candidate).
- spell_ray_of_truth: `src/magic.c:3956` (lexical_call_candidate).
- spell_acid_breath: `src/magic.c:4478` (lexical_call_candidate).
- spell_fire_breath: `src/magic.c:4509` (lexical_call_candidate).
- spell_frost_breath: `src/magic.c:4565` (lexical_call_candidate).
- spell_gas_breath: `src/magic.c:4620` (lexical_call_candidate).
- spell_lightning_breath: `src/magic.c:4658` (lexical_call_candidate).
- weather_update: `src/update.c:523` (lexical_call_candidate).
- weather_update: `src/update.c:523` (lexical_call_candidate).
- weather_update: `src/update.c:523` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2147` (declaration_or_dispatch_reference).

Dependencies: `number_range`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.dice.switch.001` | 3088 | `switch ( size )` |  | pending |
| `db.dice.case.001` | 3090 | `case 0: return 0;` |  | pending |
| `db.dice.return.001` | 3090 | `return 0;` |  | pending |
| `db.dice.case.002` | 3091 | `case 1: return number;` |  | pending |
| `db.dice.return.002` | 3091 | `return number;` |  | pending |
| `db.dice.for.001` | 3094 | `for ( idice = 0, sum = 0; idice < number; idice++ )` |  | pending |
| `db.dice.return.003` | 3097 | `return sum;` |  | pending |
| `db.dice.size-zero.path` | 3088 | `size zero` | db.dice.size-zero | specified |
| `db.dice.size-one.path` | 3088 | `size one` | db.dice.size-one | specified |
| `db.dice.size-one-negative-count-quirk.path` | 3088 | `size one negative count quirk` | db.dice.size-one-negative-count-quirk | specified |
| `db.dice.zero-dice.path` | 3088 | `zero dice` | db.dice.zero-dice | specified |
| `db.dice.negative-count.path` | 3088 | `negative count` | db.dice.negative-count | specified |
| `db.dice.one-die.path` | 3088 | `one die` | db.dice.one-die | specified |
| `db.dice.multiple.path` | 3088 | `multiple` | db.dice.multiple | specified |

## interpolate

[Source line 3105](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3105); ends at line 3108. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- create_mobile: `src/db.c:1714` (lexical_call_candidate).
- create_mobile: `src/db.c:1715` (lexical_call_candidate).
- one_hit: `src/fight.c:462` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2148` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.interpolate.return.001` | 3107 | `return value_00 + level * (value_32 - value_00) / 32;` |  | pending |
| `db.interpolate.zero.path` | 3107 | `zero` | db.interpolate.zero | specified |
| `db.interpolate.endpoint.path` | 3107 | `endpoint` | db.interpolate.endpoint | specified |
| `db.interpolate.positive-fraction.path` | 3107 | `positive fraction` | db.interpolate.positive-fraction | specified |
| `db.interpolate.negative-fraction-truncates-to-zero.path` | 3107 | `negative fraction truncates to zero` | db.interpolate.negative-fraction-truncates-to-zero | specified |
| `db.interpolate.negative-level.path` | 3107 | `negative level` | db.interpolate.negative-level | specified |
| `db.interpolate.extrapolates.path` | 3107 | `extrapolates` | db.interpolate.extrapolates | specified |

## smash_tilde

[Source line 3116](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3116); ends at line 3125. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_prompt: `src/act_info.c:888` (lexical_call_candidate).
- do_title: `src/act_info.c:2405` (lexical_call_candidate).
- do_description: `src/act_info.c:2419` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2523` (lexical_call_candidate).
- do_bamfin: `src/act_wiz.c:442` (lexical_call_candidate).
- do_bamfout: `src/act_wiz.c:472` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3333` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3709` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3872` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:3984` (lexical_call_candidate).
- do_alias: `src/alias.c:110` (lexical_call_candidate).
- parse_note: `src/note.c:581` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2149` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.smash_tilde.for.001` | 3118 | `for ( ; *str != '\0'; str++ )` |  | pending |
| `db.smash_tilde.if.001` | 3120 | `if ( *str == '~' )` |  | pending |
| `db.smash_tilde.return.001` | 3124 | `return;` |  | pending |
| `db.smash_tilde.empty.path` | 3120 | `empty` | db.smash_tilde.empty | specified |
| `db.smash_tilde.no-tilde.path` | 3120 | `no tilde` | db.smash_tilde.no-tilde | specified |
| `db.smash_tilde.one.path` | 3120 | `one` | db.smash_tilde.one | specified |
| `db.smash_tilde.multiple.path` | 3120 | `multiple` | db.smash_tilde.multiple | specified |

## str_cmp

[Source line 3134](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3134); ends at line 3155. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_order: `src/act_comm.c:1623` (lexical_call_candidate).
- do_order: `src/act_comm.c:1641` (lexical_call_candidate).
- do_look: `src/act_info.c:1025` (lexical_call_candidate).
- do_look: `src/act_info.c:1056` (lexical_call_candidate).
- do_look: `src/act_info.c:1056` (lexical_call_candidate).
- do_look: `src/act_info.c:1056` (lexical_call_candidate).
- do_look: `src/act_info.c:1200` (lexical_call_candidate).
- do_look: `src/act_info.c:1200` (lexical_call_candidate).
- do_look: `src/act_info.c:1201` (lexical_call_candidate).
- do_look: `src/act_info.c:1201` (lexical_call_candidate).
- do_look: `src/act_info.c:1202` (lexical_call_candidate).
- do_look: `src/act_info.c:1202` (lexical_call_candidate).
- do_look: `src/act_info.c:1203` (lexical_call_candidate).
- do_look: `src/act_info.c:1203` (lexical_call_candidate).
- do_look: `src/act_info.c:1204` (lexical_call_candidate).
- do_look: `src/act_info.c:1204` (lexical_call_candidate).
- do_look: `src/act_info.c:1205` (lexical_call_candidate).
- do_look: `src/act_info.c:1205` (lexical_call_candidate).
- do_exits: `src/act_info.c:1326` (lexical_call_candidate).
- do_help: `src/act_info.c:1781` (lexical_call_candidate).
- find_door: `src/act_move.c:292` (lexical_call_candidate).
- find_door: `src/act_move.c:292` (lexical_call_candidate).
- find_door: `src/act_move.c:293` (lexical_call_candidate).
- find_door: `src/act_move.c:293` (lexical_call_candidate).
- find_door: `src/act_move.c:294` (lexical_call_candidate).
- find_door: `src/act_move.c:294` (lexical_call_candidate).
- find_door: `src/act_move.c:295` (lexical_call_candidate).
- find_door: `src/act_move.c:295` (lexical_call_candidate).
- find_door: `src/act_move.c:296` (lexical_call_candidate).
- find_door: `src/act_move.c:296` (lexical_call_candidate).
- find_door: `src/act_move.c:297` (lexical_call_candidate).
- find_door: `src/act_move.c:297` (lexical_call_candidate).
- do_train: `src/act_move.c:1506` (lexical_call_candidate).
- do_train: `src/act_move.c:1514` (lexical_call_candidate).
- do_train: `src/act_move.c:1522` (lexical_call_candidate).
- do_train: `src/act_move.c:1530` (lexical_call_candidate).
- do_train: `src/act_move.c:1538` (lexical_call_candidate).
- do_train: `src/act_move.c:1546` (lexical_call_candidate).
- do_train: `src/act_move.c:1549` (lexical_call_candidate).
- do_train: `src/act_move.c:1588` (lexical_call_candidate).
- do_train: `src/act_move.c:1605` (lexical_call_candidate).
- can_loot: `src/act_obj.c:70` (lexical_call_candidate).
- can_loot: `src/act_obj.c:76` (lexical_call_candidate).
- do_get: `src/act_obj.c:204` (lexical_call_candidate).
- do_get: `src/act_obj.c:216` (lexical_call_candidate).
- do_get: `src/act_obj.c:255` (lexical_call_candidate).
- do_get: `src/act_obj.c:294` (lexical_call_candidate).
- do_put: `src/act_obj.c:355` (lexical_call_candidate).
- do_put: `src/act_obj.c:355` (lexical_call_candidate).
- do_put: `src/act_obj.c:364` (lexical_call_candidate).
- do_put: `src/act_obj.c:388` (lexical_call_candidate).
- do_drop: `src/act_obj.c:513` (lexical_call_candidate).
- do_drop: `src/act_obj.c:513` (lexical_call_candidate).
- do_drop: `src/act_obj.c:514` (lexical_call_candidate).
- do_drop: `src/act_obj.c:514` (lexical_call_candidate).
- do_drop: `src/act_obj.c:520` (lexical_call_candidate).
- do_drop: `src/act_obj.c:520` (lexical_call_candidate).
- do_drop: `src/act_obj.c:521` (lexical_call_candidate).
- do_drop: `src/act_obj.c:585` (lexical_call_candidate).
- do_give: `src/act_obj.c:679` (lexical_call_candidate).
- do_give: `src/act_obj.c:679` (lexical_call_candidate).
- do_give: `src/act_obj.c:680` (lexical_call_candidate).
- do_give: `src/act_obj.c:680` (lexical_call_candidate).
- do_give: `src/act_obj.c:686` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1037` (lexical_call_candidate).
- do_wear: `src/act_obj.c:1686` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1754` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2242` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2243` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2244` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2245` (lexical_call_candidate).
- obj_to_keeper: `src/act_obj.c:2389` (lexical_call_candidate).
- get_obj_keeper: `src/act_obj.c:2443` (lexical_call_candidate).
- get_cost: `src/act_obj.c:2482` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2647` (lexical_call_candidate).
- do_list: `src/act_obj.c:2824` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:627` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:638` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:797` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1057` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1063` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1069` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1069` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1742` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1748` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1748` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1754` (lexical_call_candidate).
- do_vnum: `src/act_wiz.c:1754` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2445` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2445` (lexical_call_candidate).
- do_load: `src/act_wiz.c:2451` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2764` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2791` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2911` (lexical_call_candidate).
- do_slookup: `src/act_wiz.c:3175` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3283` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3366` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3381` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3396` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3410` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3425` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3901` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3901` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3907` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3907` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3913` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3913` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3919` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3919` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3925` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3925` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4106` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4114` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4136` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4159` (lexical_call_candidate).
- do_alias: `src/alias.c:146` (lexical_call_candidate).
- do_alias: `src/alias.c:160` (lexical_call_candidate).
- do_alias: `src/alias.c:184` (lexical_call_candidate).
- ban_site: `src/ban.c:216` (lexical_call_candidate).
- do_allow: `src/ban.c:284` (lexical_call_candidate).
- nanny: `src/comm.c:1695` (lexical_call_candidate).
- nanny: `src/comm.c:2006` (lexical_call_candidate).
- check_parse_name: `src/comm.c:2158` (lexical_call_candidate).
- check_parse_name: `src/comm.c:2162` (lexical_call_candidate).
- check_reconnect: `src/comm.c:2255` (lexical_call_candidate).
- check_playing: `src/comm.c:2300` (lexical_call_candidate).
- boot_db: `src/db.c:348` (lexical_call_candidate).
- boot_db: `src/db.c:349` (lexical_call_candidate).
- boot_db: `src/db.c:350` (lexical_call_candidate).
- boot_db: `src/db.c:351` (lexical_call_candidate).
- boot_db: `src/db.c:352` (lexical_call_candidate).
- boot_db: `src/db.c:353` (lexical_call_candidate).
- boot_db: `src/db.c:354` (lexical_call_candidate).
- boot_db: `src/db.c:355` (lexical_call_candidate).
- boot_db: `src/db.c:356` (lexical_call_candidate).
- boot_db: `src/db.c:357` (lexical_call_candidate).
- boot_db: `src/db.c:358` (lexical_call_candidate).
- load_helps: `src/db.c:441` (lexical_call_candidate).
- str_suffix: `src/db.c:3230` (lexical_call_candidate).
- is_exact_name: `src/handler.c:860` (lexical_call_candidate).
- get_char_room: `src/handler.c:2023` (lexical_call_candidate).
- check_social: `src/interp.c:575` (lexical_call_candidate).
- do_cast: `src/magic.c:534` (lexical_call_candidate).
- spell_control_weather: `src/magic.c:1467` (lexical_call_candidate).
- spell_control_weather: `src/magic.c:1469` (lexical_call_candidate).
- do_play: `src/music.c:243` (lexical_call_candidate).
- do_play: `src/music.c:254` (lexical_call_candidate).
- do_play: `src/music.c:290` (lexical_call_candidate).
- load_thread: `src/note.c:237` (lexical_call_candidate).
- load_thread: `src/note.c:241` (lexical_call_candidate).
- load_thread: `src/note.c:245` (lexical_call_candidate).
- load_thread: `src/note.c:249` (lexical_call_candidate).
- load_thread: `src/note.c:253` (lexical_call_candidate).
- load_thread: `src/note.c:257` (lexical_call_candidate).
- is_note_to: `src/note.c:345` (lexical_call_candidate).
- note_remove: `src/note.c:403` (lexical_call_candidate).
- note_remove: `src/note.c:410` (lexical_call_candidate).
- hide_note: `src/note.c:500` (lexical_call_candidate).
- parse_note: `src/note.c:587` (lexical_call_candidate).
- parse_note: `src/note.c:775` (lexical_call_candidate).
- parse_note: `src/note.c:803` (lexical_call_candidate).
- parse_note: `src/note.c:932` (lexical_call_candidate).
- parse_note: `src/note.c:940` (lexical_call_candidate).
- fwrite_char: `src/save.c:182` (lexical_call_candidate).
- load_char_obj: `src/save.c:614` (lexical_call_candidate).
- load_char_obj: `src/save.c:615` (lexical_call_candidate).
- load_char_obj: `src/save.c:616` (lexical_call_candidate).
- load_char_obj: `src/save.c:617` (lexical_call_candidate).
- load_char_obj: `src/save.c:618` (lexical_call_candidate).
- fread_char: `src/save.c:759` (lexical_call_candidate).
- fread_char: `src/save.c:775` (lexical_call_candidate).
- fread_char: `src/save.c:791` (lexical_call_candidate).
- fread_char: `src/save.c:791` (lexical_call_candidate).
- fread_char: `src/save.c:798` (lexical_call_candidate).
- fread_char: `src/save.c:808` (lexical_call_candidate).
- fread_char: `src/save.c:832` (lexical_call_candidate).
- fread_char: `src/save.c:857` (lexical_call_candidate).
- fread_char: `src/save.c:857` (lexical_call_candidate).
- fread_char: `src/save.c:866` (lexical_call_candidate).
- fread_char: `src/save.c:866` (lexical_call_candidate).
- fread_char: `src/save.c:889` (lexical_call_candidate).
- fread_char: `src/save.c:889` (lexical_call_candidate).
- fread_char: `src/save.c:897` (lexical_call_candidate).
- fread_char: `src/save.c:918` (lexical_call_candidate).
- fread_char: `src/save.c:939` (lexical_call_candidate).
- fread_char: `src/save.c:939` (lexical_call_candidate).
- fread_char: `src/save.c:962` (lexical_call_candidate).
- fread_char: `src/save.c:962` (lexical_call_candidate).
- fread_char: `src/save.c:974` (lexical_call_candidate).
- fread_char: `src/save.c:974` (lexical_call_candidate).
- fread_char: `src/save.c:1006` (lexical_call_candidate).
- fread_char: `src/save.c:1037` (lexical_call_candidate).
- fread_char: `src/save.c:1058` (lexical_call_candidate).
- fread_char: `src/save.c:1058` (lexical_call_candidate).
- fread_char: `src/save.c:1087` (lexical_call_candidate).
- fread_char: `src/save.c:1087` (lexical_call_candidate).
- fread_char: `src/save.c:1106` (lexical_call_candidate).
- fread_pet: `src/save.c:1140` (lexical_call_candidate).
- fread_pet: `src/save.c:1176` (lexical_call_candidate).
- fread_pet: `src/save.c:1186` (lexical_call_candidate).
- fread_pet: `src/save.c:1210` (lexical_call_candidate).
- fread_pet: `src/save.c:1235` (lexical_call_candidate).
- fread_pet: `src/save.c:1245` (lexical_call_candidate).
- fread_pet: `src/save.c:1267` (lexical_call_candidate).
- fread_pet: `src/save.c:1295` (lexical_call_candidate).
- fread_obj: `src/save.c:1364` (lexical_call_candidate).
- fread_obj: `src/save.c:1410` (lexical_call_candidate).
- fread_obj: `src/save.c:1433` (lexical_call_candidate).
- fread_obj: `src/save.c:1471` (lexical_call_candidate).
- fread_obj: `src/save.c:1481` (lexical_call_candidate).
- fread_obj: `src/save.c:1481` (lexical_call_candidate).
- fread_obj: `src/save.c:1494` (lexical_call_candidate).
- fread_obj: `src/save.c:1550` (lexical_call_candidate).
- fread_obj: `src/save.c:1567` (lexical_call_candidate).
- fread_obj: `src/save.c:1580` (lexical_call_candidate).
- fread_obj: `src/save.c:1611` (lexical_call_candidate).
- fread_obj: `src/save.c:1611` (lexical_call_candidate).
- fread_obj: `src/save.c:1623` (lexical_call_candidate).
- fread_obj: `src/save.c:1634` (lexical_call_candidate).
- do_scan: `src/scan.c:71` (lexical_call_candidate).
- do_scan: `src/scan.c:71` (lexical_call_candidate).
- do_scan: `src/scan.c:72` (lexical_call_candidate).
- do_scan: `src/scan.c:72` (lexical_call_candidate).
- do_scan: `src/scan.c:73` (lexical_call_candidate).
- do_scan: `src/scan.c:73` (lexical_call_candidate).
- do_scan: `src/scan.c:74` (lexical_call_candidate).
- do_scan: `src/scan.c:74` (lexical_call_candidate).
- do_scan: `src/scan.c:75` (lexical_call_candidate).
- do_scan: `src/scan.c:75` (lexical_call_candidate).
- do_scan: `src/scan.c:76` (lexical_call_candidate).
- do_scan: `src/scan.c:76` (lexical_call_candidate).
- do_groups: `src/skills.c:867` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2150` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/save.c:707` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/save.c:720` (declaration_or_dispatch_reference).

Dependencies: `bug`, `LOWER`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.str_cmp.if.001` | 3136 | `if ( astr == NULL )` |  | pending |
| `db.str_cmp.return.001` | 3139 | `return TRUE;` |  | pending |
| `db.str_cmp.if.002` | 3142 | `if ( bstr == NULL )` |  | pending |
| `db.str_cmp.return.002` | 3145 | `return TRUE;` |  | pending |
| `db.str_cmp.for.001` | 3148 | `for ( ; *astr \|\| *bstr; astr++, bstr++ )` |  | pending |
| `db.str_cmp.or.001` | 3148 | `\|\| *bstr;` |  | pending |
| `db.str_cmp.if.003` | 3150 | `if ( LOWER(*astr) != LOWER(*bstr) )` |  | pending |
| `db.str_cmp.return.003` | 3151 | `return TRUE;` |  | pending |
| `db.str_cmp.return.004` | 3154 | `return FALSE;` |  | pending |
| `db.str_cmp.empty-equal.path` | 3134 | `empty equal` | db.str_cmp.empty-equal | specified |
| `db.str_cmp.ascii-case-equal.path` | 3134 | `ascii case equal` | db.str_cmp.ascii-case-equal | specified |
| `db.str_cmp.first-mismatch.path` | 3134 | `first mismatch` | db.str_cmp.first-mismatch | specified |
| `db.str_cmp.left-shorter.path` | 3134 | `left shorter` | db.str_cmp.left-shorter | specified |
| `db.str_cmp.right-shorter.path` | 3134 | `right shorter` | db.str_cmp.right-shorter | specified |
| `db.str_cmp.null-left.path` | 3136 | `null left` | db.str_cmp.null-left | specified |
| `db.str_cmp.null-right.path` | 3142 | `null right` | db.str_cmp.null-right | specified |
| `db.str_cmp.both-null-left-dominates.path` | 3136 | `both null left dominates` | db.str_cmp.both-null-left-dominates | specified |

## str_prefix

[Source line 3164](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3164); ends at line 3185. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_whois: `src/act_info.c:1842` (lexical_call_candidate).
- do_who: `src/act_info.c:1955` (lexical_call_candidate).
- do_who: `src/act_info.c:1968` (lexical_call_candidate).
- do_get: `src/act_obj.c:216` (lexical_call_candidate).
- do_get: `src/act_obj.c:255` (lexical_call_candidate).
- do_get: `src/act_obj.c:294` (lexical_call_candidate).
- do_put: `src/act_obj.c:364` (lexical_call_candidate).
- do_put: `src/act_obj.c:388` (lexical_call_candidate).
- do_drop: `src/act_obj.c:585` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:69` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:76` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:84` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:105` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:198` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2327` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2337` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2337` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3220` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3220` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3226` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3226` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3232` (lexical_call_candidate).
- do_set: `src/act_wiz.c:3238` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3440` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3453` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3485` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3503` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3509` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3515` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3528` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3541` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3554` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3565` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3576` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3587` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3605` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3623` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3641` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3659` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3681` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3725` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3725` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3738` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3750` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3757` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3764` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3772` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3784` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3802` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3812` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3819` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3826` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3833` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3833` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3931` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3937` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3943` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3949` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3955` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3961` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4024` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4030` (lexical_call_candidate).
- substitute_alias: `src/alias.c:49` (lexical_call_candidate).
- substitute_alias: `src/alias.c:61` (lexical_call_candidate).
- substitute_alias: `src/alias.c:61` (lexical_call_candidate).
- substitute_alias: `src/alias.c:62` (lexical_call_candidate).
- substitute_alias: `src/alias.c:75` (lexical_call_candidate).
- do_alias: `src/alias.c:146` (lexical_call_candidate).
- do_alias: `src/alias.c:173` (lexical_call_candidate).
- do_alias: `src/alias.c:173` (lexical_call_candidate).
- check_ban: `src/ban.c:128` (lexical_call_candidate).
- ban_site: `src/ban.c:180` (lexical_call_candidate).
- ban_site: `src/ban.c:182` (lexical_call_candidate).
- ban_site: `src/ban.c:184` (lexical_call_candidate).
- check_parse_name: `src/comm.c:2162` (lexical_call_candidate).
- str_infix: `src/db.c:3209` (lexical_call_candidate).
- load_mobiles: `src/db2.c:257` (lexical_call_candidate).
- load_mobiles: `src/db2.c:259` (lexical_call_candidate).
- load_mobiles: `src/db2.c:261` (lexical_call_candidate).
- load_mobiles: `src/db2.c:263` (lexical_call_candidate).
- load_mobiles: `src/db2.c:265` (lexical_call_candidate).
- load_mobiles: `src/db2.c:267` (lexical_call_candidate).
- load_mobiles: `src/db2.c:269` (lexical_call_candidate).
- load_mobiles: `src/db2.c:271` (lexical_call_candidate).
- do_flag: `src/flags.c:91` (lexical_call_candidate).
- do_flag: `src/flags.c:91` (lexical_call_candidate).
- do_flag: `src/flags.c:101` (lexical_call_candidate).
- do_flag: `src/flags.c:113` (lexical_call_candidate).
- do_flag: `src/flags.c:125` (lexical_call_candidate).
- do_flag: `src/flags.c:131` (lexical_call_candidate).
- do_flag: `src/flags.c:137` (lexical_call_candidate).
- do_flag: `src/flags.c:143` (lexical_call_candidate).
- do_flag: `src/flags.c:149` (lexical_call_candidate).
- do_flag: `src/flags.c:161` (lexical_call_candidate).
- do_flag: `src/flags.c:173` (lexical_call_candidate).
- race_lookup: `src/handler.c:123` (lexical_call_candidate).
- liq_lookup: `src/handler.c:137` (lexical_call_candidate).
- weapon_lookup: `src/handler.c:151` (lexical_call_candidate).
- weapon_type: `src/handler.c:165` (lexical_call_candidate).
- item_lookup: `src/handler.c:180` (lexical_call_candidate).
- attack_lookup: `src/handler.c:214` (lexical_call_candidate).
- wiznet_lookup: `src/handler.c:229` (lexical_call_candidate).
- class_lookup: `src/handler.c:244` (lexical_call_candidate).
- is_name: `src/handler.c:839` (lexical_call_candidate).
- is_name: `src/handler.c:842` (lexical_call_candidate).
- do_heal: `src/healer.c:82` (lexical_call_candidate).
- do_heal: `src/healer.c:90` (lexical_call_candidate).
- do_heal: `src/healer.c:98` (lexical_call_candidate).
- do_heal: `src/healer.c:106` (lexical_call_candidate).
- do_heal: `src/healer.c:114` (lexical_call_candidate).
- do_heal: `src/healer.c:122` (lexical_call_candidate).
- do_heal: `src/healer.c:130` (lexical_call_candidate).
- do_heal: `src/healer.c:138` (lexical_call_candidate).
- do_heal: `src/healer.c:138` (lexical_call_candidate).
- do_heal: `src/healer.c:146` (lexical_call_candidate).
- do_heal: `src/healer.c:146` (lexical_call_candidate).
- do_heal: `src/healer.c:155` (lexical_call_candidate).
- do_heal: `src/healer.c:155` (lexical_call_candidate).
- interpret: `src/interp.c:424` (lexical_call_candidate).
- check_social: `src/interp.c:539` (lexical_call_candidate).
- flag_lookup: `src/lookup.c:45` (lexical_call_candidate).
- clan_lookup: `src/lookup.c:59` (lexical_call_candidate).
- position_lookup: `src/lookup.c:73` (lexical_call_candidate).
- sex_lookup: `src/lookup.c:87` (lexical_call_candidate).
- size_lookup: `src/lookup.c:101` (lexical_call_candidate).
- skill_lookup: `src/magic.c:65` (lexical_call_candidate).
- find_spell: `src/magic.c:85` (lexical_call_candidate).
- say_spell: `src/magic.c:186` (lexical_call_candidate).
- do_play: `src/music.c:270` (lexical_call_candidate).
- do_play: `src/music.c:274` (lexical_call_candidate).
- do_play: `src/music.c:316` (lexical_call_candidate).
- parse_note: `src/note.c:583` (lexical_call_candidate).
- parse_note: `src/note.c:593` (lexical_call_candidate).
- parse_note: `src/note.c:655` (lexical_call_candidate).
- parse_note: `src/note.c:693` (lexical_call_candidate).
- parse_note: `src/note.c:718` (lexical_call_candidate).
- parse_note: `src/note.c:743` (lexical_call_candidate).
- parse_note: `src/note.c:849` (lexical_call_candidate).
- parse_note: `src/note.c:865` (lexical_call_candidate).
- parse_note: `src/note.c:880` (lexical_call_candidate).
- parse_note: `src/note.c:892` (lexical_call_candidate).
- parse_note: `src/note.c:916` (lexical_call_candidate).
- parse_note: `src/note.c:916` (lexical_call_candidate).
- do_gain: `src/skills.c:75` (lexical_call_candidate).
- do_gain: `src/skills.c:132` (lexical_call_candidate).
- do_gain: `src/skills.c:148` (lexical_call_candidate).
- do_spells: `src/skills.c:272` (lexical_call_candidate).
- do_skills: `src/skills.c:392` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:671` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:683` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:802` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:808` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:814` (lexical_call_candidate).
- parse_gen_groups: `src/skills.c:820` (lexical_call_candidate).
- group_lookup: `src/skills.c:973` (lexical_call_candidate).
- spec_lookup: `src/special.c:106` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2151` (declaration_or_dispatch_reference).

Dependencies: `bug`, `LOWER`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.str_prefix.if.001` | 3166 | `if ( astr == NULL )` |  | pending |
| `db.str_prefix.return.001` | 3169 | `return TRUE;` |  | pending |
| `db.str_prefix.if.002` | 3172 | `if ( bstr == NULL )` |  | pending |
| `db.str_prefix.return.002` | 3175 | `return TRUE;` |  | pending |
| `db.str_prefix.for.001` | 3178 | `for ( ; *astr; astr++, bstr++ )` |  | pending |
| `db.str_prefix.if.003` | 3180 | `if ( LOWER(*astr) != LOWER(*bstr) )` |  | pending |
| `db.str_prefix.return.003` | 3181 | `return TRUE;` |  | pending |
| `db.str_prefix.return.004` | 3184 | `return FALSE;` |  | pending |
| `db.str_prefix.empty-prefix.path` | 3164 | `empty prefix` | db.str_prefix.empty-prefix | specified |
| `db.str_prefix.both-empty.path` | 3164 | `both empty` | db.str_prefix.both-empty | specified |
| `db.str_prefix.ascii-case-prefix.path` | 3164 | `ascii case prefix` | db.str_prefix.ascii-case-prefix | specified |
| `db.str_prefix.equal.path` | 3164 | `equal` | db.str_prefix.equal | specified |
| `db.str_prefix.longer-than-candidate.path` | 3164 | `longer than candidate` | db.str_prefix.longer-than-candidate | specified |
| `db.str_prefix.first-mismatch.path` | 3164 | `first mismatch` | db.str_prefix.first-mismatch | specified |
| `db.str_prefix.null-left.path` | 3166 | `null left` | db.str_prefix.null-left | specified |
| `db.str_prefix.null-right.path` | 3172 | `null right` | db.str_prefix.null-right | specified |
| `db.str_prefix.both-null-left-dominates.path` | 3166 | `both null left dominates` | db.str_prefix.both-null-left-dominates | specified |

## str_infix

[Source line 3194](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3194); ends at line 3214. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/merc.h:2152` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `strlen`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.str_infix.if.001` | 3201 | `if ( ( c0 = LOWER(astr[0]) ) == '\0' )` |  | pending |
| `db.str_infix.return.001` | 3202 | `return FALSE;` |  | pending |
| `db.str_infix.for.001` | 3207 | `for ( ichar = 0; ichar <= sstr2 - sstr1; ichar++ )` |  | pending |
| `db.str_infix.if.002` | 3209 | `if ( c0 == LOWER(bstr[ichar]) && !str_prefix( astr, bstr + ichar ) )` |  | pending |
| `db.str_infix.and.001` | 3209 | `&& !str_prefix( astr, bstr + ichar ) )` |  | pending |
| `db.str_infix.return.002` | 3210 | `return FALSE;` |  | pending |
| `db.str_infix.return.003` | 3213 | `return TRUE;` |  | pending |
| `db.str_infix.empty-needle.path` | 3194 | `empty needle` | db.str_infix.empty-needle | specified |
| `db.str_infix.longer-needle.path` | 3194 | `longer needle` | db.str_infix.longer-needle | specified |
| `db.str_infix.interior-case-insensitive.path` | 3194 | `interior case insensitive` | db.str_infix.interior-case-insensitive | specified |
| `db.str_infix.end-match.path` | 3194 | `end match` | db.str_infix.end-match | specified |
| `db.str_infix.no-match.path` | 3194 | `no match` | db.str_infix.no-match | specified |

## str_suffix

[Source line 3223](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3223); ends at line 3234. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_prompt: `src/act_info.c:889` (lexical_call_candidate).
- check_ban: `src/ban.c:124` (lexical_call_candidate).
- check_parse_name: `src/comm.c:2163` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2153` (declaration_or_dispatch_reference).

Dependencies: `strlen`, `str_cmp`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.str_suffix.if.001` | 3230 | `if ( sstr1 <= sstr2 && !str_cmp( astr, bstr + sstr2 - sstr1 ) )` |  | pending |
| `db.str_suffix.and.001` | 3230 | `&& !str_cmp( astr, bstr + sstr2 - sstr1 ) )` |  | pending |
| `db.str_suffix.return.001` | 3231 | `return FALSE;` |  | pending |
| `db.str_suffix.return.002` | 3233 | `return TRUE;` |  | pending |
| `db.str_suffix.empty-suffix.path` | 3223 | `empty suffix` | db.str_suffix.empty-suffix | specified |
| `db.str_suffix.case-suffix.path` | 3223 | `case suffix` | db.str_suffix.case-suffix | specified |
| `db.str_suffix.equal.path` | 3223 | `equal` | db.str_suffix.equal | specified |
| `db.str_suffix.longer.path` | 3223 | `longer` | db.str_suffix.longer | specified |
| `db.str_suffix.wrong-suffix.path` | 3223 | `wrong suffix` | db.str_suffix.wrong-suffix | specified |

## capitalize

[Source line 3241](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3241); ends at line 3251. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_delete: `src/act_comm.c:68` (lexical_call_candidate).
- do_group: `src/act_comm.c:1722` (lexical_call_candidate).
- do_exits: `src/act_info.c:1355` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:222` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:225` (lexical_call_candidate).
- check_ban: `src/ban.c:110` (lexical_call_candidate).
- check_parse_name: `src/comm.c:2162` (lexical_call_candidate).
- do_play: `src/music.c:262` (lexical_call_candidate).
- save_char_obj: `src/save.c:123` (lexical_call_candidate).
- save_char_obj: `src/save.c:138` (lexical_call_candidate).
- load_char_obj: `src/save.c:577` (lexical_call_candidate).
- load_char_obj: `src/save.c:586` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2154` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `UPPER`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.capitalize.for.001` | 3246 | `for ( i = 0; str[i] != '\0'; i++ )` |  | pending |
| `db.capitalize.return.001` | 3250 | `return strcap;` |  | pending |
| `db.capitalize.empty.path` | 3249 | `empty` | db.capitalize.empty | specified |
| `db.capitalize.mixed.path` | 3249 | `mixed` | db.capitalize.mixed | specified |
| `db.capitalize.nonletter-first.path` | 3249 | `nonletter first` | db.capitalize.nonletter-first | specified |

## append_file

[Source line 3257](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3257); ends at line 3279. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_bug: `src/act_comm.c:1368` (lexical_call_candidate).
- do_typo: `src/act_comm.c:1375` (lexical_call_candidate).
- do_shutdown: `src/act_wiz.c:2046` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2155` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `fclose`, `fopen`, `perror`, `send_to_char`, `fprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.append_file.if.001` | 3261 | `if ( IS_NPC(ch) \|\| str[0] == '\0' )` |  | pending |
| `db.append_file.or.001` | 3261 | `\|\| str[0] == '\0' )` |  | pending |
| `db.append_file.return.001` | 3262 | `return;` |  | pending |
| `db.append_file.if.002` | 3265 | `if ( ( fp = fopen( file, "a" ) ) == NULL )` |  | pending |
| `db.append_file.ternary.001` | 3273 | `? ch->in_room->vnum : 0, ch->name, str );` |  | pending |
| `db.append_file.return.002` | 3278 | `return;` |  | pending |

## bug

[Source line 3286](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3286); ends at line 3336. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- add_follower: `src/act_comm.c:1521` (lexical_call_candidate).
- stop_follower: `src/act_comm.c:1542` (lexical_call_candidate).
- set_title: `src/act_info.c:2370` (lexical_call_candidate).
- move_char: `src/act_move.c:75` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1183` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1198` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1424` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1453` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1566` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:1975` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:2000` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2537` (lexical_call_candidate).
- do_list: `src/act_obj.c:2762` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:593` (lexical_call_candidate).
- close_socket: `src/comm.c:1019` (lexical_call_candidate).
- write_to_buffer: `src/comm.c:1487` (lexical_call_candidate).
- nanny: `src/comm.c:1563` (lexical_call_candidate).
- act_new: `src/comm.c:2463` (lexical_call_candidate).
- act_new: `src/comm.c:2500` (lexical_call_candidate).
- act_new: `src/comm.c:2507` (lexical_call_candidate).
- boot_db: `src/db.c:242` (lexical_call_candidate).
- boot_db: `src/db.c:341` (lexical_call_candidate).
- boot_db: `src/db.c:361` (lexical_call_candidate).
- load_old_mob: `src/db.c:478` (lexical_call_candidate).
- load_old_mob: `src/db.c:489` (lexical_call_candidate).
- load_old_mob: `src/db.c:572` (lexical_call_candidate).
- load_old_obj: `src/db.c:602` (lexical_call_candidate).
- load_old_obj: `src/db.c:613` (lexical_call_candidate).
- load_resets: `src/db.c:745` (lexical_call_candidate).
- load_resets: `src/db.c:783` (lexical_call_candidate).
- load_resets: `src/db.c:818` (lexical_call_candidate).
- load_resets: `src/db.c:824` (lexical_call_candidate).
- load_resets: `src/db.c:835` (lexical_call_candidate).
- load_rooms: `src/db.c:866` (lexical_call_candidate).
- load_rooms: `src/db.c:880` (lexical_call_candidate).
- load_rooms: `src/db.c:891` (lexical_call_candidate).
- load_rooms: `src/db.c:936` (lexical_call_candidate).
- load_rooms: `src/db.c:951` (lexical_call_candidate).
- load_rooms: `src/db.c:992` (lexical_call_candidate).
- load_rooms: `src/db.c:1001` (lexical_call_candidate).
- load_specials: `src/db.c:1070` (lexical_call_candidate).
- load_specials: `src/db.c:1084` (lexical_call_candidate).
- fix_exits: `src/db.c:1158` (lexical_call_candidate).
- reset_area: `src/db.c:1237` (lexical_call_candidate).
- reset_area: `src/db.c:1243` (lexical_call_candidate).
- reset_area: `src/db.c:1249` (lexical_call_candidate).
- reset_area: `src/db.c:1298` (lexical_call_candidate).
- reset_area: `src/db.c:1304` (lexical_call_candidate).
- reset_area: `src/db.c:1325` (lexical_call_candidate).
- reset_area: `src/db.c:1331` (lexical_call_candidate).
- reset_area: `src/db.c:1370` (lexical_call_candidate).
- reset_area: `src/db.c:1379` (lexical_call_candidate).
- reset_area: `src/db.c:1457` (lexical_call_candidate).
- reset_area: `src/db.c:1488` (lexical_call_candidate).
- create_mobile: `src/db.c:1526` (lexical_call_candidate).
- create_object: `src/db.c:1832` (lexical_call_candidate).
- create_object: `src/db.c:1874` (lexical_call_candidate).
- get_mob_index: `src/db.c:2082` (lexical_call_candidate).
- get_obj_index: `src/db.c:2109` (lexical_call_candidate).
- get_room_index: `src/db.c:2136` (lexical_call_candidate).
- fread_number: `src/db.c:2193` (lexical_call_candidate).
- fread_string: `src/db.c:2301` (lexical_call_candidate).
- fread_string: `src/db.c:2334` (lexical_call_candidate).
- fread_string_eol: `src/db.c:2413` (lexical_call_candidate).
- fread_string_eol: `src/db.c:2441` (lexical_call_candidate).
- fread_word: `src/db.c:2559` (lexical_call_candidate).
- alloc_mem: `src/db.c:2584` (lexical_call_candidate).
- free_mem: `src/db.c:2621` (lexical_call_candidate).
- free_mem: `src/db.c:2622` (lexical_call_candidate).
- free_mem: `src/db.c:2637` (lexical_call_candidate).
- alloc_perm: `src/db.c:2663` (lexical_call_candidate).
- str_cmp: `src/db.c:3138` (lexical_call_candidate).
- str_cmp: `src/db.c:3144` (lexical_call_candidate).
- str_prefix: `src/db.c:3168` (lexical_call_candidate).
- str_prefix: `src/db.c:3174` (lexical_call_candidate).
- load_mobiles: `src/db2.c:152` (lexical_call_candidate).
- load_mobiles: `src/db2.c:163` (lexical_call_candidate).
- load_mobiles: `src/db2.c:275` (lexical_call_candidate).
- load_objects: `src/db2.c:312` (lexical_call_candidate).
- load_objects: `src/db2.c:323` (lexical_call_candidate).
- load_objects: `src/db2.c:452` (lexical_call_candidate).
- damage: `src/fight.c:689` (lexical_call_candidate).
- check_killer: `src/fight.c:1222` (lexical_call_candidate).
- set_fighting: `src/fight.c:1387` (lexical_call_candidate).
- group_gain: `src/fight.c:1722` (lexical_call_candidate).
- dam_message: `src/fight.c:2031` (lexical_call_candidate).
- get_skill: `src/handler.c:363` (lexical_call_candidate).
- affect_modify: `src/handler.c:945` (lexical_call_candidate).
- affect_remove: `src/handler.c:1160` (lexical_call_candidate).
- affect_remove: `src/handler.c:1187` (lexical_call_candidate).
- affect_remove_obj: `src/handler.c:1203` (lexical_call_candidate).
- affect_remove_obj: `src/handler.c:1245` (lexical_call_candidate).
- char_from_room: `src/handler.c:1333` (lexical_call_candidate).
- char_from_room: `src/handler.c:1364` (lexical_call_candidate).
- char_to_room: `src/handler.c:1386` (lexical_call_candidate).
- obj_from_char: `src/handler.c:1485` (lexical_call_candidate).
- obj_from_char: `src/handler.c:1510` (lexical_call_candidate).
- equip_char: `src/handler.c:1584` (lexical_call_candidate).
- unequip_char: `src/handler.c:1638` (lexical_call_candidate).
- unequip_char: `src/handler.c:1671` (lexical_call_candidate).
- unequip_char: `src/handler.c:1679` (lexical_call_candidate).
- unequip_char: `src/handler.c:1680` (lexical_call_candidate).
- obj_from_room: `src/handler.c:1733` (lexical_call_candidate).
- obj_from_room: `src/handler.c:1760` (lexical_call_candidate).
- obj_from_obj: `src/handler.c:1824` (lexical_call_candidate).
- obj_from_obj: `src/handler.c:1847` (lexical_call_candidate).
- extract_obj: `src/handler.c:1910` (lexical_call_candidate).
- extract_char: `src/handler.c:1998` (lexical_call_candidate).
- deduct_cost: `src/handler.c:2236` (lexical_call_candidate).
- deduct_cost: `src/handler.c:2241` (lexical_call_candidate).
- create_money: `src/handler.c:2255` (lexical_call_candidate).
- affect_loc_name: `src/handler.c:2574` (lexical_call_candidate).
- slot_lookup: `src/magic.c:119` (lexical_call_candidate).
- do_cast: `src/magic.c:356` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:593` (lexical_call_candidate).
- obj_cast_spell: `src/magic.c:600` (lexical_call_candidate).
- load_songs: `src/music.c:170` (lexical_call_candidate).
- load_songs: `src/music.c:208` (lexical_call_candidate).
- load_thread: `src/note.c:279` (lexical_call_candidate).
- note_remove: `src/note.c:457` (lexical_call_candidate).
- new_buf_size: `src/recycle.c:562` (lexical_call_candidate).
- add_buf: `src/recycle.c:611` (lexical_call_candidate).
- save_char_obj: `src/save.c:126` (lexical_call_candidate).
- save_char_obj: `src/save.c:141` (lexical_call_candidate).
- load_char_obj: `src/save.c:609` (lexical_call_candidate).
- load_char_obj: `src/save.c:621` (lexical_call_candidate).
- fread_char: `src/save.c:817` (lexical_call_candidate).
- fread_char: `src/save.c:841` (lexical_call_candidate).
- fread_char: `src/save.c:950` (lexical_call_candidate).
- fread_char: `src/save.c:1071` (lexical_call_candidate).
- fread_char: `src/save.c:1123` (lexical_call_candidate).
- fread_pet: `src/save.c:1147` (lexical_call_candidate).
- fread_pet: `src/save.c:1155` (lexical_call_candidate).
- fread_pet: `src/save.c:1195` (lexical_call_candidate).
- fread_pet: `src/save.c:1219` (lexical_call_candidate).
- fread_pet: `src/save.c:1335` (lexical_call_candidate).
- fread_obj: `src/save.c:1372` (lexical_call_candidate).
- fread_obj: `src/save.c:1419` (lexical_call_candidate).
- fread_obj: `src/save.c:1442` (lexical_call_candidate).
- fread_obj: `src/save.c:1498` (lexical_call_candidate).
- fread_obj: `src/save.c:1555` (lexical_call_candidate).
- fread_obj: `src/save.c:1589` (lexical_call_candidate).
- fread_obj: `src/save.c:1593` (lexical_call_candidate).
- fread_obj: `src/save.c:1640` (lexical_call_candidate).
- fread_obj: `src/save.c:1661` (lexical_call_candidate).
- weather_update: `src/update.c:534` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2156` (declaration_or_dispatch_reference).

Dependencies: `ftell`, `fseek`, `getc`, `sprintf`, `log_string`, `strcpy`, `strlen`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.bug.if.001` | 3290 | `if ( fpArea != NULL )` |  | pending |
| `db.bug.if.002` | 3295 | `if ( fpArea == stdin )` |  | pending |
| `db.bug.for.001` | 3303 | `for ( iLine = 0; ftell( fpArea ) < iChar; iLine++ )` |  | pending |
| `db.bug.while.001` | 3305 | `while ( getc( fpArea ) != '\n' )` |  | pending |
| `db.bug.return.001` | 3335 | `return;` |  | pending |

## log_string

[Source line 3343](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3343); ends at line 3351. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_quit: `src/act_comm.c:1418` (lexical_call_candidate).
- main: `src/comm.c:411` (lexical_call_candidate).
- main: `src/comm.c:419` (lexical_call_candidate).
- main: `src/comm.c:427` (lexical_call_candidate).
- init_descriptor: `src/comm.c:917` (lexical_call_candidate).
- close_socket: `src/comm.c:988` (lexical_call_candidate).
- read_from_descriptor: `src/comm.c:1045` (lexical_call_candidate).
- read_from_descriptor: `src/comm.c:1083` (lexical_call_candidate).
- read_from_buffer: `src/comm.c:1173` (lexical_call_candidate).
- nanny: `src/comm.c:1587` (lexical_call_candidate).
- nanny: `src/comm.c:1668` (lexical_call_candidate).
- nanny: `src/comm.c:1909` (lexical_call_candidate).
- check_reconnect: `src/comm.c:2273` (lexical_call_candidate).
- bug: `src/db.c:3312` (lexical_call_candidate).
- bug: `src/db.c:3324` (lexical_call_candidate).
- damage: `src/fight.c:874` (lexical_call_candidate).
- interpret: `src/interp.c:444` (lexical_call_candidate).
- fread_char: `src/save.c:738` (lexical_call_candidate).
- gain_exp: `src/update.c:132` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2157` (declaration_or_dispatch_reference).

Dependencies: `ctime`, `strlen`, `fprintf`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.log_string.return.001` | 3350 | `return;` |  | pending |

## tail_chain

[Source line 3369](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3369); ends at line 3372. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- one_hit: `src/fight.c:507` (lexical_call_candidate).
- one_hit: `src/fight.c:667` (lexical_call_candidate).
- damage: `src/fight.c:986` (lexical_call_candidate).
- interpret: `src/interp.c:509` (lexical_call_candidate).
- update_handler: `src/update.c:1125` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2158` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `db.tail_chain.return.001` | 3371 | `return;` |  | pending |

## Preprocessor and macro inventory

- Line 28: `#include <stdio.h>` — pending configuration/reachability review.
- Line 29: `#include <string.h>` — pending configuration/reachability review.
- Line 30: `#include <stdlib.h>` — pending configuration/reachability review.
- Line 31: `#include <ctype.h>` — pending configuration/reachability review.
- Line 32: `#include <time.h>` — pending configuration/reachability review.
- Line 33: `#if defined(macintosh)` — pending configuration/reachability review.
- Line 34: `#include <types.h>` — pending configuration/reachability review.
- Line 35: `#else` — pending configuration/reachability review.
- Line 36: `#include <sys/types.h>` — pending configuration/reachability review.
- Line 37: `#include <sys/time.h>` — pending configuration/reachability review.
- Line 38: `#include <sys/resource.h>` — pending configuration/reachability review.
- Line 39: `#endif` — pending configuration/reachability review.
- Line 41: `#include "merc.h"` — pending configuration/reachability review.
- Line 42: `#include "db.h"` — pending configuration/reachability review.
- Line 43: `#include "recycle.h"` — pending configuration/reachability review.
- Line 44: `#include "music.h"` — pending configuration/reachability review.
- Line 45: `#include "lookup.h"` — pending configuration/reachability review.
- Line 48: `#if !defined(macintosh)` — pending configuration/reachability review.
- Line 50: `#endif` — pending configuration/reachability review.
- Line 52: `#if !defined(OLD_RAND)` — pending configuration/reachability review.
- Line 53: `#if !defined(linux)` — pending configuration/reachability review.
- Line 55: `#endif` — pending configuration/reachability review.
- Line 59: `#endif` — pending configuration/reachability review.
- Line 182: `#define			MAX_STRING	1413120` — pending configuration/reachability review.
- Line 183: `#define			MAX_PERM_BLOCK	131072` — pending configuration/reachability review.
- Line 184: `#define			MAX_MEM_LIST	11` — pending configuration/reachability review.
- Line 3023: `#if defined (OLD_RAND)` — pending configuration/reachability review.
- Line 3025: `#endif` — pending configuration/reachability review.
- Line 3029: `#if defined (OLD_RAND)` — pending configuration/reachability review.
- Line 3045: `#else` — pending configuration/reachability review.
- Line 3047: `#endif` — pending configuration/reachability review.
- Line 3055: `#if defined (OLD_RAND)` — pending configuration/reachability review.
- Line 3074: `#else` — pending configuration/reachability review.
- Line 3076: `#endif` — pending configuration/reachability review.

## Static tables

- `rgSizeList` at line 187 — pending entry/termination review.

## Commented code candidates

- Lines 3313–3319: disabled inside block comment; content hash `60021261b381a2ca530553a900782930d30f9156cc440925f21c074974e23f50`.
- Lines 3325–3333: disabled inside block comment; content hash `2e07fa9cbc7107d89ac14b7127deda49ab47a7731c513612e0519d30bd546b87`.

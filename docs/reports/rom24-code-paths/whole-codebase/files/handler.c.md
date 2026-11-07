# src/handler.c

Role: translation_unit. Disposition: **partially_specified**. SHA-256: `0e95a3bd6480448855bba8d7cae6b6f8b5aad3d2be2738a21cd58571f7bf2261`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## is_friend

[Source line 50](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:50); ends at line 91. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):


Dependencies: `is_same_group`, `IS_NPC`, `IS_SET`, `IS_AFFECTED`, `IS_GOOD`, `IS_EVIL`, `IS_NEUTRAL`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.is_friend.if.001` | 52 | `if (is_same_group(ch,victim))` |  | pending |
| `handler.is_friend.return.001` | 53 | `return TRUE;` |  | pending |
| `handler.is_friend.if.002` | 56 | `if (!IS_NPC(ch))` |  | pending |
| `handler.is_friend.return.002` | 57 | `return FALSE;` |  | pending |
| `handler.is_friend.if.003` | 59 | `if (!IS_NPC(victim))` |  | pending |
| `handler.is_friend.if.004` | 61 | `if (IS_SET(ch->off_flags,ASSIST_PLAYERS))` |  | pending |
| `handler.is_friend.return.003` | 62 | `return TRUE;` |  | pending |
| `handler.is_friend.return.004` | 64 | `return FALSE;` |  | pending |
| `handler.is_friend.if.005` | 67 | `if (IS_AFFECTED(ch,AFF_CHARM))` |  | pending |
| `handler.is_friend.return.005` | 68 | `return FALSE;` |  | pending |
| `handler.is_friend.if.006` | 70 | `if (IS_SET(ch->off_flags,ASSIST_ALL))` |  | pending |
| `handler.is_friend.return.006` | 71 | `return TRUE;` |  | pending |
| `handler.is_friend.if.007` | 73 | `if (ch->group && ch->group == victim->group)` |  | pending |
| `handler.is_friend.and.001` | 73 | `&& ch->group == victim->group)` |  | pending |
| `handler.is_friend.return.007` | 74 | `return TRUE;` |  | pending |
| `handler.is_friend.if.008` | 76 | `if (IS_SET(ch->off_flags,ASSIST_VNUM)      &&  ch->pIndexData == victim->pIndexData)` |  | pending |
| `handler.is_friend.and.002` | 77 | `&&  ch->pIndexData == victim->pIndexData)` |  | pending |
| `handler.is_friend.return.008` | 78 | `return TRUE;` |  | pending |
| `handler.is_friend.if.009` | 80 | `if (IS_SET(ch->off_flags,ASSIST_RACE) && ch->race == victim->race)` |  | pending |
| `handler.is_friend.and.003` | 80 | `&& ch->race == victim->race)` |  | pending |
| `handler.is_friend.return.009` | 81 | `return TRUE;` |  | pending |
| `handler.is_friend.if.010` | 83 | `if (IS_SET(ch->off_flags,ASSIST_ALIGN)     &&  !IS_SET(ch->act,ACT_NOALIGN) && !IS_SET(victim->act,ACT_NOALIGN)     &&  ((IS_GOOD(ch) && IS_GOOD(victim))     \|\|	 (IS_EVIL(ch) && IS_EVIL(victim))     \|\|   (IS_NEUTRAL(ch) && IS_NEUTRAL(victim))))` |  | pending |
| `handler.is_friend.and.004` | 84 | `&&  !IS_SET(ch->act,ACT_NOALIGN) && !IS_SET(victim->act,ACT_NOALIGN)` |  | pending |
| `handler.is_friend.and.005` | 84 | `&& !IS_SET(victim->act,ACT_NOALIGN)` |  | pending |
| `handler.is_friend.and.006` | 85 | `&&  ((IS_GOOD(ch) && IS_GOOD(victim))` |  | pending |
| `handler.is_friend.and.007` | 85 | `&& IS_GOOD(victim))` |  | pending |
| `handler.is_friend.or.001` | 86 | `\|\|	 (IS_EVIL(ch) && IS_EVIL(victim))` |  | pending |
| `handler.is_friend.and.008` | 86 | `&& IS_EVIL(victim))` |  | pending |
| `handler.is_friend.or.002` | 87 | `\|\|   (IS_NEUTRAL(ch) && IS_NEUTRAL(victim))))` |  | pending |
| `handler.is_friend.and.009` | 87 | `&& IS_NEUTRAL(victim))))` |  | pending |
| `handler.is_friend.return.010` | 88 | `return TRUE;` |  | pending |
| `handler.is_friend.return.011` | 90 | `return FALSE;` |  | pending |

## count_users

[Source line 94](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:94); ends at line 107. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_stand: `src/act_move.c:896` (lexical_call_candidate).
- do_rest: `src/act_move.c:1008` (lexical_call_candidate).
- do_sit: `src/act_move.c:1143` (lexical_call_candidate).
- do_sleep: `src/act_move.c:1270` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2184` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.count_users.if.001` | 99 | `if (obj->in_room == NULL)` |  | pending |
| `handler.count_users.return.001` | 100 | `return 0;` |  | pending |
| `handler.count_users.for.001` | 102 | `for (fch = obj->in_room->people; fch != NULL; fch = fch->next_in_room)` |  | pending |
| `handler.count_users.if.002` | 103 | `if (fch->on == obj)` |  | pending |
| `handler.count_users.return.002` | 106 | `return count;` |  | pending |

## material_lookup

[Source line 110](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:110); ends at line 113. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/merc.h:2189` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.material_lookup.return.001` | 112 | `return 0;` |  | pending |

## race_lookup

[Source line 116](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:116); ends at line 128. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_who: `src/act_info.c:1964` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3663` (lexical_call_candidate).
- nanny: `src/comm.c:1824` (lexical_call_candidate).
- load_old_mob: `src/db.c:546` (lexical_call_candidate).
- load_old_mob: `src/db.c:549` (lexical_call_candidate).
- load_mobiles: `src/db2.c:176` (lexical_call_candidate).
- get_curr_stat: `src/handler.c:744` (lexical_call_candidate).
- get_max_train: `src/handler.c:763` (lexical_call_candidate).
- load_char_obj: `src/save.c:556` (lexical_call_candidate).
- load_char_obj: `src/save.c:637` (lexical_call_candidate).
- fread_char: `src/save.c:1035` (lexical_call_candidate).
- fread_pet: `src/save.c:1323` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2196` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.race_lookup.for.001` | 120 | `for ( race = 0; race_table[race].name != NULL; race++)` |  | pending |
| `handler.race_lookup.if.001` | 122 | `if (LOWER(name[0]) == LOWER(race_table[race].name[0]) 	&&  !str_prefix( name,race_table[race].name))` |  | pending |
| `handler.race_lookup.and.001` | 123 | `&&  !str_prefix( name,race_table[race].name))` |  | pending |
| `handler.race_lookup.return.001` | 124 | `return race;` |  | pending |
| `handler.race_lookup.return.002` | 127 | `return 0;` |  | pending |

## liq_lookup

[Source line 130](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:130); ends at line 142. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_objects: `src/db2.c:361` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2188` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.liq_lookup.for.001` | 134 | `for ( liq = 0; liq_table[liq].liq_name != NULL; liq++)` |  | pending |
| `handler.liq_lookup.if.001` | 136 | `if (LOWER(name[0]) == LOWER(liq_table[liq].liq_name[0]) 	&& !str_prefix(name,liq_table[liq].liq_name))` |  | pending |
| `handler.liq_lookup.and.001` | 137 | `&& !str_prefix(name,liq_table[liq].liq_name))` |  | pending |
| `handler.liq_lookup.return.001` | 138 | `return liq;` |  | pending |
| `handler.liq_lookup.return.002` | 141 | `return -1;` |  | pending |

## weapon_lookup

[Source line 144](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:144); ends at line 156. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1980` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2190` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.weapon_lookup.for.001` | 148 | `for (type = 0; weapon_table[type].name != NULL; type++)` |  | pending |
| `handler.weapon_lookup.if.001` | 150 | `if (LOWER(name[0]) == LOWER(weapon_table[type].name[0]) 	&&  !str_prefix(name,weapon_table[type].name))` |  | pending |
| `handler.weapon_lookup.and.001` | 151 | `&&  !str_prefix(name,weapon_table[type].name))` |  | pending |
| `handler.weapon_lookup.return.001` | 152 | `return type;` |  | pending |
| `handler.weapon_lookup.return.002` | 155 | `return -1;` |  | pending |

## weapon_type

[Source line 158](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:158); ends at line 170. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_objects: `src/db2.c:344` (lexical_call_candidate).
- weapon_name: `src/handler.c:202` (function_symbol_reference_candidate).
- declaration_or_dispatch_reference: `src/const.c:77` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:380` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:1890` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2191` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.weapon_type.for.001` | 162 | `for (type = 0; weapon_table[type].name != NULL; type++)` |  | pending |
| `handler.weapon_type.if.001` | 164 | `if (LOWER(name[0]) == LOWER(weapon_table[type].name[0])         &&  !str_prefix(name,weapon_table[type].name))` |  | pending |
| `handler.weapon_type.and.001` | 165 | `&&  !str_prefix(name,weapon_table[type].name))` |  | pending |
| `handler.weapon_type.return.001` | 166 | `return weapon_table[type].type;` |  | pending |
| `handler.weapon_type.return.002` | 169 | `return WEAPON_EXOTIC;` |  | pending |

## item_lookup

[Source line 173](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:173); ends at line 185. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_objects: `src/db2.c:338` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2193` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.item_lookup.for.001` | 177 | `for (type = 0; item_table[type].name != NULL; type++)` |  | pending |
| `handler.item_lookup.if.001` | 179 | `if (LOWER(name[0]) == LOWER(item_table[type].name[0])         &&  !str_prefix(name,item_table[type].name))` |  | pending |
| `handler.item_lookup.and.001` | 180 | `&&  !str_prefix(name,item_table[type].name))` |  | pending |
| `handler.item_lookup.return.001` | 181 | `return item_table[type].type;` |  | pending |
| `handler.item_lookup.return.002` | 184 | `return -1;` |  | pending |

## item_name

[Source line 187](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:187); ends at line 195. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_ostat: `src/act_wiz.c:1231` (lexical_call_candidate).
- spell_identify: `src/magic.c:3239` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2194` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.item_name.for.001` | 191 | `for (type = 0; item_table[type].name != NULL; type++)` |  | pending |
| `handler.item_name.if.001` | 192 | `if (item_type == item_table[type].type)` |  | pending |
| `handler.item_name.return.001` | 193 | `return item_table[type].name;` |  | pending |
| `handler.item_name.return.002` | 194 | `return "none";` |  | pending |

## weapon_name

[Source line 197](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:197); ends at line 205. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/merc.h:2192` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.weapon_name.for.001` | 201 | `for (type = 0; weapon_table[type].name != NULL; type++)` |  | pending |
| `handler.weapon_name.if.001` | 202 | `if (weapon_type == weapon_table[type].type)` |  | pending |
| `handler.weapon_name.return.001` | 203 | `return weapon_table[type].name;` |  | pending |
| `handler.weapon_name.return.002` | 204 | `return "exotic";` |  | pending |

## attack_lookup

[Source line 207](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:207); ends at line 219. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_mobiles: `src/db2.c:212` (lexical_call_candidate).
- load_objects: `src/db2.c:347` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2195` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.attack_lookup.for.001` | 211 | `for ( att = 0; attack_table[att].name != NULL; att++)` |  | pending |
| `handler.attack_lookup.if.001` | 213 | `if (LOWER(name[0]) == LOWER(attack_table[att].name[0]) 	&&  !str_prefix(name,attack_table[att].name))` |  | pending |
| `handler.attack_lookup.and.001` | 214 | `&&  !str_prefix(name,attack_table[att].name))` |  | pending |
| `handler.attack_lookup.return.001` | 215 | `return att;` |  | pending |
| `handler.attack_lookup.return.002` | 218 | `return 0;` |  | pending |

## wiznet_lookup

[Source line 222](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:222); ends at line 234. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_wiznet: `src/act_wiz.c:126` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2197` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.wiznet_lookup.for.001` | 226 | `for (flag = 0; wiznet_table[flag].name != NULL; flag++)` |  | pending |
| `handler.wiznet_lookup.if.001` | 228 | `if (LOWER(name[0]) == LOWER(wiznet_table[flag].name[0]) 	&& !str_prefix(name,wiznet_table[flag].name))` |  | pending |
| `handler.wiznet_lookup.and.001` | 229 | `&& !str_prefix(name,wiznet_table[flag].name))` |  | pending |
| `handler.wiznet_lookup.return.001` | 230 | `return flag;` |  | pending |
| `handler.wiznet_lookup.return.002` | 233 | `return -1;` |  | pending |

## class_lookup

[Source line 237](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:237); ends at line 249. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_who: `src/act_info.c:1961` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3463` (lexical_call_candidate).
- nanny: `src/comm.c:1897` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2198` (declaration_or_dispatch_reference).

Dependencies: `LOWER`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.class_lookup.for.001` | 241 | `for ( class = 0; class < MAX_CLASS; class++)` |  | pending |
| `handler.class_lookup.if.001` | 243 | `if (LOWER(name[0]) == LOWER(class_table[class].name[0])         &&  !str_prefix( name,class_table[class].name))` |  | pending |
| `handler.class_lookup.and.001` | 244 | `&&  !str_prefix( name,class_table[class].name))` |  | pending |
| `handler.class_lookup.return.001` | 245 | `return class;` |  | pending |
| `handler.class_lookup.return.002` | 248 | `return -1;` |  | pending |

## check_immune

[Source line 255](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:255); ends at line 326. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- damage: `src/fight.c:786` (lexical_call_candidate).
- saves_spell: `src/magic.c:224` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2187` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `case`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.check_immune.if.001` | 263 | `if (dam_type == DAM_NONE)` |  | pending |
| `handler.check_immune.return.001` | 264 | `return immune;` |  | pending |
| `handler.check_immune.if.002` | 266 | `if (dam_type <= 3)` |  | pending |
| `handler.check_immune.if.003` | 268 | `if (IS_SET(ch->imm_flags,IMM_WEAPON))` |  | pending |
| `handler.check_immune.if.004` | 270 | `if (IS_SET(ch->res_flags,RES_WEAPON))` |  | pending |
| `handler.check_immune.if.005` | 272 | `if (IS_SET(ch->vuln_flags,VULN_WEAPON))` |  | pending |
| `handler.check_immune.if.006` | 277 | `if (IS_SET(ch->imm_flags,IMM_MAGIC))` |  | pending |
| `handler.check_immune.if.007` | 279 | `if (IS_SET(ch->res_flags,RES_MAGIC))` |  | pending |
| `handler.check_immune.if.008` | 281 | `if (IS_SET(ch->vuln_flags,VULN_MAGIC))` |  | pending |
| `handler.check_immune.switch.001` | 286 | `switch (dam_type)` |  | pending |
| `handler.check_immune.case.001` | 288 | `case(DAM_BASH):		bit = IMM_BASH;` |  | pending |
| `handler.check_immune.break.001` | 288 | `break;` |  | pending |
| `handler.check_immune.case.002` | 289 | `case(DAM_PIERCE):	bit = IMM_PIERCE;` |  | pending |
| `handler.check_immune.break.002` | 289 | `break;` |  | pending |
| `handler.check_immune.case.003` | 290 | `case(DAM_SLASH):	bit = IMM_SLASH;` |  | pending |
| `handler.check_immune.break.003` | 290 | `break;` |  | pending |
| `handler.check_immune.case.004` | 291 | `case(DAM_FIRE):		bit = IMM_FIRE;` |  | pending |
| `handler.check_immune.break.004` | 291 | `break;` |  | pending |
| `handler.check_immune.case.005` | 292 | `case(DAM_COLD):		bit = IMM_COLD;` |  | pending |
| `handler.check_immune.break.005` | 292 | `break;` |  | pending |
| `handler.check_immune.case.006` | 293 | `case(DAM_LIGHTNING):	bit = IMM_LIGHTNING;` |  | pending |
| `handler.check_immune.break.006` | 293 | `break;` |  | pending |
| `handler.check_immune.case.007` | 294 | `case(DAM_ACID):		bit = IMM_ACID;` |  | pending |
| `handler.check_immune.break.007` | 294 | `break;` |  | pending |
| `handler.check_immune.case.008` | 295 | `case(DAM_POISON):	bit = IMM_POISON;` |  | pending |
| `handler.check_immune.break.008` | 295 | `break;` |  | pending |
| `handler.check_immune.case.009` | 296 | `case(DAM_NEGATIVE):	bit = IMM_NEGATIVE;` |  | pending |
| `handler.check_immune.break.009` | 296 | `break;` |  | pending |
| `handler.check_immune.case.010` | 297 | `case(DAM_HOLY):		bit = IMM_HOLY;` |  | pending |
| `handler.check_immune.break.010` | 297 | `break;` |  | pending |
| `handler.check_immune.case.011` | 298 | `case(DAM_ENERGY):	bit = IMM_ENERGY;` |  | pending |
| `handler.check_immune.break.011` | 298 | `break;` |  | pending |
| `handler.check_immune.case.012` | 299 | `case(DAM_MENTAL):	bit = IMM_MENTAL;` |  | pending |
| `handler.check_immune.break.012` | 299 | `break;` |  | pending |
| `handler.check_immune.case.013` | 300 | `case(DAM_DISEASE):	bit = IMM_DISEASE;` |  | pending |
| `handler.check_immune.break.013` | 300 | `break;` |  | pending |
| `handler.check_immune.case.014` | 301 | `case(DAM_DROWNING):	bit = IMM_DROWNING;` |  | pending |
| `handler.check_immune.break.014` | 301 | `break;` |  | pending |
| `handler.check_immune.case.015` | 302 | `case(DAM_LIGHT):	bit = IMM_LIGHT;` |  | pending |
| `handler.check_immune.break.015` | 302 | `break;` |  | pending |
| `handler.check_immune.case.016` | 303 | `case(DAM_CHARM):	bit = IMM_CHARM;` |  | pending |
| `handler.check_immune.break.016` | 303 | `break;` |  | pending |
| `handler.check_immune.case.017` | 304 | `case(DAM_SOUND):	bit = IMM_SOUND;` |  | pending |
| `handler.check_immune.break.017` | 304 | `break;` |  | pending |
| `handler.check_immune.default.001` | 305 | `default:		return def;` |  | pending |
| `handler.check_immune.return.002` | 305 | `return def;` |  | pending |
| `handler.check_immune.if.009` | 308 | `if (IS_SET(ch->imm_flags,bit))` |  | pending |
| `handler.check_immune.if.010` | 310 | `if (IS_SET(ch->res_flags,bit) && immune != IS_IMMUNE)` |  | pending |
| `handler.check_immune.and.001` | 310 | `&& immune != IS_IMMUNE)` |  | pending |
| `handler.check_immune.if.011` | 312 | `if (IS_SET(ch->vuln_flags,bit))` |  | pending |
| `handler.check_immune.if.012` | 314 | `if (immune == IS_IMMUNE)` |  | pending |
| `handler.check_immune.if.013` | 316 | `if (immune == IS_RESISTANT)` |  | pending |
| `handler.check_immune.if.014` | 322 | `if (immune == -1)` |  | pending |
| `handler.check_immune.return.003` | 323 | `return def;` |  | pending |
| `handler.check_immune.return.004` | 325 | `return immune;` |  | pending |

## is_clan

[Source line 328](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:328); ends at line 331. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_clantalk: `src/act_comm.c:662` (lexical_call_candidate).
- do_who: `src/act_info.c:2030` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2188` (lexical_call_candidate).
- is_safe: `src/fight.c:1070` (lexical_call_candidate).
- is_safe: `src/fight.c:1079` (lexical_call_candidate).
- is_safe_spell: `src/fight.c:1173` (lexical_call_candidate).
- is_safe_spell: `src/fight.c:1179` (lexical_call_candidate).
- check_killer: `src/fight.c:1245` (lexical_call_candidate).
- make_corpse: `src/fight.c:1454` (lexical_call_candidate).
- spell_gate: `src/magic.c:2898` (lexical_call_candidate).
- spell_portal: `src/magic2.c:74` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:127` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2199` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.is_clan.return.001` | 330 | `return ch->clan;` | handler.is_clan.clan-0, handler.is_clan.clan-1, handler.is_clan.clan-2 | specified |
| `handler.is_clan.clan-0.path` | 330 | `clan 0` | handler.is_clan.clan-0 | specified |
| `handler.is_clan.clan-1.path` | 330 | `clan 1` | handler.is_clan.clan-1 | specified |
| `handler.is_clan.clan-2.path` | 330 | `clan 2` | handler.is_clan.clan-2 | specified |

## is_same_clan

[Source line 333](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:333); ends at line 339. Status: traced.

Entry references (reviewed in the completion record):

Completed contract and caller audit: [is_same_clan completion](../same-clan-completion.md). No remaining gaps for this function.

- do_clantalk: `src/act_comm.c:697` (lexical_call_candidate).
- damage: `src/fight.c:898` (lexical_call_candidate).
- spell_gate: `src/magic.c:2898` (lexical_call_candidate).
- spell_portal: `src/magic2.c:74` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:127` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2200` (declaration_or_dispatch_reference).

Dependencies: `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.is_same_clan.if.001` | 335 | `if (clan_table[ch->clan].independent)` | handler.is_same_clan.clans-0-0, handler.is_same_clan.clans-1-1, handler.is_same_clan.clans-2-2, handler.is_same_clan.clans-2-1, handler.is_same_clan.clans-0-1, handler.is_same_clan.clans-0-2, handler.is_same_clan.clans-1-0, handler.is_same_clan.clans-1-2, handler.is_same_clan.clans-2-0, handler.is_same_clan.self-clan-0, handler.is_same_clan.self-clan-1, handler.is_same_clan.self-clan-2, handler.is_same_clan.kinds-npc-pc, handler.is_same_clan.kinds-pc-npc, handler.is_same_clan.kinds-npc-npc, handler.is_same_clan.independent-0-null-victim, handler.is_same_clan.independent-1-null-victim, handler.is_same_clan.victim-clan-outside-table--1, handler.is_same_clan.victim-clan-outside-table-3 | specified |
| `handler.is_same_clan.return.001` | 336 | `return FALSE;` | handler.is_same_clan.clans-0-0, handler.is_same_clan.clans-1-1, handler.is_same_clan.clans-0-1, handler.is_same_clan.clans-0-2, handler.is_same_clan.clans-1-0, handler.is_same_clan.clans-1-2, handler.is_same_clan.self-clan-0, handler.is_same_clan.self-clan-1, handler.is_same_clan.independent-0-null-victim, handler.is_same_clan.independent-1-null-victim | specified |
| `handler.is_same_clan.return.002` | 338 | `return (ch->clan == victim->clan);` | handler.is_same_clan.clans-2-2, handler.is_same_clan.clans-2-1, handler.is_same_clan.clans-2-0, handler.is_same_clan.self-clan-2, handler.is_same_clan.kinds-npc-pc, handler.is_same_clan.kinds-pc-npc, handler.is_same_clan.kinds-npc-npc, handler.is_same_clan.victim-clan-outside-table--1, handler.is_same_clan.victim-clan-outside-table-3 | specified |
| `handler.is_same_clan.clans-0-0.path` | 335 | `clans 0 0` | handler.is_same_clan.clans-0-0 | specified |
| `handler.is_same_clan.clans-1-1.path` | 335 | `clans 1 1` | handler.is_same_clan.clans-1-1 | specified |
| `handler.is_same_clan.clans-2-2.path` | 335 | `clans 2 2` | handler.is_same_clan.clans-2-2 | specified |
| `handler.is_same_clan.clans-2-1.path` | 335 | `clans 2 1` | handler.is_same_clan.clans-2-1 | specified |
| `handler.is_same_clan.clans-0-1.path` | 335 | `clans 0 1` | handler.is_same_clan.clans-0-1 | specified |
| `handler.is_same_clan.clans-0-2.path` | 335 | `clans 0 2` | handler.is_same_clan.clans-0-2 | specified |
| `handler.is_same_clan.clans-1-0.path` | 335 | `clans 1 0` | handler.is_same_clan.clans-1-0 | specified |
| `handler.is_same_clan.clans-1-2.path` | 335 | `clans 1 2` | handler.is_same_clan.clans-1-2 | specified |
| `handler.is_same_clan.clans-2-0.path` | 335 | `clans 2 0` | handler.is_same_clan.clans-2-0 | specified |
| `handler.is_same_clan.self-clan-0.path` | 335 | `self clan 0` | handler.is_same_clan.self-clan-0 | specified |
| `handler.is_same_clan.self-clan-1.path` | 335 | `self clan 1` | handler.is_same_clan.self-clan-1 | specified |
| `handler.is_same_clan.self-clan-2.path` | 335 | `self clan 2` | handler.is_same_clan.self-clan-2 | specified |
| `handler.is_same_clan.kinds-npc-pc.path` | 335 | `kinds npc pc` | handler.is_same_clan.kinds-npc-pc | specified |
| `handler.is_same_clan.kinds-pc-npc.path` | 335 | `kinds pc npc` | handler.is_same_clan.kinds-pc-npc | specified |
| `handler.is_same_clan.kinds-npc-npc.path` | 335 | `kinds npc npc` | handler.is_same_clan.kinds-npc-npc | specified |
| `handler.is_same_clan.independent-0-null-victim.path` | 335 | `independent 0 null victim` | handler.is_same_clan.independent-0-null-victim | specified |
| `handler.is_same_clan.independent-1-null-victim.path` | 335 | `independent 1 null victim` | handler.is_same_clan.independent-1-null-victim | specified |
| `handler.is_same_clan.victim-clan-outside-table--1.path` | 335 | `victim clan outside table  1` | handler.is_same_clan.victim-clan-outside-table--1 | specified |
| `handler.is_same_clan.victim-clan-outside-table-3.path` | 335 | `victim clan outside table 3` | handler.is_same_clan.victim-clan-outside-table-3 | specified |

## is_old_mob

[Source line 342](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:342); ends at line 349. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/merc.h:2201` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.is_old_mob.if.001` | 344 | `if (ch->pIndexData == NULL)` |  | pending |
| `handler.is_old_mob.return.001` | 345 | `return FALSE;` |  | pending |
| `handler.is_old_mob.if.002` | 346 | `if (ch->pIndexData->new_format)` |  | pending |
| `handler.is_old_mob.return.002` | 347 | `return FALSE;` |  | pending |
| `handler.is_old_mob.return.003` | 348 | `return TRUE;` |  | pending |

## get_skill

[Source line 352](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:352); ends at line 455. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_char_to_char_1: `src/act_info.c:482` (lexical_call_candidate).
- do_pick: `src/act_move.c:768` (lexical_call_candidate).
- do_sneak: `src/act_move.c:1345` (lexical_call_candidate).
- do_hide: `src/act_move.c:1372` (lexical_call_candidate).
- do_recall: `src/act_move.c:1436` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:848` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1932` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:1986` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2107` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2187` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2576` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2697` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2899` (lexical_call_candidate).
- multi_hit: `src/fight.c:220` (lexical_call_candidate).
- multi_hit: `src/fight.c:233` (lexical_call_candidate).
- mob_hit: `src/fight.c:279` (lexical_call_candidate).
- mob_hit: `src/fight.c:291` (lexical_call_candidate).
- one_hit: `src/fight.c:474` (lexical_call_candidate).
- one_hit: `src/fight.c:556` (lexical_call_candidate).
- one_hit: `src/fight.c:559` (lexical_call_candidate).
- check_parry: `src/fight.c:1270` (lexical_call_candidate).
- check_shield_block: `src/fight.c:1303` (lexical_call_candidate).
- check_dodge: `src/fight.c:1331` (lexical_call_candidate).
- do_berserk: `src/fight.c:2125` (lexical_call_candidate).
- do_bash: `src/fight.c:2216` (lexical_call_candidate).
- do_bash: `src/fight.c:2296` (lexical_call_candidate).
- do_bash: `src/fight.c:2302` (lexical_call_candidate).
- do_dirt: `src/fight.c:2347` (lexical_call_candidate).
- do_trip: `src/fight.c:2480` (lexical_call_candidate).
- do_backstab: `src/fight.c:2785` (lexical_call_candidate).
- do_backstab: `src/fight.c:2786` (lexical_call_candidate).
- do_rescue: `src/fight.c:2913` (lexical_call_candidate).
- do_kick: `src/fight.c:2958` (lexical_call_candidate).
- do_disarm: `src/fight.c:2983` (lexical_call_candidate).
- do_disarm: `src/fight.c:2990` (lexical_call_candidate).
- can_see: `src/handler.c:2475` (lexical_call_candidate).
- do_cast: `src/magic.c:539` (lexical_call_candidate).
- hit_gain: `src/update.c:176` (lexical_call_candidate).
- mana_gain: `src/update.c:242` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2202` (declaration_or_dispatch_reference).

Dependencies: `bug`, `IS_NPC`, `IS_SET`, `URANGE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_skill.if.001` | 356 | `if (sn == -1)` |  | pending |
| `handler.get_skill.if.002` | 361 | `if (sn < -1 \|\| sn > MAX_SKILL)` |  | pending |
| `handler.get_skill.or.001` | 361 | `\|\| sn > MAX_SKILL)` |  | pending |
| `handler.get_skill.if.003` | 367 | `if (!IS_NPC(ch))` |  | pending |
| `handler.get_skill.if.004` | 369 | `if (ch->level < skill_table[sn].skill_level[ch->class])` |  | pending |
| `handler.get_skill.if.005` | 379 | `if (skill_table[sn].spell_fun != spell_null)` |  | pending |
| `handler.get_skill.if.006` | 382 | `if (sn == gsn_sneak \|\| sn == gsn_hide)` |  | pending |
| `handler.get_skill.or.002` | 382 | `\|\| sn == gsn_hide)` |  | pending |
| `handler.get_skill.if.007` | 385 | `if ((sn == gsn_dodge && IS_SET(ch->off_flags,OFF_DODGE))  	\|\|       (sn == gsn_parry && IS_SET(ch->off_flags,OFF_PARRY)))` |  | pending |
| `handler.get_skill.and.001` | 385 | `&& IS_SET(ch->off_flags,OFF_DODGE))` |  | pending |
| `handler.get_skill.or.003` | 386 | `\|\|       (sn == gsn_parry && IS_SET(ch->off_flags,OFF_PARRY)))` |  | pending |
| `handler.get_skill.and.002` | 386 | `&& IS_SET(ch->off_flags,OFF_PARRY)))` |  | pending |
| `handler.get_skill.if.008` | 389 | `if (sn == gsn_shield_block)` |  | pending |
| `handler.get_skill.if.009` | 392 | `if (sn == gsn_second_attack  	&& (IS_SET(ch->act,ACT_WARRIOR) \|\| IS_SET(ch->act,ACT_THIEF)))` |  | pending |
| `handler.get_skill.and.003` | 393 | `&& (IS_SET(ch->act,ACT_WARRIOR) \|\| IS_SET(ch->act,ACT_THIEF)))` |  | pending |
| `handler.get_skill.or.004` | 393 | `\|\| IS_SET(ch->act,ACT_THIEF)))` |  | pending |
| `handler.get_skill.if.010` | 396 | `if (sn == gsn_third_attack && IS_SET(ch->act,ACT_WARRIOR))` |  | pending |
| `handler.get_skill.and.004` | 396 | `&& IS_SET(ch->act,ACT_WARRIOR))` |  | pending |
| `handler.get_skill.if.011` | 399 | `if (sn == gsn_hand_to_hand)` |  | pending |
| `handler.get_skill.if.012` | 402 | `if (sn == gsn_trip && IS_SET(ch->off_flags,OFF_TRIP))` |  | pending |
| `handler.get_skill.and.005` | 402 | `&& IS_SET(ch->off_flags,OFF_TRIP))` |  | pending |
| `handler.get_skill.if.013` | 405 | `if (sn == gsn_bash && IS_SET(ch->off_flags,OFF_BASH))` |  | pending |
| `handler.get_skill.and.006` | 405 | `&& IS_SET(ch->off_flags,OFF_BASH))` |  | pending |
| `handler.get_skill.if.014` | 408 | `if (sn == gsn_disarm  	     &&  (IS_SET(ch->off_flags,OFF_DISARM)  	     \|\|   IS_SET(ch->act,ACT_WARRIOR) 	     \|\|	  IS_SET(ch->act,ACT_THIEF)))` |  | pending |
| `handler.get_skill.and.007` | 409 | `&&  (IS_SET(ch->off_flags,OFF_DISARM)` |  | pending |
| `handler.get_skill.or.005` | 410 | `\|\|   IS_SET(ch->act,ACT_WARRIOR)` |  | pending |
| `handler.get_skill.or.006` | 411 | `\|\|	  IS_SET(ch->act,ACT_THIEF)))` |  | pending |
| `handler.get_skill.if.015` | 414 | `if (sn == gsn_berserk && IS_SET(ch->off_flags,OFF_BERSERK))` |  | pending |
| `handler.get_skill.and.008` | 414 | `&& IS_SET(ch->off_flags,OFF_BERSERK))` |  | pending |
| `handler.get_skill.if.016` | 417 | `if (sn == gsn_kick)` |  | pending |
| `handler.get_skill.if.017` | 420 | `if (sn == gsn_backstab && IS_SET(ch->act,ACT_THIEF))` |  | pending |
| `handler.get_skill.and.009` | 420 | `&& IS_SET(ch->act,ACT_THIEF))` |  | pending |
| `handler.get_skill.if.018` | 423 | `if (sn == gsn_rescue)` |  | pending |
| `handler.get_skill.if.019` | 426 | `if (sn == gsn_recall)` |  | pending |
| `handler.get_skill.if.020` | 429 | `if (sn == gsn_sword 	\|\|  sn == gsn_dagger 	\|\|  sn == gsn_spear 	\|\|  sn == gsn_mace 	\|\|  sn == gsn_axe 	\|\|  sn == gsn_flail 	\|\|  sn == gsn_whip 	\|\|  sn == gsn_polearm)` |  | pending |
| `handler.get_skill.or.007` | 430 | `\|\|  sn == gsn_dagger` |  | pending |
| `handler.get_skill.or.008` | 431 | `\|\|  sn == gsn_spear` |  | pending |
| `handler.get_skill.or.009` | 432 | `\|\|  sn == gsn_mace` |  | pending |
| `handler.get_skill.or.010` | 433 | `\|\|  sn == gsn_axe` |  | pending |
| `handler.get_skill.or.011` | 434 | `\|\|  sn == gsn_flail` |  | pending |
| `handler.get_skill.or.012` | 435 | `\|\|  sn == gsn_whip` |  | pending |
| `handler.get_skill.or.013` | 436 | `\|\|  sn == gsn_polearm)` |  | pending |
| `handler.get_skill.if.021` | 443 | `if (ch->daze > 0)` |  | pending |
| `handler.get_skill.if.022` | 445 | `if (skill_table[sn].spell_fun != spell_null)` |  | pending |
| `handler.get_skill.if.023` | 451 | `if ( !IS_NPC(ch) && ch->pcdata->condition[COND_DRUNK]  > 10 )` |  | pending |
| `handler.get_skill.and.010` | 451 | `&& ch->pcdata->condition[COND_DRUNK]  > 10 )` |  | pending |
| `handler.get_skill.return.001` | 454 | `return URANGE(0,skill,100);` |  | pending |

## get_weapon_sn

[Source line 458](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:458); ends at line 479. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- wear_obj: `src/act_obj.c:1619` (lexical_call_candidate).
- mob_hit: `src/fight.c:339` (lexical_call_candidate).
- one_hit: `src/fight.c:438` (lexical_call_candidate).
- do_disarm: `src/fight.c:3010` (lexical_call_candidate).
- do_disarm: `src/fight.c:3011` (lexical_call_candidate).
- do_disarm: `src/fight.c:3012` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2203` (declaration_or_dispatch_reference).

Dependencies: `get_eq_char`, `case`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_weapon_sn.if.001` | 464 | `if (wield == NULL \|\| wield->item_type != ITEM_WEAPON)` |  | pending |
| `handler.get_weapon_sn.or.001` | 464 | `\|\| wield->item_type != ITEM_WEAPON)` |  | pending |
| `handler.get_weapon_sn.switch.001` | 466 | `switch (wield->value[0])` |  | pending |
| `handler.get_weapon_sn.default.001` | 468 | `default :               sn = -1;` |  | pending |
| `handler.get_weapon_sn.break.001` | 468 | `break;` |  | pending |
| `handler.get_weapon_sn.case.001` | 469 | `case(WEAPON_SWORD):     sn = gsn_sword;` |  | pending |
| `handler.get_weapon_sn.break.002` | 469 | `break;` |  | pending |
| `handler.get_weapon_sn.case.002` | 470 | `case(WEAPON_DAGGER):    sn = gsn_dagger;` |  | pending |
| `handler.get_weapon_sn.break.003` | 470 | `break;` |  | pending |
| `handler.get_weapon_sn.case.003` | 471 | `case(WEAPON_SPEAR):     sn = gsn_spear;` |  | pending |
| `handler.get_weapon_sn.break.004` | 471 | `break;` |  | pending |
| `handler.get_weapon_sn.case.004` | 472 | `case(WEAPON_MACE):      sn = gsn_mace;` |  | pending |
| `handler.get_weapon_sn.break.005` | 472 | `break;` |  | pending |
| `handler.get_weapon_sn.case.005` | 473 | `case(WEAPON_AXE):       sn = gsn_axe;` |  | pending |
| `handler.get_weapon_sn.break.006` | 473 | `break;` |  | pending |
| `handler.get_weapon_sn.case.006` | 474 | `case(WEAPON_FLAIL):     sn = gsn_flail;` |  | pending |
| `handler.get_weapon_sn.break.007` | 474 | `break;` |  | pending |
| `handler.get_weapon_sn.case.007` | 475 | `case(WEAPON_WHIP):      sn = gsn_whip;` |  | pending |
| `handler.get_weapon_sn.break.008` | 475 | `break;` |  | pending |
| `handler.get_weapon_sn.case.008` | 476 | `case(WEAPON_POLEARM):   sn = gsn_polearm;` |  | pending |
| `handler.get_weapon_sn.break.009` | 476 | `break;` |  | pending |
| `handler.get_weapon_sn.return.001` | 478 | `return sn;` |  | pending |

## get_weapon_skill

[Source line 481](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:481); ends at line 505. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- wear_obj: `src/act_obj.c:1624` (lexical_call_candidate).
- one_hit: `src/fight.c:439` (lexical_call_candidate).
- do_disarm: `src/fight.c:3010` (lexical_call_candidate).
- do_disarm: `src/fight.c:3011` (lexical_call_candidate).
- do_disarm: `src/fight.c:3012` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2204` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `URANGE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_weapon_skill.if.001` | 486 | `if (IS_NPC(ch))` |  | pending |
| `handler.get_weapon_skill.if.002` | 488 | `if (sn == -1)` |  | pending |
| `handler.get_weapon_skill.if.003` | 490 | `if (sn == gsn_hand_to_hand)` |  | pending |
| `handler.get_weapon_skill.if.004` | 498 | `if (sn == -1)` |  | pending |
| `handler.get_weapon_skill.return.001` | 504 | `return URANGE(0,skill,100);` |  | pending |

## reset_char

[Source line 509](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:509); ends at line 700. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:2077` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2206` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `get_eq_char`, `apply_ac`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.reset_char.if.001` | 516 | `if (IS_NPC(ch))` |  | pending |
| `handler.reset_char.return.001` | 517 | `return;` |  | pending |
| `handler.reset_char.if.002` | 519 | `if (ch->pcdata->perm_hit == 0      \|\|	ch->pcdata->perm_mana == 0     \|\|  ch->pcdata->perm_move == 0     \|\|	ch->pcdata->last_level == 0)` |  | pending |
| `handler.reset_char.or.001` | 520 | `\|\|	ch->pcdata->perm_mana == 0` |  | pending |
| `handler.reset_char.or.002` | 521 | `\|\|  ch->pcdata->perm_move == 0` |  | pending |
| `handler.reset_char.or.003` | 522 | `\|\|	ch->pcdata->last_level == 0)` |  | pending |
| `handler.reset_char.for.001` | 525 | `for (loc = 0; loc < MAX_WEAR; loc++)` |  | pending |
| `handler.reset_char.if.003` | 528 | `if (obj == NULL)` |  | pending |
| `handler.reset_char.continue.001` | 529 | `continue;` |  | pending |
| `handler.reset_char.if.004` | 530 | `if (!obj->enchanted)` |  | pending |
| `handler.reset_char.for.002` | 531 | `for ( af = obj->pIndexData->affected; af != NULL; af = af->next )` |  | pending |
| `handler.reset_char.switch.001` | 534 | `switch(af->location)` |  | pending |
| `handler.reset_char.case.001` | 536 | `case APPLY_SEX:	ch->sex		-= mod;` |  | pending |
| `handler.reset_char.if.005` | 537 | `if (ch->sex < 0 \|\| ch->sex >2)` |  | pending |
| `handler.reset_char.or.004` | 537 | `\|\| ch->sex >2)` |  | pending |
| `handler.reset_char.ternary.001` | 538 | `?` |  | pending |
| `handler.reset_char.break.001` | 541 | `break;` |  | pending |
| `handler.reset_char.case.002` | 542 | `case APPLY_MANA:	ch->max_mana	-= mod;` |  | pending |
| `handler.reset_char.break.002` | 542 | `break;` |  | pending |
| `handler.reset_char.case.003` | 543 | `case APPLY_HIT:	ch->max_hit	-= mod;` |  | pending |
| `handler.reset_char.break.003` | 543 | `break;` |  | pending |
| `handler.reset_char.case.004` | 544 | `case APPLY_MOVE:	ch->max_move	-= mod;` |  | pending |
| `handler.reset_char.break.004` | 544 | `break;` |  | pending |
| `handler.reset_char.for.003` | 548 | `for ( af = obj->affected; af != NULL; af = af->next )` |  | pending |
| `handler.reset_char.switch.002` | 551 | `switch(af->location)` |  | pending |
| `handler.reset_char.case.005` | 553 | `case APPLY_SEX:     ch->sex         -= mod;` |  | pending |
| `handler.reset_char.break.005` | 553 | `break;` |  | pending |
| `handler.reset_char.case.006` | 554 | `case APPLY_MANA:    ch->max_mana    -= mod;` |  | pending |
| `handler.reset_char.break.006` | 554 | `break;` |  | pending |
| `handler.reset_char.case.007` | 555 | `case APPLY_HIT:     ch->max_hit     -= mod;` |  | pending |
| `handler.reset_char.break.007` | 555 | `break;` |  | pending |
| `handler.reset_char.case.008` | 556 | `case APPLY_MOVE:    ch->max_move    -= mod;` |  | pending |
| `handler.reset_char.break.008` | 556 | `break;` |  | pending |
| `handler.reset_char.if.006` | 565 | `if (ch->pcdata->true_sex < 0 \|\| ch->pcdata->true_sex > 2)` |  | pending |
| `handler.reset_char.or.005` | 565 | `\|\| ch->pcdata->true_sex > 2)` |  | pending |
| `handler.reset_char.if.007` | 566 | `if (ch->sex > 0 && ch->sex < 3)` |  | pending |
| `handler.reset_char.and.001` | 566 | `&& ch->sex < 3)` |  | pending |
| `handler.reset_char.for.004` | 575 | `for (stat = 0; stat < MAX_STATS; stat++)` |  | pending |
| `handler.reset_char.if.008` | 578 | `if (ch->pcdata->true_sex < 0 \|\| ch->pcdata->true_sex > 2)` |  | pending |
| `handler.reset_char.or.006` | 578 | `\|\| ch->pcdata->true_sex > 2)` |  | pending |
| `handler.reset_char.for.005` | 585 | `for (i = 0; i < 4; i++)` |  | pending |
| `handler.reset_char.for.006` | 593 | `for (loc = 0; loc < MAX_WEAR; loc++)` |  | pending |
| `handler.reset_char.if.009` | 596 | `if (obj == NULL)` |  | pending |
| `handler.reset_char.continue.002` | 597 | `continue;` |  | pending |
| `handler.reset_char.for.007` | 598 | `for (i = 0; i < 4; i++)` |  | pending |
| `handler.reset_char.if.010` | 601 | `if (!obj->enchanted)` |  | pending |
| `handler.reset_char.for.008` | 602 | `for ( af = obj->pIndexData->affected; af != NULL; af = af->next )` |  | pending |
| `handler.reset_char.switch.003` | 605 | `switch(af->location)` |  | pending |
| `handler.reset_char.case.009` | 607 | `case APPLY_STR:		ch->mod_stat[STAT_STR]	+= mod;` |  | pending |
| `handler.reset_char.break.009` | 607 | `break;` |  | pending |
| `handler.reset_char.case.010` | 608 | `case APPLY_DEX:		ch->mod_stat[STAT_DEX]	+= mod;` |  | pending |
| `handler.reset_char.break.010` | 608 | `break;` |  | pending |
| `handler.reset_char.case.011` | 609 | `case APPLY_INT:		ch->mod_stat[STAT_INT]	+= mod;` |  | pending |
| `handler.reset_char.break.011` | 609 | `break;` |  | pending |
| `handler.reset_char.case.012` | 610 | `case APPLY_WIS:		ch->mod_stat[STAT_WIS]	+= mod;` |  | pending |
| `handler.reset_char.break.012` | 610 | `break;` |  | pending |
| `handler.reset_char.case.013` | 611 | `case APPLY_CON:		ch->mod_stat[STAT_CON]	+= mod;` |  | pending |
| `handler.reset_char.break.013` | 611 | `break;` |  | pending |
| `handler.reset_char.case.014` | 613 | `case APPLY_SEX:		ch->sex			+= mod;` |  | pending |
| `handler.reset_char.break.014` | 613 | `break;` |  | pending |
| `handler.reset_char.case.015` | 614 | `case APPLY_MANA:	ch->max_mana		+= mod;` |  | pending |
| `handler.reset_char.break.015` | 614 | `break;` |  | pending |
| `handler.reset_char.case.016` | 615 | `case APPLY_HIT:		ch->max_hit		+= mod;` |  | pending |
| `handler.reset_char.break.016` | 615 | `break;` |  | pending |
| `handler.reset_char.case.017` | 616 | `case APPLY_MOVE:	ch->max_move		+= mod;` |  | pending |
| `handler.reset_char.break.017` | 616 | `break;` |  | pending |
| `handler.reset_char.case.018` | 618 | `case APPLY_AC:` |  | pending |
| `handler.reset_char.for.009` | 619 | `for (i = 0; i < 4; i ++)` |  | pending |
| `handler.reset_char.break.018` | 621 | `break;` |  | pending |
| `handler.reset_char.case.019` | 622 | `case APPLY_HITROLL:	ch->hitroll		+= mod;` |  | pending |
| `handler.reset_char.break.019` | 622 | `break;` |  | pending |
| `handler.reset_char.case.020` | 623 | `case APPLY_DAMROLL:	ch->damroll		+= mod;` |  | pending |
| `handler.reset_char.break.020` | 623 | `break;` |  | pending |
| `handler.reset_char.case.021` | 625 | `case APPLY_SAVES:		ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.021` | 625 | `break;` |  | pending |
| `handler.reset_char.case.022` | 626 | `case APPLY_SAVING_ROD: 		ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.022` | 626 | `break;` |  | pending |
| `handler.reset_char.case.023` | 627 | `case APPLY_SAVING_PETRI:	ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.023` | 627 | `break;` |  | pending |
| `handler.reset_char.case.024` | 628 | `case APPLY_SAVING_BREATH: 	ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.024` | 628 | `break;` |  | pending |
| `handler.reset_char.case.025` | 629 | `case APPLY_SAVING_SPELL:	ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.025` | 629 | `break;` |  | pending |
| `handler.reset_char.for.010` | 633 | `for ( af = obj->affected; af != NULL; af = af->next )` |  | pending |
| `handler.reset_char.switch.004` | 636 | `switch(af->location)` |  | pending |
| `handler.reset_char.case.026` | 638 | `case APPLY_STR:         ch->mod_stat[STAT_STR]  += mod;` |  | pending |
| `handler.reset_char.break.026` | 638 | `break;` |  | pending |
| `handler.reset_char.case.027` | 639 | `case APPLY_DEX:         ch->mod_stat[STAT_DEX]  += mod;` |  | pending |
| `handler.reset_char.break.027` | 639 | `break;` |  | pending |
| `handler.reset_char.case.028` | 640 | `case APPLY_INT:         ch->mod_stat[STAT_INT]  += mod;` |  | pending |
| `handler.reset_char.break.028` | 640 | `break;` |  | pending |
| `handler.reset_char.case.029` | 641 | `case APPLY_WIS:         ch->mod_stat[STAT_WIS]  += mod;` |  | pending |
| `handler.reset_char.break.029` | 641 | `break;` |  | pending |
| `handler.reset_char.case.030` | 642 | `case APPLY_CON:         ch->mod_stat[STAT_CON]  += mod;` |  | pending |
| `handler.reset_char.break.030` | 642 | `break;` |  | pending |
| `handler.reset_char.case.031` | 644 | `case APPLY_SEX:         ch->sex                 += mod;` |  | pending |
| `handler.reset_char.break.031` | 644 | `break;` |  | pending |
| `handler.reset_char.case.032` | 645 | `case APPLY_MANA:        ch->max_mana            += mod;` |  | pending |
| `handler.reset_char.break.032` | 645 | `break;` |  | pending |
| `handler.reset_char.case.033` | 646 | `case APPLY_HIT:         ch->max_hit             += mod;` |  | pending |
| `handler.reset_char.break.033` | 646 | `break;` |  | pending |
| `handler.reset_char.case.034` | 647 | `case APPLY_MOVE:        ch->max_move            += mod;` |  | pending |
| `handler.reset_char.break.034` | 647 | `break;` |  | pending |
| `handler.reset_char.case.035` | 649 | `case APPLY_AC:` |  | pending |
| `handler.reset_char.for.011` | 650 | `for (i = 0; i < 4; i ++)` |  | pending |
| `handler.reset_char.break.035` | 652 | `break;` |  | pending |
| `handler.reset_char.case.036` | 653 | `case APPLY_HITROLL:     ch->hitroll             += mod;` |  | pending |
| `handler.reset_char.break.036` | 653 | `break;` |  | pending |
| `handler.reset_char.case.037` | 654 | `case APPLY_DAMROLL:     ch->damroll             += mod;` |  | pending |
| `handler.reset_char.break.037` | 654 | `break;` |  | pending |
| `handler.reset_char.case.038` | 656 | `case APPLY_SAVES:         ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.038` | 656 | `break;` |  | pending |
| `handler.reset_char.case.039` | 657 | `case APPLY_SAVING_ROD:          ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.039` | 657 | `break;` |  | pending |
| `handler.reset_char.case.040` | 658 | `case APPLY_SAVING_PETRI:        ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.040` | 658 | `break;` |  | pending |
| `handler.reset_char.case.041` | 659 | `case APPLY_SAVING_BREATH:       ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.041` | 659 | `break;` |  | pending |
| `handler.reset_char.case.042` | 660 | `case APPLY_SAVING_SPELL:        ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.042` | 660 | `break;` |  | pending |
| `handler.reset_char.for.012` | 666 | `for (af = ch->affected; af != NULL; af = af->next)` |  | pending |
| `handler.reset_char.switch.005` | 669 | `switch(af->location)` |  | pending |
| `handler.reset_char.case.043` | 671 | `case APPLY_STR:         ch->mod_stat[STAT_STR]  += mod;` |  | pending |
| `handler.reset_char.break.043` | 671 | `break;` |  | pending |
| `handler.reset_char.case.044` | 672 | `case APPLY_DEX:         ch->mod_stat[STAT_DEX]  += mod;` |  | pending |
| `handler.reset_char.break.044` | 672 | `break;` |  | pending |
| `handler.reset_char.case.045` | 673 | `case APPLY_INT:         ch->mod_stat[STAT_INT]  += mod;` |  | pending |
| `handler.reset_char.break.045` | 673 | `break;` |  | pending |
| `handler.reset_char.case.046` | 674 | `case APPLY_WIS:         ch->mod_stat[STAT_WIS]  += mod;` |  | pending |
| `handler.reset_char.break.046` | 674 | `break;` |  | pending |
| `handler.reset_char.case.047` | 675 | `case APPLY_CON:         ch->mod_stat[STAT_CON]  += mod;` |  | pending |
| `handler.reset_char.break.047` | 675 | `break;` |  | pending |
| `handler.reset_char.case.048` | 677 | `case APPLY_SEX:         ch->sex                 += mod;` |  | pending |
| `handler.reset_char.break.048` | 677 | `break;` |  | pending |
| `handler.reset_char.case.049` | 678 | `case APPLY_MANA:        ch->max_mana            += mod;` |  | pending |
| `handler.reset_char.break.049` | 678 | `break;` |  | pending |
| `handler.reset_char.case.050` | 679 | `case APPLY_HIT:         ch->max_hit             += mod;` |  | pending |
| `handler.reset_char.break.050` | 679 | `break;` |  | pending |
| `handler.reset_char.case.051` | 680 | `case APPLY_MOVE:        ch->max_move            += mod;` |  | pending |
| `handler.reset_char.break.051` | 680 | `break;` |  | pending |
| `handler.reset_char.case.052` | 682 | `case APPLY_AC:` |  | pending |
| `handler.reset_char.for.013` | 683 | `for (i = 0; i < 4; i ++)` |  | pending |
| `handler.reset_char.break.052` | 685 | `break;` |  | pending |
| `handler.reset_char.case.053` | 686 | `case APPLY_HITROLL:     ch->hitroll             += mod;` |  | pending |
| `handler.reset_char.break.053` | 686 | `break;` |  | pending |
| `handler.reset_char.case.054` | 687 | `case APPLY_DAMROLL:     ch->damroll             += mod;` |  | pending |
| `handler.reset_char.break.054` | 687 | `break;` |  | pending |
| `handler.reset_char.case.055` | 689 | `case APPLY_SAVES:         ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.055` | 689 | `break;` |  | pending |
| `handler.reset_char.case.056` | 690 | `case APPLY_SAVING_ROD:          ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.056` | 690 | `break;` |  | pending |
| `handler.reset_char.case.057` | 691 | `case APPLY_SAVING_PETRI:        ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.057` | 691 | `break;` |  | pending |
| `handler.reset_char.case.058` | 692 | `case APPLY_SAVING_BREATH:       ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.058` | 692 | `break;` |  | pending |
| `handler.reset_char.case.059` | 693 | `case APPLY_SAVING_SPELL:        ch->saving_throw += mod;` |  | pending |
| `handler.reset_char.break.059` | 693 | `break;` |  | pending |
| `handler.reset_char.if.011` | 698 | `if (ch->sex < 0 \|\| ch->sex > 2)` |  | pending |
| `handler.reset_char.or.007` | 698 | `\|\| ch->sex > 2)` |  | pending |

## get_trust

[Source line 706](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:706); ends at line 718. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_delete: `src/act_comm.c:88` (lexical_call_candidate).
- do_quit: `src/act_comm.c:1419` (lexical_call_candidate).
- do_commands: `src/act_comm.c:1944` (lexical_call_candidate).
- do_wizhelp: `src/act_comm.c:1969` (lexical_call_candidate).
- show_char_to_char: `src/act_info.c:503` (lexical_call_candidate).
- do_score: `src/act_info.c:1415` (lexical_call_candidate).
- do_score: `src/act_info.c:1418` (lexical_call_candidate).
- do_help: `src/act_info.c:1772` (lexical_call_candidate).
- get_obj: `src/act_obj.c:138` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:112` (lexical_call_candidate).
- do_wiznet: `src/act_wiz.c:128` (lexical_call_candidate).
- wiznet: `src/act_wiz.c:165` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:314` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:314` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:522` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:522` (lexical_call_candidate).
- do_echo: `src/act_wiz.c:669` (lexical_call_candidate).
- do_echo: `src/act_wiz.c:669` (lexical_call_candidate).
- do_recho: `src/act_wiz.c:697` (lexical_call_candidate).
- do_recho: `src/act_wiz.c:697` (lexical_call_candidate).
- do_zecho: `src/act_wiz.c:723` (lexical_call_candidate).
- do_zecho: `src/act_wiz.c:723` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:750` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:750` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:750` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:830` (lexical_call_candidate).
- do_at: `src/act_wiz.c:886` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:941` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:952` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:967` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:1008` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:1023` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2127` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2149` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2149` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2171` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2232` (lexical_call_candidate).
- do_return: `src/act_wiz.c:2272` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2380` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2424` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2486` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2509` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2519` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2538` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2596` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2596` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2660` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2744` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2784` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2791` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2837` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2868` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2868` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2977` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2977` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3030` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3030` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3077` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3077` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4119` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4129` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4129` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4141` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4151` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4151` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4164` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4174` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4174` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4206` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4206` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4212` (lexical_call_candidate).
- do_invis: `src/act_wiz.c:4250` (lexical_call_candidate).
- do_invis: `src/act_wiz.c:4258` (lexical_call_candidate).
- do_incognito: `src/act_wiz.c:4295` (lexical_call_candidate).
- do_incognito: `src/act_wiz.c:4303` (lexical_call_candidate).
- ban_site: `src/ban.c:218` (lexical_call_candidate).
- ban_site: `src/ban.c:236` (lexical_call_candidate).
- do_allow: `src/ban.c:286` (lexical_call_candidate).
- read_from_buffer: `src/comm.c:1175` (lexical_call_candidate).
- read_from_buffer: `src/comm.c:1178` (lexical_call_candidate).
- read_from_buffer: `src/comm.c:1181` (lexical_call_candidate).
- nanny: `src/comm.c:1669` (lexical_call_candidate).
- nanny: `src/comm.c:1911` (lexical_call_candidate).
- nanny: `src/comm.c:2121` (lexical_call_candidate).
- do_slay: `src/fight.c:3084` (lexical_call_candidate).
- can_see_room: `src/handler.c:2416` (lexical_call_candidate).
- can_see: `src/handler.c:2448` (lexical_call_candidate).
- can_see: `src/handler.c:2452` (lexical_call_candidate).
- interpret: `src/interp.c:420` (lexical_call_candidate).
- interpret: `src/interp.c:443` (lexical_call_candidate).
- do_commands: `src/interp.c:757` (lexical_call_candidate).
- do_wizhelp: `src/interp.c:782` (lexical_call_candidate).
- parse_note: `src/note.c:718` (lexical_call_candidate).
- save_char_obj: `src/save.c:131` (lexical_call_candidate).
- scan_list: `src/scan.c:105` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:1811` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:1812` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:1813` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2207` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_trust.if.001` | 708 | `if ( ch->desc != NULL && ch->desc->original != NULL )` | handler.get_trust.pc-level, handler.get_trust.explicit-trust, handler.get_trust.npc-below-hero, handler.get_trust.npc-at-hero-capped, handler.get_trust.npc-above-hero-capped, handler.get_trust.npc-explicit-trust-before-cap, handler.get_trust.switched-original-controls, handler.get_trust.descriptor-without-original, handler.get_trust.negative-trust-is-explicit, handler.get_trust.switched-original-trust-wins | specified |
| `handler.get_trust.and.001` | 708 | `&& ch->desc->original != NULL )` | handler.get_trust.pc-level, handler.get_trust.explicit-trust, handler.get_trust.npc-below-hero, handler.get_trust.npc-at-hero-capped, handler.get_trust.npc-above-hero-capped, handler.get_trust.npc-explicit-trust-before-cap, handler.get_trust.switched-original-controls, handler.get_trust.descriptor-without-original, handler.get_trust.negative-trust-is-explicit, handler.get_trust.switched-original-trust-wins | specified |
| `handler.get_trust.if.002` | 711 | `if (ch->trust)` | handler.get_trust.pc-level, handler.get_trust.explicit-trust, handler.get_trust.npc-below-hero, handler.get_trust.npc-at-hero-capped, handler.get_trust.npc-above-hero-capped, handler.get_trust.npc-explicit-trust-before-cap, handler.get_trust.switched-original-controls, handler.get_trust.descriptor-without-original, handler.get_trust.negative-trust-is-explicit, handler.get_trust.switched-original-trust-wins | specified |
| `handler.get_trust.return.001` | 712 | `return ch->trust;` | handler.get_trust.explicit-trust, handler.get_trust.npc-explicit-trust-before-cap, handler.get_trust.negative-trust-is-explicit, handler.get_trust.switched-original-trust-wins | specified |
| `handler.get_trust.if.003` | 714 | `if ( IS_NPC(ch) && ch->level >= LEVEL_HERO )` | handler.get_trust.pc-level, handler.get_trust.npc-below-hero, handler.get_trust.npc-at-hero-capped, handler.get_trust.npc-above-hero-capped, handler.get_trust.switched-original-controls, handler.get_trust.descriptor-without-original | specified |
| `handler.get_trust.and.002` | 714 | `&& ch->level >= LEVEL_HERO )` | handler.get_trust.pc-level, handler.get_trust.npc-below-hero, handler.get_trust.npc-at-hero-capped, handler.get_trust.npc-above-hero-capped, handler.get_trust.switched-original-controls, handler.get_trust.descriptor-without-original | specified |
| `handler.get_trust.return.002` | 715 | `return LEVEL_HERO - 1;` | handler.get_trust.npc-at-hero-capped, handler.get_trust.npc-above-hero-capped | specified |
| `handler.get_trust.return.003` | 717 | `return ch->level;` | handler.get_trust.pc-level, handler.get_trust.npc-below-hero, handler.get_trust.switched-original-controls, handler.get_trust.descriptor-without-original | specified |
| `handler.get_trust.pc-level.path` | 708 | `pc level` | handler.get_trust.pc-level | specified |
| `handler.get_trust.explicit-trust.path` | 708 | `explicit trust` | handler.get_trust.explicit-trust | specified |
| `handler.get_trust.npc-below-hero.path` | 708 | `npc below hero` | handler.get_trust.npc-below-hero | specified |
| `handler.get_trust.npc-at-hero-capped.path` | 708 | `npc at hero capped` | handler.get_trust.npc-at-hero-capped | specified |
| `handler.get_trust.npc-above-hero-capped.path` | 708 | `npc above hero capped` | handler.get_trust.npc-above-hero-capped | specified |
| `handler.get_trust.npc-explicit-trust-before-cap.path` | 708 | `npc explicit trust before cap` | handler.get_trust.npc-explicit-trust-before-cap | specified |
| `handler.get_trust.switched-original-controls.path` | 708 | `switched original controls` | handler.get_trust.switched-original-controls | specified |
| `handler.get_trust.descriptor-without-original.path` | 708 | `descriptor without original` | handler.get_trust.descriptor-without-original | specified |
| `handler.get_trust.negative-trust-is-explicit.path` | 708 | `negative trust is explicit` | handler.get_trust.negative-trust-is-explicit | specified |
| `handler.get_trust.switched-original-trust-wins.path` | 708 | `switched original trust wins` | handler.get_trust.switched-original-trust-wins | specified |

## get_age

[Source line 724](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:724); ends at line 727. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_score: `src/act_info.c:1411` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1638` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2205` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_age.return.001` | 726 | `return 17 + ( ch->played + (int) (current_time - ch->logon) ) / 72000;` |  | pending |

## get_curr_stat

[Source line 730](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:730); ends at line 751. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_score: `src/act_info.c:1450` (lexical_call_candidate).
- do_score: `src/act_info.c:1452` (lexical_call_candidate).
- do_score: `src/act_info.c:1454` (lexical_call_candidate).
- do_score: `src/act_info.c:1456` (lexical_call_candidate).
- do_score: `src/act_info.c:1458` (lexical_call_candidate).
- do_practice: `src/act_info.c:2602` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1600` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1569` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1571` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1573` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1575` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1577` (lexical_call_candidate).
- do_bash: `src/fight.c:2283` (lexical_call_candidate).
- do_bash: `src/fight.c:2284` (lexical_call_candidate).
- do_dirt: `src/fight.c:2404` (lexical_call_candidate).
- do_dirt: `src/fight.c:2405` (lexical_call_candidate).
- do_trip: `src/fight.c:2550` (lexical_call_candidate).
- do_trip: `src/fight.c:2551` (lexical_call_candidate).
- do_disarm: `src/fight.c:3025` (lexical_call_candidate).
- do_disarm: `src/fight.c:3026` (lexical_call_candidate).
- can_carry_n: `src/handler.c:784` (lexical_call_candidate).
- can_carry_w: `src/handler.c:800` (lexical_call_candidate).
- affect_modify: `src/handler.c:984` (lexical_call_candidate).
- can_see: `src/handler.c:2476` (lexical_call_candidate).
- can_see: `src/handler.c:2477` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3063` (lexical_call_candidate).
- check_improve: `src/skills.c:923` (lexical_call_candidate).
- advance_level: `src/update.c:76` (lexical_call_candidate).
- advance_level: `src/update.c:79` (lexical_call_candidate).
- advance_level: `src/update.c:80` (lexical_call_candidate).
- advance_level: `src/update.c:83` (lexical_call_candidate).
- advance_level: `src/update.c:84` (lexical_call_candidate).
- advance_level: `src/update.c:85` (lexical_call_candidate).
- hit_gain: `src/update.c:173` (lexical_call_candidate).
- mana_gain: `src/update.c:239` (lexical_call_candidate).
- mana_gain: `src/update.c:240` (lexical_call_candidate).
- move_gain: `src/update.c:303` (lexical_call_candidate).
- move_gain: `src/update.c:304` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:1826` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:1828` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:1830` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2208` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `race_lookup`, `UMIN`, `URANGE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_curr_stat.if.001` | 734 | `if (IS_NPC(ch) \|\| ch->level > LEVEL_IMMORTAL)` |  | pending |
| `handler.get_curr_stat.or.001` | 734 | `\|\| ch->level > LEVEL_IMMORTAL)` |  | pending |
| `handler.get_curr_stat.if.002` | 741 | `if (class_table[ch->class].attr_prime == stat)` |  | pending |
| `handler.get_curr_stat.if.003` | 744 | `if ( ch->race == race_lookup("human"))` |  | pending |
| `handler.get_curr_stat.return.001` | 750 | `return URANGE(3,ch->perm_stat[stat] + ch->mod_stat[stat], max);` |  | pending |

## get_max_train

[Source line 754](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:754); ends at line 770. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_train: `src/act_move.c:1555` (lexical_call_candidate).
- do_train: `src/act_move.c:1557` (lexical_call_candidate).
- do_train: `src/act_move.c:1559` (lexical_call_candidate).
- do_train: `src/act_move.c:1561` (lexical_call_candidate).
- do_train: `src/act_move.c:1563` (lexical_call_candidate).
- do_train: `src/act_move.c:1622` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3368` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3372` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3383` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3387` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3398` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3401` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3412` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3416` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3427` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3431` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2209` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `race_lookup`, `UMIN`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_max_train.if.001` | 758 | `if (IS_NPC(ch) \|\| ch->level > LEVEL_IMMORTAL)` |  | pending |
| `handler.get_max_train.or.001` | 758 | `\|\| ch->level > LEVEL_IMMORTAL)` |  | pending |
| `handler.get_max_train.return.001` | 759 | `return 25;` |  | pending |
| `handler.get_max_train.if.002` | 762 | `if (class_table[ch->class].attr_prime == stat)` |  | pending |
| `handler.get_max_train.if.003` | 763 | `if (ch->race == race_lookup("human"))` |  | pending |
| `handler.get_max_train.return.002` | 769 | `return UMIN(max,25);` |  | pending |

## can_carry_n

[Source line 776](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:776); ends at line 785. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_score: `src/act_info.c:1443` (lexical_call_candidate).
- get_obj: `src/act_obj.c:102` (lexical_call_candidate).
- do_give: `src/act_obj.c:799` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2288` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2682` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2210` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `get_curr_stat`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.can_carry_n.if.001` | 778 | `if ( !IS_NPC(ch) && ch->level >= LEVEL_IMMORTAL )` |  | pending |
| `handler.can_carry_n.and.001` | 778 | `&& ch->level >= LEVEL_IMMORTAL )` |  | pending |
| `handler.can_carry_n.return.001` | 779 | `return 1000;` |  | pending |
| `handler.can_carry_n.if.002` | 781 | `if ( IS_NPC(ch) && IS_SET(ch->act, ACT_PET) )` |  | pending |
| `handler.can_carry_n.and.002` | 781 | `&& IS_SET(ch->act, ACT_PET) )` |  | pending |
| `handler.can_carry_n.return.002` | 782 | `return 0;` |  | pending |
| `handler.can_carry_n.return.003` | 784 | `return MAX_WEAR +  2 * get_curr_stat(ch,STAT_DEX) + ch->level;` |  | pending |

## can_carry_w

[Source line 792](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:792); ends at line 801. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_score: `src/act_info.c:1444` (lexical_call_candidate).
- get_obj: `src/act_obj.c:110` (lexical_call_candidate).
- do_give: `src/act_obj.c:805` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2294` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2688` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2211` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `get_curr_stat`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.can_carry_w.if.001` | 794 | `if ( !IS_NPC(ch) && ch->level >= LEVEL_IMMORTAL )` |  | pending |
| `handler.can_carry_w.and.001` | 794 | `&& ch->level >= LEVEL_IMMORTAL )` |  | pending |
| `handler.can_carry_w.return.001` | 795 | `return 10000000;` |  | pending |
| `handler.can_carry_w.if.002` | 797 | `if ( IS_NPC(ch) && IS_SET(ch->act, ACT_PET) )` |  | pending |
| `handler.can_carry_w.and.002` | 797 | `&& IS_SET(ch->act, ACT_PET) )` |  | pending |
| `handler.can_carry_w.return.002` | 798 | `return 0;` |  | pending |
| `handler.can_carry_w.return.003` | 800 | `return str_app[get_curr_stat(ch,STAT_STR)].carry * 10 + ch->level * 25;` |  | pending |

## is_name

[Source line 809](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:809); ends at line 846. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_look: `src/act_info.c:1139` (lexical_call_candidate).
- do_look: `src/act_info.c:1169` (lexical_call_candidate).
- do_help: `src/act_info.c:1775` (lexical_call_candidate).
- do_where: `src/act_info.c:2302` (lexical_call_candidate).
- find_door: `src/act_move.c:305` (lexical_call_candidate).
- do_get: `src/act_obj.c:235` (lexical_call_candidate).
- do_get: `src/act_obj.c:313` (lexical_call_candidate).
- do_put: `src/act_obj.c:451` (lexical_call_candidate).
- do_drop: `src/act_obj.c:619` (lexical_call_candidate).
- get_obj_keeper: `src/act_obj.c:2435` (lexical_call_candidate).
- do_list: `src/act_obj.c:2807` (lexical_call_candidate).
- do_mfind: `src/act_wiz.c:1798` (lexical_call_candidate).
- do_ofind: `src/act_wiz.c:1849` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1889` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1972` (lexical_call_candidate).
- do_sockets: `src/act_wiz.c:4060` (lexical_call_candidate).
- do_sockets: `src/act_wiz.c:4061` (lexical_call_candidate).
- check_parse_name: `src/comm.c:2233` (lexical_call_candidate).
- load_old_obj: `src/db.c:648` (lexical_call_candidate).
- load_old_obj: `src/db.c:649` (lexical_call_candidate).
- load_old_obj: `src/db.c:650` (lexical_call_candidate).
- get_extra_descr: `src/db.c:2056` (lexical_call_candidate).
- get_char_room: `src/handler.c:2027` (lexical_call_candidate).
- get_char_world: `src/handler.c:2057` (lexical_call_candidate).
- get_obj_list: `src/handler.c:2100` (lexical_call_candidate).
- get_obj_carry: `src/handler.c:2128` (lexical_call_candidate).
- get_obj_wear: `src/handler.c:2156` (lexical_call_candidate).
- get_obj_world: `src/handler.c:2207` (lexical_call_candidate).
- is_room_owner: `src/handler.c:2381` (lexical_call_candidate).
- do_cast: `src/magic.c:429` (lexical_call_candidate).
- spell_create_water: `src/magic.c:1543` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3602` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2212` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `str_prefix`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.is_name.if.001` | 815 | `if (namelist == NULL \|\| namelist[0] == '\0')` |  | pending |
| `handler.is_name.or.001` | 815 | `\|\| namelist[0] == '\0')` |  | pending |
| `handler.is_name.return.001` | 816 | `return FALSE;` |  | pending |
| `handler.is_name.if.002` | 819 | `if (str[0] == '\0')` |  | pending |
| `handler.is_name.return.002` | 820 | `return FALSE;` |  | pending |
| `handler.is_name.for.001` | 824 | `for ( ; ; )` |  | pending |
| `handler.is_name.if.003` | 828 | `if (part[0] == '\0' )` |  | pending |
| `handler.is_name.return.003` | 829 | `return TRUE;` |  | pending |
| `handler.is_name.for.002` | 833 | `for ( ; ; )` |  | pending |
| `handler.is_name.if.004` | 836 | `if (name[0] == '\0')` |  | pending |
| `handler.is_name.return.004` | 837 | `return FALSE;` |  | pending |
| `handler.is_name.if.005` | 839 | `if (!str_prefix(string,name))` |  | pending |
| `handler.is_name.return.005` | 840 | `return TRUE;` |  | pending |
| `handler.is_name.if.006` | 842 | `if (!str_prefix(part,name))` |  | pending |
| `handler.is_name.break.001` | 843 | `break;` |  | pending |

## is_exact_name

[Source line 848](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:848); ends at line 863. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- check_parse_name: `src/comm.c:2148` (lexical_call_candidate).
- spell_ventriloquate: `src/magic.c:4398` (lexical_call_candidate).
- is_note_to: `src/note.c:348` (lexical_call_candidate).
- is_note_to: `src/note.c:351` (lexical_call_candidate).
- is_note_to: `src/note.c:354` (lexical_call_candidate).
- is_note_to: `src/note.c:357` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2213` (declaration_or_dispatch_reference).

Dependencies: `one_argument`, `str_cmp`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.is_exact_name.if.001` | 852 | `if (namelist == NULL)` |  | pending |
| `handler.is_exact_name.return.001` | 853 | `return FALSE;` |  | pending |
| `handler.is_exact_name.for.001` | 855 | `for ( ; ; )` |  | pending |
| `handler.is_exact_name.if.002` | 858 | `if ( name[0] == '\0' )` |  | pending |
| `handler.is_exact_name.return.002` | 859 | `return FALSE;` |  | pending |
| `handler.is_exact_name.if.003` | 860 | `if ( !str_cmp( str, name ) )` |  | pending |
| `handler.is_exact_name.return.003` | 861 | `return TRUE;` |  | pending |

## affect_enchant

[Source line 866](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:866); ends at line 891. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- acid_effect: `src/effects.c:135` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2186` (declaration_or_dispatch_reference).

Dependencies: `new_affect`, `UMAX`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_enchant.if.001` | 869 | `if (!obj->enchanted)` |  | pending |
| `handler.affect_enchant.for.001` | 874 | `for (paf = obj->pIndexData->affected;              paf != NULL; paf = paf->next)` |  | pending |

## affect_modify

[Source line 897](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:897); ends at line 1000. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- affect_to_char: `src/handler.c:1114` (lexical_call_candidate).
- affect_remove: `src/handler.c:1164` (lexical_call_candidate).
- affect_remove_obj: `src/handler.c:1208` (lexical_call_candidate).
- equip_char: `src/handler.c:1609` (lexical_call_candidate).
- equip_char: `src/handler.c:1614` (lexical_call_candidate).
- unequip_char: `src/handler.c:1664` (lexical_call_candidate).
- unequip_char: `src/handler.c:1688` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/handler.c:46` (declaration_or_dispatch_reference).

Dependencies: `SET_BIT`, `REMOVE_BIT`, `bug`, `IS_NPC`, `get_eq_char`, `get_obj_weight`, `get_curr_stat`, `act`, `obj_from_char`, `obj_to_room`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_modify.if.001` | 904 | `if ( fAdd )` |  | pending |
| `handler.affect_modify.switch.001` | 906 | `switch (paf->where)` |  | pending |
| `handler.affect_modify.case.001` | 908 | `case TO_AFFECTS:` |  | pending |
| `handler.affect_modify.break.001` | 910 | `break;` |  | pending |
| `handler.affect_modify.case.002` | 911 | `case TO_IMMUNE:` |  | pending |
| `handler.affect_modify.break.002` | 913 | `break;` |  | pending |
| `handler.affect_modify.case.003` | 914 | `case TO_RESIST:` |  | pending |
| `handler.affect_modify.break.003` | 916 | `break;` |  | pending |
| `handler.affect_modify.case.004` | 917 | `case TO_VULN:` |  | pending |
| `handler.affect_modify.break.004` | 919 | `break;` |  | pending |
| `handler.affect_modify.switch.002` | 924 | `switch (paf->where)` |  | pending |
| `handler.affect_modify.case.005` | 926 | `case TO_AFFECTS:` |  | pending |
| `handler.affect_modify.break.005` | 928 | `break;` |  | pending |
| `handler.affect_modify.case.006` | 929 | `case TO_IMMUNE:` |  | pending |
| `handler.affect_modify.break.006` | 931 | `break;` |  | pending |
| `handler.affect_modify.case.007` | 932 | `case TO_RESIST:` |  | pending |
| `handler.affect_modify.break.007` | 934 | `break;` |  | pending |
| `handler.affect_modify.case.008` | 935 | `case TO_VULN:` |  | pending |
| `handler.affect_modify.break.008` | 937 | `break;` |  | pending |
| `handler.affect_modify.switch.003` | 942 | `switch ( paf->location )` |  | pending |
| `handler.affect_modify.default.001` | 944 | `default:` |  | pending |
| `handler.affect_modify.return.001` | 946 | `return;` |  | pending |
| `handler.affect_modify.case.009` | 948 | `case APPLY_NONE:						break;` |  | pending |
| `handler.affect_modify.break.009` | 948 | `break;` |  | pending |
| `handler.affect_modify.case.010` | 949 | `case APPLY_STR:           ch->mod_stat[STAT_STR]	+= mod;` |  | pending |
| `handler.affect_modify.break.010` | 949 | `break;` |  | pending |
| `handler.affect_modify.case.011` | 950 | `case APPLY_DEX:           ch->mod_stat[STAT_DEX]	+= mod;` |  | pending |
| `handler.affect_modify.break.011` | 950 | `break;` |  | pending |
| `handler.affect_modify.case.012` | 951 | `case APPLY_INT:           ch->mod_stat[STAT_INT]	+= mod;` |  | pending |
| `handler.affect_modify.break.012` | 951 | `break;` |  | pending |
| `handler.affect_modify.case.013` | 952 | `case APPLY_WIS:           ch->mod_stat[STAT_WIS]	+= mod;` |  | pending |
| `handler.affect_modify.break.013` | 952 | `break;` |  | pending |
| `handler.affect_modify.case.014` | 953 | `case APPLY_CON:           ch->mod_stat[STAT_CON]	+= mod;` |  | pending |
| `handler.affect_modify.break.014` | 953 | `break;` |  | pending |
| `handler.affect_modify.case.015` | 954 | `case APPLY_SEX:           ch->sex			+= mod;` |  | pending |
| `handler.affect_modify.break.015` | 954 | `break;` |  | pending |
| `handler.affect_modify.case.016` | 955 | `case APPLY_CLASS:						break;` |  | pending |
| `handler.affect_modify.break.016` | 955 | `break;` |  | pending |
| `handler.affect_modify.case.017` | 956 | `case APPLY_LEVEL:						break;` |  | pending |
| `handler.affect_modify.break.017` | 956 | `break;` |  | pending |
| `handler.affect_modify.case.018` | 957 | `case APPLY_AGE:						break;` |  | pending |
| `handler.affect_modify.break.018` | 957 | `break;` |  | pending |
| `handler.affect_modify.case.019` | 958 | `case APPLY_HEIGHT:						break;` |  | pending |
| `handler.affect_modify.break.019` | 958 | `break;` |  | pending |
| `handler.affect_modify.case.020` | 959 | `case APPLY_WEIGHT:						break;` |  | pending |
| `handler.affect_modify.break.020` | 959 | `break;` |  | pending |
| `handler.affect_modify.case.021` | 960 | `case APPLY_MANA:          ch->max_mana		+= mod;` |  | pending |
| `handler.affect_modify.break.021` | 960 | `break;` |  | pending |
| `handler.affect_modify.case.022` | 961 | `case APPLY_HIT:           ch->max_hit		+= mod;` |  | pending |
| `handler.affect_modify.break.022` | 961 | `break;` |  | pending |
| `handler.affect_modify.case.023` | 962 | `case APPLY_MOVE:          ch->max_move		+= mod;` |  | pending |
| `handler.affect_modify.break.023` | 962 | `break;` |  | pending |
| `handler.affect_modify.case.024` | 963 | `case APPLY_GOLD:						break;` |  | pending |
| `handler.affect_modify.break.024` | 963 | `break;` |  | pending |
| `handler.affect_modify.case.025` | 964 | `case APPLY_EXP:						break;` |  | pending |
| `handler.affect_modify.break.025` | 964 | `break;` |  | pending |
| `handler.affect_modify.case.026` | 965 | `case APPLY_AC:` |  | pending |
| `handler.affect_modify.for.001` | 966 | `for (i = 0; i < 4; i ++)` |  | pending |
| `handler.affect_modify.break.026` | 968 | `break;` |  | pending |
| `handler.affect_modify.case.027` | 969 | `case APPLY_HITROLL:       ch->hitroll		+= mod;` |  | pending |
| `handler.affect_modify.break.027` | 969 | `break;` |  | pending |
| `handler.affect_modify.case.028` | 970 | `case APPLY_DAMROLL:       ch->damroll		+= mod;` |  | pending |
| `handler.affect_modify.break.028` | 970 | `break;` |  | pending |
| `handler.affect_modify.case.029` | 971 | `case APPLY_SAVES:   ch->saving_throw		+= mod;` |  | pending |
| `handler.affect_modify.break.029` | 971 | `break;` |  | pending |
| `handler.affect_modify.case.030` | 972 | `case APPLY_SAVING_ROD:    ch->saving_throw		+= mod;` |  | pending |
| `handler.affect_modify.break.030` | 972 | `break;` |  | pending |
| `handler.affect_modify.case.031` | 973 | `case APPLY_SAVING_PETRI:  ch->saving_throw		+= mod;` |  | pending |
| `handler.affect_modify.break.031` | 973 | `break;` |  | pending |
| `handler.affect_modify.case.032` | 974 | `case APPLY_SAVING_BREATH: ch->saving_throw		+= mod;` |  | pending |
| `handler.affect_modify.break.032` | 974 | `break;` |  | pending |
| `handler.affect_modify.case.033` | 975 | `case APPLY_SAVING_SPELL:  ch->saving_throw		+= mod;` |  | pending |
| `handler.affect_modify.break.033` | 975 | `break;` |  | pending |
| `handler.affect_modify.case.034` | 976 | `case APPLY_SPELL_AFFECT:  					break;` |  | pending |
| `handler.affect_modify.break.034` | 976 | `break;` |  | pending |
| `handler.affect_modify.if.002` | 983 | `if ( !IS_NPC(ch) && ( wield = get_eq_char( ch, WEAR_WIELD ) ) != NULL     &&   get_obj_weight(wield) > (str_app[get_curr_stat(ch,STAT_STR)].wield*10))` |  | pending |
| `handler.affect_modify.and.001` | 983 | `&& ( wield = get_eq_char( ch, WEAR_WIELD ) ) != NULL` |  | pending |
| `handler.affect_modify.and.002` | 984 | `&&   get_obj_weight(wield) > (str_app[get_curr_stat(ch,STAT_STR)].wield*10))` |  | pending |
| `handler.affect_modify.if.003` | 988 | `if ( depth == 0 )` |  | pending |
| `handler.affect_modify.return.002` | 999 | `return;` |  | pending |

## affect_find

[Source line 1004](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1004); ends at line 1015. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- one_hit: `src/fight.c:594` (lexical_call_candidate).
- spell_bless: `src/magic.c:787` (lexical_call_candidate).
- spell_curse: `src/magic.c:1696` (lexical_call_candidate).
- char_update: `src/update.c:799` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2182` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_find.for.001` | 1008 | `for ( paf_find = paf; paf_find != NULL; paf_find = paf_find->next )` |  | pending |
| `handler.affect_find.if.001` | 1010 | `if ( paf_find->type == sn )` |  | pending |
| `handler.affect_find.return.001` | 1011 | `return paf_find;` |  | pending |
| `handler.affect_find.return.002` | 1014 | `return NULL;` |  | pending |

## affect_check

[Source line 1018](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1018); ends at line 1097. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- affect_remove: `src/handler.c:1194` (lexical_call_candidate).
- affect_remove_obj: `src/handler.c:1253` (lexical_call_candidate).
- unequip_char: `src/handler.c:1665` (lexical_call_candidate).
- unequip_char: `src/handler.c:1689` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2183` (declaration_or_dispatch_reference).

Dependencies: `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_check.if.001` | 1023 | `if (where == TO_OBJECT \|\| where == TO_WEAPON \|\| vector == 0)` |  | pending |
| `handler.affect_check.or.001` | 1023 | `\|\| where == TO_WEAPON \|\| vector == 0)` |  | pending |
| `handler.affect_check.or.002` | 1023 | `\|\| vector == 0)` |  | pending |
| `handler.affect_check.return.001` | 1024 | `return;` |  | pending |
| `handler.affect_check.for.001` | 1026 | `for (paf = ch->affected; paf != NULL; paf = paf->next)` |  | pending |
| `handler.affect_check.if.002` | 1027 | `if (paf->where == where && paf->bitvector == vector)` |  | pending |
| `handler.affect_check.and.001` | 1027 | `&& paf->bitvector == vector)` |  | pending |
| `handler.affect_check.switch.001` | 1029 | `switch (where)` |  | pending |
| `handler.affect_check.case.001` | 1031 | `case TO_AFFECTS:` |  | pending |
| `handler.affect_check.break.001` | 1033 | `break;` |  | pending |
| `handler.affect_check.case.002` | 1034 | `case TO_IMMUNE:` |  | pending |
| `handler.affect_check.break.002` | 1036 | `break;` |  | pending |
| `handler.affect_check.case.003` | 1037 | `case TO_RESIST:` |  | pending |
| `handler.affect_check.break.003` | 1039 | `break;` |  | pending |
| `handler.affect_check.case.004` | 1040 | `case TO_VULN:` |  | pending |
| `handler.affect_check.break.004` | 1042 | `break;` |  | pending |
| `handler.affect_check.return.002` | 1044 | `return;` |  | pending |
| `handler.affect_check.for.002` | 1047 | `for (obj = ch->carrying; obj != NULL; obj = obj->next_content)` |  | pending |
| `handler.affect_check.if.003` | 1049 | `if (obj->wear_loc == -1)` |  | pending |
| `handler.affect_check.continue.001` | 1050 | `continue;` |  | pending |
| `handler.affect_check.for.003` | 1052 | `for (paf = obj->affected; paf != NULL; paf = paf->next)` |  | pending |
| `handler.affect_check.if.004` | 1053 | `if (paf->where == where && paf->bitvector == vector)` |  | pending |
| `handler.affect_check.and.002` | 1053 | `&& paf->bitvector == vector)` |  | pending |
| `handler.affect_check.switch.002` | 1055 | `switch (where)` |  | pending |
| `handler.affect_check.case.005` | 1057 | `case TO_AFFECTS:` |  | pending |
| `handler.affect_check.break.005` | 1059 | `break;` |  | pending |
| `handler.affect_check.case.006` | 1060 | `case TO_IMMUNE:` |  | pending |
| `handler.affect_check.break.006` | 1062 | `break;` |  | pending |
| `handler.affect_check.case.007` | 1063 | `case TO_RESIST:` |  | pending |
| `handler.affect_check.break.007` | 1065 | `break;` |  | pending |
| `handler.affect_check.case.008` | 1066 | `case TO_VULN:` |  | pending |
| `handler.affect_check.return.003` | 1070 | `return;` |  | pending |
| `handler.affect_check.if.005` | 1073 | `if (obj->enchanted)` |  | pending |
| `handler.affect_check.continue.002` | 1074 | `continue;` |  | pending |
| `handler.affect_check.for.004` | 1076 | `for (paf = obj->pIndexData->affected; paf != NULL; paf = paf->next)` |  | pending |
| `handler.affect_check.if.006` | 1077 | `if (paf->where == where && paf->bitvector == vector)` |  | pending |
| `handler.affect_check.and.003` | 1077 | `&& paf->bitvector == vector)` |  | pending |
| `handler.affect_check.switch.003` | 1079 | `switch (where)` |  | pending |
| `handler.affect_check.case.009` | 1081 | `case TO_AFFECTS:` |  | pending |
| `handler.affect_check.break.008` | 1083 | `break;` |  | pending |
| `handler.affect_check.case.010` | 1084 | `case TO_IMMUNE:` |  | pending |
| `handler.affect_check.break.009` | 1086 | `break;` |  | pending |
| `handler.affect_check.case.011` | 1087 | `case TO_RESIST:` |  | pending |
| `handler.affect_check.break.010` | 1089 | `break;` |  | pending |
| `handler.affect_check.case.012` | 1090 | `case TO_VULN:` |  | pending |
| `handler.affect_check.break.011` | 1092 | `break;` |  | pending |
| `handler.affect_check.return.004` | 1094 | `return;` |  | pending |

## affect_to_char

[Source line 1102](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1102); ends at line 1116. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_sneak: `src/act_move.c:1355` (lexical_call_candidate).
- create_mobile: `src/db.c:1652` (lexical_call_candidate).
- create_mobile: `src/db.c:1665` (lexical_call_candidate).
- create_mobile: `src/db.c:1677` (lexical_call_candidate).
- create_mobile: `src/db.c:1689` (lexical_call_candidate).
- clone_mobile: `src/db.c:1814` (lexical_call_candidate).
- fire_effect: `src/effects.c:338` (lexical_call_candidate).
- do_berserk: `src/fight.c:2187` (lexical_call_candidate).
- do_berserk: `src/fight.c:2190` (lexical_call_candidate).
- do_berserk: `src/fight.c:2194` (lexical_call_candidate).
- do_dirt: `src/fight.c:2461` (lexical_call_candidate).
- affect_join: `src/handler.c:1318` (lexical_call_candidate).
- equip_char: `src/handler.c:1612` (lexical_call_candidate).
- spell_armor: `src/magic.c:758` (lexical_call_candidate).
- spell_bless: `src/magic.c:840` (lexical_call_candidate).
- spell_bless: `src/magic.c:844` (lexical_call_candidate).
- spell_blindness: `src/magic.c:869` (lexical_call_candidate).
- spell_calm: `src/magic.c:1007` (lexical_call_candidate).
- spell_calm: `src/magic.c:1010` (lexical_call_candidate).
- spell_change_sex: `src/magic.c:1305` (lexical_call_candidate).
- spell_charm_person: `src/magic.c:1352` (lexical_call_candidate).
- spell_curse: `src/magic.c:1741` (lexical_call_candidate).
- spell_curse: `src/magic.c:1745` (lexical_call_candidate).
- spell_detect_evil: `src/magic.c:1803` (lexical_call_candidate).
- spell_detect_good: `src/magic.c:1831` (lexical_call_candidate).
- spell_detect_hidden: `src/magic.c:1860` (lexical_call_candidate).
- spell_detect_invis: `src/magic.c:1890` (lexical_call_candidate).
- spell_detect_magic: `src/magic.c:1920` (lexical_call_candidate).
- spell_faerie_fire: `src/magic.c:2739` (lexical_call_candidate).
- spell_fly: `src/magic.c:2819` (lexical_call_candidate).
- spell_frenzy: `src/magic.c:2868` (lexical_call_candidate).
- spell_frenzy: `src/magic.c:2871` (lexical_call_candidate).
- spell_frenzy: `src/magic.c:2875` (lexical_call_candidate).
- spell_giant_strength: `src/magic.c:2953` (lexical_call_candidate).
- spell_haste: `src/magic.c:3015` (lexical_call_candidate).
- spell_infravision: `src/magic.c:3479` (lexical_call_candidate).
- spell_invis: `src/magic.c:3531` (lexical_call_candidate).
- spell_mass_invis: `src/magic.c:3710` (lexical_call_candidate).
- spell_pass_door: `src/magic.c:3748` (lexical_call_candidate).
- spell_protection_evil: `src/magic.c:3892` (lexical_call_candidate).
- spell_protection_good: `src/magic.c:3921` (lexical_call_candidate).
- spell_sanctuary: `src/magic.c:4140` (lexical_call_candidate).
- spell_shield: `src/magic.c:4169` (lexical_call_candidate).
- spell_slow: `src/magic.c:4277` (lexical_call_candidate).
- spell_stone_skin: `src/magic.c:4307` (lexical_call_candidate).
- spell_weaken: `src/magic.c:4422` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2214` (declaration_or_dispatch_reference).

Dependencies: `new_affect`, `VALIDATE`, `affect_modify`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_to_char.return.001` | 1115 | `return;` |  | pending |

## affect_to_obj

[Source line 1119](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1119); ends at line 1146. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_envenom: `src/act_obj.c:920` (lexical_call_candidate).
- create_object: `src/db.c:1959` (lexical_call_candidate).
- clone_object: `src/db.c:1999` (lexical_call_candidate).
- spell_bless: `src/magic.c:811` (lexical_call_candidate).
- spell_curse: `src/magic.c:1720` (lexical_call_candidate).
- spell_fireproof: `src/magic.c:2703` (lexical_call_candidate).
- spell_invis: `src/magic.c:3510` (lexical_call_candidate).
- spell_poison: `src/magic.c:3836` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2215` (declaration_or_dispatch_reference).

Dependencies: `new_affect`, `VALIDATE`, `SET_BIT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_to_obj.if.001` | 1132 | `if (paf->bitvector)` |  | pending |
| `handler.affect_to_obj.switch.001` | 1133 | `switch (paf->where)` |  | pending |
| `handler.affect_to_obj.case.001` | 1135 | `case TO_OBJECT:` |  | pending |
| `handler.affect_to_obj.break.001` | 1137 | `break;` |  | pending |
| `handler.affect_to_obj.case.002` | 1138 | `case TO_WEAPON:` |  | pending |
| `handler.affect_to_obj.if.002` | 1139 | `if (obj->item_type == ITEM_WEAPON)` |  | pending |
| `handler.affect_to_obj.break.002` | 1141 | `break;` |  | pending |
| `handler.affect_to_obj.return.001` | 1145 | `return;` |  | pending |

## affect_remove

[Source line 1153](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1153); ends at line 1196. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- raw_kill: `src/fight.c:1678` (lexical_call_candidate).
- affect_strip: `src/handler.c:1271` (lexical_call_candidate).
- affect_join: `src/handler.c:1313` (lexical_call_candidate).
- unequip_char: `src/handler.c:1657` (lexical_call_candidate).
- unequip_char: `src/handler.c:1681` (lexical_call_candidate).
- free_char: `src/recycle.c:364` (lexical_call_candidate).
- char_update: `src/update.c:731` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2216` (declaration_or_dispatch_reference).

Dependencies: `bug`, `affect_modify`, `free_affect`, `affect_check`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_remove.if.001` | 1158 | `if ( ch->affected == NULL )` |  | pending |
| `handler.affect_remove.return.001` | 1161 | `return;` |  | pending |
| `handler.affect_remove.if.002` | 1168 | `if ( paf == ch->affected )` |  | pending |
| `handler.affect_remove.for.001` | 1176 | `for ( prev = ch->affected; prev != NULL; prev = prev->next )` |  | pending |
| `handler.affect_remove.if.003` | 1178 | `if ( prev->next == paf )` |  | pending |
| `handler.affect_remove.break.001` | 1181 | `break;` |  | pending |
| `handler.affect_remove.if.004` | 1185 | `if ( prev == NULL )` |  | pending |
| `handler.affect_remove.return.002` | 1188 | `return;` |  | pending |
| `handler.affect_remove.return.003` | 1195 | `return;` |  | pending |

## affect_remove_obj

[Source line 1198](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1198); ends at line 1255. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- spell_bless: `src/magic.c:791` (lexical_call_candidate).
- spell_curse: `src/magic.c:1700` (lexical_call_candidate).
- obj_update: `src/update.c:898` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2217` (declaration_or_dispatch_reference).

Dependencies: `bug`, `affect_modify`, `REMOVE_BIT`, `free_affect`, `affect_check`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_remove_obj.if.001` | 1201 | `if ( obj->affected == NULL )` |  | pending |
| `handler.affect_remove_obj.return.001` | 1204 | `return;` |  | pending |
| `handler.affect_remove_obj.if.002` | 1207 | `if (obj->carried_by != NULL && obj->wear_loc != -1)` |  | pending |
| `handler.affect_remove_obj.and.001` | 1207 | `&& obj->wear_loc != -1)` |  | pending |
| `handler.affect_remove_obj.if.003` | 1214 | `if (paf->bitvector)` |  | pending |
| `handler.affect_remove_obj.switch.001` | 1215 | `switch( paf->where)` |  | pending |
| `handler.affect_remove_obj.case.001` | 1217 | `case TO_OBJECT:` |  | pending |
| `handler.affect_remove_obj.break.001` | 1219 | `break;` |  | pending |
| `handler.affect_remove_obj.case.002` | 1220 | `case TO_WEAPON:` |  | pending |
| `handler.affect_remove_obj.if.004` | 1221 | `if (obj->item_type == ITEM_WEAPON)` |  | pending |
| `handler.affect_remove_obj.break.002` | 1223 | `break;` |  | pending |
| `handler.affect_remove_obj.if.005` | 1226 | `if ( paf == obj->affected )` |  | pending |
| `handler.affect_remove_obj.for.001` | 1234 | `for ( prev = obj->affected; prev != NULL; prev = prev->next )` |  | pending |
| `handler.affect_remove_obj.if.006` | 1236 | `if ( prev->next == paf )` |  | pending |
| `handler.affect_remove_obj.break.003` | 1239 | `break;` |  | pending |
| `handler.affect_remove_obj.if.007` | 1243 | `if ( prev == NULL )` |  | pending |
| `handler.affect_remove_obj.return.002` | 1246 | `return;` |  | pending |
| `handler.affect_remove_obj.if.008` | 1252 | `if (obj->carried_by != NULL && obj->wear_loc != -1)` |  | pending |
| `handler.affect_remove_obj.and.002` | 1252 | `&& obj->wear_loc != -1)` |  | pending |
| `handler.affect_remove_obj.return.003` | 1254 | `return;` |  | pending |

## affect_strip

[Source line 1262](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1262); ends at line 1275. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- stop_follower: `src/act_comm.c:1549` (lexical_call_candidate).
- do_sneak: `src/act_move.c:1340` (lexical_call_candidate).
- do_visible: `src/act_move.c:1390` (lexical_call_candidate).
- do_visible: `src/act_move.c:1391` (lexical_call_candidate).
- do_visible: `src/act_move.c:1392` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2194` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2770` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2771` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2772` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2773` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2774` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2802` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2803` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2804` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2805` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2806` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2825` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2826` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2827` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2828` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2829` (lexical_call_candidate).
- damage: `src/fight.c:748` (lexical_call_candidate).
- damage: `src/fight.c:749` (lexical_call_candidate).
- check_killer: `src/fight.c:1223` (lexical_call_candidate).
- set_fighting: `src/fight.c:1392` (lexical_call_candidate).
- check_dispel: `src/magic.c:266` (lexical_call_candidate).
- spell_faerie_fog: `src/magic.c:2762` (lexical_call_candidate).
- spell_faerie_fog: `src/magic.c:2763` (lexical_call_candidate).
- spell_faerie_fog: `src/magic.c:2764` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2218` (declaration_or_dispatch_reference).

Dependencies: `affect_remove`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_strip.for.001` | 1267 | `for ( paf = ch->affected; paf != NULL; paf = paf_next )` |  | pending |
| `handler.affect_strip.if.001` | 1270 | `if ( paf->type == sn )` |  | pending |
| `handler.affect_strip.return.001` | 1274 | `return;` |  | pending |

## is_affected

[Source line 1282](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1282); ends at line 1293. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_berserk: `src/fight.c:2134` (lexical_call_candidate).
- do_berserk: `src/fight.c:2135` (lexical_call_candidate).
- check_dispel: `src/magic.c:258` (lexical_call_candidate).
- spell_armor: `src/magic.c:743` (lexical_call_candidate).
- spell_bless: `src/magic.c:824` (lexical_call_candidate).
- spell_calm: `src/magic.c:988` (lexical_call_candidate).
- spell_change_sex: `src/magic.c:1284` (lexical_call_candidate).
- spell_cure_blindness: `src/magic.c:1563` (lexical_call_candidate).
- spell_cure_disease: `src/magic.c:1602` (lexical_call_candidate).
- spell_cure_poison: `src/magic.c:1642` (lexical_call_candidate).
- spell_dispel_magic: `src/magic.c:2146` (lexical_call_candidate).
- spell_frenzy: `src/magic.c:2832` (lexical_call_candidate).
- spell_frenzy: `src/magic.c:2841` (lexical_call_candidate).
- spell_giant_strength: `src/magic.c:2937` (lexical_call_candidate).
- spell_haste: `src/magic.c:2981` (lexical_call_candidate).
- spell_shield: `src/magic.c:4153` (lexical_call_candidate).
- spell_slow: `src/magic.c:4236` (lexical_call_candidate).
- spell_stone_skin: `src/magic.c:4291` (lexical_call_candidate).
- spell_weaken: `src/magic.c:4412` (lexical_call_candidate).
- char_update: `src/update.c:741` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2219` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.is_affected.for.001` | 1286 | `for ( paf = ch->affected; paf != NULL; paf = paf->next )` |  | pending |
| `handler.is_affected.if.001` | 1288 | `if ( paf->type == sn )` |  | pending |
| `handler.is_affected.return.001` | 1289 | `return TRUE;` |  | pending |
| `handler.is_affected.return.002` | 1292 | `return FALSE;` |  | pending |

## affect_join

[Source line 1300](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1300); ends at line 1320. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_drink: `src/act_obj.c:1248` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1327` (lexical_call_candidate).
- cold_effect: `src/effects.c:231` (lexical_call_candidate).
- poison_effect: `src/effects.c:480` (lexical_call_candidate).
- one_hit: `src/fight.c:613` (lexical_call_candidate).
- char_to_room: `src/handler.c:1449` (lexical_call_candidate).
- spell_chill_touch: `src/magic.c:1389` (lexical_call_candidate).
- spell_plague: `src/magic.c:3778` (lexical_call_candidate).
- spell_poison: `src/magic.c:3862` (lexical_call_candidate).
- spell_sleep: `src/magic.c:4220` (lexical_call_candidate).
- char_update: `src/update.c:784` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2220` (declaration_or_dispatch_reference).

Dependencies: `affect_remove`, `affect_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_join.for.001` | 1306 | `for ( paf_old = ch->affected; paf_old != NULL; paf_old = paf_old->next )` |  | pending |
| `handler.affect_join.if.001` | 1308 | `if ( paf_old->type == paf->type )` |  | pending |
| `handler.affect_join.break.001` | 1314 | `break;` |  | pending |
| `handler.affect_join.return.001` | 1319 | `return;` |  | pending |

## char_from_room

[Source line 1327](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1327); ends at line 1371. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:137` (lexical_call_candidate).
- move_char: `src/act_move.c:196` (lexical_call_candidate).
- do_recall: `src/act_move.c:1458` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:852` (lexical_call_candidate).
- do_at: `src/act_wiz.c:894` (lexical_call_candidate).
- do_at: `src/act_wiz.c:906` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:961` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:1017` (lexical_call_candidate).
- stop_idling: `src/comm.c:2325` (lexical_call_candidate).
- extract_char: `src/handler.c:1955` (lexical_call_candidate).
- spell_gate: `src/magic.c:2913` (lexical_call_candidate).
- spell_gate: `src/magic.c:2923` (lexical_call_candidate).
- spell_summon: `src/magic.c:4342` (lexical_call_candidate).
- spell_teleport: `src/magic.c:4374` (lexical_call_candidate).
- spell_word_of_recall: `src/magic.c:4458` (lexical_call_candidate).
- char_update: `src/update.c:696` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2221` (declaration_or_dispatch_reference).

Dependencies: `bug`, `IS_NPC`, `get_eq_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.char_from_room.if.001` | 1331 | `if ( ch->in_room == NULL )` |  | pending |
| `handler.char_from_room.return.001` | 1334 | `return;` |  | pending |
| `handler.char_from_room.if.002` | 1337 | `if ( !IS_NPC(ch) )` |  | pending |
| `handler.char_from_room.if.003` | 1340 | `if ( ( obj = get_eq_char( ch, WEAR_LIGHT ) ) != NULL     &&   obj->item_type == ITEM_LIGHT     &&   obj->value[2] != 0     &&   ch->in_room->light > 0 )` |  | pending |
| `handler.char_from_room.and.001` | 1341 | `&&   obj->item_type == ITEM_LIGHT` |  | pending |
| `handler.char_from_room.and.002` | 1342 | `&&   obj->value[2] != 0` |  | pending |
| `handler.char_from_room.and.003` | 1343 | `&&   ch->in_room->light > 0 )` |  | pending |
| `handler.char_from_room.if.004` | 1346 | `if ( ch == ch->in_room->people )` |  | pending |
| `handler.char_from_room.for.001` | 1354 | `for ( prev = ch->in_room->people; prev; prev = prev->next_in_room )` |  | pending |
| `handler.char_from_room.if.005` | 1356 | `if ( prev->next_in_room == ch )` |  | pending |
| `handler.char_from_room.break.001` | 1359 | `break;` |  | pending |
| `handler.char_from_room.if.006` | 1363 | `if ( prev == NULL )` |  | pending |
| `handler.char_from_room.return.002` | 1370 | `return;` |  | pending |

## char_to_room

[Source line 1378](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1378); ends at line 1456. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:138` (lexical_call_candidate).
- move_char: `src/act_move.c:197` (lexical_call_candidate).
- do_recall: `src/act_move.c:1459` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2604` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:853` (lexical_call_candidate).
- do_at: `src/act_wiz.c:895` (lexical_call_candidate).
- do_at: `src/act_wiz.c:907` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:962` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:1018` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2420` (lexical_call_candidate).
- do_mload: `src/act_wiz.c:2483` (lexical_call_candidate).
- nanny: `src/comm.c:2099` (lexical_call_candidate).
- nanny: `src/comm.c:2106` (lexical_call_candidate).
- nanny: `src/comm.c:2110` (lexical_call_candidate).
- nanny: `src/comm.c:2114` (lexical_call_candidate).
- nanny: `src/comm.c:2125` (lexical_call_candidate).
- stop_idling: `src/comm.c:2326` (lexical_call_candidate).
- reset_area: `src/db.c:1290` (lexical_call_candidate).
- char_to_room: `src/handler.c:1389` (lexical_call_candidate).
- extract_char: `src/handler.c:1960` (lexical_call_candidate).
- spell_gate: `src/magic.c:2914` (lexical_call_candidate).
- spell_gate: `src/magic.c:2924` (lexical_call_candidate).
- spell_summon: `src/magic.c:4343` (lexical_call_candidate).
- spell_teleport: `src/magic.c:4375` (lexical_call_candidate).
- spell_word_of_recall: `src/magic.c:4459` (lexical_call_candidate).
- char_update: `src/update.c:697` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2222` (declaration_or_dispatch_reference).

Dependencies: `bug`, `get_room_index`, `char_to_room`, `IS_NPC`, `get_eq_char`, `IS_AFFECTED`, `REMOVE_BIT`, `number_range`, `saves_spell`, `IS_IMMORTAL`, `number_bits`, `send_to_char`, `act`, `affect_join`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.char_to_room.if.001` | 1382 | `if ( pRoomIndex == NULL )` |  | pending |
| `handler.char_to_room.if.002` | 1388 | `if ((room = get_room_index(ROOM_VNUM_TEMPLE)) != NULL)` |  | pending |
| `handler.char_to_room.return.001` | 1391 | `return;` |  | pending |
| `handler.char_to_room.if.003` | 1398 | `if ( !IS_NPC(ch) )` |  | pending |
| `handler.char_to_room.if.004` | 1400 | `if (ch->in_room->area->empty)` |  | pending |
| `handler.char_to_room.if.005` | 1408 | `if ( ( obj = get_eq_char( ch, WEAR_LIGHT ) ) != NULL     &&   obj->item_type == ITEM_LIGHT     &&   obj->value[2] != 0 )` |  | pending |
| `handler.char_to_room.and.001` | 1409 | `&&   obj->item_type == ITEM_LIGHT` |  | pending |
| `handler.char_to_room.and.002` | 1410 | `&&   obj->value[2] != 0 )` |  | pending |
| `handler.char_to_room.if.006` | 1413 | `if (IS_AFFECTED(ch,AFF_PLAGUE))` |  | pending |
| `handler.char_to_room.for.001` | 1418 | `for ( af = ch->affected; af != NULL; af = af->next )` |  | pending |
| `handler.char_to_room.if.007` | 1420 | `if (af->type == gsn_plague)` |  | pending |
| `handler.char_to_room.break.001` | 1421 | `break;` |  | pending |
| `handler.char_to_room.if.008` | 1424 | `if (af == NULL)` |  | pending |
| `handler.char_to_room.return.002` | 1427 | `return;` |  | pending |
| `handler.char_to_room.if.009` | 1430 | `if (af->level == 1)` |  | pending |
| `handler.char_to_room.return.003` | 1431 | `return;` |  | pending |
| `handler.char_to_room.for.002` | 1441 | `for ( vch = ch->in_room->people; vch != NULL; vch = vch->next_in_room)` |  | pending |
| `handler.char_to_room.if.010` | 1443 | `if (!saves_spell(plague.level - 2,vch,DAM_DISEASE)  	    &&  !IS_IMMORTAL(vch) &&             	!IS_AFFECTED(vch,AFF_PLAGUE) && number_bits(6) == 0)` |  | pending |
| `handler.char_to_room.and.003` | 1444 | `&&  !IS_IMMORTAL(vch) &&` |  | pending |
| `handler.char_to_room.and.004` | 1444 | `&&` |  | pending |
| `handler.char_to_room.and.005` | 1445 | `&& number_bits(6) == 0)` |  | pending |
| `handler.char_to_room.return.004` | 1455 | `return;` |  | pending |

## obj_to_char

[Source line 1463](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1463); ends at line 1472. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- get_obj: `src/act_obj.c:184` (lexical_call_candidate).
- do_give: `src/act_obj.c:818` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2301` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2735` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:247` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:255` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:276` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:286` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2373` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2416` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2534` (lexical_call_candidate).
- nanny: `src/comm.c:2097` (lexical_call_candidate).
- reset_area: `src/db.c:1448` (lexical_call_candidate).
- disarm: `src/fight.c:2110` (lexical_call_candidate).
- spell_create_rose: `src/magic.c:1499` (lexical_call_candidate).
- spell_floating_disc: `src/magic.c:2793` (lexical_call_candidate).
- fread_obj: `src/save.c:1529` (lexical_call_candidate).
- spec_janitor: `src/special.c:869` (lexical_call_candidate).
- mobile_update: `src/update.c:435` (lexical_call_candidate).
- obj_update: `src/update.c:971` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2223` (declaration_or_dispatch_reference).

Dependencies: `get_obj_number`, `get_obj_weight`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.obj_to_char.entry` | 1463 | `Straight-line entry` |  | pending |

## obj_from_char

[Source line 1479](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1479); ends at line 1518. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_put: `src/act_obj.c:430` (lexical_call_candidate).
- do_put: `src/act_obj.c:468` (lexical_call_candidate).
- do_drop: `src/act_obj.c:600` (lexical_call_candidate).
- do_drop: `src/act_obj.c:625` (lexical_call_candidate).
- do_give: `src/act_obj.c:817` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2300` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2729` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2924` (lexical_call_candidate).
- make_corpse: `src/fight.c:1487` (lexical_call_candidate).
- group_gain: `src/fight.c:1768` (lexical_call_candidate).
- disarm: `src/fight.c:2108` (lexical_call_candidate).
- affect_modify: `src/handler.c:993` (lexical_call_candidate).
- equip_char: `src/handler.c:1597` (lexical_call_candidate).
- extract_obj: `src/handler.c:1881` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3071` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3093` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3121` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3142` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2224` (declaration_or_dispatch_reference).

Dependencies: `bug`, `unequip_char`, `get_obj_number`, `get_obj_weight`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.obj_from_char.if.001` | 1483 | `if ( ( ch = obj->carried_by ) == NULL )` |  | pending |
| `handler.obj_from_char.return.001` | 1486 | `return;` |  | pending |
| `handler.obj_from_char.if.002` | 1489 | `if ( obj->wear_loc != WEAR_NONE )` |  | pending |
| `handler.obj_from_char.if.003` | 1492 | `if ( ch->carrying == obj )` |  | pending |
| `handler.obj_from_char.for.001` | 1500 | `for ( prev = ch->carrying; prev != NULL; prev = prev->next_content )` |  | pending |
| `handler.obj_from_char.if.004` | 1502 | `if ( prev->next_content == obj )` |  | pending |
| `handler.obj_from_char.break.001` | 1505 | `break;` |  | pending |
| `handler.obj_from_char.if.005` | 1509 | `if ( prev == NULL )` |  | pending |
| `handler.obj_from_char.return.002` | 1517 | `return;` |  | pending |

## apply_ac

[Source line 1525](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1525); ends at line 1549. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- reset_char: `src/handler.c:599` (lexical_call_candidate).
- equip_char: `src/handler.c:1603` (lexical_call_candidate).
- unequip_char: `src/handler.c:1643` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2225` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.apply_ac.if.001` | 1527 | `if ( obj->item_type != ITEM_ARMOR )` |  | pending |
| `handler.apply_ac.return.001` | 1528 | `return 0;` |  | pending |
| `handler.apply_ac.switch.001` | 1530 | `switch ( iWear )` |  | pending |
| `handler.apply_ac.case.001` | 1532 | `case WEAR_BODY:	return 3 * obj->value[type];` |  | pending |
| `handler.apply_ac.return.002` | 1532 | `return 3 * obj->value[type];` |  | pending |
| `handler.apply_ac.case.002` | 1533 | `case WEAR_HEAD:	return 2 * obj->value[type];` |  | pending |
| `handler.apply_ac.return.003` | 1533 | `return 2 * obj->value[type];` |  | pending |
| `handler.apply_ac.case.003` | 1534 | `case WEAR_LEGS:	return 2 * obj->value[type];` |  | pending |
| `handler.apply_ac.return.004` | 1534 | `return 2 * obj->value[type];` |  | pending |
| `handler.apply_ac.case.004` | 1535 | `case WEAR_FEET:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.005` | 1535 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.005` | 1536 | `case WEAR_HANDS:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.006` | 1536 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.006` | 1537 | `case WEAR_ARMS:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.007` | 1537 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.007` | 1538 | `case WEAR_SHIELD:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.008` | 1538 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.008` | 1539 | `case WEAR_NECK_1:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.009` | 1539 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.009` | 1540 | `case WEAR_NECK_2:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.010` | 1540 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.010` | 1541 | `case WEAR_ABOUT:	return 2 * obj->value[type];` |  | pending |
| `handler.apply_ac.return.011` | 1541 | `return 2 * obj->value[type];` |  | pending |
| `handler.apply_ac.case.011` | 1542 | `case WEAR_WAIST:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.012` | 1542 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.012` | 1543 | `case WEAR_WRIST_L:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.013` | 1543 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.013` | 1544 | `case WEAR_WRIST_R:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.014` | 1544 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.case.014` | 1545 | `case WEAR_HOLD:	return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.015` | 1545 | `return     obj->value[type];` |  | pending |
| `handler.apply_ac.return.016` | 1548 | `return 0;` |  | pending |

## get_eq_char

[Source line 1556](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1556); ends at line 1570. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_char_to_char_1: `src/act_info.c:465` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2125` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1067` (lexical_call_candidate).
- remove_obj: `src/act_obj.c:1351` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1402` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1403` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1408` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1416` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1431` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1432` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1437` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1445` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1540` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1541` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1546` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1556` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1578` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1609` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:1959` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2055` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:243` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:251` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:260` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:280` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:282` (lexical_call_candidate).
- one_hit: `src/fight.c:415` (lexical_call_candidate).
- one_hit: `src/fight.c:537` (lexical_call_candidate).
- damage: `src/fight.c:694` (lexical_call_candidate).
- check_parry: `src/fight.c:1272` (lexical_call_candidate).
- check_shield_block: `src/fight.c:1306` (lexical_call_candidate).
- disarm: `src/fight.c:2091` (lexical_call_candidate).
- do_backstab: `src/fight.c:2770` (lexical_call_candidate).
- do_disarm: `src/fight.c:2989` (lexical_call_candidate).
- do_disarm: `src/fight.c:3003` (lexical_call_candidate).
- do_disarm: `src/fight.c:3017` (lexical_call_candidate).
- get_weapon_sn: `src/handler.c:463` (lexical_call_candidate).
- reset_char: `src/handler.c:527` (lexical_call_candidate).
- reset_char: `src/handler.c:595` (lexical_call_candidate).
- affect_modify: `src/handler.c:983` (lexical_call_candidate).
- char_from_room: `src/handler.c:1340` (lexical_call_candidate).
- char_to_room: `src/handler.c:1408` (lexical_call_candidate).
- equip_char: `src/handler.c:1582` (lexical_call_candidate).
- spell_floating_disc: `src/magic.c:2779` (lexical_call_candidate).
- spell_portal: `src/magic2.c:80` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:133` (lexical_call_candidate).
- spec_patrolman: `src/special.c:273` (lexical_call_candidate).
- spec_patrolman: `src/special.c:275` (lexical_call_candidate).
- char_update: `src/update.c:666` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2226` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_eq_char.if.001` | 1560 | `if (ch == NULL)` |  | pending |
| `handler.get_eq_char.return.001` | 1561 | `return NULL;` |  | pending |
| `handler.get_eq_char.for.001` | 1563 | `for ( obj = ch->carrying; obj != NULL; obj = obj->next_content )` |  | pending |
| `handler.get_eq_char.if.002` | 1565 | `if ( obj->wear_loc == iWear )` |  | pending |
| `handler.get_eq_char.return.002` | 1566 | `return obj;` |  | pending |
| `handler.get_eq_char.return.003` | 1569 | `return NULL;` |  | pending |

## equip_char

[Source line 1577](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1577); ends at line 1622. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- wear_obj: `src/act_obj.c:1396` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1412` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1420` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1441` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1449` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1464` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1474` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1484` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1494` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1504` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1514` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1524` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1534` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1552` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1562` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1588` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1617` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1651` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1661` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:248` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:256` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:277` (lexical_call_candidate).
- do_outfit: `src/act_wiz.c:287` (lexical_call_candidate).
- reset_area: `src/db.c:1450` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2227` (declaration_or_dispatch_reference).

Dependencies: `get_eq_char`, `bug`, `IS_OBJ_STAT`, `IS_EVIL`, `IS_GOOD`, `IS_NEUTRAL`, `act`, `obj_from_char`, `obj_to_room`, `apply_ac`, `affect_modify`, `affect_to_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.equip_char.if.001` | 1582 | `if ( get_eq_char( ch, iWear ) != NULL )` |  | pending |
| `handler.equip_char.return.001` | 1585 | `return;` |  | pending |
| `handler.equip_char.if.002` | 1588 | `if ( ( IS_OBJ_STAT(obj, ITEM_ANTI_EVIL)    && IS_EVIL(ch)    )     \|\|   ( IS_OBJ_STAT(obj, ITEM_ANTI_GOOD)    && IS_GOOD(ch)    )     \|\|   ( IS_OBJ_STAT(obj, ITEM_ANTI_NEUTRAL) && IS_NEUTRAL(ch) ) )` |  | pending |
| `handler.equip_char.and.001` | 1588 | `&& IS_EVIL(ch)    )` |  | pending |
| `handler.equip_char.or.001` | 1589 | `\|\|   ( IS_OBJ_STAT(obj, ITEM_ANTI_GOOD)    && IS_GOOD(ch)    )` |  | pending |
| `handler.equip_char.and.002` | 1589 | `&& IS_GOOD(ch)    )` |  | pending |
| `handler.equip_char.or.002` | 1590 | `\|\|   ( IS_OBJ_STAT(obj, ITEM_ANTI_NEUTRAL) && IS_NEUTRAL(ch) ) )` |  | pending |
| `handler.equip_char.and.003` | 1590 | `&& IS_NEUTRAL(ch) ) )` |  | pending |
| `handler.equip_char.return.002` | 1599 | `return;` |  | pending |
| `handler.equip_char.for.001` | 1602 | `for (i = 0; i < 4; i++)` |  | pending |
| `handler.equip_char.if.003` | 1606 | `if (!obj->enchanted)` |  | pending |
| `handler.equip_char.for.002` | 1607 | `for ( paf = obj->pIndexData->affected; paf != NULL; paf = paf->next )` |  | pending |
| `handler.equip_char.if.004` | 1608 | `if ( paf->location != APPLY_SPELL_AFFECT )` |  | pending |
| `handler.equip_char.for.003` | 1610 | `for ( paf = obj->affected; paf != NULL; paf = paf->next )` |  | pending |
| `handler.equip_char.if.005` | 1611 | `if ( paf->location == APPLY_SPELL_AFFECT )` |  | pending |
| `handler.equip_char.if.006` | 1616 | `if ( obj->item_type == ITEM_LIGHT     &&   obj->value[2] != 0     &&   ch->in_room != NULL )` |  | pending |
| `handler.equip_char.and.004` | 1617 | `&&   obj->value[2] != 0` |  | pending |
| `handler.equip_char.and.005` | 1618 | `&&   ch->in_room != NULL )` |  | pending |
| `handler.equip_char.return.003` | 1621 | `return;` |  | pending |

## unequip_char

[Source line 1629](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1629); ends at line 1699. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- remove_obj: `src/act_obj.c:1363` (lexical_call_candidate).
- obj_from_char: `src/handler.c:1490` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2228` (declaration_or_dispatch_reference).

Dependencies: `bug`, `apply_ac`, `affect_remove`, `affect_modify`, `affect_check`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.unequip_char.if.001` | 1636 | `if ( obj->wear_loc == WEAR_NONE )` |  | pending |
| `handler.unequip_char.return.001` | 1639 | `return;` |  | pending |
| `handler.unequip_char.for.001` | 1642 | `for (i = 0; i < 4; i++)` |  | pending |
| `handler.unequip_char.if.002` | 1646 | `if (!obj->enchanted)` |  | pending |
| `handler.unequip_char.for.002` | 1647 | `for ( paf = obj->pIndexData->affected; paf != NULL; paf = paf->next )` |  | pending |
| `handler.unequip_char.if.003` | 1648 | `if ( paf->location == APPLY_SPELL_AFFECT )` |  | pending |
| `handler.unequip_char.for.003` | 1650 | `for ( lpaf = ch->affected; lpaf != NULL; lpaf = lpaf_next )` |  | pending |
| `handler.unequip_char.if.004` | 1653 | `if ((lpaf->type == paf->type) && 		        (lpaf->level == paf->level) && 		        (lpaf->location == APPLY_SPELL_AFFECT))` |  | pending |
| `handler.unequip_char.and.001` | 1653 | `&&` |  | pending |
| `handler.unequip_char.and.002` | 1654 | `&&` |  | pending |
| `handler.unequip_char.for.004` | 1668 | `for ( paf = obj->affected; paf != NULL; paf = paf->next )` |  | pending |
| `handler.unequip_char.if.005` | 1669 | `if ( paf->location == APPLY_SPELL_AFFECT )` |  | pending |
| `handler.unequip_char.for.005` | 1672 | `for ( lpaf = ch->affected; lpaf != NULL; lpaf = lpaf_next )` |  | pending |
| `handler.unequip_char.if.006` | 1675 | `if ((lpaf->type == paf->type) && 		    (lpaf->level == paf->level) && 		    (lpaf->location == APPLY_SPELL_AFFECT))` |  | pending |
| `handler.unequip_char.and.003` | 1675 | `&&` |  | pending |
| `handler.unequip_char.and.004` | 1676 | `&&` |  | pending |
| `handler.unequip_char.if.007` | 1692 | `if ( obj->item_type == ITEM_LIGHT     &&   obj->value[2] != 0     &&   ch->in_room != NULL     &&   ch->in_room->light > 0 )` |  | pending |
| `handler.unequip_char.and.005` | 1693 | `&&   obj->value[2] != 0` |  | pending |
| `handler.unequip_char.and.006` | 1694 | `&&   ch->in_room != NULL` |  | pending |
| `handler.unequip_char.and.007` | 1695 | `&&   ch->in_room->light > 0 )` |  | pending |
| `handler.unequip_char.return.002` | 1698 | `return;` |  | pending |

## count_obj_list

[Source line 1706](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1706); ends at line 1719. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- reset_area: `src/db.c:1309` (lexical_call_candidate).
- reset_area: `src/db.c:1346` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2229` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.count_obj_list.for.001` | 1712 | `for ( obj = list; obj != NULL; obj = obj->next_content )` |  | pending |
| `handler.count_obj_list.if.001` | 1714 | `if ( obj->pIndexData == pObjIndex )` |  | pending |
| `handler.count_obj_list.return.001` | 1718 | `return nMatch;` |  | pending |

## obj_from_room

[Source line 1726](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1726); ends at line 1768. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:142` (lexical_call_candidate).
- get_obj: `src/act_obj.c:157` (lexical_call_candidate).
- extract_obj: `src/handler.c:1879` (lexical_call_candidate).
- spec_janitor: `src/special.c:868` (lexical_call_candidate).
- mobile_update: `src/update.c:434` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2230` (declaration_or_dispatch_reference).

Dependencies: `bug`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.obj_from_room.if.001` | 1731 | `if ( ( in_room = obj->in_room ) == NULL )` |  | pending |
| `handler.obj_from_room.return.001` | 1734 | `return;` |  | pending |
| `handler.obj_from_room.for.001` | 1737 | `for (ch = in_room->people; ch != NULL; ch = ch->next_in_room)` |  | pending |
| `handler.obj_from_room.if.002` | 1738 | `if (ch->on == obj)` |  | pending |
| `handler.obj_from_room.if.003` | 1741 | `if ( obj == in_room->contents )` |  | pending |
| `handler.obj_from_room.for.002` | 1749 | `for ( prev = in_room->contents; prev; prev = prev->next_content )` |  | pending |
| `handler.obj_from_room.if.004` | 1751 | `if ( prev->next_content == obj )` |  | pending |
| `handler.obj_from_room.break.001` | 1754 | `break;` |  | pending |
| `handler.obj_from_room.if.005` | 1758 | `if ( prev == NULL )` |  | pending |
| `handler.obj_from_room.return.002` | 1761 | `return;` |  | pending |
| `handler.obj_from_room.return.003` | 1767 | `return;` |  | pending |

## obj_to_room

[Source line 1775](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1775); ends at line 1783. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:143` (lexical_call_candidate).
- do_drop: `src/act_obj.c:579` (lexical_call_candidate).
- do_drop: `src/act_obj.c:601` (lexical_call_candidate).
- do_drop: `src/act_obj.c:626` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2375` (lexical_call_candidate).
- do_oload: `src/act_wiz.c:2536` (lexical_call_candidate).
- reset_area: `src/db.c:1318` (lexical_call_candidate).
- acid_effect: `src/effects.c:178` (lexical_call_candidate).
- acid_effect: `src/effects.c:180` (lexical_call_candidate).
- fire_effect: `src/effects.c:427` (lexical_call_candidate).
- fire_effect: `src/effects.c:429` (lexical_call_candidate).
- make_corpse: `src/fight.c:1515` (lexical_call_candidate).
- make_corpse: `src/fight.c:1526` (lexical_call_candidate).
- make_corpse: `src/fight.c:1533` (lexical_call_candidate).
- death_cry: `src/fight.c:1632` (lexical_call_candidate).
- group_gain: `src/fight.c:1769` (lexical_call_candidate).
- disarm: `src/fight.c:2113` (lexical_call_candidate).
- affect_modify: `src/handler.c:994` (lexical_call_candidate).
- equip_char: `src/handler.c:1598` (lexical_call_candidate).
- spell_continual_light: `src/magic.c:1457` (lexical_call_candidate).
- spell_create_food: `src/magic.c:1487` (lexical_call_candidate).
- spell_create_spring: `src/magic.c:1509` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3072` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3094` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3122` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3143` (lexical_call_candidate).
- spell_portal: `src/magic2.c:99` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:153` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:167` (lexical_call_candidate).
- spec_fido: `src/special.c:779` (lexical_call_candidate).
- obj_update: `src/update.c:969` (lexical_call_candidate).
- obj_update: `src/update.c:977` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2231` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.obj_to_room.return.001` | 1782 | `return;` |  | pending |

## obj_to_obj

[Source line 1790](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1790); ends at line 1811. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_put: `src/act_obj.c:431` (lexical_call_candidate).
- do_put: `src/act_obj.c:469` (lexical_call_candidate).
- recursive_clone: `src/act_wiz.c:2305` (lexical_call_candidate).
- reset_area: `src/db.c:1356` (lexical_call_candidate).
- make_corpse: `src/fight.c:1442` (lexical_call_candidate).
- make_corpse: `src/fight.c:1461` (lexical_call_candidate).
- make_corpse: `src/fight.c:1530` (lexical_call_candidate).
- fread_obj: `src/save.c:1531` (lexical_call_candidate).
- obj_update: `src/update.c:962` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2232` (declaration_or_dispatch_reference).

Dependencies: `get_obj_number`, `get_obj_weight`, `WEIGHT_MULT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.obj_to_obj.if.001` | 1797 | `if (obj_to->pIndexData->vnum == OBJ_VNUM_PIT)` |  | pending |
| `handler.obj_to_obj.for.001` | 1800 | `for ( ; obj_to != NULL; obj_to = obj_to->in_obj )` |  | pending |
| `handler.obj_to_obj.if.002` | 1802 | `if ( obj_to->carried_by != NULL )` |  | pending |
| `handler.obj_to_obj.return.001` | 1810 | `return;` |  | pending |

## obj_from_obj

[Source line 1818](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1818); ends at line 1866. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- get_obj: `src/act_obj.c:151` (lexical_call_candidate).
- acid_effect: `src/effects.c:176` (lexical_call_candidate).
- fire_effect: `src/effects.c:425` (lexical_call_candidate).
- make_corpse: `src/fight.c:1514` (lexical_call_candidate).
- extract_obj: `src/handler.c:1883` (lexical_call_candidate).
- spec_fido: `src/special.c:778` (lexical_call_candidate).
- obj_update: `src/update.c:959` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2233` (declaration_or_dispatch_reference).

Dependencies: `bug`, `get_obj_number`, `get_obj_weight`, `WEIGHT_MULT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.obj_from_obj.if.001` | 1822 | `if ( ( obj_from = obj->in_obj ) == NULL )` |  | pending |
| `handler.obj_from_obj.return.001` | 1825 | `return;` |  | pending |
| `handler.obj_from_obj.if.002` | 1828 | `if ( obj == obj_from->contains )` |  | pending |
| `handler.obj_from_obj.for.001` | 1836 | `for ( prev = obj_from->contains; prev; prev = prev->next_content )` |  | pending |
| `handler.obj_from_obj.if.003` | 1838 | `if ( prev->next_content == obj )` |  | pending |
| `handler.obj_from_obj.break.001` | 1841 | `break;` |  | pending |
| `handler.obj_from_obj.if.004` | 1845 | `if ( prev == NULL )` |  | pending |
| `handler.obj_from_obj.return.002` | 1848 | `return;` |  | pending |
| `handler.obj_from_obj.for.002` | 1855 | `for ( ; obj_from != NULL; obj_from = obj_from->in_obj )` |  | pending |
| `handler.obj_from_obj.if.005` | 1857 | `if ( obj_from->carried_by != NULL )` |  | pending |
| `handler.obj_from_obj.return.003` | 1865 | `return;` |  | pending |

## extract_obj

[Source line 1873](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1873); ends at line 1918. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:207` (lexical_call_candidate).
- get_obj: `src/act_obj.c:180` (lexical_call_candidate).
- do_drop: `src/act_obj.c:553` (lexical_call_candidate).
- do_drop: `src/act_obj.c:558` (lexical_call_candidate).
- do_drop: `src/act_obj.c:563` (lexical_call_candidate).
- do_drop: `src/act_obj.c:568` (lexical_call_candidate).
- do_drop: `src/act_obj.c:574` (lexical_call_candidate).
- do_drop: `src/act_obj.c:608` (lexical_call_candidate).
- do_drop: `src/act_obj.c:633` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1338` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1834` (lexical_call_candidate).
- do_quaff: `src/act_obj.c:1878` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1946` (lexical_call_candidate).
- do_brandish: `src/act_obj.c:2033` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2126` (lexical_call_candidate).
- obj_to_keeper: `src/act_obj.c:2394` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2920` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2573` (lexical_call_candidate).
- acid_effect: `src/effects.c:183` (lexical_call_candidate).
- acid_effect: `src/effects.c:191` (lexical_call_candidate).
- cold_effect: `src/effects.c:294` (lexical_call_candidate).
- fire_effect: `src/effects.c:432` (lexical_call_candidate).
- fire_effect: `src/effects.c:439` (lexical_call_candidate).
- shock_effect: `src/effects.c:617` (lexical_call_candidate).
- damage: `src/fight.c:697` (lexical_call_candidate).
- make_corpse: `src/fight.c:1500` (lexical_call_candidate).
- make_corpse: `src/fight.c:1521` (lexical_call_candidate).
- extract_obj: `src/handler.c:1888` (lexical_call_candidate).
- extract_char: `src/handler.c:1951` (lexical_call_candidate).
- spell_enchant_armor: `src/magic.c:2289` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2482` (lexical_call_candidate).
- spell_recharge: `src/magic.c:4047` (lexical_call_candidate).
- spell_portal: `src/magic2.c:92` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:145` (lexical_call_candidate).
- free_char: `src/recycle.c:358` (lexical_call_candidate).
- fread_obj: `src/save.c:1523` (lexical_call_candidate).
- spec_fido: `src/special.c:781` (lexical_call_candidate).
- char_update: `src/update.c:675` (lexical_call_candidate).
- obj_update: `src/update.c:967` (lexical_call_candidate).
- obj_update: `src/update.c:974` (lexical_call_candidate).
- obj_update: `src/update.c:981` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2234` (declaration_or_dispatch_reference).

Dependencies: `obj_from_room`, `obj_from_char`, `obj_from_obj`, `extract_obj`, `bug`, `free_obj`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.extract_obj.if.001` | 1878 | `if ( obj->in_room != NULL )` |  | pending |
| `handler.extract_obj.if.002` | 1880 | `if ( obj->carried_by != NULL )` |  | pending |
| `handler.extract_obj.if.003` | 1882 | `if ( obj->in_obj != NULL )` |  | pending |
| `handler.extract_obj.for.001` | 1885 | `for ( obj_content = obj->contains; obj_content; obj_content = obj_next )` |  | pending |
| `handler.extract_obj.if.004` | 1891 | `if ( object_list == obj )` |  | pending |
| `handler.extract_obj.for.002` | 1899 | `for ( prev = object_list; prev != NULL; prev = prev->next )` |  | pending |
| `handler.extract_obj.if.005` | 1901 | `if ( prev->next == obj )` |  | pending |
| `handler.extract_obj.break.001` | 1904 | `break;` |  | pending |
| `handler.extract_obj.if.006` | 1908 | `if ( prev == NULL )` |  | pending |
| `handler.extract_obj.return.001` | 1911 | `return;` |  | pending |
| `handler.extract_obj.return.002` | 1917 | `return;` |  | pending |

## extract_char

[Source line 1925](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:1925); ends at line 2007. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_quit: `src/act_comm.c:1427` (lexical_call_candidate).
- do_quit: `src/act_comm.c:1440` (lexical_call_candidate).
- nuke_pets: `src/act_comm.c:1575` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2566` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2609` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2617` (lexical_call_candidate).
- raw_kill: `src/fight.c:1672` (lexical_call_candidate).
- raw_kill: `src/fight.c:1676` (lexical_call_candidate).
- char_update: `src/update.c:639` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2235` (declaration_or_dispatch_reference).

Dependencies: `nuke_pets`, `die_follower`, `stop_fighting`, `extract_obj`, `char_from_room`, `char_to_room`, `get_room_index`, `IS_NPC`, `do_function`, `bug`, `free_char`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.extract_char.if.001` | 1942 | `if ( fPull )` |  | pending |
| `handler.extract_char.for.001` | 1948 | `for ( obj = ch->carrying; obj != NULL; obj = obj_next )` |  | pending |
| `handler.extract_char.if.002` | 1954 | `if (ch->in_room != NULL)` |  | pending |
| `handler.extract_char.if.003` | 1958 | `if ( !fPull )` |  | pending |
| `handler.extract_char.return.001` | 1961 | `return;` |  | pending |
| `handler.extract_char.if.004` | 1964 | `if ( IS_NPC(ch) )` |  | pending |
| `handler.extract_char.if.005` | 1967 | `if ( ch->desc != NULL && ch->desc->original != NULL )` |  | pending |
| `handler.extract_char.and.001` | 1967 | `&& ch->desc->original != NULL )` |  | pending |
| `handler.extract_char.for.002` | 1973 | `for ( wch = char_list; wch != NULL; wch = wch->next )` |  | pending |
| `handler.extract_char.if.006` | 1975 | `if ( wch->reply == ch )` |  | pending |
| `handler.extract_char.if.007` | 1979 | `if ( ch == char_list )` |  | pending |
| `handler.extract_char.for.003` | 1987 | `for ( prev = char_list; prev != NULL; prev = prev->next )` |  | pending |
| `handler.extract_char.if.008` | 1989 | `if ( prev->next == ch )` |  | pending |
| `handler.extract_char.break.001` | 1992 | `break;` |  | pending |
| `handler.extract_char.if.009` | 1996 | `if ( prev == NULL )` |  | pending |
| `handler.extract_char.return.002` | 1999 | `return;` |  | pending |
| `handler.extract_char.if.010` | 2003 | `if ( ch->desc != NULL )` |  | pending |
| `handler.extract_char.return.003` | 2006 | `return;` |  | pending |

## get_char_room

[Source line 2014](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2014); ends at line 2034. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_follow: `src/act_comm.c:1477` (lexical_call_candidate).
- do_order: `src/act_comm.c:1649` (lexical_call_candidate).
- do_group: `src/act_comm.c:1733` (lexical_call_candidate).
- do_look: `src/act_info.c:1111` (lexical_call_candidate).
- do_consider: `src/act_info.c:2336` (lexical_call_candidate).
- do_wake: `src/act_move.c:1319` (lexical_call_candidate).
- do_give: `src/act_obj.c:695` (lexical_call_candidate).
- do_give: `src/act_obj.c:779` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1059` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1921` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2082` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2152` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2544` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2340` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2349` (lexical_call_candidate).
- do_bash: `src/fight.c:2235` (lexical_call_candidate).
- do_dirt: `src/fight.c:2366` (lexical_call_candidate).
- do_trip: `src/fight.c:2500` (lexical_call_candidate).
- do_kill: `src/fight.c:2601` (lexical_call_candidate).
- do_murder: `src/fight.c:2679` (lexical_call_candidate).
- do_backstab: `src/fight.c:2747` (lexical_call_candidate).
- do_rescue: `src/fight.c:2876` (lexical_call_candidate).
- do_slay: `src/fight.c:3072` (lexical_call_candidate).
- get_char_world: `src/handler.c:2049` (lexical_call_candidate).
- check_social: `src/interp.c:589` (lexical_call_candidate).
- do_cast: `src/magic.c:373` (lexical_call_candidate).
- do_cast: `src/magic.c:417` (lexical_call_candidate).
- do_cast: `src/magic.c:467` (lexical_call_candidate).
- do_cast: `src/magic.c:510` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2236` (declaration_or_dispatch_reference).

Dependencies: `number_argument`, `str_cmp`, `can_see`, `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_char_room.if.001` | 2023 | `if ( !str_cmp( arg, "self" ) )` |  | pending |
| `handler.get_char_room.return.001` | 2024 | `return ch;` |  | pending |
| `handler.get_char_room.for.001` | 2025 | `for ( rch = ch->in_room->people; rch != NULL; rch = rch->next_in_room )` |  | pending |
| `handler.get_char_room.if.002` | 2027 | `if ( !can_see( ch, rch ) \|\| !is_name( arg, rch->name ) )` |  | pending |
| `handler.get_char_room.or.001` | 2027 | `\|\| !is_name( arg, rch->name ) )` |  | pending |
| `handler.get_char_room.continue.001` | 2028 | `continue;` |  | pending |
| `handler.get_char_room.if.003` | 2029 | `if ( ++count == number )` |  | pending |
| `handler.get_char_room.return.002` | 2030 | `return rch;` |  | pending |
| `handler.get_char_room.return.003` | 2033 | `return NULL;` |  | pending |

## get_char_world

[Source line 2042](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2042); ends at line 2064. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_tell: `src/act_comm.c:847` (lexical_call_candidate).
- do_guild: `src/act_wiz.c:192` (lexical_call_candidate).
- do_nochannels: `src/act_wiz.c:308` (lexical_call_candidate).
- do_deny: `src/act_wiz.c:510` (lexical_call_candidate).
- do_disconnect: `src/act_wiz.c:571` (lexical_call_candidate).
- do_pardon: `src/act_wiz.c:615` (lexical_call_candidate).
- do_pecho: `src/act_wiz.c:744` (lexical_call_candidate).
- find_location: `src/act_wiz.c:769` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:837` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1084` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1539` (lexical_call_candidate).
- do_protect: `src/act_wiz.c:2074` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2111` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2200` (lexical_call_candidate).
- do_purge: `src/act_wiz.c:2581` (lexical_call_candidate).
- do_advance: `src/act_wiz.c:2641` (lexical_call_candidate).
- do_trust: `src/act_wiz.c:2731` (lexical_call_candidate).
- do_restore: `src/act_wiz.c:2819` (lexical_call_candidate).
- do_freeze: `src/act_wiz.c:2856` (lexical_call_candidate).
- do_log: `src/act_wiz.c:2926` (lexical_call_candidate).
- do_noemote: `src/act_wiz.c:2970` (lexical_call_candidate).
- do_noshout: `src/act_wiz.c:3018` (lexical_call_candidate).
- do_notell: `src/act_wiz.c:3071` (lexical_call_candidate).
- do_sset: `src/act_wiz.c:3271` (lexical_call_candidate).
- do_mset: `src/act_wiz.c:3349` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3727` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4186` (lexical_call_candidate).
- do_flag: `src/flags.c:93` (lexical_call_candidate).
- spell_gate: `src/magic.c:2888` (lexical_call_candidate).
- spell_summon: `src/magic.c:4319` (lexical_call_candidate).
- spell_portal: `src/magic2.c:61` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:113` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2237` (declaration_or_dispatch_reference).

Dependencies: `get_char_room`, `number_argument`, `can_see`, `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_char_world.if.001` | 2049 | `if ( ( wch = get_char_room( ch, argument ) ) != NULL )` |  | pending |
| `handler.get_char_world.return.001` | 2050 | `return wch;` |  | pending |
| `handler.get_char_world.for.001` | 2054 | `for ( wch = char_list; wch != NULL ; wch = wch->next )` |  | pending |
| `handler.get_char_world.if.002` | 2056 | `if ( wch->in_room == NULL \|\| !can_see( ch, wch )  	\|\|   !is_name( arg, wch->name ) )` |  | pending |
| `handler.get_char_world.or.001` | 2056 | `\|\| !can_see( ch, wch )` |  | pending |
| `handler.get_char_world.or.002` | 2057 | `\|\|   !is_name( arg, wch->name ) )` |  | pending |
| `handler.get_char_world.continue.001` | 2058 | `continue;` |  | pending |
| `handler.get_char_world.if.003` | 2059 | `if ( ++count == number )` |  | pending |
| `handler.get_char_world.return.002` | 2060 | `return wch;` |  | pending |
| `handler.get_char_world.return.003` | 2063 | `return NULL;` |  | pending |

## get_obj_type

[Source line 2072](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2072); ends at line 2083. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- reset_area: `src/db.c:1343` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2238` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_obj_type.for.001` | 2076 | `for ( obj = object_list; obj != NULL; obj = obj->next )` |  | pending |
| `handler.get_obj_type.if.001` | 2078 | `if ( obj->pIndexData == pObjIndex )` |  | pending |
| `handler.get_obj_type.return.001` | 2079 | `return obj;` |  | pending |
| `handler.get_obj_type.return.002` | 2082 | `return NULL;` |  | pending |

## get_obj_list

[Source line 2089](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2089); ends at line 2108. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_enter: `src/act_enter.c:80` (lexical_call_candidate).
- do_stand: `src/act_move.c:882` (lexical_call_candidate).
- do_rest: `src/act_move.c:988` (lexical_call_candidate).
- do_sit: `src/act_move.c:1123` (lexical_call_candidate).
- do_sleep: `src/act_move.c:1254` (lexical_call_candidate).
- do_get: `src/act_obj.c:219` (lexical_call_candidate).
- do_get: `src/act_obj.c:297` (lexical_call_candidate).
- do_envenom: `src/act_obj.c:840` (lexical_call_candidate).
- do_sacrifice: `src/act_obj.c:1763` (lexical_call_candidate).
- damage: `src/fight.c:909` (lexical_call_candidate).
- damage: `src/fight.c:914` (lexical_call_candidate).
- damage: `src/fight.c:926` (lexical_call_candidate).
- get_obj_here: `src/handler.c:2175` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2239` (declaration_or_dispatch_reference).

Dependencies: `number_argument`, `can_see_obj`, `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_obj_list.for.001` | 2098 | `for ( obj = list; obj != NULL; obj = obj->next_content )` |  | pending |
| `handler.get_obj_list.if.001` | 2100 | `if ( can_see_obj( ch, obj ) && is_name( arg, obj->name ) )` |  | pending |
| `handler.get_obj_list.and.001` | 2100 | `&& is_name( arg, obj->name ) )` |  | pending |
| `handler.get_obj_list.if.002` | 2102 | `if ( ++count == number )` |  | pending |
| `handler.get_obj_list.return.001` | 2103 | `return obj;` |  | pending |
| `handler.get_obj_list.return.002` | 2107 | `return NULL;` |  | pending |

## get_obj_carry

[Source line 2115](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2115); ends at line 2136. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_compare: `src/act_info.c:2167` (lexical_call_candidate).
- do_compare: `src/act_info.c:2191` (lexical_call_candidate).
- do_put: `src/act_obj.c:391` (lexical_call_candidate).
- do_drop: `src/act_obj.c:588` (lexical_call_candidate).
- do_give: `src/act_obj.c:767` (lexical_call_candidate).
- do_fill: `src/act_obj.c:957` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1025` (lexical_call_candidate).
- do_eat: `src/act_obj.c:1271` (lexical_call_candidate).
- do_wear: `src/act_obj.c:1700` (lexical_call_candidate).
- do_quaff: `src/act_obj.c:1853` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1895` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2274` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2864` (lexical_call_candidate).
- do_value: `src/act_obj.c:2956` (lexical_call_candidate).
- get_obj_here: `src/handler.c:2179` (lexical_call_candidate).
- do_cast: `src/magic.c:446` (lexical_call_candidate).
- do_cast: `src/magic.c:515` (lexical_call_candidate).
- spell_continual_light: `src/magic.c:1437` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2241` (declaration_or_dispatch_reference).

Dependencies: `number_argument`, `can_see_obj`, `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_obj_carry.for.001` | 2124 | `for ( obj = ch->carrying; obj != NULL; obj = obj->next_content )` |  | pending |
| `handler.get_obj_carry.if.001` | 2126 | `if ( obj->wear_loc == WEAR_NONE 	&&   (can_see_obj( viewer, obj ) )  	&&   is_name( arg, obj->name ) )` |  | pending |
| `handler.get_obj_carry.and.001` | 2127 | `&&   (can_see_obj( viewer, obj ) )` |  | pending |
| `handler.get_obj_carry.and.002` | 2128 | `&&   is_name( arg, obj->name ) )` |  | pending |
| `handler.get_obj_carry.if.002` | 2130 | `if ( ++count == number )` |  | pending |
| `handler.get_obj_carry.return.001` | 2131 | `return obj;` |  | pending |
| `handler.get_obj_carry.return.002` | 2135 | `return NULL;` |  | pending |

## get_obj_wear

[Source line 2143](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2143); ends at line 2164. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_remove: `src/act_obj.c:1727` (lexical_call_candidate).
- get_obj_here: `src/handler.c:2182` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2243` (declaration_or_dispatch_reference).

Dependencies: `number_argument`, `can_see_obj`, `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_obj_wear.for.001` | 2152 | `for ( obj = ch->carrying; obj != NULL; obj = obj->next_content )` |  | pending |
| `handler.get_obj_wear.if.001` | 2154 | `if ( obj->wear_loc != WEAR_NONE 	&&   can_see_obj( ch, obj ) 	&&   is_name( arg, obj->name ) )` |  | pending |
| `handler.get_obj_wear.and.001` | 2155 | `&&   can_see_obj( ch, obj )` |  | pending |
| `handler.get_obj_wear.and.002` | 2156 | `&&   is_name( arg, obj->name ) )` |  | pending |
| `handler.get_obj_wear.if.002` | 2158 | `if ( ++count == number )` |  | pending |
| `handler.get_obj_wear.return.001` | 2159 | `return obj;` |  | pending |
| `handler.get_obj_wear.return.002` | 2163 | `return NULL;` |  | pending |

## get_obj_here

[Source line 2171](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2171); ends at line 2186. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_look: `src/act_info.c:1065` (lexical_call_candidate).
- do_examine: `src/act_info.c:1263` (lexical_call_candidate).
- do_open: `src/act_move.c:343` (lexical_call_candidate).
- do_close: `src/act_move.c:437` (lexical_call_candidate).
- do_lock: `src/act_move.c:538` (lexical_call_candidate).
- do_unlock: `src/act_move.c:646` (lexical_call_candidate).
- do_pick: `src/act_move.c:775` (lexical_call_candidate).
- do_get: `src/act_obj.c:261` (lexical_call_candidate).
- do_put: `src/act_obj.c:370` (lexical_call_candidate).
- do_pour: `src/act_obj.c:1057` (lexical_call_candidate).
- do_drink: `src/act_obj.c:1161` (lexical_call_candidate).
- do_recite: `src/act_obj.c:1922` (lexical_call_candidate).
- do_zap: `src/act_obj.c:2083` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2330` (lexical_call_candidate).
- do_clone: `src/act_wiz.c:2350` (lexical_call_candidate).
- get_obj_world: `src/handler.c:2200` (lexical_call_candidate).
- do_cast: `src/magic.c:492` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2244` (declaration_or_dispatch_reference).

Dependencies: `get_obj_list`, `get_obj_carry`, `get_obj_wear`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_obj_here.if.001` | 2176 | `if ( obj != NULL )` |  | pending |
| `handler.get_obj_here.return.001` | 2177 | `return obj;` |  | pending |
| `handler.get_obj_here.if.002` | 2179 | `if ( ( obj = get_obj_carry( ch, argument, ch ) ) != NULL )` |  | pending |
| `handler.get_obj_here.return.002` | 2180 | `return obj;` |  | pending |
| `handler.get_obj_here.if.003` | 2182 | `if ( ( obj = get_obj_wear( ch, argument ) ) != NULL )` |  | pending |
| `handler.get_obj_here.return.003` | 2183 | `return obj;` |  | pending |
| `handler.get_obj_here.return.004` | 2185 | `return NULL;` |  | pending |

## get_obj_world

[Source line 2193](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2193); ends at line 2215. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- find_location: `src/act_wiz.c:772` (lexical_call_candidate).
- do_stat: `src/act_wiz.c:1077` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1219` (lexical_call_candidate).
- do_string: `src/act_wiz.c:3806` (lexical_call_candidate).
- do_oset: `src/act_wiz.c:3887` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2245` (declaration_or_dispatch_reference).

Dependencies: `get_obj_here`, `number_argument`, `can_see_obj`, `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_obj_world.if.001` | 2200 | `if ( ( obj = get_obj_here( ch, argument ) ) != NULL )` |  | pending |
| `handler.get_obj_world.return.001` | 2201 | `return obj;` |  | pending |
| `handler.get_obj_world.for.001` | 2205 | `for ( obj = object_list; obj != NULL; obj = obj->next )` |  | pending |
| `handler.get_obj_world.if.002` | 2207 | `if ( can_see_obj( ch, obj ) && is_name( arg, obj->name ) )` |  | pending |
| `handler.get_obj_world.and.001` | 2207 | `&& is_name( arg, obj->name ) )` |  | pending |
| `handler.get_obj_world.if.003` | 2209 | `if ( ++count == number )` |  | pending |
| `handler.get_obj_world.return.002` | 2210 | `return obj;` |  | pending |
| `handler.get_obj_world.return.003` | 2214 | `return NULL;` |  | pending |

## deduct_cost

[Source line 2219](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2219); ends at line 2244. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_buy: `src/act_obj.c:2585` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2717` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2912` (lexical_call_candidate).
- do_heal: `src/healer.c:179` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2185` (declaration_or_dispatch_reference).

Dependencies: `UMIN`, `bug`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.deduct_cost.if.001` | 2225 | `if (silver < cost)` | handler.deduct_cost.silver-only, handler.deduct_cost.gold-exact, handler.deduct_cost.gold-change, handler.deduct_cost.mixed-change, handler.deduct_cost.zero, handler.deduct_cost.negative-cost-credits, handler.deduct_cost.insufficient-gold-clamped | specified |
| `handler.deduct_cost.if.002` | 2234 | `if (ch->gold < 0)` | handler.deduct_cost.silver-only, handler.deduct_cost.gold-exact, handler.deduct_cost.gold-change, handler.deduct_cost.mixed-change, handler.deduct_cost.zero, handler.deduct_cost.negative-cost-credits, handler.deduct_cost.insufficient-gold-clamped | specified |
| `handler.deduct_cost.if.003` | 2239 | `if (ch->silver < 0)` | handler.deduct_cost.silver-only, handler.deduct_cost.gold-exact, handler.deduct_cost.gold-change, handler.deduct_cost.mixed-change, handler.deduct_cost.zero, handler.deduct_cost.negative-cost-credits, handler.deduct_cost.insufficient-gold-clamped | specified |
| `handler.deduct_cost.silver-only.path` | 2223 | `silver only` | handler.deduct_cost.silver-only | specified |
| `handler.deduct_cost.gold-exact.path` | 2223 | `gold exact` | handler.deduct_cost.gold-exact | specified |
| `handler.deduct_cost.gold-change.path` | 2223 | `gold change` | handler.deduct_cost.gold-change | specified |
| `handler.deduct_cost.mixed-change.path` | 2223 | `mixed change` | handler.deduct_cost.mixed-change | specified |
| `handler.deduct_cost.zero.path` | 2223 | `zero` | handler.deduct_cost.zero | specified |
| `handler.deduct_cost.negative-cost-credits.path` | 2223 | `negative cost credits` | handler.deduct_cost.negative-cost-credits | specified |
| `handler.deduct_cost.insufficient-gold-clamped.path` | 2223 | `insufficient gold clamped` | handler.deduct_cost.insufficient-gold-clamped | specified |

## create_money

[Source line 2248](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2248); ends at line 2302. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_drop: `src/act_obj.c:579` (lexical_call_candidate).
- make_corpse: `src/fight.c:1442` (lexical_call_candidate).
- make_corpse: `src/fight.c:1461` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2246` (declaration_or_dispatch_reference).

Dependencies: `bug`, `UMIN`, `UMAX`, `create_object`, `get_obj_index`, `sprintf`, `free_string`, `str_dup`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.create_money.if.001` | 2253 | `if ( gold < 0 \|\| silver < 0 \|\| (gold == 0 && silver == 0) )` |  | pending |
| `handler.create_money.or.001` | 2253 | `\|\| silver < 0 \|\| (gold == 0 && silver == 0) )` |  | pending |
| `handler.create_money.or.002` | 2253 | `\|\| (gold == 0 && silver == 0) )` |  | pending |
| `handler.create_money.and.001` | 2253 | `&& silver == 0) )` |  | pending |
| `handler.create_money.if.002` | 2260 | `if (gold == 0 && silver == 1)` |  | pending |
| `handler.create_money.and.002` | 2260 | `&& silver == 1)` |  | pending |
| `handler.create_money.if.003` | 2264 | `if (gold == 1 && silver == 0)` |  | pending |
| `handler.create_money.and.003` | 2264 | `&& silver == 0)` |  | pending |
| `handler.create_money.if.004` | 2268 | `if (silver == 0)` |  | pending |
| `handler.create_money.if.005` | 2278 | `if (gold == 0)` |  | pending |
| `handler.create_money.return.001` | 2301 | `return obj;` |  | pending |

## get_obj_number

[Source line 2310](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2310); ends at line 2324. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- get_obj: `src/act_obj.c:102` (lexical_call_candidate).
- do_give: `src/act_obj.c:799` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2288` (lexical_call_candidate).
- obj_to_keeper: `src/act_obj.c:2416` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2682` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1243` (lexical_call_candidate).
- obj_to_char: `src/handler.c:1470` (lexical_call_candidate).
- obj_from_char: `src/handler.c:1515` (lexical_call_candidate).
- obj_to_obj: `src/handler.c:1804` (lexical_call_candidate).
- obj_from_obj: `src/handler.c:1859` (lexical_call_candidate).
- get_obj_number: `src/handler.c:2321` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2247` (declaration_or_dispatch_reference).

Dependencies: `get_obj_number`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_obj_number.if.001` | 2314 | `if (obj->item_type == ITEM_CONTAINER \|\| obj->item_type == ITEM_MONEY     \|\|  obj->item_type == ITEM_GEM \|\| obj->item_type == ITEM_JEWELRY)` |  | pending |
| `handler.get_obj_number.or.001` | 2314 | `\|\| obj->item_type == ITEM_MONEY` |  | pending |
| `handler.get_obj_number.or.002` | 2315 | `\|\|  obj->item_type == ITEM_GEM \|\| obj->item_type == ITEM_JEWELRY)` |  | pending |
| `handler.get_obj_number.or.003` | 2315 | `\|\| obj->item_type == ITEM_JEWELRY)` |  | pending |
| `handler.get_obj_number.for.001` | 2320 | `for ( obj = obj->contains; obj != NULL; obj = obj->next_content )` |  | pending |
| `handler.get_obj_number.return.001` | 2323 | `return number;` |  | pending |

## get_obj_weight

[Source line 2330](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2330); ends at line 2340. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- get_obj: `src/act_obj.c:110` (lexical_call_candidate).
- do_put: `src/act_obj.c:415` (lexical_call_candidate).
- do_put: `src/act_obj.c:417` (lexical_call_candidate).
- do_put: `src/act_obj.c:457` (lexical_call_candidate).
- do_put: `src/act_obj.c:459` (lexical_call_candidate).
- do_give: `src/act_obj.c:805` (lexical_call_candidate).
- wear_obj: `src/act_obj.c:1600` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2294` (lexical_call_candidate).
- obj_to_keeper: `src/act_obj.c:2417` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2688` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1244` (lexical_call_candidate).
- affect_modify: `src/handler.c:984` (lexical_call_candidate).
- obj_to_char: `src/handler.c:1471` (lexical_call_candidate).
- obj_from_char: `src/handler.c:1516` (lexical_call_candidate).
- obj_to_obj: `src/handler.c:1805` (lexical_call_candidate).
- obj_from_obj: `src/handler.c:1860` (lexical_call_candidate).
- get_obj_weight: `src/handler.c:2337` (lexical_call_candidate).
- get_true_weight: `src/handler.c:2348` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2248` (declaration_or_dispatch_reference).

Dependencies: `get_obj_weight`, `WEIGHT_MULT`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_obj_weight.for.001` | 2336 | `for ( tobj = obj->contains; tobj != NULL; tobj = tobj->next_content )` |  | pending |
| `handler.get_obj_weight.return.001` | 2339 | `return weight;` |  | pending |

## get_true_weight

[Source line 2342](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2342); ends at line 2351. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_put: `src/act_obj.c:415` (lexical_call_candidate).
- do_put: `src/act_obj.c:457` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1244` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2249` (declaration_or_dispatch_reference).

Dependencies: `get_obj_weight`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.get_true_weight.for.001` | 2347 | `for ( obj = obj->contains; obj != NULL; obj = obj->next_content )` |  | pending |
| `handler.get_true_weight.return.001` | 2350 | `return weight;` |  | pending |

## room_is_dark

[Source line 2356](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2356); ends at line 2373. Status: traced.

Entry references (reviewed in the completion record):

Completed contract and caller audit: [room_is_dark completion](../darkness-completion.md). No remaining gaps for this function.

- show_char_to_char: `src/act_info.c:510` (lexical_call_candidate).
- do_look: `src/act_info.c:1013` (lexical_call_candidate).
- do_exits: `src/act_info.c:1356` (lexical_call_candidate).
- bust_a_prompt: `src/comm.c:1423` (lexical_call_candidate).
- can_see: `src/handler.c:2462` (lexical_call_candidate).
- can_see_obj: `src/handler.c:2518` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2250` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.room_is_dark.if.001` | 2358 | `if ( pRoomIndex->light > 0 )` | handler.room_is_dark.positive-light-beats-dark, handler.room_is_dark.zero-light-dark-flag, handler.room_is_dark.negative-light-dark-flag, handler.room_is_dark.inside-at-night, handler.room_is_dark.city-at-night, handler.room_is_dark.field-at-sunset, handler.room_is_dark.field-at-night, handler.room_is_dark.field-day, handler.room_is_dark.field-sunrise, handler.room_is_dark.matrix-sect_inside-sun_rise, handler.room_is_dark.matrix-sect_inside-sun_light, handler.room_is_dark.matrix-sect_inside-sun_set, handler.room_is_dark.matrix-sect_city-sun_rise, handler.room_is_dark.matrix-sect_city-sun_light, handler.room_is_dark.matrix-sect_city-sun_set, handler.room_is_dark.matrix-sect_forest-sun_dark, handler.room_is_dark.matrix-sect_forest-sun_rise, handler.room_is_dark.matrix-sect_forest-sun_light, handler.room_is_dark.matrix-sect_forest-sun_set, handler.room_is_dark.matrix-sect_hills-sun_dark, handler.room_is_dark.matrix-sect_hills-sun_rise, handler.room_is_dark.matrix-sect_hills-sun_light, handler.room_is_dark.matrix-sect_hills-sun_set, handler.room_is_dark.matrix-sect_mountain-sun_dark, handler.room_is_dark.matrix-sect_mountain-sun_rise, handler.room_is_dark.matrix-sect_mountain-sun_light, handler.room_is_dark.matrix-sect_mountain-sun_set, handler.room_is_dark.matrix-sect_water_swim-sun_dark, handler.room_is_dark.matrix-sect_water_swim-sun_rise, handler.room_is_dark.matrix-sect_water_swim-sun_light, handler.room_is_dark.matrix-sect_water_swim-sun_set, handler.room_is_dark.matrix-sect_water_noswim-sun_dark, handler.room_is_dark.matrix-sect_water_noswim-sun_rise, handler.room_is_dark.matrix-sect_water_noswim-sun_light, handler.room_is_dark.matrix-sect_water_noswim-sun_set, handler.room_is_dark.matrix-sect_unused-sun_dark, handler.room_is_dark.matrix-sect_unused-sun_rise, handler.room_is_dark.matrix-sect_unused-sun_light, handler.room_is_dark.matrix-sect_unused-sun_set, handler.room_is_dark.matrix-sect_air-sun_dark, handler.room_is_dark.matrix-sect_air-sun_rise, handler.room_is_dark.matrix-sect_air-sun_light, handler.room_is_dark.matrix-sect_air-sun_set, handler.room_is_dark.matrix-sect_desert-sun_dark, handler.room_is_dark.matrix-sect_desert-sun_rise, handler.room_is_dark.matrix-sect_desert-sun_light, handler.room_is_dark.matrix-sect_desert-sun_set, handler.room_is_dark.light-boundary--32768-dark-inside, handler.room_is_dark.light-boundary--1-dark-inside, handler.room_is_dark.light-boundary-0-dark-inside, handler.room_is_dark.light-boundary-1-dark-inside, handler.room_is_dark.light-boundary-32767-dark-inside, handler.room_is_dark.negative-light--32768-sun_light, handler.room_is_dark.negative-light--32768-sun_dark, handler.room_is_dark.negative-light--1-sun_light, handler.room_is_dark.negative-light--1-sun_dark, handler.room_is_dark.unrelated-flag-does-not-light-room, handler.room_is_dark.unknown-sunlight-falls-through, handler.room_is_dark.unknown-sector-uses-weather | specified |
| `handler.room_is_dark.return.001` | 2359 | `return FALSE;` | handler.room_is_dark.positive-light-beats-dark, handler.room_is_dark.light-boundary-1-dark-inside, handler.room_is_dark.light-boundary-32767-dark-inside | specified |
| `handler.room_is_dark.if.002` | 2361 | `if ( IS_SET(pRoomIndex->room_flags, ROOM_DARK) )` | handler.room_is_dark.zero-light-dark-flag, handler.room_is_dark.negative-light-dark-flag, handler.room_is_dark.inside-at-night, handler.room_is_dark.city-at-night, handler.room_is_dark.field-at-sunset, handler.room_is_dark.field-at-night, handler.room_is_dark.field-day, handler.room_is_dark.field-sunrise, handler.room_is_dark.matrix-sect_inside-sun_rise, handler.room_is_dark.matrix-sect_inside-sun_light, handler.room_is_dark.matrix-sect_inside-sun_set, handler.room_is_dark.matrix-sect_city-sun_rise, handler.room_is_dark.matrix-sect_city-sun_light, handler.room_is_dark.matrix-sect_city-sun_set, handler.room_is_dark.matrix-sect_forest-sun_dark, handler.room_is_dark.matrix-sect_forest-sun_rise, handler.room_is_dark.matrix-sect_forest-sun_light, handler.room_is_dark.matrix-sect_forest-sun_set, handler.room_is_dark.matrix-sect_hills-sun_dark, handler.room_is_dark.matrix-sect_hills-sun_rise, handler.room_is_dark.matrix-sect_hills-sun_light, handler.room_is_dark.matrix-sect_hills-sun_set, handler.room_is_dark.matrix-sect_mountain-sun_dark, handler.room_is_dark.matrix-sect_mountain-sun_rise, handler.room_is_dark.matrix-sect_mountain-sun_light, handler.room_is_dark.matrix-sect_mountain-sun_set, handler.room_is_dark.matrix-sect_water_swim-sun_dark, handler.room_is_dark.matrix-sect_water_swim-sun_rise, handler.room_is_dark.matrix-sect_water_swim-sun_light, handler.room_is_dark.matrix-sect_water_swim-sun_set, handler.room_is_dark.matrix-sect_water_noswim-sun_dark, handler.room_is_dark.matrix-sect_water_noswim-sun_rise, handler.room_is_dark.matrix-sect_water_noswim-sun_light, handler.room_is_dark.matrix-sect_water_noswim-sun_set, handler.room_is_dark.matrix-sect_unused-sun_dark, handler.room_is_dark.matrix-sect_unused-sun_rise, handler.room_is_dark.matrix-sect_unused-sun_light, handler.room_is_dark.matrix-sect_unused-sun_set, handler.room_is_dark.matrix-sect_air-sun_dark, handler.room_is_dark.matrix-sect_air-sun_rise, handler.room_is_dark.matrix-sect_air-sun_light, handler.room_is_dark.matrix-sect_air-sun_set, handler.room_is_dark.matrix-sect_desert-sun_dark, handler.room_is_dark.matrix-sect_desert-sun_rise, handler.room_is_dark.matrix-sect_desert-sun_light, handler.room_is_dark.matrix-sect_desert-sun_set, handler.room_is_dark.light-boundary--32768-dark-inside, handler.room_is_dark.light-boundary--1-dark-inside, handler.room_is_dark.light-boundary-0-dark-inside, handler.room_is_dark.negative-light--32768-sun_light, handler.room_is_dark.negative-light--32768-sun_dark, handler.room_is_dark.negative-light--1-sun_light, handler.room_is_dark.negative-light--1-sun_dark, handler.room_is_dark.unrelated-flag-does-not-light-room, handler.room_is_dark.unknown-sunlight-falls-through, handler.room_is_dark.unknown-sector-uses-weather | specified |
| `handler.room_is_dark.return.002` | 2362 | `return TRUE;` | handler.room_is_dark.zero-light-dark-flag, handler.room_is_dark.negative-light-dark-flag, handler.room_is_dark.light-boundary--32768-dark-inside, handler.room_is_dark.light-boundary--1-dark-inside, handler.room_is_dark.light-boundary-0-dark-inside | specified |
| `handler.room_is_dark.if.003` | 2364 | `if ( pRoomIndex->sector_type == SECT_INSIDE     \|\|   pRoomIndex->sector_type == SECT_CITY )` | handler.room_is_dark.inside-at-night, handler.room_is_dark.city-at-night, handler.room_is_dark.field-at-sunset, handler.room_is_dark.field-at-night, handler.room_is_dark.field-day, handler.room_is_dark.field-sunrise, handler.room_is_dark.matrix-sect_inside-sun_rise, handler.room_is_dark.matrix-sect_inside-sun_light, handler.room_is_dark.matrix-sect_inside-sun_set, handler.room_is_dark.matrix-sect_city-sun_rise, handler.room_is_dark.matrix-sect_city-sun_light, handler.room_is_dark.matrix-sect_city-sun_set, handler.room_is_dark.matrix-sect_forest-sun_dark, handler.room_is_dark.matrix-sect_forest-sun_rise, handler.room_is_dark.matrix-sect_forest-sun_light, handler.room_is_dark.matrix-sect_forest-sun_set, handler.room_is_dark.matrix-sect_hills-sun_dark, handler.room_is_dark.matrix-sect_hills-sun_rise, handler.room_is_dark.matrix-sect_hills-sun_light, handler.room_is_dark.matrix-sect_hills-sun_set, handler.room_is_dark.matrix-sect_mountain-sun_dark, handler.room_is_dark.matrix-sect_mountain-sun_rise, handler.room_is_dark.matrix-sect_mountain-sun_light, handler.room_is_dark.matrix-sect_mountain-sun_set, handler.room_is_dark.matrix-sect_water_swim-sun_dark, handler.room_is_dark.matrix-sect_water_swim-sun_rise, handler.room_is_dark.matrix-sect_water_swim-sun_light, handler.room_is_dark.matrix-sect_water_swim-sun_set, handler.room_is_dark.matrix-sect_water_noswim-sun_dark, handler.room_is_dark.matrix-sect_water_noswim-sun_rise, handler.room_is_dark.matrix-sect_water_noswim-sun_light, handler.room_is_dark.matrix-sect_water_noswim-sun_set, handler.room_is_dark.matrix-sect_unused-sun_dark, handler.room_is_dark.matrix-sect_unused-sun_rise, handler.room_is_dark.matrix-sect_unused-sun_light, handler.room_is_dark.matrix-sect_unused-sun_set, handler.room_is_dark.matrix-sect_air-sun_dark, handler.room_is_dark.matrix-sect_air-sun_rise, handler.room_is_dark.matrix-sect_air-sun_light, handler.room_is_dark.matrix-sect_air-sun_set, handler.room_is_dark.matrix-sect_desert-sun_dark, handler.room_is_dark.matrix-sect_desert-sun_rise, handler.room_is_dark.matrix-sect_desert-sun_light, handler.room_is_dark.matrix-sect_desert-sun_set, handler.room_is_dark.negative-light--32768-sun_light, handler.room_is_dark.negative-light--32768-sun_dark, handler.room_is_dark.negative-light--1-sun_light, handler.room_is_dark.negative-light--1-sun_dark, handler.room_is_dark.unrelated-flag-does-not-light-room, handler.room_is_dark.unknown-sunlight-falls-through, handler.room_is_dark.unknown-sector-uses-weather | specified |
| `handler.room_is_dark.or.001` | 2365 | `\|\|   pRoomIndex->sector_type == SECT_CITY )` | handler.room_is_dark.inside-at-night, handler.room_is_dark.city-at-night, handler.room_is_dark.field-at-sunset, handler.room_is_dark.field-at-night, handler.room_is_dark.field-day, handler.room_is_dark.field-sunrise, handler.room_is_dark.matrix-sect_inside-sun_rise, handler.room_is_dark.matrix-sect_inside-sun_light, handler.room_is_dark.matrix-sect_inside-sun_set, handler.room_is_dark.matrix-sect_city-sun_rise, handler.room_is_dark.matrix-sect_city-sun_light, handler.room_is_dark.matrix-sect_city-sun_set, handler.room_is_dark.matrix-sect_forest-sun_dark, handler.room_is_dark.matrix-sect_forest-sun_rise, handler.room_is_dark.matrix-sect_forest-sun_light, handler.room_is_dark.matrix-sect_forest-sun_set, handler.room_is_dark.matrix-sect_hills-sun_dark, handler.room_is_dark.matrix-sect_hills-sun_rise, handler.room_is_dark.matrix-sect_hills-sun_light, handler.room_is_dark.matrix-sect_hills-sun_set, handler.room_is_dark.matrix-sect_mountain-sun_dark, handler.room_is_dark.matrix-sect_mountain-sun_rise, handler.room_is_dark.matrix-sect_mountain-sun_light, handler.room_is_dark.matrix-sect_mountain-sun_set, handler.room_is_dark.matrix-sect_water_swim-sun_dark, handler.room_is_dark.matrix-sect_water_swim-sun_rise, handler.room_is_dark.matrix-sect_water_swim-sun_light, handler.room_is_dark.matrix-sect_water_swim-sun_set, handler.room_is_dark.matrix-sect_water_noswim-sun_dark, handler.room_is_dark.matrix-sect_water_noswim-sun_rise, handler.room_is_dark.matrix-sect_water_noswim-sun_light, handler.room_is_dark.matrix-sect_water_noswim-sun_set, handler.room_is_dark.matrix-sect_unused-sun_dark, handler.room_is_dark.matrix-sect_unused-sun_rise, handler.room_is_dark.matrix-sect_unused-sun_light, handler.room_is_dark.matrix-sect_unused-sun_set, handler.room_is_dark.matrix-sect_air-sun_dark, handler.room_is_dark.matrix-sect_air-sun_rise, handler.room_is_dark.matrix-sect_air-sun_light, handler.room_is_dark.matrix-sect_air-sun_set, handler.room_is_dark.matrix-sect_desert-sun_dark, handler.room_is_dark.matrix-sect_desert-sun_rise, handler.room_is_dark.matrix-sect_desert-sun_light, handler.room_is_dark.matrix-sect_desert-sun_set, handler.room_is_dark.negative-light--32768-sun_light, handler.room_is_dark.negative-light--32768-sun_dark, handler.room_is_dark.negative-light--1-sun_light, handler.room_is_dark.negative-light--1-sun_dark, handler.room_is_dark.unrelated-flag-does-not-light-room, handler.room_is_dark.unknown-sunlight-falls-through, handler.room_is_dark.unknown-sector-uses-weather | specified |
| `handler.room_is_dark.return.003` | 2366 | `return FALSE;` | handler.room_is_dark.inside-at-night, handler.room_is_dark.city-at-night, handler.room_is_dark.matrix-sect_inside-sun_rise, handler.room_is_dark.matrix-sect_inside-sun_light, handler.room_is_dark.matrix-sect_inside-sun_set, handler.room_is_dark.matrix-sect_city-sun_rise, handler.room_is_dark.matrix-sect_city-sun_light, handler.room_is_dark.matrix-sect_city-sun_set | specified |
| `handler.room_is_dark.if.004` | 2368 | `if ( weather_info.sunlight == SUN_SET     \|\|   weather_info.sunlight == SUN_DARK )` | handler.room_is_dark.field-at-sunset, handler.room_is_dark.field-at-night, handler.room_is_dark.field-day, handler.room_is_dark.field-sunrise, handler.room_is_dark.matrix-sect_forest-sun_dark, handler.room_is_dark.matrix-sect_forest-sun_rise, handler.room_is_dark.matrix-sect_forest-sun_light, handler.room_is_dark.matrix-sect_forest-sun_set, handler.room_is_dark.matrix-sect_hills-sun_dark, handler.room_is_dark.matrix-sect_hills-sun_rise, handler.room_is_dark.matrix-sect_hills-sun_light, handler.room_is_dark.matrix-sect_hills-sun_set, handler.room_is_dark.matrix-sect_mountain-sun_dark, handler.room_is_dark.matrix-sect_mountain-sun_rise, handler.room_is_dark.matrix-sect_mountain-sun_light, handler.room_is_dark.matrix-sect_mountain-sun_set, handler.room_is_dark.matrix-sect_water_swim-sun_dark, handler.room_is_dark.matrix-sect_water_swim-sun_rise, handler.room_is_dark.matrix-sect_water_swim-sun_light, handler.room_is_dark.matrix-sect_water_swim-sun_set, handler.room_is_dark.matrix-sect_water_noswim-sun_dark, handler.room_is_dark.matrix-sect_water_noswim-sun_rise, handler.room_is_dark.matrix-sect_water_noswim-sun_light, handler.room_is_dark.matrix-sect_water_noswim-sun_set, handler.room_is_dark.matrix-sect_unused-sun_dark, handler.room_is_dark.matrix-sect_unused-sun_rise, handler.room_is_dark.matrix-sect_unused-sun_light, handler.room_is_dark.matrix-sect_unused-sun_set, handler.room_is_dark.matrix-sect_air-sun_dark, handler.room_is_dark.matrix-sect_air-sun_rise, handler.room_is_dark.matrix-sect_air-sun_light, handler.room_is_dark.matrix-sect_air-sun_set, handler.room_is_dark.matrix-sect_desert-sun_dark, handler.room_is_dark.matrix-sect_desert-sun_rise, handler.room_is_dark.matrix-sect_desert-sun_light, handler.room_is_dark.matrix-sect_desert-sun_set, handler.room_is_dark.negative-light--32768-sun_light, handler.room_is_dark.negative-light--32768-sun_dark, handler.room_is_dark.negative-light--1-sun_light, handler.room_is_dark.negative-light--1-sun_dark, handler.room_is_dark.unrelated-flag-does-not-light-room, handler.room_is_dark.unknown-sunlight-falls-through, handler.room_is_dark.unknown-sector-uses-weather | specified |
| `handler.room_is_dark.or.002` | 2369 | `\|\|   weather_info.sunlight == SUN_DARK )` | handler.room_is_dark.field-at-sunset, handler.room_is_dark.field-at-night, handler.room_is_dark.field-day, handler.room_is_dark.field-sunrise, handler.room_is_dark.matrix-sect_forest-sun_dark, handler.room_is_dark.matrix-sect_forest-sun_rise, handler.room_is_dark.matrix-sect_forest-sun_light, handler.room_is_dark.matrix-sect_forest-sun_set, handler.room_is_dark.matrix-sect_hills-sun_dark, handler.room_is_dark.matrix-sect_hills-sun_rise, handler.room_is_dark.matrix-sect_hills-sun_light, handler.room_is_dark.matrix-sect_hills-sun_set, handler.room_is_dark.matrix-sect_mountain-sun_dark, handler.room_is_dark.matrix-sect_mountain-sun_rise, handler.room_is_dark.matrix-sect_mountain-sun_light, handler.room_is_dark.matrix-sect_mountain-sun_set, handler.room_is_dark.matrix-sect_water_swim-sun_dark, handler.room_is_dark.matrix-sect_water_swim-sun_rise, handler.room_is_dark.matrix-sect_water_swim-sun_light, handler.room_is_dark.matrix-sect_water_swim-sun_set, handler.room_is_dark.matrix-sect_water_noswim-sun_dark, handler.room_is_dark.matrix-sect_water_noswim-sun_rise, handler.room_is_dark.matrix-sect_water_noswim-sun_light, handler.room_is_dark.matrix-sect_water_noswim-sun_set, handler.room_is_dark.matrix-sect_unused-sun_dark, handler.room_is_dark.matrix-sect_unused-sun_rise, handler.room_is_dark.matrix-sect_unused-sun_light, handler.room_is_dark.matrix-sect_unused-sun_set, handler.room_is_dark.matrix-sect_air-sun_dark, handler.room_is_dark.matrix-sect_air-sun_rise, handler.room_is_dark.matrix-sect_air-sun_light, handler.room_is_dark.matrix-sect_air-sun_set, handler.room_is_dark.matrix-sect_desert-sun_dark, handler.room_is_dark.matrix-sect_desert-sun_rise, handler.room_is_dark.matrix-sect_desert-sun_light, handler.room_is_dark.matrix-sect_desert-sun_set, handler.room_is_dark.negative-light--32768-sun_light, handler.room_is_dark.negative-light--32768-sun_dark, handler.room_is_dark.negative-light--1-sun_light, handler.room_is_dark.negative-light--1-sun_dark, handler.room_is_dark.unrelated-flag-does-not-light-room, handler.room_is_dark.unknown-sunlight-falls-through, handler.room_is_dark.unknown-sector-uses-weather | specified |
| `handler.room_is_dark.return.004` | 2370 | `return TRUE;` | handler.room_is_dark.field-at-sunset, handler.room_is_dark.field-at-night, handler.room_is_dark.matrix-sect_forest-sun_dark, handler.room_is_dark.matrix-sect_forest-sun_set, handler.room_is_dark.matrix-sect_hills-sun_dark, handler.room_is_dark.matrix-sect_hills-sun_set, handler.room_is_dark.matrix-sect_mountain-sun_dark, handler.room_is_dark.matrix-sect_mountain-sun_set, handler.room_is_dark.matrix-sect_water_swim-sun_dark, handler.room_is_dark.matrix-sect_water_swim-sun_set, handler.room_is_dark.matrix-sect_water_noswim-sun_dark, handler.room_is_dark.matrix-sect_water_noswim-sun_set, handler.room_is_dark.matrix-sect_unused-sun_dark, handler.room_is_dark.matrix-sect_unused-sun_set, handler.room_is_dark.matrix-sect_air-sun_dark, handler.room_is_dark.matrix-sect_air-sun_set, handler.room_is_dark.matrix-sect_desert-sun_dark, handler.room_is_dark.matrix-sect_desert-sun_set, handler.room_is_dark.negative-light--32768-sun_dark, handler.room_is_dark.negative-light--1-sun_dark, handler.room_is_dark.unrelated-flag-does-not-light-room, handler.room_is_dark.unknown-sector-uses-weather | specified |
| `handler.room_is_dark.return.005` | 2372 | `return FALSE;` | handler.room_is_dark.field-day, handler.room_is_dark.field-sunrise, handler.room_is_dark.matrix-sect_forest-sun_rise, handler.room_is_dark.matrix-sect_forest-sun_light, handler.room_is_dark.matrix-sect_hills-sun_rise, handler.room_is_dark.matrix-sect_hills-sun_light, handler.room_is_dark.matrix-sect_mountain-sun_rise, handler.room_is_dark.matrix-sect_mountain-sun_light, handler.room_is_dark.matrix-sect_water_swim-sun_rise, handler.room_is_dark.matrix-sect_water_swim-sun_light, handler.room_is_dark.matrix-sect_water_noswim-sun_rise, handler.room_is_dark.matrix-sect_water_noswim-sun_light, handler.room_is_dark.matrix-sect_unused-sun_rise, handler.room_is_dark.matrix-sect_unused-sun_light, handler.room_is_dark.matrix-sect_air-sun_rise, handler.room_is_dark.matrix-sect_air-sun_light, handler.room_is_dark.matrix-sect_desert-sun_rise, handler.room_is_dark.matrix-sect_desert-sun_light, handler.room_is_dark.negative-light--32768-sun_light, handler.room_is_dark.negative-light--1-sun_light, handler.room_is_dark.unknown-sunlight-falls-through | specified |
| `handler.room_is_dark.positive-light-beats-dark.path` | 2358 | `positive light beats dark` | handler.room_is_dark.positive-light-beats-dark | specified |
| `handler.room_is_dark.zero-light-dark-flag.path` | 2358 | `zero light dark flag` | handler.room_is_dark.zero-light-dark-flag | specified |
| `handler.room_is_dark.negative-light-dark-flag.path` | 2358 | `negative light dark flag` | handler.room_is_dark.negative-light-dark-flag | specified |
| `handler.room_is_dark.inside-at-night.path` | 2358 | `inside at night` | handler.room_is_dark.inside-at-night | specified |
| `handler.room_is_dark.city-at-night.path` | 2358 | `city at night` | handler.room_is_dark.city-at-night | specified |
| `handler.room_is_dark.field-at-sunset.path` | 2358 | `field at sunset` | handler.room_is_dark.field-at-sunset | specified |
| `handler.room_is_dark.field-at-night.path` | 2358 | `field at night` | handler.room_is_dark.field-at-night | specified |
| `handler.room_is_dark.field-day.path` | 2358 | `field day` | handler.room_is_dark.field-day | specified |
| `handler.room_is_dark.field-sunrise.path` | 2358 | `field sunrise` | handler.room_is_dark.field-sunrise | specified |
| `handler.room_is_dark.matrix-sect_inside-sun_rise.path` | 2358 | `matrix sect_inside sun_rise` | handler.room_is_dark.matrix-sect_inside-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_inside-sun_light.path` | 2358 | `matrix sect_inside sun_light` | handler.room_is_dark.matrix-sect_inside-sun_light | specified |
| `handler.room_is_dark.matrix-sect_inside-sun_set.path` | 2358 | `matrix sect_inside sun_set` | handler.room_is_dark.matrix-sect_inside-sun_set | specified |
| `handler.room_is_dark.matrix-sect_city-sun_rise.path` | 2358 | `matrix sect_city sun_rise` | handler.room_is_dark.matrix-sect_city-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_city-sun_light.path` | 2358 | `matrix sect_city sun_light` | handler.room_is_dark.matrix-sect_city-sun_light | specified |
| `handler.room_is_dark.matrix-sect_city-sun_set.path` | 2358 | `matrix sect_city sun_set` | handler.room_is_dark.matrix-sect_city-sun_set | specified |
| `handler.room_is_dark.matrix-sect_forest-sun_dark.path` | 2358 | `matrix sect_forest sun_dark` | handler.room_is_dark.matrix-sect_forest-sun_dark | specified |
| `handler.room_is_dark.matrix-sect_forest-sun_rise.path` | 2358 | `matrix sect_forest sun_rise` | handler.room_is_dark.matrix-sect_forest-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_forest-sun_light.path` | 2358 | `matrix sect_forest sun_light` | handler.room_is_dark.matrix-sect_forest-sun_light | specified |
| `handler.room_is_dark.matrix-sect_forest-sun_set.path` | 2358 | `matrix sect_forest sun_set` | handler.room_is_dark.matrix-sect_forest-sun_set | specified |
| `handler.room_is_dark.matrix-sect_hills-sun_dark.path` | 2358 | `matrix sect_hills sun_dark` | handler.room_is_dark.matrix-sect_hills-sun_dark | specified |
| `handler.room_is_dark.matrix-sect_hills-sun_rise.path` | 2358 | `matrix sect_hills sun_rise` | handler.room_is_dark.matrix-sect_hills-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_hills-sun_light.path` | 2358 | `matrix sect_hills sun_light` | handler.room_is_dark.matrix-sect_hills-sun_light | specified |
| `handler.room_is_dark.matrix-sect_hills-sun_set.path` | 2358 | `matrix sect_hills sun_set` | handler.room_is_dark.matrix-sect_hills-sun_set | specified |
| `handler.room_is_dark.matrix-sect_mountain-sun_dark.path` | 2358 | `matrix sect_mountain sun_dark` | handler.room_is_dark.matrix-sect_mountain-sun_dark | specified |
| `handler.room_is_dark.matrix-sect_mountain-sun_rise.path` | 2358 | `matrix sect_mountain sun_rise` | handler.room_is_dark.matrix-sect_mountain-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_mountain-sun_light.path` | 2358 | `matrix sect_mountain sun_light` | handler.room_is_dark.matrix-sect_mountain-sun_light | specified |
| `handler.room_is_dark.matrix-sect_mountain-sun_set.path` | 2358 | `matrix sect_mountain sun_set` | handler.room_is_dark.matrix-sect_mountain-sun_set | specified |
| `handler.room_is_dark.matrix-sect_water_swim-sun_dark.path` | 2358 | `matrix sect_water_swim sun_dark` | handler.room_is_dark.matrix-sect_water_swim-sun_dark | specified |
| `handler.room_is_dark.matrix-sect_water_swim-sun_rise.path` | 2358 | `matrix sect_water_swim sun_rise` | handler.room_is_dark.matrix-sect_water_swim-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_water_swim-sun_light.path` | 2358 | `matrix sect_water_swim sun_light` | handler.room_is_dark.matrix-sect_water_swim-sun_light | specified |
| `handler.room_is_dark.matrix-sect_water_swim-sun_set.path` | 2358 | `matrix sect_water_swim sun_set` | handler.room_is_dark.matrix-sect_water_swim-sun_set | specified |
| `handler.room_is_dark.matrix-sect_water_noswim-sun_dark.path` | 2358 | `matrix sect_water_noswim sun_dark` | handler.room_is_dark.matrix-sect_water_noswim-sun_dark | specified |
| `handler.room_is_dark.matrix-sect_water_noswim-sun_rise.path` | 2358 | `matrix sect_water_noswim sun_rise` | handler.room_is_dark.matrix-sect_water_noswim-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_water_noswim-sun_light.path` | 2358 | `matrix sect_water_noswim sun_light` | handler.room_is_dark.matrix-sect_water_noswim-sun_light | specified |
| `handler.room_is_dark.matrix-sect_water_noswim-sun_set.path` | 2358 | `matrix sect_water_noswim sun_set` | handler.room_is_dark.matrix-sect_water_noswim-sun_set | specified |
| `handler.room_is_dark.matrix-sect_unused-sun_dark.path` | 2358 | `matrix sect_unused sun_dark` | handler.room_is_dark.matrix-sect_unused-sun_dark | specified |
| `handler.room_is_dark.matrix-sect_unused-sun_rise.path` | 2358 | `matrix sect_unused sun_rise` | handler.room_is_dark.matrix-sect_unused-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_unused-sun_light.path` | 2358 | `matrix sect_unused sun_light` | handler.room_is_dark.matrix-sect_unused-sun_light | specified |
| `handler.room_is_dark.matrix-sect_unused-sun_set.path` | 2358 | `matrix sect_unused sun_set` | handler.room_is_dark.matrix-sect_unused-sun_set | specified |
| `handler.room_is_dark.matrix-sect_air-sun_dark.path` | 2358 | `matrix sect_air sun_dark` | handler.room_is_dark.matrix-sect_air-sun_dark | specified |
| `handler.room_is_dark.matrix-sect_air-sun_rise.path` | 2358 | `matrix sect_air sun_rise` | handler.room_is_dark.matrix-sect_air-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_air-sun_light.path` | 2358 | `matrix sect_air sun_light` | handler.room_is_dark.matrix-sect_air-sun_light | specified |
| `handler.room_is_dark.matrix-sect_air-sun_set.path` | 2358 | `matrix sect_air sun_set` | handler.room_is_dark.matrix-sect_air-sun_set | specified |
| `handler.room_is_dark.matrix-sect_desert-sun_dark.path` | 2358 | `matrix sect_desert sun_dark` | handler.room_is_dark.matrix-sect_desert-sun_dark | specified |
| `handler.room_is_dark.matrix-sect_desert-sun_rise.path` | 2358 | `matrix sect_desert sun_rise` | handler.room_is_dark.matrix-sect_desert-sun_rise | specified |
| `handler.room_is_dark.matrix-sect_desert-sun_light.path` | 2358 | `matrix sect_desert sun_light` | handler.room_is_dark.matrix-sect_desert-sun_light | specified |
| `handler.room_is_dark.matrix-sect_desert-sun_set.path` | 2358 | `matrix sect_desert sun_set` | handler.room_is_dark.matrix-sect_desert-sun_set | specified |
| `handler.room_is_dark.light-boundary--32768-dark-inside.path` | 2358 | `light boundary  32768 dark inside` | handler.room_is_dark.light-boundary--32768-dark-inside | specified |
| `handler.room_is_dark.light-boundary--1-dark-inside.path` | 2358 | `light boundary  1 dark inside` | handler.room_is_dark.light-boundary--1-dark-inside | specified |
| `handler.room_is_dark.light-boundary-0-dark-inside.path` | 2358 | `light boundary 0 dark inside` | handler.room_is_dark.light-boundary-0-dark-inside | specified |
| `handler.room_is_dark.light-boundary-1-dark-inside.path` | 2358 | `light boundary 1 dark inside` | handler.room_is_dark.light-boundary-1-dark-inside | specified |
| `handler.room_is_dark.light-boundary-32767-dark-inside.path` | 2358 | `light boundary 32767 dark inside` | handler.room_is_dark.light-boundary-32767-dark-inside | specified |
| `handler.room_is_dark.negative-light--32768-sun_light.path` | 2358 | `negative light  32768 sun_light` | handler.room_is_dark.negative-light--32768-sun_light | specified |
| `handler.room_is_dark.negative-light--32768-sun_dark.path` | 2358 | `negative light  32768 sun_dark` | handler.room_is_dark.negative-light--32768-sun_dark | specified |
| `handler.room_is_dark.negative-light--1-sun_light.path` | 2358 | `negative light  1 sun_light` | handler.room_is_dark.negative-light--1-sun_light | specified |
| `handler.room_is_dark.negative-light--1-sun_dark.path` | 2358 | `negative light  1 sun_dark` | handler.room_is_dark.negative-light--1-sun_dark | specified |
| `handler.room_is_dark.unrelated-flag-does-not-light-room.path` | 2358 | `unrelated flag does not light room` | handler.room_is_dark.unrelated-flag-does-not-light-room | specified |
| `handler.room_is_dark.unknown-sunlight-falls-through.path` | 2358 | `unknown sunlight falls through` | handler.room_is_dark.unknown-sunlight-falls-through | specified |
| `handler.room_is_dark.unknown-sector-uses-weather.path` | 2358 | `unknown sector uses weather` | handler.room_is_dark.unknown-sector-uses-weather | specified |

## is_room_owner

[Source line 2376](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2376); ends at line 2382. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_where: `src/act_info.c:2278` (lexical_call_candidate).
- move_char: `src/act_move.c:104` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:829` (lexical_call_candidate).
- do_at: `src/act_wiz.c:885` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:940` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1118` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2142` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2218` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4004` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4198` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2251` (declaration_or_dispatch_reference).

Dependencies: `is_name`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.is_room_owner.if.001` | 2378 | `if (room->owner == NULL \|\| room->owner[0] == '\0')` |  | pending |
| `handler.is_room_owner.or.001` | 2378 | `\|\| room->owner[0] == '\0')` |  | pending |
| `handler.is_room_owner.return.001` | 2379 | `return FALSE;` |  | pending |
| `handler.is_room_owner.return.002` | 2381 | `return is_name(ch->name,room->owner);` |  | pending |

## room_is_private

[Source line 2387](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2387); ends at line 2410. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- get_random_room: `src/act_enter.c:51` (lexical_call_candidate).
- do_enter: `src/act_enter.c:116` (lexical_call_candidate).
- do_where: `src/act_info.c:2279` (lexical_call_candidate).
- move_char: `src/act_move.c:104` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:829` (lexical_call_candidate).
- do_at: `src/act_wiz.c:885` (lexical_call_candidate).
- do_goto: `src/act_wiz.c:940` (lexical_call_candidate).
- do_violate: `src/act_wiz.c:997` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1119` (lexical_call_candidate).
- do_snoop: `src/act_wiz.c:2143` (lexical_call_candidate).
- do_switch: `src/act_wiz.c:2219` (lexical_call_candidate).
- do_rset: `src/act_wiz.c:4005` (lexical_call_candidate).
- do_force: `src/act_wiz.c:4200` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2252` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.room_is_private.if.001` | 2393 | `if (pRoomIndex->owner != NULL && pRoomIndex->owner[0] != '\0')` | handler.room_is_private.owned-empty, handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.private-two, handler.room_is_private.private-three, handler.room_is_private.solitary-zero, handler.room_is_private.solitary-one, handler.room_is_private.imp-empty, handler.room_is_private.public-many, handler.room_is_private.private-zero, handler.room_is_private.private-and-solitary-one | specified |
| `handler.room_is_private.and.001` | 2393 | `&& pRoomIndex->owner[0] != '\0')` | handler.room_is_private.owned-empty, handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.private-two, handler.room_is_private.private-three, handler.room_is_private.solitary-zero, handler.room_is_private.solitary-one, handler.room_is_private.imp-empty, handler.room_is_private.public-many, handler.room_is_private.private-zero, handler.room_is_private.private-and-solitary-one | specified |
| `handler.room_is_private.return.001` | 2394 | `return TRUE;` | handler.room_is_private.owned-empty | specified |
| `handler.room_is_private.for.001` | 2397 | `for ( rch = pRoomIndex->people; rch != NULL; rch = rch->next_in_room )` | handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.private-two, handler.room_is_private.private-three, handler.room_is_private.solitary-zero, handler.room_is_private.solitary-one, handler.room_is_private.imp-empty, handler.room_is_private.public-many, handler.room_is_private.private-zero, handler.room_is_private.private-and-solitary-one | specified |
| `handler.room_is_private.if.002` | 2400 | `if ( IS_SET(pRoomIndex->room_flags, ROOM_PRIVATE)  && count >= 2 )` | handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.private-two, handler.room_is_private.private-three, handler.room_is_private.solitary-zero, handler.room_is_private.solitary-one, handler.room_is_private.imp-empty, handler.room_is_private.public-many, handler.room_is_private.private-zero, handler.room_is_private.private-and-solitary-one | specified |
| `handler.room_is_private.and.002` | 2400 | `&& count >= 2 )` | handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.private-two, handler.room_is_private.private-three, handler.room_is_private.solitary-zero, handler.room_is_private.solitary-one, handler.room_is_private.imp-empty, handler.room_is_private.public-many, handler.room_is_private.private-zero, handler.room_is_private.private-and-solitary-one | specified |
| `handler.room_is_private.return.002` | 2401 | `return TRUE;` | handler.room_is_private.private-two, handler.room_is_private.private-three | specified |
| `handler.room_is_private.if.003` | 2403 | `if ( IS_SET(pRoomIndex->room_flags, ROOM_SOLITARY) && count >= 1 )` | handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.solitary-zero, handler.room_is_private.solitary-one, handler.room_is_private.imp-empty, handler.room_is_private.public-many, handler.room_is_private.private-zero, handler.room_is_private.private-and-solitary-one | specified |
| `handler.room_is_private.and.003` | 2403 | `&& count >= 1 )` | handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.solitary-zero, handler.room_is_private.solitary-one, handler.room_is_private.imp-empty, handler.room_is_private.public-many, handler.room_is_private.private-zero, handler.room_is_private.private-and-solitary-one | specified |
| `handler.room_is_private.return.003` | 2404 | `return TRUE;` | handler.room_is_private.solitary-one, handler.room_is_private.private-and-solitary-one | specified |
| `handler.room_is_private.if.004` | 2406 | `if ( IS_SET(pRoomIndex->room_flags, ROOM_IMP_ONLY) )` | handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.solitary-zero, handler.room_is_private.imp-empty, handler.room_is_private.public-many, handler.room_is_private.private-zero | specified |
| `handler.room_is_private.return.004` | 2407 | `return TRUE;` | handler.room_is_private.imp-empty | specified |
| `handler.room_is_private.return.005` | 2409 | `return FALSE;` | handler.room_is_private.null-owner-empty, handler.room_is_private.empty-owner-empty, handler.room_is_private.private-one, handler.room_is_private.solitary-zero, handler.room_is_private.public-many, handler.room_is_private.private-zero | specified |
| `handler.room_is_private.owned-empty.path` | 2393 | `owned empty` | handler.room_is_private.owned-empty | specified |
| `handler.room_is_private.null-owner-empty.path` | 2393 | `null owner empty` | handler.room_is_private.null-owner-empty | specified |
| `handler.room_is_private.empty-owner-empty.path` | 2393 | `empty owner empty` | handler.room_is_private.empty-owner-empty | specified |
| `handler.room_is_private.private-one.path` | 2393 | `private one` | handler.room_is_private.private-one | specified |
| `handler.room_is_private.private-two.path` | 2393 | `private two` | handler.room_is_private.private-two | specified |
| `handler.room_is_private.private-three.path` | 2393 | `private three` | handler.room_is_private.private-three | specified |
| `handler.room_is_private.solitary-zero.path` | 2393 | `solitary zero` | handler.room_is_private.solitary-zero | specified |
| `handler.room_is_private.solitary-one.path` | 2393 | `solitary one` | handler.room_is_private.solitary-one | specified |
| `handler.room_is_private.imp-empty.path` | 2393 | `imp empty` | handler.room_is_private.imp-empty | specified |
| `handler.room_is_private.public-many.path` | 2393 | `public many` | handler.room_is_private.public-many | specified |
| `handler.room_is_private.private-zero.path` | 2396 | `private zero` | handler.room_is_private.private-zero | specified |
| `handler.room_is_private.private-and-solitary-one.path` | 2396 | `private and solitary one` | handler.room_is_private.private-and-solitary-one | specified |

## can_see_room

[Source line 2413](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2413); ends at line 2435. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- get_random_room: `src/act_enter.c:50` (lexical_call_candidate).
- do_enter: `src/act_enter.c:115` (lexical_call_candidate).
- do_exits: `src/act_info.c:1343` (lexical_call_candidate).
- move_char: `src/act_move.c:82` (lexical_call_candidate).
- move_char: `src/act_move.c:216` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1904` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1946` (lexical_call_candidate).
- bust_a_prompt: `src/comm.c:1365` (lexical_call_candidate).
- spell_gate: `src/magic.c:2891` (lexical_call_candidate).
- spell_portal: `src/magic2.c:64` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:116` (lexical_call_candidate).
- spell_nexus: `src/magic2.c:116` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2255` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `get_trust`, `IS_IMMORTAL`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.can_see_room.if.001` | 2415 | `if (IS_SET(pRoomIndex->room_flags, ROOM_IMP_ONLY)      &&  get_trust(ch) < MAX_LEVEL)` |  | pending |
| `handler.can_see_room.and.001` | 2416 | `&&  get_trust(ch) < MAX_LEVEL)` |  | pending |
| `handler.can_see_room.return.001` | 2417 | `return FALSE;` |  | pending |
| `handler.can_see_room.if.002` | 2419 | `if (IS_SET(pRoomIndex->room_flags, ROOM_GODS_ONLY)     &&  !IS_IMMORTAL(ch))` |  | pending |
| `handler.can_see_room.and.002` | 2420 | `&&  !IS_IMMORTAL(ch))` |  | pending |
| `handler.can_see_room.return.002` | 2421 | `return FALSE;` |  | pending |
| `handler.can_see_room.if.003` | 2423 | `if (IS_SET(pRoomIndex->room_flags, ROOM_HEROES_ONLY)     &&  !IS_IMMORTAL(ch))` |  | pending |
| `handler.can_see_room.and.003` | 2424 | `&&  !IS_IMMORTAL(ch))` |  | pending |
| `handler.can_see_room.return.003` | 2425 | `return FALSE;` |  | pending |
| `handler.can_see_room.if.004` | 2427 | `if (IS_SET(pRoomIndex->room_flags,ROOM_NEWBIES_ONLY)     &&  ch->level > 5 && !IS_IMMORTAL(ch))` |  | pending |
| `handler.can_see_room.and.004` | 2428 | `&&  ch->level > 5 && !IS_IMMORTAL(ch))` |  | pending |
| `handler.can_see_room.and.005` | 2428 | `&& !IS_IMMORTAL(ch))` |  | pending |
| `handler.can_see_room.return.004` | 2429 | `return FALSE;` |  | pending |
| `handler.can_see_room.if.005` | 2431 | `if (!IS_IMMORTAL(ch) && pRoomIndex->clan && ch->clan != pRoomIndex->clan)` |  | pending |
| `handler.can_see_room.and.006` | 2431 | `&& pRoomIndex->clan && ch->clan != pRoomIndex->clan)` |  | pending |
| `handler.can_see_room.and.007` | 2431 | `&& ch->clan != pRoomIndex->clan)` |  | pending |
| `handler.can_see_room.return.005` | 2432 | `return FALSE;` |  | pending |
| `handler.can_see_room.return.006` | 2434 | `return TRUE;` |  | pending |
| `handler.can_see_room.ordinary-room.path` | 2415 | `ordinary room` | handler.can_see_room.ordinary-room | specified |
| `handler.can_see_room.imp-below.path` | 2415 | `imp below` | handler.can_see_room.imp-below | specified |
| `handler.can_see_room.imp-at-max.path` | 2415 | `imp at max` | handler.can_see_room.imp-at-max | specified |
| `handler.can_see_room.gods-below.path` | 2415 | `gods below` | handler.can_see_room.gods-below | specified |
| `handler.can_see_room.gods-at-immortal.path` | 2415 | `gods at immortal` | handler.can_see_room.gods-at-immortal | specified |
| `handler.can_see_room.heroes-hero-still-denied.path` | 2415 | `heroes hero still denied` | handler.can_see_room.heroes-hero-still-denied | specified |
| `handler.can_see_room.heroes-at-immortal.path` | 2415 | `heroes at immortal` | handler.can_see_room.heroes-at-immortal | specified |
| `handler.can_see_room.newbie-at-five.path` | 2415 | `newbie at five` | handler.can_see_room.newbie-at-five | specified |
| `handler.can_see_room.newbie-at-six.path` | 2415 | `newbie at six` | handler.can_see_room.newbie-at-six | specified |
| `handler.can_see_room.newbie-immortal-exception.path` | 2415 | `newbie immortal exception` | handler.can_see_room.newbie-immortal-exception | specified |
| `handler.can_see_room.clan-mismatch.path` | 2415 | `clan mismatch` | handler.can_see_room.clan-mismatch | specified |
| `handler.can_see_room.clan-matches.path` | 2415 | `clan matches` | handler.can_see_room.clan-matches | specified |
| `handler.can_see_room.clan-immortal-exception.path` | 2415 | `clan immortal exception` | handler.can_see_room.clan-immortal-exception | specified |
| `handler.can_see_room.trust-qualifies-low-level.path` | 2415 | `trust qualifies low level` | handler.can_see_room.trust-qualifies-low-level | specified |
| `handler.can_see_room.npc-level-sixty-not-immortal.path` | 2415 | `npc level sixty not immortal` | handler.can_see_room.npc-level-sixty-not-immortal | specified |
| `handler.can_see_room.safe-and-no-recall-do-not-hide-room.path` | 2415 | `safe and no recall do not hide room` | handler.can_see_room.safe-and-no-recall-do-not-hide-room | specified |

## can_see

[Source line 2442](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2442); ends at line 2490. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- add_follower: `src/act_comm.c:1528` (lexical_call_candidate).
- stop_follower: `src/act_comm.c:1552` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:415` (lexical_call_candidate).
- show_char_to_char: `src/act_info.c:506` (lexical_call_candidate).
- do_whois: `src/act_info.c:1834` (lexical_call_candidate).
- do_whois: `src/act_info.c:1839` (lexical_call_candidate).
- do_who: `src/act_info.c:2017` (lexical_call_candidate).
- do_who: `src/act_info.c:2022` (lexical_call_candidate).
- do_count: `src/act_info.c:2091` (lexical_call_candidate).
- do_where: `src/act_info.c:2281` (lexical_call_candidate).
- do_where: `src/act_info.c:2301` (lexical_call_candidate).
- do_give: `src/act_obj.c:738` (lexical_call_candidate).
- do_give: `src/act_obj.c:748` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2180` (lexical_call_candidate).
- find_keeper: `src/act_obj.c:2369` (lexical_call_candidate).
- do_transfer: `src/act_wiz.c:804` (lexical_call_candidate).
- do_rstat: `src/act_wiz.c:1162` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1256` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1899` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1945` (lexical_call_candidate).
- do_sockets: `src/act_wiz.c:4059` (lexical_call_candidate).
- process_output: `src/comm.c:1234` (lexical_call_candidate).
- check_assist: `src/fight.c:163` (lexical_call_candidate).
- one_hit: `src/fight.c:487` (lexical_call_candidate).
- check_parry: `src/fight.c:1280` (lexical_call_candidate).
- check_dodge: `src/fight.c:1333` (lexical_call_candidate).
- get_char_room: `src/handler.c:2027` (lexical_call_candidate).
- get_char_world: `src/handler.c:2056` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3613` (lexical_call_candidate).
- scan_list: `src/scan.c:106` (lexical_call_candidate).
- do_gain: `src/skills.c:61` (lexical_call_candidate).
- spec_cast_adept: `src/special.c:486` (lexical_call_candidate).
- spec_executioner: `src/special.c:737` (lexical_call_candidate).
- spec_executioner: `src/special.c:741` (lexical_call_candidate).
- spec_guard: `src/special.c:811` (lexical_call_candidate).
- spec_guard: `src/special.c:815` (lexical_call_candidate).
- spec_thief: `src/special.c:1015` (lexical_call_candidate).
- aggr_update: `src/update.c:1036` (lexical_call_candidate).
- aggr_update: `src/update.c:1055` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:1858` (declaration_or_dispatch_reference).
- declaration_or_dispatch_reference: `src/merc.h:2253` (declaration_or_dispatch_reference).

Dependencies: `get_trust`, `IS_NPC`, `IS_SET`, `IS_IMMORTAL`, `IS_AFFECTED`, `room_is_dark`, `get_skill`, `get_curr_stat`, `number_percent`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.can_see.if.001` | 2445 | `if ( ch == victim )` |  | pending |
| `handler.can_see.return.001` | 2446 | `return TRUE;` |  | pending |
| `handler.can_see.if.002` | 2448 | `if ( get_trust(ch) < victim->invis_level)` |  | pending |
| `handler.can_see.return.002` | 2449 | `return FALSE;` |  | pending |
| `handler.can_see.if.003` | 2452 | `if (get_trust(ch) < victim->incog_level && ch->in_room != victim->in_room)` |  | pending |
| `handler.can_see.and.001` | 2452 | `&& ch->in_room != victim->in_room)` |  | pending |
| `handler.can_see.return.003` | 2453 | `return FALSE;` |  | pending |
| `handler.can_see.if.004` | 2455 | `if ( (!IS_NPC(ch) && IS_SET(ch->act, PLR_HOLYLIGHT))      \|\|   (IS_NPC(ch) && IS_IMMORTAL(ch)))` |  | pending |
| `handler.can_see.and.002` | 2455 | `&& IS_SET(ch->act, PLR_HOLYLIGHT))` |  | pending |
| `handler.can_see.or.001` | 2456 | `\|\|   (IS_NPC(ch) && IS_IMMORTAL(ch)))` |  | pending |
| `handler.can_see.and.003` | 2456 | `&& IS_IMMORTAL(ch)))` |  | pending |
| `handler.can_see.return.004` | 2457 | `return TRUE;` |  | pending |
| `handler.can_see.if.005` | 2459 | `if ( IS_AFFECTED(ch, AFF_BLIND) )` |  | pending |
| `handler.can_see.return.005` | 2460 | `return FALSE;` |  | pending |
| `handler.can_see.if.006` | 2462 | `if ( room_is_dark( ch->in_room ) && !IS_AFFECTED(ch, AFF_INFRARED) )` |  | pending |
| `handler.can_see.and.004` | 2462 | `&& !IS_AFFECTED(ch, AFF_INFRARED) )` |  | pending |
| `handler.can_see.return.006` | 2463 | `return FALSE;` |  | pending |
| `handler.can_see.if.007` | 2465 | `if ( IS_AFFECTED(victim, AFF_INVISIBLE)     &&   !IS_AFFECTED(ch, AFF_DETECT_INVIS) )` |  | pending |
| `handler.can_see.and.005` | 2466 | `&&   !IS_AFFECTED(ch, AFF_DETECT_INVIS) )` |  | pending |
| `handler.can_see.return.007` | 2467 | `return FALSE;` |  | pending |
| `handler.can_see.if.008` | 2470 | `if ( IS_AFFECTED(victim, AFF_SNEAK)     &&   !IS_AFFECTED(ch,AFF_DETECT_HIDDEN)     &&   victim->fighting == NULL)` |  | pending |
| `handler.can_see.and.006` | 2471 | `&&   !IS_AFFECTED(ch,AFF_DETECT_HIDDEN)` |  | pending |
| `handler.can_see.and.007` | 2472 | `&&   victim->fighting == NULL)` |  | pending |
| `handler.can_see.if.009` | 2480 | `if (number_percent() < chance)` |  | pending |
| `handler.can_see.return.008` | 2481 | `return FALSE;` |  | pending |
| `handler.can_see.if.010` | 2484 | `if ( IS_AFFECTED(victim, AFF_HIDE)     &&   !IS_AFFECTED(ch, AFF_DETECT_HIDDEN)     &&   victim->fighting == NULL)` |  | pending |
| `handler.can_see.and.008` | 2485 | `&&   !IS_AFFECTED(ch, AFF_DETECT_HIDDEN)` |  | pending |
| `handler.can_see.and.009` | 2486 | `&&   victim->fighting == NULL)` |  | pending |
| `handler.can_see.return.009` | 2487 | `return FALSE;` |  | pending |
| `handler.can_see.return.010` | 2489 | `return TRUE;` |  | pending |
| `handler.can_see.ordinary-visible.path` | 2445 | `ordinary visible` | handler.can_see.ordinary-visible | specified |
| `handler.can_see.self-before-blindness.path` | 2445 | `self before blindness` | handler.can_see.self-before-blindness | specified |
| `handler.can_see.invis-level-above-trust.path` | 2445 | `invis level above trust` | handler.can_see.invis-level-above-trust | specified |
| `handler.can_see.invis-level-equal-trust.path` | 2445 | `invis level equal trust` | handler.can_see.invis-level-equal-trust | specified |
| `handler.can_see.holylight-does-not-beat-wizinvis.path` | 2445 | `holylight does not beat wizinvis` | handler.can_see.holylight-does-not-beat-wizinvis | specified |
| `handler.can_see.incognito-same-room.path` | 2445 | `incognito same room` | handler.can_see.incognito-same-room | specified |
| `handler.can_see.incognito-other-room.path` | 2445 | `incognito other room` | handler.can_see.incognito-other-room | specified |
| `handler.can_see.incognito-equal-trust-other-room.path` | 2445 | `incognito equal trust other room` | handler.can_see.incognito-equal-trust-other-room | specified |
| `handler.can_see.holylight-beats-blindness.path` | 2445 | `holylight beats blindness` | handler.can_see.holylight-beats-blindness | specified |
| `handler.can_see.immortal-npc-beats-blindness.path` | 2445 | `immortal npc beats blindness` | handler.can_see.immortal-npc-beats-blindness | specified |
| `handler.can_see.blind-denies.path` | 2445 | `blind denies` | handler.can_see.blind-denies | specified |
| `handler.can_see.dark-denies.path` | 2445 | `dark denies` | handler.can_see.dark-denies | specified |
| `handler.can_see.infrared-beats-dark.path` | 2445 | `infrared beats dark` | handler.can_see.infrared-beats-dark | specified |
| `handler.can_see.invisible-denies.path` | 2445 | `invisible denies` | handler.can_see.invisible-denies | specified |
| `handler.can_see.detect-invisible.path` | 2445 | `detect invisible` | handler.can_see.detect-invisible | specified |
| `handler.can_see.sneak-roll-below-thirty.path` | 2445 | `sneak roll below thirty` | handler.can_see.sneak-roll-below-thirty | specified |
| `handler.can_see.sneak-roll-equal-thirty.path` | 2445 | `sneak roll equal thirty` | handler.can_see.sneak-roll-equal-thirty | specified |
| `handler.can_see.sneak-roll-above-thirty.path` | 2445 | `sneak roll above thirty` | handler.can_see.sneak-roll-above-thirty | specified |
| `handler.can_see.sneak-fighting-skips-roll.path` | 2445 | `sneak fighting skips roll` | handler.can_see.sneak-fighting-skips-roll | specified |
| `handler.can_see.sneak-detect-hidden-skips-roll.path` | 2445 | `sneak detect hidden skips roll` | handler.can_see.sneak-detect-hidden-skips-roll | specified |
| `handler.can_see.hide-without-detection.path` | 2445 | `hide without detection` | handler.can_see.hide-without-detection | specified |
| `handler.can_see.hide-while-fighting-visible.path` | 2445 | `hide while fighting visible` | handler.can_see.hide-while-fighting-visible | specified |
| `handler.can_see.hide-with-detection-visible.path` | 2445 | `hide with detection visible` | handler.can_see.hide-with-detection-visible | specified |
| `handler.can_see.sneak-roll-succeeds-but-hide-denies.path` | 2445 | `sneak roll succeeds but hide denies` | handler.can_see.sneak-roll-succeeds-but-hide-denies | specified |

## can_see_obj

[Source line 2497](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2497); ends at line 2522. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- show_list_to_char: `src/act_info.c:160` (lexical_call_candidate).
- show_char_to_char_1: `src/act_info.c:466` (lexical_call_candidate).
- do_look: `src/act_info.c:1119` (lexical_call_candidate).
- do_look: `src/act_info.c:1151` (lexical_call_candidate).
- do_equipment: `src/act_info.c:2129` (lexical_call_candidate).
- do_compare: `src/act_info.c:2178` (lexical_call_candidate).
- do_get: `src/act_obj.c:236` (lexical_call_candidate).
- do_get: `src/act_obj.c:314` (lexical_call_candidate).
- do_put: `src/act_obj.c:452` (lexical_call_candidate).
- do_drop: `src/act_obj.c:620` (lexical_call_candidate).
- do_give: `src/act_obj.c:811` (lexical_call_candidate).
- do_wear: `src/act_obj.c:1693` (lexical_call_candidate).
- get_obj_keeper: `src/act_obj.c:2433` (lexical_call_candidate).
- get_obj_keeper: `src/act_obj.c:2434` (lexical_call_candidate).
- do_buy: `src/act_obj.c:2632` (lexical_call_candidate).
- do_list: `src/act_obj.c:2804` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2878` (lexical_call_candidate).
- do_value: `src/act_obj.c:2964` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1889` (lexical_call_candidate).
- act_new: `src/comm.c:2522` (lexical_call_candidate).
- act_new: `src/comm.c:2528` (lexical_call_candidate).
- damage: `src/fight.c:910` (lexical_call_candidate).
- disarm: `src/fight.c:2114` (lexical_call_candidate).
- get_obj_list: `src/handler.c:2100` (lexical_call_candidate).
- get_obj_carry: `src/handler.c:2127` (lexical_call_candidate).
- get_obj_wear: `src/handler.c:2155` (lexical_call_candidate).
- get_obj_world: `src/handler.c:2207` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3602` (lexical_call_candidate).
- do_play: `src/music.c:228` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2254` (declaration_or_dispatch_reference).

Dependencies: `IS_NPC`, `IS_SET`, `IS_AFFECTED`, `IS_OBJ_STAT`, `room_is_dark`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.can_see_obj.if.001` | 2499 | `if ( !IS_NPC(ch) && IS_SET(ch->act, PLR_HOLYLIGHT) )` |  | pending |
| `handler.can_see_obj.and.001` | 2499 | `&& IS_SET(ch->act, PLR_HOLYLIGHT) )` |  | pending |
| `handler.can_see_obj.return.001` | 2500 | `return TRUE;` |  | pending |
| `handler.can_see_obj.if.002` | 2502 | `if ( IS_SET(obj->extra_flags,ITEM_VIS_DEATH))` |  | pending |
| `handler.can_see_obj.return.002` | 2503 | `return FALSE;` |  | pending |
| `handler.can_see_obj.if.003` | 2505 | `if ( IS_AFFECTED( ch, AFF_BLIND ) && obj->item_type != ITEM_POTION)` |  | pending |
| `handler.can_see_obj.and.002` | 2505 | `&& obj->item_type != ITEM_POTION)` |  | pending |
| `handler.can_see_obj.return.003` | 2506 | `return FALSE;` |  | pending |
| `handler.can_see_obj.if.004` | 2508 | `if ( obj->item_type == ITEM_LIGHT && obj->value[2] != 0 )` |  | pending |
| `handler.can_see_obj.and.003` | 2508 | `&& obj->value[2] != 0 )` |  | pending |
| `handler.can_see_obj.return.004` | 2509 | `return TRUE;` |  | pending |
| `handler.can_see_obj.if.005` | 2511 | `if ( IS_SET(obj->extra_flags, ITEM_INVIS)     &&   !IS_AFFECTED(ch, AFF_DETECT_INVIS) )` |  | pending |
| `handler.can_see_obj.and.004` | 2512 | `&&   !IS_AFFECTED(ch, AFF_DETECT_INVIS) )` |  | pending |
| `handler.can_see_obj.return.005` | 2513 | `return FALSE;` |  | pending |
| `handler.can_see_obj.if.006` | 2515 | `if ( IS_OBJ_STAT(obj,ITEM_GLOW))` |  | pending |
| `handler.can_see_obj.return.006` | 2516 | `return TRUE;` |  | pending |
| `handler.can_see_obj.if.007` | 2518 | `if ( room_is_dark( ch->in_room ) && !IS_AFFECTED(ch, AFF_DARK_VISION) )` |  | pending |
| `handler.can_see_obj.and.005` | 2518 | `&& !IS_AFFECTED(ch, AFF_DARK_VISION) )` |  | pending |
| `handler.can_see_obj.return.007` | 2519 | `return FALSE;` |  | pending |
| `handler.can_see_obj.return.008` | 2521 | `return TRUE;` |  | pending |
| `handler.can_see_obj.ordinary.path` | 2499 | `ordinary` | handler.can_see_obj.ordinary | specified |
| `handler.can_see_obj.holylight-beats-death.path` | 2499 | `holylight beats death` | handler.can_see_obj.holylight-beats-death | specified |
| `handler.can_see_obj.death-hidden.path` | 2499 | `death hidden` | handler.can_see_obj.death-hidden | specified |
| `handler.can_see_obj.blind-nonpotion.path` | 2499 | `blind nonpotion` | handler.can_see_obj.blind-nonpotion | specified |
| `handler.can_see_obj.blind-potion-exception.path` | 2499 | `blind potion exception` | handler.can_see_obj.blind-potion-exception | specified |
| `handler.can_see_obj.lit-light-before-invis-dark.path` | 2499 | `lit light before invis dark` | handler.can_see_obj.lit-light-before-invis-dark | specified |
| `handler.can_see_obj.infinite-light-negative-duration.path` | 2499 | `infinite light negative duration` | handler.can_see_obj.infinite-light-negative-duration | specified |
| `handler.can_see_obj.unlit-light-in-dark.path` | 2499 | `unlit light in dark` | handler.can_see_obj.unlit-light-in-dark | specified |
| `handler.can_see_obj.invisible-glow-still-hidden.path` | 2499 | `invisible glow still hidden` | handler.can_see_obj.invisible-glow-still-hidden | specified |
| `handler.can_see_obj.detect-invis.path` | 2499 | `detect invis` | handler.can_see_obj.detect-invis | specified |
| `handler.can_see_obj.glow-beats-dark.path` | 2499 | `glow beats dark` | handler.can_see_obj.glow-beats-dark | specified |
| `handler.can_see_obj.dark-without-vision.path` | 2499 | `dark without vision` | handler.can_see_obj.dark-without-vision | specified |
| `handler.can_see_obj.infrared-does-not-suffice-for-objects.path` | 2499 | `infrared does not suffice for objects` | handler.can_see_obj.infrared-does-not-suffice-for-objects | specified |
| `handler.can_see_obj.dark-vision-for-objects.path` | 2499 | `dark vision for objects` | handler.can_see_obj.dark-vision-for-objects | specified |

## can_drop_obj

[Source line 2529](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2529); ends at line 2538. Status: partially_specified.

Entry references (lexical candidates; caller guards still require inspection):

- do_put: `src/act_obj.c:403` (lexical_call_candidate).
- do_put: `src/act_obj.c:456` (lexical_call_candidate).
- do_drop: `src/act_obj.c:594` (lexical_call_candidate).
- do_drop: `src/act_obj.c:622` (lexical_call_candidate).
- do_give: `src/act_obj.c:793` (lexical_call_candidate).
- do_steal: `src/act_obj.c:2280` (lexical_call_candidate).
- do_sell: `src/act_obj.c:2872` (lexical_call_candidate).
- do_value: `src/act_obj.c:2970` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3061` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3086` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3112` (lexical_call_candidate).
- spell_heat_metal: `src/magic.c:3135` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2256` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `IS_NPC`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.can_drop_obj.if.001` | 2531 | `if ( !IS_SET(obj->extra_flags, ITEM_NODROP) )` | handler.can_drop_obj.normal-object, handler.can_drop_obj.nodrop-mortal, handler.can_drop_obj.nodrop-immortal, handler.can_drop_obj.trust-alone-insufficient, handler.can_drop_obj.npc-no-exception | specified |
| `handler.can_drop_obj.return.001` | 2532 | `return TRUE;` | handler.can_drop_obj.normal-object | specified |
| `handler.can_drop_obj.if.002` | 2534 | `if ( !IS_NPC(ch) && ch->level >= LEVEL_IMMORTAL )` | handler.can_drop_obj.nodrop-mortal, handler.can_drop_obj.nodrop-immortal, handler.can_drop_obj.trust-alone-insufficient, handler.can_drop_obj.npc-no-exception | specified |
| `handler.can_drop_obj.and.001` | 2534 | `&& ch->level >= LEVEL_IMMORTAL )` | handler.can_drop_obj.nodrop-mortal, handler.can_drop_obj.nodrop-immortal, handler.can_drop_obj.trust-alone-insufficient, handler.can_drop_obj.npc-no-exception | specified |
| `handler.can_drop_obj.return.002` | 2535 | `return TRUE;` | handler.can_drop_obj.nodrop-immortal | specified |
| `handler.can_drop_obj.return.003` | 2537 | `return FALSE;` | handler.can_drop_obj.nodrop-mortal, handler.can_drop_obj.trust-alone-insufficient, handler.can_drop_obj.npc-no-exception | specified |
| `handler.can_drop_obj.normal-object.path` | 2531 | `normal object` | handler.can_drop_obj.normal-object | specified |
| `handler.can_drop_obj.nodrop-mortal.path` | 2531 | `nodrop mortal` | handler.can_drop_obj.nodrop-mortal | specified |
| `handler.can_drop_obj.nodrop-immortal.path` | 2531 | `nodrop immortal` | handler.can_drop_obj.nodrop-immortal | specified |
| `handler.can_drop_obj.trust-alone-insufficient.path` | 2531 | `trust alone insufficient` | handler.can_drop_obj.trust-alone-insufficient | specified |
| `handler.can_drop_obj.npc-no-exception.path` | 2531 | `npc no exception` | handler.can_drop_obj.npc-no-exception | specified |

## affect_loc_name

[Source line 2544](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2544); ends at line 2576. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_affects: `src/act_info.c:1647` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1436` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1484` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1712` (lexical_call_candidate).
- spell_identify: `src/magic.c:3366` (lexical_call_candidate).
- spell_identify: `src/magic.c:3407` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2257` (declaration_or_dispatch_reference).

Dependencies: `bug`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_loc_name.switch.001` | 2546 | `switch ( location )` |  | pending |
| `handler.affect_loc_name.case.001` | 2548 | `case APPLY_NONE:		return "none";` |  | pending |
| `handler.affect_loc_name.return.001` | 2548 | `return "none";` |  | pending |
| `handler.affect_loc_name.case.002` | 2549 | `case APPLY_STR:		return "strength";` |  | pending |
| `handler.affect_loc_name.return.002` | 2549 | `return "strength";` |  | pending |
| `handler.affect_loc_name.case.003` | 2550 | `case APPLY_DEX:		return "dexterity";` |  | pending |
| `handler.affect_loc_name.return.003` | 2550 | `return "dexterity";` |  | pending |
| `handler.affect_loc_name.case.004` | 2551 | `case APPLY_INT:		return "intelligence";` |  | pending |
| `handler.affect_loc_name.return.004` | 2551 | `return "intelligence";` |  | pending |
| `handler.affect_loc_name.case.005` | 2552 | `case APPLY_WIS:		return "wisdom";` |  | pending |
| `handler.affect_loc_name.return.005` | 2552 | `return "wisdom";` |  | pending |
| `handler.affect_loc_name.case.006` | 2553 | `case APPLY_CON:		return "constitution";` |  | pending |
| `handler.affect_loc_name.return.006` | 2553 | `return "constitution";` |  | pending |
| `handler.affect_loc_name.case.007` | 2554 | `case APPLY_SEX:		return "sex";` |  | pending |
| `handler.affect_loc_name.return.007` | 2554 | `return "sex";` |  | pending |
| `handler.affect_loc_name.case.008` | 2555 | `case APPLY_CLASS:		return "class";` |  | pending |
| `handler.affect_loc_name.return.008` | 2555 | `return "class";` |  | pending |
| `handler.affect_loc_name.case.009` | 2556 | `case APPLY_LEVEL:		return "level";` |  | pending |
| `handler.affect_loc_name.return.009` | 2556 | `return "level";` |  | pending |
| `handler.affect_loc_name.case.010` | 2557 | `case APPLY_AGE:		return "age";` |  | pending |
| `handler.affect_loc_name.return.010` | 2557 | `return "age";` |  | pending |
| `handler.affect_loc_name.case.011` | 2558 | `case APPLY_MANA:		return "mana";` |  | pending |
| `handler.affect_loc_name.return.011` | 2558 | `return "mana";` |  | pending |
| `handler.affect_loc_name.case.012` | 2559 | `case APPLY_HIT:		return "hp";` |  | pending |
| `handler.affect_loc_name.return.012` | 2559 | `return "hp";` |  | pending |
| `handler.affect_loc_name.case.013` | 2560 | `case APPLY_MOVE:		return "moves";` |  | pending |
| `handler.affect_loc_name.return.013` | 2560 | `return "moves";` |  | pending |
| `handler.affect_loc_name.case.014` | 2561 | `case APPLY_GOLD:		return "gold";` |  | pending |
| `handler.affect_loc_name.return.014` | 2561 | `return "gold";` |  | pending |
| `handler.affect_loc_name.case.015` | 2562 | `case APPLY_EXP:		return "experience";` |  | pending |
| `handler.affect_loc_name.return.015` | 2562 | `return "experience";` |  | pending |
| `handler.affect_loc_name.case.016` | 2563 | `case APPLY_AC:		return "armor class";` |  | pending |
| `handler.affect_loc_name.return.016` | 2563 | `return "armor class";` |  | pending |
| `handler.affect_loc_name.case.017` | 2564 | `case APPLY_HITROLL:		return "hit roll";` |  | pending |
| `handler.affect_loc_name.return.017` | 2564 | `return "hit roll";` |  | pending |
| `handler.affect_loc_name.case.018` | 2565 | `case APPLY_DAMROLL:		return "damage roll";` |  | pending |
| `handler.affect_loc_name.return.018` | 2565 | `return "damage roll";` |  | pending |
| `handler.affect_loc_name.case.019` | 2566 | `case APPLY_SAVES:		return "saves";` |  | pending |
| `handler.affect_loc_name.return.019` | 2566 | `return "saves";` |  | pending |
| `handler.affect_loc_name.case.020` | 2567 | `case APPLY_SAVING_ROD:	return "save vs rod";` |  | pending |
| `handler.affect_loc_name.return.020` | 2567 | `return "save vs rod";` |  | pending |
| `handler.affect_loc_name.case.021` | 2568 | `case APPLY_SAVING_PETRI:	return "save vs petrification";` |  | pending |
| `handler.affect_loc_name.return.021` | 2568 | `return "save vs petrification";` |  | pending |
| `handler.affect_loc_name.case.022` | 2569 | `case APPLY_SAVING_BREATH:	return "save vs breath";` |  | pending |
| `handler.affect_loc_name.return.022` | 2569 | `return "save vs breath";` |  | pending |
| `handler.affect_loc_name.case.023` | 2570 | `case APPLY_SAVING_SPELL:	return "save vs spell";` |  | pending |
| `handler.affect_loc_name.return.023` | 2570 | `return "save vs spell";` |  | pending |
| `handler.affect_loc_name.case.024` | 2571 | `case APPLY_SPELL_AFFECT:	return "none";` |  | pending |
| `handler.affect_loc_name.return.024` | 2571 | `return "none";` |  | pending |
| `handler.affect_loc_name.return.025` | 2575 | `return "(unknown)";` |  | pending |

## affect_bit_name

[Source line 2583](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2583); ends at line 2615. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_ostat: `src/act_wiz.c:1449` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1492` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1685` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1715` (lexical_call_candidate).
- spell_identify: `src/magic.c:3374` (lexical_call_candidate).
- spell_identify: `src/magic.c:3420` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2258` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.affect_bit_name.if.001` | 2588 | `if ( vector & AFF_BLIND         )` |  | pending |
| `handler.affect_bit_name.if.002` | 2589 | `if ( vector & AFF_INVISIBLE     )` |  | pending |
| `handler.affect_bit_name.if.003` | 2590 | `if ( vector & AFF_DETECT_EVIL   )` |  | pending |
| `handler.affect_bit_name.if.004` | 2591 | `if ( vector & AFF_DETECT_GOOD   )` |  | pending |
| `handler.affect_bit_name.if.005` | 2592 | `if ( vector & AFF_DETECT_INVIS  )` |  | pending |
| `handler.affect_bit_name.if.006` | 2593 | `if ( vector & AFF_DETECT_MAGIC  )` |  | pending |
| `handler.affect_bit_name.if.007` | 2594 | `if ( vector & AFF_DETECT_HIDDEN )` |  | pending |
| `handler.affect_bit_name.if.008` | 2595 | `if ( vector & AFF_SANCTUARY     )` |  | pending |
| `handler.affect_bit_name.if.009` | 2596 | `if ( vector & AFF_FAERIE_FIRE   )` |  | pending |
| `handler.affect_bit_name.if.010` | 2597 | `if ( vector & AFF_INFRARED      )` |  | pending |
| `handler.affect_bit_name.if.011` | 2598 | `if ( vector & AFF_CURSE         )` |  | pending |
| `handler.affect_bit_name.if.012` | 2599 | `if ( vector & AFF_POISON        )` |  | pending |
| `handler.affect_bit_name.if.013` | 2600 | `if ( vector & AFF_PROTECT_EVIL  )` |  | pending |
| `handler.affect_bit_name.if.014` | 2601 | `if ( vector & AFF_PROTECT_GOOD  )` |  | pending |
| `handler.affect_bit_name.if.015` | 2602 | `if ( vector & AFF_SLEEP         )` |  | pending |
| `handler.affect_bit_name.if.016` | 2603 | `if ( vector & AFF_SNEAK         )` |  | pending |
| `handler.affect_bit_name.if.017` | 2604 | `if ( vector & AFF_HIDE          )` |  | pending |
| `handler.affect_bit_name.if.018` | 2605 | `if ( vector & AFF_CHARM         )` |  | pending |
| `handler.affect_bit_name.if.019` | 2606 | `if ( vector & AFF_FLYING        )` |  | pending |
| `handler.affect_bit_name.if.020` | 2607 | `if ( vector & AFF_PASS_DOOR     )` |  | pending |
| `handler.affect_bit_name.if.021` | 2608 | `if ( vector & AFF_BERSERK	    )` |  | pending |
| `handler.affect_bit_name.if.022` | 2609 | `if ( vector & AFF_CALM	    )` |  | pending |
| `handler.affect_bit_name.if.023` | 2610 | `if ( vector & AFF_HASTE	    )` |  | pending |
| `handler.affect_bit_name.if.024` | 2611 | `if ( vector & AFF_SLOW          )` |  | pending |
| `handler.affect_bit_name.if.025` | 2612 | `if ( vector & AFF_PLAGUE	    )` |  | pending |
| `handler.affect_bit_name.if.026` | 2613 | `if ( vector & AFF_DARK_VISION   )` |  | pending |
| `handler.affect_bit_name.return.001` | 2614 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.affect_bit_name.ternary.001` | 2614 | `? buf+1 : "none";` |  | pending |

## extra_bit_name

[Source line 2622](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2622); ends at line 2649. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_ostat: `src/act_wiz.c:1239` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1457` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1496` (lexical_call_candidate).
- spell_identify: `src/magic.c:3240` (lexical_call_candidate).
- spell_identify: `src/magic.c:3378` (lexical_call_candidate).
- spell_identify: `src/magic.c:3424` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2259` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.extra_bit_name.if.001` | 2627 | `if ( extra_flags & ITEM_GLOW         )` |  | pending |
| `handler.extra_bit_name.if.002` | 2628 | `if ( extra_flags & ITEM_HUM          )` |  | pending |
| `handler.extra_bit_name.if.003` | 2629 | `if ( extra_flags & ITEM_DARK         )` |  | pending |
| `handler.extra_bit_name.if.004` | 2630 | `if ( extra_flags & ITEM_LOCK         )` |  | pending |
| `handler.extra_bit_name.if.005` | 2631 | `if ( extra_flags & ITEM_EVIL         )` |  | pending |
| `handler.extra_bit_name.if.006` | 2632 | `if ( extra_flags & ITEM_INVIS        )` |  | pending |
| `handler.extra_bit_name.if.007` | 2633 | `if ( extra_flags & ITEM_MAGIC        )` |  | pending |
| `handler.extra_bit_name.if.008` | 2634 | `if ( extra_flags & ITEM_NODROP       )` |  | pending |
| `handler.extra_bit_name.if.009` | 2635 | `if ( extra_flags & ITEM_BLESS        )` |  | pending |
| `handler.extra_bit_name.if.010` | 2636 | `if ( extra_flags & ITEM_ANTI_GOOD    )` |  | pending |
| `handler.extra_bit_name.if.011` | 2637 | `if ( extra_flags & ITEM_ANTI_EVIL    )` |  | pending |
| `handler.extra_bit_name.if.012` | 2638 | `if ( extra_flags & ITEM_ANTI_NEUTRAL )` |  | pending |
| `handler.extra_bit_name.if.013` | 2639 | `if ( extra_flags & ITEM_NOREMOVE     )` |  | pending |
| `handler.extra_bit_name.if.014` | 2640 | `if ( extra_flags & ITEM_INVENTORY    )` |  | pending |
| `handler.extra_bit_name.if.015` | 2641 | `if ( extra_flags & ITEM_NOPURGE	 )` |  | pending |
| `handler.extra_bit_name.if.016` | 2642 | `if ( extra_flags & ITEM_VIS_DEATH	 )` |  | pending |
| `handler.extra_bit_name.if.017` | 2643 | `if ( extra_flags & ITEM_ROT_DEATH	 )` |  | pending |
| `handler.extra_bit_name.if.018` | 2644 | `if ( extra_flags & ITEM_NOLOCATE	 )` |  | pending |
| `handler.extra_bit_name.if.019` | 2645 | `if ( extra_flags & ITEM_SELL_EXTRACT )` |  | pending |
| `handler.extra_bit_name.if.020` | 2646 | `if ( extra_flags & ITEM_BURN_PROOF	 )` |  | pending |
| `handler.extra_bit_name.if.021` | 2647 | `if ( extra_flags & ITEM_NOUNCURSE	 )` |  | pending |
| `handler.extra_bit_name.return.001` | 2648 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.extra_bit_name.ternary.001` | 2648 | `? buf+1 : "none";` |  | pending |

## act_bit_name

[Source line 2652](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2652); ends at line 2699. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_mstat: `src/act_wiz.c:1645` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2261` (declaration_or_dispatch_reference).

Dependencies: `IS_SET`, `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.act_bit_name.if.001` | 2658 | `if (IS_SET(act_flags,ACT_IS_NPC))` |  | pending |
| `handler.act_bit_name.if.002` | 2661 | `if (act_flags & ACT_SENTINEL 	)` |  | pending |
| `handler.act_bit_name.if.003` | 2662 | `if (act_flags & ACT_SCAVENGER	)` |  | pending |
| `handler.act_bit_name.if.004` | 2663 | `if (act_flags & ACT_AGGRESSIVE	)` |  | pending |
| `handler.act_bit_name.if.005` | 2664 | `if (act_flags & ACT_STAY_AREA	)` |  | pending |
| `handler.act_bit_name.if.006` | 2665 | `if (act_flags & ACT_WIMPY	)` |  | pending |
| `handler.act_bit_name.if.007` | 2666 | `if (act_flags & ACT_PET		)` |  | pending |
| `handler.act_bit_name.if.008` | 2667 | `if (act_flags & ACT_TRAIN	)` |  | pending |
| `handler.act_bit_name.if.009` | 2668 | `if (act_flags & ACT_PRACTICE	)` |  | pending |
| `handler.act_bit_name.if.010` | 2669 | `if (act_flags & ACT_UNDEAD	)` |  | pending |
| `handler.act_bit_name.if.011` | 2670 | `if (act_flags & ACT_CLERIC	)` |  | pending |
| `handler.act_bit_name.if.012` | 2671 | `if (act_flags & ACT_MAGE	)` |  | pending |
| `handler.act_bit_name.if.013` | 2672 | `if (act_flags & ACT_THIEF	)` |  | pending |
| `handler.act_bit_name.if.014` | 2673 | `if (act_flags & ACT_WARRIOR	)` |  | pending |
| `handler.act_bit_name.if.015` | 2674 | `if (act_flags & ACT_NOALIGN	)` |  | pending |
| `handler.act_bit_name.if.016` | 2675 | `if (act_flags & ACT_NOPURGE	)` |  | pending |
| `handler.act_bit_name.if.017` | 2676 | `if (act_flags & ACT_IS_HEALER	)` |  | pending |
| `handler.act_bit_name.if.018` | 2677 | `if (act_flags & ACT_IS_CHANGER  )` |  | pending |
| `handler.act_bit_name.if.019` | 2678 | `if (act_flags & ACT_GAIN	)` |  | pending |
| `handler.act_bit_name.if.020` | 2679 | `if (act_flags & ACT_UPDATE_ALWAYS)` |  | pending |
| `handler.act_bit_name.if.021` | 2684 | `if (act_flags & PLR_AUTOASSIST	)` |  | pending |
| `handler.act_bit_name.if.022` | 2685 | `if (act_flags & PLR_AUTOEXIT	)` |  | pending |
| `handler.act_bit_name.if.023` | 2686 | `if (act_flags & PLR_AUTOLOOT	)` |  | pending |
| `handler.act_bit_name.if.024` | 2687 | `if (act_flags & PLR_AUTOSAC	)` |  | pending |
| `handler.act_bit_name.if.025` | 2688 | `if (act_flags & PLR_AUTOGOLD	)` |  | pending |
| `handler.act_bit_name.if.026` | 2689 | `if (act_flags & PLR_AUTOSPLIT	)` |  | pending |
| `handler.act_bit_name.if.027` | 2690 | `if (act_flags & PLR_HOLYLIGHT	)` |  | pending |
| `handler.act_bit_name.if.028` | 2691 | `if (act_flags & PLR_CANLOOT	)` |  | pending |
| `handler.act_bit_name.if.029` | 2692 | `if (act_flags & PLR_NOSUMMON	)` |  | pending |
| `handler.act_bit_name.if.030` | 2693 | `if (act_flags & PLR_NOFOLLOW	)` |  | pending |
| `handler.act_bit_name.if.031` | 2694 | `if (act_flags & PLR_FREEZE	)` |  | pending |
| `handler.act_bit_name.if.032` | 2695 | `if (act_flags & PLR_THIEF	)` |  | pending |
| `handler.act_bit_name.if.033` | 2696 | `if (act_flags & PLR_KILLER	)` |  | pending |
| `handler.act_bit_name.return.001` | 2698 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.act_bit_name.ternary.001` | 2698 | `? buf+1 : "none";` |  | pending |

## comm_bit_name

[Source line 2701](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2701); ends at line 2726. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_mstat: `src/act_wiz.c:1650` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2267` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.comm_bit_name.if.001` | 2707 | `if (comm_flags & COMM_QUIET		)` |  | pending |
| `handler.comm_bit_name.if.002` | 2708 | `if (comm_flags & COMM_DEAF		)` |  | pending |
| `handler.comm_bit_name.if.003` | 2709 | `if (comm_flags & COMM_NOWIZ		)` |  | pending |
| `handler.comm_bit_name.if.004` | 2710 | `if (comm_flags & COMM_NOAUCTION	)` |  | pending |
| `handler.comm_bit_name.if.005` | 2711 | `if (comm_flags & COMM_NOGOSSIP	)` |  | pending |
| `handler.comm_bit_name.if.006` | 2712 | `if (comm_flags & COMM_NOQUESTION	)` |  | pending |
| `handler.comm_bit_name.if.007` | 2713 | `if (comm_flags & COMM_NOMUSIC	)` |  | pending |
| `handler.comm_bit_name.if.008` | 2714 | `if (comm_flags & COMM_NOQUOTE	)` |  | pending |
| `handler.comm_bit_name.if.009` | 2715 | `if (comm_flags & COMM_COMPACT	)` |  | pending |
| `handler.comm_bit_name.if.010` | 2716 | `if (comm_flags & COMM_BRIEF		)` |  | pending |
| `handler.comm_bit_name.if.011` | 2717 | `if (comm_flags & COMM_PROMPT	)` |  | pending |
| `handler.comm_bit_name.if.012` | 2718 | `if (comm_flags & COMM_COMBINE	)` |  | pending |
| `handler.comm_bit_name.if.013` | 2719 | `if (comm_flags & COMM_NOEMOTE	)` |  | pending |
| `handler.comm_bit_name.if.014` | 2720 | `if (comm_flags & COMM_NOSHOUT	)` |  | pending |
| `handler.comm_bit_name.if.015` | 2721 | `if (comm_flags & COMM_NOTELL	)` |  | pending |
| `handler.comm_bit_name.if.016` | 2722 | `if (comm_flags & COMM_NOCHANNELS	)` |  | pending |
| `handler.comm_bit_name.return.001` | 2725 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.comm_bit_name.ternary.001` | 2725 | `? buf+1 : "none";` |  | pending |

## imm_bit_name

[Source line 2728](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2728); ends at line 2758. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_ostat: `src/act_wiz.c:1461` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1465` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1469` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1500` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1504` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1508` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1662` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1668` (lexical_call_candidate).
- do_mstat: `src/act_wiz.c:1674` (lexical_call_candidate).
- spell_identify: `src/magic.c:3382` (lexical_call_candidate).
- spell_identify: `src/magic.c:3386` (lexical_call_candidate).
- spell_identify: `src/magic.c:3390` (lexical_call_candidate).
- spell_identify: `src/magic.c:3432` (lexical_call_candidate).
- spell_identify: `src/magic.c:3436` (lexical_call_candidate).
- spell_identify: `src/magic.c:3440` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2263` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.imm_bit_name.if.001` | 2734 | `if (imm_flags & IMM_SUMMON		)` |  | pending |
| `handler.imm_bit_name.if.002` | 2735 | `if (imm_flags & IMM_CHARM		)` |  | pending |
| `handler.imm_bit_name.if.003` | 2736 | `if (imm_flags & IMM_MAGIC		)` |  | pending |
| `handler.imm_bit_name.if.004` | 2737 | `if (imm_flags & IMM_WEAPON		)` |  | pending |
| `handler.imm_bit_name.if.005` | 2738 | `if (imm_flags & IMM_BASH		)` |  | pending |
| `handler.imm_bit_name.if.006` | 2739 | `if (imm_flags & IMM_PIERCE		)` |  | pending |
| `handler.imm_bit_name.if.007` | 2740 | `if (imm_flags & IMM_SLASH		)` |  | pending |
| `handler.imm_bit_name.if.008` | 2741 | `if (imm_flags & IMM_FIRE		)` |  | pending |
| `handler.imm_bit_name.if.009` | 2742 | `if (imm_flags & IMM_COLD		)` |  | pending |
| `handler.imm_bit_name.if.010` | 2743 | `if (imm_flags & IMM_LIGHTNING	)` |  | pending |
| `handler.imm_bit_name.if.011` | 2744 | `if (imm_flags & IMM_ACID		)` |  | pending |
| `handler.imm_bit_name.if.012` | 2745 | `if (imm_flags & IMM_POISON		)` |  | pending |
| `handler.imm_bit_name.if.013` | 2746 | `if (imm_flags & IMM_NEGATIVE	)` |  | pending |
| `handler.imm_bit_name.if.014` | 2747 | `if (imm_flags & IMM_HOLY		)` |  | pending |
| `handler.imm_bit_name.if.015` | 2748 | `if (imm_flags & IMM_ENERGY		)` |  | pending |
| `handler.imm_bit_name.if.016` | 2749 | `if (imm_flags & IMM_MENTAL		)` |  | pending |
| `handler.imm_bit_name.if.017` | 2750 | `if (imm_flags & IMM_DISEASE	)` |  | pending |
| `handler.imm_bit_name.if.018` | 2751 | `if (imm_flags & IMM_DROWNING	)` |  | pending |
| `handler.imm_bit_name.if.019` | 2752 | `if (imm_flags & IMM_LIGHT		)` |  | pending |
| `handler.imm_bit_name.if.020` | 2753 | `if (imm_flags & VULN_IRON		)` |  | pending |
| `handler.imm_bit_name.if.021` | 2754 | `if (imm_flags & VULN_WOOD		)` |  | pending |
| `handler.imm_bit_name.if.022` | 2755 | `if (imm_flags & VULN_SILVER	)` |  | pending |
| `handler.imm_bit_name.return.001` | 2757 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.imm_bit_name.ternary.001` | 2757 | `? buf+1 : "none";` |  | pending |

## wear_bit_name

[Source line 2760](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2760); ends at line 2784. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_ostat: `src/act_wiz.c:1239` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2260` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.wear_bit_name.if.001` | 2765 | `if (wear_flags & ITEM_TAKE		)` |  | pending |
| `handler.wear_bit_name.if.002` | 2766 | `if (wear_flags & ITEM_WEAR_FINGER	)` |  | pending |
| `handler.wear_bit_name.if.003` | 2767 | `if (wear_flags & ITEM_WEAR_NECK	)` |  | pending |
| `handler.wear_bit_name.if.004` | 2768 | `if (wear_flags & ITEM_WEAR_BODY	)` |  | pending |
| `handler.wear_bit_name.if.005` | 2769 | `if (wear_flags & ITEM_WEAR_HEAD	)` |  | pending |
| `handler.wear_bit_name.if.006` | 2770 | `if (wear_flags & ITEM_WEAR_LEGS	)` |  | pending |
| `handler.wear_bit_name.if.007` | 2771 | `if (wear_flags & ITEM_WEAR_FEET	)` |  | pending |
| `handler.wear_bit_name.if.008` | 2772 | `if (wear_flags & ITEM_WEAR_HANDS	)` |  | pending |
| `handler.wear_bit_name.if.009` | 2773 | `if (wear_flags & ITEM_WEAR_ARMS	)` |  | pending |
| `handler.wear_bit_name.if.010` | 2774 | `if (wear_flags & ITEM_WEAR_SHIELD	)` |  | pending |
| `handler.wear_bit_name.if.011` | 2775 | `if (wear_flags & ITEM_WEAR_ABOUT	)` |  | pending |
| `handler.wear_bit_name.if.012` | 2776 | `if (wear_flags & ITEM_WEAR_WAIST	)` |  | pending |
| `handler.wear_bit_name.if.013` | 2777 | `if (wear_flags & ITEM_WEAR_WRIST	)` |  | pending |
| `handler.wear_bit_name.if.014` | 2778 | `if (wear_flags & ITEM_WIELD		)` |  | pending |
| `handler.wear_bit_name.if.015` | 2779 | `if (wear_flags & ITEM_HOLD		)` |  | pending |
| `handler.wear_bit_name.if.016` | 2780 | `if (wear_flags & ITEM_NO_SAC	)` |  | pending |
| `handler.wear_bit_name.if.017` | 2781 | `if (wear_flags & ITEM_WEAR_FLOAT	)` |  | pending |
| `handler.wear_bit_name.return.001` | 2783 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.wear_bit_name.ternary.001` | 2783 | `? buf+1 : "none";` |  | pending |

## form_bit_name

[Source line 2786](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2786); ends at line 2819. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_mstat: `src/act_wiz.c:1679` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2264` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.form_bit_name.if.001` | 2791 | `if (form_flags & FORM_POISON	)` |  | pending |
| `handler.form_bit_name.if.002` | 2792 | `if (form_flags & FORM_EDIBLE	)` |  | pending |
| `handler.form_bit_name.if.003` | 2793 | `if (form_flags & FORM_MAGICAL	)` |  | pending |
| `handler.form_bit_name.if.004` | 2794 | `if (form_flags & FORM_INSTANT_DECAY	)` |  | pending |
| `handler.form_bit_name.if.005` | 2795 | `if (form_flags & FORM_OTHER		)` |  | pending |
| `handler.form_bit_name.if.006` | 2796 | `if (form_flags & FORM_ANIMAL	)` |  | pending |
| `handler.form_bit_name.if.007` | 2797 | `if (form_flags & FORM_SENTIENT	)` |  | pending |
| `handler.form_bit_name.if.008` | 2798 | `if (form_flags & FORM_UNDEAD	)` |  | pending |
| `handler.form_bit_name.if.009` | 2799 | `if (form_flags & FORM_CONSTRUCT	)` |  | pending |
| `handler.form_bit_name.if.010` | 2800 | `if (form_flags & FORM_MIST		)` |  | pending |
| `handler.form_bit_name.if.011` | 2801 | `if (form_flags & FORM_INTANGIBLE	)` |  | pending |
| `handler.form_bit_name.if.012` | 2802 | `if (form_flags & FORM_BIPED		)` |  | pending |
| `handler.form_bit_name.if.013` | 2803 | `if (form_flags & FORM_CENTAUR	)` |  | pending |
| `handler.form_bit_name.if.014` | 2804 | `if (form_flags & FORM_INSECT	)` |  | pending |
| `handler.form_bit_name.if.015` | 2805 | `if (form_flags & FORM_SPIDER	)` |  | pending |
| `handler.form_bit_name.if.016` | 2806 | `if (form_flags & FORM_CRUSTACEAN	)` |  | pending |
| `handler.form_bit_name.if.017` | 2807 | `if (form_flags & FORM_WORM		)` |  | pending |
| `handler.form_bit_name.if.018` | 2808 | `if (form_flags & FORM_BLOB		)` |  | pending |
| `handler.form_bit_name.if.019` | 2809 | `if (form_flags & FORM_MAMMAL	)` |  | pending |
| `handler.form_bit_name.if.020` | 2810 | `if (form_flags & FORM_BIRD		)` |  | pending |
| `handler.form_bit_name.if.021` | 2811 | `if (form_flags & FORM_REPTILE	)` |  | pending |
| `handler.form_bit_name.if.022` | 2812 | `if (form_flags & FORM_SNAKE		)` |  | pending |
| `handler.form_bit_name.if.023` | 2813 | `if (form_flags & FORM_DRAGON	)` |  | pending |
| `handler.form_bit_name.if.024` | 2814 | `if (form_flags & FORM_AMPHIBIAN	)` |  | pending |
| `handler.form_bit_name.if.025` | 2815 | `if (form_flags & FORM_FISH		)` |  | pending |
| `handler.form_bit_name.if.026` | 2816 | `if (form_flags & FORM_COLD_BLOOD 	)` |  | pending |
| `handler.form_bit_name.return.001` | 2818 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.form_bit_name.ternary.001` | 2818 | `? buf+1 : "none";` |  | pending |

## part_bit_name

[Source line 2821](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2821); ends at line 2849. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_mstat: `src/act_wiz.c:1679` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2265` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.part_bit_name.if.001` | 2826 | `if (part_flags & PART_HEAD		)` |  | pending |
| `handler.part_bit_name.if.002` | 2827 | `if (part_flags & PART_ARMS		)` |  | pending |
| `handler.part_bit_name.if.003` | 2828 | `if (part_flags & PART_LEGS		)` |  | pending |
| `handler.part_bit_name.if.004` | 2829 | `if (part_flags & PART_HEART		)` |  | pending |
| `handler.part_bit_name.if.005` | 2830 | `if (part_flags & PART_BRAINS	)` |  | pending |
| `handler.part_bit_name.if.006` | 2831 | `if (part_flags & PART_GUTS		)` |  | pending |
| `handler.part_bit_name.if.007` | 2832 | `if (part_flags & PART_HANDS		)` |  | pending |
| `handler.part_bit_name.if.008` | 2833 | `if (part_flags & PART_FEET		)` |  | pending |
| `handler.part_bit_name.if.009` | 2834 | `if (part_flags & PART_FINGERS	)` |  | pending |
| `handler.part_bit_name.if.010` | 2835 | `if (part_flags & PART_EAR		)` |  | pending |
| `handler.part_bit_name.if.011` | 2836 | `if (part_flags & PART_EYE		)` |  | pending |
| `handler.part_bit_name.if.012` | 2837 | `if (part_flags & PART_LONG_TONGUE	)` |  | pending |
| `handler.part_bit_name.if.013` | 2838 | `if (part_flags & PART_EYESTALKS	)` |  | pending |
| `handler.part_bit_name.if.014` | 2839 | `if (part_flags & PART_TENTACLES	)` |  | pending |
| `handler.part_bit_name.if.015` | 2840 | `if (part_flags & PART_FINS		)` |  | pending |
| `handler.part_bit_name.if.016` | 2841 | `if (part_flags & PART_WINGS		)` |  | pending |
| `handler.part_bit_name.if.017` | 2842 | `if (part_flags & PART_TAIL		)` |  | pending |
| `handler.part_bit_name.if.018` | 2843 | `if (part_flags & PART_CLAWS		)` |  | pending |
| `handler.part_bit_name.if.019` | 2844 | `if (part_flags & PART_FANGS		)` |  | pending |
| `handler.part_bit_name.if.020` | 2845 | `if (part_flags & PART_HORNS		)` |  | pending |
| `handler.part_bit_name.if.021` | 2846 | `if (part_flags & PART_SCALES	)` |  | pending |
| `handler.part_bit_name.return.001` | 2848 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.part_bit_name.ternary.001` | 2848 | `? buf+1 : "none";` |  | pending |

## weapon_bit_name

[Source line 2851](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2851); ends at line 2866. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_ostat: `src/act_wiz.c:1384` (lexical_call_candidate).
- do_ostat: `src/act_wiz.c:1453` (lexical_call_candidate).
- spell_identify: `src/magic.c:3347` (lexical_call_candidate).
- spell_identify: `src/magic.c:3428` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2266` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.weapon_bit_name.if.001` | 2856 | `if (weapon_flags & WEAPON_FLAMING	)` |  | pending |
| `handler.weapon_bit_name.if.002` | 2857 | `if (weapon_flags & WEAPON_FROST	)` |  | pending |
| `handler.weapon_bit_name.if.003` | 2858 | `if (weapon_flags & WEAPON_VAMPIRIC	)` |  | pending |
| `handler.weapon_bit_name.if.004` | 2859 | `if (weapon_flags & WEAPON_SHARP	)` |  | pending |
| `handler.weapon_bit_name.if.005` | 2860 | `if (weapon_flags & WEAPON_VORPAL	)` |  | pending |
| `handler.weapon_bit_name.if.006` | 2861 | `if (weapon_flags & WEAPON_TWO_HANDS )` |  | pending |
| `handler.weapon_bit_name.if.007` | 2862 | `if (weapon_flags & WEAPON_SHOCKING 	)` |  | pending |
| `handler.weapon_bit_name.if.008` | 2863 | `if (weapon_flags & WEAPON_POISON	)` |  | pending |
| `handler.weapon_bit_name.return.001` | 2865 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.weapon_bit_name.ternary.001` | 2865 | `? buf+1 : "none";` |  | pending |

## cont_bit_name

[Source line 2868](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2868); ends at line 2880. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_ostat: `src/act_wiz.c:1398` (lexical_call_candidate).
- spell_identify: `src/magic.c:3311` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2268` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.cont_bit_name.if.001` | 2874 | `if (cont_flags & CONT_CLOSEABLE	)` |  | pending |
| `handler.cont_bit_name.if.002` | 2875 | `if (cont_flags & CONT_PICKPROOF	)` |  | pending |
| `handler.cont_bit_name.if.003` | 2876 | `if (cont_flags & CONT_CLOSED	)` |  | pending |
| `handler.cont_bit_name.if.004` | 2877 | `if (cont_flags & CONT_LOCKED	)` |  | pending |
| `handler.cont_bit_name.return.001` | 2879 | `return (buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.cont_bit_name.ternary.001` | 2879 | `? buf+1 : "none";` |  | pending |

## off_bit_name

[Source line 2883](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2883); ends at line 2912. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_mstat: `src/act_wiz.c:1656` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/merc.h:2262` (declaration_or_dispatch_reference).

Dependencies: `strcat`, `return`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `handler.off_bit_name.if.001` | 2889 | `if (off_flags & OFF_AREA_ATTACK	)` |  | pending |
| `handler.off_bit_name.if.002` | 2890 | `if (off_flags & OFF_BACKSTAB	)` |  | pending |
| `handler.off_bit_name.if.003` | 2891 | `if (off_flags & OFF_BASH		)` |  | pending |
| `handler.off_bit_name.if.004` | 2892 | `if (off_flags & OFF_BERSERK		)` |  | pending |
| `handler.off_bit_name.if.005` | 2893 | `if (off_flags & OFF_DISARM		)` |  | pending |
| `handler.off_bit_name.if.006` | 2894 | `if (off_flags & OFF_DODGE		)` |  | pending |
| `handler.off_bit_name.if.007` | 2895 | `if (off_flags & OFF_FADE		)` |  | pending |
| `handler.off_bit_name.if.008` | 2896 | `if (off_flags & OFF_FAST		)` |  | pending |
| `handler.off_bit_name.if.009` | 2897 | `if (off_flags & OFF_KICK		)` |  | pending |
| `handler.off_bit_name.if.010` | 2898 | `if (off_flags & OFF_KICK_DIRT	)` |  | pending |
| `handler.off_bit_name.if.011` | 2899 | `if (off_flags & OFF_PARRY		)` |  | pending |
| `handler.off_bit_name.if.012` | 2900 | `if (off_flags & OFF_RESCUE		)` |  | pending |
| `handler.off_bit_name.if.013` | 2901 | `if (off_flags & OFF_TAIL		)` |  | pending |
| `handler.off_bit_name.if.014` | 2902 | `if (off_flags & OFF_TRIP		)` |  | pending |
| `handler.off_bit_name.if.015` | 2903 | `if (off_flags & OFF_CRUSH		)` |  | pending |
| `handler.off_bit_name.if.016` | 2904 | `if (off_flags & ASSIST_ALL		)` |  | pending |
| `handler.off_bit_name.if.017` | 2905 | `if (off_flags & ASSIST_ALIGN	)` |  | pending |
| `handler.off_bit_name.if.018` | 2906 | `if (off_flags & ASSIST_RACE		)` |  | pending |
| `handler.off_bit_name.if.019` | 2907 | `if (off_flags & ASSIST_PLAYERS	)` |  | pending |
| `handler.off_bit_name.if.020` | 2908 | `if (off_flags & ASSIST_GUARD	)` |  | pending |
| `handler.off_bit_name.if.021` | 2909 | `if (off_flags & ASSIST_VNUM		)` |  | pending |
| `handler.off_bit_name.return.001` | 2911 | `return ( buf[0] != '\0' ) ? buf+1 : "none";` |  | pending |
| `handler.off_bit_name.ternary.001` | 2911 | `? buf+1 : "none";` |  | pending |

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
- Line 37: `#include "merc.h"` — pending configuration/reachability review.
- Line 38: `#include "interp.h"` — pending configuration/reachability review.
- Line 39: `#include "magic.h"` — pending configuration/reachability review.
- Line 40: `#include "recycle.h"` — pending configuration/reachability review.
- Line 41: `#include "tables.h"` — pending configuration/reachability review.

## Static tables


## Commented code candidates

- Lines 1931–1937: disabled inside block comment; content hash `bdf289c0d729a8454c6a82484fe72247bdb8962b86d4692f60482f28f7d91bc9`.

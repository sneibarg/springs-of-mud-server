# src/recycle.c

Role: translation_unit. Disposition: **pending**. SHA-256: `e865a8e902cca05d5ff1917986837a12606bfe6c540da52568051917a57602d6`.

This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.

## new_note

[Source line 44](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:44); ends at line 57. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- note_attach: `src/note.c:372` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:45` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_note.if.001` | 48 | `if (note_free == NULL)` |  | pending |
| `recycle.new_note.return.001` | 56 | `return note;` |  | pending |

## free_note

[Source line 59](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:59); ends at line 73. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_thread: `src/note.c:263` (lexical_call_candidate).
- note_remove: `src/note.c:465` (lexical_call_candidate).
- parse_note: `src/note.c:884` (lexical_call_candidate).
- free_char: `src/recycle.c:373` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:46` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `free_string`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_note.if.001` | 61 | `if (!IS_VALID(note))` |  | pending |
| `recycle.free_note.return.001` | 62 | `return;` |  | pending |

## new_ban

[Source line 79](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:79); ends at line 96. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_bans: `src/ban.c:90` (lexical_call_candidate).
- ban_site: `src/ban.c:234` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:51` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_ban.if.001` | 84 | `if (ban_free == NULL)` |  | pending |
| `recycle.new_ban.return.001` | 95 | `return ban;` |  | pending |

## free_ban

[Source line 98](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:98); ends at line 108. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- ban_site: `src/ban.c:229` (lexical_call_candidate).
- do_allow: `src/ban.c:297` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:52` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `free_string`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_ban.if.001` | 100 | `if (!IS_VALID(ban))` |  | pending |
| `recycle.free_ban.return.001` | 101 | `return;` |  | pending |

## new_descriptor

[Source line 113](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:113); ends at line 129. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- init_descriptor: `src/comm.c:888` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:57` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_descriptor.if.001` | 118 | `if (descriptor_free == NULL)` |  | pending |
| `recycle.new_descriptor.return.001` | 128 | `return d;` |  | pending |

## free_descriptor

[Source line 131](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:131); ends at line 141. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- init_descriptor: `src/comm.c:936` (lexical_call_candidate).
- close_socket: `src/comm.c:1023` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:58` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `free_string`, `free_mem`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_descriptor.if.001` | 133 | `if (!IS_VALID(d))` |  | pending |
| `recycle.free_descriptor.return.001` | 134 | `return;` |  | pending |

## new_gen_data

[Source line 146](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:146); ends at line 161. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:1947` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:63` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_gen_data.if.001` | 151 | `if (gen_data_free == NULL)` |  | pending |
| `recycle.new_gen_data.return.001` | 160 | `return gen;` |  | pending |

## free_gen_data

[Source line 163](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:163); ends at line 172. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- nanny: `src/comm.c:2029` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:64` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_gen_data.if.001` | 165 | `if (!IS_VALID(gen))` |  | pending |
| `recycle.free_gen_data.return.001` | 166 | `return;` |  | pending |

## new_extra_descr

[Source line 177](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:177); ends at line 193. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_string: `src/act_wiz.c:3847` (lexical_call_candidate).
- clone_object: `src/db.c:2004` (lexical_call_candidate).
- fread_obj: `src/save.c:1485` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:69` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_extra_descr.if.001` | 181 | `if (extra_descr_free == NULL)` |  | pending |
| `recycle.new_extra_descr.return.001` | 192 | `return ed;` |  | pending |

## free_extra_descr

[Source line 195](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:195); ends at line 206. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- free_obj: `src/recycle.c:281` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:70` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `free_string`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_extra_descr.if.001` | 197 | `if (!IS_VALID(ed))` |  | pending |
| `recycle.free_extra_descr.return.001` | 198 | `return;` |  | pending |

## new_affect

[Source line 212](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:212); ends at line 230. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- acid_effect: `src/effects.c:152` (lexical_call_candidate).
- affect_enchant: `src/handler.c:877` (lexical_call_candidate).
- affect_to_char: `src/handler.c:1106` (lexical_call_candidate).
- affect_to_obj: `src/handler.c:1123` (lexical_call_candidate).
- spell_enchant_armor: `src/magic.c:2328` (lexical_call_candidate).
- spell_enchant_armor: `src/magic.c:2379` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2521` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2574` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2603` (lexical_call_candidate).
- fread_char: `src/save.c:813` (lexical_call_candidate).
- fread_char: `src/save.c:837` (lexical_call_candidate).
- fread_pet: `src/save.c:1191` (lexical_call_candidate).
- fread_pet: `src/save.c:1215` (lexical_call_candidate).
- fread_obj: `src/save.c:1415` (lexical_call_candidate).
- fread_obj: `src/save.c:1438` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:75` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_affect.if.001` | 217 | `if (affect_free == NULL)` |  | pending |
| `recycle.new_affect.return.001` | 229 | `return af;` |  | pending |

## free_affect

[Source line 232](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:232); ends at line 240. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- affect_remove: `src/handler.c:1192` (lexical_call_candidate).
- affect_remove_obj: `src/handler.c:1250` (lexical_call_candidate).
- spell_enchant_armor: `src/magic.c:2305` (lexical_call_candidate).
- spell_enchant_weapon: `src/magic.c:2498` (lexical_call_candidate).
- free_obj: `src/recycle.c:274` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:76` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_affect.if.001` | 234 | `if (!IS_VALID(af))` |  | pending |
| `recycle.free_affect.return.001` | 235 | `return;` |  | pending |

## new_obj

[Source line 245](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:245); ends at line 261. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_clone: `src/act_wiz.c:2386` (function_symbol_reference_candidate).
- do_clone: `src/act_wiz.c:2413` (function_symbol_reference_candidate).
- do_clone: `src/act_wiz.c:2414` (function_symbol_reference_candidate).
- do_clone: `src/act_wiz.c:2415` (function_symbol_reference_candidate).
- do_clone: `src/act_wiz.c:2416` (function_symbol_reference_candidate).
- do_clone: `src/act_wiz.c:2417` (function_symbol_reference_candidate).
- create_object: `src/db.c:1836` (lexical_call_candidate).
- fread_obj: `src/save.c:1384` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:81` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_obj.if.001` | 250 | `if (obj_free == NULL)` |  | pending |
| `recycle.new_obj.return.001` | 260 | `return obj;` |  | pending |

## free_obj

[Source line 263](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:263); ends at line 293. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- extract_obj: `src/handler.c:1916` (lexical_call_candidate).
- fread_obj: `src/save.c:1499` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:82` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `free_affect`, `free_extra_descr`, `free_string`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_obj.if.001` | 268 | `if (!IS_VALID(obj))` |  | pending |
| `recycle.free_obj.return.001` | 269 | `return;` |  | pending |
| `recycle.free_obj.for.001` | 271 | `for (paf = obj->affected; paf != NULL; paf = paf_next)` |  | pending |
| `recycle.free_obj.for.002` | 278 | `for (ed = obj->extra_descr; ed != NULL; ed = ed_next )` |  | pending |

## new_char

[Source line 299](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:299); ends at line 339. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- create_mobile: `src/db.c:1530` (lexical_call_candidate).
- load_char_obj: `src/save.c:549` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:88` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_char.if.001` | 305 | `if (char_free == NULL)` |  | pending |
| `recycle.new_char.for.001` | 323 | `for (i = 0; i < 4; i++)` |  | pending |
| `recycle.new_char.for.002` | 332 | `for (i = 0; i < MAX_STATS; i ++)` |  | pending |
| `recycle.new_char.return.001` | 338 | `return ch;` |  | pending |

## free_char

[Source line 342](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:342); ends at line 381. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- close_socket: `src/comm.c:998` (lexical_call_candidate).
- nanny: `src/comm.c:1706` (lexical_call_candidate).
- nanny: `src/comm.c:1716` (lexical_call_candidate).
- nanny: `src/comm.c:1740` (lexical_call_candidate).
- check_reconnect: `src/comm.c:2264` (lexical_call_candidate).
- extract_char: `src/handler.c:2005` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:89` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `IS_NPC`, `extract_obj`, `affect_remove`, `free_string`, `free_note`, `free_pcdata`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_char.if.001` | 349 | `if (!IS_VALID(ch))` |  | pending |
| `recycle.free_char.return.001` | 350 | `return;` |  | pending |
| `recycle.free_char.if.002` | 352 | `if (IS_NPC(ch))` |  | pending |
| `recycle.free_char.for.001` | 355 | `for (obj = ch->carrying; obj != NULL; obj = obj_next)` |  | pending |
| `recycle.free_char.for.002` | 361 | `for (paf = ch->affected; paf != NULL; paf = paf_next)` |  | pending |
| `recycle.free_char.return.002` | 380 | `return;` |  | pending |

## new_pcdata

[Source line 385](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:385); ends at line 412. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_char_obj: `src/save.c:550` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:90` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `new_buf`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_pcdata.if.001` | 392 | `if (pcdata_free == NULL)` |  | pending |
| `recycle.new_pcdata.for.001` | 402 | `for (alias = 0; alias < MAX_ALIAS; alias++)` |  | pending |
| `recycle.new_pcdata.return.001` | 411 | `return pcdata;` |  | pending |

## free_pcdata

[Source line 415](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:415); ends at line 438. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- free_char: `src/recycle.c:374` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:91` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `free_string`, `free_buf`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_pcdata.if.001` | 419 | `if (!IS_VALID(pcdata))` |  | pending |
| `recycle.free_pcdata.return.001` | 420 | `return;` |  | pending |
| `recycle.free_pcdata.for.001` | 428 | `for (alias = 0; alias < MAX_ALIAS; alias++)` |  | pending |
| `recycle.free_pcdata.return.002` | 437 | `return;` |  | pending |

## get_pc_id

[Source line 447](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:447); ends at line 454. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- load_char_obj: `src/save.c:555` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:98` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.get_pc_id.ternary.001` | 451 | `? last_pc_id + 1 : current_time;` |  | pending |
| `recycle.get_pc_id.return.001` | 453 | `return val;` |  | pending |

## get_mob_id

[Source line 456](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:456); ends at line 460. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- create_mobile: `src/db.c:1535` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:99` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.get_mob_id.return.001` | 459 | `return last_mob_id;` |  | pending |

## new_mem_data

[Source line 468](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:468); ends at line 487. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/recycle.h:100` (declaration_or_dispatch_reference).

Dependencies: `alloc_mem`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_mem_data.if.001` | 472 | `if (mem_data_free == NULL)` |  | pending |
| `recycle.new_mem_data.return.001` | 486 | `return memory;` |  | pending |

## free_mem_data

[Source line 489](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:489); ends at line 497. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/recycle.h:101` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_mem_data.if.001` | 491 | `if (!IS_VALID(memory))` |  | pending |
| `recycle.free_mem_data.return.001` | 492 | `return;` |  | pending |

## get_size

[Source line 509](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:509); ends at line 520. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- new_buf: `src/recycle.c:536` (lexical_call_candidate).
- new_buf_size: `src/recycle.c:559` (lexical_call_candidate).
- add_buf: `src/recycle.c:605` (lexical_call_candidate).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.get_size.for.001` | 513 | `for (i = 0; i < MAX_BUF_LIST; i++)` |  | pending |
| `recycle.get_size.if.001` | 514 | `if (buf_size[i] >= val)` |  | pending |
| `recycle.get_size.return.001` | 516 | `return buf_size[i];` |  | pending |
| `recycle.get_size.return.002` | 519 | `return -1;` |  | pending |

## new_buf

[Source line 522](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:522); ends at line 543. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_list_to_char: `src/act_info.c:146` (lexical_call_candidate).
- do_help: `src/act_info.c:1753` (lexical_call_candidate).
- do_whois: `src/act_info.c:1827` (lexical_call_candidate).
- do_who: `src/act_info.c:2007` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1879` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1941` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1968` (lexical_call_candidate).
- ban_site: `src/ban.c:156` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3598` (lexical_call_candidate).
- do_play: `src/music.c:250` (lexical_call_candidate).
- parse_note: `src/note.c:791` (lexical_call_candidate).
- new_pcdata: `src/recycle.c:408` (lexical_call_candidate).
- do_spells: `src/skills.c:366` (lexical_call_candidate).
- do_skills: `src/skills.c:483` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:107` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `get_size`, `alloc_mem`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_buf.if.001` | 526 | `if (buf_free == NULL)` |  | pending |
| `recycle.new_buf.return.001` | 542 | `return buffer;` |  | pending |

## new_buf_size

[Source line 545](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:545); ends at line 570. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- declaration_or_dispatch_reference: `src/recycle.h:108` (declaration_or_dispatch_reference).

Dependencies: `alloc_perm`, `get_size`, `bug`, `exit`, `alloc_mem`, `VALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.new_buf_size.if.001` | 549 | `if (buf_free == NULL)` |  | pending |
| `recycle.new_buf_size.if.002` | 560 | `if (buffer->size == -1)` |  | pending |
| `recycle.new_buf_size.return.001` | 569 | `return buffer;` |  | pending |

## free_buf

[Source line 573](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:573); ends at line 586. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- show_list_to_char: `src/act_info.c:234` (lexical_call_candidate).
- do_help: `src/act_info.c:1806` (lexical_call_candidate).
- do_whois: `src/act_info.c:1885` (lexical_call_candidate).
- do_who: `src/act_info.c:2078` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1923` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1963` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1990` (lexical_call_candidate).
- ban_site: `src/ban.c:175` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3641` (lexical_call_candidate).
- do_play: `src/music.c:286` (lexical_call_candidate).
- parse_note: `src/note.c:798` (lexical_call_candidate).
- free_pcdata: `src/recycle.c:426` (lexical_call_candidate).
- do_spells: `src/skills.c:372` (lexical_call_candidate).
- do_skills: `src/skills.c:489` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:109` (declaration_or_dispatch_reference).

Dependencies: `IS_VALID`, `free_mem`, `INVALIDATE`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.free_buf.if.001` | 575 | `if (!IS_VALID(buffer))` |  | pending |
| `recycle.free_buf.return.001` | 576 | `return;` |  | pending |

## add_buf

[Source line 589](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:589); ends at line 627. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_tell: `src/act_comm.c:860` (lexical_call_candidate).
- do_tell: `src/act_comm.c:889` (lexical_call_candidate).
- do_reply: `src/act_comm.c:925` (lexical_call_candidate).
- do_reply: `src/act_comm.c:961` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:211` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:215` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:218` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:219` (lexical_call_candidate).
- do_help: `src/act_info.c:1779` (lexical_call_candidate).
- do_help: `src/act_info.c:1783` (lexical_call_candidate).
- do_help: `src/act_info.c:1784` (lexical_call_candidate).
- do_help: `src/act_info.c:1791` (lexical_call_candidate).
- do_help: `src/act_info.c:1793` (lexical_call_candidate).
- do_whois: `src/act_info.c:1874` (lexical_call_candidate).
- do_who: `src/act_info.c:2072` (lexical_call_candidate).
- do_who: `src/act_info.c:2076` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1912` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1958` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1981` (lexical_call_candidate).
- ban_site: `src/ban.c:158` (lexical_call_candidate).
- ban_site: `src/ban.c:171` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3630` (lexical_call_candidate).
- do_play: `src/music.c:262` (lexical_call_candidate).
- do_play: `src/music.c:278` (lexical_call_candidate).
- do_play: `src/music.c:280` (lexical_call_candidate).
- do_play: `src/music.c:283` (lexical_call_candidate).
- parse_note: `src/note.c:793` (lexical_call_candidate).
- parse_note: `src/note.c:794` (lexical_call_candidate).
- parse_note: `src/note.c:795` (lexical_call_candidate).
- do_spells: `src/skills.c:369` (lexical_call_candidate).
- do_spells: `src/skills.c:370` (lexical_call_candidate).
- do_skills: `src/skills.c:486` (lexical_call_candidate).
- do_skills: `src/skills.c:487` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:110` (declaration_or_dispatch_reference).

Dependencies: `strlen`, `get_size`, `bug`, `alloc_mem`, `strcpy`, `free_mem`, `strcat`.

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.add_buf.if.001` | 598 | `if (buffer->state == BUFFER_OVERFLOW)` |  | pending |
| `recycle.add_buf.return.001` | 599 | `return FALSE;` |  | pending |
| `recycle.add_buf.while.001` | 603 | `while (len >= buffer->size)` |  | pending |
| `recycle.add_buf.if.002` | 607 | `if (buffer->size == -1)` |  | pending |
| `recycle.add_buf.return.002` | 612 | `return FALSE;` |  | pending |
| `recycle.add_buf.if.003` | 617 | `if (buffer->size != oldsize)` |  | pending |
| `recycle.add_buf.return.003` | 626 | `return TRUE;` |  | pending |

## clear_buf

[Source line 630](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:630); ends at line 634. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_replay: `src/act_comm.c:266` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:111` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.clear_buf.entry` | 630 | `Straight-line entry` |  | pending |

## buf_string

[Source line 637](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:637); ends at line 640. Status: pending.

Entry references (lexical candidates; caller guards still require inspection):

- do_replay: `src/act_comm.c:259` (lexical_call_candidate).
- do_replay: `src/act_comm.c:265` (lexical_call_candidate).
- show_list_to_char: `src/act_info.c:229` (lexical_call_candidate).
- do_help: `src/act_info.c:1805` (lexical_call_candidate).
- do_whois: `src/act_info.c:1884` (lexical_call_candidate).
- do_who: `src/act_info.c:2077` (lexical_call_candidate).
- do_owhere: `src/act_wiz.c:1921` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1962` (lexical_call_candidate).
- do_mwhere: `src/act_wiz.c:1988` (lexical_call_candidate).
- ban_site: `src/ban.c:174` (lexical_call_candidate).
- spell_locate_object: `src/magic.c:3639` (lexical_call_candidate).
- do_play: `src/music.c:285` (lexical_call_candidate).
- parse_note: `src/note.c:797` (lexical_call_candidate).
- do_spells: `src/skills.c:371` (lexical_call_candidate).
- do_skills: `src/skills.c:488` (lexical_call_candidate).
- declaration_or_dispatch_reference: `src/recycle.h:112` (declaration_or_dispatch_reference).

Dependencies: .

| Ledger ID | Line | Predicate/transfer | Cases | Disposition |
|---|---:|---|---|---|
| `recycle.buf_string.return.001` | 639 | `return buffer->string;` |  | pending |

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
- Line 39: `#include "recycle.h"` — pending configuration/reachability review.

## Static tables

- `buf_size` at line 502 — pending entry/termination review.

## Commented code candidates


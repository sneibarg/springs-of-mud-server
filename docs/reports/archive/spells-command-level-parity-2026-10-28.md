# Spells command level grouping

The reported single `Level 1` heading was caused by missing spell metadata: all 97 documents in `SOMDB.Spells.json` lacked `levelByClass` and `ratingByClass`. Info's learned-list helper defaulted missing requirements to level 1, so its otherwise sorted/grouped rows all shared the same level. Learned-entry `level` is proficiency and cannot supply the class acquisition level.

ROM's `do_spells` reads `skill_table[sn].skill_level[ch->class]`, accumulates a separate group for each level, and emits groups in ascending level order. Its class order is mage, cleric, thief, warrior. For example, armor has requirements 7/2/10/5; fireball has 22/53/30/26; magic missile has 1/53/2/2.

Evidence:

- [ROM listing](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/skills.c:255)
- [ROM armor requirements](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/const.c:1016)
- [Python requirement resolution](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:1094)
- [Python ordering and grouping](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:1114)

The collection now carries the exact ROM class-level and rating maps for all 97 spells. Existing IDs, payloads, formulas, and other spell fields are unchanged. Missing definitions or class requirements are excluded rather than silently presented as level-one abilities. The shared skills formatter retains its existing grouping behavior.

Validation: **507 focused tests passed** across isolated processes, including nine new collection-backed tests covering metadata loading, mage and cleric requirements, heading/order correctness, every populated level in the full spell collection, numeric ranges, future spells under `all`, zero proficiency, missing metadata, and the shared skills path. All 97 restored maps were independently compared with the local C table. Compilation and diff whitespace checks passed.

Deploy the corrected spell documents through the content service and reload spells or restart the server with the runtime change. No live external-service deployment was performed. This review covers spell-list level grouping and its metadata, not a new audit of all spell behavior.

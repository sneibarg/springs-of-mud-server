# Completed item: spec_lookup

**Complete static behavioral specification for `src/special.c:spec_lookup`.** There are 37 specified cases, no blocked cases and no unresolved dependencies within its defined entry contract. The other special procedures and the complete caller implementations remain separate report items. No runtime changes or executable gameplay tests are part of this work.

Source: [spec_lookup](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:99), lines 99–111. Snapshot HEAD reference: `d3a29007355e7298e0033fcb666e9a6895c2146f`; special.c SHA-256: `78e00c637522c18be0626547577cfa6ddcee0ac68206772d3c0409f361cdd2b6`. The [manifest](manifest.json) preserves all reviewed file hashes and the independent HEAD comparison; normal Git status is unavailable. Generation checks the reviewed table and source hash before preserving completion.

## Defined contract and dependencies

Input is a non-NULL readable NUL-terminated byte string. The helper returns a registered `SPEC_FUN` pointer or C NULL. It scans the immutable [22-entry table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:69) in order. Each row first compares the ASCII-folded initial byte; only equality evaluates `str_prefix(name, row.name)`. False from that helper means a prefix match. The first matching row returns immediately, so `s` and `spec_` select `spec_breath_any`, `spec_cast` selects `spec_cast_adept`, and `spec_breath_f` selects `spec_breath_fire` before frost.

[LOWER](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1799) folds A–Z using byte arithmetic. [str_prefix](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3164) returns true on the first folded-byte mismatch and false when the query terminator is reached. A query longer than a row mismatches that row's NUL and returns before advancing beyond it. Both pointers passed to this helper are non-null under the entry/table contracts, so its null logging guards are unreachable here. No remaining helper behavior is stubbed away.

Empty input fails the first-character test for every row: despite empty strings being prefixes in `str_prefix`, it is never called. Leading/trailing spaces are not trimmed; input is not tokenized. Byte 0xE9 does not match initial `s`, irrespective of signed-char representation. This is not Unicode or locale-dependent case folding.

The helper neither invokes the returned procedure nor mutates input/table/world state. It allocates nothing, consumes no randomness, emits no messages and performs no authorization. Its function/table have no conditional compilation alternatives. NULL input is outside its entry contract: `name[0]` is evaluated before the null-aware `str_prefix` could help. No crash, graceful failure or other portable result is asserted for invalid storage.

## Cases and full path disposition

The [case catalog](cases.json) and [pseudo suite](pseudo-suite.md) preserve the five existing IDs and add 32 cases. They include each of the 22 full names, first/interior/last matches, ambiguous and single-letter prefixes, uppercase names, same-initial-byte misses, empty/unknown input, overlong names, leading/trailing/embedded whitespace and a non-ASCII first byte.

| Control outcome | Concrete coverage | Disposition |
|---|---|---|
| Initial-byte mismatch skips `str_prefix` | empty, unknown, leading-space, whitespace-only, nonascii-first-byte | Specified |
| Initial-byte match then failed prefix continues | same-first-letter-no-prefix; every later full-name match | Specified |
| Prefix succeeds, return first matching function | every full name; single-letter and ambiguous-prefix cases | Specified |
| All rows fail, sentinel stops loop, return NULL | both short-circuit misses and prefix-comparison misses | Specified |
| One iteration | first-full, one-letter-first-match | Specified |
| Multiple iterations and early exit | all interior/last full names | Specified |
| Zero iterations | First row is non-null in immutable table | Unreachable in this snapshot |
| Mutation, callbacks, recursion | No writes or indirect invocation in helper | Absent |

For a match at index `k`, guard and initial-byte checks visit indices 0..k, and the pointer equals `spec_table[k].function`. For a miss, guards visit 0..22 and initial-byte checks only 0..21; the NULL sentinel name is never dereferenced. Every case specifies exact ordered helper calls and returns. All table names begin with `s`, so a matching initial byte means `str_prefix` runs for every visited real row. This finite control-outcome criterion covers the defined helper behavior without enumerating infinitely many possible strings.

```text
CASE special.spec_lookup.ambiguous-breath-f-first-fire
GIVEN query "spec_breath_f" and the immutable checkout table
WHEN spec_lookup is called
THEN inspect rows 0, 1, 2 in order
AND str_prefix returns TRUE, TRUE, FALSE for any, acid, fire
AND return the spec_breath_fire pointer without visiting frost or invoking fire

CASE special.spec_lookup.empty
GIVEN query "" and the same table
WHEN spec_lookup is called
THEN all 22 initial-byte comparisons fail
AND never call str_prefix, never dereference the sentinel name
AND return C NULL without messages or state changes
```

## Both caller contracts

Source-wide search identifies two call sites and a [header declaration](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:2304); no function-pointer dispatch table, tick or callback references this helper itself.

1. [boot_db](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:358) dispatches a SPECIALS section to [load_specials](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1060). For an M record, it resolves the prototype and passes the `fread_word` result to `spec_lookup`. Assignment to `pMobIndex->spec_fun` happens first. NULL then produces `bug("Load_specials: 'M': vnum %d.", vnum)` and `exit(1)`; success retains the pointer and proceeds to line consumption. The helper does not validate prototypes, parse files or exit. Area files select names but cannot change the compiled table; all 22 mappings cover its data-dependent results.
2. [do_string](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3700) applies `smash_tilde`, parses type/target/field, and copies the remaining text as the lookup name. Required fields, character/mobile type and successful victim lookup precede clearing `victim->zone`. The spec branch rejects PCs. For NPCs, [assignment](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3792) precedes the NULL test: a miss clears an existing procedure and sends `No such spec fun.\n\r` to the actor; success assigns the pointer without a confirmation message. Neither path invokes it. Trailing spaces in the remainder can turn an otherwise valid name into a miss. These are caller side effects, not lookup side effects.

The [string command](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:338) requires L5=55 trust, POS_DEAD and LOG_ALWAYS; interpreter freeze/authorization handling applies. Internal `do_function` and direct helper calls bypass those gates. The `do_string` self-dispatch with an empty argument at line 3859 reaches its syntax return, not the lookup. No authorization requirement belongs to the helper's direct contract.

## Adaptation and validation

Python's [MobileHandler._special_library](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/mobile/MobileHandler.py:345) builds a dictionary of normalized designer-provided names and behavior sequences. A neutral fixture may map names to symbolic procedure identities; assert C prefix-selection outcomes without running a special. Do not assume the Python dictionary supplies ROM's first-prefix behavior or change designer data to imitate the C table. No parity or override is claimed.

Validation checks snapshot/table identity, all 22 explicit mappings, the 37 cases' ordered comparisons, branch links and completed disposition. The source was manually traced; these checks verify artifacts, not C execution. See [verification](verification.json). There are no remaining function-level gaps; full command, loader, networking and gameplay traces retain their independent partial/pending statuses.

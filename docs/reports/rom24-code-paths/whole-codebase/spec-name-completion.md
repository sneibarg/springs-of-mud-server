# Completed item: spec_name

**Status: complete static behavioral specification for `src/special.c:spec_name`.** All 24 cases are specified; no blocked cases or unresolved dependencies remain for this function. This does not complete `special.c`, its callers, or the whole-codebase report. No executable gameplay tests were generated or run.

The source is [spec_name](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:113), lines 113–124, and the immutable [spec_table](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/special.c:69). Snapshot HEAD reference: `d3a29007355e7298e0033fcb666e9a6895c2146f`; `src/special.c` SHA-256: `78e00c637522c18be0626547577cfa6ddcee0ac68206772d3c0409f361cdd2b6`. Normal Git status is unavailable; the [manifest](manifest.json) records per-file hashes and the independent HEAD comparison. Report generation refuses to preserve this completion if the reviewed source file changes.

## Entry and return contract

Input is a valid `SPEC_FUN` function pointer or C NULL. The [type declaration](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:104) defines a function taking `CHAR_DATA *` and returning `bool`; the helper never calls it. Forged invalid pointer representations, table corruption and modification of the const table are outside the defined C entry contract, not alternative lookup outcomes.

The helper scans the table in order and returns the stored name pointer for the first equal function pointer. Equality is pointer equality, not name/prefix comparison. It returns C NULL when no entry matches, including NULL input. Names are borrowed string literals: no allocation, copy, mutation, free or ownership transfer occurs. Callers must not modify/free the returned name. No character, room, descriptor, trust, clock, randomness or game state affects the result. There are no callees, indirect calls, macros or conditional compilation inside the helper or its table.

The table contains 22 distinct registered functions at indices 0–21 and `{NULL,NULL}` at index 22. Each name is the corresponding function's spelling. Every mapping has a case in the [catalog](cases.json) and [readable pseudo suite](pseudo-suite.md). The 20 interior mappings supplement the original first/last cases; all original case IDs are retained.

## Complete path ledger

| Path/outcome | Cases | Disposition |
|---|---|---|
| First entry matches; one guard and one comparison | `special.spec_name.first-function` (`spec_breath_any`) | Specified |
| Earlier comparisons fail; an interior entry matches | 20 `special.spec_name.registered-spec_*` cases, one per index 1–20 | Specified |
| Last real entry matches | `special.spec_name.last-function` (`spec_patrolman`) | Specified |
| All real entries fail for a valid nonmember pointer | `special.spec_name.unregistered-function` | Specified |
| All real entries fail for NULL input | `special.spec_name.null-function` | Specified |
| Sentinel guard false; sentinel is never compared to input | Both all-miss cases | Specified |
| Zero loop iterations | Impossible with this immutable table: entry zero is non-null | Unreachable in this snapshot |
| Duplicate function pointers, mutation during iteration | No duplicate pointers; no callbacks/writes; const table | Not a reachable defined path in this snapshot |
| Recursion or reentry state effects | No recursion or mutable static state | Absent |

For a match at index `k`, guards and equality comparisons visit exactly 0 through `k`; return is the identical pointer `spec_table[k].name`. For a miss, guards visit 0 through 22 and equality comparisons visit only 0 through 21. The sentinel name is not returned even for NULL input. These finite classes cover every feasible control outcome in the function; they do not claim measured executable branch coverage.

```text
CASE special.spec_name.last-function
GIVEN the unmodified 22-entry table and input pointer spec_patrolman
WHEN spec_name is called once
THEN guards and equality comparisons inspect indices 0 through 21 in order
AND return the existing spec_table[21].name pointer, text "spec_patrolman"
AND NEVER inspect index 22, call any procedure, allocate, mutate or emit messages

CASE special.spec_name.null-function
GIVEN the same table and input C NULL
WHEN spec_name is called once
THEN compare input against entries 0 through 21, all unequal
AND stop at the NULL function guard at index 22 without comparing that entry
AND return C NULL with no side effects
```

## Caller and reachability audit

A source-wide symbol search finds one call, [do_mstat](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1700), and one [header declaration](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:2305); no callback/dispatch entry takes `spec_name` itself. There are no scheduled tick or special-procedure invocation routes to this helper.

`do_mstat` rejects an empty argument or failed character lookup before its diagnostic output. At the call site it requires `IS_NPC(victim) && victim->spec_fun != 0`. A PC, or NPC without a procedure, skips this diagnostic. For a registered procedure, it formats `Mobile has special procedure <name>.\n\r` and calls `send_to_char` for the inspecting actor. The helper itself sends nothing; network delivery belongs to the caller/output-layer specification.

[do_stat](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:1038) dispatches `stat mob/char` through `do_function` to `do_mstat`. Its generic route prefers a matching object, then a matching character. The [stat command entry](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:337) requires IM trust (52) and POS_DEAD. Interpreter processing rejects frozen PCs before dispatch and performs trust/position checks. [do_function](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:514) invokes its handler directly, without those authorization gates. There is no separate `mstat` command-table entry. None of these caller guards is an entry requirement for calling `spec_name` directly.

The normal assignment routes support table membership: [load_specials](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1081) resolves via `spec_lookup` and exits on failure; [mobile creation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1539) and [cloning](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:1798) copy the pointer; [do_string](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_wiz.c:3792) resolves through the same table and leaves NULL on lookup failure. Area data chooses among names; it cannot add rows to the compiled table. Testing all 22 rows therefore covers the helper's data-dependent outcomes without requiring an area-file fixture.

**Caller limitation, not an unresolved helper oracle:** a valid but unregistered non-null procedure pointer still passes the `do_mstat` guard. `spec_name` deterministically returns NULL; the caller supplies it to `%s`, which has no portable C result. Do not assert a crash or a particular placeholder string. The unregistered-pointer helper case remains fully specified. No target behavior override or runtime fix is authorized by this report.

## Python adaptation and verification

[Mobile.special_name](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/mobile/Mobile.py:39) already carries the neutral procedure identity; [MobileService](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/mobile/MobileService.py:44) attaches the designer-provided name. A future Python test should assert identity/absence at that metadata or diagnostic boundary, without executing a special procedure or recreating C function pointers. No reverse callable-lookup API or Python parity is claimed.

Verification consists of manual source/caller tracing, all-entry table comparison, snapshot hashes, unique stable IDs, bidirectional path links, exact expected comparison bounds and artifact regeneration. The [validation result](verification.json) records what ran. No dynamic C probe, executable test generation or gameplay execution is claimed. The completion record lives on this function in the manifest; all unrelated partial dispositions are retained.

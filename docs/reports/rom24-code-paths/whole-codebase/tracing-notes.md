# Trace contracts, reference quirks and continuation notes

This is a checkpoint for the requested whole-codebase specification. The inventory covers the files in the local reference `Rom24/src`; the semantic specification is partial. The manifest deliberately leaves functions with cases as `partially_specified`: neither a set of local boundary cases nor a lexical branch index proves that all caller, callee, data and platform paths have been traced.

## Snapshot and configuration

The reference repository HEAD is `d3a29007355e7298e0033fcb666e9a6895c2146f`. The normal Git working-tree commands fail in this execution environment. Reading the Git tree and independently computing Git blob hashes nevertheless found no changed, missing or untracked content in `Rom24`, allowing either raw bytes or CRLF-to-LF checkout conversion. This does not establish staging or file-mode status. The manifest records SHA-256 hashes of the actual files, rather than treating the commit alone as the source snapshot.

The default [Makefile](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/Makefile:1) specifies GCC, `-Wall -O -g` and crypt linkage. Its Linux, normal and Solaris variants are inventoried separately. No C compilation, live server, C oracle probe or Python gameplay test ran for this reporting task. The structural report checks are the only executed validation.

The lexical inventory retains preprocessor alternatives instead of pretending they all execute in one binary. `OLD_RAND` changes the generator in [db.c](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:3023); the random adapter cases script `number_mm` or its wrappers at a boundary and do not prescribe a system `random()` sequence. `macintosh`, `MSDOS`, platform socket declarations and crypt configuration need separate configuration-specific tracing. Block comments containing code-like text have an explicit disabled disposition; this scan can also classify prose containing code as a candidate. It is not a C preprocessor.

ASCII comparison cases assume valid NUL-terminated buffers. `LOWER` in [merc.h](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1799) folds ASCII uppercase only; these expectations do not imply Unicode case folding. `one_argument` uses `isspace` to skip whitespace but an unquoted token ends at a literal space, so an interior tab remains part of the token. Buffer safety and non-ASCII locale behavior still need a separate audit.

## Execution and dispatch contracts

- [interpret](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:367) removes leading whitespace, returns for an empty input, removes `AFF_HIDE`, then checks a player's freeze flag. Command lookup is ordered, prefix-based and restricted by trust. Logging and snooping precede the minimum-position rejection. These observations are navigation notes; full interpreter cases remain pending.
- [do_function](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:514) duplicates the argument, invokes the function pointer and frees the copy. It does not perform interpreter trust, position, freeze, hiding or logging checks. The report's direct-helper cases therefore never imply that an unprivileged player can issue the corresponding command through `interpret`.
- The command table contains `alia`, `alias`, `unalias` and privileged `flag` entries. A search of this snapshot's command table found no `do_scan` entry. [spell_farsight](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/magic2.c:44) calls `do_scan` through `do_function`; direct scan cases describe that helper, not an established ordinary `scan` command route.

## Lookup and scan checkpoint

- The five lookup helpers accept a valid NUL-terminated name. They first compare folded initials and only call `str_prefix` on an initial match. Clan lookup reads exactly the three available rows on a miss and returns zero both for a miss and for its empty-name row. Position, sex and size stop at their null-name sentinels and return minus one on a miss. Flag lookup accepts a caller-supplied sentinel-terminated table, returns zero on a miss and ignores the row's settable bit. The direct helper specifications leave the caller's policy and mutations in the caller's ledger. [Lookup helpers](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/lookup.c:38) · [Static table rows](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/tables.c:39)
- The scan fixture for a null destination describes a malformed graph. An around scan can pass that destination to the null-safe `scan_list`. A directional scan assigns it to the cursor and dereferences it on the next iteration. Loader reachability for that malformed graph is open. [Scan exit traversal](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/scan.c:58)
- `scan_list` filters visibility before dispatching to `scan_char`. The `PERS` macro then checks visibility again and can produce `someone` even after an occupant passed the first filter. A visible NPC supplies its short description and a visible PC supplies its name. [Scan filters and formatting](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/scan.c:101) · [PERS macro](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1858)
- Python scan cases can use the spell context with room and exit fixtures, then inspect `to_char` messages and targeted `to_room` payloads. Record C visibility rechecks and undefined inputs separately from target adaptation. The corresponding Python entry point receives rules and a spell context. [Python scan](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:1443)
- `substitute_alias` is invoked by both platform game-loop alternatives. It reads aliases and prefixes from `descriptor.original` when switched, while interpreting as `descriptor.character`. Case expectations record that distinction.
- Function call lists are lexical candidates. Prototypes, table entries, address-taking and callback symbols are separately labeled; none establishes actual runtime reachability without checking the caller and configuration. Indirect function-pointer call sites remain pending.

## Shared dependency boundaries

Fixtures are neutral descriptions, not serialized C structs. `kind=NPC` requires the NPC marker bit; an `act` list supplies additional or explicitly named bits. IDs express pointer identity. JSON `null` in a pointer-valued fixture field means C NULL; a missing field means the dependency is irrelevant or controlled separately, not zero or an empty string. Tables represented by rows are terminated as described by their fixture contract.

Each case names its controlled collaborators. A recording boundary asserts a call's arguments and ordering; it does not assert that every internal effect of that collaborator was traced. In particular:

| Collaborator | Established local contract | Remaining dependency work |
|---|---|---|
| `str_cmp`, `str_prefix`, `str_suffix`, `str_infix` | False means match; ASCII comparisons; explicitly specified null handling for the first two | Overlong, invalid-buffer and locale/platform inputs |
| `get_trust` | Switched original first; explicit trust next; NPC level at or above 51 caps at 50; otherwise level | All callers' authorization and assumptions |
| `number_range`, `number_percent`, `number_door`, `number_bits`, `number_fuzzy`, `dice` | Rejection sampling, masks, endpoints and ordered calls in the pseudo suite | Generator initialization, platform sequences, invalid widths and overflowing domains |
| `get_char_world`, `get_obj_list`, `get_eq_char`, `get_room_index` | Explicit scripted return or argument recording in these cases | Actual keyword/ordinal/visibility searches and registry behavior |
| `create_object`, `obj_to_room`, `extract_obj` | Spell cases record prototype 25, creation arguments, field assignments, room placement and component extraction order | Prototype contents; equipment/effect reversal, recursive extraction, counts and global lists |
| `act`, `send_to_char`, `wiznet` | Exact literal/template, intended channel, anchor and ordering when specified | Descriptor filtering, visibility expansion, recipients' positions and network delivery |
| `get_skill`, `get_curr_stat`, `check_immune` | Scripted helper results in visibility/save cases | Independent exhaustive helper contracts |
| Healer-selected spell function | Exact function pointer, skill index, level, healer caster and patient target | Each cure's internal effects and failure paths |
| Update callbacks | Invocation indices and ordering from fresh static-counter state | Each callback's world mutation and random consumption |

For direct room visibility and trust cases, the local helper code was inspected. For `can_see` and `can_see_obj`, room darkness and stat/skill helpers are explicit boundaries; the test double must not replace the visibility predicate under test. Message-boundary cases assert an `act` request, which is distinct from asserting successful delivery to every entity in that channel.

All quantities in the suite use C units. One gold equals 100 silver. Scheduler calls are pulses at four pulses per second; `PULSE_VIOLENCE` is 12 pulses. Waits use the maximum of the old and requested wait. Portal timers are object-update countdown units; mapping them to wall time depends on object update behavior, which remains pending. Examples of signed C division truncate toward zero, including negative interpolation products. None authorizes signed overflow.

## Source quirks and portable-oracle gaps

These are source behavior observations, not requests to change the target game. No intentional target overrides were authorized.

1. **Flag mutation ordering:** `do_flag` selects a valid field, snapshots its old bits, then clears `victim.zone` before validating every flag word. An invalid word returns without committing any bit changes, but the zone remains cleared. The advertised `off` field is not accepted by the field-selection chain.
2. **Nonsettable bits:** the `settable=false` branch preserves a bit already set in the old mask. It does not forbid adding a previously absent nonsettable bit. An absent `PLR_HOLYLIGHT` can therefore be added through the helper; removing an already present protected bit is refused by preservation. Duplicate requested flag words collapse into one marked bit, so default toggling happens once per table entry.
3. **Alias protection direction:** `do_alias` checks whether the entire replacement is a prefix of `delete` or `prefix`. Thus `del` is rejected while `delete yes` passes that check. This is the literal checkout behavior, not a safer target validation rule.
4. **Alias length undefined behavior:** `substitute_alias` checks `strlen(prefix)+strlen(argument)>256`, but formatting also writes a separating space and terminating NUL. Some inputs that pass the check overflow the 256-byte local prefix buffer. The corresponding case is blocked; it specifies no accidental stack-corruption result. Replacement strings are also concatenated before truncation, so large source replacements require a broader buffer audit.
5. **Scan around undefined behavior:** current-room scans pass `(depth=0, door=-1)`. `scan_char` evaluates `dir_name[door]` for `sprintf` even when `distance[0]` has no format substitution. Evaluating `dir_name[-1]` is out of bounds. That path has a blocked portable oracle.
6. **Directional scanning:** it follows up to three existing exits without testing `EX_CLOSED`, room visibility or intermediate room privacy in `do_scan`. A formatted directional heading is assigned to `buf` but never sent. If an exit is missing, the loop does not break; it checks the same room's missing exit on remaining iterations. Actual `can_see` filtering is separate and can consume sneak randomness.
7. **Portal/nexus differences:** portal does not reject `ROOM_SAFE` on the origin, while nexus does. Both reject a target at `spell_level+3`, and a PC at hero level uses actual level rather than trust. Immortals bypass the required warp stone, but an immortal holding one still consumes it. Nexus creates only one portal when targeting another character in the same room. Full extraction, prototype and final message-delivery contracts remain pending.
8. **Healer price mismatch:** the serious-wounds menu advertises 15 gold, but its selected branch charges 1,600 silver. Payment, healer credit and incantation happen before the `sn==-1` return, so a missing skill lookup does not cause a refund. The healer is the spell caster; the buyer is the target. This is not equivalent to the buyer casting a spell.
9. **Strict saves:** `number_percent()<save` means a clamped threshold of 5 succeeds for rolls 1–4, and 95 succeeds for 1–94. It does not mean 5% or 95% success with a uniform 1–100 adapter. Mana-class scaling occurs before clamping. `saves_dispel` increases permanent-effect spell level by five before computing the save.
10. **Ban matching:** `BAN_PREFIX` uses a host suffix test and `BAN_SUFFIX` uses a host prefix test. When both flags are set, the first check searches `strstr(ban.name,host)`, with the host as the substring; subsequent one-flag checks can still match. With neither prefix nor suffix set, this function has no exact-match fallback.
11. **Fixed scheduler intervals:** comments describe randomized ticks, but the random interval expressions are commented out. Every group runs on the first call because static counters initialize to zero; subsequent calls use fixed periods. The order is area, music, mobile, violence, point group, aggression, tail chain. The first repeat of violence is call 13, not call 12.
12. **Random room law condition:** the sampler accepts a law room for any NPC, and also for a PC with the `ACT_AGGRESSIVE` bit set. Portal entry later has a separate aggressive-NPC law rejection. There is no retry bound in `get_random_room`; a world without an acceptable candidate has no guaranteed termination.

Review decisions should preserve each defined behavior as the C oracle unless the user explicitly chooses an intentional target change. Undefined behavior should receive a safe, explicit target policy, separately from the reference specification.

## Loaded data and reachability

[boot_db](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:310) opens `AREA_LIST`, reads filenames until a token starts with `$`, supports `-` as standard input and dispatches `AREA`, `HELPS`, `MOBOLD`, `MOBILES`, `OBJOLD`, `OBJECTS`, `RESETS`, `ROOMS`, `SHOPS`, `SOCIALS` and `SPECIALS` sections. Unknown sections and missing files exit the process. It then fixes exits, clears the boot flag, resets areas and loads notes, bans and songs. These loader behaviors have not yet been expanded into complete pseudo cases.

The manifest includes the actual `area/area.lst` order, file existence and section locators, assuming a process CWD of `Rom24/area`. Filenames in `merc.h` are relative to the process CWD; that assumption must be checked against the intended launch procedure. Area section indexing is not proof that resets, shop tables, object prototypes, special-function assignments, portals or social definitions have been behaviorally reviewed. All such data paths remain pending. Files outside `src`, including alternative implementations under `pysrc`, are inventoried and hashed with a pending disposition instead of silently omitted.

## Python consumer mapping

These mappings were checked against the actual Python files, but no implementation parity claim follows from them. No collection JSON was inspected or edited for this report.

| Neutral fixture/event | Candidate Python boundary | Assertion style |
|---|---|---|
| Alias owner, original controller, body and command text | [AliasApi](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/AliasApi.py:18), particularly `substitute_command` | Compare substituted command, message key and stored alias state; separately test active session/controller dispatch |
| Room graph and room occupants | [Room](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/Room.py:1), [Character](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/Character.py:1), [LookupUtil](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/util/LookupUtil.py:6) | Assert entity IDs, ordered room membership, lookup outcome and unchanged observers |
| Spell context, portal creation and scan | [SpellContext](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/skill/SpellContext.py:1), [SpellApi](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/SpellApi.py:1322) | Build minimal world/item fixtures, control helpers and assert queued events plus object ownership/timer/destination |
| Literal C `act` or `send_to_char` intent | [GamePayload](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/GamePayload.py:15), [MessageBus](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/messaging/MessageBus.py:17) | Map message semantics to designer-owned payload keys/channels; assert recipients, ordering and forbidden deliveries using async recording doubles |
| Periodic update event | [UpdateHandler](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/UpdateHandler.py:1) | Test the target scheduler's corresponding boundary without copying C static globals into the design |
| C-only persistence formats, platform socket loops, allocation/free lists and file diagnostics | Unmapped | Specify behavior first, then choose a target boundary appropriate to Python services and prepared persistence snapshots |

Keep expected C outcomes separate from any approved text, feature or scheduling differences. `unittest` fixtures may expose the right entity/API boundary without duplicating C structs or algorithms. The pseudo suite is language-neutral and does not import the Python runtime.

## Continuation and validation

The manifest is the authoritative checkpoint. Every source function has a pending or partially specified disposition, and every lexical control site has a pending disposition until its feasible outcomes are manually linked. Specified semantic paths have their own stable IDs and case links. This is intentionally conservative: unrelated syntax sites are not marked covered simply because a function has a case.

Continue with: complete local-ledger reconciliation for the functions already carrying cases; then interpreter/session/network routes, movement and object ownership, combat, spells/effects, update callbacks, save/load and parsing, special procedures and all loaded data. Resolve platform and indirect-call reachability throughout. The pending workload is not a set of exclusions from the user's request.

`build_report.py` validates JSON fields, unique IDs, bidirectional case links, citation bounds, file/function dispositions and counts. `validate_report.py` independently reparses the final artifacts and checks every snapshot hash, Markdown link and cited line bound. Neither establishes the truth of an expected outcome. Manual checks revisited the source formulas for random rejection boundaries, C division, stealth chance, currency change, spell timers, strict saving thresholds and scheduler call numbers. No generated executable tests or measured branch coverage are part of this delivery.

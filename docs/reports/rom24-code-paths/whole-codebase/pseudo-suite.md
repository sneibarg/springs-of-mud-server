# Language-neutral pseudo suite

Evidence: static source tracing only. These cases have not been executed against C or Python.

## db.str_cmp.empty-equal

empty equal

```text
CASE db.str_cmp.empty-equal
SOURCE src/db.c:str_cmp:3134
GIVEN {"arguments": {"astr": "", "bstr": ""}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_cmp with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_cmp.ascii-case-equal

ascii case equal

```text
CASE db.str_cmp.ascii-case-equal
SOURCE src/db.c:str_cmp:3134
GIVEN {"arguments": {"astr": "ROM", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_cmp with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_cmp.first-mismatch

first mismatch

```text
CASE db.str_cmp.first-mismatch
SOURCE src/db.c:str_cmp:3134
GIVEN {"arguments": {"astr": "cat", "bstr": "bat"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_cmp with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_cmp.left-shorter

left shorter

```text
CASE db.str_cmp.left-shorter
SOURCE src/db.c:str_cmp:3134
GIVEN {"arguments": {"astr": "ca", "bstr": "cat"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_cmp with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_cmp.right-shorter

right shorter

```text
CASE db.str_cmp.right-shorter
SOURCE src/db.c:str_cmp:3134
GIVEN {"arguments": {"astr": "cat", "bstr": "ca"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_cmp with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_prefix.empty-prefix

empty prefix

```text
CASE db.str_prefix.empty-prefix
SOURCE src/db.c:str_prefix:3164
GIVEN {"arguments": {"astr": "", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_prefix.both-empty

both empty

```text
CASE db.str_prefix.both-empty
SOURCE src/db.c:str_prefix:3164
GIVEN {"arguments": {"astr": "", "bstr": ""}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_prefix.ascii-case-prefix

ascii case prefix

```text
CASE db.str_prefix.ascii-case-prefix
SOURCE src/db.c:str_prefix:3164
GIVEN {"arguments": {"astr": "RO", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_prefix.equal

equal

```text
CASE db.str_prefix.equal
SOURCE src/db.c:str_prefix:3164
GIVEN {"arguments": {"astr": "rom", "bstr": "ROM"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_prefix.longer-than-candidate

longer than candidate

```text
CASE db.str_prefix.longer-than-candidate
SOURCE src/db.c:str_prefix:3164
GIVEN {"arguments": {"astr": "roms", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_prefix.first-mismatch

first mismatch

```text
CASE db.str_prefix.first-mismatch
SOURCE src/db.c:str_prefix:3164
GIVEN {"arguments": {"astr": "x", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_infix.empty-needle

empty needle

```text
CASE db.str_infix.empty-needle
SOURCE src/db.c:str_infix:3194
GIVEN {"arguments": {"astr": "", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_infix.longer-needle

longer needle

```text
CASE db.str_infix.longer-needle
SOURCE src/db.c:str_infix:3194
GIVEN {"arguments": {"astr": "roms", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_infix.interior-case-insensitive

interior case insensitive

```text
CASE db.str_infix.interior-case-insensitive
SOURCE src/db.c:str_infix:3194
GIVEN {"arguments": {"astr": "OM", "bstr": "romance"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_infix.end-match

end match

```text
CASE db.str_infix.end-match
SOURCE src/db.c:str_infix:3194
GIVEN {"arguments": {"astr": "ce", "bstr": "romance"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_infix.no-match

no match

```text
CASE db.str_infix.no-match
SOURCE src/db.c:str_infix:3194
GIVEN {"arguments": {"astr": "zz", "bstr": "romance"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_suffix.empty-suffix

empty suffix

```text
CASE db.str_suffix.empty-suffix
SOURCE src/db.c:str_suffix:3223
GIVEN {"arguments": {"astr": "", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_suffix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_suffix.case-suffix

case suffix

```text
CASE db.str_suffix.case-suffix
SOURCE src/db.c:str_suffix:3223
GIVEN {"arguments": {"astr": "OM", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_suffix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_suffix.equal

equal

```text
CASE db.str_suffix.equal
SOURCE src/db.c:str_suffix:3223
GIVEN {"arguments": {"astr": "ROM", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_suffix with the fixture arguments once.
THEN {"return": false, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_suffix.longer

longer

```text
CASE db.str_suffix.longer
SOURCE src/db.c:str_suffix:3223
GIVEN {"arguments": {"astr": "room", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_suffix with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_suffix.wrong-suffix

wrong suffix

```text
CASE db.str_suffix.wrong-suffix
SOURCE src/db.c:str_suffix:3223
GIVEN {"arguments": {"astr": "ro", "bstr": "rom"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke str_suffix with the fixture arguments once.
THEN {"return": true, "unchanged": ["both input strings"], "forbidden": ["messages", "random draws"]}
```

## db.str_cmp.null-left

null left

```text
CASE db.str_cmp.null-left
SOURCE src/db.c:str_cmp:3136
GIVEN {"arguments": {"astr": {"C_NULL": true}, "bstr": "x"}}
AND {"bug": "Recording collaborator; logging internals are outside this helper-boundary case.", "randomness": "none"}
WHEN Invoke str_cmp with the fixture arguments once.
THEN {"return": true, "ordered_events": [{"call": "bug", "arguments": ["Str_cmp: null astr.", 0]}], "forbidden": ["dereference NULL", "second bug call"]}
```

## db.str_cmp.null-right

null right

```text
CASE db.str_cmp.null-right
SOURCE src/db.c:str_cmp:3142
GIVEN {"arguments": {"astr": "x", "bstr": {"C_NULL": true}}}
AND {"bug": "Recording collaborator; logging internals are outside this helper-boundary case.", "randomness": "none"}
WHEN Invoke str_cmp with the fixture arguments once.
THEN {"return": true, "ordered_events": [{"call": "bug", "arguments": ["Str_cmp: null bstr.", 0]}], "forbidden": ["dereference NULL", "second bug call"]}
```

## db.str_cmp.both-null-left-dominates

both null left dominates

```text
CASE db.str_cmp.both-null-left-dominates
SOURCE src/db.c:str_cmp:3136
GIVEN {"arguments": {"astr": {"C_NULL": true}, "bstr": {"C_NULL": true}}}
AND {"bug": "Recording collaborator; logging internals are outside this helper-boundary case.", "randomness": "none"}
WHEN Invoke str_cmp with the fixture arguments once.
THEN {"return": true, "ordered_events": [{"call": "bug", "arguments": ["Str_cmp: null astr.", 0]}], "forbidden": ["dereference NULL", "second bug call"]}
```

## db.str_prefix.null-left

null left

```text
CASE db.str_prefix.null-left
SOURCE src/db.c:str_prefix:3166
GIVEN {"arguments": {"astr": {"C_NULL": true}, "bstr": "x"}}
AND {"bug": "Recording collaborator; logging internals are outside this helper-boundary case.", "randomness": "none"}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": true, "ordered_events": [{"call": "bug", "arguments": ["Strn_cmp: null astr.", 0]}], "forbidden": ["dereference NULL", "second bug call"]}
```

## db.str_prefix.null-right

null right

```text
CASE db.str_prefix.null-right
SOURCE src/db.c:str_prefix:3172
GIVEN {"arguments": {"astr": "x", "bstr": {"C_NULL": true}}}
AND {"bug": "Recording collaborator; logging internals are outside this helper-boundary case.", "randomness": "none"}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": true, "ordered_events": [{"call": "bug", "arguments": ["Strn_cmp: null bstr.", 0]}], "forbidden": ["dereference NULL", "second bug call"]}
```

## db.str_prefix.both-null-left-dominates

both null left dominates

```text
CASE db.str_prefix.both-null-left-dominates
SOURCE src/db.c:str_prefix:3166
GIVEN {"arguments": {"astr": {"C_NULL": true}, "bstr": {"C_NULL": true}}}
AND {"bug": "Recording collaborator; logging internals are outside this helper-boundary case.", "randomness": "none"}
WHEN Invoke str_prefix with the fixture arguments once.
THEN {"return": true, "ordered_events": [{"call": "bug", "arguments": ["Strn_cmp: null astr.", 0]}], "forbidden": ["dereference NULL", "second bug call"]}
```

## db.smash_tilde.empty

empty

```text
CASE db.smash_tilde.empty
SOURCE src/db.c:smash_tilde:3120
GIVEN {"arguments": {"str": ""}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke smash_tilde with the fixture arguments once.
THEN {"return": "void", "resulting_string": "", "forbidden": ["allocation", "messages"]}
```

## db.smash_tilde.no-tilde

no tilde

```text
CASE db.smash_tilde.no-tilde
SOURCE src/db.c:smash_tilde:3120
GIVEN {"arguments": {"str": "abc"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke smash_tilde with the fixture arguments once.
THEN {"return": "void", "resulting_string": "abc", "forbidden": ["allocation", "messages"]}
```

## db.smash_tilde.one

one

```text
CASE db.smash_tilde.one
SOURCE src/db.c:smash_tilde:3120
GIVEN {"arguments": {"str": "a~b"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke smash_tilde with the fixture arguments once.
THEN {"return": "void", "resulting_string": "a-b", "forbidden": ["allocation", "messages"]}
```

## db.smash_tilde.multiple

multiple

```text
CASE db.smash_tilde.multiple
SOURCE src/db.c:smash_tilde:3120
GIVEN {"arguments": {"str": "~~a~"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke smash_tilde with the fixture arguments once.
THEN {"return": "void", "resulting_string": "--a-", "forbidden": ["allocation", "messages"]}
```

## db.capitalize.empty

empty

```text
CASE db.capitalize.empty
SOURCE src/db.c:capitalize:3249
GIVEN {"arguments": {"str": ""}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke capitalize with the fixture arguments once.
THEN {"result_string": "", "unchanged": ["input string"], "storage": "Shared static buffer, not a fresh caller-owned allocation."}
```

## db.capitalize.mixed

mixed

```text
CASE db.capitalize.mixed
SOURCE src/db.c:capitalize:3249
GIVEN {"arguments": {"str": "hELLO ROM"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke capitalize with the fixture arguments once.
THEN {"result_string": "Hello rom", "unchanged": ["input string"], "storage": "Shared static buffer, not a fresh caller-owned allocation."}
```

## db.capitalize.nonletter-first

nonletter first

```text
CASE db.capitalize.nonletter-first
SOURCE src/db.c:capitalize:3249
GIVEN {"arguments": {"str": "1ROM"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke capitalize with the fixture arguments once.
THEN {"result_string": "1rom", "unchanged": ["input string"], "storage": "Shared static buffer, not a fresh caller-owned allocation."}
```

## db.interpolate.zero

zero

```text
CASE db.interpolate.zero
SOURCE src/db.c:interpolate:3107
GIVEN {"arguments": {"level": 0, "value_00": 10, "value_32": 42}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke interpolate with the fixture arguments once.
THEN {"return": 10, "arithmetic": "Signed integer division truncates toward zero; no clamping."}
```

## db.interpolate.endpoint

endpoint

```text
CASE db.interpolate.endpoint
SOURCE src/db.c:interpolate:3107
GIVEN {"arguments": {"level": 32, "value_00": 10, "value_32": 42}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke interpolate with the fixture arguments once.
THEN {"return": 42, "arithmetic": "Signed integer division truncates toward zero; no clamping."}
```

## db.interpolate.positive-fraction

positive fraction

```text
CASE db.interpolate.positive-fraction
SOURCE src/db.c:interpolate:3107
GIVEN {"arguments": {"level": 1, "value_00": 10, "value_32": 11}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke interpolate with the fixture arguments once.
THEN {"return": 10, "arithmetic": "Signed integer division truncates toward zero; no clamping."}
```

## db.interpolate.negative-fraction-truncates-to-zero

negative fraction truncates to zero

```text
CASE db.interpolate.negative-fraction-truncates-to-zero
SOURCE src/db.c:interpolate:3107
GIVEN {"arguments": {"level": 1, "value_00": 10, "value_32": 9}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke interpolate with the fixture arguments once.
THEN {"return": 10, "arithmetic": "Signed integer division truncates toward zero; no clamping."}
```

## db.interpolate.negative-level

negative level

```text
CASE db.interpolate.negative-level
SOURCE src/db.c:interpolate:3107
GIVEN {"arguments": {"level": -1, "value_00": 10, "value_32": 11}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke interpolate with the fixture arguments once.
THEN {"return": 10, "arithmetic": "Signed integer division truncates toward zero; no clamping."}
```

## db.interpolate.extrapolates

extrapolates

```text
CASE db.interpolate.extrapolates
SOURCE src/db.c:interpolate:3107
GIVEN {"arguments": {"level": 64, "value_00": 10, "value_32": 42}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke interpolate with the fixture arguments once.
THEN {"return": 74, "arithmetic": "Signed integer division truncates toward zero; no clamping."}
```

## interp.one_argument.empty

empty

```text
CASE interp.one_argument.empty
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "", "arg_first": "writable output array of at least 256 bytes"}, "locale": "C/ASCII for isspace and LOWER"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "", "returned_remainder": "", "unchanged": ["input bytes"], "forbidden": ["messages", "randomness"]}
```

## interp.one_argument.leading-spaces

leading spaces

```text
CASE interp.one_argument.leading-spaces
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "  LOOK  North", "arg_first": "writable output array of at least 256 bytes"}, "locale": "C/ASCII for isspace and LOWER"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "look", "returned_remainder": "North", "unchanged": ["input bytes"], "forbidden": ["messages", "randomness"]}
```

## interp.one_argument.single-quotes

single quotes

```text
CASE interp.one_argument.single-quotes
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "'Two Words' tail", "arg_first": "writable output array of at least 256 bytes"}, "locale": "C/ASCII for isspace and LOWER"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "two words", "returned_remainder": "tail", "unchanged": ["input bytes"], "forbidden": ["messages", "randomness"]}
```

## interp.one_argument.double-quotes

double quotes

```text
CASE interp.one_argument.double-quotes
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "\"Two Words\" tail", "arg_first": "writable output array of at least 256 bytes"}, "locale": "C/ASCII for isspace and LOWER"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "two words", "returned_remainder": "tail", "unchanged": ["input bytes"], "forbidden": ["messages", "randomness"]}
```

## interp.one_argument.unclosed-quote

unclosed quote

```text
CASE interp.one_argument.unclosed-quote
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "'Two Words", "arg_first": "writable output array of at least 256 bytes"}, "locale": "C/ASCII for isspace and LOWER"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "two words", "returned_remainder": "", "unchanged": ["input bytes"], "forbidden": ["messages", "randomness"]}
```

## interp.one_argument.empty-quoted-token

empty quoted token

```text
CASE interp.one_argument.empty-quoted-token
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "'' tail", "arg_first": "writable output array of at least 256 bytes"}, "locale": "C/ASCII for isspace and LOWER"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "", "returned_remainder": "tail", "unchanged": ["input bytes"], "forbidden": ["messages", "randomness"]}
```

## interp.one_argument.embedded-tab

embedded tab

```text
CASE interp.one_argument.embedded-tab
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "look\tnorth rest", "arg_first": "writable output array of at least 256 bytes"}, "locale": "C/ASCII for isspace and LOWER"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "look\tnorth", "returned_remainder": "rest", "unchanged": ["input bytes"], "forbidden": ["messages", "randomness"]}
```

## interp.one_argument.trailing-whitespace

trailing whitespace

```text
CASE interp.one_argument.trailing-whitespace
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "look \t\n north", "arg_first": "writable output array of at least 256 bytes"}, "locale": "C/ASCII for isspace and LOWER"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "look", "returned_remainder": "north", "unchanged": ["input bytes"], "forbidden": ["messages", "randomness"]}
```

## lookup.position_lookup.standing-full

standing full

```text
CASE lookup.position_lookup.standing-full
SOURCE src/lookup.c:position_lookup:72
GIVEN {"arguments": {"name": "standing"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke position_lookup with the fixture arguments once.
THEN {"return": 8, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.position_lookup.ambiguous-s-first-stunned

ambiguous s first stunned

```text
CASE lookup.position_lookup.ambiguous-s-first-stunned
SOURCE src/lookup.c:position_lookup:72
GIVEN {"arguments": {"name": "s"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke position_lookup with the fixture arguments once.
THEN {"return": 3, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.position_lookup.case-insensitive

case insensitive

```text
CASE lookup.position_lookup.case-insensitive
SOURCE src/lookup.c:position_lookup:72
GIVEN {"arguments": {"name": "SLEEP"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke position_lookup with the fixture arguments once.
THEN {"return": 4, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.position_lookup.empty

empty

```text
CASE lookup.position_lookup.empty
SOURCE src/lookup.c:position_lookup:72
GIVEN {"arguments": {"name": ""}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke position_lookup with the fixture arguments once.
THEN {"return": -1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.position_lookup.missing

missing

```text
CASE lookup.position_lookup.missing
SOURCE src/lookup.c:position_lookup:72
GIVEN {"arguments": {"name": "z"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke position_lookup with the fixture arguments once.
THEN {"return": -1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.position_lookup.longer

longer

```text
CASE lookup.position_lookup.longer
SOURCE src/lookup.c:position_lookup:72
GIVEN {"arguments": {"name": "standings"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke position_lookup with the fixture arguments once.
THEN {"return": -1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.sex_lookup.none

none

```text
CASE lookup.sex_lookup.none
SOURCE src/lookup.c:sex_lookup:86
GIVEN {"arguments": {"name": "n"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke sex_lookup with the fixture arguments once.
THEN {"return": 0, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.sex_lookup.male

male

```text
CASE lookup.sex_lookup.male
SOURCE src/lookup.c:sex_lookup:86
GIVEN {"arguments": {"name": "M"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke sex_lookup with the fixture arguments once.
THEN {"return": 1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.sex_lookup.female

female

```text
CASE lookup.sex_lookup.female
SOURCE src/lookup.c:sex_lookup:86
GIVEN {"arguments": {"name": "fem"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke sex_lookup with the fixture arguments once.
THEN {"return": 2, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.sex_lookup.last-entry

last entry

```text
CASE lookup.sex_lookup.last-entry
SOURCE src/lookup.c:sex_lookup:86
GIVEN {"arguments": {"name": "either"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke sex_lookup with the fixture arguments once.
THEN {"return": 3, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.sex_lookup.empty

empty

```text
CASE lookup.sex_lookup.empty
SOURCE src/lookup.c:sex_lookup:86
GIVEN {"arguments": {"name": ""}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke sex_lookup with the fixture arguments once.
THEN {"return": -1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.sex_lookup.missing

missing

```text
CASE lookup.sex_lookup.missing
SOURCE src/lookup.c:sex_lookup:86
GIVEN {"arguments": {"name": "z"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke sex_lookup with the fixture arguments once.
THEN {"return": -1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.size_lookup.tiny

tiny

```text
CASE lookup.size_lookup.tiny
SOURCE src/lookup.c:size_lookup:100
GIVEN {"arguments": {"name": "t"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": 0, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.size_lookup.small

small

```text
CASE lookup.size_lookup.small
SOURCE src/lookup.c:size_lookup:100
GIVEN {"arguments": {"name": "SM"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": 1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.size_lookup.medium

medium

```text
CASE lookup.size_lookup.medium
SOURCE src/lookup.c:size_lookup:100
GIVEN {"arguments": {"name": "m"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": 2, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.size_lookup.large

large

```text
CASE lookup.size_lookup.large
SOURCE src/lookup.c:size_lookup:100
GIVEN {"arguments": {"name": "l"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": 3, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.size_lookup.huge

huge

```text
CASE lookup.size_lookup.huge
SOURCE src/lookup.c:size_lookup:100
GIVEN {"arguments": {"name": "h"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": 4, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.size_lookup.last-entry

last entry

```text
CASE lookup.size_lookup.last-entry
SOURCE src/lookup.c:size_lookup:100
GIVEN {"arguments": {"name": "g"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": 5, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.size_lookup.empty

empty

```text
CASE lookup.size_lookup.empty
SOURCE src/lookup.c:size_lookup:100
GIVEN {"arguments": {"name": ""}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": -1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.size_lookup.missing

missing

```text
CASE lookup.size_lookup.missing
SOURCE src/lookup.c:size_lookup:100
GIVEN {"arguments": {"name": "z"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": -1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.clan_lookup.loner

loner

```text
CASE lookup.clan_lookup.loner
SOURCE src/lookup.c:clan_lookup:58
GIVEN {"arguments": {"name": "L"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke clan_lookup with the fixture arguments once.
THEN {"return": 1, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.clan_lookup.rom

rom

```text
CASE lookup.clan_lookup.rom
SOURCE src/lookup.c:clan_lookup:58
GIVEN {"arguments": {"name": "ro"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke clan_lookup with the fixture arguments once.
THEN {"return": 2, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.clan_lookup.empty-matches-entry-zero

empty matches entry zero

```text
CASE lookup.clan_lookup.empty-matches-entry-zero
SOURCE src/lookup.c:clan_lookup:58
GIVEN {"arguments": {"name": ""}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke clan_lookup with the fixture arguments once.
THEN {"return": 0, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.clan_lookup.unknown-indistinguishable-from-zero

unknown indistinguishable from zero

```text
CASE lookup.clan_lookup.unknown-indistinguishable-from-zero
SOURCE src/lookup.c:clan_lookup:58
GIVEN {"arguments": {"name": "z"}, "table": "Unmodified src/tables.c for this snapshot."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke clan_lookup with the fixture arguments once.
THEN {"return": 0, "lookup": "ASCII case-insensitive prefix; source table order determines first match.", "forbidden": ["messages", "mutation"]}
```

## lookup.flag_lookup.empty-table

empty table

```text
CASE lookup.flag_lookup.empty-table
SOURCE src/lookup.c:flag_lookup:44
GIVEN {"arguments": {"name": "a", "flag_table": []}, "table_contract": "Each row is [name,bit,settable], followed by a name=C NULL sentinel."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 0, "unchanged": ["table"], "forbidden": ["messages"]}
```

## lookup.flag_lookup.first-of-multiple-prefixes

first of multiple prefixes

```text
CASE lookup.flag_lookup.first-of-multiple-prefixes
SOURCE src/lookup.c:flag_lookup:44
GIVEN {"arguments": {"name": "al", "flag_table": [["alpha", 2, false], ["alpine", 4, true]]}, "table_contract": "Each row is [name,bit,settable], followed by a name=C NULL sentinel."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 2, "unchanged": ["table"], "forbidden": ["messages"]}
```

## lookup.flag_lookup.case-insensitive

case insensitive

```text
CASE lookup.flag_lookup.case-insensitive
SOURCE src/lookup.c:flag_lookup:44
GIVEN {"arguments": {"name": "ALP", "flag_table": [["alpha", 2, false]]}, "table_contract": "Each row is [name,bit,settable], followed by a name=C NULL sentinel."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 2, "unchanged": ["table"], "forbidden": ["messages"]}
```

## lookup.flag_lookup.nonsettable-still-found

nonsettable still found

```text
CASE lookup.flag_lookup.nonsettable-still-found
SOURCE src/lookup.c:flag_lookup:44
GIVEN {"arguments": {"name": "alpha", "flag_table": [["alpha", 2, false]]}, "table_contract": "Each row is [name,bit,settable], followed by a name=C NULL sentinel."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 2, "unchanged": ["table"], "forbidden": ["messages"]}
```

## lookup.flag_lookup.skip-nonmatch

skip nonmatch

```text
CASE lookup.flag_lookup.skip-nonmatch
SOURCE src/lookup.c:flag_lookup:44
GIVEN {"arguments": {"name": "b", "flag_table": [["alpha", 2, true], ["beta", 4, true]]}, "table_contract": "Each row is [name,bit,settable], followed by a name=C NULL sentinel."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 4, "unchanged": ["table"], "forbidden": ["messages"]}
```

## lookup.flag_lookup.unknown

unknown

```text
CASE lookup.flag_lookup.unknown
SOURCE src/lookup.c:flag_lookup:44
GIVEN {"arguments": {"name": "z", "flag_table": [["alpha", 2, true]]}, "table_contract": "Each row is [name,bit,settable], followed by a name=C NULL sentinel."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 0, "unchanged": ["table"], "forbidden": ["messages"]}
```

## lookup.flag_lookup.empty-name-does-not-match-nonempty

empty name does not match nonempty

```text
CASE lookup.flag_lookup.empty-name-does-not-match-nonempty
SOURCE src/lookup.c:flag_lookup:44
GIVEN {"arguments": {"name": "", "flag_table": [["alpha", 2, true]]}, "table_contract": "Each row is [name,bit,settable], followed by a name=C NULL sentinel."}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 0, "unchanged": ["table"], "forbidden": ["messages"]}
```

## db.number_range.both-zero

both zero

```text
CASE db.number_range.both-zero
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": 0, "to": 0}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": []}, "other_random_calls": "forbidden"}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 0, "number_mm_calls": 0, "ordered_consumed_draws": []}
```

## db.number_range.equal

equal

```text
CASE db.number_range.equal
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": 7, "to": 7}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": []}, "other_random_calls": "forbidden"}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 7, "number_mm_calls": 0, "ordered_consumed_draws": []}
```

## db.number_range.reversed

reversed

```text
CASE db.number_range.reversed
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": 9, "to": 4}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": []}, "other_random_calls": "forbidden"}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 9, "number_mm_calls": 0, "ordered_consumed_draws": []}
```

## db.number_range.lower-end

lower end

```text
CASE db.number_range.lower-end
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": 10, "to": 12}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [0]}, "other_random_calls": "forbidden"}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 10, "number_mm_calls": 1, "ordered_consumed_draws": [0]}
```

## db.number_range.upper-end

upper end

```text
CASE db.number_range.upper-end
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": 10, "to": 12}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [2]}, "other_random_calls": "forbidden"}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 12, "number_mm_calls": 1, "ordered_consumed_draws": [2]}
```

## db.number_range.reject-equality-then-accept

reject equality then accept

```text
CASE db.number_range.reject-equality-then-accept
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": 10, "to": 12}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [3, 1]}, "other_random_calls": "forbidden"}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 11, "number_mm_calls": 2, "ordered_consumed_draws": [3, 1]}
```

## db.number_range.multiple-rejections

multiple rejections

```text
CASE db.number_range.multiple-rejections
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": 10, "to": 14}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [7, 5, 4]}, "other_random_calls": "forbidden"}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 14, "number_mm_calls": 3, "ordered_consumed_draws": [7, 5, 4]}
```

## db.number_range.negative-domain

negative domain

```text
CASE db.number_range.negative-domain
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": -2, "to": 0}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [2]}, "other_random_calls": "forbidden"}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 0, "number_mm_calls": 1, "ordered_consumed_draws": [2]}
```

## db.number_percent.lower

lower

```text
CASE db.number_percent.lower
SOURCE src/db.c:number_percent:2983
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [0]}}
WHEN Invoke number_percent with the fixture arguments once.
THEN {"return": 1, "number_mm_calls": 1, "ordered_consumed_draws": [0]}
```

## db.number_percent.upper

upper

```text
CASE db.number_percent.upper
SOURCE src/db.c:number_percent:2983
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [99]}}
WHEN Invoke number_percent with the fixture arguments once.
THEN {"return": 100, "number_mm_calls": 1, "ordered_consumed_draws": [99]}
```

## db.number_percent.reject-100

reject 100

```text
CASE db.number_percent.reject-100
SOURCE src/db.c:number_percent:2983
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [100, 99]}}
WHEN Invoke number_percent with the fixture arguments once.
THEN {"return": 100, "number_mm_calls": 2, "ordered_consumed_draws": [100, 99]}
```

## db.number_percent.reject-127

reject 127

```text
CASE db.number_percent.reject-127
SOURCE src/db.c:number_percent:2983
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [127, 0]}}
WHEN Invoke number_percent with the fixture arguments once.
THEN {"return": 1, "number_mm_calls": 2, "ordered_consumed_draws": [127, 0]}
```

## db.number_percent.mask-before-test

mask before test

```text
CASE db.number_percent.mask-before-test
SOURCE src/db.c:number_percent:2983
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [128]}}
WHEN Invoke number_percent with the fixture arguments once.
THEN {"return": 1, "number_mm_calls": 1, "ordered_consumed_draws": [128]}
```

## db.number_door.lower

lower

```text
CASE db.number_door.lower
SOURCE src/db.c:number_door:2998
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [0]}}
WHEN Invoke number_door with the fixture arguments once.
THEN {"return": 0, "number_mm_calls": 1, "ordered_consumed_draws": [0]}
```

## db.number_door.upper

upper

```text
CASE db.number_door.upper
SOURCE src/db.c:number_door:2998
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [5]}}
WHEN Invoke number_door with the fixture arguments once.
THEN {"return": 5, "number_mm_calls": 1, "ordered_consumed_draws": [5]}
```

## db.number_door.reject-six-seven

reject six seven

```text
CASE db.number_door.reject-six-seven
SOURCE src/db.c:number_door:2998
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [6, 7, 2]}}
WHEN Invoke number_door with the fixture arguments once.
THEN {"return": 2, "number_mm_calls": 3, "ordered_consumed_draws": [6, 7, 2]}
```

## db.number_door.mask-before-test

mask before test

```text
CASE db.number_door.mask-before-test
SOURCE src/db.c:number_door:2998
GIVEN {"arguments": {}}
AND {"number_mm": {"kind": "stubbed entropy boundary", "ordered_returns": [8]}}
WHEN Invoke number_door with the fixture arguments once.
THEN {"return": 0, "number_mm_calls": 1, "ordered_consumed_draws": [8]}
```

## db.number_bits.width-0-raw-255

width 0 raw 255

```text
CASE db.number_bits.width-0-raw-255
SOURCE src/db.c:number_bits:3006
GIVEN {"arguments": {"width": 0}}
AND {"number_mm": {"ordered_returns": [255], "kind": "stubbed entropy boundary"}}
WHEN Invoke number_bits with the fixture arguments once.
THEN {"return": 0, "number_mm_calls": 1}
```

## db.number_bits.width-1-raw-2

width 1 raw 2

```text
CASE db.number_bits.width-1-raw-2
SOURCE src/db.c:number_bits:3006
GIVEN {"arguments": {"width": 1}}
AND {"number_mm": {"ordered_returns": [2], "kind": "stubbed entropy boundary"}}
WHEN Invoke number_bits with the fixture arguments once.
THEN {"return": 0, "number_mm_calls": 1}
```

## db.number_bits.width-2-raw-7

width 2 raw 7

```text
CASE db.number_bits.width-2-raw-7
SOURCE src/db.c:number_bits:3006
GIVEN {"arguments": {"width": 2}}
AND {"number_mm": {"ordered_returns": [7], "kind": "stubbed entropy boundary"}}
WHEN Invoke number_bits with the fixture arguments once.
THEN {"return": 3, "number_mm_calls": 1}
```

## db.number_bits.width-3-raw-5

width 3 raw 5

```text
CASE db.number_bits.width-3-raw-5
SOURCE src/db.c:number_bits:3006
GIVEN {"arguments": {"width": 3}}
AND {"number_mm": {"ordered_returns": [5], "kind": "stubbed entropy boundary"}}
WHEN Invoke number_bits with the fixture arguments once.
THEN {"return": 5, "number_mm_calls": 1}
```

## db.number_fuzzy.number-10-bits-0

number 10 bits 0

```text
CASE db.number_fuzzy.number-10-bits-0
SOURCE src/db.c:number_fuzzy:2940
GIVEN {"arguments": {"number": 10}}
AND {"number_bits": {"kind": "stubbed helper boundary; bit masking separately specified", "ordered_returns": [0]}}
WHEN Invoke number_fuzzy with the fixture arguments once.
THEN {"return": 9, "number_bits_calls": [{"width": 2}]}
```

## db.number_fuzzy.number-10-bits-1

number 10 bits 1

```text
CASE db.number_fuzzy.number-10-bits-1
SOURCE src/db.c:number_fuzzy:2940
GIVEN {"arguments": {"number": 10}}
AND {"number_bits": {"kind": "stubbed helper boundary; bit masking separately specified", "ordered_returns": [1]}}
WHEN Invoke number_fuzzy with the fixture arguments once.
THEN {"return": 10, "number_bits_calls": [{"width": 2}]}
```

## db.number_fuzzy.number-10-bits-2

number 10 bits 2

```text
CASE db.number_fuzzy.number-10-bits-2
SOURCE src/db.c:number_fuzzy:2940
GIVEN {"arguments": {"number": 10}}
AND {"number_bits": {"kind": "stubbed helper boundary; bit masking separately specified", "ordered_returns": [2]}}
WHEN Invoke number_fuzzy with the fixture arguments once.
THEN {"return": 10, "number_bits_calls": [{"width": 2}]}
```

## db.number_fuzzy.number-10-bits-3

number 10 bits 3

```text
CASE db.number_fuzzy.number-10-bits-3
SOURCE src/db.c:number_fuzzy:2940
GIVEN {"arguments": {"number": 10}}
AND {"number_bits": {"kind": "stubbed helper boundary; bit masking separately specified", "ordered_returns": [3]}}
WHEN Invoke number_fuzzy with the fixture arguments once.
THEN {"return": 11, "number_bits_calls": [{"width": 2}]}
```

## db.number_fuzzy.number-1-bits-0

number 1 bits 0

```text
CASE db.number_fuzzy.number-1-bits-0
SOURCE src/db.c:number_fuzzy:2940
GIVEN {"arguments": {"number": 1}}
AND {"number_bits": {"kind": "stubbed helper boundary; bit masking separately specified", "ordered_returns": [0]}}
WHEN Invoke number_fuzzy with the fixture arguments once.
THEN {"return": 1, "number_bits_calls": [{"width": 2}]}
```

## db.number_fuzzy.number-0-bits-3

number 0 bits 3

```text
CASE db.number_fuzzy.number-0-bits-3
SOURCE src/db.c:number_fuzzy:2940
GIVEN {"arguments": {"number": 0}}
AND {"number_bits": {"kind": "stubbed helper boundary; bit masking separately specified", "ordered_returns": [3]}}
WHEN Invoke number_fuzzy with the fixture arguments once.
THEN {"return": 1, "number_bits_calls": [{"width": 2}]}
```

## db.number_fuzzy.number--2-bits-1

number  2 bits 1

```text
CASE db.number_fuzzy.number--2-bits-1
SOURCE src/db.c:number_fuzzy:2940
GIVEN {"arguments": {"number": -2}}
AND {"number_bits": {"kind": "stubbed helper boundary; bit masking separately specified", "ordered_returns": [1]}}
WHEN Invoke number_fuzzy with the fixture arguments once.
THEN {"return": 1, "number_bits_calls": [{"width": 2}]}
```

## db.dice.size-zero

size zero

```text
CASE db.dice.size-zero
SOURCE src/db.c:dice:3088
GIVEN {"arguments": {"number": 5, "size": 0}}
AND {"number_range": {"kind": "stubbed helper boundary; separately specified", "ordered_returns": []}}
WHEN Invoke dice with the fixture arguments once.
THEN {"return": 0, "ordered_number_range_calls": []}
```

## db.dice.size-one

size one

```text
CASE db.dice.size-one
SOURCE src/db.c:dice:3088
GIVEN {"arguments": {"number": 5, "size": 1}}
AND {"number_range": {"kind": "stubbed helper boundary; separately specified", "ordered_returns": []}}
WHEN Invoke dice with the fixture arguments once.
THEN {"return": 5, "ordered_number_range_calls": []}
```

## db.dice.size-one-negative-count-quirk

size one negative count quirk

```text
CASE db.dice.size-one-negative-count-quirk
SOURCE src/db.c:dice:3088
GIVEN {"arguments": {"number": -2, "size": 1}}
AND {"number_range": {"kind": "stubbed helper boundary; separately specified", "ordered_returns": []}}
WHEN Invoke dice with the fixture arguments once.
THEN {"return": -2, "ordered_number_range_calls": []}
```

## db.dice.zero-dice

zero dice

```text
CASE db.dice.zero-dice
SOURCE src/db.c:dice:3088
GIVEN {"arguments": {"number": 0, "size": 6}}
AND {"number_range": {"kind": "stubbed helper boundary; separately specified", "ordered_returns": []}}
WHEN Invoke dice with the fixture arguments once.
THEN {"return": 0, "ordered_number_range_calls": []}
```

## db.dice.negative-count

negative count

```text
CASE db.dice.negative-count
SOURCE src/db.c:dice:3088
GIVEN {"arguments": {"number": -2, "size": 6}}
AND {"number_range": {"kind": "stubbed helper boundary; separately specified", "ordered_returns": []}}
WHEN Invoke dice with the fixture arguments once.
THEN {"return": 0, "ordered_number_range_calls": []}
```

## db.dice.one-die

one die

```text
CASE db.dice.one-die
SOURCE src/db.c:dice:3088
GIVEN {"arguments": {"number": 1, "size": 6}}
AND {"number_range": {"kind": "stubbed helper boundary; separately specified", "ordered_returns": [6]}}
WHEN Invoke dice with the fixture arguments once.
THEN {"return": 6, "ordered_number_range_calls": [{"from": 1, "to": 6, "returns": 6}]}
```

## db.dice.multiple

multiple

```text
CASE db.dice.multiple
SOURCE src/db.c:dice:3088
GIVEN {"arguments": {"number": 3, "size": 6}}
AND {"number_range": {"kind": "stubbed helper boundary; separately specified", "ordered_returns": [1, 6, 3]}}
WHEN Invoke dice with the fixture arguments once.
THEN {"return": 10, "ordered_number_range_calls": [{"from": 1, "to": 6, "returns": 1}, {"from": 1, "to": 6, "returns": 6}, {"from": 1, "to": 6, "returns": 3}]}
```

## handler.get_trust.pc-level

pc level

```text
CASE handler.get_trust.pc-level
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "PC", "level": 30, "trust": 0, "desc": null}, "constants": {"LEVEL_HERO": 51}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 30, "unchanged": ["actor and descriptor"]}
```

## handler.get_trust.explicit-trust

explicit trust

```text
CASE handler.get_trust.explicit-trust
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "PC", "level": 10, "trust": 55, "desc": null}, "constants": {"LEVEL_HERO": 51}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 55, "unchanged": ["actor and descriptor"]}
```

## handler.get_trust.npc-below-hero

npc below hero

```text
CASE handler.get_trust.npc-below-hero
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "NPC", "level": 50, "trust": 0, "desc": null}, "constants": {"LEVEL_HERO": 51}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 50, "unchanged": ["actor and descriptor"]}
```

## handler.get_trust.npc-at-hero-capped

npc at hero capped

```text
CASE handler.get_trust.npc-at-hero-capped
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "NPC", "level": 51, "trust": 0, "desc": null}, "constants": {"LEVEL_HERO": 51}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 50, "unchanged": ["actor and descriptor"]}
```

## handler.get_trust.npc-above-hero-capped

npc above hero capped

```text
CASE handler.get_trust.npc-above-hero-capped
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "NPC", "level": 60, "trust": 0, "desc": null}, "constants": {"LEVEL_HERO": 51}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 50, "unchanged": ["actor and descriptor"]}
```

## handler.get_trust.npc-explicit-trust-before-cap

npc explicit trust before cap

```text
CASE handler.get_trust.npc-explicit-trust-before-cap
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "NPC", "level": 60, "trust": 58, "desc": null}, "constants": {"LEVEL_HERO": 51}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 58, "unchanged": ["actor and descriptor"]}
```

## handler.get_trust.switched-original-controls

switched original controls

```text
CASE handler.get_trust.switched-original-controls
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "NPC", "level": 60, "trust": 58, "desc": {"original": {"kind": "PC", "level": 20, "trust": 0}}}, "constants": {"LEVEL_HERO": 51}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 20, "unchanged": ["actor and descriptor"]}
```

## handler.room_is_dark.positive-light-beats-dark

positive light beats dark

```text
CASE handler.room_is_dark.positive-light-beats-dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2359
GIVEN {"room": {"light": 1, "room_flags": ["ROOM_DARK"], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["room.room_flags", "room.sector_type", "weather_info.sunlight"]}
```

## handler.room_is_dark.zero-light-dark-flag

zero light dark flag

```text
CASE handler.room_is_dark.zero-light-dark-flag
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2362
GIVEN {"room": {"light": 0, "room_flags": ["ROOM_DARK"], "sector_type": "SECT_CITY"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light", "room.room_flags"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["room.sector_type", "weather_info.sunlight"]}
```

## handler.room_is_dark.negative-light-dark-flag

negative light dark flag

```text
CASE handler.room_is_dark.negative-light-dark-flag
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2362
GIVEN {"room": {"light": -1, "room_flags": ["ROOM_DARK"], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light", "room.room_flags"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["room.sector_type", "weather_info.sunlight"]}
```

## handler.room_is_dark.inside-at-night

inside at night

```text
CASE handler.room_is_dark.inside-at-night
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2366
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["weather_info.sunlight"]}
```

## handler.room_is_dark.city-at-night

city at night

```text
CASE handler.room_is_dark.city-at-night
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2366
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_CITY"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["weather_info.sunlight"]}
```

## handler.room_is_dark.field-at-sunset

field at sunset

```text
CASE handler.room_is_dark.field-at-sunset
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.field-at-night

field at night

```text
CASE handler.room_is_dark.field-at-night
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.field-day

field day

```text
CASE handler.room_is_dark.field-day
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.field-sunrise

field sunrise

```text
CASE handler.room_is_dark.field-sunrise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "unchanged": ["room", "weather", "all entities"], "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_private.owned-empty

owned empty

```text
CASE handler.room_is_private.owned-empty
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "Alice", "room_flags": [], "people": []}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": true, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.null-owner-empty

null owner empty

```text
CASE handler.room_is_private.null-owner-empty
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": {"C_NULL": true}, "room_flags": [], "people": []}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": false, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.empty-owner-empty

empty owner empty

```text
CASE handler.room_is_private.empty-owner-empty
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "", "room_flags": [], "people": []}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": false, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.private-one

private one

```text
CASE handler.room_is_private.private-one
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "", "room_flags": ["ROOM_PRIVATE"], "people": [{"id": "p0", "kind": "PC"}]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": false, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.private-two

private two

```text
CASE handler.room_is_private.private-two
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "", "room_flags": ["ROOM_PRIVATE"], "people": [{"id": "p0", "kind": "PC"}, {"id": "p1", "kind": "NPC"}]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": true, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.private-three

private three

```text
CASE handler.room_is_private.private-three
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "", "room_flags": ["ROOM_PRIVATE"], "people": [{"id": "p0", "kind": "PC"}, {"id": "p1", "kind": "NPC"}, {"id": "p2", "kind": "PC"}]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": true, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.solitary-zero

solitary zero

```text
CASE handler.room_is_private.solitary-zero
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "", "room_flags": ["ROOM_SOLITARY"], "people": []}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": false, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.solitary-one

solitary one

```text
CASE handler.room_is_private.solitary-one
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "", "room_flags": ["ROOM_SOLITARY"], "people": [{"id": "p0", "kind": "PC"}]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": true, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.imp-empty

imp empty

```text
CASE handler.room_is_private.imp-empty
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "", "room_flags": ["ROOM_IMP_ONLY"], "people": []}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": true, "unchanged": ["all room occupants and room"]}
```

## handler.room_is_private.public-many

public many

```text
CASE handler.room_is_private.public-many
SOURCE src/handler.c:room_is_private:2393
GIVEN {"room": {"owner": "", "room_flags": [], "people": [{"id": "p0", "kind": "PC"}, {"id": "p1", "kind": "NPC"}, {"id": "p2", "kind": "PC"}]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": false, "unchanged": ["all room occupants and room"]}
```

## handler.is_clan.clan-0

clan 0

```text
CASE handler.is_clan.clan-0
SOURCE src/handler.c:is_clan:330
GIVEN {"actor": {"clan": 0}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke is_clan with the fixture arguments once.
THEN {"return_raw": 0, "truth_value": false}
```

## handler.is_clan.clan-1

clan 1

```text
CASE handler.is_clan.clan-1
SOURCE src/handler.c:is_clan:330
GIVEN {"actor": {"clan": 1}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke is_clan with the fixture arguments once.
THEN {"return_raw": 1, "truth_value": true}
```

## handler.is_clan.clan-2

clan 2

```text
CASE handler.is_clan.clan-2
SOURCE src/handler.c:is_clan:330
GIVEN {"actor": {"clan": 2}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke is_clan with the fixture arguments once.
THEN {"return_raw": 2, "truth_value": true}
```

## handler.is_same_clan.clans-0-0

clans 0 0

```text
CASE handler.is_same_clan.clans-0-0
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"clan": 0, "kind": "PC"}, "victim": {"clan": 0, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.clans-1-1

clans 1 1

```text
CASE handler.is_same_clan.clans-1-1
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"clan": 1, "kind": "PC"}, "victim": {"clan": 1, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.clans-2-2

clans 2 2

```text
CASE handler.is_same_clan.clans-2-2
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"clan": 2, "kind": "PC"}, "victim": {"clan": 2, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": true, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## handler.is_same_clan.clans-2-1

clans 2 1

```text
CASE handler.is_same_clan.clans-2-1
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"clan": 2, "kind": "PC"}, "victim": {"clan": 1, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## flags.do_flag.no-arguments

no arguments

```text
CASE flags.do_flag.no-arguments
SOURCE src/flags.c:do_flag:61
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": ""}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "first_message": {"recipient": "admin", "text": "Syntax:\n\r"}, "unchanged": ["victim flags", "victim zone"], "forbidden": ["world lookup", "flag mutation"], "remaining_messages": ["  flag mob  <name> <field> <flags>\n\r", "  flag char <name> <field> <flags>\n\r", "  mob  flags: act,aff,off,imm,res,vuln,form,part\n\r", "  char flags: plr,comm,aff,imm,res,vuln,\n\r", "  +: add flag, -: remove flag, = set equal to\n\r", "  otherwise flag toggles the flags listed.\n\r"]}
```

## flags.do_flag.missing-target

missing target

```text
CASE flags.do_flag.missing-target
SOURCE src/flags.c:do_flag:61
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "first_message": {"recipient": "admin", "text": "What do you wish to set flags on?\n\r"}, "unchanged": ["victim flags", "victim zone"], "forbidden": ["world lookup", "flag mutation"]}
```

## flags.do_flag.missing-field

missing field

```text
CASE flags.do_flag.missing-field
SOURCE src/flags.c:do_flag:61
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "first_message": {"recipient": "admin", "text": "You need to specify a flag to set.\n\r"}, "unchanged": ["victim flags", "victim zone"], "forbidden": ["world lookup", "flag mutation"]}
```

## flags.do_flag.missing-flags

missing flags

```text
CASE flags.do_flag.missing-flags
SOURCE src/flags.c:do_flag:61
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "first_message": {"recipient": "admin", "text": "Which flags do you wish to change?\n\r"}, "unchanged": ["victim flags", "victim zone"], "forbidden": ["world lookup", "flag mutation"]}
```

## flags.do_flag.missing-world-target

missing world target

```text
CASE flags.do_flag.missing-world-target
SOURCE src/flags.c:do_flag:93
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob missing act sentinel"}
AND {"get_char_world": {"kind": "stubbed world-lookup boundary", "returns": "C NULL"}, "randomness": "none"}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "messages": [{"recipient": "admin", "text": "You can't find them.\n\r"}], "unchanged": ["victim flags", "victim zone"]}
```

## flags.do_flag.act-on-pc

act on pc

```text
CASE flags.do_flag.act-on-pc
SOURCE src/flags.c:do_flag:93
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "PC", "act": [], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act sentinel"}
AND {"get_char_world": {"kind": "stubbed world-lookup boundary", "returns": "bob"}, "randomness": "none"}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "messages": [{"recipient": "admin", "text": "Use plr for PCs.\n\r"}], "unchanged": ["victim flags", "victim zone"]}
```

## flags.do_flag.plr-on-npc

plr on npc

```text
CASE flags.do_flag.plr-on-npc
SOURCE src/flags.c:do_flag:93
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "char bob plr permit"}
AND {"get_char_world": {"kind": "stubbed world-lookup boundary", "returns": "bob"}, "randomness": "none"}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "messages": [{"recipient": "admin", "text": "Use act for NPCs.\n\r"}], "unchanged": ["victim flags", "victim zone"]}
```

## flags.do_flag.form-on-pc

form on pc

```text
CASE flags.do_flag.form-on-pc
SOURCE src/flags.c:do_flag:93
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "PC", "act": [], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "char bob form animal"}
AND {"get_char_world": {"kind": "stubbed world-lookup boundary", "returns": "bob"}, "randomness": "none"}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "messages": [{"recipient": "admin", "text": "Form can't be set on PCs.\n\r"}], "unchanged": ["victim flags", "victim zone"]}
```

## flags.do_flag.parts-on-pc

parts on pc

```text
CASE flags.do_flag.parts-on-pc
SOURCE src/flags.c:do_flag:93
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "PC", "act": [], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "char bob parts head"}
AND {"get_char_world": {"kind": "stubbed world-lookup boundary", "returns": "bob"}, "randomness": "none"}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "messages": [{"recipient": "admin", "text": "Parts can't be set on PCs.\n\r"}], "unchanged": ["victim flags", "victim zone"]}
```

## flags.do_flag.comm-on-npc

comm on npc

```text
CASE flags.do_flag.comm-on-npc
SOURCE src/flags.c:do_flag:93
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob comm quiet"}
AND {"get_char_world": {"kind": "stubbed world-lookup boundary", "returns": "bob"}, "randomness": "none"}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "messages": [{"recipient": "admin", "text": "Comm can't be set on NPCs.\n\r"}], "unchanged": ["victim flags", "victim zone"]}
```

## flags.do_flag.unsupported-off-field

unsupported off field

```text
CASE flags.do_flag.unsupported-off-field
SOURCE src/flags.c:do_flag:93
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob off bash"}
AND {"get_char_world": {"kind": "stubbed world-lookup boundary", "returns": "bob"}, "randomness": "none"}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "messages": [{"recipient": "admin", "text": "That's not an acceptable flag.\n\r"}], "unchanged": ["victim flags", "victim zone"]}
```

## flags.do_flag.unknown-type-silent

unknown type silent

```text
CASE flags.do_flag.unknown-type-silent
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "object bob act sentinel"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SENTINEL"], "bob.zone": "zone-A"}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.invalid-word-clears-zone

invalid word clears zone

```text
CASE flags.do_flag.invalid-word-clears-zone
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act + nosuchflag"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SENTINEL"], "bob.zone": {"C_NULL": true}}, "messages": [{"recipient": "admin", "text": "That flag doesn't exist!\n\r"}], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.valid-then-invalid-atomic-flags

valid then invalid atomic flags

```text
CASE flags.do_flag.valid-then-invalid-atomic-flags
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act + scavenger nosuchflag"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SENTINEL"], "bob.zone": {"C_NULL": true}}, "messages": [{"recipient": "admin", "text": "That flag doesn't exist!\n\r"}], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.add

add

```text
CASE flags.do_flag.add
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act + scavenger"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SENTINEL", "ACT_SCAVENGER"], "bob.zone": {"C_NULL": true}}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.remove

remove

```text
CASE flags.do_flag.remove
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act - sentinel"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC"], "bob.zone": {"C_NULL": true}}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.toggle-present

toggle present

```text
CASE flags.do_flag.toggle-present
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act sentinel"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC"], "bob.zone": {"C_NULL": true}}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.toggle-absent

toggle absent

```text
CASE flags.do_flag.toggle-absent
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act scavenger"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SENTINEL", "ACT_SCAVENGER"], "bob.zone": {"C_NULL": true}}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.equal-preserves-npc

equal preserves npc

```text
CASE flags.do_flag.equal-preserves-npc
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act = scavenger"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SCAVENGER"], "bob.zone": {"C_NULL": true}}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.nonsettable-present-preserved

nonsettable present preserved

```text
CASE flags.do_flag.nonsettable-present-preserved
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act - npc"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SENTINEL"], "bob.zone": {"C_NULL": true}}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.duplicate-toggle-only-once

duplicate toggle only once

```text
CASE flags.do_flag.duplicate-toggle-only-once
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act sentinel sentinel"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC"], "bob.zone": {"C_NULL": true}}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.type-label-does-not-restrict-kind

type label does not restrict kind

```text
CASE flags.do_flag.type-label-does-not-restrict-kind
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "char bob act + scavenger"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SENTINEL", "ACT_SCAVENGER"], "bob.zone": {"C_NULL": true}}, "messages": [], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.operator-alone

operator alone

```text
CASE flags.do_flag.operator-alone
SOURCE src/flags.c:do_flag:56
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_SENTINEL"], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "mob bob act ="}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["ACT_IS_NPC", "ACT_SENTINEL"], "bob.zone": "zone-A"}, "messages": [{"recipient": "admin", "text": "Which flags do you wish to change?\n\r"}], "forbidden": ["messages to bob or bystanders", "changes to other flag fields"]}
```

## flags.do_flag.nonsettable-absent-can-be-added-reference-quirk

nonsettable absent can be added reference quirk

```text
CASE flags.do_flag.nonsettable-absent-can-be-added-reference-quirk
SOURCE src/flags.c:do_flag:217
GIVEN {"actor": {"id": "admin", "kind": "PC"}, "victim": {"id": "bob", "kind": "PC", "act": [], "zone": "zone-A"}, "lookup": "get_char_world returns bob for bob", "flags": "src/tables.c; symbolic A=1 B=2 C=4", "argument": "char bob plr + holylight"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"return": "void", "result": {"bob.act": ["PLR_HOLYLIGHT"], "bob.zone": {"C_NULL": true}}, "messages": [], "quirk": "settable=false only protects a bit already present in old; it does not reject adding an absent bit."}
```

## alias.substitute_alias.exact-first-word

exact first word

```text
CASE alias.substitute_alias.exact-first-word
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "x sword"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "look sword"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.no-recursive-expansion

no recursive expansion

```text
CASE alias.substitute_alias.no-recursive-expansion
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": [["x", "xx"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "x"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "xx "}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.prefix-not-exact-alias

prefix not exact alias

```text
CASE alias.substitute_alias.prefix-not-exact-alias
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "xyz sword"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "xyz sword"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.input-lowercases-first-word-only

input lowercases first word only

```text
CASE alias.substitute_alias.input-lowercases-first-word-only
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "X Sword"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "look Sword"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.protected-alias-command

protected alias command

```text
CASE alias.substitute_alias.protected-alias-command
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "alias x look"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "alias x look"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.protected-una-prefix

protected una prefix

```text
CASE alias.substitute_alias.protected-una-prefix
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "unacceptable x"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "unacceptable x"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.prefix-precedes-alias

prefix precedes alias

```text
CASE alias.substitute_alias.prefix-precedes-alias
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "x", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "sword"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "look sword"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.prefix-command-bypasses-prefix

prefix command bypasses prefix

```text
CASE alias.substitute_alias.prefix-command-bypasses-prefix
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "x", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "prefix abc"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "prefix abc"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.no-aliases

no aliases

```text
CASE alias.substitute_alias.no-aliases
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": []}, "body": {"id": "body", "kind": "NPC"}, "argument": "x"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "x"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.original-npc-bypasses-alias

original npc bypasses alias

```text
CASE alias.substitute_alias.original-npc-bypasses-alias
SOURCE src/alias.c:substitute_alias:46
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "NPC", "prefix": "", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "x"}
AND {"interpret": "Recording boundary only; gameplay side effects of interpreted command specified separately.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "x"}], "unchanged": ["alias definitions", "prefix", "owner/body gameplay state at this boundary"], "forbidden": ["recursive substitute_alias call"]}
```

## alias.substitute_alias.replacement-truncates-at-255

replacement truncates at 255

```text
CASE alias.substitute_alias.replacement-truncates-at-255
SOURCE src/alias.c:substitute_alias:85
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": [["x", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "x bc"}
AND {"interpret": "Recording collaborator; do not dispatch gameplay.", "randomness": "none"}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "send_to_char", "recipient": "owner", "text": "Alias substitution too long. Truncated.\r\n"}, {"call": "interpret", "actor": "body", "argument": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "}], "result_length": 255}
```

## alias.substitute_alias.prefix-overflow-boundary-undefined

prefix overflow boundary undefined

```text
CASE alias.substitute_alias.prefix-overflow-boundary-undefined
SOURCE src/alias.c:substitute_alias:51
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "aliases": [["x", "look"], ["xx", "north"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "x"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"portable_oracle": "Unavailable: strlen(prefix)+strlen(argument)==256 passes the >256 guard, but sprintf writes 258 bytes into prefix[256]."}
```

Open questions: Undefined stack write. Choose a target validation policy separately; do not reproduce an accidental C outcome.

## alias.do_alia.requires-full-name

requires full name

```text
CASE alias.do_alia.requires-full-name
SOURCE src/alias.c:do_alia:100
GIVEN {"actor": {"id": "ch"}, "argument": ""}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alia with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "I'm sorry, alias must be entered in full.\n\r"}], "return": "void"}
```

## alias.do_alias.no-aliases

no aliases

```text
CASE alias.do_alias.no-aliases
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": ""}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [], "messages": [{"recipient": "ch", "text": "You have no aliases defined.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.reserved-alias

reserved alias

```text
CASE alias.do_alias.reserved-alias
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": "alias look"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [], "messages": [{"recipient": "ch", "text": "Sorry, that word is reserved.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.reserved-una-prefix

reserved una prefix

```text
CASE alias.do_alias.reserved-una-prefix
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": "unacceptable look"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [], "messages": [{"recipient": "ch", "text": "Sorry, that word is reserved.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.undefined-query

undefined query

```text
CASE alias.do_alias.undefined-query
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": "x"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [], "messages": [{"recipient": "ch", "text": "That alias is not defined.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.defined-query

defined query

```text
CASE alias.do_alias.defined-query
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["x", "look"]]}, "argument": "x"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [["x", "look"]], "messages": [{"recipient": "ch", "text": "x aliases to 'look'.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.add

add

```text
CASE alias.do_alias.add
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": "x look"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [["x", "look"]], "messages": [{"recipient": "ch", "text": "x is now aliased to 'look'.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.redefine

redefine

```text
CASE alias.do_alias.redefine
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["x", "look"]]}, "argument": "x north"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [["x", "north"]], "messages": [{"recipient": "ch", "text": "x is now realiased to 'north'.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.delete-abbreviation-rejected

delete abbreviation rejected

```text
CASE alias.do_alias.delete-abbreviation-rejected
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": "x del"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [], "messages": [{"recipient": "ch", "text": "That shall not be done!\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.prefix-abbreviation-rejected

prefix abbreviation rejected

```text
CASE alias.do_alias.prefix-abbreviation-rejected
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": "x pre"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [], "messages": [{"recipient": "ch", "text": "That shall not be done!\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.full-delete-plus-argument-allowed-quirk

full delete plus argument allowed quirk

```text
CASE alias.do_alias.full-delete-plus-argument-allowed-quirk
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": "x delete yes"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [["x", "delete yes"]], "messages": [{"recipient": "ch", "text": "x is now aliased to 'delete yes'.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.tilde-sanitized

tilde sanitized

```text
CASE alias.do_alias.tilde-sanitized
SOURCE src/alias.c:do_alias:110
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": []}, "argument": "x look~"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": [["x", "look-"]], "messages": [{"recipient": "ch", "text": "x is now aliased to 'look-'.\n\r"}], "return": "void", "forbidden": ["interpret command", "messages to bystanders"]}
```

## alias.do_alias.at-five-alias-limit

at five alias limit

```text
CASE alias.do_alias.at-five-alias-limit
SOURCE src/alias.c:do_alias:194
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["a", "look"], ["b", "look"], ["c", "look"], ["d", "look"], ["e", "look"]]}, "argument": "f north"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Sorry, you have reached the alias limit.\n\r"}], "unchanged": ["all five aliases"], "forbidden": ["sixth alias"]}
```

## alias.do_unalias.missing-name

missing name

```text
CASE alias.do_unalias.missing-name
SOURCE src/alias.c:do_unalias:223
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["a", "look"]]}, "argument": ""}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Unalias what?\n\r"}], "result_aliases": [["a", "look"]], "tail_slots": "C NULL after last occupied slot", "forbidden": ["interpret command"]}
```

## alias.do_unalias.not-found

not found

```text
CASE alias.do_unalias.not-found
SOURCE src/alias.c:do_unalias:223
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["a", "look"]]}, "argument": "z"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "No alias of that name to remove.\n\r"}], "result_aliases": [["a", "look"]], "tail_slots": "C NULL after last occupied slot", "forbidden": ["interpret command"]}
```

## alias.do_unalias.remove-only

remove only

```text
CASE alias.do_unalias.remove-only
SOURCE src/alias.c:do_unalias:223
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["a", "look"]]}, "argument": "a"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Alias removed.\n\r"}], "result_aliases": [], "tail_slots": "C NULL after last occupied slot", "forbidden": ["interpret command"]}
```

## alias.do_unalias.remove-first-shifts-all

remove first shifts all

```text
CASE alias.do_unalias.remove-first-shifts-all
SOURCE src/alias.c:do_unalias:223
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["a", "look"], ["b", "north"], ["c", "south"]]}, "argument": "a"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Alias removed.\n\r"}], "result_aliases": [["b", "north"], ["c", "south"]], "tail_slots": "C NULL after last occupied slot", "forbidden": ["interpret command"]}
```

## alias.do_unalias.remove-middle-shifts-tail

remove middle shifts tail

```text
CASE alias.do_unalias.remove-middle-shifts-tail
SOURCE src/alias.c:do_unalias:223
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["a", "look"], ["b", "north"], ["c", "south"]]}, "argument": "b"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Alias removed.\n\r"}], "result_aliases": [["a", "look"], ["c", "south"]], "tail_slots": "C NULL after last occupied slot", "forbidden": ["interpret command"]}
```

## alias.do_unalias.remove-last

remove last

```text
CASE alias.do_unalias.remove-last
SOURCE src/alias.c:do_unalias:223
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["a", "look"], ["c", "south"]]}, "argument": "c"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Alias removed.\n\r"}], "result_aliases": [["a", "look"]], "tail_slots": "C NULL after last occupied slot", "forbidden": ["interpret command"]}
```

## alias.substitute_alias.active-owner-prefix-over-limit

active owner prefix over limit

```text
CASE alias.substitute_alias.active-owner-prefix-over-limit
SOURCE src/alias.c:substitute_alias:52
GIVEN {"descriptor": {"character": "ch", "original": null}, "actor": {"id": "ch", "kind": "PC", "prefix": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "aliases": []}, "argument": "go"}
AND {"interpret": "Record dispatch without executing gameplay."}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "send_to_char", "recipient": "ch", "text": "Line to long, prefix not processed.\r\n"}, {"call": "interpret", "actor": "ch", "argument": "go"}]}
```

## alias.substitute_alias.five-nonmatching-slots

five nonmatching slots

```text
CASE alias.substitute_alias.five-nonmatching-slots
SOURCE src/alias.c:substitute_alias:70
GIVEN {"descriptor": {"character": "body", "original": "owner"}, "owner": {"id": "owner", "kind": "PC", "prefix": "", "aliases": [["a", "look"], ["b", "look"], ["c", "look"], ["d", "look"], ["e", "look"]]}, "body": {"id": "body", "kind": "NPC"}, "argument": "z"}
AND {"interpret": "Record dispatch without executing gameplay."}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"ordered_events": [{"call": "interpret", "actor": "body", "argument": "z"}], "forbidden": ["one_argument", "message", "alias mutation"]}
```

## alias.do_alias.npc-without-original-returns

npc without original returns

```text
CASE alias.do_alias.npc-without-original-returns
SOURCE src/alias.c:do_alias:117
GIVEN {"actor": {"id": "ch", "kind": "NPC", "desc": {"original": null}, "pcdata": null}, "argument": "x look"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"messages": [], "forbidden": ["alias slot access", "one_argument"], "unchanged": ["alias state"]}
```

## alias.do_unalias.npc-without-original-returns

npc without original returns

```text
CASE alias.do_unalias.npc-without-original-returns
SOURCE src/alias.c:do_unalias:220
GIVEN {"actor": {"id": "ch", "kind": "NPC", "desc": {"original": null}, "pcdata": null}, "argument": "x look"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"messages": [], "forbidden": ["alias slot access", "one_argument"], "unchanged": ["alias state"]}
```

## alias.do_alias.list-two

list two

```text
CASE alias.do_alias.list-two
SOURCE src/alias.c:do_alias:131
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["x", "look"], ["y", "north"]]}, "argument": ""}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Your current aliases are:\n\r"}, {"recipient": "ch", "text": "    x:  look\n\r"}, {"recipient": "ch", "text": "    y:  north\n\r"}], "unchanged": ["alias slots"]}
```

## alias.do_alias.list-stops-at-null-replacement

list stops at null replacement

```text
CASE alias.do_alias.list-stops-at-null-replacement
SOURCE src/alias.c:do_alias:131
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["x", "look"], ["y", null], ["z", "south"]]}, "argument": ""}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Your current aliases are:\n\r"}, {"recipient": "ch", "text": "    x:  look\n\r"}], "unchanged": ["alias slots"]}
```

## alias.do_alias.list-five

list five

```text
CASE alias.do_alias.list-five
SOURCE src/alias.c:do_alias:131
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["a", "look"], ["b", "look"], ["c", "look"], ["d", "look"], ["e", "look"]]}, "argument": ""}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Your current aliases are:\n\r"}, {"recipient": "ch", "text": "    a:  look\n\r"}, {"recipient": "ch", "text": "    b:  look\n\r"}, {"recipient": "ch", "text": "    c:  look\n\r"}, {"recipient": "ch", "text": "    d:  look\n\r"}, {"recipient": "ch", "text": "    e:  look\n\r"}], "unchanged": ["alias slots"]}
```

## alias.do_alias.switched-owner-edited-active-body-notified

switched owner edited active body notified

```text
CASE alias.do_alias.switched-owner-edited-active-body-notified
SOURCE src/alias.c:do_alias:115
GIVEN {"actor": {"id": "body", "kind": "NPC", "desc": {"original": "owner"}}, "owner": {"id": "owner", "kind": "PC", "aliases": [["x", "look"]]}, "argument": "X north"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"result_aliases": {"owner": [["x", "north"]]}, "messages": [{"recipient": "body", "text": "x is now realiased to 'north'.\n\r"}], "forbidden": ["mutate body aliases", "send to owner"]}
```

## alias.do_alias.query-stops-at-null-replacement

query stops at null replacement

```text
CASE alias.do_alias.query-stops-at-null-replacement
SOURCE src/alias.c:do_alias:169
GIVEN {"actor": {"id": "ch", "kind": "PC", "desc": null, "aliases": [["x", null], ["y", "look"]]}, "argument": "y"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "That alias is not defined.\n\r"}], "unchanged": ["alias slots"]}
```

## alias.do_unalias.switched-owner-first-of-duplicate-names

switched owner first of duplicate names

```text
CASE alias.do_unalias.switched-owner-first-of-duplicate-names
SOURCE src/alias.c:do_unalias:236
GIVEN {"actor": {"id": "body", "kind": "NPC", "desc": {"original": "owner"}}, "owner": {"id": "owner", "kind": "PC", "aliases": [["x", "look"], ["x", "north"], ["y", "south"]]}, "argument": "X ignored"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"result_aliases": {"owner": [["x", "north"], ["y", "south"]]}, "messages": [{"recipient": "body", "text": "Alias removed.\n\r"}], "forbidden": ["second deletion", "send to owner"]}
```

## scan.do_scan.invalid-direction

invalid direction

```text
CASE scan.do_scan.invalid-direction
SOURCE src/scan.c:do_scan:77
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "northeast"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Which way do you want to scan?\n\r"}], "forbidden": ["scan_list", "room messages", "movement"]}
```

## scan.do_scan.around-includes-current-and-each-exit

around includes current and each exit

```text
CASE scan.do_scan.around-includes-current-and-each-exit
SOURCE src/scan.c:do_scan:58
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "", "rooms": {"A": {"exit": {"north": {"to_room": "B", "flags": ["EX_CLOSED"]}, "east": {"to_room": "B", "flags": []}}}}}
AND {"scan_list": "Recording helper boundary; separate cases trace occupant filtering.", "randomness": "none"}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "$n looks all around.", "channel": "TO_ROOM"}, {"send_to_char": "Looking around you see:\n\r", "recipient": "ch"}, {"scan_list": ["A", "ch", 0, -1]}, {"scan_list": ["B", "ch", 1, 0]}, {"scan_list": ["B", "ch", 1, 1]}], "forbidden": ["exit closed check", "deduplication of same destination", "movement"]}
```

## scan.do_scan.north-short

north short

```text
CASE scan.do_scan.north-short
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "n", "rooms": {"A": {"selected_exit": "B"}, "B": {"selected_exit": "C"}, "C": {"selected_exit": "D"}, "D": {"selected_exit": "E"}}}
AND {"scan_list": "Recording helper boundary; occupant filtering specified separately.", "randomness": "none"}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM"}, {"scan_list": ["B", "ch", 1, 0]}, {"scan_list": ["C", "ch", 2, 0]}, {"scan_list": ["D", "ch", 3, 0]}], "forbidden": ["scan fourth room E", "send formatted Looking direction header; it is only sprintf into buf", "movement"]}
```

## scan.do_scan.north-long

north long

```text
CASE scan.do_scan.north-long
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "north", "rooms": {"A": {"selected_exit": "B"}, "B": {"selected_exit": "C"}, "C": {"selected_exit": "D"}, "D": {"selected_exit": "E"}}}
AND {"scan_list": "Recording helper boundary; occupant filtering specified separately.", "randomness": "none"}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM"}, {"scan_list": ["B", "ch", 1, 0]}, {"scan_list": ["C", "ch", 2, 0]}, {"scan_list": ["D", "ch", 3, 0]}], "forbidden": ["scan fourth room E", "send formatted Looking direction header; it is only sprintf into buf", "movement"]}
```

## scan.do_scan.east-short

east short

```text
CASE scan.do_scan.east-short
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "e", "rooms": {"A": {"selected_exit": "B"}, "B": {"selected_exit": "C"}, "C": {"selected_exit": "D"}, "D": {"selected_exit": "E"}}}
AND {"scan_list": "Recording helper boundary; occupant filtering specified separately.", "randomness": "none"}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM"}, {"scan_list": ["B", "ch", 1, 1]}, {"scan_list": ["C", "ch", 2, 1]}, {"scan_list": ["D", "ch", 3, 1]}], "forbidden": ["scan fourth room E", "send formatted Looking direction header; it is only sprintf into buf", "movement"]}
```

## scan.do_scan.south-short

south short

```text
CASE scan.do_scan.south-short
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "s", "rooms": {"A": {"selected_exit": "B"}, "B": {"selected_exit": "C"}, "C": {"selected_exit": "D"}, "D": {"selected_exit": "E"}}}
AND {"scan_list": "Recording helper boundary; occupant filtering specified separately.", "randomness": "none"}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM"}, {"scan_list": ["B", "ch", 1, 2]}, {"scan_list": ["C", "ch", 2, 2]}, {"scan_list": ["D", "ch", 3, 2]}], "forbidden": ["scan fourth room E", "send formatted Looking direction header; it is only sprintf into buf", "movement"]}
```

## scan.do_scan.west-short

west short

```text
CASE scan.do_scan.west-short
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "w", "rooms": {"A": {"selected_exit": "B"}, "B": {"selected_exit": "C"}, "C": {"selected_exit": "D"}, "D": {"selected_exit": "E"}}}
AND {"scan_list": "Recording helper boundary; occupant filtering specified separately.", "randomness": "none"}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM"}, {"scan_list": ["B", "ch", 1, 3]}, {"scan_list": ["C", "ch", 2, 3]}, {"scan_list": ["D", "ch", 3, 3]}], "forbidden": ["scan fourth room E", "send formatted Looking direction header; it is only sprintf into buf", "movement"]}
```

## scan.do_scan.up-short

up short

```text
CASE scan.do_scan.up-short
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "u", "rooms": {"A": {"selected_exit": "B"}, "B": {"selected_exit": "C"}, "C": {"selected_exit": "D"}, "D": {"selected_exit": "E"}}}
AND {"scan_list": "Recording helper boundary; occupant filtering specified separately.", "randomness": "none"}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM"}, {"scan_list": ["B", "ch", 1, 4]}, {"scan_list": ["C", "ch", 2, 4]}, {"scan_list": ["D", "ch", 3, 4]}], "forbidden": ["scan fourth room E", "send formatted Looking direction header; it is only sprintf into buf", "movement"]}
```

## scan.do_scan.down-short

down short

```text
CASE scan.do_scan.down-short
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "d", "rooms": {"A": {"selected_exit": "B"}, "B": {"selected_exit": "C"}, "C": {"selected_exit": "D"}, "D": {"selected_exit": "E"}}}
AND {"scan_list": "Recording helper boundary; occupant filtering specified separately.", "randomness": "none"}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM"}, {"scan_list": ["B", "ch", 1, 5]}, {"scan_list": ["C", "ch", 2, 5]}, {"scan_list": ["D", "ch", 3, 5]}], "forbidden": ["scan fourth room E", "send formatted Looking direction header; it is only sprintf into buf", "movement"]}
```

## scan.scan_list.null-room

null room

```text
CASE scan.scan_list.null-room
SOURCE src/scan.c:scan_list:101
GIVEN {"arguments": {"scan_room": {"C_NULL": true}, "ch": "ch", "depth": 1, "door": 0}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke scan_list with the fixture arguments once.
THEN {"return": "void", "forbidden": ["can_see", "scan_char", "get_trust", "messages"]}
```

## scan.scan_list.empty

empty

```text
CASE scan.scan_list.empty
SOURCE src/scan.c:scan_list:104
GIVEN {"actor": {"id": "ch"}, "scan_room": {"people_in_list_order": []}, "arguments": {"depth": 2, "door": 0}}
AND {"get_trust": {"kind": "stubbed helper; get_trust independently specified", "returns": 10}, "can_see": {"kind": "stubbed visibility boundary; internal random draws belong to can_see cases", "returns_by_victim": {}}, "scan_char": "Recording helper boundary; formatting contract separate."}
WHEN Invoke scan_list with the fixture arguments once.
THEN {"scan_char_calls_in_order": [], "can_see_calls": [], "unchanged": ["room list and all entities"]}
```

## scan.scan_list.self-skipped

self skipped

```text
CASE scan.scan_list.self-skipped
SOURCE src/scan.c:scan_list:104
GIVEN {"actor": {"id": "ch"}, "scan_room": {"people_in_list_order": [{"id": "ch", "kind": "PC", "invis_level": 0}]}, "arguments": {"depth": 2, "door": 0}}
AND {"get_trust": {"kind": "stubbed helper; get_trust independently specified", "returns": 10}, "can_see": {"kind": "stubbed visibility boundary; internal random draws belong to can_see cases", "returns_by_victim": {}}, "scan_char": "Recording helper boundary; formatting contract separate."}
WHEN Invoke scan_list with the fixture arguments once.
THEN {"scan_char_calls_in_order": [], "can_see_calls": [], "unchanged": ["room list and all entities"]}
```

## scan.scan_list.pc-invis-too-high

pc invis too high

```text
CASE scan.scan_list.pc-invis-too-high
SOURCE src/scan.c:scan_list:104
GIVEN {"actor": {"id": "ch"}, "scan_room": {"people_in_list_order": [{"id": "v", "kind": "PC", "invis_level": 11}]}, "arguments": {"depth": 2, "door": 0}}
AND {"get_trust": {"kind": "stubbed helper; get_trust independently specified", "returns": 10}, "can_see": {"kind": "stubbed visibility boundary; internal random draws belong to can_see cases", "returns_by_victim": {}}, "scan_char": "Recording helper boundary; formatting contract separate."}
WHEN Invoke scan_list with the fixture arguments once.
THEN {"scan_char_calls_in_order": [], "can_see_calls": [], "unchanged": ["room list and all entities"]}
```

## scan.scan_list.pc-invis-equality-visible

pc invis equality visible

```text
CASE scan.scan_list.pc-invis-equality-visible
SOURCE src/scan.c:scan_list:104
GIVEN {"actor": {"id": "ch"}, "scan_room": {"people_in_list_order": [{"id": "v", "kind": "PC", "invis_level": 10}]}, "arguments": {"depth": 2, "door": 0}}
AND {"get_trust": {"kind": "stubbed helper; get_trust independently specified", "returns": 10}, "can_see": {"kind": "stubbed visibility boundary; internal random draws belong to can_see cases", "returns_by_victim": {"v": true}}, "scan_char": "Recording helper boundary; formatting contract separate."}
WHEN Invoke scan_list with the fixture arguments once.
THEN {"scan_char_calls_in_order": [{"victim": "v", "ch": "ch", "depth": 2, "door": 0}], "can_see_calls": ["v"], "unchanged": ["room list and all entities"]}
```

## scan.scan_list.npc-bypasses-pre-filter

npc bypasses pre filter

```text
CASE scan.scan_list.npc-bypasses-pre-filter
SOURCE src/scan.c:scan_list:104
GIVEN {"actor": {"id": "ch"}, "scan_room": {"people_in_list_order": [{"id": "v", "kind": "NPC", "invis_level": 99}]}, "arguments": {"depth": 2, "door": 0}}
AND {"get_trust": {"kind": "stubbed helper; get_trust independently specified", "returns": 10}, "can_see": {"kind": "stubbed visibility boundary; internal random draws belong to can_see cases", "returns_by_victim": {"v": true}}, "scan_char": "Recording helper boundary; formatting contract separate."}
WHEN Invoke scan_list with the fixture arguments once.
THEN {"scan_char_calls_in_order": [{"victim": "v", "ch": "ch", "depth": 2, "door": 0}], "can_see_calls": ["v"], "unchanged": ["room list and all entities"]}
```

## scan.scan_list.can-see-false

can see false

```text
CASE scan.scan_list.can-see-false
SOURCE src/scan.c:scan_list:104
GIVEN {"actor": {"id": "ch"}, "scan_room": {"people_in_list_order": [{"id": "v", "kind": "PC", "invis_level": 0}]}, "arguments": {"depth": 2, "door": 0}}
AND {"get_trust": {"kind": "stubbed helper; get_trust independently specified", "returns": 10}, "can_see": {"kind": "stubbed visibility boundary; internal random draws belong to can_see cases", "returns_by_victim": {"v": false}}, "scan_char": "Recording helper boundary; formatting contract separate."}
WHEN Invoke scan_list with the fixture arguments once.
THEN {"scan_char_calls_in_order": [], "can_see_calls": ["v"], "unchanged": ["room list and all entities"]}
```

## scan.scan_list.multiple-in-list-order

multiple in list order

```text
CASE scan.scan_list.multiple-in-list-order
SOURCE src/scan.c:scan_list:104
GIVEN {"actor": {"id": "ch"}, "scan_room": {"people_in_list_order": [{"id": "a", "kind": "PC", "invis_level": 0}, {"id": "b", "kind": "NPC", "invis_level": 0}]}, "arguments": {"depth": 2, "door": 0}}
AND {"get_trust": {"kind": "stubbed helper; get_trust independently specified", "returns": 10}, "can_see": {"kind": "stubbed visibility boundary; internal random draws belong to can_see cases", "returns_by_victim": {"a": true, "b": true}}, "scan_char": "Recording helper boundary; formatting contract separate."}
WHEN Invoke scan_list with the fixture arguments once.
THEN {"scan_char_calls_in_order": [{"victim": "a", "ch": "ch", "depth": 2, "door": 0}, {"victim": "b", "ch": "ch", "depth": 2, "door": 0}], "can_see_calls": ["a", "b"], "unchanged": ["room list and all entities"]}
```

## scan.scan_char.depth-1

depth 1

```text
CASE scan.scan_char.depth-1
SOURCE src/scan.c:scan_char:121
GIVEN {"victim": {"id": "v"}, "actor": {"id": "ch"}, "arguments": {"depth": 1, "door": 0}}
AND {"PERS": "Formatting boundary returns A guard; visibility/name helpers not bypassed in their own cases.", "dir_name[0]": "north", "randomness": "none"}
WHEN Invoke scan_char with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "A guard, nearby to the north.\n\r"}], "forbidden": ["messages to victim or observers", "movement"]}
```

## scan.scan_char.depth-2

depth 2

```text
CASE scan.scan_char.depth-2
SOURCE src/scan.c:scan_char:121
GIVEN {"victim": {"id": "v"}, "actor": {"id": "ch"}, "arguments": {"depth": 2, "door": 0}}
AND {"PERS": "Formatting boundary returns A guard; visibility/name helpers not bypassed in their own cases.", "dir_name[0]": "north", "randomness": "none"}
WHEN Invoke scan_char with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "A guard, not far north.\n\r"}], "forbidden": ["messages to victim or observers", "movement"]}
```

## scan.scan_char.depth-3

depth 3

```text
CASE scan.scan_char.depth-3
SOURCE src/scan.c:scan_char:121
GIVEN {"victim": {"id": "v"}, "actor": {"id": "ch"}, "arguments": {"depth": 3, "door": 0}}
AND {"PERS": "Formatting boundary returns A guard; visibility/name helpers not bypassed in their own cases.", "dir_name[0]": "north", "randomness": "none"}
WHEN Invoke scan_char with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "A guard, off in the distance north.\n\r"}], "forbidden": ["messages to victim or observers", "movement"]}
```

## scan.scan_char.around-depth-zero-negative-door-undefined

around depth zero negative door undefined

```text
CASE scan.scan_char.around-depth-zero-negative-door-undefined
SOURCE src/scan.c:scan_char:121
GIVEN {"arguments": {"depth": 0, "door": -1}, "victim": "v", "actor": "ch"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke scan_char with the fixture arguments once.
THEN {"portable_oracle": "Unavailable: dir_name[-1] is evaluated as a sprintf argument even though distance[0] contains no conversion."}
```

Open questions: do_scan around invokes this state for visible occupants in the current room. Define a safe target behavior explicitly; C out-of-bounds access is not portable.

## magic2.spell_farsight.blind-rejects-before-scan

blind rejects before scan

```text
CASE magic2.spell_farsight.blind-rejects-before-scan
SOURCE src/magic2.c:spell_farsight:46
GIVEN {"actor": {"id": "ch", "affected_by": ["AFF_BLIND"]}, "target_name": "north", "arguments": {"sn": 0, "level": 1, "vo": {"C_NULL": true}, "target": 0}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke spell_farsight with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Maybe it would help if you could see?\n\r"}], "forbidden": ["do_function", "scan", "movement"]}
```

## magic2.spell_farsight.delegates-raw-target-name

delegates raw target name

```text
CASE magic2.spell_farsight.delegates-raw-target-name
SOURCE src/magic2.c:spell_farsight:52
GIVEN {"actor": {"id": "ch", "affected_by": [], "position": "POS_SLEEPING"}, "target_name": "north", "arguments": {"sn": 0, "level": 1, "vo": {"C_NULL": true}, "target": 0}}
AND {"do_function": "Recording wrapper boundary; wrapper duplicates string, invokes handler and frees copy; does not enforce command-table position."}
WHEN Invoke spell_farsight with the fixture arguments once.
THEN {"ordered_events": [{"call": "do_function", "arguments": ["ch", "&do_scan", "north"]}], "forbidden": ["local position check", "interpret", "local resource charge"]}
```

## handler.can_see_room.ordinary-room

ordinary room

```text
CASE handler.can_see_room.ordinary-room
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 10, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": [], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.imp-below

imp below

```text
CASE handler.can_see_room.imp-below
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 59, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_IMP_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": false, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.imp-at-max

imp at max

```text
CASE handler.can_see_room.imp-at-max
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 60, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_IMP_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.gods-below

gods below

```text
CASE handler.can_see_room.gods-below
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 51, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_GODS_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": false, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.gods-at-immortal

gods at immortal

```text
CASE handler.can_see_room.gods-at-immortal
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_GODS_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.heroes-hero-still-denied

heroes hero still denied

```text
CASE handler.can_see_room.heroes-hero-still-denied
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 51, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_HEROES_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": false, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.heroes-at-immortal

heroes at immortal

```text
CASE handler.can_see_room.heroes-at-immortal
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_HEROES_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.newbie-at-five

newbie at five

```text
CASE handler.can_see_room.newbie-at-five
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 5, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_NEWBIES_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.newbie-at-six

newbie at six

```text
CASE handler.can_see_room.newbie-at-six
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 6, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_NEWBIES_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": false, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.newbie-immortal-exception

newbie immortal exception

```text
CASE handler.can_see_room.newbie-immortal-exception
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_NEWBIES_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.clan-mismatch

clan mismatch

```text
CASE handler.can_see_room.clan-mismatch
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 10, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": [], "clan": 2}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": false, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.clan-matches

clan matches

```text
CASE handler.can_see_room.clan-matches
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 10, "trust": 0, "clan": 2, "desc": null}, "room": {"room_flags": [], "clan": 2}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.clan-immortal-exception

clan immortal exception

```text
CASE handler.can_see_room.clan-immortal-exception
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": [], "clan": 2}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.trust-qualifies-low-level

trust qualifies low level

```text
CASE handler.can_see_room.trust-qualifies-low-level
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 1, "trust": 52, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_GODS_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.npc-level-sixty-not-immortal

npc level sixty not immortal

```text
CASE handler.can_see_room.npc-level-sixty-not-immortal
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "NPC", "level": 60, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_GODS_ONLY"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": false, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_room.safe-and-no-recall-do-not-hide-room

safe and no recall do not hide room

```text
CASE handler.can_see_room.safe-and-no-recall-do-not-hide-room
SOURCE src/handler.c:can_see_room:2415
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 10, "trust": 0, "clan": 0, "desc": null}, "room": {"room_flags": ["ROOM_SAFE", "ROOM_NO_RECALL"], "clan": 0}, "constants": {"MAX_LEVEL": 60, "LEVEL_IMMORTAL": 52}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_see_room with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and character"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see.ordinary-visible

ordinary visible

```text
CASE handler.can_see.ordinary-visible
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.self-before-blindness

self before blindness

```text
CASE handler.can_see.self-before-blindness
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_BLIND"], "in_room": "A", "desc": null}, "victim": {"id": "ch", "kind": "PC", "level": 10, "invis_level": 99, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.invis-level-above-trust

invis level above trust

```text
CASE handler.can_see.invis-level-above-trust
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 21, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.invis-level-equal-trust

invis level equal trust

```text
CASE handler.can_see.invis-level-equal-trust
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 20, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.holylight-does-not-beat-wizinvis

holylight does not beat wizinvis

```text
CASE handler.can_see.holylight-does-not-beat-wizinvis
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": ["PLR_HOLYLIGHT"], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 21, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.incognito-same-room

incognito same room

```text
CASE handler.can_see.incognito-same-room
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 99, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.incognito-other-room

incognito other room

```text
CASE handler.can_see.incognito-other-room
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 21, "affected_by": [], "fighting": null, "in_room": "B"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.incognito-equal-trust-other-room

incognito equal trust other room

```text
CASE handler.can_see.incognito-equal-trust-other-room
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 20, "affected_by": [], "fighting": null, "in_room": "B"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.holylight-beats-blindness

holylight beats blindness

```text
CASE handler.can_see.holylight-beats-blindness
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": ["PLR_HOLYLIGHT"], "affected_by": ["AFF_BLIND"], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.immortal-npc-beats-blindness

immortal npc beats blindness

```text
CASE handler.can_see.immortal-npc-beats-blindness
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "NPC", "level": 20, "trust": 52, "act": [], "affected_by": ["AFF_BLIND"], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.blind-denies

blind denies

```text
CASE handler.can_see.blind-denies
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_BLIND"], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.dark-denies

dark denies

```text
CASE handler.can_see.dark-denies
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.infrared-beats-dark

infrared beats dark

```text
CASE handler.can_see.infrared-beats-dark
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_INFRARED"], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": [], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.invisible-denies

invisible denies

```text
CASE handler.can_see.invisible-denies
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_INVISIBLE"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.detect-invisible

detect invisible

```text
CASE handler.can_see.detect-invisible
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_DETECT_INVIS"], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_INVISIBLE"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.sneak-roll-below-thirty

sneak roll below thirty

```text
CASE handler.can_see.sneak-roll-below-thirty
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_SNEAK"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [29]}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [29], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.sneak-roll-equal-thirty

sneak roll equal thirty

```text
CASE handler.can_see.sneak-roll-equal-thirty
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_SNEAK"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [30]}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [30], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.sneak-roll-above-thirty

sneak roll above thirty

```text
CASE handler.can_see.sneak-roll-above-thirty
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_SNEAK"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [31]}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [31], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.sneak-fighting-skips-roll

sneak fighting skips roll

```text
CASE handler.can_see.sneak-fighting-skips-roll
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_SNEAK"], "fighting": "enemy", "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.sneak-detect-hidden-skips-roll

sneak detect hidden skips roll

```text
CASE handler.can_see.sneak-detect-hidden-skips-roll
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_DETECT_HIDDEN"], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_SNEAK"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.hide-without-detection

hide without detection

```text
CASE handler.can_see.hide-without-detection
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_HIDE"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.hide-while-fighting-visible

hide while fighting visible

```text
CASE handler.can_see.hide-while-fighting-visible
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_HIDE"], "fighting": "enemy", "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.hide-with-detection-visible

hide with detection visible

```text
CASE handler.can_see.hide-with-detection-visible
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_DETECT_HIDDEN"], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_HIDE"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": true, "ordered_number_percent_returns": [], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see.sneak-roll-succeeds-but-hide-denies

sneak roll succeeds but hide denies

```text
CASE handler.can_see.sneak-roll-succeeds-but-hide-denies
SOURCE src/handler.c:can_see:2445
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "victim": {"id": "v", "kind": "PC", "level": 10, "invis_level": 0, "incog_level": 0, "affected_by": ["AFF_SNEAK", "AFF_HIDE"], "fighting": null, "in_room": "A"}, "identity": "victim aliases actor exactly when id=ch; actor state then applies", "skill_and_stats": {"victim.gsn_sneak": 40, "victim.STAT_DEX": 10, "actor.STAT_INT": 10}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "get_skill": {"kind": "stubbed skill calculation boundary", "returns": 40}, "get_curr_stat": {"victim.STAT_DEX": 10, "actor.STAT_INT": 10}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [30]}, "get_trust": "Real contract independently specified, actor level/trust/descriptor above."}
WHEN Invoke can_see with the fixture arguments once.
THEN {"return": false, "ordered_number_percent_returns": [30], "sneak_chance_when_used": "40 + (10*3/2) - (10*2) - (20 - 10*3/2) = 30", "unchanged": ["actor, victim, rooms"], "forbidden": ["messages", "unscripted random draws"]}
```

## handler.can_see_obj.ordinary

ordinary

```text
CASE handler.can_see_obj.ordinary
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": [], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.holylight-beats-death

holylight beats death

```text
CASE handler.can_see_obj.holylight-beats-death
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": ["PLR_HOLYLIGHT"], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": ["ITEM_VIS_DEATH"], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.death-hidden

death hidden

```text
CASE handler.can_see_obj.death-hidden
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": ["ITEM_VIS_DEATH"], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.blind-nonpotion

blind nonpotion

```text
CASE handler.can_see_obj.blind-nonpotion
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_BLIND"], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": [], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.blind-potion-exception

blind potion exception

```text
CASE handler.can_see_obj.blind-potion-exception
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_BLIND"], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_POTION", "extra_flags": [], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.lit-light-before-invis-dark

lit light before invis dark

```text
CASE handler.can_see_obj.lit-light-before-invis-dark
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_LIGHT", "extra_flags": ["ITEM_INVIS"], "value[2]": 1}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.infinite-light-negative-duration

infinite light negative duration

```text
CASE handler.can_see_obj.infinite-light-negative-duration
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_LIGHT", "extra_flags": [], "value[2]": -1}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.unlit-light-in-dark

unlit light in dark

```text
CASE handler.can_see_obj.unlit-light-in-dark
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_LIGHT", "extra_flags": [], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.invisible-glow-still-hidden

invisible glow still hidden

```text
CASE handler.can_see_obj.invisible-glow-still-hidden
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": ["ITEM_INVIS", "ITEM_GLOW"], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.detect-invis

detect invis

```text
CASE handler.can_see_obj.detect-invis
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_DETECT_INVIS"], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": ["ITEM_INVIS"], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": false}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.glow-beats-dark

glow beats dark

```text
CASE handler.can_see_obj.glow-beats-dark
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": ["ITEM_GLOW"], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.dark-without-vision

dark without vision

```text
CASE handler.can_see_obj.dark-without-vision
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": [], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": [], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.infrared-does-not-suffice-for-objects

infrared does not suffice for objects

```text
CASE handler.can_see_obj.infrared-does-not-suffice-for-objects
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_INFRARED"], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": [], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_see_obj.dark-vision-for-objects

dark vision for objects

```text
CASE handler.can_see_obj.dark-vision-for-objects
SOURCE src/handler.c:can_see_obj:2499
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 20, "trust": 0, "act": [], "affected_by": ["AFF_DARK_VISION"], "in_room": "A", "desc": null}, "object": {"id": "o", "item_type": "ITEM_WEAPON", "extra_flags": [], "value[2]": 0}}
AND {"room_is_dark": {"kind": "stubbed helper; independently specified", "returns": true}, "other_dependencies": "Flag macros only."}
WHEN Invoke can_see_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"], "forbidden": ["messages", "random draws"]}
```

## handler.can_drop_obj.normal-object

normal object

```text
CASE handler.can_drop_obj.normal-object
SOURCE src/handler.c:can_drop_obj:2531
GIVEN {"actor": {"kind": "PC", "level": 1, "trust": 0}, "object": {"extra_flags": []}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_drop_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"]}
```

## handler.can_drop_obj.nodrop-mortal

nodrop mortal

```text
CASE handler.can_drop_obj.nodrop-mortal
SOURCE src/handler.c:can_drop_obj:2531
GIVEN {"actor": {"kind": "PC", "level": 51, "trust": 0}, "object": {"extra_flags": ["ITEM_NODROP"]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_drop_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"]}
```

## handler.can_drop_obj.nodrop-immortal

nodrop immortal

```text
CASE handler.can_drop_obj.nodrop-immortal
SOURCE src/handler.c:can_drop_obj:2531
GIVEN {"actor": {"kind": "PC", "level": 52, "trust": 0}, "object": {"extra_flags": ["ITEM_NODROP"]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_drop_obj with the fixture arguments once.
THEN {"return": true, "unchanged": ["actor and object"]}
```

## handler.can_drop_obj.trust-alone-insufficient

trust alone insufficient

```text
CASE handler.can_drop_obj.trust-alone-insufficient
SOURCE src/handler.c:can_drop_obj:2531
GIVEN {"actor": {"kind": "PC", "level": 1, "trust": 60}, "object": {"extra_flags": ["ITEM_NODROP"]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_drop_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"]}
```

## handler.can_drop_obj.npc-no-exception

npc no exception

```text
CASE handler.can_drop_obj.npc-no-exception
SOURCE src/handler.c:can_drop_obj:2531
GIVEN {"actor": {"kind": "NPC", "level": 60, "trust": 60}, "object": {"extra_flags": ["ITEM_NODROP"]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke can_drop_obj with the fixture arguments once.
THEN {"return": false, "unchanged": ["actor and object"]}
```

## magic2.spell_portal.no-victim

no victim

```text
CASE magic2.spell_portal.no-victim
SOURCE src/magic2.c:spell_portal:61
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "C NULL"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": []}
```

## magic2.spell_portal.self-target

self target

```text
CASE magic2.spell_portal.self-target
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:62
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "ch"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": []}
```

## magic2.spell_portal.victim-no-room

victim no room

```text
CASE magic2.spell_portal.victim-no-room
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:63
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": null, "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": []}
```

## magic2.spell_portal.room-not-visible

room not visible

```text
CASE magic2.spell_portal.room-not-visible
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:64
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": false}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.destination-safe

destination safe

```text
CASE magic2.spell_portal.destination-safe
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:65
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": ["ROOM_SAFE"], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.destination-private

destination private

```text
CASE magic2.spell_portal.destination-private
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:66
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": ["ROOM_PRIVATE"], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.destination-solitary

destination solitary

```text
CASE magic2.spell_portal.destination-solitary
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:67
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": ["ROOM_SOLITARY"], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.destination-no-recall

destination no recall

```text
CASE magic2.spell_portal.destination-no-recall
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:68
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": ["ROOM_NO_RECALL"], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.origin-no-recall

origin no recall

```text
CASE magic2.spell_portal.origin-no-recall
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:69
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": ["ROOM_NO_RECALL"], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.victim-level-at-spell-plus-three

victim level at spell plus three

```text
CASE magic2.spell_portal.victim-level-at-spell-plus-three
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:70
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 43, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.hero-pc-regardless-of-trust

hero pc regardless of trust

```text
CASE magic2.spell_portal.hero-pc-regardless-of-trust
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:71
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 51, "clan": 0, "in_room": "B", "imm_flags": [], "trust": 0}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 60, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.npc-summon-immune

npc summon immune

```text
CASE magic2.spell_portal.npc-summon-immune
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:72
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "NPC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": ["IMM_SUMMON"]}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.npc-saves

npc saves

```text
CASE magic2.spell_portal.npc-saves
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:73
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "NPC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": true, "calls": 1}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.clan-mismatch

clan mismatch

```text
CASE magic2.spell_portal.clan-mismatch
SOURCE src/magic2.c:spell_portal:61; src/magic2.c:spell_portal:74
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 2, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_portal.mortal-no-component

mortal no component

```text
CASE magic2.spell_portal.mortal-no-component
SOURCE src/magic2.c:spell_portal:80
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": null}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"world_lookup": "v", "can_see_room": true, "saves_spell_calls": 0, "get_eq_char(WEAR_HOLD)": null, "create_object/obj_to_room/act": "Recording boundaries; creation suffix cases specify full ordered contract."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"outcome": "return with component failure", "messages_before_creation": [{"recipient": "ch", "text": "You lack the proper component for this spell.\n\r"}], "unchanged": ["wrong held item, if present"], "extract_obj_calls": 0, "create_object_calls": 0}
```

## magic2.spell_portal.mortal-wrong-component

mortal wrong component

```text
CASE magic2.spell_portal.mortal-wrong-component
SOURCE src/magic2.c:spell_portal:80
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "sword", "item_type": "ITEM_WEAPON"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"world_lookup": "v", "can_see_room": true, "saves_spell_calls": 0, "get_eq_char(WEAR_HOLD)": {"id": "sword", "item_type": "ITEM_WEAPON"}, "create_object/obj_to_room/act": "Recording boundaries; creation suffix cases specify full ordered contract."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"outcome": "return with component failure", "messages_before_creation": [{"recipient": "ch", "text": "You lack the proper component for this spell.\n\r"}], "unchanged": ["wrong held item, if present"], "extract_obj_calls": 0, "create_object_calls": 0}
```

## magic2.spell_portal.immortal-no-component

immortal no component

```text
CASE magic2.spell_portal.immortal-no-component
SOURCE src/magic2.c:spell_portal:80
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": null}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"world_lookup": "v", "can_see_room": true, "saves_spell_calls": 0, "get_eq_char(WEAR_HOLD)": null, "create_object/obj_to_room/act": "Recording boundaries; creation suffix cases specify full ordered contract."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"outcome": "continue to portal creation", "messages_before_creation": [], "unchanged": ["wrong held item, if present"], "extract_obj_calls": 0, "create_object_calls": 1}
```

## magic2.spell_portal.immortal-wrong-component

immortal wrong component

```text
CASE magic2.spell_portal.immortal-wrong-component
SOURCE src/magic2.c:spell_portal:80
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "sword", "item_type": "ITEM_WEAPON"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"world_lookup": "v", "can_see_room": true, "saves_spell_calls": 0, "get_eq_char(WEAR_HOLD)": {"id": "sword", "item_type": "ITEM_WEAPON"}, "create_object/obj_to_room/act": "Recording boundaries; creation suffix cases specify full ordered contract."}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"outcome": "continue to portal creation", "messages_before_creation": [], "unchanged": ["wrong held item, if present"], "extract_obj_calls": 0, "create_object_calls": 1}
```

## magic2.spell_portal.success-level-24

success level 24

```text
CASE magic2.spell_portal.success-level-24
SOURCE src/magic2.c:spell_portal:96
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 1, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 24, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "get_eq_char(WEAR_HOLD)": "stone", "create_object": "Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.", "extract_obj": "Record component consumption; internals of unequip/extraction remain separate pending dependencies.", "act": "Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.", "randomness": "none; victim is PC"}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"ordered_events": [{"act": "You draw upon the power of $p.", "channel": "TO_CHAR", "object": "stone"}, {"act": "It flares brightly and vanishes!", "channel": "TO_CHAR", "object": "stone"}, {"extract_obj": "stone"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-1"}}, {"set": {"portal-1.timer": 2, "portal-1.value[3]": 200}}, {"obj_to_room": ["portal-1", "A"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}], "result": {"stone": "extracted", "characters_in_rooms": "unchanged"}, "forbidden": ["movement", "additional mana/wait charges in this function", "backlink portal"]}
```

## magic2.spell_portal.success-level-25

success level 25

```text
CASE magic2.spell_portal.success-level-25
SOURCE src/magic2.c:spell_portal:96
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 1, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 25, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "get_eq_char(WEAR_HOLD)": "stone", "create_object": "Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.", "extract_obj": "Record component consumption; internals of unequip/extraction remain separate pending dependencies.", "act": "Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.", "randomness": "none; victim is PC"}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"ordered_events": [{"act": "You draw upon the power of $p.", "channel": "TO_CHAR", "object": "stone"}, {"act": "It flares brightly and vanishes!", "channel": "TO_CHAR", "object": "stone"}, {"extract_obj": "stone"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-1"}}, {"set": {"portal-1.timer": 3, "portal-1.value[3]": 200}}, {"obj_to_room": ["portal-1", "A"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}], "result": {"stone": "extracted", "characters_in_rooms": "unchanged"}, "forbidden": ["movement", "additional mana/wait charges in this function", "backlink portal"]}
```

## magic2.spell_portal.success-level-49

success level 49

```text
CASE magic2.spell_portal.success-level-49
SOURCE src/magic2.c:spell_portal:96
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 1, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 49, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "get_eq_char(WEAR_HOLD)": "stone", "create_object": "Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.", "extract_obj": "Record component consumption; internals of unequip/extraction remain separate pending dependencies.", "act": "Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.", "randomness": "none; victim is PC"}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"ordered_events": [{"act": "You draw upon the power of $p.", "channel": "TO_CHAR", "object": "stone"}, {"act": "It flares brightly and vanishes!", "channel": "TO_CHAR", "object": "stone"}, {"extract_obj": "stone"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-1"}}, {"set": {"portal-1.timer": 3, "portal-1.value[3]": 200}}, {"obj_to_room": ["portal-1", "A"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}], "result": {"stone": "extracted", "characters_in_rooms": "unchanged"}, "forbidden": ["movement", "additional mana/wait charges in this function", "backlink portal"]}
```

## magic2.spell_portal.success-level-50

success level 50

```text
CASE magic2.spell_portal.success-level-50
SOURCE src/magic2.c:spell_portal:96
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 1, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 50, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "get_eq_char(WEAR_HOLD)": "stone", "create_object": "Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.", "extract_obj": "Record component consumption; internals of unequip/extraction remain separate pending dependencies.", "act": "Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.", "randomness": "none; victim is PC"}
WHEN Invoke spell_portal with the fixture arguments once.
THEN {"ordered_events": [{"act": "You draw upon the power of $p.", "channel": "TO_CHAR", "object": "stone"}, {"act": "It flares brightly and vanishes!", "channel": "TO_CHAR", "object": "stone"}, {"extract_obj": "stone"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-1"}}, {"set": {"portal-1.timer": 4, "portal-1.value[3]": 200}}, {"obj_to_room": ["portal-1", "A"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}], "result": {"stone": "extracted", "characters_in_rooms": "unchanged"}, "forbidden": ["movement", "additional mana/wait charges in this function", "backlink portal"]}
```

## magic2.spell_nexus.no-victim

no victim

```text
CASE magic2.spell_nexus.no-victim
SOURCE src/magic2.c:spell_nexus:113
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "C NULL"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": []}
```

## magic2.spell_nexus.self-target

self target

```text
CASE magic2.spell_nexus.self-target
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:114
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "ch"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": []}
```

## magic2.spell_nexus.victim-no-room

victim no room

```text
CASE magic2.spell_nexus.victim-no-room
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:115
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": null, "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": []}
```

## magic2.spell_nexus.room-not-visible

room not visible

```text
CASE magic2.spell_nexus.room-not-visible
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:116
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": false}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B"]}
```

## magic2.spell_nexus.destination-safe

destination safe

```text
CASE magic2.spell_nexus.destination-safe
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:117
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": ["ROOM_SAFE"], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.destination-private

destination private

```text
CASE magic2.spell_nexus.destination-private
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:119
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": ["ROOM_PRIVATE"], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.destination-solitary

destination solitary

```text
CASE magic2.spell_nexus.destination-solitary
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:120
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": ["ROOM_SOLITARY"], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.destination-no-recall

destination no recall

```text
CASE magic2.spell_nexus.destination-no-recall
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:121
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": ["ROOM_NO_RECALL"], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.origin-no-recall

origin no recall

```text
CASE magic2.spell_nexus.origin-no-recall
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:122
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": ["ROOM_NO_RECALL"], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.victim-level-at-spell-plus-three

victim level at spell plus three

```text
CASE magic2.spell_nexus.victim-level-at-spell-plus-three
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:123
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 43, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.hero-pc-regardless-of-trust

hero pc regardless of trust

```text
CASE magic2.spell_nexus.hero-pc-regardless-of-trust
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:124
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 51, "clan": 0, "in_room": "B", "imm_flags": [], "trust": 0}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 60, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.npc-summon-immune

npc summon immune

```text
CASE magic2.spell_nexus.npc-summon-immune
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:125
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "NPC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": ["IMM_SUMMON"]}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.npc-saves

npc saves

```text
CASE magic2.spell_nexus.npc-saves
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:126
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "NPC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": true, "calls": 1}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.clan-mismatch

clan mismatch

```text
CASE magic2.spell_nexus.clan-mismatch
SOURCE src/magic2.c:spell_nexus:113; src/magic2.c:spell_nexus:127
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 2, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": {"kind": "stubbed lookup boundary", "returns": "v"}, "can_see_room": {"kind": "helper boundary; separately specified", "returns": true}, "saves_spell": {"kind": "spell-save boundary", "returns": false, "calls": 0}, "is_clan/is_same_clan": "Real contracts with snapshot clan table, separately specified.", "randomness": "No direct random draw in spell; saving helper is scripted."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["held stone and ownership", "all rooms and characters"], "forbidden": ["get_eq_char", "extract_obj", "create_object", "movement", "local mana/wait changes"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.mortal-no-component

mortal no component

```text
CASE magic2.spell_nexus.mortal-no-component
SOURCE src/magic2.c:spell_nexus:133
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": null}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"world_lookup": "v", "can_see_room": true, "saves_spell_calls": 0, "get_eq_char(WEAR_HOLD)": null, "create_object/obj_to_room/act": "Recording boundaries; creation suffix cases specify full ordered contract."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"outcome": "return with component failure", "messages_before_creation": [{"recipient": "ch", "text": "You lack the proper component for this spell.\n\r"}], "unchanged": ["wrong held item, if present"], "extract_obj_calls": 0, "create_object_calls": 0}
```

## magic2.spell_nexus.mortal-wrong-component

mortal wrong component

```text
CASE magic2.spell_nexus.mortal-wrong-component
SOURCE src/magic2.c:spell_nexus:133
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "sword", "item_type": "ITEM_WEAPON"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"world_lookup": "v", "can_see_room": true, "saves_spell_calls": 0, "get_eq_char(WEAR_HOLD)": {"id": "sword", "item_type": "ITEM_WEAPON"}, "create_object/obj_to_room/act": "Recording boundaries; creation suffix cases specify full ordered contract."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"outcome": "return with component failure", "messages_before_creation": [{"recipient": "ch", "text": "You lack the proper component for this spell.\n\r"}], "unchanged": ["wrong held item, if present"], "extract_obj_calls": 0, "create_object_calls": 0}
```

## magic2.spell_nexus.immortal-no-component

immortal no component

```text
CASE magic2.spell_nexus.immortal-no-component
SOURCE src/magic2.c:spell_nexus:133
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": null}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"world_lookup": "v", "can_see_room": true, "saves_spell_calls": 0, "get_eq_char(WEAR_HOLD)": null, "create_object/obj_to_room/act": "Recording boundaries; creation suffix cases specify full ordered contract."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"outcome": "continue to portal creation", "messages_before_creation": [], "unchanged": ["wrong held item, if present"], "extract_obj_calls": 0, "create_object_calls": 2}
```

## magic2.spell_nexus.immortal-wrong-component

immortal wrong component

```text
CASE magic2.spell_nexus.immortal-wrong-component
SOURCE src/magic2.c:spell_nexus:133
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "sword", "item_type": "ITEM_WEAPON"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"world_lookup": "v", "can_see_room": true, "saves_spell_calls": 0, "get_eq_char(WEAR_HOLD)": {"id": "sword", "item_type": "ITEM_WEAPON"}, "create_object/obj_to_room/act": "Recording boundaries; creation suffix cases specify full ordered contract."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"outcome": "continue to portal creation", "messages_before_creation": [], "unchanged": ["wrong held item, if present"], "extract_obj_calls": 0, "create_object_calls": 2}
```

## magic2.spell_nexus.success-level-9

success level 9

```text
CASE magic2.spell_nexus.success-level-9
SOURCE src/magic2.c:spell_nexus:150
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 1, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 9, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "get_eq_char(WEAR_HOLD)": "stone", "create_object": "Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.", "extract_obj": "Record component consumption; internals of unequip/extraction remain separate pending dependencies.", "act": "Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.", "randomness": "none; victim is PC"}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"ordered_events": [{"act": "You draw upon the power of $p.", "channel": "TO_CHAR", "object": "stone"}, {"act": "It flares brightly and vanishes!", "channel": "TO_CHAR", "object": "stone"}, {"extract_obj": "stone"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-1"}}, {"set": {"portal-1.timer": 1, "portal-1.value[3]": 200}}, {"obj_to_room": ["portal-1", "A"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-2"}}, {"set": {"portal-2.timer": 1, "portal-2.value[3]": 100}}, {"obj_to_room": ["portal-2", "B"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "v"}, {"act": "$p rises up from the ground.", "channel": "TO_CHAR", "anchor": "v"}], "result": {"stone": "extracted", "characters_in_rooms": "unchanged"}, "forbidden": ["movement", "additional mana/wait charges in this function", "third portal"]}
```

## magic2.spell_nexus.success-level-10

success level 10

```text
CASE magic2.spell_nexus.success-level-10
SOURCE src/magic2.c:spell_nexus:150
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 1, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 10, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "get_eq_char(WEAR_HOLD)": "stone", "create_object": "Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.", "extract_obj": "Record component consumption; internals of unequip/extraction remain separate pending dependencies.", "act": "Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.", "randomness": "none; victim is PC"}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"ordered_events": [{"act": "You draw upon the power of $p.", "channel": "TO_CHAR", "object": "stone"}, {"act": "It flares brightly and vanishes!", "channel": "TO_CHAR", "object": "stone"}, {"extract_obj": "stone"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-1"}}, {"set": {"portal-1.timer": 2, "portal-1.value[3]": 200}}, {"obj_to_room": ["portal-1", "A"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-2"}}, {"set": {"portal-2.timer": 2, "portal-2.value[3]": 100}}, {"obj_to_room": ["portal-2", "B"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "v"}, {"act": "$p rises up from the ground.", "channel": "TO_CHAR", "anchor": "v"}], "result": {"stone": "extracted", "characters_in_rooms": "unchanged"}, "forbidden": ["movement", "additional mana/wait charges in this function", "third portal"]}
```

## magic2.spell_nexus.success-level-19

success level 19

```text
CASE magic2.spell_nexus.success-level-19
SOURCE src/magic2.c:spell_nexus:150
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 1, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 19, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "get_eq_char(WEAR_HOLD)": "stone", "create_object": "Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.", "extract_obj": "Record component consumption; internals of unequip/extraction remain separate pending dependencies.", "act": "Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.", "randomness": "none; victim is PC"}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"ordered_events": [{"act": "You draw upon the power of $p.", "channel": "TO_CHAR", "object": "stone"}, {"act": "It flares brightly and vanishes!", "channel": "TO_CHAR", "object": "stone"}, {"extract_obj": "stone"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-1"}}, {"set": {"portal-1.timer": 2, "portal-1.value[3]": 200}}, {"obj_to_room": ["portal-1", "A"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-2"}}, {"set": {"portal-2.timer": 2, "portal-2.value[3]": 100}}, {"obj_to_room": ["portal-2", "B"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "v"}, {"act": "$p rises up from the ground.", "channel": "TO_CHAR", "anchor": "v"}], "result": {"stone": "extracted", "characters_in_rooms": "unchanged"}, "forbidden": ["movement", "additional mana/wait charges in this function", "third portal"]}
```

## magic2.spell_nexus.success-level-20

success level 20

```text
CASE magic2.spell_nexus.success-level-20
SOURCE src/magic2.c:spell_nexus:150
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 1, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 20, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "get_eq_char(WEAR_HOLD)": "stone", "create_object": "Recording allocation boundary with required portal prototype vnum=25; returns distinct object IDs.", "extract_obj": "Record component consumption; internals of unequip/extraction remain separate pending dependencies.", "act": "Record literal template/channel/object/anchor; final visibility-expanded delivery is a separate dependency.", "randomness": "none; victim is PC"}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"ordered_events": [{"act": "You draw upon the power of $p.", "channel": "TO_CHAR", "object": "stone"}, {"act": "It flares brightly and vanishes!", "channel": "TO_CHAR", "object": "stone"}, {"extract_obj": "stone"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-1"}}, {"set": {"portal-1.timer": 3, "portal-1.value[3]": 200}}, {"obj_to_room": ["portal-1", "A"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}, {"create_object": {"index_vnum": 25, "level": 0, "id": "portal-2"}}, {"set": {"portal-2.timer": 3, "portal-2.value[3]": 100}}, {"obj_to_room": ["portal-2", "B"]}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "v"}, {"act": "$p rises up from the ground.", "channel": "TO_CHAR", "anchor": "v"}], "result": {"stone": "extracted", "characters_in_rooms": "unchanged"}, "forbidden": ["movement", "additional mana/wait charges in this function", "third portal"]}
```

## magic2.spell_nexus.same-room-one-portal

same room one portal

```text
CASE magic2.spell_nexus.same-room-one-portal
SOURCE src/magic2.c:spell_nexus:159
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "A", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "create_object/act/extract_obj": "Recording boundaries as in nexus success cases.", "randomness": "none"}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"create_object_calls": 1, "portal": {"in_room": "A", "value[3]": 100, "timer": 5}, "stone": "consumed before creation", "forbidden": ["return portal creation", "destination-anchor messages"]}
```

## magic2.spell_nexus.safe-origin-denies

safe origin denies

```text
CASE magic2.spell_nexus.safe-origin-denies
SOURCE src/magic2.c:spell_nexus:118
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": ["ROOM_SAFE"], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": true, "saves_spell_calls": 0}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You failed.\n\r"}], "unchanged": ["stone", "all entities"], "forbidden": ["component lookup", "creation"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.origin-invisible-after-visible-destination

origin invisible after visible destination

```text
CASE magic2.spell_nexus.origin-invisible-after-visible-destination
SOURCE src/magic2.c:spell_nexus:116
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 40, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": {"id": "stone", "item_type": "ITEM_WARP_STONE"}}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": ["v", "observer-B"]}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}}
AND {"get_char_world": "v", "can_see_room": {"ordered_returns": [true, false]}}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"ordered_events": [{"get_char_world": ["ch", "v"]}, {"can_see_room": ["ch", "B"]}, {"can_see_room": ["ch", "A"]}, {"send_to_char": "You failed.\n\r", "recipient": "ch"}], "forbidden": ["saves_spell", "get_eq_char", "extract_obj", "create_object"], "can_see_room_calls_in_order": ["B", "A"]}
```

## magic2.spell_nexus.empty-destination-people-skips-announcements

empty destination people skips announcements

```text
CASE magic2.spell_nexus.empty-destination-people-skips-announcements
SOURCE src/magic2.c:spell_nexus:169
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 52, "trust": 0, "desc": null, "clan": 0, "in_room": "A", "held_item": null}, "victim": {"id": "v", "kind": "PC", "level": 20, "clan": 0, "in_room": "B", "imm_flags": []}, "rooms": {"A": {"vnum": 100, "room_flags": [], "clan": 0, "people": ["ch", "observer-A"]}, "B": {"vnum": 200, "room_flags": [], "clan": 0, "people": []}}, "target_name": "v", "arguments": {"sn": 1, "level": 40, "vo": null, "target": 0}, "invariant_override": "The lookup returns v with in_room B although B has no linked occupants."}
AND {"get_char_world": "Script v at the lookup boundary.", "can_see_room": {"ordered_returns": [true, true]}, "create_object": "Return portal-1 then portal-2.", "act": "Record template and recipient channel."}
WHEN Invoke spell_nexus with the fixture arguments once.
THEN {"ordered_events": [{"obj_to_room": ["portal-1", "A"], "timer": 5, "value[3]": 200}, {"act": "$p rises up from the ground.", "channel": "TO_ROOM", "anchor": "ch"}, {"act": "$p rises up before you.", "channel": "TO_CHAR", "anchor": "ch"}, {"obj_to_room": ["portal-2", "B"], "timer": 5, "value[3]": 100}], "forbidden": ["destination act", "extract_obj", "movement"]}
```

## healer.do_heal.no-healer-before-argument-parsing

no healer before argument parsing

```text
CASE healer.do_heal.no-healer-before-argument-parsing
SOURCE src/healer.c:do_heal:56
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 100, "silver": 0, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch"]}, "argument": "nonsense"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You can't do that here.\n\r"}], "unchanged": ["gold, silver, wait, mana"], "forbidden": ["one_argument", "skill_lookup", "spell call"]}
```

## healer.do_heal.price-menu

price menu

```text
CASE healer.do_heal.price-menu
SOURCE src/healer.c:do_heal:64
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 100, "silver": 0, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": ""}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"act": "$N says 'I offer the following spells:'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "subsequent_send_to_char_in_order": ["  light: cure light wounds      10 gold\n\r", "  serious: cure serious wounds  15 gold\n\r", "  critic: cure critical wounds  25 gold\n\r", "  heal: healing spell\t      50 gold\n\r", "  blind: cure blindness         20 gold\n\r", "  disease: cure disease         15 gold\n\r", "  poison:  cure poison\t      25 gold\n\r", "  uncurse: remove curse\t      50 gold\n\r", "  refresh: restore movement      5 gold\n\r", "  mana:  restore mana\t      10 gold\n\r", " Type heal <type> to be healed.\n\r"], "unchanged": ["currencies, wait, mana"], "forbidden": ["spell execution", "dice"]}
```

## healer.do_heal.unknown-service

unknown service

```text
CASE healer.do_heal.unknown-service
SOURCE src/healer.c:do_heal:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 100, "silver": 0, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "nonsense"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"act_calls": [{"template": "$N says 'Type 'heal' for a list of spells.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "unchanged": ["currencies, wait, mana"], "forbidden": ["deduct_cost", "spell", "dice"]}
```

## healer.do_heal.light-one-silver-short

light one silver short

```text
CASE healer.do_heal.light-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 999, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "light"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure light", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.light-exact-price

light exact price

```text
CASE healer.do_heal.light-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 1000, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "light"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure light", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 1000]}, {"healer_currency_credit": {"gold": 10, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "judicandus dies"}, {"spell_call": {"function": "spell_cure_light", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.serious-one-silver-short

serious one silver short

```text
CASE healer.do_heal.serious-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 1599, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "serious"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure serious", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.serious-exact-price

serious exact price

```text
CASE healer.do_heal.serious-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 1600, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "serious"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure serious", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 1600]}, {"healer_currency_credit": {"gold": 16, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "judicandus gzfuajg"}, {"spell_call": {"function": "spell_cure_serious", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.critical-one-silver-short

critical one silver short

```text
CASE healer.do_heal.critical-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 2499, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "critical"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure critical", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.critical-exact-price

critical exact price

```text
CASE healer.do_heal.critical-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 2500, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "critical"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure critical", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 2500]}, {"healer_currency_credit": {"gold": 25, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "judicandus qfuhuqar"}, {"spell_call": {"function": "spell_cure_critical", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.heal-one-silver-short

heal one silver short

```text
CASE healer.do_heal.heal-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 4999, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "heal"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "heal", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.heal-exact-price

heal exact price

```text
CASE healer.do_heal.heal-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 5000, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "heal"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "heal", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 5000]}, {"healer_currency_credit": {"gold": 50, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "pzar"}, {"spell_call": {"function": "spell_heal", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.blindness-one-silver-short

blindness one silver short

```text
CASE healer.do_heal.blindness-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 1999, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "blindness"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure blindness", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.blindness-exact-price

blindness exact price

```text
CASE healer.do_heal.blindness-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 2000, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "blindness"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure blindness", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 2000]}, {"healer_currency_credit": {"gold": 20, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "judicandus noselacri"}, {"spell_call": {"function": "spell_cure_blindness", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.disease-one-silver-short

disease one silver short

```text
CASE healer.do_heal.disease-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 1499, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "disease"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure disease", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.disease-exact-price

disease exact price

```text
CASE healer.do_heal.disease-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 1500, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "disease"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure disease", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 1500]}, {"healer_currency_credit": {"gold": 15, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "judicandus eugzagz"}, {"spell_call": {"function": "spell_cure_disease", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.poison-one-silver-short

poison one silver short

```text
CASE healer.do_heal.poison-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 2499, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "poison"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure poison", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.poison-exact-price

poison exact price

```text
CASE healer.do_heal.poison-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 2500, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "poison"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure poison", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 2500]}, {"healer_currency_credit": {"gold": 25, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "judicandus sausabru"}, {"spell_call": {"function": "spell_cure_poison", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.uncurse-one-silver-short

uncurse one silver short

```text
CASE healer.do_heal.uncurse-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 4999, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "uncurse"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "remove curse", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.uncurse-exact-price

uncurse exact price

```text
CASE healer.do_heal.uncurse-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 5000, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "uncurse"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "remove curse", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 5000]}, {"healer_currency_credit": {"gold": 50, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "candussido judifgz"}, {"spell_call": {"function": "spell_remove_curse", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.curse-one-silver-short

curse one silver short

```text
CASE healer.do_heal.curse-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 4999, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "curse"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "remove curse", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.curse-exact-price

curse exact price

```text
CASE healer.do_heal.curse-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 5000, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "curse"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "remove curse", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 5000]}, {"healer_currency_credit": {"gold": 50, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "candussido judifgz"}, {"spell_call": {"function": "spell_remove_curse", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.refresh-one-silver-short

refresh one silver short

```text
CASE healer.do_heal.refresh-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 499, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "refresh"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "refresh", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.refresh-exact-price

refresh exact price

```text
CASE healer.do_heal.refresh-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 500, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "refresh"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "refresh", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 500]}, {"healer_currency_credit": {"gold": 5, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "candusima"}, {"spell_call": {"function": "spell_refresh", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.moves-one-silver-short

moves one silver short

```text
CASE healer.do_heal.moves-one-silver-short
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 499, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "moves"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "refresh", "returns": 7}, {"act": "$N says 'You do not have enough gold for my services.'", "channel": "TO_CHAR", "actor": "ch", "victim": "h"}], "post_balance_if_enough": "unchanged", "forbidden": ["WAIT_STATE", "deduct_cost", "healer credit", "spell execution"]}
```

## healer.do_heal.moves-exact-price

moves exact price

```text
CASE healer.do_heal.moves-exact-price
SOURCE src/healer.c:do_heal:170
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 0, "silver": 500, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "moves"}
AND {"skill_lookup": {"kind": "stubbed skill-index boundary", "returns": 7}, "spell": "Recording behavior boundary; the selected healing spell internals remain separate pending paths.", "deduct_cost": "Use independent currency contract, specified below.", "act": "Record template, substitutions and channel; delivery rendering remains separate.", "randomness": "No direct random draws on non-mana path."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "refresh", "returns": 7}, {"wait": {"ch": 12}}, {"deduct_cost": ["ch", 500]}, {"healer_currency_credit": {"gold": 5, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "candusima"}, {"spell_call": {"function": "spell_refresh", "sn": 7, "level": 30, "caster": "h", "target": "ch", "target_type": "TARGET_CHAR"}}], "post_balance_if_enough": {"ch.gold": 0, "ch.silver": 0}, "forbidden": []}
```

## healer.do_heal.mana-uncapped

mana uncapped

```text
CASE healer.do_heal.mana-uncapped
SOURCE src/healer.c:do_heal:184
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 10, "silver": 0, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "mana"}
AND {"dice": {"kind": "scripted helper; separately specified", "returns": 2}, "deduct_cost": "Independently specified currency contract.", "randomness": "Only dice(2,8) boundary consumes scripted randomness."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"wait": 12}, {"deduct_cost": ["ch", 1000]}, {"healer_currency_credit": {"gold": 10, "silver": 0}}, {"act": "$n utters the words '$T'.", "actor": "h", "channel": "TO_ROOM", "words": "energizer"}, {"dice": [2, 8], "returns": 2}, {"mana_result": 22}, {"send_to_char": "A warm glow passes through you.\n\r", "recipient": "ch"}], "forbidden": ["skill_lookup", "spell function call"]}
```

## healer.do_heal.mana-capped

mana capped

```text
CASE healer.do_heal.mana-capped
SOURCE src/healer.c:do_heal:184
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 10, "silver": 0, "wait": 0, "mana": 95, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "mana"}
AND {"dice": {"kind": "scripted helper; separately specified", "returns": 16}, "deduct_cost": "Independently specified currency contract.", "randomness": "Only dice(2,8) boundary consumes scripted randomness."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"wait": 12}, {"deduct_cost": ["ch", 1000]}, {"healer_currency_credit": {"gold": 10, "silver": 0}}, {"act": "$n utters the words '$T'.", "actor": "h", "channel": "TO_ROOM", "words": "energizer"}, {"dice": [2, 8], "returns": 16}, {"mana_result": 100}, {"send_to_char": "A warm glow passes through you.\n\r", "recipient": "ch"}], "forbidden": ["skill_lookup", "spell function call"]}
```

## healer.do_heal.mana-existing-wait-preserved

mana existing wait preserved

```text
CASE healer.do_heal.mana-existing-wait-preserved
SOURCE src/healer.c:do_heal:184
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 10, "silver": 0, "wait": 20, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "mana"}
AND {"dice": {"kind": "scripted helper; separately specified", "returns": 2}, "deduct_cost": "Independently specified currency contract.", "randomness": "Only dice(2,8) boundary consumes scripted randomness."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"wait": 20}, {"deduct_cost": ["ch", 1000]}, {"healer_currency_credit": {"gold": 10, "silver": 0}}, {"act": "$n utters the words '$T'.", "actor": "h", "channel": "TO_ROOM", "words": "energizer"}, {"dice": [2, 8], "returns": 2}, {"mana_result": 22}, {"send_to_char": "A warm glow passes through you.\n\r", "recipient": "ch"}], "forbidden": ["skill_lookup", "spell function call"]}
```

## healer.do_heal.missing-skill-index-still-charges

missing skill index still charges

```text
CASE healer.do_heal.missing-skill-index-still-charges
SOURCE src/healer.c:do_heal:192
GIVEN {"actor": {"id": "ch", "kind": "PC", "in_room": "A", "gold": 100, "silver": 0, "wait": 0, "mana": 10, "max_mana": 100}, "healer": {"id": "h", "kind": "NPC", "act": ["ACT_IS_NPC", "ACT_IS_HEALER"], "level": 30, "gold": 0, "silver": 0}, "room": {"id": "A", "people_in_order": ["ch", "h"]}, "argument": "light"}
AND {"skill_lookup": {"kind": "failure injection at lookup boundary", "returns": -1}, "spell": "Record calls; none permitted."}
WHEN Invoke do_heal with the fixture arguments once.
THEN {"ordered_events": [{"skill_lookup": "cure light", "returns": -1}, {"wait": 12}, {"deduct_cost": ["ch", 1000]}, {"healer_currency_credit": {"gold": 10, "silver": 0}}, {"act": "$n utters the words '$T'.", "channel": "TO_ROOM", "actor": "h", "words": "judicandus dies"}], "return": "void", "forbidden": ["spell function call", "refund"]}
```

## handler.deduct_cost.silver-only

silver only

```text
CASE handler.deduct_cost.silver-only
SOURCE src/handler.c:deduct_cost:2223
GIVEN {"actor": {"gold": 2, "silver": 170}, "arguments": {"cost": 100}}
AND {"bug": "Recording logging boundary; no changes beyond this function."}
WHEN Invoke deduct_cost with the fixture arguments once.
THEN {"result": {"gold": 2, "silver": 70}, "bug_calls": [], "forbidden": ["messages", "random draws"]}
```

## handler.deduct_cost.gold-exact

gold exact

```text
CASE handler.deduct_cost.gold-exact
SOURCE src/handler.c:deduct_cost:2223
GIVEN {"actor": {"gold": 2, "silver": 0}, "arguments": {"cost": 100}}
AND {"bug": "Recording logging boundary; no changes beyond this function."}
WHEN Invoke deduct_cost with the fixture arguments once.
THEN {"result": {"gold": 1, "silver": 0}, "bug_calls": [], "forbidden": ["messages", "random draws"]}
```

## handler.deduct_cost.gold-change

gold change

```text
CASE handler.deduct_cost.gold-change
SOURCE src/handler.c:deduct_cost:2223
GIVEN {"actor": {"gold": 1, "silver": 0}, "arguments": {"cost": 1}}
AND {"bug": "Recording logging boundary; no changes beyond this function."}
WHEN Invoke deduct_cost with the fixture arguments once.
THEN {"result": {"gold": 0, "silver": 99}, "bug_calls": [], "forbidden": ["messages", "random draws"]}
```

## handler.deduct_cost.mixed-change

mixed change

```text
CASE handler.deduct_cost.mixed-change
SOURCE src/handler.c:deduct_cost:2223
GIVEN {"actor": {"gold": 2, "silver": 50}, "arguments": {"cost": 170}}
AND {"bug": "Recording logging boundary; no changes beyond this function."}
WHEN Invoke deduct_cost with the fixture arguments once.
THEN {"result": {"gold": 0, "silver": 80}, "bug_calls": [], "forbidden": ["messages", "random draws"]}
```

## handler.deduct_cost.zero

zero

```text
CASE handler.deduct_cost.zero
SOURCE src/handler.c:deduct_cost:2223
GIVEN {"actor": {"gold": 2, "silver": 50}, "arguments": {"cost": 0}}
AND {"bug": "Recording logging boundary; no changes beyond this function."}
WHEN Invoke deduct_cost with the fixture arguments once.
THEN {"result": {"gold": 2, "silver": 50}, "bug_calls": [], "forbidden": ["messages", "random draws"]}
```

## handler.deduct_cost.negative-cost-credits

negative cost credits

```text
CASE handler.deduct_cost.negative-cost-credits
SOURCE src/handler.c:deduct_cost:2223
GIVEN {"actor": {"gold": 2, "silver": 50}, "arguments": {"cost": -20}}
AND {"bug": "Recording logging boundary; no changes beyond this function."}
WHEN Invoke deduct_cost with the fixture arguments once.
THEN {"result": {"gold": 2, "silver": 70}, "bug_calls": [], "forbidden": ["messages", "random draws"]}
```

## handler.deduct_cost.insufficient-gold-clamped

insufficient gold clamped

```text
CASE handler.deduct_cost.insufficient-gold-clamped
SOURCE src/handler.c:deduct_cost:2223
GIVEN {"actor": {"gold": 0, "silver": 10}, "arguments": {"cost": 100}}
AND {"bug": "Recording logging boundary; no changes beyond this function."}
WHEN Invoke deduct_cost with the fixture arguments once.
THEN {"result": {"gold": 0, "silver": 10}, "bug_calls": [["deduct costs: gold %d < 0", -1]], "forbidden": ["messages", "random draws"]}
```

## magic.saves_dispel.equal-level-below

equal level below

```text
CASE magic.saves_dispel.equal-level-below
SOURCE src/magic.c:saves_dispel:247
GIVEN {"arguments": {"dis_level": 20, "spell_level": 20, "duration": 1}}
AND {"number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [49]}}
WHEN Invoke saves_dispel with the fixture arguments once.
THEN {"return": true, "save_threshold": 50, "number_percent_calls": 1}
```

## magic.saves_dispel.equal-level-equality

equal level equality

```text
CASE magic.saves_dispel.equal-level-equality
SOURCE src/magic.c:saves_dispel:247
GIVEN {"arguments": {"dis_level": 20, "spell_level": 20, "duration": 1}}
AND {"number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [50]}}
WHEN Invoke saves_dispel with the fixture arguments once.
THEN {"return": false, "save_threshold": 50, "number_percent_calls": 1}
```

## magic.saves_dispel.permanent-adds-five

permanent adds five

```text
CASE magic.saves_dispel.permanent-adds-five
SOURCE src/magic.c:saves_dispel:247
GIVEN {"arguments": {"dis_level": 20, "spell_level": 20, "duration": -1}}
AND {"number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [74]}}
WHEN Invoke saves_dispel with the fixture arguments once.
THEN {"return": true, "save_threshold": 75, "number_percent_calls": 1}
```

## magic.saves_dispel.permanent-threshold

permanent threshold

```text
CASE magic.saves_dispel.permanent-threshold
SOURCE src/magic.c:saves_dispel:247
GIVEN {"arguments": {"dis_level": 20, "spell_level": 20, "duration": -1}}
AND {"number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [75]}}
WHEN Invoke saves_dispel with the fixture arguments once.
THEN {"return": false, "save_threshold": 75, "number_percent_calls": 1}
```

## magic.saves_dispel.lower-cap-below

lower cap below

```text
CASE magic.saves_dispel.lower-cap-below
SOURCE src/magic.c:saves_dispel:247
GIVEN {"arguments": {"dis_level": 100, "spell_level": 1, "duration": 0}}
AND {"number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [4]}}
WHEN Invoke saves_dispel with the fixture arguments once.
THEN {"return": true, "save_threshold": 5, "number_percent_calls": 1}
```

## magic.saves_dispel.lower-cap-equality

lower cap equality

```text
CASE magic.saves_dispel.lower-cap-equality
SOURCE src/magic.c:saves_dispel:247
GIVEN {"arguments": {"dis_level": 100, "spell_level": 1, "duration": 0}}
AND {"number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [5]}}
WHEN Invoke saves_dispel with the fixture arguments once.
THEN {"return": false, "save_threshold": 5, "number_percent_calls": 1}
```

## magic.saves_dispel.upper-cap-below

upper cap below

```text
CASE magic.saves_dispel.upper-cap-below
SOURCE src/magic.c:saves_dispel:247
GIVEN {"arguments": {"dis_level": 1, "spell_level": 100, "duration": 0}}
AND {"number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [94]}}
WHEN Invoke saves_dispel with the fixture arguments once.
THEN {"return": true, "save_threshold": 95, "number_percent_calls": 1}
```

## magic.saves_dispel.upper-cap-equality

upper cap equality

```text
CASE magic.saves_dispel.upper-cap-equality
SOURCE src/magic.c:saves_dispel:247
GIVEN {"arguments": {"dis_level": 1, "spell_level": 100, "duration": 0}}
AND {"number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [95]}}
WHEN Invoke saves_dispel with the fixture arguments once.
THEN {"return": false, "save_threshold": 95, "number_percent_calls": 1}
```

## magic.saves_spell.normal-below

normal below

```text
CASE magic.saves_spell.normal-below
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [49]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 50, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.normal-equality

normal equality

```text
CASE magic.saves_spell.normal-equality
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [50]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 50, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.immune-no-roll

immune no roll

```text
CASE magic.saves_spell.immune-no-roll
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_IMMUNE"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": []}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": null, "number_percent_calls": 0, "unchanged": ["victim"]}
```

## magic.saves_spell.resistant-below

resistant below

```text
CASE magic.saves_spell.resistant-below
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_RESISTANT"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [51]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 52, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.resistant-equality

resistant equality

```text
CASE magic.saves_spell.resistant-equality
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_RESISTANT"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [52]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 52, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.vulnerable-equality

vulnerable equality

```text
CASE magic.saves_spell.vulnerable-equality
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_VULNERABLE"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [48]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 48, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.berserk-adds-half-level

berserk adds half level

```text
CASE magic.saves_spell.berserk-adds-half-level
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": ["AFF_BERSERK"], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [59]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 60, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.negative-saving-throw-improves

negative saving throw improves

```text
CASE magic.saves_spell.negative-saving-throw-improves
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": -2, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [53]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 54, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.positive-saving-throw-weakens

positive saving throw weakens

```text
CASE magic.saves_spell.positive-saving-throw-weakens
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 2, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [46]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 46, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.mana-class-nine-tenths

mana class nine tenths

```text
CASE magic.saves_spell.mana-class-nine-tenths
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "PC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": true}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [45]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 45, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.mana-class-integer-truncation

mana class integer truncation

```text
CASE magic.saves_spell.mana-class-integer-truncation
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "PC", "level": 20, "saving_throw": 1, "affected_by": [], "class_fMana": true}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [43]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 43, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.lower-cap

lower cap

```text
CASE magic.saves_spell.lower-cap
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": 100, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [5]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 5, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## magic.saves_spell.upper-cap

upper cap

```text
CASE magic.saves_spell.upper-cap
SOURCE src/magic.c:saves_spell:220
GIVEN {"victim": {"id": "v", "kind": "NPC", "level": 20, "saving_throw": -100, "affected_by": [], "class_fMana": false}, "arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "class_contract": "class_table[victim.class].fMana is class_fMana above; this fixture supplies a table row at the boundary."}
AND {"check_immune": {"kind": "stubbed helper boundary", "returns": "IS_NORMAL"}, "number_percent": {"kind": "scripted helper; independently specified", "ordered_returns": [95]}}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 95, "number_percent_calls": 1, "unchanged": ["victim"]}
```

## ban.check_ban.empty-list

empty list

```text
CASE ban.check_ban.empty-list
SOURCE src/ban.c:check_ban:110
GIVEN {"arguments": {"site": "EXAMPLE.COM", "type": "BAN_ALL"}, "ban_list_in_order": []}
AND {"capitalize/str_prefix/str_suffix": "Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host."}
WHEN Invoke check_ban with the fixture arguments once.
THEN {"return": false, "unchanged": ["site and ban list"], "forbidden": ["messages", "persistence writes", "random draws"]}
```

## ban.check_ban.type-not-set

type not set

```text
CASE ban.check_ban.type-not-set
SOURCE src/ban.c:check_ban:110
GIVEN {"arguments": {"site": "example.com", "type": "BAN_ALL"}, "ban_list_in_order": [{"name": "example.com", "flags": ["BAN_SUFFIX"]}]}
AND {"capitalize/str_prefix/str_suffix": "Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host."}
WHEN Invoke check_ban with the fixture arguments once.
THEN {"return": false, "unchanged": ["site and ban list"], "forbidden": ["messages", "persistence writes", "random draws"]}
```

## ban.check_ban.exact-without-prefix-suffix-does-not-match

exact without prefix suffix does not match

```text
CASE ban.check_ban.exact-without-prefix-suffix-does-not-match
SOURCE src/ban.c:check_ban:110
GIVEN {"arguments": {"site": "example.com", "type": "BAN_ALL"}, "ban_list_in_order": [{"name": "example.com", "flags": ["BAN_ALL"]}]}
AND {"capitalize/str_prefix/str_suffix": "Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host."}
WHEN Invoke check_ban with the fixture arguments once.
THEN {"return": false, "unchanged": ["site and ban list"], "forbidden": ["messages", "persistence writes", "random draws"]}
```

## ban.check_ban.prefix-flag-tests-host-suffix

prefix flag tests host suffix

```text
CASE ban.check_ban.prefix-flag-tests-host-suffix
SOURCE src/ban.c:check_ban:110
GIVEN {"arguments": {"site": "Host.Example.COM", "type": "BAN_ALL"}, "ban_list_in_order": [{"name": "example.com", "flags": ["BAN_ALL", "BAN_PREFIX"]}]}
AND {"capitalize/str_prefix/str_suffix": "Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host."}
WHEN Invoke check_ban with the fixture arguments once.
THEN {"return": true, "unchanged": ["site and ban list"], "forbidden": ["messages", "persistence writes", "random draws"]}
```

## ban.check_ban.suffix-flag-tests-host-prefix

suffix flag tests host prefix

```text
CASE ban.check_ban.suffix-flag-tests-host-prefix
SOURCE src/ban.c:check_ban:110
GIVEN {"arguments": {"site": "HOST.example.com", "type": "BAN_ALL"}, "ban_list_in_order": [{"name": "host", "flags": ["BAN_ALL", "BAN_SUFFIX"]}]}
AND {"capitalize/str_prefix/str_suffix": "Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host."}
WHEN Invoke check_ban with the fixture arguments once.
THEN {"return": true, "unchanged": ["site and ban list"], "forbidden": ["messages", "persistence writes", "random draws"]}
```

## ban.check_ban.both-flags-host-contained-in-pattern

both flags host contained in pattern

```text
CASE ban.check_ban.both-flags-host-contained-in-pattern
SOURCE src/ban.c:check_ban:110
GIVEN {"arguments": {"site": "Example.COM", "type": "BAN_ALL"}, "ban_list_in_order": [{"name": "xxexample.comyy", "flags": ["BAN_ALL", "BAN_PREFIX", "BAN_SUFFIX"]}]}
AND {"capitalize/str_prefix/str_suffix": "Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host."}
WHEN Invoke check_ban with the fixture arguments once.
THEN {"return": true, "unchanged": ["site and ban list"], "forbidden": ["messages", "persistence writes", "random draws"]}
```

## ban.check_ban.both-flags-do-not-match-interior-pattern-in-host

both flags do not match interior pattern in host

```text
CASE ban.check_ban.both-flags-do-not-match-interior-pattern-in-host
SOURCE src/ban.c:check_ban:110
GIVEN {"arguments": {"site": "xxexample.comyy", "type": "BAN_ALL"}, "ban_list_in_order": [{"name": "example.com", "flags": ["BAN_ALL", "BAN_PREFIX", "BAN_SUFFIX"]}]}
AND {"capitalize/str_prefix/str_suffix": "Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host."}
WHEN Invoke check_ban with the fixture arguments once.
THEN {"return": false, "unchanged": ["site and ban list"], "forbidden": ["messages", "persistence writes", "random draws"]}
```

## ban.check_ban.later-entry-matches

later entry matches

```text
CASE ban.check_ban.later-entry-matches
SOURCE src/ban.c:check_ban:110
GIVEN {"arguments": {"site": "host.example.com", "type": "BAN_ALL"}, "ban_list_in_order": [{"name": "other", "flags": ["BAN_ALL", "BAN_SUFFIX"]}, {"name": "example.com", "flags": ["BAN_ALL", "BAN_PREFIX"]}]}
AND {"capitalize/str_prefix/str_suffix": "Real string contracts independently specified. strcpy host then LOWER(host[0]) lowercases the whole host."}
WHEN Invoke check_ban with the fixture arguments once.
THEN {"return": true, "unchanged": ["site and ban list"], "forbidden": ["messages", "persistence writes", "random draws"]}
```

## ban.save_bans.empty

empty

```text
CASE ban.save_bans.empty
SOURCE src/ban.c:save_bans:68
GIVEN {"ban_list": [], "fpReserve": "R0", "existing_ban_file": "old\n"}
AND {"fopen": {"ordered_returns": ["W", "R1"]}, "writes_close_and_unlink": "Succeed where called.", "print_flags": "Script BDF then AEF for the two permanent rows. Isolate the serializer signed-shift platform issue."}
WHEN Invoke save_bans with the fixture arguments once.
THEN {"ordered_events": [{"fclose": "R0"}, {"fopen": ["ban.txt", "w"]}, {"fclose": "W"}, {"fopen": ["/dev/null", "r"]}, {"unlink": "ban.txt"}], "fpReserve": "R1", "final_ban_file": null, "unchanged": ["ban_list"]}
```

## ban.save_bans.temporary-only

temporary only

```text
CASE ban.save_bans.temporary-only
SOURCE src/ban.c:save_bans:68
GIVEN {"ban_list": [["temp", 56, ["BAN_ALL"]]], "fpReserve": "R0", "existing_ban_file": "old\n"}
AND {"fopen": {"ordered_returns": ["W", "R1"]}, "writes_close_and_unlink": "Succeed where called.", "print_flags": "Script BDF then AEF for the two permanent rows. Isolate the serializer signed-shift platform issue."}
WHEN Invoke save_bans with the fixture arguments once.
THEN {"ordered_events": [{"fclose": "R0"}, {"fopen": ["ban.txt", "w"]}, {"fclose": "W"}, {"fopen": ["/dev/null", "r"]}, {"unlink": "ban.txt"}], "fpReserve": "R1", "final_ban_file": null, "unchanged": ["ban_list"]}
```

## ban.save_bans.permanent-in-list-order

permanent in list order

```text
CASE ban.save_bans.permanent-in-list-order
SOURCE src/ban.c:save_bans:68
GIVEN {"ban_list": [["alpha", 56, ["BAN_PREFIX", "BAN_ALL", "BAN_PERMANENT"]], ["temp", 56, ["BAN_ALL"]], ["beta", 60, ["BAN_SUFFIX", "BAN_PERMIT", "BAN_PERMANENT"]]], "fpReserve": "R0", "existing_ban_file": "old\n"}
AND {"fopen": {"ordered_returns": ["W", "R1"]}, "writes_close_and_unlink": "Succeed where called.", "print_flags": "Script BDF then AEF for the two permanent rows. Isolate the serializer signed-shift platform issue."}
WHEN Invoke save_bans with the fixture arguments once.
THEN {"ordered_events": [{"fclose": "R0"}, {"fopen": ["ban.txt", "w"]}, {"write": ["W", "alpha                56 BDF\n"]}, {"write": ["W", "beta                 60 AEF\n"]}, {"fclose": "W"}, {"fopen": ["/dev/null", "r"]}], "fpReserve": "R1", "final_ban_file": "alpha                56 BDF\nbeta                 60 AEF\n", "unchanged": ["ban_list"]}
```

## ban.save_bans.open-failure-permanent-row-undefined

open failure permanent row undefined

```text
CASE ban.save_bans.open-failure-permanent-row-undefined
SOURCE src/ban.c:save_bans:53
GIVEN {"ban_list": [["alpha", 56, ["BAN_ALL", "BAN_PERMANENT"]]], "fpReserve": "R0"}
AND {"fopen": {"ordered_returns": [null]}}
WHEN Invoke save_bans with the fixture arguments once.
THEN {"defined_prefix": [{"fclose": "R0"}, {"fopen": ["ban.txt", "w"]}, {"perror": "ban.txt"}], "portable_oracle": "Unavailable after the diagnostic because fprintf receives a null stream."}
```

Open questions: The source continues after the failed open. A portable fixture cannot assert the resulting process state.

## ban.save_bans.open-failure-without-permanent-row-undefined

open failure without permanent row undefined

```text
CASE ban.save_bans.open-failure-without-permanent-row-undefined
SOURCE src/ban.c:save_bans:53
GIVEN {"ban_list": [], "fpReserve": "R0"}
AND {"fopen": {"ordered_returns": [null]}}
WHEN Invoke save_bans with the fixture arguments once.
THEN {"defined_prefix": [{"fclose": "R0"}, {"fopen": ["ban.txt", "w"]}, {"perror": "ban.txt"}], "portable_oracle": "Unavailable after the diagnostic because fclose receives a null stream."}
```

Open questions: The failed open does not branch around fclose.

## ban.load_bans.missing-file

missing file

```text
CASE ban.load_bans.missing-file
SOURCE src/ban.c:load_bans:77
GIVEN {"ban_list": [], "file": null}
AND {"fopen": {"ordered_returns": [null]}}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"ordered_events": [{"fopen": ["ban.txt", "r"]}], "unchanged": ["ban_list"], "forbidden": ["new_ban", "fclose", "read"]}
```

## ban.load_bans.loads-two-rows-in-file-order

loads two rows in file order

```text
CASE ban.load_bans.loads-two-rows-in-file-order
SOURCE src/ban.c:load_bans:97
GIVEN {"ban_list": [], "file": "alpha 56 BDF\nbeta 60 AEF\n"}
AND {"fopen": "Succeed; use the real parser on fixture bytes."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_PREFIX", "BAN_ALL", "BAN_PERMANENT"]], ["beta", 60, ["BAN_SUFFIX", "BAN_PERMIT", "BAN_PERMANENT"]]], "ordered_events": ["Open ban.txt for reading", "Allocate and link alpha as head", "Allocate and append beta", "Close file after EOF"], "forbidden": ["save_bans"]}
```

## ban.load_bans.nonempty-list-first-append-undefined

nonempty list first append undefined

```text
CASE ban.load_bans.nonempty-list-first-append-undefined
SOURCE src/ban.c:load_bans:100
GIVEN {"ban_list": [["old", 56, ["BAN_ALL"]]], "file": "alpha 56 BDF\n"}
AND {"fopen": "Succeed; use the real parser on fixture bytes."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"defined_prefix": ["Open file and parse alpha row"], "portable_oracle": "ban_last is still NULL on first append."}
```

Open questions: The boot caller starts with an empty global list. A later direct call with existing entries dereferences NULL.

## ban.do_allow.missing-name

missing name

```text
CASE ban.do_allow.missing-name
SOURCE src/ban.c:do_allow:275
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "", "ban_list": [["alpha", 56, ["BAN_ALL"]]]}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke do_allow with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_ALL"]]], "ordered_events": [{"send_to_char": "Remove which site from the ban list?\n\r", "recipient": "ch"}], "forbidden": ["free_ban", "save_bans"]}
```

## ban.do_allow.missing-entry

missing entry

```text
CASE ban.do_allow.missing-entry
SOURCE src/ban.c:do_allow:275
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "z", "ban_list": [["alpha", 56, ["BAN_ALL"]], ["beta", 55, ["BAN_NEWBIES"]]]}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke do_allow with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_ALL"]], ["beta", 55, ["BAN_NEWBIES"]]], "ordered_events": [{"send_to_char": "Site is not banned.\n\r", "recipient": "ch"}], "forbidden": ["free_ban", "save_bans"]}
```

## ban.do_allow.higher-trust

higher trust

```text
CASE ban.do_allow.higher-trust
SOURCE src/ban.c:do_allow:275
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "alpha", "ban_list": [["alpha", 57, ["BAN_ALL"]]]}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke do_allow with the fixture arguments once.
THEN {"result_list": [["alpha", 57, ["BAN_ALL"]]], "ordered_events": [{"send_to_char": "You are not powerful enough to lift that ban.\n\r", "recipient": "ch"}], "forbidden": ["free_ban", "save_bans"]}
```

## ban.do_allow.remove-head-at-equal-trust

remove head at equal trust

```text
CASE ban.do_allow.remove-head-at-equal-trust
SOURCE src/ban.c:do_allow:275
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "ALPHA ignored", "ban_list": [["alpha", 56, ["BAN_ALL"]], ["beta", 55, ["BAN_NEWBIES"]]]}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke do_allow with the fixture arguments once.
THEN {"result_list": [["beta", 55, ["BAN_NEWBIES"]]], "ordered_events": [{"free_ban": "alpha"}, {"send_to_char": "Ban on alpha lifted.\n\r", "recipient": "ch"}, {"save_bans": [["beta", 55, ["BAN_NEWBIES"]]]}], "forbidden": []}
```

## ban.do_allow.remove-interior

remove interior

```text
CASE ban.do_allow.remove-interior
SOURCE src/ban.c:do_allow:275
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "beta", "ban_list": [["alpha", 56, ["BAN_ALL"]], ["beta", 55, ["BAN_NEWBIES"]], ["gamma", 55, ["BAN_ALL"]]]}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke do_allow with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_ALL"]], ["gamma", 55, ["BAN_ALL"]]], "ordered_events": [{"free_ban": "beta"}, {"send_to_char": "Ban on beta lifted.\n\r", "recipient": "ch"}, {"save_bans": [["alpha", 56, ["BAN_ALL"]], ["gamma", 55, ["BAN_ALL"]]]}], "forbidden": []}
```

## ban.do_ban.dispatch-unchanged-argument

dispatch unchanged argument

```text
CASE ban.do_ban.dispatch-unchanged-argument
SOURCE src/ban.c:do_ban:258
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "*Alpha* n"}
AND {"ban_site": "Recording boundary."}
WHEN Invoke do_ban with the fixture arguments once.
THEN {"ordered_events": [{"ban_site": ["ch", "*Alpha* n", false]}]}
```

## ban.do_permban.dispatch-unchanged-argument

dispatch unchanged argument

```text
CASE ban.do_permban.dispatch-unchanged-argument
SOURCE src/ban.c:do_permban:263
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "*Alpha* n"}
AND {"ban_site": "Recording boundary."}
WHEN Invoke do_permban with the fixture arguments once.
THEN {"ordered_events": [{"ban_site": ["ch", "*Alpha* n", true]}]}
```

## ban.ban_site.no-sites

no sites

```text
CASE ban.ban_site.no-sites
SOURCE src/ban.c:ban_site:146
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "", "fPerm": false, "ban_list": []}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [], "ordered_events": [{"send_to_char": "No sites banned at this time.\n\r", "recipient": "ch"}], "forbidden": ["new_ban", "save_bans"]}
```

## ban.ban_site.invalid-type-before-pattern

invalid type before pattern

```text
CASE ban.ban_site.invalid-type-before-pattern
SOURCE src/ban.c:ban_site:146
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "* invalid", "fPerm": false, "ban_list": []}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [], "ordered_events": [{"send_to_char": "Acceptable ban types are all, newbies, and permit.\n\r", "recipient": "ch"}], "forbidden": ["new_ban", "save_bans"]}
```

## ban.ban_site.double-star-empty-name

double star empty name

```text
CASE ban.ban_site.double-star-empty-name
SOURCE src/ban.c:ban_site:146
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "**", "fPerm": false, "ban_list": []}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [], "ordered_events": [{"send_to_char": "You have to ban SOMETHING.\n\r", "recipient": "ch"}], "forbidden": ["new_ban", "save_bans"]}
```

## ban.ban_site.higher-trust

higher trust

```text
CASE ban.ban_site.higher-trust
SOURCE src/ban.c:ban_site:146
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "ALPHA a", "fPerm": true, "ban_list": [["alpha", 57, ["BAN_ALL"]]]}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [["alpha", 57, ["BAN_ALL"]]], "ordered_events": [{"send_to_char": "That ban was set by a higher power.\n\r", "recipient": "ch"}], "forbidden": ["new_ban", "save_bans"]}
```

## ban.ban_site.plain-default-type

plain default type

```text
CASE ban.ban_site.plain-default-type
SOURCE src/ban.c:ban_site:146
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "alpha", "fPerm": false, "ban_list": [["beta", 55, ["BAN_NEWBIES"]]]}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_ALL"]], ["beta", 55, ["BAN_NEWBIES"]]], "ordered_events": [{"new_ban": ["alpha", 56, ["BAN_ALL"]]}, {"save_bans": [["alpha", 56, ["BAN_ALL"]], ["beta", 55, ["BAN_NEWBIES"]]]}, {"send_to_char": "alpha has been banned.\n\r", "recipient": "ch"}], "forbidden": []}
```

## ban.ban_site.both-wildcards-permanent-newbies

both wildcards permanent newbies

```text
CASE ban.ban_site.both-wildcards-permanent-newbies
SOURCE src/ban.c:ban_site:146
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "*Alpha* n", "fPerm": true, "ban_list": []}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_NEWBIES", "BAN_PREFIX", "BAN_SUFFIX", "BAN_PERMANENT"]]], "ordered_events": [{"new_ban": ["alpha", 56, ["BAN_NEWBIES", "BAN_PREFIX", "BAN_SUFFIX", "BAN_PERMANENT"]]}, {"save_bans": [["alpha", 56, ["BAN_NEWBIES", "BAN_PREFIX", "BAN_SUFFIX", "BAN_PERMANENT"]]]}, {"send_to_char": "alpha has been banned.\n\r", "recipient": "ch"}], "forbidden": []}
```

## ban.ban_site.suffix-permit

suffix permit

```text
CASE ban.ban_site.suffix-permit
SOURCE src/ban.c:ban_site:146
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "alpha* p", "fPerm": false, "ban_list": []}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_PERMIT", "BAN_SUFFIX"]]], "ordered_events": [{"new_ban": ["alpha", 56, ["BAN_PERMIT", "BAN_SUFFIX"]]}, {"save_bans": [["alpha", 56, ["BAN_PERMIT", "BAN_SUFFIX"]]]}, {"send_to_char": "alpha has been banned.\n\r", "recipient": "ch"}], "forbidden": []}
```

## ban.ban_site.list-formats-wildcards-and-type-precedence

list formats wildcards and type precedence

```text
CASE ban.ban_site.list-formats-wildcards-and-type-precedence
SOURCE src/ban.c:ban_site:149
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "", "fPerm": false, "ban_list": [["alpha", 56, ["BAN_PREFIX", "BAN_SUFFIX", "BAN_NEWBIES", "BAN_PERMIT", "BAN_PERMANENT"]], ["beta", 55, ["BAN_SUFFIX", "BAN_PERMIT"]], ["gamma", 54, ["BAN_ALL"]], ["delta", 53, []]]}
AND {"buffer": "Record append order and concatenate all entries within capacity."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"ordered_events": [{"page_to_char": "Banned sites  level  type     status\n\r*alpha*         56   newbies  perm\n\rbeta*           55   permit   temp\n\rgamma           54   all      temp\n\rdelta           53            temp\n\r", "recipient": "ch"}, {"free_buf": "listing"}], "unchanged": ["ban_list"], "forbidden": ["save_bans", "new_ban"]}
```

## ban.ban_site.replace-head-with-empty-free-list

replace head with empty free list

```text
CASE ban.ban_site.replace-head-with-empty-free-list
SOURCE src/ban.c:ban_site:225
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "alpha p", "fPerm": false, "ban_list": [["alpha", 56, ["BAN_ALL"]], ["beta", 55, ["BAN_NEWBIES"]]], "ban_free": []}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_PERMIT"]], ["beta", 55, ["BAN_NEWBIES"]]], "ordered_events": [{"free_ban": "old alpha"}, {"new_ban": "reuses old alpha record"}, {"save_bans": [["alpha", 56, ["BAN_PERMIT"]], ["beta", 55, ["BAN_NEWBIES"]]]}, {"send_to_char": "alpha has been banned.\n\r", "recipient": "ch"}]}
```

## ban.ban_site.replace-interior-with-empty-free-list

replace interior with empty free list

```text
CASE ban.ban_site.replace-interior-with-empty-free-list
SOURCE src/ban.c:ban_site:225
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "alpha p", "fPerm": false, "ban_list": [["beta", 55, ["BAN_NEWBIES"]], ["alpha", 56, ["BAN_ALL"]]], "ban_free": []}
AND {"save_bans": "Record the list at persistence boundary."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"result_list": [["alpha", 56, ["BAN_PERMIT"]], ["beta", 55, ["BAN_NEWBIES"]]], "ordered_events": [{"free_ban": "old alpha"}, {"new_ban": "reuses old alpha record"}, {"save_bans": [["alpha", 56, ["BAN_PERMIT"]], ["beta", 55, ["BAN_NEWBIES"]]]}, {"send_to_char": "alpha has been banned.\n\r", "recipient": "ch"}]}
```

## ban.ban_site.single-star-empty-name-index-undefined

single star empty name index undefined

```text
CASE ban.ban_site.single-star-empty-name-index-undefined
SOURCE src/ban.c:ban_site:201
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 56, "trust": 0, "desc": null}, "argument": "*", "fPerm": false, "ban_list": []}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"portable_oracle": "After consuming the leading star, strlen(name) is zero. The unsigned subtraction wraps and the computed array index lies outside arg1."}
```

Open questions: The empty-pattern diagnostic comes after the out-of-bounds expression.

## update.update_handler.fresh-process-through-call-1

fresh process through call 1

```text
CASE update.update_handler.fresh-process-through-call-1
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 1 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1], "mobile_update": [1], "violence_update": [1], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 480, "pulse_music": 24, "pulse_mobile": 16, "pulse_violence": 12, "pulse_point": 240}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-2

fresh process through call 2

```text
CASE update.update_handler.fresh-process-through-call-2
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 2 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1], "mobile_update": [1], "violence_update": [1], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 479, "pulse_music": 23, "pulse_mobile": 15, "pulse_violence": 11, "pulse_point": 239}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-12

fresh process through call 12

```text
CASE update.update_handler.fresh-process-through-call-12
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 12 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1], "mobile_update": [1], "violence_update": [1], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 469, "pulse_music": 13, "pulse_mobile": 5, "pulse_violence": 1, "pulse_point": 229}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-13

fresh process through call 13

```text
CASE update.update_handler.fresh-process-through-call-13
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 13 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1], "mobile_update": [1], "violence_update": [1, 13], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 468, "pulse_music": 12, "pulse_mobile": 4, "pulse_violence": 12, "pulse_point": 228}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-16

fresh process through call 16

```text
CASE update.update_handler.fresh-process-through-call-16
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 16 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1], "mobile_update": [1], "violence_update": [1, 13], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 465, "pulse_music": 9, "pulse_mobile": 1, "pulse_violence": 9, "pulse_point": 225}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-17

fresh process through call 17

```text
CASE update.update_handler.fresh-process-through-call-17
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 17 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1], "mobile_update": [1, 17], "violence_update": [1, 13], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 464, "pulse_music": 8, "pulse_mobile": 16, "pulse_violence": 8, "pulse_point": 224}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-24

fresh process through call 24

```text
CASE update.update_handler.fresh-process-through-call-24
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 24 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1], "mobile_update": [1, 17], "violence_update": [1, 13], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 457, "pulse_music": 1, "pulse_mobile": 9, "pulse_violence": 1, "pulse_point": 217}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-25

fresh process through call 25

```text
CASE update.update_handler.fresh-process-through-call-25
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 25 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1, 25], "mobile_update": [1, 17], "violence_update": [1, 13, 25], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 456, "pulse_music": 24, "pulse_mobile": 8, "pulse_violence": 12, "pulse_point": 216}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-240

fresh process through call 240

```text
CASE update.update_handler.fresh-process-through-call-240
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 240 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1, 25, 49, 73, 97, 121, 145, 169, 193, 217], "mobile_update": [1, 17, 33, 49, 65, 81, 97, 113, 129, 145, 161, 177, 193, 209, 225], "violence_update": [1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121, 133, 145, 157, 169, 181, 193, 205, 217, 229], "point_group": [1]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 241, "pulse_music": 1, "pulse_mobile": 1, "pulse_violence": 1, "pulse_point": 1}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-241

fresh process through call 241

```text
CASE update.update_handler.fresh-process-through-call-241
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 241 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1, 25, 49, 73, 97, 121, 145, 169, 193, 217, 241], "mobile_update": [1, 17, 33, 49, 65, 81, 97, 113, 129, 145, 161, 177, 193, 209, 225, 241], "violence_update": [1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121, 133, 145, 157, 169, 181, 193, 205, 217, 229, 241], "point_group": [1, 241]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 240, "pulse_music": 24, "pulse_mobile": 16, "pulse_violence": 12, "pulse_point": 240}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-480

fresh process through call 480

```text
CASE update.update_handler.fresh-process-through-call-480
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 480 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1], "song_update": [1, 25, 49, 73, 97, 121, 145, 169, 193, 217, 241, 265, 289, 313, 337, 361, 385, 409, 433, 457], "mobile_update": [1, 17, 33, 49, 65, 81, 97, 113, 129, 145, 161, 177, 193, 209, 225, 241, 257, 273, 289, 305, 321, 337, 353, 369, 385, 401, 417, 433, 449, 465], "violence_update": [1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121, 133, 145, 157, 169, 181, 193, 205, 217, 229, 241, 253, 265, 277, 289, 301, 313, 325, 337, 349, 361, 373, 385, 397, 409, 421, 433, 445, 457, 469], "point_group": [1, 241]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 1, "pulse_music": 1, "pulse_mobile": 1, "pulse_violence": 1, "pulse_point": 1}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## update.update_handler.fresh-process-through-call-481

fresh process through call 481

```text
CASE update.update_handler.fresh-process-through-call-481
SOURCE src/update.c:update_handler:1083
GIVEN {"static_counters_initial": {"pulse_area": 0, "pulse_music": 0, "pulse_mobile": 0, "pulse_violence": 0, "pulse_point": 0}, "units": "One invocation per game-loop pulse; PULSE_PER_SECOND=4."}
AND {"scheduled_helpers": "Recording boundaries only; helper world mutations are not stubbed in their own subsystem cases.", "wiznet": "Record message/channel/flags without network delivery.", "randomness": "No random calls in this wrapper; interval randomizers are commented out."}
WHEN In a fresh scheduler state, invoke update_handler 481 times sequentially; retain counters between invocations.
THEN {"call_indices_by_event": {"area_update": [1, 481], "song_update": [1, 25, 49, 73, 97, 121, 145, 169, 193, 217, 241, 265, 289, 313, 337, 361, 385, 409, 433, 457, 481], "mobile_update": [1, 17, 33, 49, 65, 81, 97, 113, 129, 145, 161, 177, 193, 209, 225, 241, 257, 273, 289, 305, 321, 337, 353, 369, 385, 401, 417, 433, 449, 465, 481], "violence_update": [1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121, 133, 145, 157, 169, 181, 193, 205, 217, 229, 241, 253, 265, 277, 289, 301, 313, 325, 337, 349, 361, 373, 385, 397, 409, 421, 433, 445, 457, 469, 481], "point_group": [1, 241, 481]}, "point_group_order": ["wiznet(TICK!,C NULL,C NULL,WIZ_TICKS,0,0)", "pulse_point reset", "weather_update", "char_update", "obj_update"], "same_invocation_group_order": ["area_update", "song_update", "mobile_update", "violence_update", "point_group", "aggr_update", "tail_chain"], "every_invocation": ["aggr_update", "tail_chain"], "counter_result": {"pulse_area": 480, "pulse_music": 24, "pulse_mobile": 16, "pulse_violence": 12, "pulse_point": 240}, "forbidden": ["number_range calls to randomize tick or area interval"]}
```

## act_enter.get_random_room.reject-missing-index

reject missing index

```text
CASE act_enter.get_random_room.reject-missing-index
SOURCE src/act_enter.c:get_random_room:48
GIVEN {"actor": {"id": "ch", "kind": "PC", "act": []}, "candidate": {"id": "bad", "room_flags": []}, "accepted": {"id": "good", "room_flags": []}}
AND {"number_range": {"kind": "scripted helper; independently specified", "ordered_returns": [1, 2]}, "get_room_index": {"1": "C NULL", "2": "good"}, "can_see_room": {"bad": true, "good": true}, "room_is_private": {"bad": false, "good": false}, "helper_boundaries": "Lookup and room permission collaborators are recorded/scripted; private and visible contracts independently specified."}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"ordered_sampling": [{"number_range": [0, 65535], "returns": 1}, {"get_room_index": 1, "returns": "C NULL"}, {"number_range": [0, 65535], "returns": 2}, {"get_room_index": 2, "returns": "good"}], "return": "good", "unchanged": ["actor, rooms"], "forbidden": ["movement", "messages"], "can_see_room_calls_in_order": ["good"], "room_is_private_calls_in_order": ["good"]}
```

## act_enter.get_random_room.reject-invisible

reject invisible

```text
CASE act_enter.get_random_room.reject-invisible
SOURCE src/act_enter.c:get_random_room:48
GIVEN {"actor": {"id": "ch", "kind": "PC", "act": []}, "candidate": {"id": "bad", "room_flags": []}, "accepted": {"id": "good", "room_flags": []}}
AND {"number_range": {"kind": "scripted helper; independently specified", "ordered_returns": [1, 2]}, "get_room_index": {"1": "bad", "2": "good"}, "can_see_room": {"bad": false, "good": true}, "room_is_private": {"bad": false, "good": false}, "helper_boundaries": "Lookup and room permission collaborators are recorded/scripted; private and visible contracts independently specified."}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"ordered_sampling": [{"number_range": [0, 65535], "returns": 1}, {"get_room_index": 1, "returns": "bad"}, {"number_range": [0, 65535], "returns": 2}, {"get_room_index": 2, "returns": "good"}], "return": "good", "unchanged": ["actor, rooms"], "forbidden": ["movement", "messages"], "can_see_room_calls_in_order": ["bad", "good"], "room_is_private_calls_in_order": ["good"]}
```

## act_enter.get_random_room.reject-private-helper

reject private helper

```text
CASE act_enter.get_random_room.reject-private-helper
SOURCE src/act_enter.c:get_random_room:48
GIVEN {"actor": {"id": "ch", "kind": "PC", "act": []}, "candidate": {"id": "bad", "room_flags": []}, "accepted": {"id": "good", "room_flags": []}}
AND {"number_range": {"kind": "scripted helper; independently specified", "ordered_returns": [1, 2]}, "get_room_index": {"1": "bad", "2": "good"}, "can_see_room": {"bad": true, "good": true}, "room_is_private": {"bad": true, "good": false}, "helper_boundaries": "Lookup and room permission collaborators are recorded/scripted; private and visible contracts independently specified."}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"ordered_sampling": [{"number_range": [0, 65535], "returns": 1}, {"get_room_index": 1, "returns": "bad"}, {"number_range": [0, 65535], "returns": 2}, {"get_room_index": 2, "returns": "good"}], "return": "good", "unchanged": ["actor, rooms"], "forbidden": ["movement", "messages"], "can_see_room_calls_in_order": ["bad", "good"], "room_is_private_calls_in_order": ["bad", "good"]}
```

## act_enter.get_random_room.reject-private-flag

reject private flag

```text
CASE act_enter.get_random_room.reject-private-flag
SOURCE src/act_enter.c:get_random_room:48
GIVEN {"actor": {"id": "ch", "kind": "PC", "act": []}, "candidate": {"id": "bad", "room_flags": ["ROOM_PRIVATE"]}, "accepted": {"id": "good", "room_flags": []}}
AND {"number_range": {"kind": "scripted helper; independently specified", "ordered_returns": [1, 2]}, "get_room_index": {"1": "bad", "2": "good"}, "can_see_room": {"bad": true, "good": true}, "room_is_private": {"bad": false, "good": false}, "helper_boundaries": "Lookup and room permission collaborators are recorded/scripted; private and visible contracts independently specified."}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"ordered_sampling": [{"number_range": [0, 65535], "returns": 1}, {"get_room_index": 1, "returns": "bad"}, {"number_range": [0, 65535], "returns": 2}, {"get_room_index": 2, "returns": "good"}], "return": "good", "unchanged": ["actor, rooms"], "forbidden": ["movement", "messages"], "can_see_room_calls_in_order": ["bad", "good"], "room_is_private_calls_in_order": ["bad", "good"]}
```

## act_enter.get_random_room.reject-solitary-flag

reject solitary flag

```text
CASE act_enter.get_random_room.reject-solitary-flag
SOURCE src/act_enter.c:get_random_room:48
GIVEN {"actor": {"id": "ch", "kind": "PC", "act": []}, "candidate": {"id": "bad", "room_flags": ["ROOM_SOLITARY"]}, "accepted": {"id": "good", "room_flags": []}}
AND {"number_range": {"kind": "scripted helper; independently specified", "ordered_returns": [1, 2]}, "get_room_index": {"1": "bad", "2": "good"}, "can_see_room": {"bad": true, "good": true}, "room_is_private": {"bad": false, "good": false}, "helper_boundaries": "Lookup and room permission collaborators are recorded/scripted; private and visible contracts independently specified."}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"ordered_sampling": [{"number_range": [0, 65535], "returns": 1}, {"get_room_index": 1, "returns": "bad"}, {"number_range": [0, 65535], "returns": 2}, {"get_room_index": 2, "returns": "good"}], "return": "good", "unchanged": ["actor, rooms"], "forbidden": ["movement", "messages"], "can_see_room_calls_in_order": ["bad", "good"], "room_is_private_calls_in_order": ["bad", "good"]}
```

## act_enter.get_random_room.reject-safe-flag

reject safe flag

```text
CASE act_enter.get_random_room.reject-safe-flag
SOURCE src/act_enter.c:get_random_room:48
GIVEN {"actor": {"id": "ch", "kind": "PC", "act": []}, "candidate": {"id": "bad", "room_flags": ["ROOM_SAFE"]}, "accepted": {"id": "good", "room_flags": []}}
AND {"number_range": {"kind": "scripted helper; independently specified", "ordered_returns": [1, 2]}, "get_room_index": {"1": "bad", "2": "good"}, "can_see_room": {"bad": true, "good": true}, "room_is_private": {"bad": false, "good": false}, "helper_boundaries": "Lookup and room permission collaborators are recorded/scripted; private and visible contracts independently specified."}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"ordered_sampling": [{"number_range": [0, 65535], "returns": 1}, {"get_room_index": 1, "returns": "bad"}, {"number_range": [0, 65535], "returns": 2}, {"get_room_index": 2, "returns": "good"}], "return": "good", "unchanged": ["actor, rooms"], "forbidden": ["movement", "messages"], "can_see_room_calls_in_order": ["bad", "good"], "room_is_private_calls_in_order": ["bad", "good"]}
```

## act_enter.get_random_room.reject-law-denies-ordinary-pc

reject law denies ordinary pc

```text
CASE act_enter.get_random_room.reject-law-denies-ordinary-pc
SOURCE src/act_enter.c:get_random_room:48
GIVEN {"actor": {"id": "ch", "kind": "PC", "act": []}, "candidate": {"id": "bad", "room_flags": ["ROOM_LAW"]}, "accepted": {"id": "good", "room_flags": []}}
AND {"number_range": {"kind": "scripted helper; independently specified", "ordered_returns": [1, 2]}, "get_room_index": {"1": "bad", "2": "good"}, "can_see_room": {"bad": true, "good": true}, "room_is_private": {"bad": false, "good": false}, "helper_boundaries": "Lookup and room permission collaborators are recorded/scripted; private and visible contracts independently specified."}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"ordered_sampling": [{"number_range": [0, 65535], "returns": 1}, {"get_room_index": 1, "returns": "bad"}, {"number_range": [0, 65535], "returns": 2}, {"get_room_index": 2, "returns": "good"}], "return": "good", "unchanged": ["actor, rooms"], "forbidden": ["movement", "messages"], "can_see_room_calls_in_order": ["bad", "good"], "room_is_private_calls_in_order": ["bad", "good"]}
```

## act_enter.get_random_room.npc-law-allowed-even-aggressive

npc law allowed even aggressive

```text
CASE act_enter.get_random_room.npc-law-allowed-even-aggressive
SOURCE src/act_enter.c:get_random_room:55
GIVEN {"actor": {"kind": "NPC", "act": ["ACT_IS_NPC", "ACT_AGGRESSIVE"]}, "room": {"id": "R", "room_flags": ["ROOM_LAW"]}}
AND {"number_range": {"kind": "scripted helper", "ordered_returns": [1]}, "get_room_index(1)": "R", "can_see_room": true, "room_is_private": false}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"return": "R", "number_range_calls": 1, "unchanged": ["all entities"]}
```

## act_enter.get_random_room.pc-aggressive-bit-law-allowed

pc aggressive bit law allowed

```text
CASE act_enter.get_random_room.pc-aggressive-bit-law-allowed
SOURCE src/act_enter.c:get_random_room:55
GIVEN {"actor": {"kind": "PC", "act": ["ACT_AGGRESSIVE"]}, "room": {"id": "R", "room_flags": ["ROOM_LAW"]}}
AND {"number_range": {"kind": "scripted helper", "ordered_returns": [1]}, "get_room_index(1)": "R", "can_see_room": true, "room_is_private": false}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"return": "R", "number_range_calls": 1, "unchanged": ["all entities"]}
```

## act_enter.get_random_room.ordinary-room-first-draw

ordinary room first draw

```text
CASE act_enter.get_random_room.ordinary-room-first-draw
SOURCE src/act_enter.c:get_random_room:55
GIVEN {"actor": {"kind": "PC", "act": []}, "room": {"id": "R", "room_flags": []}}
AND {"number_range": {"kind": "scripted helper", "ordered_returns": [1]}, "get_room_index(1)": "R", "can_see_room": true, "room_is_private": false}
WHEN Invoke get_random_room with the fixture arguments once.
THEN {"return": "R", "number_range_calls": 1, "unchanged": ["all entities"]}
```

## act_enter.do_enter.fighting-silent

fighting silent

```text
CASE act_enter.do_enter.fighting-silent
SOURCE src/act_enter.c:do_enter:68
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": "enemy", "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, 0, 200, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": {"kind": "object lookup boundary", "returns": "P", "calls": 0}, "get_trust": "Real helper contract with actor level/trust/descriptor above."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"messages": [], "unchanged": ["room membership", "portal values and ownership", "actor resources"], "forbidden": ["get_random_room", "destination room lookup", "movement", "charge use", "follower recursion"]}
```

## act_enter.do_enter.empty-argument

empty argument

```text
CASE act_enter.do_enter.empty-argument
SOURCE src/act_enter.c:do_enter:68
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, 0, 200, 0], "in_room": "A"}, "argument": ""}
AND {"get_obj_list": {"kind": "object lookup boundary", "returns": "P", "calls": 0}, "get_trust": "Real helper contract with actor level/trust/descriptor above."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Nope, can't do it.\n\r"}], "unchanged": ["room membership", "portal values and ownership", "actor resources"], "forbidden": ["get_random_room", "destination room lookup", "movement", "charge use", "follower recursion"]}
```

## act_enter.do_enter.no-object

no object

```text
CASE act_enter.do_enter.no-object
SOURCE src/act_enter.c:do_enter:68
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, 0, 200, 0], "in_room": "A"}, "argument": "missing"}
AND {"get_obj_list": {"kind": "object lookup boundary", "returns": "C NULL", "calls": 1}, "get_trust": "Real helper contract with actor level/trust/descriptor above."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You don't see that here.\n\r"}], "unchanged": ["room membership", "portal values and ownership", "actor resources"], "forbidden": ["get_random_room", "destination room lookup", "movement", "charge use", "follower recursion"]}
```

## act_enter.do_enter.not-a-portal

not a portal

```text
CASE act_enter.do_enter.not-a-portal
SOURCE src/act_enter.c:do_enter:68
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_WEAPON", "value": [0, 0, 0, 200, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": {"kind": "object lookup boundary", "returns": "P", "calls": 1}, "get_trust": "Real helper contract with actor level/trust/descriptor above."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You can't seem to find a way in.\n\r"}], "unchanged": ["room membership", "portal values and ownership", "actor resources"], "forbidden": ["get_random_room", "destination room lookup", "movement", "charge use", "follower recursion"]}
```

## act_enter.do_enter.closed-mortal

closed mortal

```text
CASE act_enter.do_enter.closed-mortal
SOURCE src/act_enter.c:do_enter:68
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, ["EX_CLOSED"], [], 200, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": {"kind": "object lookup boundary", "returns": "P", "calls": 1}, "get_trust": "Real helper contract with actor level/trust/descriptor above."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "You can't seem to find a way in.\n\r"}], "unchanged": ["room membership", "portal values and ownership", "actor resources"], "forbidden": ["get_random_room", "destination room lookup", "movement", "charge use", "follower recursion"]}
```

## act_enter.do_enter.cursed-mortal

cursed mortal

```text
CASE act_enter.do_enter.cursed-mortal
SOURCE src/act_enter.c:do_enter:68
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": ["AFF_CURSE"], "act": []}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, 0, 200, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": {"kind": "object lookup boundary", "returns": "P", "calls": 1}, "get_trust": "Real helper contract with actor level/trust/descriptor above."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "Something prevents you from leaving...\n\r"}], "unchanged": ["room membership", "portal values and ownership", "actor resources"], "forbidden": ["get_random_room", "destination room lookup", "movement", "charge use", "follower recursion"]}
```

## act_enter.do_enter.random-flag-records-before-origin-rejection

random flag records before origin rejection

```text
CASE act_enter.do_enter.random-flag-records-before-origin-rejection
SOURCE src/act_enter.c:do_enter:103
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, ["GATE_RANDOM", "GATE_BUGGY"], 200, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": "P", "get_random_room": "A", "number_percent": {"ordered_returns": []}}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": [{"get_obj_list": ["ch", "portal", "A.contents"]}, {"get_random_room": "ch", "returns": "A"}, {"set": {"P.value[3]": 100}}, {"act": "$p doesn't seem to go anywhere.", "channel": "TO_CHAR", "actor": "ch", "object": "P"}], "P.value[3]": 100, "forbidden": ["can_see_room", "room_is_private", "movement", "charge mutation", "follower dispatch"]}
```

## act_enter.do_enter.minus-one-records-before-origin-rejection

minus one records before origin rejection

```text
CASE act_enter.do_enter.minus-one-records-before-origin-rejection
SOURCE src/act_enter.c:do_enter:103
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, ["GATE_BUGGY"], -1, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": "P", "get_random_room": "A", "number_percent": {"ordered_returns": []}}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": [{"get_obj_list": ["ch", "portal", "A.contents"]}, {"get_random_room": "ch", "returns": "A"}, {"set": {"P.value[3]": 100}}, {"act": "$p doesn't seem to go anywhere.", "channel": "TO_CHAR", "actor": "ch", "object": "P"}], "P.value[3]": 100, "forbidden": ["can_see_room", "room_is_private", "movement", "charge mutation", "follower dispatch"]}
```

## act_enter.do_enter.buggy-four-uses-random-without-recording

buggy four uses random without recording

```text
CASE act_enter.do_enter.buggy-four-uses-random-without-recording
SOURCE src/act_enter.c:do_enter:103
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, ["GATE_BUGGY"], 200, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": "P", "get_random_room": "A", "number_percent": {"ordered_returns": [4]}}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": [{"get_obj_list": ["ch", "portal", "A.contents"]}, {"number_percent": 4}, {"get_random_room": "ch", "returns": "A"}, {"act": "$p doesn't seem to go anywhere.", "channel": "TO_CHAR", "actor": "ch", "object": "P"}], "P.value[3]": 200, "forbidden": ["can_see_room", "room_is_private", "movement", "charge mutation", "follower dispatch"]}
```

## act_enter.do_enter.buggy-five-uses-index

buggy five uses index

```text
CASE act_enter.do_enter.buggy-five-uses-index
SOURCE src/act_enter.c:do_enter:103
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, ["GATE_BUGGY"], 200, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": "P", "get_room_index": null, "number_percent": {"ordered_returns": [5]}}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": [{"get_obj_list": ["ch", "portal", "A.contents"]}, {"number_percent": 5}, {"get_room_index": 200, "returns": null}, {"act": "$p doesn't seem to go anywhere.", "channel": "TO_CHAR", "actor": "ch", "object": "P"}], "P.value[3]": 200, "forbidden": ["can_see_room", "room_is_private", "movement", "charge mutation", "follower dispatch"]}
```

## act_enter.do_enter.fixed-portal-skips-percent

fixed portal skips percent

```text
CASE act_enter.do_enter.fixed-portal-skips-percent
SOURCE src/act_enter.c:do_enter:103
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, [], 200, 0], "in_room": "A"}, "argument": "portal"}
AND {"get_obj_list": "P", "get_room_index": null, "number_percent": {"ordered_returns": []}}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": [{"get_obj_list": ["ch", "portal", "A.contents"]}, {"get_room_index": 200, "returns": null}, {"act": "$p doesn't seem to go anywhere.", "channel": "TO_CHAR", "actor": "ch", "object": "P"}], "P.value[3]": 200, "forbidden": ["can_see_room", "room_is_private", "movement", "charge mutation", "follower dispatch"]}
```

## act_enter.do_enter.unlimited-stationary-portal

unlimited stationary portal

```text
CASE act_enter.do_enter.unlimited-stationary-portal
SOURCE src/act_enter.c:do_enter:137
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, [], 200, 0], "in_room": "A"}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}}
AND {"get_obj_list": "P", "get_room_index(200)": "B", "can_see_room": true, "room_is_private": false, "act/do_function": "Record delivery boundaries. do_look does not mutate the fixture."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_destination_resolution": [{"act": "$n steps into $p.", "channel": "TO_ROOM", "anchor": "ch", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "channel": "TO_CHAR", "anchor": "ch"}, {"char_from_room": "ch"}, {"char_to_room": ["ch", "B"]}, {"act": "$n has arrived through $p.", "channel": "TO_ROOM", "anchor": "ch", "room": "B"}, {"do_function": ["ch", "do_look", "auto"], "charge_during_look": 0}], "ch.in_room": "B", "portal_final_state": {"value[0]": 0, "in_room": "A"}, "forbidden": ["follower dispatch", "number_percent"]}
```

## act_enter.do_enter.charged-portal-goes-with-actor

charged portal goes with actor

```text
CASE act_enter.do_enter.charged-portal-goes-with-actor
SOURCE src/act_enter.c:do_enter:137
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [2, 0, ["GATE_GOWITH", "GATE_NORMAL_EXIT"], 200, 0], "in_room": "A"}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}}
AND {"get_obj_list": "P", "get_room_index(200)": "B", "can_see_room": true, "room_is_private": false, "act/do_function": "Record delivery boundaries. do_look does not mutate the fixture."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_destination_resolution": [{"act": "$n steps into $p.", "channel": "TO_ROOM", "anchor": "ch", "room": "A"}, {"act": "You enter $p.", "channel": "TO_CHAR", "anchor": "ch"}, {"char_from_room": "ch"}, {"char_to_room": ["ch", "B"]}, {"obj_from_room": "P"}, {"obj_to_room": ["P", "B"]}, {"act": "$n has arrived.", "channel": "TO_ROOM", "anchor": "ch", "room": "B"}, {"do_function": ["ch", "do_look", "auto"], "charge_during_look": 2}, {"set": {"P.value[0]": 1}}], "ch.in_room": "B", "portal_final_state": {"value[0]": 1, "in_room": "B"}, "forbidden": ["follower dispatch", "number_percent"]}
```

## act_enter.do_enter.last-charge-fades-after-look

last charge fades after look

```text
CASE act_enter.do_enter.last-charge-fades-after-look
SOURCE src/act_enter.c:do_enter:137
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [1, 0, [], 200, 0], "in_room": "A"}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}}
AND {"get_obj_list": "P", "get_room_index(200)": "B", "can_see_room": true, "room_is_private": false, "act/do_function": "Record delivery boundaries. do_look does not mutate the fixture."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_destination_resolution": [{"act": "$n steps into $p.", "channel": "TO_ROOM", "anchor": "ch", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "channel": "TO_CHAR", "anchor": "ch"}, {"char_from_room": "ch"}, {"char_to_room": ["ch", "B"]}, {"act": "$n has arrived through $p.", "channel": "TO_ROOM", "anchor": "ch", "room": "B"}, {"do_function": ["ch", "do_look", "auto"], "charge_during_look": 1}, {"set": {"P.value[0]": 0}}, {"set": {"P.value[0]": -1}}, {"act": "$p fades out of existence.", "channel": "TO_CHAR", "anchor": "ch"}, {"extract_obj": "P"}], "ch.in_room": "B", "portal_final_state": "extracted", "forbidden": ["follower dispatch", "number_percent"]}
```

## act_enter.do_enter.standing-follower-reenters-by-keyword

standing follower reenters by keyword

```text
CASE act_enter.do_enter.standing-follower-reenters-by-keyword
SOURCE src/act_enter.c:do_enter:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": [], "position": "POS_STANDING"}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, [], 200, 0], "in_room": "A", "name": "portal", "contains": []}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}, "follower": {"id": "f", "kind": "PC", "master": "ch", "in_room": "A", "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null}, "observer": {"id": "observer", "kind": "PC", "master": null, "position": "POS_STANDING"}}
AND {"room_graph": "Resolve fixed destination B. Both actors can see B. It is not private.", "object_lookup": "Visible keyword lookup in each actor’s current room. P is the only matching item.", "do_look": "Record the automatic look without mutation.", "messages": "Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.", "stand_and_enter": "Use real do_function dispatch and the real do_stand/do_enter paths.", "extraction": "P starts valid at the object-list head with prototype count 1 and no children."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_leader_move_and_look": [{"act": "You follow $N.", "channel": "TO_CHAR", "anchor": "f", "victim": "ch"}, {"do_function": ["f", "do_enter", "portal"]}, {"act": "$n steps into $p.", "channel": "TO_ROOM", "anchor": "f", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "channel": "TO_CHAR", "anchor": "f"}, {"char_from_room": "f"}, {"char_to_room": ["f", "B"]}, {"act": "$n has arrived through $p.", "channel": "TO_ROOM", "anchor": "f", "room": "B"}, {"do_function": ["f", "do_look", "auto"]}], "ch.in_room": "B", "unchanged": ["observer stays in A"], "f.in_room": "B", "P.in_room": "A", "P.value[0]": 0}
```

## act_enter.do_enter.sitting-charmed-follower-stands-before-entry

sitting charmed follower stands before entry

```text
CASE act_enter.do_enter.sitting-charmed-follower-stands-before-entry
SOURCE src/act_enter.c:do_enter:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": [], "position": "POS_STANDING"}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, [], 200, 0], "in_room": "A", "name": "portal", "contains": []}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}, "follower": {"id": "f", "kind": "PC", "master": "ch", "in_room": "A", "fighting": null, "position": "POS_SITTING", "affected_by": ["AFF_CHARM"], "act": [], "on": "bench"}, "observer": {"id": "observer", "kind": "PC", "master": null, "position": "POS_STANDING"}}
AND {"room_graph": "Resolve fixed destination B. Both actors can see B. It is not private.", "object_lookup": "Visible keyword lookup in each actor’s current room. P is the only matching item.", "do_look": "Record the automatic look without mutation.", "messages": "Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.", "stand_and_enter": "Use real do_function dispatch and the real do_stand/do_enter paths.", "extraction": "P starts valid at the object-list head with prototype count 1 and no children."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_leader_move_and_look": [{"do_function": ["f", "do_stand", ""]}, {"send_to_char": "You stand up.\n\r", "recipient": "f"}, {"act": "$n stands up.", "channel": "TO_ROOM", "anchor": "f", "room": "A"}, {"set": {"f.position": "POS_STANDING", "f.on": null}}, {"act": "You follow $N.", "channel": "TO_CHAR", "anchor": "f", "victim": "ch"}, {"do_function": ["f", "do_enter", "portal"]}, {"act": "$n steps into $p.", "channel": "TO_ROOM", "anchor": "f", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "channel": "TO_CHAR", "anchor": "f"}, {"char_from_room": "f"}, {"char_to_room": ["f", "B"]}, {"act": "$n has arrived through $p.", "channel": "TO_ROOM", "anchor": "f", "room": "B"}, {"do_function": ["f", "do_look", "auto"]}], "ch.in_room": "B", "unchanged": ["observer stays in A"], "f.in_room": "B", "f.position": "POS_STANDING", "f.on": null, "P.value[0]": 0}
```

## act_enter.do_enter.magical-sleep-prevents-charmed-follower-entry

magical sleep prevents charmed follower entry

```text
CASE act_enter.do_enter.magical-sleep-prevents-charmed-follower-entry
SOURCE src/act_enter.c:do_enter:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": [], "position": "POS_STANDING"}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, [], 200, 0], "in_room": "A", "name": "portal", "contains": []}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}, "follower": {"id": "f", "kind": "PC", "master": "ch", "in_room": "A", "fighting": null, "position": "POS_SLEEPING", "affected_by": ["AFF_CHARM", "AFF_SLEEP"], "act": [], "on": null}, "observer": {"id": "observer", "kind": "PC", "master": null, "position": "POS_STANDING"}}
AND {"room_graph": "Resolve fixed destination B. Both actors can see B. It is not private.", "object_lookup": "Visible keyword lookup in each actor’s current room. P is the only matching item.", "do_look": "Record the automatic look without mutation.", "messages": "Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.", "stand_and_enter": "Use real do_function dispatch and the real do_stand/do_enter paths.", "extraction": "P starts valid at the object-list head with prototype count 1 and no children."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_leader_move_and_look": [{"do_function": ["f", "do_stand", ""]}, {"send_to_char": "You can't wake up!\n\r", "recipient": "f"}], "ch.in_room": "B", "unchanged": ["observer stays in A"], "f.in_room": "A", "f.position": "POS_SLEEPING", "P.value[0]": 0}
```

## act_enter.do_enter.uncharmed-sitting-follower-stays

uncharmed sitting follower stays

```text
CASE act_enter.do_enter.uncharmed-sitting-follower-stays
SOURCE src/act_enter.c:do_enter:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": [], "position": "POS_STANDING"}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, [], 200, 0], "in_room": "A", "name": "portal", "contains": []}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}, "follower": {"id": "f", "kind": "PC", "master": "ch", "in_room": "A", "fighting": null, "position": "POS_SITTING", "affected_by": [], "act": [], "on": null}, "observer": {"id": "observer", "kind": "PC", "master": null, "position": "POS_STANDING"}}
AND {"room_graph": "Resolve fixed destination B. Both actors can see B. It is not private.", "object_lookup": "Visible keyword lookup in each actor’s current room. P is the only matching item.", "do_look": "Record the automatic look without mutation.", "messages": "Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.", "stand_and_enter": "Use real do_function dispatch and the real do_stand/do_enter paths.", "extraction": "P starts valid at the object-list head with prototype count 1 and no children."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_leader_move_and_look": [], "ch.in_room": "B", "unchanged": ["observer stays in A"], "f.in_room": "A", "f.position": "POS_SITTING", "P.value[0]": 0}
```

## act_enter.do_enter.fighting-follower-gets-follow-notice-before-silent-return

fighting follower gets follow notice before silent return

```text
CASE act_enter.do_enter.fighting-follower-gets-follow-notice-before-silent-return
SOURCE src/act_enter.c:do_enter:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": [], "position": "POS_STANDING"}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, [], 200, 0], "in_room": "A", "name": "portal", "contains": []}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}, "follower": {"id": "f", "kind": "PC", "master": "ch", "in_room": "A", "fighting": "observer", "position": "POS_STANDING", "affected_by": [], "act": [], "on": null}, "observer": {"id": "observer", "kind": "PC", "master": null, "position": "POS_STANDING"}}
AND {"room_graph": "Resolve fixed destination B. Both actors can see B. It is not private.", "object_lookup": "Visible keyword lookup in each actor’s current room. P is the only matching item.", "do_look": "Record the automatic look without mutation.", "messages": "Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.", "stand_and_enter": "Use real do_function dispatch and the real do_stand/do_enter paths.", "extraction": "P starts valid at the object-list head with prototype count 1 and no children."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_leader_move_and_look": [{"act": "You follow $N.", "channel": "TO_CHAR", "anchor": "f", "victim": "ch"}, {"do_function": ["f", "do_enter", "portal"]}], "ch.in_room": "B", "unchanged": ["observer stays in A"], "f.in_room": "A", "f.fighting": "observer", "P.value[0]": 0}
```

## act_enter.do_enter.aggressive-npc-follower-denied-by-city

aggressive npc follower denied by city

```text
CASE act_enter.do_enter.aggressive-npc-follower-denied-by-city
SOURCE src/act_enter.c:do_enter:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": [], "position": "POS_STANDING"}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, [], 200, 0], "in_room": "A", "name": "portal", "contains": []}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": ["ROOM_LAW"]}, "follower": {"id": "f", "kind": "NPC", "master": "ch", "in_room": "A", "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": ["ACT_AGGRESSIVE"], "on": null}, "observer": {"id": "observer", "kind": "PC", "master": null, "position": "POS_STANDING"}}
AND {"room_graph": "Resolve fixed destination B. Both actors can see B. It is not private.", "object_lookup": "Visible keyword lookup in each actor’s current room. P is the only matching item.", "do_look": "Record the automatic look without mutation.", "messages": "Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.", "stand_and_enter": "Use real do_function dispatch and the real do_stand/do_enter paths.", "extraction": "P starts valid at the object-list head with prototype count 1 and no children."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_leader_move_and_look": [{"act": "You can't bring $N into the city.", "channel": "TO_CHAR", "anchor": "ch", "victim": "f"}, {"act": "You aren't allowed in the city.", "channel": "TO_CHAR", "anchor": "f"}], "ch.in_room": "B", "unchanged": ["observer stays in A"], "f.in_room": "A", "P.value[0]": 0}
```

## act_enter.do_enter.moved-portal-follower-repeats-lookup-in-old-room

moved portal follower repeats lookup in old room

```text
CASE act_enter.do_enter.moved-portal-follower-repeats-lookup-in-old-room
SOURCE src/act_enter.c:do_enter:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": [], "position": "POS_STANDING"}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, ["GATE_GOWITH"], 200, 0], "in_room": "A", "name": "portal", "contains": []}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}, "follower": {"id": "f", "kind": "PC", "master": "ch", "in_room": "A", "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null}, "observer": {"id": "observer", "kind": "PC", "master": null, "position": "POS_STANDING"}}
AND {"room_graph": "Resolve fixed destination B. Both actors can see B. It is not private.", "object_lookup": "Visible keyword lookup in each actor’s current room. P is the only matching item.", "do_look": "Record the automatic look without mutation.", "messages": "Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.", "stand_and_enter": "Use real do_function dispatch and the real do_stand/do_enter paths.", "extraction": "P starts valid at the object-list head with prototype count 1 and no children."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_leader_move_and_look": [{"act": "You follow $N.", "channel": "TO_CHAR", "anchor": "f", "victim": "ch"}, {"do_function": ["f", "do_enter", "portal"]}, {"send_to_char": "You don't see that here.\n\r", "recipient": "f"}], "ch.in_room": "B", "unchanged": ["observer stays in A"], "f.in_room": "A", "P.in_room": "B", "P.value[0]": 0}
```

## act_enter.do_enter.last-charge-skips-follower-and-notifies-origin

last charge skips follower and notifies origin

```text
CASE act_enter.do_enter.last-charge-skips-follower-and-notifies-origin
SOURCE src/act_enter.c:do_enter:165
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": [], "position": "POS_STANDING"}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [1, 0, [], 200, 0], "in_room": "A", "name": "portal", "contains": []}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}, "follower": {"id": "f", "kind": "PC", "master": "ch", "in_room": "A", "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null}, "observer": {"id": "observer", "kind": "PC", "master": null, "position": "POS_STANDING"}}
AND {"room_graph": "Resolve fixed destination B. Both actors can see B. It is not private.", "object_lookup": "Visible keyword lookup in each actor’s current room. P is the only matching item.", "do_look": "Record the automatic look without mutation.", "messages": "Record send_to_char and act calls with channel and anchor. Only listed events are expected after leader look.", "stand_and_enter": "Use real do_function dispatch and the real do_stand/do_enter paths.", "extraction": "P starts valid at the object-list head with prototype count 1 and no children."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_leader_move_and_look": [{"set": {"P.value[0]": 0}}, {"set": {"P.value[0]": -1}}, {"act": "$p fades out of existence.", "channel": "TO_CHAR", "anchor": "ch"}, {"act": "$p fades out of existence.", "channel": "TO_CHAR", "anchor": "f"}, {"act": "$p fades out of existence.", "channel": "TO_ROOM", "anchor": "f"}, {"extract_obj": "P"}], "ch.in_room": "B", "unchanged": ["observer stays in A"], "f.in_room": "A", "portal_final_state": "removed from A and the world list, prototype count 0"}
```

## act_enter.do_enter.nested-last-charge-leaves-outer-frame-with-recycled-portal

nested last charge leaves outer frame with recycled portal

```text
CASE act_enter.do_enter.nested-last-charge-leaves-outer-frame-with-recycled-portal
SOURCE src/act_enter.c:do_enter:195; src/handler.c:extract_obj:1910; src/recycle.c:free_obj:289; src/db.c:free_string:2716
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": [], "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P"]}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [2, 0, [], 200, 0], "in_room": "A", "name": "portal", "contains": [], "short_descr_storage": "Shared db string space", "short_descr": "a shimmering portal"}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "people": [], "room_flags": []}, "follower": {"id": "f", "kind": "PC", "master": "ch", "position": "POS_STANDING", "in_room": "A", "fighting": null}, "observer": {"id": "observer", "master": null, "position": "POS_STANDING"}, "leader_connection": {"descriptor": "connected", "position": "POS_STANDING"}}
AND {"visibility": "Both actors see B. The connected leader passes act position filtering and can_see_obj for P.", "room_private": false, "look": "No mutation", "object_reuse": "No allocation reuses P after nested extraction.", "object_list": "P starts valid as the only world object, vnum 25, with prototype count 1.", "messages": "Record act calls without expansion. Shared description is preserved by free_string."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": ["Leader moves and looks, then charge 2 becomes 1", "Follower receives follow notice and reenters", "Follower moves and looks, then charge 1 becomes 0 then -1", "Nested fade act calls anchor on f for TO_CHAR, then observer for TO_CHAR and TO_ROOM", "Nested extract_obj removes P from room and world list, decrements prototype count and recycles P", "Outer frame skips observer, then repeats fade act calls anchored on ch and observer", "Outer extract_obj finds no P in the world list and logs Extract_obj: obj 25 not found."], "final": {"ch.in_room": "B", "f.in_room": "B", "observer.in_room": "A", "prototype.count": 0, "portal": "invalid and on recycle list once"}}
```

## act_enter.do_enter.destination-invisible-before-privacy

destination invisible before privacy

```text
CASE act_enter.do_enter.destination-invisible-before-privacy
SOURCE src/act_enter.c:do_enter:113
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, 0, 200, 0], "in_room": "A"}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "room_flags": []}}
AND {"get_obj_list": "P", "get_room_index(200)": "B", "can_see_room": false, "room_is_private": true}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_lookup": [{"act": "$p doesn't seem to go anywhere.", "channel": "TO_CHAR", "anchor": "ch"}], "room_is_private_calls": [], "unchanged": ["ch.in_room", "P.in_room", "P.value[0]"], "forbidden": ["move", "do_look", "extract_obj", "follow dispatch"]}
```

## act_enter.do_enter.private-destination-rejects-trust-59

private destination rejects trust 59

```text
CASE act_enter.do_enter.private-destination-rejects-trust-59
SOURCE src/act_enter.c:do_enter:113
GIVEN {"actor": {"id": "ch", "kind": "PC", "level": 30, "trust": 59, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": []}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, 0, 200, 0], "in_room": "A"}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "room_flags": []}}
AND {"get_obj_list": "P", "get_room_index(200)": "B", "can_see_room": true, "room_is_private": true}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_lookup": [{"act": "$p doesn't seem to go anywhere.", "channel": "TO_CHAR", "anchor": "ch"}], "room_is_private_calls": ["B"], "unchanged": ["ch.in_room", "P.in_room", "P.value[0]"], "forbidden": ["move", "do_look", "extract_obj", "follow dispatch"]}
```

## act_enter.do_enter.aggressive-npc-directly-rejected-by-law

aggressive npc directly rejected by law

```text
CASE act_enter.do_enter.aggressive-npc-directly-rejected-by-law
SOURCE src/act_enter.c:do_enter:113
GIVEN {"actor": {"id": "ch", "kind": "NPC", "level": 30, "trust": 0, "desc": null, "fighting": null, "in_room": "A", "affected_by": [], "act": ["ACT_IS_NPC", "ACT_AGGRESSIVE"]}, "room": {"id": "A", "room_flags": []}, "portal": {"id": "P", "item_type": "ITEM_PORTAL", "value": [0, 0, 0, 200, 0], "in_room": "A"}, "argument": "portal", "destination": {"id": "B", "vnum": 200, "room_flags": ["ROOM_LAW"]}}
AND {"get_obj_list": "P", "get_room_index(200)": "B", "can_see_room": true, "room_is_private": false}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events_after_lookup": [{"send_to_char": "Something prevents you from leaving...\n\r", "recipient": "ch"}], "room_is_private_calls": ["B"], "unchanged": ["ch.in_room", "P.in_room", "P.value[0]"], "forbidden": ["move", "do_look", "extract_obj", "follow dispatch"]}
```

## lookup.flag_lookup.same-initial-failed-prefix-continues

same initial failed prefix continues

```text
CASE lookup.flag_lookup.same-initial-failed-prefix-continues
SOURCE src/lookup.c:flag_lookup:45
GIVEN {"arguments": {"name": "al", "flag_table": [["amber", 2, true], ["alpha", 4, true], [null, 0, false]]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 4, "prefix_comparisons": [["al", "amber"], ["al", "alpha"]], "unchanged": ["table"]}
```

## lookup.flag_lookup.different-initial-skips-prefix-comparison

different initial skips prefix comparison

```text
CASE lookup.flag_lookup.different-initial-skips-prefix-comparison
SOURCE src/lookup.c:flag_lookup:44
GIVEN {"arguments": {"name": "al", "flag_table": [["beta", 2, true], [null, 0, false]]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke flag_lookup with the fixture arguments once.
THEN {"return": 0, "prefix_comparisons": [], "unchanged": ["table"]}
```

## lookup.clan_lookup.same-initial-failed-prefix

same initial failed prefix

```text
CASE lookup.clan_lookup.same-initial-failed-prefix
SOURCE src/lookup.c:clan_lookup:59
GIVEN {"arguments": {"name": "lx"}, "table": "Snapshot tables.c"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke clan_lookup with the fixture arguments once.
THEN {"return": 0, "prefix_comparisons": [["lx", "loner"]], "unchanged": ["table"]}
```

## lookup.position_lookup.same-initial-failed-prefix

same initial failed prefix

```text
CASE lookup.position_lookup.same-initial-failed-prefix
SOURCE src/lookup.c:position_lookup:73
GIVEN {"arguments": {"name": "dx"}, "table": "Snapshot tables.c"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke position_lookup with the fixture arguments once.
THEN {"return": -1, "prefix_comparisons": [["dx", "dead"]], "unchanged": ["table"]}
```

## lookup.sex_lookup.same-initial-failed-prefix

same initial failed prefix

```text
CASE lookup.sex_lookup.same-initial-failed-prefix
SOURCE src/lookup.c:sex_lookup:87
GIVEN {"arguments": {"name": "nx"}, "table": "Snapshot tables.c"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke sex_lookup with the fixture arguments once.
THEN {"return": -1, "prefix_comparisons": [["nx", "none"]], "unchanged": ["table"]}
```

## lookup.size_lookup.same-initial-failed-prefix

same initial failed prefix

```text
CASE lookup.size_lookup.same-initial-failed-prefix
SOURCE src/lookup.c:size_lookup:101
GIVEN {"arguments": {"name": "tx"}, "table": "Snapshot tables.c"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke size_lookup with the fixture arguments once.
THEN {"return": -1, "prefix_comparisons": [["tx", "tiny"]], "unchanged": ["table"]}
```

## scan.do_scan.north-long-with-0-hops

north long with 0 hops

```text
CASE scan.do_scan.north-long-with-0-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "NORTH ignored", "rooms": {"A": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "north"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "north"}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.north-long-with-1-hops

north long with 1 hops

```text
CASE scan.do_scan.north-long-with-1-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "NORTH ignored", "rooms": {"A": {"exit": {"north": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "north"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "north"}, {"scan_list": ["B", "ch", 1, 0]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.north-long-with-2-hops

north long with 2 hops

```text
CASE scan.do_scan.north-long-with-2-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "NORTH ignored", "rooms": {"A": {"exit": {"north": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {"north": {"to_room": "C", "flags": ["EX_CLOSED"]}}}, "C": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "north"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "north"}, {"scan_list": ["B", "ch", 1, 0]}, {"scan_list": ["C", "ch", 2, 0]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.east-long-with-0-hops

east long with 0 hops

```text
CASE scan.do_scan.east-long-with-0-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "EAST ignored", "rooms": {"A": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "east"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "east"}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.east-long-with-1-hops

east long with 1 hops

```text
CASE scan.do_scan.east-long-with-1-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "EAST ignored", "rooms": {"A": {"exit": {"east": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "east"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "east"}, {"scan_list": ["B", "ch", 1, 1]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.east-long-with-2-hops

east long with 2 hops

```text
CASE scan.do_scan.east-long-with-2-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "EAST ignored", "rooms": {"A": {"exit": {"east": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {"east": {"to_room": "C", "flags": ["EX_CLOSED"]}}}, "C": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "east"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "east"}, {"scan_list": ["B", "ch", 1, 1]}, {"scan_list": ["C", "ch", 2, 1]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.south-long-with-0-hops

south long with 0 hops

```text
CASE scan.do_scan.south-long-with-0-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "SOUTH ignored", "rooms": {"A": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "south"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "south"}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.south-long-with-1-hops

south long with 1 hops

```text
CASE scan.do_scan.south-long-with-1-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "SOUTH ignored", "rooms": {"A": {"exit": {"south": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "south"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "south"}, {"scan_list": ["B", "ch", 1, 2]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.south-long-with-2-hops

south long with 2 hops

```text
CASE scan.do_scan.south-long-with-2-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "SOUTH ignored", "rooms": {"A": {"exit": {"south": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {"south": {"to_room": "C", "flags": ["EX_CLOSED"]}}}, "C": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "south"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "south"}, {"scan_list": ["B", "ch", 1, 2]}, {"scan_list": ["C", "ch", 2, 2]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.west-long-with-0-hops

west long with 0 hops

```text
CASE scan.do_scan.west-long-with-0-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "WEST ignored", "rooms": {"A": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "west"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "west"}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.west-long-with-1-hops

west long with 1 hops

```text
CASE scan.do_scan.west-long-with-1-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "WEST ignored", "rooms": {"A": {"exit": {"west": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "west"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "west"}, {"scan_list": ["B", "ch", 1, 3]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.west-long-with-2-hops

west long with 2 hops

```text
CASE scan.do_scan.west-long-with-2-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "WEST ignored", "rooms": {"A": {"exit": {"west": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {"west": {"to_room": "C", "flags": ["EX_CLOSED"]}}}, "C": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "west"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "west"}, {"scan_list": ["B", "ch", 1, 3]}, {"scan_list": ["C", "ch", 2, 3]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.up-long-with-0-hops

up long with 0 hops

```text
CASE scan.do_scan.up-long-with-0-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "UP ignored", "rooms": {"A": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "up"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "up"}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.up-long-with-1-hops

up long with 1 hops

```text
CASE scan.do_scan.up-long-with-1-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "UP ignored", "rooms": {"A": {"exit": {"up": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "up"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "up"}, {"scan_list": ["B", "ch", 1, 4]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.up-long-with-2-hops

up long with 2 hops

```text
CASE scan.do_scan.up-long-with-2-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "UP ignored", "rooms": {"A": {"exit": {"up": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {"up": {"to_room": "C", "flags": ["EX_CLOSED"]}}}, "C": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "up"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "up"}, {"scan_list": ["B", "ch", 1, 4]}, {"scan_list": ["C", "ch", 2, 4]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.down-long-with-0-hops

down long with 0 hops

```text
CASE scan.do_scan.down-long-with-0-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "DOWN ignored", "rooms": {"A": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "down"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "down"}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.down-long-with-1-hops

down long with 1 hops

```text
CASE scan.do_scan.down-long-with-1-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "DOWN ignored", "rooms": {"A": {"exit": {"down": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "down"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "down"}, {"scan_list": ["B", "ch", 1, 5]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.down-long-with-2-hops

down long with 2 hops

```text
CASE scan.do_scan.down-long-with-2-hops
SOURCE src/scan.c:do_scan:85
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "DOWN ignored", "rooms": {"A": {"exit": {"down": {"to_room": "B", "flags": ["EX_CLOSED"]}}}, "B": {"exit": {"down": {"to_room": "C", "flags": ["EX_CLOSED"]}}}, "C": {"exit": {}}}}
AND {"scan_list": "Record helper calls without rendering occupants."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "You peer intently $T.", "channel": "TO_CHAR", "arg2": "down"}, {"act": "$n peers intently $T.", "channel": "TO_ROOM", "arg2": "down"}, {"scan_list": ["B", "ch", 1, 5]}, {"scan_list": ["C", "ch", 2, 5]}], "unchanged": ["room membership", "exits"], "forbidden": ["send formatted direction header", "inspect other directions", "random draws"]}
```

## scan.do_scan.null-exit-destination-fails-next-iteration

null exit destination fails next iteration

```text
CASE scan.do_scan.null-exit-destination-fails-next-iteration
SOURCE src/scan.c:do_scan:87
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "n", "rooms": {"A": {"exit": {"north": {"to_room": null}}}}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"defined_prefix": ["Emit directional acts", "Call scan_list(NULL, ch, 1, 0), which returns immediately"], "portable_oracle": "Unavailable after first hop. Depth two reads exit through a null scan_room."}
```

Open questions: The fixture tests a malformed exit. Establish loader invariants before treating this path as reachable in a loaded world.

## scan.scan_char.pers-rechecks-visibility

pers rechecks visibility

```text
CASE scan.scan_char.pers-rechecks-visibility
SOURCE src/scan.c:scan_char:119
GIVEN {"arguments": {"victim": "v", "ch": "ch", "depth": 1, "door": 0}, "victim": {"kind": "NPC", "short_descr": "a guard"}}
AND {"can_see": {"ordered_returns": [false]}, "PERS": "Evaluate the real macro."}
WHEN Invoke scan_char with the fixture arguments once.
THEN {"ordered_events": [{"can_see": ["ch", "v"]}, {"send_to_char": "someone, nearby to the north.\n\r", "recipient": "ch"}]}
```

## scan.scan_char.pers-visible-npc

pers visible npc

```text
CASE scan.scan_char.pers-visible-npc
SOURCE src/scan.c:scan_char:119
GIVEN {"arguments": {"victim": "v", "ch": "ch", "depth": 0, "door": 0}, "victim": {"kind": "NPC", "name": "guard", "short_descr": "a guard"}}
AND {"can_see": {"ordered_returns": [true]}, "PERS": "Evaluate the real macro."}
WHEN Invoke scan_char with the fixture arguments once.
THEN {"ordered_events": [{"can_see": ["ch", "v"]}, {"send_to_char": "a guard, right here.\n\r", "recipient": "ch"}]}
```

## scan.scan_char.pers-visible-pc

pers visible pc

```text
CASE scan.scan_char.pers-visible-pc
SOURCE src/scan.c:scan_char:119
GIVEN {"arguments": {"victim": "v", "ch": "ch", "depth": 0, "door": 0}, "victim": {"kind": "PC", "name": "Mira", "short_descr": "unused"}}
AND {"can_see": {"ordered_returns": [true]}, "PERS": "Evaluate the real macro."}
WHEN Invoke scan_char with the fixture arguments once.
THEN {"ordered_events": [{"can_see": ["ch", "v"]}, {"send_to_char": "Mira, right here.\n\r", "recipient": "ch"}]}
```

## scan.do_scan.around-null-destination-is-safe

around null destination is safe

```text
CASE scan.do_scan.around-null-destination-is-safe
SOURCE src/scan.c:do_scan:67
GIVEN {"actor": {"id": "ch", "in_room": "A"}, "argument": "", "rooms": {"A": {"exit": {"north": {"to_room": null}}, "people_in_list_order": ["ch"]}}}
AND {"scan_list": "Run the helper and record calls."}
WHEN Invoke do_scan with the fixture arguments once.
THEN {"ordered_events": [{"act": "$n looks all around.", "channel": "TO_ROOM"}, {"send_to_char": "Looking around you see:\n\r", "recipient": "ch"}, {"scan_list": ["A", "ch", 0, -1]}, {"scan_list": [null, "ch", 1, 0]}], "forbidden": ["scan_char", "dereference null destination", "movement"]}
```

## special.spec_lookup.first-full

first full

```text
CASE special.spec_lookup.first-full
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_breath_any"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_any", "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"], "loop_guard_indices_in_order": [0], "first_character_comparisons_in_order": [0], "str_prefix_table_indices_in_order": [0], "str_prefix_returns_in_order": [false], "return_pointer_identity": "spec_table[0].function", "unchanged": ["input bytes", "table", "all caller and world state"]}
```

## special.spec_lookup.ambiguous-prefix-first

ambiguous prefix first

```text
CASE special.spec_lookup.ambiguous-prefix-first
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "SPEC_BREATH"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_any", "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"], "loop_guard_indices_in_order": [0], "first_character_comparisons_in_order": [0], "str_prefix_table_indices_in_order": [0], "str_prefix_returns_in_order": [false], "return_pointer_identity": "spec_table[0].function", "unchanged": ["input bytes", "table", "all caller and world state"]}
```

## special.spec_lookup.last-full

last full

```text
CASE special.spec_lookup.last-full
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_patrolman"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_patrolman", "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[21].function", "unchanged": ["input bytes", "table", "all caller and world state"]}
```

## special.spec_lookup.unknown

unknown

```text
CASE special.spec_lookup.unknown
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110
GIVEN {"arguments": {"name": "no_such_special"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [], "str_prefix_returns_in_order": [], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"]}
```

## special.spec_lookup.empty

empty

```text
CASE special.spec_lookup.empty
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110
GIVEN {"arguments": {"name": ""}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [], "str_prefix_returns_in_order": [], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"]}
```

## special.spec_name.first-function

first function

```text
CASE special.spec_name.first-function
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_breath_any"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_breath_any", "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"], "return_pointer": "spec_table[0].name (same pointer, not a copy)", "equality_comparisons_in_order": [0], "loop_guard_indices_in_order": [0], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"]}
```

## special.spec_name.last-function

last function

```text
CASE special.spec_name.last-function
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_patrolman"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_patrolman", "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"], "return_pointer": "spec_table[21].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"]}
```

## special.spec_name.null-function

null function

```text
CASE special.spec_name.null-function
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:123
GIVEN {"arguments": {"function": "C NULL"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "C NULL", "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"], "return_pointer": "C NULL", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"]}
```

## special.spec_name.unregistered-function

unregistered function

```text
CASE special.spec_name.unregistered-function
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:123
GIVEN {"arguments": {"function": "unregistered_valid_function_pointer"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "C NULL", "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"], "return_pointer": "C NULL", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"]}
```

## act_enter.do_enter.grandchild-mutation-revisits-moved-follower

grandchild mutation revisits moved follower

```text
CASE act_enter.do_enter.grandchild-mutation-revisits-moved-follower
SOURCE src/act_enter.c:do_enter:167; src/handler.c:char_from_room:1367; src/handler.c:char_to_room:1395; src/handler.c:get_obj_list:2100
GIVEN {"argument": "portal", "actor": "ch", "rooms": {"A": {"room_flags": [], "light": 1, "owner": "", "sector_type": "SECT_INSIDE", "vnum": 100, "people": ["ch", "f", "g", "observer"], "contents": ["P"], "area": "areaA"}, "B": {"room_flags": [], "light": 1, "owner": "", "sector_type": "SECT_INSIDE", "vnum": 200, "people": [], "contents": [], "area": "areaB"}}, "characters": {"ch": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": null}, "f": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": "ch"}, "g": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": "f"}, "observer": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": null}}, "objects": {"P": {"item_type": "ITEM_PORTAL", "name": "portal", "extra_flags": [], "value": [0, 0, 0, 200, 0], "in_room": "A", "contains": []}}, "areas": {"areaA": {"nplayer": 4, "empty": false, "age": 10}, "areaB": {"nplayer": 0, "empty": false, "age": 10}}}
AND {"lookup": "Execute get_obj_list, number_argument, is_name, one_argument and can_see_obj; all rooms lit. Resolve vnums 100/200/300 to A/B/C. No room is private.", "movement": "Execute char_from_room/char_to_room: unlink and clear next pointer, then prepend to destination people. No lights, plague or equipped objects.", "do_function": "Execute actual dispatcher and recursive do_enter; automatic do_look is a recording boundary without mutation.", "messages": "Record act template, actor, object, target and channel; delivery/rendering are separate pending contracts.", "randomness": "No random calls permitted."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": [{"act": "$n steps into $p.", "actor": "ch", "object": "P", "channel": "TO_ROOM", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "actor": "ch", "object": "P", "channel": "TO_CHAR"}, {"char_from_room": "ch"}, {"char_to_room": ["ch", "B"]}, {"act": "$n has arrived through $p.", "actor": "ch", "object": "P", "channel": "TO_ROOM", "room": "B"}, {"do_function": ["ch", "do_look", "auto"]}, {"act": "You follow $N.", "actor": "f", "victim": "ch", "channel": "TO_CHAR"}, {"do_function": ["f", "do_enter", "portal"]}, {"act": "$n steps into $p.", "actor": "f", "object": "P", "channel": "TO_ROOM", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "actor": "f", "object": "P", "channel": "TO_CHAR"}, {"char_from_room": "f"}, {"char_to_room": ["f", "B"]}, {"act": "$n has arrived through $p.", "actor": "f", "object": "P", "channel": "TO_ROOM", "room": "B"}, {"do_function": ["f", "do_look", "auto"]}, {"act": "You follow $N.", "actor": "g", "victim": "f", "channel": "TO_CHAR"}, {"do_function": ["g", "do_enter", "portal"]}, {"act": "$n steps into $p.", "actor": "g", "object": "P", "channel": "TO_ROOM", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "actor": "g", "object": "P", "channel": "TO_CHAR"}, {"char_from_room": "g"}, {"char_to_room": ["g", "B"]}, {"act": "$n has arrived through $p.", "actor": "g", "object": "P", "channel": "TO_ROOM", "room": "B"}, {"do_function": ["g", "do_look", "auto"]}, {"act": "You follow $N.", "actor": "f", "victim": "ch", "channel": "TO_CHAR"}, {"do_function": ["f", "do_enter", "portal"]}, {"send_to_char": "You don't see that here.\n\r", "recipient": "f"}], "outer_loop_visited_ids": ["f", "g", "f", "ch"], "explanation": "Outer cached next is g. Recursive f moves g; g.next_in_room becomes f in B. Returning outer frame resumes g and follows its new link to f, then ch.", "final_people": {"A": ["observer"], "B": ["g", "f", "ch"]}, "final_area_nplayer": {"areaA": 1, "areaB": 3}, "unchanged": ["room light", "area ages and empty flags", "P remains in A with zero unlimited charges", "master pointers"], "forbidden": ["portal extraction", "extra movement after g enters B", "do_stand", "random draws"]}
```

## act_enter.do_enter.moved-gate-exposes-nonportal-name-match

moved gate exposes nonportal name match

```text
CASE act_enter.do_enter.moved-gate-exposes-nonportal-name-match
SOURCE src/act_enter.c:do_enter:80; src/handler.c:get_obj_list:2096; src/handler.c:is_name:809; src/interp.c:number_argument:663
GIVEN {"argument": "portal", "actor": "ch", "characters": {"ch": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": null}, "f": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": "ch"}, "observer": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": null}}, "rooms": {"A": {"room_flags": [], "light": 1, "owner": "", "sector_type": "SECT_INSIDE", "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["P", "Q"], "area": "areaA"}, "B": {"room_flags": [], "light": 1, "owner": "", "sector_type": "SECT_INSIDE", "vnum": 200, "people": [], "contents": [], "area": "areaB"}}, "areas": {"areaA": {"nplayer": 3, "empty": false, "age": 10}, "areaB": {"nplayer": 0, "empty": false, "age": 10}}, "objects": {"P": {"item_type": "ITEM_PORTAL", "name": "portal", "extra_flags": [], "value": [0, 0, ["GATE_GOWITH"], 200, 0], "in_room": "A", "contains": []}, "Q": {"item_type": "ITEM_WEAPON", "name": "portal", "extra_flags": [], "value": [0, 0, 0, 200, 0], "in_room": "A", "contains": []}}}
AND {"lookup": "Execute get_obj_list, number_argument, is_name, one_argument and can_see_obj; all rooms lit. Resolve vnums 100/200/300 to A/B/C. No room is private.", "movement": "Execute char_from_room/char_to_room: unlink and clear next pointer, then prepend to destination people. No lights, plague or equipped objects.", "do_function": "Execute actual dispatcher and recursive do_enter; automatic do_look is a recording boundary without mutation.", "messages": "Record act template, actor, object, target and channel; delivery/rendering are separate pending contracts.", "randomness": "No random calls permitted."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": [{"act": "$n steps into $p.", "actor": "ch", "object": "P", "channel": "TO_ROOM", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "actor": "ch", "object": "P", "channel": "TO_CHAR"}, {"char_from_room": "ch"}, {"char_to_room": ["ch", "B"]}, {"obj_from_room": "P"}, {"obj_to_room": ["P", "B"]}, {"act": "$n has arrived through $p.", "actor": "ch", "object": "P", "channel": "TO_ROOM", "room": "B"}, {"do_function": ["ch", "do_look", "auto"]}, {"act": "You follow $N.", "actor": "f", "victim": "ch", "channel": "TO_CHAR"}, {"do_function": ["f", "do_enter", "portal"]}, {"send_to_char": "You can't seem to find a way in.\n\r", "recipient": "f"}], "lookup_results_in_order": ["P", "Q"], "final_people": {"A": ["f", "observer"], "B": ["ch"]}, "final_contents": {"A": ["Q"], "B": ["P"]}, "final_area_nplayer": {"areaA": 2, "areaB": 1}, "unchanged": ["both charge fields remain zero", "master pointers", "Q location", "room light"], "forbidden": ["follower movement", "portal extraction", "random draws"]}
```

## act_enter.do_enter.ordinal-repeated-after-gate-moves

ordinal repeated after gate moves

```text
CASE act_enter.do_enter.ordinal-repeated-after-gate-moves
SOURCE src/act_enter.c:do_enter:80; src/handler.c:get_obj_list:2096; src/handler.c:is_name:809; src/interp.c:number_argument:663
GIVEN {"argument": "2.portal", "actor": "ch", "characters": {"ch": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": null}, "f": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": "ch"}, "observer": {"kind": "PC", "level": 30, "trust": 0, "desc": null, "fighting": null, "position": "POS_STANDING", "affected_by": [], "act": [], "on": null, "equipment": [], "in_room": "A", "master": null}}, "rooms": {"A": {"room_flags": [], "light": 1, "owner": "", "sector_type": "SECT_INSIDE", "vnum": 100, "people": ["ch", "f", "observer"], "contents": ["Q", "P"], "area": "areaA"}, "B": {"room_flags": [], "light": 1, "owner": "", "sector_type": "SECT_INSIDE", "vnum": 200, "people": [], "contents": [], "area": "areaB"}}, "areas": {"areaA": {"nplayer": 3, "empty": false, "age": 10}, "areaB": {"nplayer": 0, "empty": false, "age": 10}}, "objects": {"P": {"item_type": "ITEM_PORTAL", "name": "portal", "extra_flags": [], "value": [0, 0, ["GATE_GOWITH"], 200, 0], "in_room": "A", "contains": []}, "Q": {"item_type": "ITEM_PORTAL", "name": "portal", "extra_flags": [], "value": [0, 0, 0, 200, 0], "in_room": "A", "contains": []}}}
AND {"lookup": "Execute get_obj_list, number_argument, is_name, one_argument and can_see_obj; all rooms lit. Resolve vnums 100/200/300 to A/B/C. No room is private.", "movement": "Execute char_from_room/char_to_room: unlink and clear next pointer, then prepend to destination people. No lights, plague or equipped objects.", "do_function": "Execute actual dispatcher and recursive do_enter; automatic do_look is a recording boundary without mutation.", "messages": "Record act template, actor, object, target and channel; delivery/rendering are separate pending contracts.", "randomness": "No random calls permitted."}
WHEN Invoke do_enter with the fixture arguments once.
THEN {"ordered_events": [{"act": "$n steps into $p.", "actor": "ch", "object": "P", "channel": "TO_ROOM", "room": "A"}, {"act": "You walk through $p and find yourself somewhere else...", "actor": "ch", "object": "P", "channel": "TO_CHAR"}, {"char_from_room": "ch"}, {"char_to_room": ["ch", "B"]}, {"obj_from_room": "P"}, {"obj_to_room": ["P", "B"]}, {"act": "$n has arrived through $p.", "actor": "ch", "object": "P", "channel": "TO_ROOM", "room": "B"}, {"do_function": ["ch", "do_look", "auto"]}, {"act": "You follow $N.", "actor": "f", "victim": "ch", "channel": "TO_CHAR"}, {"do_function": ["f", "do_enter", "2.portal"]}, {"send_to_char": "You don't see that here.\n\r", "recipient": "f"}], "lookup_results_in_order": ["P", null], "final_people": {"A": ["f", "observer"], "B": ["ch"]}, "final_contents": {"A": ["Q"], "B": ["P"]}, "final_area_nplayer": {"areaA": 2, "areaB": 1}, "unchanged": ["both charge fields remain zero", "master pointers", "Q location", "room light"], "forbidden": ["follower movement", "portal extraction", "random draws"]}
```

## handler.get_trust.descriptor-without-original

descriptor without original

```text
CASE handler.get_trust.descriptor-without-original
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "PC", "level": 20, "trust": 0, "desc": {"original": null}}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 20, "unchanged": ["actor, original and descriptor"]}
```

## handler.get_trust.negative-trust-is-explicit

negative trust is explicit

```text
CASE handler.get_trust.negative-trust-is-explicit
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "PC", "level": 20, "trust": -1, "desc": null}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": -1, "unchanged": ["actor, original and descriptor"]}
```

## handler.get_trust.switched-original-trust-wins

switched original trust wins

```text
CASE handler.get_trust.switched-original-trust-wins
SOURCE src/handler.c:get_trust:708
GIVEN {"actor": {"kind": "NPC", "level": 60, "trust": 60, "desc": {"original": {"kind": "PC", "level": 20, "trust": 55}}}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke get_trust with the fixture arguments once.
THEN {"return": 55, "unchanged": ["actor, original and descriptor"]}
```

## handler.room_is_private.private-zero

private zero

```text
CASE handler.room_is_private.private-zero
SOURCE src/handler.c:room_is_private:2396
GIVEN {"room": {"owner": "", "room_flags": ["ROOM_PRIVATE"], "people": []}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": false, "unchanged": ["room and occupants"]}
```

## handler.room_is_private.private-and-solitary-one

private and solitary one

```text
CASE handler.room_is_private.private-and-solitary-one
SOURCE src/handler.c:room_is_private:2396
GIVEN {"room": {"owner": "", "room_flags": ["ROOM_PRIVATE", "ROOM_SOLITARY"], "people": ["p"]}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke room_is_private with the fixture arguments once.
THEN {"return": true, "unchanged": ["room and occupants"]}
```

## interp.one_argument.whitespace-only

whitespace only

```text
CASE interp.one_argument.whitespace-only
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": " \t\r\n", "arg_first": "256-byte writable output buffer"}, "locale": "C locale, ASCII input"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "", "returned_remainder": "", "unchanged": ["input bytes"], "forbidden": ["messages", "random draws"]}
```

## interp.one_argument.tab-leading

tab leading

```text
CASE interp.one_argument.tab-leading
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "\tLOOK north", "arg_first": "256-byte writable output buffer"}, "locale": "C locale, ASCII input"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "look", "returned_remainder": "north", "unchanged": ["input bytes"], "forbidden": ["messages", "random draws"]}
```

## interp.one_argument.quote-followed-without-space

quote followed without space

```text
CASE interp.one_argument.quote-followed-without-space
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "'LOOK'north", "arg_first": "256-byte writable output buffer"}, "locale": "C locale, ASCII input"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "look", "returned_remainder": "north", "unchanged": ["input bytes"], "forbidden": ["messages", "random draws"]}
```

## interp.one_argument.embedded-quote-unquoted

embedded quote unquoted

```text
CASE interp.one_argument.embedded-quote-unquoted
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "ab\"cd tail", "arg_first": "256-byte writable output buffer"}, "locale": "C locale, ASCII input"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "ab\"cd", "returned_remainder": "tail", "unchanged": ["input bytes"], "forbidden": ["messages", "random draws"]}
```

## interp.one_argument.quoted-tab-preserved

quoted tab preserved

```text
CASE interp.one_argument.quoted-tab-preserved
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "\"a\tb\" tail", "arg_first": "256-byte writable output buffer"}, "locale": "C locale, ASCII input"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "a\tb", "returned_remainder": "tail", "unchanged": ["input bytes"], "forbidden": ["messages", "random draws"]}
```

## interp.one_argument.one-character-token

one character token

```text
CASE interp.one_argument.one-character-token
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "A", "arg_first": "256-byte writable output buffer"}, "locale": "C locale, ASCII input"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "a", "returned_remainder": "", "unchanged": ["input bytes"], "forbidden": ["messages", "random draws"]}
```

## interp.one_argument.max-fitting-token

max fitting token

```text
CASE interp.one_argument.max-fitting-token
SOURCE src/interp.c:one_argument:721
GIVEN {"arguments": {"argument": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "arg_first": "256-byte writable output buffer"}, "locale": "C locale, ASCII input"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"output_token": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "returned_remainder": "", "unchanged": ["input bytes"], "forbidden": ["messages", "random draws"]}
```

## interp.one_argument.output-buffer-overflow

output buffer overflow

```text
CASE interp.one_argument.output-buffer-overflow
SOURCE src/interp.c:one_argument:736
GIVEN {"arguments": {"argument": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "arg_first": "256-byte writable output buffer"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke one_argument with the fixture arguments once.
THEN {"limitation": "Terminating NUL writes index 256 out of bounds; no portable return."}
```

Open questions: No capacity argument exists; callers must provide token length plus one bytes.

## magic.saves_spell.nonmana-pc

nonmana pc

```text
CASE magic.saves_spell.nonmana-pc
SOURCE src/magic.c:saves_spell:220
GIVEN {"arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "victim": {"kind": "PC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false}}
AND {"check_immune": {"returns": "IS_NORMAL", "kind": "recorded helper boundary"}, "number_percent": {"ordered_returns": [49]}, "class_table": "Explicit class_fMana fixture where accessed."}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 50, "number_percent_calls": 1, "unchanged": ["victim"], "forbidden": []}
```

## magic.saves_spell.npc-does-not-index-class

npc does not index class

```text
CASE magic.saves_spell.npc-does-not-index-class
SOURCE src/magic.c:saves_spell:220
GIVEN {"arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "victim": {"kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false, "class": -1}}
AND {"check_immune": {"returns": "IS_NORMAL", "kind": "recorded helper boundary"}, "number_percent": {"ordered_returns": [49]}, "class_table": "Explicit class_fMana fixture where accessed."}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 50, "number_percent_calls": 1, "unchanged": ["victim"], "forbidden": ["class_table access"]}
```

## magic.saves_spell.berserk-odd-level-truncation

berserk odd level truncation

```text
CASE magic.saves_spell.berserk-odd-level-truncation
SOURCE src/magic.c:saves_spell:220
GIVEN {"arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "victim": {"kind": "NPC", "level": 21, "saving_throw": 0, "affected_by": ["AFF_BERSERK"], "class_fMana": false}}
AND {"check_immune": {"returns": "IS_NORMAL", "kind": "recorded helper boundary"}, "number_percent": {"ordered_returns": [64]}, "class_table": "Explicit class_fMana fixture where accessed."}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 65, "number_percent_calls": 1, "unchanged": ["victim"], "forbidden": []}
```

## magic.saves_spell.vulnerable-below

vulnerable below

```text
CASE magic.saves_spell.vulnerable-below
SOURCE src/magic.c:saves_spell:220
GIVEN {"arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "victim": {"kind": "NPC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false}}
AND {"check_immune": {"returns": "IS_VULNERABLE", "kind": "recorded helper boundary"}, "number_percent": {"ordered_returns": [47]}, "class_table": "Explicit class_fMana fixture where accessed."}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 48, "number_percent_calls": 1, "unchanged": ["victim"], "forbidden": []}
```

## magic.saves_spell.mana-before-upper-clamp

mana before upper clamp

```text
CASE magic.saves_spell.mana-before-upper-clamp
SOURCE src/magic.c:saves_spell:220
GIVEN {"arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "victim": {"kind": "PC", "level": 20, "saving_throw": -25, "affected_by": [], "class_fMana": true}}
AND {"check_immune": {"returns": "IS_NORMAL", "kind": "recorded helper boundary"}, "number_percent": {"ordered_returns": [90]}, "class_table": "Explicit class_fMana fixture where accessed."}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": false, "threshold_after_clamp": 90, "number_percent_calls": 1, "unchanged": ["victim"], "forbidden": []}
```

## magic.saves_spell.mana-negative-before-lower-clamp

mana negative before lower clamp

```text
CASE magic.saves_spell.mana-negative-before-lower-clamp
SOURCE src/magic.c:saves_spell:220
GIVEN {"arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "victim": {"kind": "PC", "level": 20, "saving_throw": 26, "affected_by": [], "class_fMana": true}}
AND {"check_immune": {"returns": "IS_NORMAL", "kind": "recorded helper boundary"}, "number_percent": {"ordered_returns": [4]}, "class_table": "Explicit class_fMana fixture where accessed."}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 5, "number_percent_calls": 1, "unchanged": ["victim"], "forbidden": []}
```

## magic.saves_spell.upper-cap-last-success

upper cap last success

```text
CASE magic.saves_spell.upper-cap-last-success
SOURCE src/magic.c:saves_spell:220
GIVEN {"arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "victim": {"kind": "NPC", "level": 20, "saving_throw": -100, "affected_by": [], "class_fMana": false}}
AND {"check_immune": {"returns": "IS_NORMAL", "kind": "recorded helper boundary"}, "number_percent": {"ordered_returns": [94]}, "class_table": "Explicit class_fMana fixture where accessed."}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": 95, "number_percent_calls": 1, "unchanged": ["victim"], "forbidden": []}
```

## magic.saves_spell.immune-skips-invalid-class

immune skips invalid class

```text
CASE magic.saves_spell.immune-skips-invalid-class
SOURCE src/magic.c:saves_spell:220
GIVEN {"arguments": {"level": 20, "dam_type": "DAM_FIRE"}, "victim": {"kind": "PC", "level": 20, "saving_throw": 0, "affected_by": [], "class_fMana": false, "class": -1}}
AND {"check_immune": {"returns": "IS_IMMUNE", "kind": "recorded helper boundary"}, "number_percent": {"ordered_returns": []}, "class_table": "Explicit class_fMana fixture where accessed."}
WHEN Invoke saves_spell with the fixture arguments once.
THEN {"return": true, "threshold_after_clamp": null, "number_percent_calls": 0, "unchanged": ["victim"], "forbidden": ["class_table access"]}
```

## flags.do_flag.aff-field

aff field

```text
CASE flags.do_flag.aff-field
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob aff + blind", "victim": {"id": "bob", "kind": "PC", "zone": "zone-A", "all_flag_fields": 0, "act": 0}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.affected_by": 1, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.immunity-field

immunity field

```text
CASE flags.do_flag.immunity-field
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob immunity + fire", "victim": {"id": "bob", "kind": "PC", "zone": "zone-A", "all_flag_fields": 0, "act": 0}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.imm_flags": 128, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.resist-field

resist field

```text
CASE flags.do_flag.resist-field
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob resist + fire", "victim": {"id": "bob", "kind": "PC", "zone": "zone-A", "all_flag_fields": 0, "act": 0}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.res_flags": 128, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.vuln-field

vuln field

```text
CASE flags.do_flag.vuln-field
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob vuln + fire", "victim": {"id": "bob", "kind": "PC", "zone": "zone-A", "all_flag_fields": 0, "act": 0}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.vuln_flags": 128, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.form-field

form field

```text
CASE flags.do_flag.form-field
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob form + edible", "victim": {"id": "bob", "kind": "NPC", "zone": "zone-A", "all_flag_fields": 0, "act": 1}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.form": 1, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.parts-field

parts field

```text
CASE flags.do_flag.parts-field
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob parts + head", "victim": {"id": "bob", "kind": "NPC", "zone": "zone-A", "all_flag_fields": 0, "act": 1}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.parts": 1, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.comm-field

comm field

```text
CASE flags.do_flag.comm-field
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob comm + quiet", "victim": {"id": "bob", "kind": "PC", "zone": "zone-A", "all_flag_fields": 0, "act": 0}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.comm": 1, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.plr-field

plr field

```text
CASE flags.do_flag.plr-field
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob plr + permit", "victim": {"id": "bob", "kind": "PC", "zone": "zone-A", "all_flag_fields": 0, "act": 0}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.act": 1048576, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.ambiguous-a-selects-act

ambiguous a selects act

```text
CASE flags.do_flag.ambiguous-a-selects-act
SOURCE src/flags.c:do_flag:191
GIVEN {"actor": {"id": "admin", "kind": "PC", "level": 1, "trust": 0}, "argument": "char bob a + sentinel", "victim": {"id": "bob", "kind": "NPC", "zone": "zone-A", "all_flag_fields": 0, "act": 1}, "tables": "Unmodified src/tables.c flag tables."}
AND {"get_char_world": "Returns bob; world lookup is a recording boundary.", "flag_lookup": "Use real table lookup."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"result": {"bob.act": 3, "bob.zone": null}, "unchanged": ["all unselected flag fields", "actor"], "forbidden": ["messages", "trust check", "persistence"]}
```

## flags.do_flag.operator-attached-consumes-word

operator attached consumes word

```text
CASE flags.do_flag.operator-attached-consumes-word
SOURCE src/flags.c:do_flag:58
GIVEN {"argument": "mob bob act +sentinel", "actor": {"id": "admin"}, "victim": {"id": "bob", "act": 1, "zone": "zone-A"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke do_flag with the fixture arguments once.
THEN {"messages": [{"recipient": "admin", "text": "Which flags do you wish to change?\n\r"}], "unchanged": ["bob.act", "bob.zone"], "forbidden": ["get_char_world"]}
```

## alias.substitute_alias.loaded-uppercase-not-substituted

loaded uppercase not substituted

```text
CASE alias.substitute_alias.loaded-uppercase-not-substituted
SOURCE src/alias.c:substitute_alias:78; src/save.c:fread_char:784
GIVEN {"argument": "X", "descriptor": {"character": "ch", "original": null}, "actor": {"id": "ch", "kind": "PC", "prefix": "", "desc": "descriptor", "aliases": [["X", "look"]]}, "storage": "Remaining four slots NULL. A saved Alias X look~ record is loaded without normalizing X."}
AND {"interpret": "Recording boundary.", "string_helpers": "Real ASCII parsing and comparison."}
WHEN Invoke substitute_alias with the fixture arguments once.
THEN {"interpret": {"actor": "ch", "argument": "X"}, "unchanged": ["aliases"]}
```

## alias.do_alias.loaded-uppercase-query-found

loaded uppercase query found

```text
CASE alias.do_alias.loaded-uppercase-query-found
SOURCE src/alias.c:do_alias:160; src/save.c:fread_char:784
GIVEN {"argument": "X", "descriptor": {"character": "ch", "original": null}, "actor": {"id": "ch", "kind": "PC", "prefix": "", "desc": "descriptor", "aliases": [["X", "look"]]}, "storage": "Remaining four slots NULL. A saved Alias X look~ record is loaded without normalizing X."}
AND {"interpret": "Recording boundary.", "string_helpers": "Real ASCII parsing and comparison."}
WHEN Invoke do_alias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "X aliases to 'look'.\n\r"}], "unchanged": ["aliases"]}
```

## alias.do_unalias.loaded-uppercase-not-removed

loaded uppercase not removed

```text
CASE alias.do_unalias.loaded-uppercase-not-removed
SOURCE src/alias.c:do_unalias:245; src/save.c:fread_char:784
GIVEN {"argument": "X", "descriptor": {"character": "ch", "original": null}, "actor": {"id": "ch", "kind": "PC", "prefix": "", "desc": "descriptor", "aliases": [["X", "look"]]}, "storage": "Remaining four slots NULL. A saved Alias X look~ record is loaded without normalizing X."}
AND {"interpret": "Recording boundary.", "string_helpers": "Real ASCII parsing and comparison."}
WHEN Invoke do_unalias with the fixture arguments once.
THEN {"messages": [{"recipient": "ch", "text": "No alias of that name to remove.\n\r"}], "unchanged": ["aliases"]}
```

## db.str_infix.first-character-match-rest-mismatch

first character match rest mismatch

```text
CASE db.str_infix.first-character-match-rest-mismatch
SOURCE src/db.c:str_infix:3201
GIVEN {"arguments": {"astr": "ab", "bstr": "ac"}}
AND {"str_prefix": "Execute real helper; record candidate arguments."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": true, "ordered_str_prefix_candidates": ["ac"], "unchanged": ["input strings"], "forbidden": ["output", "random draws"]}
```

## db.str_infix.retry-after-partial-match

retry after partial match

```text
CASE db.str_infix.retry-after-partial-match
SOURCE src/db.c:str_infix:3201
GIVEN {"arguments": {"astr": "ab", "bstr": "acab"}}
AND {"str_prefix": "Execute real helper; record candidate arguments."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": false, "ordered_str_prefix_candidates": ["acab", "ab"], "unchanged": ["input strings"], "forbidden": ["output", "random draws"]}
```

## db.str_infix.one-character

one character

```text
CASE db.str_infix.one-character
SOURCE src/db.c:str_infix:3201
GIVEN {"arguments": {"astr": "a", "bstr": "A"}}
AND {"str_prefix": "Execute real helper; record candidate arguments."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": false, "ordered_str_prefix_candidates": ["A"], "unchanged": ["input strings"], "forbidden": ["output", "random draws"]}
```

## db.str_infix.empty-both

empty both

```text
CASE db.str_infix.empty-both
SOURCE src/db.c:str_infix:3201
GIVEN {"arguments": {"astr": "", "bstr": ""}}
AND {"str_prefix": "Execute real helper; record candidate arguments."}
WHEN Invoke str_infix with the fixture arguments once.
THEN {"return": false, "ordered_str_prefix_candidates": [], "unchanged": ["input strings"], "forbidden": ["output", "random draws"]}
```

## db.capitalize.shared-buffer-overwritten

shared buffer overwritten

```text
CASE db.capitalize.shared-buffer-overwritten
SOURCE src/db.c:capitalize:3243
GIVEN {"first_input": "HELLO", "second_input": "x"}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Call capitalize("HELLO"), retain its pointer, then call capitalize("x").
THEN {"ordered_results": ["Hello", "X"], "pointer_identity": "Both returns identify the same static array.", "first_pointer_after_second_call": "X", "unchanged": ["both input arrays"]}
```

## db.capitalize.maximum-fitting-input

maximum fitting input

```text
CASE db.capitalize.maximum-fitting-input
SOURCE src/db.c:capitalize:3247
GIVEN {"arguments": {"str": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke capitalize with the fixture arguments once.
THEN {"result_string": "Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "terminator_index": 4607}
```

## db.capitalize.static-buffer-overflow

static buffer overflow

```text
CASE db.capitalize.static-buffer-overflow
SOURCE src/db.c:capitalize:3248
GIVEN {"arguments": {"str": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}
AND {"randomness": "No random calls on this path.", "collaborators": "Record output and mutations; no actor/target state beyond the specified dependency contract affects this path."}
WHEN Invoke capitalize with the fixture arguments once.
THEN {"limitation": "The terminating NUL is written beyond the 4608-byte static array; no portable result."}
```

Open questions: Undefined out-of-bounds write. A target length policy needs a separate decision.

## db.number_range.zero-lower-nonzero-upper

zero lower nonzero upper

```text
CASE db.number_range.zero-lower-nonzero-upper
SOURCE src/db.c:number_range:2965
GIVEN {"arguments": {"from": 0, "to": 1}}
AND {"number_mm": {"kind": "entropy boundary", "ordered_returns": [1]}}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 1, "ordered_consumed_draws": [1], "number_mm_calls": 1}
```

## db.number_range.power-loop-zero-iterations

power loop zero iterations

```text
CASE db.number_range.power-loop-zero-iterations
SOURCE src/db.c:number_range:2965
GIVEN {"arguments": {"from": 5, "to": 6}}
AND {"number_mm": {"kind": "entropy boundary", "ordered_returns": [2]}}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 5, "ordered_consumed_draws": [2], "number_mm_calls": 1}
```

## db.number_range.exact-power-domain

exact power domain

```text
CASE db.number_range.exact-power-domain
SOURCE src/db.c:number_range:2965
GIVEN {"arguments": {"from": 1, "to": 4}}
AND {"number_mm": {"kind": "entropy boundary", "ordered_returns": [3]}}
WHEN Invoke number_range with the fixture arguments once.
THEN {"return": 4, "ordered_consumed_draws": [3], "number_mm_calls": 1}
```

## db.dice.negative-size

negative size

```text
CASE db.dice.negative-size
SOURCE src/db.c:dice:3095
GIVEN {"arguments": {"number": 2, "size": -3}}
AND {"number_range": "Run real helper: reversed domain returns 1 without entropy."}
WHEN Invoke dice with the fixture arguments once.
THEN {"return": 2, "ordered_number_range_calls": [[1, -3], [1, -3]], "number_mm_calls": 0}
```

## db.number_bits.invalid-shift--1

invalid shift  1

```text
CASE db.number_bits.invalid-shift--1
SOURCE src/db.c:number_bits:3006
GIVEN {"arguments": {"width": -1}, "platform": "32-bit signed int"}
AND {"number_mm": "Returns 0; operand evaluation order is unspecified."}
WHEN Invoke number_bits with the fixture arguments once.
THEN {"limitation": "Negative shift, unrepresentable signed left shift, or shift at type width; no portable return."}
```

Open questions: Undefined shift; the C helper does not validate the width.

## db.number_bits.invalid-shift-31

invalid shift 31

```text
CASE db.number_bits.invalid-shift-31
SOURCE src/db.c:number_bits:3006
GIVEN {"arguments": {"width": 31}, "platform": "32-bit signed int"}
AND {"number_mm": "Returns 0; operand evaluation order is unspecified."}
WHEN Invoke number_bits with the fixture arguments once.
THEN {"limitation": "Negative shift, unrepresentable signed left shift, or shift at type width; no portable return."}
```

Open questions: Undefined shift; the C helper does not validate the width.

## db.number_bits.invalid-shift-32

invalid shift 32

```text
CASE db.number_bits.invalid-shift-32
SOURCE src/db.c:number_bits:3006
GIVEN {"arguments": {"width": 32}, "platform": "32-bit signed int"}
AND {"number_mm": "Returns 0; operand evaluation order is unspecified."}
WHEN Invoke number_bits with the fixture arguments once.
THEN {"limitation": "Negative shift, unrepresentable signed left shift, or shift at type width; no portable return."}
```

Open questions: Undefined shift; the C helper does not validate the width.

## db.number_range.domain-subtraction-overflow

domain subtraction overflow

```text
CASE db.number_range.domain-subtraction-overflow
SOURCE src/db.c:number_range:2962
GIVEN {"arguments": {"from": -2147483648, "to": 2147483647}, "platform": "32-bit signed int"}
AND {"number_bits": "Returns 3 if called.", "number_mm": "Must not be reached before the identified overflow."}
WHEN Invoke number_range with the fixture arguments once.
THEN {"limitation": "Signed overflow has no portable result; do not assert wrapped arithmetic."}
```

Open questions: Undefined signed arithmetic outside the safe direct-helper domain.

## db.number_range.power-growth-overflow

power growth overflow

```text
CASE db.number_range.power-growth-overflow
SOURCE src/db.c:number_range:2965
GIVEN {"arguments": {"from": 0, "to": 1073741824}, "platform": "32-bit signed int"}
AND {"number_bits": "Returns 3 if called.", "number_mm": "Must not be reached before the identified overflow."}
WHEN Invoke number_range with the fixture arguments once.
THEN {"limitation": "Signed overflow has no portable result; do not assert wrapped arithmetic."}
```

Open questions: Undefined signed arithmetic outside the safe direct-helper domain.

## db.number_fuzzy.increment-overflow

increment overflow

```text
CASE db.number_fuzzy.increment-overflow
SOURCE src/db.c:number_fuzzy:2943
GIVEN {"arguments": {"number": 2147483647}, "platform": "32-bit signed int"}
AND {"number_bits": "Returns 3 if called.", "number_mm": "Must not be reached before the identified overflow."}
WHEN Invoke number_fuzzy with the fixture arguments once.
THEN {"limitation": "Signed overflow has no portable result; do not assert wrapped arithmetic."}
```

Open questions: Undefined signed arithmetic outside the safe direct-helper domain.

## db.interpolate.product-overflow

product overflow

```text
CASE db.interpolate.product-overflow
SOURCE src/db.c:interpolate:3107
GIVEN {"arguments": {"level": 2147483647, "value_00": 0, "value_32": 2}, "platform": "32-bit signed int"}
AND {"number_bits": "Returns 3 if called.", "number_mm": "Must not be reached before the identified overflow."}
WHEN Invoke interpolate with the fixture arguments once.
THEN {"limitation": "Signed overflow has no portable result; do not assert wrapped arithmetic."}
```

Open questions: Undefined signed arithmetic outside the safe direct-helper domain.

## ban.load_bans.empty-file-parser-exits

empty file parser exits

```text
CASE ban.load_bans.empty-file-parser-exits
SOURCE src/ban.c:load_bans:92; src/db.c:fread_word:2524; src/db.c:fread_number:2166; src/db.c:fread_flag:2214; src/db.c:fread_to_eol:2499
GIVEN {"file_bytes": "", "ban_list": [], "ban_free": [], "platform": "C locale, 8-bit signed char with EOF=-1 preserved when stored in char; successful file open and allocations."}
AND {"parsers": "Run fread_word, fread_number, fread_flag, flag_convert and fread_to_eol; no parser stubs.", "allocation": "Successful recording boundary.", "stdio": "Byte stream with persistent EOF; exit is captured as termination, not return."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"ordered_events": ["new_ban", "fread_word fills its buffer with EOF bytes", "bug(\"Fread_word: word too long.\",0)", "exit(1)"], "forbidden": ["append ban", "normal return"]}
```

## ban.load_bans.whitespace-only-parser-exits

whitespace only parser exits

```text
CASE ban.load_bans.whitespace-only-parser-exits
SOURCE src/ban.c:load_bans:92; src/db.c:fread_word:2524; src/db.c:fread_number:2166; src/db.c:fread_flag:2214; src/db.c:fread_to_eol:2499
GIVEN {"file_bytes": " \t\n", "ban_list": [], "ban_free": [], "platform": "C locale, 8-bit signed char with EOF=-1 preserved when stored in char; successful file open and allocations."}
AND {"parsers": "Run fread_word, fread_number, fread_flag, flag_convert and fread_to_eol; no parser stubs.", "allocation": "Successful recording boundary.", "stdio": "Byte stream with persistent EOF; exit is captured as termination, not return."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"ordered_events": ["new_ban", "fread_word skips initial whitespace then fills buffer with EOF bytes", "bug(\"Fread_word: word too long.\",0)", "exit(1)"], "forbidden": ["append ban", "normal return"]}
```

## ban.load_bans.bad-level-parser-exits

bad level parser exits

```text
CASE ban.load_bans.bad-level-parser-exits
SOURCE src/ban.c:load_bans:92; src/db.c:fread_word:2524; src/db.c:fread_number:2166; src/db.c:fread_flag:2214; src/db.c:fread_to_eol:2499
GIVEN {"file_bytes": "example.org x A\n", "ban_list": [], "ban_free": [], "platform": "C locale, 8-bit signed char with EOF=-1 preserved when stored in char; successful file open and allocations."}
AND {"parsers": "Run fread_word, fread_number, fread_flag, flag_convert and fread_to_eol; no parser stubs.", "allocation": "Successful recording boundary.", "stdio": "Byte stream with persistent EOF; exit is captured as termination, not return."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"ordered_events": ["new_ban", "store name example.org", "bug(\"Fread_number: bad format.\",0)", "exit(1)"], "forbidden": ["append ban", "normal return"]}
```

## ban.load_bans.no-final-newline-does-not-terminate

no final newline does not terminate

```text
CASE ban.load_bans.no-final-newline-does-not-terminate
SOURCE src/ban.c:load_bans:92; src/db.c:fread_word:2524; src/db.c:fread_number:2166; src/db.c:fread_flag:2214; src/db.c:fread_to_eol:2499
GIVEN {"file_bytes": "example.org 10 A", "ban_list": [], "ban_free": [], "platform": "C locale, 8-bit signed char with EOF=-1 preserved when stored in char; successful file open and allocations."}
AND {"parsers": "Run fread_word, fread_number, fread_flag, flag_convert and fread_to_eol; no parser stubs.", "allocation": "Successful recording boundary.", "stdio": "Byte stream with persistent EOF; exit is captured as termination, not return."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"ordered_events": ["new_ban", "store name example.org", "store level 10", "store ban_flags 1", "fread_to_eol repeatedly reads EOF"], "control": "No return: EOF is neither newline nor carriage return.", "forbidden": ["append ban", "fclose", "next allocation"]}
```

## ban.load_bans.trailing-spaces-create-phantom-record

trailing spaces create phantom record

```text
CASE ban.load_bans.trailing-spaces-create-phantom-record
SOURCE src/ban.c:load_bans:92; src/db.c:fread_word:2524; src/db.c:fread_number:2166; src/db.c:fread_flag:2214; src/db.c:fread_to_eol:2499
GIVEN {"file_bytes": "example.org 10 A\n  ", "ban_list": [], "ban_free": [], "platform": "C locale, 8-bit signed char with EOF=-1 preserved when stored in char; successful file open and allocations."}
AND {"parsers": "Run fread_word, fread_number, fread_flag, flag_convert and fread_to_eol; no parser stubs.", "allocation": "Successful recording boundary.", "stdio": "Byte stream with persistent EOF; exit is captured as termination, not return."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"ordered_events": ["append first record example.org, level 10, flags 1", "new_ban for second record", "bug(\"Fread_word: word too long.\",0)", "exit(1)"], "ban_list_before_exit": ["example.org"], "forbidden": ["append second record", "normal return"]}
```

## ban.load_bans.invalid-flag-character-is-zero

invalid flag character is zero

```text
CASE ban.load_bans.invalid-flag-character-is-zero
SOURCE src/ban.c:load_bans:92; src/db.c:fread_word:2524; src/db.c:fread_number:2166; src/db.c:fread_flag:2214; src/db.c:fread_to_eol:2499
GIVEN {"file_bytes": "example.org 10 ?\n", "ban_list": [], "ban_free": [], "platform": "C locale, 8-bit signed char with EOF=-1 preserved when stored in char; successful file open and allocations."}
AND {"parsers": "Run fread_word, fread_number, fread_flag, flag_convert and fread_to_eol; no parser stubs.", "allocation": "Successful recording boundary.", "stdio": "Byte stream with persistent EOF; exit is captured as termination, not return."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"ordered_events": ["new_ban", "store name example.org", "store level 10", "fread_flag returns 0 and pushes back ?", "fread_to_eol consumes ? and newline, then reads EOF", "append record", "fclose", "return"], "ban_list": [{"name": "example.org", "level": 10, "ban_flags": 0}]}
```

## ban.load_bans.duplicate-letter-flags-add

duplicate letter flags add

```text
CASE ban.load_bans.duplicate-letter-flags-add
SOURCE src/ban.c:load_bans:92; src/db.c:fread_word:2524; src/db.c:fread_number:2166; src/db.c:fread_flag:2214; src/db.c:fread_to_eol:2499
GIVEN {"file_bytes": "example.org 10 AA\n", "ban_list": [], "ban_free": [], "platform": "C locale, 8-bit signed char with EOF=-1 preserved when stored in char; successful file open and allocations."}
AND {"parsers": "Run fread_word, fread_number, fread_flag, flag_convert and fread_to_eol; no parser stubs.", "allocation": "Successful recording boundary.", "stdio": "Byte stream with persistent EOF; exit is captured as termination, not return."}
WHEN Invoke load_bans with the fixture arguments once.
THEN {"ordered_events": ["new_ban", "parse name example.org, level 10, flags 2", "append record", "fclose", "return"], "ban_list": [{"name": "example.org", "level": 10, "ban_flags": 2}], "quirk": "Flag letters are added, not bitwise ORed."}
```

## ban.ban_site.replacement-walks-recycle-list

replacement walks recycle list

```text
CASE ban.ban_site.replacement-walks-recycle-list
SOURCE src/ban.c:ban_site:229; src/recycle.c:free_ban:98; src/recycle.c:new_ban:79
GIVEN {"actor": {"id": "admin", "trust": 60}, "argument": "example.org all", "fPerm": false, "ban_list": [{"id": "old", "name": "example.org", "level": 60, "valid": true, "next": "tail"}, {"id": "tail", "name": "unrelated.org", "level": 60, "valid": true, "next": null}], "ban_free": [{"id": "free1", "name": "recycled.org", "valid": false, "next": null}], "string_storage": "All existing names are immutable shared database strings; free_string leaves these bytes unchanged."}
AND {"get_trust": "Returns 60.", "save_bans": "Recording persistence boundary.", "recycler": "Execute new_ban/free_ban; allocation succeeds.", "str_dup": "Allocation boundary returns an owned copy of the requested name; do not execute unrelated-pointer ordering comparisons in the allocator."}
WHEN Invoke ban_site with the fixture arguments once.
THEN {"ordered_events": ["unlink old; live head becomes tail", "free_ban(old) changes old.next to free1 and free-list head to old", "replacement loop compares free1.name, then terminates without visiting tail", "new_ban reuses old and leaves free1 as free-list head", "assign new name, level 60 and BAN_ALL", "prepend old before tail", "save_bans", "send example.org has been banned.\n\r to admin"], "result_list": ["old", "tail"], "result_free_list": ["free1"], "forbidden": ["compare tail.name", "message to other characters"]}
```

## special.spec_name.registered-spec_breath_acid

registered spec_breath_acid

```text
CASE special.spec_name.registered-spec_breath_acid
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_breath_acid"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_breath_acid", "return_pointer": "spec_table[1].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1], "loop_guard_indices_in_order": [0, 1], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_breath_fire

registered spec_breath_fire

```text
CASE special.spec_name.registered-spec_breath_fire
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_breath_fire"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_breath_fire", "return_pointer": "spec_table[2].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2], "loop_guard_indices_in_order": [0, 1, 2], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_breath_frost

registered spec_breath_frost

```text
CASE special.spec_name.registered-spec_breath_frost
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_breath_frost"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_breath_frost", "return_pointer": "spec_table[3].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3], "loop_guard_indices_in_order": [0, 1, 2, 3], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_breath_gas

registered spec_breath_gas

```text
CASE special.spec_name.registered-spec_breath_gas
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_breath_gas"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_breath_gas", "return_pointer": "spec_table[4].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4], "loop_guard_indices_in_order": [0, 1, 2, 3, 4], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_breath_lightning

registered spec_breath_lightning

```text
CASE special.spec_name.registered-spec_breath_lightning
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_breath_lightning"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_breath_lightning", "return_pointer": "spec_table[5].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_cast_adept

registered spec_cast_adept

```text
CASE special.spec_name.registered-spec_cast_adept
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_cast_adept"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_cast_adept", "return_pointer": "spec_table[6].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_cast_cleric

registered spec_cast_cleric

```text
CASE special.spec_name.registered-spec_cast_cleric
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_cast_cleric"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_cast_cleric", "return_pointer": "spec_table[7].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_cast_judge

registered spec_cast_judge

```text
CASE special.spec_name.registered-spec_cast_judge
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_cast_judge"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_cast_judge", "return_pointer": "spec_table[8].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_cast_mage

registered spec_cast_mage

```text
CASE special.spec_name.registered-spec_cast_mage
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_cast_mage"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_cast_mage", "return_pointer": "spec_table[9].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_cast_undead

registered spec_cast_undead

```text
CASE special.spec_name.registered-spec_cast_undead
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_cast_undead"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_cast_undead", "return_pointer": "spec_table[10].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_executioner

registered spec_executioner

```text
CASE special.spec_name.registered-spec_executioner
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_executioner"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_executioner", "return_pointer": "spec_table[11].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_fido

registered spec_fido

```text
CASE special.spec_name.registered-spec_fido
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_fido"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_fido", "return_pointer": "spec_table[12].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_guard

registered spec_guard

```text
CASE special.spec_name.registered-spec_guard
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_guard"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_guard", "return_pointer": "spec_table[13].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_janitor

registered spec_janitor

```text
CASE special.spec_name.registered-spec_janitor
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_janitor"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_janitor", "return_pointer": "spec_table[14].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_mayor

registered spec_mayor

```text
CASE special.spec_name.registered-spec_mayor
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_mayor"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_mayor", "return_pointer": "spec_table[15].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_poison

registered spec_poison

```text
CASE special.spec_name.registered-spec_poison
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_poison"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_poison", "return_pointer": "spec_table[16].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_thief

registered spec_thief

```text
CASE special.spec_name.registered-spec_thief
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_thief"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_thief", "return_pointer": "spec_table[17].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_nasty

registered spec_nasty

```text
CASE special.spec_name.registered-spec_nasty
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_nasty"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_nasty", "return_pointer": "spec_table[18].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_troll_member

registered spec_troll_member

```text
CASE special.spec_name.registered-spec_troll_member
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_troll_member"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_troll_member", "return_pointer": "spec_table[19].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_name.registered-spec_ogre_member

registered spec_ogre_member

```text
CASE special.spec_name.registered-spec_ogre_member
SOURCE src/special.c:spec_name:117; src/special.c:spec_name:119; src/special.c:spec_name:120
GIVEN {"arguments": {"function": "spec_ogre_member"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}, "identity_contract": "Names denote distinct functions with the SPEC_FUN signature; unregistered_valid_function_pointer denotes a distinct valid compatible function absent from the table."}
AND {"collaborators": "None: execute the real function and immutable table.", "randomness": "None; no RNG, clock, allocator, I/O or callback is invoked."}
WHEN Invoke spec_name with the fixture arguments once.
THEN {"returned_name": "spec_ogre_member", "return_pointer": "spec_table[20].name (same pointer, not a copy)", "equality_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "sentinel_function_compared_to_argument": false, "unchanged": ["table", "all names", "all caller and world state"], "forbidden": ["invoke input function", "invoke any table function", "allocation/free", "messages to any recipient", "random draws", "read beyond sentinel"]}
```

## special.spec_lookup.registered-spec_breath_acid

registered spec_breath_acid

```text
CASE special.spec_lookup.registered-spec_breath_acid
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_breath_acid"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_acid", "loop_guard_indices_in_order": [0, 1], "first_character_comparisons_in_order": [0, 1], "str_prefix_table_indices_in_order": [0, 1], "str_prefix_returns_in_order": [true, false], "return_pointer_identity": "spec_table[1].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_breath_fire

registered spec_breath_fire

```text
CASE special.spec_lookup.registered-spec_breath_fire
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_breath_fire"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_fire", "loop_guard_indices_in_order": [0, 1, 2], "first_character_comparisons_in_order": [0, 1, 2], "str_prefix_table_indices_in_order": [0, 1, 2], "str_prefix_returns_in_order": [true, true, false], "return_pointer_identity": "spec_table[2].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_breath_frost

registered spec_breath_frost

```text
CASE special.spec_lookup.registered-spec_breath_frost
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_breath_frost"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_frost", "loop_guard_indices_in_order": [0, 1, 2, 3], "first_character_comparisons_in_order": [0, 1, 2, 3], "str_prefix_table_indices_in_order": [0, 1, 2, 3], "str_prefix_returns_in_order": [true, true, true, false], "return_pointer_identity": "spec_table[3].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_breath_gas

registered spec_breath_gas

```text
CASE special.spec_lookup.registered-spec_breath_gas
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_breath_gas"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_gas", "loop_guard_indices_in_order": [0, 1, 2, 3, 4], "first_character_comparisons_in_order": [0, 1, 2, 3, 4], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4], "str_prefix_returns_in_order": [true, true, true, true, false], "return_pointer_identity": "spec_table[4].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_breath_lightning

registered spec_breath_lightning

```text
CASE special.spec_lookup.registered-spec_breath_lightning
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_breath_lightning"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_lightning", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5], "str_prefix_returns_in_order": [true, true, true, true, true, false], "return_pointer_identity": "spec_table[5].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_cast_adept

registered spec_cast_adept

```text
CASE special.spec_lookup.registered-spec_cast_adept
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_cast_adept"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_cast_adept", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6], "str_prefix_returns_in_order": [true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[6].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_cast_cleric

registered spec_cast_cleric

```text
CASE special.spec_lookup.registered-spec_cast_cleric
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_cast_cleric"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_cast_cleric", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[7].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_cast_judge

registered spec_cast_judge

```text
CASE special.spec_lookup.registered-spec_cast_judge
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_cast_judge"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_cast_judge", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[8].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_cast_mage

registered spec_cast_mage

```text
CASE special.spec_lookup.registered-spec_cast_mage
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_cast_mage"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_cast_mage", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[9].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_cast_undead

registered spec_cast_undead

```text
CASE special.spec_lookup.registered-spec_cast_undead
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_cast_undead"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_cast_undead", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[10].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_executioner

registered spec_executioner

```text
CASE special.spec_lookup.registered-spec_executioner
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_executioner"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_executioner", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[11].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_fido

registered spec_fido

```text
CASE special.spec_lookup.registered-spec_fido
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_fido"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_fido", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[12].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_guard

registered spec_guard

```text
CASE special.spec_lookup.registered-spec_guard
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_guard"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_guard", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[13].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_janitor

registered spec_janitor

```text
CASE special.spec_lookup.registered-spec_janitor
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_janitor"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_janitor", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[14].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_mayor

registered spec_mayor

```text
CASE special.spec_lookup.registered-spec_mayor
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_mayor"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_mayor", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[15].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_poison

registered spec_poison

```text
CASE special.spec_lookup.registered-spec_poison
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_poison"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_poison", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[16].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_thief

registered spec_thief

```text
CASE special.spec_lookup.registered-spec_thief
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_thief"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_thief", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[17].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_nasty

registered spec_nasty

```text
CASE special.spec_lookup.registered-spec_nasty
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_nasty"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_nasty", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[18].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_troll_member

registered spec_troll_member

```text
CASE special.spec_lookup.registered-spec_troll_member
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_troll_member"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_troll_member", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[19].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.registered-spec_ogre_member

registered spec_ogre_member

```text
CASE special.spec_lookup.registered-spec_ogre_member
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_ogre_member"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_ogre_member", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[20].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.one-letter-first-match

one letter first match

```text
CASE special.spec_lookup.one-letter-first-match
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "s"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_any", "loop_guard_indices_in_order": [0], "first_character_comparisons_in_order": [0], "str_prefix_table_indices_in_order": [0], "str_prefix_returns_in_order": [false], "return_pointer_identity": "spec_table[0].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.common-prefix-first-match

common prefix first match

```text
CASE special.spec_lookup.common-prefix-first-match
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_any", "loop_guard_indices_in_order": [0], "first_character_comparisons_in_order": [0], "str_prefix_table_indices_in_order": [0], "str_prefix_returns_in_order": [false], "return_pointer_identity": "spec_table[0].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.ambiguous-cast-first-adept

ambiguous cast first adept

```text
CASE special.spec_lookup.ambiguous-cast-first-adept
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_cast"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_cast_adept", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6], "str_prefix_returns_in_order": [true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[6].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.ambiguous-breath-f-first-fire

ambiguous breath f first fire

```text
CASE special.spec_lookup.ambiguous-breath-f-first-fire
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_breath_f"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_breath_fire", "loop_guard_indices_in_order": [0, 1, 2], "first_character_comparisons_in_order": [0, 1, 2], "str_prefix_table_indices_in_order": [0, 1, 2], "str_prefix_returns_in_order": [true, true, false], "return_pointer_identity": "spec_table[2].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.uppercase-last-match

uppercase last match

```text
CASE special.spec_lookup.uppercase-last-match
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:107; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "SPEC_PATROLMAN"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "spec_patrolman", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false], "return_pointer_identity": "spec_table[21].function", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.same-first-letter-no-prefix

same first letter no prefix

```text
CASE special.spec_lookup.same-first-letter-no-prefix
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "sz"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.longer-than-complete-name

longer than complete name

```text
CASE special.spec_lookup.longer-than-complete-name
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_patrolman_extra"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.trailing-space-not-trimmed

trailing space not trimmed

```text
CASE special.spec_lookup.trailing-space-not-trimmed
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec_patrolman "}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.leading-space-not-trimmed

leading space not trimmed

```text
CASE special.spec_lookup.leading-space-not-trimmed
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110
GIVEN {"arguments": {"name": " spec_patrolman"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [], "str_prefix_returns_in_order": [], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.embedded-space-not-tokenized

embedded space not tokenized

```text
CASE special.spec_lookup.embedded-space-not-tokenized
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110; src/db.c:str_prefix:3178
GIVEN {"arguments": {"name": "spec patrolman"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_returns_in_order": [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.whitespace-only

whitespace only

```text
CASE special.spec_lookup.whitespace-only
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110
GIVEN {"arguments": {"name": " "}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [], "str_prefix_returns_in_order": [], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## special.spec_lookup.nonascii-first-byte

nonascii first byte

```text
CASE special.spec_lookup.nonascii-first-byte
SOURCE src/special.c:spec_lookup:103; src/special.c:spec_lookup:105; src/special.c:spec_lookup:106; src/special.c:spec_lookup:110
GIVEN {"arguments": {"name": "é"}, "table": {"entries_in_order": ["spec_breath_any", "spec_breath_acid", "spec_breath_fire", "spec_breath_frost", "spec_breath_gas", "spec_breath_lightning", "spec_cast_adept", "spec_cast_cleric", "spec_cast_judge", "spec_cast_mage", "spec_cast_undead", "spec_executioner", "spec_fido", "spec_guard", "spec_janitor", "spec_mayor", "spec_poison", "spec_thief", "spec_nasty", "spec_troll_member", "spec_ogre_member", "spec_patrolman"], "sentinel_index": 22, "sentinel": {"name": "C NULL", "function": "C NULL"}}}
AND {"str_prefix": "Execute actual src/db.c helper: false means ASCII case-insensitive prefix match. Do not stub the predicate.", "LOWER": "Actual merc.h macro folds A..Z only; no locale or Unicode normalization.", "randomness": "None; no callback, allocator, clock or I/O."}
WHEN Invoke spec_lookup with the fixture arguments once.
THEN {"return_function_pointer": "C NULL", "loop_guard_indices_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "first_character_comparisons_in_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "str_prefix_table_indices_in_order": [], "str_prefix_returns_in_order": [], "return_pointer_identity": "C NULL", "unchanged": ["input bytes", "table", "all caller and world state"], "forbidden": ["compare sentinel name bytes", "invoke returned procedure", "messages", "allocation/free", "random draws", "trim or tokenize input"]}
```

## handler.is_same_clan.clans-0-1

clans 0 1

```text
CASE handler.is_same_clan.clans-0-1
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"clan": 0, "kind": "PC"}, "victim": {"clan": 1, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.clans-0-2

clans 0 2

```text
CASE handler.is_same_clan.clans-0-2
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"clan": 0, "kind": "PC"}, "victim": {"clan": 2, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.clans-1-0

clans 1 0

```text
CASE handler.is_same_clan.clans-1-0
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"clan": 1, "kind": "PC"}, "victim": {"clan": 0, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.clans-1-2

clans 1 2

```text
CASE handler.is_same_clan.clans-1-2
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"clan": 1, "kind": "PC"}, "victim": {"clan": 2, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.clans-2-0

clans 2 0

```text
CASE handler.is_same_clan.clans-2-0
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"clan": 2, "kind": "PC"}, "victim": {"clan": 0, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## handler.is_same_clan.self-clan-0

self clan 0

```text
CASE handler.is_same_clan.self-clan-0
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"id": "ch", "clan": 0, "kind": "PC"}, "victim": {"same_entity_as": "ch"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.self-clan-1

self clan 1

```text
CASE handler.is_same_clan.self-clan-1
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"id": "ch", "clan": 1, "kind": "PC"}, "victim": {"same_entity_as": "ch"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.self-clan-2

self clan 2

```text
CASE handler.is_same_clan.self-clan-2
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"id": "ch", "clan": 2, "kind": "PC"}, "victim": {"same_entity_as": "ch"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": true, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## handler.is_same_clan.kinds-npc-pc

kinds npc pc

```text
CASE handler.is_same_clan.kinds-npc-pc
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"clan": 2, "kind": "NPC"}, "victim": {"clan": 2, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": true, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## handler.is_same_clan.kinds-pc-npc

kinds pc npc

```text
CASE handler.is_same_clan.kinds-pc-npc
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"clan": 2, "kind": "PC"}, "victim": {"clan": 2, "kind": "NPC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": true, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## handler.is_same_clan.kinds-npc-npc

kinds npc npc

```text
CASE handler.is_same_clan.kinds-npc-npc
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"clan": 2, "kind": "NPC"}, "victim": {"clan": 2, "kind": "NPC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": true, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## handler.is_same_clan.independent-0-null-victim

independent 0 null victim

```text
CASE handler.is_same_clan.independent-0-null-victim
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"clan": 0, "kind": "PC"}, "victim": {"C_NULL": true}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.independent-1-null-victim

independent 1 null victim

```text
CASE handler.is_same_clan.independent-1-null-victim
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:336
GIVEN {"actor": {"clan": 1, "kind": "PC"}, "victim": {"C_NULL": true}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent"], "victim_read": false, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks", "dereference victim"]}
```

## handler.is_same_clan.victim-clan-outside-table--1

victim clan outside table  1

```text
CASE handler.is_same_clan.victim-clan-outside-table--1
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"clan": 2, "kind": "PC"}, "victim": {"clan": -1, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## handler.is_same_clan.victim-clan-outside-table-3

victim clan outside table 3

```text
CASE handler.is_same_clan.victim-clan-outside-table-3
SOURCE src/handler.c:is_same_clan:335; src/handler.c:is_same_clan:338
GIVEN {"actor": {"clan": 2, "kind": "PC"}, "victim": {"clan": 3, "kind": "PC"}, "table": {"MAX_CLAN": 3, "rows": [{"index": 0, "name": "", "independent": true}, {"index": 1, "name": "loner", "independent": true}, {"index": 2, "name": "rom", "independent": false}]}}
AND {"collaborators": "None. Read the real immutable clan table.", "randomness": "None."}
WHEN Invoke is_same_clan with the fixture arguments once.
THEN {"return": false, "ordered_reads": ["actor.clan", "clan_table[actor.clan].independent", "compare actor.clan and victim.clan; operand read order unspecified"], "victim_read": true, "unchanged": ["all entities and table"], "forbidden": ["messages", "random draws", "allocation", "clan mutation", "trust or kind checks"]}
```

## handler.room_is_dark.matrix-sect_inside-sun_rise

matrix sect_inside sun_rise

```text
CASE handler.room_is_dark.matrix-sect_inside-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2366
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["weather_info.sunlight"]}
```

## handler.room_is_dark.matrix-sect_inside-sun_light

matrix sect_inside sun_light

```text
CASE handler.room_is_dark.matrix-sect_inside-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2366
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["weather_info.sunlight"]}
```

## handler.room_is_dark.matrix-sect_inside-sun_set

matrix sect_inside sun_set

```text
CASE handler.room_is_dark.matrix-sect_inside-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2366
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["weather_info.sunlight"]}
```

## handler.room_is_dark.matrix-sect_city-sun_rise

matrix sect_city sun_rise

```text
CASE handler.room_is_dark.matrix-sect_city-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2366
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_CITY"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["weather_info.sunlight"]}
```

## handler.room_is_dark.matrix-sect_city-sun_light

matrix sect_city sun_light

```text
CASE handler.room_is_dark.matrix-sect_city-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2366
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_CITY"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["weather_info.sunlight"]}
```

## handler.room_is_dark.matrix-sect_city-sun_set

matrix sect_city sun_set

```text
CASE handler.room_is_dark.matrix-sect_city-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2366
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_CITY"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["weather_info.sunlight"]}
```

## handler.room_is_dark.matrix-sect_forest-sun_dark

matrix sect_forest sun_dark

```text
CASE handler.room_is_dark.matrix-sect_forest-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FOREST"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_forest-sun_rise

matrix sect_forest sun_rise

```text
CASE handler.room_is_dark.matrix-sect_forest-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FOREST"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_forest-sun_light

matrix sect_forest sun_light

```text
CASE handler.room_is_dark.matrix-sect_forest-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FOREST"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_forest-sun_set

matrix sect_forest sun_set

```text
CASE handler.room_is_dark.matrix-sect_forest-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FOREST"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_hills-sun_dark

matrix sect_hills sun_dark

```text
CASE handler.room_is_dark.matrix-sect_hills-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_HILLS"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_hills-sun_rise

matrix sect_hills sun_rise

```text
CASE handler.room_is_dark.matrix-sect_hills-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_HILLS"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_hills-sun_light

matrix sect_hills sun_light

```text
CASE handler.room_is_dark.matrix-sect_hills-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_HILLS"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_hills-sun_set

matrix sect_hills sun_set

```text
CASE handler.room_is_dark.matrix-sect_hills-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_HILLS"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_mountain-sun_dark

matrix sect_mountain sun_dark

```text
CASE handler.room_is_dark.matrix-sect_mountain-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_MOUNTAIN"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_mountain-sun_rise

matrix sect_mountain sun_rise

```text
CASE handler.room_is_dark.matrix-sect_mountain-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_MOUNTAIN"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_mountain-sun_light

matrix sect_mountain sun_light

```text
CASE handler.room_is_dark.matrix-sect_mountain-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_MOUNTAIN"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_mountain-sun_set

matrix sect_mountain sun_set

```text
CASE handler.room_is_dark.matrix-sect_mountain-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_MOUNTAIN"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_water_swim-sun_dark

matrix sect_water_swim sun_dark

```text
CASE handler.room_is_dark.matrix-sect_water_swim-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_WATER_SWIM"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_water_swim-sun_rise

matrix sect_water_swim sun_rise

```text
CASE handler.room_is_dark.matrix-sect_water_swim-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_WATER_SWIM"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_water_swim-sun_light

matrix sect_water_swim sun_light

```text
CASE handler.room_is_dark.matrix-sect_water_swim-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_WATER_SWIM"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_water_swim-sun_set

matrix sect_water_swim sun_set

```text
CASE handler.room_is_dark.matrix-sect_water_swim-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_WATER_SWIM"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_water_noswim-sun_dark

matrix sect_water_noswim sun_dark

```text
CASE handler.room_is_dark.matrix-sect_water_noswim-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_WATER_NOSWIM"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_water_noswim-sun_rise

matrix sect_water_noswim sun_rise

```text
CASE handler.room_is_dark.matrix-sect_water_noswim-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_WATER_NOSWIM"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_water_noswim-sun_light

matrix sect_water_noswim sun_light

```text
CASE handler.room_is_dark.matrix-sect_water_noswim-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_WATER_NOSWIM"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_water_noswim-sun_set

matrix sect_water_noswim sun_set

```text
CASE handler.room_is_dark.matrix-sect_water_noswim-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_WATER_NOSWIM"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_unused-sun_dark

matrix sect_unused sun_dark

```text
CASE handler.room_is_dark.matrix-sect_unused-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_UNUSED"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_unused-sun_rise

matrix sect_unused sun_rise

```text
CASE handler.room_is_dark.matrix-sect_unused-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_UNUSED"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_unused-sun_light

matrix sect_unused sun_light

```text
CASE handler.room_is_dark.matrix-sect_unused-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_UNUSED"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_unused-sun_set

matrix sect_unused sun_set

```text
CASE handler.room_is_dark.matrix-sect_unused-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_UNUSED"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_air-sun_dark

matrix sect_air sun_dark

```text
CASE handler.room_is_dark.matrix-sect_air-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_AIR"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_air-sun_rise

matrix sect_air sun_rise

```text
CASE handler.room_is_dark.matrix-sect_air-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_AIR"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_air-sun_light

matrix sect_air sun_light

```text
CASE handler.room_is_dark.matrix-sect_air-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_AIR"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_air-sun_set

matrix sect_air sun_set

```text
CASE handler.room_is_dark.matrix-sect_air-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_AIR"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_desert-sun_dark

matrix sect_desert sun_dark

```text
CASE handler.room_is_dark.matrix-sect_desert-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_DESERT"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_desert-sun_rise

matrix sect_desert sun_rise

```text
CASE handler.room_is_dark.matrix-sect_desert-sun_rise
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_DESERT"}, "weather_info": {"sunlight": "SUN_RISE"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_desert-sun_light

matrix sect_desert sun_light

```text
CASE handler.room_is_dark.matrix-sect_desert-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_DESERT"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.matrix-sect_desert-sun_set

matrix sect_desert sun_set

```text
CASE handler.room_is_dark.matrix-sect_desert-sun_set
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_DESERT"}, "weather_info": {"sunlight": "SUN_SET"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.light-boundary--32768-dark-inside

light boundary  32768 dark inside

```text
CASE handler.room_is_dark.light-boundary--32768-dark-inside
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2362
GIVEN {"room": {"light": -32768, "room_flags": ["ROOM_DARK"], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["room.sector_type", "weather_info.sunlight"]}
```

## handler.room_is_dark.light-boundary--1-dark-inside

light boundary  1 dark inside

```text
CASE handler.room_is_dark.light-boundary--1-dark-inside
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2362
GIVEN {"room": {"light": -1, "room_flags": ["ROOM_DARK"], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["room.sector_type", "weather_info.sunlight"]}
```

## handler.room_is_dark.light-boundary-0-dark-inside

light boundary 0 dark inside

```text
CASE handler.room_is_dark.light-boundary-0-dark-inside
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2362
GIVEN {"room": {"light": 0, "room_flags": ["ROOM_DARK"], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["room.sector_type", "weather_info.sunlight"]}
```

## handler.room_is_dark.light-boundary-1-dark-inside

light boundary 1 dark inside

```text
CASE handler.room_is_dark.light-boundary-1-dark-inside
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2359
GIVEN {"room": {"light": 1, "room_flags": ["ROOM_DARK"], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["room.room_flags", "room.sector_type", "weather_info.sunlight"]}
```

## handler.room_is_dark.light-boundary-32767-dark-inside

light boundary 32767 dark inside

```text
CASE handler.room_is_dark.light-boundary-32767-dark-inside
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2359
GIVEN {"room": {"light": 32767, "room_flags": ["ROOM_DARK"], "sector_type": "SECT_INSIDE"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": ["room.room_flags", "room.sector_type", "weather_info.sunlight"]}
```

## handler.room_is_dark.negative-light--32768-sun_light

negative light  32768 sun_light

```text
CASE handler.room_is_dark.negative-light--32768-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": -32768, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.negative-light--32768-sun_dark

negative light  32768 sun_dark

```text
CASE handler.room_is_dark.negative-light--32768-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": -32768, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.negative-light--1-sun_light

negative light  1 sun_light

```text
CASE handler.room_is_dark.negative-light--1-sun_light
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": -1, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_LIGHT"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.negative-light--1-sun_dark

negative light  1 sun_dark

```text
CASE handler.room_is_dark.negative-light--1-sun_dark
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": -1, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.unrelated-flag-does-not-light-room

unrelated flag does not light room

```text
CASE handler.room_is_dark.unrelated-flag-does-not-light-room
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": ["ROOM_SAFE"], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.unknown-sunlight-falls-through

unknown sunlight falls through

```text
CASE handler.room_is_dark.unknown-sunlight-falls-through
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2372
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": "SECT_FIELD"}, "weather_info": {"sunlight": 99}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": false, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

## handler.room_is_dark.unknown-sector-uses-weather

unknown sector uses weather

```text
CASE handler.room_is_dark.unknown-sector-uses-weather
SOURCE src/handler.c:room_is_dark:2358; src/handler.c:room_is_dark:2370
GIVEN {"room": {"light": 0, "room_flags": [], "sector_type": 99}, "weather_info": {"sunlight": "SUN_DARK"}}
AND {"collaborators": "No callees. Actual IS_SET(flag,bit) bitwise AND; ROOM_DARK=A=1.", "weather": "Fixed global sunlight; no scheduler invocation or wall-clock lookup.", "randomness": "None."}
WHEN Invoke room_is_dark with the fixture arguments once.
THEN {"return": true, "read_dependencies_in_order": ["room.light", "room.room_flags", "room.sector_type", "weather_info.sunlight"], "unchanged": ["room", "weather", "all entities"], "forbidden": ["messages", "allocation", "RNG", "clock reads", "actor visibility checks", "writes"], "unread_dependencies": []}
```

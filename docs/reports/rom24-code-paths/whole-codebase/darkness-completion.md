# Completed item: room_is_dark

**Complete static behavioral specification for `src/handler.c:room_is_dark`: 59 specified cases, no blocked cases and no remaining function-level gaps.** Nine original IDs are preserved and 50 cases added. All six direct caller sites are reviewed below. This does not complete those callers or handler.c. No executable gameplay tests were generated or run.

Source: [room_is_dark](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2356), lines 2356–2373. HEAD reference: `d3a29007355e7298e0033fcb666e9a6895c2146f`. SHA-256: handler.c `0e95a3bd6480448855bba8d7cae6b6f8b5aad3d2be2738a21cd58571f7bf2261`; merc.h `080da51df18acf5fac5540cbe03dea9d44aeda7cb47e920a928a28fad83e7937`. Generation checks these reviewed hashes before retaining completion. Normal Git status is unavailable; the [manifest](manifest.json) retains independent HEAD comparison evidence and supporting hashes.

## Ordered decision contract

Input is a non-NULL readable room; global `weather_info.sunlight` supplies the explicitly controlled weather state. No actor, perception, privilege, descriptor, occupancy or room ownership affects this predicate.

| First satisfied condition | Return | Later dependencies not read |
|---|---|---|
| `light > 0` | FALSE | flags, sector, sunlight |
| ROOM_DARK bit set | TRUE | sector, sunlight |
| sector INSIDE or CITY | FALSE | sunlight |
| sunlight SUN_SET or SUN_DARK | TRUE | none |
| otherwise | FALSE | none |

Positive light beats even ROOM_DARK; the flag in turn beats inside/city exceptions. Zero and negative light follow the same remaining guards. Other flag bits are irrelevant. The helper reads sunlight rather than hour, sky, weather change or a clock. It has no callees, loops, recursion, callbacks, allocation, random draws, output or writes.

Constants come from [merc.h](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:192): SUN_DARK=0, SUN_RISE=1, SUN_LIGHT=2, SUN_SET=3. [ROOM_DARK](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1082) is bit A (1); [IS_SET](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1801) is bitwise AND. [Sector constants](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:1134) enumerate INSIDE=0, CITY=1, then FIELD, FOREST, HILLS, MOUNTAIN, WATER_SWIM, WATER_NOSWIM, UNUSED, AIR and DESERT through 10. Only 0 and 1 have the weather exemption. Neither the helper nor these definitions introduces conditional alternatives for this contract.

The [catalog](cases.json) and [pseudo suite](pseudo-suite.md) contain all 44 combinations of the eleven defined sectors and four sun states with zero light and no dark flag. Inside/city always return false there; every other sector is true at sunset/night and false at sunrise/day. Further cases cover light -32768, -1, 0, 1 and 32767, ROOM_DARK precedence, unrelated ROOM_SAFE, and scalar fallthrough outside enum values. Sector 99 uses the weather branch; sunlight 99 is neither sunset nor night and returns false when earlier guards fail. These scalar comparisons do not perform array indexing. NULL room violates the immediate light-read precondition; no portable outcome is claimed for it.

The ledger maps both outcomes of each of four conditions, both operands of each OR, and all five returns. INSIDE short-circuits the CITY operand; SUN_SET short-circuits SUN_DARK. Cases for CITY and SUN_DARK require their second operand; FIELD and SUN_LIGHT distinguish neither matching. Ordered dependency reads and forbidden later reads are explicit in each case. This bounded criterion covers all input equivalence classes rather than a Cartesian product of irrelevant world state.

```text
CASE handler.room_is_dark.light-boundary-1-dark-inside
GIVEN light=1, ROOM_DARK, sector INSIDE, sunlight SUN_LIGHT
WHEN room_is_dark(room) is called
THEN return FALSE after reading light
AND NEVER read flags, sector or sunlight, or emit messages

CASE handler.room_is_dark.negative-light--1-sun_dark
GIVEN light=-1, no room flags, sector FIELD, sunlight SUN_DARK
WHEN room_is_dark(room) is called
THEN evaluate light, flags, sector and sunlight in that order
AND return TRUE with all room/weather state unchanged
```

## Caller audit

Source-wide search finds six direct calls and one [declaration](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/merc.h:2250). No table takes the helper's address; it is not itself a command or scheduler callback. The following gates belong to callers, not its entry contract.

- [show_char_to_char](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:493): skips self and targets above observer trust. After `can_see` fails, it calls the helper; darkness plus **the target's** AFF_INFRARED emits `You see glowing red eyes watching YOU!\n\r` to the observer. The darkness helper itself emits nothing.
- [do_look](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:980): descriptor absence, low/sleeping position and blindness checks occur first. Only a PC without PLR_HOLYLIGHT reaches this check. Darkness prints `It is pitch black ... \n\r`, calls `show_char_to_char` and returns before parsing the look argument. The guard has no infrared exception, even though character visibility has one.
- [do_exits](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1317): after blindness checks, only an existing exit with non-NULL destination, successful room visibility and no EX_CLOSED enters formatting. Automatic mode lists directions without calling darkness. Non-auto mode calls it on the destination and selects `Too dark to tell` instead of the destination name when true. This local choice has no holylight or infrared bypass.
- [bust_a_prompt](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1423): `%r` with no room renders a space. A PC holylight bypass chooses the room name without evaluating darkness; otherwise blindness short-circuits the call. A nonblind character receives the room name if false, `darkness` if true. These are prompt substitutions, not output from the helper.
- [can_see](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2442): self, trust/invisibility, incognito, PC holylight/immortal-NPC and blindness guards precede darkness. Darkness denies character visibility unless the observer has AFF_INFRARED. Passing this gate does not bypass later invisibility, sneak or hide rules.
- [can_see_obj](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2496): PC holylight, ITEM_VIS_DEATH, blindness/potion, lit-light, invisibility and glow checks precede darkness. Here AFF_DARK_VISION, not AFF_INFRARED, is the darkness exception. Earlier light/glow returns can bypass the call entirely.

Boot initialization and [weather_update](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:475) assign global sunlight. They are producers of the scalar input, not callees. This checkout's boot and update sunrise/day assignments differ in their hour-5/hour-6 ordering; the cases deliberately specify the actual symbolic input rather than invent a wall-clock rule. Full scheduling remains a separate report item. Room flags, sector and accumulated light may come from content or movement/equipment updates; all resulting scalar classes are covered without changing or assuming a particular loaded area.

## Python adaptation and validation

The actual Python boundary is [Room.is_room_dark](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/area/Room.py:301). Supply explicit light/flags/sector and enum mappings, and control the provider used by `CharacterApi._weather()`. Its no-weather fallback is an additional Python condition, not a C oracle override. No target parity is inferred. Actor-specific visibility should be asserted at the separate character/object/description boundaries.

Source inspection established these expectations. Structural validation checks both pinned source hashes, all 44 sector/sun cells, case IDs, function-scoped citations, branch links and completed status. See [verification](verification.json). No dynamic C probe or gameplay execution is claimed. No unresolved dependencies remain for the selected environmental predicate; its six callers retain independent coverage statuses.

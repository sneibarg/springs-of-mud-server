# Mobile specials: ROM24 parity review

Scope: mobile pulse scheduling, eligibility, special binding and dispatch, and the Midgaard mayor's time script. Compared against the local `PyRom/Rom24/src` checkout. This is a comparison report; no runtime or collection changes were made for this review.

## Expected timing and verified wiring

- ROM24 `merc.h:138–143` and the collection's `enums.gameParameters` agree: four server pulses per second, mobile update every 16 pulses (four seconds), and a game hour every 240 pulses (60 seconds).
- ROM24 `special.c:879–976` starts the mayor's route at hours 6 and 20, then executes one path instruction per eligible mobile update. His remarks are scripted route instructions, rather than random idle chatter. The mayor has the sentinel flag, so generic random wandering is suppressed.
- The local special document assigns `spec_mayor` to mob `3143` in the correct area and contains the same two route strings as C. `MobileService.py:47–50` binds the assignment; spawn code copies it. Existing binding tests pass.
- Both implementations skip charmed mobiles and mobiles in empty areas without `ACT_UPDATE_ALWAYS`. Both dispatch assigned specials before the standing-position check. Sleeping alone therefore does not prevent the mayor's special from being called.

## Verified findings

### P2: Mayor wake/sleep instructions leave effective position unchanged

Python: `src/api/MobileApi.py:452,456`; position reader: `src/game/AnimateEntity.py:85–99`.
ROM24: `special.c:923,928`.

The script writes `actor.position`, but effective position reads `character_attributes.position` first. Live mobile creation initializes that attribute. A sleeping mayor processing `W` announces waking and sets the outer position to standing while remaining effectively asleep. `S` similarly leaves an effectively standing mayor awake. This makes awake/position predicates and generic mobile eligibility disagree.

Reproduced with both position fields initially sleeping: after `W`, outer position was 8, effective position remained 4, and the script advanced to instruction 1. Use the existing position setter so both fields change together.

### P2: Mayor route advances while fighting

Python: `src/api/MobileApi.py:110–113,422–481`, with the two lambdas in the `spec_mayor` collection document.
ROM24: `special.c:908–909`.

C returns directly from the mage special whenever the mayor is fighting, even if that special returns false. Python delegates, but does not finish the lambda sequence, so the time-script lambda still runs. With an active route and a mage delegate returning false, a reproduction advanced the route and queued `Hello Honey!` while fighting. If the delegate succeeds without finishing context, the route can also continue. Route execution must pause independently of whether a spell succeeds. C also initializes a due route before the combat branch, which should be preserved.

### P2: Successful mayor instructions incorrectly suppress generic mobile processing

Python: `src/api/MobileApi.py:479–481`, `src/mobile/MobileHandler.py:113–119`.
ROM24: `special.c:975–976`, `update.c:393–414`.

C returns false after every normal route instruction, allowing subsequent shop/standing/scavenge/wander processing. Python marks the context performed after a successful instruction, causing the mobile update to continue to the next mob immediately. The stock mayor is a sentinel, so random wandering remains disabled either way; this discrepancy matters for generic behavior on other mobiles using the primitive. Queuing an action and claiming the rest of a mobile pulse are distinct behaviors here.

### P2: Hour ticks run before specials instead of after them

Python: `src/game/UpdateHandler.py:57–71`.
ROM24: `update.c:1102–1124`.

When both counters expire, Python advances weather/time and runs character/object ticks before mobile specials and violence. C runs mobile specials and violence first. At an hour transition, the mayor therefore observes the new hour one mobile update earlier in Python, shifting the route start by four seconds under the configured cadence. This does not explain indefinite inactivity by itself.

### P2: Shop replenishment occurs even when a special claims the pulse

Python: `src/mobile/MobileHandler.py:111–119`.
ROM24: `update.c:393–405`.

Python replenishes shop money before executing the assigned special. C executes the special first and skips replenishment when it returns true. A shopkeeper with a successful special receives money and consumes replenishment random rolls in Python when C would do neither. This affects specials generally, though it is not the mayor's inactivity cause.

## Validation and remaining uncertainty

Ran `tests.test_mobile_special_binding` and `tests.test_mobile_special_room_access`: 11 tests passed. Ran isolated behavioral checks reproducing the stale effective position and combat route advancement. Async verification required execution outside the sandbox because sandboxed Windows socketpair initialization stalled before tests could run.

The configured cadence and local binding data do not establish a general failure to call specials. Complete inactivity in the running server remains unconfirmed: the runtime service may supply different data, the live mob may lack a binding, the area may be empty, or the game-loop thread may have stopped. `MudServer.py:32–41` logs and exits that thread after an unhandled update exception. No current server log or live process state was available in this checkout to distinguish these cases. Confirm game time advances, the live mayor has two bound lambdas, and mobile-update logs reach the mayor at hours 6/20 before treating any one of these as the root cause.

This review did not exhaustively compare the individual behaviors of all 411 special documents or every movement/gate/spell helper.

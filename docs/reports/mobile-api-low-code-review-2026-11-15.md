# MobileApi low-code review

November 15, 2026 · Server revision `9b27ec3`

The Mayor’s `Special` should own the schedule, ordered route steps, gate targets, combat delegate, and player-facing messages. Give those fields a structured representation that `springs-of-mud-designer` can edit and save. The Python runtime should execute the steps through its existing movement, posture, door, and messaging primitives.

## Findings

### P1 · The Mayor’s route only exposes part of its content

The bundled `spec_mayor` for mobile `3143` passes opening and closing hours, two encoded paths, and the `spec_cast_mage` delegate to `MobileApi.follow_time_script`. The method embeds the wake and sleep emotes, six speeches, and the door keyword `gate`. For example, `a` selects a specific greeting and `E` selects the lockup line. Changing either line today requires a backend edit. Changing where a line occurs or where a door command runs requires editing the encoded path inside a Python expression. [Bundled Mayor record](../../resources/collections/SOMDB.Specials.json#L5396) · [Route executor](../../src/api/MobileApi.py#L417)

### P1 · The Special contract and runtime binding prevent a complete edit-and-publish path

`Special.from_json` normalizes incoming keys and constructs a `Special` from them. The current model rejects both `payload` and `timedRoute`. Adding either field to the current feed can cause loading or a staged reload to fail. Extend the consumers before publishing a record with the new fields. [Special model](../../src/area/Special.py#L7) · [Special service](../../src/area/SpecialService.py#L20) · [Staged loader](../../src/server/FetchAndRegisterMixin.py#L62)

Mobile loading copies the script into the prototype and spawning copies it into the instance. `MobileHandler` also builds and retains a by-name script cache for delegates. The existing F14 finding records the effect of these copies after a reload. The by-name cache takes the first nonempty script for a name, so independently editing multiple assignments under the same name would also make a delegate’s selection ambiguous. Publish and resolve the assigned definition by stable ID. For delegated calls, use an explicit reference to a reusable definition and resolve its message keys against that definition’s payload. Keep existing name-based delegates compatible during the migration. [Prototype binding](../../src/mobile/MobileService.py#L39) · [Spawn binding](../../src/mobile/MobileFactory.py#L140) · [Delegate cache](../../src/mobile/MobileHandler.py#L424) · [F14](archive/mobile-specials-rom24-parity-2026-11-15.md#f14--reloading-specials-leaves-cached-and-copied-scripts-stale)

### P2 · Other helpers embed editable text and content identifiers

| Runtime path | Proposed cleanup |
| --- | --- |
| `pickpocket_room_player` and `nasty_combat_turn` | Move discovery, purse, and victim notices to named payload messages. Keep target selection, rolls, coin transfer, and combat decisions in the runtime. [Pickpocket](../../src/api/MobileApi.py#L500) · [Combat turn](../../src/api/MobileApi.py#L558) |
| `blow_patrol_whistle` and patrol selection | Honor the configured whistle `item_vnum`, expose the two notices as message keys, and pass the excluded patrol mobile and candidate group IDs as explicit content inputs. A probe with configured vnum `9000` rejected that equipped item and accepted `2116`. The bundled specials have no caller for the whistle helper, so this is a dormant contract defect. [Whistle](../../src/api/MobileApi.py#L608) · [Selection](../../src/api/MobileApi.py#L321) · [Group aliases](../../src/api/MobileApi.py#L873) |
| `poison_bite` and corpse devouring | Move positional and fallback text to named recipient messages as those specials migrate. `poison_bite` currently discards the `to_char` tuple entry. Audit authored values before enabling that channel so the migration preserves the intended audience. [Poison bite](../../src/api/MobileApi.py#L481) · [Corpse devouring](../../src/api/MobileApi.py#L390) |
| Trainer and practice eligibility | Audit which mobiles currently qualify through their special name or description phrases. Set the existing `ACT_TRAIN` and `ACT_PRACTICE` flags where appropriate, then remove the corresponding text heuristics after verifying command eligibility. [Trainer](../../src/api/MobileApi.py#L913) · [Practice](../../src/api/MobileApi.py#L939) |

## Proposed Mayor definition

Add an optional `payload` using the existing recipient-channel and message-key conventions, and an optional typed `timedRoute` to the existing Special record. `springs-of-mud-designer` would edit these fields through the content service alongside the rest of the record. The JSON excerpt shows the proposed service representation, omits existing metadata, abbreviates both routes, and uses a placeholder delegate reference. The migration should expand every current opcode in order and copy the full current text and door targets. [Payload model](../../src/game/GamePayload.py) · [Runtime patterns](../references/RuntimePatterns.md)

```json
{
  "name": "spec_mayor",
  "mobVnum": "3143",
  "payload": {
    "toRoom": {
      "wake": "{actor} awakens and groans loudly.",
      "greetAtHome": "{actor} says 'Hello Honey!'",
      "sleep": "{actor} lies down and falls asleep."
    }
  },
  "timedRoute": {
    "combatSpecialRef": "<stable reference to the shared mage behavior>",
    "starts": [
      {
        "hour": 6,
        "steps": [
          {"op": "setPosition", "position": "POS_STANDING", "messageKey": "wake"},
          {"op": "move", "direction": "west"},
          {"op": "message", "messageKey": "greetAtHome"},
          {"op": "door", "action": "open", "target": "gate"},
          {"op": "end"}
        ]
      },
      {
        "hour": 20,
        "steps": [
          {"op": "door", "action": "close", "target": "gate"},
          {"op": "setPosition", "position": "POS_SLEEPING", "messageKey": "sleep"},
          {"op": "end"}
        ]
      }
    ]
  }
}
```

The designer could expose one form per scheduled route, an ordered list of steps with controls for each operation, and a message editor with token help. Mobile and delegate references should resolve through selectors. The service should validate clock hours, distinct starts, operation-specific fields, direction and position values, message references, and delegate references. Normalize step message references with the same convention as `GamePayload`, so `greetAtHome` resolves to the stored `greet_at_home` key. Preserve IDs, area IDs, and mobile assignments through reads, writes, and exports. Existing records should still load with their `specialFunction` scripts. For a migrated record, require one execution entry point and clear its legacy script in the same publish operation. This adds a typed contract and a one-time route conversion. An editable text payload alone could ship sooner, with the schedule and step order still embedded in the current expression. [Collection contract guidance](../references/Collections.md)

## Runtime boundaries

- **Route execution.** Put the cursor and timing rules in a small route runner called by `MobileHandler`. Store each mobile’s cursor in its own runtime state. Reuse posture, movement, and door operations. Keep one step per mobile pulse, including failed actions and the terminator, and preserve the current ordering of schedule initialization and combat delegation. Preserve F05’s posture handling, combat pause/resume, and the ordinary mobile update after route activity. Preserve the current movement behavior during this migration, with the known F04 gate-path issue tracked separately. [Mobile update](../../src/mobile/MobileHandler.py#L200) · [Current route](../../src/api/MobileApi.py#L417) · [Bundled specials parity report](archive/mobile-specials-rom24-parity-2026-11-15.md)
- **Message delivery.** Have route and special actions resolve a message key from the current definition. Reuse `MobileApi`’s room-message path or extract its small recipient-aware rendering function once a second caller needs it. Keep observer-specific visibility tokens, room listener filtering, and asynchronous message delivery. Let the normal door command produce its own action feedback. [Room messaging](../../src/api/MobileApi.py#L749) · [Visibility and listeners](../../src/util/DisplayUtil.py#L30)
- **Publishing.** Replace the registry snapshot only after validating a proposed publish. Have existing mobiles resolve their stable Special assignment at the next pulse. Pin an active route to the definition it started with so an edit to the step list cannot redirect a running cursor. The next route should use the published definition, and the designer should state that timing when saving. A first release that uses server restart for activation should label that explicitly. [Existing reload](../../src/area/SpecialService.py#L20) · [Runtime ownership](../references/Architecture.md)

## Rollout and acceptance

1. Agree on the optional schema across `som-server-modulith`, `springs-of-mud-designer`, and the Python runtime. Verify existing Special records still load, malformed publishes leave the previous definition available, and the new shape survives a designer save, service read, and collection export.
2. Migrate only the Mayor first. Replay both schedules against the current implementation and compare step order, output and recipients, door calls, and outcomes for failed steps. Exercise F05’s wake, sleep, fight interruption, and same-pulse follow-on behavior. Save an edited line and door target, then verify the running server uses them on the next scheduled route under the chosen publication policy. Verify two assigned definitions with the same name resolve independently and a delegate reads its own payload.
3. Move the remaining content out of `MobileApi` as individual specials use the new contract. Prioritize authored messages and explicitly configured identifiers. Audit trainer-role data before retiring fallbacks.

## Review verification

Inspected the checked-in server and queried the bundled Special records with the collection CLI. In-memory probes confirmed the two rejected fields and the ignored whistle item vnum. Eleven travel integration tests and six targeted Mayor and Fido regression tests passed against the existing implementation. The designer and content-service checkouts were unavailable for this review. Their schema, UI controls, and save-to-runtime flow are proposed and still need end-to-end verification.

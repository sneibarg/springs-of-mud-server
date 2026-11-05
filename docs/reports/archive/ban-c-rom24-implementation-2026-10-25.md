# ROM24 site bans and admission implementation

Implemented October 25, 2026 against the local ROM24 `src/ban.c`, the ban-related admission branches in `src/comm.c`, and command levels in `src/interp.c`. This preserves the Python runtime's owner-loop, ordered background persistence, and content-authored messages. The C checkout was not modified.

## Acceptance criteria and behavior

1. **`ban_site` and `do_ban`:** [Wiz.py:991](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Wiz.py:991) routes `ban` to the typed site-ban policy. Empty input lists rules; optional type abbreviations resolve `all`, `newbies`, or `permit`. Both wildcard ends, setter trust, replacement, invalid input, and temporary status are represented. `permban` uses the same policy with permanent status. Existing command authorization requires L2 for ban/allow and L1 for permban (58/59 under the current maximum of 60), with immortal access and command-position checks still enforced by the shared interpreter.
2. **`allow`:** removes a named site's rule only if the actor's trust is at least the original setter's. It reports missing names, missing rules, and insufficient trust through command payloads. Legacy flat deny-list rules remain removable. A protected structured rule cannot be bypassed by also finding a legacy entry.
3. **`load_bans` / `save_bans` / `check_ban`:** [SiteBans.py](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/SiteBans.py) owns parsing, policy checks, trust constraints, and permanent-only snapshots. `GameData.from_json` loads rules at startup; `GameService.queue_save_bans` captures a detached JSON-ready snapshot for the existing ordered content worker. Temporary bans are never included in saved records. Empty permanent lists are written as `[]` so removing the last ban survives restart. Failed writes are logged and do not remove the active in-memory rule.

Admission rejects `all` bans before welcome/authentication. Conditional `permit` bans reject characters without canonical `PLR_PERMIT`, before replacing an existing connection, and admission rechecks policy after a replacement confirmation. Existing account `banned` and character `PLR_DENY` checks remain independent and continue to reject once, close transport, and avoid room/session admission. Permanent character denial still uses the existing character save path; `allow` lifts site bans rather than account/character flags.

IP address checks always remain active. When hostname rules exist, reverse lookup runs off-loop with a two-second admission timeout; lookup failure falls back to the peer address. Conditional admission checks both the actual IP and resolved hostname. Numeric-only site rules do not require reverse lookup. Existing connected players are not automatically kicked when a site ban is created, matching ROM's site-ban command rather than the former Python account-ban side effect.

## Command usage

```text
ban                              # list temporary, permanent, and legacy rules
ban 192.0.2.*                    # temporary all-connections ban
ban *.example.com permit        # temporary rule requiring PLR_PERMIT
permban *.example.com newbies   # permanent new-character policy
permban *example* all           # permanent substring match
allow .example.com              # use the stored name, without wildcard markers
```

The syntax is **site first, type second**, as in ROM. `ban` now manages sites, replacing its previous account-target behavior. Use the separate character-denial flow for character sanctions; existing account bans remain enforced. Empty input lists rules, while `list` is not a special site-ban keyword in ROM.

Names and peer hosts are compared case-insensitively. A leading `*` matches a host ending in the stored name, a trailing `*` matches a host beginning with it, both mean containment, and neither means exact matching. Types are distinct: `all` does not grant a permit exemption, and a `newbies` rule does not reject an existing character merely because it is low-level.

## Persistence and deployment contract

Permanent rules live in a new optional `GameData.bans` array. Existing documents without it load an empty structured policy. Example PATCH/GET representation:

```json
{
  "bans": [
    {"name": ".example.com", "level": 59, "type": "permit", "prefix": true, "suffix": false}
  ],
  "denyList": ["198.51.100.*"]
}
```

The existing GameData endpoint receives a PATCH containing permanent `bans` and the current legacy `denyList`; ordinary legacy deny-list updates retain their prior wire contract. The external content service must accept, retain, and return `bans` on subsequent fetches. Mocked HTTP and GameData round trips are tested; the external service schema/deployment was not modified or verified. In-memory rules take effect immediately, while persistence is queued; a failed write means durability is not guaranteed until a later successful save.

Updated `ban`, `allow`, and `permban` collection documents remove obsolete account-target guards and provide typed-rule/list messages. Command levels are unchanged. Runtime validation enforces site-rule invariants even with the older live guard arrays; missing response keys fall back to the bundled designer-editable payload. Responses are explicitly restricted to the actor channel, avoiding obsolete account-victim/wiznet messages. Loading the updated command documents remains recommended.

The bundled-message compatibility reader now lives in `interp/CommandDefaults.py` and is reused by the healer path, preserving its existing older-content fixes. Custom live message keys take precedence. Collection changes were reviewed through mandatory dry runs and verified with collection-query. Where Windows blocked atomic replacement of the open snapshot, the tool-generated output was applied in place only after semantic comparison against the expected single-document change. Prior working changes were preserved.

## Boundaries and deliberate deviations

- **New-character creation:** this Python server accepts existing account/character identities and has no nanny character-creation branch. `check_ban(host, 'newbies')` is implemented and tested, and those rules persist and list normally. The separate service that creates characters must invoke the equivalent policy check to enforce creation bans there. Rejecting existing low-level characters would not reproduce ROM's creation-only rule, so no such substitute was added. This external creation integration remains outstanding if the card requires end-to-end new-character admission.
- The local C `check_ban` has no exact-match branch and reverses the containment arguments for the both-wildcard case. Python deliberately implements functional exact and containment matches instead of reproducing these reference defects. Other reviewed branch precedence, temporary/permanent semantics, and setter-trust rules follow the C behavior.
- Legacy flat deny-list entries have no recorded setter trust; they are displayed as permanent `all` rules with legacy level zero. Existing site-deny compatibility remains supported. This does not invent missing historical ownership information.
- No new account-authentication mechanism, character-creation flow, broad nanny rewrite, or external service changes were included. The previously deferred identifiers-only authentication issue remains unchanged.

## Verification

- **17 new tests pass** in `tests/test_site_bans.py`: matcher boundaries/types/case, invalid patterns, atomic loading, temporary/permanent round trips, setter trust, command syntax and privilege levels, legacy rules, permanent HTTP snapshots/failures, pre-auth site rejection, permit exceptions and takeover protection, hostname resolution/fallback, existing account/character rejection, and older live command payloads.
- Existing focused suites pass: 14 reconnect tests, 25 prior application/login tests, 11 wizard metadata tests, 11 persistence/input tests, 7 GameData tests, 12 healer tests, and 55 object-command tests. Direct-GameData consumers were also rerun after correcting an import-cycle regression encountered during implementation.
- Final repository pass: **88 top-level unittest modules in separate interpreters; 81 passed, the same seven modules failed, 1,089 test executions**. Failing modules remain `test_area_pet_shop_resets`, `test_combat_api_dynamic_checks`, `test_combat_death_rules`, `test_combat_group_rewards`, `test_object_fountain_commands`, `test_player_handler_cast_prompt`, and `test_spell_affect_payload_messages`. These were already recorded before this implementation.
- All **340 source/test Python files parse**; `git diff --check` passes. Tests use real models and policies with mocked transport, DNS, and HTTP; no live bans, account flags, external service data, deployment, or server restart were performed.

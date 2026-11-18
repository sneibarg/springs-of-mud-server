# ROM24 parity review of scroll and output paging

This review covers the `scroll` command, the lifetime of its setting, and the path from long output through first-page delivery, continuation, dismissal, and snooping. It uses the non-Macintosh ROM24 pager in the local checkout. The `areas` command serves as a representative source of long output. Area ordering and formatting are outside scope.

## Confirmed discrepancies

### Typed commands advance an active pager

While a page is pending, press Enter and then type `look`. ROM24 advances on the empty first token. The second input dismisses the remaining output and is consumed by the pager, so the next input can reach the interpreter. Springs sends another page on any game input. If more output remains, the pager still owns the next input. In the probe, an eight-line page limit and a 25-row listing yielded an initial page plus three queued pages. Enter and `look` each sent eight rows, the pager stayed active, and neither input reached command dispatch. A whitespace-only tail can also create a pending blank page in Springs. ROM24 scans past whitespace to decide whether to clear the pager at the previous page boundary. [ROM24 input routing](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:765) · [ROM24 dismissal and whitespace scan](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2378) · [Springs input routing](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:381) · [Springs split and queue](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/messaging/MessageBus.py:52)

### Malformed numeric input can turn paging off

ROM24 parses the first token with `one_argument` and validates it with `is_number` before converting it. Springs validates the entire argument string, uses `lstrip("-")` for the digit check, and independently converts the input with a zero fallback. The repeated-minus case passes the digit check but fails conversion, so it takes the same mutation branch as an explicit `scroll 0`. Each Springs result below was reproduced through the public interpreter with paging already enabled. [ROM24 scroll parser](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:538) · [ROM24 number check](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:640) · [Springs scroll parser](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:198) · [Bundled scroll guards](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:3717)

| Input | ROM24 | Springs |
| --- | --- | --- |
| `scroll +20` | Sets 20 | Rejects as nonnumeric |
| `scroll 20 extra` | Sets 20 | Rejects as nonnumeric |
| `scroll "20"` | Sets 20 | Rejects as nonnumeric |
| `scroll --10` | Rejects and retains the current setting | Disables paging |

### Disabled status and fresh loads lose the ROM24 setting semantics

After `scroll 0`, bare `scroll` reports that long messages are unpaged in ROM24. Springs reports a page length of zero even though the bundled command has a separate `disabled` message. ROM24 initializes the internal limit to 22, displays it as 24, and saves and restores it under `Scro`. Springs defaults to unpaged output when the context key is absent and stores a change only in character context. After `scroll 20`, the probe serialized a production character and reloaded it. The original internal value was 18 and the reloaded character had no context, so paging was disabled on the fresh instance. The default and save behavior are verified differences. Their product intent remains unconfirmed. [ROM24 default](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/recycle.c:322) · [ROM24 status](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:546) · [ROM24 save](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:197) · [ROM24 load](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/save.c:1051) · [Springs setting and status](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:204) · [Springs serializer](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/CharacterService.py:94)

### Snoop omits continuation pages

ROM24 adds every displayed page to the descriptor output buffer and forwards that buffer to the snooper. Springs mirrors the first page through `MessageBus.send_to_character`. Later pages go straight to the player's connection through `send_text`, bypassing the message bus. With an active snooper, the two delivered continuation pages produced zero writes to the snooper's connection in the probe. [ROM24 page buffering](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:2401) · [ROM24 snoop forwarding](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1290) · [Springs first-page delivery](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/messaging/MessageBus.py:52) · [Springs continuation delivery](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/handlers/ConnectionHandler.py:497)

## Paging eligibility differs

ROM24 opts individual responses into paging through `page_to_char`. For example, help uses that function, while `areas` sends its rows directly. Springs applies the limit to game messages delivered through the message bus when the pager is idle, including the combined `areas` response. Consequently, `scroll 10` makes a long `areas` listing modal in Springs. ROM24 sends the full listing and accepts the next command normally. The intended eligibility policy for Springs is unconfirmed. [ROM24 help delivery](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:1805) · [ROM24 areas delivery](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/db.c:2745) · [Springs areas delivery](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/player/PlayerHandler.py:334) · [Springs paging eligibility](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/messaging/MessageBus.py:34)

## Matching paths and validation

Both implementations accept ordinary decimal values from 10 through 100 inclusive, reserve two lines, reject adjacent out-of-range inputs without changing the setting, and use zero to disable paging. Both show the first page immediately, advance on Enter, and replace the normal prompt with a continuation notice while further pages are pending. [ROM24 bounds](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:565) · [ROM24 continuation prompt](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:1224) · [Springs setting](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:218) · [Springs prompt suppression](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/messaging/MessageBus.py:87)

Ruff ran read-only against three Python files. Rule counts and concise diagnostics kept unrelated lint output out of the trace. The probes used the bundled `scroll` and `areas` commands, a synthetic area registry, the production interpreter and game loop, and test connections. All 51 focused tests passed in five isolated invocations. The message-delivery suite required the source directory on `PYTHONPATH`. ROM24 behavior was derived from source. Live socket behavior, cross-service storage, and paging preferences across body switches were outside the runtime probes.

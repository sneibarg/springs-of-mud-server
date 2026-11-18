# ROM24 parity review of the player count command

This review covers `count` from command access through session selection, viewer visibility, and the reported peak. Earlier roster work traced title ownership in `who` and `whois`. This command has a different ROM24 visibility rule for switched sessions and its own peak counter. [Earlier title review](player-title-rom24-parity-2026-11-17.md)

## Verified behavioral differences

### The population tally includes sessions hidden from the caller

ROM24 visits each `CON_PLAYING` descriptor and counts it only if the caller can see its **current body**. Self-visibility succeeds first. Trust checks gate wizinvis and out-of-room incognito before holy light can bypass ordinary sight checks. The remaining checks include blindness, darkness in the caller's room, spell invisibility, sneak, and hide. Springs counts the length of the playing-session list and never consults the caller or the session's character. Its shared visibility helper already has equivalent checks for the deterministic cases below. The probe ran the bundled command with three playing sessions and one authenticating session. [ROM24 count loop](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2082) · [ROM24 visibility](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/handler.c:2442) · [Springs count](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:898) · [Springs visibility helper](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/api/CharacterApi.py:426)

| State with three playing sessions | ROM24 tally | Springs tally |
| --- | ---: | ---: |
| All three visible | 3 | 3 |
| One target is above the caller's wizinvis trust, with or without holy light | 2 | 3 |
| One target is above the caller's incognito trust in the same room | 3 | 3 |
| The same incognito target is in a different room | 2 | 3 |
| One target is spell-invisible and the caller lacks detect invisibility | 2 | 3 |
| The caller gains detect invisibility | 3 | 3 |
| The caller is blind without holy light | 1 | 3 |
| A switched player has a hidden original and a visible controlled body | 3 | 3 |
| A switched player has a visible original and a wizinvis controlled body | 2 | 3 |

If a hidden session connects or leaves, the Springs total changes for the caller even when the character stays unobservable by room and roster rules. The tally does not identify the hidden character. Whether Springs intends a global population tally is unconfirmed. The switched cases exercise the descriptor's current body; ROM24's separate `who` path resolves the original player after its visibility check. [ROM24 WHO switched handling](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2017) · [Springs switched session](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/game/WizHandler.py:91)

### The peak observation is missing

ROM24 initializes `max_on` to zero and updates it when a player invokes `count`. It remembers the highest **visible tally observed by any caller** across calls in that process. Despite the word “today” in the message, the source contains no midnight reset or connection-time update. When the current tally ties the peak, ROM24 reports that the current total is the most so far. After a caller sees three and the other two disconnect, the next count reports one current character and a peak of three. Springs reports only one current player. Its bundled `charactersMostSoFar` payload has no caller in the runtime. Intent for dropping the peak is unconfirmed. [ROM24 peak initialization](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:71) · [ROM24 peak update and branches](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/act_info.c:2094) · [Springs output path](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/interp/commands/Info.py:898) · [Bundled peak payload](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:2623)

## Matching paths

The command is available from sleeping upward at level zero in both implementations. The probe confirmed that sleeping input executes and stunned input is rejected before tallying. The command ignores trailing words. An authenticating session is excluded. A still-connected idle character remains eligible, while a link-dead character left in the room loses its descriptor or session and leaves the tally. The comparison for idle characters assumes ordinary visibility. ROM24's separate limbo relocation can change room-dependent visibility. The Springs probe also exercised the authored `cou` and `coun` shortcuts. [ROM24 command entry](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/interp.c:117) · [ROM24 idle relocation](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/update.c:684) · [ROM24 link loss](C:/Users/scott/PycharmProjects/PyRom/Rom24/src/comm.c:985) · [Springs session selection](C:/Users/scott/PycharmProjects/springs-of-mud-server/src/server/session/SessionHandler.py:35) · [Springs command metadata](C:/Users/scott/PycharmProjects/springs-of-mud-server/resources/collections/SOMDB.Commands.json:2609)

## Validation

Ruff ran read-only on four Python files. Rule counts and concise diagnostics let the review skip unrelated lint findings and read the session and command branches directly. Probes used the bundled command, production interpreter and session registry, and in-memory connections. For the tested states, the Springs visibility helper independently produced the tally expected from the ROM24 source. All 62 focused tests passed across four isolated invocations. ROM24 was traced statically. Live connections and randomized sneak outcomes were outside the probes.

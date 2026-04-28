from __future__ import annotations

from skill.SpellSyllable import SpellSyllable


SYL_TABLE: tuple[SpellSyllable, ...] = (
    SpellSyllable(" ", " "),
    SpellSyllable("ar", "abra"),
    SpellSyllable("au", "kada"),
    SpellSyllable("bless", "fido"),
    SpellSyllable("blind", "nose"),
    SpellSyllable("bur", "mosa"),
    SpellSyllable("cu", "judi"),
    SpellSyllable("de", "oculo"),
    SpellSyllable("en", "unso"),
    SpellSyllable("light", "dies"),
    SpellSyllable("lo", "hi"),
    SpellSyllable("mor", "zak"),
    SpellSyllable("move", "sido"),
    SpellSyllable("ness", "lacri"),
    SpellSyllable("ning", "illa"),
    SpellSyllable("per", "duda"),
    SpellSyllable("ra", "gru"),
    SpellSyllable("fresh", "ima"),
    SpellSyllable("re", "candus"),
    SpellSyllable("son", "sabru"),
    SpellSyllable("tect", "infra"),
    SpellSyllable("tri", "cula"),
    SpellSyllable("ven", "nofo"),
    SpellSyllable("a", "a"),
    SpellSyllable("b", "b"),
    SpellSyllable("c", "q"),
    SpellSyllable("d", "e"),
    SpellSyllable("e", "z"),
    SpellSyllable("f", "y"),
    SpellSyllable("g", "o"),
    SpellSyllable("h", "p"),
    SpellSyllable("i", "u"),
    SpellSyllable("j", "y"),
    SpellSyllable("k", "t"),
    SpellSyllable("l", "r"),
    SpellSyllable("m", "w"),
    SpellSyllable("n", "i"),
    SpellSyllable("o", "a"),
    SpellSyllable("p", "s"),
    SpellSyllable("q", "d"),
    SpellSyllable("r", "f"),
    SpellSyllable("s", "g"),
    SpellSyllable("t", "h"),
    SpellSyllable("u", "j"),
    SpellSyllable("v", "z"),
    SpellSyllable("w", "x"),
    SpellSyllable("x", "n"),
    SpellSyllable("y", "l"),
    SpellSyllable("z", "k"),
)


class SpellSpeech:
    @staticmethod
    def translate_spell_name(spell_name: str) -> str:
        source = str(spell_name or "")
        if not source:
            return ""

        parts: list[str] = []
        index = 0
        while index < len(source):
            matched = False
            remaining = source[index:]
            for syllable in SYL_TABLE:
                if remaining.startswith(syllable.old):
                    parts.append(syllable.new)
                    index += len(syllable.old) or 1
                    matched = True
                    break
            if not matched:
                parts.append(source[index])
                index += 1
        return "".join(parts)

    @staticmethod
    def utterance(spell_name: str, speaker_name: str, translated: bool = False) -> str:
        spoken = SpellSpeech.translate_spell_name(spell_name) if translated else str(spell_name or "")
        speaker = str(speaker_name or "Someone")
        return f"{speaker} utters the words, '{spoken}'.\r\n"

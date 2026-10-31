from __future__ import annotations

from api.GameApi import GameApi
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil


class CommunicationsUtil:
    @staticmethod
    def pmote_text(text: str, name: str) -> str:
        """Apply ROM's case-sensitive name/possessive scan for one recipient."""
        start = text.find(name) if name else -1
        if start < 0:
            return text
        output, pending, matched = [text[:start]], '', 0
        for letter in text[start:]:
            if matched == len(name):
                if letter == "'":
                    output.append('r')
                    continue
                if letter == 's':
                    matched = 0
                    continue
                matched = 0
            if letter == name[matched]:
                matched += 1
                if matched == len(name):
                    output.append('you')
                    pending = ''
                else:
                    pending += letter
                continue
            output.extend((pending, letter))
            pending, matched = '', 0
        return ''.join(output)

    @staticmethod
    def parse_argument(raw_result, parameters) -> str:
        text = (raw_result if isinstance(raw_result, str) else "").strip()
        if text:
            return text
        return " ".join(parameters or []).strip()

    @staticmethod
    def split_first(argument: str) -> tuple[str, str]:
        first, rest = InterpUtil.one_argument(argument or "")
        return first, rest.strip()

    @staticmethod
    def has_comm(character, comm_flags, name: str) -> bool:
        if comm_flags is None or name not in comm_flags.__members__:
            return False
        raw = GenericUtil.to_int(character.status_flags.comm, 0)
        return GameApi.is_set(raw, int(comm_flags[name].value))

    @staticmethod
    def set_comm(character, comm_flags, name: str, enabled: bool):
        if comm_flags is None or name not in comm_flags.__members__:
            return
        bit = int(comm_flags[name].value)
        if enabled:
            character.status_flags.set_flag("comm", bit)
            return
        character.status_flags.unset_flag("comm", bit)

    @staticmethod
    def ensure_message_break(text: str) -> str:
        rendered = str(text or "")
        if rendered and not rendered.endswith("\r\n"):
            rendered += "\r\n"
        return rendered

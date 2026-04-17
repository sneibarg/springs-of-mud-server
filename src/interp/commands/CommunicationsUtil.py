from __future__ import annotations

from game.GameMacros import GameMacros
from game.GenericUtil import GenericUtil
from interp.InterpUtil import InterpUtil


class CommunicationsUtil:
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
    def flags_to_int(raw) -> int:
        value = GenericUtil.to_int(raw, None)
        if value is not None:
            return value
        return GameMacros.convert_flags(str(raw or "0"))

    @staticmethod
    def int_to_letters(value: int) -> str:
        if value <= 0:
            return ""
        out = []
        for bit in range(26):
            if value & (1 << bit):
                out.append(chr(ord("A") + bit))
        return "".join(out)

    @staticmethod
    def has_comm(character, comm_flags, name: str) -> bool:
        if comm_flags is None or not hasattr(comm_flags, name):
            return False
        raw = CommunicationsUtil.flags_to_int(getattr(character.character_flags, "comm", "") or "0")
        return (raw & int(getattr(comm_flags, name).value)) != 0

    @staticmethod
    def set_comm(character, comm_flags, name: str, enabled: bool):
        if comm_flags is None or not hasattr(comm_flags, name):
            return
        bit = int(getattr(comm_flags, name).value)
        raw = CommunicationsUtil.flags_to_int(getattr(character.character_flags, "comm", "") or "0")
        if enabled:
            raw |= bit
        else:
            raw &= ~bit
        character.character_flags.comm = CommunicationsUtil.int_to_letters(raw)

    @staticmethod
    def append_tell_buffer(character, line: str):
        if getattr(character, "context", None) is None:
            character.context = {}
        history = character.context.get("tell_buffer", [])
        if not isinstance(history, list):
            history = []
        history.append(line)
        character.context["tell_buffer"] = history[-50:]

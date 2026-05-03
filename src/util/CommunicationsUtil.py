from __future__ import annotations

from game.GameMacros import GameMacros
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil


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
    def has_comm(character, comm_flags, name: str) -> bool:
        if comm_flags is None or not hasattr(comm_flags, name):
            return False
        raw = GenericUtil.to_int(getattr(character.status_flags, "comm", 0), 0)
        return GameMacros.is_set(raw, int(getattr(comm_flags, name).value))

    @staticmethod
    def set_comm(character, comm_flags, name: str, enabled: bool):
        if comm_flags is None or not hasattr(comm_flags, name):
            return
        bit = int(getattr(comm_flags, name).value)
        if enabled:
            character.status_flags.set_flag("comm", bit)
            return
        character.status_flags.unset_flag("comm", bit)

    @staticmethod
    def append_tell_buffer(character, line: str):
        if getattr(character, "context", None) is None:
            character.context = {}
        history = character.context.get("tell_buffer", [])
        if not isinstance(history, list):
            history = []
        history.append(line)
        character.context["tell_buffer"] = history[-50:]

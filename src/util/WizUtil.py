from __future__ import annotations

from typing import Any

from util.InterpUtil import InterpUtil


class WizUtil:
    @staticmethod
    def argument_text(raw_result: Any, parameters: list[str] | None) -> str:
        if isinstance(raw_result, str) and raw_result.strip():
            return raw_result.strip()
        return " ".join(parameters or []).strip()

    @staticmethod
    def split_argument(argument: str) -> tuple[str, str]:
        arg, rest = InterpUtil.one_argument(argument or "")
        return arg, rest.strip()

    @staticmethod
    def name_matches(query: str, candidate: str) -> bool:
        q = (query or "").strip().lower()
        c = (candidate or "").strip().lower()
        if not q or not c:
            return False
        return c == q or c.startswith(q)

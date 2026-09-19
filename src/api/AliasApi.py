from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from interp.InterpView import InterpView


@dataclass(frozen=True)
class AliasSubstitution:
    command: str
    message: str = ""
    message_key: str = ""


class AliasApi:
    MAX_ALIAS = 5
    MAX_INPUT_LENGTH = 256
    ALIASES_KEY = "aliases"

    @classmethod
    def alias_parts(cls, view: "InterpView") -> tuple[str, str]:
        alias_name, replacement = cls._one_argument(cls._argument_text(view))
        return alias_name.strip().lower(), replacement.strip()

    @classmethod
    def aliases(cls, character) -> dict[str, str]:
        context = cls._context(character)
        character_aliases = getattr(character, cls.ALIASES_KEY, None)
        raw = context.get(cls.ALIASES_KEY, character_aliases)
        if character_aliases:
            raw = character_aliases

        aliases = cls._normalize_aliases(raw)
        context[cls.ALIASES_KEY] = aliases
        if hasattr(character, cls.ALIASES_KEY):
            setattr(character, cls.ALIASES_KEY, aliases)
        return aliases

    @classmethod
    def _normalize_aliases(cls, raw) -> dict[str, str]:
        if isinstance(raw, dict):
            return {str(key).strip().lower(): str(value) for key, value in raw.items() if str(key).strip()}
        if isinstance(raw, list):
            aliases = {}
            for entry in raw:
                if isinstance(entry, dict):
                    name = str(entry.get("name", entry.get("alias", "")) or "").strip().lower()
                    replacement = str(entry.get("replacement", entry.get("substitution", "")) or "")
                    if name:
                        aliases[name] = replacement
            return aliases
        return {}

    @classmethod
    def alias_tokens(cls, view: "InterpView") -> dict[str, Any]:
        alias_name, replacement = cls.alias_parts(view)
        if not replacement:
            replacement = cls.aliases(view.context.character).get(alias_name, "")
        return {
            "alias": alias_name,
            "replacement": replacement,
            "s": alias_name,
            "t": replacement,
        }

    @classmethod
    def reserved_alias_word(cls, view: "InterpView") -> bool:
        alias_name, _replacement = cls.alias_parts(view)
        return bool(alias_name) and (alias_name == "alias" or alias_name.startswith("una"))

    @classmethod
    def lookup_missing(cls, view: "InterpView") -> bool:
        alias_name, replacement = cls.alias_parts(view)
        return bool(alias_name) and not replacement and alias_name not in cls.aliases(view.context.character)

    @classmethod
    def invalid_alias_substitution(cls, view: "InterpView") -> bool:
        _alias_name, replacement = cls.alias_parts(view)
        command, _rest = cls._one_argument(replacement)
        return bool(command) and (command.startswith("delete") or command.startswith("prefix"))

    @classmethod
    def alias_limit_reached(cls, view: "InterpView") -> bool:
        alias_name, replacement = cls.alias_parts(view)
        aliases = cls.aliases(view.context.character)
        return bool(alias_name and replacement and alias_name not in aliases and len(aliases) >= cls.MAX_ALIAS)

    @classmethod
    def set_alias(cls, character, alias_name: str, replacement: str) -> bool:
        aliases = cls.aliases(character)
        existing = alias_name in aliases
        aliases[alias_name] = replacement
        return existing

    @classmethod
    def remove_alias(cls, character, alias_name: str) -> bool:
        aliases = cls.aliases(character)
        if alias_name not in aliases:
            return False
        del aliases[alias_name]
        return True

    @classmethod
    def unalias_name(cls, view: "InterpView") -> str:
        alias_name, _replacement = cls._one_argument(cls._argument_text(view))
        return alias_name.strip().lower()

    @classmethod
    def unalias_no_argument(cls, view: "InterpView") -> bool:
        return not cls.unalias_name(view)

    @classmethod
    def unalias_missing(cls, view: "InterpView") -> bool:
        alias_name = cls.unalias_name(view)
        return bool(alias_name) and alias_name not in cls.aliases(view.context.character)

    @classmethod
    def substitute_command(cls, character, command_text: str) -> AliasSubstitution:
        original = str(command_text or "")
        if not original.strip() or character is None or cls._is_npc(character):
            return AliasSubstitution(original)

        command_name, rest = cls._one_argument(original)
        if not command_name or command_name in ("alias", "prefix") or command_name.startswith("una"):
            return AliasSubstitution(original)

        replacement = cls.aliases(character).get(command_name)
        if replacement is None:
            return AliasSubstitution(original)

        expanded = replacement if not rest else f"{replacement} {rest}"
        if len(expanded) <= cls.MAX_INPUT_LENGTH - 1:
            return AliasSubstitution(expanded)
        return AliasSubstitution(
            expanded[: cls.MAX_INPUT_LENGTH - 1],
            "Alias substitution too long. Truncated.\r\n",
            "substitution_too_long",
        )

    @staticmethod
    def _context(character) -> dict[str, Any]:
        current = getattr(character, "context", None)
        if not isinstance(current, dict):
            current = {}
            setattr(character, "context", current)
        return current

    @staticmethod
    def _is_npc(character) -> bool:
        try:
            from api.CharacterApi import CharacterApi

            return CharacterApi.is_npc(character)
        except Exception:
            return str(getattr(character, "role", "") or "").lower() == "mobile"

    @staticmethod
    def _argument_text(view: "InterpView") -> str:
        context = view.context
        result = getattr(context, "result", "")
        if isinstance(result, str) and result.strip():
            return result.strip()
        return " ".join(getattr(context, "parameters", []) or []).strip()

    @staticmethod
    def _one_argument(argument: str) -> tuple[str, str]:
        text = str(argument or "").lstrip()
        if not text:
            return "", ""
        if text[0] in ("'", '"'):
            quote = text[0]
            text = text[1:]
            end = text.find(quote)
            if end < 0:
                return text.lower(), ""
            return text[:end].lower(), text[end + 1 :].lstrip()
        parts = text.split(maxsplit=1)
        return parts[0].lower(), parts[1] if len(parts) > 1 else ""

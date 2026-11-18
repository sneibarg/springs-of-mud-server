from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from api.CharacterApi import CharacterApi
from interp.Context import Context
from util.InterpUtil import InterpUtil

if TYPE_CHECKING:
    from interp.InterpView import InterpView


@dataclass(frozen=True)
class AliasSubstitution:
    command: str
    message: str = ""
    message_key: str = ""
    message_command: str = "alias"


class AliasApi:
    MAX_ALIAS = 5
    MAX_INPUT_LENGTH = 256
    ALIASES_KEY = "aliases"

    @classmethod
    def alias_parts(cls, view: "InterpView") -> tuple[str, str]:
        raw = view.context.result
        argument = raw if isinstance(raw, str) and raw else InterpUtil.argument_text(view)
        alias_name, replacement = InterpUtil.one_argument(argument.replace("~", "-"))
        return alias_name.strip().lower(), replacement

    @staticmethod
    def owner(character):
        seen = set()
        while character is not None and id(character) not in seen:
            seen.add(id(character))
            controller = (getattr(character, "context", None) or {}).get("controller_original")
            if controller is None:
                return character
            character = controller
        return None

    @classmethod
    def aliases(cls, character) -> dict[str, str]:
        character = cls.owner(character)
        if character is None or CharacterApi.is_npc(character):
            return {}
        context = Context.for_character(character)
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
        replacement = replacement.lower()
        return bool(replacement) and any(word.startswith(replacement) for word in ("delete", "prefix"))

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
        alias_name, _replacement = InterpUtil.one_argument(InterpUtil.argument_text(view))
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
        if not original.strip() or character is None:
            return AliasSubstitution(original)
        body = character
        character = cls.owner(body)
        if character is None:
            return AliasSubstitution(original)
        command_name, rest = InterpUtil.one_argument(original)
        prefix = str(Context.for_character(character).get('prefix', '') or '')
        warning = ''
        if prefix and command_name not in ('prefix', 'pref', 'prefi'):
            expanded = f'{prefix} {original}'
            if len(expanded) >= cls.MAX_INPUT_LENGTH:
                warning = 'Line too long, prefix not processed.\r\n'
            else:
                original = expanded
        result = AliasSubstitution(original, warning, 'overflow' if warning else '', 'prefix')
        if CharacterApi.is_npc(character):
            return result
        command_name, rest = InterpUtil.one_argument(original)
        raw_lower = original.lower()
        if (not command_name or not raw_lower.startswith(command_name)
                or raw_lower.startswith(('alias', 'una', 'prefix')) or command_name in ('pref', 'prefi')):
            return result

        replacement = cls.aliases(character).get(command_name)
        if replacement is None:
            return result

        expanded = replacement if not rest else f"{replacement} {rest}"
        if len(expanded) <= cls.MAX_INPUT_LENGTH - 1:
            return AliasSubstitution(expanded, warning, 'overflow' if warning else '', 'prefix')
        if body is not character:
            return AliasSubstitution(expanded[: cls.MAX_INPUT_LENGTH - 1], warning,
                                     'overflow' if warning else '', 'prefix')
        return AliasSubstitution(
            expanded[: cls.MAX_INPUT_LENGTH - 1],
            warning + "Alias substitution too long. Truncated.\r\n",
            "" if warning else "substitution_too_long",
        )

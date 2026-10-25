"""Shared guard content contract for command and ability definitions."""

from typing import Any

from util.GenericUtil import GenericUtil


def normalize_guards(value: Any) -> list[dict[str, Any]]:
    """Normalize designer-authored guard fields without compiling predicates.

    Accept list entries as predicate strings or field mappings. Ignore malformed
    entries, preserve shorthand shape, and return fresh runtime mappings.
    """
    if not isinstance(value, list):
        return []

    normalized: list[dict[str, Any]] = []
    for entry in value:
        if isinstance(entry, str):
            text = entry.strip()
            if text:
                normalized.append({"predicate": text})
            continue
        if not isinstance(entry, dict):
            continue
        check = GenericUtil.camel_to_snake_case(entry)
        predicate = str(check.get("predicate", check.get("lambda", "")) or "").strip()
        if not predicate:
            continue
        raw_message_key = str(check.get("message_key", "") or "").strip()
        normalized_message_key = ""
        if raw_message_key:
            normalized_message_key = next(iter(GenericUtil.camel_to_snake_case({raw_message_key: ""}).keys()), raw_message_key)
        normalized.append(
            {
                "predicate": predicate,
                "channel": str(check.get("channel", "") or "").strip(),
                "message_key": normalized_message_key,
                "fallback": str(check.get("fallback", "") or ""),
                "token_factory": str(check.get("token_factory", "") or "").strip(),
            }
        )
    return normalized

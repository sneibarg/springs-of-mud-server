import re
from typing import Optional, Union, Any


class CommandUtil:
    pass

    @staticmethod
    def _coerce_entries(payload, fallback_keyword):
        if payload is None:
            return []
        if isinstance(payload, list):
            return payload
        if isinstance(payload, str):
            return [{"keyword": fallback_keyword, "level": 0, "text": payload}]
        if isinstance(payload, dict):
            if any(k.lower() in ("keyword", "text", "level") for k in payload.keys()):
                return [payload]

            for key in ("items", "results", "content", "data"):
                value = payload.get(key)
                if isinstance(value, list):
                    return value

            embedded = payload.get("_embedded")
            if isinstance(embedded, dict):
                for value in embedded.values():
                    if isinstance(value, list):
                        return value
        return []

    @staticmethod
    def find_json_object_by_name(name: str, commands: dict) -> Optional[dict]:
        if not commands:
            return None
        for command in commands:
            if name in command.get('shortcuts', []):
                return command
            if command.get('name') == name:
                return command
        return None

    @staticmethod
    def normalize_help_entries(help_payload, fallback_keyword: str) -> list[dict]:
        fallback_keyword = (fallback_keyword or "").strip().lower()
        normalized = []
        for raw in CommandUtil._coerce_entries(help_payload, fallback_keyword):
            if not isinstance(raw, dict):
                continue

            lowered = {str(k).lower(): v for k, v in raw.items()}
            keyword = str(lowered.get("keyword", fallback_keyword) or fallback_keyword).strip().lower()
            text = str(lowered.get("text", "") or "")
            level_raw = lowered.get("level", 0)
            try:
                level = int(level_raw)
            except (TypeError, ValueError):
                level = 0
            normalized.append({
                "keyword": keyword,
                "level": level,
                "text": text
            })

        return normalized

    @staticmethod
    def is_name_match(query: str, keyword: str) -> bool:
        q_words = (query or "").strip().lower().split()
        k_words = (keyword or "").strip().lower().split()
        if not q_words or not k_words:
            return False
        return all(any(k.startswith(q) for k in k_words) for q in q_words)

    @staticmethod
    def extract_parameters(command_registry, command: str) -> Union[tuple[Any, str], tuple[None, None]]:
        for cmd_json in command_registry.registry.values():
            shortcuts = cmd_json['shortcuts'].split(", ")
            if command in shortcuts or command.startswith(cmd_json['name']):
                return cmd_json, ' '.join(re.split(' ', command)[1:]).strip()
        return None, None

    @staticmethod
    def append_entries(entries: list[dict], topic: str) -> list[str]:
        found = False
        output_parts: list[str] = []
        for help_entry in entries:
            keyword = str(help_entry.get("keyword", "")).strip().lower()
            if not keyword:
                continue
            if not CommandUtil.is_name_match(topic, keyword):
                continue

            level = int(help_entry.get("level", 0))
            if found:
                output_parts.append("\n\r============================================================\n\r\n\r")

            if level >= 0 and topic != "imotd":
                output_parts.append(str(help_entry.get("keyword", "")))
                output_parts.append("\n\r")

            text = str(help_entry.get("text", ""))
            if text.startswith("."):
                text = text[1:]
            output_parts.append(text)

        return output_parts

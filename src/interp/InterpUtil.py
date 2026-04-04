from typing import Optional, Union, Any


class InterpUtil:
    pass

    @staticmethod
    def command_attr(command, attr_name: str, default=None):
        if isinstance(command, dict):
            return command.get(attr_name, default)
        return getattr(command, attr_name, default)

    @staticmethod
    def shortcut_tokens(shortcuts) -> list[str]:
        if shortcuts is None:
            return []
        if isinstance(shortcuts, list):
            values = shortcuts
        else:
            values = str(shortcuts).split(",")

        tokens = []
        for value in values:
            token = str(value).strip().lower()
            if token:
                tokens.append(token)
        return tokens

    @staticmethod
    def coerce_entries(payload, fallback_keyword):
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
    def find_json_object_by_name(name: str, commands) -> Optional[Any]:
        for command in commands:
            shortcuts = InterpUtil.shortcut_tokens(command.shortcuts)
            if name in shortcuts:
                return command
            if command.name == name:
                return command
        return None

    @staticmethod
    def normalize_help_entries(help_payload, fallback_keyword: str) -> list[dict]:
        fallback_keyword = (fallback_keyword or "").strip().lower()
        normalized = []
        for raw in InterpUtil.coerce_entries(help_payload, fallback_keyword):
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
    def extract_parameters(interp_registry, command: str) -> Union[tuple[Any, str], tuple[None, None]]:
        normalized = " ".join((command or "").split()).strip()
        if not normalized:
            return None, None

        parts = normalized.split(" ", 1)
        command_text = parts[0].lower()
        parameters = parts[1].strip() if len(parts) > 1 else ""
        get_or_none = getattr(interp_registry, "get_or_none", None)
        if callable(get_or_none):
            exact = get_or_none(name=command_text)
            if exact is not None:
                return exact, parameters

        for cmd in interp_registry.all_commands():
            if not cmd.name:
                continue

            shortcuts = InterpUtil.shortcut_tokens(cmd.name)
            if command_text == cmd.name or command_text in shortcuts:
                return cmd, parameters
        return None, None


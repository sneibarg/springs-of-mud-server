def victim_name(entity, is_npc):
    if is_npc(entity):
        return str(getattr(entity, "short_description", "") or getattr(entity, "name", "someone"))
    return str(getattr(entity, "name", "someone"))


def format_template(text, name):
    """Preserve ROM-derived %s item templates, including malformed fallbacks."""
    raw = str(text or "")
    if "%s" in raw:
        try:
            return raw % name
        except Exception:
            return raw.replace("%s", name)
    return raw

class DisplayUtil:
    @staticmethod
    def entity_name(entity, *, is_npc) -> str:
        if entity is None:
            return "someone"
        if is_npc(entity):
            return str(getattr(entity, "short_description", "") or getattr(entity, "name", "someone"))
        return str(getattr(entity, "name", "someone"))

    @staticmethod
    def display_effect_message(message) -> str:
        text = str(message or "").strip()
        if len(text) >= 2 and text.startswith("!") and text.endswith("!"):
            return ""
        return text

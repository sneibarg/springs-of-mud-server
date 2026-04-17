from __future__ import annotations

from game.GenericUtil import GenericUtil


class FightUtil:
    @staticmethod
    def parse_cast_argument(raw_result, parameters) -> tuple[str, str]:
        text = (raw_result if isinstance(raw_result, str) else "").strip()
        if not text:
            text = " ".join(parameters or []).strip()
        if not text:
            return "", ""

        if text[0] in ("'", '"'):
            quote = text[0]
            end = text.find(quote, 1)
            if end > 1:
                return text[1:end].strip().lower(), text[end + 1:].strip()
        parts = text.split(maxsplit=1)
        spell = parts[0].strip().lower()
        target = parts[1].strip() if len(parts) > 1 else ""
        return spell, target

    @staticmethod
    def spell_handler_name(spell_name: str) -> str:
        return "spell." + spell_name.strip().lower().replace(" ", "_")

    @staticmethod
    def level_for_class(skill, character) -> int:
        class_name = str(getattr(getattr(character, "character_class", None), "name", "") or "").strip().lower()
        level_map = getattr(skill, "level_by_class", {}) or {}
        if class_name in level_map:
            return GenericUtil.to_int(level_map.get(class_name), 99)
        return GenericUtil.to_int(level_map.get("mage", 99), 99)

    @staticmethod
    def min_mana(skill) -> int:
        return max(0, GenericUtil.to_int(getattr(skill, "min_mana", 0), 0))

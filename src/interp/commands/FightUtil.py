from __future__ import annotations

from game.GenericUtil import GenericUtil


class FightUtil:
    @staticmethod
    def parse_action_argument(raw_result, parameters) -> str:
        text = (raw_result if isinstance(raw_result, str) else "").strip()
        if text:
            return text
        return " ".join(parameters or []).strip()

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

    @staticmethod
    def find_spell(spell_registry, spell_name: str):
        if spell_registry is None:
            return None
        want_handler = FightUtil.spell_handler_name(spell_name)
        for spell in spell_registry.all_spells():
            handler_id = str(getattr(spell, "handler_id", "") or "").strip().lower()
            name = str(getattr(spell, "name", "") or "").strip().lower()
            if handler_id == want_handler or name == spell_name:
                return spell
        return None

    @staticmethod
    def find_spell_skill(skill_registry, character, spell_name: str):
        want_handler = FightUtil.spell_handler_name(spell_name)
        best = None
        for skill in skill_registry.all_skills():
            handler_id = str(getattr(skill, "handler_id", "") or "").strip().lower()
            if handler_id in ("", "spell.none"):
                continue
            if handler_id == want_handler or str(getattr(skill, "name", "") or "").strip().lower() == spell_name:
                best = skill
                req = FightUtil.level_for_class(skill, character)
                if int(getattr(character, "level", 0)) >= req:
                    return skill
        return best

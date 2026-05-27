from __future__ import annotations

from util.GenericUtil import GenericUtil


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
        wanted = str(spell_name or "").strip().lower()
        for skill in list(getattr(character, "spells", []) or []):
            name = str(getattr(skill, "name", skill.get("name", "") if isinstance(skill, dict) else "") or "").strip().lower()
            if name == wanted:
                return skill
        if skill_registry is None:
            return None
        all_skills = getattr(skill_registry, "all_skills", None)
        if not callable(all_skills):
            return None
        for skill in all_skills():
            if str(getattr(skill, "name", "") or "").strip().lower() == wanted:
                return skill
        return None

    @staticmethod
    def normalize_damage_type_name(dam_type: str | None) -> str:
        text = str(dam_type or "").strip().upper()
        if not text or text == "NONE":
            return "DAM_NONE"
        if text.startswith("DAM_"):
            return text
        return f"DAM_{text}"

    @staticmethod
    def set_fighting_position(entity, PositionsEnum) -> None:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            attrs.position = PositionsEnum.POS_FIGHTING.value
            return
        setattr(entity, "position", PositionsEnum.POS_FIGHTING.value)

    @staticmethod
    def entity_position_value(entity) -> int:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None and hasattr(attrs, "position"):
            return GenericUtil.to_int(getattr(attrs, "position", 0), 0)
        if hasattr(entity, "position"):
            return GenericUtil.to_int(getattr(entity, "position", 0), 0)
        return GenericUtil.to_int(getattr(entity, "start_pos", 0), 0)

    @staticmethod
    def dynamic_combat_bonus(entity, *names: str) -> int:
        total = 0
        for name in names:
            value = getattr(entity, name, None)
            if value is not None:
                total += GenericUtil.to_int(value, 0)
        return total

    @staticmethod
    def interpolate(level: int, value_00: int, value_32: int) -> int:
        return value_00 + level * (value_32 - value_00) // 32

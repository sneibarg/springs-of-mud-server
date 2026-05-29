from util.GenericUtil import GenericUtil
from api.CharacterApi import CharacterApi

class SkillUtil:
    @staticmethod
    def _weapon_enum_skill_name(enum_name: str) -> str:
        text = str(enum_name or "").strip().lower()
        if text.startswith("weapon_"):
            text = text[len("weapon_"):]
        return "hand to hand" if text == "exotic" else text

    @staticmethod
    def weapon_skill_name(weapon, weapon_class_names=None) -> str:
        if weapon is None:
            return "hand to hand"

        raw = getattr(weapon, "value0", None)
        token = str(raw or "").strip()
        members = getattr(weapon_class_names, "__members__", {}) or {}

        try:
            weapon_class = CharacterApi.get_enum("weaponClass")
        except RuntimeError:
            weapon_class = None

        numeric = GenericUtil.to_int(raw, None)
        if numeric is not None and weapon_class is not None:
            for enum_name in members.keys():
                member = getattr(weapon_class, enum_name, None)
                if member is not None and int(getattr(member, "value", member)) == numeric:
                    return SkillUtil._weapon_enum_skill_name(enum_name)

        upper_token = token.upper()
        if upper_token in members:
            return SkillUtil._weapon_enum_skill_name(upper_token)

        lowered = token.lower()
        if lowered in {SkillUtil._weapon_enum_skill_name(name) for name in members.keys()}:
            return lowered
        return ""

    @staticmethod
    def active_melee_skill_name(weapon, weapon_class_names=None) -> str:
        return SkillUtil.weapon_skill_name(weapon, weapon_class_names) or "hand to hand"


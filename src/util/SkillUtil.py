from util.GenericUtil import GenericUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros


class SkillUtil:
    pass

    @staticmethod
    def is_practice_trainer(mob, practice_bit: int) -> bool:
        mob_flags = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "act", 0), 0)
        if practice_bit and CharacterMacros.is_set(mob_flags, practice_bit):
            return True

        special_name = str(getattr(mob, "special_name", "") or "").strip().lower()
        if special_name == "spec_cast_adept":
            return True

        long_description = str(getattr(mob, "long_description", "") or "").strip().lower()
        if "help you practice" in long_description or "ready to help you practice" in long_description:
            return True

        return False

    @staticmethod
    def find_character_skill(skills: list[dict], wanted: str) -> dict | None:
        query = str(wanted or "").strip().lower()
        if not query:
            return None

        prefix_match = None
        for skill in skills or []:
            skill_name = str(skill.get("name", "") or "").strip().lower()
            if not skill_name:
                continue
            if skill_name == query:
                return skill
            if prefix_match is None and skill_name.startswith(query):
                prefix_match = skill
        return prefix_match

    @staticmethod
    def practice_class_name(character: Character) -> str:
        return str(getattr(getattr(character, "character_class", None), "name", "") or "").strip().lower()

    @staticmethod
    def practice_adept(character: Character) -> int:
        adept = GenericUtil.to_int(getattr(getattr(character, "character_class", None), "skill_adept", 75), 75)
        return adept if adept > 0 else 75

    @staticmethod
    def practice_gain(character: Character, rating: int) -> int:
        intelligence = GenericUtil.to_int(getattr(getattr(character, "character_attributes", None), "intelligence", 0), 0)
        learn_bonus = GenericUtil.to_int(
            CharacterMacros.get_attribute_bonus("intelligence", str(intelligence)).get("learn", 0), 0)
        rating = max(1, GenericUtil.to_int(rating, 1))
        gain = learn_bonus // rating
        return max(1, gain)
import random

from player.CharacterAdvancement import CharacterAdvancement
from util.GenericUtil import GenericUtil
from player.Character import Character
from api.CharacterApi import CharacterApi


class SkillUtil:
    @staticmethod
    def is_practice_trainer(mob, practice_bit: int) -> bool:
        mob_flags = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "act", 0), 0)
        if practice_bit and CharacterApi.is_set(mob_flags, practice_bit):
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
        intelligence = GenericUtil.to_int(getattr(getattr(character, "character_attributes", None), "intelligence", 0),
                                          0)
        learn_bonus = GenericUtil.to_int(
            CharacterApi.get_attribute_bonus("intelligence", str(intelligence)).get("learn", 0), 0)
        rating = max(1, GenericUtil.to_int(rating, 1))
        gain = learn_bonus // rating
        return max(1, gain)

    @staticmethod
    def check_improve(ch: Character, skill_id: str, success: bool, multiplier: int = 1) -> None:
        if CharacterApi.is_npc(ch):
            return

        registry = CharacterApi.get_registry()
        ability = getattr(registry, "skill_registry", None).get_or_none(id=skill_id) if getattr(registry, "skill_registry", None) is not None else None
        if ability is None and getattr(registry, "spell_registry", None) is not None:
            ability = registry.spell_registry.get_or_none(id=skill_id)
        if ability is None:
            return

        class_name = SkillUtil.practice_class_name(ch)
        required_level = CharacterApi.skill_value_for_class(getattr(ability, "level_by_class", {}) or {}, class_name, 99)
        rating = max(0, CharacterApi.skill_value_for_class(getattr(ability, "rating_by_class", {}) or {}, class_name, 0))
        learned_entry = SkillUtil._find_learned_entry(ch, str(getattr(ability, "name", "") or ""))
        learned = SkillUtil._learned_level(learned_entry)
        adept = SkillUtil.practice_adept(ch)

        if ch.level < required_level or rating == 0 or learned <= 0 or learned >= adept:
            return

        intelligence = GenericUtil.to_int(getattr(getattr(ch, "character_attributes", None), "intelligence", 0), 0)
        learn_bonus = GenericUtil.to_int(
            CharacterApi.get_attribute_bonus("intelligence", str(intelligence)).get("learn", 0), 0
        )

        multiplier = max(1, GenericUtil.to_int(multiplier, 1))
        chance = (10 * learn_bonus) // (multiplier * rating * 4) + GenericUtil.to_int(ch.level, 0)

        if random.randint(1, 1000) > chance:
            return

        if success:
            chance = max(5, min(adept - learned, 95))
            if random.randint(1, 100) < chance:
                SkillUtil._set_learned_level(learned_entry, min(learned + 1, adept))
                CharacterAdvancement.gain_experience(ch, 2 * rating)
        else:
            chance = max(5, min(learned // 2, 30))
            if random.randint(1, 100) < chance:
                SkillUtil._set_learned_level(learned_entry, min(learned + random.randint(1, 3), adept))
                CharacterAdvancement.gain_experience(ch, 2 * rating)

    @staticmethod
    def _find_learned_entry(character: Character, ability_name: str):
        wanted = str(ability_name or "").strip().lower()
        if not wanted:
            return None

        for collection_name in ("skills", "spells"):
            for entry in list(getattr(character, collection_name, []) or []):
                if isinstance(entry, dict):
                    name = str(entry.get("name", "") or "").strip().lower()
                else:
                    name = str(getattr(entry, "name", "") or "").strip().lower()
                if name == wanted:
                    return entry
        return None

    @staticmethod
    def find_learned_entry(character: Character, ability_name: str):
        return SkillUtil._find_learned_entry(character, ability_name)

    @staticmethod
    def _learned_level(entry) -> int:
        if entry is None:
            return 0
        if isinstance(entry, dict):
            return max(0, min(100, GenericUtil.to_int(entry.get("level", 0), 0)))
        return max(0, min(100, GenericUtil.to_int(getattr(entry, "level", 0), 0)))

    @staticmethod
    def _set_learned_level(entry, value: int) -> None:
        if entry is None:
            return
        normalized = max(0, min(100, GenericUtil.to_int(value, 0)))
        if isinstance(entry, dict):
            entry["level"] = normalized
            return
        setattr(entry, "level", normalized)

    @staticmethod
    def ensure_learned_entry(character: Character, ability_name: str, *, collection_name: str) -> dict:
        collection_name = "spells" if str(collection_name or "").strip().lower() == "spells" else "skills"
        entry = SkillUtil._find_learned_entry(character, ability_name)
        if entry is not None:
            return entry

        collection = getattr(character, collection_name, None)
        if collection is None:
            collection = []
            setattr(character, collection_name, collection)

        entry = {"name": str(ability_name or "").strip(), "level": 0}
        collection.append(entry)
        return entry

    @staticmethod
    def set_character_learned_level(character: Character, ability_name: str, value: int, *, collection_name: str) -> dict:
        entry = SkillUtil.ensure_learned_entry(character, ability_name, collection_name=collection_name)
        SkillUtil._set_learned_level(entry, value)
        return entry

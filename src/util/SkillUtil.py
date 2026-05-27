import random

from player.CharacterAdvancement import CharacterAdvancement
from util.GenericUtil import GenericUtil
from player.Character import Character
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_logger(__name__)


class SkillUtil:
    @staticmethod
    def _weapon_enum_skill_name(enum_name: str) -> str:
        text = str(enum_name or "").strip().lower()
        if text.startswith("weapon_"):
            text = text[len("weapon_"):]
        return "hand to hand" if text == "exotic" else text

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
    def find_character_skill(skills: list, wanted: str):
        query = str(wanted or "").strip().lower()
        if not query:
            return None

        prefix_match = None
        for skill in skills or []:
            skill_name = SkillUtil.learned_entry_name(skill).lower()
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
    def practice_meta(ability_name: str):
        wanted = str(ability_name or "").strip().lower()
        if not wanted:
            return None

        try:
            registry = CharacterApi.get_registry()
        except RuntimeError:
            return None

        skill_registry = getattr(registry, "skill_registry", None)
        if skill_registry is not None:
            all_skills = getattr(skill_registry, "all_skills", None)
            if callable(all_skills):
                for skill in all_skills():
                    if str(getattr(skill, "name", "") or "").strip().lower() == wanted:
                        return skill

        spell_registry = getattr(registry, "spell_registry", None)
        if spell_registry is not None:
            all_spells = getattr(spell_registry, "all_spells", None)
            if callable(all_spells):
                for spell in all_spells():
                    if str(getattr(spell, "name", "") or "").strip().lower() == wanted:
                        return spell

        return None

    @staticmethod
    def _resolve_practice_meta(meta_or_name):
        if meta_or_name is None:
            return None
        if isinstance(meta_or_name, str):
            return SkillUtil.practice_meta(meta_or_name)
        return meta_or_name

    @staticmethod
    def practice_level_requirement(character: Character, meta_or_name) -> int:
        meta = SkillUtil._resolve_practice_meta(meta_or_name)
        if meta is None:
            return 0
        class_name = SkillUtil.practice_class_name(character)
        level_map = getattr(meta, "level_by_class", {}) or {}
        fallback = CharacterApi.skill_value_for_class(level_map, "mage", 99)
        return max(0, CharacterApi.skill_value_for_class(level_map, class_name, fallback))

    @staticmethod
    def practice_visible(character: Character, meta_or_name) -> bool:
        meta = SkillUtil._resolve_practice_meta(meta_or_name)
        if meta is None:
            return True
        required_level = SkillUtil.practice_level_requirement(character, meta)
        return GenericUtil.to_int(getattr(character, "level", 0), 0) >= required_level

    @staticmethod
    def practice_rating(character: Character, meta_or_name) -> int:
        meta = SkillUtil._resolve_practice_meta(meta_or_name)
        if meta is None:
            return 1
        class_name = SkillUtil.practice_class_name(character)
        rating_map = getattr(meta, "rating_by_class", {}) or {}
        fallback = CharacterApi.skill_value_for_class(rating_map, "mage", 0)
        return max(0, CharacterApi.skill_value_for_class(rating_map, class_name, fallback))

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
    def practice_meta_id(meta_or_name) -> str:
        meta = SkillUtil._resolve_practice_meta(meta_or_name)
        return str(getattr(meta, "id", "") or "").strip()

    @staticmethod
    def check_improve_by_name(ch: Character, ability_name: str, success: bool, multiplier: int = 1) -> None:
        ability_id = SkillUtil.practice_meta_id(ability_name)
        if not ability_id:
            return
        SkillUtil.check_improve(ch, ability_id, success, multiplier)

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

        rating = SkillUtil.practice_rating(ch, ability)
        learned_entry = SkillUtil._find_learned_entry(ch, str(getattr(ability, "name", "") or ""))
        learned = SkillUtil._learned_level(learned_entry)
        adept = SkillUtil.practice_adept(ch)
        intelligence = ch.character_attributes.intelligence
        learn_bonus = GenericUtil.to_int(CharacterApi.get_attribute_bonus("intelligence", str(intelligence)).get("learn", 0), 0)
        multiplier = max(1, GenericUtil.to_int(multiplier, 1))
        chance = (10 * learn_bonus) // (multiplier * rating * 4) + ch.level
        random_integer = random.randint(1, 1000)
        logger.debug(f"Skill {getattr(ability, 'name', '')} for {ch.name} (level {ch.level}, adept {adept}) - chance: {chance}; random_integer={random_integer} learn_bonus={learn_bonus}; rating={rating} learned={learned}; multiplier={multiplier}; success={success}")
        if random_integer > chance:
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
        logger.debug(f"Random chance SUCCESS - actual chance: {chance}")

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
    def visible_learned_entries(character: Character) -> list:
        visible_entries = []
        for collection_name in ("skills", "spells"):
            for entry in list(getattr(character, collection_name, []) or []):
                if SkillUtil._learned_level(entry) < 1:
                    continue
                name = SkillUtil.learned_entry_name(entry)
                if not name or not SkillUtil.practice_visible(character, name):
                    continue
                visible_entries.append(entry)
        return visible_entries

    @staticmethod
    def find_learned_entry(character: Character, ability_name: str):
        if character is None:
            return None
        entry = SkillUtil.find_character_skill(SkillUtil.visible_learned_entries(character), ability_name)
        if SkillUtil._learned_level(entry) < 1:
            return None
        return entry

    @staticmethod
    def learned_entry_name(entry) -> str:
        if entry is None:
            return ""
        if isinstance(entry, dict):
            return str(entry.get("name", "") or "").strip()
        return str(getattr(entry, "name", "") or "").strip()

    @staticmethod
    def learned_level(entry) -> int:
        return SkillUtil._learned_level(entry)

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

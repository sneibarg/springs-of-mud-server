import random

from game.RandomNumberGenerator import RandomNumberGenerator
from player.CharacterAdvancement import CharacterAdvancement
from util.GenericUtil import GenericUtil
from player.Character import Character
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_logger(__name__)
rng = RandomNumberGenerator()

class SkillUtil:
    _IMPROVE_MESSAGES_ATTR = "_skill_improve_messages"

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
        collection_name = "skills"
        ability = getattr(registry, "skill_registry", None).get_or_none(id=skill_id) if getattr(registry, "skill_registry", None) is not None else None
        if ability is None and getattr(registry, "spell_registry", None) is not None:
            ability = registry.spell_registry.get_or_none(id=skill_id)
            collection_name = "spells"
        if ability is None:
            return

        rating = SkillUtil.practice_rating(ch, ability)
        learned_entry = Character.get_learned(ch, ability.name, collection_name=collection_name)
        learned = Character.learned_entry_level(learned_entry)
        adept = SkillUtil.practice_adept(ch)
        intelligence = ch.character_attributes.intelligence
        learn_bonus = GenericUtil.to_int(CharacterApi.get_attribute_bonus("intelligence", str(intelligence)).get("learn", 0), 0)
        multiplier = max(1, GenericUtil.to_int(multiplier, 1))
        chance = (10 * learn_bonus) // (multiplier * rating * 4) + ch.level
        random_integer = random.randint(1, 1000)
        logger.info(f"Skill {getattr(ability, 'name', '')} for {ch.name} (level {ch.level}, adept {adept}) - chance: {chance}; random_integer={random_integer} learn_bonus={learn_bonus}; rating={rating} learned={learned}; multiplier={multiplier}; success={success}")
        if random_integer > chance:
            return

        if success:
            chance = max(5, min(adept - learned, 95))
            if rng.number_percent() < chance:
                improved = min(learned + 1, adept)
                Character.set_learned(ch, getattr(ability, "name", ""), improved, collection_name=collection_name, create=True)
                if improved > learned:
                    SkillUtil._queue_improve_message(ch, f"You have become better at {getattr(ability, 'name', '')}!\r\n")
                    CharacterAdvancement.gain_experience(ch, 2 * rating)
        else:
            chance = max(5, min(learned // 2, 30))
            if rng.number_percent() < chance:
                improved = min(learned + random.randint(1, 3), adept)
                Character.set_learned(ch, getattr(ability, "name", ""), improved, collection_name=collection_name, create=True)
                if improved > learned:
                    SkillUtil._queue_improve_message(ch, f"You learn from your mistakes, and your {getattr(ability, 'name', '')} skill improves.\r\n")
                    CharacterAdvancement.gain_experience(ch, 2 * rating)
        logger.info(f"Random chance SUCCESS - actual chance: {chance}")

    @staticmethod
    def _queue_improve_message(character: Character, message: str) -> None:
        if character is None or not message:
            return
        messages = list(getattr(character, SkillUtil._IMPROVE_MESSAGES_ATTR, []) or [])
        messages.append(str(message))
        setattr(character, SkillUtil._IMPROVE_MESSAGES_ATTR, messages)

    @staticmethod
    def take_improve_messages(character: Character) -> str:
        if character is None:
            return ""
        messages = list(getattr(character, SkillUtil._IMPROVE_MESSAGES_ATTR, []) or [])
        setattr(character, SkillUtil._IMPROVE_MESSAGES_ATTR, [])
        return "".join(messages)


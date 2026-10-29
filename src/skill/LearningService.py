from __future__ import annotations

from player.Character import Character
from skill.LearningMessages import LearningMessages
from util.GenericUtil import GenericUtil


class LearningService:
    """Coordinate learning with explicit definition, rules, random and XP collaborators."""

    def __init__(self, resolver, rules, rng, random_source, advance, logger):
        self.resolver = resolver
        self.rules = rules
        self.rng = rng
        self.random = random_source
        self.advance = advance
        self.logger = logger

    def practice_class_name(self, character: Character) -> str:
        return str(character.character_class.name or "").strip().lower()

    def practice_adept(self, character: Character) -> int:
        adept = GenericUtil.to_int(character.character_class.skill_adept, 75)
        return adept if adept > 0 else 75

    def practice_meta(self, ability_name: str):
        return self.resolver.by_name(ability_name)

    def _resolve_practice_meta(self, meta_or_name):
        if meta_or_name is None:
            return None
        if isinstance(meta_or_name, str):
            return self.practice_meta(meta_or_name)
        return meta_or_name

    def practice_level_requirement(self, character: Character, meta_or_name) -> int:
        meta = self._resolve_practice_meta(meta_or_name)
        if meta is None:
            return 0
        class_name = self.practice_class_name(character)
        if callable(getattr(meta, "level_for_class", None)):
            return meta.level_for_class(class_name)
        level_map = meta.level_by_class or {}
        fallback = self.rules.skill_value_for_class(level_map, "mage", 99)
        return max(0, self.rules.skill_value_for_class(level_map, class_name, fallback))

    def practice_visible(self, character: Character, meta_or_name) -> bool:
        meta = self._resolve_practice_meta(meta_or_name)
        if meta is None:
            return True
        required_level = self.practice_level_requirement(character, meta)
        return GenericUtil.to_int(character.level, 0) >= required_level

    def practice_rating(self, character: Character, meta_or_name) -> int:
        meta = self._resolve_practice_meta(meta_or_name)
        if meta is None:
            return 1
        class_name = self.practice_class_name(character)
        if callable(getattr(meta, "rating_for_class", None)):
            return meta.rating_for_class(class_name)
        rating_map = meta.rating_by_class or {}
        fallback = self.rules.skill_value_for_class(rating_map, "mage", 0)
        return max(0, self.rules.skill_value_for_class(rating_map, class_name, fallback))

    def practice_gain(self, character: Character, rating: int) -> int:
        intelligence = self.rules.current_stat(character, 'intelligence')
        learn_bonus = GenericUtil.to_int(
            self.rules.get_attribute_bonus("intelligence", str(intelligence)).get("learn", 0), 0)
        rating = max(1, GenericUtil.to_int(rating, 1))
        gain = learn_bonus // rating
        return max(1, gain)

    def practice_meta_id(self, meta_or_name) -> str:
        meta = self._resolve_practice_meta(meta_or_name)
        return "" if meta is None else str(meta.id or "").strip()

    def check_improve_by_name(self, ch: Character, ability_name: str, success: bool, multiplier: int = 1) -> None:
        ability_id = self.practice_meta_id(ability_name)
        if not ability_id:
            return
        self.check_improve(ch, ability_id, success, multiplier)

    def check_improve(self, ch: Character, ability_id: str, success: bool, multiplier: int = 1) -> None:
        if self.rules.is_npc(ch):
            return

        ability, collection_name = self.resolver.by_id(ability_id)
        if ability is None:
            return

        rating = self.practice_rating(ch, ability)
        learned_entry = Character.get_learned(ch, ability.name, collection_name=collection_name)
        learned = Character.learned_entry_level(learned_entry)
        if not self.practice_visible(ch, ability) or rating <= 0 or learned <= 0 or learned >= 100:
            return
        intelligence = self.rules.current_stat(ch, 'intelligence')
        learn_bonus = GenericUtil.to_int(self.rules.get_attribute_bonus("intelligence", str(intelligence)).get("learn", 0), 0)
        multiplier = max(1, GenericUtil.to_int(multiplier, 1))
        chance = (10 * learn_bonus) // (multiplier * rating * 4) + ch.level
        random_integer = self.random.randint(1, 1000)
        self.logger.info(f"Skill {ability.name} for {ch.name} (level {ch.level}) - chance: {chance}; random_integer={random_integer} learn_bonus={learn_bonus}; rating={rating} learned={learned}; multiplier={multiplier}; success={success}")
        if random_integer > chance:
            return

        if success:
            chance = max(5, min(100 - learned, 95))
            if self.rng.number_percent() < chance:
                improved = min(learned + 1, 100)
                Character.set_learned(ch, ability.name, improved, collection_name=collection_name, create=True)
                if improved > learned:
                    self._queue_improve_message(ch, f"You have become better at {ability.name}!\r\n")
                    self.advance(ch, 2 * rating)
        else:
            chance = max(5, min(learned // 2, 30))
            if self.rng.number_percent() < chance:
                improved = min(learned + self.random.randint(1, 3), 100)
                Character.set_learned(ch, ability.name, improved, collection_name=collection_name, create=True)
                if improved > learned:
                    self._queue_improve_message(ch, f"You learn from your mistakes, and your {ability.name} skill improves.\r\n")
                    self.advance(ch, 2 * rating)
        self.logger.info(f"Random chance SUCCESS - actual chance: {chance}")

    def _queue_improve_message(self, character, message):
        LearningMessages.queue(character, message)

    def take_improve_messages(self, character):
        return LearningMessages.take(character)

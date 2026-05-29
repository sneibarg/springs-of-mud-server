from __future__ import annotations

import json
import random

from dataclasses import dataclass, field
from typing import Any

from api.CharacterApi import CharacterApi
from game.GamePayload import GamePayload
from game.RandomNumberGenerator import RandomNumberGenerator
from player.Character import Character
from player.CharacterAdvancement import CharacterAdvancement
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil


logger = LoggerFactory.get_logger(__name__)
rng = RandomNumberGenerator()


@dataclass
class Ability:
    id: str
    name: str
    kind: str
    handler_id: str
    target: str
    min_position: str
    noun_damage: str
    msg_off: str
    msg_obj: str
    level_by_class: dict[str, int]
    rating_by_class: dict[str, int]
    slot: int
    min_mana: int
    beats: int
    payload: GamePayload = field(default_factory=GamePayload)

    def message(self, channel: str, key: str, fallback: str = "", **values) -> str:
        return self.payload.render(channel, key, fallback=fallback, **values)

    @classmethod
    def _base_payload_from_json(cls, data) -> dict[str, Any]:
        if isinstance(data, str):
            data = json.loads(data)
        payload = GenericUtil.camel_to_snake_case(data)
        payload["id"] = cls._extract_id(data, payload)
        payload["payload"] = GamePayload.from_json(payload.get("payload"))
        payload.pop("_id", None)
        return payload

    @staticmethod
    def _extract_id(source: dict[str, Any], payload: dict[str, Any]) -> str:
        raw_id = payload.get("id")
        if isinstance(raw_id, str) and raw_id.strip():
            return raw_id.strip()

        nested_id = source.get("_id")
        if isinstance(nested_id, dict):
            oid = nested_id.get("$oid")
            if oid:
                return str(oid)

        if nested_id:
            return str(nested_id)
        return ""

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
            return Ability.practice_meta(meta_or_name)
        return meta_or_name

    @staticmethod
    def practice_level_requirement(character: Character, meta_or_name) -> int:
        meta = Ability._resolve_practice_meta(meta_or_name)
        if meta is None:
            return 0
        class_name = Ability.practice_class_name(character)
        level_map = getattr(meta, "level_by_class", {}) or {}
        fallback = CharacterApi.skill_value_for_class(level_map, "mage", 99)
        return max(0, CharacterApi.skill_value_for_class(level_map, class_name, fallback))

    @staticmethod
    def practice_visible(character: Character, meta_or_name) -> bool:
        meta = Ability._resolve_practice_meta(meta_or_name)
        if meta is None:
            return True
        required_level = Ability.practice_level_requirement(character, meta)
        return GenericUtil.to_int(getattr(character, "level", 0), 0) >= required_level

    @staticmethod
    def practice_rating(character: Character, meta_or_name) -> int:
        meta = Ability._resolve_practice_meta(meta_or_name)
        if meta is None:
            return 1
        class_name = Ability.practice_class_name(character)
        rating_map = getattr(meta, "rating_by_class", {}) or {}
        fallback = CharacterApi.skill_value_for_class(rating_map, "mage", 0)
        return max(0, CharacterApi.skill_value_for_class(rating_map, class_name, fallback))

    @staticmethod
    def practice_gain(character: Character, rating: int) -> int:
        intelligence = GenericUtil.to_int(getattr(getattr(character, "character_attributes", None), "intelligence", 0), 0)
        learn_bonus = GenericUtil.to_int(
            CharacterApi.get_attribute_bonus("intelligence", str(intelligence)).get("learn", 0), 0)
        rating = max(1, GenericUtil.to_int(rating, 1))
        gain = learn_bonus // rating
        return max(1, gain)

    @staticmethod
    def practice_meta_id(meta_or_name) -> str:
        meta = Ability._resolve_practice_meta(meta_or_name)
        return str(getattr(meta, "id", "") or "").strip()

    @staticmethod
    def check_improve_by_name(ch: Character, ability_name: str, success: bool, multiplier: int = 1) -> None:
        ability_id = Ability.practice_meta_id(ability_name)
        if not ability_id:
            return
        Ability.check_improve(ch, ability_id, success, multiplier)

    @staticmethod
    def check_improve(ch: Character, ability_id: str, success: bool, multiplier: int = 1) -> None:
        if CharacterApi.is_npc(ch):
            return

        registry = CharacterApi.get_registry()
        collection_name = "skills"
        ability = getattr(registry, "skill_registry", None).get_or_none(id=ability_id) if getattr(registry, "skill_registry", None) is not None else None
        if ability is None and getattr(registry, "spell_registry", None) is not None:
            ability = registry.spell_registry.get_or_none(id=ability_id)
            collection_name = "spells"
        if ability is None:
            return

        rating = Ability.practice_rating(ch, ability)
        learned_entry = Character.get_learned(ch, ability.name, collection_name=collection_name)
        learned = Character.learned_entry_level(learned_entry)
        adept = Ability.practice_adept(ch)
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
                    Ability._queue_improve_message(ch, f"You have become better at {getattr(ability, 'name', '')}!\r\n")
                    CharacterAdvancement.gain_experience(ch, 2 * rating)
        else:
            chance = max(5, min(learned // 2, 30))
            if rng.number_percent() < chance:
                improved = min(learned + random.randint(1, 3), adept)
                Character.set_learned(ch, getattr(ability, "name", ""), improved, collection_name=collection_name, create=True)
                if improved > learned:
                    Ability._queue_improve_message(ch, f"You learn from your mistakes, and your {getattr(ability, 'name', '')} skill improves.\r\n")
                    CharacterAdvancement.gain_experience(ch, 2 * rating)
        logger.info(f"Random chance SUCCESS - actual chance: {chance}")

    @staticmethod
    def _queue_improve_message(character: Character, message: str) -> None:
        if character is None or not message:
            return
        messages = list(getattr(character, "_skill_improve_messages", []) or [])
        messages.append(str(message))
        setattr(character, "_skill_improve_messages", messages)

    @staticmethod
    def take_improve_messages(character: Character) -> str:
        if character is None:
            return ""
        messages = list(getattr(character, "_skill_improve_messages", []) or [])
        setattr(character, "_skill_improve_messages", [])
        return "".join(messages)

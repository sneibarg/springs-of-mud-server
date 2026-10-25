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
    level_by_class: dict[str, int]
    rating_by_class: dict[str, int]
    slot: int
    min_mana: int
    beats: int
    payload: GamePayload = field(default_factory=GamePayload)
    guards: list[dict[str, Any]] = field(default_factory=list)

    def message(self, channel: str, key: str, fallback: str = "", **values) -> str:
        if not isinstance(self.payload, GamePayload):
            self.payload = GamePayload.from_json(self.payload)
        return self.payload.render(channel, key, fallback=fallback, **values)

    @classmethod
    def _base_payload_from_json(cls, data) -> dict[str, Any]:
        if isinstance(data, str):
            data = json.loads(data)
        payload = GenericUtil.camel_to_snake_case(data)
        payload["id"] = cls._extract_id(data, payload)
        payload["payload"] = GamePayload.from_json(payload.get("payload"))
        payload["guards"] = cls._normalize_checks(payload.get("guards"))
        payload.pop("msg_off", None)
        payload.pop("msg_obj", None)
        payload.pop("_id", None)
        return payload

    @staticmethod
    def _normalize_checks(value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []

        normalized: list[dict[str, Any]] = []
        for entry in value:
            if isinstance(entry, str):
                text = entry.strip()
                if text:
                    normalized.append({"predicate": text})
                continue
            if not isinstance(entry, dict):
                continue
            check = GenericUtil.camel_to_snake_case(entry)
            predicate = str(check.get("predicate", check.get("lambda", "")) or "").strip()
            if not predicate:
                continue
            raw_message_key = str(check.get("message_key", "") or "").strip()
            normalized_message_key = ""
            if raw_message_key:
                normalized_message_key = next(iter(GenericUtil.camel_to_snake_case({raw_message_key: ""}).keys()), raw_message_key)
            normalized.append(
                {
                    "predicate": predicate,
                    "channel": str(check.get("channel", "") or "").strip(),
                    "message_key": normalized_message_key,
                    "fallback": str(check.get("fallback", "") or ""),
                    "token_factory": str(check.get("token_factory", "") or "").strip(),
                }
            )
        return normalized

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

    _learning = None

    def level_for_class(self, class_name):
        fallback = CharacterApi.skill_value_for_class(self.level_by_class or {}, "mage", 99)
        return max(0, CharacterApi.skill_value_for_class(self.level_by_class or {}, class_name, fallback))

    def rating_for_class(self, class_name):
        fallback = CharacterApi.skill_value_for_class(self.rating_by_class or {}, "mage", 0)
        return max(0, CharacterApi.skill_value_for_class(self.rating_by_class or {}, class_name, fallback))

    @classmethod
    def configure_learning(cls, service):
        cls._learning = service

    @classmethod
    def _learning_service(cls):
        if cls._learning is not None:
            return cls._learning
        # Compatibility for isolated model users; server bootstrap supplies the
        # persistent service. Resolve dependencies afresh, never cache a world.
        from skill.AbilityResolver import AbilityResolver
        from skill.LearningService import LearningService
        try:
            get_registry = getattr(CharacterApi, "get_registry", None)
            registry = get_registry() if callable(get_registry) else None
        except RuntimeError:
            registry = None
        resolver = AbilityResolver(getattr(registry, "skill_registry", None),
                                   getattr(registry, "spell_registry", None))
        return LearningService(resolver, CharacterApi, rng, random,
                               CharacterAdvancement.gain_experience, logger)

    @staticmethod
    def practice_class_name(character: Character) -> str:
        return Ability._learning_service().practice_class_name(character)

    @staticmethod
    def practice_adept(character: Character) -> int:
        return Ability._learning_service().practice_adept(character)

    @staticmethod
    def practice_meta(ability_name: str):
        return Ability._learning_service().practice_meta(ability_name)

    @staticmethod
    def _resolve_practice_meta(meta_or_name):
        return Ability._learning_service()._resolve_practice_meta(meta_or_name)

    @staticmethod
    def practice_level_requirement(character: Character, meta_or_name) -> int:
        return Ability._learning_service().practice_level_requirement(character, meta_or_name)

    @staticmethod
    def practice_visible(character: Character, meta_or_name) -> bool:
        return Ability._learning_service().practice_visible(character, meta_or_name)

    @staticmethod
    def practice_rating(character: Character, meta_or_name) -> int:
        return Ability._learning_service().practice_rating(character, meta_or_name)

    @staticmethod
    def practice_gain(character: Character, rating: int) -> int:
        return Ability._learning_service().practice_gain(character, rating)

    @staticmethod
    def practice_meta_id(meta_or_name) -> str:
        return Ability._learning_service().practice_meta_id(meta_or_name)

    @staticmethod
    def check_improve_by_name(ch: Character, ability_name: str, success: bool, multiplier: int = 1) -> None:
        ability_id = Ability.practice_meta_id(ability_name)
        if ability_id:
            Ability.check_improve(ch, ability_id, success, multiplier)

    @staticmethod
    def check_improve(ch: Character, ability_id: str, success: bool, multiplier: int = 1) -> None:
        return Ability._learning_service().check_improve(ch, ability_id, success, multiplier)

    @staticmethod
    def _queue_improve_message(character: Character, message: str) -> None:
        from skill.LearningMessages import LearningMessages
        LearningMessages.queue(character, message)

    @staticmethod
    def take_improve_messages(character: Character) -> str:
        from skill.LearningMessages import LearningMessages
        return LearningMessages.take(character)

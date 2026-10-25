import asyncio
from copy import deepcopy
from dataclasses import is_dataclass
from enum import Enum
from typing import Any

import requests

from injector import inject
from player.Character import Character
from player.CharacterRegistry import CharacterRegistry
from player.CharacterRace import CharacterRace
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.BackgroundIO import submit
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class CharacterService(FetchAndRegisterMixin):
    @inject
    def __init__(self, config: ServiceConfig, character_registry: CharacterRegistry):
        self.__name__ = "CharacterService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.characters_endpoint = config.characters_endpoint
        self.character_registry = character_registry
        self.load_characters()

    def reload_characters(self) -> bool:
        return self._reload_collection(self.characters_endpoint, "characters", self.character_registry)

    def load_characters(self):
        self._fetch_and_register(self.characters_endpoint, "all characters")
        self.logger.info(f"Initialized CharacterService instance with {str(len(self.character_registry))} player characters.")

    def load_character(self, character_name: str):
        url = f"{self.characters_endpoint}/name/{character_name}"
        return self._fetch_and_register(url, f"character '{character_name}'")

    def _save_snapshot(self, character):
        return deepcopy(self._serialize_character(character))

    def queue_save_character(self, character):
        """Capture now; return a future for the ordered HTTP write."""
        # Submit while holding the model lock so snapshots cannot overtake each other.
        with character.lock:
            return submit(self._persist_character, self._save_snapshot(character))

    async def save_character_async(self, character) -> bool:
        return await asyncio.shield(asyncio.wrap_future(self.queue_save_character(character)))

    def save_character(self, character: Character) -> bool:
        """Blocking compatibility entry point; async gameplay uses the queue."""
        with character.lock:
            payload = self._save_snapshot(character)
        result = self._persist_character(payload)
        if result:
            self.character_registry.register(character)
        return result

    def _persist_character(self, payload) -> bool:
        character_id = str(payload.get("id") or "")
        if not character_id:
            self.logger.error("Refusing to save character without an id.")
            return False
        payload["id"] = character_id
        try:
            response = requests.put(f"{self.characters_endpoint}/{character_id}", json=payload, timeout=10)
            response.raise_for_status()
            self.logger.debug(f"Saved character {payload.get('name', '')} ({character_id}).")
            return True
        except requests.RequestException as e:
            self.logger.error(f"Failed to save character {character_id}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error saving character {character_id}: {e}", exc_info=True)
            return False

    def _build_fetch_item(self, character_data) -> Character:
        character = Character.from_json(character_data)
        self.logger.debug(f"Registering character {character.name}: {character}")
        return character

    def _register_fetch_item(self, character: Character) -> None:
        self.character_registry.register(character)

    @classmethod
    def _serialize_character(cls, character: Character) -> dict[str, Any]:
        return {
            "id": character.id,
            "accountId": character.account_id,
            "title": character.title,
            "description": character.description,
            "cloaked": bool(character.cloaked),
            "guild": character.guild,
            "characterRace": cls._serialize_character_race(character.character_race),
            "name": character.name,
            "areaId": character.area_id,
            "roomId": character.room_id,
            "role": character.role,
            "sex": character.sex,
            "level": character.level,
            "hit": character.hit,
            "maxHit": character.max_hit,
            "mana": character.mana,
            "maxMana": character.max_mana,
            "movement": character.movement,
            "maxMovement": character.max_movement,
            "gold": character.gold,
            "silver": character.silver,
            "trust": character.trust,
            "inventory": [cls._serialize_value(item) for item in cls._inventory_items(character)],
            "effects": cls._serialize_value(character.effects),
            "skills": cls._serialize_value(character.skills),
            "spells": cls._serialize_value(character.spells),
            "groups": list(character.groups),
            "aliases": dict(getattr(character, "aliases", {})),
            "statusFlags": cls._serialize_value(character.status_flags),
            "characterAttributes": cls._serialize_value(character.character_attributes),
            "armorClass": cls._serialize_value(character.armor_class),
            "characterClass": cls._serialize_value(character.character_class),
            "promptFormat": cls._serialize_prompt_format(character.prompt_format),
            "equipped": cls._serialize_value(character.equipped),
        }

    @staticmethod
    def _inventory_items(character: Character) -> list[Any]:
        return list(character.get_items())

    @staticmethod
    def _serialize_character_race(character_race: CharacterRace | None) -> dict[str, Any]:
        race = CharacterRace.from_json(character_race)
        return {
            "whoName": race.who_name,
            "points": race.points,
            "classMult": race.class_mult,
            "skills": list(race.skills),
            "strength": race.strength,
            "maxStrength": race.max_strength,
            "intelligence": race.intelligence,
            "maxIntelligence": race.max_intelligence,
            "wisdom": race.wisdom,
            "maxWisdom": race.max_wisdom,
            "dexterity": race.dexterity,
            "maxDexterity": race.max_dexterity,
            "constitution": race.constitution,
            "maxConstitution": race.max_constitution,
            "size": race.size,
        }

    @classmethod
    def _serialize_value(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, list):
            return [cls._serialize_value(item) for item in value]
        if isinstance(value, tuple):
            return [cls._serialize_value(item) for item in value]
        if isinstance(value, set):
            return [cls._serialize_value(item) for item in value]
        if isinstance(value, dict):
            return {cls._camelize(str(key)): cls._serialize_value(item) for key, item in value.items()}
        if is_dataclass(value):
            data = {}
            for field_name in value.__dataclass_fields__:
                if field_name in {"room_data"}:
                    continue
                data[cls._camelize(field_name)] = cls._serialize_value(getattr(value, field_name))
            return data
        return value

    @staticmethod
    def _serialize_prompt_format(prompt_format) -> dict[str, bool]:
        if prompt_format is None:
            return {}

        return {
            "hp": bool(prompt_format.health),
            "max_hp": bool(prompt_format.max_health),
            "mana": bool(prompt_format.mana),
            "max_mana": bool(prompt_format.max_mana),
            "movement": bool(prompt_format.movement),
            "max_movement": bool(prompt_format.max_movement),
            "xp": bool(prompt_format.experience),
            "max_xp": bool(prompt_format.accumulated_experience),
            "gold": bool(prompt_format.gold),
            "silver": bool(prompt_format.silver),
            "alignment": bool(prompt_format.alignment),
            "room_name": bool(prompt_format.room_name),
            "exits": bool(prompt_format.exits),
            "room_vnum": bool(prompt_format.room_vnum),
            "area_name": bool(prompt_format.area_name),
            "carriage_return": bool(prompt_format.carriage_return),
        }

    @staticmethod
    def _camelize(name: str) -> str:
        if "_" not in name:
            return name
        head, *tail = name.split("_")
        return head + "".join(part.capitalize() for part in tail)

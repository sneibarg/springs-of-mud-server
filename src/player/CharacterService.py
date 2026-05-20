from dataclasses import is_dataclass
from enum import Enum
from typing import Any, Optional

import requests

from injector import inject
from player.Character import Character
from player.CharacterRegistry import CharacterRegistry
from player.CharacterRace import CharacterRace
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class CharacterService:
    @inject
    def __init__(self, config: ServiceConfig, character_registry: CharacterRegistry):
        self.__name__ = "CharacterService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.characters_endpoint = config.characters_endpoint
        self.character_registry = character_registry
        self.load_characters()

    def reload_characters(self) -> None:
        self.logger.info("Reloading all characters...")
        self.character_registry.reset()
        self.load_characters()
        self.logger.info("Characters reload completed.")

    def load_characters(self):
        self._fetch_and_register(self.characters_endpoint, "all characters")
        self.logger.info(f"Initialized CharacterService instance with {str(len(self.character_registry))} player characters.")

    def load_player(self, character_name: str):
        url = f"{self.characters_endpoint}/name/{character_name}"
        return self._fetch_and_register(url, f"character '{character_name}'")

    def save_character(self, character: Character) -> bool:
        character_id = str(getattr(character, "id", "") or "")
        if not character_id:
            self.logger.error("Refusing to save character without an id.")
            return False

        payload = self._serialize_character(character)
        payload["id"] = character_id
        url = f"{self.characters_endpoint}/{character_id}"
        try:
            response = requests.put(url, json=payload, timeout=10)
            response.raise_for_status()

            try:
                data = response.json()
            except ValueError:
                data = None

            if isinstance(data, dict) and data.get("id"):
                self.character_registry.unregister(item=character)
                self.character_registry.register(character)
            else:
                self.character_registry.register(character)

            self.logger.debug(f"Saved character {character.name} ({character_id}).")
            return True
        except requests.RequestException as e:
            self.logger.error(f"Failed to save character {character_id} to {self.characters_endpoint}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error saving character {character_id}: {e}", exc_info=True)
            return False

    def _fetch_and_register(self, url: str, description: str) -> Optional[Character]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                count = 0
                for character_data in data:
                    char = Character.from_json(character_data)
                    self.logger.debug(f"Registering character {char.name}: {char}")
                    self.character_registry.register(char)
                    count += 1
                self.logger.info(f"Loaded {count} {description}.")
                return None
            else:
                character = Character.from_json(data)
                self.character_registry.register(character)
                self.logger.info(f"Loaded {description}.")
                return character

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None

    @classmethod
    def _serialize_character(cls, character: Character) -> dict[str, Any]:
        return {
            "id": character.id,
            "accountId": getattr(character, "account_id", ""),
            "title": getattr(character, "title", ""),
            "description": getattr(character, "description", ""),
            "cloaked": bool(getattr(character, "cloaked", False)),
            "guild": getattr(character, "guild", ""),
            "characterRace": cls._serialize_character_race(getattr(character, "character_race", None)),
            "name": getattr(character, "name", ""),
            "areaId": getattr(character, "area_id", ""),
            "roomId": getattr(character, "room_id", ""),
            "role": getattr(character, "role", ""),
            "sex": getattr(character, "sex", ""),
            "level": getattr(character, "level", 0),
            "hit": getattr(character, "hit", 0),
            "maxHit": getattr(character, "max_hit", 0),
            "mana": getattr(character, "mana", 0),
            "maxMana": getattr(character, "max_mana", 0),
            "movement": getattr(character, "movement", 0),
            "maxMovement": getattr(character, "max_movement", 0),
            "gold": getattr(character, "gold", 0),
            "silver": getattr(character, "silver", 0),
            "trust": getattr(character, "trust", 0),
            "inventory": [cls._serialize_value(item) for item in cls._inventory_items(character)],
            "effects": cls._serialize_value(getattr(character, "effects", [])),
            "skills": cls._serialize_value(getattr(character, "skills", [])),
            "spells": cls._serialize_value(getattr(character, "spells", [])),
            "statusFlags": cls._serialize_value(getattr(character, "status_flags", None)),
            "characterAttributes": cls._serialize_value(getattr(character, "character_attributes", None)),
            "armorClass": cls._serialize_value(getattr(character, "armor_class", None)),
            "characterClass": cls._serialize_value(getattr(character, "character_class", None)),
            "promptFormat": cls._serialize_prompt_format(getattr(character, "prompt_format", None)),
            "equipped": cls._serialize_value(getattr(character, "equipped", None)),
        }

    @staticmethod
    def _inventory_items(character: Character) -> list[Any]:
        if hasattr(character, "get_items"):
            return list(character.get_items())
        return list(getattr(character, "inventory", []) or [])

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
            "hp": bool(getattr(prompt_format, "health", False)),
            "max_hp": bool(getattr(prompt_format, "max_health", False)),
            "mana": bool(getattr(prompt_format, "mana", False)),
            "max_mana": bool(getattr(prompt_format, "max_mana", False)),
            "movement": bool(getattr(prompt_format, "movement", False)),
            "max_movement": bool(getattr(prompt_format, "max_movement", False)),
            "xp": bool(getattr(prompt_format, "experience", False)),
            "max_xp": bool(getattr(prompt_format, "accumulated_experience", False)),
            "gold": bool(getattr(prompt_format, "gold", False)),
            "silver": bool(getattr(prompt_format, "silver", False)),
            "alignment": bool(getattr(prompt_format, "alignment", False)),
            "room_name": bool(getattr(prompt_format, "room_name", False)),
            "exits": bool(getattr(prompt_format, "exits", False)),
            "room_vnum": bool(getattr(prompt_format, "room_vnum", False)),
            "area_name": bool(getattr(prompt_format, "area_name", False)),
            "carriage_return": bool(getattr(prompt_format, "carriage_return", False)),
        }

    @staticmethod
    def _camelize(name: str) -> str:
        if "_" not in name:
            return name
        head, *tail = name.split("_")
        return head + "".join(part.capitalize() for part in tail)

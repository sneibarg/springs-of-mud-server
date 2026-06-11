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
        character_id = str(character.id or "")
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

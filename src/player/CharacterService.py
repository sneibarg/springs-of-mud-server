import requests

from typing import Optional
from injector import inject
from player.Character import Character
from player.CharacterRegistry import CharacterRegistry
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

    def _fetch_and_register(self, url: str, description: str) -> Optional[Character]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                count = 0
                for character_data in data:
                    self.character_registry.register(Character.from_json(character_data))
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

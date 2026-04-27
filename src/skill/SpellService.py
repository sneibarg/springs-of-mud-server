import requests

from typing import Optional
from injector import inject

from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from skill.Spell import Spell
from skill.SpellRegistry import SpellRegistry


class SpellService:
    @inject
    def __init__(self, config: ServiceConfig, spell_registry: SpellRegistry):
        self.__name__ = "SpellService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.spells_endpoint = config.spells_endpoint
        self.spell_registry = spell_registry
        self.load_spells()

    def reload_spells(self) -> None:
        self.logger.info("Reloading all spells...")
        self.spell_registry.reset()
        self.load_spells()
        self.logger.info("Spells reload completed.")

    def load_spells(self):
        self._fetch_and_register(self.spells_endpoint, "all spells")

    def load_spell(self, spell_name: str):
        url = f"{self.spells_endpoint}/name/{spell_name}"
        return self._fetch_and_register(url, f"spell '{spell_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Spell]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                count = 0
                for spell_data in data:
                    self.spell_registry.register(Spell.from_json(spell_data))
                    count += 1
                self.logger.info(f"Loaded {count} {description}.")
                return None
            spell = Spell.from_json(data)
            self.spell_registry.register(spell)
            self.logger.info(f"Loaded {description}.")
            return spell
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None

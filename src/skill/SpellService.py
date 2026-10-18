from injector import inject

from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from skill.Spell import Spell
from skill.SpellRegistry import SpellRegistry


class SpellService(FetchAndRegisterMixin):
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

    def _build_fetch_item(self, spell_data) -> Spell:
        return Spell.from_json(spell_data)

    def _register_fetch_item(self, spell: Spell) -> None:
        self.spell_registry.register(spell)

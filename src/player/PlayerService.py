from typing import Optional

import requests

from injector import inject
from player.Player import Player
from player.PlayerRegistry import PlayerRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class PlayerService:
    @inject
    def __init__(self, config: ServiceConfig, player_registry: PlayerRegistry):
        self.__name__ = "CharacterService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.players_endpoint = config.players_endpoint
        self.characters_endpoint = config.characters_endpoint
        self.player_registry = player_registry
        self.load_players()

    def reload_players(self) -> None:
        self.logger.info("Reloading all players...")
        self.player_registry.reset()
        self.load_players()
        self.logger.info("Skills reload completed.")

    def load_players(self):
        self._fetch_and_register(self.players_endpoint, "all players")
        self.logger.info(f"Players PlayerService instance with {str(len(self.player_registry))} player accounts.")

    def load_player(self, player_name: str):
        url = f"{self.players_endpoint}/name/{player_name}"
        return self._fetch_and_register(url, f"player '{player_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Player]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                count = 0
                for player_data in data:
                    self.player_registry.register(Player.from_json(player_data))
                    count += 1
                self.logger.info(f"Loaded {count} {description}.")
                return None
            else:
                player = Player.from_json(data)
                self.player_registry.register(player)
                self.logger.info(f"Loaded {description}.")
                return player

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None

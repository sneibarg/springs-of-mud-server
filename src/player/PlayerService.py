from typing import Optional
from dataclasses import is_dataclass
from enum import Enum
from typing import Any

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

    def save_player(self, player: Player) -> bool:
        player_id = str(player.id or "")
        if not player_id:
            self.logger.error("Refusing to save player without an id.")
            return False

        payload = self._serialize_player(player)
        payload["id"] = player_id
        url = f"{self.players_endpoint}/{player_id}"
        try:
            response = requests.put(url, json=payload, timeout=10)
            response.raise_for_status()
            self.player_registry.register(player)
            self.logger.debug(f"Saved player {player.account_name} ({player_id}).")
            return True
        except requests.RequestException as e:
            self.logger.error(f"Failed to save player {player_id} to {self.players_endpoint}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error saving player {player_id}: {e}", exc_info=True)
            return False

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

    @classmethod
    def _serialize_player(cls, player: Player) -> dict[str, Any]:
        return {
            "id": player.id,
            "banned": bool(player.banned),
            "firstName": player.first_name,
            "lastName": player.last_name,
            "accountName": player.account_name,
            "emailAddress": player.email_address,
            "password": player.password,
            "playerCharacterList": cls._serialize_value(player.player_character_list),
            "ansiEnabled": bool(player.ansi_enabled),
            "usage": player.usage,
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
                if field_name in {"connection", "current_characters", "lock", "logger"}:
                    continue
                data[cls._camelize(field_name)] = cls._serialize_value(getattr(value, field_name))
            return data
        return value

    @staticmethod
    def _camelize(name: str) -> str:
        if "_" not in name:
            return name
        head, *tail = name.split("_")
        return head + "".join(part.capitalize() for part in tail)

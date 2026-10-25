from copy import deepcopy
from dataclasses import is_dataclass
from enum import Enum
from typing import Any

import requests

from injector import inject
from player.Player import Player
from player.PlayerRegistry import PlayerRegistry
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.BackgroundIO import submit
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class PlayerService(FetchAndRegisterMixin):
    @inject
    def __init__(self, config: ServiceConfig, player_registry: PlayerRegistry):
        self.__name__ = "PlayerService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.players_endpoint = config.players_endpoint
        self.characters_endpoint = config.characters_endpoint
        self.player_registry = player_registry
        self.load_players()

    def reload_players(self) -> bool:
        return self._reload_collection(self.players_endpoint, "players", self.player_registry)

    def load_players(self):
        self._fetch_and_register(self.players_endpoint, "all players")
        self.logger.info(f"Initialized PlayerService instance with {str(len(self.player_registry))} player accounts.")

    def load_player(self, player_name: str):
        url = f"{self.players_endpoint}/name/{player_name}"
        return self._fetch_and_register(url, f"player '{player_name}'")

    def queue_save_player(self, player):
        with player.lock:
            payload = deepcopy(self._serialize_player(player))
            return submit(self._persist_player, payload)

    def save_player(self, player: Player) -> bool:
        result = self._persist_player(self._serialize_player(player))
        if result:
            self.player_registry.register(player)
        return result

    def _persist_player(self, payload) -> bool:
        player_id = str(payload.get("id") or "")
        if not player_id:
            self.logger.error("Refusing to save player without an id.")
            return False

        payload["id"] = player_id
        url = f"{self.players_endpoint}/{player_id}"
        try:
            response = requests.put(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            self.logger.error(f"Failed to save player {player_id} to {self.players_endpoint}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error saving player {player_id}: {e}", exc_info=True)
            return False

    def _build_fetch_item(self, player_data) -> Player:
        return Player.from_json(player_data)

    def _register_fetch_item(self, player: Player) -> None:
        self.player_registry.register(player)

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

import requests

from injector import inject
from player import Player, Character
from registry.PlayerRegistry import PlayerRegistry
from registry.CharacterRegistry import CharacterRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class PlayerService:
    @inject
    def __init__(self, config: ServiceConfig, player_registry: PlayerRegistry, character_registry: CharacterRegistry):
        self.__name__ = "PlayerService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.config = config
        self.player_registry = player_registry
        self.character_registry = character_registry
        self.message_bus = None
        self.player_list = self.get_accounts()
        self.character_list = self.get_characters()

    def start(self):
        self.logger.info(f"Initialized PlayerService instance with {str(len(self.player_list))} player accounts and {str(len(self.character_list))} player characters.")
        for player in self.player_list:
            self.player_registry.register_player(Player.from_json(player))
            for character_id in player["playerCharacterList"]:
                character = self.get_character(character_id)
                self.character_registry.register_character(player["id"], Character.from_json(character))
        self.logger.info(f"Populated registry with {str(len(self.character_registry.registry))} characters and {str(len(self.player_registry.registry))} players.")

    def get_accounts(self):
        return requests.get(self.config.players_endpoint).json()

    def get_account_by_id(self, account_id):
        url = self.config.players_endpoint+"/"+account_id
        self.logger.debug("GET: " + url)
        return requests.get(url).json()

    def get_account_by_name(self, account_name):
        url = self.config.players_endpoint+"/name/"+account_name
        self.logger.debug("GET: " + url)
        return requests.get(url).json()

    def get_characters(self):
        return requests.get(self.config.characters_endpoint).json()

    def get_player_characters(self, account_id):
        url = self.config.characters_endpoint + "/account/" + account_id
        self.logger.debug("GET: " + url)
        return requests.get(url).json()

    def get_character(self, character_id):
        url = self.config.characters_endpoint + "/" + character_id
        self.logger.debug(f"GET: {url}")
        return requests.get(url).json()

    def create_character(self, sheet):
        self.logger.debug("POST: " + self.config.characters_endpoint + ", SHEET=" + sheet)
        r = requests.post(self.config.characters_endpoint, json=sheet)
        if r.status_code == 201:
            return r.json()
        else:
            raise Exception(f"Error creating character: {r.text}")

    def delete_character(self, character_id):
        self.logger.debug("DELETE: " + self.config.characters_endpoint + ", CHARACTER_ID: " + character_id)
        return requests.delete(self.config.characters_endpoint, json={"characterId": character_id}).json()

    def create_account(self, account_name, password):
        data = {"accountName": account_name, "password": password}
        r = requests.post(self.config.players_endpoint, data=data)
        if r.status_code == 201:
            return r.json()["id"]
        else:
            raise Exception(f"Error creating account: {r.text}")

    def update_account(self, account_id, account_name=None, password=None):
        data = {}
        if account_name:
            data["accountName"] = account_name
        if password:
            data["password"] = password
        r = requests.put(f"{self.config.players_endpoint}/{account_id}", data=data)
        return r.status_code == 204

    def update_character(self, character_id, character_name=None):
        data = {}
        if character_name:
            data["characterName"] = character_name
        r = requests.put(f"{self.config.characters_endpoint}/{character_id}", data=data)
        return r.status_code == 204

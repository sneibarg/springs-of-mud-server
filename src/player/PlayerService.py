import requests

from injector import inject

from registry import RegistryService
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class PlayerService:
    @inject
    def __init__(self, config: ServiceConfig, registry_service: RegistryService):
        self.__name__ = "PlayerService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.config = config
        self.registry_service = registry_service
        self.player_list = self.get_accounts()
        self.character_list = self.get_characters()
        self.logger.info("Initialized PlayerService instance with "+str(len(self.player_list))+" player accounts and " +
                         str(len(self.character_list))+" player characters.")
        self.logger.info(f"PlayerService: {self.registry_service}")

    def get_in_room(self, character):
        loiterers = []
        for registered_characters in self.registry_service.character_registry.values():
            if registered_characters.name == character.name:
                continue
            other = self.registry_service.character_registry[registered_characters.name]
            if other.get_room_id() == character.get_room_id():
                loiterers.append(other)
        return loiterers

    def to_room(self, character, message, pattern):
        loiterers = self.get_in_room(character)
        cloaked_name = "Someone"
        cloaked = character.cloaked
        character_name = character.name
        if pattern is not None:
            pattern = pattern.replace('%p', cloaked_name if cloaked else character_name)
            pattern = pattern.replace('%m', message)
            message = pattern + "\r\n"
        else:
            message = message + "\r\n"
        for in_room in loiterers:
            in_room.get_writer().write(message.encode('utf-8'))

    def get_accounts(self):
        return requests.get(self.config.players_endpoint).json()

    def get_account_by_id(self, account_id):
        url = self.config.players_endpoint+"/"+account_id
        self.logger.debug("GET: " + url)
        return requests.get(url).json()

    def get_account_by_name(self, account_name):
        url = self.config.players_endpoint+"/name/"+account_name
        print(f"GET: {url}")
        self.logger.debug("GET: " + url)
        return requests.get(url).json()

    def get_characters(self):
        return requests.get(self.config.characters_endpoint).json()

    def get_player_characters(self, account_id):
        url = self.config.characters_endpoint + "/account/" + account_id
        self.logger.debug("GET: " + url)
        return requests.get(url).json()

    def get_character(self, character_id):
        parameters = {"characterId": character_id}
        self.logger.debug("GET: " + self.config.characters_endpoint + ", PARAMS=" + str(parameters))
        return requests.get(self.config.characters_endpoint, params=parameters).json()

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

    def visible(self, player):
        visible = []
        current_character = player.current_character
        role = current_character.role
        for character in self.registry_service.character_registry.values():
            if character.name == current_character.name:
                continue
            if character.cloaked and role == "player":
                continue
            else:
                visible.append(character)
        return visible

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

    @staticmethod
    def get_characters_url(self):
        return self.character_config['characters_endpoint']

    @staticmethod
    def get_character_url(self):
        return self.character_config['characters_endpoint']

    @staticmethod
    def get_accounts_url(self):
        return self.accounts_url

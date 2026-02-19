import requests

from server.LoggerFactory import LoggerFactory
from event import EventHandler


class PlayerService:
    def __init__(self, injector, player_config, character_config):
        self.__name__ = "PlayerService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.injector = injector
        self.player_config = player_config['endpoints']
        self.character_config = character_config['endpoints']
        self.event_handler = self.injector.get(EventHandler)
        self.player_list = self.get_accounts()
        self.character_list = self.get_characters()
        self.logger.info("Initialized PlayerService instance with "+str(len(self.player_list))+" player accounts and " +
                         str(len(self.character_list))+" player characters.")

    def get_in_room(self, character):
        loiterers = []
        for character_name in self.event_handler.character_registry:
            if character_name == character.get_name():
                continue
            other = self.event_handler.character_registry[character_name]
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

    def get_connected_player(self, name):
        return self.event_handler.character_registry[name]

    def get_connected_players(self):
        return self.event_handler.character_registry

    def disconnect_character(self, character):
        if character.get_name() in self.event_handler.character_registry:
            self.event_handler.unregister_character(character)

    def get_accounts(self):
        return requests.get(self.player_config['players_endpoint']).json()

    def get_account_by_id(self, account_id):
        url = self.player_config['players_endpoint']+"/"+account_id
        self.logger.debug("GET: " + url)
        return requests.get(url).json()

    def get_account_by_name(self, account_name):
        url = self.player_config['players_endpoint']+"/name/"+account_name
        print(f"GET: {url}")
        self.logger.debug("GET: " + url)
        return requests.get(url).json()

    def get_characters(self):
        return requests.get(self.character_config['characters_endpoint']).json()

    def get_player_characters(self, account_id):
        url = self.character_config['characters_endpoint'] + "/account/" + account_id
        self.logger.debug("GET: " + url)
        print(f"GET_PLAYER_CHARACTERS: {url}")
        return requests.get(url).json()

    def get_character(self, character_id):
        parameters = {"characterId": character_id}
        self.logger.debug("GET: " + self.character_config['characters_endpoint'] + ", PARAMS=" + str(parameters))
        return requests.get(self.character_config['characters_endpoint'], params=parameters).json()

    def create_character(self, sheet):
        self.logger.debug("POST: " + self.character_config['character_endpoint'] + ", SHEET=" + sheet)
        return requests.post(self.character_config['character_endpoint'], json=sheet).json()

    def delete_character(self, character_id):
        self.logger.debug("DELETE: " + self.character_config['character_endpoint'] + ", CHARACTER_ID: " + character_id)
        return requests.delete(self.character_config['character_endpoint'], json={"characterId": character_id}).json()

    def visible(self, player):
        visible = []
        current_character = player.current_character
        role = current_character.role
        for name in self.get_connected_players():
            if name == current_character.name:
                continue
            connected = self.get_connected_player(name)
            if connected.cloaked and role == "player":
                continue
            else:
                visible.append(connected)
        return visible

    def create_account(self, account_name, password):
        data = {"accountName": account_name, "password": password}
        r = requests.post(self.player_config['account_endpoint'], data=data)
        if r.status_code == 201:
            return r.json()["id"]
        else:
            raise Exception(f"Error creating account: {r.text}")

    def create_character(self, character_name, account_id):
        data = {"characterName": character_name, "accountId": account_id}
        r = requests.post(self.character_config['character_endpoint'], data=data)
        if r.status_code == 201:
            return r.json()["id"]
        else:
            raise Exception(f"Error creating character: {r.text}")

    def update_account(self, account_id, account_name=None, password=None):
        data = {}
        if account_name:
            data["accountName"] = account_name
        if password:
            data["password"] = password
        r = requests.put(f"{self.player_config['account_endpoint']}/{account_id}", data=data)
        return r.status_code == 204

    def update_character(self, character_id, character_name=None):
        data = {}
        if character_name:
            data["characterName"] = character_name
        r = requests.put(f"{self.character_config['character_endpoint']}/{character_id}", data=data)
        return r.status_code == 204

    @staticmethod
    def get_characters_url(self):
        return self.character_config['characters_endpoint']

    @staticmethod
    def get_character_url(self):
        return self.character_config['character_endpoint']

    @staticmethod
    def get_accounts_url(self):
        return self.accounts_url

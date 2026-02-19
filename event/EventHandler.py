from server.LoggerFactory import LoggerFactory


def do_to_mobile():
    pass


class EventHandler:
    def __init__(self):
        self.__name__ = "EventHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.command_list = None
        self.character_registry = dict()
        self.mobile_registry = dict()
        self.character_events = dict()
        self.mobile_events = dict()
        self.logger.info("Initialized EventHandler instance.")

    def set_command_list(self, command_list):
        self.command_list = command_list

    def register_character(self, character):
        self.logger.info("Registering character "+character.name)
        self.character_registry[character.name] = character

    def unregister_character(self, character):
        self.logger.info("Unregistering character "+character)
        del self.character_registry[character]

    def register_mobile(self, mobile):
        self.logger.debug("Registering mobile "+mobile.name)
        self.mobile_registry[mobile.get_instance_id()] = mobile

    def unregister_mobile(self, mobile):
        self.logger.debug("Unregistering mobile "+mobile.name)
        del self.mobile_registry[mobile.name]

    def process_events(self):
        self.process_player_events()

    def process_player_events(self):
        pass

    def to_mobile(self, player, cmd, mobile, parameters):
        command = [json_obj for json_obj in self.command_list if json_obj['name'] == cmd]
        if command is None:
            return

        if mobile.casefold() in self.character_registry:
            mobile = self.character_registry[mobile.title]

        if mobile.casefold() in self.mobile_registry:
            mobile = self.mobile_registry[mobile.title]



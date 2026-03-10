import re
import requests
from injector import inject, Injector

from typing import Union, Any
from asyncio import StreamWriter
from game import CommunicationService
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from registry import RegistryService
from command import CommandHandler
from area import AreaService
from mobile import MobileService, Mobile
from player import PlayerService, Player, Character
from event import EventHandler
from object import ItemService, Item


lambda_mappings = {
    'p': 'Player',
    'c': 'Character',
    'r': 'Room',
    'rs': 'RegistryService',
    'cs': 'CommandService',
    'cms': 'CommunicationService',
    'ps': 'PlayerService',
    'zs': 'AreaService',  # the 'zs' is ZoneService
    'ms': 'MobileService',
    'os': 'ObjectService',
    'ss': 'SkillService',
    'eh': 'EventHandler',
    'ch': 'CommandHandler',
    'sw': 'StreamWriter',
    'm': 'Mobile',
    'i': 'Item',
    'msg': 'str',
    'usage': 'lambda'
}


def get_class_obj(class_name):
    if class_name == "lambda":
        return None
    elif class_name == "Room":
        return class_name

    class_map = {
        'Player': Player,
        'Character': Character,
        'CommandService': CommandService,
        'CommunicationService': CommunicationService,
        'PlayerService': PlayerService,
        'RegistryService': RegistryService,
        'AreaService': AreaService,
        'MobileService': MobileService,
        'ObjectService': ItemService,
        'SkillService': None,
        'EventHandler': EventHandler,
        'CommandHandler': CommandHandler,
        'StreamWriter': StreamWriter,
        'Mobile': Mobile,
        'Item': Item,
        'str': str,
    }

    if class_name in class_map:
        return class_map[class_name]

    return globals().get(class_name)


def parse_args(args):
    input_args = re.search(r'lambda\s+([^:]+)', args).group(1)
    if ", " in input_args:
        input_args = input_args.split(", ")
    else:
        input_args = [input_args]
    return input_args


def get_args(lambda_string, player, injector, parameters):
    registry = injector.get(RegistryService)
    input_args = parse_args(lambda_string)
    args = []
    for arg in input_args:
        if arg == 'msg':
            if type(parameters) is not str:
                raise ValueError(f'Input is not a string.')
            if callable(parameters):
                raise ValueError(f'Input cannot be callable.')
            args.append(parameters)
            continue
        if arg in lambda_mappings:
            class_name = lambda_mappings[arg]
            class_obj = get_class_obj(class_name)
            obj = None
            if arg == 'p':
                obj = player
            elif arg == 'w':
                obj = player.writer()
            elif arg == 'm':
                obj = registry.get_mobile_from_registry(class_name)
            elif arg == 'c':
                obj = player.current_character
            elif arg == 'r':
                character = player.current_character
                room = registry.room_registry[character.room_id]
                class_obj = type(room)
                obj = room
            elif arg in ['ps', 'zs', 'ms', 'os', 'eh', 'ch', 'cs', 'rs']:
                obj = injector.get(class_obj)
            elif arg == 'usage':
                obj = player.usage
                if callable(obj):
                    args.append(obj)
                    continue

            if not isinstance(obj, class_obj):
                raise ValueError(f'Input is not a {class_name} object.')
            args.append(obj)
        else:
            raise ValueError(f'Invalid input argument: {arg}')
    return args


def handle_lambdas(command_service, player, command, parameters):
    if parameters is None:
        parameters = []

    lambda_list = command['lambda']
    for lambda_function in lambda_list:
        if lambda_function is not None:
            if not isinstance(lambda_function, str):
                raise TypeError('Expected string representation of lambda function')

            lambda_string = str(lambda_function)
            lambda_function = eval(lambda_function)

            if not callable(lambda_function):
                raise TypeError('lambda_function is not a callable function.')

            args = get_args(lambda_string, player, command_service.injector, parameters)
            command_service.logger.info("".join(str(args)) + " " + lambda_string)
            lambda_function(*args)
        else:
            raise ValueError('Failed to retrieve specified lambda function from REST service')


class CommandService:
    @inject
    def __init__(self, config: ServiceConfig, injector: Injector):
        self.__name__ = "CommandService"
        self.injector = injector
        self.commands_endpoint = config.commands_endpoint
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.command_list = self.load_command_list()
        self.logger.info("Initialized CommandService instance.")

    def load_command_list(self):
        response = requests.get(self.commands_endpoint)
        if response.status_code == 200:
            commands = response.json()
            return {command['name']: command for command in commands}
        raise ValueError('Failed to retrieve commands from MongoDB')

    def load_command_by_id(self, command_id):
        url = self.commands_endpoint + "/" + command_id
        return requests.get(url).json()

    def load_command_by_name(self, command_name):
        url = self.commands_endpoint + "/name/" + command_name
        if url:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    command = response.json()
                    if command:
                        self.command_list[command_name] = command
                        return command
            except Exception as e:
                self.logger.error(f"Failed to fetch command '{command_name}': {e}")
        return None

    def get_command_by_name(self, command_name):
        if command_name in self.command_list:
            return self.command_list[command_name]
        return self.load_command_by_name(command_name)

    def get_message(self, cmd):
        return self.command_list[cmd]['message']

    def call_lambda(self, player, command_name, command_list, parameters):
        command_json = CommandService.find_json_object_by_name(command_name, command_list)
        if command_json is None:
            raise ValueError('Null JSON returned from find_json_object_by_name')

        if command_json is False:
            player.writer().write(b"Huh?\r\n")
            return

        try:
            handle_lambdas(self, player, command_json, parameters)
        except ValueError as ve:
            self.logger.error("ValueError: " + str(ve))
            raise
        except TypeError as te:
            self.logger.error("TypeError: " + str(te))
            raise

    @staticmethod
    def find_json_object_by_name(name: str, commands: dict) -> Union[bool, Any]:
        if not commands:
            return False
        for command_name, command in commands.items():
            if name in command.get('shortcuts', []):
                return command
            if command.get('name') == name:
                return command
        return False
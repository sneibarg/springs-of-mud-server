import re
import requests

from server.LoggerFactory import LoggerFactory
from command import CommandHandler
from asyncio import StreamWriter
from area.AreaService import AreaService
from mobile import MobileService, RomMobile
from player import PlayerService, Player, Character
from event import EventHandler
from object.Item import Item
from server.server_util import find_json_object_by_name

lambda_mappings = {
    'p': 'Player',
    'c': 'Character',
    'r': 'RomRoom',
    'cs': 'CommandService',
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
    """
    Get class object by name for lambda command execution.
    All imports are explicitly referenced to ensure they're recognized as used.
    """
    if class_name == "lambda":
        return None
    elif class_name == "RomRoom":
        return class_name

    class_map = {
        'Player': Player,
        'Character': Character,
        'CommandService': None,
        'PlayerService': PlayerService,
        'AreaService': AreaService,
        'MobileService': MobileService,
        'ObjectService': None,
        'SkillService': None,
        'EventHandler': EventHandler,
        'CommandHandler': CommandHandler,
        'StreamWriter': StreamWriter,
        'Mobile': RomMobile,
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
    return input_args


def get_args(lambda_string, player, injector, parameters):
    from registry import RegistryService
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
                room = character.injector.get(RegistryService).room_registry[character.room_id]
                class_obj = type(room)
                obj = room
            elif arg in ['ps', 'zs', 'cs', 'ms', 'os', 'eh', 'ch']:
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
    def __init__(self, injector, config):
        self.__name__ = "CommandService"
        self.injector = injector
        self.config = config['endpoints']
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.command_list = self.get_commands()
        self.logger.info("Initialized CommandService instance.")

    def get_commands(self):
        commands_endpoint = self.config['commands_endpoint']
        response = requests.get(commands_endpoint)
        if response.status_code == 200:
            commands = response.json()
            return {command['name']: command for command in commands}
        raise ValueError('Failed to retrieve commands from MongoDB')

    def get_command(self, command_id):
        command_endpoint = self.config['command_endpoint']
        params = {'commandId': command_id}
        return requests.get(command_endpoint, params=params).json()

    def get_message(self, cmd):
        return self.command_list[cmd]['message']

    def call_lambda(self, player, command_name, command_list, parameters):
        command_json = find_json_object_by_name(command_name, command_list)
        if command_json is None:
            raise ValueError('Null JSON returned from find_json_object_by_name')

        if command_json is False:
            player.writer().write(b"Huh?\r\n")
            return

        try:
            print(f"PLAYER={player}\r\nJSON={command_json}\r\nPARAM={parameters}")
            handle_lambdas(self, player, command_json, parameters)
        except ValueError as ve:
            self.logger.error("ValueError: " + str(ve))
        except TypeError as te:
            self.logger.error("TypeError: " + str(te))

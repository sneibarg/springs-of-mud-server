import re
import requests
import inspect

from injector import inject, Injector
from typing import Union, Any
from area.RoomHandler import RoomHandler
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from registry.RegistryService import RegistryService
from area.AreaService import AreaService
from area.RoomService import RoomService
from mobile.MobileService import MobileService
from mobile.Mobile import Mobile
from event.EventHandler import EventHandler
from object.ItemService import ItemService
from server.connection.ConnectionManager import ConnectionManager
from server.messaging.MessageBus import MessageBus
from server.protocol.Message import MessageType, Message
from skill.SkillService import SkillService

lambda_mappings = {
    'p': 'Player',
    'c': 'Character',
    'r': 'Room',
    'rgs': 'RegistryService',
    'ah': 'AreaHandler',
    'rh': 'RoomHandler',
    'ih': 'ItemHandler',
    'mh': 'MobileHandler',
    'ch': 'CharacterHandler',
    'ph': 'PlayerHandler',
    'sh': 'SkillHandler',
    'cs': 'CommandService',
    'ps': 'PlayerService',
    'ms': 'MobileService',
    'os': 'ObjectService',
    'ss': 'SkillService',
    'eh': 'EventHandler',
    'cn': 'TelnetConnection',
    'mb': 'MessageBus',
    'm': 'Mobile',
    'i': 'Item',
    'msg': 'str',
    'usage': 'lambda'
}


def get_class_obj(class_name):
    if class_name == "lambda":
        return None

    class_map = {
        'CommandService': CommandService,
        'RegistryService': RegistryService,
        'RoomService': RoomService,
        'AreaService': AreaService,
        'MobileService': MobileService,
        'ObjectService': ItemService,
        'SkillService': SkillService,
        'EventHandler': EventHandler,
        'RoomHandler': RoomHandler,
        'MessageBus': MessageBus,
        'Mobile': Mobile,
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
            elif arg == 'm':
                obj = registry.get_mobile_from_registry(class_name)
            elif arg == 'c':
                obj = player.current_character
            elif arg == 'cn':
                telnet_connection = injector.get(ConnectionManager).get_connection_by_player(player.id)
                obj = telnet_connection if telnet_connection else None
            elif arg == 'r':
                character = player.current_character
                room = registry.room_registry[character.room_id]
                class_obj = type(room)
                obj = room
            elif arg == 'i':  # Item unimplemented
                pass
            elif arg in ['ps', 'zs', 'ms', 'os', 'eh', 'ch', 'cs', 'rh', 'rgs', 'mb', 'cnh', 'rh', 'ih', 'ah', 'mh', 'ph', 'ss', 'sh']:
                obj = injector.get(class_obj)
            elif arg == 'usage':
                obj = player.usage
                if callable(obj):
                    args.append(obj)
                    continue

            if class_obj is not None and not isinstance(obj, class_obj):
                raise ValueError(f'Input is not a {class_name} object.')
            args.append(obj)
        else:
            raise ValueError(f'Invalid input argument: {arg}')
    return args


async def handle_lambdas(command_service, player, command, parameters):
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
            result = lambda_function(*args)
            if inspect.isawaitable(result):
                await result
        else:
            raise ValueError('Failed to retrieve specified lambda function from REST service')


class CommandService:
    @inject
    def __init__(self, config: ServiceConfig, injector: Injector):
        self.__name__ = "CommandService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.injector = injector
        self.message_bus = injector.get(MessageBus)
        self.commands_endpoint = config.commands_endpoint
        self.command_not_found_message = Message(type=MessageType.GAME, data={"text": "Huh?\r\n"})
        self.command_list = self.load_command_list()
        self.logger.info(f"Initialized CommandService instance with a total of {len(self.command_list)} commands.")

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

    async def call_lambda(self, player, command_name, command_list, parameters):
        command_json = CommandService.find_json_object_by_name(command_name, command_list)
        if command_json is None:
            raise ValueError('Null JSON returned from find_json_object_by_name')

        if command_json is False:
            return await self.message_bus.send_to_character(player.id, self.command_not_found_message)

        try:
            await handle_lambdas(self, player, command_json, parameters)
        except ValueError as ve:
            self.logger.error("ValueError: " + str(ve))
            raise
        except TypeError as te:
            self.logger.error("TypeError: " + str(te))
            raise

    async def handle_command(self, player, command):
        usage = None
        cmd, parameters = self.extract_parameters(command)
        if cmd is None:
            await self.message_bus.send_to_character(player.id, self.message_bus.text_to_message(f"Huh?\r\n"))
            return None

        if cmd is not None and "usage" in cmd:
            usage = cmd['usage']

        if usage is not None:
            usage_function = eval(usage)
            if not callable(usage_function):
                self.logger.info("NOT_CALLABLE: " + str(usage_function))
            else:
                player.set_usage(usage_function)

        self.logger.debug(f"CMD: {cmd['name']}, PARAMETERS: {parameters}, USAGE: {str(usage)}")
        return await self.call_lambda(player, cmd['name'], self.command_list, parameters)

    def extract_parameters(self, command: str) -> Union[tuple[Any, str], tuple[None, None]]:
        for cmd in self.command_list:
            json = self.command_list[cmd]
            shortcuts = json['shortcuts'].split(", ")
            if command in shortcuts or command.startswith(json['name']):
                return json, ' '.join(re.split(' ', command)[1:]).strip()
        return None, None

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

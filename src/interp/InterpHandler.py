import inspect
import re

from injector import inject, Injector
from interp.SocialRegistry import SocialRegistry
from interp.InterpService import InterpService
from interp.InterpUtil import InterpUtil
from interp.SocialHandler import SocialHandler
from interp.InterpRegistry import InterpRegistry
from game.RegistryService import RegistryService
from area.AreaService import AreaService
from area.RoomService import RoomService
from mobile.MobileService import MobileService
from mobile.Mobile import Mobile
from fight.FightHandler import FightHandler
from player.PlayerHandler import PlayerHandler
from player.PlayerService import PlayerService
from object.ItemService import ItemService
from server.LoggerFactory import LoggerFactory
from server.connection.ConnectionManager import ConnectionManager
from area.RoomHandler import RoomHandler
from object.ItemHandler import ItemHandler
from server.messaging import MessageBus
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
    'cmh': 'InterpHandler',
    'sh': 'SkillHandler',
    'cs': 'InterpService',
    'ps': 'CharacterService',
    'ms': 'MobileService',
    'os': 'ObjectService',
    'ss': 'SkillService',
    'eh': 'FightHandler',
    'cn': 'TelnetConnection',
    'mb': 'MessageBus',
    'v': 'Character',  # victim aka target
    'm': 'Mobile',
    'i': 'Item',
    'msg': 'str',
    'usage': 'lambda'
}


def get_class_obj(class_name):
    if class_name == "lambda":
        return None

    class_map = {
        'InterpService': InterpService,
        'RegistryService': RegistryService,
        'RoomService': RoomService,
        'AreaService': AreaService,
        'MobileService': MobileService,
        'ObjectService': ItemService,
        'SkillService': SkillService,
        'CharacterService': PlayerService,
        'FightHandler': FightHandler,
        'RoomHandler': RoomHandler,
        'PlayerHandler': PlayerHandler,
        'ItemHandler': ItemHandler,
        'cmh': InterpHandler,
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


def get_args(lambda_string, player, character, injector, parameters):
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
                for playing in player.current_characters:
                    if character.name == playing.name:
                        obj = playing
                        break
            elif arg == 'cn':
                telnet_connection = injector.get(ConnectionManager).get_connection_by_character(character.id)
                obj = telnet_connection if telnet_connection else None
            elif arg == 'r':
                room = registry.room_registry.get_room_by_id(character.room_id)
                class_obj = type(room)
                obj = room
            elif arg == 'i':  # Item unimplemented
                pass
            elif arg in ['ps', 'zs', 'ms', 'os', 'eh', 'ch', 'cs', 'rh', 'rgs', 'mb',
                         'cnh', 'rh', 'ih', 'ah', 'mh', 'ph', 'ss', 'sh', 'cmh']:
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


async def handle_lambdas(handler, player, character, command, parameters):
    if parameters is None:
        parameters = []

    lambda_list = getattr(command, "lambdas", None)
    if lambda_list is None and isinstance(command, dict):
        lambda_list = command.get("lambda") or command.get("lambdas")
    lambda_list = lambda_list or []
    for lambda_function in lambda_list:
        if lambda_function is not None:
            if not isinstance(lambda_function, str):
                raise TypeError('Expected string representation of lambda function')

            lambda_string = str(lambda_function)
            lambda_function = eval(lambda_function)

            if not callable(lambda_function):
                raise TypeError('lambda_function is not a callable function.')

            args = get_args(lambda_string, player, character, handler.injector, parameters)
            result = lambda_function(*args)
            if inspect.isawaitable(result):
                await result
        else:
            raise ValueError('Failed to retrieve specified lambda function from REST service')


class InterpHandler:
    @inject
    def __init__(self, injector: Injector, message_bus: MessageBus, interp_registry: InterpRegistry, social_registry: SocialRegistry, social_handler: SocialHandler):
        self.__name__ = "InterpHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.injector = injector
        self.message_bus = message_bus
        self.interp_registry = interp_registry
        self.social_registry = social_registry
        self.social_handler = social_handler
        self.command_not_found_message = self.message_bus.text_to_message("Huh?\r\n")

    def get_message(self, cmd):
        command = self.interp_registry.get_or_none(name=cmd.lower())
        if command is None:
            raise ValueError(f"Command {cmd} not found in command registry.")
        return InterpUtil.command_attr(command, "message", None)

    async def call_lambda(self, player, character, command_name, command_list, parameters):
        command_json = InterpUtil.find_command_by_name(command_name, command_list)
        if command_json is None:
            return await self.message_bus.send_to_character(character.id, self.command_not_found_message)

        try:
            await handle_lambdas(self, player, character, command_json, parameters)
        except ValueError as ve:
            self.logger.error("ValueError: " + str(ve))
            raise
        except TypeError as te:
            self.logger.error("TypeError: " + str(te))
            raise

    async def handle_command(self, player, character, command):
        cmd, parameters = InterpUtil.extract_parameters(self.interp_registry, command)
        if cmd is None:
            social = self.social_registry.get_or_none(name=command.lower())
            if social is not None:
                return await self.social_handler.handle_social(character, command, social)
            await self.message_bus.send_to_character(character.id, self.command_not_found_message)
            return None

        usage = InterpUtil.command_attr(cmd, "usage", None)
        if isinstance(usage, str) and usage.strip():
            usage_function = eval(usage)
            if not callable(usage_function):
                self.logger.debug("NOT_CALLABLE: " + str(usage_function))
            else:
                player.usage = usage_function

        cmd_name = InterpUtil.command_attr(cmd, "name", "")
        self.logger.debug(f"CMD: {cmd_name}, PARAMETERS: {parameters}, USAGE: {str(usage)}")
        return await self.call_lambda(player, character, cmd_name, self.interp_registry.all_commands(), parameters)

    async def help_usage(self, character, argument: str = ""):
        arg_all = " ".join((argument or "").split()).lower()
        if not arg_all:
            arg_all = "summary"
        output_parts = []
        found = False
        for command in self.interp_registry.all_commands():
            help_entry = InterpUtil.command_attr(command, "help", None)
            if help_entry is None:
                continue

            if not help_entry.keyword:
                continue

            q_words = arg_all.split()
            k_words = help_entry.keyword.split()
            if not q_words or not k_words:
                continue
            if not all(any(k.startswith(q) for k in k_words) for q in q_words):
                continue

            level_raw = getattr(help_entry, "level", 0)
            try:
                level = int(level_raw)
            except (TypeError, ValueError):
                level = 0

            if found:
                output_parts.append("\n\r============================================================\n\r\n\r")
            found = True

            if level >= 0 and arg_all != "imotd":
                output_parts.append(str(getattr(help_entry, "keyword", "")))
                output_parts.append("\n\r")

            text = str(getattr(help_entry, "text", "") or "")
            if text.startswith("."):
                text = text[1:]
            output_parts.append(text)

        message_text = "".join(output_parts) if len(output_parts) > 0 else "No help on that word.\n\r"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message_text))

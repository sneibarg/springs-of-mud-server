import re

from enum import IntEnum
from typing import Dict, Any, Iterable
from injector import singleton, Injector
from area.AreaHandler import AreaHandler
from area.RoomHandler import RoomHandler
from object.ItemHandler import ItemHandler
from mobile.MobileHandler import MobileHandler
from player.PlayerHandler import PlayerHandler
from game.GameData import GameData
from game.GameService import GameService
from mobile.MobileService import MobileService
from object.ObjectMacros import ObjectMacros
from player.CharacterConstants import CharacterConstants
from player.CharacterMacros import CharacterMacros
from player.PlayerService import PlayerService
from server.LoggerFactory import LoggerFactory
from skill.SkillService import SkillService
from registry.RegistryService import RegistryService
from registry import ItemRegistry, SkillRegistry
from event.EventHandler import EventHandler
from command.CommandService import CommandService
from server.handlers.ConnectionHandler import ConnectionHandler
from area.AreaService import AreaService
from area.RoomService import RoomService
from object.ItemService import ItemService
from server.connection.ConnectionManager import ConnectionManager
from server.messaging.MessageBus import MessageBus
from server.session.AuthenticationService import AuthenticationService
from server.session.SessionHandler import SessionHandler
from server.ServiceConfig import ServiceConfig
from update import WeatherService


logger = LoggerFactory.get_logger("ServerUtil")


class ServerUtil:
    def __init__(self):
        pass

    @staticmethod
    def bind_dependencies(service_config) -> Injector:
        injector = Injector()
        injector.binder.bind(ServiceConfig, to=service_config, scope=singleton)

        ServerUtil._bind_network_services(injector)
        ServerUtil._bind_registries(injector)
        ServerUtil._bind_handlers(injector)
        ServerUtil._bind_game_data(injector)
        ServerUtil._bind_game_services(injector, service_config)

        injector.binder.bind(ConnectionHandler, scope=singleton)
        injector.binder.bind(SessionHandler, to=SessionHandler(injector.get(GameData).constants.max['idleTime']), scope=singleton)

        return injector

    @staticmethod
    def _bind_network_services(injector):
        injector.binder.bind(MessageBus, scope=singleton)
        injector.binder.bind(ConnectionManager, scope=singleton)

    @staticmethod
    def _bind_game_services(injector, service_config):
        injector.binder.bind(GameService, scope=singleton)
        injector.binder.bind(SkillService, scope=singleton)
        injector.binder.bind(PlayerService, scope=singleton)
        injector.binder.bind(CommandService, scope=singleton)
        injector.binder.bind(AreaService, scope=singleton)
        injector.binder.bind(RoomService, scope=singleton)
        injector.binder.bind(MobileService, scope=singleton)
        injector.binder.bind(AuthenticationService, scope=singleton)
        injector.binder.bind(WeatherService, scope=singleton)
        injector.binder.bind(ItemService, to=ItemService(service_config,
                                                         injector.get(ItemRegistry),
                                                         injector.get(SkillRegistry),
                                                         injector.get(GameService).game_data,
                                                         injector.get(ObjectMacros)), scope=singleton)

    @staticmethod
    def _bind_handlers(injector):
        injector.binder.bind(AreaHandler, scope=singleton)
        injector.binder.bind(RoomHandler, scope=singleton)
        injector.binder.bind(EventHandler, scope=singleton)
        injector.binder.bind(ItemHandler, scope=singleton)
        injector.binder.bind(MobileHandler, scope=singleton)
        injector.binder.bind(PlayerHandler, scope=singleton)
        logger.info(f"All game handlers have been bound.")

    @staticmethod
    def _bind_registries(injector):
        from registry import PlayerRegistry, ItemRegistry, SkillRegistry, CharacterRegistry, MobileRegistry, AreaRegistry, RoomRegistry
        injector.binder.bind(PlayerRegistry, scope=singleton)
        injector.binder.bind(CharacterRegistry, scope=singleton)
        injector.binder.bind(MobileRegistry, scope=singleton)
        injector.binder.bind(AreaRegistry, scope=singleton)
        injector.binder.bind(RoomRegistry, scope=singleton)
        injector.binder.bind(ItemRegistry, scope=singleton)
        injector.binder.bind(SkillRegistry, scope=singleton)
        injector.binder.bind(RegistryService, scope=singleton)
        injector.get(RegistryService)
        logger.info(f"The RegistryService has been bound with all injected dependencies: {injector.get(RegistryService)}")

    @staticmethod
    def _bind_game_data(injector):
        injector.binder.bind(GameData, to=injector.get(GameService).game_data, scope=singleton)
        injector.binder.bind(CharacterConstants, to=CharacterConstants(injector.get(GameData).constants,
                                                                       injector.get(GameService).enums['positions'],
                                                                       injector.get(GameService).enums['actBits'],
                                                                       injector.get(GameData).attribute_bonuses), scope=singleton)
        injector.binder.bind(CharacterMacros, to=CharacterMacros(injector.get(RegistryService),
                                                                 injector.get(GameData).enums['roomFlags'],
                                                                 injector.get(GameData).attribute_bonuses,
                                                                 injector.get(CharacterConstants)), scope=singleton)
        injector.binder.bind(ObjectMacros, to=ObjectMacros(injector.get(GameData).races,
                                                           injector.get(GameData).item_table,
                                                           injector.get(GameService).enums['itemTypes']), scope=singleton)

    @staticmethod
    def load_services(injector) -> None:
        game_service = injector.get(GameService)
        player_service = injector.get(PlayerService)
        room_service = injector.get(RoomService)
        area_service = injector.get(AreaService)
        skill_service = injector.get(SkillService)
        item_service = injector.get(ItemService)
        weather_service = injector.get(WeatherService)
        mobile_service = injector.get(MobileService)

        game_service.set_weather_service(weather_service)
        game_service.start_mobile_service(mobile_service)

        logger.info("The following services have been started: ")
        logger.info(f"{game_service.__name__}; {player_service.__name__}; {room_service.__name__}; {area_service.__name__}; {skill_service.__name__}; {item_service.__name__}; {weather_service.__name__}; {mobile_service.__name__}")

    @staticmethod
    def camel_to_snake_case(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        if dictionary is None:
            return {}

        def camel_case_to_snake_case(string: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        snake_case_dict = {}
        try:
            snake_case_dict = {camel_case_to_snake_case(key): value for key, value in dictionary.items()}
        except AttributeError:
            logger.error(f"Error converting dictionary to snake case: {dictionary}")
        return snake_case_dict

    @staticmethod
    def build_int_enum(enum_name: str, enum_fields: dict[str, int] | list[str] | tuple[str, ...]) -> type[IntEnum]:
        if isinstance(enum_fields, dict):
            items: Iterable[tuple[str, int]] = (
                (str(member_name), int(member_value))
                for member_name, member_value in enum_fields.items()
            )
        elif isinstance(enum_fields, (list, tuple)):
            items = (
                (str(member_name), index)
                for index, member_name in enumerate(enum_fields)
            )
        else:
            raise TypeError(
                f"enum_fields for '{enum_name}' must be dict/list/tuple, got {type(enum_fields).__name__}"
            )

        members = {}
        for member_name, member_value in items:
            normalized_name = member_name.strip().upper()
            if not normalized_name:
                raise ValueError(f"Enum '{enum_name}' contains an empty member name")
            members[normalized_name] = member_value

        return IntEnum(enum_name, members)

    @staticmethod
    def convert_flags(flag_value: str) -> int:
        numeric_value = 0
        for char in str(flag_value).upper():
            if char.isalpha() and 'A' <= char <= 'Z':
                bit_position = ord(char) - ord('A')
                numeric_value |= (1 << bit_position)
        return numeric_value

import random
import re
import time

from enum import IntEnum
from typing import Dict, Any, Iterable
from injector import singleton, Injector

from area.ShopService import ShopService
from area.AreaHandler import AreaHandler
from area.ResetService import ResetService
from area.RoomHandler import RoomHandler
from area.SpecialService import SpecialService
from interp.HelpService import HelpService
from interp.InterpHandler import InterpHandler
from interp.SocialHandler import SocialHandler
from interp.SocialService import SocialService
from object.ItemHandler import ItemHandler
from mobile.MobileHandler import MobileHandler
from player.PlayerHandler import PlayerHandler
from game.GameData import GameData
from game.GameService import GameService
from game.NoteHandler import NoteHandler
from game.NoteService import NoteService
from mobile.MobileService import MobileService
from object.ObjectMacros import ObjectMacros
from player.CharacterConstants import CharacterConstants
from player.CharacterMacros import CharacterMacros
from player.PlayerService import PlayerService
from player.CharacterService import CharacterService
from server.LoggerFactory import LoggerFactory
from skill.SkillService import SkillService
from game.RegistryService import RegistryService
from fight.FightHandler import FightHandler
from interp.InterpService import InterpService
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
        from object.ItemRegistry import ItemRegistry
        from skill.SkillRegistry import SkillRegistry
        injector.binder.bind(GameService, scope=singleton)
        injector.binder.bind(SkillService, scope=singleton)
        injector.binder.bind(PlayerService, scope=singleton)
        injector.binder.bind(CharacterService, scope=singleton)
        injector.binder.bind(HelpService, scope=singleton)
        injector.binder.bind(InterpService, scope=singleton)
        injector.binder.bind(AreaService, scope=singleton)
        injector.binder.bind(RoomService, scope=singleton)
        injector.binder.bind(MobileService, scope=singleton)
        injector.binder.bind(AuthenticationService, scope=singleton)
        injector.binder.bind(WeatherService, scope=singleton)
        injector.binder.bind(SocialService, scope=singleton)
        injector.binder.bind(NoteService, scope=singleton)
        injector.binder.bind(ItemService, to=ItemService(service_config,
                                                         injector.get(ItemRegistry),
                                                         injector.get(SkillRegistry),
                                                         injector.get(GameService).game_data,
                                                         injector.get(ObjectMacros)), scope=singleton)

    @staticmethod
    def _bind_handlers(injector):
        injector.binder.bind(SocialHandler, scope=singleton)
        injector.binder.bind(AreaHandler, scope=singleton)
        injector.binder.bind(RoomHandler, scope=singleton)
        injector.binder.bind(FightHandler, scope=singleton)
        injector.binder.bind(ItemHandler, scope=singleton)
        injector.binder.bind(MobileHandler, scope=singleton)
        injector.binder.bind(PlayerHandler, scope=singleton)
        injector.binder.bind(InterpHandler, scope=singleton)
        injector.binder.bind(NoteHandler, scope=singleton)
        logger.info(f"All game handlers have been bound.")

    @staticmethod
    def _bind_registries(injector):
        from game.NoteRegistry import NoteRegistry
        from player.PlayerRegistry import PlayerRegistry
        from player.CharacterRegistry import CharacterRegistry
        from mobile.MobileRegistry import MobileRegistry
        from area.AreaRegistry import AreaRegistry
        from area.RoomRegistry import RoomRegistry
        from object.ItemRegistry import ItemRegistry
        from skill.SkillRegistry import SkillRegistry
        from interp.InterpRegistry import InterpRegistry
        from interp.SocialRegistry import SocialRegistry
        from interp.HelpRegistry import HelpRegistry
        from area.ShopRegistry import ShopRegistry
        from area.SpecialRegistry import SpecialRegistry
        from area.ResetRegistry import ResetRegistry

        injector.binder.bind(NoteRegistry, scope=singleton)
        injector.binder.bind(PlayerRegistry, scope=singleton)
        injector.binder.bind(CharacterRegistry, scope=singleton)
        injector.binder.bind(MobileRegistry, scope=singleton)
        injector.binder.bind(AreaRegistry, scope=singleton)
        injector.binder.bind(RoomRegistry, scope=singleton)
        injector.binder.bind(ItemRegistry, scope=singleton)
        injector.binder.bind(SkillRegistry, scope=singleton)
        injector.binder.bind(HelpRegistry, scope=singleton)
        injector.binder.bind(InterpRegistry, scope=singleton)
        injector.binder.bind(SocialRegistry, scope=singleton)
        injector.binder.bind(ShopRegistry, scope=singleton)
        injector.binder.bind(ResetRegistry, scope=singleton)
        injector.binder.bind(SpecialRegistry, scope=singleton)
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
                                                           injector.get(GameService).enums['itemTypes'],
                                                           injector.get(GameService).enums['damageTypes']), scope=singleton)

    @staticmethod
    def load_services(injector) -> None:
        game_service = injector.get(GameService)
        player_service = injector.get(PlayerService)
        character_service = injector.get(CharacterService)
        room_service = injector.get(RoomService)
        area_service = injector.get(AreaService)
        skill_service = injector.get(SkillService)
        item_service = injector.get(ItemService)
        weather_service = injector.get(WeatherService)
        social_service = injector.get(SocialService)
        mobile_service = injector.get(MobileService)
        help_service = injector.get(HelpService)
        interp_service = injector.get(InterpService)
        note_service = injector.get(NoteService)
        shop_service = injector.get(ShopService)
        reset_service = injector.get(ResetService)
        special_service = injector.get(SpecialService)

        game_service.set_weather_service(weather_service)
        game_service.start_mobile_service(mobile_service)

        service_list = (f"- {game_service.__name__}\r\n- {player_service.__name__}\r\n- {room_service.__name__}\r\n- {area_service.__name__}\r\n- "
                        f"{skill_service.__name__}\r\n- {item_service.__name__}\r\n- {weather_service.__name__}\r\n- {mobile_service.__name__}\r\n- "
                        f"{interp_service.__name__}\r\n- {social_service.__name__}\r\n- {note_service.__name__}\r\n- {character_service.__name__}\r\n- "
                        f"{help_service.__name__}\r\n- {shop_service.__name__}\r\n- {reset_service.__name__}\r\n- {special_service.__name__}\r\n")
        logger.info(f"The following services have been started:\r\n{service_list}")

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

    @staticmethod
    def generate_mongo_id() -> str:
        timestamp = int(time.time()).to_bytes(4, 'big')
        machine_id = random.getrandbits(24).to_bytes(3, 'big')
        process_id = random.getrandbits(16).to_bytes(2, 'big')
        counter = random.getrandbits(24).to_bytes(3, 'big')
        return (timestamp + machine_id + process_id + counter).hex()

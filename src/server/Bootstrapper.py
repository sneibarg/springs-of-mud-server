from injector import Injector, singleton

from api.CharacterApi import CharacterApi
from api.FightApi import FightApi
from api.GameApi import GameApi
from api.InterpApi import InterpApi
from api.SkillApi import SkillApi
from area.AreaHandler import AreaHandler
from area.AreaRegistry import AreaRegistry
from area.AreaService import AreaService
from area.ResetRegistry import ResetRegistry
from area.ResetService import ResetService
from area.RoomHandler import RoomHandler
from area.RoomRegistry import RoomRegistry
from area.RoomService import RoomService
from area.ShopRegistry import ShopRegistry
from area.ShopService import ShopService
from area.SpecialRegistry import SpecialRegistry
from area.SpecialService import SpecialService
from fight.FightHandler import FightHandler
from fight.CombatRegistry import CombatRegistry
from game.EnumProvider import EnumProvider
from game.GameData import GameData
from game.GameService import GameService
from game.HandlerService import HandlerService
from game.NoteHandler import NoteHandler
from game.NoteRegistry import NoteRegistry
from game.NoteService import NoteService
from game.RegistryService import RegistryService
from game.UpdateHandler import UpdateHandler
from game.WeatherHandler import WeatherHandler
from game.WizHandler import WizHandler
from interp.HelpRegistry import HelpRegistry
from interp.HelpService import HelpService
from interp.InterpHandler import InterpHandler
from interp.InterpRegistry import InterpRegistry
from interp.InterpService import InterpService
from interp.SocialHandler import SocialHandler
from interp.SocialRegistry import SocialRegistry
from interp.SocialService import SocialService
from interp.commands.Communications import Communications
from interp.commands.Fight import Fight
from interp.commands.Info import Info
from interp.commands.Movement import Movement
from interp.commands.Object import Object
from interp.commands.Wiz import Wiz
from item.BodyForm import BodyForm
from item.BodyParts import BodyParts
from item.ItemHandler import ItemHandler
from item.ItemRegistry import ItemRegistry
from item.ItemService import ItemService
from mobile.MobileHandler import MobileHandler
from mobile.MobileRegistry import MobileRegistry
from mobile.MobileService import MobileService
from player.CharacterRegistry import CharacterRegistry
from player.CharacterService import CharacterService
from player.PlayerHandler import PlayerHandler
from player.PlayerRegistry import PlayerRegistry
from player.PlayerService import PlayerService
from server.ServiceConfig import ServiceConfig
from server.connection import ConnectionManager
from server.handlers.ConnectionHandler import ConnectionHandler
from server.messaging import MessageBus
from server.session.AuthenticationService import AuthenticationService
from server.session.SessionHandler import SessionHandler
from skill.SkillRegistry import SkillRegistry
from skill.SkillService import SkillService
from skill.SpellRegistry import SpellRegistry
from skill.SpellService import SpellService
from server.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_logger("Bootstrapper")


class Bootstrapper:
    @staticmethod
    def create_injector(service_config: ServiceConfig) -> Injector:
        injector = Injector()
        injector.binder.bind(ServiceConfig, to=service_config, scope=singleton)
        injector.binder.bind(GameService, scope=singleton)

        Bootstrapper._bind_game_data(injector)
        Bootstrapper._bind_network(injector)
        Bootstrapper._bind_registries(injector)
        Bootstrapper._bind_handlers(injector)
        Bootstrapper._bind_apis(injector)
        Bootstrapper._bind_game_services(injector, service_config)

        injector.binder.bind(ConnectionHandler, scope=singleton)
        injector.binder.bind(
            SessionHandler,
            to=SessionHandler(
                injector.get(GameService).enums.get("gameParameters")["MAX_IDLE"]
            ),
            scope=singleton,
        )

        logger.info("IOC container fully configured.")
        return injector

    @staticmethod
    def _bind_network(injector: Injector):
        injector.binder.bind(MessageBus, scope=singleton)
        injector.binder.bind(ConnectionManager, scope=singleton)

    @staticmethod
    def _bind_singleton_classes(injector: Injector, classes: list):
        for clazz in classes:
            injector.binder.bind(clazz, scope=singleton)

    @staticmethod
    def _bind_registries(injector: Injector):
        Bootstrapper._bind_singleton_classes(injector, [
            NoteRegistry, PlayerRegistry, CharacterRegistry, MobileRegistry,
            RoomRegistry, ItemRegistry, SkillRegistry, SpellRegistry,
            HelpRegistry, InterpRegistry, SocialRegistry, ShopRegistry,
            ResetRegistry, SpecialRegistry, RegistryService, AreaRegistry,
            CombatRegistry,
        ])
        logger.info("All registries bound.")

    @staticmethod
    def _bind_handlers(injector: Injector):
        Bootstrapper._bind_singleton_classes(injector, [
            SocialHandler, Communications, Fight, Info, Movement, Object, Wiz,
            AreaHandler, RoomHandler, FightHandler, ItemHandler, MobileHandler,
            PlayerHandler, WizHandler, InterpHandler, NoteHandler,
            WeatherHandler, UpdateHandler
        ])
        logger.info("All command and game handlers bound.")

    @staticmethod
    def _bind_apis(injector: Injector):
        injector.binder.bind(SkillApi, scope=singleton)
        injector.binder.bind(FightApi, scope=singleton)
        injector.binder.bind(InterpApi, scope=singleton)

    @staticmethod
    def _bind_game_services(injector: Injector, service_config: ServiceConfig):
        Bootstrapper._bind_singleton_classes(injector, [
            SkillService, SpellService, PlayerService,
            CharacterService, HelpService, InterpService,
            AreaService, RoomService, MobileService,
            AuthenticationService, SocialService, NoteService, HandlerService
        ])

        injector.binder.bind(ItemService, to=ItemService(service_config, injector.get(ItemRegistry), injector.get(SkillRegistry), injector.get(GameService).game_data), scope=singleton)

    @staticmethod
    def _bind_game_data(injector: Injector):
        game_service = injector.get(GameService)
        game_data = game_service.game_data
        enum_provider = EnumProvider(game_service.enums)

        injector.binder.bind(EnumProvider, to=enum_provider, scope=singleton)
        injector.binder.bind(GameData, to=game_data, scope=singleton)

        GameApi.configure(game_data, enum_provider)
        BodyForm.configure(game_data)
        BodyParts.configure(game_data)

    @staticmethod
    def lazy_load(injector: Injector) -> None:
        CharacterApi.lazy_load(
            injector.get(WeatherHandler),
            registry_service=injector.get(RegistryService),
        )

        to_load = [GameService, PlayerService, CharacterService, ShopService, ResetService,
                   SpecialService, RoomService, AreaService, SkillService, SpellService,
                   ItemService, SocialService, MobileService, HelpService, InterpService, NoteService]

        for service in to_load:
            injector.get(service)

        injector.get(Fight).lazy_load()
        injector.get(SkillApi).lazy_load()
        injector.get(UpdateHandler)
        injector.get(FightHandler).set_mobile_handler(injector.get(MobileHandler))
        injector.get(AreaHandler).initialize_world()
        injector.get(GameService).set_update_handler(injector.get(UpdateHandler))

        service_list = "; ".join(s.__name__ for s in to_load)
        logger.info(f"The following services have been started: {service_list}.")

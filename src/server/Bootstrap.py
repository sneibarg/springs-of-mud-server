from injector import Injector, singleton

from api.CharacterApi import CharacterApi
from api.CommunicationsApi import CommunicationsApi
from api.FightApi import FightApi
from api.InterpApi import InterpApi
from api.ItemApi import ItemApi
from api.MobileApi import MobileApi
from api.MovementApi import MovementApi
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

logger = LoggerFactory.get_logger("ServerBootstrap")


class ServerBootstrap:
    @staticmethod
    def create_injector(service_config: ServiceConfig) -> Injector:
        injector = Injector()
        injector.binder.bind(ServiceConfig, to=service_config, scope=singleton)

        ServerBootstrap._bind_network(injector)
        ServerBootstrap._bind_registries(injector)
        ServerBootstrap._bind_handlers(injector)
        ServerBootstrap._bind_apis(injector)
        ServerBootstrap._bind_game_data(injector)
        ServerBootstrap._bind_game_services(injector, service_config)

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
        ServerBootstrap._bind_singleton_classes(injector, [
            NoteRegistry, PlayerRegistry, CharacterRegistry, MobileRegistry,
            RoomRegistry, ItemRegistry, SkillRegistry, SpellRegistry,
            HelpRegistry, InterpRegistry, SocialRegistry, ShopRegistry,
            ResetRegistry, SpecialRegistry, RegistryService, AreaRegistry,
            CombatRegistry,
        ])
        logger.info("All registries bound.")

    @staticmethod
    def _bind_handlers(injector: Injector):
        ServerBootstrap._bind_singleton_classes(injector, [
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
        ServerBootstrap._bind_singleton_classes(injector, [
            GameService, SkillService, SpellService, PlayerService,
            CharacterService, HelpService, InterpService, AreaService,
            RoomService, MobileService, AuthenticationService,
            SocialService, NoteService, HandlerService
        ])

        injector.binder.bind(
            ItemService,
            to=ItemService(
                service_config,
                injector.get(ItemRegistry),
                injector.get(SkillRegistry),
                injector.get(GameService).game_data
            ),
            scope=singleton
        )

    @staticmethod
    def _bind_game_data(injector: Injector):
        game_data = injector.get(GameService).game_data
        injector.binder.bind(GameData, to=game_data, scope=singleton)

        BodyForm.configure(game_data)
        BodyParts.configure(game_data)
        ItemApi.configure(game_data)
        MobileApi.configure(game_data)
        CharacterApi.configure(game_data)
        MovementApi.configure(game_data)
        CommunicationsApi.configure(game_data)

    @staticmethod
    def lazy_load_all(injector: Injector) -> None:
        CharacterApi.set_registry(injector.get(RegistryService))
        CharacterApi.lazy_load(injector.get(WeatherHandler))

        game_service = injector.get(GameService)
        player_service = injector.get(PlayerService)
        character_service = injector.get(CharacterService)
        shop_service = injector.get(ShopService)
        reset_service = injector.get(ResetService)
        special_service = injector.get(SpecialService)
        room_service = injector.get(RoomService)
        area_service = injector.get(AreaService)
        skill_service = injector.get(SkillService)
        spell_service = injector.get(SpellService)
        item_service = injector.get(ItemService)
        social_service = injector.get(SocialService)
        mobile_service = injector.get(MobileService)
        help_service = injector.get(HelpService)
        interp_service = injector.get(InterpService)
        note_service = injector.get(NoteService)

        injector.get(Fight).lazy_load()
        injector.get(SkillApi).lazy_load()

        update_handler = injector.get(UpdateHandler)
        fight_handler = injector.get(FightHandler)
        fight_handler.lazy_load()
        fight_handler.set_mobile_handler(injector.get(MobileHandler))

        injector.get(Wiz).lazy_load()
        injector.get(Movement).lazy_load()
        injector.get(Info).lazy_load()
        injector.get(Object).lazy_load()
        injector.get(Communications).lazy_load()
        enums = injector.get(GameService).enums
        area_handler = injector.get(AreaHandler)
        area_handler.set_enums(injector.get(GameService).enums)
        area_handler.initialize_world()
        update_handler.set_enums(enums)
        area_handler.set_enums(enums)

        injector.get(WeatherHandler).lazy_load()
        injector.get(GameService).set_update_handler(injector.get(UpdateHandler))

        services = (
            game_service, player_service, room_service, area_service, skill_service, spell_service, item_service,
            help_service, mobile_service, interp_service, social_service, note_service, character_service, shop_service,
            reset_service, special_service
        )
        service_list = "; ".join(s.__name__ for s in services)
        logger.info(f"The following services have been started: {service_list}.")
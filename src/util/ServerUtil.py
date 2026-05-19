from injector import singleton, Injector

from api.MovementApi import MovementApi
from area.ShopService import ShopService
from area.AreaHandler import AreaHandler
from area.ResetService import ResetService
from area.RoomHandler import RoomHandler
from area.SpecialService import SpecialService
from api.FightApi import FightApi
from game.HandlerService import HandlerService
from game.WizHandler import WizHandler
from interp.commands.Fight import Fight
from interp.commands.Communications import Communications
from api.InterpApi import InterpApi
from interp.commands.Info import Info
from interp.commands.Movement import Movement
from interp.commands.Object import Object
from interp.commands.Wiz import Wiz
from interp.HelpService import HelpService
from interp.InterpHandler import InterpHandler
from interp.SocialHandler import SocialHandler
from interp.SocialService import SocialService
from item.ItemHandler import ItemHandler
from item.BodyForm import BodyForm
from item.BodyParts import BodyParts
from mobile.MobileHandler import MobileHandler
from api.MobileApi import MobileApi
from player.PlayerHandler import PlayerHandler
from game.GameData import GameData
from game.GameService import GameService
from game.NoteHandler import NoteHandler
from game.NoteService import NoteService
from mobile.MobileService import MobileService
from api.ItemApi import ItemApi
from api.CharacterApi import CharacterApi
from player.PlayerService import PlayerService
from player.CharacterService import CharacterService
from server.LoggerFactory import LoggerFactory
from api.SkillApi import SkillApi
from skill.SkillService import SkillService
from skill.SpellService import SpellService
from game.RegistryService import RegistryService
from fight.FightHandler import FightHandler
from interp.InterpService import InterpService
from server.handlers.ConnectionHandler import ConnectionHandler
from area.AreaService import AreaService
from area.RoomService import RoomService
from item.ItemService import ItemService
from server.connection.ConnectionManager import ConnectionManager
from server.messaging.MessageBus import MessageBus
from server.session.AuthenticationService import AuthenticationService
from server.session.SessionHandler import SessionHandler
from server.ServiceConfig import ServiceConfig
from game.WeatherHandler import WeatherHandler
from game.UpdateHandler import UpdateHandler

logger = LoggerFactory.get_logger("ServerUtil")


class ServerUtil:
    @staticmethod
    def bind_dependencies(service_config) -> Injector:
        injector = Injector()
        injector.binder.bind(ServiceConfig, to=service_config, scope=singleton)

        ServerUtil._bind_network_services(injector)
        ServerUtil._bind_registries(injector)
        ServerUtil._bind_handlers(injector)
        ServerUtil._bind_api_instances(injector)
        ServerUtil._bind_game_data(injector)
        ServerUtil._bind_game_services(injector, service_config)

        enums = injector.get(GameService).enums

        injector.binder.bind(ConnectionHandler, scope=singleton)
        injector.binder.bind(SessionHandler, to=SessionHandler(enums.get("gameParameters")["MAX_IDLE"]), scope=singleton)

        return injector

    @staticmethod
    def _bind_singleton_classes(injector, classes):
        for clazz in classes:
            injector.binder.bind(clazz, scope=singleton)

    @staticmethod
    def _bind_network_services(injector):
        injector.binder.bind(MessageBus, scope=singleton)
        injector.binder.bind(ConnectionManager, scope=singleton)

    @staticmethod
    def _bind_game_services(injector, service_config):
        from item.ItemRegistry import ItemRegistry
        from skill.SkillRegistry import SkillRegistry
        ServerUtil._bind_singleton_classes(injector, [GameService, SkillService, SpellService, PlayerService,
                                                      CharacterService, HelpService, InterpService, AreaService,
                                                      RoomService, MobileService, AuthenticationService,
                                                      SocialService, NoteService, HandlerService])
        injector.binder.bind(ItemService, to=ItemService(service_config,
                                                         injector.get(ItemRegistry),
                                                         injector.get(SkillRegistry),
                                                         injector.get(GameService).game_data), scope=singleton)

    @staticmethod
    def _bind_handlers(injector):
        ServerUtil._bind_singleton_classes(injector,
                                           [SocialHandler, Communications, Fight, Info,
                                            Movement, Object, Wiz, AreaHandler,
                                            RoomHandler, FightHandler, ItemHandler, MobileHandler, PlayerHandler,
                                            WizHandler,
                                            InterpHandler, NoteHandler, WeatherHandler, UpdateHandler])
        logger.info(f"All game handlers have been bound.")

    @staticmethod
    def _bind_registries(injector):
        from game.NoteRegistry import NoteRegistry
        from fight.CombatRegistry import CombatRegistry
        from player.PlayerRegistry import PlayerRegistry
        from player.CharacterRegistry import CharacterRegistry
        from mobile.MobileRegistry import MobileRegistry
        from area.AreaRegistry import AreaRegistry
        from area.RoomRegistry import RoomRegistry
        from item.ItemRegistry import ItemRegistry
        from skill.SkillRegistry import SkillRegistry
        from skill.SpellRegistry import SpellRegistry
        from interp.InterpRegistry import InterpRegistry
        from interp.SocialRegistry import SocialRegistry
        from interp.HelpRegistry import HelpRegistry
        from area.ShopRegistry import ShopRegistry
        from area.SpecialRegistry import SpecialRegistry
        from area.ResetRegistry import ResetRegistry

        ServerUtil._bind_singleton_classes(injector, [NoteRegistry, PlayerRegistry, CharacterRegistry,
                                                      MobileRegistry, RoomRegistry, ItemRegistry, SkillRegistry,
                                                      SpellRegistry, HelpRegistry, InterpRegistry, SocialRegistry,
                                                      ShopRegistry, ResetRegistry, SpecialRegistry, RegistryService,
                                                      AreaRegistry, CombatRegistry, ])
        logger.info(
            f"The RegistryService has been bound with all injected dependencies: {injector.get(RegistryService)}")

    @staticmethod
    def _bind_game_data(injector):
        game_data = injector.get(GameService).game_data
        injector.binder.bind(GameData, to=game_data, scope=singleton)
        BodyForm.configure(game_data)
        BodyParts.configure(game_data)
        ItemApi.configure(game_data)
        MobileApi.configure(game_data)
        CharacterApi.configure(game_data)
        MovementApi.configure(game_data)

    @staticmethod
    def _bind_api_instances(injector):
        injector.binder.bind(SkillApi, scope=singleton)
        injector.binder.bind(FightApi, scope=singleton)
        injector.binder.bind(InterpApi, scope=singleton)

    @staticmethod
    def lazy_load(injector) -> None:
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
        area_handler = injector.get(AreaHandler)
        weather_handler = injector.get(WeatherHandler)
        update_handler = injector.get(UpdateHandler)
        item_handler = injector.get(ItemHandler)
        fight_handler = injector.get(FightHandler)
        mobile_handler = injector.get(MobileHandler)
        registry_service = injector.get(RegistryService)
        enums = injector.get(GameService).enums
        communications_commands = injector.get(Communications)
        object_commands = injector.get(Object)
        info_commands = injector.get(Info)
        movement_commands = injector.get(Movement)
        wiz_commands = injector.get(Wiz)
        skill_api = injector.get(SkillApi)
        fight_commands = injector.get(Fight)

        CharacterApi.set_registry(registry_service)
        CharacterApi.lazy_load(weather_handler)

        fight_commands.lazy_load()
        skill_api.lazy_load()
        fight_handler.lazy_load()
        fight_handler.set_mobile_handler(mobile_handler)
        wiz_commands.lazy_load()
        movement_commands.lazy_load()
        info_commands.lazy_load()
        object_commands.lazy_load()
        communications_commands.lazy_load()
        update_handler.set_enums(enums)
        area_handler.set_enums(enums)
        area_handler.initialize_world()
        weather_handler.lazy_load()
        game_service.set_update_handler(injector.get(UpdateHandler))

        services = (
            game_service, player_service, room_service, area_service, skill_service, spell_service, item_service,
            help_service, mobile_service, interp_service, social_service, note_service, character_service, shop_service,
            reset_service, special_service
        )
        service_list = "; ".join(s.__name__ for s in services)
        logger.info(f"The following services have been started: {service_list}.")

from injector import singleton, Injector

from area.RoomHelper import RoomHelper
from area.ShopService import ShopService
from area.AreaHandler import AreaHandler
from area.ResetService import ResetService
from area.RoomHandler import RoomHandler
from area.SpecialService import SpecialService
from game.HandlerService import HandlerService
from interp.CommandHelper import CommandHelper
from interp.commands.FightCommands import FightCommands
from interp.commands.CommunicationsCommands import CommunicationsCommands
from interp.commands.InfoCommands import InfoCommands
from interp.commands.MovementCommands import MovementCommands
from interp.commands.ObjectCommands import ObjectCommands
from interp.commands.WizCommands import WizCommands
from interp.HelpService import HelpService
from interp.InterpHandler import InterpHandler
from interp.SocialHandler import SocialHandler
from interp.SocialService import SocialService
from mobile.MobileHelper import MobileHelper
from object.ItemHandler import ItemHandler
from object.BodyForm import BodyForm
from object.BodyParts import BodyParts
from mobile.MobileHandler import MobileHandler
from player.PlayerHandler import PlayerHandler
from game.GameData import GameData
from game.GameService import GameService
from game.NoteHandler import NoteHandler
from game.NoteService import NoteService
from mobile.MobileService import MobileService
from object.ObjectMacros import ObjectMacros
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from player.PlayerService import PlayerService
from player.CharacterService import CharacterService
from server.LoggerFactory import LoggerFactory
from skill.SkillService import SkillService
from skill.SpellService import SpellService
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
from game.WeatherHandler import WeatherHandler
from game.UpdateHandler import UpdateHandler

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
        ServerUtil._bind_helpers(injector)
        ServerUtil._bind_handlers(injector)
        ServerUtil._bind_game_data(injector)
        ServerUtil._bind_game_services(injector, service_config)

        enums = injector.get(GameService).enums
        injector.binder.bind(ConnectionHandler, scope=singleton)
        injector.binder.bind(SessionHandler, to=SessionHandler(enums.get("gameParameters")["MAX_IDLE"]), scope=singleton)

        return injector

    @staticmethod
    def _bind_helpers(injector):
        injector.binder.bind(CommandHelper, scope=singleton)
        injector.binder.bind(RoomHelper, scope=singleton)
        injector.binder.bind(MobileHelper, scope=singleton)
        injector.binder.bind(PlayerHelper, scope=singleton)

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
        from object.ItemRegistry import ItemRegistry
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
                                           [SocialHandler, CommunicationsCommands, FightCommands, InfoCommands,
                                            MovementCommands, ObjectCommands, WizCommands, AreaHandler,
                                            RoomHandler, FightHandler, ItemHandler, MobileHandler, PlayerHandler,
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
        from object.ItemRegistry import ItemRegistry
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
        injector.binder.bind(GameData, to=injector.get(GameService).game_data, scope=singleton)
        BodyForm.configure(injector.get(GameData))
        BodyParts.configure(injector.get(GameData))
        ObjectMacros.configure(
            races_provider=lambda: injector.get(GameData).races,
            item_table_provider=lambda: injector.get(GameData).item_table,
            enums_provider=lambda: injector.get(GameService).enums,
        )

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
        attribute_bonuses = injector.get(GameData).attribute_bonuses
        pc_races = injector.get(GameData).pc_races
        enums = injector.get(GameService).enums
        communications_commands = injector.get(CommunicationsCommands)
        object_commands = injector.get(ObjectCommands)
        info_commands = injector.get(InfoCommands)
        movement_commands = injector.get(MovementCommands)
        wiz_commands = injector.get(WizCommands)
        command_helper = injector.get(CommandHelper)
        room_helper = injector.get(RoomHelper)

        CharacterMacros.configure(
            registry_provider=lambda: registry_service,
            enums_provider=lambda: enums,
            attribute_bonuses_provider=lambda: attribute_bonuses,
            pc_races_provider=lambda: pc_races,
            titles_provider=lambda: injector.get(GameData).titles,
            weather_handler_provider=lambda: weather_handler,
        )

        fight_handler.lazy_load()
        fight_handler.set_mobile_handler(mobile_handler)
        wiz_commands.lazy_load()
        movement_commands.lazy_load()
        info_commands.lazy_load()
        command_helper.lazy_load()
        object_commands.lazy_load()
        communications_commands.lazy_load()
        update_handler.set_enums(enums)
        area_handler.set_enums(enums)
        area_handler.initialize_world()
        weather_handler.lazy_load()
        room_helper.lazy_load(weather_handler)
        game_service.set_update_handler(injector.get(UpdateHandler))

        service_list = (
            f"{game_service.__name__}; {player_service.__name__}; {room_service.__name__}; {area_service.__name__}; "
            f"{skill_service.__name__}; {spell_service.__name__}; {item_service.__name__}\r\n{help_service.__name__}; {mobile_service.__name__}; "
            f"{interp_service.__name__}; {social_service.__name__}; {note_service.__name__}; {character_service.__name__} "
            f"{shop_service.__name__}; {reset_service.__name__}; {special_service.__name__}.")
        logger.info(f"The following services have been started: {service_list}")

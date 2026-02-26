import asyncio

from injector import Injector, singleton
from area import AreaService
from game.GameService import GameService
from mobile import MobileService
from object import ItemService
from player import PlayerService, Player
from command import CommandService, CommandHandler
from event import EventHandler
from registry import RegistryService
from server.ServerUtil import ServerUtil
from server.handlers import ConnectionHandler


class MudServer:
    def __init__(self, config: dict, logger_factory):
        self.connection_handler = None
        self.__name__ = "MudServer"
        self.config = config
        self.injector = Injector()
        self.player_one = None
        self.account_list = None
        self.character_list = None
        self.host = config['mudserver']['host']
        self.port = config['mudserver']['port']
        self.services = config['mudserver']['services']
        self.logger = logger_factory.get_logger(self.__name__)
        self.player_service_class = PlayerService
        self._configure_server()
        self.connection_handler = self.injector.get(ConnectionHandler)
        self.game_service = self.injector.get(GameService)

    async def start(self):
        asyncio.create_task(self.game_service.start())
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        self.logger.info(f"MudServer started on {self.host}:{self.port}")
        await server.serve_forever()

    async def handle_client(self, reader, writer):
        try:
            await self.connection_handler.handle_new_connection(reader, writer)
        except Exception as e:
            self.logger.error(f"Error in handle_client: {e}", exc_info=True)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    def _configure_server(self):
        self._start_services()
        self._configure_player_data()
        self.player_one = self._load_player_one()

    def _configure_player_data(self):
        player_service = self.injector.get(PlayerService)
        self.account_list = player_service.get_accounts()
        self.character_list = player_service.get_characters()

    def _start_services(self):
        self.injector.binder.bind(EventHandler, scope=singleton)
        self.injector.binder.bind(CommandService, to=CommandService(self.injector, self.services['commands']), scope=singleton)
        self.injector.binder.bind(CommandHandler, to=CommandHandler(self.injector), scope=singleton)
        self.injector.binder.bind(RegistryService, scope=singleton)
        self.injector.binder.bind(PlayerService, to=PlayerService(self.injector, self.services['players'], self.services['characters']), scope=singleton)
        self.injector.binder.bind(AreaService, to=AreaService(self.injector, self.services['areas'], self.services['rooms']), scope=singleton)
        self.injector.binder.bind(ItemService, to=ItemService(self.injector, self.services['items']), scope=singleton)
        self.injector.binder.bind(MobileService, to=MobileService(self.injector, self.services['mobiles']), scope=singleton)
        self.injector.binder.bind(ConnectionHandler, to=ConnectionHandler(self), scope=singleton)
        self.injector.binder.bind(GameService, to=GameService(self.injector, self.services['game_data']), scope=singleton)

    def _load_player_one(self):
        config = self.config
        from player import PlayerService
        player_service = self.injector.get(PlayerService)
        account_id = config['mudserver']['playerone']['accountId']
        account_json = ServerUtil.camel_to_snake_case(player_service.get_account_by_id(account_id))
        return Player.from_json(account_json)


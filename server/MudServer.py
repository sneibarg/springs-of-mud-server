import asyncio
from injector import Injector, singleton
from area.AreaService import AreaService
from mobile import MobileService
from object import ItemService
from player import PlayerService
from command import CommandService, CommandHandler
from event import EventHandler
from registry import RegistryService
from server.server_util import load_player_one


class MudServer:
    def __init__(self, config: dict, logger_factory):
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
        self.configure_server()

        # Initialize new architecture
        from server.handlers import ConnectionHandler
        self.connection_handler = ConnectionHandler(self)

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        self.logger.info(f"MudServer started on {self.host}:{self.port}")
        await server.serve_forever()

    async def handle_client(self, reader, writer):
        """
        Main connection handler - now uses new architecture.
        Falls back to legacy for compatibility during transition.
        """
        try:
            # Use new architecture
            await self.connection_handler.handle_new_connection(reader, writer)
        except Exception as e:
            self.logger.error(f"Error in handle_client: {e}", exc_info=True)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    def configure_server(self):
        self.start_services()
        self.configure_player_data()
        self.player_one = load_player_one(self)

    def configure_player_data(self):
        player_service = self.injector.get(PlayerService)
        self.account_list = player_service.get_accounts()
        self.character_list = player_service.get_characters()

    def start_services(self):
        self.injector.binder.bind(EventHandler, scope=singleton)
        self.injector.binder.bind(CommandService, to=CommandService(self.injector, self.services['commands']), scope=singleton)
        self.injector.binder.bind(CommandHandler, to=CommandHandler(self.injector), scope=singleton)
        self.injector.binder.bind(RegistryService, scope=singleton)
        self.injector.binder.bind(PlayerService, to=PlayerService(self.injector, self.services['players'], self.services['characters']), scope=singleton)
        self.injector.binder.bind(AreaService, to=AreaService(self.injector, self.services['areas'], self.services['rooms']), scope=singleton)
        self.injector.binder.bind(ItemService, to=ItemService(self.injector, self.services['items']), scope=singleton)
        self.injector.binder.bind(MobileService, to=MobileService(self.injector, self.services['mobiles']), scope=singleton)


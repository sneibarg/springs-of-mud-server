import asyncio
import threading

from player import Player
from server.ServiceConfig import ServiceConfig
from server.handlers import ConnectionHandler


class MudServer:
    def __init__(self, config: dict, logger_factory):
        self.__name__ = "MudServer"
        self.logger = logger_factory.get_logger(self.__name__)
        self.config = config
        self.injector = None
        self.player_one = None
        self.connection_handler = None
        self.host = config['mudserver']['host']
        self.port = config['mudserver']['port']
        self.modulith_host = config['mudserver']['modulith_host']
        self.modulith_port = config['mudserver']['modulith_port']
        self.service_endpoints = config['mudserver']['services']['endpoints']
        self.service_config: ServiceConfig = self._load_service_config()
        self._configure_server()

    async def start(self):
        game_thread = threading.Thread(target=self._run_game_loop, daemon=True, name="GameLoop")
        game_thread.start()
        self.logger.info("GameService started in background thread")
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        self.logger.info(f"MudServer started on {self.host}:{self.port}")
        await server.serve_forever()

    def _run_game_loop(self):
        from game.GameService import GameService
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.injector.get(GameService).start())
        except Exception as e:
            self.logger.error(f"Game loop error: {e}", exc_info=True)
        finally:
            loop.close()

    async def handle_client(self, reader, writer):
        try:
            await self.connection_handler.handle_new_connection(reader, writer)
        except asyncio.CancelledError:
            self.logger.info("Client connection cancelled")
            raise
        except (ConnectionResetError, BrokenPipeError) as e:
            self.logger.warning(f"Client connection lost: {e}")
        except OSError as e:
            self.logger.error(f"Network error handling client: {e}", exc_info=True)
        except Exception as e:
            self.logger.error(f"Unexpected error handling client: {e}", exc_info=True)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                self.logger.debug(f"Error closing connection: {e}")

    def _configure_server(self):
        self._start_services()
        self.player_one = self._load_player_one()

    def _start_services(self):
        from player.PlayerService import PlayerService
        from server.ServerUtil import ServerUtil

        self.injector = ServerUtil.bind_dependencies(self.service_config)
        self.player_service = self.injector.get(PlayerService)
        self.connection_handler = self.injector.get(ConnectionHandler)
        self.player_service.start()

        ServerUtil.load_services(self.injector)

    def _load_player_one(self):
        try:
            from server.ServerUtil import ServerUtil
            account_id = self.config['mudserver']['playerone']['accountId']
            account_json = ServerUtil.camel_to_snake_case(self.player_service.get_account_by_id(account_id))
            return Player.from_json(account_json)
        except KeyError as e:
            self.logger.error(f"Missing configuration key: {e}")
            self.logger.error(f"Available keys in config['mudserver']: {list(self.config.get('mudserver', {}).keys())}")
            raise RuntimeError(f"Configuration error: 'playerone' section not found in server.yml") from e

    def _construct_service_endpoint(self, endpoint):
        api_version = self.config['mudserver']['api_version']
        endpoint = self.config['mudserver']['services']['endpoints'][endpoint]
        return f"http://{self.modulith_host}:{self.modulith_port}{api_version}{endpoint}"

    def _load_service_config(self):
        return ServiceConfig(
            game_data_endpoint=self._construct_service_endpoint('game_data_endpoint'),
            commands_endpoint=self._construct_service_endpoint('commands_endpoint'),
            players_endpoint=self._construct_service_endpoint('players_endpoint'),
            characters_endpoint=self._construct_service_endpoint('characters_endpoint'),
            rooms_endpoint=self._construct_service_endpoint('rooms_endpoint'),
            areas_endpoint=self._construct_service_endpoint('areas_endpoint'),
            items_endpoint=self._construct_service_endpoint('items_endpoint'),
            mobiles_endpoint=self._construct_service_endpoint('mobiles_endpoint'),
            skills_endpoint=self._construct_service_endpoint('skills_endpoint')
        )

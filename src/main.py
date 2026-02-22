#!/usr/bin/python3
import asyncio
import os
import yaml

from server import MudServer, LoggerFactory

installation_directory = os.getcwd()
server_config_yaml = os.path.join(installation_directory, 'resources', 'server.yml')
logger_factory = LoggerFactory(os.path.join(installation_directory, 'log'))
logger = logger_factory.get_logger(__name__)
with open(server_config_yaml, 'r') as f:
    server_config = yaml.safe_load(f)


async def main():
    logger.info("Starting MudServer services.")
    mud_server = MudServer(server_config, logger_factory)
    logger.info("MudServer services started successfully.")
    logger.info("Starting main loop.")
    try:
        await mud_server.start()
        logger.info("Exiting...")
    except Exception as e:
        logger.info("An unhandled exception occurred: %s", e)


if __name__ == '__main__':
    asyncio.run(main())

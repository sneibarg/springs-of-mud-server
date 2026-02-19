import threading

from player import Character
from player import Player
from player.Player import Player


def print_room(area_service, writer, character):
    room = area_service.get_registry().room_registry[character.room_id]
    writer.write(f'[{room.name}]'.encode('utf-8'))
    area_service.print_description(writer, room)
    area_service.print_exits(writer, room)


def visible_players(player_service, interested_player) -> list:
    visible = []
    current_character = interested_player.current_character
    role = current_character.role
    for name in player_service.get_connected_players():
        if name == current_character.name:
            continue
        connected = player_service.get_connected_player(name)
        if connected.cloaked and role == "player":
            continue
        else:
            visible.append(connected)
    return visible


def is_playable_character(character_list, character_name):
    for character in character_list:
        if character_name.upper() in character['name'].upper():
            return character
    return None


def to_room(player_service, character, message, pattern):
    loiterers = player_service.get_in_room(character)
    cloaked_name = "Someone"
    cloaked = character.cloaked
    character_name = character.name
    if pattern is not None:
        pattern = pattern.replace('%p', cloaked_name if cloaked else character_name)
        pattern = pattern.replace('%m', message)
        message = pattern + "\r\n"
    else:
        message = message + "\r\n"
    for in_room in loiterers:
        in_room.get_writer().write(message.encode('utf-8'))


async def choose_character(mud_server, interested_player) -> Character:
    from player import PlayerService
    player_service = mud_server.injector.get(PlayerService)
    writer = interested_player.writer()
    reader = interested_player.reader()
    character_list = player_service.get_player_characters(interested_player.id)
    if character_list is None:
        writer.write(b"You don't have any characters! Would you like to create one? yes or no\r\n")
        message = await reader.readline()
        if message == "no":
            writer.write(b"Maybe next time...")
            writer.write_eof()
        return None
    else:
        writer.write(b"Select one of the following characters: \r\n\n\n")
        player_characters = {}
        for character in character_list:
            player_characters[character['name']] = character
            line = "- " + character['name'] + "\r\n"
            writer.write(line.encode('utf-8'))
        writer.write(b"\r\n")
        character_name = await reader.readline()
        from utilities.server_util import camel_to_snake_case
        character_definition = camel_to_snake_case(
            is_playable_character(character_list, character_name.decode('utf-8').strip()))
        character_definition['injector'] = mud_server.injector
        character_definition['writer'] = writer
        character_definition['reader'] = reader
        character_definition['lock'] = threading.Lock()
        from player.Character import Character
        character = Character.from_json(character_definition)
        if isinstance(character, Character):
            writer.write(b"Logging you onto the server as " + character_name)
            return character
        else:
            writer.write(b'That is not one of your characters.\r\n')
            return None


def bust_a_prompt(interested_player):
    character = interested_player.current_character
    prompt = "<"+str(character.health) + "hp " + str(character.mana) + "m " + str(character.movement) + "mv>\r\n"
    character.writer.write(prompt.encode('utf-8'))


async def prompt_ansi(reader, writer):
    from utilities.server_util import strip_telnet_commands
    try:
        writer.write("Do you want ANSI colors? (Y/N) ".encode('utf-8'))
        await writer.drain()
        response = await reader.read(1024)
        response = strip_telnet_commands(response)
        response = response.decode('utf-8').replace("\r\n", "")
        return response.strip().lower() == 'y'
    except UnicodeDecodeError as e:
        print(f"Decode error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


async def log_on_character(mud_server, reader, writer):
    from server import EventHandler
    event_handler = mud_server.injector.get(EventHandler)
    from utilities.server_util import server_hello
    interested_player, character = await server_hello(mud_server, reader, writer)
    interested_player.current_character = character
    event_handler.register_character(character)
    return interested_player, character


async def receive_data(mud_server, interested_player):
    from server.command import CommandHandler
    command_handler = mud_server.injector.get(CommandHandler)
    reader = interested_player.reader()
    writer = interested_player.writer()
    while True:
        if reader.at_eof() and writer.is_closing():
            writer.close()
            return
        message = await reader.readline()
        if not message or message is None:
            continue
        message = message.decode('utf-8')
        if message == "\r\n":
            bust_a_prompt(interested_player)
            continue
        command_handler.handle_command(interested_player, message.replace("\r\n", ""))
        bust_a_prompt(interested_player)
        await writer.drain()


async def log_in(mud_server, reader, writer):
    from player import PlayerService
    player_service = mud_server.injector.get(PlayerService)
    attempt_count = 0
    while attempt_count < 3:
        if attempt_count == 3:
            writer.write(
                b"You have exceeded the number of attempts to enter a valid account name. The connection will now "
                b"be terminated.\r\n")
            writer.write_eof()

        writer.write(b"You are not logged in.\r\n\n What is your account name?")
        account_name = await reader.readline()
        account_name = account_name.decode('utf-8')
        account_name = account_name.strip()
        from utilities.server_util import camel_to_snake_case
        account = camel_to_snake_case(player_service.get_account_by_name(account_name))

        if not account:
            writer.write(b"That account does not exist. What is your account name?\r\n")
            attempt_count += 1
            continue

        writer.write(b"What is your password?\r\n")
        account_password = await reader.readline()
        account_password = account_password.decode('utf-8')
        account_password = account_password.strip()

        if account_password == account['password']:
            writer.write(b"You have authenticated successfully.\r\n")
        else:
            writer.write(b"The password you supplied does not match our records.\r\n")
            attempt_count += 1
            continue

        account['connection'] = reader, writer
        account['current_character'] = None

        return Player.from_json(account)

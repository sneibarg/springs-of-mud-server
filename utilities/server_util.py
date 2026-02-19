import random
import re
from typing import Union, Optional, Any, Dict

from player import Character
from player.Player import Player
from utilities.player_util import prompt_ansi

alphanumerics = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
ascii_chars = ['#', '@', '$', '%', '&', '*', '+', '-', ':', '.', ' ']
color_codes = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}


def strip_telnet_commands(data):
    IAC = 255  # Interpret As Command
    DO = 253
    DONT = 254
    WILL = 251
    WONT = 252
    SB = 250  # Subnegotiation Begin
    SE = 240  # Subnegotiation End

    i = 0
    result = bytearray()
    length = len(data)
    while i < length:
        byte = data[i]
        if byte == IAC:
            i += 1
            if i < length:
                cmd = data[i]
                # Commands with options
                if cmd in (DO, DONT, WILL, WONT):
                    i += 1  # Skip the option byte
                elif cmd == SB:
                    # Skip until SE (Subnegotiation End)
                    i += 1
                    while i < length and not (data[i] == IAC and data[i+1] == SE):
                        i += 1
                    i += 2  # Skip SE
                else:
                    # Other commands without options
                    pass
        else:
            result.append(byte)
        i += 1
    return bytes(result)


def camel_to_snake_case(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    def camel_case_to_snake_case(string: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    snake_case_dict = {}
    for key, value in dictionary.items():
        snake_case_dict[camel_case_to_snake_case(key)] = value
    return snake_case_dict


def add_color(string):
    colored_string = ""
    for char in string:
        color_code = "\033[3" + str(random.randint(1, 6)) + "m"
        colored_char = color_code + char + "\033[0m"
        colored_string += colored_char
    return colored_string


def generate_diamond():
    characters = []
    characters.extend(ascii_chars)
    characters.extend(alphanumerics)
    width = 80
    height = width
    diamond = ''
    for i in range(-height // 2, height // 2 + 1):
        line = ''
        line += ' ' * abs(i)
        for j in range(-height // 2, height // 2 + 1):
            if abs(i) + abs(j) <= height // 2:
                char = random.choice(characters)
                color = random.randint(31, 36)
                line += f'\033[{color}m{char}'
            else:
                line += ' '
        line += ' ' * abs(i)
        if len(line.strip()) > 0:
            diamond += line + '\n'
    diamond += '\033[0m'
    return diamond


def generate_ascii_art():
    characters = []
    characters.extend(ascii_chars)
    characters.extend(alphanumerics)

    width = random.randint(100, 300)
    height = random.randint(20, 40)

    art = ''
    for _ in range(height):
        line = ''
        for _ in range(width):
            char = random.choice(characters)
            color = random.randint(31, 36)
            line += f'\033[{color}m{char}'
        art += line + '\n'
    art += '\033[0m'

    return art


def load_player_one(mud_server):
    config = mud_server.config
    from player import PlayerService
    player_service = mud_server.injector.get(PlayerService)
    account_id = config['mudserver']['playerone']['accountId']
    account_json = camel_to_snake_case(player_service.get_account_by_id(account_id))
    return Player.from_json(account_json)


def is_valid_direction(direction, room):
    if direction == "east":
        return room.exit_east
    if direction == "west":
        return room.exit_west
    if direction == "north":
        return room.exit_north
    if direction == "south":
        return room.exit_south
    if direction == "up":
        return room.exit_up
    if direction == "down":
        return room.exit_down


async def server_hello(server, reader, writer) -> Union[tuple[None, None], tuple[Any, Optional[Character]]]:
    from utilities.player_util import log_in, choose_character
    pick = 1
    pick_again = 3
    art = generate_diamond()
    welcome_message = 'Welcome to the server!\n\n\n\n' + art + '\n\n\n\n'
    try:
        writer.write(welcome_message.encode('utf-8'))
    except Exception as e:
        server.logger.info("An unhandled exception occurred: %s", e)
    ansi_enabled = await prompt_ansi(reader, writer)
    player = await log_in(server, reader, writer)
    player.ansi_enabled = ansi_enabled
    character = await choose_character(server, player)
    while character is None and pick <= pick_again:
        pick = pick + 1
        character = await choose_character(server, player)
        if character is None and pick == pick_again:
            writer.write(b'Logging you off until you can stop making typos.')
            writer.drain()
            writer.close()
            return None, None
    return player, character

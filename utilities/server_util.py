import re

from typing import Any, Dict
from player.Player import Player

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


def camel_to_snake_case(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    def camel_case_to_snake_case(string: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    snake_case_dict = {}
    for key, value in dictionary.items():
        snake_case_dict[camel_case_to_snake_case(key)] = value
    return snake_case_dict


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


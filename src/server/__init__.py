from typing import Dict, Any, Union
from .MudServer import MudServer
from .LoggerFactory import LoggerFactory
from .TimeVal import TimeVal

import json
import re


def find_json_object_by_name(name: str, commands: dict) -> Union[bool, Any]:
    if not commands:
        return False
    for command_name, command in commands.items():
        if name in command.get('shortcuts', []):
            return command
        if command.get('name') == name:
            return command
    return False


def get_json(text):
    try:
        json_data = json.loads(text)
    except TypeError:
        print("Error loading json data.")
        print("Response=" + str(text))
        json_data = None
    return json_data


def camel_to_snake_case(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    def camel_case_to_snake_case(string: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    snake_case_dict = {}
    for key, value in dictionary.items():
        snake_case_dict[camel_case_to_snake_case(key)] = value
    return snake_case_dict


__all__ = ['MudServer', 'LoggerFactory', 'TimeVal', 'find_json_object_by_name', 'get_json', 'camel_to_snake_case']

import json

from typing import Union, Any


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

import json
import ast

from typing import Mapping
from dataclasses import dataclass


@dataclass
class CharacterFlags:
    act: str
    comm: str
    affected_by: str

    @classmethod
    def from_json(cls, data):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            try:
                data = ast.literal_eval(data)
            except (SyntaxError, ValueError):
                data = json.loads(data.replace("'", '"'))

        if not isinstance(data, Mapping):
            raise TypeError(f"CharacterClass.from_json expected mapping or JSON string, got {type(data).__name__}")
        from server.ServerUtil import ServerUtil
        return cls(**ServerUtil.camel_to_snake_case(data))

import json

from dataclasses import dataclass, field
from typing import Any, Optional

from game.GamePayload import GamePayload
from game.action.GuardNormalization import normalize_guards
from interp.HelpEntry import HelpEntry


@dataclass
class Command:
    _id: str
    id: str
    name: str
    shortcuts: str
    role: str
    position: str
    enabled: bool
    lambdas: list[str]
    function: list[str]
    usage: str
    level: int
    max_arguments: int
    pipeline: bool = False
    message: Optional[str] = None
    skill_id: Optional[str] = None
    log: Optional[str] = field(default=None)
    help: Optional[HelpEntry] = field(default=None)
    payload: GamePayload = field(default_factory=GamePayload)
    guards: list[dict[str, Any]] = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Command):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from util.GenericUtil import GenericUtil
        data['id'] = GenericUtil.generate_mongo_id()
        data['_id'] = GenericUtil.generate_mongo_id()
        data = GenericUtil.camel_to_snake_case(data)
        data["payload"] = GamePayload.from_json(data.get("payload"))
        data["guards"] = normalize_guards(data.get("guards"))
        return cls(**data)

    def render_message(self, channel: str, key: str, fallback: str = "", **values) -> str:
        return self.payload.render(channel, key, fallback=fallback, **values)

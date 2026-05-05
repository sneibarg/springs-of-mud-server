from dataclasses import dataclass, field
from typing import Optional

from game.GamePayload import GamePayload
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

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Command):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from util.GenericUtil import GenericUtil
        data['id'] = GenericUtil.generate_mongo_id()
        data['_id'] = GenericUtil.generate_mongo_id()
        data = GenericUtil.camel_to_snake_case(data)
        return cls(**data)

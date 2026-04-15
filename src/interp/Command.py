from dataclasses import dataclass, field
from typing import Optional
from interp.HelpEntry import HelpEntry


@dataclass
class Command:
    _id: str
    id: str
    name: str
    shortcuts: str
    role: str
    message: str
    skill_id: str
    position: str
    enabled: bool
    lambdas: list[str]
    function: list[str]
    usage: str
    level: int
    max_arguments: int
    pipeline: bool = False
    log: Optional[str] = field(default=None)
    help: Optional[HelpEntry] = field(default=None)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Command):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data['id'] = ServerUtil.generate_mongo_id()
        data['_id'] = ServerUtil.generate_mongo_id()
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)

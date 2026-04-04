from dataclasses import dataclass


@dataclass
class HelpEntry:
    id: str
    keyword: str
    text: str
    level: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, HelpEntry):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data['id'] = ServerUtil.generate_mongo_id()
        data = ServerUtil.camel_to_snake_case(data)
        data['keyword'] = data['keyword'].lower()
        return cls(**data)

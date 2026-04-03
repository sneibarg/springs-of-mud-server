from dataclasses import dataclass


@dataclass
class Social:
    id: str
    name: str
    char_no_arg: str
    others_no_arg: str
    char_found: str
    others_found: str
    vict_found: str
    char_not_found: str
    char_auto: str
    others_auto: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Social):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)

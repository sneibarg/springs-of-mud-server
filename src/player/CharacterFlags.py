from dataclasses import dataclass


@dataclass
class CharacterFlags:
    act: str
    comm: str
    affected_by: str

    @classmethod
    def from_json(cls, data) -> CharacterFlags:
        from util.GenericUtil import GenericUtil
        return cls(**GenericUtil.camel_to_snake_case(data))

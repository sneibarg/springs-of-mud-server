import json

from enum import Enum
from dataclasses import dataclass


class AffectWhere(Enum):
    TO_AFFECTS = 0  # applies effect/spell to the character
    TO_OBJECT = 1  # modifies the item's base stats
    TO_IMMUNE = 2  # applies immunity to the character
    TO_RESIST = 3  # applies resistance to the character
    TO_VULN = 4  # applies vulnerability to the character
    TO_WEAPON = 5  # modifies the weapon's base stats


@dataclass
class Effect:
    valid: bool = False
    where: str | int = 0
    type: str | int = ""
    level: int = 0
    duration: int = 0
    location: str | int = 0
    modifier: int = 0
    bitvector: str | int = 0
    apply_to: str = ""
    source: str = ""

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from util.GenericUtil import GenericUtil
        payload = GenericUtil.camel_to_snake_case(data)
        return cls(**payload)

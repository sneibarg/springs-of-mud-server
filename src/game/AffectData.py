import json
from dataclasses import dataclass
from enum import Enum
from typing import Any


class AffectWhere(Enum):
    TO_AFFECTS = 0  # applies effect/spell to the character
    TO_OBJECT = 1  # modifies the object's base stats
    TO_IMMUNE = 2  # applies immunity to the character
    TO_RESIST = 3  # applies resistance to the character
    TO_VULN = 4  # applies vulnerability to the character
    TO_WEAPON = 5  # modifies the weapon's base stats


@dataclass
class AffectData:
    valid: bool
    where: Any
    type: Any
    level: Any
    duration: Any
    location: Any
    modifier: Any
    bitvector: Any
    apply_to: str = ""

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from game.GenericUtil import GenericUtil
        payload = GenericUtil.camel_to_snake_case(data)
        return cls(**payload)


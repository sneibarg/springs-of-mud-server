from dataclasses import dataclass
from enum import Enum


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
    where: int
    type: int
    level: int
    duration: int
    location: int
    modifier: int
    bitvector: int  # The bitvector flags determine which effect bits are set (like AFF_DETECT_INVIS, AFF_SANCTUARY, etc.)

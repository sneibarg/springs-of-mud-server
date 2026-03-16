from dataclasses import dataclass
from enum import Enum


class AffectWhere(Enum):
    TO_AFFECTS = 0
    TO_OBJECT = 1
    TO_IMMUNE = 2
    TO_RESIST = 3
    TO_VULN = 4
    TO_WEAPON = 5


@dataclass
class AffectData:
    valid: bool
    where: int
    type: int
    level: int
    duration: int
    location: int
    modifier: int
    bitvector: int

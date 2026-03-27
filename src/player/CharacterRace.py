from dataclasses import dataclass


@dataclass
class CharacterRace:
    name: str
    who_name: str
    skills: str
    points: int
    class_mult: int
    stats: int
    max_stats: int
    size: int

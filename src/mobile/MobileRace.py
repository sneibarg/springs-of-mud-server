from dataclasses import dataclass


@dataclass
class MobileRace:
    name: str
    pc_race: bool
    act: int
    aff: int
    off: int
    imm: int
    res: int
    vuln: int
    form: int
    parts: int

from dataclasses import dataclass


@dataclass
class MobileFlags:
    act: int
    affect: int
    off: int
    imm: int
    res: int
    vuln: int
    form: int
    parts: int

    @classmethod
    def default(cls) -> "MobileFlags":
        return cls(0, 0, 0, 0, 0, 0, 0, 0)

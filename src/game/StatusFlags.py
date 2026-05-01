from dataclasses import dataclass


@dataclass
class StatusFlags:
    act: int
    comm: int
    affected_by: int
    off: int
    imm: int
    res: int
    vuln: int
    form: int
    parts: int
    invis_level: int
    incog_level: int
    played: int
    logon: int
    pulse_wait: int
    pulse_daze: int

    @classmethod
    def default(cls) -> "StatusFlags":
        return cls(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    @classmethod
    def from_json(cls, data) -> "StatusFlags":
        from util.GenericUtil import GenericUtil
        return cls(**GenericUtil.camel_to_snake_case(data))

from dataclasses import dataclass


@dataclass
class TemporalMechanics:
    played: int
    logon: int
    pulse_wait: int
    pulse_daze: int

    @classmethod
    def from_json(cls, data) -> TemporalMechanics:
        from util.GenericUtil import GenericUtil
        return cls(**GenericUtil.camel_to_snake_case(data))

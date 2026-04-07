import json

from dataclasses import dataclass


@dataclass
class TemporalMechanics:
    played: int
    logon: int
    pulse_wait: int
    pulse_daze: int

    @classmethod
    def from_json(cls, data) -> TemporalMechanics:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise TypeError(f"TemporalMechanics.from_json expected mapping or JSON string, got {type(data).__name__}")
        from server.ServerUtil import ServerUtil
        return cls(**ServerUtil.camel_to_snake_case(data))

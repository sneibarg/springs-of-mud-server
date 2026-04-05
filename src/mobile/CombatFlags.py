from dataclasses import dataclass


@dataclass
class CombatFlags:
    off_flags: int
    imm_flags: int
    res_flags: int
    vuln_flags: int

    @classmethod
    def from_json(cls, data) -> CombatFlags:
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)



from dataclasses import dataclass
from enum import IntEnum
from game.GameMacros import GameMacros


@dataclass
class CombatFlags:
    off_flags: int
    imm_flags: int
    res_flags: int
    vuln_flags: int

    @classmethod
    def from_raw(cls, data, flag_letters: type[IntEnum]) -> "CombatFlags":
        if isinstance(data, str):
            data = data.replace("'", '"')
            import json
            try:
                parsed = json.loads(data)
            except json.JSONDecodeError:
                parsed = {}
        else:
            parsed = data or {}

        off_flags = parsed.get("off_flags", 0)
        imm_flags = parsed.get("imm_flags", 0)
        res_flags = parsed.get("res_flags", 0)
        vuln_flags = parsed.get("vuln_flags", 0)

        if isinstance(off_flags, str):
            off_flags = GameMacros.parse_flag_string(off_flags, flag_letters)
        if isinstance(imm_flags, str):
            imm_flags = GameMacros.parse_flag_string(imm_flags, flag_letters)
        if isinstance(res_flags, str):
            res_flags = GameMacros.parse_flag_string(res_flags, flag_letters)
        if isinstance(vuln_flags, str):
            vuln_flags = GameMacros.parse_flag_string(vuln_flags, flag_letters)

        return cls(
            off_flags=off_flags,
            imm_flags=imm_flags,
            res_flags=res_flags,
            vuln_flags=vuln_flags
        )

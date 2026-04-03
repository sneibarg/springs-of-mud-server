from dataclasses import dataclass


@dataclass
class CombatEvent:
    attacker: str
    defender: str
    room_id: str

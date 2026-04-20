from dataclasses import dataclass, field
import time


@dataclass
class CombatEvent:
    id: str
    attacker_id: str
    defender_id: str
    room_id: str
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    @property
    def event_id(self) -> str:
        return self.id

    @event_id.setter
    def event_id(self, value: str) -> None:
        self.id = value

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, CombatEvent):
            return self.id == other.id
        return False

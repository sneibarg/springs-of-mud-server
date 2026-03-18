from dataclasses import dataclass


@dataclass
class Skill:
    id: str
    name: str
    kind: str
    handler_id: str
    target: str
    min_position: str
    noun_damage: str
    msg_off: str
    msg_obj: str
    level_by_class: dict[str, int]
    level_by_rating: dict[str, int]
    slot: int
    min_mana: int
    beats: int

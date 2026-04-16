from dataclasses import dataclass
from typing import Optional
from object import Item


@dataclass
class Equipped:
    light: Optional[Item] = None
    finger1: Optional[Item] = None
    finger2: Optional[Item] = None
    neck1: Optional[Item] = None
    neck2: Optional[Item] = None
    torso: Optional[Item] = None
    head: Optional[Item] = None
    legs: Optional[Item] = None
    feet: Optional[Item] = None
    hands: Optional[Item] = None
    arms: Optional[Item] = None
    shield: Optional[Item] = None
    body: Optional[Item] = None
    waist: Optional[Item] = None
    wrist1: Optional[Item] = None
    wrist2: Optional[Item] = None
    wielded: Optional[Item] = None
    held: Optional[Item] = None
    floating_nearby: Optional[Item] = None

    def format_equipped(self) -> str:
        return "\n".join(f"{slot}: {item.name}" for slot, item in self.__dict__.items() if item)

import threading

from dataclasses import dataclass, field
from typing import List

from util.AreaUtil import AreaUtil
from area.Exit import Exit
from mobile.Mobile import Mobile
from object.Item import Item
from player.Character import Character
from object.ExtraDescriptionData import ExtraDescriptionData


@dataclass
class Room:
    id: str = ""
    area_id: str = ""
    vnum: str = ""
    name: str = ""
    description: str = ""
    pvp: bool = False
    spawn: bool = False
    spawn_timer: int = 0
    spawn_time: int = 0
    tele_delay: int = 0
    room_flags: int = 0
    sector_type: int = 0
    light: int = 0
    heal_rate: int = 0
    mana_rate: int = 0
    clan: int = 0
    extra_description: ExtraDescriptionData = None
    contents: dict[str, Item] = field(default_factory=dict)
    characters: dict[str, Character] = field(default_factory=dict)
    mobiles: dict[str, Mobile] = field(default_factory=dict)
    exits: List[Exit] = field(default_factory=list)

    def __post_init__(self):
        self.clan = None
        self.heal_rate = 100
        self.mana_rate = 100
        self.combat_events = []
        self.populace = {}
        self.lock = threading.Lock()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Room):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def get_formatted_exits(self):
        return AreaUtil.cardinal_direction(self)

    def add_player_to_room(self, character: Character):
        with self.lock:
            self.characters[character.id] = character

    def remove_player_from_room(self, character: Character):
        with self.lock:
            if character.id in self.characters:
                del self.characters[character.id]

    def add_mobile_to_room(self, mobile: Mobile):
        with self.lock:
            self.mobiles[mobile.id] = mobile

    def remove_mobile_from_room(self, mobile: Mobile):
        with self.lock:
            if mobile.id not in self.mobiles:
                del self.mobiles[mobile.id]

    def add_item_to_room(self, item: Item):
        with self.lock:
            self.contents[item.id] = item

    def remove_item_from_room(self, item: Item):
        with self.lock:
            if item.id in self.contents:
                del self.contents[item.id]

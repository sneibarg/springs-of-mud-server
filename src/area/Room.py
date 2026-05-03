import threading

from dataclasses import dataclass, field
from typing import List, Any

from util.AreaUtil import AreaUtil
from area.Exit import Exit
from mobile.Mobile import Mobile
from object.Item import Item
from player.Character import Character
from object.ExtraDescriptionData import ExtraDescriptionData
from util.GenericUtil import GenericUtil


@dataclass
class Room:
    DIRECTION_ALIASES = {
        "n": 0,
        "north": 0,
        "e": 1,
        "east": 1,
        "s": 2,
        "south": 2,
        "w": 3,
        "west": 3,
        "u": 4,
        "up": 4,
        "d": 5,
        "down": 5,
    }

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

    @classmethod
    def direction_index(cls, direction_name: str) -> int:
        return cls.DIRECTION_ALIASES.get((direction_name or "").strip().lower(), -1)

    def get_exit(self, direction: int):
        for ex in self.exits:
            if int(getattr(ex, "direction", -1)) == int(direction):
                return ex
        return None

    def destination_id_for_direction(self, direction_name: str):
        direction = self.direction_index(direction_name)
        if direction < 0:
            return None
        exit_obj = self.get_exit(direction)
        return None if exit_obj is None else getattr(exit_obj, "to_room_id", None)

    def find_door(self, arg: str) -> int:
        direction = self.direction_index(arg)
        if direction >= 0:
            return direction if self.get_exit(direction) is not None else -1

        wanted = (arg or "").strip().lower()
        if not wanted:
            return -1
        for ex in self.exits:
            keyword = (getattr(ex, "keyword", "") or "").lower()
            if wanted == keyword or wanted in keyword.split():
                return int(getattr(ex, "direction", -1))
        return -1

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
            if mobile.id in self.mobiles:
                del self.mobiles[mobile.id]

    def add_item_to_room(self, item: Item):
        with self.lock:
            self.contents[item.id] = item

    def remove_item_from_room(self, item: Item):
        with self.lock:
            if item.id in self.contents:
                del self.contents[item.id]

    def players_in_room(self) -> List[Character]:
        with self.lock:
            return list(self.characters.values())

    def mobiles_in_room(self) -> List[Mobile]:
        with self.lock:
            return list(self.mobiles.values())

    def people(self) -> List[Any]:
        with self.lock:
            chars = [self.characters.items()]
            mobs = [self.mobiles.items()]
            return chars + mobs

    def player_targets(self, character: Character) -> List[Character]:
        with self.lock:
            return [ch for ch in self.characters.values() if ch.id != character.id]

    def find_character_in_room(self, arg: str, name_matches_fn):
        q = (arg or "").strip().lower()
        for ch in self.characters.values():
            if name_matches_fn(q, getattr(ch, "name", "")):
                return ch
        return None

    def find_entity_in_room(self, entity_id: str):
        wanted = str(entity_id or "")
        if not wanted:
            return None
        if wanted in self.characters:
            return self.characters[wanted]
        if wanted in self.mobiles:
            return self.mobiles[wanted]
        return None

    def find_item_in_room(self, arg: str, name_matches_fn):
        q = (arg or "").strip().lower()
        for item in self.contents.values():
            if name_matches_fn(q, getattr(item, "name", "")):
                return item
        return None

    def find_visible_character(self, observer, wanted: str, room_helper):
        from player.CharacterMacros import CharacterMacros

        query = (wanted or "").strip().lower()
        if not query:
            return None

        for char in self.characters.values():
            if not CharacterMacros.can_see(observer, char, room_helper):
                continue
            if getattr(char, "room_id", None) != self.id:
                continue
            name = (getattr(char, "name", "") or "").strip().lower()
            if name == query or name.startswith(query):
                return char
        return None

    def find_visible_mobile(self, observer, wanted: str, room_helper):
        from player.CharacterMacros import CharacterMacros
        from util.InterpUtil import InterpUtil

        mob = InterpUtil.find_nth_by_keyword(self.mobiles, wanted)
        if mob is not None and CharacterMacros.can_see(observer, mob, room_helper):
            return mob
        return None

    def find_visible_target(self, observer, wanted: str, room_helper):
        query = (wanted or "").strip().lower()
        if not query:
            return None
        if query == "self":
            return observer

        target = self.find_visible_character(observer, query, room_helper)
        if target is not None:
            return target
        return self.find_visible_mobile(observer, query, room_helper)

    def is_room_private(self, room_flags) -> bool:
        private = GenericUtil.to_int(getattr(getattr(room_flags, "ROOM_PRIVATE", None), "value", 0), 0)
        solitary = GenericUtil.to_int(getattr(getattr(room_flags, "ROOM_SOLITARY", None), "value", 0), 0)
        flags = GenericUtil.to_int(getattr(self, "room_flags", 0), 0)
        if private and (flags & private) and len(getattr(self, "characters", {})) >= 2:
            return True
        if solitary and (flags & solitary) and len(getattr(self, "characters", {})) >= 1:
            return True
        return False

    def is_air_room(self, sector_types) -> bool:
        if sector_types is None:
            return False
        air = getattr(sector_types, "SECT_AIR", None)
        return air is not None and GenericUtil.to_int(getattr(self, "sector_type", 0), 0) == int(air.value)

    def requires_boat(self, sector_types) -> bool:
        if sector_types is None:
            return False
        no_swim = getattr(sector_types, "SECT_WATER_NOSWIM", None)
        return no_swim is not None and GenericUtil.to_int(getattr(self, "sector_type", 0), 0) == int(no_swim.value)

from __future__ import annotations

import threading

from dataclasses import dataclass, field
from typing import List, Any, TYPE_CHECKING

from api.CharacterApi import CharacterApi
from area.Exit import Exit
from mobile.Mobile import Mobile
from item.ExtraDescriptionData import ExtraDescriptionData
from util.GenericUtil import GenericUtil
from util.PlayerUtil import PlayerUtil


if TYPE_CHECKING:
    from area.Area import Area
    from item.Item import Item
    from player.Character import Character


@dataclass
class Room:
    DIRECTION_ALIASES = {
        alias: index for index, name in enumerate(Exit.DIRECTION_NAMES) for alias in (name, name[0])
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
    heal_rate: int = 100
    mana_rate: int = 100
    clan: int = 0
    owner: str = ""
    extra_description: ExtraDescriptionData = None
    contents: dict[str, Item] = field(default_factory=dict)
    characters: dict[str, Character] = field(default_factory=dict)
    mobiles: dict[str, Mobile] = field(default_factory=dict)
    exits: List[Exit] = field(default_factory=list)
    area: 'Area | None' = field(default=None, init=False, repr=False, compare=False)

    def __post_init__(self):
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
        if not self.exits:
            return "none"
        names = [Exit.direction_label(exit_obj.direction) for exit_obj in self.exits]
        return ", ".join(name for name in names if name) or "none"

    def adjust_light(self, amount: int) -> None:
        self.light = max(0, GenericUtil.to_int(getattr(self, "light", 0), 0) + amount)

    def item_locations(self):
        """Yield the room's top-level items and their immediate ownership locations."""
        for item in list(self.contents.values()):
            yield item, {"kind": "room", "parent": self, "container": None, "room": self}
        for kind, entities, inventory in (("char", self.characters, "loot"), ("mob", self.mobiles, "inventory")):
            for entity in list(entities.values()):
                for item in list(getattr(entity, inventory, []) or []):
                    yield item, {"kind": f"{kind}_{inventory}", "parent": entity, "container": None, "room": self}
                equipped = getattr(entity, "equipped", None)
                for item in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    if item is not None:
                        yield item, {"kind": f"{kind}_equipped", "parent": entity, "container": None, "room": self}

    def world_items(self):
        from item.Item import Item

        seen = set()
        for item, _ in Room.item_locations(self):
            if item is not None:
                yield from Item.walk_contents(item, seen)

    def locate_item(self, target):
        from item.Item import Item

        for item, location in Room.item_locations(self):
            if item is target:
                return location
            if item is not None:
                found = Item.locate_contained_item(item, target, self)
                if found is not None:
                    return found
        return None

    @classmethod
    def direction_index(cls, direction_name: str) -> int:
        return cls.DIRECTION_ALIASES.get((direction_name or "").strip().lower(), -1)

    def get_exit(self, direction: int):
        for ex in self.exits:
            if int(ex.direction) == int(direction):
                return ex
        return None

    def destination_id_for_direction(self, direction_name: str):
        direction = self.direction_index(direction_name)
        if direction < 0:
            return None
        exit_obj = self.get_exit(direction)
        return None if exit_obj is None else exit_obj.to_room_id

    def find_door(self, arg: str) -> int:
        direction = self.direction_index(arg)
        if direction >= 0:
            return direction if self.get_exit(direction) is not None else -1

        wanted = (arg or "").strip().lower()
        if not wanted:
            return -1
        for ex in self.exits:
            keyword = (ex.keyword or "").lower()
            if wanted == keyword or wanted in keyword.split():
                return int(ex.direction)
        return -1

    def add_player_to_room(self, character: Character):
        with self.lock:
            from game.Equipped import Equipped
            if character.id not in self.characters:
                self.adjust_light(Equipped.light_contribution(character))
            if character.id not in self.characters and self.area is not None:
                self.area.player_entered()
            self.characters[character.id] = character
            character._equipment_room = self

    def remove_player_from_room(self, character: Character):
        with self.lock:
            if character.id in self.characters:
                from game.Equipped import Equipped
                self.adjust_light(-Equipped.light_contribution(character))
                character._equipment_room = None
                character.on = None
                del self.characters[character.id]
                if self.area is not None:
                    self.area.player_left()

    def bind_area(self, area: 'Area | None') -> None:
        """Attach runtime ownership, including players already present when an area loads."""
        with self.lock:
            if self.area is area:
                return
            for _ in self.characters:
                if self.area is not None:
                    self.area.player_left()
                if area is not None:
                    area.player_entered()
            self.area = area

    def add_mobile_to_room(self, mobile: Mobile):
        with self.lock:
            from game.Equipped import Equipped
            if mobile.id not in self.mobiles:
                self.adjust_light(Equipped.light_contribution(mobile))
            self.mobiles[mobile.id] = mobile
            mobile._equipment_room = self

    def remove_mobile_from_room(self, mobile: Mobile):
        with self.lock:
            if mobile.id in self.mobiles:
                from game.Equipped import Equipped
                self.adjust_light(-Equipped.light_contribution(mobile))
                mobile._equipment_room = None
                mobile.on = None
                del self.mobiles[mobile.id]

    def add_item_to_room(self, item: Item):
        with self.lock:
            self.contents[item.id] = item

    def remove_item_from_room(self, item: Item):
        with self.lock:
            if item.id in self.contents:
                for person in list(self.characters.values()) + list(self.mobiles.values()):
                    if getattr(person, "on", None) is item:
                        person.on = None
                del self.contents[item.id]

    def players_in_room(self) -> List[Character]:
        with self.lock:
            return list(self.characters.values())

    def mobiles_in_room(self) -> List[Mobile]:
        with self.lock:
            return list(self.mobiles.values())

    def people(self) -> List[Any]:
        with self.lock:
            return list(self.characters.values()) + list(self.mobiles.values())

    def player_targets(self, character: Character) -> List[Character]:
        with self.lock:
            return [ch for ch in self.characters.values() if ch.id != character.id]

    def to_not_victim(self, victim: Character) -> List[Character]:
        with self.lock:
            return [ch for ch in self.characters.values() if victim.id != ch.id]

    def find_character_in_room(self, arg: str, name_matches_fn):
        q = (arg or "").strip().lower()
        for ch in self.characters.values():
            if name_matches_fn(q, ch.name):
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

    def find_room_item(self, wanted: str, *, observer=None):
        from util.LookupUtil import LookupUtil
        return LookupUtil.find(list(self.contents.values()), wanted,
                               visible=lambda item: LookupUtil.object_visible(observer, self, item))

    def find_visible_character(self, observer, wanted: str):
        from api.CharacterApi import CharacterApi
        from util.LookupUtil import LookupUtil
        return LookupUtil.find(list(self.characters.values()), wanted,
                               visible=lambda target: CharacterApi.can_see(observer, target, self))

    def find_visible_mobile(self, observer, wanted: str):
        from api.CharacterApi import CharacterApi
        from util.LookupUtil import LookupUtil
        return LookupUtil.find(list(self.mobiles.values()), wanted,
                               visible=lambda target: CharacterApi.can_see(observer, target, self))

    def find_visible_target(self, observer, wanted: str):
        from api.CharacterApi import CharacterApi
        from util.LookupUtil import LookupUtil
        return LookupUtil.character(self, observer, wanted,
                                    visible=lambda target: CharacterApi.can_see(observer, target, self))

    def is_private(self, room_flags) -> bool:
        if getattr(self, "owner", ""):
            return True
        private = room_flags.ROOM_PRIVATE.value
        solitary = room_flags.ROOM_SOLITARY.value
        flags = GenericUtil.to_int(self.room_flags, 0)
        count = len(self.characters) + len(self.mobiles)
        if private and (flags & private) and count >= 2:
            return True
        if solitary and (flags & solitary) and count >= 1:
            return True
        if flags & int(getattr(room_flags, "ROOM_IMP_ONLY", 0)):
            return True
        return False

    def is_air_room(self, sector_types) -> bool:
        if sector_types is None:
            return False
        return GenericUtil.to_int(self.sector_type, 0) == int(sector_types.SECT_AIR.value)

    def requires_boat(self, sector_types) -> bool:
        if sector_types is None:
            return False
        return GenericUtil.to_int(self.sector_type, 0) == int(sector_types.SECT_WATER_NOSWIM.value)

    def is_room_dark(self) -> bool:
        if self.light > 0:
            return False

        RoomFlags = CharacterApi.get_enum("roomFlags")
        SectorTypes = CharacterApi.get_enum("sectorTypes")
        if CharacterApi.is_set(self.room_flags, RoomFlags.ROOM_DARK.value):
            return True

        if self.sector_type == SectorTypes.SECT_INSIDE.value or self.sector_type == SectorTypes.SECT_CITY.value:
            return False

        weather = CharacterApi._weather()
        if weather is None:
            return False
        time_and_weather = CharacterApi.get_enum("timeAndWeather")
        return weather.weather_info.sunlight in (time_and_weather.SUN_SET, time_and_weather.SUN_DARK)

    def format_room_description(self) -> str:
        body = str(self.description or "").strip()
        return f"{self.name}\r\n\t\t{body}"

    def get_players_in_room(self, character: Character) -> str:
        text = ""
        for char_in_room in self.players_in_room():
            if char_in_room.id == character.id:
                continue
            if char_in_room.cloaked:
                continue
            if not CharacterApi.can_see(character, char_in_room, self):
                continue
            text += PlayerUtil.format_visible_character_line(character, char_in_room)
        return text

    def get_mobiles_in_room(self, character: Character) -> str:
        text = ""
        for char_in_room in self.mobiles_in_room():
            if not CharacterApi.can_see(character, char_in_room, self):
                continue
            text += PlayerUtil.format_visible_character_line(character, char_in_room)
        return text

    @staticmethod
    def can_see_room_vnum(char: Any) -> bool:
        if CharacterApi.is_immortal(char) and (CharacterApi.is_npc(char) or CharacterApi.has_holy_light(char)):
            return True
        return False

    @staticmethod
    def item_description_lines(room, observer) -> list:
        from api.ItemApi import ItemApi
        lines = []
        for item in room.contents.values():
            if not ItemApi.can_see_object(room, observer, item):
                continue
            raw_long = item.long_description or ""
            line = raw_long.rstrip("\r\n")
            if not raw_long.strip():
                line = item.short_description or item.name
            if line:
                line = f"    {line}"
                lines.append(line)
        return lines

    def randomize_exits(self, max_exits: int, rng):
        if max_exits <= 1:
            return

        slots = {i: None for i in range(len(Exit.DIRECTION_NAMES))}
        for exit_obj in self.exits:
            direction = int(getattr(exit_obj, "direction", -1))
            if 0 <= direction < len(Exit.DIRECTION_NAMES):
                slots[direction] = exit_obj

        upper = min(max_exits, len(Exit.DIRECTION_NAMES))
        for d0 in range(upper - 1):
            d1 = rng.number_range(d0, upper - 1)
            slots[d0], slots[d1] = slots[d1], slots[d0]

        rebuilt = []
        for direction in range(len(Exit.DIRECTION_NAMES)):
            exit_obj = slots[direction]
            if exit_obj is not None:
                exit_obj.direction = direction
                rebuilt.append(exit_obj)
        self.exits = rebuilt

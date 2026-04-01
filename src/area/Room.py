import threading

from dataclasses import dataclass, field
from area.AreaUtil import AreaUtil
from area.Exits import Exits


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
    extra_description: list = field(default_factory=list)
    mobiles: list = field(default_factory=list)
    exits: Exits = field(default_factory=Exits)

    def __post_init__(self):
        self.clan = None
        self.heal_rate = 100
        self.mana_rate = 100
        self.combat_events = []
        self.populace = {}
        self.lock = threading.Lock()

    @classmethod
    def from_json(cls, data):
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)

    def get_formatted_exits(self):
        return AreaUtil.cardinal_direction(self)

    def get_populace(self):
        with self.lock:
            return self.populace

    def add_to_populace(self, mobile):
        with self.lock:
            self.populace[mobile.get_instance_id()] = mobile

    def remove_from_populace(self, mobile):
        with self.lock:
            del self.populace[mobile.get_instance_id()]

    def get_combat_events(self):
        with self.lock:
            return self.combat_events

    def add_to_combat_events(self, combat_event):
        with self.lock:
            self.combat_events.append(combat_event)

    def remove_from_combat_events(self, combat_event):
        with self.lock:
            self.combat_events.remove(combat_event)

    def print_description(self, writer, room):
        if writer is None or room is None:
            room.logger.info("print_description: writer=" + str(writer) + ", room=" + self.name)
            return
        writer.write(str(room.description + "\r\n").encode('utf-8'))

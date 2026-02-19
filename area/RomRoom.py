from dataclasses import dataclass
import threading


@dataclass
class RomRoom:
    id: str
    area_id: str
    vnum: str
    name: str
    description: str
    exit_north: str
    exit_west: str
    exit_east: str
    exit_south: str
    exit_up: str
    exit_down: str
    pvp: bool
    spawn: bool
    spawn_timer: int
    spawn_time: int
    tele_delay: int
    room_flags: int
    sector_type: int
    mobiles: list
    alternate_routes: list
    extra_description: list

    def __post_init__(self):
        self.clan = None
        self.heal_rate = 100
        self.mana_rate = 100
        self.combat_events = []
        self.populace = {}
        self.lock = threading.Lock()

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def get_exits(self):
        return [room_exit for room_exit in
                [self.exit_north, self.exit_south, self.exit_east, self.exit_west, self.exit_up, self.exit_down, self.alternate_routes] if
                room_exit is not None]

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


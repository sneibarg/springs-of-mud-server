from typing import List
from injector import inject
from event.CombatEvent import CombatEvent
from server.LoggerFactory import LoggerFactory


class EventHandler:
    @inject
    def __init__(self):
        self.__name__ = "EventHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.combat_events: dict[str, CombatEvent] = dict()
        self.logger.info("Initialized EventHandler instance.")

    def get_combat_event_by_id(self, event_id: str) -> CombatEvent:
        return self.combat_events[event_id]

    def get_combat_event_by_room(self, room_id: str) -> List[CombatEvent]:
        events = []
        for event in self.combat_events.values():
            if event.room_id == room_id:
                events.append(event)
        return events


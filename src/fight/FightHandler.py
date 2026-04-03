from typing import List
from injector import inject
from fight.CombatEvent import CombatEvent
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus


class FightHandler:
    @inject
    def __init__(self, message_bus: MessageBus):
        self.__name__ = "FightHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.message_bus = message_bus
        self.combat_events: dict[str, CombatEvent] = dict()
        self.logger.info("Initialized FightHandler instance.")

    def get_combat_event_by_id(self, event_id: str) -> CombatEvent:
        try:
            return self.combat_events[event_id]
        except KeyError:
            return None

    def get_combat_event_by_room(self, room_id: str) -> List[CombatEvent]:
        events = []
        for event in self.combat_events.values():
            if event.room_id == room_id:
                events.append(event)
        return events


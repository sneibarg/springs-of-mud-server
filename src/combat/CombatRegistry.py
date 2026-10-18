from __future__ import annotations

import time

from registries import Registry

from combat.CombatEvent import CombatEvent
from util.GenericUtil import GenericUtil
from server.LoggerFactory import LoggerFactory


class CombatRegistry(Registry[CombatEvent]):
    lookup_attrs = ("id",)

    def __init__(self):
        super().__init__()
        self.__name__ = "CombatRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    @staticmethod
    def _key(attacker_id: str, defender_id: str, room_id: str) -> tuple[str, str, str]:
        return str(attacker_id), str(defender_id), str(room_id)

    def all_events(self) -> list[CombatEvent]:
        return list(self._items)

    def get_by_room(self, room_id: str) -> list[CombatEvent]:
        wanted = str(room_id)
        return [event for event in self._items if event.room_id == wanted]

    def get_by_combatant(self, combatant_id: str) -> list[CombatEvent]:
        wanted = str(combatant_id)
        return [
            event
            for event in self._items
            if event.attacker_id == wanted or event.defender_id == wanted
        ]

    def upsert(self, attacker_id: str, defender_id: str, room_id: str) -> CombatEvent:
        key = self._key(attacker_id, defender_id, room_id)
        now = time.time()

        for event in self._items:
            if self._key(event.attacker_id, event.defender_id, event.room_id) == key:
                event.updated_at = now
                return event

        event = CombatEvent(
            id=GenericUtil.generate_mongo_id(),
            attacker_id=key[0],
            defender_id=key[1],
            room_id=key[2],
            created_at=now,
            updated_at=now,
        )
        self.register(event)
        return event

    def remove_by_id(self, event_id: str) -> None:
        event = self.get_or_none(id=str(event_id))
        if event is not None:
            self.unregister(event)

    def remove_by_combatant(self, combatant_id: str) -> None:
        for event in list(self.get_by_combatant(combatant_id)):
            self.unregister(event)

    def retain_keys(self, active_keys: set[tuple[str, str, str]]) -> None:
        normalized = {
            self._key(attacker_id, defender_id, room_id)
            for attacker_id, defender_id, room_id in active_keys
        }
        for event in list(self._items):
            event_key = self._key(event.attacker_id, event.defender_id, event.room_id)
            if event_key not in normalized:
                self.unregister(event)

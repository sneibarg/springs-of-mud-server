import threading

from typing import Optional, List
from notes.InGameNote import InGameNote
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil


class NoteRegistry:
    lookup_attrs = ('id', 'name')

    def __init__(self):
        self.__name__ = "NoteRegistry"
        self.logger = LoggerFactory.get_logger(__name__)
        self.registry: dict[str, InGameNote] = {}
        self.lock = threading.Lock()

    def get_note_by_id(self, note_id: str) -> Optional[InGameNote]:
        try:
            return self.registry[note_id]
        except KeyError:
            return None

    def get_notes_by_type(self, note_type: str) -> List[InGameNote]:
        notes = []
        wanted = GenericUtil.to_int(note_type, -1)
        for note in self.registry.values():
            if GenericUtil.to_int(note.type, -2) == wanted:
                notes.append(note)
        return notes

    def all_notes(self) -> List[InGameNote]:
        return list(self.registry.values())

    def register_note(self, note: InGameNote):
        with self.lock:
            self.registry[note.id] = note

    def unregister_note(self, note_id: str):
        with self.lock:
            if note_id in self.registry:
                del self.registry[note_id]

    def clear(self):
        with self.lock:
            self.registry.clear()

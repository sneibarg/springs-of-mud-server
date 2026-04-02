import threading

from typing import Optional, List
from game.InGameNote import InGameNote
from server.LoggerFactory import LoggerFactory


class NoteRegistry:
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
        for note in self.registry.values():
            if note.type == note_type:
                notes.append(note)
        return notes

    def register_note(self, note: InGameNote):
        with self.lock:
            self.registry[note.id] = note

    def unregister_note(self, note_id: str):
        with self.lock:
            if note_id in self.registry:
                del self.registry[note_id]

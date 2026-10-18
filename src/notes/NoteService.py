import requests

from injector import inject
from notes.InGameNote import InGameNote
from notes.NoteRegistry import NoteRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class NoteService:
    @inject
    def __init__(self, config: ServiceConfig, note_registry: NoteRegistry):
        self.__name__ = "NoteService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.notes_endpoint = config.notes_endpoint
        self.note_registry = note_registry
        self.load_notes()

    def load_notes(self):
        try:
            response = requests.get(self.notes_endpoint, timeout=10)
            response.raise_for_status()
            notes = response.json()
            self.note_registry.clear()
            for note in notes:
                self.note_registry.register_note(InGameNote.from_json(note))
            return self.note_registry.all_notes()
        except Exception as e:
            self.logger.error("Failed to load note: " + str(e))
            return self.note_registry.all_notes()

    def get_notes_by_type(self, note_type: int):
        try:
            response = requests.get(f"{self._base_url()}/type/{int(note_type)}", timeout=10)
            response.raise_for_status()
            notes = [InGameNote.from_json(note) for note in response.json()]
            for note in notes:
                self.note_registry.register_note(note)
            return notes
        except Exception as e:
            self.logger.error("Failed to load notes by type: " + str(e))
            return self.note_registry.get_notes_by_type(note_type)

    def create_note(self, note: InGameNote):
        try:
            response = requests.post(self._base_url(), json=note.to_json(), timeout=10)
            response.raise_for_status()
            created = InGameNote.from_json(response.json())
            self.note_registry.register_note(created)
            return created
        except Exception as e:
            self.logger.error("Failed to create note: " + str(e))
            return None

    def update_note(self, note: InGameNote):
        try:
            response = requests.put(f"{self._base_url()}/{note.id}", json=note.to_json(), timeout=10)
            response.raise_for_status()
            updated = InGameNote.from_json(response.json())
            self.note_registry.register_note(updated)
            return updated
        except Exception as e:
            self.logger.error("Failed to update note: " + str(e))
            return None

    def delete_note(self, note_id: str) -> bool:
        try:
            response = requests.delete(f"{self._base_url()}/{note_id}", timeout=10)
            response.raise_for_status()
            self.note_registry.unregister_note(note_id)
            return True
        except Exception as e:
            self.logger.error("Failed to delete note: " + str(e))
            return False

    def _base_url(self) -> str:
        return str(self.notes_endpoint or "").rstrip("/")

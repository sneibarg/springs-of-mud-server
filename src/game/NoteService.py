import requests

from injector import inject
from game.InGameNote import InGameNote
from registry.NoteRegistry import NoteRegistry
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
            notes = requests.get(self.notes_endpoint).json()
            for note in notes:
                self.note_registry.register_note(InGameNote.from_json(note))
        except Exception as e:
            self.logger.error("Failed to load note: " + str(e))

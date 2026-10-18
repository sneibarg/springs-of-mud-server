import json
import os
import sys
import types
import unittest
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import patch


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
COMMANDS_PATH = os.path.join(ROOT, "resources", "collections", "SOMDB.Commands.json")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def _stub_package(name: str):
    module = types.ModuleType(name)
    module.__path__ = [os.path.join(SRC, name)]
    sys.modules[name] = module
    return module


class _Logger:
    def info(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None

    def debug(self, *_args, **_kwargs):
        return None


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


class _CharacterApi:
    @staticmethod
    def is_immortal(character) -> bool:
        return bool(getattr(character, "immortal", False))


_stub_module("injector", inject=lambda target: target)
_stub_package("api")
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_module("server.messaging", MessageBus=object)
_stub_module("api.CharacterApi", CharacterApi=_CharacterApi)


from interp.Command import Command
from notes.InGameNote import InGameNote, InGameNoteEnum
from notes.NoteHandler import NoteHandler
from notes.NoteRegistry import NoteRegistry
from notes.NoteService import NoteService


def _load_command(name: str) -> Command:
    with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
        commands = json.load(handle)
    for entry in commands:
        if entry.get("name") == name:
            payload = deepcopy(entry)
            payload.setdefault("shortcuts", "")
            payload.setdefault("function", [])
            payload.setdefault("usage", "")
            return Command.from_json(payload)
    raise KeyError(name)


class _FakeInterpApi:
    def render_message_key(self, context, message_key: str, channel: str = "", fallback: str = "", **tokens):
        target_channel = channel or "to_char"
        text = context.command.render_message(target_channel, message_key, fallback=fallback, **tokens)
        if text and not text.endswith("\r\n"):
            text += "\r\n"
        return {target_channel: text} if text else {}


class _Context(SimpleNamespace):
    def __init__(self, **kwargs):
        kwargs.setdefault("result", "")
        kwargs.setdefault("parameters", [])
        kwargs.setdefault("done", False)
        super().__init__(**kwargs)

    def finish(self):
        self.done = True


class _NoteService:
    def __init__(self, notes=None):
        self.notes = list(notes or [])
        self.created = []
        self.deleted = []

    def get_notes_by_type(self, note_type: int):
        return [note for note in self.notes if int(note.type) == int(note_type)]

    def create_note(self, note: InGameNote):
        note.id = f"created-{len(self.created) + 1}"
        self.created.append(note)
        self.notes.append(note)
        return note

    def delete_note(self, note_id: str) -> bool:
        self.deleted.append(note_id)
        self.notes = [note for note in self.notes if note.id != note_id]
        return True


class TestNoteCommands(unittest.TestCase):
    def _handler(self, notes=None):
        registry = NoteRegistry()
        service = _NoteService(notes)
        return NoteHandler(None, service, registry, _FakeInterpApi()), service

    def _context(self, command_name: str, result: str = ""):
        return _Context(command=_load_command(command_name), result=result, parameters=[])

    def test_note_model_accepts_modulith_note_view_shape(self):
        note = InGameNote.from_json({
            "id": "n1",
            "type": 0,
            "sender": "Ann",
            "date": "Mon Jan 01 00:00:00 2026",
            "toList": "all",
            "subject": "Hello",
            "text": "Body",
            "dateStamp": 123,
        })

        self.assertTrue(note.valid)
        self.assertEqual("all", note.to_list)
        self.assertEqual("all", note.to_json()["toList"])
        self.assertEqual(123, note.to_json()["dateStamp"])

    def test_registry_matches_note_type_as_int(self):
        registry = NoteRegistry()
        registry.register_note(InGameNote(id="n1", type=InGameNoteEnum.NOTE_NOTE.value))

        self.assertEqual(["n1"], [note.id for note in registry.get_notes_by_type("0")])

    @patch("notes.NoteService.requests.get")
    def test_service_loads_and_registers_notes(self, mock_get):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = [{"id": "n1", "type": 0, "sender": "Ann", "subject": "Hello"}]

        registry = NoteRegistry()
        service = NoteService(SimpleNamespace(notes_endpoint="http://notes"), registry)

        self.assertEqual("n1", service.note_registry.get_note_by_id("n1").id)
        mock_get.assert_called_once_with("http://notes", timeout=10)

    @patch("notes.NoteService.requests.post")
    @patch("notes.NoteService.requests.get")
    def test_service_creates_note_through_api(self, mock_get, mock_post):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = []
        mock_post.return_value.raise_for_status.return_value = None
        mock_post.return_value.json.return_value = {
            "id": "created",
            "type": 0,
            "sender": "Ann",
            "toList": "all",
            "subject": "Hello",
            "text": "Body",
            "dateStamp": 123,
        }

        registry = NoteRegistry()
        service = NoteService(SimpleNamespace(notes_endpoint="http://notes/"), registry)
        created = service.create_note(InGameNote(type=0, sender="Ann", to_list="all", subject="Hello", text="Body", date_stamp=123))

        self.assertEqual("created", created.id)
        self.assertEqual("all", mock_post.call_args.kwargs["json"]["toList"])
        mock_post.assert_called_once()

    def test_metadata_routes_note_commands_to_note_handler(self):
        for name in ("note", "idea", "news", "changes", "penalty"):
            self.assertEqual(
                ["lambda ctx: ctx.player_handler().do_note_command(ctx.character, ctx)"],
                _load_command(name).lambdas,
                name,
            )
        self.assertEqual([], _load_command("idea").guards)

    def test_lists_and_reads_visible_notes(self):
        note = InGameNote(id="n1", type=0, sender="Ann", to_list="all", subject="Hello", text="Body", date_stamp=10)
        handler, _service = self._handler([note])
        character = SimpleNamespace(name="Bob", context={}, immortal=False)

        payload = handler.execute(character, self._context("note", "list"))
        self.assertIn("[  1] Ann: Hello", payload["to_char"])

        payload = handler.execute(character, self._context("note", "read 1"))
        self.assertIn("To: all", payload["to_char"])
        self.assertEqual(10, character.context["note_read_stamps"]["0"])

    def test_draft_flow_posts_note_through_service(self):
        handler, service = self._handler()
        character = SimpleNamespace(name="Bob", context={}, immortal=False)

        for text in ("write", "to all", "subject Greetings", "+ First line", "+ Second line"):
            payload = handler.execute(character, self._context("note", text))
            self.assertIn("Ok.", payload["to_char"])

        payload = handler.execute(character, self._context("note", "post"))

        self.assertIn("Ok.", payload["to_char"])
        self.assertEqual(1, len(service.created))
        self.assertEqual("all", service.created[0].to_list)
        self.assertEqual("Greetings", service.created[0].subject)
        self.assertEqual("First line\r\nSecond line", service.created[0].text)
        self.assertNotIn("note_draft", character.context)

    def test_only_sender_or_immortal_can_delete_note(self):
        note = InGameNote(id="n1", type=0, sender="Ann", to_list="all", subject="Hello", text="Body", date_stamp=10)
        handler, service = self._handler([note])
        mortal = SimpleNamespace(name="Bob", context={}, immortal=False)
        immortal = SimpleNamespace(name="Admin", context={}, immortal=True)

        payload = handler.execute(mortal, self._context("note", "remove 1"))
        self.assertIn("You can't do that.", payload["to_char"])
        self.assertEqual([], service.deleted)

        payload = handler.execute(immortal, self._context("note", "remove 1"))
        self.assertIn("Ok.", payload["to_char"])
        self.assertEqual(["n1"], service.deleted)


if __name__ == "__main__":
    unittest.main()

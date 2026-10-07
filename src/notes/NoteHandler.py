from datetime import datetime
import time

from injector import inject

from api.InterpApi import InterpApi
from notes.InGameNote import InGameNote, InGameNoteEnum
from notes.NoteRegistry import NoteRegistry
from notes.NoteService import NoteService
from server.messaging import MessageBus
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil


class NoteHandler:
    @inject
    def __init__(self, message_bus: MessageBus,
                 note_service: NoteService,
                 note_registry: NoteRegistry,
                 interp_api: InterpApi):
        self.__name__ = "NoteHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.message_bus = message_bus
        self.note_service = note_service
        self.note_registry = note_registry
        self.interp_api = interp_api
        self.note_types = {
            "note": InGameNoteEnum.NOTE_NOTE.value,
            "idea": InGameNoteEnum.NOTE_IDEA.value,
            "penalty": InGameNoteEnum.NOTE_PENALTY.value,
            "news": InGameNoteEnum.NOTE_NEWS.value,
            "changes": InGameNoteEnum.NOTE_CHANGES.value,
        }
        self.note_labels = {
            InGameNoteEnum.NOTE_NOTE.value: ("note", "notes", "no_notes"),
            InGameNoteEnum.NOTE_IDEA.value: ("idea", "ideas", "no_ideas"),
            InGameNoteEnum.NOTE_PENALTY.value: ("penalty", "penalties", "no_penalties"),
            InGameNoteEnum.NOTE_NEWS.value: ("news", "news", "no_news"),
            InGameNoteEnum.NOTE_CHANGES.value: ("change", "changes", "no_changes"),
        }

    def execute(self, character, context):
        context.finish()
        command_name = str(getattr(getattr(context, "command", None), "name", "") or "note").strip().lower()
        note_type = self.note_types.get(command_name, InGameNoteEnum.NOTE_NOTE.value)
        argument = self._argument_text(context)
        action, rest = self._split_note_argument(argument)

        if not action:
            return self._read_next_unread(character, context, note_type)
        if action == "list":
            return self._list_notes(character, context, note_type, rest)
        if action == "read":
            return self._read_note(character, context, note_type, rest)
        if action.isdigit():
            return self._read_note(character, context, note_type, action)
        if action in ("remove", "delete"):
            return self._delete_note(character, context, note_type, rest, action)
        if action == "catchup":
            return self._catchup(character, context, note_type)
        if action == "write":
            return self._start_draft(character, context, note_type)
        if action == "to":
            return self._set_draft_field(character, context, note_type, "to_list", rest, "missing_recipient")
        if action == "subject":
            return self._set_draft_field(character, context, note_type, "subject", rest, "missing_subject")
        if action == "text":
            return self._set_draft_text(character, context, note_type, rest)
        if action == "+":
            return self._append_draft_line(character, context, note_type, rest)
        if action == "-":
            return self._remove_draft_line(character, context, note_type)
        if action == "clear":
            return self._clear_draft(character, context, note_type)
        if action == "show":
            return self._show_draft(character, context, note_type)
        if action in ("post", "send"):
            return self._post_draft(character, context, note_type)
        return self._message(context, "invalid_number", fallback="Read which number?\r\n")

    def _list_notes(self, character, context, note_type: int, rest: str):
        notes = self._visible_notes(character, note_type)
        if not notes:
            return self._message(context, self._no_notes_key(note_type), fallback="There are no notes for you.\r\n")
        if rest and not rest.isdigit():
            return self._message(context, "invalid_number", fallback="Read which number?\r\n")
        limit = GenericUtil.to_int(rest, len(notes)) if rest else len(notes)
        selected = notes[-limit:] if limit > 0 else []
        if not selected:
            return self._message(context, self._no_notes_key(note_type), fallback="There are no notes for you.\r\n")
        return {"to_char": self._format_note_list(selected, start_index=len(notes) - len(selected) + 1)}

    def _read_next_unread(self, character, context, note_type: int):
        notes = self._visible_notes(character, note_type)
        if not notes:
            return self._message(context, self._no_notes_key(note_type), fallback="There are no notes for you.\r\n")
        last_read = self._read_stamp(character, note_type)
        for index, note in enumerate(notes, start=1):
            stamp = GenericUtil.to_int(getattr(note, "date_stamp", 0), 0)
            if stamp > last_read:
                self._mark_read(character, note_type, stamp)
                return {"to_char": self._format_note(note, index)}
        return self._message(context, "have_no_unread", s=self._plural_name(note_type), fallback=f"You have no unread {self._plural_name(note_type)}.\r\n")

    def _read_note(self, character, context, note_type: int, rest: str):
        notes = self._visible_notes(character, note_type)
        if not notes:
            return self._message(context, self._no_notes_key(note_type), fallback="There are no notes for you.\r\n")
        if not rest:
            return self._read_next_unread(character, context, note_type)
        if not rest.isdigit():
            return self._message(context, "invalid_number", fallback="Read which number?\r\n")
        index = GenericUtil.to_int(rest, 0)
        note = self._note_at(notes, index)
        if note is None:
            return self._message(context, "aren_t_that_many", s=self._plural_name(note_type), fallback=f"There aren't that many {self._plural_name(note_type)}.\r\n")
        self._mark_read(character, note_type, GenericUtil.to_int(getattr(note, "date_stamp", 0), 0))
        return {"to_char": self._format_note(note, index)}

    def _delete_note(self, character, context, note_type: int, rest: str, action: str):
        notes = self._visible_notes(character, note_type)
        if not rest or not rest.isdigit():
            key = "note_remove_which_number" if action == "remove" else "note_delete_which_number"
            fallback = "Note remove which number?\r\n" if action == "remove" else "Note delete which number?\r\n"
            return self._message(context, key, fallback=fallback)
        note = self._note_at(notes, GenericUtil.to_int(rest, 0))
        if note is None:
            return self._message(context, "aren_t_that_many", s=self._plural_name(note_type), fallback=f"There aren't that many {self._plural_name(note_type)}.\r\n")
        if not self._can_delete(character, note):
            return self._message(context, "can_t_do_that", fallback="You can't do that.\r\n")
        if not self.note_service.delete_note(str(getattr(note, "id", "") or "")):
            return self._message(context, "can_t_do_that", fallback="You can't do that.\r\n")
        return self._message(context, "ok2", fallback="Ok.\r\n")

    def _catchup(self, character, context, note_type: int):
        notes = self._visible_notes(character, note_type)
        latest = max([GenericUtil.to_int(getattr(note, "date_stamp", 0), 0) for note in notes] or [int(time.time())])
        self._mark_read(character, note_type, latest)
        return self._message(context, "ok2", fallback="Ok.\r\n")

    def _start_draft(self, character, context, note_type: int):
        existing = self._draft(character)
        if existing is not None and GenericUtil.to_int(existing.get("type"), -1) != int(note_type):
            return self._message(context, "already_have_different_note", fallback="You already have a different note in progress.\r\n")
        if existing is not None:
            return self._message(context, "already_have_note", fallback="You already have a note in progress.\r\n")
        self._character_context(character)["note_draft"] = {
            "type": int(note_type),
            "to_list": "",
            "subject": "",
            "lines": [],
        }
        return self._message(context, "ok3", fallback="Ok.\r\n")

    def _set_draft_field(self, character, context, note_type: int, field_name: str, value: str, missing_key: str):
        draft = self._matching_draft(character, context, note_type)
        if isinstance(draft, dict) and draft.get("blocked"):
            return draft
        if not value.strip():
            return self._message(context, missing_key, fallback="You need to provide a value.\r\n")
        draft[field_name] = value.strip()
        return self._message(context, "ok4", fallback="Ok.\r\n")

    def _set_draft_text(self, character, context, note_type: int, text: str):
        draft = self._matching_draft(character, context, note_type)
        if isinstance(draft, dict) and draft.get("blocked"):
            return draft
        draft["lines"] = [text] if text else []
        return self._message(context, "ok5", fallback="Ok.\r\n")

    def _append_draft_line(self, character, context, note_type: int, line: str):
        draft = self._matching_draft(character, context, note_type)
        if isinstance(draft, dict) and draft.get("blocked"):
            return draft
        current = "\r\n".join(draft.get("lines", []))
        if len(current) + len(line) + 2 > 4096:
            return self._message(context, "too_long", fallback="Note too long.\r\n")
        draft.setdefault("lines", []).append(line)
        return self._message(context, "ok5", fallback="Ok.\r\n")

    def _remove_draft_line(self, character, context, note_type: int):
        draft = self._matching_draft(character, context, note_type)
        if isinstance(draft, dict) and draft.get("blocked"):
            return draft
        lines = draft.setdefault("lines", [])
        if not lines:
            return self._message(context, "nothing_to_remove", fallback="No lines left to remove.\r\n")
        lines.pop()
        return self._message(context, "ok6", fallback="Ok.\r\n")

    def _clear_draft(self, character, context, note_type: int):
        draft = self._matching_draft(character, context, note_type)
        if isinstance(draft, dict) and draft.get("blocked"):
            return draft
        self._character_context(character).pop("note_draft", None)
        return self._message(context, "ok2", fallback="Ok.\r\n")

    def _show_draft(self, character, context, note_type: int):
        draft = self._matching_draft(character, context, note_type)
        if isinstance(draft, dict) and draft.get("blocked"):
            return draft
        return {"to_char": self._format_draft(draft)}

    def _post_draft(self, character, context, note_type: int):
        draft = self._matching_draft(character, context, note_type)
        if isinstance(draft, dict) and draft.get("blocked"):
            return draft
        to_list = str(draft.get("to_list", "") or "").strip()
        subject = str(draft.get("subject", "") or "").strip()
        if not to_list:
            return self._message(context, "missing_recipient", fallback="You need to provide a recipient (name, all, or immortal).\r\n")
        if not subject:
            return self._message(context, "missing_subject", fallback="You need to provide a subject.\r\n")
        stamp = int(time.time())
        note = InGameNote(
            type=int(note_type),
            sender=str(getattr(character, "name", "") or ""),
            date=datetime.fromtimestamp(stamp).strftime("%a %b %d %H:%M:%S %Y"),
            to_list=to_list,
            subject=subject,
            text="\r\n".join(draft.get("lines", [])),
            date_stamp=stamp,
        )
        created = self.note_service.create_note(note)
        if created is None:
            return self._message(context, "can_t_do_that", fallback="You can't do that.\r\n")
        self._character_context(character).pop("note_draft", None)
        return self._message(context, "ok2", fallback="Ok.\r\n")

    def _matching_draft(self, character, context, note_type: int):
        draft = self._draft(character)
        if draft is None:
            return self._blocked_message(context, "no_draft", fallback="You have no note in progress.\r\n")
        if GenericUtil.to_int(draft.get("type"), -1) != int(note_type):
            return self._blocked_message(context, "aren_t_working_that", fallback="You aren't working on that kind of note.\r\n")
        return draft

    def _visible_notes(self, character, note_type: int):
        notes = list(self.note_service.get_notes_by_type(int(note_type)) or [])
        visible = [note for note in notes if self._can_read(character, note)]
        return sorted(visible, key=lambda note: GenericUtil.to_int(getattr(note, "date_stamp", 0), 0))

    def _can_read(self, character, note) -> bool:
        from api.CharacterApi import CharacterApi

        reader = str(getattr(character, "name", "") or "").strip().lower()
        sender = str(getattr(note, "sender", "") or "").strip().lower()
        recipients = self._recipient_tokens(getattr(note, "to_list", ""))
        if not recipients or "all" in recipients:
            return True
        if reader and (reader in recipients or sender == reader):
            return True
        if CharacterApi.is_immortal(character) and {"immortal", "immortals", "imm"} & recipients:
            return True
        return False

    def _can_delete(self, character, note) -> bool:
        from api.CharacterApi import CharacterApi

        actor = str(getattr(character, "name", "") or "").strip().lower()
        sender = str(getattr(note, "sender", "") or "").strip().lower()
        return CharacterApi.is_immortal(character) or (actor and actor == sender)

    @staticmethod
    def _recipient_tokens(to_list: str) -> set[str]:
        normalized = str(to_list or "").replace(",", " ").replace(";", " ")
        return {part.strip().lower() for part in normalized.split() if part.strip()}

    def _draft(self, character):
        context = self._character_context(character)
        draft = context.get("note_draft")
        return draft if isinstance(draft, dict) else None

    @staticmethod
    def _character_context(character):
        if not isinstance(getattr(character, "context", None), dict):
            character.context = {}
        return character.context

    @staticmethod
    def _note_at(notes: list, index: int):
        if index < 1 or index > len(notes):
            return None
        return notes[index - 1]

    @staticmethod
    def _format_note(note, index: int) -> str:
        return (
            f"[{index:3d}] {getattr(note, 'sender', '')}: {getattr(note, 'subject', '')}\r\n"
            f"To: {getattr(note, 'to_list', '')}\r\n"
            f"Date: {getattr(note, 'date', '')}\r\n\r\n"
            f"{getattr(note, 'text', '')}\r\n"
        )

    @staticmethod
    def _format_note_list(notes: list, start_index: int = 1) -> str:
        lines = []
        for offset, note in enumerate(notes):
            lines.append(f"[{start_index + offset:3d}] {getattr(note, 'sender', '')}: {getattr(note, 'subject', '')}")
        return "\r\n".join(lines) + "\r\n"

    @staticmethod
    def _format_draft(draft: dict) -> str:
        lines = draft.get("lines", [])
        body = "\r\n".join(lines)
        return (
            f"To: {draft.get('to_list', '')}\r\n"
            f"Subject: {draft.get('subject', '')}\r\n\r\n"
            f"{body}\r\n"
        )

    def _read_stamp(self, character, note_type: int) -> int:
        read_notes = self._character_context(character).setdefault("note_read_stamps", {})
        return GenericUtil.to_int(read_notes.get(str(int(note_type))), 0)

    def _mark_read(self, character, note_type: int, stamp: int):
        read_notes = self._character_context(character).setdefault("note_read_stamps", {})
        current = GenericUtil.to_int(read_notes.get(str(int(note_type))), 0)
        read_notes[str(int(note_type))] = max(current, GenericUtil.to_int(stamp, 0))

    def _no_notes_key(self, note_type: int) -> str:
        return self.note_labels.get(int(note_type), self.note_labels[InGameNoteEnum.NOTE_NOTE.value])[2]

    def _plural_name(self, note_type: int) -> str:
        return self.note_labels.get(int(note_type), self.note_labels[InGameNoteEnum.NOTE_NOTE.value])[1]

    @staticmethod
    def _argument_text(context) -> str:
        if isinstance(getattr(context, "result", None), str) and context.result.strip():
            return context.result.strip()
        return " ".join(getattr(context, "parameters", None) or []).strip()

    @staticmethod
    def _split_note_argument(argument: str) -> tuple[str, str]:
        text = str(argument or "").strip()
        if text.startswith("+"):
            return "+", text[1:].lstrip()
        if not text:
            return "", ""
        if text[0] in ("'", '"'):
            quote = text[0]
            end = text.find(quote, 1)
            if end < 0:
                return text[1:].strip().lower(), ""
            return text[1:end].strip().lower(), text[end + 1:].strip()
        parts = text.split(maxsplit=1)
        if len(parts) == 1:
            return parts[0].strip().lower(), ""
        return parts[0].strip().lower(), parts[1].strip()

    def _message(self, context, message_key: str, fallback: str = "", **tokens):
        rendered = self.interp_api.render_message_key(context, message_key, channel="to_char", fallback=fallback, **tokens)
        return rendered if rendered.get("to_char") else {"to_char": fallback}

    def _blocked_message(self, context, message_key: str, fallback: str = "", **tokens):
        rendered = self._message(context, message_key, fallback=fallback, **tokens)
        rendered["blocked"] = True
        return rendered

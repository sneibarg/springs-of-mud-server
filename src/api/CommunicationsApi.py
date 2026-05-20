from dataclasses import dataclass
from typing import Any, List

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from interp.Context import Context
from interp.InterpView import InterpView
from player.Character import Character
from util.CommunicationsUtil import CommunicationsUtil
from util.InterpUtil import InterpUtil


@dataclass(frozen=True)
class BufferedMessage:
    sender: str
    message: str


class CommunicationsApi(GameApi):
    _registry_service = None
    _tell_buffer: dict[str, List[BufferedMessage]] = {}
    _logger = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    @classmethod
    def reset_for_tests(cls) -> None:
        with cls._lock:
            cls._configured = False
            cls._game_data = None
            cls._enums = None
            cls._races = None
            cls._item_table = None
            cls._attribute_bonuses = None
            cls._classes = None
            cls._pc_races = None
            cls._titles = None
            cls._reset_internal_variables()

    @classmethod
    def _reset_internal_variables(cls) -> None:
        cls._registry_service = None
        cls._tell_buffer = {}
        cls._logger = None

    @classmethod
    def get_message_buffer(cls, recipient: str, sender: str):
        if not recipient:
            return []
        return [
            entry
            for entry in cls._tell_buffer.get(recipient, [])
            if entry.sender == sender
        ]

    @classmethod
    def append_tell_buffer(cls, character: Character, sender: Character, line: str):
        if character is None or not character.name:
            return

        recipient_name = character.name
        sender_name = sender.name if sender else "unknown"
        if recipient_name not in cls._tell_buffer:
            cls._tell_buffer[recipient_name] = []

        cls._tell_buffer[recipient_name].append(BufferedMessage(sender=sender_name, message=line))
        if len(cls._tell_buffer[recipient_name]) > 100:
            cls._tell_buffer[recipient_name] = cls._tell_buffer[recipient_name][-100:]

    @classmethod
    def get_tell_buffer(cls, character) -> list[BufferedMessage]:
        if character is None or character.name not in cls._tell_buffer:
            return []
        return cls._tell_buffer.pop(character.name)

    @classmethod
    def has_buffered_tells(cls, character) -> bool:
        return bool(character and character.name in cls._tell_buffer)

    @classmethod
    def tell_target_name(cls, view: InterpView) -> str:
        context = view.context
        override = str(getattr(context, "tell_target_name", "") or "").strip()
        if override:
            return override
        target, _message = CommunicationsUtil.split_first(InterpUtil.argument_text(view))
        return target

    @classmethod
    def tell_target(cls, view: InterpView):
        context = view.context
        override = getattr(context, "tell_target", None)
        if override is not None:
            return override

        player_handler = cls._player_handler(view)
        communications = getattr(player_handler, "communications_commands", None)
        session_handler = getattr(communications, "session_handler", None)
        if session_handler is None:
            return None
        return CharacterApi.find_playing_character(cls.tell_target_name(view), session_handler)

    @classmethod
    def tell_target_tokens(cls, view: InterpView) -> dict[str, Any]:
        return cls._target_tokens(cls.tell_target(view), fallback_name=cls.tell_target_name(view))

    @classmethod
    def tell_target_blocks_tells(cls, view: InterpView) -> bool:
        return cls._target_blocks_tells(cls.tell_target(view))

    @staticmethod
    def reply_target_id(view: InterpView):
        return (getattr(view.context.character, "context", {}) or {}).get("reply_to", "")

    @classmethod
    def reply_target(cls, view: InterpView):
        context = view.context
        override = getattr(context, "reply_target", None)
        if override is not None:
            return override

        target_id = cls.reply_target_id(view)
        if not target_id:
            return None

        player_handler = cls._player_handler(view)
        registry = getattr(player_handler, "character_registry", None)
        if registry is None:
            communications = getattr(player_handler, "communications_commands", None)
            registry = getattr(communications, "character_registry", None)
        if registry is None or not hasattr(registry, "get_or_none"):
            return None
        return registry.get_or_none(id=target_id)

    @classmethod
    def reply_target_tokens(cls, view: InterpView) -> dict[str, Any]:
        return cls._target_tokens(cls.reply_target(view))

    @classmethod
    def reply_target_blocks_tells(cls, view: InterpView) -> bool:
        return cls._target_blocks_tells(cls.reply_target(view))

    @staticmethod
    def _player_handler(view: InterpView):
        context: Context | Any = getattr(view, "context", None)
        if context is None or not hasattr(context, "player_handler"):
            return None
        return context.player_handler()

    @classmethod
    def _target_blocks_tells(cls, target) -> bool:
        if target is None:
            return False
        comm_flags = cls.get_enum("commFlags")
        return any(
            CommunicationsUtil.has_comm(target, comm_flags, flag)
            for flag in ("COMM_DEAF", "COMM_QUIET", "COMM_NOTELL")
        )

    @staticmethod
    def _target_tokens(target, fallback_name: str = "") -> dict[str, Any]:
        name = str(getattr(target, "name", "") or fallback_name or "")
        if not name:
            return {}
        return {"t": name, "v": name}

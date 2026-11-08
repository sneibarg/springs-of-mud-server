from dataclasses import dataclass
from typing import Any, List

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from interp.InterpView import InterpView
from player.Character import Character
from util.CommunicationsUtil import CommunicationsUtil
from util.InterpUtil import InterpUtil
from util.WizUtil import WizUtil


@dataclass(frozen=True)
class BufferedMessage:
    sender: str
    message: str
    rendered_text: str | None = None

    def format_message(self):
        if self.rendered_text is not None:
            return CommunicationsUtil.ensure_message_break(self.rendered_text)
        return CommunicationsUtil.ensure_message_break(f"{self.sender} tells you '{self.message}'")


class CommunicationsApi(GameApi):
    _tell_buffer: dict[str, List[BufferedMessage]] = {}
    _logger = None

    @classmethod
    def reset_for_tests(cls) -> None:
        with cls._lock:
            cls._configured = False
            cls._reset_internal_variables()

    @classmethod
    def _reset_internal_variables(cls) -> None:
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
    def append_tell_buffer(cls, character: Character, sender: Character, line: str, *, rendered_text: str | None = None):
        if character is None or not character.name:
            return

        recipient_name = character.name
        sender_name = sender.name if sender else "unknown"
        if recipient_name not in cls._tell_buffer:
            cls._tell_buffer[recipient_name] = []

        cls._tell_buffer[recipient_name].append(BufferedMessage(sender=sender_name, message=line, rendered_text=rendered_text))
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
        if hasattr(context, "tell_target"):
            return context.tell_target

        player_handler = view.context.player_handler()
        session_handler = player_handler.communications_commands.session_handler
        return cls.find_tell_target(view.context.character, cls.tell_target_name(view),
                                    session_handler, view.context.registry_service.room_registry)

    @staticmethod
    def find_tell_target(actor, name, session_handler, room_registry):
        target = CharacterApi.find_playing_character(name, session_handler)
        if target is not None and not getattr(target, 'world_retired', False):
            return target
        return WizUtil.find_world_entity(None, room_registry, name, include_mobiles=False, observer=actor)

    @staticmethod
    def recipient_disconnected(target, session_handler) -> bool:
        return (target is not None and not CharacterApi.is_npc(target)
                and not any((session.character.id if session.character is not None else None) == target.id
                            for session in session_handler.get_playing_sessions()))

    @classmethod
    def tell_target_tokens(cls, view: InterpView) -> dict[str, Any]:
        return cls._target_tokens(cls.tell_target(view), fallback_name=cls.tell_target_name(view))

    @classmethod
    def tell_target_blocks_tells(cls, view: InterpView) -> bool:
        return (not getattr(view.context, 'tell_disconnected', False)
                and not CharacterApi.is_immortal(view.context.character)
                and cls._target_blocks_tells(cls.tell_target(view)))

    @classmethod
    def tell_target_asleep(cls, view: InterpView) -> bool:
        if getattr(view.context, 'tell_disconnected', False):
            return False
        target, actor = cls.tell_target(view), view.context.character
        override = (CharacterApi.is_immortal(actor)
                    and actor.level > int(CharacterApi.get_enum('gameParameters').LEVEL_IMMORTAL))
        return target is not None and not override and not CharacterApi.is_awake(target)

    @classmethod
    def follow_target(cls, view: InterpView):
        override = getattr(view.context, "follow_target", None)
        if override is not None:
            return override

        room = cls.current_room(view)
        if room is None:
            return None

        wanted = InterpUtil.argument_text(view)
        finder = getattr(room, "find_visible_target", None)
        if callable(finder):
            return finder(view.context.character, wanted)

        q = str(wanted or "").strip().lower()
        for candidate in list((room.characters or {}).values()) + list((room.mobiles or {}).values()):
            name = str(candidate.name or "").strip().lower()
            short = str(getattr(candidate, "short_description", "") or "").strip().lower()
            if q and (name == q or name.startswith(q) or short == q or short.startswith(q)):
                return candidate
        return None

    @classmethod
    def follow_target_tokens(cls, view: InterpView) -> dict[str, Any]:
        target = cls.follow_target(view)
        leader = cls.follow_leader(view.context.character)
        tokens = cls._target_tokens(target)
        if leader is not None:
            tokens["M"] = leader.name
        return tokens

    @staticmethod
    def follow_leader(character):
        return (character.master if character is not None else None)

    @classmethod
    def follow_charmed_with_master(cls, view: InterpView) -> bool:
        affected = CharacterApi.get_enum("affectedBy")
        charm_bit = CharacterApi.enum_bit(affected, "AFF_CHARM")
        status_flags = view.context.character.status_flags
        return bool(
            charm_bit
            and CharacterApi.is_set(status_flags.affected_by if status_flags is not None else 0, charm_bit)
            and cls.follow_leader(view.context.character) is not None
        )

    @classmethod
    def follow_self_without_master(cls, view: InterpView) -> bool:
        return cls.follow_target(view) == view.context.character and cls.follow_leader(view.context.character) is None

    @classmethod
    def follow_target_blocks_followers(cls, view: InterpView) -> bool:
        target = cls.follow_target(view)
        if target is None or CharacterApi.is_npc(target) or CharacterApi.is_immortal(view.context.character):
            return False
        player_bits = CharacterApi.get_enum("playerActBits")
        nofollow_bit = CharacterApi.enum_bit(player_bits, "PLR_NOFOLLOW")
        status_flags = target.status_flags
        return bool(nofollow_bit and CharacterApi.is_set(status_flags.act if status_flags is not None else 0, nofollow_bit))

    @classmethod
    def order_args(cls, view: InterpView) -> tuple[str, str, str]:
        target, command_text = CommunicationsUtil.split_first(InterpUtil.argument_text(view))
        command, _rest = CommunicationsUtil.split_first(command_text)
        return target, command_text, command

    @classmethod
    def order_delete(cls, view: InterpView) -> bool:
        _target, _command_text, command = cls.order_args(view)
        return command == "delete"

    @classmethod
    def order_missing_argument(cls, view: InterpView) -> bool:
        target, command_text, _command = cls.order_args(view)
        return not target or not command_text

    @classmethod
    def order_actor_charmed(cls, view: InterpView) -> bool:
        return cls.is_charmed(view.context.character)

    @classmethod
    def order_target(cls, view: InterpView):
        target, _command_text, _command = cls.order_args(view)
        if target == "all":
            return None
        return cls.room_target(view, target)

    @classmethod
    def order_target_missing(cls, view: InterpView) -> bool:
        target, _command_text, _command = cls.order_args(view)
        return bool(target and target != "all" and cls.order_target(view) is None)

    @classmethod
    def order_target_self(cls, view: InterpView) -> bool:
        return cls.order_target(view) == view.context.character

    @classmethod
    def order_target_not_submissive(cls, view: InterpView) -> bool:
        victim = cls.order_target(view)
        if victim is None:
            return False
        actor = view.context.character
        return (
            not cls.is_charmed(victim)
            or cls.master_of(victim) != actor
            or (CharacterApi.is_immortal(victim) and CharacterApi.get_trust(victim) >= CharacterApi.get_trust(actor))
        )

    @classmethod
    def order_targets(cls, view: InterpView) -> list[Any]:
        target, _command_text, _command = cls.order_args(view)
        victim = cls.order_target(view)
        f_all = target == "all"
        actor = view.context.character
        targets = []
        for candidate in cls.room_people(view):
            if cls.is_charmed(candidate) and cls.master_of(candidate) == actor and (f_all or candidate == victim):
                targets.append(candidate)
        return targets

    @classmethod
    def order_tokens(cls, view: InterpView) -> dict[str, Any]:
        target, command_text, _command = cls.order_args(view)
        tokens = {"s": command_text, "t": target}
        victim = cls.order_target(view)
        if victim is not None:
            tokens.update(cls._target_tokens(victim))
        return tokens

    @classmethod
    def group_target(cls, view: InterpView):
        return cls.room_target(view, InterpUtil.argument_text(view))

    @classmethod
    def group_target_missing(cls, view: InterpView) -> bool:
        return bool(InterpUtil.argument_text(view) and cls.group_target(view) is None)

    @classmethod
    def group_actor_follows_another(cls, view: InterpView) -> bool:
        actor = view.context.character
        return cls.master_of(actor) is not None or (actor.leader is not None and actor.leader != actor)

    @classmethod
    def group_target_not_follower(cls, view: InterpView) -> bool:
        victim = cls.group_target(view)
        actor = view.context.character
        return victim is not None and victim != actor and cls.master_of(victim) != actor

    @classmethod
    def group_target_charmed(cls, view: InterpView) -> bool:
        victim = cls.group_target(view)
        return victim is not None and cls.is_charmed(victim)

    @classmethod
    def group_actor_charmed(cls, view: InterpView) -> bool:
        return cls.is_charmed(view.context.character)

    @classmethod
    def group_target_tokens(cls, view: InterpView) -> dict[str, Any]:
        target = cls.group_target(view)
        tokens = cls._target_tokens(target, fallback_name=InterpUtil.argument_text(view))
        actor = view.context.character
        tokens["m"] = actor.name
        tokens["m_pronoun"] = cls.object_pronoun(actor)
        tokens["s_poss"] = cls.possessive_pronoun(actor)
        return tokens

    @classmethod
    def group_members(cls, view: InterpView) -> list[Any]:
        actor = view.context.character
        return [candidate for candidate in cls.all_known_people(view) if CharacterApi.is_same_group(candidate, actor)]

    @classmethod
    def room_target(cls, view: InterpView, target_name: str):
        room = cls.current_room(view)
        if room is None:
            return None
        finder = getattr(room, "find_visible_target", None)
        if callable(finder):
            return finder(view.context.character, target_name)
        q = str(target_name or "").strip().lower()
        if q == "self":
            return view.context.character
        for candidate in cls.room_people(view):
            name = str(candidate.name or "").strip().lower()
            short = str(getattr(candidate, "short_description", "") or "").strip().lower()
            if q and (name == q or name.startswith(q) or short == q or short.startswith(q)):
                return candidate
        return None

    @classmethod
    def current_room(cls, view: InterpView):
        context = view.context
        room = context.room
        if room is not None:
            return room
        return context.registry_service.room_registry.get_or_none(id=context.character.room_id)

    @classmethod
    def room_people(cls, view: InterpView) -> list[Any]:
        room = cls.current_room(view)
        if room is None:
            return []
        people = getattr(room, "people", None)
        if callable(people):
            return list(people())
        return list((room.characters or {}).values()) + list((room.mobiles or {}).values())

    @classmethod
    def all_known_people(cls, view: InterpView) -> list[Any]:
        people: dict[str, Any] = {}
        for room in view.context.registry_service.room_registry.all_rooms():
            for candidate in list((room.characters or {}).values()) + list((room.mobiles or {}).values()):
                people[str(candidate.id)] = candidate
        return list(people.values())

    @classmethod
    def is_charmed(cls, character) -> bool:
        affected = CharacterApi.get_enum("affectedBy")
        charm_bit = CharacterApi.enum_bit(affected, "AFF_CHARM")
        status_flags = character.status_flags if character is not None else None
        return bool(charm_bit and CharacterApi.is_set(status_flags.affected_by if status_flags is not None else 0, charm_bit))

    @staticmethod
    def master_of(character):
        return (character.master if character is not None else None)

    @staticmethod
    def object_pronoun(character) -> str:
        sex = str((character.sex if character is not None else "") or "").strip().lower()
        if sex in ("1", "male", "m"):
            return "him"
        if sex in ("2", "female", "f"):
            return "her"
        return "it"

    @staticmethod
    def possessive_pronoun(character) -> str:
        sex = str((character.sex if character is not None else "") or "").strip().lower()
        if sex in ("1", "male", "m"):
            return "his"
        if sex in ("2", "female", "f"):
            return "her"
        return "its"

    @staticmethod
    def reply_target_id(view: InterpView):
        return (view.context.character.context or {}).get("reply_to", "")

    @classmethod
    def reply_target(cls, view: InterpView):
        context = view.context
        if hasattr(context, "reply_target"):
            return context.reply_target

        target_id = cls.reply_target_id(view)
        if not target_id:
            return None

        registries = context.registry_service
        return cls.find_reply_target(target_id, registries.character_registry, registries.room_registry)

    @staticmethod
    def find_reply_target(target_id, character_registry, room_registry):
        if not target_id:
            return None
        target = character_registry.get_or_none(id=target_id)
        if target is not None:
            return target
        return next((entity for entity in WizUtil.live_world_entities(room_registry)
                     if entity.id == target_id), None)

    @classmethod
    def reply_target_tokens(cls, view: InterpView) -> dict[str, Any]:
        return cls._target_tokens(cls.reply_target(view))

    @classmethod
    def reply_target_blocks_tells(cls, view: InterpView) -> bool:
        target = cls.reply_target(view)
        return (not getattr(view.context, 'tell_disconnected', False)
                and not CharacterApi.is_immortal(view.context.character)
                and not CharacterApi.is_immortal(target) and cls._target_blocks_tells(target))

    @classmethod
    def reply_target_asleep(cls, view: InterpView) -> bool:
        target = cls.reply_target(view)
        return (target is not None and not getattr(view.context, 'tell_disconnected', False)
                and not CharacterApi.is_immortal(view.context.character)
                and not CharacterApi.is_awake(target))

    @classmethod
    def _target_blocks_tells(cls, target) -> bool:
        if target is None:
            return False
        comm_flags = cls.get_enum("commFlags")
        return any(
            CommunicationsUtil.has_comm(target, comm_flags, flag)
            for flag in ("COMM_DEAF", "COMM_QUIET")
        )

    @staticmethod
    def _target_tokens(target, fallback_name: str = "") -> dict[str, Any]:
        name = str(("" if target is None else target.name) or fallback_name or "")
        if not name:
            return {}
        return {"t": name, "v": name}

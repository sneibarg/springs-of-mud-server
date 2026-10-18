from dataclasses import dataclass
from typing import Any, List

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from interp.Context import Context
from interp.InterpView import InterpView
from player.Character import Character
from util.CommunicationsUtil import CommunicationsUtil
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil


@dataclass(frozen=True)
class BufferedMessage:
    sender: str
    message: str

    def format_message(self):
        return CommunicationsUtil.ensure_message_break(f"{self.sender} tells you '{self.message}'")


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
        if player_handler is None:
            return None
        session_handler = player_handler.communications_commands.session_handler
        return CharacterApi.find_playing_character(cls.tell_target_name(view), session_handler)

    @classmethod
    def tell_target_tokens(cls, view: InterpView) -> dict[str, Any]:
        return cls._target_tokens(cls.tell_target(view), fallback_name=cls.tell_target_name(view))

    @classmethod
    def tell_target_blocks_tells(cls, view: InterpView) -> bool:
        return cls._target_blocks_tells(cls.tell_target(view))

    @classmethod
    def follow_target(cls, view: InterpView):
        override = getattr(view.context, "follow_target", None)
        if override is not None:
            return override

        player_handler = cls._player_handler(view)
        if player_handler is None:
            return None
        room = getattr(view.context, "room", None)
        if room is None:
            room_registry = getattr(player_handler, "room_registry", None)
            room = None if room_registry is None else room_registry.get_or_none(id=getattr(view.context.character, "room_id", ""))
        if room is None:
            return None

        wanted = InterpUtil.argument_text(view)
        finder = getattr(room, "find_visible_target", None)
        if callable(finder):
            return finder(view.context.character, wanted)

        q = str(wanted or "").strip().lower()
        for candidate in list(getattr(room, "characters", {}) or {}).values() + list(getattr(room, "mobiles", {}) or {}).values():
            name = str(getattr(candidate, "name", "") or "").strip().lower()
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
            tokens["M"] = getattr(leader, "name", "")
        return tokens

    @staticmethod
    def follow_leader(character):
        return getattr(character, "master", None)

    @classmethod
    def follow_charmed_with_master(cls, view: InterpView) -> bool:
        affected = CharacterApi.get_enum("affectedBy")
        charm_bit = CharacterApi.enum_bit(affected, "AFF_CHARM")
        return bool(
            charm_bit
            and CharacterApi.is_set(getattr(view.context.character.status_flags, "affected_by", 0), charm_bit)
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
        return bool(nofollow_bit and CharacterApi.is_set(getattr(target.status_flags, "act", 0), nofollow_bit))

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
        return cls.master_of(actor) is not None or (getattr(actor, "leader", None) is not None and getattr(actor, "leader", None) != actor)

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
        tokens["m"] = getattr(actor, "name", "")
        tokens["m_pronoun"] = cls.object_pronoun(actor)
        tokens["s_poss"] = cls.possessive_pronoun(actor)
        return tokens

    @classmethod
    def group_members(cls, view: InterpView) -> list[Any]:
        actor = view.context.character
        return [candidate for candidate in cls.all_known_people(view) if CharacterApi.is_same_group(candidate, actor)]

    @classmethod
    def split_amounts(cls, view: InterpView) -> dict[str, int]:
        silver_text, rest = CommunicationsUtil.split_first(InterpUtil.argument_text(view))
        gold_text, _extra = CommunicationsUtil.split_first(rest)
        return {
            "silver": GenericUtil.to_int(silver_text, 0),
            "gold": GenericUtil.to_int(gold_text, 0) if gold_text else 0,
        }

    @classmethod
    def split_missing_amount(cls, view: InterpView) -> bool:
        first, _rest = CommunicationsUtil.split_first(InterpUtil.argument_text(view))
        return not first

    @classmethod
    def split_negative(cls, view: InterpView) -> bool:
        amounts = cls.split_amounts(view)
        return amounts["silver"] < 0 or amounts["gold"] < 0

    @classmethod
    def split_zero(cls, view: InterpView) -> bool:
        amounts = cls.split_amounts(view)
        return amounts["silver"] == 0 and amounts["gold"] == 0

    @classmethod
    def split_insufficient_funds(cls, view: InterpView) -> bool:
        amounts = cls.split_amounts(view)
        actor = view.context.character
        return GenericUtil.to_int(getattr(actor, "silver", 0), 0) < amounts["silver"] or GenericUtil.to_int(getattr(actor, "gold", 0), 0) < amounts["gold"]

    @classmethod
    def split_members(cls, view: InterpView) -> list[Any]:
        actor = view.context.character
        return [
            candidate
            for candidate in cls.room_people(view)
            if CharacterApi.is_same_group(candidate, actor) and not cls.is_charmed(candidate)
        ]

    @classmethod
    def split_too_few_members(cls, view: InterpView) -> bool:
        return len(cls.split_members(view)) < 2

    @classmethod
    def split_shares(cls, view: InterpView) -> dict[str, int]:
        amounts = cls.split_amounts(view)
        members = max(1, len(cls.split_members(view)))
        return {
            "silver": amounts["silver"] // members,
            "gold": amounts["gold"] // members,
            "extra_silver": amounts["silver"] % members,
            "extra_gold": amounts["gold"] % members,
        }

    @classmethod
    def split_share_zero(cls, view: InterpView) -> bool:
        shares = cls.split_shares(view)
        return shares["silver"] == 0 and shares["gold"] == 0

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
            name = str(getattr(candidate, "name", "") or "").strip().lower()
            short = str(getattr(candidate, "short_description", "") or "").strip().lower()
            if q and (name == q or name.startswith(q) or short == q or short.startswith(q)):
                return candidate
        return None

    @classmethod
    def current_room(cls, view: InterpView):
        room = getattr(view.context, "room", None)
        if room is not None:
            return room
        player_handler = cls._player_handler(view)
        room_registry = None if player_handler is None else getattr(player_handler, "room_registry", None)
        return None if room_registry is None else room_registry.get_or_none(id=getattr(view.context.character, "room_id", ""))

    @classmethod
    def room_people(cls, view: InterpView) -> list[Any]:
        room = cls.current_room(view)
        if room is None:
            return []
        people = getattr(room, "people", None)
        if callable(people):
            return list(people())
        return list(getattr(room, "characters", {}) or {}).values() + list(getattr(room, "mobiles", {}) or {}).values()

    @classmethod
    def all_known_people(cls, view: InterpView) -> list[Any]:
        player_handler = cls._player_handler(view)
        room_registry = None if player_handler is None else getattr(player_handler, "room_registry", None)
        all_rooms = getattr(room_registry, "all_rooms", None)
        if not callable(all_rooms):
            return cls.room_people(view)
        people: dict[str, Any] = {}
        for room in all_rooms():
            for candidate in list((getattr(room, "characters", {}) or {}).values()) + list((getattr(room, "mobiles", {}) or {}).values()):
                people[str(getattr(candidate, "id", id(candidate)))] = candidate
        return list(people.values())

    @classmethod
    def is_charmed(cls, character) -> bool:
        affected = CharacterApi.get_enum("affectedBy")
        charm_bit = CharacterApi.enum_bit(affected, "AFF_CHARM")
        return bool(charm_bit and CharacterApi.is_set(getattr(getattr(character, "status_flags", None), "affected_by", 0), charm_bit))

    @staticmethod
    def master_of(character):
        return getattr(character, "master", None)

    @staticmethod
    def object_pronoun(character) -> str:
        sex = str(getattr(character, "sex", "") or "").strip().lower()
        if sex in ("1", "male", "m"):
            return "him"
        if sex in ("2", "female", "f"):
            return "her"
        return "it"

    @staticmethod
    def possessive_pronoun(character) -> str:
        sex = str(getattr(character, "sex", "") or "").strip().lower()
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
        override = getattr(context, "reply_target", None)
        if override is not None:
            return override

        target_id = cls.reply_target_id(view)
        if not target_id:
            return None

        player_handler = cls._player_handler(view)
        if player_handler is None:
            return None
        registry = player_handler.character_registry
        return registry.get_or_none(id=target_id)

    @classmethod
    def reply_target_tokens(cls, view: InterpView) -> dict[str, Any]:
        return cls._target_tokens(cls.reply_target(view))

    @classmethod
    def reply_target_blocks_tells(cls, view: InterpView) -> bool:
        return cls._target_blocks_tells(cls.reply_target(view))

    @staticmethod
    def _player_handler(view: InterpView):
        return view.context.player_handler()

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
        name = str(("" if target is None else target.name) or fallback_name or "")
        if not name:
            return {}
        return {"t": name, "v": name}

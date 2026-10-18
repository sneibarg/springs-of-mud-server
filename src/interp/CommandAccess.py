from dataclasses import dataclass

from api.CharacterApi import CharacterApi
from util.CommunicationsUtil import CommunicationsUtil
from util.GenericUtil import GenericUtil


@dataclass(frozen=True)
class CommandDenial:
    message_key: str
    fallback: str = "Huh?\r\n"

    def render(self, command) -> str:
        render = getattr(command, "render_message", None)
        text = render("to_char", self.message_key, fallback=self.fallback) if callable(render) else self.fallback
        return CommunicationsUtil.ensure_message_break(text or self.fallback)


class CommandAccess:
    """Enforce command metadata at every interpreter execution boundary."""

    POSITION_MESSAGE_KEYS = {
        "POS_DEAD": "dead",
        "POS_MORTAL": "hurt",
        "POS_INCAP": "hurt",
        "POS_STUNNED": "stunned",
        "POS_SLEEPING": "sleeping",
        "POS_RESTING": "resting",
        "POS_SITTING": "sitting",
        "POS_FIGHTING": "fighting",
    }

    @staticmethod
    def _enum_number(enum, name: str):
        member = getattr(enum, name, None)
        return GenericUtil.to_int(getattr(member, "value", member), None)

    @classmethod
    def _required_level(cls, raw, game_parameters):
        if isinstance(raw, bool):
            return None
        if isinstance(raw, int):
            return raw if raw >= 0 else None
        if not isinstance(raw, str):
            return None
        name = raw.strip().upper()
        if name.isdecimal():
            return int(name)
        name = {"ML": "MAX_LEVEL", "IM": "LEVEL_IMMORTAL"}.get(name, name)
        if len(name) == 2 and name[0] == "L" and name[1] in "12345678":
            maximum = cls._enum_number(game_parameters, "MAX_LEVEL")
            return maximum - int(name[1]) if maximum is not None else None
        return cls._enum_number(game_parameters, name) if name else None

    @staticmethod
    def _principal(actor):
        # A switched body retains its controller's authority, but its own position.
        seen = set()
        while actor is not None:
            if id(actor) in seen:
                return None
            seen.add(id(actor))
            controller = (getattr(actor, "context", None) or {}).get("controller_original")
            if controller is None:
                return actor
            actor = controller
        return None

    @classmethod
    def check(cls, actor, command) -> CommandDenial | None:
        if actor is None or getattr(command, "enabled", False) is not True:
            return CommandDenial("command_unavailable")
        try:
            game_parameters = CharacterApi.get_enum("gameParameters")
            positions = CharacterApi.get_enum("positions")
        except (RuntimeError, KeyError):
            return CommandDenial("command_unavailable")

        required_level = cls._required_level(getattr(command, "level", None), game_parameters)
        position_name = str(getattr(command, "position", "") or "").strip().upper()
        if position_name and not position_name.startswith("POS_"):
            position_name = f"POS_{position_name}"
        required_position = cls._enum_number(positions, position_name)
        principal = cls._principal(actor)
        if required_level is None or required_position is None or principal is None:
            return CommandDenial("command_unavailable")

        role = str(getattr(command, "role", "") or "").strip().lower()
        actor_role = str(getattr(principal, "role", "") or "").strip().lower()
        trust = CharacterApi.get_trust(principal)
        if trust < required_level:
            return CommandDenial("command_not_allowed")
        if role == "immortal":
            immortal_level = cls._enum_number(game_parameters, "LEVEL_IMMORTAL")
            if immortal_level is None or (actor_role not in {"immortal", "admin"} and trust < immortal_level):
                return CommandDenial("command_not_allowed")
        elif role != "player":
            return CommandDenial("command_not_allowed")

        current_position = CharacterApi.position_value(actor)
        if current_position < required_position:
            key = next((key for name, key in cls.POSITION_MESSAGE_KEYS.items()
                        if cls._enum_number(positions, name) == current_position), "command_unavailable")
            return CommandDenial(f"command_position_{key}" if key != "command_unavailable" else key)
        return None

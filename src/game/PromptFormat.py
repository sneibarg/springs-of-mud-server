import inspect

from dataclasses import dataclass, asdict
from typing import Callable, Union, TYPE_CHECKING
from area import Room, Area
from player import Character
from server.protocol import Message, MessageType

if TYPE_CHECKING:
    from server.session import SessionStatus


def build_prompt_map():
    return {
        "%h": lambda c: c.health,
        "%H": lambda c: c.max_health,
        "%m": lambda c: c.mana,
        "%M": lambda c: c.max_mana,
        "%v": lambda c: c.movement,
        "%V": lambda c: c.max_movement,
        "%x": lambda c: c.experience,
        "%X": lambda c: c.accumulated_experience,
        "%g": lambda c: c.gold,
        "%s": lambda c: c.silver,
        "%a": lambda c: c.alignment,
        "%r": lambda r: r.name if r and r.name else "",
        "%e": lambda r: r.get_formatted_exits() if r else "",
        "%R": lambda c, r: r.vnum if c.is_immortal() and r else "",
        "%z": lambda c, a: a.name if c.is_immortal() and a else "",
        "%c": lambda: "\n",
    }


PromptFn = Union[
    Callable[[], str],
    Callable[[Character], str],
    Callable[[Room], str],
    Callable[[Area], str],
    Callable[[Character, Room], str],
    Callable[[Character, Area], str],
]


@dataclass
class PromptFormat:
    health: bool = False
    max_health: bool = False
    mana: bool = False
    max_mana: bool = False
    movement: bool = False
    max_movement: bool = False
    experience: bool = False
    accumulated_experience: bool = False
    gold: bool = False
    silver: bool = False
    alignment: bool = False
    room_name: bool = False
    exits: bool = False
    room_vnum: bool = False
    area_name: bool = False
    carriage_return: bool = False

    @classmethod
    def default(cls) -> PromptFormat:
        return cls(health=True, mana=True, movement=True)

    @classmethod
    def from_template(cls, template: dict) -> PromptFormat:
        if template is None:
            template = {}

        return cls(
            health=bool(template.get("hp", False)),
            max_health=bool(template.get("max_hp", False)),
            mana=bool(template.get("mana", False)),
            max_mana=bool(template.get("max_mana", False)),
            movement=bool(template.get("movement", False)),
            max_movement=bool(template.get("max_movement", False)),
            experience=bool(template.get("xp", False)),
            accumulated_experience=bool(template.get("max_xp", False)),
            gold=bool(template.get("gold", False)),
            silver=bool(template.get("silver", False)),
            alignment=bool(template.get("alignment", False)),
            room_name=bool(template.get("room_name", False)),
            exits=bool(template.get("exits", False)),
            room_vnum=bool(template.get("room_vnum", False)),
            area_name=bool(template.get("area_name", False)),
            carriage_return=bool(template.get("carriage_return", False)),
        )

    def to_json(self) -> dict:
        return asdict(self)

    def _render_health(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.health and not self.max_health:
            parts.append(f"{self._call_prompt_lambda(prompt_map['%h'], character, room, area)}hp")
        elif self.health:
            parts.append(str(self._call_prompt_lambda(prompt_map["%h"], character, room, area)))

        if self.max_health:
            parts.append(f"/{self._call_prompt_lambda(prompt_map['%H'], character, room, area)}")

    def _render_mana(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.mana and not self.max_mana:
            if self.health or self.max_health:
                parts.append(" ")
            parts.append(f"{self._call_prompt_lambda(prompt_map['%m'], character, room, area)}m")
        elif self.mana:
            parts.append(str(self._call_prompt_lambda(prompt_map["%m"], character, room, area)))

        if self.max_mana:
            parts.append(f"/{self._call_prompt_lambda(prompt_map['%M'], character, room, area)}")

    def _render_movement(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.movement and not self.max_movement:
            if self.health or self.max_health or self.mana or self.max_mana:
                parts.append(" ")
            parts.append(f"{self._call_prompt_lambda(prompt_map['%v'], character, room, area)}mv")
        elif self.movement:
            parts.append(str(self._call_prompt_lambda(prompt_map["%v"], character, room, area)))

        if self.max_movement:
            parts.append(f"/{self._call_prompt_lambda(prompt_map['%V'], character, room, area)}")

    def _render_experience(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.experience and not self.accumulated_experience:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(f"{self._call_prompt_lambda(prompt_map['%x'], character, room, area)}xp")
        elif self.experience:
            parts.append(str(self._call_prompt_lambda(prompt_map["%x"], character, room, area)))

        if self.accumulated_experience:
            parts.append(f"/{self._call_prompt_lambda(prompt_map['%X'], character, room, area)}")

    def _render_gold(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.gold:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(prompt_map["%g"], character, room, area)))

    def _render_silver(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.silver:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(prompt_map["%s"], character, room, area)))

    def _render_alignment(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.alignment:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(prompt_map["%a"], character, room, area)))

    def _render_room_name(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.room_name:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(prompt_map["%r"], character, room, area)))

    def _render_exits(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.exits:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(prompt_map["%e"], character, room, area)))

    def _render_room_vnum(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.room_vnum:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(prompt_map["%R"], character, room, area)))

    def _render_area_name(self, parts: list[str], prompt_map: dict, character: Character, room: Room, area: Area):
        if self.area_name:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(prompt_map["%z"], character, room, area)))

    def render_prompt(self, status: SessionStatus, character: Character, room: Room, area: Area) -> Message:
        parts = [self._tag_afk(status), "<"]
        prompt_map = build_prompt_map()

        self._render_health(parts, prompt_map, character, room, area)
        self._render_mana(parts, prompt_map, character, room, area)
        self._render_movement(parts, prompt_map, character, room, area)
        self._render_experience(parts, prompt_map, character, room, area)
        self._render_gold(parts, prompt_map, character, room, area)
        self._render_silver(parts, prompt_map, character, room, area)
        self._render_alignment(parts, prompt_map, character, room, area)
        self._render_room_name(parts, prompt_map, character, room, area)
        self._render_exits(parts, prompt_map, character, room, area)
        self._render_room_vnum(parts, prompt_map, character, room, area)
        self._render_area_name(parts, prompt_map, character, room, area)

        parts.append(">")
        if self.carriage_return:
            parts.append(str(self._call_prompt_lambda(prompt_map["%c"], character, room, area)))

        return Message(type=MessageType.GAME, data={'text': "".join(parts)})

    @staticmethod
    def _tag_afk(status: SessionStatus) -> str:
        from server.session import SessionStatus
        if status == SessionStatus.IDLING:
            return "<AFK>"
        return ""

    @staticmethod
    def _call_prompt_lambda(fn: PromptFn, character: Character, room: Room, area: Area) -> str:
        argc = len(inspect.signature(fn).parameters)
        if argc == 0:
            return fn()

        if argc == 1:
            names = list(inspect.signature(fn).parameters.keys())
            param = names[0]
            if param == "c":
                return fn(character)
            if param == "r":
                return fn(room)
            if param == "a":
                return fn(area)
            raise ValueError(f"Unsupported single-arg lambda parameter: {param}")

        if argc == 2:
            names = list(inspect.signature(fn).parameters.keys())
            if names == ["c", "r"]:
                return fn(character, room)
            if names == ["c", "a"]:
                return fn(character, area)
            raise ValueError(f"Unsupported two-arg lambda parameters: {names}")

        raise ValueError("Unsupported lambda arity")
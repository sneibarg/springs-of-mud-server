import inspect

from dataclasses import dataclass, asdict
from typing import Callable, Union
from area import Room, Area
from player import Character
from server.protocol import Message, MessageType
from server.session import SessionStatus


def build_prompt_map():
    return {
        "%h": lambda c: c.hp,
        "%H": lambda c: c.max_hp,
        "%m": lambda c: c.mana,
        "%M": lambda c: c.max_mana,
        "%v": lambda c: c.move,
        "%V": lambda c: c.max_move,
        "%x": lambda c: c.exp,
        "%X": lambda c: c.exp_to_level,
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
    hp: bool = False
    max_hp: bool = False
    mana: bool = False
    max_mana: bool = False
    movement: bool = False
    max_movement: bool = False
    xp: bool = False
    max_xp: bool = False
    gold: bool = False
    silver: bool = False
    alignment: bool = False
    room_name: bool = False
    exits: bool = False
    room_vnum: bool = False
    area_name: bool = False
    carriage_return: bool = False

    @classmethod
    def default(cls) -> "PromptFormat":
        return cls(hp=True, mana=True, movement=True)

    @classmethod
    def from_template(cls, template: str) -> "PromptFormat":
        return cls(
            hp="%h" in template,
            max_hp="%H" in template,
            mana="%m" in template,
            max_mana="%M" in template,
            movement="%v" in template,
            max_movement="%V" in template,
            xp="%x" in template,
            max_xp="%X" in template,
            gold="%g" in template,
            silver="%s" in template,
            alignment="%a" in template,
            room_name="%r" in template,
            exits="%e" in template,
            room_vnum="%R" in template,
            area_name="%z" in template,
            carriage_return="%c" in template,
        )

    def to_json(self) -> dict:
        return asdict(self)

    def render_prompt(self, status: SessionStatus, character: Character, room: Room, area: Area) -> Message:
        parts = [self._tag_afk(status), "<"]
        if self.hp:
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%h"], character, room, area)))
        if self.max_hp:
            parts.append(f"/{self._call_prompt_lambda(build_prompt_map()['%H'], character, room, area)}")

        if self.mana:
            if self.hp or self.max_hp:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%m"], character, room, area)))
        if self.max_mana:
            parts.append(f"/{self._call_prompt_lambda(build_prompt_map()['%M'], character, room, area)}")

        if self.movement:
            if self.hp or self.max_hp or self.mana or self.max_mana:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%v"], character, room, area)))
        if self.max_movement:
            parts.append(f"/{self._call_prompt_lambda(build_prompt_map()['%V'], character, room, area)}")

        if self.xp:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%x"], character, room, area)))
        if self.max_xp:
            parts.append(f"/{self._call_prompt_lambda(build_prompt_map()['%X'], character, room, area)}")

        if self.gold:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%g"], character, room, area)))

        if self.silver:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%s"], character, room, area)))

        if self.alignment:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%a"], character, room, area)))

        if self.room_name:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%r"], character, room, area)))

        if self.exits:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%e"], character, room, area)))

        if self.room_vnum:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%R"], character, room, area)))

        if self.area_name:
            if len(parts) > 2:
                parts.append(" ")
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%z"], character, room, area)))

        parts.append(">")
        if self.carriage_return:
            parts.append(str(self._call_prompt_lambda(build_prompt_map()["%c"], character, room, area)))

        return Message(type=MessageType.GAME, data={'text': "".join(parts)})

    @staticmethod
    def _tag_afk(status: SessionStatus) -> str:
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
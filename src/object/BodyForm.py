from __future__ import annotations

from enum import IntEnum

from game.GameData import GameData


class BodyForm:
    _enum: type[IntEnum] | None = None

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("BodyForm may not be instantiated.")

    @classmethod
    def configure(cls, game_data: GameData) -> None:
        member_map = dict(getattr(game_data, "enums", {}).get("bodyForm", {}))
        if not member_map:
            raise RuntimeError("GameData is missing bodyForm enum definitions.")

        cls.reset_for_tests()
        cls._enum = IntEnum("BodyForm", {str(name).strip().upper(): int(value) for name, value in member_map.items()})
        for name, member in cls._enum.__members__.items():
            setattr(cls, name, member)

    @classmethod
    def reset_for_tests(cls) -> None:
        for name in list(vars(cls).keys()):
            if name.startswith("FORM_"):
                delattr(cls, name)
        cls._enum = None

    @classmethod
    def _require_configured(cls) -> type[IntEnum]:
        if cls._enum is None:
            raise RuntimeError("BodyForm has not been configured.")
        return cls._enum

    @classmethod
    def members(cls) -> dict[str, IntEnum]:
        return dict(cls._require_configured().__members__)

    @classmethod
    def value(cls, name: str) -> int:
        enum_type = cls._require_configured()
        return int(enum_type[str(name).strip().upper()].value)

    @classmethod
    def mask(cls, *names: str) -> int:
        total = 0
        for name in names:
            total |= cls.value(name)
        return total

    @classmethod
    def has(cls, flags: int, bit) -> bool:
        raw_bit = getattr(bit, "value", bit)
        return (int(flags) & int(raw_bit)) != 0

    @classmethod
    def default_player_form(cls) -> int:
        return cls.mask("FORM_EDIBLE", "FORM_SENTIENT", "FORM_BIPED", "FORM_MAMMAL")


__all__ = ["BodyForm"]

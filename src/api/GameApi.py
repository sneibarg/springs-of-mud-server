from enum import IntEnum
from threading import RLock
from typing import Any

from game.GameData import GameData

from util.GenericUtil import GenericUtil


class GameApi:
    _lock = RLock()
    _configured = False
    _shared_enums = None
    _shared_enums_source = None
    _game_data = None
    _enums = None
    _races = None
    _item_table = None
    _attribute_bonuses = None
    _classes = None
    _pc_races = None
    _titles = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._lock = RLock()
        cls._configured = False
        cls._game_data = None
        cls._enums = None
        cls._races = None
        cls._item_table = None
        cls._attribute_bonuses = None
        cls._classes = None
        cls._pc_races = None
        cls._titles = None

    def __new__(cls, *args, **kwargs):
        raise RuntimeError(
            f"{cls.__name__} may not be instantiated. Use {cls.__name__}.<method>(...)."
        )

    @classmethod
    def configure(cls, game_data: GameData) -> None:
        with cls._lock:
            cls._game_data = game_data
            cls._configure_enums(game_data)
            cls._configure_races(game_data)
            cls._configure_item_table(game_data)
            cls._configure_attribute_bonuses(game_data)
            cls._configure_classes(game_data)
            cls._configure_pc_races(game_data)
            cls._configure_titles(game_data)
            cls._configure_internal_variables(game_data)
            cls._configured = True

    @classmethod
    def reset_for_tests(cls) -> None:
        with cls._lock:
            prior_game_data = cls._game_data
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

        if GameApi._shared_enums_source is prior_game_data:
            GameApi._shared_enums = None
            GameApi._shared_enums_source = None

    @classmethod
    def _configure_internal_variables(cls, game_data: GameData) -> None:
        return None

    @classmethod
    def _reset_internal_variables(cls) -> None:
        return None

    @classmethod
    def _require_configured(cls) -> None:
        if not cls._configured:
            raise RuntimeError(f"{cls.__name__} has not been configured.")

    @classmethod
    def _configure_enums(cls, game_data: GameData) -> None:
        cls._enums = cls._shared_enums_for(game_data)

    @classmethod
    def _shared_enums_for(cls, game_data: GameData) -> dict[str, type[IntEnum]]:
        if GameApi._shared_enums_source is not game_data:
            GameApi._shared_enums = {
                enum_name: GenericUtil.build_int_enum(enum_name, member_map)
                for enum_name, member_map in game_data.enums.items()
            }
            GameApi._shared_enums_source = game_data
        return GameApi._shared_enums or {}

    @classmethod
    def register_shared_enums(cls, game_data: GameData, enums: dict[str, type[IntEnum]]) -> None:
        GameApi._shared_enums = enums
        GameApi._shared_enums_source = game_data

    @classmethod
    def _configure_races(cls, game_data: GameData) -> None:
        cls._races = dict(game_data.races or {})

    @classmethod
    def _configure_item_table(cls, game_data: GameData) -> None:
        cls._item_table = dict(game_data.item_table or {})

    @classmethod
    def _configure_attribute_bonuses(cls, game_data: GameData) -> None:
        cls._attribute_bonuses = dict(game_data.attribute_bonuses or {})

    @classmethod
    def _configure_classes(cls, game_data: GameData) -> None:
        cls._classes = dict(game_data.classes or {})

    @classmethod
    def _configure_pc_races(cls, game_data: GameData) -> None:
        cls._pc_races = dict(game_data.pc_races or {})

    @classmethod
    def _configure_titles(cls, game_data: GameData) -> None:
        cls._titles = dict(game_data.titles or {})

    @classmethod
    def _enums_map(cls) -> dict[str, type[IntEnum]]:
        cls._require_configured()
        return cls._enums or {}

    @classmethod
    def _races_map(cls) -> dict:
        cls._require_configured()
        return cls._races or {}

    @classmethod
    def _item_table_map(cls) -> dict:
        cls._require_configured()
        return cls._item_table or {}

    @classmethod
    def _attribute_bonus_map(cls) -> dict:
        cls._require_configured()
        return cls._attribute_bonuses or {}

    @classmethod
    def _classes_map(cls) -> dict:
        cls._require_configured()
        return cls._classes or {}

    @classmethod
    def _pc_races_map(cls) -> dict:
        cls._require_configured()
        return cls._pc_races or {}

    @classmethod
    def _titles_map(cls) -> dict:
        cls._require_configured()
        return cls._titles or {}

    @classmethod
    def get_enum(cls, enum_name: str) -> type[IntEnum] | Any | None:
        return cls._enums_map().get(enum_name)

    @staticmethod
    def is_set(flag: int, bit) -> bool:
        if hasattr(bit, "value"):
            return (flag & bit.value) != 0
        return (flag & bit) != 0

    @staticmethod
    def set_bit(flag: int, bit) -> int:
        if hasattr(bit, "value"):
            return flag | bit.value
        return flag | bit

    @staticmethod
    def unset_bit(flag: int, bit) -> int:
        if hasattr(bit, "value"):
            return flag & ~bit.value
        return flag & ~bit

    @staticmethod
    def parse_flag_string(flag_str: str | None, FlagLetters: type[IntEnum] | None) -> int:
        if not flag_str or str(flag_str).strip() in ("", "0", "None", "null"):
            return 0

        total = 0
        for char in flag_str.strip():
            if char.isalnum():
                upper = char.upper()
                try:
                    member = FlagLetters[upper]
                    total |= member
                except KeyError:
                    pass

        return total

    @staticmethod
    def convert_flags(flag_value: str) -> int:
        return GameApi.letters_to_flags(str(flag_value or ""))

    @staticmethod
    def letters_to_flags(value: str) -> int:
        total = 0
        for c in str(value or "").upper():
            if "A" <= c <= "Z":
                total |= (1 << (ord(c) - ord("A")))
        return total

    @staticmethod
    def flags_to_letters(value: int) -> str:
        if GenericUtil.to_int(value, 0) <= 0:
            return ""
        out = []
        raw = GenericUtil.to_int(value, 0)
        for bit in range(26):
            if raw & (1 << bit):
                out.append(chr(ord("A") + bit))
        return "".join(out)

    @staticmethod
    def flags_to_int(raw) -> int:
        value = GenericUtil.to_int(raw, None)
        if value is not None:
            return value
        return GameApi.letters_to_flags(str(raw or "0"))

    @staticmethod
    def enum_bit(enum_obj, *names: str) -> int:
        if enum_obj is None:
            return 0
        for name in names:
            if hasattr(enum_obj, name):
                return int(getattr(enum_obj, name).value)
        return 0

    @staticmethod
    def enum_names(enum_obj, prefix: str) -> list[str]:
        if enum_obj is None:
            return []
        names = []
        for field in dir(enum_obj):
            if field.startswith(prefix):
                names.append(field)
        return sorted(names)

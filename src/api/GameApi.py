from enum import IntEnum
from threading import RLock
from typing import Any

from game.EnumProvider import EnumProvider
from game.GameData import GameData
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil


class GameApi:
    _lock = RLock()
    _configured = False
    _game_data = None
    _enums: dict[str, type[IntEnum]] = {}
    _enum_provider = None
    _races = {}
    _item_table = {}
    _attribute_bonuses = {}
    _classes = {}
    _pc_races = {}
    _titles = {}
    _logger = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._lock = RLock()
        cls._logger = None

    @classmethod
    def configure(cls, game_data: GameData, enum_provider: EnumProvider | None = None) -> None:
        with GameApi._lock:
            provider = enum_provider or GameApi._build_enum_provider(game_data)
            GameApi._game_data = game_data
            GameApi._enum_provider = provider
            GameApi._enums = {
                name: provider.get(name)
                for name in provider.all_names()
            }
            GameApi._configure_races(game_data)
            GameApi._configure_item_table(game_data)
            GameApi._configure_attribute_bonuses(game_data)
            GameApi._configure_classes(game_data)
            GameApi._configure_pc_races(game_data)
            GameApi._configure_titles(game_data)
            GameApi._configured = True

    @classmethod
    def reset_for_tests(cls) -> None:
        with GameApi._lock:
            GameApi._configured = False
            GameApi._game_data = None
            GameApi._enum_provider = None
            GameApi._enums = {}
            GameApi._races = {}
            GameApi._item_table = {}
            GameApi._attribute_bonuses = {}
            GameApi._classes = {}
            GameApi._pc_races = {}
            GameApi._titles = {}
            cls._reset_internal_variables()

    @classmethod
    def _reset_internal_variables(cls) -> None:
        return None

    @classmethod
    def _require_configured(cls) -> None:
        if not GameApi._configured:
            raise RuntimeError(f"{cls.__name__} has not been configured.")

    @classmethod
    def _logger_obj(cls):
        if cls._logger is None:
            cls._logger = LoggerFactory.get_logger(__name__)
        return cls._logger

    @classmethod
    def _configure_races(cls, game_data: GameData) -> None:
        GameApi._races = dict(game_data.races or {})

    @classmethod
    def _configure_item_table(cls, game_data: GameData) -> None:
        GameApi._item_table = dict(game_data.item_table or {})

    @classmethod
    def _configure_attribute_bonuses(cls, game_data: GameData) -> None:
        GameApi._attribute_bonuses = dict(game_data.attribute_bonuses or {})

    @classmethod
    def _configure_classes(cls, game_data: GameData) -> None:
        GameApi._classes = dict(game_data.classes or {})

    @classmethod
    def _configure_pc_races(cls, game_data: GameData) -> None:
        GameApi._pc_races = dict(game_data.pc_races or {})

    @classmethod
    def _configure_titles(cls, game_data: GameData) -> None:
        GameApi._titles = dict(game_data.titles or {})

    @staticmethod
    def _build_enum_provider(game_data: GameData) -> EnumProvider:
        enums = {}
        for enum_name, member_map in dict(getattr(game_data, "enums", {}) or {}).items():
            enums[enum_name] = GenericUtil.build_int_enum(enum_name, member_map)
        return EnumProvider(enums)

    @classmethod
    def _enums_map(cls) -> dict[str, type[IntEnum]]:
        cls._require_configured()
        return GameApi._enums

    @classmethod
    def _races_map(cls) -> dict:
        cls._require_configured()
        return GameApi._races

    @classmethod
    def _item_table_map(cls) -> dict:
        cls._require_configured()
        return GameApi._item_table

    @classmethod
    def _attribute_bonus_map(cls) -> dict:
        cls._require_configured()
        return GameApi._attribute_bonuses

    @classmethod
    def _classes_map(cls) -> dict:
        cls._require_configured()
        return GameApi._classes

    @classmethod
    def _pc_races_map(cls) -> dict:
        cls._require_configured()
        return GameApi._pc_races

    @classmethod
    def _titles_map(cls) -> dict:
        cls._require_configured()
        return GameApi._titles

    @classmethod
    def get_enum(cls, enum_name: str) -> type[IntEnum] | Any | None:
        cls._require_configured()
        if GameApi._enum_provider is None or not GameApi._enum_provider.contains(enum_name):
            return None
        return GameApi._enum_provider.get(enum_name)

    @classmethod
    def load_enums(cls, **aliases: str) -> None:
        cls._require_configured()
        for attr_name, enum_name in aliases.items():
            setattr(cls, attr_name, cls.get_enum(enum_name))

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

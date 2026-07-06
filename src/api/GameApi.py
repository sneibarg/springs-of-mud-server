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
    _weapons = {}
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
            GameApi._game_data = game_data
            GameApi._enum_provider = enum_provider
            GameApi._configure_races(game_data)
            GameApi._configure_item_table(game_data)
            GameApi._configure_weapons(game_data)
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
            GameApi._weapons = {}
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
    def _configure_weapons(cls, game_data: GameData) -> None:
        GameApi._weapons = dict(game_data.weapons or {})

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

    @classmethod
    def enums(cls) -> dict[str, type[IntEnum]]:
        cls._require_configured()
        return GameApi._enums

    @classmethod
    def enum_provider(cls) -> EnumProvider:
        cls._require_configured()
        if GameApi._enum_provider is None:
            raise RuntimeError("Enum provider is not configured.")
        return GameApi._enum_provider

    @classmethod
    def races_map(cls) -> dict:
        cls._require_configured()
        return GameApi._races

    @classmethod
    def item_table_map(cls) -> dict:
        cls._require_configured()
        return GameApi._item_table

    @classmethod
    def weapons_map(cls) -> dict:
        cls._require_configured()
        return GameApi._weapons

    @classmethod
    def attribute_bonus_map(cls) -> dict:
        cls._require_configured()
        return GameApi._attribute_bonuses

    @classmethod
    def classes_map(cls) -> dict:
        cls._require_configured()
        return GameApi._classes

    @classmethod
    def pc_races_map(cls) -> dict:
        cls._require_configured()
        return GameApi._pc_races

    @classmethod
    def titles(cls) -> dict:
        cls._require_configured()
        return GameApi._titles

    @classmethod
    def deny_list(cls) -> list[str]:
        cls._require_configured()
        if GameApi._game_data is None:
            return []
        deny_list = getattr(GameApi._game_data, "denyList", None)
        if deny_list is None:
            object.__setattr__(GameApi._game_data, "denyList", [])
        return GameApi._game_data.denyList

    @classmethod
    def add_denied_site(cls, site: str) -> bool:
        normalized = cls.normalize_site(site)
        if not normalized:
            return False
        deny_list = cls.deny_list()
        if any(cls.normalize_site(entry) == normalized for entry in deny_list):
            return False
        deny_list.append(normalized)
        return True

    @classmethod
    def remove_denied_site(cls, site: str) -> bool:
        normalized = cls.normalize_site(site)
        if not normalized:
            return False
        deny_list = cls.deny_list()
        for index, entry in enumerate(list(deny_list)):
            if cls.normalize_site(entry) == normalized:
                del deny_list[index]
                return True
        return False

    @classmethod
    def has_denied_site(cls, site: str) -> bool:
        normalized = cls.normalize_site(site)
        if not normalized:
            return False
        return any(cls.normalize_site(entry) == normalized for entry in cls.deny_list())

    @classmethod
    def is_site_denied(cls, site: str) -> bool:
        normalized = cls.normalize_site(site)
        if not normalized:
            return False
        return any(cls._site_pattern_matches(entry, normalized) for entry in cls.deny_list())

    @classmethod
    def get_enum(cls, enum_name: str) -> type[IntEnum] | Any | None:
        cls._require_configured()
        if GameApi._enum_provider is None or not GameApi._enum_provider.contains(enum_name):
            return None
        return GameApi._enum_provider.get(enum_name)

    @staticmethod
    def normalize_site(site: str) -> str:
        return str(site or "").strip().lower()

    @staticmethod
    def looks_like_site(site: str) -> bool:
        text = GameApi.normalize_site(site).strip("*")
        if not text:
            return False
        if ":" in text or "." in text:
            return True
        return all(part.isdigit() for part in text.split(".")) if "." in text else False

    @staticmethod
    def _site_pattern_matches(pattern: str, site: str) -> bool:
        entry = GameApi.normalize_site(pattern)
        host = GameApi.normalize_site(site)
        if not entry or not host:
            return False
        prefix = entry.startswith("*")
        suffix = entry.endswith("*")
        name = entry.strip("*")
        if not name:
            return False
        if prefix and suffix:
            return name in host
        if prefix:
            return host.endswith(name)
        if suffix:
            return host.startswith(name)
        return host == name

    @classmethod
    def load_enums(cls, **aliases: str) -> None:
        cls._require_configured()
        for attr_name, enum_name in aliases.items():
            setattr(cls, attr_name, cls.get_enum(enum_name))

    @classmethod
    def is_set(cls, flag: int, bit) -> bool:
        if type(flag) is str:
            flag = GameApi.flags_to_int(flag)
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
            if name in enum_obj.__members__:
                return int(enum_obj[name].value)
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

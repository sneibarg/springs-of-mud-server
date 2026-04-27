from enum import IntEnum
from threading import RLock
from typing import Any, Callable, Dict, List, Optional

from game.GameMacros import GameMacros
from object.Item import Item


class ObjectMacros(GameMacros):
    _lock = RLock()
    _configured = False

    _races_provider: Optional[Callable[[], dict]] = None
    _item_table_provider: Optional[Callable[[], dict]] = None
    _enums_provider: Optional[Callable[[], dict[str, IntEnum]]] = None

    _races = None
    _item_table = None
    _enums = None

    def __new__(cls, *args, **kwargs):
        raise RuntimeError(
            "ObjectMacros may not be instantiated. Use ObjectMacros.<method>(...)."
        )

    @classmethod
    def configure(
        cls,
        *,
        races_provider: Callable[[], dict],
        item_table_provider: Callable[[], dict],
        enums_provider: Callable[[], dict[str, IntEnum]],
    ) -> None:
        with cls._lock:
            cls._races_provider = races_provider
            cls._item_table_provider = item_table_provider
            cls._enums_provider = enums_provider
            cls._configured = True

    @classmethod
    def reset_for_tests(cls) -> None:
        with cls._lock:
            cls._configured = False
            cls._races_provider = None
            cls._item_table_provider = None
            cls._enums_provider = None
            cls._races = None
            cls._item_table = None
            cls._enums = None

    @classmethod
    def _require_configured(cls) -> None:
        if not cls._configured:
            raise RuntimeError("ObjectMacros has not been configured.")

    @classmethod
    def _races_map(cls) -> dict:
        if cls._races is None:
            cls._require_configured()
            if cls._races_provider is None:
                raise RuntimeError("ObjectMacros races provider not configured.")
            cls._races = cls._races_provider()
        return cls._races

    @classmethod
    def _item_table_map(cls) -> dict:
        if cls._item_table is None:
            cls._require_configured()
            if cls._item_table_provider is None:
                raise RuntimeError("ObjectMacros item_table provider not configured.")
            cls._item_table = cls._item_table_provider()
        return cls._item_table

    @classmethod
    def _enums_map(cls) -> dict[str, IntEnum]:
        if cls._enums is None:
            cls._require_configured()
            if cls._enums_provider is None:
                raise RuntimeError("ObjectMacros enums provider not configured.")
            cls._enums = cls._enums_provider()
        return cls._enums

    @classmethod
    def get_enum(cls, enum_name: str) -> Any:
        return cls._enums_map().get(enum_name)

    @classmethod
    def race_data(cls, race_name: str) -> dict:
        return cls._races_map().get(race_name, {})

    @classmethod
    def is_container_closed(cls, item) -> bool:
        try:
            flags = int(item.value1)
            container_state = cls.get_enum("containerState")
            if not hasattr(container_state, "CONT_CLOSED"):
                return False
            return cls.is_set(flags, container_state.CONT_CLOSED.value)
        except (TypeError, ValueError):
            return False

    @classmethod
    def can_wear(cls, obj: Item, part: int) -> bool:
        return cls.is_set(int(obj.wear_flags), part)

    @classmethod
    def is_obj_stat(cls, obj: Item, stat: int) -> bool:
        return cls.is_set(int(obj.extra_flags), stat)

    @classmethod
    def is_weapon_stat(cls, obj: Item, stat: int) -> bool:
        return cls.is_set(int(obj.value4), stat)

    @classmethod
    def weight_multiplier(cls, obj: Item) -> int:
        item_types = cls.get_enum("itemTypes")
        item_table = cls._item_table_map()
        return int(obj.value3) if item_table[obj.item_type] == item_types.ITEM_CONTAINER.name else 100

    @classmethod
    def decode_form_and_parts(cls, race_name: str, BodyForm: type[IntEnum], BodyParts: type[IntEnum]) -> Dict[str, List[str]]:
        race = cls._races_map().get(race_name)
        if not race:
            return {"form": [], "parts": []}

        form_value: int = race.get("form", 0)
        parts_value: int = race.get("parts", 0)

        decoded_form = [member.name for member in BodyForm if form_value & member.value]
        decoded_parts = [member.name for member in BodyParts if parts_value & member.value]

        return {
            "form": decoded_form,
            "parts": decoded_parts
        }

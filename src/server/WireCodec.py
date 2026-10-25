"""Convert schema values without rewriting arbitrary mapping keys."""

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any


def camelize_field_name(name: str) -> str:
    head, *tail = name.split('_')
    return head + ''.join(part.capitalize() for part in tail)


def serialize_wire_value(value: Any, *, excluded_fields: frozenset[str] = frozenset()) -> Any:
    """Dataclass fields are schema names; dictionary keys are caller-owned data.

    Services supply their own exclusions and explicit top-level wire fields.
    Raw dictionary records must already use their intended wire keys.
    """
    if isinstance(value, Enum):
        return serialize_wire_value(value.value, excluded_fields=excluded_fields)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple, set)):
        return [serialize_wire_value(item, excluded_fields=excluded_fields) for item in value]
    if isinstance(value, dict):
        return {key: serialize_wire_value(item, excluded_fields=excluded_fields) for key, item in value.items()}
    if is_dataclass(value) and not isinstance(value, type):
        return {
            camelize_field_name(field.name): serialize_wire_value(
                getattr(value, field.name), excluded_fields=excluded_fields)
            for field in fields(value) if field.name not in excluded_fields
        }
    return value

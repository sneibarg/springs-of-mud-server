from dataclasses import dataclass, field
from typing import Any
from server.LoggerFactory import LoggerFactory


@dataclass
class Special:
    id: str = ""
    area_id: str = ""
    mob_vnum: str = ""
    name: str = ""
    special_function: list[str] = field(default_factory=list)
    comment: str = ""

    def __post_init__(self):
        self.__name__ = "Special"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Special):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from game.GenericUtil import GenericUtil
        normalized = GenericUtil.camel_to_snake_case(data)
        normalized["id"] = cls._extract_id(data, normalized)
        normalized["area_id"] = str(normalized.get("area_id", "") or "")
        normalized["mob_vnum"] = str(normalized.get("mob_vnum", "") or "")
        normalized["comment"] = str(normalized.get("comment", "") or "")
        normalized.pop("_class", None)
        normalized.pop("_id", None)

        raw_name = normalized.get("name")
        raw_special = normalized.get("special_function")

        if not raw_name and isinstance(raw_special, str):
            raw_name = raw_special
            raw_special = []

        normalized["name"] = str(raw_name or "")
        normalized["special_function"] = cls._normalize_lambdas(raw_special)
        return cls(**normalized)

    @staticmethod
    def _extract_id(source: dict[str, Any], normalized: dict[str, Any]) -> str:
        raw_id = normalized.get("id")
        if isinstance(raw_id, str) and raw_id.strip():
            return raw_id.strip()

        nested_id = source.get("_id")
        if isinstance(nested_id, dict):
            oid = nested_id.get("$oid")
            if oid:
                return str(oid)

        if nested_id:
            return str(nested_id)
        return ""

    @staticmethod
    def _normalize_lambdas(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(entry).strip() for entry in value if str(entry).strip()]
        if isinstance(value, str) and value.strip().startswith("lambda "):
            return [value.strip()]
        return []

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CharacterRace:
    who_name: str = ""
    points: int = 0
    class_mult: int = 100
    skills: list[str] = field(default_factory=list)
    strength: int = 0
    max_strength: int = 0
    intelligence: int = 0
    max_intelligence: int = 0
    wisdom: int = 0
    max_wisdom: int = 0
    dexterity: int = 0
    max_dexterity: int = 0
    constitution: int = 0
    max_constitution: int = 0
    size: str = ""

    @classmethod
    def from_json(cls, data: Any, character_class: Any = None) -> "CharacterRace":
        from util.GenericUtil import GenericUtil

        if isinstance(data, CharacterRace):
            return data
        if isinstance(data, str):
            return cls.from_name(data)
        if not isinstance(data, dict):
            return cls()

        payload = GenericUtil.camel_to_snake_case(data)
        payload.setdefault("who_name", "")
        payload["points"] = int(payload.get("points", 0) or 0)
        payload["skills"] = [str(value) for value in list(payload.get("skills", []) or [])]
        payload["size"] = str(payload.get("size", "") or "")

        if isinstance(payload.get("stats"), list) or isinstance(payload.get("max_stats"), list) or isinstance(payload.get("class_mult"), list):
            stats = [int(value) for value in list(payload.get("stats", []) or [])]
            max_stats = [int(value) for value in list(payload.get("max_stats", []) or [])]
            payload = {
                "who_name": str(payload.get("who_name", "") or ""),
                "points": int(payload.get("points", 0) or 0),
                "class_mult": cls._class_mult_for_class(payload.get("class_mult", []), character_class),
                "skills": [str(value) for value in list(payload.get("skills", []) or [])],
                "strength": cls._stat_at(stats, 0),
                "max_strength": cls._stat_at(max_stats, 0),
                "intelligence": cls._stat_at(stats, 1),
                "max_intelligence": cls._stat_at(max_stats, 1),
                "wisdom": cls._stat_at(stats, 2),
                "max_wisdom": cls._stat_at(max_stats, 2),
                "dexterity": cls._stat_at(stats, 3),
                "max_dexterity": cls._stat_at(max_stats, 3),
                "constitution": cls._stat_at(stats, 4),
                "max_constitution": cls._stat_at(max_stats, 4),
                "size": str(payload.get("size", "") or ""),
            }
        else:
            payload["class_mult"] = int(payload.get("class_mult", 100) or 100)
            for field_name in (
                "strength",
                "max_strength",
                "intelligence",
                "max_intelligence",
                "wisdom",
                "max_wisdom",
                "dexterity",
                "max_dexterity",
                "constitution",
                "max_constitution",
            ):
                payload[field_name] = int(payload.get(field_name, 0) or 0)
        return cls(**payload)

    @classmethod
    def from_name(cls, race_name: str) -> "CharacterRace":
        label = str(race_name or "").strip()
        return cls(who_name=label)

    @property
    def name(self) -> str:
        return str(self.who_name or "").strip()

    @staticmethod
    def _stat_at(values: list[int], index: int) -> int:
        if 0 <= index < len(values):
            return int(values[index] or 0)
        return 0

    @staticmethod
    def _class_mult_for_class(values: Any, character_class: Any) -> int:
        if not isinstance(values, list):
            return int(values or 100)
        class_name = str(getattr(character_class, "name", character_class) or "").strip().lower()
        class_index = {
            "mage": 0,
            "cleric": 1,
            "thief": 2,
            "warrior": 3,
        }.get(class_name, 0)
        if 0 <= class_index < len(values):
            return int(values[class_index] or 100)
        return 100

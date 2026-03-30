from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class GameData:
    id: str
    kind: str
    status: str
    version: Version
    constants: Constants
    enums: Dict[str, Dict[str, int]]
    flags: Dict[str, Dict[str, int]]
    attribute_bonuses: Dict[str, Dict[str, Dict]] = field(default_factory=dict)
    classes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    races: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    pc_races: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    wiznet_table: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    groups: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    titles: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    item_table: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    weapons: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    attacks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    liquids: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    well_known_vnums: Dict[str, Dict[str, int]] = field(default_factory=dict)
    integrity: Integrity = field(default_factory=lambda: Integrity("", BuildInfo("", "")))

    @staticmethod
    def from_json(doc: Dict[str, Any]) -> "GameData":
        _id = doc.get("_id", doc.get("id"))
        if not _id:
            raise KeyError("GameData requires '_id' (or 'id')")

        return GameData(
            id=_id,
            kind=doc["kind"],
            status=doc.get("status", "active"),
            version=Version.from_dict(doc["version"]),
            constants=Constants.from_dict(doc.get("constants", {})),
            enums=dict(doc.get("enums", {})),
            flags=dict(doc.get("flags", {})),

            classes=dict(doc.get("classes", {})),
            races=dict(doc.get("races", {})),
            pc_races=dict(doc.get("pcRaces", {})),
            groups=dict(doc.get("groups", {})),
            weapons=dict(doc.get("weapons", {})),
            attacks=dict(doc.get("attacks", {})),
            liquids=dict(doc.get("liquids", {})),

            well_known_vnums=dict(doc.get("wellKnownVnums", {})),
            integrity=Integrity.from_dict(doc.get("integrity", {})),
        )

    def flag_value(self, domain: str, name: str) -> int:
        return self.flags[domain][name]


@dataclass(frozen=True)
class Version:
    family: str
    lineage: list[str]
    semver: str
    created_at: datetime
    notes: Optional[str] = None

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Version":
        return Version(
            family=d["family"],
            lineage=list(d.get("lineage", [])),
            semver=d["semver"],
            created_at=_parse_datetime(d["createdAt"]),
            notes=d.get("notes"),
        )


@dataclass(frozen=True)
class Constants:
    max: Dict[str, int]
    pulses: Dict[str, int]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Constants":
        return Constants(
            max=dict(d.get("max", {})),
            pulses=dict(d.get("pulses", {})),
        )


@dataclass(frozen=True)
class Integrity:
    content_hash: str
    build: BuildInfo

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Integrity":
        if not d:
            return Integrity(content_hash="", build=BuildInfo(source="", tool_version=""))
        return Integrity(
            content_hash=d.get("contentHash", ""),
            build=BuildInfo.from_dict(d.get("build", {})),
        )


@dataclass(frozen=True)
class BuildInfo:
    source: str
    tool_version: str
    extra: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BuildInfo":
        if not d:
            return BuildInfo(source="", tool_version="", extra={})
        extra = {k: v for k, v in d.items() if k not in ("source", "toolVersion")}
        return BuildInfo(
            source=d.get("source", ""),
            tool_version=d.get("toolVersion", ""),
            extra=extra,
        )


def _parse_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

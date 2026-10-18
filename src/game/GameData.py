from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, List


@dataclass(frozen=True)
class GameData:
    id: str
    kind: str
    status: str
    version: Version
    enums: Dict[str, Dict[str, int]]
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
    integrity: Integrity = field(default_factory=lambda: Integrity("", BuildInfo("", "")))
    denyList: List[str] = field(default_factory=list)

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
            enums=dict(doc.get("enums") or {}),
            attribute_bonuses=dict(doc.get("attributeBonuses", doc.get("attribute_bonuses")) or {}),
            classes=dict(doc.get("classes") or {}),
            races=dict(doc.get("races") or {}),
            pc_races=dict(doc.get("pcRaces") or {}),
            wiznet_table=dict(doc.get("wiznetTable", doc.get("wiznet_table")) or {}),
            groups=dict(doc.get("groups") or {}),
            titles=dict(doc.get("titles") or {}),
            item_table=dict(doc.get("itemTable", doc.get("item_table")) or {}),
            weapons=dict(doc.get("weapons") or {}),
            attacks=dict(doc.get("attacks") or {}),
            liquids=dict(doc.get("liquids") or {}),
            integrity=Integrity.from_dict(doc.get("integrity") or {}),
            denyList=list(doc.get("denyList") or []),
        )


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

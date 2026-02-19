from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any


@dataclass(frozen=True)
class GameData:
    id: str
    kind: str
    status: str
    version: Version
    constants: Constants
    enums: Dict[str, List[str]]
    flag_domains: Dict[str, List[str]]
    catalogs: Catalogs
    well_known_vnums: Dict[str, Dict[str, int]]
    integrity: Integrity

    @staticmethod
    def from_mongo(doc: Dict[str, Any]) -> "GameData":
        return GameData(
            id=doc["_id"],
            kind=doc["kind"],
            status=doc.get("status", "active"),
            version=Version.from_dict(doc["version"]),
            constants=Constants.from_dict(doc["constants"]),
            enums=doc["enums"],
            flag_domains=doc["flagDomains"],
            catalogs=Catalogs.from_dict(doc["catalogs"]),
            well_known_vnums=doc.get("wellKnownVnums", {}),
            integrity=Integrity.from_dict(doc["integrity"]),
        )


@dataclass(frozen=True)
class Version:
    family: str
    lineage: List[str]
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
class Catalogs:
    classes: Catalog
    races: Catalog
    pc_races: Catalog
    skills: Catalog
    groups: Catalog
    weapons: Catalog
    attacks: Catalog
    liquids: Catalog

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Catalogs":
        return Catalogs(
            classes=Catalog.from_dict(d["classes"]),
            races=Catalog.from_dict(d["races"]),
            pc_races=Catalog.from_dict(d["pcRaces"]),
            skills=Catalog.from_dict(d["skills"]),
            groups=Catalog.from_dict(d["groups"]),
            weapons=Catalog.from_dict(d["weapons"]),
            attacks=Catalog.from_dict(d["attacks"]),
            liquids=Catalog.from_dict(d["liquids"]),
        )


@dataclass(frozen=True)
class Catalog:
    by_id: Dict[str, Dict[str, Any]]
    by_name: Dict[str, str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Catalog":
        return Catalog(
            by_id=dict(d.get("byId", {})),
            by_name=dict(d.get("byName", {})),
        )

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if key in self.by_id:
            return self.by_id[key]
        resolved = self.by_name.get(key)
        return self.by_id.get(resolved) if resolved else None


@dataclass(frozen=True)
class Integrity:
    content_hash: str
    build: BuildInfo

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Integrity":
        return Integrity(
            content_hash=d["contentHash"],
            build=BuildInfo.from_dict(d["build"]),
        )


@dataclass(frozen=True)
class BuildInfo:
    source: str
    tool_version: str
    extra: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BuildInfo":
        known = {
            "source": d.get("source"),
            "tool_version": d.get("toolVersion"),
        }
        extra = {k: v for k, v in d.items() if k not in ("source", "toolVersion")}
        return BuildInfo(
            source=known["source"],
            tool_version=known["tool_version"],
            extra=extra,
        )


def _parse_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

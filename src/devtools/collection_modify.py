"""Safely modify resources/collections JSON dumps.

Run from the repository root with:
    python -m src.devtools modify <command>
or:
    python -m src.devtools.collection_modify <command>
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .collection_query import (
    Collection,
    default_collections_dir,
    document_id,
    find_one,
    load_collections,
    type_name,
)


MISSING = object()


@dataclass(frozen=True)
class PathTarget:
    parent: Any
    key: str | int
    value: Any
    exists: bool


def parse_path(path: str) -> list[str | int]:
    text = str(path or "").strip()
    if text in {"", "."}:
        return []
    parts: list[str | int] = []
    for raw_part in text.split("."):
        part = raw_part.strip()
        if not part:
            raise ValueError(f"Invalid empty path segment in {path!r}")
        parts.append(int(part) if part.isdigit() else part)
    return parts


def read_path(value: Any, path: str) -> tuple[bool, Any]:
    current = value
    for part in parse_path(path):
        if isinstance(part, int):
            if not isinstance(current, list) or part >= len(current):
                return False, MISSING
            current = current[part]
            continue
        if not isinstance(current, dict) or part not in current:
            return False, MISSING
        current = current[part]
    return True, current


def resolve_target(document: dict[str, Any], path: str, *, create_sections: bool = False) -> PathTarget:
    parts = parse_path(path)
    if not parts:
        raise ValueError("Path must point to a field or section, not the whole document.")

    current: Any = document
    for part in parts[:-1]:
        if isinstance(part, int):
            if not isinstance(current, list):
                raise ValueError(f"Cannot index non-list section at {part!r}.")
            if part >= len(current):
                raise ValueError(f"List index {part} is out of range.")
            current = current[part]
            continue

        if not isinstance(current, dict):
            raise ValueError(f"Cannot descend through non-object section before {part!r}.")
        if part not in current:
            if not create_sections:
                raise ValueError(f"Missing section {part!r}; pass --add-section or use add-section explicitly.")
            current[part] = {}
        if not isinstance(current[part], dict):
            raise ValueError(f"Section {part!r} exists but is not an object.")
        current = current[part]

    key = parts[-1]
    if isinstance(key, int):
        if not isinstance(current, list):
            raise ValueError(f"Cannot index non-list section at final segment {key}.")
        if key >= len(current):
            raise ValueError(f"List index {key} is out of range.")
        return PathTarget(current, key, current[key], True)

    if not isinstance(current, dict):
        raise ValueError(f"Cannot set field {key!r} on non-object section.")
    exists = key in current
    return PathTarget(current, key, current.get(key, MISSING), exists)


def parse_json_value(raw: str, *, json_value: bool) -> Any:
    if json_value:
        return json.loads(raw)
    return raw


def key_style(key: str) -> str:
    text = str(key or "")
    if "_" in text:
        return "snake"
    if text.isupper():
        return "upper"
    if text.islower():
        return "lower"
    if text[:1].islower() and any(ch.isupper() for ch in text):
        return "camel"
    return "mixed"


def validate_key_style(parent: dict[str, Any], key: str, *, ignore: str = "") -> None:
    siblings = [str(item) for item in parent.keys() if str(item) != str(ignore)]
    if len(siblings) < 3:
        return
    styles = [key_style(item) for item in siblings]
    dominant = max(set(styles), key=styles.count)
    if styles.count(dominant) < max(2, len(styles) // 2):
        return
    actual = key_style(key)
    if actual != dominant:
        raise ValueError(f"Key {key!r} uses {actual} style; sibling convention is {dominant}.")


def infer_expected_type(collection: Collection, path: str, current: Any = MISSING) -> str:
    if current is not MISSING:
        return type_name(current)

    counts: dict[str, int] = {}
    for document in collection.documents:
        exists, value = read_path(document, path)
        if not exists:
            continue
        name = type_name(value)
        counts[name] = counts.get(name, 0) + 1
    if counts:
        return max(counts, key=counts.get)
    return ""


def infer_sibling_type(parent: Any) -> str:
    if not isinstance(parent, dict):
        return ""
    counts: dict[str, int] = {}
    for value in parent.values():
        name = type_name(value)
        counts[name] = counts.get(name, 0) + 1
    if counts:
        return max(counts, key=counts.get)
    return ""


def coerce_to_type(value: Any, expected_type: str) -> Any:
    if not expected_type:
        return value
    if expected_type == type_name(value):
        return value
    if expected_type == "str":
        if isinstance(value, (dict, list)):
            raise ValueError("Object/array value does not match expected str convention.")
        return str(value)
    if expected_type == "int":
        if isinstance(value, bool):
            raise ValueError("Boolean value does not match expected int convention.")
        return int(value)
    if expected_type == "float":
        if isinstance(value, bool):
            raise ValueError("Boolean value does not match expected float convention.")
        return float(value)
    if expected_type == "bool":
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text in {"true", "1", "yes", "on"}:
            return True
        if text in {"false", "0", "no", "off"}:
            return False
        raise ValueError(f"Value {value!r} does not match expected bool convention.")
    if expected_type in {"object", "array"}:
        raise ValueError(f"Use --json-value with a JSON {expected_type} value.")
    if expected_type == "null":
        if value in ("", None):
            return None
        raise ValueError(f"Value {value!r} does not match expected null convention.")
    return value


def format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return repr(value)


def write_collection(path: Path, documents: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent, suffix=".tmp") as handle:
        temp_name = handle.name
        json.dump(documents, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    os.replace(temp_name, path)


def load_one(collections_dir: Path, collection_name: str, key: str, lookup_fields: Sequence[str] | None):
    collections = load_collections(collections_dir, [collection_name])
    collection = next(iter(collections.values()))
    document = find_one(collection, key, lookup_fields)
    if document is None:
        raise SystemExit(f"No document found in {collection.name!r} for {key!r}")
    if not isinstance(document, dict):
        raise SystemExit(f"Matched document in {collection.name!r} is not a JSON object.")
    return collection, document


def maybe_write(args: argparse.Namespace, collection: Collection) -> None:
    if args.write:
        write_collection(collection.path, collection.documents)
        print(f"Wrote {collection.path}")
    else:
        print("Dry run only. Pass --write to rewrite the collection file.")


def command_set(args: argparse.Namespace) -> int:
    collection, document = load_one(args.collections_dir, args.collection, args.key, args.lookup_field)
    target = resolve_target(document, args.path, create_sections=args.add_section)
    if not target.exists and not args.add_section:
        raise SystemExit(f"Missing field {args.path!r}; pass --add-section to create it.")
    if not target.exists and isinstance(target.parent, dict):
        validate_key_style(target.parent, str(target.key))

    raw_value = parse_json_value(args.value, json_value=args.json_value)
    expected = infer_expected_type(collection, args.path, target.value if target.exists else MISSING)
    if not expected and not target.exists:
        expected = infer_sibling_type(target.parent)
    if not expected and not args.allow_new_convention:
        raise SystemExit(f"No existing convention found for {args.path!r}; pass --allow-new-convention to set it.")
    value = coerce_to_type(raw_value, expected)

    if args.expect_current is not None:
        if not target.exists:
            raise SystemExit(f"Cannot check --expect-current because {args.path!r} does not exist.")
        expected_current = coerce_to_type(parse_json_value(args.expect_current, json_value=args.json_value), type_name(target.value))
        if target.value != expected_current:
            raise SystemExit(
                f"Current value mismatch for {args.path!r}: expected {format_value(expected_current)}, found {format_value(target.value)}"
            )

    old_text = "(missing)" if not target.exists else format_value(target.value)
    target.parent[target.key] = value
    print(f"{collection.name}:{document_id(document)} {args.path}: {old_text} -> {format_value(value)}")
    maybe_write(args, collection)
    return 0


def command_add_section(args: argparse.Namespace) -> int:
    collection, document = load_one(args.collections_dir, args.collection, args.key, args.lookup_field)
    target = resolve_target(document, args.path, create_sections=False)
    if target.exists:
        raise SystemExit(f"Section {args.path!r} already exists.")
    if not isinstance(target.parent, dict):
        raise SystemExit(f"Parent for {args.path!r} is not an object.")
    validate_key_style(target.parent, str(target.key))
    value = json.loads(args.value) if args.value is not None else {}
    if not isinstance(value, dict):
        raise SystemExit("add-section value must be a JSON object.")
    target.parent[target.key] = value
    print(f"{collection.name}:{document_id(document)} added section {args.path}: {format_value(value)}")
    maybe_write(args, collection)
    return 0


def command_rename_section(args: argparse.Namespace) -> int:
    collection, document = load_one(args.collections_dir, args.collection, args.key, args.lookup_field)
    exists, parent = read_path(document, args.parent_path)
    if not exists:
        raise SystemExit(f"Parent path {args.parent_path!r} does not exist.")
    if not isinstance(parent, dict):
        raise SystemExit(f"Parent path {args.parent_path!r} is not an object.")
    if args.old_name not in parent:
        raise SystemExit(f"Section {args.old_name!r} does not exist under {args.parent_path!r}.")
    if args.new_name in parent:
        raise SystemExit(f"Section {args.new_name!r} already exists under {args.parent_path!r}.")
    validate_key_style(parent, args.new_name, ignore=args.old_name)

    renamed = {}
    for key, value in parent.items():
        renamed[args.new_name if key == args.old_name else key] = value
    parent.clear()
    parent.update(renamed)
    print(f"{collection.name}:{document_id(document)} renamed {args.parent_path}.{args.old_name} -> {args.parent_path}.{args.new_name}")
    maybe_write(args, collection)
    return 0


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("collection", help="Collection name, e.g. skills or SOMDB.Skills.json.")
    parser.add_argument("key", help="Exact document lookup value.")
    parser.add_argument("--lookup-field", action="append", help="Field to match exactly. Repeat for multiple fields.")
    parser.add_argument("--write", action="store_true", help="Rewrite the collection file. Without this, only a dry run is printed.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="collection-modify",
        description="Safely rewrite resources/collections JSON files through validated operations.",
    )
    parser.add_argument(
        "--collections-dir",
        type=Path,
        default=default_collections_dir(),
        help="Directory containing SOMDB.*.json files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set", help="Set an existing field, or create one with --add-section.")
    add_common_arguments(set_parser)
    set_parser.add_argument("path", help="Field path, e.g. payload.toChar.msgOff.")
    set_parser.add_argument("value", help="New value. Use --json-value for objects, arrays, booleans, or null.")
    set_parser.add_argument("--json-value", action="store_true", help="Parse value as JSON instead of a raw string.")
    set_parser.add_argument("--add-section", action="store_true", help="Allow missing object sections or a missing final key to be created.")
    set_parser.add_argument("--allow-new-convention", action="store_true", help="Allow setting a path with no existing type convention.")
    set_parser.add_argument("--expect-current", help="Abort unless the current value matches this value.")
    set_parser.set_defaults(func=command_set)

    add_parser = subparsers.add_parser("add-section", help="Add a new object section at a missing path.")
    add_common_arguments(add_parser)
    add_parser.add_argument("path", help="Missing object section path to add.")
    add_parser.add_argument("--value", help="JSON object to use for the new section. Defaults to {}.")
    add_parser.set_defaults(func=command_add_section)

    rename_parser = subparsers.add_parser("rename-section", help="Rename an existing key under an object section.")
    add_common_arguments(rename_parser)
    rename_parser.add_argument("parent_path", help="Object path containing the section. Use . for the document root.")
    rename_parser.add_argument("old_name", help="Existing subsection key.")
    rename_parser.add_argument("new_name", help="New subsection key.")
    rename_parser.set_defaults(func=command_rename_section)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    sys.exit(main())

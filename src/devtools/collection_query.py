"""Query concise facts from resources/collections JSON dumps.

Run from the repository root with:
    python -m src.devtools <command>
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


DEFAULT_FIELDS = (
    "name",
    "vnum",
    "kind",
    "areaId",
    "handlerId",
    "target",
    "minPosition",
    "itemType",
    "level",
    "shortDescription",
)

LOOKUP_FIELDS = ("name", "vnum", "_id", "id", "handlerId", "command")


@dataclass(frozen=True)
class Collection:
    name: str
    path: Path
    documents: list[Any]


def default_collections_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "resources" / "collections"


def collection_name(path: Path) -> str:
    stem = path.name
    if stem.startswith("SOMDB."):
        stem = stem[len("SOMDB.") :]
    if stem.endswith(".json"):
        stem = stem[: -len(".json")]
    return stem.lower()


def normalize_collection_name(name: str) -> str:
    candidate = Path(name).name
    if candidate.lower().endswith(".json"):
        candidate = candidate[:-5]
    if candidate.startswith("SOMDB."):
        candidate = candidate[len("SOMDB.") :]
    return candidate.lower()


def load_collection(path: Path) -> Collection:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    documents = payload if isinstance(payload, list) else [payload]
    return Collection(collection_name(path), path, documents)


def load_collections(collections_dir: Path, selected: Sequence[str] | None = None) -> dict[str, Collection]:
    wanted = {normalize_collection_name(name) for name in selected or ()}
    collections: dict[str, Collection] = {}
    for path in sorted(collections_dir.glob("*.json")):
        name = collection_name(path)
        if wanted and name not in wanted:
            continue
        collections[name] = load_collection(path)
    missing = sorted(wanted - set(collections))
    if missing:
        available = ", ".join(collection_name(path) for path in sorted(collections_dir.glob("*.json")))
        raise SystemExit(f"Unknown collection(s): {', '.join(missing)}. Available: {available}")
    return collections


def document_id(document: Any) -> str:
    if not isinstance(document, dict):
        return ""
    value = document.get("_id", "")
    if isinstance(value, dict) and "$oid" in value:
        return str(value["$oid"])
    return str(value)


def iter_documents(collections: dict[str, Collection]) -> Iterable[tuple[str, Any]]:
    for name, collection in collections.items():
        for document in collection.documents:
            yield name, document


def get_path(value: Any, path: str) -> Any:
    current = value
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            current = current[index] if index < len(current) else None
        else:
            return None
    return current


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "float"
    return "str"


def scalar_text(value: Any, max_len: int = 80) -> str:
    if value is None:
        text = ""
    elif isinstance(value, bool):
        text = "true" if value else "false"
    elif isinstance(value, (int, float, str)):
        text = str(value).replace("\r", " ").replace("\n", "\\n")
    elif isinstance(value, list):
        text = f"[{len(value)}]"
    elif isinstance(value, dict):
        text = f"{{{len(value)}}}"
    else:
        text = str(value)
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text


def field_names(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return []
    return list(document.keys())


def default_display_fields(documents: Sequence[Any], requested: Sequence[str] | None = None) -> list[str]:
    if requested:
        return list(requested)
    seen = {field for document in documents for field in field_names(document)}
    fields = [field for field in DEFAULT_FIELDS if field in seen]
    if not fields:
        fields = sorted(seen)[:8]
    return fields[:10]


def format_table(rows: Sequence[dict[str, Any]], fields: Sequence[str]) -> str:
    if not rows:
        return "(no rows)"
    rendered = [
        {field: scalar_text(row.get(field), 120) for field in fields}
        for row in rows
    ]
    widths = {
        field: max(len(field), *(len(row[field]) for row in rendered))
        for field in fields
    }
    lines = ["  ".join(field.ljust(widths[field]) for field in fields)]
    lines.append("  ".join("-" * widths[field] for field in fields))
    lines.extend("  ".join(row[field].ljust(widths[field]) for field in fields) for row in rendered)
    return "\n".join(lines)


def compact_document(document: Any, fields: Sequence[str] | None = None) -> dict[str, Any]:
    if not isinstance(document, dict):
        return {"value": document}
    selected = default_display_fields([document], fields)
    row = {field: get_path(document, field) for field in selected}
    if "_id" in document and "_id" not in row:
        row["_id"] = document_id(document)
    return row


def document_matches(document: Any, term: str, fields: Sequence[str] | None = None, exact: bool = False) -> bool:
    if not isinstance(document, dict):
        text = scalar_text(document, 10_000).lower()
        needle = term.lower()
        return text == needle if exact else needle in text

    field_list = fields or field_names(document)
    needle = term.lower()
    for field in field_list:
        value = get_path(document, field)
        if isinstance(value, (dict, list)):
            haystack = json.dumps(value, ensure_ascii=False, sort_keys=True).lower()
        else:
            haystack = scalar_text(value, 10_000).lower()
        if exact:
            if haystack == needle:
                return True
        elif needle in haystack:
            return True
    return False


def find_one(collection: Collection, key: str, fields: Sequence[str] | None = None) -> Any | None:
    lookup_fields = tuple(fields or LOOKUP_FIELDS)
    for document in collection.documents:
        if document_matches(document, key, lookup_fields, exact=True):
            return document
    needle = key.lower()
    for document in collection.documents:
        if not isinstance(document, dict):
            continue
        if document_id(document).lower() == needle:
            return document
    return None


def command_list(args: argparse.Namespace) -> int:
    collections = load_collections(args.collections_dir)
    rows: list[dict[str, Any]] = []
    for name, collection in collections.items():
        rows.append(
            {
                "collection": name,
                "documents": len(collection.documents),
                "file": collection.path.name,
            }
        )
    print(format_table(rows, ("collection", "documents", "file")))
    return 0


def command_summary(args: argparse.Namespace) -> int:
    collections = load_collections(args.collections_dir, args.collection)
    rows: list[dict[str, Any]] = []
    for name, collection in collections.items():
        all_fields = Counter()
        for document in collection.documents:
            if not isinstance(document, dict):
                continue
            for field in document:
                all_fields[field] += 1
        fields = ", ".join(field for field, _count in all_fields.most_common(args.limit))
        rows.append(
            {
                "collection": name,
                "documents": len(collection.documents),
                "fields": len(all_fields),
                "top_fields": fields,
            }
        )
    print(format_table(rows, ("collection", "documents", "fields", "top_fields")))
    return 0


def command_fields(args: argparse.Namespace) -> int:
    collections = load_collections(args.collections_dir, [args.collection])
    collection = next(iter(collections.values()))
    counts = Counter()
    types_by_field: dict[str, Counter[str]] = {}
    for document in collection.documents:
        if not isinstance(document, dict):
            continue
        for field, value in document.items():
            counts[field] += 1
            types_by_field.setdefault(field, Counter())[type_name(value)] += 1
    rows = []
    for field, count in counts.most_common():
        types = ",".join(t for t, _count in types_by_field[field].most_common())
        rows.append({"field": field, "count": count, "types": types})
    print(format_table(rows, ("field", "count", "types")))
    return 0


def command_find(args: argparse.Namespace) -> int:
    collections = load_collections(args.collections_dir, args.collection)
    matches: list[dict[str, Any]] = []
    for collection_name_, document in iter_documents(collections):
        if not document_matches(document, args.term, args.search_field, args.exact):
            continue
        row = {"collection": collection_name_}
        row.update(compact_document(document, args.field))
        matches.append(row)
        if len(matches) >= args.limit:
            break
    fields = ["collection"] + [field for field in default_display_fields(matches, args.field) if field != "collection"]
    print(format_table(matches, fields))
    return 0


def command_get(args: argparse.Namespace) -> int:
    collections = load_collections(args.collections_dir, [args.collection])
    collection = next(iter(collections.values()))
    document = find_one(collection, args.key, args.lookup_field)
    if document is None:
        raise SystemExit(f"No document found in {collection.name!r} for {args.key!r}")
    if args.json:
        print(json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        compact = compact_document(document, args.field)
        fields = list(compact)
        print(format_table([compact], fields))
    return 0


def command_values(args: argparse.Namespace) -> int:
    collections = load_collections(args.collections_dir, [args.collection])
    collection = next(iter(collections.values()))
    counts: Counter[str] = Counter()
    for document in collection.documents:
        value = get_path(document, args.field)
        if isinstance(value, list):
            if not value:
                counts["[]"] += 1
            for item in value:
                counts[scalar_text(item, 120)] += 1
        else:
            counts[scalar_text(value, 120)] += 1
    rows = [
        {"value": value, "count": count}
        for value, count in counts.most_common(args.limit)
    ]
    print(format_table(rows, ("value", "count")))
    return 0


def command_path(args: argparse.Namespace) -> int:
    collections = load_collections(args.collections_dir, [args.collection])
    collection = next(iter(collections.values()))
    document = find_one(collection, args.key, args.lookup_field)
    if document is None:
        raise SystemExit(f"No document found in {collection.name!r} for {args.key!r}")
    value = get_path(document, args.path)
    if isinstance(value, (dict, list)):
        print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(scalar_text(value, 10_000))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="collection-query",
        description="Query concise facts from resources/collections JSON files.",
    )
    parser.add_argument(
        "--collections-dir",
        type=Path,
        default=default_collections_dir(),
        help="Directory containing SOMDB.*.json files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List available collections.")
    list_parser.set_defaults(func=command_list)

    summary_parser = subparsers.add_parser("summary", help="Summarize collections and their top fields.")
    summary_parser.add_argument("collection", nargs="*", help="Optional collection names.")
    summary_parser.add_argument("--limit", type=int, default=12, help="Number of top fields to show.")
    summary_parser.set_defaults(func=command_summary)

    fields_parser = subparsers.add_parser("fields", help="Show field names, counts, and observed JSON types.")
    fields_parser.add_argument("collection", help="Collection name, e.g. skills or SOMDB.Skills.json.")
    fields_parser.set_defaults(func=command_fields)

    find_parser = subparsers.add_parser("find", help="Search documents and print concise matching rows.")
    find_parser.add_argument("term", help="Text to search for.")
    find_parser.add_argument("collection", nargs="*", help="Optional collection names.")
    find_parser.add_argument("--field", action="append", help="Field to print. Repeat for multiple fields.")
    find_parser.add_argument("--search-field", action="append", help="Field to search. Repeat for multiple fields.")
    find_parser.add_argument("--exact", action="store_true", help="Require an exact field match.")
    find_parser.add_argument("--limit", type=int, default=20, help="Maximum rows to print.")
    find_parser.set_defaults(func=command_find)

    get_parser = subparsers.add_parser("get", help="Fetch one document by name, vnum, id, or another lookup field.")
    get_parser.add_argument("collection", help="Collection name.")
    get_parser.add_argument("key", help="Exact lookup value.")
    get_parser.add_argument("--field", action="append", help="Field to print. Repeat for multiple fields.")
    get_parser.add_argument("--lookup-field", action="append", help="Field to match exactly. Repeat for multiple fields.")
    get_parser.add_argument("--json", action="store_true", help="Print the full matching document as JSON.")
    get_parser.set_defaults(func=command_get)

    values_parser = subparsers.add_parser("values", help="Count distinct values for a field.")
    values_parser.add_argument("collection", help="Collection name.")
    values_parser.add_argument("field", help="Field path, e.g. kind or levelByClass.mage.")
    values_parser.add_argument("--limit", type=int, default=30, help="Maximum values to print.")
    values_parser.set_defaults(func=command_values)

    path_parser = subparsers.add_parser("path", help="Print one field path from one matching document.")
    path_parser.add_argument("collection", help="Collection name.")
    path_parser.add_argument("key", help="Exact lookup value.")
    path_parser.add_argument("path", help="Field path, e.g. payload.toChar.msgOff.")
    path_parser.add_argument("--lookup-field", action="append", help="Field to match exactly. Repeat for multiple fields.")
    path_parser.set_defaults(func=command_path)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

"""Import missing ROM #HELPS records, preserving authored documents and aliases.

Run with --area-dir PATH; dry-run is the default. Existing exact keyword records
are never rewritten, including intentional topic disambiguation.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import shlex

from .collection_query import load_collections
from .collection_modify import write_collection


def parse_helps(text):
    section = re.search(r'^#HELPS\s*', text, re.MULTILINE)
    if section is None:
        return []
    position = section.end()
    records = []
    while True:
        header = re.match(r'\s*(-?\d+)\s+([^~]*)~', text[position:])
        if header is None:
            raise ValueError(f'Invalid help header at offset {position}')
        level, keyword = header.groups()
        keyword = keyword.strip()
        position += header.end()
        if keyword.startswith('$'):
            return records
        end = text.find('~', position)
        if end < 0:
            raise ValueError(f'Unterminated help text: {keyword}')
        records.append({'keyword': keyword, 'level': int(level),
                        'text': text[position:end].lstrip().rstrip()})
        position = end + 1


def topic_names(keyword, ability_names=()):
    phrase = ' '.join(keyword.split()).casefold()
    # ROM's unquoted MASS HEALING header names one spell, not the HEALING group.
    if phrase in ability_names:
        return [phrase]
    return list(dict.fromkeys(' '.join(alias.split()).casefold() for alias in shlex.split(keyword)))


def plan_import(existing, sources, ability_names=()):
    result = deepcopy(existing)
    keywords = {doc['keyword'].casefold() for doc in existing}
    claimed = {topic.casefold() for doc in existing for topic in doc.get('topics', topic_names(doc['keyword']))}
    additions = []
    for source, records in sources:
        for record in records:
            if record['keyword'].casefold() in keywords:
                continue
            topics = [topic for topic in topic_names(record['keyword'], ability_names) if topic not in claimed]
            if not topics:
                continue
            identity = hashlib.sha256(('rom24-help:' + source + ':' + record['keyword']).encode()).hexdigest()[:24]
            document = {'_class': 'org.springy.som.modulith.domain.command.internal.HelpDocument',
                        '_id': {'$oid': identity}, **record, 'topics': topics}
            result.append(document)
            additions.append({'source': source, 'keyword': record['keyword'], 'topics': topics})
            keywords.add(record['keyword'].casefold())
            claimed.update(topics)
    ids = [doc['_id']['$oid'] for doc in result]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate help document IDs')
    return result, additions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--area-dir', type=Path, required=True)
    parser.add_argument('--collections-dir', type=Path, default=Path('resources/collections'))
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--in-place', action='store_true',
                        help='Use direct writing when Windows denies atomic replacement (requires --write).')
    args = parser.parse_args()
    collections = load_collections(args.collections_dir, ['helps', 'skills', 'spells'])
    existing = collections['helps'].documents
    abilities = {doc['name'].casefold() for name in ('skills', 'spells') for doc in collections[name].documents}
    # Follow the reference boot order, rather than arbitrary directory order.
    area_names = args.area_dir.joinpath('area.lst').read_text().split()
    sources = [(name, parse_helps(args.area_dir.joinpath(name).read_text(encoding='latin-1')))
               for name in area_names if name != '$']
    result, additions = plan_import(existing, sources, abilities)
    print(json.dumps({'before': len(existing), 'after': len(result), 'additions': additions}, indent=2))
    if args.write and additions:
        path = collections['helps'].path
        if json.loads(path.read_text(encoding='utf-8')) != existing:
            raise ValueError('Help collection changed during import planning')
        if args.in_place:
            original_text = path.read_text(encoding='utf-8')
            prefix = original_text[:original_text.rfind(']')].rstrip()
            appended = ',\n'.join(json.dumps(doc, indent=2, ensure_ascii=False)
                                   for doc in result[len(existing):])
            output = prefix + (',\n' if existing else '\n') + appended + ']\n'
            if json.loads(output) != result:
                raise ValueError('Append serialization failed verification')
            path.write_text(output, encoding='utf-8', newline='\n')
            if json.loads(path.read_text(encoding='utf-8')) != result:
                raise ValueError('Written help collection failed verification')
        else:
            write_collection(path, result)


if __name__ == '__main__':
    main()

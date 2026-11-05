"""Validate report references and snapshot integrity, without executing gameplay."""
import hashlib
import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
manifest = json.loads((OUT / 'manifest.json').read_text(encoding='utf8'))
cases = json.loads((OUT / 'cases.json').read_text(encoding='utf8'))['cases']
source = Path(manifest['scope']['source_root'])
files = manifest['inventory']
functions = [fn for f in files for fn in f['functions']]
ledger = [b for fn in functions for b in fn['branch_ledger']]
assert len({b['id'] for b in ledger}) == len(ledger)
assert len({c['id'] for c in cases}) == len(cases)
case_map = {c['id']: c for c in cases}
branch_map = {b['id']: b for b in ledger}
function_map = {(fn['file'], fn['name']): fn for fn in functions}
for case in cases:
    assert len(case['branch_ids']) == len(set(case['branch_ids'])), case['id']
    for bid in case['branch_ids']:
        assert case['id'] in branch_map[bid]['case_ids']
    for reference in case['source_refs']:
        function = function_map[reference['file'], reference['function']]
        assert function['line'] <= reference['line'] <= function['end_line'], reference
    if case['status'] == 'blocked':
        assert case['open_questions'], case['id']
for branch in ledger:
    for cid in branch['case_ids']:
        assert branch['id'] in case_map[cid]['branch_ids']
    assert branch['disposition'] != 'specified' or branch['case_ids'], branch['id']
for file in files + manifest['ancillary_inventory']:
    assert hashlib.sha256((source / file['path']).read_bytes()).hexdigest() == file['sha256'], file['path']
checked_links = 0
for md in OUT.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)', md.read_text(encoding='utf8')):
        if link.startswith(('http:', 'https:', '#')):
            continue
        match = re.match(r'^(.*?):(\d+)$', link)
        target = Path(match[1] if match else link)
        if not target.is_absolute():
            target = md.parent / target
        assert target.is_file(), (str(md), link)
        if match:
            assert 1 <= int(match[2]) <= len(target.read_text(encoding='latin1').splitlines()), link
        checked_links += 1
assert manifest['counts']['functions_inventoried'] == len(functions)
reviewed = [fn for fn in functions if 'local_ledger_review' in fn]
assert manifest['counts']['additional_local_ledgers_reconciled'] == len(reviewed)
for function in reviewed:
    assert function['status'] == 'partially_specified', function['name']
    assert all(b['disposition'] != 'pending' for b in function['branch_ledger']), function['name']
assert manifest['counts']['cases_specified'] == sum(c['status'] == 'specified' for c in cases)
assert manifest['counts']['cases_blocked'] == sum(c['status'] == 'blocked' for c in cases)
assert manifest['counts']['cases_dynamically_verified'] == 0
assert manifest['status'] == 'partial'
result = {'result': 'passed', 'command': [sys.executable, str(Path(__file__).resolve())],
                  'checks': 'JSON integrity, unique branch links, bidirectional references, blocked reasons, all snapshot hashes, Markdown links and function-scoped citation bounds, count consistency, local ledger reconciliation without promoting function status, truthful partial status',
                  'source_and_supporting_files_hashed': len(files) + len(manifest['ancillary_inventory']),
                  'functions_inventoried': len(functions), 'cases': len(cases), 'markdown_links_checked': checked_links,
                  'gameplay_tests_run': 0}
(OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8')
print(json.dumps(result, indent=2))

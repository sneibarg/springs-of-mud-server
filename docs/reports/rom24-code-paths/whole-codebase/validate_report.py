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
from spec_name_completion import NAMES, check_source
check_source(source)
completed = function_map['src/special.c', 'spec_name']
assert completed['status'] == 'traced'
assert completed['completion_review']['remaining_gaps'] == []
selected = [c for c in cases if c['id'].startswith('special.spec_name.')]
assert len(selected) == 24
assert {c['fixture']['arguments']['function'] for c in selected} == set(NAMES) | {'C NULL', 'unregistered_valid_function_pointer'}
for case in selected:
    pointer = case['fixture']['arguments']['function']
    k = NAMES.index(pointer) if pointer in NAMES else None
    assert case['status'] == 'specified' and not case['open_questions']
    assert case['expected']['returned_name'] == ('C NULL' if k is None else NAMES[k])
    assert case['expected']['equality_comparisons_in_order'] == list(range(22 if k is None else k + 1))
    assert case['expected']['loop_guard_indices_in_order'] == list(range(23 if k is None else k + 1))
    assert case['expected']['sentinel_function_compared_to_argument'] is False
assert all(b['disposition'] == 'specified' for b in completed['branch_ledger'])
from spec_lookup_completion import validate_cases as validate_lookup_cases
lookup_case_count = validate_lookup_cases(cases)
lookup = function_map['src/special.c', 'spec_lookup']
assert lookup['status'] == 'traced'
assert lookup['completion_review']['remaining_gaps'] == []
assert lookup['completion_review']['case_count'] == lookup_case_count
assert all(b['disposition'] == 'specified' for b in lookup['branch_ledger'])
from same_clan_completion import validate_cases as validate_clan_cases, check_source as check_clan_source
check_clan_source(source)
clan_case_count = validate_clan_cases(cases)
clan = function_map['src/handler.c', 'is_same_clan']
assert clan['status'] == 'traced' and clan['completion_review']['remaining_gaps'] == []
assert clan['completion_review']['case_count'] == clan_case_count
assert all(b['disposition'] == 'specified' for b in clan['branch_ledger'])
from darkness_completion import validate_cases as validate_darkness_cases, check_source as check_darkness_source
check_darkness_source(source)
darkness_case_count = validate_darkness_cases(cases)
darkness = function_map['src/handler.c', 'room_is_dark']
assert darkness['status'] == 'traced' and darkness['completion_review']['remaining_gaps'] == []
assert darkness['completion_review']['case_count'] == darkness_case_count
assert all(b['disposition'] == 'specified' for b in darkness['branch_ledger'])
assert manifest['counts']['functions_completely_traced'] == sum(f['status'] == 'traced' for f in functions)
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
                  'completed_spec_name_cases_checked': len(selected),
                  'completed_spec_lookup_cases_checked': lookup_case_count,
                  'completed_is_same_clan_cases_checked': clan_case_count,
                  'completed_room_is_dark_cases_checked': darkness_case_count, 'gameplay_tests_run': 0}
(OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8')
print(json.dumps(result, indent=2))

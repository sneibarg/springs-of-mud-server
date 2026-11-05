"""Reproducible static inventory and source-grounded case catalog renderer.

This is report tooling, not a C parser, gameplay implementation, or test runner.
Run from any directory with Python 3. No third-party dependencies.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
TARGET = OUT.parents[3]
SOURCE = TARGET.parent / 'PyRom' / 'Rom24'


def mask(text):
    # Keep offsets and newlines exact while hiding comments and literals.
    pattern = r'/\*[\s\S]*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    return re.sub(pattern, lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), text)


def line(text, offset):
    return text.count('\n', 0, offset) + 1


def balanced_end(text, start, opening='(', closing=')'):
    depth = 0
    for pos in range(start, len(text)):
        if text[pos] == opening:
            depth += 1
        elif text[pos] == closing:
            depth -= 1
            if depth == 0:
                return pos
    raise ValueError(f'Unbalanced {opening} at {start}')


def ref(file, function, ln):
    return {'repository': 'ROM24', 'file': file, 'function': function, 'line': ln}


def inventory():
    files, funcs = [], []
    texts = {}
    for path in sorted((SOURCE / 'src').iterdir()):
        if not path.is_file():
            continue
        rel = path.relative_to(SOURCE).as_posix()
        text = path.read_text(encoding='latin1')
        clean = mask(text)
        texts[rel] = (text, clean)
        role = 'translation_unit' if path.suffix == '.c' else 'header' if path.suffix == '.h' else 'build_configuration'
        f = {'path': rel, 'role': role, 'status': 'pending', 'lines': len(text.splitlines()),
             'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'functions': [],
             'preprocessor_directives': [], 'macros': [], 'static_tables': []}
        for m in re.finditer(r'^[ \t]*#[ \t]*(if|ifdef|ifndef|elif|else|endif|define|undef|include)\b(?:[^\n]*\\\n)*[^\n]*', text, re.M):
            row = {'line': line(text, m.start()), 'text': m[0].strip(), 'status': 'pending'}
            f['preprocessor_directives'].append(row)
            if m[1] == 'define':
                f['macros'].append(row)
        f['commented_code_candidates'] = []
        for m in re.finditer(r'/\*[\s\S]*?\*/', text):
            if re.search(r'\b(?:if|while|for)\s*\(|\breturn\s+[^;]+;', m[0]):
                f['commented_code_candidates'].append({'line': line(text, m.start()),
                    'end_line': line(text, m.end()), 'disposition': 'disabled',
                    'reason': 'Inside C block comment; code-like text is not executable in this source snapshot.',
                    'sha256': hashlib.sha256(m[0].encode('latin1')).hexdigest()})
        for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\[[^;{}]*?\]\s*=\s*\{', clean):
            opening = clean.index('{', m.start(), m.end())
            closing = balanced_end(clean, opening, '{', '}')
            f['static_tables'].append({'name': m[1], 'line': line(text, m.start()),
                'end_line': line(text, closing), 'status': 'pending',
                'function_references': [], 'entry_inventory': []})
        if path.suffix == '.c':
            depths, depth = [], 0
            for c in clean:
                depths.append(depth)
                depth += (c == '{') - (c == '}')
            for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\(', clean):
                if depths[m.start()] != 0 or m[1] in {'if', 'for', 'while', 'switch'}:
                    continue
                par = clean.index('(', m.start(), m.end())
                close = balanced_end(clean, par)
                start = close + 1
                while start < len(clean) and clean[start].isspace():
                    start += 1
                if start >= len(clean) or clean[start] != '{':
                    continue
                end = balanced_end(clean, start, '{', '}')
                name = m[1]
                fn = {'name': name, 'file': rel, 'line': line(text, m.start()), 'end_line': line(text, end),
                      'status': 'pending', 'entry_routes': [], 'dependencies': [], 'branch_ledger': [],
                      'inventory_method': 'comment/literal-masked lexical function-definition scan; not compiler verified'}
                body = clean[start:end+1]
                offsets = collections.Counter()
                # Explicit syntactic sites only. Implicit behavioral branches require manual tracing.
                for b in re.finditer(r'\b(if|for|while|switch|case|default|return|break|continue|goto)\b|&&|\|\||\?', body):
                    kind = b[0]
                    pos = start + b.start()
                    offsets[kind] += 1
                    if kind in {'if', 'for', 'while', 'switch'}:
                        par = clean.find('(', pos)
                        stop = balanced_end(clean, par) + 1
                    else:
                        stops = [x for x in (clean.find('\n', pos), clean.find(';', pos)) if x >= 0]
                        stop = min(stops) + 1 if stops else pos + len(kind)
                    token = {'&&': 'and', '||': 'or', '?': 'ternary'}.get(kind, kind)
                    fn['branch_ledger'].append({'id': f'{path.stem}.{name}.{token}.{offsets[kind]:03}',
                        'source_ref': ref(rel, name, line(text, pos)), 'kind': kind,
                        'predicate_or_transfer': text[pos:stop].strip(), 'disposition': 'pending',
                        'case_ids': [], 'gap': 'Lexically indexed; feasible outcomes, ordering, implicit paths, and caller contracts require semantic tracing.'})
                if not fn['branch_ledger']:
                    fn['branch_ledger'].append({'id': f'{path.stem}.{name}.entry', 'source_ref': ref(rel, name, fn['line']),
                        'kind': 'entry', 'predicate_or_transfer': 'Straight-line entry', 'disposition': 'pending', 'case_ids': [],
                        'gap': 'Observable helper contracts and side effects require semantic tracing.'})
                fn['_start'], fn['_end'] = start, end
                funcs.append(fn)
                f['functions'].append(fn)
        files.append(f)
    names = {f['name'] for f in funcs}
    for file in files:
        text, clean = texts[file['path']]
        lines = text.splitlines()
        for table in file['static_tables']:
            table['function_references'] = sorted(set(re.findall(r'\b[A-Za-z_]\w*\b',
                '\n'.join(lines[table['line']-1:table['end_line']]))) & names)
            if table['function_references']:
                # Rows are locators, not preprocessor-resolved dispatch behavior.
                table['entry_inventory'] = [{'line': n + 1, 'text': lines[n].strip(), 'status': 'pending'}
                    for n in range(table['line'] - 1, table['end_line'])
                    if any(re.search(r'\b' + re.escape(name) + r'\b', lines[n]) for name in table['function_references'])]
    by_name = collections.defaultdict(list)
    for fn in funcs:
        by_name[fn['name']].append(fn)
    for fn in funcs:
        text, clean = texts[fn['file']]
        body = clean[fn['_start']:fn['_end']+1]
        seen = set()
        for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\(', body):
            name = m[1]
            if name in {'if', 'for', 'while', 'switch', 'sizeof'}:
                continue
            if name not in seen:
                fn['dependencies'].append({'name': name, 'kind': 'local_function' if name in names else 'macro_external_or_indirect', 'status': 'pending'})
                seen.add(name)
            for callee in by_name.get(name, []):
                callee['entry_routes'].append({'kind': 'lexical_call_candidate', 'caller': fn['name'],
                    'file': fn['file'], 'line': line(text, fn['_start'] + m.start()), 'reachability': 'pending'})
        for m in re.finditer(r'\b([A-Za-z_]\w*)\b(?!\s*\()', body):
            if m[1] not in names:
                continue
            for callee in by_name[m[1]]:
                callee['entry_routes'].append({'kind': 'function_symbol_reference_candidate', 'caller': fn['name'],
                    'file': fn['file'], 'line': line(text, fn['_start'] + m.start()),
                    'reachability': 'pending; callback/address-taking candidate, not proof of invocation'})
        fn['indirect_call_sites'] = [{'line': line(text, fn['_start'] + m.start()),
            'expression': text[fn['_start'] + m.start():fn['_start'] + m.end()], 'status': 'pending'}
            for m in re.finditer(r'\(\s*\*[^()\n]+\)\s*\(', body)]
    # Include table references, address-taking, and symbols passed without parentheses.
    for rel, (text, clean) in texts.items():
        for m in re.finditer(r'\b[A-Za-z_]\w*\b', clean):
            name = m[0]
            if name not in names:
                continue
            ln = line(text, m.start())
            if any(f['file'] == rel and f['line'] <= ln <= f['end_line'] for f in funcs):
                continue
            for callee in by_name[name]:
                callee['entry_routes'].append({'kind': 'declaration_or_dispatch_reference', 'file': rel, 'line': ln,
                    'reachability': 'pending; may be prototype, dispatch-table entry, or conditional definition'})
    for fn in funcs:
        del fn['_start'], fn['_end']
    return files, funcs


def main():
    files, funcs = inventory()
    cases = json.loads((OUT / 'cases.json').read_text(encoding='utf8'))['cases']
    ledger = {b['id']: b for f in funcs for b in f['branch_ledger']}
    assert len(ledger) == sum(len(f['branch_ledger']) for f in funcs), 'Duplicate lexical ledger IDs'
    # Semantic case links supplement the raw syntax inventory; no blanket coverage claims.
    by_key = {(f['file'], f['name']): f for f in funcs}
    for case in cases:
        fn = by_key[(case['source_refs'][0]['file'], case['source_refs'][0]['function'])]
        for bid in case['branch_ids']:
            if bid not in ledger:
                assert bid == case['id'] + '.path', bid
                branch = {'id': bid, 'source_ref': case['source_refs'][0], 'kind': 'semantic_path',
                          'predicate_or_transfer': case['title'], 'disposition': case['status'], 'case_ids': []}
                fn['branch_ledger'].append(branch)
                ledger[bid] = branch
            branch = ledger[bid]
            assert branch in fn['branch_ledger'], bid
            branch['case_ids'].append(case['id'])
            if case['status'] == 'specified':
                branch['disposition'] = 'specified'
        fn['status'] = 'partially_specified'
    for f in files:
        if f['path'] == 'src/lookup.c':
            # The direct helper contracts cover all lookup loops, both guard
            # operands and both returns. Caller behavior lives in its own files.
            for fn in f['functions']:
                assert all(b['disposition'] == 'specified' for b in fn['branch_ledger']), fn['name']
                fn['status'] = 'traced'
            f['status'] = 'lookup_contracts_traced'
        if any(fn['status'] == 'partially_specified' for fn in f['functions']):
            f['status'] = 'partially_specified'
    circular_return = ledger['act_enter.do_enter.return.007']
    assert not circular_return['case_ids']
    circular_return['disposition'] = 'unreachable'
    circular_return['disposition_note'] = (
        'Line 114 rejects equality of the same two local room pointers before movement. '
        'Neither local is reassigned or passed by address before line 162.'
    )
    # A reconciled local ledger is not an end-to-end caller/dependency trace.
    reconciled = {
        'src/db.c': {'number_fuzzy', 'number_range', 'number_percent', 'number_door',
                     'number_bits', 'dice', 'interpolate', 'smash_tilde', 'str_cmp',
                     'str_prefix', 'str_infix', 'str_suffix', 'capitalize'},
        'src/handler.c': {'is_clan', 'is_same_clan', 'get_trust', 'deduct_cost',
                          'room_is_dark', 'room_is_private', 'can_drop_obj'},
        'src/interp.c': {'one_argument'},
        'src/magic.c': {'saves_spell', 'saves_dispel'},
        'src/special.c': {'spec_lookup', 'spec_name'},
    }
    for fn in funcs:
        if fn['name'] in reconciled.get(fn['file'], set()):
            assert all(b['disposition'] != 'pending' for b in fn['branch_ledger']), fn['name']
            fn['local_ledger_review'] = {
                'status': 'reconciled',
                'criterion': 'Concrete cases linked to every indexed local control site; bounded loop classes and direct-helper input domains. Not executable coverage or a claim that every outcome of every expression has been established.',
                'remaining': 'Caller reachability, unexpanded collaborator internals, platform alternatives and invalid-input policies remain distinct from the local cases. See tracing-notes.md.',
            }
    from spec_name_completion import complete
    complete(funcs, cases, SOURCE)
    git_head = SOURCE.parent / '.git/HEAD'
    head_text = git_head.read_text().strip() if git_head.exists() else 'unknown'
    git_ref = SOURCE.parent / '.git' / head_text[5:] if head_text.startswith('ref: ') else None
    revision = git_ref.read_text().strip() if git_ref and git_ref.exists() else head_text
    comparison = {'status': 'unavailable'}
    try:
        tree = subprocess.run(['git', '--git-dir=' + str(SOURCE.parent / '.git'), 'ls-tree', '-r', 'HEAD', '--', 'Rom24'],
                              capture_output=True, check=True).stdout.decode('utf8')
        tracked = {row.split('\t', 1)[1][6:]: row.split()[2] for row in tree.splitlines() if '\t' in row}
        changed, untracked, missing = [], [], []
        for rel, oid in tracked.items():
            path = SOURCE / rel
            if not path.is_file():
                missing.append(rel)
                continue
            raw = path.read_bytes()
            variants = [raw, raw.replace(b'\r\n', b'\n')]
            hashes = [hashlib.sha1(b'blob ' + str(len(v)).encode() + b'\0' + v).hexdigest() for v in variants]
            if oid not in hashes:
                changed.append(rel)
        for p in SOURCE.rglob('*'):
            if p.is_file() and p.relative_to(SOURCE).as_posix() not in tracked:
                untracked.append(p.relative_to(SOURCE).as_posix())
        comparison = {'status': 'git_blob_content_comparison', 'command': 'git --git-dir=<PyRom>/.git ls-tree -r HEAD -- Rom24',
            'method': 'Compare raw and CRLF-to-LF normalized Git blob SHA-1 against HEAD tree. Does not inspect staging or file-mode status.',
            'changed_content': changed, 'untracked_files': untracked, 'missing_tracked_files': missing}
    except (OSError, subprocess.CalledProcessError) as exc:
        comparison['error'] = str(exc)
    ancillary = []
    for path in sorted(SOURCE.rglob('*')):
        if not path.is_file() or 'src' in path.relative_to(SOURCE).parts[:1]:
            continue
        ancillary.append({'path': path.relative_to(SOURCE).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'role': 'loaded_data_candidate' if path.relative_to(SOURCE).parts[0] in {'area', 'data'} else 'documentation_or_alternative_implementation',
            'status': 'pending', 'disposition_note': 'Inventory only; load reachability and behavior not yet traced.'})
    area_list = SOURCE / 'area/area.lst'
    boot_files = []
    if area_list.exists():
        for n, word in enumerate(area_list.read_text(encoding='latin1').splitlines(), 1):
            word = word.strip()
            if word.startswith('$'):
                break
            if not word:
                continue
            path = SOURCE / 'area' / word
            sections = []
            if path.is_file():
                sections = [{'line': ln + 1, 'section': row.strip(), 'disposition': 'pending'}
                    for ln, row in enumerate(path.read_text(encoding='latin1').splitlines())
                    if re.match(r'^#[A-Za-z$]', row)]
            boot_files.append({'list_line': n, 'path': 'area/' + word, 'present': path.is_file(),
                'sections': sections, 'disposition': 'pending',
                'assumption': 'Process current directory is area; AREA_LIST and filenames are opened relative to process CWD. See db.c boot_db.'})
    counts = {'source_files': len(files), 'translation_units': sum(f['role'] == 'translation_unit' for f in files),
        'source_lines': sum(f['lines'] for f in files), 'functions_inventoried': len(funcs),
        'functions_with_cases': sum(f['status'] in {'partially_specified', 'traced'} for f in funcs),
        'functions_completely_traced': sum(f['status'] == 'traced' for f in funcs),
        'additional_local_ledgers_reconciled': sum('local_ledger_review' in f for f in funcs),
        'cases_specified': sum(c['status'] == 'specified' for c in cases), 'cases_blocked': sum(c['status'] == 'blocked' for c in cases),
        'cases_dynamically_verified': 0, 'lexical_sites_pending': sum(b['disposition'] == 'pending' for b in ledger.values()),
        'ancillary_files_inventoried': len(ancillary)}
    manifest = {'schema_version': 1, 'status': 'partial', 'scope': {'requested': 'Entire ROM2.4 C codebase and execution-affecting data',
        'source_root': str(SOURCE), 'target_root': str(TARGET), 'requested_exclusions': [],
        'inventory_limitations': 'Lexical scan, not preprocessed/compiler AST; disabled definitions retained; function pointers/macros and implicit branches require manual resolution.'},
        'snapshot': {'revision': revision, 'revision_evidence': 'Read .git/HEAD and refs/heads/master; git work-tree commands fail in this environment.',
            'dirty_status': 'Normal git status unavailable. HEAD content comparison is recorded separately; staging and mode status unknown. Per-file SHA-256 identifies actual bytes.',
            'head_content_comparison': comparison,
            'sha256': {f['path']: f['sha256'] for f in files},
            'build_assumptions': ['No C build or gameplay probe performed.', 'Default Makefile: gcc -Wall -O -g, crypt linkage; Linux/normal/Solaris variants retained.',
                'Preprocessor alternatives including macintosh, MSDOS, unix and NOCRYPT are not resolved by the lexical inventory.',
                'Specified ASCII string cases assume valid NUL-terminated arrays, sufficient buffers, locale-independent ASCII LOWER.',
                'C integer examples assume representable signed arithmetic with division truncating toward zero. Undefined inputs are not portable oracles.']},
        'counts': counts, 'inventory': files, 'ancillary_inventory': ancillary,
        'boot_area_list': {'path': 'area/area.lst', 'source_entry': ref('src/db.c', 'boot_db', 310),
                           'files': boot_files, 'status': 'pending', 'note': 'Section locators only; content, resets and specials not semantically traced.'},
        'verification': {'structural': [], 'runtime_tests': [], 'external_validation_report': 'verification.json',
            'commands': [{'command': '.venv/Scripts/python.exe docs/reports/rom24-code-paths/whole-codebase/build_report.py',
                          'kind': 'report generation and structural validation', 'result': 'passed before final artifact rendering'}],
            'pending': ['Resolve every pending lexical site into feasible semantic paths.',
            'Trace all remaining function bodies, macros, dispatch/caller guards, callback routes and loaded data.',
            'Audit lexical inventory against compiler/preprocessor output for each supported platform.',
            'No executable regression tests generated or run; pseudo cases are static specifications.']}}
    ids = [c['id'] for c in cases]
    assert len(ids) == len(set(ids))
    for c in cases:
        for bid in c['branch_ids']:
            assert bid in ledger and c['id'] in ledger[bid]['case_ids']
        assert c['status'] in {'specified', 'blocked'}
        for r in c['source_refs']:
            text = (SOURCE / r['file']).read_text(encoding='latin1').splitlines()
            assert 1 <= r['line'] <= len(text), r
            source_function = by_key[(r['file'], r['function'])]
            assert source_function['line'] <= r['line'] <= source_function['end_line'], r
        for field in ('entry', 'fixture', 'controls', 'action', 'expected', 'evidence', 'open_questions'):
            assert field in c, (c['id'], field)
    for b in ledger.values():
        assert b['disposition'] in {'specified', 'blocked', 'pending', 'disabled', 'unreachable', 'out_of_scope'}
        assert all(cid in ids for cid in b['case_ids'])
    manifest['verification']['structural'] = ['JSON parsed; unique case and branch IDs; bidirectional branch/case references; required case fields; source citation line bounds; all inventory/ledger entries have a disposition.',
        'Counts distinguish lexical inventory, partially specified functions, and dynamically verified cases. No coverage percentage inferred.']
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8')
    (OUT / 'cases.json').write_text(json.dumps({'schema_version': 1, 'cases': cases}, indent=2) + '\n', encoding='utf8')
    pages = OUT / 'files'
    pages.mkdir(exist_ok=True)
    for f in files:
        rows = [f"# {f['path']}", '', f"Role: {f['role']}. Disposition: **{f['status']}**. SHA-256: `{f['sha256']}`.", '',
            'This page is an inventory/checkpoint. Pending syntax sites are not established behavioral paths or executable coverage.', '']
        for fn in f['functions']:
            rows += [f"## {fn['name']}", '', f"[Source line {fn['line']}]({(SOURCE / f['path']).as_posix()}:{fn['line']}); ends at line {fn['end_line']}. Status: {fn['status']}.", '',
                'Entry references (reviewed in the completion record):' if 'completion_review' in fn else 'Entry references (lexical candidates; caller guards still require inspection):', '']
            if 'completion_review' in fn:
                rows += ['Completed contract and caller audit: [spec_name completion](../spec-name-completion.md). No remaining gaps for this function.', '']
            rows += [f"- {r.get('caller', r['kind'])}: `{r['file']}:{r['line']}` ({r['kind']})." for r in fn['entry_routes']]
            rows += ['', 'Dependencies: ' + ', '.join(f"`{d['name']}`" for d in fn['dependencies']) + '.', '', '| Ledger ID | Line | Predicate/transfer | Cases | Disposition |', '|---|---:|---|---|---|']
            for b in fn['branch_ledger']:
                pred = b['predicate_or_transfer'].replace('|', '\\|').replace('\n', ' ').replace('\r', '')
                disposition = b['disposition']
                if 'disposition_note' in b:
                    disposition += '. ' + b['disposition_note']
                rows.append(f"| `{b['id']}` | {b['source_ref']['line']} | `{pred}` | {', '.join(b['case_ids'])} | {disposition} |")
            rows += ['']
        rows += ['## Preprocessor and macro inventory', ''] + [f"- Line {r['line']}: `{r['text'].replace(chr(10), ' ')}` — pending configuration/reachability review." for r in f['preprocessor_directives']]
        rows += ['', '## Static tables', ''] + [f"- `{r['name']}` at line {r['line']} — pending entry/termination review." for r in f['static_tables']]
        rows += ['', '## Commented code candidates', ''] + [f"- Lines {r['line']}–{r['end_line']}: disabled inside block comment; content hash `{r['sha256']}`." for r in f['commented_code_candidates']]
        (pages / (Path(f['path']).name + '.md')).write_text('\n'.join(rows) + '\n', encoding='utf8')
    pseudo = ['# Language-neutral pseudo suite', '', 'Evidence: static source tracing only. These cases have not been executed against C or Python.', '']
    for c in cases:
        pseudo += [f"## {c['id']}", '', c['title'], '', '```text', 'CASE ' + c['id'],
            'SOURCE ' + '; '.join(f"{r['file']}:{r['function']}:{r['line']}" for r in c['source_refs']),
            'GIVEN ' + json.dumps(c['fixture'], ensure_ascii=False), 'AND ' + json.dumps(c['controls'], ensure_ascii=False),
            'WHEN ' + c['action'], 'THEN ' + json.dumps(c['expected'], ensure_ascii=False), '```', '']
        if c['open_questions']:
            pseudo += ['Open questions: ' + '; '.join(c['open_questions']), '']
    (OUT / 'pseudo-suite.md').write_text('\n'.join(pseudo), encoding='utf8')
    summary = ['# ROM2.4 whole-codebase code-path report', '', '**Status: partial behavioral specification; whole-source lexical inventory. The requested complete semantic trace is unfinished.**', '',
        f"Source: `{SOURCE}`. HEAD reference: `{revision}`. Per-file hashes identify the inspected snapshot. Normal Git status is unavailable. The manifest records an independent comparison against HEAD content.", '',
        '## Coverage and evidence', '', '| Measure | Count |', '|---|---:|']
    summary += [f'| {k.replace("_", " ")} | {v} |' for k, v in counts.items()]
    summary += ['', 'No executable branch coverage, whole-server parity, successful C build, or passing gameplay tests is claimed. Every file/function/site has an explicit pending or specified disposition in the manifest; pending sites are work remaining, not exclusions.', '',
        '## Artifacts', '', '- [Pseudo suite](pseudo-suite.md): readable Arrange/Act/Assert contracts.', '- [Case catalog](cases.json): portable structured expectations.',
        '- [Coverage manifest](manifest.json): hashes, function inventory, call candidates, macros, preprocessor alternatives, tables, data inventory, and pending work.',
        '- [Tracing notes](tracing-notes.md): helper contracts, source quirks, configuration risks and Python adaptation.', '',
        '- [Validation results](verification.json): snapshot, link and structural checks; no gameplay execution.', '',
        '## File inventory', '', '| File | Lines | Definitions | Disposition |', '|---|---:|---:|---|']
    summary += [f"| [{f['path']}](files/{Path(f['path']).name}.md) | {f['lines']} | {len(f['functions'])} | {f['status']} |" for f in files]
    summary += ['', '## Coverage criterion and continuation', '',
        '`spec_name` is now fully traced: all 22 mappings, NULL/nonmember inputs, sentinel termination, pointer ownership and caller reachability are specified in 24 cases. See [completion audit](spec-name-completion.md). Together with the five lookup helpers, six functions are fully traced. The rest of special.c remains partial.', '',
        'Scan has linked cases for its explicit control sites and additional tests for missing exits, visibility rechecks and undefined inputs. Scan delivery through the communication layer, platform configuration and the remaining subsystems are open.', '',
        'The continuation adds 63 cases and reconciles the local control-site ledgers of 25 existing utility/helper functions. These local ledgers remain distinct from complete caller/dependency tracing; no additional function is promoted to fully traced solely from lexical links.', '',
        'Alias storage cases now cover uppercase names retained by the loader. Ban cases cover a populated recycle list with shared-string names, empty/whitespace input, malformed levels/flags, duplicate flag letters, trailing spaces and missing final newlines. Allocated recycled names, other malformed formats, complete caller/storage invariants and platform persistence behavior remain open.', '',
        'Portal cases now trace repeated ordinal lookup, an alternate nonportal match, and a three-level follower graph whose linked-list mutation revisits a moved follower. Recipient rendering, other follower graph classes, dynamically allocated descriptions and complete movement/lookup helper suites remain open.', '',
        'Case selection distinguishes observable guard outcomes, ordered failures, string and arithmetic boundaries, loop cardinalities, mutation order and caller-versus-helper contracts. It does not enumerate a Cartesian product of all game states. The lexical index includes explicit control transfers and short-circuit operators but cannot establish feasibility or find every implicit branch.', '',
        'Continue from `manifest.json`, keeping current case IDs. First resolve syntax sites in functions already carrying cases; then process command dispatch/session handling, movement/objects/combat, magic/effects, update/persistence, content loaders and specials. Load-dependent area/data contracts and platform branches remain in scope. Do not mark a function complete solely because it has one case.', '',
        'To regenerate, run `author_cases.py`, `build_report.py` and `validate_report.py` in that order with Python. The scripts read the C checkout and write the report artifacts in this directory.']
    (OUT / 'report.md').write_text('\n'.join(summary) + '\n', encoding='utf8')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    main()

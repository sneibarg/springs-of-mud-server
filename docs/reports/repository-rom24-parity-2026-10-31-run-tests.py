"""Run current top-level unittest modules separately to isolate module stubs."""
import concurrent.futures
import json
import os
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]


def run(module):
    start = time.monotonic()
    try:
        process = subprocess.run([sys.executable, '-m', 'unittest', module], cwd=ROOT,
                                 capture_output=True, text=True, timeout=60,
                                 env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})
        output = process.stdout + process.stderr
        match = re.search(r'Ran (\d+) tests?', output)
        return dict(module=module, returncode=process.returncode,
                    tests=int(match[1]) if match else None,
                    seconds=round(time.monotonic() - start, 2), output=output)
    except subprocess.TimeoutExpired:
        return dict(module=module, returncode='timeout', tests=None, seconds=60)


if __name__ == '__main__':
    modules = ['tests.' + path.stem for path in sorted((ROOT / 'tests').glob('test_*.py'))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(run, modules))
    output = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'docs/reports/repository-rom24-parity-2026-10-31-tests.json')
    output.write_text(
        json.dumps(rows, indent=2), encoding='utf-8')
    print(json.dumps(dict(modules=len(rows), tests=sum(row['tests'] or 0 for row in rows),
                          passing_modules=sum(row['returncode'] == 0 for row in rows),
                          other=[{key: value for key, value in row.items() if key != 'output'}
                                 for row in rows if row['returncode'] != 0]), indent=2))

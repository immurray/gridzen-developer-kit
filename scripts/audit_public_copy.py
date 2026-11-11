"""Audit tracked distribution prose and built long descriptions; never mutate files."""
from pathlib import Path
import argparse
import json
import re
import runpy
import subprocess
import tarfile
import tomllib
import zipfile
from email.parser import Parser

ROOT = Path(__file__).resolve().parents[1]
POLICY = runpy.run_path(str(ROOT/'tests/test_public_verification_copy.py'))
PATTERN = POLICY['PUBLIC_COPY_BAD']


def normalize(text, path):
    text = POLICY['public_copy_normalized'](text)
    # Exact compatibility inputs, output keys/enums and workflow action identifiers.
    # Never exempt a whole line, section or a file just because it mentions CEP.
    text = re.sub(r'''(?P<quote>["'])payout(?P=quote)''', 'LEGACY_EVENT', text) if path.suffix in ('.py', '.json') else text
    text = re.sub(r'\bpayout(?=:)', 'LEGACY_EVENT', text) if path.suffix == '.js' else text
    text = re.sub(r'\bpayout_account\b', 'LEGACY_ACCOUNT_EVENT', text)
    if path.suffix in ('.py', '.json'):
        text = re.sub(r'''(?P<quote>["'])prepaid(?P=quote)''', 'CREDIT_AVAILABILITY_ENUM', text)
        text = text.replace('"payments-operations"', 'LEGACY_OWNER_VALUE')
    text = text.replace('cep-existing-payment-2026-10-22', 'CEP_TERMS_VERSION')
    text = text.replace('event=\\\"payout\\\"', 'event=LEGACY_EVENT')
    text = re.sub(r'actions/checkout@v[0-9]+', 'GIT_ACTION', text)
    return text


def scope_paths():
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    paths = set(POLICY['current_public_copy_paths']())
    for name in filter(None, tracked):
        p = Path(name)
        if name.startswith(('docs/', 'distribution/')) or name.startswith('src/') or name.startswith('skills/'):
            if p.suffix in ('.md', '.json', '.py', '.js', '.html', '.yml', '.yaml'):
                paths.add(ROOT/p)
        if name.startswith('examples/') and (p.name.startswith('README') or p.suffix in ('.py', '.ts', '.json')):
            paths.add(ROOT/p)
    return sorted(paths)


def scan_repository():
    rows, failures = [], []
    for path in scope_paths():
        relative = path.relative_to(ROOT)
        raw = path.read_text()
        if path.parent == ROOT and path.name.startswith('README'):
            if POLICY['strict_description_violations'](raw):
                failures.append(f'{relative}: strict README description violation')
        text = normalize(raw, relative)
        for line_number, line in enumerate(text.splitlines(), 1):
            rows.append(f'{relative}:{line_number}:{line}')
            if PATTERN.search(line):
                failures.append(f'{relative}:{line_number}:{line}')
    return rows, failures


def check_artifacts(directory):
    checked = []
    expected_version = tomllib.loads((ROOT/'pyproject.toml').read_text())['project']['version']
    expected_lines = (ROOT/'README.md').read_text().rstrip().splitlines()
    for path in sorted(directory.iterdir()):
        payloads = []
        if path.suffix == '.whl':
            with zipfile.ZipFile(path) as archive:
                payloads = [(n, archive.read(n)) for n in archive.namelist() if n.endswith('.dist-info/METADATA')]
        elif path.name.endswith('.tar.gz'):
            with tarfile.open(path) as archive:
                payloads = [(m.name, archive.extractfile(m).read()) for m in archive if m.name.endswith('/PKG-INFO')]
        if path.suffix == '.whl' or path.name.endswith('.tar.gz'):
            assert payloads, (path, 'missing long-description metadata')
        for name, raw in payloads:
            metadata = Parser().parsestr(raw.decode('utf-8'))
            body = metadata.get_payload()
            assert metadata['Version'] == expected_version, (path, 'version')
            assert isinstance(body, str), (path, name, 'invalid description')
            assert metadata['Description-Content-Type'] == 'text/markdown', (path, name, 'content type')
            assert body.rstrip().splitlines() == expected_lines, (path, name, 'line-by-line description drift')
            assert not POLICY['strict_description_violations'](body), (path, name)
            checked.append(f'{path.name}:{name}')
    assert any('.whl:' in n for n in checked) and any('.tar.gz:' in n for n in checked), 'wheel and sdist required'
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus', type=Path)
    parser.add_argument('--artifacts', type=Path)
    args = parser.parse_args()
    rows, failures = scan_repository()
    if args.corpus:
        args.corpus.write_text('\n'.join(rows)+'\n')
    if failures:
        print('\n'.join(failures))
        return 1
    print(f'PASS public copy: {len(scope_paths())} files; zero non-exempt matches')
    if args.artifacts:
        for name in check_artifacts(args.artifacts):
            print('PASS long description:', name, '; version='+tomllib.loads((ROOT/'pyproject.toml').read_text())['project']['version']+'; line-by-line match; 0 red-line matches')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

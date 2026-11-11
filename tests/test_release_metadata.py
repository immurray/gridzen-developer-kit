"""Candidate version consistency and fail-closed checks of real archive metadata."""
import ast
import io
import json
from pathlib import Path
import runpy
import tarfile
import tomllib
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
VERSION = tomllib.loads((ROOT/'pyproject.toml').read_text())['project']['version']


def test_current_release_declarations_are_consistent():
    from gridzen_developer import __version__
    from gridzen_developer.server import app, health
    from gridzen_developer.atomic import catalog
    assert VERSION == __version__ == app.version == health()['version'] == catalog()['package_version'] == '0.7.3'
    for name in ('plugin.json', 'server.json', '.claude-plugin/plugin.json', '.cursor-plugin/plugin.json'):
        assert json.loads((ROOT/name).read_text())['version'] == VERSION, name
    for name in ('README.md', 'README.es.md', 'README.zh-CN.md', 'llms-install.md', 'NOTICE.md', 'CHANGELOG.md'):
        assert VERSION in (ROOT/name).read_text(), name
    for name in ('server.py', 'mcp.py', 'atomic.py', 'production_mcp.py'):
        tree = ast.parse((ROOT/'src/gridzen_developer'/name).read_text())
        versions = [keyword.value.value for node in ast.walk(tree) if isinstance(node, ast.Call)
                    for keyword in node.keywords if keyword.arg == 'version' and isinstance(keyword.value, ast.Constant)]
        assert versions and set(versions) == {VERSION}, name


def audit_module():
    return runpy.run_path(str(ROOT/'scripts/audit_public_copy.py'))


def write_archives(directory, body, version=VERSION, content_type='text/markdown'):
    metadata = f'Metadata-Version: 2.4\nName: gridzen-developer-kit\nVersion: {version}\nDescription-Content-Type: {content_type}\n\n{body}'
    with zipfile.ZipFile(directory/f'gridzen_developer_kit-{version}-py3-none-any.whl', 'w') as archive:
        archive.writestr(f'gridzen_developer_kit-{version}.dist-info/METADATA', metadata)
    with tarfile.open(directory/f'gridzen_developer_kit-{version}.tar.gz', 'w:gz') as archive:
        for name in (f'gridzen_developer_kit-{version}/PKG-INFO',
                     f'gridzen_developer_kit-{version}/src/gridzen_developer_kit.egg-info/PKG-INFO'):
            raw = metadata.encode()
            entry = tarfile.TarInfo(name); entry.size = len(raw)
            archive.addfile(entry, io.BytesIO(raw))


def test_archive_guard_reads_wheel_and_both_sdist_descriptions(tmp_path):
    write_archives(tmp_path, (ROOT/'README.md').read_text())
    checked = audit_module()['check_artifacts'](tmp_path)
    assert len(checked) == 3


@pytest.mark.parametrize('bad', [
    'https://gridzen.ai/pricing/', '/pricing/', '/payments', 'Real payments remain disabled.',
    'Payments', 'pagos reales', 'cobros reales', 'cobro', 'checkout', 'prepaid', 'funding',
    '收费', '收款', '出款', '提现', '付款', '入金',
    'payout', 'payout_account', 'payout-policy-designer',
])
def test_archive_guard_rejects_forbidden_copies_even_when_source_matches(tmp_path, bad):
    audit = audit_module()
    # A contaminated source must not legitimize an equally contaminated build.
    source = tmp_path/'source'; source.mkdir()
    (source/'README.md').write_text((ROOT/'README.md').read_text()+'\n'+bad+'\n')
    (source/'pyproject.toml').write_text((ROOT/'pyproject.toml').read_text())
    audit['check_artifacts'].__globals__['ROOT'] = source
    artifacts = tmp_path/'artifacts'; artifacts.mkdir()
    write_archives(artifacts, (source/'README.md').read_text())
    with pytest.raises(AssertionError):
        audit['check_artifacts'](artifacts)


def test_archive_guard_rejects_pre_fix_package_version(tmp_path):
    write_archives(tmp_path, (ROOT/'README.md').read_text(), version='0.7.2')
    with pytest.raises(AssertionError, match='version'):
        audit_module()['check_artifacts'](tmp_path)


def test_archive_guard_rejects_stale_description_and_missing_format(tmp_path):
    write_archives(tmp_path, 'An older clean README is still the wrong release source.\n')
    with pytest.raises(AssertionError, match='description drift'):
        audit_module()['check_artifacts'](tmp_path)
    for path in tmp_path.iterdir(): path.unlink()
    write_archives(tmp_path, (ROOT/'README.md').read_text())
    next(tmp_path.glob('*.whl')).unlink()
    with pytest.raises(AssertionError, match='wheel and sdist required'):
        audit_module()['check_artifacts'](tmp_path)

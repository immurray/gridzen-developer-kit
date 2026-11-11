"""Validate an actual wheel/sdist installation against canonical public assets.

Run with the clean environment's Python, outside an editable install. No network
or provider calls are made. Optional website archives are downloaded separately.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import sysconfig
import tempfile
import tomllib
import zipfile


def check(source, website_source=None, website_skills=None):
    from gridzen_developer import __version__
    import gridzen_developer
    from gridzen_developer.skills import list_skills

    source = source.resolve()
    config = tomllib.loads((source / 'pyproject.toml').read_text())
    version = config['project']['version']
    assert __version__ == importlib.metadata.version('gridzen-developer-kit') == version
    assert Path(gridzen_developer.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()), 'Editable/source fallback is not an installed-package test'
    root = Path(sysconfig.get_path('data')) / 'share/gridzen-developer-kit'
    installed = {}
    for destination, names in config['tool']['setuptools']['data-files'].items():
        for name in names:
            relative = Path(destination).relative_to('share/gridzen-developer-kit') / Path(name).name
            file = root / relative
            assert file.is_file() and file.read_bytes() == (source / name).read_bytes(), str(relative)
            installed[str(relative)] = hashlib.sha256(file.read_bytes()).hexdigest()
    required_docs = {'README.md', 'README.zh-CN.md', 'README.es.md', 'NOTICE.md',
                     'docs/activation.md', 'docs/atomic-tools.md',
                     'docs/verification-evaluation.md', 'docs/mexico-identity-account.md',
                     'docs/multilingual-ui.md', 'docs/harness/README.md'}
    assert required_docs <= installed.keys(), 'Public guides missing from the package manifest'
    assert len(list((root / 'docs/harness').glob('*.md'))) == 11
    skills = list_skills()
    expected_names = {p.parent.name for p in (source / 'skills').glob('*/SKILL.md')}
    assert len(skills) == len(expected_names) == 14
    assert {s['name'] for s in skills} == expected_names
    assert all(Path(s['path']).resolve().is_relative_to(root.resolve()) for s in skills)
    metadata = importlib.metadata.metadata('gridzen-developer-kit')
    assert metadata.get_payload().rstrip() == (source / 'README.md').read_text().rstrip()
    assert 'Fourteen Skills' in metadata.get_payload()
    assert not re.search(r'\b(funding|checkout|prepaid)\b|smithery.ai/servers/support-35ug', metadata.get_payload(), re.I)
    for relative in installed:
        if not relative.endswith('.md'):
            continue
        text = (root / relative).read_text()
        for link in re.findall(r'\]\(([^ )]+)', text):
            if link.startswith(('https:', 'http:', 'mailto:', '#', '/')):
                continue
            target = (root / relative).parent / link.split('#')[0]
            assert target.exists(), (relative, link)
    website_matches = {}
    for archive_path, prefix, selected in (
        (website_source, 'gridzen-developer-kit/', installed),
        (website_skills, '', {k: v for k, v in installed.items() if k.startswith('skills/')}),
    ):
        if archive_path:
            with zipfile.ZipFile(archive_path) as archive:
                for relative in selected:
                    assert archive.read(prefix + relative) == (root / relative).read_bytes(), relative
            website_matches[archive_path.name] = len(selected)
    commands = []
    with tempfile.TemporaryDirectory(prefix='gridzen-install-check-') as tmp:
        work = Path(tmp)
        env = dict(os.environ, GRIDZEN_TELEMETRY_DIR=str(work / 'telemetry'))
        env.pop('PYTHONPATH', None)
        cli = Path(sys.executable).parent / ('gridzen.exe' if os.name == 'nt' else 'gridzen')

        def run(*args, as_json=True):
            result = subprocess.run([str(cli), *args], cwd=work, env=env, text=True, capture_output=True, timeout=30, check=True)
            commands.append(list(args))
            return json.loads(result.stdout) if as_json else result.stdout

        assert 'Gridzen' in run('--help', as_json=False)
        assert len(run('skills')) == 14
        assert len(run('tools')['products']) == 8
        assert run('coverage', '--country', 'MX')['mode'] == 'research'
        assert run('plan', '--country', 'ID', '--event', 'onboarding')['execution']['live_available'] is False
        result = run('simulate', '--country', 'ID', '--capability', 'bank_account_match', '--scenario', 'timeout')
        assert result['simulated'] is True and result['verified'] is False and result['provider_calls'] == 0
        payload = work / 'input.json'
        payload.write_text('{"phone":"+1 (202) 555-0123"}')
        assert run('tool', 'phone-format', '--input-file', str(payload))['normalized'] == '+12025550123'
        project = work / 'project'
        project.mkdir()
        preview = run('setup', '--client', 'all', '--project', str(project))
        assert preview['changed_files'] > 0 and not list(project.iterdir())
        applied = run('setup', '--client', 'all', '--project', str(project), '--apply')
        assert len(applied['clients']) == 10 and all(c['skill_count'] == 14 for c in applied['clients'])
        assert run('setup', '--client', 'all', '--project', str(project), '--apply')['changed_files'] == 0
    return {'status': 'PASS', 'version': version, 'skills': 14, 'profiles': 8, 'installed_files': len(installed), 'installed_hashes': installed, 'website_matches': website_matches, 'cli_commands': commands, 'network_calls': 0, 'live_provider_calls': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--website-source', type=Path)
    parser.add_argument('--website-skills', type=Path)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    result = check(args.source_root, args.website_source, args.website_skills)
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'installed_hashes'}))

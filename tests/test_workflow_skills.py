import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest
from gridzen_developer.skills import list_skills

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['mexico-pilot-scoper','payout-policy-designer','provider-rights-readiness']


def test_six_skill_assets_are_discoverable():
    assert len(list_skills()) == 6


@pytest.mark.parametrize('name', NAMES)
def test_workflow_full_response_contracts_and_original_tests(name):
    directory = ROOT / 'skills' / name
    spec = json.loads((directory/'spec.json').read_text())
    assert spec['version'] == '1.0.0'
    assert 'MIT' in (directory/'LICENSE').read_text()
    module_spec = importlib.util.spec_from_file_location(name, directory/'evaluate.py')
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    for file in sorted((directory/'examples').glob('*.json')):
        fixture = json.loads(file.read_text())
        expected = fixture['expected_output']
        assert expected['approval_granted'] is False
        assert expected['network_calls'] is False
        if fixture['kind'] == 'out-of-scope':
            with pytest.raises(ValueError): module.evaluate(fixture['input'], spec)
            assert expected['status'] == 'refused'
        else:
            assert module.evaluate(fixture['input'], spec) == expected
            assert expected['status'] in ('draft_for_review','needs_information')
            if 'policy_draft' in expected: assert expected['policy_draft']['deployed'] is False
    result = subprocess.run([sys.executable,'-m','unittest','test_evaluate.py'],cwd=directory,capture_output=True,text=True)
    assert result.returncode == 0, result.stderr

import json
from pathlib import Path
import tomllib
import zipfile
import pytest
from gridzen_developer.setup import CLIENTS, setup


def test_all_clients_dry_run_apply_and_repeat(tmp_path):
 assert setup('all',tmp_path)['changed_files'] > 30
 assert list(tmp_path.iterdir()) == []
 result=setup('all',tmp_path,True)
 assert len(result['clients']) == 10
 assert setup('all',tmp_path,True)['changed_files'] == 0
 assert tomllib.loads((tmp_path/'.codex/config.toml').read_text())['mcp_servers']['gridzen']['url'].endswith('/mcp')
 assert json.loads((tmp_path/'.vscode/mcp.json').read_text())['servers']['gridzen']['type'] == 'http'
 assert json.loads((tmp_path/'.gemini/settings.json').read_text())['mcpServers']['gridzen']['httpUrl'].endswith('/mcp')
 for name,(_,skills,_,mode) in CLIENTS.items():
  if skills: assert len(list((tmp_path/skills).glob('*/SKILL.md'))) == 6
 archives=list((tmp_path/'gridzen-clients/claude-desktop/skills').glob('*.zip'))
 assert len(archives)==6
 for archive in archives:
  with zipfile.ZipFile(archive) as z:
   assert sum(name.endswith('/SKILL.md') for name in z.namelist())==1
   assert any(name.endswith('/LICENSE') for name in z.namelist())


def test_merge_preserves_other_servers_and_credentials_without_echo(tmp_path):
 file=tmp_path/'.cursor/mcp.json';file.parent.mkdir()
 file.write_text(json.dumps({'custom':'PRIVATE_SENTINEL','mcpServers':{'existing':{'command':'example','env':{'TOKEN':'PRIVATE_SENTINEL'}}}}))
 result=setup('cursor',tmp_path,True)
 assert 'PRIVATE_SENTINEL' not in json.dumps(result)
 assert json.loads(file.read_text())['mcpServers']['existing']['env']['TOKEN']=='PRIVATE_SENTINEL'
 backups=list(file.parent.glob('mcp.json.gridzen-backup-*'))
 assert len(backups)==1 and (backups[0].stat().st_mode & 0o777)==0o600


def test_conflict_leaves_all_files_unchanged(tmp_path):
 file=tmp_path/'.cursor/mcp.json';file.parent.mkdir()
 original='{"mcpServers":{"gridzen":{"url":"https://different.example/mcp"}}}'
 file.write_text(original)
 with pytest.raises(ValueError):setup('all',tmp_path,True)
 assert file.read_text()==original
 assert not (tmp_path/'.codex').exists()


def test_symlink_escape_is_rejected(tmp_path):
 outside=tmp_path/'outside';outside.mkdir()
 (tmp_path/'.codex').symlink_to(outside,target_is_directory=True)
 with pytest.raises(ValueError):setup('codex',tmp_path,True)
 assert list(outside.iterdir())==[]


def test_individual_archives_have_root_folder_license_and_repeatable_bytes(tmp_path):
    import zipfile
    from io import BytesIO
    from gridzen_developer.setup import skill_zip
    directory = tmp_path / 'example-skill'
    directory.mkdir()
    (directory / 'SKILL.md').write_text('---\nname: example-skill\ndescription: synthetic test\n---\n')
    first = skill_zip(directory)
    assert first == skill_zip(directory)
    with zipfile.ZipFile(BytesIO(first)) as archive:
        assert archive.namelist() == ['example-skill/SKILL.md', 'example-skill/LICENSE']
        assert 'MIT License' in archive.read('example-skill/LICENSE').decode()

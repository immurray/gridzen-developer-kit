"""Project-scoped harness setup. Dry-run default; refuses conflicts and symlinks."""
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib
import zipfile
from io import BytesIO
from .skills import list_skills

URL = 'https://gridzen.ai/developers/mcp'
CLIENTS = {
 'codex': ('.codex/config.toml', '.agents/skills', 'toml', 'native'),
 'claude-code': ('.mcp.json', '.claude/skills', 'http', 'native'),
 'claude-desktop': ('gridzen-clients/claude-desktop/claude_desktop_config.json', None, 'stdio', 'manual-import'),
 'cursor': ('.cursor/mcp.json', '.cursor/skills', 'url', 'native'),
 'vscode': ('.vscode/mcp.json', '.github/skills', 'vscode', 'native'),
 'copilot-cli': ('.github/mcp.json', '.github/skills', 'copilot', 'native'),
 'gemini-cli': ('.gemini/settings.json', '.gemini/skills', 'gemini', 'native'),
 'cline': ('gridzen-clients/cline/cline_mcp_settings.json', '.cline/skills', 'cline', 'manual-import'),
 'roo-code': ('.roo/mcp.json', '.roo/skills', 'roo', 'native'),
 'opencode': ('opencode.json', '.opencode/skills', 'opencode', 'native'),
}

def server_entry(kind):
 if kind == 'stdio':
  command = Path(sys.executable).parent / ('gridzen-mcp.exe' if os.name == 'nt' else 'gridzen-mcp')
  if not command.is_file(): raise ValueError('Run setup from the installed Gridzen environment so the desktop command is available.')
  return {'command': str(command), 'args': []}
 if kind == 'cline': return {'type': 'streamableHttp', 'url': URL, 'disabled': False, 'autoApprove': []}
 if kind == 'roo': return {'type': 'streamable-http', 'url': URL}
 if kind == 'url': return {'url': URL}
 if kind == 'gemini': return {'httpUrl': URL}
 if kind == 'copilot': return {'type': 'http', 'url': URL, 'tools': ['*']}
 if kind == 'opencode': return {'type': 'remote', 'url': URL, 'enabled': True, 'oauth': False}
 return {'type': 'http', 'url': URL}


def skill_zip(directory):
 stream = BytesIO()
 license_path = Path(__file__).parent / 'data/LICENSE'
 with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
  for file in sorted(directory.rglob('*')):
   if file.is_file() and '__pycache__' not in file.parts and file.suffix not in ('.pyc','.pyo'):
    item = zipfile.ZipInfo(directory.name+'/'+str(file.relative_to(directory)), (2026,10,9,0,0,0))
    item.compress_type=zipfile.ZIP_DEFLATED
    archive.writestr(item, file.read_bytes())
  if not (directory/'LICENSE').exists():
   item = zipfile.ZipInfo(directory.name+'/LICENSE', (2026,10,9,0,0,0))
   item.compress_type=zipfile.ZIP_DEFLATED
   archive.writestr(item, license_path.read_bytes())
 return stream.getvalue()


def setup(client, project, apply=False):
 root = Path(project).resolve()
 if not root.is_dir(): raise ValueError('Project directory must already exist.')
 skills = list_skills()
 if len(skills) != 6: raise ValueError('Expected six installed Skills; reinstall the complete package.')
 names = list(CLIENTS) if client == 'all' else [client]
 writes = {}
 originals = {}
 summaries = []
 def proposed(relative, content):
  path = root / relative
  for part in [path, *path.parents]:
   if part == root: break
   if part.is_symlink(): raise ValueError(f'Refusing symlink: {relative}')
  old = path.read_bytes() if path.is_file() else None
  if path.exists() and not path.is_file(): raise ValueError(f'Expected regular file: {relative}')
  if path in writes and writes[path] != content: raise ValueError(f'Conflicting client templates: {relative}')
  writes[path] = content; originals[path] = old
  return old
 for name in names:
  config, skill_path, kind, mode = CLIENTS[name]
  file = root / config
  # Reject links before reading config, including links in its parent directories.
  old = proposed(config, b'')
  text = old.decode('utf-8') if old is not None else ''
  if kind == 'toml':
   current = tomllib.loads(text) if text else {}
   wanted = {'url': URL}
   existing = current.get('mcp_servers', {}).get('gridzen')
   if existing is not None and existing != wanted: raise ValueError(f'Existing Gridzen configuration differs: {config}')
   content = old if existing is not None else (text.rstrip()+'\n\n[mcp_servers.gridzen]\nurl = '+json.dumps(URL)+'\n').lstrip().encode()
  else:
   current = json.loads(text) if text else {}
   if not isinstance(current,dict): raise ValueError(f'Expected configuration object: {config}')
   key = 'servers' if kind == 'vscode' else 'mcp' if kind == 'opencode' else 'mcpServers'
   group = current.setdefault(key,{})
   if not isinstance(group,dict): raise ValueError(f'Expected server map: {config}')
   wanted = server_entry(kind)
   if 'gridzen' in group:
    existing = group['gridzen']
    if not isinstance(existing,dict) or any(existing.get(k) != v for k,v in wanted.items()):
     raise ValueError(f'Existing Gridzen configuration differs: {config}')
    content = old
   else:
    group['gridzen'] = wanted
    content = (json.dumps(current,ensure_ascii=False,indent=2)+'\n').encode()
  writes[file] = content
  for skill in skills:
   source = Path(skill['path'])
   if skill_path:
    for item in sorted(source.rglob('*')):
     if not item.is_file() or '__pycache__' in item.parts or item.suffix in ('.pyc','.pyo'): continue
     relative = str(Path(skill_path)/source.name/item.relative_to(source))
     data = item.read_bytes(); previous = proposed(relative,data)
     if previous is not None and previous != data: raise ValueError(f'Existing Skill differs: {relative}')
   else:
    relative = f'gridzen-clients/claude-desktop/skills/{source.name}.zip'
    data = skill_zip(source);previous=proposed(relative,data)
    if previous is not None and previous != data: raise ValueError(f'Existing Skill archive differs: {relative}')
  summaries.append({'client':name,'config':config,'skills':skill_path or 'gridzen-clients/claude-desktop/skills','skill_count':6,'activation':mode})
 changed = [path for path,data in writes.items() if originals[path] != data]
 # Validate every destination before making any writes. Do not print existing config.
 for path in changed:
  current = path.read_bytes() if path.is_file() else None
  if current != originals[path]: raise ValueError('Concurrent project configuration change; no files written.')
 if apply:
  for path in changed:
   path.parent.mkdir(parents=True,exist_ok=True)
   if originals[path] is not None:
    fd,backup = tempfile.mkstemp(prefix=path.name+'.gridzen-backup-',dir=path.parent)
    with os.fdopen(fd,'wb') as stream: stream.write(originals[path])
   fd,temporary = tempfile.mkstemp(prefix='.gridzen-',dir=path.parent)
   try:
    with os.fdopen(fd,'wb') as stream: stream.write(writes[path])
    os.replace(temporary,path)
   finally:
    if os.path.exists(temporary): os.unlink(temporary)
 return {'status':'applied' if apply else 'dry_run','project':str(root),'clients':summaries,'changed_files':len(changed),'notice':'Native clients require workspace trust/restart. Desktop and Cline MCP need manual import. Installation is not model or client acceptance; no real verification is enabled.'}

"""Validate checked-in manifests against pinned official schema snapshots."""
from pathlib import Path
import json,zipfile
import jsonschema
root=Path(__file__).resolve().parents[1]
for file,schema in [('plugin.json','plugin.schema.json'),('mcp.json','mcp.schema.json'),('server.json','server.schema.json')]:
 jsonschema.validate(json.loads((root/file).read_text()),json.loads((root/'distribution/schemas'/schema).read_text()))
for name in ['.claude-plugin/plugin.json','.cursor-plugin/plugin.json']:
 value=json.loads((root/name).read_text())
 for key in ['skills','mcpServers']:
  assert (root/value[key]).exists(),(name,key)
for archive in (root/'dist').glob('*.zip'):
 with zipfile.ZipFile(archive) as z:
  names=z.namelist()
  assert len([n for n in names if n.endswith('SKILL.md')])==6
  assert not any(n.startswith('/') or '..' in Path(n).parts or n.endswith(('.pem','.env')) or 'secrets/' in n for n in names)
  assert 'LICENSE' in names
  assert not any(n.endswith(('.whl','.tar.gz','.zip')) for n in names)
print('PASS official registry/portable schemas, client paths and plugin archive boundaries')

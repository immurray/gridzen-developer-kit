"""Export an explicit developer-only allowlist into an existing public checkout."""
from pathlib import Path
import shutil,sys
root=Path(__file__).resolve().parents[1]
destination=Path(sys.argv[1]).resolve()
if destination==root or not (destination/'.git').is_dir():
 raise SystemExit('Use a separate checkout of the public developer repository')
files=['pyproject.toml','MANIFEST.in','README.md','README.zh-CN.md','README.es.md','LICENSE','NOTICE.md','SECURITY.md','.gitignore','server.json','plugin.json','mcp.json','.mcp.json','glama.json','llms-install.md']
paths=[root/p for p in files]
for directory in ['skills','examples','assets','tests','scripts','.claude-plugin','.cursor-plugin','distribution']:
 paths.extend(p for p in (root/directory).rglob('*') if p.is_file())
paths.extend((root/'src/gridzen_developer').glob('*.py'))
paths.extend((root/'src/gridzen_developer/data').glob('*.json'))
for extension in ['*.html','*.css','*.js','*.svg','*.png']:
 paths.extend((root/'src/gridzen_developer/web').glob(extension))
for path in paths:
 if '__pycache__' in path.parts or path.suffix in ('.pyc','.pem'):continue
 target=destination/path.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
workflow=destination/'.github/workflows';workflow.mkdir(parents=True,exist_ok=True)
for name in ['public-ci.yml','publish-pypi.yml']:shutil.copy2(root/'distribution'/name,workflow/name)
print('Exported public allowlist to',destination)

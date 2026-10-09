from pathlib import Path
import zipfile,hashlib,json
root=Path(__file__).resolve().parents[1];dest=root/'src/gridzen_developer/web/downloads';dest.mkdir(exist_ok=True)
def write(name,paths,prefix):
 with zipfile.ZipFile(dest/name,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(paths):
   if p.is_file() and '__pycache__' not in p.parts:z.write(p,prefix+str(p.relative_to(root)))
 return hashlib.sha256((dest/name).read_bytes()).hexdigest()
source=[root/'pyproject.toml',root/'MANIFEST.in',root/'README.md',root/'LICENSE',root/'NOTICE.md']+list((root/'src/gridzen_developer').glob('*.py'))+list((root/'src/gridzen_developer/data').glob('*.json'))+list((root/'examples').glob('*'))+list((root/'skills').rglob('*'))
source+=list(root.glob('README.*.md'))
source+=list((root/'src/gridzen_developer/web').glob('*.html'))+list((root/'src/gridzen_developer/web').glob('*.css'))+list((root/'src/gridzen_developer/web').glob('*.js'))
source+=list((root/'src/gridzen_developer/web').glob('*.svg'))+list((root/'src/gridzen_developer/web').glob('*.png'))
checks={'gridzen-developer-kit.zip':write('gridzen-developer-kit.zip',source,'gridzen-developer-kit/'),'gridzen-skills.zip':write('gridzen-skills.zip',list((root/'skills').rglob('*'))+[root/'LICENSE',root/'NOTICE.md'],'')}
(dest/'sha256.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))

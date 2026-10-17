from pathlib import Path
import zipfile,hashlib,json
root=Path(__file__).resolve().parents[1];dest=root/'src/gridzen_developer/web/downloads';dest.mkdir(exist_ok=True)
def write(name,paths,prefix):
 with zipfile.ZipFile(dest/name,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(set(paths)):
   if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
    info=zipfile.ZipInfo(prefix+str(p.relative_to(root)),date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
    z.writestr(info,p.read_bytes())
 return hashlib.sha256((dest/name).read_bytes()).hexdigest()
source=[root/'pyproject.toml',root/'MANIFEST.in',root/'README.md',root/'LICENSE',root/'NOTICE.md']+list((root/'src/gridzen_developer').glob('*.py'))+list((root/'src/gridzen_developer/data').glob('*.json'))+[root/'src/gridzen_developer/data/LICENSE']+list((root/'examples').rglob('*'))+list((root/'skills').rglob('*'))
source+=[root/'docs/activation.md',root/'docs/verification-evaluation.md']
source+=list(root.glob('README.*.md'))
source+=list((root/'src/gridzen_developer/web').glob('*.html'))+list((root/'src/gridzen_developer/web').glob('*.css'))+list((root/'src/gridzen_developer/web').glob('*.js'))
source+=list((root/'src/gridzen_developer/web').glob('*.svg'))+list((root/'src/gridzen_developer/web').glob('*.png'))
source+=list((root/'clients').rglob('*'))+list((root/'docs/harness').rglob('*'))+[root/'scripts/check_integration.py']+list((root/'src/gridzen_developer/web').glob('*.json'))
checks={'gridzen-developer-kit.zip':write('gridzen-developer-kit.zip',source,'gridzen-developer-kit/'),'gridzen-skills.zip':write('gridzen-skills.zip',list((root/'skills').rglob('*'))+[root/'LICENSE',root/'NOTICE.md'],'')}
import sys
sys.path.insert(0,str(root/'src'))
from gridzen_developer.setup import skill_zip
for directory in sorted((root/'skills').iterdir()):
 if (directory/'SKILL.md').exists():
  name=directory.name+'.zip'; (dest/name).write_bytes(skill_zip(directory));checks[name]=hashlib.sha256((dest/name).read_bytes()).hexdigest()
checks['gridzen-harnesses.zip']=write('gridzen-harnesses.zip',list((root/'clients').rglob('*'))+list((root/'docs/harness').rglob('*'))+list((root/'skills').rglob('*'))+[root/'LICENSE',root/'NOTICE.md'],'')
(dest/'sha256.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))

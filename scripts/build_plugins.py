"""Build client packages from canonical Skills and metadata; no private checkout."""
from pathlib import Path
import hashlib,json,zipfile

root=Path(__file__).resolve().parents[1]
dest=root/'dist';dest.mkdir(exist_ok=True)
common=[root/'LICENSE',root/'NOTICE.md',root/'README.md']+list((root/'skills').rglob('*'))+list((root/'assets').glob('*'))
def build(name,extra):
 with zipfile.ZipFile(dest/name,'w',zipfile.ZIP_DEFLATED) as archive:
  for path in sorted(common+[root/p for p in extra]):
   if path.is_file() and '__pycache__' not in path.parts:
    info=zipfile.ZipInfo(str(path.relative_to(root)),date_time=(2026,10,8,0,0,0))
    info.compress_type=zipfile.ZIP_DEFLATED
    archive.writestr(info,path.read_bytes())
 return hashlib.sha256((dest/name).read_bytes()).hexdigest()
checks={
 'gridzen-verification-plugin.zip':build('gridzen-verification-plugin.zip',['plugin.json','mcp.json']),
 'gridzen-verification-claude.zip':build('gridzen-verification-claude.zip',['.claude-plugin/plugin.json','.mcp.json','.claude-plugin/marketplace.json']),
 'gridzen-verification-cursor.zip':build('gridzen-verification-cursor.zip',['.cursor-plugin/plugin.json','.mcp.json']),
}
(dest/'plugin-sha256.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks))

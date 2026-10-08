import json,re
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
def test_every_declared_translation_exists_in_three_languages():
 text=(ROOT/'src/gridzen_developer/web/locales.js').read_text()
 data=json.loads(text.split('=',1)[1].split(';\nfor ',1)[0])
 keys=set(data['en'])
 assert set(data)=={'en','zh','es'}
 for locale in data.values():
  assert set(locale)==keys
  assert all(isinstance(v,str) and v.strip() for v in locale.values())
 for file in ['index.html','quickstart.html']:
  html=(ROOT/'src/gridzen_developer/web'/file).read_text()
  assert set(re.findall(r'data-i18n="([^"]+)"',html))<=keys
  assert '/developers/language.js' in html

def test_quickstart_preserves_code_and_localized_download_instructions():
 import zipfile
 with zipfile.ZipFile(ROOT/'src/gridzen_developer/web/downloads/gridzen-developer-kit.zip') as z:
  for path in ['README.zh-CN.md','README.es.md']:
   data=z.read('gridzen-developer-kit/'+path).decode()
   assert 'gridzen simulate --country ID --capability bank_account_match --scenario timeout' in data
   assert 'verified=false' in data

"""Copy acceptance only: the existing tools, event contract and Skills stay intact."""
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import tomllib
import pytest
ROOT=Path(__file__).parents[1]
WEB=ROOT/'src/gridzen_developer/web'
BAD=re.compile(r'funding|payout|checkout|prepaid',re.I)
class Render(HTMLParser):
    def __init__(self,locale):super().__init__();self.locale=locale;self.output=[];self.current=None
    def handle_starttag(self,tag,attrs):
        self.output.extend(v for k,v in attrs if k=='href')
        if 'data-i18n' in dict(attrs):self.current=tag;self.output.append(self.locale[dict(attrs)['data-i18n']])
    def handle_data(self,data):
        if self.current is None:self.output.append(data)
    def handle_endtag(self,tag):
        if tag==self.current:self.current=None

def locales():return json.JSONDecoder().raw_decode((WEB/'locales.js').read_text().split('=',1)[1].lstrip())[0]

@pytest.mark.parametrize('language',['en','es','zh','vi'])
def test_developer_entry_localized_output(language):
    html=(WEB/'index.html').read_text();assert not BAD.search(html)
    assert 'data-i18n="dev.payout"' not in html and 'value="payout"' not in html
    p=Render(locales()[language]);p.feed(html);rendered='\n'.join(p.output)
    assert not BAD.search(rendered)
    assert not re.search(r'/(?:console|help)/payments',rendered)
    assert '14' in locales()[language]['dev.three']
    assert len(list((ROOT/'skills').glob('*/SKILL.md')))==14

@pytest.mark.parametrize('name',['README.md','README.es.md','README.zh-CN.md'])
def test_readme_copy_and_cep_preservation(name):
    text=(ROOT/name).read_text();assert not BAD.search(text)
    assert 'https://smithery.ai/servers/support-35ug/gridzen-verification' not in text
    if name=='README.md':assert 'CEP' in text and 'SPEI' in text and 'Fourteen Skills' in text

def test_readme_is_the_package_long_description_source():
    assert tomllib.loads((ROOT/'pyproject.toml').read_text())['project']['readme']=='README.md'

def test_changed_localized_copy_has_a_fresh_browser_cache_key():
    digest=hashlib.sha256((WEB/'locales.js').read_bytes()).hexdigest()[:12]
    assert '/developers/locales.js?v='+digest in (WEB/'index.html').read_text()

def test_docs_example_uses_existing_onboarding_contract():
    from gridzen_developer import core
    assert core.plan('ID','onboarding')['event']=='onboarding'
    assert 'payout' in core.EVENTS  # No feature removed from the supported API.

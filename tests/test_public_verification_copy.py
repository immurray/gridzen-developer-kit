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


# Only current redistributable prose: do not rename the legacy API or Skill.
PUBLIC_COPY_BAD = re.compile(
    r"/(?:pricing|payments)(?:[/#?]|\b)|\b(?:payout(?:_account)?|funding|payments?|pagos?|cobros?)\b"
    r"|收款|出款|提现|付款|入金|真实收费|pagamentos?\s+reais|thanh\s+toán\s+thực", re.I,
)

def public_copy_violations(text):
    # This exact neutral CEP wording and existing endpoint remain supported.
    text = text.replace('https://gridzen.ai/console/api/payment-evidence/mx/cep/capabilities', 'CEP_CAPABILITIES')
    text = re.sub(r'(?<=SPEI )payment(?= evidence\b)', 'CEP', text, flags=re.I)
    text = text.replace('payout-policy-designer', 'LEGACY_SKILL_IDENTIFIER')
    # Exact compatibility declarations and existing CEP discovery inputs only.
    text = text.replace('legacy event identifier `payout`', 'legacy event identifier `EVENT`')
    text = text.replace('event="payout", task="mx_cep_existing_payment"', 'event="EVENT", task="CEP_TASK"')
    text = re.sub(r'(?<=SPEI )payment(?=-evidence approaches\b)', 'CEP', text)
    text = re.sub(r'(?<=/)(?:payment-evidence)(?=/mx/cep(?:[/` .]|$))', 'cep-evidence', text)
    for phrase in ('independent payment record', 'Check a SPEI payment',
                   'authorized existing payment', 'mexico payment operations'):
        text = re.sub(re.escape(phrase), phrase.replace('payment', 'CEP'), text, flags=re.I)
    return [match.group() for match in PUBLIC_COPY_BAD.finditer(text)]


def current_public_copy_paths():
    metadata = tomllib.loads((ROOT/'pyproject.toml').read_text())
    readme = metadata['project']['readme']
    readme = readme if isinstance(readme, str) else readme['file']
    paths = {ROOT/readme, *ROOT.glob('README*.md'), ROOT/'llms-install.md', ROOT/'docs/site-integration.md', ROOT/'NOTICE.md'}
    paths.update((ROOT/'skills').rglob('*.md'))
    paths.update((ROOT/'examples').rglob('*.md'))
    paths.update((ROOT/'distribution/market-expansion-2026-10-13/articles').glob('*.md'))
    for files in metadata['tool']['setuptools']['data-files'].values():
        paths.update(ROOT/name for name in files if name.startswith('docs/') and name.endswith('.md'))
    return sorted(paths)


@pytest.mark.parametrize('path', current_public_copy_paths(), ids=lambda p: str(p.relative_to(ROOT)))
def test_current_readmes_and_bundled_guides_have_no_retired_service_copy(path):
    assert not public_copy_violations(path.read_text()), path.relative_to(ROOT)


@pytest.mark.parametrize('text', [
    'https://gridzen.ai/pricing/', '[Prices](/pricing/)', '[Legacy](/payments)',
    '[Legacy](https://gridzen.ai/console/payments?lang=en)',
    'Real payments remain disabled.', 'Real payments are disabled.',
    'cobro', 'cobros', '真实收费仍关闭', 'los cobros reales', 'El cobro real',
    'pagos reales desactivados', 'cobros reales deshabilitados',
    'No real payment authorization.', 'pagos reales deshabilitados',
    'no autoriza altas ni pagos reales', '提现', '不授权真实入驻或付款', '收款', '出款',
    'funding is the next step', '--event payout', '--event=payout', 'payout_account',
    'examples/payout.py', 'pagamentos reais desabilitados', 'thanh toán thực bị vô hiệu hóa',
    # The CEP exception must not hide unrelated claims within the same section.
    'Existing Mexico SPEI payment evidence. Real payments remain disabled.',
])
def test_public_copy_guard_detects_retired_wording(text):
    assert public_copy_violations(text)


@pytest.mark.parametrize('text', [
    'Existing Mexico SPEI payment evidence',
    'https://gridzen.ai/console/api/payment-evidence/mx/cep/capabilities',
    'skills/payout-policy-designer/SKILL.md',
    'Task, pricing boundaries and zero-cost integration examples',
    'not live identity verification; paid activation remains unavailable',
])
def test_public_copy_guard_preserves_evidence_identifiers_and_neutral_boundaries(text):
    assert not public_copy_violations(text)


@pytest.mark.parametrize('path', sorted((ROOT/'skills').glob('*/references/product.json')), ids=lambda p: str(p.relative_to(ROOT)))
def test_bundled_product_reference_prose_has_no_retired_service_copy(path):
    reference = json.loads(path.read_text())
    # Check prose only; API availability enums and input contracts are unchanged.
    for field in ('description', 'audience', 'boundary'):
        assert not public_copy_violations(reference.get(field, '')), (path, field)

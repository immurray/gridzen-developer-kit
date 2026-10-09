import json
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a': self.hrefs.append(dict(attrs).get('href'))

def test_packaged_shell_has_language_safe_product_and_skill_paths():
    shell = json.loads((ROOT / 'src/gridzen_developer/web/site-shell.json').read_text())
    assert set(shell['languages']) == {'en', 'es', 'zh'}
    for lang, row in shell['languages'].items():
        prefix = '' if lang == 'en' else '/' + lang
        nav = Links(); nav.feed(row['nav'])
        assert prefix + '/docs/' in nav.hrefs
        assert '/developers/?lang=' + lang in nav.hrefs
        assert not any('/skills/' in path for path in nav.hrefs)
        footer = Links(); footer.feed(row['footer'])
        assert prefix + '/skills/' in footer.hrefs
        assert prefix + '/contact/' in footer.hrefs
        assert '<i></i>GridZen' in row['nav']

def test_source_download_contains_same_fallback_shell():
    import zipfile
    expected = (ROOT / 'src/gridzen_developer/web/site-shell.json').read_bytes()
    with zipfile.ZipFile(ROOT / 'src/gridzen_developer/web/downloads/gridzen-developer-kit.zip') as archive:
        assert archive.read('gridzen-developer-kit/src/gridzen_developer/web/site-shell.json') == expected

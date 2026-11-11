from pathlib import Path
import hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parents[1]

def test_current_docs_have_no_payment_entry_or_retired_listing():
    docs=[*ROOT.glob('README*.md'),*ROOT.glob('docs/harness/*.md'),ROOT/'docs/atomic-tools.md',ROOT/'docs/mexico-identity-account.md']
    for p in docs:
        text=p.read_text()
        assert not re.search(r'\b(funding|checkout|prepaid)\b',text,re.I),p
        assert 'smithery.ai/servers/support-35ug/gridzen-verification' not in text,p
        assert '/help/payments/' not in text,p

def test_all_fourteen_downloadable_skills_keep_identity_and_boundary():
    root=ROOT/'src/gridzen_developer/web/downloads'
    checks=json.loads((root/'sha256.json').read_text())
    with zipfile.ZipFile(root/'gridzen-skills.zip') as archive:
        names=[n for n in archive.namelist() if n.endswith('/SKILL.md')]
        assert len(names)==14
        for name in names:
            text=archive.read(name).decode()
            identity=re.search(r'^name: ([a-z0-9-]+)$',text,re.M)
            assert identity and identity[1]==Path(name).parent.name
            assert text==(ROOT/name).read_text()
    for name,digest in checks.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
    with zipfile.ZipFile(root/'gridzen-developer-kit.zip') as archive:
        assert archive.read('gridzen-developer-kit/README.md')==(ROOT/'README.md').read_bytes()
        assert archive.read('gridzen-developer-kit/docs/atomic-tools.md')==(ROOT/'docs/atomic-tools.md').read_bytes()

def test_quickstart_is_onboarding_without_changing_api_enums():
    text=(ROOT/'src/gridzen_developer/web/quickstart.html').read_text()
    assert '--event onboarding' in text
    assert '"event":"onboarding"' in text
    assert '--event payout' not in text
    # Keep the legacy event compatible; it is not a new public payment offering.
    assert (ROOT/'skills/payout-policy-designer/SKILL.md').exists()

def test_source_download_markdown_links_are_resolvable():
    import posixpath
    with zipfile.ZipFile(ROOT/'src/gridzen_developer/web/downloads/gridzen-developer-kit.zip') as archive:
        names=set(archive.namelist())
        for name in names:
            if not name.endswith('.md'):continue
            for link in re.findall(r'\]\(([^ )]+)',archive.read(name).decode()):
                if link.startswith(('https:','http:','mailto:','#','/')):continue
                target=posixpath.normpath(posixpath.join(posixpath.dirname(name),link.split('#')[0]))
                assert target in names or any(n.startswith(target.rstrip('/')+'/') for n in names),(name,link)

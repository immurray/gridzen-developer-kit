"""Keep current distribution copy aligned with the installed Skill inventory."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
COUNTS = {
    word: count
    for words in (
        'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty',
        'cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete dieciocho diecinueve veinte',
    )
    for count, word in enumerate(words.split())
}
COUNTS.update({'三': 3, '六': 6, '十四': 14})
# Subgroup counts have explicit research/workflow qualifiers and do not match.
COUNT = re.compile(
    rf'\b(\d+|{"|".join(COUNTS)})\s+'
    r'(?:(?:bundled|individual|integration|developer|agent|installable|project)\s+)*skills?\b(?!\.sh|\s+de investigación/flujos)'
    r'|(十四|六|三|\d+)\s*个\s*(?:开发者\s*)?skills?\b(?!\.sh|\s+de investigación/flujos)',
    re.IGNORECASE,
)


def test_current_skill_counts():
    expected = len(list((ROOT / 'skills').glob('*/SKILL.md')))
    paths = [
        *ROOT.glob('README*.md'), ROOT / 'llms-install.md', ROOT / 'plugin.json',
        *(ROOT / 'docs/harness').glob('*.md'), ROOT / 'docs/activation.md',
        ROOT / 'clients/compatibility.json',
        ROOT / 'src/gridzen_developer/web/compatibility.json',
    ]
    for path in paths:
        text = path.read_text()
        if path.suffix == '.json':
            # Recorded test reasons describe past runs, not the current product.
            value = json.loads(text)
            text = json.dumps(value, ensure_ascii=False, default=str)
            if path.name == 'compatibility.json':
                text = '\n'.join(record['skill_path'] for record in value['clients'])
        for match in COUNT.finditer(text):
            token = (match.group(1) or match.group(2)).lower()
            count = int(token) if token.isdigit() else COUNTS[token]
            assert count == expected, (path.relative_to(ROOT), match.group(), expected)

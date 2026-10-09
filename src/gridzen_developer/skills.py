"""Discover installed Skill assets without auto-activating an assistant."""
from pathlib import Path
import sysconfig

def list_skills():
    installed = Path(sysconfig.get_path('data')) / 'share/gridzen-developer-kit/skills'
    source = Path(__file__).resolve().parents[2] / 'skills'
    root = installed if installed.is_dir() else source
    return [{'name':p.parent.name,'path':str(p.parent),'instructions':str(p)} for p in sorted(root.glob('*/SKILL.md'))]

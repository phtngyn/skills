#!/usr/bin/env python3
"""Check the installed catalog contract and reachable Markdown resources."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
UPSTREAM = ROOT / 'repos/pstack/pstack/skills'


def validate():
    errors = []
    actual = {p.parent.name for p in SKILLS.glob('*/SKILL.md')}
    if not UPSTREAM.is_dir():
        return ['Missing pinned Poteto source; run setup before collection validation.']
    expected = {p.parent.name for p in UPSTREAM.glob('*/SKILL.md')} - {'make-bot-ui'}
    expected |= {'design', 'effect'}
    if actual != expected:
        errors.append(f'Catalog mismatch: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
    for name in sorted(actual):
        folder = SKILLS / name
        text = (folder / 'SKILL.md').read_text()
        match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not match:
            errors.append(f'{name}: missing frontmatter')
            continue
        front = match[1]
        if not re.search(r'^name: ' + re.escape(name) + r'$', front, re.M):
            errors.append(f'{name}: name does not match its directory')
        if not re.search(r'^description: \S.+$', front, re.M):
            errors.append(f'{name}: missing description')
        if len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            errors.append(f'{name}: invalid skill name')
        if name not in {'design', 'effect'}:
            if re.search(r'^(?:paths|disable-model-invocation):', front, re.M):
                errors.append(f'{name}: unsupported host metadata')
            original = (UPSTREAM / name / 'SKILL.md').read_text()
            implicit = 'false' if 'disable-model-invocation: true' in original else 'true'
            policy = folder / 'agents/openai.yaml'
            if not policy.is_file() or not re.search(r'allow_implicit_invocation: ' + implicit + r'\b', policy.read_text()):
                errors.append(f'{name}: invocation policy differs from upstream')
        for resource in folder.rglob('*'):
            if 'node_modules' in resource.parts:
                continue
            if resource.is_symlink() and not resource.exists():
                errors.append(f'{resource.relative_to(ROOT)}: broken symlink')
        for document in folder.rglob('*.md'):
            if 'node_modules' in document.parts:
                continue
            content = document.read_text()
            for target in re.findall(r'\]\(([^)]+)\)', content):
                target = target.strip('<>')
                if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                # Examples and templates contain intentionally unresolved paths.
                if '<' in target or '>' in target:
                    continue
                path = unquote(target.split('#', 1)[0])
                path = re.sub(r':\d+(?:-\d+)?$', '', path)
                if path and not (document.parent / path).exists():
                    errors.append(f'{document.relative_to(ROOT)}: missing link {target}')
    return errors


if __name__ == '__main__':
    errors = validate()
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'{len(list(SKILLS.glob("*/SKILL.md")))} skills validated; catalog, policies, and linked resources resolve.')

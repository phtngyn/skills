#!/usr/bin/env python3
"""Check the catalog, documentation coverage, and local Markdown links."""
from html import unescape
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'make-bot-ui', 'typescript-best-practices', 'create-formal-verification-skill', 'maintain-formal-verification-skill'}
PERSONAL = {'design', 'effect'}
LINK = re.compile(r'''\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+(?:"[^"\n]*"|'[^'\n]*'))?\s*\)''')


def heading_anchors(content):
    anchors = set()
    fence = None
    for line in content.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = (marker[1][0], len(marker[1]))
            continue
        heading = re.match(r'^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$', line)
        if not heading:
            continue
        text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', heading[1])
        text = unescape(re.sub(r'<[^>]+>', '', text)).replace('`', '')
        slug = re.sub(r'[^\w\s-]', '', text.lower()).strip()
        slug = re.sub(r'\s', '-', slug)
        anchor = slug
        suffix = 0
        while anchor in anchors:
            suffix += 1
            anchor = f'{slug}-{suffix}'
        anchors.add(anchor)
    return anchors


def check_links(document, root):
    errors = []
    for match in LINK.finditer(document.read_text()):
        target = match[1] if match[1] is not None else match[2]
        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        # Examples and templates contain intentionally unresolved paths.
        if '<' in target or '>' in target:
            continue
        path, _, anchor = target.partition('#')
        path = re.sub(r':\d+(?:-\d+)?$', '', unquote(path))
        destination = document.parent / path if path else document
        label = document.relative_to(root)
        if not destination.exists():
            errors.append(f'{label}: missing link {target}')
        elif anchor and destination.is_file() and destination.suffix == '.md':
            if unquote(anchor) not in heading_anchors(destination.read_text()):
                errors.append(f'{label}: missing heading in link {target}')
    return errors


def check_catalog_docs(root, actual):
    errors = []
    readme = (root / 'README.md').read_text()
    listed = set(re.findall(r'^\| `([a-z0-9-]+)` \|', readme, re.M))
    listed |= {'principle-' + name for name in re.findall(r'^- `([a-z0-9-]+)`$', readme, re.M)}
    if listed != actual:
        errors.append(f'README.md: catalog coverage mismatch: missing={sorted(actual-listed)}, extra={sorted(listed-actual)}')
    counts = [
        (r'\b(\d+) skills\b(?! are principles\b)', len(actual), 'skills'),
        (r'\b(\d+) Poteto (?:core )?skill(?:s| directories)\b', len(actual - PERSONAL), 'Poteto skills'),
        (r'\b(\d+) (?:skills are )?principles\b', sum(name.startswith('principle-') for name in actual), 'principles'),
        (r'\b(\d+) playbooks\b', len(list((root / 'skills/poteto-mode/playbooks').glob('*.md'))), 'playbooks'),
    ]
    for document in root.glob('*.md'):
        content = document.read_text()
        for pattern, expected, category in counts:
            for match in re.finditer(pattern, content):
                if int(match[1]) != expected:
                    errors.append(f'{document.name}: claims {match[1]} {category}, found {expected}')
    return errors


def validate(root=ROOT):
    skills = root / 'skills'
    upstream = root / 'repos/pstack/pstack/skills'
    errors = []
    actual = {p.parent.name for p in skills.glob('*/SKILL.md')}
    if not upstream.is_dir():
        return ['Missing pinned Poteto source; run setup before collection validation.']
    expected = {p.parent.name for p in upstream.glob('*/SKILL.md')} - EXCLUDED
    expected |= PERSONAL
    if actual != expected:
        errors.append(f'Catalog mismatch: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
    for name in sorted(actual):
        folder = skills / name
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
        if name not in PERSONAL:
            if re.search(r'^(?:paths|disable-model-invocation):', front, re.M):
                errors.append(f'{name}: unsupported host metadata')
            if name not in expected:
                continue
            original = (upstream / name / 'SKILL.md').read_text()
            implicit = 'false' if 'disable-model-invocation: true' in original else 'true'
            policy = folder / 'agents/openai.yaml'
            if not policy.is_file() or not re.search(r'allow_implicit_invocation: ' + implicit + r'\b', policy.read_text()):
                errors.append(f'{name}: invocation policy differs from upstream')
        for resource in folder.rglob('*'):
            if 'node_modules' in resource.parts:
                continue
            if resource.is_symlink() and not resource.exists():
                errors.append(f'{resource.relative_to(root)}: broken symlink')
        for document in folder.rglob('*.md'):
            if 'node_modules' in document.parts:
                continue
            errors.extend(check_links(document, root))
    for document in root.glob('*.md'):
        errors.extend(check_links(document, root))
    errors.extend(check_catalog_docs(root, actual))
    return errors


if __name__ == '__main__':
    errors = validate()
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'{len(list((ROOT / "skills").glob("*/SKILL.md")))} skills validated; catalog, policies, documentation, and links resolve.')

#!/usr/bin/env python3
"""Check the catalog, documentation coverage, and local Markdown links."""
from html import unescape
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'make-bot-ui', 'typescript-best-practices'}
EMIL_SPEC = importlib.util.spec_from_file_location('port_emil', Path(__file__).with_name('port_emil.py'))
EMIL = importlib.util.module_from_spec(EMIL_SPEC)
EMIL_SPEC.loader.exec_module(EMIL)
DESIGN = EMIL.NAMES
PERSONAL = DESIGN | {'effect', 'full-send', 'full-stop'}
EXTERNAL = {'stageshow', 'deslop'}
LINK = re.compile(r'''\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+(?:"[^"\n]*"|'[^'\n]*'))?\s*\)''')

PORT_SPEC = importlib.util.spec_from_file_location('port_poteto', Path(__file__).with_name('port_poteto.py'))
PORT = importlib.util.module_from_spec(PORT_SPEC)
PORT_SPEC.loader.exec_module(PORT)


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


def check_links(document, root, forbidden_skills=()):
    errors = []
    for match in LINK.finditer(document.read_text()):
        target = match[1] if match[1] is not None else match[2]
        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        # Examples and templates contain intentionally unresolved paths.
        if '<' in target or '>' in target or (target == 'url' and document.name.endswith('-prompt.md')):
            continue
        path, _, anchor = target.partition('#')
        path = re.sub(r':\d+(?:-\d+)?$', '', unquote(path))
        destination = document.parent / path if path else document
        label = document.relative_to(root)
        try:
            linked_skill = destination.resolve().relative_to((root / 'skills').resolve()).parts[0]
        except (ValueError, IndexError):
            linked_skill = None
        if linked_skill in forbidden_skills:
            errors.append(f'{label}: Design family cannot depend on Poteto skill {linked_skill}')
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
        (r'\b(\d+) Poteto (?:core )?skill(?:s| directories)\b', len(actual - PERSONAL - EXTERNAL), 'Poteto skills'),
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
    poteto = {p.parent.name for p in upstream.glob('*/SKILL.md')} - EXCLUDED
    expected = poteto.copy()
    expected |= PERSONAL | EXTERNAL
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
        if name != 'effect':
            policy = folder / 'agents/openai.yaml'
            if not policy.is_file() or not re.search(r'allow_implicit_invocation: false\b', policy.read_text()):
                errors.append(f'{name}: only effect may allow implicit invocation')
        for resource in folder.rglob('*'):
            if 'node_modules' in resource.parts:
                continue
            if resource.is_symlink() and not resource.exists():
                errors.append(f'{resource.relative_to(root)}: broken symlink')
        for document in folder.rglob('*.md'):
            if 'node_modules' in document.parts:
                continue
            source = upstream / name / document.relative_to(folder) if name in poteto else root / 'repos/emil/skills' / name / document.relative_to(folder)
            if not source.is_file() or source.read_bytes() != document.read_bytes():
                errors.extend(check_links(document, root))
    for document in root.glob('*.md'):
        errors.extend(check_links(document, root))
    errors.extend(check_catalog_docs(root, actual))
    for relative, payload in PORT.expected_files(root).items():
        installed = skills / relative
        if not installed.is_file() or installed.read_bytes() != payload:
            errors.append(f'Poteto source drift: {relative}; regenerate with scripts/port_poteto.py')
    if (root / 'repos/emil/skills').is_dir():
        for relative, payload in EMIL.expected_files(root).items():
            installed = skills / relative
            if not installed.is_file() or installed.read_bytes() != payload:
                errors.append(f'Emil source drift: {relative}; regenerate with scripts/port_emil.py')
    if (root / 'repos/pstack/.git').exists() and 'deslop' in actual:
        source = subprocess.check_output([
            'git', '-C', str(root / 'repos/pstack'),
            'show', 'HEAD:cursor-team-kit/skills/deslop/SKILL.md',
        ])
        if (skills / 'deslop/SKILL.md').read_bytes() != source:
            errors.append('Cursor Team Kit source drift: deslop/SKILL.md')
    stageshow = root / 'repos/benjitaylor/stageshow'
    if stageshow.is_dir():
        for source in stageshow.rglob('*'):
            if not source.is_file() or 'node_modules' in source.parts:
                continue
            installed = skills / 'stageshow' / source.relative_to(stageshow)
            if not installed.is_file() or installed.read_bytes() != source.read_bytes():
                errors.append(f'Stageshow source drift: {source.relative_to(stageshow)}')
    for relative in PORT.REMOVED:
        if (skills / relative).exists():
            errors.append(f'Redundant port manual: {relative}')
    return errors


if __name__ == '__main__':
    errors = validate()
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'{len(list((ROOT / "skills").glob("*/SKILL.md")))} skills validated; catalog, policies, documentation, and links resolve.')

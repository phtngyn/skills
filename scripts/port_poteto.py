#!/usr/bin/env python3
"""Copy retained Poteto skills byte for byte from the pinned source."""
from pathlib import Path
import argparse
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'make-bot-ui', 'typescript-best-practices'}
REMOVED = ('poteto-mode/references/codex.md', 'no-comments/references/comment-reviewer.md')


def expected_files(root=ROOT):
    source = root / 'repos/pstack/pstack/skills'
    files = {}
    for folder in sorted(source.iterdir()):
        if folder.name in EXCLUDED or not (folder / 'SKILL.md').is_file():
            continue
        for path in folder.rglob('*'):
            if not path.is_file() or 'node_modules' in path.parts:
                continue
            relative = path.relative_to(source).as_posix()
            payload = path.read_bytes()
            files[relative] = payload
        files[f'{folder.name}/agents/openai.yaml'] = b'policy:\n  allow_implicit_invocation: false\n'
    return files


def obsolete_files(root, files):
    managed = {Path(relative).parts[0] for relative in files}
    tracked = subprocess.check_output(
        ['git', '-C', str(root), 'ls-files', '-z', '--', 'skills/'], text=True,
    ).split('\0')
    return [
        Path(path).relative_to('skills').as_posix()
        for path in tracked if path
        and Path(path).parts[1] in managed
        and Path(path).relative_to('skills').as_posix() not in files
        and (root / path).is_file()
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report drift without writing.')
    args = parser.parse_args()
    pin_row = next(row for row in (ROOT / 'UPSTREAM.md').read_text().splitlines() if row.startswith('| Poteto |'))
    pin = re.findall(r'`([0-9a-f]{40})`', pin_row)[-1]
    revision = subprocess.check_output(['git', '-C', str(ROOT / 'repos/pstack'), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != pin:
        parser.error(f'Poteto checkout is at {revision}, expected {pin}')
    dirty = subprocess.check_output(['git', '-C', str(ROOT / 'repos/pstack'), 'status', '--porcelain'], text=True).strip()
    if dirty:
        parser.error('Poteto source has local changes; preserve or resolve them before regeneration.')
    files = expected_files()
    changed = []
    for relative, payload in files.items():
        destination = ROOT / 'skills' / relative
        if destination.is_symlink() or not destination.exists() or destination.read_bytes() != payload:
            changed.append(relative)
            if not args.check:
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.is_symlink():
                    destination.unlink()
                destination.write_bytes(payload)
                original = ROOT / 'repos/pstack/pstack/skills' / relative
                if original.exists():
                    destination.chmod(original.stat().st_mode & 0o777)
    for relative in set(REMOVED) | set(obsolete_files(ROOT, files)):
        destination = ROOT / 'skills' / relative
        if destination.exists():
            changed.append(relative + ' (remove)')
            if not args.check:
                destination.unlink()
    if args.check and changed:
        print('Poteto port drift:\n' + '\n'.join(changed), file=sys.stderr)
        return 1
    print(f'{len(files)} upstream-derived files {"match" if args.check else "generated"}; {len(changed)} changes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Generate the retained Poteto skills with the Codex port applied."""
from pathlib import Path
import argparse
import os
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'make-bot-ui', 'typescript-best-practices'}
REMOVED = ('no-comments/references/comment-reviewer.md',)


def apply_codex_port(files, patch):
    """Apply the maintained patch in isolation before touching installed files."""
    with tempfile.TemporaryDirectory(prefix='poteto-port-') as temporary:
        tree = Path(temporary)
        for relative, payload in files.items():
            path = tree / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        env = os.environ.copy()
        for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE', 'GIT_PREFIX'):
            env.pop(key, None)
        env['GIT_CEILING_DIRECTORIES'] = str(tree.parent.resolve())
        result = subprocess.run(
            ['git', '-C', str(tree), 'apply', '--unidiff-zero', '--whitespace=nowarn', str(patch.resolve())],
            capture_output=True, text=True, env=env,
        )
        if result.returncode:
            raise ValueError(f'Codex port does not apply to the Poteto source:\n{result.stderr.strip()}')
        return {
            path.relative_to(tree).as_posix(): path.read_bytes()
            for path in sorted(tree.rglob('*')) if path.is_file()
        }


def expected_files(root=ROOT):
    patch = root / 'scripts/poteto-codex.patch'
    if not patch.is_file():
        raise ValueError(f'Missing Codex port patch: {patch}')

    source = root / 'repos/pstack/pstack/skills'
    files = {}
    for folder in sorted(source.iterdir()):
        if folder.name in EXCLUDED or not (folder / 'SKILL.md').is_file():
            continue
        for path in folder.rglob('*'):
            if not path.is_file() or 'node_modules' in path.parts:
                continue
            files[path.relative_to(source).as_posix()] = path.read_bytes()
        files[f'{folder.name}/agents/openai.yaml'] = b'policy:\n  allow_implicit_invocation: false\n'
    return apply_codex_port(files, patch)


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
    try:
        files = expected_files()
    except ValueError as error:
        parser.error(str(error))
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
